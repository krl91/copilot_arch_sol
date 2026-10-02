---
name: exigence-systeme
description: Décline une exigence client en exigences système Jira rédigées en anglais selon les règles INCOSE, avec critique de l'exigence client, questions de clarification, critères d'acceptation, méthode de vérification, vue CESAM et lien de traçabilité. À utiliser pour toute exigence client, customer requirement, system requirement, ticket Jira d'exigence ou matrice de traçabilité.
user-invocable: false
---
# Exigence client → exigences système

Conventions Jira : {{JIRA_CONVENTIONS}}
Règles de rédaction : [regles-redaction.md](regles-redaction.md) · Exemples : [exemples.md](exemples.md)

## Déroulé (copier et cocher)
```
- [ ] 1. Exigence client et contexte lus, citations extraites
- [ ] 2. Critique de l'exigence client + questions client
- [ ] 3. Exigences système rédigées (brouillon Drafts/)
- [ ] 4. Auto-contrôle avec regles-redaction.md (chaque règle)
- [ ] 5. Contrôle automatique : 0 bloquant
- [ ] 6. Vérification N2 (verificateur)
- [ ] 7. OK → création Jira + liens + entrée decisions.md si interprétation
```

1. **Lire** l'exigence client (ticket, extrait converti ou texte), les tickets liés et la note Topic du sujet.
2. **Critiquer** — `| # | Extrait client | Problème (ambigu, non mesurable, multiple, implicite, conflit) | Question au client (EN) |`.
3. **Rédiger** 1..n exigences dans `1 Projects/<P>/Drafts/req-<clé>.md`. Pour chacune :
   ID provisoire en début de ligne (`SR-1:`, `SR-2:`… remplacés par les clés Jira à la création), Title, Statement (« The <system> shall … »), Rationale, CESAM view
   (Operational / Functional / Constructional), Verification method (Test / Analysis / Inspection /
   Demonstration), Acceptance criteria (valeurs et unités), Source (clé client), Assumptions / Open questions.
4. **Auto-contrôler** chaque exigence avec [regles-redaction.md](regles-redaction.md) → corriger → recontrôler.
5. **Contrôle automatique** : `{{PYTHON_CMD}} outils/verifier_sources.py "<brouillon>"` jusqu'à 0 bloquant.
6. **Vérifier** (N2) via le sous-agent `verificateur`.
7. **Publier** après accord ; tracer toute interprétation dans `decisions.md`.

Exemples d'évaluation : [evals.json](evals.json).
