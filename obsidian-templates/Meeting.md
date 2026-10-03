---
type: meeting
meeting_type: internal    # internal | customer-workshop | handover
project: 
customer: 
date: {{date:YYYY-MM-DD}}
start: {{time}}
duration: 
location: 
organizer: 
minute_taker: 
participants: []
absent: []
distribution: []          # participants + absents + autres destinataires
classification: internal  # public | internal | confidential (client)
previous_meeting:         # [[note de la réunion précédente]] → revue des actions
language: en
recording: 
status: raw               # raw → processed (mis à jour par /reunion)
minutes_status: draft     # draft | sent | confirmed
tags: [meeting]
---
# {{title}}

## Prep
<!-- 5 minutes AVANT la réunion. Objectif clair = réunion courte. -->
- **Purpose**:
- **Desired outcomes** (decisions / information / alignment):
- **Agenda**:
  1. 
- **Pre-reads**:
- **Open actions from previous meeting** (voir `previous_meeting`):
- **My questions to ask**:
  - 
- **Commitments I must NOT make** (scope, dates, cost):

## Teams recap
<!-- Coller ici le compte rendu Copilot de Teams (modèle adapté au type de réunion) -->

## Transcript
<!-- Optionnel : la partie utile de la transcription, pour le contrôle de compréhension -->

## My notes
<!-- Impressions, non-dits, doutes ("pas sûr d'avoir compris X"), signaux faibles -->

## Summary
<!-- Généré par /reunion -->

## Actions
<!-- Rempli par /reunion. Chaque action : responsable + échéance + critère d'achèvement.
     Responsable ou date non dits en réunion : TBD [OPEN], à faire confirmer. -->
| ID | Action (verb + deliverable) | Owner (one person) | Due | Done when | Status |
|---|---|---|---|---|---|

## Follow-up
- [ ] Minutes sent within 24 h to participants **and absentees** (version sans parties internes)
- [ ] Minutes confirmed by customer (workshop)
- [ ] Actions added to the project hub and the Excel tracker
- [ ] Vault updated (/maj-vault)
- [ ] Journal entry (/journal)

## Sources
<!-- Rempli par /reunion : - [S1] MEETING <note> § Teams recap | Transcript | My notes (YYYY-MM-DD) — "citation exacte" -->
