#!/usr/bin/env python3
"""Make every ingredient-page selector tile show its product at the SAME size.

    python3 scripts/normalise-tile-scale.py --check
    python3 scripts/normalise-tile-scale.py

The nine tiles came from nine different product shoots, so the product fills
anywhere from 47% to 84% of its frame and the row reads as ragged. Malcolm chose
the two references: the PDRN serum for bottles, the Copper Peptide night cream for
jars. Everything else is re-framed to match.

NOTHING IS RESAMPLED. The product is never scaled - only the CANVAS around it
changes, so the pixels a visitor sees are the originals. To make a product occupy
a smaller fraction, the canvas grows; to make it occupy a larger one, the canvas is
cropped in. New canvas edge = product_height / target_fraction.

Finding the product is the hard part, and brightness thresholding does not do it: a
frosted white bottle on a white sweep has almost no brightness contrast, and that
approach measured the acetyl bottle at 18% of frame against a true 80%. What the
product does have is SHARP EDGES while the studio background has only smooth
gradients, so the silhouette is found from gradient magnitude, closed solid, holes
filled, largest blob kept. Two frames need a more sensitive threshold than the rest
and say so in TILES.

Author: Claude Code, 2026-08-25.
"""
import argparse
import numpy as np
from PIL import Image
from pathlib import Path
from scipy import ndimage

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets/publish-ready/page-ingredients-tiles"
PR = "assets/publish-ready"; RUN = "assets/ai-generated"

#: (slot, kind, source, edge-sensitivity). Lower sensitivity finds fainter edges;
#: 0.10 suits a product that contrasts with its ground, 0.04 is needed where the
#: product is white-on-white and 0.10 finds only its printed label.
TILES = [
 ("t_copper","serum", f"{PR}/copper-peptide-repair-serum/__copper_peptide_ghk_cu_2_percent_advanced_repair_skin_serum_hero_white_bg_4_skingenetix.jpg", 0.10),
 ("t_acetyl","serum", f"{PR}/acetyl-hexapeptide-8-serum/_acetyl_hexapeptide_8_10_percent_anti_wrinkle_line_smoothing_skin_serum_hero_white_bg_2_skingenetix.jpg", 0.10),
 ("t_matrixyl","serum", f"{RUN}/2026-08-21-matrixyl-3000-pro-collagen-serum/run-01/matrixyl_3000_pro_collagen_10_percent_firming_repair_skin_serum_hero_white_bg_3_skingenetix.png", 0.10),
 ("t_pdrn","serum", f"{PR}/pdrn-skin-repair-serum/__pdrn_skin_repair_deep_renewal_face_serum_hero_white_bg_8_skingenetix.jpg", 0.10),
 ("t_glut","serum", f"{PR}/glutathione-brightening-serum/_glutathione_2_percent_vitamin_c_brightening_radiant_glow_skin_serum_hero_white_bg_1_skingenetix.jpg", 0.04),
 ("t_cday","cream", f"{PR}/copper-peptide-day-repair-cream/copper_peptide_ghk_cu_advanced_day_repair_face_cream_hero_whitebg_1_skingenetix.jpg", 0.10),
 ("t_cnight","cream", f"{PR}/copper-peptide-night-repair-cream/__copper_peptide_ghk_cu_advanced_night_repair_skin_cream_hero_whitebg_1_skingenetix.jpg", 0.10),
 ("t_mcream","cream", f"{RUN}/2026-08-21-matrixyl-3000-pro-collagen-cream/run-01/matrixyl_3000_triple_collagen_elastin_full_firming_face_cream_hero_whitebg_7_skingenetix.png", 0.10),
 ("t_pcream","cream", f"{PR}/pdrn-collagen-repair-cream/__pdrn_collagen_copper_peptide_deep_renewal_repair_skin_cream_hero_whitebg_2_skingenetix.jpg", 0.10),
]
REF = {"serum": "t_pdrn", "cream": "t_cnight"}


def bbox(path, fac):
    im = Image.open(path).convert("RGB")
    a = np.array(im).astype(float).mean(axis=2)
    s = max(a.shape) / 1024.0
    sm = ndimage.gaussian_filter(a, 1.5 * s)
    g = np.hypot(ndimage.sobel(sm, axis=1), ndimage.sobel(sm, axis=0))
    m = g > max(np.percentile(g, 99.0) * fac, 0.6)
    k = int(round(21 * s)) | 1
    m = ndimage.binary_fill_holes(ndimage.binary_closing(m, np.ones((k, k))))
    m = ndimage.binary_opening(m, np.ones((max(3, int(5 * s)),) * 2))
    lab, n = ndimage.label(m)
    sizes = ndimage.sum(m, lab, range(1, n + 1))
    ys, xs = np.where(lab == int(np.argmax(sizes)) + 1)
    return im, (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))


def reframe(im, box, target):
    """Grow or crop the canvas so the product is `target` of the frame height."""
    W, H = im.size
    ph = box[3] - box[1]
    n = int(round(ph / target))                       # new square edge
    cx = (box[0] + box[2]) // 2
    cy = (box[1] + box[3]) // 2
    a = np.array(im).astype(np.uint8)
    # Where the source sits in the new frame, as pad amounts. Negative means crop.
    top = n // 2 - cy; left = n // 2 - cx
    bot = n - H - top; right = n - W - left
    # Crop first, on whichever sides are negative...
    y0 = max(0, -top); x0 = max(0, -left)
    y1 = H - max(0, -bot); x1 = W - max(0, -right)
    a = a[y0:y1, x0:x1]
    # ...then grow the rest by REPLICATING THE EDGE, not by filling flat. These
    # sweeps are gradients, not white: a median-sampled flat fill left a visible
    # rectangle on five of the nine tiles where it butted against the original.
    # Edge replication carries the gradient outward instead, so the join has
    # nothing to show. A light blur over the grown band only removes the streaking
    # that replicating a noisy edge row would otherwise produce.
    pads = ((max(0, top), max(0, bot)), (max(0, left), max(0, right)), (0, 0))
    out = np.pad(a, pads, mode="edge").astype(np.float64)
    if max(pads[0] + pads[1]) > 0:
        soft = ndimage.gaussian_filter(out, (9, 9, 0))
        keep = np.zeros(out.shape[:2], bool)
        keep[pads[0][0]:out.shape[0] - pads[0][1],
             pads[1][0]:out.shape[1] - pads[1][1]] = True
        m = ndimage.gaussian_filter(keep.astype(float), 12)[..., None]
        out = out * m + soft * (1 - m)
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    boxes = {s: bbox(p, f) for s, k, p, f in TILES}
    tgt = {k: (lambda b: (b[1][3] - b[1][1]) / b[0].size[1])(boxes[REF[k]]) for k in REF}
    print("targets: " + ", ".join(f"{k} {v*100:.1f}% (from {REF[k]})" for k, v in tgt.items()))
    OUT.mkdir(parents=True, exist_ok=True)
    for slot, kind, path, fac in TILES:
        im, box = boxes[slot]
        before = (box[3] - box[1]) / im.size[1]
        new = reframe(im, box, tgt[kind])
        _, nb = None, None
        print(f"  {slot:<12} {kind:<6} {before*100:5.1f}% -> {tgt[kind]*100:5.1f}%   "
              f"canvas {im.size[0]} -> {new.size[0]}")
        if not args.check:
            p = OUT / f"{slot}.jpg"
            new.save(p, format="JPEG", quality=95, optimize=True,
                     progressive=True, subsampling=0)
    if not args.check:
        print(f"\nwrote {len(TILES)} tiles -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
