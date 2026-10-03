# Kit Copilot – Architecte solution smart metering

Kit pour travailler avec **GitHub Copilot (VS Code) + MCP Jira/Xray/Confluence**,
**Copilot 365** et un **second cerveau Obsidian (PARA)**, avec une **chaîne de validation
anti-hallucination**, des **convertisseurs Word / Excel / PowerPoint / PDF → markdown**, conçu selon les bonnes pratiques d'Anthropic et de la documentation VS Code (voir section 12 du mode d'emploi).

👉 **Tout est expliqué dans [MODE-EMPLOI.md](MODE-EMPLOI.md)** : installation, configuration,
usage quotidien, rôle de chaque fichier, dépannage.
👉 **Les deux workflows clés pas à pas dans [WORKFLOWS.md](WORKFLOWS.md)** : de la réunion au compte rendu
professionnel, et le suivi de projet (actions, planning, avancement).

## Démarrage en 6 étapes
1. Sauvegarde ton vault.
2. Copie le contenu de ce dossier à la racine du vault.
3. VS Code → *Fichier → Ouvrir le dossier* → le vault → faire confiance au dossier.
4. Vérifie dans les paramètres : « instruction files », « prompt files », « agent skills » activés.
5. Chat Copilot → agent **kit-setup** → `Installe le kit`.
6. Après la prochaine réunion : `/reunion`.

## Commandes principales
| Commande | Pour | Coût |
|---|---|---|
| `/reunion` | Compte rendu + contrôle de compréhension + vault | Premium |
| `/recherche` | Info à jour, sourcée, capitalisée | Premium |
| `/exigence` | Exigence client → exigences système (vérifiées) | Premium |
| `/page-cesam` | Page Confluence CESAM (vérifiée) | Premium |
| `/revue-couverture` | Revue spec / plan de test (vérifiée) | Premium |
| `/verifier` | Vérification indépendante d'un brouillon | Vérificateur |
| `/suivi` · `/point-projet` · `/rapport-avancement` | Registre des actions et planning · où en est le projet · rapport d'avancement vérifié | Premium |
| `/challenge` · `/teach-back` | Mettre à l'épreuve une décision · vérifier sa compréhension | Premium |
| `/cadrer-demande` · `/convertir` · `/email` · `/journal` | Cadrage, conversion, email, mesure | Gratuit |
