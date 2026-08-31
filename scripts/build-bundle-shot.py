#!/usr/bin/env python3
"""Compose a 3-up or 6-up bundle shot: units staggered back in a V.

    python3 scripts/extract-product-sprite.py --all          # sprites first
    python3 scripts/build-bundle-shot.py --all --sheet

    python3 scripts/build-bundle-shot.py \
        --product copper-peptide-repair-serum --count 3 --layout apex

Product pages need "buy 3" and "buy 6" bundle imagery for every product. This
draws them from the sprite cut by `extract-product-sprite.py`, which comes in
turn from the authoritative Drive master.

WHY THIS IS COMPOSITED AND NOT GENERATED. The house rule is that every website
image goes to every supplier (BRAND-003), and that rule is right for scenes -
engines fail in non-overlapping ways and Malcolm picks the winner. A bundle is
not a scene. It is the SAME product drawn three or six times, and the units sit
side by side where any difference between them is immediately visible. Six units
means six independent chances for an engine to garble the label, and this project
has already lost rounds to exactly that: PDRN set as PORN, GHK-CU set as GHB-CU, a
helix drawn wrong on a frame whose spelling was perfect. Compositing from the
master gives units that are identical by construction and carry the real artwork,
and it makes the geometry a parameter rather than a wish in a prompt - which is
what makes this a template that can be re-run for the other seven products.

An engine still has a job here if a bundle is ever wanted in a SCENE - on stone,
in a bathroom, held. That is a separate brief and should go to every supplier.

THE V. A symmetric V built around a single front unit holds 1 + 2A units, so it
can be 3, 5 or 7 - never 6. The two counts therefore use different figures, and
both are offered as variants rather than guessed at:

    apex     1 front, then a pair per depth step        3, 5, 7
    chevron  no front unit; two arms meeting at centre  2, 4, 6
    wedge    rows of 1, 2, 3 - a filled triangle        6

Depth is bought four ways at once, because any one of them alone reads as a flat
sticker: units get smaller, sit higher up the frame, spread wider apart, and are
drawn back-to-front so the near units occlude the far ones. Haze and blur are
deliberately tiny - the label has to survive at render size, and this project has
a standing rule against judging these only on a contact sheet.

Author: Claude Code, 2026-08-31.
"""
import argparse
import json
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
SPRITES = ROOT / "assets/images/_sprites"
OUT_DIR = ROOT / "assets/ai-generated/2026-08-31-bundle-prototype"
WEB_DIR = ROOT / "assets/publish-ready/product-bundles"
PLAN = ROOT / "configs/banners/product-bundle-images-2026-08-31-rollout.json"

CANVAS = 2048

#: Long edge of the file that actually gets uploaded. NOT 3000 like every other
#: image on this site, and the difference is the point.
#:
#: `upload-theme-images.py` caps at 3000 because that is the widest the THEME's
#: srcset ever asks for. These do not go through the theme. Pumper Bundles prints
#: the bare Shopify CDN URL with no `&width=` and no srcset, so whatever is
#: uploaded is what every visitor downloads, at full size, for a thumbnail the app
#: renders at 64 CSS px (`imageSize: [64, 64, 64]` in its offer config).
#:
#: Measured off this store's CDN on 2026-08-31, the file live in that slot today:
#:     1021px PNG -> 1,058.5K raw to any client that does not send Accept: webp,
#:                      35.0K WebP to one that does
#: and the same picture re-rendered, WebP at q80 as the CDN proxy:
#:     192px -> 4.2K   256px -> 6.4K   384px -> 11.9K
#:     512px -> 17.6K  768px -> 31.1K  2048px -> 102.0K
#:
#: 64 CSS px needs 192px on a 3x display. 512 is chosen over 192 for headroom -
#: it still covers 3x if the slot is ever doubled to 128 - and it halves what the
#: slot delivers today. Uploading the 2048px render instead would have tripled it.
WEB_EDGE = 512

