#!/usr/bin/env python3
"""Cut the two library images used on /pages/faq down to the 4:3 the block renders at.

    python3 scripts/make-faq-category-crops.py

Three of the five FAQ category pictures were generated straight to 4:3 (see
configs/banners/faq-category-images.json). The other two came out of the existing
library at 1:1, and this is what turned them into 4:3 masters.

WHY CROP HERE AND NOT LET THE THEME DO IT. The injected <img> carries
`aspect-ratio: 4 / 3; object-fit: cover`, so a square source loses 25% of its height at
every viewport whatever we do. Cropping in the browser means the browser chooses what
goes — a centred cut, on every screen, forever. Cropping here chooses it once, on
purpose, and uploads only the part that will ever be seen.

THE BORDER TRIM IS NOT COSMETIC. NBP Flash baked a ragged near-black film-frame border
into CREAM-2, measured at 51px left, 50 right, 42 top and 42 bottom on a 4096 square by
walking the row and column means until they rose 6 levels above the frame's own value.
Trimmed at 70 for the ragged edge. Left in, it renders as a dark bar down both sides of
the block, because `cover` fills the width and the border goes with it.

assets/ is gitignored, so this file is what makes those two masters reproducible.

Author: Claude Code, 2026-08-25.
"""
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "faq-final"

#: (source, output, border to trim before cropping)
JOBS = [
    ("assets/ai-generated/2026-08-22-multi-cream-application-faces/"
     "CREAM-2-WEST-AFRICAN-LIGHTBLUE/CREAM-2-WEST-AFRICAN-LIGHTBLUE-nbp_flash_01.png",
     "faq-products-usage.png", 70),
    ("assets/ai-generated/ALL-copper-peptide-night-repair-cream/"
     "_run-02__08_open_jar_single_lid_seedream_0.png",
     "faq-ingredients-safety.png", 0),
    # Superseded the line above on 2026-08-25 at Malcolm's request: the block wanted
    # the formulation, not the pack. Gemini delivers 4800x3584, which is 1.339 rather
    # than 1.333 — 22px per side. Nothing would be visible at that margin, but the
    # other four masters are cut to exact 4:3 and one odd member of a set is how a
    # column of pictures starts looking mismatched. See
    # configs/banners/faq-ingredients-cream-macro.json.
    ("assets/ai-generated/2026-08-22-multi-faq-ingredients-cream-macro/"
     "FAQJAR-ingredients/FAQJAR-ingredients-nbp_pro_02.png",
     "faq-ingredients-cream-macro.png", 0),
]


def crop_43(src: Path, dst: Path, trim: int) -> None:
    im = Image.open(src).convert("RGB")
    if trim:
        im = im.crop((trim, trim, im.width - trim, im.height - trim))
    # Cut whichever axis is surplus. The first two sources were square, so only the
    # height ever needed taking; a 4800x3584 Gemini frame is a hair WIDER than 4:3,
    # and taking the height there asks PIL for rows the image does not have — which
    # it answers with black padding rather than an error.
    if im.width * 3 >= im.height * 4:
        width = round(im.height * 4 / 3)
        left = (im.width - width) // 2
        box = (left, 0, left + width, im.height)
    else:
        height = round(im.width * 3 / 4)
        top = (im.height - height) // 2
        box = (0, top, im.width, top + height)
    im.crop(box).save(dst)
    print(f"  {dst.name}  {box[2] - box[0]}x{box[3] - box[1]}")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for source, name, trim in JOBS:
        src = ROOT / source
        if not src.exists():
            raise SystemExit(f"missing source: {source}")
        crop_43(src, OUT / name, trim)


if __name__ == "__main__":
    main()
