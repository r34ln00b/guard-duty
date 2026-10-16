#!/usr/bin/env python3
"""Count how many times each person held each duty (דורס, דורס א, כרמל א, תורנים) in past rounds.

Usage: python duty_history.py tab1.json [tab2.json ...] [--role תורנים]

Each JSON is a Google Sheets values read of one round tab from A1 (e.g. range "סבב 3!A1:Z150"),
saved as returned: {"range": "'סבב 3'!A1:Z150", "values": [[...], ...]}. Duty columns are found by
their header, so tabs with different layouts work. A merged 24h block (value only in its first row)
and a value repeated on every row of the block both count once per block.

Prints JSON: per role, each roster person's count (zero included), lowest first.
"""
import argparse
import json
import re
import sys
from collections import Counter

ROLES = [("דורס א", "דורס א"), ("דורס", "דורס"), ("כרמל א", "כרמל א"),
         ("תורנים", "תורנים"), ("תרנים", "תורנים")]
ROSTER_HEADERS = ("מחלקה", 'חפ"ק', 'מפל"ג')
TIME = re.compile(r"^\d{1,2}:\d{2}$")
MERGED_GAP = 6  # empty rows after a value that mean "merged block" rather than "left empty"


def role_of(header):
    h = header.strip()
    for prefix, role in ROLES:
        if h.startswith(prefix):
            return role
    return None


def read_tab(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    tab = data.get("tab") or re.sub(r"^'?(.*?)'?!.*$", r"\1", data.get("range", path))
    rows = [list(r) for r in data.get("values", [])]
    width = max((len(r) for r in rows), default=0)
    return tab, [r + [""] * (width - len(r)) for r in rows]


def roster_of(rows):
    """Names under the מחלקה / חפ"ק / מפל"ג headers, until the first row where all are empty."""
    for i, row in enumerate(rows):
        cols = [c for c, v in enumerate(row) if str(v).strip().startswith(ROSTER_HEADERS)]
        if cols:
            names = {}
            for r in rows[i + 1:]:
                vals = [str(r[c]).strip() for c in cols]
                if not any(vals):
                    break
                for c, v in zip(cols, vals):
                    if v and v not in ROSTER_HEADERS and not v.isdigit():
                        names[v] = str(row[c]).strip()
            return names
    return {}


def split_names(cell, roster):
    names = []
    for piece in re.split(r"[\n+,]", str(cell)):
        piece = piece.strip()
        if not piece or re.search(r"\d", piece):
            continue  # empty, or a template placeholder like "1,2,3"
        if piece in roster:
            names.append(piece)
            continue
        tokens = piece.split()
        i = 0
        while i < len(tokens):  # "אליעזר עקיבא שמואל", "דביר ו." (names may hold a space)
            two = " ".join(tokens[i:i + 2])
            if i + 1 < len(tokens) and two in roster:
                names.append(two)
                i += 2
            else:
                names.append(tokens[i])
                i += 1
    return names


def count_tab(rows, roster):
    header_i = next((i for i, r in enumerate(rows) if any(role_of(str(v)) for v in r)), None)
    if header_i is None:
        return {}
    header = rows[header_i]
    time_c = next((c for c, v in enumerate(header) if str(v).strip() == "שעה"), None)
    cols = {c: role_of(str(v)) for c, v in enumerate(header) if role_of(str(v))}
    counts = {role: Counter() for role in set(cols.values())}
    for c, role in cols.items():
        last, gap = set(), 0
        for r in rows[header_i + 1:]:
            if time_c is not None and not TIME.match(str(r[time_c]).strip()):
                continue
            v = str(r[c]).strip()
            if not v:
                gap += 1
                continue
            names = set(split_names(v, roster))
            # A person starts a new turn when they weren't in the cell above, or when the same
            # names come back after a merged block's empty rows. A short gap (a column left empty
            # overnight) or a partner swap mid-block doesn't start a new turn.
            new = names if gap >= MERGED_GAP else names - last
            counts[role].update(new)
            last, gap = names, 0
    return counts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tabs", nargs="+")
    ap.add_argument("--role", help="only this role (דורס, דורס א, כרמל א, תורנים)")
    args = ap.parse_args()

    total, per_tab, roster = {}, {}, {}
    for path in args.tabs:
        tab, rows = read_tab(path)
        tab_roster = roster_of(rows)
        roster.update(tab_roster)
        counts = count_tab(rows, tab_roster)
        per_tab[tab] = {role: dict(c) for role, c in counts.items()}
        for role, c in counts.items():
            total.setdefault(role, Counter()).update(c)

    out = {"tabs": list(per_tab), "roles": {}, "unknown_names": []}
    for role, c in total.items():
        if args.role and role != args.role:
            continue
        people = {n: c.get(n, 0) for n in roster}
        out["roles"][role] = sorted(
            [{"name": n, "group": roster.get(n, "?"), "count": k,
              "per_tab": {t: per_tab[t].get(role, {}).get(n, 0) for t in per_tab}}
             for n, k in people.items()],
            key=lambda p: (p["count"], p["name"]))
        out["unknown_names"] += sorted(n for n in c if n not in roster)
    out["unknown_names"] = sorted(set(out["unknown_names"]))
    json.dump(out, sys.stdout, ensure_ascii=False, indent=1)
    print()


if __name__ == "__main__":
    main()
