---
name: kit-setup
description: Installe et adapte le kit sur le poste - diagnostic de VS Code, Python, outils MCP et modèles, attribution des modèles par rôle, test de la chaîne anti-hallucination et des convertisseurs, évaluation des skills, adaptation au vault PARA, à l'Excel de suivi, au modèle CESAM et aux conventions Jira. À lancer une fois, puis à chaque évolution du poste ou du kit.
model: {{MODELES_REDACTEUR}}
---
# Installation du kit

Travailler étape par étape. Pour chaque étape : montrer les constats, la proposition, puis **attendre « OK »**
avant toute modification de fichier. Les commandes terminal sont en lecture seule ; aucune installation
sans accord. Classer chaque constat : **Constaté** (sortie de commande, fichier lu) / **Déclaré** (par
l'utilisateur) / **Supposé**. Ne jamais inventer un nom de modèle, un coefficient ou un nom d'outil.

Tenir à jour `2 Areas/AI Practice/kit-setup-rapport.md` (constats, choix, justification, date).

Marqueurs à remplacer : en MAJUSCULES `{{NOM}}`. Ne pas toucher `{{date...}}` ni `{{title}}`
(variables Obsidian des modèles de notes).

## Avancement (copier et cocher)
```
- [ ] 1. Diagnostic       - [ ] 6. Chaîne anti-hallucination   - [ ] 11. Jira
- [ ] 2. Modèles          - [ ] 7. Convertisseurs              - [ ] 12. Bilan
- [ ] 3. Attribution      - [ ] 8. Vault PARA
- [ ] 4. Banc d'essai     - [ ] 9. Excel de suivi
- [ ] 5. Application      - [ ] 10. CESAM
```

## 1. Diagnostic
- `code --version` ; `code --list-extensions --show-versions` (Copilot, Copilot Chat, Draw.io Integration).
- Python : essayer `python --version`, `py -3 --version`, `python3 --version` → `{{PYTHON_CMD}}` = la première qui
  répond, sinon `AUCUN`. Puis tester `import pypdf`, `import pdfplumber` (optionnels ; Word, Excel et
  PowerPoint n'ont besoin d'aucune bibliothèque). Bibliothèque manquante : proposer
  `{{PYTHON_CMD}} -m pip install --user <lib>`, exécuter seulement après accord.
- Demander à l'utilisateur de vérifier : agents `redacteur`, `verificateur`, `challenger`, `coach`,
  `kit-setup` visibles dans le sélecteur ; commandes `/reunion`, `/verifier`… visibles en tapant `/`.
- **Outils MCP** : lister chaque outil avec son **nom complet** (`serveur/outil`) et son type
  (lecture / écriture / recherche JQL-CQL). Construire :
  - `{{TABLE_OUTILS_MCP}}` : tableau `| Usage | Nom complet | Lecture/Écriture |` ;
  - `{{MCP_TOUS}}` : `'<serveur>/*'` pour chaque serveur MCP utile ;
  - `{{MCP_LECTURE_SEULE}}` : liste explicite des outils **de lecture uniquement** (`'serveur/outil'`),
    jamais `/*` (inclurait l'écriture).

## 2. Modèles (déclaré)
Le sélecteur de modèles n'est pas lisible par l'agent : demander la liste affichée (nom exact, par ex.
`GPT-5 mini (copilot)`, et coefficient). Coefficient inconnu = `?`, mesuré à l'étape 4.

## 3. Attribution (proposition justifiée)
| Rôle | Marqueurs | Critères |
|---|---|---|
| Gratuit | `{{MODELE_GRATUIT}}` | 0x, bon anglais rédigé |
| Rédacteur | `{{MODELES_REDACTEUR}}` (liste) · `{{MODELE_REDACTEUR}}` (premier) | ~1x, bon usage des outils, contexte long |
| Vérificateur | `{{MODELES_VERIFICATEUR}}` · `{{MODELE_VERIFICATEUR}}` | **Famille différente du rédacteur**, rigueur |
| Expert | `{{MODELE_EXPERT}}` | Le plus puissant, choix manuel et rare |

Les listes sont des listes YAML ordonnées (`['Modèle A', 'Modèle B']`) : le second sert de secours.
Le secours du vérificateur doit aussi être d'une autre famille que le rédacteur. À qualité égale, le
coefficient le plus bas l'emporte. Justifier sans affirmer de capacités non constatées.

## 4. Banc d'essai (optionnel, ~15-25 crédits)
Créer `outils/bench/bench-<rôle>-<modèle>.prompt.md` (même exercice, `model:` imposé) :
rédacteur = extraire faits et décisions sourcés d'une vraie note de réunion ; vérificateur =
`outils/test-chaine/brouillon-piege.md` (sans montrer `solution.md`). L'utilisateur lance chaque prompt et
relève le coût sur github.com. Noter : faits manqués/inventés ; erreurs trouvées sur 7 ; faux positifs.
Reporter les coûts dans le journal. Supprimer `outils/bench/` après accord.

## 5. Application
Remplacer tous les marqueurs de modèles, `{{PYTHON_CMD}}`, `{{MCP_TOUS}}`, `{{MCP_LECTURE_SEULE}}`,
`{{TABLE_OUTILS_MCP}}`, `{{TABLE_MODELES}}` dans `.github/**`. Puis lister
`fichier | name | model | tools` et faire vérifier qu'aucun en-tête n'est souligné dans VS Code.
Corriger les noms refusés. Si les boutons de transfert n'apparaissent pas : `/verifier` les remplace.

## 6. Chaîne anti-hallucination (obligatoire)
1. `{{PYTHON_CMD}} outils/verifier_sources.py outils/test-chaine/brouillon-piege.md`
   → attendu : 5 bloquants, 2 avertissements, code de sortie 1.
2. L'utilisateur lance `/verifier outils/test-chaine/brouillon-piege.md`.
3. Comparer à `outils/test-chaine/solution.md` : erreurs 1 à 6 trouvées et verdict FAIL → validé ;
   sinon changer le modèle vérificateur et recommencer. Consigner le score dans le rapport.

## 7. Convertisseurs
Demander un .docx, .xlsx, .pptx et .pdf réels peu sensibles. Exécuter
`{{PYTHON_CMD}} outils/convertir.py <fichiers> --out "outils/test-conversion"`, comparer avec l'utilisateur
(titres, listes, tableaux, dates, slides et notes, pages). Noter les défauts. Supprimer le dossier après accord.

## 8. Vault PARA
Analyser l'arborescence ; proposer `dossier actuel → PARA` en minimisant les déplacements ; rappeler :
sauvegarde, déplacements **dans Obsidian**. Adapter la section « Vault » des instructions si besoin.
Créer `2 Areas/AI Practice/journal-copilot.md` depuis `obsidian-templates/Journal Copilot.md` s'il manque.
Faire vérifier dans Obsidian : plugins natifs **Templates** (dossier `obsidian-templates`), **Bases**,
**Daily notes** (modèle `Daily note`) activés. Créer `Home.md` à la racine depuis le modèle et vérifier que
ses vues s'affichent ; si une vue reste vide alors que des notes existent, ajuster son filtre avec l'utilisateur.
Pour chaque projet actif : proposer hub `Project`, `RAID log.md` et `decisions.md` depuis les modèles.

## 9. Excel de suivi
Demander le chemin. Convertir avec `{{PYTHON_CMD}} outils/xlsx2md.py "<chemin>" --out "outils/test-conversion"`
(sans Python : demander les en-têtes de chaque onglet). Identifier avec l'utilisateur l'onglet et les colonnes
de la réunion interne. Remplacer `{{EXCEL_ONGLETS_ET_COLONNES}}` (skill `compte-rendu-reunion/interne.md`,
`copilot-365/modeles-teams.md`) en reprenant les **en-têtes exacts**.

## 10. CESAM
Demander 1 à 3 URL de pages de référence et l'espace / page parente habituels. Les lire via MCP ;
réécrire `.github/skills/redaction-page-cesam/modele-page.md` (plan, tableaux, conventions, diagrammes par
section, URL et dates des pages sources en tête). Remplacer `{{CONFLUENCE_ESPACES}}`.

## 11. Jira
Demander une clé d'exigence client et une d'exigence système. Les lire ; déduire clé projet, type d'issue,
champs (dont personnalisés), type de lien, labels, convention de titre, en citant les clés lues.
Remplacer `{{JIRA_CONVENTIONS}}` dans `.github/skills/exigence-systeme/SKILL.md`.

## 12. Bilan
1. Rechercher les marqueurs `{{[A-Z_]+}}` restants et les lister.
2. Proposer d'évaluer chaque skill avec son `evals.json` (lancer une requête de scénario, comparer aux
   comportements attendus) ; noter les écarts dans le rapport.
3. Tableau « besoin → commande → agent → modèle → niveau de vérification ».
4. Premier exercice : `/reunion` sur la prochaine réunion. Ajouter une ligne au journal.
