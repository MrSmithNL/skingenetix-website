#!/usr/bin/env python3
"""Put all nine product references in ONE frame at TRUE RELATIVE SCALE.

    python3 scripts/normalise-product-refs.py [--apply] [--sheet]

WHY
Malcolm, 2026-09-14, on the brightening-duo output: the Glutathione bottles held a milky liquid,
the Copper Peptide cream read pale instead of navy, and "the bottle size next to the cream pot
size is important". The colour faults were a dead code path (`substance_block` was never called
- fixed in bundle_set_spec.py). The SIZE fault is here, and it has two halves:

  1. EVERY REFERENCE WAS AT ITS OWN ARBITRARY SCALE. The cream jar fills 84% of its frame width
     while a serum bottle fills about a third of its own, so an engine handed both is being shown
     a huge jar beside a small bottle. Wording cannot beat that; the picture outranks it.
  2. THE BOTTLES DISAGREED WITH EACH OTHER. "some are too tall and too thin" - Malcolm. Acetyl is
     a photograph, not a render, and an earlier height-only fit left it at aspect 0.385 against
     the render's 0.414, which reads as a visibly skinnier bottle.

THE MASTER IS GLUTATHIONE, because Malcolm named Copper and Glutathione as the two correct
renders and rejected Matrixyl's. Its bottle was hand-read off a 50px grid at 2048: x 742..1279,
y 356..1654 - so 537 x 1298, aspect 0.414.

RATIOS ARE MEASURED, NOT DESCRIBED, off the two frames Malcolm named correct (Z441, Z466):
bottle height / jar height 1.76 and 1.89. Jar aspect comes from each jar's own reference,
measured reliably because a dark jar on white is the one detection case that works here.

A RESIDUAL IS ACCEPTED KNOWINGLY. Malcolm also measured jar/bottle WIDTH at 1.77-1.81. With the
true aspects (bottle 0.414, jar ~1.17) the height ratio and the width ratio cannot both hold -
honouring height gives a width ratio near 1.6. Height is anchored because that is what he asked
for and vertical extents are the easier read; his width figures came from rendered frames that
may already carry the fault. Do not "fix" this by stretching a jar.

ACETYL IS STRETCHED 7% HORIZONTALLY to reach 0.414. It is the only product with no isolated
render (its own still carries the superseded ARGIRELINE artwork), so its aspect cannot be
corrected any other way. A 7% stretch on a cylinder is invisible; leaving it is not, which is
how Malcolm spotted it.

ADDITIVE: writes product_tight_norm.png beside each original, never overwriting. Reverts by
deleting nine files. bundle_set_spec.ref_files() prefers _norm when present.

Author: Claude Code, 2026-09-14.
"""
import argparse, json, sys
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
REFS = ROOT / "assets" / "images" / "_refs-2026-08-19"
DRIVE = Path("/Users/malcolmsmith/Library/CloudStorage/GoogleDrive-msmithnl@gmail.com/"
             "My Drive/Skingenetix/Images/Products")
CANVAS, BASELINE = 1024, 827          # every product stands on this line
BOTTLE_H = 649                        # Glutathione's bottle height, scaled 2048 -> 1024
BOTTLE_ASPECT = 537 / 1298            # 0.414, the master
HEIGHT_RATIO = 1.82                   # bottle height / jar height, mean of Z441 and Z466
JAR_H = round(BOTTLE_H / HEIGHT_RATIO)

#: Hand-read off a 50px grid at 2048. The four renders are NOT identical - Glutathione's base
#: sits 84px lower than Matrixyl's - so they cannot share one box.
SERUM_RENDERS = {
    "glutathione-brightening-serum": ("Glutahione Brightening Serum/Glutathione Radient Glow Serum.png",
                                      (742, 356, 1279, 1654)),
    "copper-peptide-repair-serum":   ("Copper Peptide Repair Serum/Copper Peptide Repair Serum.png",
                                      (742, 356, 1279, 1654)),   # same camera as Glutathione
    "matrixyl-3000-pro-collagen-serum": ("Matrixyl 3000 Pro Collagen Serum/Matrixyl Pro Collagen Serum.png",
                                         (740, 326, 1286, 1570)),
    "pdrn-skin-repair-serum":        ("PDRN Skin Repair Serum/PDRN Skin Repair Serum.png",
                                      (740, 326, 1286, 1570)),   # patterns with Matrixyl
}
ACETYL = ("acetyl-hexapeptide-8-serum", (353, 121, 669, 941))
CREAMS = ["copper-peptide-day-repair-cream", "copper-peptide-night-repair-cream",
          "matrixyl-3000-pro-collagen-cream", "pdrn-collagen-repair-cream"]


def flatten(p):
    im = Image.open(p)
    if im.mode in ("RGBA", "LA"):
        im = Image.alpha_composite(Image.new("RGBA", im.size, (255, 255, 255, 255)),
                                   im.convert("RGBA"))
    return im.convert("RGB")


def jar_box(im, tol=60):
    """A dark jar on white is the ONE detection case that is reliable here."""
    a = np.asarray(im).astype(int)
    bg = np.median(np.concatenate([a[:8].reshape(-1, 3), a[-8:].reshape(-1, 3)]), axis=0)
    ys, xs = np.where(np.abs(a - bg).sum(2) > tol)
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


def place(src, box, target_h, ground, force_aspect=None):
    x0, y0, x1, y1 = box
    sub = src.crop(box)
    h = target_h
    w = round(h * (force_aspect if force_aspect else (x1 - x0) / (y1 - y0)))
    sub = sub.resize((w, h), Image.LANCZOS)
    out = Image.new("RGB", (CANVAS, CANVAS), ground)
    out.paste(sub, (CANVAS // 2 - w // 2, BASELINE - h))
    return out, w


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    rows = []

    for slug, (rel, box) in SERUM_RENDERS.items():
        src = DRIVE / rel
        if not src.exists():
            print(f"  SKIP {slug}: {src} missing"); continue
        im = flatten(src)
        out, w = place(im, box, BOTTLE_H, im.getpixel((4, 4)))
        rows.append((slug, out, f"bottle {w}x{BOTTLE_H}  aspect {w/BOTTLE_H:.3f}"))

    slug, box = ACETYL
    im = flatten(REFS / slug / "product_tight.png")
    out, w = place(im, box, BOTTLE_H, im.getpixel((4, 4)), force_aspect=BOTTLE_ASPECT)
    nat = (box[2] - box[0]) / (box[3] - box[1])
    rows.append((slug, out, f"bottle {w}x{BOTTLE_H}  aspect {w/BOTTLE_H:.3f}  "
                            f"(stretched from {nat:.3f}, +{100*(BOTTLE_ASPECT/nat-1):.0f}%)"))

    for slug in CREAMS:
        im = flatten(REFS / slug / "product_tight.png")
        box = jar_box(im)
        out, w = place(im, box, JAR_H, im.getpixel((4, 4)))
        rows.append((slug, out, f"jar    {w}x{JAR_H}  aspect {w/JAR_H:.3f}"))

    print(f"shared frame: canvas {CANVAS}, baseline y={BASELINE}, "
          f"bottle h={BOTTLE_H}, jar h={JAR_H} (ratio {HEIGHT_RATIO})\n")
    for slug, out, note in rows:
        print(f"  {'wrote' if a.apply else 'would write'}  {slug:<36} {note}")
        if a.apply:
            out.save(REFS / slug / "product_tight_norm.png")
    if not a.apply:
        print("\nDRY RUN - pass --apply to write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
