---
description: כל המשימות הפתוחות (חוסרים, תקלות) לפי קטגוריה ואחראי. אפשר לסנן לפי קטגוריה, אחראי או חייל
argument-hint: "[קטגוריה | אחראי | חייל]"
---
Use the guard-duty skill as Denis: read its `yoman.md` (`${CLAUDE_PLUGIN_ROOT}/skills/guard-duty/yoman.md`)
and work in the shared sheet `שבצק_01`. If this is the session's first message, the opening message
is the greeting line only.

List the open tasks (`פתוח` and `בטיפול`) from the `משימות` tab, grouped by category and then owner,
as described in "Asking". Filter: $ARGUMENTS (empty = all open tasks). End with the no-owner and
open-more-than-7-days flags. Read only; don't write anything.
