"""Convertit un ou plusieurs fichiers (ou dossiers) Word, Excel, PowerPoint, PDF en markdown.

Usage :
  python outils/convertir.py "fichier.docx" "classeur.xlsx" "slides.pptx" "doc.pdf"
  python outils/convertir.py "C:/chemin/dossier" -r          (récursif)
  python outils/convertir.py ... --out "1 Projects/X/Sources"

Formats : .docx, .xlsx, .xlsm, .pptx, .pptm, .pdf   (.doc/.xls/.ppt : réenregistrer au format récent)
Sortie par défaut : "0 Inbox/Converted/" du vault (jamais à côté du fichier source).
Lecture seule des fichiers sources. Aucune connexion réseau.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import docx2md  # noqa: E402
import pdf2md  # noqa: E402
import pptx2md  # noqa: E402
import xlsx2md  # noqa: E402

CONVERTISSEURS = {".docx": docx2md, ".xlsx": xlsx2md, ".xlsm": xlsx2md,
                  ".pptx": pptx2md, ".pptm": pptx2md, ".pdf": pdf2md}
ANCIENS = {".doc": ".docx", ".xls": ".xlsx", ".ppt": ".pptx"}


def _fichiers(chemins, recursif):
    for c in map(Path, chemins):
        if c.is_dir():
            motif = "**/*" if recursif else "*"
            yield from sorted(p for p in c.glob(motif) if p.is_file())
        else:
            yield c


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("chemins", nargs="+")
    ap.add_argument("-r", "--recursif", action="store_true")
    ap.add_argument("--out", help="dossier de sortie")
    ap.add_argument("--tableaux", action="store_true", help="PDF : extraire les tableaux (pdfplumber)")
    a = ap.parse_args()

    ok, ko, ignores = 0, [], []
    for f in _fichiers(a.chemins, a.recursif):
        ext = f.suffix.lower()
        if f.name.startswith("~$"):           # fichiers verrou Office
            continue
        if ext not in CONVERTISSEURS:
            if ext in ANCIENS:
                ignores.append(f"{f.name} → réenregistrer en {ANCIENS[ext]}")
            continue
        args = [str(f)] + (["--out", a.out] if a.out else [])
        if ext == ".pdf" and a.tableaux:
            args.append("--tableaux")
        try:
            CONVERTISSEURS[ext].main(args)
            ok += 1
        except SystemExit as e:
            ko.append(f"{f.name} : {e}")
        except Exception as e:  # fichier corrompu, format inattendu…
            ko.append(f"{f.name} : {type(e).__name__} – {e}")

    print(f"\n{ok} fichier(s) converti(s).")
    for m in ignores:
        print(f"IGNORÉ  {m}")
    for m in ko:
        print(f"ÉCHEC   {m}")
    sys.exit(1 if ko else 0)


if __name__ == "__main__":
    main()
