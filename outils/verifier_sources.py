"""Contrôle automatique (déterministe) des sources d'un brouillon markdown.

Usage : python outils/verifier_sources.py "chemin/brouillon.md"
Python 3.8+, bibliothèque standard uniquement. Lecture seule.

Convention attendue (voir .github/copilot-instructions.md) :
  - dans le texte : chaque fait porte [S1], [S2]... ou [ASSUMPTION] / [OPEN]
  - en fin de document, une section "## Sources" :
      - [S1] JIRA PRJ-123 (2026-09-12) — "citation exacte"
      - [S2] CONF https://... "Titre" (2026-08-30) — "citation exacte"

Contrôles :
  1. chaque [Sx] cité existe dans Sources, chaque source est utilisée
  2. chaque source a un type, une date (YYYY-MM-DD) et une citation entre guillemets
  3. jetons sensibles du texte (clés Jira, codes OBIS, URL, nombres avec unité, dates)
     absents de toute citation / référence de source  → NON SOURCÉ
  4. lignes de contenu sans aucun marqueur → À VÉRIFIER
Code de sortie : 0 = OK, 1 = problèmes bloquants, 2 = avertissements seulement.
"""
import re
import sys
from pathlib import Path

SRC_TYPES = ("JIRA", "XRAY", "CONF", "SP", "VAULT", "MEETING", "EMAIL", "DOC", "TEAMS")
CITE = re.compile(r"\[S(\d+)\]")
TAG = re.compile(r"\[(S\d+|ASSUMPTION|OPEN)\]")
SRC_LINE = re.compile(r"^\s*[-*]\s*\[S(\d+)\]\s*(\w+)\s+(.*)$")
DATE = re.compile(r"\b(20\d\d-\d\d-\d\d)\b")
QUOTE = re.compile(r"[\"“«]([^\"”»]+)[\"”»]")
SENSITIVE = {
    "Jira key": re.compile(r"\b[A-Z][A-Z0-9]{1,9}-\d+\b"),
    "OBIS code": re.compile(r"\b\d{1,3}-\d{1,3}:\d{1,3}\.\d{1,3}\.\d{1,3}(?:\.\d{1,3})?\b"),
    "URL": re.compile(r"https?://[^\s)\]>\"]+"),
    "number+unit": re.compile(
        r"\b\d+(?:[.,]\d+)?\s?(?:ms|s|sec|min|h|hours?|days?|weeks?|months?|years?|"
        r"[kKMG]B|[kKMG]b|bytes?|bits?|kbps|Mbps|bps|%|kWh|Wh|kW|W|V|A|Hz|kHz|MHz|°C|meters|devices)\b"
    ),
    "date": DATE,
}


