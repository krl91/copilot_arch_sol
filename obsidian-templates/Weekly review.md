---
type: weekly-review
week: {{date:GGGG-[W]WW}}
date: {{date:YYYY-MM-DD}}
tags: [review]
---
# Weekly review {{date:GGGG-[W]WW}}

> Revue hebdomadaire en 3 temps (GTD, David Allen) + PARA. 45 à 60 min, vendredi après-midi.

## 1. Get clear
- [ ] `0 Inbox/` vidé (chaque note classée, convertie ou supprimée)
- [ ] Emails de la semaine triés (Outlook Copilot) ; faits utiles capturés
- [ ] Réunions non traitées passées à `/reunion` (liste ci-dessous)
- [ ] Tête vidée : nouvelles actions, idées, inquiétudes notées

```base
filters:
  and:
    - 'type == "meeting"'
    - 'status == "raw"'
views:
  - type: table
    name: Meetings to process
    order:
      - file.name
      - date
      - project
```

## 2. Get current
- [ ] Actions ouvertes revues dans chaque hub projet (fait / relancé / replanifié)
- [ ] Calendrier passé (2 semaines) : rien d'oublié ?
- [ ] Calendrier à venir (4 semaines) : réunions à préparer (section Prep)
- [ ] Statut RAG et « Status » mis à jour dans chaque projet actif
- [ ] RAID log revu : nouveaux risques, scores, hypothèses à valider
- [ ] « Waiting for » : ce que j'attends des autres

```base
filters:
  and:
    - 'type == "project"'
    - 'status == "active"'
views:
  - type: table
    name: Active projects
    order:
      - file.name
      - rag
      - deadline
      - outcome
```

## 3. Get creative
- [ ] Une idée d'amélioration du travail ou d'un livrable
- [ ] Une connaissance à capitaliser dans `3 Resources/` (fiche réutilisable)

## AI practice
- [ ] Coach : « bilan de la semaine »
- [ ] Compteur de crédits relevé (github.com) et reporté dans le journal Copilot
- Gains de la semaine :
- Erreurs attrapées par la vérification :

## Big 3 for next week
1. 
2. 
3. 
