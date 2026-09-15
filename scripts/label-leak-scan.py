#!/usr/bin/env python3
"""Count frames where the BRIEF's own words got printed on the product.

    python3 scripts/label-leak-scan.py <wave-dir> [--show]

WHY
On 2026-09-15 a pdrn-ritual frame came back with "PDRN NIGHT CREAM JAR" set in type on the jar.
That string is `PRODUCTS[key]["name"]` from bundle_set_spec - the brief's internal handle, not
artwork. The same family of fault is already logged on this project ("BODY COPY" and "WHITE"
printed as label text). Wiring substance_block in made it likelier, because the handle is now
restated a second time per product, in a sentence beginning "THE SUBSTANCE INSIDE ...".

WHY OCR AND NOT EYES: 376 tiles. Every label check here that relied on reading a contact sheet
has missed something, and a downscaled tile cannot be trusted for lettering at all.

THE MARKERS ARE CHOSEN TO BE UNAMBIGUOUS. No correct Skingenetix label contains the words JAR,
BOTTLE, SUBSTANCE or CONTAINER - they exist only in the brief's handles and scaffolding. A hit
is therefore a leak, not a judgement call.

Author: Claude Code, 2026-09-15.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OCR = ROOT / "scripts" / "bin" / "ocrtext"
MARKERS = ("JAR", "BOTTLE", "SUBSTANCE", "CONTAINER", "SERUM BOTTLE", "CREAM JAR")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("wave")
    ap.add_argument("--show", action="store_true", help="print the OCR text for every leak")
    a = ap.parse_args()

    wave = Path(a.wave)
    if not wave.is_dir():
        hits = sorted(p for p in (ROOT / "assets" / "ai-generated").glob(f"*{a.wave}*") if p.is_dir())
        if len(hits) != 1:
            sys.exit(f"{'no' if not hits else 'ambiguous'} wave for {a.wave!r}")
        wave = hits[0]
    # a WAVE nests tiles in per-slot directories; a SELECTION folder is flat. Accept both, so
    # the same check can be run over Malcolm's picks rather than only over a whole run.
    files = sorted(wave.glob("*/*.png")) or sorted(wave.glob("*.png"))
    if not files:
        sys.exit(f"no images under {wave}")
    print(f"{wave.name}\n{len(files)} tiles, reading labels ...\n")

    leaks, errs = [], 0
    B = 40                                   # batch, so one bad file cannot lose the whole run
    for i in range(0, len(files), B):
        batch = [str(p) for p in files[i:i + B]]
        out = subprocess.run([str(OCR), *batch], capture_output=True, text=True).stdout
        for line in out.splitlines():
            if "\t" not in line:
                continue
            path, text = line.split("\t", 1)
            if text.startswith("ERROR"):
                errs += 1
                continue
            found = [m for m in MARKERS if re.search(rf"\b{m}\b", text)]
            if found:
                leaks.append((Path(path), sorted(set(found)), text))
        print(f"  {min(i + B, len(files)):>4}/{len(files)}", end="\r")

    print(f"\n\nLEAKS: {len(leaks)} of {len(files)} tiles  ({100 * len(leaks) / len(files):.1f}%)"
          f"{f'   [{errs} unreadable]' if errs else ''}\n")
    by_slot, by_engine = {}, {}
    for p, found, _ in leaks:
        by_slot[p.parent.name] = by_slot.get(p.parent.name, 0) + 1
        eng = re.sub(r"_\d+$", "", p.stem.split("-")[-1])
        by_engine[eng] = by_engine.get(eng, 0) + 1
    if leaks:
        print("  by engine:", ", ".join(f"{k} {v}" for k, v in sorted(by_engine.items(), key=lambda x: -x[1])))
        print("  by slot  :")
        for s, n in sorted(by_slot.items(), key=lambda x: -x[1]):
            print(f"     {n:>2}  {s}")
        for p, found, text in leaks if a.show else []:
            print(f"\n  {p.name}\n    {','.join(found)}  ::  {text[:160]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
