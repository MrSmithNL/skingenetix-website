#!/usr/bin/env python3
"""Check that each product's label lines are PRESENT, rather than hunting for known-bad words.

    python3 scripts/verify-labels.py <folder-or-wave> --expect "LINE ONE" --expect "LINE TWO"

WHY THIS REPLACES THE DENYLIST
label-leak-scan.py looks for words that must never appear - JAR, BOTTLE, PORN, COPPEP. That
caught the handle leak on U6, and then MISSED V5 completely, because V5's corruptions were
spellings nobody had seen before: "PK (10,000 PPM) PDFIN | 30ML" on the serum and "FORN |
COLLAGEN | COTRER PEPTIDE | 50ML" on the jar. A denylist can only ever catch the corruptions
already met. Both frames were picked by Malcolm and both were one step from a live page.

An allowlist has no such hole. The correct lines are known - they are quoted verbatim in each
product config - so the test is whether they are THERE, and anything else is a fail by default.
Run over the same two rows it scored U6 at 79% and V5 at 42% while passing U1-U4 at 100%.

IT IS A SCREEN, NOT A VERDICT. OCR makes its own mistakes, which is why the output is a
similarity score rather than a yes or no: soft or distant lettering scores lower without being
wrong. Anything under 95% is worth opening at native pixels - that check, not this one, is what
distinguished the real PORN on U6 from the OCR artifact on an adjacent frame.

Author: Claude Code, 2026-09-15.
"""
import argparse
import difflib
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OCR = ROOT / "scripts" / "bin" / "ocrtext"
_norm = lambda s: re.sub(r"[^A-Z0-9%|]", "", s.upper())
SUP = re.compile(r"-([a-z0-9]+(?:_[a-z0-9]+)*_\d+)\.png$")


def best_match(expected, text):
    """Best local similarity of `expected` anywhere in `text`, both normalised."""
    e, t = _norm(expected), _norm(text)
    if not e or not t:
        return 0.0
    return max((difflib.SequenceMatcher(None, e, t[i:i + len(e)]).ratio()
                for i in range(max(1, len(t) - len(e) + 1))), default=0.0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("--expect", action="append", required=True,
                    help="a label line that MUST appear; repeat for each one")
    ap.add_argument("--pass-mark", type=float, default=0.95)
    ap.add_argument("--only-suspect", action="store_true")
    a = ap.parse_args()

    t = Path(a.target)
    files = sorted(t.glob("*/*.png")) or sorted(t.glob("*.png"))
    if not files:
        sys.exit(f"no images under {t}")

    print(f"{len(files)} images, {len(a.expect)} required line(s), pass mark "
          f"{a.pass_mark * 100:.0f}%\n")
    worst = []
    B = 40
    for i in range(0, len(files), B):
        out = subprocess.run([str(OCR), *[str(f) for f in files[i:i + B]]],
                             capture_output=True, text=True).stdout
        for line in out.splitlines():
            if "\t" not in line:
                continue
            path, text = line.split("\t", 1)
            if text.startswith("ERROR"):
                print(f"  ??  {Path(path).name}  unreadable"); continue
            scores = [best_match(e, text) for e in a.expect]
            ok = min(scores) >= a.pass_mark
            if ok and a.only_suspect:
                continue
            m = SUP.search(Path(path).name)
            cols = "  ".join(f"{s * 100:4.0f}%" for s in scores)
            print(f"  {'ok ' if ok else 'SUSPECT'}  {cols}  {m.group(1) if m else '':<14}"
                  f"{Path(path).name[:56]}")
            if not ok:
                worst.append(Path(path).name)
    print(f"\n  {len(files) - len(worst)}/{len(files)} pass. "
          f"Open every SUSPECT at native pixels before publishing it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
