# Prompts Copilot 365 (ne consomment pas les crédits GitHub)

À enregistrer dans les prompts sauvegardés de Copilot 365 si disponible.

## Recherche SharePoint / emails / Teams
```
Find the most recent information about: <TOPIC>
(context: project <PROJECT>, customer <CUSTOMER>).
Search SharePoint documents, my emails and Teams chats/meetings.
For each finding give: source (title + link), author, date of last modification,
and what it says in 1-2 sentences.
Then: flag contradictions between sources and say which one is the most recent.
Say explicitly what you could not find. Do not guess.
```

## Tri des emails du matin (Outlook)
```
Summarise my unread emails since yesterday 18:00.
Group them: 1) needs my action (with deadline), 2) decisions or information that
change something on my projects, 3) FYI only.
For group 2, give the fact, the source email and the date.
```
→ Les faits du groupe 2 : les coller dans `0 Inbox/` puis `mets à jour le vault` dans VS Code.

## Réponse à un email (Outlook)
```
Draft a reply in English, professional and concise. Goal: <WHAT I WANT>.
Do not commit to any date, scope or cost unless I state it here: <...>.
```

## Préparation de la réunion interne (Excel)
```
In this workbook, list the tasks assigned to me or blocked by me:
overdue, due within 10 days, changed since last week. Table: ID, task, status, due date, comment.
```

## Mise à jour du fichier après la réunion (Excel)
```
Here are the updates decided in today's meeting: <coller la liste "Updates to apply
in the Excel tracker" produite par VS Code>.
Show me the rows to modify and the new values before changing anything.
```
