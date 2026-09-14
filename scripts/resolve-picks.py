#!/usr/bin/env python3
"""Resolve Malcolm's grid refs against a wave, copy them out, and write the manifest.

    python3 scripts/resolve-picks.py <wave> <dest-folder> A3 B5 C5 ... [--apply]
    python3 scripts/resolve-picks.py <wave> <dest> --refs-file picks.txt [--apply]

WHY A SCRIPT
Done by hand three times now, and the hand version is where the risk lives. Two checks have to
happen every time and are easy to skip when typing it out:

  1. EVERY ROW MUST CARRY THE FULL COMPLEMENT OF TILES. A slot's candidates are globbed
     alphabetically, so the column a tile occupies is a function of how many files exist. A
     short row shifts every column after the gap AND - because wave-contact-sheet.py drops
     partial rows by default - shifts every ROW LETTER below it too. `pdrn-ritual` has a 7-tile
     row for exactly this reason. If any row is short this refuses to run.
  2. A REF THAT DOES NOT RESOLVE IS HELD, NEVER GUESSED. On firming-routine two refs had a
     stray digit and the only reading that worked was a guess; both were held and Malcolm
     confirmed them separately. A guessed pick puts an image he never chose into a gallery.

ROW LABELS ARE THE OLD SCHEME: A..Z then Z26, Z27 ... because that is what the sheets on his
Desktop were built with. A column is always a single digit, so the row is everything before the
last character - "Z266" is row Z26 column 6, "Z1" is row Z column 1. Newer sheets emit AA/AB
instead; those are read here too.

Author: Claude Code, 2026-09-14.
"""
import argparse
import glob
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GEN = ROOT / "assets" / "ai-generated"
SUPPLIERS = ("seedream", "gpt_image", "nbp_pro", "nbp_flash", "luma", "flux2")


def find_wave(arg):
    p = Path(arg)
    if p.is_dir():
        return p
    hits = [h for h in sorted(GEN.glob(f"*{arg}*")) if h.is_dir()]
    if len(hits) != 1:
        sys.exit(f"{'no' if not hits else 'ambiguous'} wave for {arg!r}"
                 + ("".join(f"\n  {h.name}" for h in hits) if hits else ""))
    return hits[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("wave")
    ap.add_argument("dest")
    ap.add_argument("refs", nargs="*")
    ap.add_argument("--refs-file")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--date", default="2026-09-14", help="date stamp for the manifest")
    a = ap.parse_args()

    refs = list(a.refs)
    if a.refs_file:
        refs += [w for w in re.split(r"[\s,]+", Path(a.refs_file).read_text()) if w]
    refs = [r.strip().upper().lstrip("-").strip() for r in refs if r.strip()]
    if not refs:
        sys.exit("no refs given")

    wave = find_wave(a.wave)
    rows = []
    for d in sorted(p for p in wave.iterdir() if p.is_dir() and not p.name.startswith("_")):
        f = sorted(glob.glob(str(d / "*.png")))
        if f:
            rows.append((d.name, f))
    if not rows:
        sys.exit(f"no images in {wave}")

    full = max(len(f) for _, f in rows)
    short = [(n, len(f)) for n, f in rows if len(f) != full]
    print(f"wave    {wave.name}\nrows    {len(rows)}   tiles {sum(len(f) for _, f in rows)}   "
          f"full row = {full}")
    if not (wave / "manifest.json").exists():
        sys.exit("no manifest.json - this wave has not finished generating")
    if short:
        print("\nSHORT ROWS - column positions below these are not trustworthy:")
        for n, c in short:
            print(f"    {n}  ({c}/{full})")
        sys.exit("refusing to resolve against a wave with short rows")

    labels = {}
    for i, v in enumerate(rows):
        labels[chr(ord("A") + i) if i < 26 else f"Z{i}"] = v
        if i >= 26:                       # also accept the newer AA/AB spelling
            labels["A" + chr(ord("A") + (i - 26))] = v

    out, held = [], []
    for ref in refs:
        row, col = ref[:-1], ref[-1]
        if not col.isdigit() or row not in labels:
            held.append((ref, f"no row {row!r}")); continue
        slot, files = labels[row]
        c = int(col)
        if not 1 <= c <= len(files):
            held.append((ref, f"column {c} of {len(files)}")); continue
        src = Path(files[c - 1])
        m = re.search(r"-(" + "|".join(SUPPLIERS) + r")_(\d+)\.png$", src.name)
        sup = f"{m.group(1)}_{m.group(2)}" if m else "?"
        out.append({"ref": ref, "slot": slot, "supplier": sup,
                    "saved_as": f"{ref}-{slot}-{sup}.png", "_src": str(src)})

    print(f"\nresolved {len(out)}/{len(refs)}")
    for o in out:
        print(f'  {o["ref"]:>6}  {o["supplier"]:<14} {o["slot"]}')
    if held:
        print("\nHELD - not resolved, NOT guessed:")
        for r, why in held:
            print(f"  {r:>6}  {why}")

    if not a.apply:
        print("\nDRY RUN - pass --apply to copy")
        return 1 if held else 0

    dest = ROOT / a.dest
    dest.mkdir(parents=True, exist_ok=True)
    for o in out:
        shutil.copy2(o.pop("_src"), dest / o["saved_as"])
    print(f"\ncopied {len(out)} -> {dest.relative_to(ROOT)}")

    # The manifest is the only backup of Malcolm's choices - assets/ is gitignored.
    short = dest.name.rsplit("-2", 1)[0]
    reg = {}
    try:
        import importlib.util
        s = importlib.util.spec_from_file_location("reg", ROOT / "scripts" / "bundle_registry.py")
        m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
        reg = next((dict(b, handle=h) for h, b in m.BUNDLES.items() if b["short"] == short), {})
    except Exception as exc:                                  # registry is a convenience here
        print(f"  (could not read bundle_registry: {exc})")
    man_path = ROOT / "configs" / f"{short}-selection-{a.date}.json"
    man_path.write_text(json.dumps({
        "_comment": (f"Malcolm's selection from the {wave.name} wave, resolved by column "
                     f"position. Safe without a guess: {len(rows)} rows x {full} tiles = "
                     f"{len(rows) * full}, no short rows, manifest.json present, so no column "
                     f"or row letter shifted. Row scheme A-Z then Z26.. "
                     f"{len(out)}/{len(refs)} refs resolved"
                     + (f"; HELD and NOT guessed: {', '.join(r for r, _ in held)}."
                        if held else "; none held, none guessed.")),
        "wave": wave.name.replace("2026-08-22-multi-", ""),
        "bundle_handle": reg.get("handle"), "product_gid": reg.get("gid"),
        "folder": str(dest.relative_to(ROOT)), "selected": out,
    }, indent=2) + "\n")
    print(f"manifest -> {man_path.relative_to(ROOT)}")
    if held:
        print(f"{len(held)} ref(s) still held - ask before assuming any reading")
    return 0


if __name__ == "__main__":
    sys.exit(main())
