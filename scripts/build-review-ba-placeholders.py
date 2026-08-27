#!/usr/bin/env python3
"""Draw brand placeholder diptychs for the review slots that have no photograph yet.

    python3 scripts/build-review-ba-placeholders.py

WHY GRAPHIC AND NOT A PHOTOGRAPH
The obvious placeholder is to repeat one of the three real before/after pairs across the twelve
empty slots. That was rejected: a before/after photograph on a review card reads as a *result*,
and putting the same result on five cards on a live store is a claim nobody has measured. These
are unmistakably graphic — no skin, no face, no photograph — so they read as "artwork pending"
rather than as evidence.

NO TEXT IS DRAWN INTO THEM
Not one pixel of type. Baked words cannot be translated, and nine locales are planned; every
label in this section is a `text` setting for that reason. See docs/reviews-before-after-carousel.md.

THE GEOMETRY MATCHES THE REAL MASTERS
1200x1200, split at exactly 50%, so each half is a portrait rectangle — the same contract the
photographs must meet, and the same one the section's label positions assume.

Colours are the homepage system's concern -> ingredient map: pearl grey for Acetyl Hexapeptide-8,
teal for Matrixyl 3000, clinical blue for Copper Peptide, champagne for Glutathione, blush for
PDRN, copper for the microneedling sets. The left half is the same hue held back and cooled; the
right half is the hue clean and lit. The peptide chain is the brand's signature device.

Author: Claude Code, 2026-08-27.
"""
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "review-before-after"

SIZE = 1200
HALF = SIZE // 2

BONE = (240, 240, 240)
GRAPHITE = (26, 26, 26)

# family -> the concern colour it owns in the homepage visual system
FAMILIES = {
    "copper-peptide": (0x01, 0x4E, 0xB1),   # clinical blue
    "matrixyl-3000": (0x01, 0x65, 0x69),    # teal
    "glutathione": (0xDF, 0xC0, 0x8F),      # champagne
    "pdrn": (0xF3, 0xBF, 0xC2),             # blush
    "acetyl-hexapeptide-8": (0xD8, 0xD6, 0xD4),  # pearl grey
    "microneedling": (0xB8, 0x73, 0x33),    # copper
}

# one file per empty slot, so twelve identical tiles never sit in one carousel
SLOTS = [
    ("rv-04", "copper-peptide"),
    ("rv-05", "pdrn"),
    ("rv-06", "glutathione"),
    ("rv-07", "copper-peptide"),
    ("rv-08", "copper-peptide"),
    ("rv-09", "matrixyl-3000"),
    ("rv-10", "pdrn"),
    ("rv-11", "microneedling"),
    ("rv-12", "microneedling"),
    ("rv-13", "copper-peptide"),
    ("rv-14", "pdrn"),
    ("rv-15", "glutathione"),
]


def mix(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def gradient(w, h, top, bottom):
    g = Image.new("RGB", (1, h))
    px = g.load()
    for y in range(h):
        px[0, y] = mix(top, bottom, y / max(h - 1, 1))
    return g.resize((w, h), Image.BILINEAR)


def chain(draw, rng, x0, x1, colour, alpha, nodes=5, r=14):
    """The brand's peptide chain: beads on a gently waving line."""
    span = x1 - x0
    pts = []
    for i in range(nodes):
        x = x0 + span * (i + 0.5) / nodes
        y = SIZE * 0.5 + math.sin(i * 1.1 + rng.random() * 2.4) * SIZE * 0.11
        pts.append((x, y))
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        draw.line([ax, ay, bx, by], fill=colour + (alpha,), width=3)
    for i, (x, y) in enumerate(pts):
        rr = r if i % 2 == 0 else r * 0.62
        draw.ellipse([x - rr, y - rr, x + rr, y + rr], fill=colour + (alpha,))


def tile(family, seed):
    hue = FAMILIES[family]
    rng = random.Random(seed)

    # BEFORE half: the hue held back and cooled toward graphite.
    left_top = mix(mix(hue, GRAPHITE, 0.55), BONE, 0.28)
    left_bottom = mix(mix(hue, GRAPHITE, 0.68), BONE, 0.16)
    # AFTER half: the same hue, clean and lit.
    right_top = mix(hue, BONE, 0.42)
    right_bottom = mix(hue, BONE, 0.16)

    im = Image.new("RGB", (SIZE, SIZE))
    im.paste(gradient(HALF, SIZE, left_top, left_bottom), (0, 0))
    im.paste(gradient(HALF, SIZE, right_top, right_bottom), (HALF, 0))

    overlay = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    chain(d, rng, SIZE * 0.06, HALF - SIZE * 0.06, BONE, 40)
    chain(d, rng, HALF + SIZE * 0.06, SIZE - SIZE * 0.06, BONE, 96)
    overlay = overlay.filter(ImageFilter.GaussianBlur(0.6))
    im = Image.alpha_composite(im.convert("RGBA"), overlay).convert("RGB")
    return im


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for i, (slot, family) in enumerate(SLOTS):
        im = tile(family, seed=i * 97 + 11)
        dest = OUT / f"skingenetix-review-before-after-placeholder-{slot}-{family}.jpg"
        im.save(dest, quality=90, optimize=True, progressive=True)
        print(f"{dest.name}  {im.size}  {dest.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
