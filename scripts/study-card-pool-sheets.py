#!/usr/bin/env python3
"""Numbered Desktop sheets of the Clinical studies card-image pool, so Malcolm can pick by number.

Author: Claude (Opus 5.5) for Malcolm Smith · 2026-09-30
Purpose: Malcolm (2026-09-30): "show me the selection and number them so i can choose". The pool index
configs/banners/clinical-studies-card-image-pool-2026-09-29.json holds 2,125 unused science images (no image
already on the store); the 2026-09-29 sheets were drawn by hand and were gone from the Desktop a day later.
This rebuilds them from the index, so the numbers on the sheet are the index's own refs (e.g. CU-037) and any
ref Malcolm names resolves to exactly one file in any session.

    python3 scripts/study-card-pool-sheets.py            # all four pools, then open them
    python3 scripts/study-card-pool-sheets.py CU ARG     # only these pools
    python3 scripts/study-card-pool-sheets.py --no-open

Not a shortlist: every ref in the index is drawn, in the index's own order (no person or product, then a person
or hand, then a product in frame), with a header row where each group starts. Tiles show the WHOLE image
(letterboxed), because a card crops it later and Malcolm must see what is there.
"""
import argparse
import json
import pathlib
import subprocess
from concurrent.futures import ThreadPoolExecutor

from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
POOL = ROOT / "configs/banners/clinical-studies-card-image-pool-2026-09-29.json"
DESKTOP = pathlib.Path.home() / "Desktop"
POOLS = {"CU": "Copper peptide (GHK-Cu) — for the Badenhorst 2016 card",
         "ARG": "Argireline — for the Raikou 2017 and Wang 2013 cards",
         "PDRN": "PDRN — for the Ye 2026 card",
         "GEN": "General science — usable on any card"}
COLS, ROWS, TILE, LABEL_H, PAD, HEAD_H = 10, 10, 210, 44, 12, 90
GROUPS = [("none", "No person, no product"), ("person", "A hand or person in frame"), ("product", "A product in frame")]


def font(size, bold=False):
    for f in (["/System/Library/Fonts/Supplemental/Arial Bold.ttf"] if bold else []) + [
            "/System/Library/Fonts/Supplemental/Arial.ttf", "/System/Library/Fonts/Helvetica.ttc"]:
        try:
            return ImageFont.truetype(f, size)
        except OSError:
            continue
    return ImageFont.load_default()


def group(v):
    return "product" if v["has_product"] else "person" if v["has_person"] else "none"


def thumb(path):
    im = Image.open(ROOT / path)
    im.draft("RGB", (TILE * 2, TILE * 2))
    im = im.convert("RGB")
    im.thumbnail((TILE, TILE))
    tile = Image.new("RGB", (TILE, TILE), (236, 236, 236))
    tile.paste(im, ((TILE - im.width) // 2, (TILE - im.height) // 2))
    return tile


def sheets_for(code, refs):
    """Lay the pool out in reading order: a header cell row where a group starts, then its tiles."""
    cells, last = [], None
    for ref, v in refs:
        g = group(v)
        if g != last:
            if cells and len(cells) % COLS:
                cells += [None] * (COLS - len(cells) % COLS)       # a group starts on a new row
            cells += [("HEAD", dict(GROUPS)[g])] + [None] * (COLS - 1)
            last = g
        cells.append((ref, v))
    per = COLS * ROWS
    return [cells[i:i + per] for i in range(0, len(cells), per)]


def draw(code, n, total, cells, thumbs):
    W = PAD + COLS * (TILE + PAD)
    H = HEAD_H + ROWS * (TILE + LABEL_H + PAD) + PAD
    sheet = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(sheet)
    refs = [c[0] for c in cells if c and c[0] != "HEAD"]
    d.text((PAD, 18), f"{POOLS[code]}  ·  sheet {n} of {total}  ·  {refs[0]} to {refs[-1]}", fill="black", font=font(30, True))
    d.text((PAD, 56), "Pick by number, e.g. \"Badenhorst: CU-037\". Every image is shown whole; the card crops it to landscape.",
           fill=(90, 90, 90), font=font(20))
    for i, c in enumerate(cells):
        if not c:
            continue
        x, y = PAD + (i % COLS) * (TILE + PAD), HEAD_H + (i // COLS) * (TILE + LABEL_H + PAD)
        if c[0] == "HEAD":
            d.rectangle([x, y, W - PAD, y + TILE + LABEL_H], fill=(26, 26, 26))
            d.text((x + 24, y + TILE // 2 - 10), c[1], fill="white", font=font(40, True))
            continue
        ref, v = c
        sheet.paste(thumbs[ref], (x, y))
        d.text((x + 2, y + TILE + 4), ref, fill="black", font=font(30, True))
        d.text((x + 118, y + TILE + 14), v["supplier"] + (" (older)" if v.get("superseded") else ""), fill=(110, 110, 110),
               font=font(15))
    out = DESKTOP / f"skingenetix-study-images-{code}-{n}.png"
    sheet.save(out)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pools", nargs="*", default=list(POOLS))
    ap.add_argument("--no-open", action="store_true")
    a = ap.parse_args()
    index = json.loads(POOL.read_text())["refs"]
    for old in DESKTOP.glob("skingenetix-study-images-*.png"):   # our own sheets only: stale page counts would mislead
        old.unlink()
    written = []
    for code in a.pools:
        refs = sorted(((r, v) for r, v in index.items() if r.startswith(code + "-")), key=lambda rv: int(rv[0].split("-")[1]))
        with ThreadPoolExecutor(8) as ex:
            thumbs = dict(zip([r for r, _ in refs], ex.map(lambda rv: thumb(rv[1]["path"]), refs)))
        pages = sheets_for(code, refs)
        for n, cells in enumerate(pages, 1):
            written.append(draw(code, n, len(pages), cells, thumbs))
        print(f"  {code}: {len(refs)} images on {len(pages)} sheets")
    if not a.no_open:
        subprocess.run(["open", *map(str, written)])
    for w in written:
        print("  ", w)


if __name__ == "__main__":
    main()
