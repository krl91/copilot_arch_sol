"""Convertit un classeur Excel (.xlsx / .xlsm) en markdown : un tableau par onglet.

Usage : python outils/xlsx2md.py "fichier.xlsx" [--out DOSSIER] [--onglet NOM ...]
                                  [--max-lignes 500] [--masques]
Bibliothèque standard uniquement (aucune installation). Lecture seule du classeur.

- Valeurs affichées = dernières valeurs calculées (les formules ne sont pas recalculées).
- Dates converties en AAAA-MM-JJ (formats de date Excel détectés).
- Lignes et colonnes entièrement vides supprimées ; 1re ligne non vide = en-tête.
- Onglets masqués ignorés sauf --masques. Au-delà de --max-lignes, le tableau est tronqué
  (et signalé) pour garder un fichier exploitable par Copilot.
"""
import argparse
import datetime as dt
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path, PurePosixPath

sys.path.insert(0, str(Path(__file__).parent))
from _commun import chemin_sortie, entete, nettoyer, tableau_md  # noqa: E402

S = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
PKG_REL = "{http://schemas.openxmlformats.org/package/2006/relationships}"
# Identifiants de formats de nombre Excel prédéfinis correspondant à des dates/heures
# (norme ECMA-376, partie 1, §18.8.30) : 14-22 et 45-47.
FORMATS_DATE_NATIFS = set(range(14, 23)) | {45, 46, 47}
# 500 lignes ≈ 30-60 k caractères de markdown : reste lisible par Copilot dans une seule requête.
# Au-delà, le tableau est tronqué (et signalé) ; --max-lignes permet d'aller plus loin.
MAX_LIGNES_DEFAUT = 500


def _xml(z, nom):
    try:
        return ET.fromstring(z.read(nom))
    except KeyError:
        return None


def _texte_si(si):
    """Texte d'une chaîne partagée (simple ou enrichie)."""
    return "".join(t.text or "" for t in si.iter(S + "t"))


def _styles_date(z):
    """Liste : index de style de cellule → True si format de date."""
    root = _xml(z, "xl/styles.xml")
    if root is None:
        return []
    perso = {}
    nf = root.find(S + "numFmts")
    if nf is not None:
        for f in nf.findall(S + "numFmt"):
            code = re.sub(r'"[^"]*"|\[[^\]]*\]|\\.', "", f.get("formatCode", "").lower())
            perso[int(f.get("numFmtId"))] = bool(re.search(r"[dy]", code)) or (
                "m" in code and not re.search(r"h|s", code))
    xfs = root.find(S + "cellXfs")
    res = []
    if xfs is not None:
        for xf in xfs.findall(S + "xf"):
            fid = int(xf.get("numFmtId", "0"))
            res.append(fid in FORMATS_DATE_NATIFS or perso.get(fid, False))
    return res


def _col_index(ref):
    lettres = re.match(r"[A-Z]+", ref).group(0)
    n = 0
    for c in lettres:
        n = n * 26 + (ord(c) - 64)
    return n - 1


def _serial_date(v, base1904):
    base = dt.datetime(1904, 1, 1) if base1904 else dt.datetime(1899, 12, 30)
    d = base + dt.timedelta(seconds=round(float(v) * 86400))  # arrondi à la seconde
    return d.strftime("%Y-%m-%d") if d.time() == dt.time(0) else d.strftime("%Y-%m-%d %H:%M")


def _nombre(v):
    try:
        f = float(v)
    except ValueError:
        return v
    if f.is_integer() and abs(f) < 1e15:
        return str(int(f))
    return f"{f:.10g}"


