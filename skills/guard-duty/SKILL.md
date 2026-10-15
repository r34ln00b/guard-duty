---
name: guard-duty
description: Build the unit's guard duty list (רשימת שמירה) for ש.ג., יוסטור, דרומית and תצפית/פטרול as an Excel file plus WhatsApp text. Use when the user asks for a guard list, שמירות, רשימת שמירה, or types /guard-duty.
---

# Guard duty list builder

Read `denis.md` (next to this file) and talk to the user as Denis while you work through this skill.

The scheduler is `scripts/guard_duty.py` (next to this file). It needs Python with `openpyxl`
(`python -m pip install --user openpyxl` if missing). The screenshot for the soldiers is
`scripts/screenshot.py`, which needs `pillow`.

## Fixed structure (don't ask about this)

- ש.ג., יוסטור, דרומית: 2-hour shifts, 24h, starting at odd hours (07, 09 … 23, 01, 03, 05).
- תצפית/פטרול: 4-hour shifts by day (07-11, 11-15, 15-19, 19-23), 2-hour shifts at night (23-01, 01-03, 03-05, 05-07).
- Each sheet covers one day, 07:00 → 07:00.
- Slots are filled with **numbers** (1..N). The user maps numbers to soldiers themselves.

## Rules the script enforces

- **Night (23:00-07:00): nobody appears twice.** That is 16 slots per night, so it needs 16 people
  who can take a night shift.
- Nobody gets the same stand twice in a row, unless the user says it's OK (globally or for one number).
- At least `min_rest_hours` (default 2) between shifts. Beyond that it maximizes the smallest rest
  gap, then balances hours and night shifts. Who gets which hours is random.

## The Google Sheet is the source of truth

