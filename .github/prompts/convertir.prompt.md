---
name: convertir
description: Convertit des fichiers Word, Excel, PowerPoint ou PDF en markdown dans le vault (skill conversion-documents, gratuit).
argument-hint: Chemin(s) de fichier ou dossier, destination éventuelle
agent: agent
model: {{MODELE_GRATUIT}}
---
Applique le skill `conversion-documents` à ${input:fichiers:chemins entre guillemets} (destination : ${input:dest:vide = 0 Inbox/Converted}).
