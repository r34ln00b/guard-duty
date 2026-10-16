# Denis on Telegram: design

Status: **draft, for both officers to approve.** Nothing here is built yet.

## Goal

- Denis posts to the unit's Telegram group on his own: open tasks with the owners tagged, the
  approved list with its screenshot, the weekly responsibility board.
- An officer builds and changes guard lists with Denis in a private chat, at the same time.
- **Budget: ₪0 on top of the officers' existing Claude subscriptions.**

## The key decision: two parts

A Claude subscription covers its owner's own use of Claude (claude.ai, the Claude app, Claude Code).
It may not run a bot that other people talk to. That would mean sharing the account, which breaks
the terms and risks a suspension. A bot that runs Claude itself needs a paid API key. To stay at
₪0, the work is split in two:

| | **Denis the officer's assistant** | **Denis the group bot** |
|---|---|---|
| What it is | This plugin, in Claude Code / the Claude app | A small Python script, no AI inside |
| Who talks to it | Each officer, on their own subscription | Everyone in the group |
| What it does | Builds lists, swaps, tasks, lessons, writes the sheet (as today) | Reads the sheet, posts summaries, tags people |
| Writes the sheet | Yes, after the officer approves | **Never** (read-only access) |
| Cost | The existing subscription | Free (Telegram, GitHub Actions, Google) |

So the "private chat for building a list" is the Claude app on the officer's phone, as it is today
(including cloud sessions like this one), not a private Telegram chat. Each officer needs their
own subscription; the two officers don't share one.

The group bot has no AI, so it can't hold a free conversation. It answers fixed commands and posts
fixed formats. Denis's humour reaches the group in two ways:

