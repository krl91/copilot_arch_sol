"""Consolide les actions de toutes les réunions d'un projet : registre, retards, échéances proches, à confirmer.

Usage : python outils/actions_projet.py "1 Projects/<P>" [--aujourdhui AAAA-MM-JJ] [--ecrire]
Python 3.8+, bibliothèque standard uniquement. À lancer depuis la racine du vault.

Sources lues (dans le dossier du projet et ses sous-dossiers) :
  - notes `type: meeting` : tableau « Actions » (ID, action, owner, due, done when, status) ;
  - leur tableau « Previous actions review » : met à jour le statut / l'échéance des actions de la réunion
    pointée par `previous_meeting` (même ID) ;
  - note `type: tracker` (modèle Project tracker) : tableau « Status updates » pour les changements connus
    hors réunion (email, échange).
Identifiant global d'une action : <date de la réunion>/<ID>, par ex. 2026-09-15/A2.

Sans --ecrire : affiche le registre (lecture seule).
Avec --ecrire : remplace uniquement le bloc entre <!-- actions:start --> et <!-- actions:end -->
de la note tracker du projet.
Code de sortie : 0 = OK, 1 = erreur, 2 = actions en retard ou à confirmer.
"""
import argparse
import datetime as dt
import re
import sys
from pathlib import Path

STATUTS_CLOS = {"done", "closed", "cancelled", "canceled", "fait", "terminé", "annulé"}
# 7 jours = horizon d'une revue hebdomadaire : ce qui doit être relancé avant la prochaine revue.
HORIZON_PROCHE_JOURS = 7
DEBUT, FIN = "<!-- actions:start -->", "<!-- actions:end -->"


def frontmatter(texte):
    m = re.match(r"^---\n(.*?)\n---\n", texte, re.S)
    props = {}
    if m:
        for ligne in m.group(1).splitlines():
            if ":" in ligne and not ligne.startswith(" "):
                k, v = ligne.split(":", 1)
                props[k.strip()] = v.split("#")[0].strip().strip('"').strip("'")
    return props, (texte[m.end():] if m else texte)


def sections(corps):
    corps = re.sub(r"<!--.*?-->", "", corps, flags=re.S)
    res, titre, lignes = {}, "", []
    for l in corps.splitlines():
        m = re.match(r"^#{1,6}\s+(.*)$", l)
        if m:
            res.setdefault(titre, []).extend(lignes)
            titre, lignes = m.group(1).strip().lower(), []
        else:
            lignes.append(l)
    res.setdefault(titre, []).extend(lignes)
    return res


def tableau(lignes):
    """Premier tableau des lignes → liste de dicts (clés = en-têtes en minuscules)."""
    entetes, rangs = None, []
    for l in lignes:
        s = l.strip()
        if not s.startswith("|"):
            if entetes is not None and rangs:
                break
            continue
        cellules = [c.strip() for c in s.strip("|").split("|")]
        if entetes is None:
            entetes = [c.lower() for c in cellules]
        elif not all(re.fullmatch(r":?-{3,}:?", c) for c in cellules if c):
            if any(cellules):
                rangs.append(dict(zip(entetes, cellules)))
    return rangs


def champ(rang, *prefixes):
    for k, v in rang.items():
        if any(k.startswith(p) for p in prefixes):
            return v
    return ""


def section(secs, prefixe):
    return next((v for k, v in secs.items() if k.startswith(prefixe)), [])


def date_iso(s):
    m = re.match(r"^(\d{4}-\d{2}-\d{2})", s or "")
    if not m:
        return None
    try:
        return dt.date.fromisoformat(m.group(1))
    except ValueError:
        return None


def lien_vers_nom(v):
    return re.sub(r"^\[\[|\]\]$", "", v or "").split("|")[0].strip()


def cellule(t):
    return (t or "").replace("|", "\\|")


def charger(projet: Path):
    reunions, tracker = {}, None
    for f in sorted(projet.rglob("*.md")):
        try:
            props, corps = frontmatter(f.read_text(encoding="utf-8"))
        except UnicodeDecodeError:
            continue
        if props.get("type") == "meeting":
            reunions[f.stem] = (f, props, sections(corps))
        elif props.get("type") == "tracker":
            tracker = (f, props, sections(corps))
    return reunions, tracker


def construire(reunions, tracker):
    actions, anomalies = {}, []
    ordre = sorted(reunions.items(), key=lambda kv: kv[1][1].get("date", ""))
    for nom, (f, props, secs) in ordre:
        d = props.get("date", "") or "????-??-??"
        for r in tableau(section(secs, "actions")):
            ident = champ(r, "id")
            if not re.match(r"^A\d+$", ident):
                continue
            actions[f"{d}/{ident}"] = {
                "action": champ(r, "action"), "owner": champ(r, "owner"), "due": champ(r, "due"),
                "done": champ(r, "done when"), "status": champ(r, "status") or "open",
                "origine": nom, "maj": f"[[{nom}]]",
            }
    # Revues des actions précédentes
    for nom, (f, props, secs) in ordre:
        prec = lien_vers_nom(props.get("previous_meeting", ""))
        rangs = tableau(section(secs, "previous actions"))
        if not rangs:
            continue
        if prec not in reunions:
            anomalies.append(f"[[{nom}]] : revue des actions précédentes sans `previous_meeting` valide.")
            continue
        dp = reunions[prec][1].get("date", "")
        for r in rangs:
            cle = f"{dp}/{champ(r, 'id')}"
            if cle not in actions:
                anomalies.append(f"[[{nom}]] : action « {champ(r, 'id')} » inconnue dans [[{prec}]].")
                continue
            if champ(r, "status"):
                actions[cle]["status"] = champ(r, "status")
            if date_iso(champ(r, "new due")):
                actions[cle]["due"] = champ(r, "new due")
            actions[cle]["maj"] = f"[[{nom}]]"
    # Mises à jour hors réunion
    if tracker:
        for r in tableau(section(tracker[2], "status updates")):
            cle = champ(r, "action id")
            if cle not in actions:
                if cle:
                    anomalies.append(f"Status updates : action « {cle} » inconnue.")
                continue
            if champ(r, "new status"):
                actions[cle]["status"] = champ(r, "new status")
            if date_iso(champ(r, "new due")):
                actions[cle]["due"] = champ(r, "new due")
            actions[cle]["maj"] = champ(r, "source") or "Status updates"
    return actions, anomalies


