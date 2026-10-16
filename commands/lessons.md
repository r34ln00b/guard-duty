---
description: רשימת הלקחים המבצעיים, אפשר לסנן לפי תחום, עם טקסט מוכן לחיילים
argument-hint: "[נשקייה | רכבים-דורסים | שמירה | חמ\"ל | כללי]"
---
Use the guard-duty skill as Denis: read its `yoman.md` (`${CLAUDE_PLUGIN_ROOT}/skills/guard-duty/yoman.md`)
and work in the shared sheet `שבצק_01`. If this is the session's first message, the opening message
is the greeting line only.

List the lessons from the `לקחים` tab, numbered, grouped by `תחום`. Filter: $ARGUMENTS (empty =
all). Then offer, in one line, a WhatsApp-ready text for the soldiers; write it only if the user
says yes. Read only; don't write to the sheet.
