"""Convertit un document Word (.docx) en markdown.

Usage : python outils/docx2md.py "fichier.docx" [--out DOSSIER]
Bibliothèque standard uniquement (aucune installation). Lecture seule du .docx.

Conserve : titres (Titre 1..6 / Heading 1..6), listes à puces et numérotées (avec niveaux),
gras/italique, liens, tableaux (cellules fusionnées horizontalement), sauts de ligne.
Modifications suivies : le texte inséré est gardé, le texte supprimé est ignoré.
Ignore : images (remplacées par [image]), en-têtes/pieds de page, commentaires, notes de bas de page.
"""
import argparse
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _commun import chemin_sortie, entete, nettoyer, tableau_md  # noqa: E402

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
PKG_REL = "{http://schemas.openxmlformats.org/package/2006/relationships}"


def _lire_xml(z, nom):
    try:
        return ET.fromstring(z.read(nom))
    except KeyError:
        return None


def _styles(z):
    """→ (styleId → niveau de titre (0 = Title, 1..6 = Heading n),
          styleId → (numId, ilvl) ou ("puce"/"num", ilvl) pour les styles de liste)."""
    niveaux, listes = {}, {}
    root = _lire_xml(z, "word/styles.xml")
    if root is None:
        return niveaux, listes
    for st in root.iter(W + "style"):
        sid = st.get(W + "styleId", "")
        name_el = st.find(W + "name")
        name = (name_el.get(W + "val") if name_el is not None else sid).lower()
        # Styles de liste : numérotation portée par le style (cas des modèles d'entreprise)
        npr = st.find(f"{W}pPr/{W}numPr")
        if npr is not None:
            nid, ilvl = npr.find(W + "numId"), npr.find(W + "ilvl")
            if nid is not None:
                listes[sid] = (nid.get(W + "val"), ilvl.get(W + "val") if ilvl is not None else "0")
        elif re.search(r"list bullet|liste à puces", name):
            listes[sid] = ("puce", "0")
        elif re.search(r"list number|liste num", name):
            listes[sid] = ("num", "0")
        m = re.match(r"^(heading|titre)\s*(\d)$", name) or re.match(r"^(heading|titre)(\d)$", sid.lower())
        if m:
            niveaux[sid] = int(m.group(2))
        elif name in ("title", "titre"):
            niveaux[sid] = 0
        else:
            # niveau de plan explicite (outlineLvl) dans le style
            ol = st.find(f"{W}pPr/{W}outlineLvl")
            if ol is not None and ol.get(W + "val", "9").isdigit() and int(ol.get(W + "val")) < 6:
                niveaux[sid] = int(ol.get(W + "val")) + 1
    return niveaux, listes


def _numerotation(z):
    """(numId, ilvl) → True si liste numérotée, False si puces."""
    root = _lire_xml(z, "word/numbering.xml")
    res = {}
    if root is None:
        return res
    abstraits = {}
    for an in root.iter(W + "abstractNum"):
        aid = an.get(W + "abstractNumId")
        for lvl in an.iter(W + "lvl"):
            fmt = lvl.find(W + "numFmt")
            val = fmt.get(W + "val") if fmt is not None else "bullet"
            abstraits[(aid, lvl.get(W + "ilvl"))] = val not in ("bullet", "none")
    for num in root.iter(W + "num"):
        nid = num.get(W + "numId")
        ref = num.find(W + "abstractNumId")
        if ref is None:
            continue
        aid = ref.get(W + "val")
        for (a, ilvl), ordonne in abstraits.items():
            if a == aid:
                res[(nid, ilvl)] = ordonne
    return res


def _liens(z):
    root = _lire_xml(z, "word/_rels/document.xml.rels")
    if root is None:
        return {}
    return {r.get("Id"): r.get("Target") for r in root.iter(PKG_REL + "Relationship")
            if r.get("TargetMode") == "External"}


def _actif(el, tag):
    """Propriété booléenne de run (w:b, w:i) active ?"""
    e = el.find(tag)
    return e is not None and e.get(W + "val", "true") not in ("0", "false", "off")


def _texte_runs(parent, liens):
    morceaux = []
    for el in parent:
        if el.tag == W + "r":
            rpr = el.find(W + "rPr")
            gras = rpr is not None and _actif(rpr, W + "b")
            ital = rpr is not None and _actif(rpr, W + "i")
            txt = ""
            for c in el:
                if c.tag == W + "t":
                    txt += c.text or ""
                elif c.tag == W + "tab":
                    txt += " "
                elif c.tag in (W + "br", W + "cr"):
                    txt += "<br>"
                elif c.tag == W + "drawing" or c.tag == W + "pict":
                    txt += "[image]"
            if txt.strip():
                debut, fin = len(txt) - len(txt.lstrip()), len(txt.rstrip())
                coeur = txt[debut:fin]
                if gras and ital:
                    coeur = f"***{coeur}***"
                elif gras:
                    coeur = f"**{coeur}**"
                elif ital:
                    coeur = f"*{coeur}*"
                txt = txt[:debut] + coeur + txt[fin:]
            morceaux.append(txt)
        elif el.tag == W + "hyperlink":
            txt = _texte_runs(el, liens)
            cible = liens.get(el.get(R + "id"))
            morceaux.append(f"[{txt}]({cible})" if cible and txt.strip() else txt)
        elif el.tag in (W + "ins", W + "smartTag", W + "sdt", W + "sdtContent", W + "fldSimple"):
            morceaux.append(_texte_runs(el, liens))
        # w:del (texte supprimé), w:commentRangeStart, etc. : ignorés
    return re.sub(r"\*\*\s*\*\*", "", "".join(morceaux))


