---
type: home
---
# Home

> Tableau de bord du vault (note d'accueil). Vues dynamiques via Obsidian Bases (plugin natif).

## Active projects
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
      - customer
      - rag
      - deadline
```

## Meetings to process
```base
filters:
  and:
    - 'type == "meeting"'
    - 'status == "raw"'
views:
  - type: table
    name: To process
    order:
      - file.name
      - date
      - project
```

## Topics to verify
```base
filters:
  and:
    - 'type == "topic"'
    - 'status == "to-verify"'
views:
  - type: table
    name: To verify
    order:
      - file.name
      - project
      - last_verified
```

## Proposed decisions
```base
filters:
  and:
    - 'type == "decision"'
    - 'status == "proposed"'
views:
  - type: table
    name: Pending decisions
    order:
      - file.name
      - project
      - date
```

## Inbox
```base
filters:
  and:
    - file.inFolder("0 Inbox")
views:
  - type: list
    name: Inbox
    order:
      - file.name
```
