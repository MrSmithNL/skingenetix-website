#!/usr/bin/env python3
"""Emit the round-4 Copper Peptide SET brief — ten HERO pack shots on pure white.

    python3 scripts/build-copper-peptide-hero-white-batch4.py
    set -a; source ~/.claude/config/image-credentials.env; set +a
    python3 scripts/generate-multi.py configs/banners/copper-peptide-hero-white-batch4-2026-09-11.json

Malcolm, 2026-09-11: "we also need a batch of the main hero image - with just white
background."

This is the primary product-gallery image, so it is the most constrained brief of the four
waves and the one with the least room for taste. The background is not a scene; it is an
absence. Round 1's `set-b-clinical-white` was the nearest thing to this and it was still a
studio SCENE - a white-to-pale-grey sweep with a surface the products sat on. Here the white
is pure and uniform and there is nothing else in the picture at all.

WHAT ACTUALLY VARIES BETWEEN HERO SHOTS IS ARRANGEMENT AND SHADOW, so that is what these ten
vary. Everything else is deliberately held constant. The shadow treatments run from a hard
shadowless cut-out, through soft contact shadows and a gloss reflection, to a single long
directional shadow - because that choice, more than anything else, decides whether the image
reads as a marketplace listing, a catalogue page or a brand campaign, and it is not a decision
to make on his behalf.

THE SHADOWLESS SLOT IS THE ONE THAT MOST NEEDS SAYING OUT LOUD. Every engine's default for a
product on white is to ground it with a shadow. `b4-e` asks for none at all, which is the
classic marketplace hero and the hardest thing on this list to get, so it states the absence
three ways: no shadow, no reflection, no contact point.

NOTHING IS CROPPED and nothing touches the frame - `negative_global` bars both, and a hero
that bleeds off the edge cannot be dropped into a square gallery slot next to eight others.

The wave negative bars every way a background stops being pure white: a tone, a gradient, a
texture, a horizon, a vignette. It does NOT bar shadows, because six of these ten want one.

The product spec is imported from `copper_peptide_set_spec`, not restated.

Author: Claude Code, 2026-09-11.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from copper_peptide_set_spec import (  # noqa: E402
    NEGATIVE, REF_FILES, build_slot,
)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "configs" / "banners" / "copper-peptide-hero-white-batch4-2026-09-11.json"

OPENING = ("A clean commercial hero pack shot of THREE DIFFERENT Skingenetix Copper Peptide "
           "products presented together as a set on a pure white background.")

#: Held constant across all ten so the only variables are arrangement and shadow.
WHITE = ("SCENE. The background is PURE WHITE, uniform and seamless, edge to edge - the same "
         "white in every corner, with no tone, no tint, no gradient, no texture, no vignette, "
         "no horizon line and no visible surface or backdrop seam anywhere. There is nothing "
         "in the picture but the three products. The light is cool and neutral so the white "
         "stays white and the frosted glass keeps its blue without any warm cast.")

#: (id, ARRANGEMENT, FRAME). SCENE is WHITE for every slot; shadow treatment lives in
#: ARRANGEMENT because it is part of how the group sits, not part of the background.
COMPOSITIONS = [
    (
        "b4-a-row-contact-shadow",
        "ARRANGEMENT. The three stand in a single straight row on one shared baseline, evenly spaced with a clear gap of white between each, the serum bottle at the centre and a jar either side. Each container carries a SOFT SHORT CONTACT SHADOW directly beneath it, just enough to sit it on the ground, with no shadow reaching across to the next. All three front labels face the camera square on and stay fully legible.",
        "FRAME. Camera straight on at the height of the labels. All three products are fully inside the frame with generous white margin above, below and to both sides; nothing is cut by any edge and nothing touches the frame. Square format. Sharp focus across all three front labels, every line legible.",
    ),
    (
        "b4-b-pyramid-silhouette",
        "ARRANGEMENT. The three form a clear triangle: the serum bottle at the centre, naturally the tallest, with the day jar and the night jar sitting either side of it and slightly forward so their lids fall well below the bottle's shoulder. The outline of the group rises to a single point at the bottle's pipette. A soft contact shadow sits under each container. All three front labels face the camera and stay fully legible.",
        "FRAME. Camera straight on at the height of the jar labels. All three products are fully inside the frame with clear white margin above the pipette and to both sides; nothing is cut by any edge. Square format. Sharp focus across all three front labels, every line legible.",
    ),
    (
        "b4-c-overlapping-three-quarter",
        "ARRANGEMENT. A tight group seen at a gentle three-quarter angle: the day jar nearest the camera at the left with its front label square to the lens, the serum bottle rising immediately behind and between, the night jar at the right and partly overlapped by the bottle. The three silhouettes touch and overlap rather than standing apart. One soft shadow pools beneath the whole group. All three front labels stay fully legible.",
        "FRAME. Camera slightly off-axis and at the height of the jar shoulders. The group sits a little left of centre with more white to the right. All three products are fully inside the frame; nothing is cut by any edge. Square format. Sharp focus across all three front labels, every line legible.",
    ),
    (
        "b4-d-staggered-depth",
        "ARRANGEMENT. The three are staggered in depth rather than in a line: the day jar nearest the camera at the left, the serum bottle a clear step further back at the centre, the night jar a further step back at the right. Each sits slightly higher in the frame than the one in front of it, as receding objects do. A soft shadow falls beneath each, smaller and fainter the further back it stands. All three front labels face the camera and stay fully legible.",
        "FRAME. Camera straight on and a little above the group so the depth reads. All three products are fully inside the frame with clear white margin all round; nothing is cut by any edge. Square format. Sharp focus across all three front labels, every line legible.",
    ),
    (
        "b4-e-floating-shadowless",
        "ARRANGEMENT. The three are presented in a straight row, evenly spaced, with ABSOLUTELY NO SHADOW OF ANY KIND. There is no contact shadow, no cast shadow, no reflection and no visible point where any container meets a surface - each simply sits against the white with clean crisp edges, the way a cut-out product listing image looks. The lighting is flat, even and shadowless from the front, with just enough soft modelling on the glass to show its curve. All three front labels face the camera square on and stay fully legible.",
        "FRAME. Camera straight on at the height of the labels. All three products are fully inside the frame with generous even white margin on every side; nothing is cut by any edge. Square format. Sharp focus across all three front labels, every line legible.",
    ),
    (
        "b4-f-gloss-reflection",
        "ARRANGEMENT. The three stand in a row on a glossy white surface that throws a soft vertical reflection of each container downward beneath it, fading out cleanly within about a third of the container's own height. The surface itself is the same pure white as the background, visible only through the reflection. The serum bottle is at the centre. All three front labels face the camera and stay fully legible.",
        "FRAME. Camera straight on, just above the height of the jar labels. The three products AND their reflections are fully inside the frame with clear white margin all round; nothing is cut by any edge. Square format. Sharp focus across all three front labels, every line legible.",
    ),
    (
        "b4-g-single-long-shadow",
        "ARRANGEMENT. The three stand in a row, close together, lit by one clean directional light from the upper left so that each casts a SINGLE LONG SOFT-EDGED SHADOW away to the lower right across the white. The three shadows run parallel and do not cross the containers themselves. The serum bottle is at the centre. All three front labels face the camera and stay fully legible and open, not lost in shade.",
        "FRAME. Camera straight on at the height of the labels, framed so the full length of all three shadows is visible. All three products and all three shadows are fully inside the frame; nothing is cut by any edge. Square format. Sharp focus across all three front labels, every line legible.",
    ),
    (
        "b4-h-bottle-forward",
        "ARRANGEMENT. The serum bottle stands alone at the front and centre, closest to the camera and clearly the hero. The day jar and the night jar sit behind it and well apart to either side, far enough out that the bottle overlaps neither. The bottle reads slightly larger than the jars because it is nearer. A soft contact shadow sits under each. All three front labels face the camera and stay fully legible.",
        "FRAME. Camera straight on at the height of the bottle's label. All three products are fully inside the frame with clear white margin all round; nothing is cut by any edge. Square format. Sharp focus across all three front labels, every line legible.",
    ),
    (
        "b4-i-airy-wide-spacing",
        "ARRANGEMENT. The three stand in a single row spaced WIDE APART, with a broad band of clean white between each one so the picture reads as spare and unhurried rather than as a stocked shelf. The gap between neighbours is roughly the width of a jar. The serum bottle is at the centre. A soft short contact shadow sits under each. All three front labels face the camera square on and stay fully legible.",
        "FRAME. Camera straight on at the height of the labels, framed wide so the white dominates and the three products occupy a band across the middle. All three are fully inside the frame; nothing is cut by any edge. Square format. Sharp focus across all three front labels, every line legible.",
    ),
    (
        "b4-j-elevated-compact",
        "ARRANGEMENT. A compact group seen from slightly above, close together, the serum bottle at the centre and the two jars either side and a little forward, so the tops of both jar lids are just visible as shallow silver ellipses. A soft shadow pools beneath the group. All three front labels are still turned up towards the camera and stay fully legible.",
        "FRAME. Camera above the group looking gently down, high enough to show the lid tops and low enough that the front labels are not foreshortened into illegibility. All three products are fully inside the frame with clear white margin all round; nothing is cut by any edge. Square format. Sharp focus across all three front labels, every line legible.",
    ),
]

#: Appended to the shared negative for this wave. Every entry is a way a background stops being
#: pure white. Shadows are deliberately NOT barred here - six of the ten want one, and `b4-e`
#: forbids its own shadow in its arrangement text where it belongs.
WHITE_NEGATIVE_EXTRA = (
    "grey background, beige background, cream background, coloured background, tinted "
    "background, gradient background, textured background, patterned background, visible "
    "horizon line, backdrop seam, curved sweep, wall, floor, table, tabletop, stone surface, "
    "fabric, props, decorative objects, vignette, darkened corners, border, frame, drop shadow "
    "on the background edge"
)


def build():
    slots = [
        build_slot(slot_id, OPENING, arrangement, WHITE, frame)
        for slot_id, arrangement, frame in COMPOSITIONS
    ]
    for s in slots:
        s["negative_extra"] = WHITE_NEGATIVE_EXTRA

    cfg = {
        "_comment": (
            "Copper Peptide SET hero pack shots on pure white, round 4, 2026-09-11. GENERATED "
            "by scripts/build-copper-peptide-hero-white-batch4.py; edit the builder, not this "
            "file. Malcolm: 'we also need a batch of the main hero image - with just white "
            "background.' This is the primary product-gallery image. The background is not a "
            "scene, it is an absence - pure uniform white, edge to edge, nothing else in the "
            "picture. What varies across the ten is ARRANGEMENT and SHADOW TREATMENT, because "
            "that pair decides whether a hero reads as a marketplace listing, a catalogue page "
            "or a brand campaign, and that is his call to make. b4-e is the shadowless cut-out "
            "and states the absence three ways, because every engine's default on white is to "
            "ground the product with a shadow. The wave negative bars every way a background "
            "stops being white but deliberately does NOT bar shadows, since six slots want one."
        ),
        "wave": "copper-peptide-hero-white-batch4-2026-09-11",
        "defaults": {"negative_global": NEGATIVE},
        "slots": slots,
    }
    OUT.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")

    print(f"{OUT.relative_to(ROOT)}\n{len(slots)} slots\n")
    for s in slots:
        print(f"  {s['id']:<28} prompt={len(s['prompt']):>5}  luma={len(s['prompt_luma']):>5}")
    missing = [r for r in REF_FILES if not (ROOT / r).exists()]
    if missing:
        raise SystemExit(f"missing reference files: {missing}")
    print(f"\n  {len(REF_FILES)} reference files present")
    print(f"  5 suppliers x 2 candidates x {len(slots)} slots = {len(slots) * 10} candidates")


if __name__ == "__main__":
    build()
