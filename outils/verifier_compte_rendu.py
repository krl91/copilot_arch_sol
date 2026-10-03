"""Contrôle automatique d'un compte rendu de réunion et de ses notes de travail.

Usage : python outils/verifier_compte_rendu.py "1 Projects/<P>/Meetings/<réunion>.md"
Python 3.8+, bibliothèque standard uniquement. Lecture seule. À lancer depuis la racine du vault.

Note Meeting (diffusable) :
  1. aucun contenu interne : marqueurs [Sx] / [ASSUMPTION], sections Understanding check, Consistency check,
     Clean notes, My notes, Transcript, Teams recap, Prep (private), Sources, Traceability, Draft email
  2. actions : un responsable nommé (pas « team », « all »…) et une échéance AAAA-MM-JJ ou TBD
Note Working notes (privée, liée par la propriété working_notes) :
  3. chaque élément identifié du compte rendu (D1, A1, C1, Q1, R1, S1…) figure dans « Traceability »
  4. convention de sources respectée (outils/verifier_sources.py)
Code de sortie : 0 = OK, 1 = problèmes bloquants, 2 = avertissements seulement.
"""
import re
import subprocess
import sys
from pathlib import Path

SECTIONS_INTERDITES = ("understanding check", "consistency check", "clean notes", "my notes", "transcript",
                       "teams recap", "sources", "traceability", "draft email", "prep (private)")
MARQUEURS_INTERDITS = re.compile(r"\[(S\d+|ASSUMPTION)\]")
# Identifiants d'éléments du compte rendu : Decision, Action, Commitment, Question, Requirement, Scope change
ID_ELEMENT = re.compile(r"^(?:D|A|C|Q|R|S)\d+$")
RESPONSABLES_FLOUS = {"team", "all", "everyone", "everybody", "we", "us", "équipe", "tous", "nous", "tbd?"}
DATE_OU_TBD = re.compile(r"^(\d{4}-\d{2}-\d{2}|TBD)\b", re.I)


def frontmatter(texte):
    m = re.match(r"^---\n(.*?)\n---\n", texte, re.S)
    props = {}
    if m:
        for ligne in m.group(1).splitlines():
            if ":" in ligne and not ligne.startswith(" "):
                k, v = ligne.split(":", 1)
                props[k.strip()] = v.split("#")[0].strip().strip('"').strip("'")
    return props, (texte[m.end():] if m else texte)


def sans_commentaires(texte):
    return re.sub(r"<!--.*?-->", "", texte, flags=re.S)


def sections(corps):
    """→ liste de (titre en minuscules, lignes) pour chaque titre markdown."""
    res, titre, lignes = [], "", []
    for l in corps.splitlines():
        m = re.match(r"^#{1,6}\s+(.*)$", l)
        if m:
            res.append((titre, lignes))
            titre, lignes = m.group(1).strip().lower(), []
        else:
            lignes.append(l)
    res.append((titre, lignes))
    return res


def tableaux(lignes):
    """→ liste de tableaux : (en-têtes, lignes de cellules)."""
    out, courant = [], None
    for l in lignes:
        s = l.strip()
        if s.startswith("|"):
            cellules = [c.strip() for c in s.strip("|").split("|")]
            if courant is None:
                courant = (cellules, [])
            elif not all(re.fullmatch(r":?-{3,}:?", c) for c in cellules if c):
                courant[1].append(cellules)
        elif courant is not None:
            out.append(courant)
            courant = None
    if courant is not None:
        out.append(courant)
    return out


