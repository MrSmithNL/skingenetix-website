#!/usr/bin/env python3
"""One contact sheet of every before/after candidate generated in the last three days.

    python3 scripts/before-after-contact-sheet.py

WHY THE RUN FOLDERS CANNOT BE DATED THE OBVIOUS WAY
Two independent traps, and each on its own would give the wrong answer:

  1. **The folder name carries the CONFIG's date, not the run date.** 147 of the 212 run folders
     are named `2026-08-22-…`; git says their configs were added on the 27th and 28th.
  2. **The mtimes were bulk-reset** — 104 folders all read `2026-08-26 16:13`.

So the run date is taken from **git**: the date the matching `configs/banners/<stem>.json` was
first committed. A run folder is `2026-08-22-multi-<config stem>`.

WHY THE BRIEF LIST IS EXPLICIT AND NOT A KEYWORD MATCH
Grepping the configs for "before"/"after" pulls in 96 briefs and 1,707 images — explainer
diagrams, mechanism illustrations, hero group shots, glow models. Almost all of those mention a
before/after somewhere without being one. The families below are the ones that actually produce a
before/after PAIR, listed by hand.

Every tile is captioned with a short id (`B0001`) and its run and supplier. The id is what to
copy back; `before-after-index.csv` next to the sheet maps every id to its full path.

Author: Claude Code, 2026-08-29.
"""
import csv
import json
import re
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
RUNS = ROOT / "assets" / "ai-generated"
CFG = ROOT / "configs" / "banners"
OUT = Path.home() / "Desktop"

SINCE = "2026-08-26"

# The brief families that genuinely produce a before/after pair.
FAMILIES = [
    (re.compile(r"^block-acetyl-research-selfie"), "acetyl-selfie"),
    (re.compile(r"^block-acetyl-research-fullface$"), "acetyl-fullface"),
    (re.compile(r"^block-acetyl-research-before-after"), "acetyl-ba"),
    (re.compile(r"^block-copper-peptide-ba-"), "copper-ba"),
    (re.compile(r"^block-glutathione-research-before-after"), "glut-ba"),
    (re.compile(r"^block-pdrn-research-crows-feet$"), "pdrn-crows"),
    (re.compile(r"^block-brightening-glow-pair$"), "bright-pair"),
]

TILE = 220
CAP = 30
COLS = 34


def added(path: Path) -> str:
    return subprocess.run(
        ["git", "log", "--diff-filter=A", "--format=%ad", "--date=short", "-1", "--", str(path)],
        capture_output=True, text=True, cwd=ROOT).stdout.strip() or "UNTRACKED"


def short(stem: str) -> str:
    for rx, label in FAMILIES:
        if rx.match(stem):
            tail = rx.sub("", stem).strip("-") or "base"
            return f"{label}/{tail}" if tail != "base" else label
    return stem


def collect():
    items = []
    for cfg in sorted(CFG.glob("*.json")):
        stem = cfg.stem
        if not any(rx.match(stem) for rx, _ in FAMILIES):
            continue
        d = added(cfg)
        if d != "UNTRACKED" and d < SINCE:
            continue
        for run in sorted(RUNS.glob(f"*-multi-{stem}")):
            for f in sorted(run.rglob("*")):
                # `_source`, `_mask`, `_blank` are inputs to an edit, not candidates
                if f.suffix.lower() not in (".png", ".jpg", ".jpeg") or f.name.startswith("_"):
                    continue
                items.append({"date": d, "run": short(stem), "slot": f.parent.name,
                              "supplier": f.stem.split("-")[-1], "path": f})
    return items


def main():
    items = collect()
    if not items:
        raise SystemExit("nothing matched")
    for i, it in enumerate(items, start=1):
        it["id"] = f"B{i:04d}"

    rows = (len(items) + COLS - 1) // COLS
    W, H = COLS * TILE, rows * (TILE + CAP)
    sheet = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(sheet)
    try:
        f_id = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 15)
        f_sm = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 11)
    except OSError:
        f_id = f_sm = ImageFont.load_default()

    for n, it in enumerate(items):
        r, c = divmod(n, COLS)
        x, y = c * TILE, r * (TILE + CAP)
        try:
            im = Image.open(it["path"]).convert("RGB")
        except Exception:
            continue
        w, h = im.size
        s = min(w, h)
        im = im.crop(((w - s) // 2, 0, (w - s) // 2 + s, s)).resize((TILE, TILE), Image.LANCZOS)
        sheet.paste(im, (x, y))
        d.rectangle([x, y + TILE, x + TILE, y + TILE + CAP], fill=(17, 17, 17))
        d.text((x + 4, y + TILE + 1), it["id"], fill="white", font=f_id)
        d.text((x + 52, y + TILE + 2), it["run"][:26], fill=(170, 170, 170), font=f_sm)
        d.text((x + 52, y + TILE + 15), f'{it["slot"][:20]} {it["supplier"]}',
               fill=(140, 140, 140), font=f_sm)

    img = OUT / "skingenetix-before-after-ALL.jpg"
    sheet.save(img, "JPEG", quality=88, optimize=True, progressive=True)

    idx = OUT / "skingenetix-before-after-index.csv"
    with idx.open("w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=["id", "date", "run", "slot", "supplier", "path"])
        w.writeheader()
        for it in items:
            w.writerow({**it, "path": str(it["path"])})

    print(f"{len(items)} candidates from {len({i['run'] for i in items})} briefs")
    print(f"sheet  {img}  {W}x{H}  {img.stat().st_size // 1024 // 1024} MB")
    print(f"index  {idx}")


if __name__ == "__main__":
    main()