#: Sprite key -> live Shopify product handle. They differ, and not by accident:
#: the Drive master is named for the artwork ("Copper Peptide Repair Serum", whose
#: label reads ADVANCED REPAIR SERUM) while the store sells it as "Copper Peptide
#: (GHK-Cu) 2% Renewal Serum". The existing product media carries the same
#: mismatch, so the filenames here follow the STORE, which is what a shopper
#: searches and what the product page ranks for.
SHOPIFY_HANDLE = {
    "copper-peptide-repair-serum": "copper-peptide-ghk-cu-renewal-serum",
    "copper-peptide-day-repair-cream": "copper-peptide-ghk-cu-day-gel-cream",
    "copper-peptide-night-repair-cream": "copper-peptide-ghk-cu-night-cream",
    "glutathione-brightening-serum": "glutathione-brightening-serum",
    "matrixyl-3000-pro-collagen-serum": "matrixyl-3000-firming-serum",
    "matrixyl-3000-pro-collagen-cream": "matrixyl-3000-pro-collagen-firming-cream",
    "pdrn-skin-repair-serum": "pdrn-renewal-serum",
    "pdrn-collagen-repair-cream": "pdrn-collagen-night-cream",
}
UNIT_NOUN = {"bottle": "bottle", "jar": "jar"}

#: Store title and pack size, for alt text. Written out rather than derived from
#: the filename: alt text is read aloud by a screen reader and indexed by an image
#: search, and neither is served by "copper-peptide-ghk-cu-renewal-serum-3-bottle".
#: The volume comes off the label in the render (30ML on the bottle, 50ML on the
#: jar), so the alt text and the picture agree.
#: The title is the STORE's, the volume is the LABEL's, and on several products
#: those two describe the same thing differently - the store sells a "2% Renewal
#: Serum" whose bottle reads ADVANCED REPAIR SERUM, and a "Collagen Night Cream"
#: whose jar reads PDRN COLLAGEN REPAIR. That mismatch is pre-existing and runs
#: through the whole range; it is not resolved here, but a shopper searches the
#: store's words, so those are what the alt text carries.
PRODUCT_ALT = {
    "copper-peptide-repair-serum": ("Copper Peptide (GHK-Cu) 2% Renewal Serum", "30ml"),
    "copper-peptide-day-repair-cream": ("Copper Peptide (GHK-Cu) 2% Day Gel-Cream", "50ml"),
    "copper-peptide-night-repair-cream": ("Copper Peptide (GHK-Cu) 2% Night Cream", "50ml"),
    "glutathione-brightening-serum": ("Glutathione 2% Brightening Serum", "30ml"),
    "matrixyl-3000-pro-collagen-serum": ("Matrixyl 3000 Firming Serum", "30ml"),
    "matrixyl-3000-pro-collagen-cream": ("Matrixyl 3000 Pro-Collagen Firming Cream", "50ml"),
    "pdrn-skin-repair-serum": ("PDRN 1% Renewal Serum", "30ml"),
    "pdrn-collagen-repair-cream": ("PDRN 1% Collagen Night Cream", "50ml"),
}
COUNT_WORD = {1: "a single", 3: "three", 6: "six"}

#: Per product-shape tuning. A tall narrow bottle can overlap much harder than a
#: squat wide jar before the rear unit stops reading as a separate object, so the
#: lateral step is expressed as a fraction of the unit's OWN width rather than as
#: a pixel figure - that is what lets the same layout serve both templates and,
#: later, the other seven products.
#:
#: Malcolm, 2026-08-31: stagger the units back more vertically than horizontally,
#: so the height carries its share of the arrangement. Both pairs below were
#: picked off a four-point sweep rendered and compared side by side, not reasoned
#: about. The binding constraint is that RISE BUYS DEPTH ONLY WHILE THE UNITS
#: STILL OVERLAP: past that the rear pair floats clear and reads as higher rather
#: than further back, which is a different picture, not a subtler one. A bottle is
#: 2.5x taller than it is wide and can spend far more rise before it hits that
#: wall than a jar, which is why the two shapes end up at very different figures
#: for what is the same instruction.
SHAPES = {
    "bottle": {
        "step_ratio": 0.46,  # lateral step, in front-unit widths
        "rise_ratio": 0.24,  # lift per depth step, in front-unit heights
        "front_gap": 1.06,  # centre-to-centre of the front pair, in unit widths
        "apex_step": 0.46,  # spacing BEYOND the second row, for a 5-up or 7-up
        # Widened twice on request. The ceiling is ~2.1: past that the front
        # bottle stops overlapping the rear pair at all and the trio reads as
        # three separate bottles rather than one group. At 1.80 that overlap is
        # still +88px. Costs no unit size - see the note on FIT_W/FIT_H below.
        "rear_gap": 1.80,  # centre-to-centre of the 3-up's second row, in THEIR widths
    },
    "jar": {
        # A jar is ~1.2x wider than tall, so the same 0.60 step buries the rear
        # units almost completely - but a wider step also spends the frame far
        # faster, which is why unit size is solved for rather than set (see
        # `build`). The rise is proportionally larger because a squat object needs
        # more vertical separation before it reads as standing further back.
        # 0.74 was tried first and left the six-up filling 85% of the frame's
        # width against 20% of its height - a letterbox of product in a square
        # gallery tile. A squat object has to overlap harder AND climb further to
        # use a square frame, so both figures move together. A rise of 0.42 then
        # overshot in the other direction: a jar is only 0.83 as tall as it is
        # wide, so at two steps back the outer pair cleared its neighbours
        # entirely and the occlusion cue vanished with the overlap - six jars in a
        # row at different heights, not a V receding.
        "step_ratio": 0.28,
        "rise_ratio": 0.90,
        "front_gap": 1.04,
        "apex_step": 0.37,
        "rear_gap": 1.16,
    },
}

