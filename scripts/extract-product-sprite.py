#!/usr/bin/env python3
"""Cut a product out of its studio master and save it as an RGBA sprite.

    python3 scripts/extract-product-sprite.py --product copper-peptide-repair-serum
    python3 scripts/extract-product-sprite.py --all --check

Bundle shots (3-up, 6-up) need the SAME product drawn several times at different
sizes with the units overlapping, so each unit has to be a free-standing sprite
with an alpha channel. This script produces those sprites from the authoritative
Drive masters under `Images/Products/<Product>/`, not from any AI-generated shot,
because the master is the only source guaranteed to carry the current artwork.

WHY NOT JUST TAKE A LAYER OUT OF THE .PSD. That was tried first and it does not
work for either template. Both masters were built by retouching a photograph that
was already on white, so the "product" is entangled with the ground:

  * serum — `Layer 10` is a full-canvas OPAQUE layer holding the bottle AND the
    studio sweep AND the floor reflection. Hiding the background layer beneath it
    changes nothing; the composite still comes back 100% opaque.
  * cream — the silver lid lives in `Layer 3`, which is the lid PLUS a white slab
    that was painted in to cover the lid of the superseded jar still sitting in
    the hidden `Layer 2`. Take the layer and you take the slab with it.

So the cut has to be made from the pixels. The two traps that decide how:

TRAP 1 — A PLAIN THRESHOLD EATS THE PRODUCT. The serum's ground is a vertical
gradient (RGB 228 at the top, 247 in the middle, 236 at the foot), so a single
background colour is wrong by up to 19 levels before any product is involved.
Worse, the bottle's frosted lower third is PALER than the ground is at the top of
the frame. A flat threshold at 18 reported the bottle as 1868px wide - it was
reading the gradient, not the glass. The background is therefore modelled PER ROW
from the outer 100 columns, which are pure ground in every row (the widest thing
in frame, the bottle body, spans x750-1283 of 2048).

TRAP 2 — AND A THRESHOLD THAT SURVIVES TRAP 1 STILL EATS THE HIGHLIGHTS. The
serum's dropper bulb is white, its collar is brushed silver, and the cream's whole
lid is silver: all of them contain pixels at or above the background value. Any
"is this pixel background-coloured" test drills holes through the middle of the
product. The fix is not a cleverer threshold - it is to stop asking that question.
Background is defined as the pale region CONNECTED TO THE FRAME BORDER; anything
pale but enclosed by product is product. A near-white highlight in the middle of a
lid is not reachable from the border, so it stays opaque by construction.

This is the same lesson the white-on-white reference cropping cost us seven
attempts to learn: measure or constrain the boundary, never merely detect it.

THE REFLECTION IS CUT OFF, NOT KEPT. The serum master stands on a reflective
surface and its reflection runs to the bottom edge of the frame - it is clipped by
the canvas, so it cannot be scaled with the bottle without the clip showing. Each
unit in a bundle sits at a different depth and needs its own reflection anyway, so
the sprite stops at the measured contact line (`base_y`) and the bundle compositor
draws contact shadows itself.

Author: Claude Code, 2026-08-31.
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = Path(__file__).resolve().parent.parent
DRIVE = Path.home() / (
    "Library/CloudStorage/GoogleDrive-msmithnl@gmail.com/My Drive/Skingenetix"
)
MASTERS = DRIVE / "Images/Products"
OUT_DIR = ROOT / "assets/images/_sprites"

#: Per-product extraction settings. `base_y` is the measured contact line in
#: master pixels - the row where the product meets the surface it stands on. It is
#: written down rather than detected because a reflection is the same width and
#: nearly the same colour as the thing reflected, so no edge test separates them.
#: Measured 2026-08-31 by cropping the base region and reading the boundary off a
#: 2x enlargement, then confirmed against the width profile.
#:
#: `bg_model` is "rows" where the ground is a gradient and "flat" where it is a
#: single value. Using "flat" on a gradient is trap 1 above.
#:
#: `thr_lo` was not chosen by eye. Each product was swept from 8 to 28 and the
#: resulting bbox compared against the silhouette measured by hand off the master.
#: Both products show a PLATEAU - a wide band of thresholds that all return the
#: same bbox - and the value below is the middle of that plateau. The plateau is
#: the real result here: a boundary whose position is unchanged by tripling the
#: threshold is a hard edge, and a hard edge is what makes the cut trustworthy.
#: Outside it the numbers move fast (serum at 15 came back 1104px wide against a
#: true 537), which is the fragmented-background failure, not a softer edge.
PRODUCTS = {
    "copper-peptide-repair-serum": {
        "master": "Copper Peptide Repair Serum/Copper Peptide Repair Serum.png",
        "bg_model": "rows",
        "base_y": 1697,
        "thr_lo": 22,  # plateau 18-28, bbox (748, 363, 1285, 1697)
        "thr_hi": 36,
        "axis_x": 1016.5,  # (748 + 1285) / 2; collar centres on 1015, so it agrees
        "kind": "bottle",
    },
    "copper-peptide-day-repair-cream": {
        "master": "Copper Peptide Day Repair Cream/Copper Peptide Day Cream.png",
        "bg_model": "flat",
        "base_y": None,  # the jar sits on flat white with no reflection to remove
        "thr_lo": 16,  # plateau 12-20, bbox (155, 269, 1320, 1239)
        "thr_hi": 28,
        # No mirror. The jar's edges are hard on all four sides and its cut needs
        # no help; mirroring an already-correct silhouette can only widen it if
        # the axis is off by a pixel.
        "axis_x": None,
        "kind": "jar",
    },
}


def background_model(arr, mode, margin=100):
    """Return an (h, 1, 3) or (1, 1, 3) estimate of the ground behind the product.

    "rows" takes the median of the outer `margin` columns in each row, which
    tracks a vertical gradient exactly. "flat" takes one median over the whole
    border ring, which is right only when the ground really is one value.
    """
    if mode == "rows":
        side = np.concatenate([arr[:, :margin], arr[:, -margin:]], axis=1)
        return np.median(side, axis=1)[:, None, :]
    ring = np.concatenate(
        [
            arr[:8].reshape(-1, 3),
            arr[-8:].reshape(-1, 3),
            arr[:, :8].reshape(-1, 3),
            arr[:, -8:].reshape(-1, 3),
        ]
    )
    return np.median(ring, axis=0)[None, None, :]


def span_fill(mask):
    """Close each row and column between its first and last set pixel.

    Both templates are ONE solid object photographed dead-on, so every row that
    crosses the product crosses exactly one continuous span of it, and so does
    every column. That is a fact about the subject, and it is the only thing
    strong enough to close the serum's dropper bulb.

    The bulb is why this exists. Its shaded flanks sit 45-61 levels off the
    ground and detect perfectly, but the highlight running over the top of the
    cap measures 249-255 against a ground of 237-253 - a separation of 1 to 8
    levels. No threshold anywhere can tell those apart, and no hole-filling can
    help either, because the gap is at the top of the silhouette and therefore
    open to the background rather than enclosed by product. Without this step the
    bulb comes out sliced flat across the crown.
    """
    out = mask.copy()
    for axis in (1, 0):
        idx = np.arange(mask.shape[axis])
        broadcast = (1, -1) if axis == 1 else (-1, 1)
        shaped = idx.reshape(broadcast)
        present = mask.any(axis=axis, keepdims=True)
        first = np.where(mask, shaped, mask.shape[axis]).min(axis=axis, keepdims=True)
        last = np.where(mask, shaped, -1).max(axis=axis, keepdims=True)
        out |= present & (shaped >= first) & (shaped <= last)
    return out


def mirror_about(mask, axis_x):
    """Reflect the mask across the vertical axis at `axis_x` (in pixels).

    Both products are solids of revolution photographed dead-on, so whatever the
    lighting does, the OUTLINE is symmetric about the bottle's own axis. Only the
    mask is mirrored, never the pixels - the shading is genuinely asymmetric and
    must stay that way.

    This recovers the serum's lit flank. The key light comes from the left, so the
    dropper bulb's left side is a highlight at 249-255 against a ground of 237-253
    while its right side is shaded at 177-192. The shaded side detects perfectly
    and the lit side not at all, which left the bulb sliced down a straight
    vertical line with only its right shoulder rounded. The span fill cannot mend
    that: a column through the missing flank has no product pixel anywhere in the
    bulb to span between.
    """
    h, w = mask.shape
    # Sample at 2x so a half-pixel axis (the usual case for an even-width object)
    # reflects without drifting the silhouette half a pixel sideways.
    src = np.arange(w)
    ref = np.rint(2.0 * axis_x - src).astype(np.int64)
    valid = (ref >= 0) & (ref < w)
    out = np.zeros_like(mask)
    out[:, valid] = mask[:, ref[valid]]
    return out


def extract(master_path, bg_model, base_y, thr_lo, thr_hi, axis_x=None):
    """Cut the product out and return a tightly-cropped RGBA image."""
    im = Image.open(master_path).convert("RGB")
    arr = np.asarray(im).astype(np.float32)
    h, w, _ = arr.shape

    bg = background_model(arr, bg_model)
    dev = np.abs(arr - bg).max(axis=2)

    # The reflection is removed BEFORE the silhouette is built, not after. It is
    # the same width and nearly the same colour as the bottle and it touches the
    # bottle at the base, so left in it joins the product's connected component
    # and drags the span fill down to the bottom edge of the frame.
    if base_y is not None:
        dev[base_y:] = 0.0

    solid = dev > thr_lo
    # Drop specks in the ground. The ground varies 11-16 levels ACROSS a single
    # row - a vignette the per-row median cannot follow - so a few pixels always
    # clear the threshold out in open space, and the span fill would rope them
    # into the silhouette as spikes.
    labels, n = ndimage.label(solid)
    if n:
        sizes = ndimage.sum(solid, labels, range(1, n + 1))
        solid = labels == (int(np.argmax(sizes)) + 1)

    if axis_x is not None:
        solid |= mirror_about(solid, axis_x)
    solid = ndimage.binary_fill_holes(span_fill(solid))

    # Soft alpha only in the transition band, forced opaque one pixel inside the
    # silhouette so that interior highlights can never be made transparent by the
    # deviation term.
    soft = np.clip((dev - thr_lo) / max(thr_hi - thr_lo, 1), 0.0, 1.0)
    interior = ndimage.binary_erosion(solid, iterations=2)
    alpha = np.where(interior, 1.0, np.where(solid, np.maximum(soft, 0.35), 0.0))
    alpha = np.where(solid, alpha, 0.0)

    if base_y is not None:
        # Feathered over 5 rows so the contact edge does not read as a scalpel
        # line when the sprite is scaled up.
        f0 = max(base_y - 5, 0)
        alpha[f0:base_y] *= np.linspace(1.0, 0.0, base_y - f0, endpoint=False)[:, None]

    out = np.dstack([np.asarray(im).astype(np.uint8), (alpha * 255).astype(np.uint8)])
    sprite = Image.fromarray(out, "RGBA")
    bbox = sprite.getchannel("A").point(lambda v: 255 if v > 2 else 0).getbbox()
    return sprite.crop(bbox), bbox


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--product", help="key from PRODUCTS")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--check", action="store_true", help="also write a magenta proof")
    args = ap.parse_args()

    keys = list(PRODUCTS) if args.all else [args.product]
    if not keys or keys == [None]:
        sys.exit("give --product <key> or --all; keys: " + ", ".join(PRODUCTS))

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for key in keys:
        cfg = PRODUCTS[key]
        master = MASTERS / cfg["master"]
        if not master.exists():
            sys.exit(f"master not found: {master}")
        sprite, bbox = extract(
            master,
            cfg["bg_model"],
            cfg["base_y"],
            cfg["thr_lo"],
            cfg["thr_hi"],
            cfg.get("axis_x"),
        )
        dest = OUT_DIR / f"{key}.png"
        sprite.save(dest)
        manifest[key] = {
            "master": str(master),
            "sprite": str(dest.relative_to(ROOT)),
            "size": list(sprite.size),
            "bbox_in_master": list(bbox),
            "kind": cfg["kind"],
        }
        print(f"{key}: {sprite.size[0]}x{sprite.size[1]} from bbox {bbox} -> {dest}")

        if args.check:
            proof = Image.new("RGBA", sprite.size, (255, 0, 255, 255))
            proof.alpha_composite(sprite)
            proof.convert("RGB").save(OUT_DIR / f"{key}_on-magenta.png")

    (OUT_DIR / "sprites.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
