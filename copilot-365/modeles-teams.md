# Modèles de compte rendu Copilot pour Teams

À créer dans Teams (modèles de récapitulatif IA / instructions de compte rendu).
Les noms exacts des menus évoluent : cherche « modèle » / « template » dans le récapitulatif
de réunion ou dans les paramètres Copilot de Teams.
Rédigés en anglais pour que le compte rendu soit directement réutilisable.

---

## 1. Internal – Project review
```
Produce meeting minutes in English with these sections:
1) Decisions taken — for each: decision, who decided.
2) Task tracker review — for each task discussed from the Excel tracker
   ({{EXCEL_ONGLETS_ET_COLONNES}}): task ID or label, status announced, what changed,
   new due date, owner.
3) Actions — action, owner, due date (absolute date).
4) Pending arbitrations — topic, options, who must decide, by when.
5) Risks and alerts (planning, scope, resources, dependencies).
6) Disagreements not resolved.
Be factual. Do not attribute a decision or an action to someone unless it was explicit.
Do not add commercial or positive wording.
```

## 2. Customer workshop (English)
```
Produce workshop minutes in English with these sections:
1) Customer requirements stated or changed — quote the customer's words.
2) Commitments made by our side — who said what, under which condition.
3) Potential scope changes — anything that sounds new versus the existing
   specification or contract.
4) Open questions — question, owner (us / customer), due date.
5) Customer terminology and acronyms used, with meaning when explained.
6) Next steps.
Mark uncertain points with [UNCLEAR]. Do not paraphrase requirements: quote them.
```

## 3. Handover
```
Produce handover minutes in English with these sections:
1) Context and objective of the topic handed over.
2) Decisions already taken and their rationale.
3) Open points and risks, with owner.
4) Key contacts and their role.
5) Documents, Confluence pages, SharePoint files and Jira tickets mentioned.
6) What was NOT covered or remains unclear.
```

---

## Astuces
- Activer **la transcription** dès le début (sans elle, le contrôle de compréhension
  du skill est limité).
- En workshop, annoncer en début de réunion : « we record the transcript to produce
  accurate minutes that we will send you for confirmation » (transparence + accord).
- Après la réunion : copier le récap **et** télécharger la transcription (.docx/.vtt),
  coller la partie utile dans la note Obsidian.