#: Fraction of the frame the arrangement is allowed to fill, and the ratio it is
#: fitted into. Both counts of both products are fitted to the SAME box, so a 3-up
#: and a 6-up of the same product sit at the same optical weight in a gallery
#: strip - the units get smaller as the count grows, the group does not.
FIT_W, FIT_H = 0.90, 0.80

#: (lateral, depth) per unit, front unit first. Lateral is in step units and may
#: be a half-step, which is what lets the chevron sit symmetrically about the
#: centre line without a unit actually standing on it. Depth is the step index.
LAYOUTS = {
    # Pumper's quantity breaks are 1 / 3 / 6, so the set needs a one-up too. Built
    # from the same sprite on the same sweep rather than reusing an existing hero
    # shot, so all three tiers sit at one scale under one light.
    ("single", 1): [(0.0, 0)],
    ("apex", 3): [(0.0, 0), (-1.0, 1), (1.0, 1)],
    ("apex", 5): [(0.0, 0), (-1.0, 1), (1.0, 1), (-2.0, 2), (2.0, 2)],
    ("chevron", 6): [
        (-0.5, 0), (0.5, 0),
        (-1.5, 1), (1.5, 1),
        (-2.5, 2), (2.5, 2),
    ],
    ("wedge", 6): [
        (0.0, 0),
        (-1.0, 1), (1.0, 1),
        (-2.0, 2), (0.0, 2), (2.0, 2),
    ],
}

DEPTH_SCALE = 0.885  # each step back is this much of the step in front of it


def place(units, cfg):
    """Resolve each (lateral, depth) to an offset in front-unit widths.

    The front pair's separation is its OWN figure and not a multiple of the arm
    step. Malcolm, 2026-08-31: both front units fully in view. They sat at half a
    step from centre, and a step is 0.46 of a unit width for a bottle and 0.37 for
    a jar, so the pair overlapped by more than half its own width and the left one
    was largely hidden behind the right. Widening the step to separate them would
    have thrown the arms apart at the same time, because one number was doing two
    jobs. `front_gap` is centre-to-centre in unit widths, so anything above 1.0
    leaves daylight between them.

    The apex layouts size their second row on `rear_gap` for the same reason, and
    it is the same fault a third time: that pair's separation was a multiple of
    the arm step, so it could not be set. It came out at +3.5% of a unit width on
    the bottle - a hair of daylight - and at MINUS 15% on the jar, where the two
    rear jars overlapped each other behind the front one. `rear_gap` is
    centre-to-centre as a multiple of the rear units' OWN width, so it is read
    directly as the daylight between them and does not drift when the depth scale
    changes. `apex_step` now only spaces rows beyond the second, which a 5-up or
    7-up would use.
    """
    apex = any(abs(l) < 1e-9 for l, _ in units)
    out = []
    for lateral, depth in units:
        if abs(lateral) < 1e-9:
            off = 0.0
        elif apex:
            half = cfg["rear_gap"] / 2 * DEPTH_SCALE
            off = (1 if lateral > 0 else -1) * (
                half + (abs(lateral) - 1) * cfg["apex_step"]
            )
        else:
            arm = (abs(lateral) - 0.5) * cfg["step_ratio"]
            off = (1 if lateral > 0 else -1) * (cfg["front_gap"] / 2 + arm)
        out.append((off, depth))
    return out


