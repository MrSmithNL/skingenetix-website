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
PRODUCTS_DIR = f"{DRIVE}/Images/Products"
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

#: Product/carton divide as a fraction of FRAME width, per pack shot.
#:
#: Explicit, not detected. Six detection attempts failed for a reason worth
#: recording: in most of these shots the product and its carton TOUCH, so there
#: is no gap to find, and the silver/white cartons sit at nearly the same value
#: as the white sweep so thresholding eats them. Automatic segmentation cannot
#: solve white-on-white with no separation. Seventeen numbers, checked by eye,
#: can - and they never regress.
#:
#: Values are usually a single cut. A (product_cut, carton_cut) pair is supported
#: for shots where the two objects genuinely overlap horizontally, though none
#: currently need it - the Copper Peptide Serum looked like it did until the
#: divide was measured properly at 48.8% (coloured) and 47.6% (silver). Guessing
#: it at 0.45 left a bottle sliver in the carton; guessing 0.50 sliced 4% off the
#: carton's left edge. Measure, do not estimate.
#:
#: Keys are the pack-shot filenames. `_DEFAULT` covers anything unlisted.
BOUNDARY_DEFAULT = 0.47
BOUNDARY = {
    P + "10-46-00.jpg": 0.44,   # pdrn serum, coloured
    P + "10-45-59.jpg": 0.46,   # pdrn serum, silver
    P + "10-46-40.jpg": 0.487,  # copper peptide serum, coloured - measured divide
    P + "10-46-41.jpg": 0.476,  # copper peptide serum, silver - measured divide
    P + "10-50-08.jpg": 0.45,   # acetyl, coloured
    P + "10-50-09.jpg": 0.45,   # acetyl, silver
    "PHOTO-2026-07-14-09-18-49.jpg": 0.47,  # matrixyl serum, coloured
    P + "10-44-15.jpg": 0.41,   # glutathione, coloured
    P + "10-44-01.jpg": 0.45,   # glutathione, silver
    P + "10-49-20.jpg": 0.47,   # pdrn cream, coloured
    P + "10-49-21.jpg": 0.47,   # pdrn cream, silver
    P + "10-41-58.jpg": 0.47,   # copper day, coloured
    P + "10-42-17.jpg": 0.47,   # copper day, silver
    P + "10-42-35.jpg": 0.47,   # copper night, coloured
    P + "10-41-31.jpg": 0.47,   # copper night, silver
    P + "10-43-23.jpg": 0.48,   # matrixyl cream, coloured
    P + "10-43-24.jpg": 0.48,   # matrixyl cream, silver
}

#: Dedicated single-product renders, one per product, 2048px on a clean sweep.
#:
#: These beat cropping the product out of a pack shot on every count: the product
#: is already isolated, there is no carton to split away from, and they carry the
#: CURRENT artwork - the Glutathione render here reads PREMIUM FORMULA and 30ML
#: where the pack shot still shows PROFESSIONAL TREATMENT and its carton shows
#: 50ML. Use them for `product_tight`; the pack shots still supply the carton
#: faces and the size relationship.
#:
#: Note the trailing spaces in two folder names - they are real, do not "tidy" them.
PRODUCT_RENDER = {
    # NOT acetyl-hexapeptide-8: the render in "Argireline Age Control Serum " is the
    # SUPERSEDED design, reading "ARGIRELINE / ADVANCED AGE CONTROL". Its own carton
    # says ACETYL HEXAPEPTIDE-8 / ANTI-WRINKLE SERUM. That product falls back to the
    # pack-shot crop until a current render exists.
    "copper-peptide-repair-serum":
        "Copper Peptide Repair Serum/Copper Peptide Repair Serum.png",
    "glutathione-brightening-serum":
        "Glutahione Brightening Serum/Glutathione Radient Glow Serum.png",
    "matrixyl-3000-pro-collagen-serum":
        "Matrixyl 3000 Pro Collagen Serum/Matrixyl Pro Collagen Serum.png",
    "pdrn-skin-repair-serum":
        "PDRN Skin Repair Serum/PDRN Skin Repair Serum.png",
    "copper-peptide-day-repair-cream":
        "Copper Peptide Day Repair Cream/Copper Peptide Day Cream.png",
    "copper-peptide-night-repair-cream":
        "Copper Peptide Night Repair Cream/Copper Peptide Night Cream.png",
    "matrixyl-3000-pro-collagen-cream":
        "Matrixyl 3000 Pro Collagen Cream /Matrixyl Pro Collagen Cream.png",
    "pdrn-collagen-repair-cream":
        "PDRN Collagen Repair Cream/PDRN Collagen Repair Cream.png",
}

