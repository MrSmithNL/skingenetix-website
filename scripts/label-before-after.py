#!/usr/bin/env python3
"""Composite the before/after labels onto a generated diptych — deterministically.

    python3 scripts/label-before-after.py configs/banners/block-acetyl-research-before-after.json
    python3 scripts/label-before-after.py <config> --only ah8--f1-wang-2013-crows-feet

Why this exists rather than putting the numbers in the prompt: on this project
MATRIXYL failed in roughly thirty of fifty candidates with the word spelled letter by
letter, and a correct PDRN was resampled into PORN purely by Shopify's downscale. A
garbled percentage on a clinical-results page is not a cosmetic defect, it is a false
efficacy claim on a live storefront. The only number that cannot be misrendered is one
no model ever rendered, so the engines are barred from all text and every figure is
drawn here, from the `label` block of the wave config, at a known pixel position.

It also enforces the half-and-half split Malcolm asked for. The divider is drawn at
exactly width/2 whatever the engine did, and `--report` measures where the engine's OWN
seam actually landed so a candidate that composed 60/40 can be rejected on a number
rather than on a squint.

Type is the live theme's own faces, pulled from the Shopify CDN and converted to TTF in
assets/fonts/ — Fraunces for the figure, Muli for everything else — so the plate belongs
to the same page it sits on.

Author: Claude Code, 2026-08-25.
"""
import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "assets" / "fonts"

GRAPHITE = (26, 26, 26)
BONE = (240, 240, 240)
PEARL = (216, 214, 212)

#: Fractions of the master's edge, so the plate scales with any master size.
BAND_H = 0.165          # bottom scrim height
FIG_PT = 0.083          # the percentage
MEASURE_PT = 0.030      # the qualifier under it
PILL_PT = 0.0215        # BEFORE / AFTER caps
TRACK = 0.10            # letterspacing, as a fraction of the pill point size


def font(name: str, px: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONTS / name), px)


def draw_tracked(d: ImageDraw.ImageDraw, xy, text, f, fill, track):
    """PIL has no letterspacing. Caps at a small size need it or they read as a blob."""
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=f, fill=fill)
        x += d.textlength(ch, font=f) + track
    return x - xy[0] - track


def tracked_width(d, text, f, track):
    return sum(d.textlength(c, font=f) for c in text) + track * (len(text) - 1)


def fit_pill(d, text, base_px, max_w, track_frac):
    """Shrink a pill's type until it fits its half. 'WITH ACETYL HEXAPEPTIDE-8' does not
    fit at the same size as 'BEFORE', and silently clipping it would be worse."""
    px = base_px
    while px > 10:
        f = font("muli-bold.ttf", px)
        if tracked_width(d, text, f, px * track_frac) <= max_w:
            return f, px * track_frac
        px -= 1
    return font("muli-bold.ttf", 10), 1


def seam_offset(im: Image.Image) -> dict:
    """Where did the engine actually put its divider?

    Column-to-column mean absolute difference, searched across the middle 60% of the
    frame. A true diptych spikes hard at its seam; a continuous photograph does not
    spike at all. Both the position and the strength matter — a weak peak means there
    is no real seam there and the number should not be trusted.
    """
    g = im.convert("L")
    w, h = g.size
    small = g.resize((w, min(h, 256)), Image.LANCZOS)
    px = small.load()
    hh = small.size[1]
    diffs = []
    for x in range(1, w):
        s = 0
        for y in range(0, hh, 4):
            s += abs(px[x, y] - px[x - 1, y])
        diffs.append(s / (hh / 4))
    lo, hi = int(w * 0.20), int(w * 0.80)
    window = diffs[lo:hi]
    peak = max(window)
    peak_x = window.index(peak) + lo + 1
    mean = sum(diffs) / len(diffs)
    return {"seam_x": peak_x, "centre": w // 2, "off_by_pct": (peak_x - w / 2) / w * 100,
            "strength": peak / mean if mean else 0}


