# Exemples (fictifs, à titre de style)

**Exigence client** : « The system must update meters quickly and securely. »

**Critique**
| # | Extrait | Problème | Question au client |
|---|---|---|---|
| 1 | quickly | Non mesurable | What maximum duration is acceptable for a firmware campaign, and for how many meters? |
| 2 | securely | Non mesurable | Which security requirements apply (DLMS security suite, image signature)? |
| 3 | update meters | Ambigu | Does "update" cover firmware only, or also configuration? |

**Mauvais** : `The system shall quickly and securely update all meters.`
(vague ×2, deux exigences dans une phrase, « all »)

**Bon** (valeurs `[OPEN]` tant que le client n'a pas répondu) :
- `SR-1` — The HES shall complete a firmware campaign for each targeted meter within [OPEN] days.
  Verification: Test. Acceptance: campaign report shows each meter status = "activated" within the limit.
- `SR-2` — The meter shall reject a firmware image whose signature verification fails.
  Verification: Test. Acceptance: image with invalid signature is not activated and event [OPEN] is logged.
