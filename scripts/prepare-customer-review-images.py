#!/usr/bin/env python3
"""Prepare Malcolm's customer before/after photographs for the reviews carousel.

    python3 scripts/prepare-customer-review-images.py

SOURCE
`~/Library/CloudStorage/GoogleDrive-.../Skingenetix/Images/Reviews /General`
(note the trailing space on `Reviews ` — the folder really is named that).
Twenty-eight square PNGs named `First-L.png`, each a before/after pair of one person,
split down the middle, with no text baked into the pixels. Fifteen are selected here.

WHY THIS SCRIPT EXISTS RATHER THAN UPLOADING THE PNGs DIRECTLY
Two reasons, both measured on this store before:

1. **Format.** Shopify's CDN inherits losslessness from a lossless source, so a PNG master
   delivers roughly 3.7x the bytes to WebP clients and about 35x to everyone else. Photographs
   are always re-encoded to JPEG. See docs/architecture.md, "web-ready must include the format".
2. **Size.** The section requests at most 1320w. Several sources are 4096px and 10 MB; the long
   edge is capped at 3000, the widest the theme's srcset ever asks for.

The originals in Drive are never touched — these are copies.

CHECKS ALREADY RUN ON THE SET (2026-08-29, before selection)
- All 28 are exactly 1:1, which is the section's contract: one file, both frames, split at 50%.
- No text is burnt into any of them, so the Before/After labels stay translatable DOM text.
- Both halves are the same person in every one, which the images they replace were NOT.
- Content-hash across all four Reviews subfolders found two photographs filed under two
  different customer names: General/Romy-S == Wrinkles/Heather-S, and
  General/Selma-D == Wrinkles/Megan-A. Neither is used here, but if the other folders are ever
  used as well, those two must not both appear or one person becomes two customers.
- Fenna-S, June-K and Brenda-S tripped an automated "halves look too similar" threshold and were
  then looked at full size: all three show a real, visible change. The threshold was wrong, not
  the photographs. Do not re-run that check and act on it without looking.

Author: Claude Code, 2026-08-29.
"""
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = Path.home() / ("Library/CloudStorage/GoogleDrive-msmithnl@gmail.com/My Drive/"
                     "Skingenetix/Images/Reviews /General")
OUT = ROOT / "assets" / "review-before-after" / "customers"

MAX_EDGE = 3000
QUALITY = 95

# Fifteen of the twenty-eight, chosen for a spread of skin tone, age and framing (full face and
# macro), and for a change that is actually visible at card size.
SELECTED = [
    "Maud-H", "Lana-D", "Faye-N", "Linda-P", "Brenda-S",
    "Mila-F", "Jade-C", "Livia-M", "Elara-M", "Noemi-R",
    "Isa-D", "Felicia-P", "Eliza-V", "Elina-B", "June-K",
]


def slug(stem: str) -> str:
    first, _, initial = stem.partition("-")
    return f"{first.lower()}-{initial.lower()}"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    if not SRC.is_dir():
        raise SystemExit(f"source folder not found: {SRC}")

    for stem in SELECTED:
        src = SRC / f"{stem}.png"
        if not src.exists():
            raise SystemExit(f"missing: {src}")
        im = Image.open(src).convert("RGB")
        w, h = im.size
        if max(w, h) > MAX_EDGE:
            s = MAX_EDGE / max(w, h)
            im = im.resize((round(w * s), round(h * s)), Image.LANCZOS)
        dest = OUT / f"skingenetix-before-after-peptide-skincare-{slug(stem)}.jpg"
        # 4:4:4 rather than 4:2:0: chroma subsampling throws away colour detail the CDN's WebP
        # pass would otherwise have kept, and skin tone is the whole subject here.
        im.save(dest, "JPEG", quality=QUALITY, optimize=True, progressive=True,
                subsampling="4:4:4")
        print(f"{stem:<12} {w}x{h} -> {dest.name}  {im.size[0]}x{im.size[1]}  "
              f"{src.stat().st_size // 1024}K -> {dest.stat().st_size // 1024}K")


if __name__ == "__main__":
    main()
