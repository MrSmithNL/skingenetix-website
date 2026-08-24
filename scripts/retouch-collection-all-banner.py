#!/usr/bin/env python3
"""Turn the chosen ChatGPT frame into the publish-ready /collections/all banner.

    python3 scripts/retouch-collection-all-banner.py

Reads  assets/ai-generated/2026-08-24-collection-all-banner/chatgpt-source-*.png
Writes assets/publish-ready/collection-all-banner/  (desktop jpg, mobile jpg, png master)

Three jobs, in order:

1. REPAIR the words the generator mis-set. They are small but legible at render
   size, and a garbled word on a hero banner reads as a broken shop:
     blue serum   "ADVANCED REPAIR / SEPAIR SERUM"      -> "ADVANCED REPAIR / SERUM"
     matrixyl jar "FULL & FIRMING TREEAENT / FREATMENT" -> "FULL & FIRMING"
   Nothing is drawn. `slide` moves real pixels along the label's own baseline so
   font, blur, lighting and grain stay consistent; `erase` rebuilds a band from
   its own de-lettered background. The two pink labels were checked at 100% and
   were already correct, so they are left alone.

2. RECOLOUR the copper-peptide bottle's descriptor line and its accent rule from
   the neutral grey the generator used to brand light blue (Malcolm, 2026-08-24).
   `ink_abundance` unmixes each pixel into "grey ink" and "white ink" fractions
   against the local glass, so only the grey element moves; COPPER PEPTIDE,
   PREMIUM FORMULA and the wordmark keep their white, and blurred stroke edges
   carry across smoothly instead of showing a hard recoloured cutout.

3. EXPORT a full-width desktop jpg and a portrait mobile crop. The theme's
   collection-banner box is a FIXED pixel height across a full-bleed width, so
   its aspect swings from ~1.0 on a phone to ~5.8 on a wide monitor; the desktop
   image is published at image_size "auto" (no crop at any width) and the phone
   gets its own crop rather than the middle third of a 3:1 frame.

Label text runs uphill to the right in this shot, so every band is defined by its
top edge at x0 plus a slope, never by a rectangle.

Author: Claude Code, 2026-08-24.
"""
import numpy as np
from PIL import Image, ImageCms
from pathlib import Path
from scipy import ndimage

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets/ai-generated/2026-08-24-collection-all-banner/chatgpt-source-2026-08-21-1707-4.png"
OUT = ROOT / "assets/publish-ready/collection-all-banner"

DESKTOP = "skingenetix-peptide-skincare-collection-copper-peptide-pdrn.jpg"
MOBILE = "skingenetix-copper-peptide-pdrn-serums-mobile.jpg"
MOBILE_CROP = (830, 0, 1450, 724)   # blue + pink serum, portrait 0.86
QUALITY = 90                        # 4:4:4 -- the labels are small coloured type

PAD = 24                            # context so a filter is not edge-biased

# measured off the copper-peptide label at 1:1
T_GREY = np.array([83.3, 90.6, 110.0])
T_WHITE = np.array([183.6, 192.6, 217.9])
LIGHT_BLUE = np.array([143.0, 211.0, 245.0])   # #8FD3F5
LABEL = (935, 460, 1200, 620)                  # x0, y0, x1, y1 around the blue label