#: Silver faces that come from a GENERATED carton rather than a pack shot.
#:
#: Matrixyl 3000 Pro Collagen Serum has no silver pack shot. Its silver carton was
#: generated from its own green face - a finish change, not an invention, since the
#: green face already carries the correct geometry and every word of the text. The
#: flat dieline was the alternative and was rejected: correct content, but no
#: perspective, edges or sheen, so it briefs the material poorly.
#:
#: The generated file is stored in Drive beside the real pack shots because it
#: CANNOT be reproduced by re-running this script - generation is not
#: deterministic. Treat it as source material, not as output.
#:
#: Replace it the day a real silver pack shot of that carton exists.
GENERATED_SILVER = {
    "matrixyl-3000-pro-collagen-serum": "GENERATED-matrixyl-serum-silver-carton.png",
}

#: Retained for reference: the dieline panel this replaced.
DIELINE_SILVER = {"matrixyl-3000-pro-collagen-serum": (0.51, 0.28, 0.71, 0.62)}

BG_TOLERANCE = 18    # how far from the corner colour still counts as background
MARGIN = 0.06        # breathing room around the subject bbox
TIGHT_TOLERANCE = 34 # stricter cut that ignores soft cast shadow
SOFT_TOLERANCE = 8   # low cut that still sees the white pipette bulb on white
MAX_TOP_LIFT = 0.16  # cap on how far the low cut may extend the box upward
SUBJECT_FILL = 0.84  # subject's longest edge as a share of the square canvas
RENDER_TOLERANCE = 90 # strict cut for the dedicated renders, which sit on a MIRROR
                      # reflection. At 34 the reflection reads as subject and the
                      # bottle ends up half-size in the crop; at 90 only the bottle
                      # survives. The bulb is still recovered by the soft pass.


def subject_bbox(im: Image.Image) -> tuple[int, int, int, int]:
    """Bounding box of the non-background content."""
    rgb = im.convert("RGB")
    bg = Image.new("RGB", rgb.size, rgb.getpixel((4, 4)))
    diff = ImageChops.difference(rgb, bg).convert("L").point(lambda p: 255 if p > BG_TOLERANCE else 0)
    return diff.getbbox() or (0, 0, *rgb.size)


def tight_bbox(im: Image.Image, strict_tol: int = TIGHT_TOLERANCE):
    """Subject box that keeps white parts but drops the cast shadow.

    Two competing failures, both white-on-white:

      * a STRICT threshold drops the serum pipette's white rubber bulb, because
        it sits at nearly the same value as the sweep - the crop then decapitates
        every serum bottle.
      * a PERMISSIVE threshold keeps the bulb but also counts the soft cast
        shadow, which inflates the box and shrinks the subject once squared -
        that was the Copper Peptide carton size mismatch.

    So: take the horizontal extent and the BOTTOM from the strict pass (shadow
    falls below and beside the object), and the TOP from the permissive pass
    (that is where the white bulb is). Shadow excluded, bulb kept.
    """
    rgb = im.convert("RGB")
    bg = Image.new("RGB", rgb.size, rgb.getpixel((4, 4)))
    strict = ImageChops.difference(rgb, bg).convert("L").point(
        lambda p: 255 if p > strict_tol else 0).getbbox()
    if strict is None:
        return None
    loose = ImageChops.difference(rgb, bg).convert("L").point(
        lambda p: 255 if p > SOFT_TOLERANCE else 0).getbbox()
    if loose is None:
        return strict
    l, t, r, b = strict
    # Extend upward only far enough to recover a white cap, and no further. An
    # unbounded extension let the low threshold latch onto the faint background
    # gradient at the top of frame, which stretched the box to the canvas edge and
    # shrank the subject to 40% of the crop.
    max_lift = int((b - t) * MAX_TOP_LIFT)
    return (l, max(t - max_lift, min(t, loose[1])), r, b)