def rise_at(depth, rise_ratio):
    """Cumulative lift at `depth`, in front-unit heights.

    Steps of equal size on the ground plane do NOT project to equal steps up the
    frame - they compress as they recede. Adding the same lift per step made the
    fault above worse at every extra depth, because the error accumulates: the
    three-up looked right at one step back while the six-up came apart at two.
    Each step is therefore scaled by the same factor the units are.
    """
    return rise_ratio * sum(DEPTH_SCALE**k for k in range(1, depth + 1))
DEPTH_HAZE = 0.06  # ground colour mixed into each step back
DEPTH_BLUR = 0.55  # px of blur per step back, at 2048
REFLECT_HEIGHT = 0.10  # mirror length, as a fraction of the unit's height
REFLECT_ALPHA = 0.20


def ground(size):
    """A soft studio sweep: white at the top easing to a warm-neutral at the foot.

    Matched to the serum master's own ground (RGB 228 at the crown, 247 in the
    middle, 236 at the foot) rather than invented, so a bundle shot sits in the
    same gallery as the single-product shots without looking relit. Kept off pure
    white so the frosted glass and the silver lid both keep an edge against it.
    """
    img = Image.new("RGB", (size, size), (255, 255, 255))
    d = ImageDraw.Draw(img)
    top, bottom = (253, 253, 252), (232, 232, 229)
    for y in range(size):
        t = y / (size - 1)
        t = t * t  # hold the sweep bright through the top half, fall away low
        d.line(
            [(0, y), (size, y)],
            fill=tuple(round(a + (b - a) * t) for a, b in zip(top, bottom)),
        )
    return img


def shadow(canvas, cx, foot_y, width, depth, opacity):
    """Lay a soft contact shadow under one unit.

    Drawn on its own layer and blurred, then composited - a shadow drawn straight
    onto the sweep cannot be blurred without smearing the sweep with it.
    """
    layer = Image.new("L", canvas.size, 0)
    d = ImageDraw.Draw(layer)
    rx, ry = width * 0.62, width * 0.085
    d.ellipse(
        [cx - rx, foot_y - ry, cx + rx, foot_y + ry],
        fill=int(255 * opacity),
    )
    layer = layer.filter(ImageFilter.GaussianBlur(width * (0.05 + 0.02 * depth)))
    canvas.paste(Image.new("RGB", canvas.size, (168, 170, 172)), (0, 0), layer)


def reflect(sprite, height):
    """A short, fading mirror of the unit, for the surface it stands on.

    Deliberately weak and short. The first pass ran it at 30% over 16% of the
    unit's height with a linear fade, and the result was legible mirrored type -
    "2% GHK-CU | 30ML" readable upside down under every bottle. A reflection that
    can be read is not a reflection, it is a second copy of the label, and on a
    six-up it appears six times. The squared falloff kills it within a third of
    its length, so what survives is the bright base of the glass and nothing that
    resolves as text.
    """
    m = sprite.transpose(Image.FLIP_TOP_BOTTOM).crop((0, 0, sprite.width, height))
    fade = Image.new("L", (sprite.width, height))
    d = ImageDraw.Draw(fade)
    for y in range(height):
        t = y / max(height - 1, 1)
        d.line([(0, y), (sprite.width, y)], fill=int(255 * REFLECT_ALPHA * (1 - t) ** 2))
    m.putalpha(ImageChops.multiply(m.getchannel("A"), fade))
    return m


def recede(sprite, depth):
    """Push a unit back: mix it toward the ground and soften it a touch.

    Both amounts are small on purpose. The label on the rearmost unit still has to
    be readable at the size the page actually renders, so this buys depth mostly
    through scale, height and overlap, and only trims the last few percent here.
    """
    if depth == 0:
        return sprite
    rgb = sprite.convert("RGB")
    haze = Image.new("RGB", sprite.size, (236, 236, 233))
    rgb = Image.blend(rgb, haze, min(DEPTH_HAZE * depth, 0.22))
    out = rgb.convert("RGBA")
    out.putalpha(sprite.getchannel("A"))
    if DEPTH_BLUR * depth >= 0.4:
        out = out.filter(ImageFilter.GaussianBlur(DEPTH_BLUR * depth))
    return out


