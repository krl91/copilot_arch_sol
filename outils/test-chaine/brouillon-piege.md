---
type: test
note: Brouillon volontairement piégé pour tester la chaîne de validation. 7 erreurs cachées (voir solution.md).
---
# Firmware upgrade – system requirements (TEST)

## Requirements
- SR-1: The meter shall accept firmware images up to 2 MB. [S1]
- SR-2: The HES shall retry a failed image transfer 5 times, with a 10 min delay. [S2]
- SR-3: The meter shall report the active firmware version in OBIS 1-0:0.2.0.255. [S1]
- SR-4: The HES shall notify the MDM within 5 s after activation. [S3]
- SR-5: The meter shall roll back automatically if activation fails.
- Traceability: derived from customer requirement CUST-4512. [S2]

## Sources
- [S1] JIRA PRJ-101 (2026-09-12) — "The meter shall accept firmware images up to 1 MB."
- [S2] MEETING 1 Projects/Demo/Meetings/2026-09-15 Workshop.md (2026-09-15) — "customer asked for 3 retries with a 10 min delay between attempts, ref CUST-4511"
- [S4] CONF https://confluence.example/pages/123 "FW design" (2026-08-30) — "Rollback is triggered by the meter after a failed activation."