The unit's sheet is `שבצק_01`
(https://docs.google.com/spreadsheets/d/13taiMKAGdcOAZQ_kIE3k8V2klLmBE3tUg3FaCIWvUcE). Two officers
share it, so always work from what is in the sheet, not from memory or an old file.

- **One tab per round** (`סבב2`, `סבב 3`, …). The newest round tab is the current one. Ask before
  starting a new round tab. Columns A-E hold the roster by group (מחלקה 2, מחלקה 3, חפ"ק, מפל"ג); the
  list is in H-N: יום | שעה | ש.ג | יוסטור | דרומית | פטרול | תצפית. Day labels change at 01:00.
- **Before building:** read the current round tab. Take the roster from columns B-E. Read the last
  filled rows into `last_shift`, and anything already filled in the hours you're scheduling into
  `fixed`. Cells like `מפלג\חפק`, `מפלג` or `חמ"ליסט` are taken by other duties: cancel those slots.
- **Draft in the `sand box` tab** (create it if missing, with the same headers as the round tab).
  Clear its old rows and write the new list there. Never write a draft into the round tab.
- **Post only after approval.** When the user approves the draft, copy those rows into the current
  round tab, changing only the rows being scheduled.
- **Keep the list tidy.** Colours mark the platoon (from the roster in columns B-E), so every
  name you write gets its platoon's colour: **yellow = מחלקה 2**, **green = מחלקה 3**,
  **pink (magenta) = מפל"ג / חפ"ק** (and slots taken by `מפלג\חפק`). A name that isn't in the roster:
  ask which platoon. Every cell you write is centred, in the tab's own font and size, like the rest.
- **Log every list** in the `לוג` tab (create it if missing), one row each:
  `תאריך יצירה | נבנה ע"י | סבב | מ- | עד | סטטוס (טיוטה/אושר/פורסם) | הערות`. Add a row for the draft
  and update its status when it is approved and posted. Ask the user their name once per session for
  `נבנה ע"י`.
- **Log every change too.** Any edit you make to the sheet outside a full list (swapping a name,
  filling or cancelling a slot, changing a colour) gets its own `לוג` row right after it, with
  status `שינוי`, `מ-`/`עד` set to the changed slot's hours, and a short free-text note in Hebrew
  in `הערות` saying what changed (e.g. `יוסטור ו' 03:00: הכט במקום מפלג\חפק, צבוע ורוד`).
- **End with the link.** After any change to the sheet (a posted list, a draft, a single edit),
  finish your reply with the sheet's link on its own line, so the user can check it in one click:
  https://docs.google.com/spreadsheets/d/13taiMKAGdcOAZQ_kIE3k8V2klLmBE3tUg3FaCIWvUcE
- Writing to the sheet needs the **Google Sheets connector**. With only Google Drive you can read the
  sheet (a sample of the first rows) but not edit it. If it's missing, say so, and offer the Excel
  file in the same column layout to paste in by hand.

## Screenshot for the soldiers

After every list you post and every change to the sheet, ask (one short line) whether they want a
screenshot of the coming shifts to send to the soldiers. Suggest the range from the earliest slot
you just changed (or the start of the new list) to the last filled row of the round tab, and let
them change it.

Read those rows of the round tab (values and background colours) and write a JSON like this:

```json
{
  "title": "שמירות ו' 16/10",
  "groups": {"yellow": ["דורון", "…"], "green": ["רפאל", "…"], "pink": ["הכט", "…"]},
  "rows": [
    {"day": "ו'", "time": "03:00", "cells": ["חדד", "הכט", "רפאל", "קינן", ""]},
    {"time": "07:00", "cells": ["אטיאס", "ברמי", "שמעון", "", "אוראל"]},
    {"time": "09:00", "cells": ["ג'ימי", "אפריים", "סאם", "", "^"]}
  ]
}
```

- `cells` are in sheet order: ש.ג, יוסטור, דרומית, פטרול, תצפית. `"^"` continues the cell above
  (the merged 4h daytime תצפית). A row without `day` belongs to the day above (labels change at 01:00).
- `groups` comes from the roster: מחלקה 2 → `yellow`, מחלקה 3 → `green`, חפ"ק and מפל"ג → `pink`.
  Cells containing `מפלג`/`חפק` are pink automatically. To force a colour on one cell, write it as
  `{"name": "…", "color": "yellow"}` (or a `#RRGGBB`).

Then run `python scripts/screenshot.py rows.json --out list.png` and send the PNG with
SendUserFile. It draws a right-to-left table (יום | שעה | stands), all text centred in one font
and size. If no Hebrew font is found, pass `--font` (on Windows `C:/Windows/Fonts/arial.ttf`). Look
at the image before sending it: Hebrew must read right-to-left and colours must match the platoons.

## Step 1: ask the user (one AskUserQuestion call or a short message, only what's missing)

1. **Start and length**: start date/time (default: tomorrow 07:00; the start must be an odd hour) and how many days.
2. **How many people** (numbers 1..N).
3. **Limitations** for today, for example:
   - a number unavailable for certain hours/days, only some stands, never some stands, no nights, nights only, max number of shifts
   - slots to cancel (e.g. the 05:00 patrol)
   - extra people (e.g. חפ"ק) and when they can guard
   - fixed assignments (number X must take a specific slot)
   - whether same stand twice in a row is OK
   - whether anyone just came off a shift before the start (`last_shift`)
4. Ask once whether they want names in the list. If yes, take a number→name map.

If they already gave some of this in their message, don't ask about it again.

## Step 2: write the config and run

Write `guard_config.json` in the current working directory, then run:

```
python "<this skill dir>/scripts/guard_duty.py" guard_config.json --out .
```

**If Python can't open files in the working directory** (seen on Windows when it is under `AppData\Roaming`), write the config with the Write tool, then in PowerShell copy it
to `$env:TEMP\guard-duty`, run the script there with `--out $env:TEMP\guard-duty`, and copy the
`shmira_*` outputs back into the working directory before sending them.

Config fields (only `start` and `people` are required):

```json
{
  "start": "2026-10-15 07:00",
  "days": 2,
  "people": 18,
  "extra": [{"id": "חפק", "night_only": true}],
  "rules": {
    "4": {"unavailable": [["2026-10-15 13:00", "2026-10-15 19:00"]]},
    "9": {"not_stands": ["patrol"]},
    "11": {"stands": ["ש.ג."], "no_night": true, "max_shifts": 3, "allow_same_stand": true}
  },
  "cancel": [
    {"stand": "patrol", "time": "05:00"},
    {"stand": "patrol", "time": "05:00", "date": "2026-10-16"},
    {"stand": "dromit", "start": "2026-10-15 13:00"},
    {"stand": "yustor", "from": "2026-10-15 23:00", "to": "2026-10-16 07:00"}
  ],
  "fixed": [{"id": "3", "stand": "ש.ג.", "start": "2026-10-15 07:00"}],
  "allow_same_stand": false,
  "min_rest_hours": 2,
  "night_rest_hours": 6,
  "last_shift": {"5": {"end": "2026-10-15 07:00", "stand": "ש.ג."}},
  "names": {"1": "דני"},
  "title": "רשימת שמירה",
  "seconds": 8
}
```

Instead of `people`, you can pass `"roster": ["נטף", "אוראל", ...]` to schedule by name; rules,
`last_shift` and `fixed` then use the names as ids. When the user sends a screenshot of a list that's
already running, read each person's last shift from it into `last_shift`.

**Always set `night_rest_hours` to 6** (the user wants at least 6h of sleep after a night shift). If that
leaves holes because everyone guards at night, push people who leave the next morning to 05:00,
so four regular people do 23:00-01:00 and are free at 07:00.

**Standing preference: רפאל and אליעזר are on תצפית/פטרול at night.** Whenever either name is
in the roster, give them `"night_stands": ["patrol"]` (by day they can take any stand). If that
leaves holes, drop it for one of them and tell the user.

**חפ"ק rules** (they have to be up at 05:00):
- Never 05:00-07:00.
- They may only take **03:00-05:00** (preferred: awake straight through to 05:00) or **21:00-23:00**
  (so they still sleep a bit). Give every חפ"ק extra (without `night_only`):
  `"never_hours": [["23:00", "03:00"], ["05:00", "21:00"]]`.
  `never_hours` is a daily window that repeats every day of the list.
- One shift per night: set `"max_shifts"` to the number of nights in the list.
- 21:00-23:00 is not a night slot, so it doesn't cover a night shortage. When they are there to fill
  a missing night slot, put them on 03:00-05:00 (`"never_hours": [["05:00", "03:00"]]`).

The Excel matches the unit's sheet: one right-to-left sheet with columns
יום | שעה | ש.ג | יוסטור | דרומית | פטרול | תצפית and green filled cells, so the user can copy and paste
it. Daytime 4h patrol shifts go under תצפית and night 2h shifts under פטרול. To change one detail
without reshuffling a list that's already out, put every existing assignment into `fixed`.

Stand aliases: `sg`, `yustor`, `dromit`/`south`, `patrol` (or the Hebrew names).
A cancel `time` with no `date` cancels that slot every day. A cancel `date` is the calendar
date of the slot's start (the 05:00 slot after the night of the 15th has date 16th).
Extra people's ids are text (e.g. `"חפק"`) and they are left out of the hours balance.
A `*_state.json` file is written with each number's last shift. If the user keeps the same
numbering for the next list, copy its `last_shift` into the next config.

## Step 3: handle the result

- **exit 2 / `"status": "SHORTAGE"`**: not enough people for a night. Nothing was written.
  Tell the user which night and how many people are missing, then ask how to fix it (don't choose
  for them). Offer these options:
  - add someone from חפ"ק (`extra`, on 03:00-05:00, see the חפ"ק rules)
  - cancel the 05:00 patrol (or another night slot)
  - add people
  - let a specific number guard twice that night (as a last resort: set `"ignore_shortage": true`;
    the script then leaves the slots it can't fill as "???" and you should report them).
  After they choose, update the config and run again.
- **exit 3 / `"status": "UNFILLED"`**: files were written but some slots show "???". List them and
  ask how to fix (relax a limitation, lower `min_rest_hours`, cancel the slot, add a person).
- **exit 0**: send the `.xlsx` with SendUserFile. In one or two lines, report the minimum rest,
  hours per person (min-max) and anything unusual. Mention the `_whatsapp.txt` text they can paste.
  If they didn't give names, offer to add them once they've given out the numbers.