def lire_classeur(source: Path, onglets=None, masques=False):
    """→ liste de (nom_onglet, état, lignes[list[str]])"""
    with zipfile.ZipFile(source) as z:
        wb = _xml(z, "xl/workbook.xml")
        pr = wb.find(S + "workbookPr")
        base1904 = pr is not None and pr.get("date1904") in ("1", "true")
        rels = {r.get("Id"): r.get("Target") for r in _xml(z, "xl/_rels/workbook.xml.rels").iter(PKG_REL + "Relationship")}
        sst_root = _xml(z, "xl/sharedStrings.xml")
        partagees = [_texte_si(si) for si in sst_root.findall(S + "si")] if sst_root is not None else []
        dates = _styles_date(z)
        resultat = []
        for sh in wb.find(S + "sheets").findall(S + "sheet"):
            nom, etat = sh.get("name"), sh.get("state", "visible")
            if onglets and nom not in onglets:
                continue
            if etat != "visible" and not masques and not onglets:
                continue
            cible = rels[sh.get(R + "id")]
            chemin = str(PurePosixPath("xl") / cible) if not cible.startswith("/") else cible.lstrip("/")
            chemin = re.sub(r"[^/]+/\.\./", "", chemin)
            root = _xml(z, chemin)
            grille = {}
            for c in root.iter(S + "c"):
                ref, t = c.get("r"), c.get("t", "n")
                v = c.find(S + "v")
                if t == "inlineStr":
                    is_ = c.find(S + "is")
                    val = _texte_si(is_) if is_ is not None else ""
                elif v is None or v.text is None:
                    continue
                elif t == "s":
                    val = partagees[int(v.text)]
                elif t == "b":
                    val = "TRUE" if v.text == "1" else "FALSE"
                elif t in ("str", "e"):
                    val = v.text
                else:
                    s_idx = int(c.get("s", "0"))
                    est_date = s_idx < len(dates) and dates[s_idx]
                    val = _serial_date(v.text, base1904) if est_date else _nombre(v.text)
                if str(val).strip() == "":
                    continue
                ligne = int(re.search(r"\d+", ref).group(0))
                grille[(ligne, _col_index(ref))] = str(val)
            if not grille:
                resultat.append((nom, etat, []))
                continue
            lignes_idx = sorted({l for l, _ in grille})
            cols_idx = sorted({c for _, c in grille})
            lignes = [[grille.get((l, c), "") for c in cols_idx] for l in lignes_idx]
            resultat.append((nom, etat, lignes))
    return resultat


def convertir_xlsx(source: Path, onglets=None, max_lignes=MAX_LIGNES_DEFAUT, masques=False) -> str:
    parties = []
    for nom, etat, lignes in lire_classeur(source, onglets, masques):
        titre = f"## Onglet : {nom}" + (" (masqué)" if etat != "visible" else "")
        if not lignes:
            parties.append(f"{titre}\n\n*(onglet vide)*")
            continue
        info = f"*{len(lignes) - 1} ligne(s) de données × {len(lignes[0])} colonne(s)*"
        tronque = ""
        if len(lignes) - 1 > max_lignes:
            tronque = (f"\n\n> ⚠️ Tronqué : {max_lignes} premières lignes sur {len(lignes) - 1}. "
                       f"Relancer avec `--max-lignes {len(lignes)}` ou `--onglet \"{nom}\"` si besoin.")
            lignes = lignes[:max_lignes + 1]
        parties.append(f"{titre}\n\n{info}\n\n{tableau_md(lignes)}{tronque}")
    return "\n\n".join(parties)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("fichier")
    ap.add_argument("--out", help="dossier de sortie (défaut : '0 Inbox/Converted' du vault)")
    ap.add_argument("--onglet", nargs="*", help="ne convertir que ces onglets")
    ap.add_argument("--max-lignes", type=int, default=MAX_LIGNES_DEFAUT)
    ap.add_argument("--masques", action="store_true", help="inclure les onglets masqués")
    a = ap.parse_args(argv)
    src = Path(a.fichier)
    if src.suffix.lower() not in (".xlsx", ".xlsm"):
        sys.exit(f"Format non pris en charge : {src.suffix}. Ouvre-le dans Excel et enregistre-le en .xlsx.")
    md = entete(src, "xlsx2md") + "\n" + convertir_xlsx(src, a.onglet, a.max_lignes, a.masques)
    dest = chemin_sortie(src, a.out)
    dest.write_text(nettoyer(md), encoding="utf-8")
    print(f"OK  {src.name}  →  {dest}")
    return dest


if __name__ == "__main__":
    main()
