---
type: area
owner: 
review: monthly
tags: [area]
---
# {{title}}

> Domaine PARA : une responsabilité continue, sans échéance, avec un niveau d'exigence à maintenir.

## Purpose
## Standard to maintain
<!-- À quoi ressemble « bien tenu » : critères observables -->
- 

## Responsibilities
- 

## Active projects
```base
filters:
  and:
    - 'type == "project"'
    - 'status == "active"'
    - file.hasLink(this.file)
views:
  - type: table
    name: Active projects
    order:
      - file.name
      - deadline
      - rag
```

## Key resources
- 

## Review notes
| Date | Observation | Action |
|---|---|---|
|  |  |  |
