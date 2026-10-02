---
name: email
description: Rédige un email en anglais appuyé sur le contexte projet (Jira, vault). Email simple → Copilot dans Outlook.
argument-hint: Destinataires, objectif, points
agent: agent
model: {{MODELE_GRATUIT}}
---
Destinataires : ${input:destinataires:ex. customer PM} · Objectif : ${input:objectif:ce que tu veux obtenir} · Points : ${input:points:en vrac}

- Objet `[<Project>] <topic> – <action expected>` ; corps court : contexte, points numérotés, demande explicite avec échéance.
- Uniquement des faits présents dans le vault ou Jira (citer les clés Jira).
- Client : courtois et prudent sur les engagements ; interne : direct.
- Sous l'email, en français : phrases pouvant être lues comme un engagement contractuel.
Email client = livrable N2 : proposer `/verifier`.