def solve_fit(sprite, cfg, units, size):
    """Return (front_w, front_h, step, base_y) that fit the whole group in frame.

    The unit size is DERIVED from the arrangement, never set first. Setting it
    first is what put four of the six jars off the canvas: a jar is 1.2x wider
    than tall, the chevron's outermost units stand 2.5 lateral steps from centre,
    and at a 0.74 step that is 3635px of arrangement inside a 2048px frame. The
    same figures are harmless for a bottle, so the fault only shows on one of the
    two templates - which is exactly the kind of thing that ships.

    So: lay the group out once with a front unit one pixel wide, measure the box
    it wants, and scale so that box lands inside the frame.
    """
    aspect = sprite.height / sprite.width
    xs, ys = [], []
    for cx, depth in place(units, cfg):
        scale = DEPTH_SCALE**depth
        w, h = scale, scale * aspect  # in front-unit widths
        foot = -rise_at(depth, cfg["rise_ratio"]) * aspect
        xs += [cx - w / 2, cx + w / 2]
        ys += [foot - h, foot]

    span_w, span_h = max(xs) - min(xs), max(ys) - min(ys)
    front_w = min(size * FIT_W / span_w, size * FIT_H / span_h)
    front_h = front_w * aspect

    # Centre the measured box in the frame, then hand back the baseline that puts
    # it there. Doing this by measurement rather than by a fixed baseline is what
    # keeps a 3-up and a 6-up optically centred as the group changes shape.
    top = (size - span_h * front_w) / 2
    base_y = top - min(ys) * front_w
    centre_x = size / 2 - (max(xs) + min(xs)) / 2 * front_w
    return front_w, front_h, base_y, centre_x


def build(sprite, shape, layout, count, size=CANVAS):
    cfg = SHAPES[shape]
    units = LAYOUTS[(layout, count)]
    canvas = ground(size)
    front_w, front_h, base_y, centre_x = solve_fit(sprite, cfg, units, size)

    # Back to front, so near units occlude far ones. Ties broken by |lateral| so
    # that within one depth step the outer units go down first.
    for offset, depth in sorted(place(units, cfg), key=lambda u: (-u[1], -abs(u[0]))):
        scale = DEPTH_SCALE**depth
        w = max(int(round(front_w * scale)), 1)
        h = max(int(round(front_h * scale)), 1)
        unit = recede(sprite.resize((w, h), Image.LANCZOS), depth)

        cx = centre_x + offset * front_w
        foot = base_y - rise_at(depth, cfg["rise_ratio"]) * front_h
        x, y = int(round(cx - w / 2)), int(round(foot - h))

        shadow(canvas, cx, foot, w, depth, 0.42 - 0.07 * depth)
        refl = reflect(unit, int(h * REFLECT_HEIGHT))
        canvas.paste(refl, (x, int(round(foot))), refl)
        canvas.paste(unit, (x, y), unit)

    return canvas


def seo_name(key, count, kind):
    """Filename a shopper's search would match, per .claude/rules/website-imagery.md.

    Brand first, then the product as the STORE names it, then what the picture
    shows. The pack size is the whole point of the image, so it stays a numeral -
    "3-bottle-bundle" is what gets typed into a search box, and `check_seo_name`
    knows not to flag a digit that is naming a pack size.
    """
    handle = SHOPIFY_HANDLE.get(key, key)
    noun = UNIT_NOUN[kind]
    tail = f"single-{noun}" if count == 1 else f"{count}-{noun}-bundle"
    return f"skingenetix-{handle}-{tail}.jpg"


