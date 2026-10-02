---
name: compte-rendu-reunion
description: Transforme une note de réunion Obsidian (récap Teams, transcription, notes personnelles) en compte rendu anglais structuré avec contrôle de compréhension, décisions, actions, tickets Jira proposés et, pour un workshop client, un email « minutes for confirmation ». À utiliser pour toute réunion interne, workshop client, handover, meeting minutes ou demande « traite cette réunion ».
user-invocable: false
---
# Compte rendu de réunion

Entrée : note créée depuis `obsidian-templates/Meeting.md` (frontmatter `meeting_type`, sections
`## Prep`, `## Teams recap`, `## Transcript`, `## My notes`, `## Sources`). Modèle de sortie selon `meeting_type` :
`internal` → [interne.md](interne.md) · `customer-workshop` → [workshop-client.md](workshop-client.md) ·
`handover` → [handover.md](handover.md).

## Déroulé (copier et cocher)
```
- [ ] 1. Métadonnées complètes (sinon ≤ 3 questions)
- [ ] 2. Contexte projet lu
- [ ] 3. Citations extraites (## Sources)
- [ ] 4. Contrôle de compréhension
- [ ] 5. Synthèse selon le modèle
- [ ] 6. Contrôle automatique : 0 bloquant
- [ ] 7. Tickets Jira proposés (non créés)
- [ ] 8. status: processed, puis skill mise-a-jour-vault
```

1. **Métadonnées** : date, projet, participants. Manquantes → au plus 3 questions ; sans réponse,
   continuer en marquant `[OPEN]`.
2. **Contexte** : hub du projet, `decisions.md`, notes Topic concernées, tickets Jira cités (lecture seule).
3. **Citations** : sources `MEETING <note> § Teams recap | Transcript | My notes (date)` avec citations exactes.
4. **Contrôle de compréhension** — `| # | Noté par moi | Dit dans la transcription | Écart (missed / different / ambiguous) |`,
   plus les points importants non notés. Sans transcription : points flous ou incohérents du récap.
5. **Synthèse** en anglais dans `## Summary`, selon le modèle du type. Comparer avec `## Prep` :
   résultats attendus obtenus ou non, questions restées sans réponse, et alerte si un engagement listé
   dans « Commitments I must NOT make » a été pris. Actions : responsable, date
   AAAA-MM-JJ, critère d'achèvement. Dates relatives converties depuis la date de réunion.
6. **Contrôle** : `{{PYTHON_CMD}} outils/verifier_sources.py "<note>"` → corriger → relancer jusqu'à 0 bloquant.
7. **Jira** : proposer les tickets (titre, type, description EN, lien existant). Création = livrable N2.
8. Mettre `status: processed`, cocher ce qui est fait dans `## Follow-up`, enchaîner sur
   `mise-a-jour-vault` (actions, RAID, décisions, engagements), terminer par les actions de l'utilisateur
   et une ligne de journal.

## Règles
- Aucune décision ni engagement attribué sans formulation explicite dans la source.
- Ne pas modifier `## Teams recap`, `## Transcript`, `## My notes`.
- Email client et tickets = **N2** (vérificateur + accord).

Exemples d'évaluation : [evals.json](evals.json).
