# Règles de compte rendu (tous types de réunion)

## Structure commune (dans cet ordre)
Chaque élément (décision D, action A, engagement C, question Q, exigence R, changement de périmètre S)
porte un ID, tracé vers sa source dans les working notes.

1. **Meeting information** — title · date, time, duration · location / link · organizer · minute-taker ·
   present · absent / excused · distribution (includes absentees) · classification · version / status.
2. **Summary** — 1 to 3 sentences: purpose and outcome.
3. **Decisions** — decision · decided by · rationale (1 line) · source.
4. **Actions** — ID (A1…) · one owner per action (a person, never "team" or "all") · verb + deliverable · due date
   YYYY-MM-DD · done when · source. Owner or date not stated → `TBD [OPEN]`, listed under
   « Owners / due dates to confirm ».
5. **Previous actions review** — each open action of the previous meeting: done / in progress / late /
   cancelled, new due date if changed.
6. **Discussion by agenda item** — in agenda order, 2-4 bullet points per item: key points, not a transcript.
7. **Sections propres au type** (interne, workshop client, handover).
8. **Open questions** · **Parking lot** (sujet, suite, responsable).
9. **Next meeting** — date, objective.
10. **References** — documents, pages, tickets, recording.

## Style
- Factual, neutral, concise, past tense, third person ("The customer confirmed…").
- No opinions, no judgments, no humour, no speculation: they stay in `## My notes`.
- No verbatim except customer requirements and commitments (quoted).
- Names: first name + last name on first mention, then consistent.
- Absolute dates only (convert "next Friday" from the meeting date).
- Nothing sensitive (personal data, commercial terms not meant for all recipients).

## Diffusion
- Draft within **2 hours**, send within **24 hours**, to all participants **and absentees**.
- **Deux notes** : la note **Meeting** est le compte rendu diffusable tel quel ; la note **working notes**
  (privée) contient récap Teams, transcription, notes personnelles, contrôle de compréhension, traçabilité,
  brouillon d'email et sources. Rien d'interne n'entre dans la note Meeting ; `outils/verifier_compte_rendu.py`
  le contrôle.
- Workshop client: status `sent` → `confirmed` after customer reply (or after the confirmation deadline).
- Corrections after sending: new version number, short change note.