def export_web(made, manifest):
    """Write the upload-sized copies and the publish plan next to them."""
    WEB_DIR.mkdir(parents=True, exist_ok=True)
    images = []
    for path, key, count in made:
        kind = manifest[key]["kind"]
        name = seo_name(key, count, kind)
        dest = WEB_DIR / name
        im = Image.open(path).convert("RGB")
        im = im.resize((WEB_EDGE, WEB_EDGE), Image.LANCZOS)
        # Saved without an exif= argument, so no metadata reaches a visitor. 4:4:4
        # for the same reason upload-theme-images.py uses it: the CDN's WebP pass
        # keeps colour detail that chroma subsampling would already have thrown out.
        im.save(dest, "JPEG", quality=95, optimize=True, progressive=True,
                subsampling="4:4:4")
        title, volume = PRODUCT_ALT[key]
        noun = UNIT_NOUN[kind] + ("" if count == 1 else "s")
        images.append({
            # `source` and `filename` are the keys upload-theme-images.py reads.
            "slot": f"{SHOPIFY_HANDLE.get(key, key)}-qty-{count}",
            "source": str(dest.relative_to(ROOT)),
            "filename": name,
            "alt": f"Skingenetix {title}, {COUNT_WORD[count]} {volume} {noun}",
            "pumper_quantity": count,
        })
        print(f"  {name}  {WEB_EDGE}x{WEB_EDGE}  {dest.stat().st_size/1024:.0f}K")

    plan = {
        "wave": "product-bundle-images-2026-08-31",
        "created": "2026-08-31",
        "note": (
            "Pumper Bundles quantity-break thumbnails, 1 / 3 / 6, for the copper "
            "peptide serum and day gel-cream. Rendered by scripts/build-bundle-shot.py "
            f"at 2048px and exported here at {WEB_EDGE}px because Pumper prints the bare "
            "CDN URL with no srcset and no &width=, so the uploaded file is what every "
            "visitor downloads for a slot the app renders at 64 CSS px. See WEB_EDGE in "
            "that script for the measured figures. Upload only - these are NOT wired to "
            "the offer, which is a Pumper-side change (see docs/todo.md BUNDLE-001)."
        ),
        "images": images,
    }
    PLAN.parent.mkdir(parents=True, exist_ok=True)
    PLAN.write_text(json.dumps(plan, indent=2) + "\n")
    print(f"\nplan -> {PLAN.relative_to(ROOT)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--product")
    ap.add_argument("--count", type=int, default=3)
    ap.add_argument("--layout", default="apex")
    ap.add_argument("--all", action="store_true", help="every prototype variant")
    ap.add_argument("--sheet", action="store_true", help="contact sheet + open")
    ap.add_argument("--web", action="store_true",
                    help=f"also write {WEB_EDGE}px SEO-named copies + an upload plan")
    args = ap.parse_args()

    manifest = json.loads((SPRITES / "sprites.json").read_text())
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    tiers = ((1, "single"), (3, "apex"), (6, "chevron"))
    if args.all:
        jobs = [(k, c, lay) for k in manifest for c, lay in tiers]
    else:
        if not args.product:
            sys.exit("give --product <key> or --all")
        jobs = [(args.product, args.count, args.layout)]

    made = []
    for key, count, layout in jobs:
        if (layout, count) not in LAYOUTS:
            sys.exit(f"no layout {layout!r} for {count} units")
        sprite = Image.open(SPRITES / f"{key}.png").convert("RGBA")
        img = build(sprite, manifest[key]["kind"], layout, count)
        dest = OUT_DIR / f"{key}_bundle-{count}_{layout}.jpg"
        img.save(dest, quality=94, subsampling=0)
        made.append((dest, key, count))
        print(f"{dest.name}  {img.size[0]}x{img.size[1]}")

    if args.web:
        print(f"\nweb deliverables at {WEB_EDGE}px:")
        export_web(made, manifest)
    if args.sheet:
        contact_sheet([p for p, _, _ in made])


def contact_sheet(paths, tile=560):
    """Tile the results and open them, per the standing rule about showing work."""
    cols = min(3, len(paths))
    rows = (len(paths) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tile, rows * (tile + 26)), (24, 24, 24))
    d = ImageDraw.Draw(sheet)
    for i, p in enumerate(paths):
        im = Image.open(p).resize((tile, tile), Image.LANCZOS)
        x, y = (i % cols) * tile, (i // cols) * (tile + 26)
        sheet.paste(im, (x, y))
        d.text((x + 8, y + tile + 6), p.stem, fill=(235, 235, 235))
    dest = Path.home() / "Desktop/skingenetix-renders.png"
    sheet.save(dest)
    print(f"contact sheet -> {dest}")


if __name__ == "__main__":
    main()
