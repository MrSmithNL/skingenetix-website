#!/usr/bin/env python3
"""Build a sheet of one bundle's SELECTED frames, and open it.

    python3 scripts/selection-sheet.py <selection-manifest.json> [--tile 420] [--cols 5]

WHY THIS IS A SCRIPT
`wave-contact-sheet.py` exists because the wave sheet was hand-written about eight times in one
day and drifted. The SELECTION sheet - the read-back that shows Malcolm what his refs actually
resolved to - was still being hand-built every round, which is the same trap one step later.

IT READS THE MANIFEST, NOT THE FOLDER. A folder listing sorts alphabetically, which puts Z276
next to Z305 and hides the ref order Malcolm sent. The manifest carries the order, the slot and
the supplier, so the sheet can be labelled with all three and checked against what he wrote.

EVERY TILE CARRIES REF + SUPPLIER + SLOT. The ref is what he typed, the supplier is the only
stable identifier (grid position is a function of how many files happen to be present), and the
slot is what he can actually recognise.

Author: Claude Code, 2026-09-14.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DESKTOP = Path.home() / "Desktop"


def font(sz, bold=True):
    from PIL import ImageFont
    name = "Arial Bold.ttf" if bold else "Arial.ttf"
    try:
        return ImageFont.truetype(f"/System/Library/Fonts/Supplemental/{name}", sz)
    except Exception:
        return ImageFont.load_default()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest", help="selection manifest, OR a folder with --folder")
    ap.add_argument("--folder", action="store_true",
                    help="read the FOLDER rather than the manifest. Use this once Malcolm has "
                         "worked in the folder himself - he adds and swaps files there, and a "
                         "manifest-driven sheet would silently omit anything he put in.")
    ap.add_argument("--tile", type=int, default=420)
    ap.add_argument("--cols", type=int, default=5)
    ap.add_argument("--out")
    a = ap.parse_args()

    from PIL import Image, ImageDraw

    if a.folder:
        folder = Path(a.manifest)
        man = {"wave": folder.name}
        picks = []
        for f in sorted(folder.iterdir()):
            if f.suffix.lower() not in (".png", ".jpg", ".jpeg"):
                continue
            m = re.match(r"^([A-Z]+\d+)-(.+?)-([a-z0-9]+(?:_[a-z0-9]+)*_\d+)\.png$", f.name)
            picks.append({"ref": m.group(1) if m else "ADDED",
                          "slot": m.group(2) if m else f.stem,
                          "supplier": m.group(3) if m else "supplied by Malcolm",
                          "saved_as": f.name})
    else:
        man = json.loads(Path(a.manifest).read_text())
        folder = ROOT / man["folder"]
        picks = man["selected"]
    missing = [p["saved_as"] for p in picks if not (folder / p["saved_as"]).exists()]
    if missing:
        sys.exit("missing from the selection folder:\n  " + "\n  ".join(missing))

    S, PAD, CAP, HDR = a.tile, 12, 44, 54
    cols = min(a.cols, len(picks))
    rows = (len(picks) + cols - 1) // cols
    W = PAD + cols * (S + PAD)
    H = HDR + rows * (S + CAP + PAD) + PAD
    sheet = Image.new("RGB", (W, H), (18, 18, 18))
    dr = ImageDraw.Draw(sheet)

    fh, fr, fs = font(30), font(21), font(16, bold=False)
    dr.text((PAD, 14), f'{man["wave"]}   —   {len(picks)} selected',
            fill=(120, 190, 255), font=fh)

    for i, p in enumerate(picks):
        r, c = divmod(i, cols)
        x = PAD + c * (S + PAD)
        y = HDR + r * (S + CAP + PAD)
        im = Image.open(folder / p["saved_as"]).convert("RGB")
        im.thumbnail((S, S), Image.LANCZOS)
        sheet.paste(im, (x + (S - im.width) // 2, y + (S - im.height) // 2))
        dr.text((x, y + S + 5), f'{p["ref"]}   {p["supplier"]}', fill=(245, 235, 220), font=fr)
        short = p["slot"].split("-", 2)[-1] if p["slot"].count("-") >= 2 else p["slot"]
        dr.text((x, y + S + 27), short, fill=(150, 150, 150), font=fs)

    out = Path(a.out) if a.out else DESKTOP / f'skingenetix-selected-{man["wave"]}.png'
    sheet.save(out)
    sheet.save(DESKTOP / "skingenetix-renders.png")
    print(f"{out}\n  {len(picks)} tiles, {sheet.size[0]}x{sheet.size[1]}")
    subprocess.run(["open", str(DESKTOP / "skingenetix-renders.png")], check=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
