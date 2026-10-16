# יומן: משימות, אחריות ולקחים

Read this when the user mentions missing or broken gear, an open issue, who is responsible for
something, or an operational lesson (לקח), or runs one of the commands below. Everything lives in
two tabs of the shared sheet `שבצק_01`, so both officers see the same thing. Same sheet rules as
in SKILL.md: read the tab before writing, change only the rows you touch, centre every cell in the
tab's font, log every write in `לוג`, and end with the sheet link.

## Tab `משימות`

Create it if missing, with this header row (columns A-I):

`# | נפתח | קטגוריה | מה | חייל/פריט | אחראי | סטטוס | נסגר | הערות`

- `#`: running number (last `#` + 1). Never reuse or renumber.
- `נפתח` / `נסגר`: dates as `DD/MM/YYYY`.
- `סטטוס`: `פתוח`, `בטיפול` or `נסגר`. Rows are never deleted; a done task is `נסגר`.
- `אחראי`: a role or a name (`רס"פ`, `נשקייה`, `מ"מ 2`, `הכט`). Ask for it if the user didn't say;
  if they don't know, leave it empty (it shows up as "בלי אחראי").

### Categories (`קטגוריה`)

Always set one. Pick it yourself from what the task is about, and ask only when it really could be
two. The officers can add a category here.

| קטגוריה | For example |
|---|---|
| ציוד | נשק, מחסניות, אופטיקה, קסדות, ווסטים, קשר, משקפות |
| לוגיסטיקה | אוכל, מים, דלק, מגורים, ניקיון, הובלות, הזמנות |
| מבצעי | עמדות, גדר, תאורה, מצלמות, שערים, נהלים ותרגולות |
| רכבים | דורסים, ג'יפים, צמיגים, טיפולים |
| כוח אדם | יציאות, החלפות, חיילים חסרים, הכשרות |
| אחר | כל השאר |

### Adding

1. Read the whole tab. If an open (`פתוח`/`בטיפול`) row is about the same thing, even in other
   words ("המחסנית של הכט שבורה" = "תקלה במחסנית, הכט"), update that row (owner, status, a note)
   instead of adding a new one, and say so.
2. Otherwise add a row: `נפתח` today, status `פתוח`.
3. Reply in one or two lines: `#`, what, category, owner.

### Closing and updating

- Find the task by `#` or by meaning. If more than one open task could match, list them and ask.
- Closing: status `נסגר`, `נסגר` today, and a note if the user said how it was fixed.
- "מטפלים בזה" / "הוזמן": status `בטיפול` plus a note.

### Asking

Answer from a fresh read of the tab, as a short list, never as a dump of the table:

- **Open tasks:** `פתוח` and `בטיפול` only, grouped by category, then by owner, oldest first.
  Each line: `#`, what, soldier/item, owner, and days open.
- **Filters:** a category, an owner or a soldier/item ("מה פתוח בציוד?", "מה על הרס"פ?",
  "מה עם הכט?"). Match by meaning, not spelling.
- **Responsibility board (`/owners`):** per owner, the number of open tasks and the list by category.
  Owners with the most open tasks first, and a `בלי אחראי` group at the end.
- Always flag at the end, in one line each: tasks with no owner, and tasks open more than 7 days.

## Tab `לקחים`

Only **operational lessons**: things the unit learned and should keep doing. For example:
- מפתחות הבונקר תמיד על הוו בחמ"ל, כדי שכל חייל יוכל להוציא תחמושת.
- הדורסים חונים במרחק טקטי אחד מהשני, כדי שטיל נ"ט אחד לא יפגע בכולם.

Create it if missing, with this header row (columns A-F):

`# | תאריך | לקח | תחום | מקור/אירוע | נכתב ע"י`

- `תחום`: `נשקייה`, `רכבים-דורסים`, `שמירה`, `חמ"ל` or `כללי`.
- `לקח`: rewrite what the user said as one short rule anyone can act on (what to do, and why in a
  few words). Show it to the user before writing if you changed the meaning or the wording much.
- `מקור/אירוע`: what led to it, if the user said (a תרגיל, an event, a check). Optional.
- Before adding, read the tab. If a similar lesson exists, offer to sharpen it instead of adding a
  second one.
- A lesson about something broken or missing is also a task: offer to open it in `משימות`.

### Bringing lessons up when they matter

- Building **דורסים**: read the `רכבים-דורסים` and `כללי` lessons.
- Building **שמירות**: read the `שמירה` and `חמ"ל` lessons.
- Mention the relevant ones in the chat, one line, after the draft. Never write them into the list,
  the round tab or the WhatsApp text on your own.
- **For the soldiers:** only when the officer asks or approves, prepare a short Hebrew text
  (a title like `לקחים · סבב 3` and the lessons as a numbered list) to paste in WhatsApp.

## Logging

Every write gets a `לוג` row: `סבב` = the current round tab, `מ-`/`עד` empty, status `משימה` or
`לקח`, and a short note in `הערות` (`משימה #12 נפתחה: מחסנית שבורה, הכט, אחראי רס"פ`,
`משימה #12 נסגרה`, `לקח #4 נוסף: מפתחות הבונקר בחמ"ל`). `נבנה ע"י` / `נכתב ע"י` is the
name the user gave once per session; ask for it if you don't have it yet.

## Tone

Tasks and lessons are serious, like the list: nothing playful in the tabs, the `לוג` or text for the
soldiers. In the chat, a light line about a long open list or the רס"פ's backlog is fine. Never
tease the soldier whose gear is broken or missing.
