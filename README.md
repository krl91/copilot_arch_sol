# Kit Copilot – Architecte solution smart metering

Kit pour travailler avec **GitHub Copilot (VS Code) + MCP Jira/Xray/Confluence**, **Copilot 365** et un
**second cerveau Obsidian (PARA)** : comptes rendus professionnels, suivi de projet, exigences, pages CESAM,
avec une **chaîne de validation anti-hallucination** et des **convertisseurs Word / Excel / PowerPoint / PDF**.

## Le quotidien en 1 minute

**Après une réunion — 2 requêtes**
1. Pendant : transcription Teams activée, tes notes dans la note *working notes*.
2. Après : colle le récap Copilot Teams et la transcription dans les *working notes* (0 crédit GitHub).
3. `/reunion` → notes mises au propre, contrôles de compréhension et de cohérence, compte rendu diffusable,
   actions avec responsable et échéance (**1 requête**).
4. Relis, réponds « OK » → vault et registre des actions mis à jour (**1 requête**).
5. Envoie la note Meeting sous 24 h aux participants et aux absents.

**Suivi de projet — souvent gratuit**
- Actions en retard, de la semaine, à confirmer : `python outils/actions_projet.py "1 Projects/<P>"` (0 crédit).
- Jalons et planning : `/suivi <P>` une fois par semaine · état du projet : `/point-projet <P>` ·
  reporting : `/rapport-avancement <P>`.

**Économie** : une commande complète plutôt qu'une conversation · un nouveau chat par sujet · scripts pour
calculer et contrôler · Copilot 365 pour capter · vérification seulement pour ce qui sort.

👉 Pas à pas et coût de chaque étape : **[WORKFLOWS.md](WORKFLOWS.md)** ·
installation, configuration et référence de chaque fichier : **[MODE-EMPLOI.md](MODE-EMPLOI.md)**.

## Démarrage en 6 étapes
1. Sauvegarde ton vault.
2. Copie le contenu de ce dossier à la racine du vault.
3. VS Code → *Fichier → Ouvrir le dossier* → le vault → faire confiance au dossier.
4. Vérifie dans les paramètres : « instruction files », « prompt files », « agent skills » activés.
5. Chat Copilot → agent **kit-setup** → `Installe le kit`.
6. Après la prochaine réunion : `/reunion`.

## Commandes

| Commande | Pour | Coût |
|---|---|---|
| `/reunion` | Compte rendu professionnel + vault + registre des actions | 2 requêtes (avec « OK ») |
| `/suivi` · `/point-projet` · `/rapport-avancement` | Jalons et planning · état du projet · rapport vérifié | 1 · 1 · 2 |
| `/recherche` | Information à jour, sourcée, capitalisée | 1-2 |
| `/exigence` · `/page-cesam` · `/revue-couverture` | Livrables vérifiés (exigences, page Confluence, revue) | 2-3 |
| `/verifier` | Vérification indépendante d'un brouillon | 1 |
| `/challenge` · `/teach-back` | Mettre à l'épreuve une décision · vérifier sa compréhension | selon l'échange |
| `/cadrer-demande` · `/convertir` · `/email` · `/journal` | Cadrage, conversion, email, mesure | gratuit |

Les coûts sont indicatifs (modèle rédacteur ~1x) ; le coût réel se mesure à l'étalonnage (kit-setup, étape 4).
