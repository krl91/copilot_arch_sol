---
name: journal
description: Ajoute une entrée au journal Copilot pour mesurer le temps gagné (gratuit).
argument-hint: ex. « analyse epic MTR-123, 3 h sans, 1 h avec, 4 requêtes »
agent: agent
model: {{MODELE_GRATUIT}}
---
Ajoute à `2 Areas/AI Practice/journal-copilot.md` une ligne datée du jour pour : ${input:entree:tâche, temps sans, temps avec, requêtes, remarque}.
Colonnes : Task, Type (meeting / search / surprise / requirement / review / confluence / email / verification / other),
Est. without, Actual with, Requests, Quality note. Information manquante : `?`, sans poser de question.
