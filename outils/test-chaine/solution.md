# Solution du brouillon piégé (ne pas donner aux agents)

| # | Ligne | Erreur | Qui doit l'attraper |
|---|---|---|---|
| 1 | SR-1 | « 2 MB » alors que la source [S1] dit 1 MB | Script (number+unit) + vérificateur |
| 2 | SR-2 | « 5 times » alors que la source dit 3 retries | **Vérificateur seulement** (pas d'unité → invisible pour le script) |
| 3 | SR-2 | Une *demande* client en réunion est transformée en exigence ferme « shall » sans confirmation | **Vérificateur seulement** (statut / attribution) |
| 4 | SR-3 | Code OBIS inventé (absent de toute source) | Script (OBIS) + vérificateur |
| 5 | SR-3 | [S1] ne parle pas du reporting de version : citation qui ne soutient pas l'affirmation | **Vérificateur seulement** |
| 6 | SR-4 | Cite [S3] qui n'existe pas ; « 5 s » non sourcé | Script |
| 7 | SR-5 / Traceability | SR-5 sans source alors que [S4] la soutient ; CUST-4512 au lieu de CUST-4511 | Script |

Résultat attendu :
- `verifier_sources.py` → 5 bloquants + 2 avertissements, code de sortie 1.
- Agent `verificateur` → verdict **FAIL**, avec au minimum les erreurs 1 à 6.
Si le vérificateur rate 2, 3 ou 5 : essayer un autre modèle pour `{{MODELE_VERIFICATEUR}}`.
