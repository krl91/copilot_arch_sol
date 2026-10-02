"""Convertit une présentation PowerPoint (.pptx) en markdown : une section par diapositive.

Usage : python outils/pptx2md.py "fichier.pptx" [--out DOSSIER] [--sans-notes] [--masquees]
Bibliothèque standard uniquement (aucune installation). Lecture seule.

- "## Slide N – Titre" pour chaque diapositive (permet de citer : DOC fichier.pptx slide N).
- Texte des zones dans l'ordre de lecture (haut → bas, gauche → droite), puces avec niveaux.
- Tableaux convertis en tableaux markdown ; groupes de formes parcourus.
- Notes du présentateur incluses (souvent la vraie information) sauf --sans-notes.
- Diapositives masquées ignorées sauf --masquees. Images/graphiques : signalés [image] / [graphique].
"""
import argparse
import posixpath
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _commun import chemin_sortie, entete, nettoyer, tableau_md  # noqa: E402

A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
PKG_REL = "{http://schemas.openxmlformats.org/package/2006/relationships}"
C_CHART = "http://schemas.openxmlformats.org/drawingml/2006/chart"
TITRES = ("title", "ctrTitle")
IGNORES = ("sldNum", "dt", "ftr", "hdr")


def _xml(z, nom):
    try:
        return ET.fromstring(z.read(nom))
    except KeyError:
        return None


def _rels(z, partie):
    dossier, nom = posixpath.split(partie)
    root = _xml(z, posixpath.join(dossier, "_rels", nom + ".rels"))
    if root is None:
        return {}
    res = {}
    for r in root.iter(PKG_REL + "Relationship"):
        cible = r.get("Target")
        if r.get("TargetMode") != "External":
            cible = posixpath.normpath(posixpath.join(dossier, cible))
        res[r.get("Id")] = (r.get("Type", "").rsplit("/", 1)[-1], cible)
    return res


def _texte_para(p):
    morceaux = []
    for el in p:
        if el.tag in (A + "r", A + "fld"):
            t = el.find(A + "t")
            txt = t.text if t is not None and t.text else ""
            rpr = el.find(A + "rPr")
            if txt.strip() and rpr is not None and rpr.get("b") == "1":
                txt = f"**{txt.strip()}** " if txt.endswith(" ") else f"**{txt.strip()}**"
            morceaux.append(txt)
        elif el.tag == A + "br":
            morceaux.append("<br>")
    return re.sub(r"\*\*\s*\*\*", "", "".join(morceaux)).strip()


def _paragraphes(tx_body, puces=True):
    lignes = []
    for p in tx_body.findall(A + "p"):
        txt = _texte_para(p)
        if not txt:
            continue
        ppr = p.find(A + "pPr")
        lvl = int(ppr.get("lvl", "0")) if ppr is not None else 0
        sans_puce = ppr is not None and ppr.find(A + "buNone") is not None
        if puces and not sans_puce:
            lignes.append("    " * lvl + "- " + txt)
        else:
            lignes.append(txt)
    return lignes


def _position(forme):
    off = forme.find(f".//{A}off")
    if off is None:
        return (10**12, 10**12)
    return (int(off.get("y", 0)), int(off.get("x", 0)))


def _placeholder(forme):
    ph = forme.find(f"{P}nvSpPr/{P}nvPr/{P}ph")
    return None if ph is None else ph.get("type", "body")