def norm(s):
    return re.sub(r"\s+", " ", s).strip().lower()


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    path = Path(sys.argv[1])
    lines = path.read_text(encoding="utf-8").splitlines()

    # Séparer corps / section Sources
    src_idx = next((i for i, l in enumerate(lines) if re.match(r"^#{1,6}\s*Sources\b", l, re.I)), None)
    body = lines if src_idx is None else lines[:src_idx]
    sources_part = [] if src_idx is None else lines[src_idx + 1:]

    errors, warnings = [], []

    # Front matter YAML ignoré
    start = 0
    if body and body[0].strip() == "---":
        end = next((i for i in range(1, len(body)) if body[i].strip() == "---"), 0)
        start = end + 1

    if src_idx is None:
        errors.append("Aucune section '## Sources' trouvée.")

    # Lignes de contenu analysées : hors front matter, blocs de code,
    # commentaires HTML et citations ">" (texte d'aide des modèles)
    content = []
    in_code = in_comment = False
    for n, l in enumerate(body[start:], start + 1):
        st = l.strip()
        if st.startswith("```"):
            in_code = not in_code
            continue
        if in_comment or st.startswith("<!--"):
            in_comment = "-->" not in st
            continue
        if in_code or st.startswith(">"):
            continue
        content.append((n, l))

    # Analyse des sources (les commentaires HTML <!-- --> sont ignorés)
    sources = {}
    in_comment = False
    for l in sources_part:
        if "<!--" in l:
            in_comment = "-->" not in l
            continue
        if in_comment:
            in_comment = "-->" not in l
            continue
        m = SRC_LINE.match(l)
        if not m:
            continue
        sid, stype, rest = m.group(1), m.group(2).upper(), m.group(3)
        sources[sid] = rest
        if stype not in SRC_TYPES:
            warnings.append(f"[S{sid}] type '{stype}' inconnu (attendu : {', '.join(SRC_TYPES)}).")
        if not DATE.search(rest):
            errors.append(f"[S{sid}] sans date au format YYYY-MM-DD.")
        if not QUOTE.search(rest):
            errors.append(f"[S{sid}] sans citation exacte entre guillemets.")

    # Références croisées
    cited = set()
    for n, l in content:
        for sid in CITE.findall(l):
            cited.add(sid)
            if sid not in sources:
                errors.append(f"Ligne {n} : [S{sid}] cité mais absent de la section Sources.")
    for sid in sources:
        if sid not in cited:
            warnings.append(f"[S{sid}] listé mais jamais cité dans le texte.")

    # Identifiants définis dans le brouillon lui-même (ex. "- SR-1: ...") : pas à sourcer
    local_ids = set()
    for _, l in content:
        m = re.match(r"^\s*(?:[-*]|\|)?\s*[`*]*([A-Z][A-Z0-9]{1,9}-\d+)[`*]*\s*[:|—–]", l)
        if m:
            local_ids.add(m.group(1))

    # Jetons sensibles non sourcés
    haystack = norm(" ".join(sources.values()))
    unsourced = []
    for n, l in content:
        for kind, rx in SENSITIVE.items():
            for m in rx.finditer(l):
                tok = m.group(0)
                if kind == "Jira key" and tok in local_ids:
                    continue
                if norm(tok) not in haystack:
                    unsourced.append((n, kind, tok))
    for n, kind, tok in unsourced:
        errors.append(f"Ligne {n} : {kind} « {tok} » n'apparaît dans aucune source/citation → NON SOURCÉ.")

    # Lignes de contenu sans marqueur
    for n, l in content:
        s = l.strip()
        if re.match(r"^[-*]\s*[^:]{1,40}:\s*$", s) or re.match(r"^[-*]\s*\*\*[^*]{1,60}\*\*[^:]{0,60}:\s*$", s):
            continue  # champ vide de modèle ("- Jira:", "- **Outcome**:")
        if re.fullmatch(r"\|(\s*\|)+", s) or re.fullmatch(r"[-*]\s*\[ \]\s*", s) or s in ("-", "1.", "2.", "3."):
            continue  # ligne de tableau ou de liste vide
        if re.match(r"^[-*]\s*\[[ xX]\]", s):
            continue  # case à cocher = tâche, pas une affirmation
        if not s or s.startswith("#") or re.match(r"^\|?\s*:?-{3,}", s):
            continue
        is_item = s.startswith(("- ", "* ")) or re.match(r"^\d+\.\s", s)
        is_row = s.startswith("|") and not re.search(r"\|\s*-{3,}", s)
        is_para = len(s) > 60
        if (is_item or is_row or is_para) and not TAG.search(s):
            # Les en-têtes de tableau (1re ligne avant ---) sont tolérés
            nxt = lines[n] if n < len(lines) else ""
            if is_row and re.search(r"\|\s*:?-{3,}", nxt):
                continue
            warnings.append(f"Ligne {n} : contenu sans [Sx]/[ASSUMPTION]/[OPEN] → « {s[:70]} »")

    # Rapport
    print(f"# Contrôle des sources : {path.name}\n")
    print(f"- Sources déclarées : {len(sources)} · citées : {len(cited)}")
    print(f"- Bloquants : {len(errors)} · Avertissements : {len(warnings)}\n")
    if errors:
        print("## ❌ Bloquants")
        for e in errors:
            print(f"- {e}")
    if warnings:
        print("\n## ⚠️ Avertissements")
        for w in warnings:
            print(f"- {w}")
    if not errors and not warnings:
        print("✅ Aucun problème détecté par le contrôle automatique.")
    print("\n> Ce contrôle est mécanique : il ne juge pas si une citation soutient vraiment "
          "l'affirmation. C'est le rôle de l'agent `verificateur`.")
    sys.exit(1 if errors else (2 if warnings else 0))


if __name__ == "__main__":
    main()
