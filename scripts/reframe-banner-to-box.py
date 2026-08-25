#!/usr/bin/env python3
"""Reframe a tall banner master to the aspect the theme's banner box actually needs.

    python3 scripts/reframe-banner-to-box.py SRC OUT --aspect 4.0 \
        --band 380 2520 --sample-cols 300

WHY THIS EXISTS. The Impact banner box is a FIXED PIXEL HEIGHT (375/400/440px) across
a full-bleed width, with object-fit: cover. So its aspect is viewport/440 - 3.27:1 at
1440, 4.36:1 at 1920 - and any master narrower than that gets its HEIGHT cropped,
centred, with no say in the matter. A 2.36:1 face master loses 46% of its height at
1920, which on 2026-08-25 cut the model's smile off the live page: the one element the
picture was commissioned for. Briefing around it failed twice, because the engines
cannot see the box.

So the fit is solved here instead, deterministically:

  --band lo hi   the rows that MUST survive (eyebrows to chin, say). The crop is
                 recentred so this band sits in the middle of the frame, and the
                 canvas is widened until the band fits inside the box's visible
                 slice at --aspect. Nothing is scaled or squashed.

This is the FLAT-BACKGROUND case only: it extends the darker edge by holding each
row's own colour and re-scattering real grain over it. Where a limb or a shoulder
runs off the edge it would smear - that case has its own tuned tool in
scripts/extend-banner-canvas.py, which shears the edge profile to follow the subject.
The guard below refuses to run if the edge is not actually flat.

Author: Claude Code, 2026-08-25.
"""
import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image

#: Above this, the edge carries a subject and holding the row colour would smear it
#: into a horizontal bar - the failure this project already logged on 2026-08-24.
FLATNESS_LIMIT = 6.0


def extend_edge(a: np.ndarray, extra: int, sample: int, side: str, seed: int) -> np.ndarray:
    """Widen `a` by `extra` px on `side`, holding each row's own colour."""
    h, w, _ = a.shape
    strip = a[:, :sample] if side == "left" else a[:, -sample:]

    flat = float(strip.std(axis=1).mean())
    if flat > FLATNESS_LIMIT:
        sys.exit(f"edge is not flat (std {flat:.2f} > {FLATNESS_LIMIT}) - a subject "
                 f"probably runs off that edge; use extend-banner-canvas.py instead")

    # Per-row colour, lightly smoothed down the rows so the fill keeps the backdrop's
    # own vertical gradient instead of banding.
    rows = strip.mean(axis=1)
    k = 41
    pad = np.pad(rows, ((k // 2, k // 2), (0, 0)), mode="edge")
    smooth = np.stack([np.convolve(pad[:, c], np.ones(k) / k, mode="valid")
                       for c in range(3)], axis=1)

    fill = np.repeat(smooth[:, None, :], extra, axis=1)

    # A smoothed plate reads as plastic beside film-grained pixels, so scatter the
    # real grain (strip minus its own row means) across the new area.
    rng = np.random.default_rng(seed)
    grain = strip - rows[:, None, :]
    idx = rng.integers(0, strip.shape[1], size=(h, extra))
    fill += np.take_along_axis(grain, idx[:, :, None].repeat(3, axis=2), axis=1)

    return np.concatenate([fill, a] if side == "left" else [a, fill], axis=1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("out")
    ap.add_argument("--aspect", type=float, required=True,
                    help="target master aspect, e.g. 4.0 (box is viewport/440)")
    ap.add_argument("--band", type=int, nargs=2, metavar=("LO", "HI"), required=True,
                    help="rows that must survive the box crop, in source pixels")
    ap.add_argument("--box-aspect", type=float, default=1920 / 440,
                    help="widest box aspect to survive (default 1920/440)")
    ap.add_argument("--side", choices=["left", "right"], default="left")
    ap.add_argument("--sample-cols", type=int, default=300)
    ap.add_argument("--seed", type=int, default=7)
    args = ap.parse_args()

    a = np.asarray(Image.open(args.src).convert("RGB")).astype(np.float32)
    h, w, _ = a.shape
    lo, hi = args.band
    band_h = hi - lo
    band_mid = (lo + hi) / 2

    # 1. Recentre: trim the longer side so the band sits on the frame's centre line.
    trim = int(round(abs(band_mid - h / 2) * 2))
    if band_mid > h / 2:
        a, lo, hi = a[trim:], lo - trim, hi - trim
    elif trim:
        a = a[:-trim]
    h = a.shape[0]

    # 2. The box shows a slice of height  h * aspect / box_aspect  (when the master is
    #    narrower than the box). Widen until that slice covers the band.
    visible = h * args.aspect / args.box_aspect
    if visible < band_h:
        sys.exit(f"aspect {args.aspect} still crops the band "
                 f"({visible:.0f}px visible < {band_h}px needed) - raise --aspect")

    target_w = int(round(h * args.aspect))
    extra = target_w - w
    if extra <= 0:
        sys.exit(f"source is already {w / h:.2f}:1 - nothing to extend")

    out = extend_edge(a, extra, args.sample_cols, args.side, args.seed)
    Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(args.out)

    print(f"  source        {w}x{int(h + trim)}  ({w / (h + trim):.3f}:1)")
    print(f"  recentred     trimmed {trim}px off the {'top' if band_mid > (h + trim) / 2 else 'bottom'}")
    print(f"  extended      +{extra}px of backdrop on the {args.side}")
    print(f"  result        {out.shape[1]}x{out.shape[0]}  ({out.shape[1] / out.shape[0]:.3f}:1)")
    print(f"  band survives {visible:.0f}px visible at {args.box_aspect:.2f}:1, needs {band_h}px")


if __name__ == "__main__":
    main()