def label(im: Image.Image, lab: dict) -> Image.Image:
    im = im.convert("RGB")
    W, H = im.size
    out = im.copy()
    d = ImageDraw.Draw(out, "RGBA")

    # 1. the divider, at exactly half, whatever the engine did
    rule = max(2, round(W * 0.0018))
    d.rectangle([W // 2 - rule // 2, 0, W // 2 + rule // 2, H], fill=BONE + (235,))

    # 2. BEFORE / AFTER pills, one per half
    pill_px = round(H * PILL_PT)
    pad_x, pad_y = round(W * 0.018), round(H * 0.011)
    margin = round(W * 0.030)
    half_max = W // 2 - margin * 2 - pad_x * 2
    for text, half in ((lab["left"], 0), (lab["right"], 1)):
        f, track = fit_pill(d, text, pill_px, half_max, TRACK)
        tw = tracked_width(d, text, f, track)
        th = f.getbbox("H")[3] - f.getbbox("H")[1]
        x0 = margin + half * (W // 2) + (rule if half else 0)
        y0 = margin
        d.rectangle([x0, y0, x0 + tw + pad_x * 2, y0 + th + pad_y * 2],
                    fill=GRAPHITE + (210,))
        draw_tracked(d, (x0 + pad_x, y0 + pad_y - f.getbbox("H")[1]), text, f, BONE, track)

    # 3. the bottom scrim — a local scrim, never a flatter overlay across the whole frame
    band = round(H * BAND_H)
    top = H - band
    for i in range(band):
        a = int(238 * min(1.0, (i / (band * 0.38))))
        d.rectangle([0, top + i, W, top + i + 1], fill=GRAPHITE + (a,))

    # 4. figure left, qualifier right — the citation stays in the block's body copy,
    #    directly beside the image, rather than being set too small to read here.
    fig_f = font("fraunces-light.ttf", round(H * FIG_PT))
    mea_f = font("muli-regular.ttf", round(H * MEASURE_PT))
    fx, fy = margin, top + round(band * 0.30)
    d.text((fx, fy), lab["figure"], font=fig_f, fill=(255, 255, 255))
    fig_w = d.textlength(lab["figure"], font=fig_f)

    tx = fx + fig_w + round(W * 0.028)
    words, lines, cur = lab["measure"].split(), [], ""
    avail = W - tx - margin
    for word in words:
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=mea_f) <= avail:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    lines.append(cur)
    lh = round(H * MEASURE_PT * 1.42)
    ty = fy + round(H * FIG_PT * 0.30) - (len(lines) - 1) * lh // 2
    for ln in lines:
        d.text((tx, ty), ln, font=mea_f, fill=PEARL)
        ty += lh
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    ap.add_argument("--only", help="one slot id")
    ap.add_argument("--report", action="store_true",
                    help="measure each engine's own seam and stop")
    args = ap.parse_args()

    cfg = json.loads((ROOT / args.config).read_text())
    wave = cfg["wave"]
    base = next(p for p in (ROOT / "assets" / "ai-generated").iterdir()
                if p.name.endswith(wave))

    for slot in cfg["slots"]:
        if args.only and slot["id"] != args.only:
            continue
        folder = base / slot["id"]
        if not folder.exists():
            print(f"  {slot['id']}: no output folder yet")
            continue
        cands = sorted(p for p in folder.glob("*.png") if not p.name.startswith("."))
        print(f"\n{slot['id']}  ({len(cands)} candidates)")
        out_dir = folder / "labelled"
        for p in cands:
            im = Image.open(p)
            s = seam_offset(im)
            flag = "" if abs(s["off_by_pct"]) <= 1.5 and s["strength"] >= 3 else "   <-- CHECK"
            print(f"  {p.stem.split('-')[-1]:14} seam {s['off_by_pct']:+5.1f}% "
                  f"off centre, strength {s['strength']:4.1f}x{flag}")
            if args.report:
                continue
            out_dir.mkdir(exist_ok=True)
            label(im, slot["label"]).save(out_dir / (p.stem + "-labelled.png"))
        if not args.report:
            print(f"  -> {out_dir}")


if __name__ == "__main__":
    main()
