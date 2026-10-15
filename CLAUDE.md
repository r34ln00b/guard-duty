# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Who you are

In this repo you are Denis, the unit's playful guard-duty sidekick:
@skills/guard-duty/denis.md

## Start every session from the latest main

Both officers work on this repo, so always start from what is on `origin/main`. The hook in
`.claude/settings.json` (`.claude/hooks/sync-main.sh`) fetches `origin/main` and merges it at every
session start, and again on the first message after 3+ hours of quiet (`SYNC_AFTER_HOURS`). Its
`[sync-main]` line appears in your context. If it says something was NOT merged (uncommitted
changes, a conflict, no network), tell the user before doing anything else. If the hook didn't run,
run `git fetch origin main` and merge it yourself before starting.

## What this repo is

A Claude Code plugin that builds an army unit's guard duty list (רשימת שמירה). The repo is both the
plugin and its own marketplace: `.claude-plugin/marketplace.json` (marketplace `guard-duty-tools`)
lists one plugin with `source: "./"`, described by `.claude-plugin/plugin.json`.

Users install it with `/plugin marketplace add r34ln00b/guard-duty` and
`/plugin install guard-duty@guard-duty-tools`. The repo is private and shared with collaborators, who
get changes through marketplace updates. **Bump `version` in `.claude-plugin/plugin.json` with every
change you push**, or installed copies won't update.

The plugin is a single skill, `skills/guard-duty/`. There are two halves, and most changes touch only one:

- `SKILL.md`: the conversation workflow (what to ask the user, how to write the config, how to react
  to each exit code) and the unit's **standing rules**: 6h rest after a night shift; חפ"ק only at
  03:00-05:00 or 21:00-23:00 and never at 05:00-07:00; רפאל and אליעזר on patrol at night. A new
  standing rule or preference from the user usually goes here as config the skill always sets, not
  as code.
- `scripts/screenshot.py`: renders a stretch of the sheet (rows JSON documented in SKILL.md) as a
  right-to-left PNG for the soldiers. Needs `pillow`; without libraqm (usual on Windows) it reverses
  the Hebrew by hand.
- `scripts/guard_duty.py`: the scheduler. Its only dependency outside the standard library is
  `openpyxl`. The config format is documented in SKILL.md, not in the script.

## Running the scheduler

```
python -m pip install --user openpyxl
python skills/guard-duty/scripts/guard_duty.py config.json --out OUTDIR
```

Minimal config: `{"start": "2026-10-15 19:00", "days": 1, "people": 16}` (or `"roster": [names]`
instead of `people`). `"seconds"` caps the search time (default 8). Set `"seed"` for reproducible output.

Exit codes: `0` = OK; `2` = SHORTAGE (a night has more slots than eligible people; nothing written);
`3` = UNFILLED (files written, holes marked `???`). It prints a JSON report to stdout either way.

There is no test suite. To check a change, run it on a few configs (a normal day, a shortage, and a
multi-day run with rules) and check the hard rules independently from the summary sheet's
per-person detail column. Never trust the script's own report for this.

On the author's Windows machine, Python can't read files under `AppData\Roaming` (where Claude
session folders live). Write configs and outputs under `%TEMP%` and copy the results back.

## Scheduler architecture (guard_duty.py)

- **Time model.** A "day" runs 07:00 to 07:00 (`DAY_START_HOUR`). `build_slots` makes 2h slots for
  ש.ג./יוסטור/דרומית around the clock, starting at odd hours. It makes the patrol stand (`PAT`,
  תצפית/פטרול) 4h by day (07, 11, 15, 19) and 2h at night (23, 01, 03, 05). Slots are clipped to
  `[start, end)`, so the start must be an odd hour. A slot is a night slot when its *start* falls in
  23:00-07:00 (`night_id` returns the date of that night's 23:00).
- **People and rules.** `Person.can_take` holds the per-slot eligibility rules: stand allow and deny
  lists, `night_stands`, `night_only` and `no_night`, absolute `unavailable` ranges, and daily
  `never_hours` windows, which may wrap past midnight. `extra` people (חפ"ק) are left out of the
  hours and nights balance.
- **Pre-check.** `shortage_report` compares each night's open slots with the number of people who
  could take any of them, and exits with code 2 before solving. Night uniqueness means one person
  per night, so 16 slots need 16 people.
- **Solver.** `solve` runs randomized multi-start greedy (`solve_once`) until the time budget runs
  out. Each run assigns slots in time order and picks, for each slot, the eligible person with the
  highest score: idle time minus a weight times hours worked so far (night count too for night
  slots), plus random jitter. The weight and jitter are drawn fresh each run. Hard constraints are
  enforced inside `solve_once`:
  - no overlap
  - `min_rest_hours`, and `night_rest_hours` after a night slot
  - nobody twice in one night
  - not the same stand twice in a row
  - `max_shifts`
  - consistency with future `fixed` slots

  `evaluate` scores each run as a tuple to minimize: (unfilled, -min rest gap, count at that min,
  hours spread, night-shift spread, -sum of per-person min gaps). `last_shift` seeds each person's
  state from a previous list.
- **Output.** `write_xlsx` writes one right-to-left sheet matching the unit's Google Sheet: יום | שעה |
  ש.ג | יוסטור | דרומית | פטרול | תצפית. Daytime 4h patrol goes under תצפית, merged over 2 rows. Night
  2h patrol goes under פטרול. It also writes a per-person summary sheet. `write_whatsapp` writes the
  paste-ready text. `*_state.json` holds each person's last shift, for the next list's `last_shift`.
- To re-render or tweak a list without reshuffling it, put every existing assignment in `fixed`.
  Fixed slots are committed as-is, without the eligibility checks.

## The Google Sheet

The sheet (`שבצק_01`) is the single source of truth shared by both officers. Each round has its own
tab (`סבב 3`, …). Drafts go to a `sand box` tab, and only an approved list is copied into the round
tab; every list gets a row in the `לוג` tab. SKILL.md has the full workflow. It has
the same column order as the Excel file, in columns H-N. Its day labels change at 01:00, not 07:00.
Colours mark the platoon: yellow = מחלקה 2, green = מחלקה 3, magenta (pink) = מפל"ג / חפ"ק
(and `מפלג\חפק` slots). Cells are centred in one font. Read the tab before writing, and change only the rows being scheduled.
