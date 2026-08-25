#!/usr/bin/env python3
"""Regenerate the five TEMPORARY placeholder images for /pages/faq.

    python3 scripts/make-faq-placeholders.py

These exist only so Malcolm could judge the picture-left / accordions-right layout
before choosing real photography (2026-08-25). Every file is named `-placeholder-`
AND carries the word PLACEHOLDER rendered into the picture, so none can quietly
become permanent. Delete them once real images land — the removal recipe is in
`configs/banners/page-faq-placeholders.json`.

`assets/` is gitignored, so the JPEGs themselves are not in the repo; this script is,
which is what makes them reproducible.

Author: Claude Code, 2026-08-25.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "placeholders"

#: slug, label, and a base tone per category — deliberately near-neutral, so the
#: layout is judgeable without the colour reading as a design decision.
CATEGORIES = [
    ("products-usage", "Products & Usage", (214, 218, 222)),
    ("ingredients-safety", "Ingredients & Safety", (216, 214, 208)),
    ("orders-shipping", "Orders & Shipping", (210, 216, 220)),
    ("returns-refunds", "Returns & Refunds", (218, 214, 214)),
    ("skincare-routine", "Skincare & Routine", (212, 216, 212)),
]

W, H = 1600, 1200
BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
REGULAR = "/System/Library/Fonts/Supplemental/Arial.ttf"


def build(slug: str, label: str, base: tuple[int, int, int]) -> Path:
    im = Image.new("RGB", (W, H), base)
    d = ImageDraw.Draw(im)
    # A soft vertical lift plus diagonals: flat grey makes it impossible to tell
    # whether the bottom scrim is working, and the scrim is the part being judged.
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(c * (1 - 0.10 * t) + 255 * 0.10 * t) for c in base))
    for k in range(9):
        x = int(W * (0.08 + 0.1 * k))
        d.line([(x, -50), (x - 260, H + 50)], fill=tuple(max(0, c - 8) for c in base), width=2)
    im = im.filter(ImageFilter.GaussianBlur(0.6))

    d = ImageDraw.Draw(im)
    title, sub = "PLACEHOLDER", label
    fb, fs = ImageFont.truetype(BOLD, 44), ImageFont.truetype(REGULAR, 30)
    d.text(((W - d.textlength(title, font=fb)) / 2, H / 2 - 56), title, fill=(120, 124, 128), font=fb)
    d.text(((W - d.textlength(sub, font=fs)) / 2, H / 2 + 10), sub, fill=(140, 144, 148), font=fs)
    d.rectangle([40, 40, W - 40, H - 40], outline=(170, 174, 178), width=3)

    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"skingenetix-faq-placeholder-{slug}.jpg"
    im.save(path, "JPEG", quality=92)
    return path


if __name__ == "__main__":
    for slug, label, base in CATEGORIES:
        print(f"  {build(slug, label, base).relative_to(ROOT)}")
