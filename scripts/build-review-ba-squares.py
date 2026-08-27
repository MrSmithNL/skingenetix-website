#!/usr/bin/env python3
"""Compose 1:1 before/after masters for the reviews carousel from the existing files.

    python3 scripts/build-review-ba-squares.py

WHY THIS EXISTS
The four before/after images live on /pages/reviews are 1200x600 diptychs with the words
BEFORE and AFTER **burnt into the pixels** — a dark teal bar and a green bar across the top
40px. Baked text cannot be translated, and nine locales are planned, so the labels have to
become DOM text (see docs/research-before-after-section.md section 3). This strips the bars.

Malcolm's brief for the carousel (2026-08-27) is that the pair reads as a SQUARE, so each
half is a taller-than-wide rectangle. The sources are two squares side by side, so each
half is centre-cropped from 600x560 to 280x560 and rejoined into 560x560.

`skingenetix-ba-firmness-combined.jpg` is deliberately NOT processed: the BEFORE half has
the image brief rendered into the photograph ("image-container", "body: display: flex...",
"alt 'Close of skin with sagging'") and the AFTER half is two different faces. It needs
regenerating, not cropping.

The output is a placeholder standing in until matched pairs are generated. Resolution is
capped by the sources at 560px square; that is soft on a 2x display and is one of the
reasons to regenerate rather than keep these.

Author: Claude Code, 2026-08-27.
"""
import io
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "review-before-after"
CDN = "https://www.skingenetix.com/cdn/shop/files/"

BAND_H = 40  # measured: rows 0-39 are the solid label bar on every source

SOURCES = {
    "fine-lines-acetyl-hexapeptide-8": "skingenetix-ba-finelines-combined.jpg",
    "skin-texture-matrixyl-3000": "skingenetix-ba-texture-combined.jpg",
    "radiance-peptide-routine": "skingenetix-ba-radiance-combined.jpg",
}


def square_diptych(im: Image.Image) -> Image.Image:
    """Strip the burnt-in label band, then centre-crop each half to 1:2 and rejoin 1:1."""
    w, h = im.size
    im = im.crop((0, BAND_H, w, h))
    w, h = im.size
    half_w = w // 2
    target_w = h // 2  # each half is half as wide as it is tall -> pair is square
    if target_w > half_w:
        raise SystemExit(f"source half {half_w}x{h} is too narrow for a 1:2 crop")

    out = Image.new("RGB", (target_w * 2, h))
    for i in range(2):
        piece = im.crop((i * half_w, 0, (i + 1) * half_w, h))
        left = (half_w - target_w) // 2
        out.paste(piece.crop((left, 0, left + target_w, h)), (i * target_w, 0))
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for slug, filename in SOURCES.items():
        url = f"{CDN}{filename}"
        raw = urllib.request.urlopen(url, timeout=60).read()
        im = Image.open(io.BytesIO(raw)).convert("RGB")
        sq = square_diptych(im)
        dest = OUT / f"skingenetix-review-before-after-{slug}.jpg"
        sq.save(dest, quality=90, optimize=True, progressive=True)
        print(f"{filename} {im.size} -> {dest.name} {sq.size}  {dest.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
