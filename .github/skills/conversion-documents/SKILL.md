---
name: conversion-documents
description: Convertit des documents Word (.docx), Excel (.xlsx/.xlsm), PowerPoint (.pptx/.pptm) et PDF en markdown dans le vault grâce aux scripts Python du kit, pour pouvoir les lire, les chercher et les citer. À utiliser dès qu'un de ces fichiers est mentionné, joint ou à analyser (lire, résumer, comparer, extraire, relire une spec, un contrat, un support de comité ou un fichier de suivi), même si le mot « convertir » n'est pas employé, et pour un dossier entier.
user-invocable: false
---
# Conversion de documents

Ne jamais lire ni analyser un fichier Office ou PDF directement : **le convertir d'abord**, puis travailler
sur le markdown produit.

## Commande
```bash
{{PYTHON_CMD}} outils/convertir.py "<fichier ou dossier>" [-r] [--out "<dossier du vault>"] [--tableaux]
```
- Sortie par défaut : `0 Inbox/Converted/<nom>.md` (jamais à côté de l'original).
- `-r` : sous-dossiers ; `--tableaux` : tableaux des PDF (nécessite pdfplumber).
- Options par format : `outils/xlsx2md.py --onglet … --max-lignes …`,
  `outils/pptx2md.py --sans-notes --masquees`, `outils/pdf2md.py --pages 1-10`.

## Après conversion (copier et cocher)
```
- [ ] Sortie du script lue : convertis / ignorés / échecs avec cause
- [ ] Alertes vérifiées : PDF scanné, tableau tronqué, onglet vide, slide sans texte
- [ ] Contenu converti NON modifié et NON résumé dans le fichier (c'est une source)
- [ ] Classement PARA proposé
```

## Cas particuliers
- `.doc`, `.xls`, `.ppt` : demander un réenregistrement au format récent.
- « pypdf absent » : proposer `{{PYTHON_CMD}} -m pip install --user pypdf` (après accord) ; sinon s'arrêter.
- PDF scanné (aucun texte) : ne pas l'utiliser comme source ; demander l'original ou un OCR.
- Graphiques, SmartArt et images ne sont pas extraits : le signaler si l'analyse en dépend.

Citation : `[Sx] DOC <fichier> (§ / onglet / slide / page) (date du fichier) — "citation"`.
Exemples d'évaluation : [evals.json](evals.json).
