# דורסים (on-call teams)

Read this when the user asks for דורסים, דורס א, כרמל א or תורנים. The sheet workflow
(sand box → approval → round tab → `לוג` → link → screenshot offer) is the same as for the guard
list in SKILL.md; this file only adds what's different.

## The teams

Every 24h block, **19:00 to 19:00 the next day**, gets one platoon's teams:

| Team | People | Notes |
|---|---|---|
| דורס | 3 | Always includes the platoon's lead: **אליעזר** for מחלקה 2, **רפאל** for מחלקה 3 |
| דורס א | 4 | |
| כרמל א | 2 | May drop to 1 when the platoon is short |
| תורנים | 2 | Also on כרמל (the header says `תורנים (גם כרמל)`), so the `כרמל א` cell lists its 2 people plus the 2 תורנים |

- **One platoon per block.** All names come from that platoon's roster column in the round tab
  (B = מחלקה 2, C = מחלקה 3). Never mix platoons unless the user says so.
- **חמ"ליסטים are left out** of the teams and of the guard stands. The fixed ones are listed below;
  ask the user whether that's still right for this block.
- **Short of people:** drop כרמל א to 1 first, then ask.
- **Extra people** in the platoon go to the `מצטרף לעמדות` column: they join the guard stands.
- **Nobody holds two things at once.** Whoever is on a team in a block takes no guard stand during
  those 24h. When you later build the guard list for those hours, give each of them
  `"unavailable": [["<day> 19:00", "<next day> 19:00"]]` in the config.
- **No rest balancing** for the teams: they're on call, not necessarily active.
- Plan one or two days ahead, as the user asks.

## Choosing the תורנים

Spread תורנות as widely as possible:

1. Ask who doesn't do תורנות this time.
2. Count past תורנות with `scripts/duty_history.py`: read each recent round tab with
   `get_values` (range `<tab>!A1:Z150`), save each result as JSON in the scratchpad, then run
   `python scripts/duty_history.py tab1.json tab2.json … --role תורנים`. It finds the columns by
   header, counts a merged block or a repeated block once, and lists everyone in the roster from
   fewest to most. Names it couldn't match to the roster are under `unknown_names`: check those
   by hand.
3. Pick the eligible people with the fewest, and show the user a short table of the counts
   (per round and total) next to your pick.

## In the sheet

- The team columns sit right of the guard list, found by their row-2 headers: `דורס`, `דורס א`,
  `כרמל א`, `תורנים (גם כרמל)`, `מצטרף לעמדות` (currently Q-U).
- One block = one cell per column, **merged from the 19:00 row down to the 17:00 row** (12 rows),
  names one per line (`\n`), centred and vertically middle, in the platoon's colour (yellow =
  מחלקה 2, green = מחלקה 3). `מצטרף לעמדות` names are comma-separated.
- Draft in `sand box` with the same headers and layout, post to the round tab only after approval,
  and log it in `לוג` (`סבב`, `מ-`/`עד` = the block's 19:00 to 19:00, note e.g. `דורסים מחלקה 3`).

## Screenshot

Offer it after posting, same as the guard list, showing **only the blocks you just worked on**.
Use `scripts/screenshot.py` with:

```json
{
  "title": "דורסים ו' 16/10",
  "columns": ["דורס", "דורס א", "כרמל א", "תורנים (גם כרמל)", "מצטרף לעמדות"],
  "groups": {"green": ["רפאל", "…"]},
  "rows": [{"day": "ו'", "time": "19:00", "cells": ["רפאל\nחדד\nג'ימי", "…", "…", "…", "…"]}],
  "caption": "…",
  "signature": "— דניס, …"
}
```

A cell with several names (one per line) gets its platoon's colour when they all share one.
Caption and signature follow `denis.md`.

## Fixed חמ"ליסטים

Not recorded yet. Ask the user for each platoon's חמ"ליסטים, add them here, and push the change.