def _paragraphe(p, ctx):
    texte = _texte_runs(p, ctx["liens"]).strip()
    if not texte:
        return ""
    ppr = p.find(W + "pPr")
    style = None
    num = None
    if ppr is not None:
        ps = ppr.find(W + "pStyle")
        style = ps.get(W + "val") if ps is not None else None
        npr = ppr.find(W + "numPr")
        if npr is not None:
            nid = npr.find(W + "numId")
            ilvl = npr.find(W + "ilvl")
            nid = nid.get(W + "val") if nid is not None else None
            ilvl = ilvl.get(W + "val") if ilvl is not None else "0"
            if nid and nid != "0":
                num = (nid, ilvl)
        ol = ppr.find(W + "outlineLvl")
    if num is None and style in ctx["listes"]:
        num = ctx["listes"][style]
    niveau = ctx["styles"].get(style) if style else None
    if niveau is None and ppr is not None and ol is not None and ol.get(W + "val", "9").isdigit():
        v = int(ol.get(W + "val"))
        niveau = v + 1 if v < 6 else None
    if niveau is not None:
        texte = re.sub(r"^\*+|\*+$", "", texte)  # pas de gras dans un titre
        return "#" * max(1, niveau) + " " + texte
    if not num:
        # Puces tapées à la main ("• texte", "◦ texte") dans les documents mal stylés
        m = re.match(r"^([•◦▪▫‣●○■□➢►✓])\s*(.+)$", texte)
        if m:
            return ("    " if m.group(1) in "◦○▫□" else "") + "- " + m.group(2)
    if num:
        indent = "    " * int(num[1])
        if num[0] in ("puce", "num"):
            ordonne = num[0] == "num"
        else:
            ordonne = ctx["num"].get(num, False)
        puce = "1." if ordonne else "-"
        return f"{indent}{puce} {texte}"
    return texte


def _tableau(tbl, ctx):
    lignes = []
    for tr in tbl.findall(W + "tr"):
        ligne = []
        for tc in tr.findall(W + "tc"):
            paras = []
            for el in tc:
                if el.tag == W + "p":
                    t = _paragraphe(el, ctx)
                    if t:
                        paras.append(re.sub(r"^#+\s|^\s*(-|1\.)\s", "", t))
                elif el.tag == W + "tbl":
                    paras.append("[tableau imbriqué]")
            ligne.append("<br>".join(paras))
            span = tc.find(f"{W}tcPr/{W}gridSpan")
            if span is not None:
                ligne += [""] * (int(span.get(W + "val", "1")) - 1)
        lignes.append(ligne)
    md = tableau_md(lignes)
    return md.replace("\\<br>", "<br>")


def _bloc(el, ctx, sortie):
    if el.tag == W + "p":
        t = _paragraphe(el, ctx)
        if t:
            sortie.append(t)
    elif el.tag == W + "tbl":
        sortie.append("\n" + _tableau(el, ctx) + "\n")
    elif el.tag in (W + "sdt", W + "sdtContent", W + "customXml"):
        for c in el:
            _bloc(c, ctx, sortie)


def convertir_docx(source: Path) -> str:
    with zipfile.ZipFile(source) as z:
        doc = _lire_xml(z, "word/document.xml")
        if doc is None:
            raise ValueError("word/document.xml introuvable : fichier .docx invalide ?")
        niveaux, listes = _styles(z)
        ctx = {"styles": niveaux, "listes": listes, "num": _numerotation(z), "liens": _liens(z)}
    corps = doc.find(W + "body")
    sortie = []
    for el in corps:
        _bloc(el, ctx, sortie)
    # Lignes vides entre blocs, sauf entre éléments de liste consécutifs
    md = []
    for i, ligne in enumerate(sortie):
        est_liste = re.match(r"^\s*(-|1\.)\s", ligne)
        prec_liste = i > 0 and re.match(r"^\s*(-|1\.)\s", sortie[i - 1])
        meme_type = est_liste and prec_liste and (
            est_liste.group(1) == prec_liste.group(1) or ligne.startswith(" ") or sortie[i - 1].startswith(" "))
        if md and not meme_type:
            md.append("")
        md.append(ligne)
    return "\n".join(md)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("fichier")
    ap.add_argument("--out", help="dossier de sortie (défaut : '0 Inbox/Converted' du vault)")
    a = ap.parse_args(argv)
    src = Path(a.fichier)
    if src.suffix.lower() != ".docx":
        sys.exit(f"Format non pris en charge : {src.suffix}. Ouvre-le dans Word et enregistre-le en .docx.")
    md = entete(src, "docx2md") + "\n" + convertir_docx(src)
    dest = chemin_sortie(src, a.out)
    dest.write_text(nettoyer(md), encoding="utf-8")
    print(f"OK  {src.name}  →  {dest}")
    return dest


if __name__ == "__main__":
    main()
