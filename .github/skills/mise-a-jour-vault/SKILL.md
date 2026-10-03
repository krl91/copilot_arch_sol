---
name: mise-a-jour-vault
description: Met à jour le second cerveau Obsidian (PARA) à partir d'une nouvelle source (réunion, email, document converti, page Confluence) - extrait les faits, les classe nouveau / confirmé / en conflit avec les notes Topic existantes, propose les modifications et le journal des décisions, liste les documents à mettre à jour. À utiliser après un compte rendu de réunion ou sur « mets à jour le vault ».
user-invocable: false
---
# Mise à jour du vault

Principe : une note Topic décrit **l'état actuel** d'un sujet ; `decisions.md` est un **journal** (ajout
seulement) ; réunions, emails et documents convertis sont les **sources**. Un fait remplacé est barré, daté
et lié, jamais supprimé : `~~Max image size: 1 MB [S1]~~ → superseded 2026-09-12 by [S4]`.
Les numéros `[Sx]` d'une note ne sont jamais réutilisés.

## Déroulé (copier et cocher)
```
- [ ] 1. Faits durables extraits avec citation
- [ ] 2. Notes Topic concernées trouvées
- [ ] 3. Tableau nouveau / confirmé / conflit présenté
- [ ] 4. OK de l'utilisateur (tout ou par numéro)
- [ ] 5. Notes Topic, decisions.md, RAID, hub projet, Person/Customer mis à jour
- [ ] 6. Contrôle automatique : 0 bloquant sur chaque note modifiée
- [ ] 7. Docs à mettre à jour ajoutés au hub projet
```

1. **Extraire** (pour une réunion : depuis la note Meeting, sources prises dans ses working notes) les faits durables (exigences, valeurs, choix, contraintes, interfaces, responsabilités, jalons)
   et les décisions, chacun avec sa citation. Ignorer le bavardage.
2. **Chercher** la note Topic concernée dans le projet, puis dans `3 Resources/` si le fait est générique.
3. **Classer** — `| # | Note Topic | 🆕 New / ✅ Confirmed / ⚠️ Conflict | Existant (source, date) | Nouveau (source, date) | Proposition |`.
   En conflit, indiquer la source qui fait autorité (contrat > spec validée > workshop > email > discussion)
   et si une confirmation est nécessaire ; dans ce cas, ajouter une question `[OPEN]` au lieu de trancher.
4. **Attendre l'accord.**
5. **Appliquer** (modèles dans `obsidian-templates/`, contenu en anglais) :
   - note **Topic** : fait dans `Key facts`, ligne dans `Change history`, `last_verified` à jour ;
   - **decisions.md** : une ligne par décision ; décision structurante (architecture, périmètre, interface)
     → proposer aussi une note **Decision** (format MADR) liée dans la colonne `Record` ;
   - **RAID log** : nouveau risque (cause → événement → effet, P, I, score), hypothèse à valider, issue,
     dépendance ;
   - **hub Project** : `Status` si l'avancement change (les actions sont consolidées par `/suivi` dans le Project tracker) ;
   - **Person / Customer** : section `Commitments` pour tout engagement pris envers ou par cette personne/ce client.
6. **Contrôler** : `{{PYTHON_CMD}} outils/verifier_sources.py "<note>"` → corriger → relancer.
7. **Docs impactés** : ajouter les pages Confluence / documents concernés à `## Docs to update` du hub projet.

Ne créer aucun dossier, ne déplacer aucun fichier. Exemples d'évaluation : [evals.json](evals.json).