def trouver_notes_travail(lien, meeting: Path):
    nom = re.sub(r"^\[\[|\]\]$", "", lien).split("|")[0].strip()
    if not nom:
        return None
    candidats = [meeting.parent / f"{nom}.md"] + list(Path(".").rglob(f"{nom}.md"))
    return next((c for c in candidats if c.is_file()), None)


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    meeting = Path(sys.argv[1])
    texte = meeting.read_text(encoding="utf-8")
    props, corps = frontmatter(texte)
    corps = sans_commentaires(corps)
    erreurs, alertes = [], []
    ids_cr = set()

    for titre, lignes in sections(corps):
        if any(titre.startswith(s) for s in SECTIONS_INTERDITES):
            erreurs.append(f"Section interne « {titre} » présente dans le compte rendu diffusable.")
        for l in lignes:
            if MARQUEURS_INTERDITS.search(l):
                erreurs.append(f"Marqueur interne dans le compte rendu : « {l.strip()[:80]} »")
            if "[OPEN]" in l:
                alertes.append(f"[OPEN] dans le compte rendu : écrire plutôt « TBD » / « to be confirmed » → « {l.strip()[:60]} »")
        revue_precedente = titre.startswith("previous actions")
        for entetes, rangs in tableaux(lignes):
            h = [e.lower() for e in entetes]
            i_owner = next((i for i, e in enumerate(h) if e.startswith("owner")), None)
            i_due = next((i for i, e in enumerate(h) if e.startswith("due")), None)
            for r in rangs:
                if not any(r):
                    continue
                ident = r[0] if r else ""
                if ID_ELEMENT.match(ident) and not revue_precedente:
                    ids_cr.add(ident)
                if titre.startswith("actions") and ident:
                    owner = r[i_owner] if i_owner is not None and i_owner < len(r) else ""
                    due = r[i_due] if i_due is not None and i_due < len(r) else ""
                    if not owner:
                        erreurs.append(f"Action {ident} sans responsable (écrire TBD si non dit).")
                    elif owner.lower() in RESPONSABLES_FLOUS or "/" in owner or " and " in owner.lower():
                        erreurs.append(f"Action {ident} : responsable « {owner} » — une seule personne nommée.")
                    if not DATE_OU_TBD.match(due):
                        erreurs.append(f"Action {ident} : échéance « {due} » — format AAAA-MM-JJ ou TBD.")
                    if owner.upper().startswith("TBD") or due.upper().startswith("TBD"):
                        alertes.append(f"Action {ident} : responsable ou échéance à faire confirmer (TBD).")

    # Notes de travail
    lien = props.get("working_notes", "")
    wn = trouver_notes_travail(lien, meeting) if lien else None
    rapport_sources = ""
    if wn is None:
        erreurs.append(f"Notes de travail introuvables (propriété working_notes = « {lien or 'absente'} »).")
    else:
        _, corps_wn = frontmatter(wn.read_text(encoding="utf-8"))
        corps_wn = sans_commentaires(corps_wn)
        ids_trace = set()
        for titre, lignes in sections(corps_wn):
            if titre.startswith("traceability"):
                for _, rangs in tableaux(lignes):
                    for r in rangs:
                        if r and r[0]:
                            ids_trace.add(r[0])
                            if len(r) < 3 or not re.search(r"\[(S\d+|ASSUMPTION|OPEN)\]", r[2]):
                                erreurs.append(f"Traçabilité : {r[0]} sans source [Sx] (ou [ASSUMPTION]/[OPEN]).")
        for i in sorted(ids_cr - ids_trace):
            erreurs.append(f"{i} figure dans le compte rendu mais pas dans la traçabilité des notes de travail.")
        for i in sorted(ids_trace - ids_cr):
            alertes.append(f"{i} tracé dans les notes de travail mais absent du compte rendu.")
        verif = Path(__file__).with_name("verifier_sources.py")
        res = subprocess.run([sys.executable, str(verif), str(wn)], capture_output=True, text=True, encoding="utf-8")
        rapport_sources = res.stdout
        if res.returncode == 1:
            erreurs.append("Notes de travail : la convention de sources a des bloquants (détail ci-dessous).")
        elif res.returncode == 2:
            alertes.append("Notes de travail : avertissements sur les sources (détail ci-dessous).")

    print(f"# Contrôle du compte rendu : {meeting.name}\n")
    print(f"- Notes de travail : {wn if wn else 'introuvables'}")
    print(f"- Éléments identifiés dans le compte rendu : {len(ids_cr)}")
    print(f"- Bloquants : {len(erreurs)} · Avertissements : {len(alertes)}\n")
    if erreurs:
        print("## ❌ Bloquants")
        print("\n".join(f"- {e}" for e in erreurs))
    if alertes:
        print("\n## ⚠️ Avertissements")
        print("\n".join(f"- {a}" for a in alertes))
    if not erreurs and not alertes:
        print("✅ Compte rendu diffusable et traçable.")
    if rapport_sources:
        print("\n---\n" + rapport_sources)
    sys.exit(1 if erreurs else (2 if alertes else 0))


if __name__ == "__main__":
    main()
