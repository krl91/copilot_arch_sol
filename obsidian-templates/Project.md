---
type: project
status: active            # active | on-hold | done (→ 4 Archives)
customer: 
outcome: 
start: {{date:YYYY-MM-DD}}
deadline: 
my_role: Solution architect
rag: green                # green | amber | red
tags: [project]
---
# {{title}}

> Hub du projet (PARA : un projet = un résultat + une échéance). Mis à jour à chaque revue hebdomadaire.

## Outcome
<!-- Résultat attendu et critère "terminé" (Definition of Done), en une ou deux phrases -->
- **Outcome**:
- **Done when**:
- **Deadline**:

## Scope
| In scope | Out of scope |
|---|---|
|  |  |

## Status — {{date:YYYY-MM-DD}}
<!-- RAG + 3 lignes max : où on en est, ce qui bloque, prochaine étape. Réécrit chaque semaine. -->
- **RAG**: 🟢
- **Progress**:
- **Blockers**:
- **Next**:

## Milestones
| Milestone | Planned | Forecast | Status |
|---|---|---|---|
|  |  |  |  |

## Stakeholders
<!-- Lier les notes Person : [[Nom]] -->
| Person | Role | Side (customer / internal / partner) | Influence / Interest |
|---|---|---|---|
|  |  |  |  |

## Actions & planning
→ [[Project tracker]] : registre des actions (en retard, sous 7 jours, à confirmer, par responsable),
« waiting for », jalons et planning, décisions attendues. Mis à jour par `/suivi`.

## RAID
→ [[RAID log]] — top risks:
| ID | Risk | Score | Owner |
|---|---|---|---|
|  |  |  |  |

## Decisions
→ [[decisions]] (journal) · décisions structurantes : notes `Decision` ci-dessous.
```base
filters:
  and:
    - file.inFolder(this.file.folder)
    - 'type == "decision"'
views:
  - type: table
    name: Decision records
    order:
      - file.name
      - status
      - date
```

## Topics
```base
filters:
  and:
    - file.inFolder(this.file.folder)
    - 'type == "topic"'
views:
  - type: table
    name: Topics
    order:
      - file.name
      - status
      - last_verified
      - owner
```

## Meetings
```base
filters:
  and:
    - file.inFolder(this.file.folder)
    - 'type == "meeting"'
views:
  - type: table
    name: Meetings
    order:
      - file.name
      - date
      - meeting_type
      - status
```

## Documentation
| Document | Location (Confluence / SharePoint / Word) | Version / date | Owner |
|---|---|---|---|
|  |  |  |  |

## Docs to update
<!-- Alimenté par le skill mise-a-jour-vault quand un fait change -->
- [ ] 

## Jira
- Customer requirements (JQL):
- System requirements (JQL):
- Test plans (Xray):

## Reusable outputs
<!-- « Intermediate packets » (BASB) : diagrammes, jeux d'exigences, slides, matrices réutilisables ailleurs -->
- 

## Lessons learned
<!-- À remplir à la clôture : ce qui a marché, ce qui n'a pas marché, ce qu'on refera -->
| What worked | What didn't | What we'll do next time |
|---|---|---|
|  |  |  |
