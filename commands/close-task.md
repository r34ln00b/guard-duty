---
description: סגירת משימה לפי מספר או תיאור
argument-hint: "<# או תיאור, ואיך זה טופל>"
---
Use the guard-duty skill as Denis: read its `yoman.md` (`${CLAUDE_PLUGIN_ROOT}/skills/guard-duty/yoman.md`)
and work in the shared sheet `שבצק_01`. If this is the session's first message, the opening message
is the greeting line only.

Close this task in the `משימות` tab, following "Closing and updating": $ARGUMENTS

If more than one open task could match, list them and ask which. Log it in `לוג` and end with the
sheet link.
