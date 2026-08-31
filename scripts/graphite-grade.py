#!/usr/bin/env python3
"""Put the brand's graphite treatment onto a real photograph, without replacing its background.

    python3 scripts/graphite-grade.py in.png out.jpg
    python3 scripts/graphite-grade.py in.png out.jpg --strength 0.7 --scrim 0.55 0.92
    python3 scripts/graphite-grade.py in.png --ladder ~/Desktop/ladder.png   # compare strengths

WHAT THIS IS FOR. Malcolm, 2026-08-30: "the background should not be a flat graphite coloured
background. it should still be the photo background. But the graphite style used. you can
still use a graphite colour background on the left - but also use overlays and gradients and
opacity to create the graphite effect."

He is describing the live banners accurately, and more accurately than the round-2 briefs did.
`the-science` and `copper-peptide-research` are dark PHOTOGRAPHS with real depth - a bench
with texture, a lab with falloff - not flat colour fills. Briefing "a seamless graphite studio
sweep" produced a literal flat sweep and lost the room, which is a different thing from the
house style even though it lands on the same colour.

So the treatment is applied as a grade over the photograph rather than generated into it. That
also makes it deterministic and repeatable, and it works on the frames Malcolm has already
chosen instead of asking him to choose again.

FOUR STEPS, in order. Each is separable so a fault can be traced to one of them:

  1. desaturate slightly toward luma - the reference banners are near-neutral
  2. darken midtones on a gamma curve that PROTECTS highlights, so lit faces stay lit while
     the room drops away. This is the step that keeps it a photograph.
  3. tint the shadows toward #1A1A1A, weighted by darkness, so the falloff goes graphite
     rather than muddy grey-brown
  4. lay a left-to-right scrim of #1A1A1A on a smoothstep ramp, for the headline

⚠️ THE SCRIM IS LOCAL, AND DELIBERATELY SO. Contrast for type is bought with a local scrim,
never by flattening the whole frame - flattening dims the subject to fix the type, which is
the trade this project has already rejected once. The ramp uses smoothstep rather than a
linear fade because a linear ramp leaves a visible shoulder where it reaches zero, and a
visible edge in a dark banner is the same failure as the hard black band that hit the FAQ
macro.

⚠️ THE SECTION ADDS ITS OWN OVERLAY ON TOP. `image-with-text-overlay` applies
`overlay_opacity` over whatever it is given, and the sibling pages run 22-25. Grade for that,
not for how the file looks on its own, or the delivered banner is darkened twice. Judge the
result at the 440px band height as well as at 100%.

Author: Claude Code, 2026-08-30.
"""
import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

#: The brand graphite. Same value the collection banners, the science hero and the research
#: tile overlay use, so a graded photograph sits in the same family as a generated one.
GRAPHITE = np.array([0x1A, 0x1A, 0x1A], dtype=np.float32) / 255.0

#: Rec.709 luma - used for the desaturate and for weighting the shadow tint.
LUMA = np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)


def smoothstep(t):
    """3t^2 - 2t^3. A linear ramp leaves a visible shoulder where it reaches zero."""
    t = np.clip(t, 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def grade(img: Image.Image, strength=1.0, desat=0.18, gamma=1.55,
          shadow_tint=0.55, scrim_span=0.55, scrim_peak=0.92) -> Image.Image:
    """Apply the graphite treatment. `strength` scales steps 1-3 only; the scrim is its own."""
    a = np.asarray(img.convert("RGB"), dtype=np.float32) / 255.0
    h, w, _ = a.shape

    # 1. desaturate toward luma
    y = (a * LUMA).sum(axis=2, keepdims=True)
    a = a + (y - a) * (desat * strength)

    # 2. darken midtones, protect highlights. Blending the gamma curve back by its own
    #    highlight weight keeps speculars and lit skin from going flat.
    g = np.power(np.clip(a, 0.0, 1.0), 1.0 + (gamma - 1.0) * strength)
    keep_hi = np.clip((y - 0.62) / 0.38, 0.0, 1.0) ** 2      # 0 below 0.62, 1 at white
    a = g + (a - g) * keep_hi

    # 3. tint shadows toward graphite, weighted by darkness
    y2 = (a * LUMA).sum(axis=2, keepdims=True)
    wgt = (1.0 - np.clip(y2, 0.0, 1.0)) ** 2 * (shadow_tint * strength)
    a = a + (GRAPHITE.reshape(1, 1, 3) - a) * wgt

    # 4. left scrim, smoothstep to zero by scrim_span of the width
    x = np.linspace(0.0, 1.0, w, dtype=np.float32).reshape(1, w, 1)
    alpha = smoothstep(1.0 - x / max(scrim_span, 1e-6)) * scrim_peak
    a = a + (GRAPHITE.reshape(1, 1, 3) - a) * alpha

    return Image.fromarray((np.clip(a, 0.0, 1.0) * 255.0 + 0.5).astype(np.uint8))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src", type=Path)
    ap.add_argument("out", type=Path, nargs="?")
    ap.add_argument("--strength", type=float, default=1.0)
    ap.add_argument("--scrim", type=float, nargs=2, default=[0.55, 0.92],
                    metavar=("SPAN", "PEAK"))
    ap.add_argument("--ladder", type=Path,
                    help="write a comparison of several strengths instead of one file")
    args = ap.parse_args()

    im = Image.open(args.src)
    span, peak = args.scrim

    if args.ladder:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 30)
        rows = [("original — no grade", im)]
        for s in (0.45, 0.70, 1.00):
            rows.append((f"strength {s:.2f}   scrim span {span}  peak {peak}",
                         grade(im, strength=s, scrim_span=span, scrim_peak=peak)))
        W = 1500
        rs = [(lab, i.resize((W, int(i.height * W / i.width)), Image.LANCZOS)) for lab, i in rows]
        sheet = Image.new("RGB", (W, sum(i.height + 40 for _, i in rs)), "black")
        d = ImageDraw.Draw(sheet)
        y = 0
        for lab, i in rs:
            d.rectangle([0, y, W, y + 40], fill="#444")
            d.text((10, y + 7), lab, font=font, fill="white")
            sheet.paste(i, (0, y + 40))
            y += i.height + 40
        sheet.save(args.ladder)
        print(f"ladder -> {args.ladder} ({sheet.width}x{sheet.height})")
        return

    if not args.out:
        raise SystemExit("need an output path (or --ladder)")
    out = grade(im, strength=args.strength, scrim_span=span, scrim_peak=peak)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    if args.out.suffix.lower() in (".jpg", ".jpeg"):
        out.save(args.out, quality=95, subsampling=0)
    else:
        out.save(args.out)
    print(f"graded -> {args.out}  ({out.width}x{out.height})")


if __name__ == "__main__":
    main()
