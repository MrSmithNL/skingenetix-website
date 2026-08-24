#!/usr/bin/env python3
"""Widen a banner shot by extending its background off the left edge.

    python3 scripts/extend-banner-canvas.py --preview
    python3 scripts/extend-banner-canvas.py

The /collections/pdrn source is 2048x848 (2.41:1) with the model hard right. The
collection banner wants a wider frame with clear space on the left for the heading,
so the canvas grows leftward to 3:1 and the new area is filled with the shot's own
backdrop -- no crop, so the full height still shows in the header.

Padding flat charcoal would not survive a look, because the subject TOUCHES the
left edge: below y=632 the shoulder runs off frame. Repeating that edge column
would smear the shoulder into a horizontal bar. So the fill is built in two parts
and stitched at the shoulder line:

  background   the smooth backdrop, held at its own vertical gradient, which is
               extrapolated below y=632 from the clean rows above it
  shoulder     the edge profile SHEARED down as it travels left, continuing the
               real slope of the shoulder (~0.5px down per px left) so it sinks
               out of the bottom-left corner the way the actual shoulder does

Grain is resampled from the real backdrop -- a smoothed profile repeated across
500px reads as a flat plate next to film-grained pixels -- and a slight vignette
falls off to the left, which is how the original backdrop is already lit and keeps
white heading text clean.

Author: Claude Code, 2026-08-24.
"""
import argparse
import numpy as np
from PIL import Image
from pathlib import Path
from scipy import ndimage

ROOT = Path(__file__).resolve().parent.parent
SRC = (ROOT / "assets/ai-generated/2026-08-22-multi-banner-library-pdrn-collagen-repair-cream"
              / "pdrn-collagen-repair-cream--B-face-full-prod-right"
              / "pdrn-collagen-repair-cream--B-face-full-prod-right-gpt_image_01.png")
OUT = ROOT / "assets/publish-ready/collection-pdrn-banner"

DESKTOP = "skingenetix-pdrn-collagen-repair-cream-skincare.jpg"
MOBILE = "skingenetix-pdrn-collagen-repair-cream-mobile.jpg"

TARGET_RATIO = 3.0      # matches the /collections/all banner
EDGE_COLS = 6           # columns averaged into the edge profile
SHOULDER_Y = 632        # row where the shoulder meets x=0
SHEAR = 0.50            # px down per px left, measured off the shoulder line
BG_FIT = (380, 560)     # clean backdrop rows used to model its vertical gradient
TEXTURE_MAX_Y = 555     # last row that is backdrop at EVERY x in the texture patch
VIGNETTE = 0.13         # how far the far-left edge is darkened
QUALITY = 95            # matches .claude/rules/website-imagery.md rule 5: the CDN,
                        # not this script, does the compressing. No ICC is embedded
                        # either -- upload-theme-images.py strips metadata anyway.
MOBILE_CROP = (1700, 2421)  # portrait crop: face and jar, label fully legible


def edge_profile(im):
    """Left-edge colour profile, and the backdrop lighting to use behind it.

    Above the shoulder the profile IS backdrop, so it is used as measured -- that
    is what makes the join invisible, since the column next to the original then
    reproduces the original's own edge exactly. Only below the shoulder line, where
    the real profile is skin, does the backdrop have to be modelled: a straight
    ramp fitted on clean rows and carried down into the area the shoulder vacates.
    """
    prof = ndimage.gaussian_filter1d(im[:, :EDGE_COLS].mean(axis=1), 2.0, axis=0)
    rows = np.arange(im.shape[0])

    ys = np.arange(*BG_FIT)
    ramp = np.stack([np.polyval(np.polyfit(ys, prof[ys, c], 1), rows) for c in range(3)],
                    axis=-1)
    hand_over = np.clip((rows - (SHOULDER_Y - 40)) / 40.0, 0, 1)[:, None]
    return prof, prof * (1 - hand_over) + ramp * hand_over


def scatter(im, box, sigma, h, w, seed):
    """Detail lifted from a real region, resampled pixel-wise at random.

    Used for the extended shoulder. Mirror-tiling skin drew a faint diamond across
    it -- the tile boundaries line up into an outline the eye finds immediately,
    and shrinking the detail scale only made it fainter, never absent. Independent
    sampling has no boundaries to line up; the light blur afterwards puts the grain
    back to roughly pore size.
    """
    y0, y1, x0, x1 = box
    patch = im[y0:y1, x0:x1].astype(np.float64)
    detail = patch - ndimage.gaussian_filter(patch, (sigma, sigma, 0))
    rng = np.random.default_rng(seed)
    ys = rng.integers(0, detail.shape[0], size=h)
    xs = rng.integers(0, detail.shape[1], size=w)
    return ndimage.gaussian_filter(detail[np.ix_(ys, xs)], (0.8, 0.8, 0))