def isolate(im: Image.Image, comp_mask, box: tuple[int, int, int, int], size: int, dest: str) -> str:
    """Crop `box` and erase everything not belonging to this component.

    Cropping to a bounding box alone still leaves a sliver of the neighbour
    wherever the two objects' boxes overlap - the carton edge showing beside a
    jar, a slice of pink bottle beside a silver carton. The component mask says
    which pixels are actually THIS object, so the rest is painted out to the
    background sweep and the reference contains one product and nothing else.
    """
    l, t, r, b = box
    pad_x, pad_y = int((r - l) * MARGIN), int((b - t) * MARGIN)
    L, T = max(0, l - pad_x), max(0, t - pad_y)
    R, B = min(im.width, r + pad_x), min(im.height, b + pad_y)

    crop = im.crop((L, T, R, B)).convert("RGB")
    sub = comp_mask[T:B, L:R]

    bg = im.getpixel((4, 4))
    px = crop.load()
    h, w = sub.shape
    for y in range(h):
        row = sub[y]
        for x in range(w):
            if not row[x]:
                px[x, y] = bg

    cw, ch = crop.size
    edge = max(cw, ch)
    canvas = Image.new("RGB", (edge, edge), bg)
    canvas.paste(crop, ((edge - cw) // 2, (edge - ch) // 2))
    canvas.resize((size, size), Image.LANCZOS).save(dest)
    return dest


def whole_crop(path: str, size: int, dest: str, strict_tol: int = TIGHT_TOLERANCE) -> str:
    """Trim a single-subject image to its subject and normalise it to SUBJECT_FILL.

    Used for the generated carton, which has no neighbour to split away from but
    must still arrive at the same scale as every other reference.
    """
    im = Image.open(path).convert("RGB")
    bb = tight_bbox(im, strict_tol) or subject_bbox(im)
    sub = im.crop(bb)
    bg = im.getpixel((4, 4))
    w, h = sub.size
    edge = int(max(w, h) / SUBJECT_FILL)
    canvas = Image.new("RGB", (edge, edge), bg)
    canvas.paste(sub, ((edge - w) // 2, (edge - h) // 2))
    canvas.resize((size, size), Image.LANCZOS).save(dest)
    return dest


def side_crop(path: str, side: str, size: int, dest: str) -> str:
    """Crop one side of a pack shot at its explicit boundary, trim to the subject,
    then pad to square on the background sweep.

    No masking. Erasing "non-subject" pixels bit chunks out of every silver and
    white carton, because those sit at nearly the same value as the white
    background - the mask could not tell carton from sweep.
    """
    im = Image.open(path).convert("RGB")
    frac = BOUNDARY.get(os.path.basename(path), BOUNDARY_DEFAULT)
    if isinstance(frac, tuple):
        frac = frac[0] if side == "left" else frac[1]
    cut = int(im.width * frac)
    part = im.crop((0, 0, cut, im.height)) if side == "left" else im.crop((cut, 0, im.width, im.height))

    # Tight bbox: a stricter threshold than subject_bbox so a soft cast shadow
    # does not inflate the box. An inflated bbox makes a larger square, which
    # makes the object SMALLER in the finished crop - that is why the two Copper
    # Peptide cartons came out at different scales from each other.
    bb = tight_bbox(part)
    if bb is None:
        bb = subject_bbox(part)
    l, t, r, b = bb
    sub = part.crop((l, t, r, b))

    # Normalise fill: the subject's longest edge always occupies the same share of
    # the square, so a product and its two carton faces arrive at a consistent
    # scale regardless of how each source shot was framed.
    bg = im.getpixel((4, 4))
    w, h = sub.size
    edge = int(max(w, h) / SUBJECT_FILL)
    canvas = Image.new("RGB", (edge, edge), bg)
    canvas.paste(sub, ((edge - w) // 2, (edge - h) // 2))
    canvas.resize((size, size), Image.LANCZOS).save(dest)
    return dest


def components(path: str):
    """Return (image, comp_masks, boxes) for the two largest objects, left to right.

    Connected-component labelling on the foreground mask. This replaces every
    variant of "split the frame at column X", none of which can avoid leaving a
    sliver of the neighbour when the two bounding boxes overlap.
    """
    import numpy as np
    from scipy import ndimage

    im = Image.open(path).convert("RGB")
    m = np.array(_mask(im)) > 0
    # close small gaps so a soft shadow does not fragment one object into several
    m = ndimage.binary_closing(m, structure=np.ones((9, 9)))
    lab, n = ndimage.label(m)
    if n == 0:
        return im, [], []

    sizes = ndimage.sum(m, lab, range(1, n + 1))
    order = sorted(range(n), key=lambda i: -sizes[i])
    keep = [i + 1 for i in order[:2]]

    # Where the two objects' shadows touch they label as ONE component. Cut the
    # merged blob at its narrowest column rather than returning a single object -
    # this happens on the PDRN cream, whose jar and carton nearly abut.
    big = lab == keep[0]
    if len(keep) < 2 or sizes[order[1]] < sizes[order[0]] * 0.15:
        cols = big.sum(axis=0)
        xs = np.where(cols > 0)[0]
        lo, hi = xs.min(), xs.max()
        span = hi - lo
        window = slice(lo + int(span * 0.30), lo + int(span * 0.70))
        cut = lo + int(span * 0.30) + int(np.argmin(cols[window]))
        left, right = big.copy(), big.copy()
        left[:, cut:] = False
        right[:, :cut] = False
        parts = [left, right]
    else:
        parts = [lab == keep[0], lab == keep[1]]

    out = []
    for comp in parts:
        ys, xs = np.where(comp)
        if len(xs) == 0:
            continue
        out.append((comp, (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))))
    out.sort(key=lambda c: c[1][0])  # left to right: product, then carton
    return im, [c[0] for c in out], [c[1] for c in out]


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

        render = PRODUCT_RENDER.get(slug)
        rpath = os.path.join(PRODUCTS_DIR, render) if render else None
        if rpath and os.path.exists(rpath):
            whole_crop(rpath, 1024, os.path.join(d, "product_tight.png"), RENDER_TOLERANCE)
        else:
            print(f"  {slug}: no dedicated render, falling back to the pack shot")
            side_crop(src, "left", 1024, os.path.join(d, "product_tight.png"))
        side_crop(src, "right", 1024, os.path.join(d, "box_coloured_face.png"))
        prep_refs.square_crop(src, os.path.join(d, "pack_full.png"), 1024)
        made = 3

        if silver:
            s = os.path.join(SRC, silver)
            if os.path.exists(s):
                side_crop(s, "right", 1024, os.path.join(d, "box_silver_face.png"))
                made += 1
        elif slug in GENERATED_SILVER:
            g = os.path.join(SRC, GENERATED_SILVER[slug])
            if os.path.exists(g):
                whole_crop(g, 1024, os.path.join(d, "box_silver_face.png"))
                made += 1
                print(f"  {slug}: silver face from the GENERATED carton "
                      f"(no pack shot exists)")
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
