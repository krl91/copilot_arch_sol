# Règles de rédaction des exigences

Synthèse inspirée du *INCOSE Guide to Writing Requirements* (GtWR). La numérotation officielle et le
texte exact des règles sont dans le guide INCOSE : s'y référer en cas de doute.

## Caractéristiques d'une exigence
Nécessaire · Appropriée (bon niveau) · Non ambiguë · Complète · Singulière · Faisable · Vérifiable ·
Correcte · Conforme aux conventions.
Pour un ensemble : complet, cohérent, faisable, compréhensible, validable.

## Règles de forme (vérifier chacune)
| Thème | Règle |
|---|---|
| Structure | Phrase complète : `The <entity> shall <action> <object> [<condition>] [<performance>]` |
| Voix | Voix active ; sujet = l'entité responsable (meter, HES, MDM, system) |
| Termes | Termes définis dans le glossaire, utilisés de façon constante ; acronymes définis |
| Articles | « the » pour une entité définie, pas « a » |
| Unités | Unités explicites et cohérentes (s, ms, kB, %, kWh) ; format décimal constant |
| Termes vagues | Interdits : fast, easy, user-friendly, flexible, adequate, robust, minimal, sufficient, etc. |
| Échappatoires | Interdits : as appropriate, if possible, where applicable, as far as possible |
| Listes ouvertes | Interdits : including but not limited to, etc., and so on |
| Singularité | Une seule exigence par phrase ; éviter « and », « or », « and/or », « / » |
| Conditions | Conditions explicites et placées en tête ; conditions multiples rendues non ambiguës |
| Négations | Éviter « not » et l'expression d'une absence ; formuler ce qui est attendu |
| Quantificateurs | « each » plutôt que « all », « any », « both » |
| Plages | Valeurs avec bornes et tolérances (`between 10 s and 30 s`, `≤ 2 MB`) |
| Performance | Performance mesurable et vérifiable |
| Temps | Dépendances temporelles explicites (pas « eventually », « before » sans référence) |
| Pronoms | Pas de pronoms (it, they) ; répéter l'entité |
| Finalité | Pas de phrase de but dans l'énoncé (« in order to ») : la mettre dans Rationale |
| Solution | Pas de solution de conception sauf contrainte client explicite |
| Modalité | « shall » = obligatoire ; « should » / « may » interdits pour une exigence obligatoire |

## Points d'attention smart metering
Volumétrie et performance (nombre de compteurs, fréquence de lecture, délais HES/MDM) ; communication
dégradée (retry, timeout, mise en mémoire) ; sécurité (clés, suites DLMS, accès) ; horodatage, fuseaux et
heure d'été ; événements et alarmes ; mise à jour firmware (échec, rollback) ; unités et codes OBIS
(**jamais inventés**, toujours cités).
