---
name: reunion
description: Traite une note de réunion (interne, workshop client, handover) avec le skill compte-rendu-reunion, puis met à jour le vault.
argument-hint: Chemin de la note (vide = fichier ouvert)
agent: redacteur
model: {{MODELE_REDACTEUR}}
---
Applique le skill `compte-rendu-reunion` à ${input:note:chemin de la note, vide = fichier ouvert}, puis `mise-a-jour-vault`.
Note du vault : N1. Email client, tickets Jira, mises à jour du fichier de suivi : N2.
