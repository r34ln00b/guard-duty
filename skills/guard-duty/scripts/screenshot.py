#!/usr/bin/env python3
"""Render a stretch of the guard list as a PNG to share with the soldiers.

Usage: python screenshot.py rows.json --out list.png

The JSON format is documented in SKILL.md ("Screenshot for the soldiers").
Needs Pillow (python -m pip install --user pillow).
"""
import argparse
import json
import os
import re
import sys

from PIL import Image, ImageDraw, ImageFont, features

STANDS = ["ש.ג", "יוסטור", "דרומית", "פטרול", "תצפית"]
COLORS = {
    "yellow": "#FFFF00",  # מחלקה 2
    "green": "#00FF00",   # מחלקה 3
    "pink": "#FF00FF",    # מפלג / חפ"ק
    "white": "#FFFFFF",
}
HEADER_BG = "#D9D9D9"
DAY_BG = "#F2F2F2"
GRID = "#000000"
MERGE_UP = "^"  # a cell holding only this continues the cell above (4h daytime תצפית)
FONT_CANDIDATES = [
    "C:/Windows/Fonts/arial.ttf",
    "C:/Windows/Fonts/segoeui.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
]
HEBREW = re.compile(r"[\u0590-\u05FF]")
HAS_RAQM = features.check("raqm")


def visual(text):
    """Without libraqm Pillow draws Hebrew left-to-right, so reverse it by hand,
    keeping runs of digits/Latin (03:00, 16/10) in reading order."""
    if HAS_RAQM or not HEBREW.search(text):
        return text
    tokens = re.findall(r"[0-9A-Za-z][0-9A-Za-z:/\-]*|.", text)
    return "".join(reversed(tokens))


def wrap(text, font, max_w):
    """Split text into lines no wider than max_w (measured in logical order)."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if cur and font.getlength(visual(trial)) > max_w:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    return lines + [cur] if cur else lines


def load_font(path, size):
    for p in [path] if path else FONT_CANDIDATES:
        if p and os.path.exists(p):
            engine = ImageFont.Layout.RAQM if HAS_RAQM else ImageFont.Layout.BASIC
            return ImageFont.truetype(p, size, layout_engine=engine)
    sys.exit("No font with Hebrew found; pass --font PATH (e.g. C:/Windows/Fonts/arial.ttf)")


def cell_color(cell, groups, explicit):
    if explicit:
        return COLORS.get(explicit, explicit)
    name = cell.strip()
    if not name:
        return COLORS["white"]
    if "מפלג" in name or "חפק" in name or 'חפ"ק' in name:
        return COLORS["pink"]
    for color, names in groups.items():
        if name in [n.strip() for n in names]:
            return COLORS.get(color, color)
    return COLORS["white"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rows_json")
    ap.add_argument("--out", default="guard_list.png")
    ap.add_argument("--font")
    ap.add_argument("--size", type=int, default=30)
    args = ap.parse_args()

    with open(args.rows_json, encoding="utf-8") as f:
        cfg = json.load(f)
    stands = cfg.get("columns", STANDS)
    groups = cfg.get("groups", {})
    rows = cfg["rows"]
    font = load_font(args.font or cfg.get("font"), args.size)

    headers = ["יום", "שעה"] + stands
    ncols = len(headers)
    # grid[r][c] = (text, bg) or None when covered by a merge from above
    grid, spans = [], {}
    last_day_row = None
    for r, row in enumerate(rows):
        cells = list(row.get("cells", [])) + [""] * len(stands)
        out = []
        day = row.get("day", "")
        if day or last_day_row is None:
            out.append((day, DAY_BG))
            last_day_row = r
            spans[(r, 0)] = 1
        else:
            out.append(None)
            spans[(last_day_row, 0)] += 1
        out.append((row.get("time", ""), DAY_BG))
        spans[(r, 1)] = 1
        for c, cell in enumerate(cells[: len(stands)]):
            col = c + 2
            color = None
            if isinstance(cell, dict):
                cell, color = cell.get("name", ""), cell.get("color")
            cell = str(cell or "")
            if cell == MERGE_UP and r > 0:
                up = r - 1
                while grid[up][col] is None:
                    up -= 1
                spans[(up, col)] += 1
                out.append(None)
            else:
                out.append((cell, cell_color(cell, groups, color)))
                spans[(r, col)] = 1
        grid.append(out)

    pad = args.size // 2
    col_w = []
    for c in range(ncols):
        texts = [headers[c]] + [g[c][0] for g in grid if g[c]]
        w = max(font.getlength(visual(t)) for t in texts)
        col_w.append(int(w) + 2 * pad + args.size)
    row_h = args.size + 2 * pad
    title = cfg.get("title", "")
    title_h = row_h if title else 0
    width = sum(col_w) + 1
    table_h = title_h + row_h * (len(rows) + 1) + 1
    # Denis's line under the table: same font, a bit smaller, wrapped to the table width
    cap_font = load_font(args.font or cfg.get("font"), int(args.size * 0.8))
    cap_lines = wrap(cfg.get("caption", ""), cap_font, width - 2 * pad)
    cap_line_h = int(args.size * 0.8) + pad // 2
    cap_h = len(cap_lines) * cap_line_h + 2 * pad if cap_lines else 0
    height = table_h + cap_h
    img = Image.new("RGB", (width, height), "white")
    d = ImageDraw.Draw(img)

    # right-to-left: column 0 (יום) is the rightmost
    x_right = [width - 1 - sum(col_w[:c]) for c in range(ncols)]

    def box(c, top, nrows, text, bg):
        x1 = x_right[c]
        x0 = x1 - col_w[c]
        y1 = top + row_h * nrows
        d.rectangle([x0, top, x1, y1], fill=bg, outline=GRID, width=1)
        if text:
            d.text(((x0 + x1) / 2, (top + y1) / 2), visual(text), font=font,
                   fill="black", anchor="mm")

    if title:
        d.text((width / 2, title_h / 2), visual(title), font=font, fill="black", anchor="mm")
    for c, h in enumerate(headers):
        box(c, title_h, 1, h, HEADER_BG)
    for r, out in enumerate(grid):
        top = title_h + row_h * (r + 1)
        for c, cell in enumerate(out):
            if cell is not None:
                box(c, top, spans[(r, c)], cell[0], cell[1])

    for i, line in enumerate(cap_lines):
        y = table_h + pad + cap_line_h * i + cap_line_h / 2
        d.text((width / 2, y), visual(line), font=cap_font, fill="#333333", anchor="mm")

    img.save(args.out)
    print(json.dumps({"status": "OK", "out": args.out, "rows": len(rows),
                      "bidi": "raqm" if HAS_RAQM else "manual"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