1. **The approval post.** When an officer approves a list, Denis (Claude, in the officer's session)
   writes the caption and signature as today, and the session posts the screenshot to the group.
2. **A bank of lines** (`bot/lines.json`) that Claude writes ahead of time, following the rules in
   `denis.md`. The scheduled posts pick from it: a greeting, a sign-off, a signature. The officers
   ask Denis to refresh it now and then. The lines are generic (coffee, 05:00, Golani, יצחק's
   תרגילים), never about a specific soldier, because nobody checks them against the day's list.

The task digest itself stays serious, per `denis.md`: only the greeting and sign-off are playful.

## Components

```
 Officer's phone / PC                     Free services
 ┌──────────────────────────┐            ┌──────────────────────────────┐
 │ Claude app / Claude Code │──writes──▶ │ Google Sheet שבצק_01         │
 │ (guard-duty plugin)      │            │ (rounds, משימות, לקחים, לוג,  │
 │                          │            │  טלגרם)                       │
 │ scripts/telegram_post.py │─┐          └──────────────▲───────────────┘
 └──────────────────────────┘ │                         │ reads (viewer)
                              │          ┌──────────────┴───────────────┐
                              │          │ GitHub Actions (cron)        │
                              │          │ bot/digest.py                │
                              │          └──────────────┬───────────────┘
                              │ posts                   │ posts
                              ▼                         ▼
                        ┌──────────────────────────────────┐
                        │ Telegram: unit group  (@DenisBot) │
                        └──────────────────────────────────┘
```

1. **Telegram bot**: created in @BotFather. Privacy mode stays **on**, so in the group it sees only
   commands, @mentions and replies to it. Added to the group as a member; it doesn't need admin.
2. **Google service account**: a free Google Cloud project with the Sheets API on, and one service
   account. The sheet is shared with it as **Viewer**. The bot can't change the sheet even if
   something goes wrong.
3. **`scripts/telegram_post.py`** (new, in the plugin): sends a text, or a photo with a caption, to
   the group through the Bot API. The skill calls it after an approval, right after the
   screenshot. Standard library only (`urllib`), like the rest of the scripts.
4. **`bot/digest.py`** (new, outside the plugin): reads `משימות` and `טלגרם`, builds the digest,
   and posts it. Run by GitHub Actions on a schedule.
5. **`.github/workflows/digest.yml`**: the cron schedule. GitHub cron is in UTC, so it is written
   for Israel time and has to be adjusted when the clocks change (or the script checks the
   local hour and skips). GitHub may start a scheduled run a few minutes late, which is fine
   for a digest.

### Secrets

| Secret | Where |
|---|---|
| `TELEGRAM_BOT_TOKEN`, `TELEGRAM_GROUP_ID` | GitHub Actions secrets, and on each officer's machine as environment variables or a file outside the repo |
| Service-account JSON | GitHub Actions secrets only |

Nothing secret is committed. Anyone with the bot token can post as Denis, so if it leaks, revoke it
in @BotFather and replace it in both places.

## Tagging people

Telegram tags by @username or by user ID, not by Hebrew name. A new sheet tab, `טלגרם`:

`שם | תפקיד | username | user_id`

- `שם` matches the names in the lists and in `משימות` (`הכט`).
- `תפקיד` is for role owners (`רס"פ`, `נשקייה`, `מ"מ 2`): a task owned by `רס"פ` tags whoever is
  the רס"פ now. When the role changes hands, edit this one row.
- `username` is enough to start with. `user_id` is optional (phase 2 can fill it in by itself), and
  is needed only for people without a username.
- No match → the name is written plainly, without a tag, and the digest says `לא מתויג: X` at
  the end, so the officers can fill in the row.

Officers fill the tab through Denis ("תוסיף להכט את @hecht_g"). Each write gets a `לוג` row,
as usual.

## What gets posted

| When (Israel time) | What | Phase |
|---|---|---|
| After an officer approves a list | Screenshot + Denis's caption and signature | 1 |
| Daily 08:00, only if there are open tasks | Open tasks by category, owner tagged, days open; tasks open > 7 days and without an owner flagged at the end | 1 |
| Sunday 09:00 | Responsibility board (as `/owners`) | 1 |
| On request of an officer in Claude | Any approved text: lessons for the soldiers, an announcement | 1 |
| 20 min before each shift | "@soldier, יוסטור ב-03:00" | 2 |

**Quiet hours:** nothing scheduled between 22:00 and 07:00, except the phase-2 shift reminders,
which are the point.

Example digest:

```
בוקר טוב, כאן דניס. הקפה מוכן, המשימות פחות.

משימות פתוחות · 16/10

ציוד
#12 מחסנית שבורה · הכט · @rasap_unit · 3 ימים
#15 משקפת לילה לעמדה דרומית · @neshkia · 9 ימים

לוגיסטיקה
#14 מים לעמדות · @rasap_unit · 1 יום

פתוחות יותר מ-7 ימים: #15
בלי אחראי: אין

— דניס, בשירות גולני
```

## Commands in the group (phase 2)

Read-only, from a fresh read of the sheet. Handled only in phase 2, because answering needs a
process that is reachable all the time.

| Command | Answer |
|---|---|
| `/myshift` | The sender's next shifts in the current round (matched through `טלגרם`) |
| `/now` | Who is on each stand right now |
| `/tasks` | Open tasks, short |
| `/lessons` | Lessons for the soldiers (only the ones the officers approved for them) |

Anything else, including requests to change the list, gets: "רק המפקדים משנים את הרשימה, דרכי
באפליקציה". The bot can't change the sheet anyway.

## Hosting, at ₪0

- **Phase 1: GitHub Actions only.** No server. The repo is private; GitHub's free plan includes a
  monthly allowance of Actions minutes for private repos, and two short runs a day use a small
  part of it. Check usage under Settings → Billing after the first month.
- **Phase 2: Google Cloud Run + Cloud Scheduler** for the commands (Telegram webhook) and the
  shift reminders (a job every 15 minutes). Both have free tiers that this load stays inside,
  and Cloud Run sleeps between requests. Google asks for a billing account to be on file
  even for the free tier. Set a budget alert at ₪1 so any charge is caught on day one.
  The free tiers can change; re-check them before phase 2.
  - Every-15-minute reminders on GitHub Actions instead would use too many minutes, so they wait
    for phase 2.

## Memory

- **Long-term:** the sheet is the memory, as today: rounds, `משימות`, `לקחים`, `לוג`, `טלגרם`.
- **Officer conversations:** the Claude session, as today.
- **The bot:** keeps nothing. Every run reads the sheet fresh. The only thing it stores is the
  date of its last digest (in the Actions cache), so it doesn't post twice.

## Security

- **Approval first.** Telegram servers (abroad) get the soldiers' names, shift hours and open
  tasks. Get the unit's information security officer (ביטחון מידע / קב"ט) to approve it before
  phase 1, and post only what is already sent on WhatsApp today.
- No stand locations, no gear serial numbers and no weapons details in the group. Task text for
  the group is the short `מה` column only, and categories can be left out of the digest (e.g. `מבצעי`)
  if the security officer asks.
- The group is private. Invite links are revoked after use.
- The bot is read-only on the sheet. Only officers' Claude sessions write, and only after
  approval, as today.
- Officer-only drafts never go to the group: `telegram_post.py` is called only after an approval.

## Phases

0. **Approvals:** both officers sign off on this doc; the security officer approves.
1. **Group posts:** bot + group, `טלגרם` tab, `telegram_post.py` and the skill step after
   approval, `bot/lines.json`, daily digest and weekly board on GitHub Actions.
2. **Commands and reminders:** Cloud Run webhook, `/myshift` `/now` `/tasks` `/lessons`, shift
   reminders, `user_id` filled in when people use a command.
3. **Later, only if needed:** a paid API key for free conversation with Denis in the group. Not part
   of the ₪0 budget.

## Open questions for the officers

1. Which group: the whole unit, or one per platoon?
2. Digest times: 08:00 daily and Sunday 09:00 OK?
3. Do the soldiers want to be tagged (it notifies them)? Tag only the owner, or the soldier too?
4. Which task categories stay out of the group?
5. Who creates the bot in @BotFather and owns the token?