def _formes(conteneur, titre, blocs):
    """Parcourt les formes d'un spTree/grpSp dans l'ordre de lecture."""
    enfants = [e for e in conteneur if e.tag in (P + "sp", P + "grpSp", P + "graphicFrame", P + "pic")]
    for f in sorted(enfants, key=_position):
        if f.tag == P + "grpSp":
            _formes(f, titre, blocs)
        elif f.tag == P + "pic":
            blocs.append("[image]")
        elif f.tag == P + "graphicFrame":
            tbl = f.find(f".//{A}tbl")
            if tbl is not None:
                lignes = []
                for tr in tbl.findall(A + "tr"):
                    lignes.append(["<br>".join(_paragraphes(tc.find(A + "txBody"), puces=False))
                                   if tc.find(A + "txBody") is not None else ""
                                   for tc in tr.findall(A + "tc")])
                if lignes:
                    blocs.append(tableau_md(lignes))
            elif f.find(f".//{A}graphicData[@uri='{C_CHART}']") is not None:
                blocs.append("[graphique]")
            else:
                blocs.append("[objet]")
        else:  # p:sp
            ph = _placeholder(f)
            if ph in IGNORES:
                continue
            tx = f.find(P + "txBody")
            if tx is None:
                continue
            if ph in TITRES and not titre:
                titre.append(" ".join(_paragraphes(tx, puces=False)))
                continue
            lignes = _paragraphes(tx, puces=(ph is not None and ph not in TITRES and ph != "subTitle"))
            if lignes:
                blocs.append("\n".join(lignes))


def _notes(z, rels):
    for typ, cible in rels.values():
        if typ == "notesSlide":
            root = _xml(z, cible)
            if root is None:
                return ""
            textes = []
            for sp in root.iter(P + "sp"):
                if _placeholder(sp) == "body" and sp.find(P + "txBody") is not None:
                    textes += _paragraphes(sp.find(P + "txBody"), puces=False)
            return "\n".join(textes)
    return ""


def convertir_pptx(source: Path, notes=True, masquees=False):
    parties, nb_masquees = [], 0
    with zipfile.ZipFile(source) as z:
        pres = _xml(z, "ppt/presentation.xml")
        if pres is None:
            raise ValueError("ppt/presentation.xml introuvable : fichier .pptx invalide ?")
        rels_pres = _rels(z, "ppt/presentation.xml")
        lst = pres.find(P + "sldIdLst")
        ids = lst.findall(P + "sldId") if lst is not None else []
        for n, sid in enumerate(ids, 1):
            chemin = rels_pres[sid.get(R + "id")][1]
            slide = _xml(z, chemin)
            masquee = slide.get("show") == "0"
            if masquee and not masquees:
                nb_masquees += 1
                continue
            titre, blocs = [], []
            _formes(slide.find(f"{P}cSld/{P}spTree"), titre, blocs)
            entete_slide = f"## Slide {n}" + (f" – {titre[0]}" if titre and titre[0] else "")
            if masquee:
                entete_slide += " (masquée)"
            corps = "\n\n".join(blocs) if blocs else "*(pas de texte)*"
            bloc = f"{entete_slide}\n\n{corps}"
            if notes:
                txt = _notes(z, _rels(z, chemin))
                if txt:
                    bloc += "\n\n> **Notes :**\n" + "\n".join("> " + l for l in txt.splitlines())
            parties.append(bloc)
    meta = {"slides_total": len(ids), "slides_masquees_ignorees": nb_masquees}
    return meta, "\n\n---\n\n".join(parties)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("fichier")
    ap.add_argument("--out", help="dossier de sortie (défaut : '0 Inbox/Converted' du vault)")
    ap.add_argument("--sans-notes", action="store_true", help="ne pas inclure les notes du présentateur")
    ap.add_argument("--masquees", action="store_true", help="inclure les diapositives masquées")
    a = ap.parse_args(argv)
    src = Path(a.fichier)
    if src.suffix.lower() not in (".pptx", ".pptm"):
        sys.exit(f"Format non pris en charge : {src.suffix}. Ouvre-le dans PowerPoint et enregistre-le en .pptx.")
    meta, corps = convertir_pptx(src, not a.sans_notes, a.masquees)
    md = entete(src, "pptx2md", meta) + "\n" + corps
    dest = chemin_sortie(src, a.out)
    dest.write_text(nettoyer(md), encoding="utf-8")
    print(f"OK  {src.name}  →  {dest}")
    return dest


if __name__ == "__main__":
    main()
