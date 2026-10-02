---
name: recherche
description: Trouve l'information à jour sur un sujet dans le vault, Confluence et Jira, avec sources datées et contradictions, puis la capitalise en fiche Answer.
argument-hint: Question (et projet éventuel)
agent: redacteur
model: {{MODELE_REDACTEUR}}
---
Question : ${input:question:que cherches-tu ?}

1. **Vault** d'abord (notes Topic, fiches Answer). Fiche de moins de 3 mois qui répond → la donner et s'arrêter.
2. **Confluence** : 2-3 recherches CQL (mots-clés EN, synonymes, acronymes), triées par date ; lire au plus
   les 5 pages les plus pertinentes. Sans recherche MCP : lire les pages du hub projet et demander les URL manquantes.
3. **Jira** : une requête JQL ciblée si utile.
4. Répondre : **Answer** (3-5 lignes, français) · **Sources** (citations, auteur, date) · **Contradictions**
   (la plus récente / la plus officielle) · **Confidence** (high / medium / low, pourquoi) · **Not found** (et qui saurait).
   Chaque affirmation porte `[Sx]` ou `[OPEN]`.
5. Fournir un **prompt prêt à coller dans Copilot 365** pour SharePoint, emails et Teams (mêmes exigences de sources).
6. Proposer une fiche `obsidian-templates/Answer.md` (anglais) dans `Topics/` ou `3 Resources/` ; la créer après accord. Niveau N1.
