---
name: exigence
description: Décline une exigence client en exigences système Jira vérifiées (skill exigence-systeme, N2).
argument-hint: Clé Jira de l'exigence client ou texte
agent: redacteur
model: {{MODELE_REDACTEUR}}
---
Applique le skill `exigence-systeme` à ${input:exigence:clé Jira ou texte}. Niveau N2 : brouillon → contrôle → verificateur → OK → Jira.