def texture(im, box, sigma, h, w):
    """Detail lifted from a real region of the shot, mirror-tiled to (h, w).

    A smoothed profile repeated 500px reads as a plate, so the actual grain is
    carried across and relit. Two regions get sampled: the backdrop's cloth weave,
    and the shoulder's skin, because an extension with no pores against real pores
    shows a seam even when the tone matches exactly.

    The backdrop patch stops well clear of the shoulder -- reading down to
    SHOULDER_Y caught its crest at y=581 and mirror-tiling that lump of lit skin
    dropped a floating leaf shape into the dark.
    """
    y0, y1, x0, x1 = box
    patch = im[y0:y1, x0:x1].astype(np.float64)
    detail = patch - ndimage.gaussian_filter(patch, (sigma, sigma, 0))
    ph, pw, _ = detail.shape
    ys = np.arange(h) % (2 * ph)
    ys = np.where(ys < ph, ys, 2 * ph - 1 - ys)
    xs = np.arange(w) % (2 * pw)
    xs = np.where(xs < pw, xs, 2 * pw - 1 - xs)
    return detail[np.ix_(ys, xs)]


def extend_left(im, extra):
    h = im.shape[0]
    prof, backdrop = edge_profile(im)
    out = np.zeros((h, extra, 3), dtype=np.float64)
    alpha = np.zeros((h, extra, 1), dtype=np.float64)
    rows = np.arange(h)

    for x in range(extra):
        d = extra - x                      # distance left of the original edge
        # The shoulder line steepens as it recedes, so a straight shear reads as a
        # ruled edge over 500px. The quadratic term sinks it out of frame by ~d=310.
        shift = SHEAR * d + 0.0006 * d * d

        src = np.clip(rows - shift, 0, h - 1)
        lo = np.floor(src).astype(int)
        f = (src - lo)[:, None]
        sheared = prof[lo] * (1 - f) + prof[np.clip(lo + 1, 0, h - 1)] * f

        a = np.clip((rows - (SHOULDER_Y + shift)) / 8.0 + 0.5, 0, 1)[:, None]
        col = backdrop * (1 - a) + sheared * a
        col *= 1.0 - VIGNETTE * (d / extra) ** 2
        out[:, x] = col
        alpha[:, x] = a

    weave = texture(im, (0, TEXTURE_MAX_Y, 0, 820), 25, h, extra)
    skin = scatter(im, (SHOULDER_Y + 30, h, 0, 460), 5, h, extra, seed=20260824)
    return np.clip(out + weave * (1 - alpha) + skin * alpha, 0, 255)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--preview", action="store_true", help="write a PNG, skip the jpgs")
    args = ap.parse_args()

    im = np.array(Image.open(SRC).convert("RGB")).astype(np.float64)
    h, w, _ = im.shape
    target_w = int(round(h * TARGET_RATIO))
    extra = target_w - w
    if extra <= 0:
        raise SystemExit(f"source is already {w / h:.2f}:1 — nothing to extend")

    wide = np.concatenate([extend_left(im, extra), im], axis=1)
    final = Image.fromarray(wide.astype(np.uint8))
    print(f"{w}x{h} ({w/h:.2f}:1)  ->  {target_w}x{h} ({target_w/h:.2f}:1), "
          f"added {extra}px of backdrop on the left")

    OUT.mkdir(parents=True, exist_ok=True)
    if args.preview:
        p = OUT / "_preview-extended.png"
        final.save(p)
        print(f"preview -> {p.relative_to(ROOT)}")
        return

    jpeg = dict(format="JPEG", quality=QUALITY, optimize=True, progressive=True,
                subsampling=0)
    final.save(OUT / DESKTOP, **jpeg)

    # portrait crop for phones, anchored on the face and the jar
    final.crop((MOBILE_CROP[0], 0, MOBILE_CROP[1], h)).save(OUT / MOBILE, **jpeg)
    final.save(OUT / "_master-extended.png", optimize=True)

    for name in (DESKTOP, MOBILE):
        p = OUT / name
        iw, ih = Image.open(p).size
        print(f"{name:<52} {iw}x{ih}  {p.stat().st_size / 1024:>6.0f} KB")


if __name__ == "__main__":
    main()
