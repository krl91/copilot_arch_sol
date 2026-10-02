---
name: cadrer-demande
description: Cadre une tâche surprise avant de s'y lancer - reformulation, questions immédiates, estimation, plan (gratuit).
argument-hint: Demande reçue et demandeur
agent: ask
model: {{MODELE_GRATUIT}}
---
Demande : ${input:demande:colle ou résume la demande} · Demandeur : ${input:demandeur:qui ?}

Réponse courte en français :
1. Reformulation en une phrase (livrable, destinataire, échéance).
2. Au plus 4 questions à poser tout de suite (périmètre, détail attendu, échéance réelle, usage).
3. Estimation : < 30 min / < 2 h / > 2 h, avec la raison.
4. Plan en 3-5 étapes avec l'outil de chaque étape (`/recherche`, Copilot 365, skill, manuel).
5. Ligne de journal (type `surprise`).
