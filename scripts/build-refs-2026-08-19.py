#!/usr/bin/env python3
"""Build reference crop sets for the nine 2026 Skingenetix products.

Sources:
  * clean pack shots  — Drive: Images/Products/New designs (product left, carton right)
  * packaging dielines — Drive: Packaging/<product>/*.pdf (flat, both faces)

The crop is anchored on the SUBJECT's bounding box, not on a blind left/right
split. The first version of this script split the frame in half and then squared
the resulting tall strip, which takes the vertical centre and cut the bottom off
every jar label — the `50ML` line and part of the sub-line. A reference that
teaches the model a truncated label is worse than no reference, and the source
pack shots were never the problem.

Backgrounds in the pack shots are a near-white sweep, so the subject is found by
thresholding away the background and taking the bounding box of what remains.

    python3 scripts/build-refs-2026-08-19.py
"""

from __future__ import annotations

import os
import sys

from PIL import Image, ImageChops

SKILL = ("/Users/malcolmsmith/Claude Code/Projects/smith-os/packages/forge/"
         "skills/product-photography/scripts")
sys.path.insert(0, SKILL)
import prep_refs  # noqa: E402

DRIVE = "/Users/malcolmsmith/Library/CloudStorage/GoogleDrive-msmithnl@gmail.com/My Drive/Skingenetix"
SRC = f"{DRIVE}/Images/Products/New designs"
PACK = f"{DRIVE}/Packaging"
OUT = ("/Users/malcolmsmith/Claude Code/Projects/skingenetix-website/"
       "assets/images/_refs-2026-08-19")

P = "PHOTO-2026-07-17-"

#: slug -> (coloured-face pack shot, silver-face pack shot | None, packaging dir)
PRODUCTS = {
    "pdrn-skin-repair-serum":
        (P + "10-46-00.jpg", P + "10-45-59.jpg", "PDRN Serum"),
    "copper-peptide-repair-serum":
        (P + "10-46-40.jpg", P + "10-46-41.jpg", "Copper Peptide Serum"),
    "acetyl-hexapeptide-8-serum":
        (P + "10-50-08.jpg", P + "10-50-09.jpg", "Acetyl Hexapeptide 8 Anti Wrinkle Serum"),
    "matrixyl-3000-pro-collagen-serum":
        ("PHOTO-2026-07-14-09-18-49.jpg", None, "Matrixyl 3000 Pro Collagen Serum"),
    "glutathione-brightening-serum":
        (P + "10-44-15.jpg", P + "10-44-01.jpg", "Glutathione Brightening Serum"),
    "pdrn-collagen-repair-cream":
        (P + "10-49-20.jpg", P + "10-49-21.jpg", "PDRN Collagen Repair Cream"),
    "copper-peptide-day-repair-cream":
        (P + "10-41-58.jpg", P + "10-42-17.jpg", "Copper Peptide Day Cream"),
    "copper-peptide-night-repair-cream":
        (P + "10-42-35.jpg", P + "10-41-31.jpg", "Copper Peptide Night Cream"),
    "matrixyl-3000-pro-collagen-cream":
        (P + "10-43-23.jpg", P + "10-43-24.jpg", "Matrixyl 3000 Pro Collagen Cream"),
}

#: Explicit product/carton divide as a fraction of the subject bbox width, for the
#: shots where automatic detection is unreliable. Serums only - the bottle is
#: narrow and its carton is tall, so they nearly touch.
SPLIT_HINT = {
    "pdrn-skin-repair-serum": 0.42,
    "copper-peptide-repair-serum": 0.42,
    "acetyl-hexapeptide-8-serum": 0.42,
    "matrixyl-3000-pro-collagen-serum": 0.42,
    "glutathione-brightening-serum": 0.42,
}

#: Where a silver face has to come from the dieline instead of a pack shot.
#: The flat artwork carries the silver panel exactly - better than approximating it.
DIELINE_SILVER = {"matrixyl-3000-pro-collagen-serum": (0.51, 0.28, 0.71, 0.62)}

BG_TOLERANCE = 18   # how far from the corner colour still counts as background
MARGIN = 0.06       # breathing room around the subject bbox


def subject_bbox(im: Image.Image) -> tuple[int, int, int, int]:
    """Bounding box of the non-background content."""
    rgb = im.convert("RGB")
    bg = Image.new("RGB", rgb.size, rgb.getpixel((4, 4)))
    diff = ImageChops.difference(rgb, bg).convert("L").point(lambda p: 255 if p > BG_TOLERANCE else 0)
    return diff.getbbox() or (0, 0, *rgb.size)


