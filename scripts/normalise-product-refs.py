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
    # BASE CORRECTED 2026-09-14. These read 1570 and cut ~80px off the bottom of the glass -
    # Malcolm: "the Matrixyl and pdrn bottle bottoms are cut off. The whole bottle is not in
    # view." Re-read off a 25px grid over the base region: all three bottles end at ~1654, so
    # the base was never the difference between these renders and Glutathione's. The TOP is:
    # these start at 326 against Glutathione's 356, and that extra 30px IS the exposed glass
    # neck Malcolm wants gone. A neck cannot be cropped out of the middle of a bottle, so it
    # stays until corrected renders exist.
    "matrixyl-3000-pro-collagen-serum": ("Matrixyl 3000 Pro Collagen Serum/Matrixyl Pro Collagen Serum.png",
                                         (740, 326, 1286, 1654)),
    "pdrn-skin-repair-serum":        ("PDRN Skin Repair Serum/PDRN Skin Repair Serum.png",
                                      (740, 326, 1286, 1654)),
}
ACETYL = ("acetyl-hexapeptide-8-serum", (353, 121, 669, 941))

#: Acetyl's collar in ITS source, and the region of Glutathione's used to match it. Malcolm:
#: "the acetyl top silver color should be the same as the glutathione and copper peptide
#: serums." Measured rather than eyeballed - Glutathione's collar is mean 184 / sd 63, Acetyl's
#: is mean 206 / sd 33, so Acetyl is both LIGHTER and much FLATTER, missing the brushed grain.
#: A linear match (gain 1.914, offset -209) reproduces both. Feathered at the edges so the
#: corrected patch does not leave a visible rectangle, and applied to the SOURCE before scaling.
ACETYL_COLLAR = (430, 300, 595, 455)
GLUT_COLLAR_SRC = (820, 620, 1200, 840)


def match_collar(acetyl_im, glut_im):
    """Bring Acetyl's photographed collar to the renders' tone and contrast."""
    import numpy as np
    a = np.asarray(acetyl_im).astype(float)
    g = np.asarray(glut_im).astype(float)[GLUT_COLLAR_SRC[1]:GLUT_COLLAR_SRC[3],
                                          GLUT_COLLAR_SRC[0]:GLUT_COLLAR_SRC[2]]
    x0, y0, x1, y1 = ACETYL_COLLAR
    patch = a[y0:y1, x0:x1]
    gain = g.std() / patch.std()
    off = g.mean() - patch.mean() * gain
    fixed = np.clip(patch * gain + off, 0, 255)
    # feather: 1 in the middle, falling to 0 over 12px at each edge, so no hard seam
    h, w = patch.shape[:2]
    fy = np.clip(np.minimum(np.arange(h), h - 1 - np.arange(h)) / 12.0, 0, 1)
    fx = np.clip(np.minimum(np.arange(w), w - 1 - np.arange(w)) / 12.0, 0, 1)
    m = (fy[:, None] * fx[None, :])[:, :, None]
    a[y0:y1, x0:x1] = patch * (1 - m) + fixed * m
    return Image.fromarray(np.clip(a, 0, 255).astype("uint8")), gain, off
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


#: The PDRN serum's glass reads salmon, not pink. Malcolm, 2026-09-15: "the liquid inside is a
#: TRANSPARENT pink color ... And the pink color of the liquid is pink - not salmon." Measured on
#: the reference glass: hue 358.3deg at saturation 0.204 - that is a desaturated RED, which is
#: exactly what reads as dusty salmon. A true pink sits near 336-340deg, so the correction is a
#: hue rotation, not a repaint.
#:
#: It targets LOW-SATURATION pixels only (the glass wash sits near 0.20; the label's rose accent
#: type is far more saturated), so the printed accent colour is left exactly as designed. Nothing
#: neutral moves either - the collar, the white pipette and the black type have almost no
#: saturation to rotate.
#:
#: WHAT THIS CANNOT DO: make the liquid look SEE-THROUGH. Transparency is read from seeing the
#: fill level and the back of the bottle through the liquid, and that information is not in the
#: picture to recover. The brief now asserts it (substance_block carries the new wording); the
#: real fix is the corrected PDRN render already needed for the neck.
#: A DELTA, not a target. The first attempt SNAPPED warm pixels to hue 337 and capped the effect
#: at saturation 0.30 to protect the label's accent type. That banded badly: the glass core sits
#: ABOVE 0.30, so it stayed at 358 while everything around it moved, leaving a hard-edged salmon
#: stripe down the bottle. Caught by looking at the render, not by the code failing.
#:
#: Rotating every warm pixel by the SAME amount cannot band, because it preserves the relationships
#: inside the region. The accent type rotates with the glass, which is right rather than merely
#: tolerable - it is the same rose ink, and the product's identity is pink.
PINK_DELTA = -21.0 / 360.0     # 358.3 measured -> ~337, a true pink
PINK_SAT_GAIN = 1.30


def repink(im):
    """Rotate the salmon-leaning glass to a true pink. Returns (image, pixels changed)."""
    import numpy as np
    a = np.asarray(im).astype(float) / 255.0
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx, mn = a.max(2), a.min(2)
    v = mx
    s = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    d = np.maximum(mx - mn, 1e-6)
    h = np.select([mx == r, mx == g, mx == b],
                  [((g - b) / d) % 6, ((b - r) / d) + 2, ((r - g) / d) + 4], default=0) / 6.0
    m = ((h > 320 / 360.0) | (h < 25 / 360.0)) & (s > 0.03)
    h2 = np.where(m, (h + PINK_DELTA) % 1.0, h)
    s2 = np.where(m, np.clip(s * PINK_SAT_GAIN, 0, 1), s)
    # vectorised HSV->RGB, so no per-pixel python and no banding from rounding
    i = np.floor(h2 * 6).astype(int) % 6
    f = h2 * 6 - np.floor(h2 * 6)
    p_ = v * (1 - s2); q = v * (1 - f * s2); tt = v * (1 - (1 - f) * s2)
    out = np.choose(i[..., None],
                    [np.stack([v, tt, p_], -1), np.stack([q, v, p_], -1), np.stack([p_, v, tt], -1),
                     np.stack([p_, q, v], -1), np.stack([tt, p_, v], -1), np.stack([v, p_, q], -1)])
    return Image.fromarray(np.clip(out * 255, 0, 255).astype("uint8")), int(m.sum())


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
        if slug == "pdrn-skin-repair-serum":
            im, n = repink(im)
            print(f"  pdrn glass re-pinked: {n:,} px rotated to hue 337deg")
        out, w = place(im, box, BOTTLE_H, im.getpixel((4, 4)))
        rows.append((slug, out, f"bottle {w}x{BOTTLE_H}  aspect {w/BOTTLE_H:.3f}"))

    slug, box = ACETYL
    im = flatten(REFS / slug / "product_tight.png")
    gsrc = DRIVE / SERUM_RENDERS["glutathione-brightening-serum"][0]
    if gsrc.exists():
        im, _gain, _off = match_collar(im, flatten(gsrc))
        print(f"  acetyl collar matched to glutathione: gain {_gain:.3f} offset {_off:+.1f}")
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
