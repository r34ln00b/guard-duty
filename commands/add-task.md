---
description: פתיחת משימה חדשה (ציוד חסר או שבור, תקלה) עם קטגוריה ואחראי
argument-hint: "<מה קרה, למי, מי אחראי>"
---
Use the guard-duty skill as Denis: read its `yoman.md` (`${CLAUDE_PLUGIN_ROOT}/skills/guard-duty/yoman.md`)
and work in the shared sheet `שבצק_01`. If this is the session's first message, the opening message
is the greeting line only.

Add this to the `משימות` tab, following "Adding": $ARGUMENTS

Infer the category, item/soldier and owner from the text; ask only for what's missing. Check for an
open task about the same thing first. Log it in `לוג` and end with the sheet link.
