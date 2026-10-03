---
name: compte-rendu-reunion
description: Transforme une note de réunion Obsidian (récap Teams, transcription, notes personnelles) en compte rendu anglais structuré avec contrôle de compréhension, décisions, actions, tickets Jira proposés et, pour un workshop client, un email « minutes for confirmation ». À utiliser pour toute réunion interne, workshop client, handover, meeting minutes ou demande « traite cette réunion ».
user-invocable: false
---
# Compte rendu de réunion

Entrée : note créée depuis `obsidian-templates/Meeting.md` (frontmatter `meeting_type`, sections
`## Prep`, `## Teams recap`, `## Transcript`, `## My notes`, `## Sources`). Modèle de sortie selon `meeting_type` :
Règles communes (structure, style, diffusion) : [regles-compte-rendu.md](regles-compte-rendu.md).
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
- [ ] 9. Version à diffuser proposée (sans parties internes), envoi sous 24 h
```

1. **Métadonnées** : date, projet, participants. Manquantes → au plus 3 questions ; sans réponse,
   continuer en marquant `[OPEN]`.
2. **Contexte** : hub du projet, `decisions.md`, notes Topic concernées, tickets Jira cités (lecture seule),
   et la **réunion précédente** (`previous_meeting`, sinon la dernière note Meeting du projet) pour la revue
   des actions précédentes.
3. **Citations** : sources `MEETING <note> § Teams recap | Transcript | My notes (date)` avec citations exactes.
4. **Contrôle de compréhension** — `| # | Noté par moi | Dit dans la transcription | Écart (missed / different / ambiguous) |`,
   plus les points importants non notés. Sans transcription : points flous ou incohérents du récap.
5. **Synthèse** en anglais dans `## Summary`, selon le modèle du type ; actions dans `## Actions`. Comparer avec `## Prep` :
   résultats attendus obtenus ou non, questions restées sans réponse, et alerte si un engagement listé
   dans « Commitments I must NOT make » a été pris. Actions : responsable, date
   AAAA-MM-JJ, critère d'achèvement. Dates relatives converties depuis la date de réunion.
6. **Contrôle** : `{{PYTHON_CMD}} outils/verifier_sources.py "<note>"` → corriger → relancer jusqu'à 0 bloquant.
7. **Jira** : proposer les tickets (titre, type, description EN, lien existant). Création = livrable N2.
8. Mettre `status: processed`, cocher ce qui est fait dans `## Follow-up`, enchaîner sur
   `mise-a-jour-vault` (actions, RAID, décisions, engagements), terminer par les actions de l'utilisateur
   et une ligne de journal.
9. **Diffusion** : proposer la version à envoyer (règles de [regles-compte-rendu.md](regles-compte-rendu.md) :
   sans contrôle de compréhension, notes personnelles, transcription ni marqueurs `[Sx]`), destinataires =
   participants + absents. Rappeler l'envoi sous 24 h ; mettre `minutes_status: sent` une fois envoyé.

## Règles
- Structure, style et diffusion : [regles-compte-rendu.md](regles-compte-rendu.md).
- **Toute action a un seul responsable (une personne) et une échéance** (et un critère d'achèvement), quel que soit le type de
  réunion : une action = un verbe + un livrable (« Send the updated interface spec », pas « Interface »).
- Responsable ou date **non dits en réunion → ne jamais les inventer** : `TBD [OPEN]`, et lister ces actions
  sous « Owners / due dates to confirm » (et dans l'email de confirmation pour un workshop).
- Actions reportées dans la section `## Actions` de la note **et** dans `Open actions` du hub projet.
- Aucune décision ni engagement attribué sans formulation explicite dans la source.
- Ne pas modifier `## Teams recap`, `## Transcript`, `## My notes`.
- Email client et tickets = **N2** (vérificateur + accord).

Exemples d'évaluation : [evals.json](evals.json).
