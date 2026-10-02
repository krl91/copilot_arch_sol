---
name: redaction-page-cesam
description: Rédige ou adapte en anglais une page Confluence de conception selon la méthode CESAM (vues opérationnelle, fonctionnelle, constructive), à partir d'une page de référence d'un autre projet ou des notes Topic, décisions et exigences du projet, avec diagrammes Mermaid ou draw.io. À utiliser pour toute page Confluence de design, d'architecture, CESAM, ou « adapte la page du projet X ».
user-invocable: false
---
# Page Confluence CESAM

Modèle de page : [modele-page.md](modele-page.md) · Diagrammes : [diagrammes-drawio.md](diagrammes-drawio.md)
Espaces et pages parentes : {{CONFLUENCE_ESPACES}}

## Déroulé (copier et cocher)
```
- [ ] 1. Mode choisi (adaptation / création)
- [ ] 2. Sources lues, citations extraites
- [ ] 3. Tableau d'adaptation validé (mode adaptation)
- [ ] 4. Brouillon complet dans Drafts/
- [ ] 5. Diagrammes
- [ ] 6. Contrôle automatique : 0 bloquant
- [ ] 7. Vérification N2 (verificateur)
- [ ] 8. OK → publication, hub projet mis à jour
```

**Mode adaptation** (« adapte <URL> pour le projet <P> ») : lire la page source et le contexte du projet
cible ; produire `| Section | Garder / Adapter / Supprimer / À compléter | Raison |` en signalant tout
élément propre au projet source (client, volumes, interfaces, normes, dates). **Toute valeur reprise doit
être re-sourcée pour le projet cible ou passer en `[OPEN]`.** Rédiger après accord.

**Mode création** (« nouvelle page CESAM sur <sujet> ») : remplir le modèle section par section depuis les
notes Topic, `decisions.md` et les exigences Jira ; ce qui manque → `[OPEN]` + question.

Brouillon : `1 Projects/<P>/Drafts/<titre>.md`. Contrôle : `{{PYTHON_CMD}} outils/verifier_sources.py`
→ corriger → relancer. Vérification N2 via `verificateur`.

**Publication** (après accord) : créer ou mettre à jour la page sous la page parente ; pour une mise à jour,
résumer d'abord le diff. Remplacer `## Sources` par `## References`. Ajouter la page à `## Documentation`
du hub projet, la retirer de `## Docs to update`. La spec Word se produit par **export Confluence**,
jamais par régénération IA.

Exemples d'évaluation : [evals.json](evals.json).
