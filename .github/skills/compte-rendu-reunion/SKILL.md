---
name: compte-rendu-reunion
description: Transforme une réunion en deux notes liées - un compte rendu anglais diffusable (décisions, actions avec responsable et échéance, discussion, prochaine réunion) et des notes de travail privées (récap Teams, transcription, notes personnelles, contrôle de compréhension, traçabilité vers les sources, brouillon d'email de confirmation). À utiliser pour toute réunion interne, workshop client, handover, meeting minutes ou demande « traite cette réunion ».
user-invocable: false
---
# Compte rendu de réunion

Deux notes liées, créées depuis `obsidian-templates/` :
- **Meeting** (`<titre>.md`) — compte rendu **diffusable tel quel** : aucun marqueur de source, aucune note
  personnelle. Propriété `working_notes` = lien vers la note privée.
- **Meeting working notes** (`<titre> (working notes).md`) — **privée** : `Prep (private)`, `Teams recap`,
  `Transcript`, `My notes`, `Clean notes`, `Understanding check`, `Consistency check`, `Traceability`,
  `Draft email`, `Sources`.

Règles communes : [regles-compte-rendu.md](regles-compte-rendu.md). Format selon `meeting_type` :
`internal` → [interne.md](interne.md) · `customer-workshop` → [workshop-client.md](workshop-client.md) ·
`handover` → [handover.md](handover.md).

## Déroulé (copier et cocher)
```
- [ ] 1. Deux notes présentes (sinon créer les working notes depuis le modèle) ; métadonnées complètes
- [ ] 2. Contexte lu (hub, decisions.md, Topics, Jira, réunion précédente)
- [ ] 3. Citations extraites dans ## Sources des working notes
- [ ] 4. Clean notes, Understanding check et Consistency check (working notes)
- [ ] 5. Compte rendu rédigé dans la note Meeting, éléments identifiés (D1, A1, C1, Q1, R1, S1…)
- [ ] 6. Traceability : chaque ID → formulation exacte → [Sx]
- [ ] 7. verifier_compte_rendu.py : 0 bloquant
- [ ] 8. Tickets Jira et email de confirmation proposés (N2, non envoyés)
- [ ] 9. status: processed, mise-a-jour-vault proposé ; après « OK » : vault + registre des actions (script)
```

1. **Notes** : si les working notes n'existent pas, les créer depuis `Meeting working notes.md` et y déplacer
   tout contenu interne trouvé dans la note Meeting (montrer le déplacement, attendre l'accord).
   Métadonnées manquantes → au plus 3 questions ; sinon continuer avec `TBD`.
2. **Contexte** : hub projet, `decisions.md`, notes Topic, tickets Jira cités (lecture seule), réunion
   précédente (`previous_meeting`, sinon la dernière note Meeting du projet) pour la revue des actions.
3. **Citations** : sources `MEETING <note working notes> § Teams recap | Transcript | My notes (date)`.
4. Dans les working notes :
   - **Clean notes** : reprendre `My notes`, les classer par point de l'ordre du jour, corriger la forme et les
     compléter avec le récap Teams et la transcription ; chaque ajout porte `[Sx]`. `My notes` reste intact.
   - **Understanding check** — `| # | Noted by me | Said in transcript | Gap |` + points importants non notés.
     Sans transcription : points flous ou incohérents du récap.
   - **Consistency check** — ce qui a été dit comparé à ce que le projet sait déjà (notes Topic, `decisions.md`,
     RAID, Jira) : nouveau, modifié ou contradictoire, avec la suite proposée (question, mise à jour du vault).
5. **Compte rendu** dans la note Meeting, selon le format du type. Chaque décision, action, engagement,
   question, exigence ou changement de périmètre reçoit un ID (`D1`, `A1`, `C1`, `Q1`, `R1`, `S1`).
   Comparer avec `Prep (private)` : résultats obtenus, questions sans réponse, **alerte** si un engagement
   de « Commitments I must NOT make » a été pris.
6. **Traceability** (working notes) : pour chaque ID, la formulation exacte du compte rendu et sa source `[Sx]`
   (ou `[OPEN]` si responsable / date non dits).
7. **Contrôle** : `{{PYTHON_CMD}} outils/verifier_compte_rendu.py "<note Meeting>"` → corriger → relancer
   jusqu'à 0 bloquant (contrôle aussi la convention de sources des working notes).
8. **Livrables N2** : tickets Jira proposés ; workshop client → brouillon d'email dans `Draft email`.
   Vérification par `verificateur` avant tout envoi ou création.
9. Mettre `status: processed`, enchaîner sur `mise-a-jour-vault` (sources = working notes) et présenter ses
   propositions **dans la même réponse**. Après l'accord de l'utilisateur (un seul message « OK ») : appliquer
   les mises à jour du vault **et** exécuter `{{PYTHON_CMD}} outils/actions_projet.py "1 Projects/<P>" --ecrire`
   (registre des actions, sans requête supplémentaire). Terminer par les actions de l'utilisateur, le rappel
   d'envoi sous 24 h (participants + absents) et une ligne de journal.

## Économie
- Tout faire en **une réponse** (étapes 1 à 9), puis une seule réponse après « OK ». Pas d'aller-retour.
- Réunion interne = N1 : contrôle par script, **pas** de sous-agent vérificateur. Vérificateur seulement pour
  l'email client et les tickets Jira (N2).
- Lire la transcription une fois ; ne pas la recopier dans la réponse ; citer seulement les extraits utiles.

## Règles
- La note Meeting est le livrable : elle peut être envoyée ou copiée telle quelle. Rien d'interne n'y entre.
- Toute action : **un seul responsable** (une personne), une échéance, un critère d'achèvement ;
  non dits en réunion → `TBD` dans le compte rendu, `[OPEN]` dans la traçabilité, jamais inventés.
- Aucune décision ni engagement attribué sans formulation explicite dans la source.
- Ne pas modifier `Teams recap`, `Transcript`, `My notes`.

Exemples d'évaluation : [evals.json](evals.json).
