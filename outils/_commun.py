"""Fonctions communes aux convertisseurs (docx2md, xlsx2md, pptx2md, pdf2md, convertir)."""
import datetime as _dt
import os
import re
from pathlib import Path

VERSION = "1.0"


def dossier_sortie_defaut():
    """Dossier de sortie par défaut, relatif au dossier courant (= racine du vault dans VS Code).

    On n'écrit JAMAIS à côté du fichier source : il est souvent dans un dossier
    SharePoint/OneDrive synchronisé et partagé.
    """
    inbox = Path("0 Inbox")
    return inbox / "Converted" if inbox.is_dir() else Path("converted")


def chemin_sortie(source: Path, out_dir):
    out = Path(out_dir) if out_dir else dossier_sortie_defaut()
    out.mkdir(parents=True, exist_ok=True)
    return out / (source.stem + ".md")


def entete(source: Path, convertisseur: str, extra: dict = None):
    """Front matter YAML + rappel de la convention de sources."""
    mtime = _dt.date.fromtimestamp(os.path.getmtime(source)).isoformat()
    today = _dt.date.today().isoformat()
    lignes = [
        "---",
        "type: converted",
        f'source_file: "{source.name}"',
        f'source_path: "{source.resolve().as_posix()}"',
        f"source_modified: {mtime}",
        f"converted: {today}",
        f"converter: {convertisseur} v{VERSION}",
    ]
    for k, v in (extra or {}).items():
        lignes.append(f"{k}: {v}")
    lignes += [
        "---",
        "",
        f"> Copie convertie automatiquement — le fichier original reste la référence.",
        f'> Citer comme : `[Sx] DOC {source.name} (§ / onglet / slide / page) ({mtime}) — "citation exacte"`',
        "",
    ]
    return "\n".join(lignes)


def cellule(texte):
    """Rend un texte sûr pour une cellule de tableau markdown."""
    if texte is None:
        return ""
    t = str(texte).replace("\\", "\\\\").replace("|", "\\|")
    t = re.sub(r"\r\n|\r|\n", "<br>", t)
    return t.strip()


def tableau_md(lignes):
    """Liste de lignes (listes de str) → tableau markdown. 1re ligne = en-tête."""
    if not lignes:
        return ""
    n = max(len(l) for l in lignes)
    lignes = [list(l) + [""] * (n - len(l)) for l in lignes]
    out = ["| " + " | ".join(cellule(c) for c in lignes[0]) + " |",
           "|" + "---|" * n]
    for l in lignes[1:]:
        out.append("| " + " | ".join(cellule(c) for c in l) + " |")
    return "\n".join(out)


def nettoyer(md):
    """Supprime les lignes vides multiples et les espaces de fin."""
    md = re.sub(r"[ \t]+\n", "\n", md)
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip() + "\n"