def rendu(actions, anomalies, aujourdhui):
    ouvertes = {k: a for k, a in actions.items() if a["status"].lower() not in STATUTS_CLOS}
    retard, proches, a_confirmer, autres = [], [], [], []
    for k, a in sorted(ouvertes.items(), key=lambda kv: (date_iso(kv[1]["due"]) or dt.date.max, kv[0])):
        d = date_iso(a["due"])
        if a["owner"].upper().startswith("TBD") or not d:
            a_confirmer.append((k, a))
        elif d < aujourdhui:
            retard.append((k, a))
        elif (d - aujourdhui).days <= HORIZON_PROCHE_JOURS:
            proches.append((k, a))
        else:
            autres.append((k, a))

    def table(liste, retard_col=False):
        if not liste:
            return "_Aucune._\n"
        t = "| ID | Action | Owner | Due | " + ("Days late | " if retard_col else "") + "Status | Last update |\n"
        t += "|---|---|---|---|" + ("---|" if retard_col else "") + "---|---|\n"
        for k, a in liste:
            j = (aujourdhui - date_iso(a["due"])).days if retard_col else None
            t += (f"| {k} | {cellule(a['action'])} | {cellule(a['owner'])} | {a['due']} | "
                  + (f"{j} | " if retard_col else "") + f"{cellule(a['status'])} | {a['maj']} |\n")
        return t

    par_owner = {}
    for _, a in ouvertes.items():
        par_owner[a["owner"] or "TBD"] = par_owner.get(a["owner"] or "TBD", 0) + 1
    md = [f"_Généré par `outils/actions_projet.py` le {aujourdhui.isoformat()} — ne pas modifier à la main "
          f"(utiliser « Status updates »)._\n",
          f"**{len(ouvertes)} action(s) ouverte(s)** · {len(retard)} en retard · {len(proches)} sous "
          f"{HORIZON_PROCHE_JOURS} jours · {len(a_confirmer)} à confirmer · "
          f"{len(actions) - len(ouvertes)} close(s)\n",
          "### 🔴 Overdue\n", table(retard, True),
          f"### 🟠 Due within {HORIZON_PROCHE_JOURS} days\n", table(proches),
          "### ❓ Owner or due date to confirm\n", table(a_confirmer),
          "### 🟢 Other open actions\n", table(autres),
          "### Open actions by owner\n",
          ("| Owner | Open |\n|---|---|\n" + "".join(f"| {cellule(o)} | {n} |\n" for o, n in
                                                 sorted(par_owner.items(), key=lambda x: -x[1])))
          if par_owner else "_Aucune._\n"]
    if anomalies:
        md += ["### ⚠️ Anomalies\n", "".join(f"- {x}\n" for x in anomalies)]
    return "\n".join(md), bool(retard or a_confirmer)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("projet")
    ap.add_argument("--aujourdhui", help="date de référence AAAA-MM-JJ (défaut : aujourd'hui)")
    ap.add_argument("--ecrire", action="store_true", help="écrire le registre dans la note tracker du projet")
    a = ap.parse_args()
    projet = Path(a.projet)
    if not projet.is_dir():
        sys.exit(f"Dossier projet introuvable : {projet}")
    aujourdhui = date_iso(a.aujourdhui) if a.aujourdhui else dt.date.today()
    reunions, tracker = charger(projet)
    if not reunions:
        print(f"Aucune note `type: meeting` dans {projet}.")
        sys.exit(0)
    actions, anomalies = construire(reunions, tracker)
    md, alerte = rendu(actions, anomalies, aujourdhui)
    if a.ecrire:
        if not tracker:
            sys.exit("Aucune note `type: tracker` dans le projet : créer « Project tracker » depuis le modèle.")
        f = tracker[0]
        texte = f.read_text(encoding="utf-8")
        if DEBUT not in texte or FIN not in texte:
            sys.exit(f"Marqueurs {DEBUT} / {FIN} absents de {f}.")
        avant, reste = texte.split(DEBUT, 1)
        _, apres = reste.split(FIN, 1)
        f.write_text(avant + DEBUT + "\n" + md + "\n" + FIN + apres, encoding="utf-8")
        print(f"Registre écrit dans {f}")
    else:
        print(md)
    sys.exit(2 if alerte else 0)


if __name__ == "__main__":
    main()
