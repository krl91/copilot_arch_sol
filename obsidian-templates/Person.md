---
type: person
organization: 
role: 
side: internal            # internal | customer | partner
location: 
language: 
influence: medium         # high | medium | low
interest: medium          # high | medium | low
tags: [person]
---
# {{title}}

> Informations **professionnelles uniquement** (rôle, attentes, sujets). Aucune donnée personnelle ou sensible.

## Role & responsibilities

## What they care about
<!-- Objectifs, critères de succès, inquiétudes -->

## How to work with them
<!-- Canal préféré, niveau de détail attendu, langue, sujets sensibles -->
- **Engagement strategy** (grille pouvoir / intérêt) : manage closely | keep satisfied | keep informed | monitor

## Open topics with them
- 

## Commitments
| Date | Who committed | What | Status |
|---|---|---|---|
|  |  |  |  |

## Interactions
```base
filters:
  and:
    - file.hasLink(this.file)
    - 'type == "meeting"'
views:
  - type: table
    name: Meetings
    order:
      - file.name
      - date
      - project
```
