"""Convertit un PDF en markdown (texte page par page, tableaux en option).

Usage : python outils/pdf2md.py "fichier.pdf" [--out DOSSIER] [--pages 1-10] [--tableaux]
Requiert : pypdf            (pip install pypdf)          – obligatoire, 100 % Python
Optionnel : pdfplumber      (pip install pdfplumber)     – pour --tableaux
Lecture seule du PDF.

- Un titre "## Page N" par page : permet de citer précisément (DOC fichier.pdf p.N).
- PDF scanné (image sans texte) : signalé, aucune invention de contenu. Il faut un OCR
  (ex. ouvrir dans Word, ou demander le document source).
- La mise en page complexe (colonnes, en-têtes répétés) peut être imparfaite :
  toujours vérifier une valeur critique dans le PDF original.
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _commun import chemin_sortie, entete, nettoyer, tableau_md  # noqa: E402


def _plage(spec, n):
    if not spec:
        return list(range(n))
    pages = set()
    for part in spec.split(","):
        if "-" in part:
            a, b = part.split("-")
            pages.update(range(int(a) - 1, min(int(b), n)))
        else:
            pages.add(int(part) - 1)
    return sorted(p for p in pages if 0 <= p < n)


def _nettoyer_page(txt):
    txt = txt.replace("­", "")                       # traits d'union conditionnels
    txt = re.sub(r"(\w)-\n(\w)", r"\1\2", txt)              # mots coupés en fin de ligne
    txt = re.sub(r"[ \t]{2,}", " ", txt)
    return txt.strip()


def convertir_pdf(source: Path, pages=None, tableaux=False):
    try:
        from pypdf import PdfReader
    except ImportError:
        sys.exit("pypdf absent. Installe-le : pip install pypdf  (ou demande à ton support IT).")
    lecteur = PdfReader(str(source))
    if lecteur.is_encrypted:
        try:
            lecteur.decrypt("")
        except Exception:
            sys.exit("PDF protégé par mot de passe : impossible à convertir.")
    n = len(lecteur.pages)
    choix = _plage(pages, n)
    plumber = None
    if tableaux:
        try:
            import pdfplumber
            plumber = pdfplumber.open(str(source))
        except ImportError:
            print("⚠️ pdfplumber absent : tableaux non extraits (pip install pdfplumber).", file=sys.stderr)

    parties, vides = [], 0
    for i in choix:
        txt = _nettoyer_page(lecteur.pages[i].extract_text() or "")
        bloc = f"## Page {i + 1}\n\n"
        if not txt:
            vides += 1
            bloc += "*(aucun texte extractible : page image/scannée)*"
        else:
            bloc += txt
        if plumber is not None:
            for k, t in enumerate(plumber.pages[i].extract_tables() or [], 1):
                lignes = [[c or "" for c in row] for row in t if any(row)]
                if lignes:
                    bloc += f"\n\n**Tableau {k} (page {i + 1})**\n\n" + tableau_md(lignes)
        parties.append(bloc)
    if plumber is not None:
        plumber.close()

    meta = {"pages_total": n, "pages_converties": len(choix)}
    alerte = ""
    if choix and vides == len(choix):
        alerte = ("> ⚠️ **Aucun texte extrait : PDF probablement scanné.** Ce fichier ne contient "
                  "pas de texte exploitable sans OCR. Ne pas l'utiliser comme source.\n\n")
    elif vides:
        alerte = f"> ⚠️ {vides} page(s) sans texte extractible (images/scans).\n\n"
    return meta, alerte + "\n\n".join(parties)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("fichier")
    ap.add_argument("--out", help="dossier de sortie (défaut : '0 Inbox/Converted' du vault)")
    ap.add_argument("--pages", help="ex. 1-10 ou 1,3,5-7 (défaut : toutes)")
    ap.add_argument("--tableaux", action="store_true", help="extraire aussi les tableaux (pdfplumber)")
    a = ap.parse_args(argv)
    src = Path(a.fichier)
    if src.suffix.lower() != ".pdf":
        sys.exit(f"Format non pris en charge : {src.suffix}")
    meta, corps = convertir_pdf(src, a.pages, a.tableaux)
    md = entete(src, "pdf2md", meta) + "\n" + corps
    dest = chemin_sortie(src, a.out)
    dest.write_text(nettoyer(md), encoding="utf-8")
    print(f"OK  {src.name}  →  {dest}")
    return dest


if __name__ == "__main__":
    main()
