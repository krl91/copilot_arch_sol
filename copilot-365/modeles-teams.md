# Modèles de compte rendu Copilot pour Teams

À créer dans Teams (modèles de récapitulatif IA / instructions de compte rendu).
Les noms exacts des menus évoluent : cherche « modèle » / « template » dans le récapitulatif
de réunion ou dans les paramètres Copilot de Teams.
Rédigés en anglais pour que le compte rendu soit directement réutilisable.

---

## 1. Internal – Project review
```
Produce meeting minutes in English with these sections:
0) Meeting information — date, time, organizer, attendees present, invited but absent.
   Summary — 1 to 3 sentences.
   Previous actions review — status of open actions from the previous meeting, if discussed.
1) Decisions taken — for each: decision, who decided.
2) Task tracker review — for each task discussed from the Excel tracker
   ({{EXCEL_ONGLETS_ET_COLONNES}}): task ID or label, status announced, what changed,
   new due date, owner.
3) Action items — action (verb + deliverable), owner, due date (absolute date). "TBD" if not stated.
4) Pending arbitrations — topic, options, who must decide, by when.
5) Risks and alerts (planning, scope, resources, dependencies).
6) Disagreements not resolved.
Be factual. Do not attribute a decision or an action to someone unless it was explicit.
Do not add commercial or positive wording.
Also include: Discussion by agenda item (in agenda order, 2-4 key points each), Next meeting (date, objective).
Style: factual, neutral, past tense, third person; no opinions; absolute dates; one owner per action.
```

## 2. Customer workshop (English)
```
Produce workshop minutes in English with these sections:
0) Meeting information — date, time, organizer, attendees present, invited but absent.
   Summary — 1 to 3 sentences.
   Decisions — decision, who decided.
1) Customer requirements stated or changed — quote the customer's words.
2) Commitments made by our side — who said what, under which condition.
3) Potential scope changes — anything that sounds new versus the existing
   specification or contract.
4) Action items — action (verb + deliverable), owner, side (us / customer), due date (absolute date).
   If the owner or the date was not stated, write "TBD" — never guess.
5) Open questions — question, owner (us / customer), due date.
6) Customer terminology and acronyms used, with meaning when explained.
7) Next steps.
Mark uncertain points with [UNCLEAR]. Do not paraphrase requirements: quote them.
Also include: Discussion by agenda item (in agenda order, 2-4 key points each), Next meeting (date, objective).
Style: factual, neutral, past tense, third person; no opinions; absolute dates; one owner per action.
```

## 3. Handover
```
Produce handover minutes in English with these sections:
0) Meeting information — date, time, organizer, attendees present, invited but absent.
   Summary — 1 to 3 sentences.
1) Context and objective of the topic handed over.
2) Decisions already taken and their rationale.
3) Open points and risks, with owner.
4) Action items — action (verb + deliverable), owner, due date (absolute date). "TBD" if not stated.
5) Key contacts and their role.
6) Documents, Confluence pages, SharePoint files and Jira tickets mentioned.
7) What was NOT covered or remains unclear.
Also include: Discussion by agenda item (in agenda order, 2-4 key points each), Next meeting (date, objective).
Style: factual, neutral, past tense, third person; no opinions; absolute dates; one owner per action.
```

---

## Astuces
- Rédiger dans les 2 heures, envoyer sous 24 heures, aux participants **et aux absents**.
- Activer **la transcription** dès le début (sans elle, le contrôle de compréhension
  du skill est limité).
- En workshop, annoncer en début de réunion : « we record the transcript to produce
  accurate minutes that we will send you for confirmation » (transparence + accord).
- Après la réunion : copier le récap **et** télécharger la transcription (.docx/.vtt),
  coller la partie utile dans la note Obsidian.