def _ramp(n, feather):
    """1.0 across the middle, cosine-eased to 0.0 at both ends."""
    w = np.ones(n)
    f = min(feather, max(1, n // 2))
    e = 0.5 - 0.5 * np.cos(np.linspace(0, np.pi, f + 2)[1:-1])
    w[:f], w[-f:] = e, e[::-1]
    return w


def background(crop, strokes, pct=50):
    """Estimate `crop` with its lettering removed.

    A rank filter wider than the strokes drops them whichever way they run, which
    matters here: the grey type is lighter than the glass in red but darker in
    blue, so a single morphological opening or closing cleans one channel and
    wrecks another (it left a green cast). A rank needs no polarity.

    pct : 50 (median) where background wins the window on area. Where the
          lettering is dense enough to fill most of it -- the jar's blurred caps
          nearly span its band -- the median returns ink and leaves a ghost, so
          bias the rank towards the label: high for dark type on a light label.
    """
    out = np.empty_like(crop, dtype=np.float64)
    for ch in range(3):
        flat = ndimage.percentile_filter(crop[:, :, ch].astype(np.float64),
                                         percentile=pct, size=strokes, mode="nearest")
        out[:, :, ch] = ndimage.gaussian_filter(flat, sigma=strokes / 3.0)
    return out


def _band(x0, x1, ytop, height, slope):
    tops = {x: int(round(ytop + slope * (x - x0))) for x in range(x0 - PAD, x1 + PAD)}
    ys = [tops[x] for x in range(x0 - PAD, x1 + PAD)]
    return tops, (x0 - PAD, min(ys) - PAD, x1 + PAD, max(ys) + height + PAD)


def _blend(out, src, tops, x0, x1, height, box, feather):
    bx0, by0 = box[0], box[1]
    xw, yw = _ramp(x1 - x0, feather * 2), _ramp(height, feather)[:, None]
    for i, x in enumerate(range(x0, x1)):
        yt = tops[x]
        col = src[yt - by0:yt - by0 + height, x - bx0]
        dest = out[yt:yt + height, x].astype(np.float64)
        a = yw * xw[i]
        out[yt:yt + height, x] = np.clip(dest * (1 - a) + col * a, 0, 255)
    return out


def erase(img, x0, x1, ytop, height, slope, strokes, pct=50, feather=4):
    """Replace a sloped band with its own de-lettered background."""
    tops, box = _band(x0, x1, ytop, height, slope)
    bg = background(img[box[1]:box[3], box[0]:box[2]], strokes, pct)
    return _blend(img.copy(), bg, tops, x0, x1, height, box, feather)


def slide(base, donor, x0, x1, ytop, height, slope, dx, dy, strokes, feather=3):
    """Move the word at (x+dx, y+dy) in `donor` onto (x, y) in `base`, matched for
    the difference in label background between the two spots. `donor` is separate
    so a band can be erased first and still be drawn from."""
    tops, box = _band(x0, x1, ytop, height, slope)
    bx0, by0, bx1, by1 = box
    bg_dst = background(base[by0:by1, bx0:bx1], strokes)
    bg_src = background(donor[by0 + dy:by1 + dy, bx0 + dx:bx1 + dx], strokes)
    src = donor[by0 + dy:by1 + dy, bx0 + dx:bx1 + dx].astype(np.float64)
    return _blend(base.copy(), src + (bg_dst - bg_src), tops, x0, x1, height, box, feather)


def ink_abundance(reg):
    """Per-pixel fraction of grey ink, unmixing reg = bg + a(grey-bg) + b(white-bg).

    Solving for both inks at once is what keeps the white type out of it: white
    strokes load onto b, so recolouring a leaves them exactly as they were."""
    bg = np.stack([ndimage.median_filter(reg[:, :, c], size=21, mode="nearest")
                   for c in range(3)], -1)
    u, v, d = T_GREY - bg, T_WHITE - bg, reg - bg
    uu, vv, uv = (u * u).sum(-1), (v * v).sum(-1), (u * v).sum(-1)
    du, dv = (d * u).sum(-1), (d * v).sum(-1)
    det = uu * vv - uv * uv
    det = np.where(np.abs(det) < 1e-6, 1e-6, det)
    return np.clip(ndimage.gaussian_filter((du * vv - dv * uv) / det, 0.6), 0, 1.4)


def main():
    orig = np.array(Image.open(SRC).convert("RGB")).astype(np.float64)
    im = orig

    # 1a. blue serum: "SEPAIR SERUM" -> "SERUM". Wipe the line, then put SERUM
    #     back at its start from the untouched original, 71px left and 7px down
    #     along the -0.10 baseline. The erase needs a window wider than a stroke
    #     plus its blur halo; the colour match only needs the local light level.
    im = erase(im, x0=980, x1=1124, ytop=524, height=30, slope=-0.10,
               strokes=21, feather=5)
    im = slide(im, orig, x0=982, x1=1052, ytop=527, height=28, slope=-0.10,
               dx=71, dy=-7, strokes=13, feather=4)

    # 1b. matrixyl jar: drop both garbled words. At this size any rebuilt glyph
    #     reads worse than clean label stock, and the jar is defocused anyway.
    im = erase(im, x0=1934, x1=2014, ytop=394, height=33, slope=-0.09,
               strokes=15, pct=80, feather=5)
    im = erase(im, x0=1832, x1=1924, ytop=428, height=21, slope=-0.09,
               strokes=15, pct=80, feather=4)

    # 2. grey descriptor line + accent rule -> brand light blue
    x0, y0, x1, y1 = LABEL
    reg = im[y0:y1, x0:x1]
    a = ink_abundance(reg)[..., None]
    im[y0:y1, x0:x1] = np.clip(reg + a * (LIGHT_BLUE - T_GREY), 0, 255)

    # 3. export
    OUT.mkdir(parents=True, exist_ok=True)
    final = Image.fromarray(im.astype(np.uint8))
    srgb = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
    jpeg = dict(format="JPEG", quality=QUALITY, optimize=True, progressive=True,
                subsampling=0, icc_profile=srgb)
    final.save(OUT / DESKTOP, **jpeg)
    final.crop(MOBILE_CROP).save(OUT / MOBILE, **jpeg)
    final.save(OUT / "_master-retouched.png", optimize=True)

    for name in (DESKTOP, MOBILE):
        p = OUT / name
        w, h = Image.open(p).size
        print(f"{name:<62} {w}x{h}  {p.stat().st_size / 1024:>6.0f} KB")


if __name__ == "__main__":
    main()
