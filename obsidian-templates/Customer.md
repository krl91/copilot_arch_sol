---
type: customer
status: active
country: 
segment:                  # utility / DSO, water, gas, energy retailer…
contract: 
tags: [area, customer]
---
# {{title}}

> Domaine PARA (responsabilité continue) : tout ce qu'il faut savoir sur ce client, au-delà d'un projet.

## Context
<!-- Activité, enjeux réglementaires, programme de déploiement, volumes annoncés [Sx] -->

## Technical landscape
| Element | Value | Source |
|---|---|---|
| Head-end system (HES) |  |  |
| MDM |  |  |
| Communication (PLC / RF / cellular) |  |  |
| Standards & profiles (DLMS/COSEM, IDIS…) |  |  |
| Security requirements |  |  |

## Contractual references
| Document | Version / date | Location |
|---|---|---|
|  |  |  |

## Key people
<!-- Lier les notes Person -->
| Person | Role | Influence / Interest |
|---|---|---|
|  |  |  |

## Customer terminology
| Customer term | Our term / meaning |
|---|---|
|  |  |

## Commitments made to this customer
| Date | Commitment | By | Source | Status |
|---|---|---|---|---|
|  |  |  |  |  |

## Projects
```base
filters:
  and:
    - 'type == "project"'
    - file.hasLink(this.file)
views:
  - type: table
    name: Projects
    order:
      - file.name
      - status
      - deadline
      - rag
```

## Sources
<!-- - [S1] TYPE emplacement (YYYY-MM-DD) — "citation exacte" -->