def square_around(im: Image.Image, box: tuple[int, int, int, int], size: int, dest: str) -> str:
    """Crop exactly `box`, then PAD to square on the background colour.

    Expanding a crop outward to reach square was the real defect behind three
    failed attempts at isolating the serums: a tall narrow bottle yields a square
    as wide as the bottle is tall, which reaches sideways and drags the carton in.
    Short wide jars were unaffected, which is why only the serums looked broken
    and the split logic kept getting blamed.

    Padding keeps the subject whole and admits nothing that was not in `box`.
    Never stretches - the subject keeps its aspect ratio inside the square.
    """
    l, t, r, b = box
    pad_x = int((r - l) * MARGIN)
    pad_y = int((b - t) * MARGIN)
    l, t = max(0, l - pad_x), max(0, t - pad_y)
    r, b = min(im.width, r + pad_x), min(im.height, b + pad_y)

    crop = im.crop((l, t, r, b))
    w, h = crop.size
    edge = max(w, h)
    canvas = Image.new("RGB", (edge, edge), im.getpixel((4, 4)))
    canvas.paste(crop, ((edge - w) // 2, (edge - h) // 2))
    canvas.resize((size, size), Image.LANCZOS).save(dest)
    return dest


def _mask(im: Image.Image) -> Image.Image:
    rgb = im.convert("RGB")
    bg = Image.new("RGB", rgb.size, rgb.getpixel((4, 4)))
    return ImageChops.difference(rgb, bg).convert("L").point(
        lambda p: 255 if p > BG_TOLERANCE else 0)


def split_subjects(path: str, split_hint: float | None = None):
    """Return (image, product_box, carton_box) from a product-left / carton-right shot.

    Splits on the WIDEST RUN OF EMPTY COLUMNS between the two objects, not on the
    midpoint of the combined bounding box. The midpoint lands inside the carton
    whenever the product is narrow — which is every serum — and drags the box into
    the product reference.
    """
    im = Image.open(path).convert("RGB")
    m = _mask(im)
    l, t, r, b = m.getbbox() or (0, 0, im.width, im.height)

    # Column of MINIMUM ink between the two objects. A "widest empty run" test
    # fails on these renders because soft shadows and reflections bridge the gap,
    # so no column is ever truly empty - and a single bad split either blanks the
    # product crop or drags the carton into it.
    px = m.load()
    step = 2
    ink = [sum(1 for y in range(t, b, step) if px[x, y]) for x in range(l, r)]

    width = r - l
    if split_hint is not None:
        # Explicit override. The serum bottle and its tall carton sit close enough
        # that no ink minimum reliably falls between them, and four successive
        # attempts at detecting it either blanked the product crop or dragged the
        # box in. Five numbers, checked by eye, beat a fifth clever heuristic.
        split = l + int(width * split_hint)
    else:
        lo, hi = int(width * 0.25), int(width * 0.75)
        split = l + min(range(lo, hi), key=lambda i: ink[i])

    left = im.crop((l, t, split, b))
    right = im.crop((split, t, r, b))
    lb = subject_bbox(left) if split > l else (0, 0, 1, 1)
    rb = subject_bbox(right) if r > split else (0, 0, 1, 1)
    product = (l + lb[0], t + lb[1], l + lb[2], t + lb[3])
    carton = (split + rb[0], t + rb[1], split + rb[2], t + rb[3])
    return im, product, carton


def main() -> int:
    total = 0
    for slug, (coloured, silver, packdir) in PRODUCTS.items():
        d = os.path.join(OUT, slug)
        os.makedirs(d, exist_ok=True)
        src = os.path.join(SRC, coloured)
        if not os.path.exists(src):
            print(f"  !! missing pack shot {coloured}")
            continue

        hint = SPLIT_HINT.get(slug)
        im, pbox, cbox = split_subjects(src, hint)
        square_around(im, pbox, 1024, os.path.join(d, "product_tight.png"))
        square_around(im, cbox, 1024, os.path.join(d, "box_coloured_face.png"))
        prep_refs.square_crop(src, os.path.join(d, "pack_full.png"), 1024)
        made = 3

        if silver:
            s = os.path.join(SRC, silver)
            if os.path.exists(s):
                im2, _, cbox2 = split_subjects(s, hint)
                square_around(im2, cbox2, 1024, os.path.join(d, "box_silver_face.png"))
                made += 1
        elif slug in DIELINE_SILVER:
            pdfs = [f for f in os.listdir(os.path.join(PACK, packdir)) if f.endswith(".pdf")]
            if pdfs:
                tmp = os.path.join(d, "_dieline.png")
                os.system(f'sips -s format png --resampleWidth 4200 '
                          f'"{os.path.join(PACK, packdir, pdfs[0])}" --out "{tmp}" >/dev/null 2>&1')
                if os.path.exists(tmp):
                    dl = Image.open(tmp).convert("RGB")
                    x0, y0, x1, y1 = DIELINE_SILVER[slug]
                    W, H = dl.size
                    panel = dl.crop((int(W * x0), int(H * y0), int(W * x1), int(H * y1)))
                    pt = os.path.join(d, "_panel.png")
                    panel.save(pt)
                    prep_refs.square_crop(pt, os.path.join(d, "box_silver_face.png"), 1024)
                    os.remove(tmp)
                    os.remove(pt)
                    made += 1
                    print(f"  {slug}: silver face taken from the DIELINE (no pack shot exists)")

        total += made
        print(f"{slug:<36}{made} crops")

    print(f"\n{total} crops across {len(PRODUCTS)} products -> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
