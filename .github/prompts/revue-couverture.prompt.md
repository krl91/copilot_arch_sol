---
name: revue-couverture
description: Relit une spec produit ou un plan de test contre des exigences système - matrice de couverture et commentaires de revue en anglais (N2).
argument-hint: Exigences (clés/JQL) + document à relire
agent: redacteur
model: {{MODELE_REDACTEUR}}
---
Exigences système : ${input:exigences:clés Jira ou JQL} · Document : ${input:document:URL, test plan Xray ou fichier}

1. Lire les exigences (statement, critères d'acceptation) et le document (le convertir s'il s'agit d'un fichier Office/PDF).
2. Matrice `| Exigence | Couverte par (section / test) | covered / partial / missing / contradicts | Commentaire | Source |`.
3. Plan de test : vérifier aussi nominal, limites, erreurs, communication dégradée, sécurité, volumétrie,
   préconditions et résultats attendus mesurables.
4. Commentaires en anglais, prêts à coller : `[Major|Minor|Question] <section> – <constat> – <proposition>`.
5. Brouillon dans `1 Projects/<P>/Drafts/review-<doc>.md` ; niveau N2 ; synthèse en français (verdict, 3 points clés).
Ne rien écrire dans Jira, Xray ou Confluence.
