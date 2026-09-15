#!/usr/bin/env python3
"""Build a grid-referenced contact sheet for a generation wave, and open it.

    python3 scripts/wave-contact-sheet.py <wave-dir-or-name> [--partial] [--tile 350]
    python3 scripts/wave-contact-sheet.py --list

WHY THIS IS A SCRIPT AND NOT AN INLINE SNIPPET
It was re-written by hand about eight times in one day, and the hand-written versions drifted:
different tile sizes, different label formats, and one that built a sheet from a row that was
still generating.

IT REFUSES A PARTIAL ROW BY DEFAULT, and that is the whole point. A slot's candidates are
globbed alphabetically, so the column a tile occupies depends on HOW MANY FILES EXIST at the
moment the sheet is drawn. Sheet a row that is half-generated and its columns renumber as it
fills — on 2026-09-11 Malcolm picked "B5-B5 nbp_pro 02" off a 6-tile row that later grew to 10,
where column 5 is a different engine entirely. `--partial` allows it anyway and marks the row
"STILL FILLING" in the header, but the default is to leave it out.

EVERY TILE IS LABELLED WITH ITS SUPPLIER as well as its grid reference, because the supplier
name is the only stable identifier: grid position is a function of how many files happen to be
present, and a lost supplier (a 422, a refusal) silently shifts every column after it.

Author: Claude Code, 2026-09-11.
"""
import argparse
import json
import glob
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GEN = ROOT / "assets" / "ai-generated"
DESKTOP = Path.home() / "Desktop"
SUPPLIERS = ("seedream", "gpt_image", "nbp_pro", "nbp_flash", "luma", "flux2")


def find_wave(arg):
    p = Path(arg)
    if p.is_dir():
        return p
    hits = sorted(GEN.glob(f"*{arg}*"))
    hits = [h for h in hits if h.is_dir()]
    if not hits:
        sys.exit(f"no wave matching {arg!r}. --list to see them.")
    if len(hits) > 1:
        sys.exit("ambiguous:\n  " + "\n  ".join(h.name for h in hits))
    return hits[0]


