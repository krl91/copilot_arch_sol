# Mode d'emploi – Kit Copilot Architecte Solution

> Pour : architecte solution fonctionnel, smart metering.
> Outils : VS Code + GitHub Copilot + MCP Jira/Xray/Confluence · Copilot 365 · Obsidian (PARA) · Python.
> Les noms exacts de certains menus VS Code / Teams changent selon les versions : quand un
> libellé diffère, cherche le mot-clé indiqué entre « guillemets ».

## Sommaire
1. [Ce que fait le kit (5 min)](#1-ce-que-fait-le-kit)
2. [Comprendre les briques Copilot (2 min)](#2-comprendre-les-briques-copilot)
3. [Prérequis](#3-prérequis)
4. [Installation pas à pas](#4-installation-pas-à-pas)
5. [Configuration (agent kit-setup)](#5-configuration-avec-lagent-kit-setup)
6. [Utilisation au quotidien – scénarios](#6-utilisation-au-quotidien)
7. [Référence : chaque fichier du kit](#7-référence--chaque-fichier-du-kit)
8. [Convertisseurs Word / Excel / PowerPoint / PDF](#8-convertisseurs-word--excel--powerpoint--pdf)
9. [Crédits : budget et règles](#9-crédits--budget-et-règles)
10. [Bonnes pratiques de senior et accompagnement d'équipe](#10-bonnes-pratiques-de-senior-et-accompagnement-déquipe)
11. [Dépannage](#11-dépannage)
12. [Principes de conception et sources d'inspiration](#12-principes-de-conception-et-sources-dinspiration)

---

## 1. Ce que fait le kit

```
             CAPTURER                    ORGANISER / DISTILLER                 PRODUIRE (EXPRESS)
  Teams + Copilot 365 (récap)  ─┐
  Emails (Outlook Copilot)     ─┼─►  Vault Obsidian (PARA)  ◄──►  VS Code + Copilot  ─►  Jira / Xray / Confluence
  Word/Excel/PPT/PDF (/convertir)┘   notes Topics = état actuel      agents, skills,        email client, revues
                                     decisions.md = journal          prompts /...
                                                 ▲                         │
                                                 └── chaîne de validation : sources [Sx] → contrôle
                                                     automatique → vérificateur (2e modèle) → ton OK
```

Trois principes :
1. **Le bon outil au bon endroit** : Copilot 365 pour capter (réunions, emails, SharePoint,
   Excel) – il ne consomme pas tes crédits GitHub ; GitHub Copilot pour produire et relier
   (Jira, Confluence, vault).
2. **Le vault est la mémoire fiable** : chaque fait a une source datée ; les faits périmés sont
   barrés, jamais effacés.
3. **Rien ne sort sans preuve** : tout livrable diffusé est sourcé, vérifié par un second modèle,
   et validé par toi.

---

## 2. Comprendre les briques Copilot

| Brique | Analogie | Fichier | Qui la déclenche | Dans le kit |
|---|---|---|---|---|
| **Instructions** | La fiche de poste donnée à l'IA | `.github/copilot-instructions.md` | Automatique, à chaque requête | Contexte, langues, PARA, sources, posture |
| **Prompt** (commande `/`) | Une recette | `.github/prompts/*.prompt.md` | Toi, en tapant `/nom` | `/reunion`, `/exigence`, `/convertir`… |
| **Agent** | Un collègue spécialisé (rôle + outils + modèle) | `.github/agents/*.agent.md` | Toi, dans le sélecteur d'agents | redacteur, verificateur, challenger, coach, kit-setup |
| **Skill** | Un classeur de procédure + modèles | `.github/skills/<nom>/SKILL.md` | L'IA, quand le sujet correspond, ou une commande `/` | compte-rendu-reunion, mise-a-jour-vault, exigence-systeme, redaction-page-cesam, conversion-documents |
| **MCP** | Les mains (accès aux outils externes) | Configuration VS Code (déjà en place) | L'IA, quand elle a besoin d'agir | Jira, Xray, Confluence |
| **Hook** | Un automatisme « à chaque fois que… » | Configuration VS Code | Automatique | Non utilisé (pas nécessaire) |

**À retenir**
- Un **skill ne choisit pas son modèle** : il tourne avec le modèle actif. Chaque skill a donc une commande `/`
  d'entrée qui impose l'agent et le modèle — **passe par la commande**. Les skills sont masqués du menu `/`
  (`user-invocable: false`) pour éviter les doublons.
- Un agent peut appeler un **sous-agent** : le rédacteur appelle lui-même le vérificateur, qui tourne avec
  **son propre modèle** et **sans l'historique** de la rédaction (vérification réellement indépendante).
- Le champ `model:` d'un agent est une **liste par ordre de préférence** : le second modèle sert de secours.

---

## 3. Prérequis

| ✔ | Élément | Comment vérifier |
|---|---|---|
| ☐ | VS Code à jour | Aide → À propos (ou « Check for Updates ») |
| ☐ | Extension **GitHub Copilot** / **Copilot Chat** à jour, connecté | Icône Copilot en bas à droite, pas d'erreur |
| ☐ | Ton serveur **MCP** Jira/Xray/Confluence opérationnel | Palette (`Ctrl+Shift+P`) → « MCP: List Servers » → statut *Running* |
| ☐ | Ton vault Obsidian (sauvegardé) | — |
| ☐ | **Python 3.9+** (fortement recommandé) | Terminal VS Code (`Ctrl+ù` ou `Ctrl+\``) → `python --version` ou `py -3 --version` |
| ☐ | `pypdf` (pour les PDF) | `python -m pip install --user pypdf` (si le poste l'autorise) |
| ☐ | Licence Copilot 365 (Teams, Outlook, Excel) | Icône Copilot dans Teams/Outlook |

Sans Python : tout fonctionne sauf les convertisseurs et le contrôle automatique des sources
(les agents le font alors à la main, moins fiablement).
Sans `pypdf` : Word, Excel et PowerPoint se convertissent quand même (aucune bibliothèque requise).

---

## 4. Installation pas à pas

### 4.1 Sauvegarder le vault
Copie le dossier du vault ailleurs (ou zip). Le kit ne supprime rien, mais c'est une bonne pratique.

### 4.2 Copier le kit dans le vault
1. Décompresse `kit-copilot-architecte.zip`.
2. Copie **le contenu** du dossier `kit-copilot-architecte/` à la **racine du vault** :
   ```
   MonVault/
   ├── .github/            ← agents, prompts, skills, instructions
   ├── copilot-365/        ← modèles Teams et prompts Copilot 365
   ├── obsidian-templates/ ← modèles de notes
   ├── outils/             ← scripts Python
   ├── MODE-EMPLOI.md
   ├── README.md
   └── (tes dossiers existants…)
   ```
3. Sur Mac, le dossier `.github` est caché : `Cmd+Maj+.` dans le Finder pour le voir.
   Sur Windows, il est visible.
4. Respecte les règles internes de transfert de fichiers : le kit ne contient aucune donnée
   d'entreprise, seulement des textes et scripts.

### 4.3 Ouvrir le vault dans VS Code
1. VS Code → **Fichier → Ouvrir le dossier…** → sélectionne le dossier du vault.
2. Si VS Code demande « Do you trust the authors? » → **Yes, I trust** (sinon les agents et
   le terminal sont bridés).
3. Ouvre le chat Copilot : icône Copilot ou `Ctrl+Alt+I` (Mac : `Ctrl+Cmd+I`).

### 4.4 Activer les fonctions du kit dans VS Code
Ouvre les paramètres (`Ctrl+,`) et vérifie, en tapant ces mots-clés dans la recherche :
- « **instruction files** » → l'utilisation des fichiers d'instructions est **activée** ;
- « **prompt files** » → activé ;
- « **agent skills** » (ou « skills ») → activé ;
- « **custom agents** » / « chat modes » → activé si l'option existe.

Contrôle :
- tape `/` dans le chat → tu dois voir `reunion`, `exigence`, `convertir`, `verifier`, `challenge`… ;
- ouvre le sélecteur d'agents (liste déroulante sous la zone de saisie, où figurent
  *Ask / Agent*) → tu dois voir `redacteur`, `verificateur`, `challenger`, `coach`, `kit-setup`.

### 4.5 Préparer Python (si autorisé)
Dans le terminal VS Code, à la racine du vault :
```bash
python --version
```
```bash
python -m pip install --user pypdf pdfplumber
```
Si `python` n'est pas reconnu sous Windows, essaie `py -3 --version`. Si pip est bloqué
par le proxy ou la politique du poste : demande au support IT, ou passe-toi des PDF.

### 4.6 Obsidian
1. Paramètres → **Plugins natifs** : activer **Templates** (dossier : `obsidian-templates`), **Bases**
   (vues dynamiques des modèles Project, Person, Customer, Home, Weekly review) et **Daily notes**
   (modèle : `obsidian-templates/Daily note`, dossier : `0 Inbox` ou `2 Areas/Daily`).
   Aucun plugin communautaire n'est nécessaire.
   Option : crée `Home.md` à la racine depuis le modèle `Home` et épingle-la comme page d'accueil.
2. Optionnel, pour ne pas polluer la recherche : Paramètres → Fichiers et liens →
   **Fichiers exclus** → ajoute `outils/` et `copilot-365/`.
3. Crée (si absents) les dossiers PARA : `0 Inbox`, `1 Projects`, `2 Areas`, `3 Resources`,
   `4 Archives` — l'agent kit-setup te proposera une correspondance avec l'existant
   (les déplacements se font **dans Obsidian**, pour que les liens suivent).

### 4.7 Teams et Copilot 365
1. Ouvre `copilot-365/modeles-teams.md` : crée les 3 modèles de récapitulatif dans Teams
   (chercher « modèle » / « template » dans le récap Copilot d'une réunion ou dans ses paramètres).
2. Ouvre `copilot-365/prompts-copilot-365.md` : enregistre les prompts dans Copilot 365
   (prompts enregistrés / favoris) si la fonction existe chez vous.

### 4.8 Lancer la configuration
Passe à la section 5. Compte **45 à 90 minutes** et **~15 à 40 crédits** (avec banc d'essai).

---

## 5. Configuration avec l'agent kit-setup

1. Chat Copilot → sélecteur d'agents → **kit-setup**.
2. Écris : `Installe le kit`.
3. L'agent avance étape par étape et **attend ton OK avant chaque modification** :

| Étape | Ce qu'il fait | Ce que tu fais |
|---|---|---|
| 1. Diagnostic | VS Code, extensions, Python, bibliothèques, **noms complets des outils MCP** (lecture / écriture) | Autorises les commandes (lecture seule) ; vérifies agents et `/` |
| 2. Modèles | Te demande la liste du sélecteur + coefficients | Copies-colles la liste exacte |
| 3. Attribution | Listes par rôle : gratuit, rédacteur, vérificateur (autre famille), expert, avec secours | Valides ou ajustes |
| 4. Banc d'essai (option) | Prompts de test par modèle | Lances chaque prompt, relèves le coût |
| 5. Application | Écrit modèles, outils et Python dans tous les fichiers | Vérifies qu'aucun en-tête n'est souligné |
| 6. Chaîne anti-hallucination | Script + vérificateur sur le brouillon piégé (7 erreurs) | Lances `/verifier outils/test-chaine/brouillon-piege.md` |
| 7. Convertisseurs | Convertit un docx, xlsx, pptx et pdf réels | Fournis 4 fichiers peu sensibles, compares |
| 8. Vault PARA | Correspondance dossiers actuels → PARA | Déplaces dans Obsidian |
| 9. Excel de suivi | Convertit le fichier, repère onglet et colonnes | Indiques l'onglet de la réunion interne |
| 10. CESAM | Lit 1 à 3 pages de référence → modèle réel | Donnes les URL |
| 11. Jira | Lit une exigence client + une système → conventions | Donnes 2 clés |
| 12. Bilan | Marqueurs restants, **évaluation des skills** (`evals.json`), tableau d'usage | Fais le 1er exercice |

Tout est tracé dans `2 Areas/AI Practice/kit-setup-rapport.md`.

**Modifier plus tard** :
- changer un modèle → ouvre le fichier `.agent.md` / `.prompt.md`, modifie la ligne `model:` ;
- relancer une étape → agent kit-setup : `Refais l'étape 9 avec cette nouvelle page : <URL>`.

---

## 6. Utilisation au quotidien

> Les deux workflows clés (réunion → compte rendu professionnel, suivi de projet) sont détaillés pas à pas,
> avec qui fait quoi, dans **[WORKFLOWS.md](WORKFLOWS.md)**.

### Routine type

| Moment | Action | Outil | Coût GitHub |
|---|---|---|---|
| Matin (5 min) | Note `Daily note` (top 3) + tri des emails → faits importants dans `0 Inbox/` | Obsidian + Outlook Copilot | 0 |
| Avant une réunion (5 min) | Note `Meeting`, section `Prep` (objectif, questions, engagements à ne pas prendre) | Obsidian | 0 |
| Avant réunion interne | Mes tâches en retard / à échéance | Excel Copilot | 0 |
| Après chaque réunion | `/reunion` puis `/suivi <projet>` | VS Code | ~2-4 |
| Tâche surprise | `/cadrer-demande` → `/recherche` + Copilot 365 | VS Code + 365 | ~1-2 |
| Document reçu | `/convertir` | VS Code | 0 (gratuit) |
| Rédaction | `/exigence`, `/page-cesam`, `/revue-couverture` → Vérifier | VS Code | ~3-6 par livrable |
| Après une tâche notable | `/journal` | VS Code | 0 |
| Vendredi (45-60 min) | Note `Weekly review` (GTD : get clear / current / creative), RAID, statuts projets, puis coach : `bilan de la semaine` | Obsidian + VS Code | 1 |
| Fin de mois | Coach : `audit du vault`, `bilan du mois` | VS Code | 2 |

### Scénario A – Réunion interne (avec le fichier Excel de suivi)

**Principe : deux notes liées par réunion.**
| Note | Contenu | Diffusion |
|---|---|---|
| `<titre>` (modèle `Meeting`) | Compte rendu : synthèse, décisions, actions, revue des actions précédentes, discussion, prochaine réunion | **Diffusable telle quelle** |
| `<titre> (working notes)` (modèle `Meeting working notes`) | Préparation privée, récap Teams, transcription, tes notes, contrôle de compréhension, traçabilité, brouillon d'email, sources | **Jamais diffusée** |

1. **Avant** : nouvelle note dans `1 Projects/<Projet>/Meetings/` → modèle `Meeting` (`meeting_type: internal`,
   `project:`, objectif et ordre du jour). Clique sur le lien des working notes → modèle `Meeting working notes` →
   remplis `Prep (private)` : tes questions et les **engagements à ne pas prendre**.
2. **Teams** : transcription activée ; après la réunion, récap Copilot avec le modèle *Internal*.
3. **Working notes** : colle le récap dans `Teams recap`, la transcription utile dans `Transcript`, tes impressions
   dans `My notes`.
4. **VS Code** : ouvre la note Meeting → `/reunion`.
5. Tu obtiens :
   - dans la **note Meeting** : synthèse, décisions, actions (responsable + échéance), **mises à jour à reporter
     dans l'Excel**, revue des actions précédentes, discussion par point, prochaine réunion — chaque élément
     avec un ID (D1, A1…) ;
   - dans les **working notes** : tes notes **mises au propre** (classées par sujet, complétées par le récap et
     la transcription), contrôle de compréhension, **contrôle de cohérence** avec ce que le projet sait déjà,
     traçabilité (ID → source), sources.
6. Contrôle automatique : `verifier_compte_rendu.py` garantit que la note Meeting ne contient **rien d'interne**
   et que chaque élément est tracé.
7. Enchaînement `mise-a-jour-vault` : faits nouveaux / confirmés / **en conflit** → tu valides.
8. **Excel Copilot** : colle la liste « Updates to apply » (prompt dans `copilot-365/`) → vérifie → applique.
9. **Diffusion** : envoie la note Meeting **sous 24 h** aux participants **et aux absents** → `minutes_status: sent`.
10. `/suivi <projet>` : le registre des actions du projet est mis à jour (voir [WORKFLOWS.md](WORKFLOWS.md)).
11. `/journal` : « CR réunion projet X, 45 min sans, 15 min avec, 2 requêtes ».

### Scénario B – Workshop client (anglais)
Comme A avec `meeting_type: customer-workshop`. En plus :
- section **Commitments made by our side** et **Potential scope changes** : à relire en priorité ;
- **brouillon d'email « minutes for confirmation »**, écrit dans les working notes à partir de la seule
  note Meeting → c'est un livrable **N2** : clique
  **🔍 Vérifier les sources** (ou `/verifier`), corrige, puis envoie depuis Outlook.

### Scénario C – Handover
`meeting_type: handover`. Le résultat inclut une **checklist de complétude** et la liste de ce qui manque
pour être autonome, rédigée en questions prêtes à envoyer.

### Scénario D – Tâche surprise (« tu peux me dire comment marche X ? »)
1. `/cadrer-demande` → colle la demande → reformulation, **questions à poser tout de suite**,
   estimation (gratuit).
2. `/recherche` → la question → vault puis Confluence puis Jira, réponse avec **sources datées**,
   contradictions, niveau de confiance, et **un prompt prêt à coller dans Copilot 365**.
3. Copilot 365 → colle le prompt → complète avec SharePoint / emails / Teams.
4. Retour dans VS Code : « ajoute ces éléments à la fiche réponse » → fiche dans le vault.
   **La prochaine fois, la réponse est déjà là.**
5. `/journal` avec le type `surprise` → le coach chiffrera le temps passé sur ces demandes.

### Scénario E – Exigence client → exigences système
1. `/exigence` → clé Jira de l'exigence client.
2. Le rédacteur produit dans `Drafts/` : critique de l'exigence client (+ questions au client),
   1..n exigences système (« shall », critères d'acceptation, méthode de vérification, vue CESAM),
   avec sources.
3. Le rédacteur appelle **automatiquement** le sous-agent vérificateur (sinon bouton **🔍 Vérifier les sources**
   ou `/verifier`) → rapport → corrections → nouveau contrôle.
4. Ton OK → création des tickets et des liens de traçabilité dans Jira.

### Scénario F – Page Confluence CESAM
- Adapter : `/page-cesam` → « adapte <URL> pour le projet X » → tableau d'adaptation (garder /
  adapter / supprimer) → brouillon → vérification → OK → publication.
- Créer : « nouvelle page CESAM sur <sujet> » → brouillon à partir des Topics, décisions et exigences.
- Diagrammes : Mermaid dans le brouillon ; sur demande, fichier `.drawio` à finaliser à la main.
- Spec Word : **export Confluence** (pas de régénération par IA).

### Scénario G – Revue d'une spec produit ou d'un plan de test
`/revue-couverture` → exigences système + document → matrice de couverture, commentaires
`[Major|Minor|Question]` en anglais prêts à coller → **Vérifier** avant d'envoyer.

### Scénario H – Utiliser un Word / Excel / PowerPoint / PDF comme source
`/convertir` → chemin du fichier → markdown dans `0 Inbox/Converted/` → tu le classes →
les agents peuvent le citer (`[Sx] DOC fichier.pdf p.12 …`). Détails en section 8.

### Scénario I – Bilan du vendredi
Agent **coach** → `bilan de la semaine` → gains, gaspillages, répétitions à automatiser,
tâches surprises, erreurs attrapées par la vérification, 3 actions, 2 questions.

### Scénario J – Se préparer : challenge et teach-back
- Avant un comité ou une décision : `/challenge` + la décision ou la page → une objection à la fois, tu
  défends, puis « fin » → synthèse (robustesse, défenses, vulnérabilités restantes).
- Avant un workshop ou après un handover : `/teach-back` + le sujet → tu expliques, l'agent compare aux
  sources du vault et te questionne sur les écarts → tableau des écarts et questions à poser.

---

## 7. Référence : chaque fichier du kit

### `.github/` – lu par Copilot

**Instructions**
| Fichier | Rôle | À modifier ? |
|---|---|---|
| `copilot-instructions.md` | Contexte, posture senior, langues, **terminologie**, PARA, convention de sources, **méthode anti-hallucination**, niveaux N0/N1/N2, outils MCP, modèles | Oui, quand ton contexte change |

**Agents** (`agents/`)
| Fichier | Rôle | Outils | Utilisation |
|---|---|---|---|
| `kit-setup.agent.md` | Installation et adaptation (12 étapes) | Tous | Une fois, puis à chaque évolution |
| `redacteur.agent.md` | Livrables sourcés ; appelle le vérificateur en sous-agent ; publie après OK | Lecture, édition, terminal, MCP, sous-agent | Via les commandes `/reunion`, `/exigence`… |
| `verificateur.agent.md` | Vérification indépendante, verdict PASS / FIX / FAIL + limites | **Lecture seule** | Automatique, bouton ou `/verifier` |
| `challenger.agent.md` | Avocat du diable et teach-back | Lecture seule | `/challenge`, `/teach-back` |
| `suivi-projet.agent.md` | Registre des actions, jalons et planning, attentes, rapprochement Excel, relances, rapport d'avancement | Lecture, édition, terminal, MCP lecture, sous-agent | `/suivi`, `/point-projet`, `/rapport-avancement` |
| `coach.agent.md` | Bilans, audit du vault, fiches équipe, **création de skills** | Lecture, édition | Vendredi, fin de mois |

**Commandes** (`prompts/`)
| Commande | Agent · modèle | Niveau | Usage |
|---|---|---|---|
| `/reunion` | redacteur · rédacteur | N1 / N2 | Après chaque réunion |
| `/maj-vault` | redacteur · rédacteur | N1 | Nouvelle info hors réunion |
| `/exigence` | redacteur · rédacteur | N2 | Exigence client à décliner |
| `/page-cesam` | redacteur · rédacteur | N2 | Page Confluence de conception |
| `/recherche` | redacteur · rédacteur | N1 | Besoin d'information |
| `/revue-couverture` | redacteur · rédacteur | N2 | Relecture spec / plan de test |
| `/verifier` | verificateur · vérificateur | — | Vérification manuelle |
| `/challenge`, `/teach-back` | challenger · rédacteur | N0 | Préparation |
| `/suivi` | suivi-projet · rédacteur | N1 | Après chaque compte rendu, revue hebdo |
| `/point-projet` | suivi-projet · rédacteur | N0 | Où en est le projet |
| `/rapport-avancement` | suivi-projet · rédacteur | N2 | Reporting, comité |
| `/cadrer-demande` | ask · gratuit | N0 | Tâche surprise |
| `/email` | agent · gratuit | N0 → N2 si client | Email technique |
| `/convertir` | agent · gratuit | — | Document reçu |
| `/journal` | agent · gratuit | — | Mesure du temps gagné |

**Skills** (`skills/`) — chacun : `SKILL.md` (déroulé à cocher) + fichiers de référence + `evals.json` (3 scénarios de test)
| Skill | Références | Entrée |
|---|---|---|
| `compte-rendu-reunion` | `regles-compte-rendu.md` (structure, style, diffusion), `interne.md`, `workshop-client.md`, `handover.md` (formats de sortie) | `/reunion` |
| `mise-a-jour-vault` | — | `/maj-vault`, après `/reunion` |
| `exigence-systeme` | `regles-redaction.md` (règles INCOSE), `exemples.md` | `/exigence` |
| `redaction-page-cesam` | `modele-page.md` (plan CESAM), `diagrammes-drawio.md` (Mermaid, draw.io, export) | `/page-cesam` |
| `conversion-documents` | — (scripts dans `outils/`) | `/convertir`, ou dès qu'un fichier Office/PDF est cité |

À adapter : les formats de sortie (`interne.md`…) si ton format change ; `modele-page.md`, conventions
Jira et Excel via kit-setup ; le reste ne se modifie qu'avec le coach (« améliorer le skill … »).

### `obsidian-templates/` – modèles de notes

Chaque modèle a une propriété `type` qui alimente les vues Bases et les skills. Contenu en anglais,
consignes en commentaires `<!-- -->` (invisibles en lecture).

| Modèle | Inspiré de | Usage | Emplacement |
|---|---|---|---|
| `Home.md` | Note d'accueil (LYT, Nick Milo) | Tableau de bord : projets actifs, réunions à traiter, sujets à vérifier, décisions en attente, Inbox | Racine du vault |
| `Project.md` | PARA / BASB (résultat + échéance, « intermediate packets ») + fiche projet PMI/PRINCE2 | Hub projet : outcome, périmètre, statut RAG, jalons, parties prenantes, actions, RAID, vues décisions/sujets/réunions, docs, retour d'expérience | `1 Projects/<P>/_<P>.md` |
| `Meeting.md` | Minutes structurées (awesome-copilot `meeting-minutes`, règles de compte rendu) | **Compte rendu diffusable** : objectif, synthèse, décisions, actions, revue des actions précédentes, discussion, prochaine réunion, suivi — lien vers les working notes | `1 Projects/<P>/Meetings/` |
| `Meeting working notes.md` | Séparation livrable / matériau de travail | **Privée** : préparation (questions, engagements à ne pas prendre), récap Teams, transcription, notes personnelles, **notes mises au propre**, contrôle de compréhension, **contrôle de cohérence projet**, traçabilité, brouillon d'email, sources | `1 Projects/<P>/Meetings/` |
| `Project tracker.md` | Registre d'actions, Gantt, « waiting for » (GTD) | Registre des actions généré par script, mises à jour hors réunion, attentes, jalons et planning, décisions attendues, historique des rapports | `1 Projects/<P>/Project tracker.md` |
| `Topic.md` | Notes « evergreen » (état actuel) | Bottom line, faits sourcés, règles, interfaces, décisions, questions, historique des changements | `1 Projects/<P>/Topics/` ou `3 Resources/` |
| `Decision.md` | **MADR 4.0** (Markdown Architectural Decision Records) | Décision structurante : contexte, critères, options, décision, conséquences, confirmation | `1 Projects/<P>/Decisions/` |
| `decisions.md` | Journal de décisions | Toutes les décisions, ajout seul, lien vers la note Decision | `1 Projects/<P>/decisions.md` |
| `RAID log.md` | **RAID** (PMI / PRINCE2) | Risques (cause → événement → effet, P × I), hypothèses, issues, dépendances | `1 Projects/<P>/RAID log.md` |
| `Answer.md` | **BLUF** (« bottom line up front ») + niveaux de confiance | Fiche réponse : réponse d'abord, preuves pour/contre, confiance, manques | `Topics/` ou `3 Resources/` |
| `Person.md` | Carte des parties prenantes (grille pouvoir / intérêt) | Rôle, attentes, façon de travailler, sujets ouverts, engagements, réunions (vue) | `2 Areas/People/` |
| `Customer.md` | Domaine PARA | Contexte client, paysage technique (HES, MDM, communication, normes), contrats, terminologie, engagements, projets (vue) | `2 Areas/<Client>.md` |
| `Area.md` | Domaine PARA | Responsabilité continue : niveau d'exigence, projets actifs (vue), revue | `2 Areas/` |
| `Handover pack.md` | Passation de connaissances | Dossier quand je transmets : statut, décisions, engagements, RAID, 30 prochains jours, contacts, emplacements | `1 Projects/<P>/` |
| `Weekly review.md` | **Revue hebdomadaire GTD** (David Allen) | Get clear / get current / get creative + pratique IA + 3 priorités | `2 Areas/Reviews/` |
| `Daily note.md` | Note quotidienne + rituel de fin de journée | Top 3, réunions, capture rapide, demandes surprises, clôture | Dossier des notes quotidiennes |
| `Glossary.md` | Glossaire de projet | Terminologie constante (utilisée par les skills) | `3 Resources/Glossary.md` |
| `Journal Copilot.md` | — | Étalonnage, compteur mensuel, journal des gains | `2 Areas/AI Practice/journal-copilot.md` |

> Les vues `base` utilisent la syntaxe officielle d'Obsidian Bases. Si une vue reste vide alors que des
> notes existent, vérifie la propriété `type` de ces notes et le dossier (les vues de hub filtrent sur le
> dossier du projet).

### `copilot-365/`

| Fichier | Contenu |
|---|---|
| `modeles-teams.md` | 3 modèles de récap Teams (interne, workshop, handover) + astuces transcription |
| `prompts-copilot-365.md` | Recherche SharePoint/emails/Teams, tri des emails, réponse email, Excel avant/après réunion |

### `outils/` – scripts Python (lecture seule des sources, aucune connexion réseau)

| Script | Rôle | Dépendances |
|---|---|---|
| `convertir.py` | Point d'entrée : convertit fichiers/dossiers Word, Excel, PowerPoint, PDF | selon format |
| `docx2md.py` | Word → markdown | **aucune** |
| `xlsx2md.py` | Excel → markdown (un tableau par onglet) | **aucune** |
| `pptx2md.py` | PowerPoint → markdown (une section par slide, notes incluses) | **aucune** |
| `pdf2md.py` | PDF → markdown (page par page, tableaux en option) | `pypdf` (+ `pdfplumber` option) |
| `verifier_sources.py` | Contrôle automatique des sources d'un brouillon | **aucune** |
| `actions_projet.py` | Consolide les actions de toutes les réunions d'un projet : en retard, sous 7 jours, à confirmer, par responsable ; écrit le registre du Project tracker (`--ecrire`) | **aucune** |
| `verifier_compte_rendu.py` | Contrôle d'un compte rendu : rien d'interne dans la note diffusable, actions avec un responsable et une échéance, chaque élément tracé dans les working notes | **aucune** |
| `_commun.py` | Fonctions partagées des convertisseurs | — |
| `test-chaine/brouillon-piege.md` | Brouillon avec 7 erreurs plantées | — |
| `test-chaine/solution.md` | Les 7 erreurs (ne pas montrer au vérificateur) | — |
| `test-chaine/reunion-ok/`, `reunion-piege/` | Couple de notes de réunion correct / piégé (6 erreurs) | — |

---

## 8. Convertisseurs Word / Excel / PowerPoint / PDF

Pourquoi : Copilot lit mal (ou pas) les fichiers Office et PDF (supports de comité, présentations client, specs, annexes de contrat). Convertis en markdown, ils
deviennent **lisibles, cherchables et citables** dans le vault.

### Commandes (terminal VS Code, depuis la racine du vault)
Remplace `python` par `py -3` si nécessaire.
```bash
python outils/convertir.py "C:/Users/moi/Downloads/Spec FW v3.docx"
```
```bash
python outils/convertir.py "C:/Users/moi/Downloads/Annexes" -r --out "1 Projects/Alpha/Sources"
```
```bash
python outils/xlsx2md.py "Suivi.xlsx" --onglet "Actions" "Risques" --max-lignes 1000
```
```bash
python outils/pptx2md.py "Steering committee.pptx" --masquees
```
```bash
python outils/pdf2md.py "Contrat annexe B.pdf" --pages 10-25 --tableaux
```
Ou, sans taper de commande : `/convertir` dans le chat.

### Ce que tu obtiens
- Un `.md` par fichier dans `0 Inbox/Converted/` (par défaut — **jamais** à côté de l'original,
  souvent dans un dossier SharePoint partagé).
- Un en-tête avec le fichier d'origine, sa date de modification, la date de conversion, et la
  façon de le citer.
- Word : titres, listes, gras/italique, liens, tableaux ; modifications suivies acceptées.
- Excel : un tableau par onglet, dates en AAAA-MM-JJ, onglets masqués ignorés (`--masques` pour
  les inclure), troncature signalée au-delà de 500 lignes.
- PowerPoint : `## Slide N – Titre`, texte dans l'ordre de lecture, puces à niveaux, tableaux,
  **notes du présentateur** (souvent l'information la plus utile ; `--sans-notes` pour les exclure),
  diapositives masquées ignorées (`--masquees` pour les inclure), images/graphiques signalés.
- PDF : `## Page N` pour citer la page ; **PDF scanné signalé** (pas de texte inventé).

### Limites (à connaître et à dire à l'équipe)
- Formats anciens `.doc` / `.xls` / `.ppt` : réenregistrer en `.docx` / `.xlsx` / `.pptx`.
- Images, en-têtes/pieds de page, commentaires Word : non repris.
- PowerPoint : le contenu des **graphiques et SmartArt** n'est pas extrait (signalé `[graphique]` /
  `[objet]`) ; un schéma dessiné avec des formes donne seulement ses libellés.
- Excel : valeurs **calculées lors du dernier enregistrement** (formules non recalculées).
- PDF : mise en page complexe parfois approximative → **toute valeur critique se vérifie dans
  l'original**.
- Confidentialité : convertir un document le met dans ton vault ; respecte sa classification.

---

## 9. Crédits : budget et règles

- Budget : **20 000 / mois ≈ 950 par jour ouvré**. Confortable : l'enjeu est l'efficience.
- **Étalonnage** (une fois) : tableau dans le journal, après le banc d'essai de kit-setup.
- **Suivi** : chaque lundi, relève le compteur sur **github.com → Settings → Copilot / Billing**
  (l'icône VS Code se met à jour avec retard). Alerte si % consommé > % du mois + 15 points.
- **Règles** :
  1. Commandes gratuites pour cadrer, convertir, journaliser, emails simples.
  2. Un prompt complet plutôt que 5 messages ; nouveau sujet = nouveau chat.
  3. Copilot 365 d'abord pour emails, SharePoint, Teams, Excel.
  4. Modèle **expert** : choix manuel, rare, pour un vrai arbitrage.
  5. La vérification N2 coûte ~1 requête : c'est le meilleur investissement du kit.

---

## 10. Bonnes pratiques de senior et accompagnement d'équipe

### Ce que tu dois incarner
1. **Sourcer** : aucune information diffusée sans source datée. « L'IA l'a dit » n'est pas une source.
2. **Vérifier proportionnellement** : N0 / N1 / N2 selon l'impact ; tout ce qui sort est N2.
3. **Assumer** : l'IA rédige, **tu signes**. Relire est non négociable.
4. **Protéger** : pas de données personnelles, contractuelles ou clients au-delà de ce qu'autorise
   la politique de l'entreprise ; pas de copier-coller d'outils non approuvés.
5. **Tracer** : brouillons sourcés et rapports de vérification gardés dans le vault.
6. **Mesurer** : journal + bilan mensuel. Des chiffres, pas des impressions.
7. **Rester honnête** : montrer aussi les limites (PDF scannés, erreurs attrapées, cas où c'était
   plus lent).

### Accompagner une équipe hétérogène
| Niveau | Objectif | Ce que tu leur donnes |
|---|---|---|
| Débutant | Usages sûrs, confiance | Copilot 365 (récap Teams, emails), 3 interdits, 1 exemple pas à pas |
| Intermédiaire | Régularité, qualité | Prompts réutilisables, choix du modèle, convention de sources, `/verifier` |
| Avancé | Industrialisation | Instructions, agents, skills, chaîne de validation, mesure du ROI |

- Génère les supports avec le coach : `fiche équipe débutant` (ou intermédiaire / avancé).
- Montre **un avant/après réel** (réunion, exigence) plutôt qu'une démo générique.
- Montre le **test du brouillon piégé** : c'est l'argument le plus convaincant sur la fiabilité.
- Partage le kit progressivement : instructions + 2 prompts d'abord, la chaîne complète ensuite.

### Présenter le ROI à l'équipe (bilan du mois du coach)
1. Temps gagné par type de tâche (journal).
2. Erreurs attrapées avant diffusion (rapports de vérification).
3. Deux exemples concrets.
4. Limites constatées et règles d'usage.
5. Coût en crédits.

---

## 11. Dépannage

| Symptôme | Cause probable | Solution |
|---|---|---|
| Les commandes `/reunion`… n'apparaissent pas | Fichiers de prompts désactivés, ou vault non ouvert comme dossier | Section 4.4 ; *Fichier → Ouvrir le dossier* sur la racine du vault |
| Les agents n'apparaissent pas | Version de VS Code / Copilot trop ancienne ou option désactivée | Mettre à jour ; chercher « custom agents » / « chat modes » dans les paramètres |
| Ligne `model:` soulignée en jaune | Nom de modèle inexact | Copier le nom exact depuis le sélecteur ; ou demander à kit-setup |
| Ligne `tools:` ou `handoffs:` soulignée | Format différent dans ta version | Demander à kit-setup de corriger ; `/verifier` remplace le bouton |
| Le rédacteur ne lance pas le vérificateur tout seul | Sous-agents non disponibles dans ta version | Bouton « 🔍 Vérifier les sources » ou `/verifier` |
| Bouton « 🔍 Vérifier les sources » absent | Handoffs non pris en charge par ta version | Utiliser `/verifier` |
| Un skill ne se déclenche pas | Skills désactivés, ou formulation trop éloignée | Passer par la commande `/` correspondante ; demander au coach « améliorer le skill … » (description) |
| `python` non reconnu | Python absent ou pas dans le PATH | Essayer `py -3` ; sinon installer via le portail d'entreprise |
| `pip install` échoue | Proxy / politique du poste | Support IT ; Word et Excel fonctionnent sans bibliothèque |
| « pypdf absent » | Bibliothèque non installée | `python -m pip install --user pypdf` |
| PDF « aucun texte extractible » | PDF scanné | Demander la source Word, ou OCR (ouvrir le PDF dans Word) |
| Le vérificateur rate des erreurs du test | Modèle vérificateur trop faible ou même famille que le rédacteur | Changer `model:` du vérificateur (kit-setup étape 3-6) |
| Outil MCP introuvable | Serveur MCP arrêté | Palette → « MCP: List Servers » → redémarrer |
| Réponse dans la mauvaise langue | Instructions non chargées | Vérifier « instruction files » activé ; rappeler « livrable en anglais » |
| Compteur de crédits pas à jour | Délai d'actualisation de l'icône | Consulter github.com |
| Le vault « bouge » après un déplacement fait dans VS Code | Liens Obsidian non mis à jour | Toujours déplacer/renommer dans Obsidian |

---

## 12. Principes de conception et sources d'inspiration

### Principes appliqués (bonnes pratiques Anthropic)
| Principe | Application dans le kit |
|---|---|
| Concision : n'écrire que ce que le modèle ne sait pas | Instructions et skills courts ; détails dans des fichiers de référence |
| Descriptions « quoi + quand », à la troisième personne | Chaque agent, skill et commande ; mots-clés FR/EN pour le déclenchement |
| Chargement progressif, références à un seul niveau | `SKILL.md` → `interne.md`, `regles-redaction.md`, `diagrammes-drawio.md`… |
| Degré de liberté adapté | Scripts à commande exacte (conversion, contrôle) ; consignes souples pour la rédaction |
| Déroulés à cocher | Chaque skill et les agents rédacteur, vérificateur, kit-setup |
| Boucles valider → corriger → recommencer | `verifier_sources.py` jusqu'à 0 bloquant ; vérificateur → corrections → contrôle |
| Scripts qui résolvent au lieu de renvoyer l'erreur | Messages explicites (pypdf absent, PDF scanné, ancien format) ; constantes justifiées |
| Terminologie constante | Glossaire dans `copilot-instructions.md` |
| Évaluations d'abord | `evals.json` (3 scénarios) par skill ; brouillon piégé pour la chaîne |
| Noms d'outils MCP complets | Table `serveur/outil` remplie par kit-setup |
| Réduction des hallucinations : citations d'abord, droit de dire « je ne sais pas », vérification par citation, retrait des affirmations non soutenues, connaissances limitées aux sources | Méthode anti-hallucination des instructions + agent vérificateur |

### Sources d'inspiration
- Anthropic – [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- Anthropic – [Reduce hallucinations](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations)
- VS Code – [Custom agents](https://code.visualstudio.com/docs/copilot/customization/custom-agents),
  [Prompt files](https://code.visualstudio.com/docs/copilot/customization/prompt-files),
  [Agent skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills),
  [Subagents](https://code.visualstudio.com/docs/copilot/agents/subagents),
  [Tools reference](https://code.visualstudio.com/docs/agents/reference/tools-reference)
- GitHub – [awesome-copilot](https://github.com/github/awesome-copilot) : skills `meeting-minutes`
  (actions avec critère d'achèvement, parking lot), `drawio` (styles, export), `convert-*-to-md`
  (description « déclencheur », conversion systématique), `verify-agent-action` (preuves pour/contre,
  indépendance des vérificateurs, « limites ») ; agents `devils-advocate` et `demonstrate-understanding` (challenger).
- Modèles de notes : [MADR](https://adr.github.io/madr/) (décisions d'architecture) ;
  [GTD Weekly Review](https://gettingthingsdone.com/wp-content/uploads/2014/10/Weekly_Review_Checklist.pdf)
  (David Allen) ; PARA et *Building a Second Brain* ([Forte Labs](https://fortelabs.com/blog/the-official-second-brain-note-template/)) ;
  RAID log (PMI / PRINCE2) ; [Obsidian Bases](https://obsidian.md/help/bases) (vues dynamiques natives).
- INCOSE – *Guide to Writing Requirements* (règles d'exigences ; se référer au guide officiel pour la numérotation).
- Microsoft – [MarkItDown](https://github.com/microsoft/markitdown) : alternative reconnue de conversion
  (`pip install 'markitdown[all]'`, gère aussi .msg, .html, .epub). Le kit utilise ses propres scripts
  sans dépendance, avec repères de citation (page, slide, onglet).

