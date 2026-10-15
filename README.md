# guard-duty

A Claude Code plugin that builds the guard duty list (רשימת שמירה) for ש.ג., יוסטור, דרומית and
תצפית/פטרול. It asks for the people, limits and dates, then produces an Excel file in the unit's
layout and a WhatsApp text, or writes straight into the Google Sheet.

## Install

Requires Python with `openpyxl`:

```
python -m pip install --user openpyxl
```

In Claude Code:

```
/plugin marketplace add <github-user>/<repo-name>
/plugin install guard-duty@guard-duty-tools
```

Then type `/guard-duty`, or ask for a guard list.

## Get updates

```
/plugin marketplace update guard-duty-tools
```

Or turn on auto-update for this marketplace in `/plugin` → Marketplaces.

## Change the tool

- Rules and questions: `skills/guard-duty/SKILL.md`
- Scheduler: `skills/guard-duty/scripts/guard_duty.py`

Bump `version` in `.claude-plugin/plugin.json` with each change, then commit and push.