def rows_of(wave):
    out = []
    for d in sorted(p for p in wave.iterdir() if p.is_dir() and not p.name.startswith("_")):
        files = sorted(glob.glob(str(d / "*.png")))
        if files:
            out.append((d.name, files))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("wave", nargs="?")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--partial", action="store_true",
                    help="include rows that are still generating (columns will renumber)")
    ap.add_argument("--tile", type=int, default=350)
    ap.add_argument("--expect", type=int, default=0,
                    help="candidates per slot when complete (suppliers x candidates); "
                         "without it, the largest row seen is assumed complete")
    ap.add_argument("--open", dest="do_open", action="store_true", default=True)
    ap.add_argument("--stable-labels", metavar="CONFIG",
                    help="take row letters from the CONFIG's full slot list rather than from the "
                         "rows that happen to exist. Lets a sheet be built mid-run with refs that "
                         "stay correct once the remaining slots land - normally the letters shift, "
                         "because they are assigned across the rows present at draw time.")
    a = ap.parse_args()

    if a.list or not a.wave:
        for d in sorted(GEN.iterdir()):
            if d.is_dir():
                n = len(glob.glob(str(d / "*" / "*.png")))
                if n:
                    print(f"  {n:>4}  {d.name}")
        return 0

    from PIL import Image, ImageDraw, ImageFont

    wave = find_wave(a.wave)
    rows = rows_of(wave)
    if not rows:
        sys.exit(f"no images in {wave}")
    # `full` cannot simply be the largest row seen: early in a run EVERY row is short, so the
    # largest is itself partial and the check passes on a row that is still filling. Two
    # anchors instead. First, --expect if given. Otherwise the largest row, BUT a wave with no
    # manifest.json has not finished — generate-multi writes it once at the very end — so the
    # last row is treated as in-flight regardless of its count.
    full = a.expect or max(len(f) for _, f in rows)
    running = not (wave / "manifest.json").exists()

    kept, dropped = [], []
    for i, (name, files) in enumerate(rows):
        in_flight = len(files) < full or (running and i == len(rows) - 1)
        (dropped if (in_flight and not a.partial) else kept).append((name, files))
    if running:
        print(f"wave still generating (no manifest.json yet) — {len(rows)} slots so far")
    if dropped:
        print("SKIPPED — still generating, columns would renumber "
              "(use --partial to include anyway):")
        for name, files in dropped:
            print(f"    {name}  ({len(files)}/{full})")
    if not kept:
        sys.exit("every row is partial; nothing stable to sheet yet")

    # Row letters normally come from the position in `kept`, which moves as a run fills. With a
    # config to hand they can come from the FULL slot list instead, so a ref given off a partial
    # sheet still resolves after the wave completes.
    fixed = None
    if a.stable_labels:
        ids = sorted(s["id"] for s in json.loads(Path(a.stable_labels).read_text())["slots"])
        fixed = {sid: (chr(ord("A") + i) if i < 26 else "A" + chr(ord("A") + (i - 26)))
                 for i, sid in enumerate(ids)}
        missing = [n for n, _ in kept if n not in fixed]
        if missing:
            sys.exit("config does not contain: " + ", ".join(missing[:4]))
        print(f"stable labels from {a.stable_labels}: {len(ids)} slots, "
              f"{len(kept)} drawn ({ids[0]}=A .. {ids[-1]}={fixed[ids[-1]]})")

    S, PAD, CAP, HDR = a.tile, 11, 28, 32
    W = PAD + full * (S + PAD)
    H = len(kept) * (HDR + S + CAP + PAD) + PAD
    sheet = Image.new("RGB", (W, H), (18, 18, 18))
    dr = ImageDraw.Draw(sheet)

    def F(sz):
        try:
            return ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", sz)
        except Exception:
            return ImageFont.load_default()

    fh, fc = F(22), F(16)
    # Row letters follow slot order, so a reference stays meaningful across a re-run.
    y = PAD
    for i, (name, files) in enumerate(kept):
        # A..Z then AA, AB, AC ... Row 26 used to be labelled "Z26", which made a tile read
        # "Z264" for row Z26 column 4 - parseable only because a column is always one digit,
        # and horrible to read back. Two-letter rows are unambiguous.
        letter = fixed[name] if fixed else (
            chr(ord("A") + i) if i < 26 else "A" + chr(ord("A") + (i - 26)))
        short = re.sub(r"^[a-z0-9-]*?-(?=[a-z])", "", name, count=1) or name
        tag = "" if len(files) >= full else f"   STILL FILLING {len(files)}/{full}"
        dr.text((PAD, y + 4), f"{letter}   {short}   ({len(files)}){tag}",
                fill=(245, 170, 90) if tag else (120, 190, 255), font=fh)
        y += HDR
        for j, p in enumerate(files):
            im = Image.open(p).convert("RGB").resize((S, S), Image.LANCZOS)
            x = PAD + j * (S + PAD)
            sheet.paste(im, (x, y))
            m = re.search(r"-(" + "|".join(SUPPLIERS) + r")_(\d+)\.png$", os.path.basename(p))
            sup = f"{m.group(1)} {m.group(2)}" if m else "?"
            dr.text((x, y + S + 6), f"{letter}{j+1}   {sup}", fill=(235, 235, 235), font=fc)
        y += S + CAP + PAD

    out = DESKTOP / f"skingenetix-{wave.name.replace('2026-08-22-multi-', '')}.png"
    sheet.save(out)
    sheet.save(DESKTOP / "skingenetix-renders.png")
    print(f"\n{out}")
    print(f"  {len(kept)} rows, {sum(len(f) for _, f in kept)} tiles, {sheet.size[0]}x{sheet.size[1]}")
    if a.do_open:
        subprocess.run(["open", str(DESKTOP / "skingenetix-renders.png")], check=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
