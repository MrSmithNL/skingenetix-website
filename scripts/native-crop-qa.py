#!/usr/bin/env python3
"""Crop one region of every candidate in a slot at NATIVE pixels and stack them to look at.

    python3 scripts/native-crop-qa.py <slot-dir> <out.png>
    python3 scripts/native-crop-qa.py <slot-dir> <out.png> --box 0.40 0.35 0.95 1.00
    python3 scripts/native-crop-qa.py <run-dir>/*/ ~/Desktop/qa.png --box ...   # one slot at a time

WHY THIS EXISTS. A contact sheet cannot judge a printed surface. The downscale breaks thin
type and on this project once resampled a correct "PDRN" into "PORN" — so the sheet is for
composition, and anything that could carry lettering has to be looked at at full resolution.
The two recurring cases:

  - a white clinical coat, which invites an embroidered name, and an embroidered name on a
    banner is an invented brand
  - a plain white carton, which invites a shipping label, a barcode or a courier logo, and
    FLUX.2 prints characters unasked (it put graduation digits on lab glassware on all three
    waves of 2026-08-25 and is the only engine that does)

⚠️ THE TRAP THIS SCRIPT IS BUILT AROUND. `banner-contact-sheet.py` leaves a hidden `.sheet/`
directory inside every slot holding 900x486 DOWNSCALED tiles plus assembled `rowN.png` files.
A QA pass that walks subdirectories finds those and crops them — so the check written to see
past the downscale ends up inspecting the downscale, and reports a clean coat from evidence
that could not have shown an embroidered one. It fails silently: on 2026-08-30 the only
symptom was the count not reconciling, 17 crops out of 11 candidates.

So: top-level glob only, never rglob, never an iterdir() subdirectory fallback, and an assert
on width — the assert is what turns the next silent recurrence into a stack trace.

--box is a fraction of frame width/height (left top right bottom), so it holds across the
five different sizes the suppliers return for one request. Default is the right-hand lower
area, where every banner brief in this project puts its subject.

Author: Claude Code, 2026-08-30.
"""
import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

#: Below this, the file is a contact-sheet tile rather than a generated master. The smallest
#: real master seen from any supplier on a wide brief is 2048px (gpt-image / FLUX.2 cap).
MIN_MASTER_W = 1800
FONT_PATH = "/System/Library/Fonts/Supplemental/Arial.ttf"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slot", type=Path, help="a single slot directory of candidates")
    ap.add_argument("out", type=Path)
    ap.add_argument("--box", type=float, nargs=4, default=[0.45, 0.50, 1.0, 1.0],
                    metavar=("L", "T", "R", "B"),
                    help="crop as fractions of frame width/height (default right lower area)")
    ap.add_argument("--width", type=int, default=1400,
                    help="cap the displayed width; crops wider than this are downscaled ONLY "
                         "for the sheet, after the native crop has been taken")
    args = ap.parse_args()

    # Top-level, non-hidden PNGs only. See the .sheet note in the docstring.
    imgs = sorted(p for p in args.slot.glob("*.png") if not p.name.startswith("."))
    if not imgs:
        raise SystemExit(f"no candidates in {args.slot}")

    l, t, r, b = args.box
    font = ImageFont.truetype(FONT_PATH, 26)
    crops = []
    for p in imgs:
        im = Image.open(p).convert("RGB")
        w, h = im.size
        assert w >= MIN_MASTER_W, (
            f"{p.name} is {w}px wide — that is a contact-sheet tile, not a master. "
            f"Something globbed into .sheet/")
        c = im.crop((int(w * l), int(h * t), int(w * r), int(h * b)))
        if c.width > args.width:
            c = c.resize((args.width, int(c.height * args.width / c.width)), Image.LANCZOS)
        crops.append((f"{p.stem}  [{w}x{h}]", c))

    cw = max(c.width for _, c in crops)
    ch = max(c.height for _, c in crops)
    sheet = Image.new("RGB", (cw, len(crops) * (ch + 34)), "black")
    d = ImageDraw.Draw(sheet)
    for i, (name, c) in enumerate(crops):
        y = i * (ch + 34)
        sheet.paste(c, (0, y + 34))
        d.rectangle([0, y, cw, y + 34], fill="#333")
        d.text((8, y + 5), name, font=font, fill="white")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(args.out)
    print(f"{len(crops)} native crops -> {args.out}  ({sheet.width}x{sheet.height})")


if __name__ == "__main__":
    main()
