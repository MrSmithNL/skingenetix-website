#!/usr/bin/env python3
"""Rebuild the five serum references on ONE shared frame, whole bottle in view.

    python3 scripts/normalise-serum-ref.py [--apply]

WHY
On 2026-09-14 Malcolm rejected all eight white-background compositions of the wrinkles-routine
bundle: the two serum bottles came back different heights, different collars, some with milky
white contents. The brief was not the weak part - `bundle_set_spec.py` already carries a
substance block, a per-colour-cluster separation clause and explicit negatives for "a colourless
liquid rendered as milky white". The REFERENCES were the weak part, and a picture outranks text.

WHAT WAS WRONG WITH THEM
`build-refs-2026-08-19.py` cropped each product independently. Malcolm, reading the boxes drawn
back onto the refs: "the red box only shows the Acetyl bottle fully in view. The Copper Peptide
almost - but missing the top of the pipette. The other 3 cut off a lot of the bottle." Three of
five references were teaching the engines a truncated bottle. The build script's own docstring
warned about exactly this: "A reference that teaches the model a truncated label is worse than
no reference."

The Drive source renders are clean - full bottle, full pipette, base and reflection, and all
four share one camera. The damage was introduced by the crop, not present in the source. So the
four renders are used AS THEY COME, merely resized to 1024. No cropping at all.

ACETYL IS THE ODD ONE OUT and cannot be fully fixed here. It has no isolated render on Drive -
`build-refs-2026-08-19.py` records why: its render still carried the superseded ARGIRELINE
artwork - so it is a photograph, not a render. It is scaled to match the Matrixyl bottle's
HEIGHT, because height is what the eye compares when bottles stand side by side. Its width then
lands ~12% narrow, as the photograph's focal length differs from the renders'. Matching width
instead would mismatch height, and stretching to match both would distort the label. Accepted
knowingly; closing it properly needs a current Acetyl render in the same 3D style.

NUMBERS ARE HAND-MEASURED AND EXPLICIT, NEVER DETECTED AT RUN TIME. Automatic boundary detection
was tried three times here on 2026-09-14 and failed three times - it returned the full canvas,
found a background band instead of a silhouette, and swallowed the reflection. That matches this
project's logged history of seven attempts and five identical failures on white-on-white. The
Matrixyl box below was read off a 50px grid at 2048 and halved. Measure, do not detect.

ADDITIVE. Writes `product_tight_norm.png` beside each original and never overwrites one, so
every other consumer of these references is unaffected and this reverts by deleting five files.

Author: Claude Code, 2026-09-14.
"""
import argparse
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
REFS = ROOT / "assets" / "images" / "_refs-2026-08-19"
DRIVE = Path("/Users/malcolmsmith/Library/CloudStorage/GoogleDrive-msmithnl@gmail.com/"
             "My Drive/Skingenetix/Images/Products")
CANVAS = 1024

#: slug -> Drive render. These four share one camera and need no crop.
RENDERS = {
    "matrixyl-3000-pro-collagen-serum":
        "Matrixyl 3000 Pro Collagen Serum/Matrixyl Pro Collagen Serum.png",
    "pdrn-skin-repair-serum": "PDRN Skin Repair Serum/PDRN Skin Repair Serum.png",
    "glutathione-brightening-serum": "Glutahione Brightening Serum/Glutathione Radient Glow Serum.png",
    "copper-peptide-repair-serum": "Copper Peptide Repair Serum/Copper Peptide Repair Serum.png",
}

#: The Matrixyl bottle in the 1024 frame: pipette tip to base. Hand-read off a 50px grid.
TARGET = dict(x0=370, y0=163, x1=643, y1=785)

#: The Acetyl bottle in its existing 1024 reference. Verified by drawing it back on and looking.
ACETYL = ("acetyl-hexapeptide-8-serum", (353, 121, 669, 941))


def flatten(path):
    im = Image.open(path)
    if im.mode in ("RGBA", "LA"):
        im = Image.alpha_composite(Image.new("RGBA", im.size, (255, 255, 255, 255)),
                                   im.convert("RGBA"))
    return im.convert("RGB")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    wrote = []

    for slug, rel in RENDERS.items():
        src = DRIVE / rel
        if not src.exists():
            print(f"  SKIP {slug}: Drive source missing ({src})")
            continue
        out = flatten(src).resize((CANVAS, CANVAS), Image.LANCZOS)
        wrote.append((REFS / slug / "product_tight_norm.png", out, "Drive render, uncropped"))

    slug, box = ACETYL
    src = flatten(REFS / slug / "product_tight.png")
    bx0, by0, bx1, by1 = box
    bw, bh = bx1 - bx0, by1 - by0
    th = TARGET["y1"] - TARGET["y0"]
    scale = th / bh
    nw = round(bw * scale)
    canvas = Image.new("RGB", (CANVAS, CANVAS), src.getpixel((4, 4)))
    canvas.paste(src.crop(box).resize((nw, th), Image.LANCZOS),
                 ((TARGET["x0"] + TARGET["x1"]) // 2 - nw // 2, TARGET["y0"]))
    tw = TARGET["x1"] - TARGET["x0"]
    wrote.append((REFS / slug / "product_tight_norm.png", canvas,
                  f"photo, height-matched (scale {scale:.4f}); width {nw} vs {tw} "
                  f"= {100 * (nw - tw) / tw:+.0f}%"))

    for path, im, note in wrote:
        print(f"  {'wrote' if a.apply else 'would write'}  {path.relative_to(ROOT)}   {note}")
        if a.apply:
            im.save(path)
    if not a.apply:
        print("\nDRY RUN - pass --apply to write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
