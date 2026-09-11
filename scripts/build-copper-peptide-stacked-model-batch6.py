#!/usr/bin/env python3
"""Emit round 6 — products stacked and piled, plus five more model shots with the two jars.

    python3 scripts/build-copper-peptide-stacked-model-batch6.py
    set -a; source ~/.claude/config/image-credentials.env; set +a
    python3 scripts/generate-multi.py configs/banners/copper-peptide-stacked-model-batch6-2026-09-11.json

Malcolm, 2026-09-11: a new batch where the products are piled or stacked on top of each other -
research it, be creative - and more model shots holding the two cream jars.

TWO FAMILIES IN ONE WAVE
  b6-a .. b6-f   STACKED. Six ways to pile three containers.
  b6-g .. b6-k   MODEL. Five more of her holding both cream jars.
They run as one config so they queue as one job, but the slot ids keep them apart on the
contact sheet.

WHAT THE RESEARCH ACTUALLY SAID, AND WHERE IT STOPS BEING USEFUL
Every practical guide to "gravity-defying" product work is about RIG: fishing line, acrylic
rods, wire, C-stands, and painting the support out afterwards. None of that transfers to a
brief - an engine has no rig to hide. What does transfer is the LOOK each rig is built to
produce, so that is what is briefed: a true balanced tower, a deliberately precarious offset,
a levitating column with clean air between the pieces, a relaxed tumble, and a horizontal
bridge. One guide was explicit that its own advice "emphasises layering and grouping rather
than dramatic stacking" - which is round 2's territory, already shot - so it is not repeated.

THE STACK IS A GEOMETRY PROBLEM AND THE JARS DO NOT HELP.
A jar is about 1.15 times wider than its full height, so two stacked are still WIDER than
tall, and a tower of them reads squat unless the frame is tight. The serum bottle is the only
tall element, which is why it is the top tier or the bridge in most of these. Each slot
therefore states what sits on what, in contact, rather than asking for "a stack" and hoping.

A STACKED LID IS A LOAD-BEARING SURFACE, and that has to be said. Left unstated, engines merge
two jars into one tall vessel or float the upper one with a gap. Every stacking slot below
says the upper jar's BASE rests ON the lower jar's LID, flat and centred and touching.

The label spec, the three-blue separation and the model casting all come from
`copper_peptide_set_spec`. This wave reuses round 5's own negative, which keeps the product and
label bars and drops the bars on set dressing and people.

Author: Claude Code, 2026-09-11.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from copper_peptide_set_spec import (  # noqa: E402
    DAY_JAR, DAY_JAR_S, MODEL, MODEL_S, NIGHT_JAR, NIGHT_JAR_S, REF_FILES, SERUM_BOTTLE,
    SERUM_BOTTLE_S, build_slot,
)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "configs" / "banners" / "copper-peptide-stacked-model-batch6-2026-09-11.json"

BOTH_JARS = [DAY_JAR, NIGHT_JAR]
BOTH_JARS_S = [DAY_JAR_S, NIGHT_JAR_S]
ALL_THREE = [DAY_JAR, SERUM_BOTTLE, NIGHT_JAR]
ALL_THREE_S = [DAY_JAR_S, SERUM_BOTTLE_S, NIGHT_JAR_S]

STACK_PHYSICS = (
    "HOW THE STACK HOLDS UP, which must read as physically true: where one container sits on "
    "another, its FLAT BASE rests directly ON the flat top face of the lid beneath it, the two "
    "in full contact with no gap and no visible support of any kind. The containers stay "
    "separate objects with a clear seam between them - they never merge into one tall vessel, "
    "and the lid of a lower container is never hidden or absorbed into the one above it."
)

OPENING = ("A premium editorial product photograph for Skingenetix Copper Peptide.")

#: (id, ARRANGEMENT, SCENE, FRAME, products, products_short, separation, extra)
COMPOSITIONS = [
    (
        "b6-a-two-jar-tower",
        "ARRANGEMENT. The two jars are STACKED ONE DIRECTLY ON TOP OF THE OTHER into a short tower: the day jar on the bottom, the night jar squarely on top of it, both perfectly centred and axis-aligned, both front labels facing the camera and both fully legible. The serum bottle stands upright on the surface immediately beside the tower, close enough to touch it, its own label facing the camera - it is roughly as tall as the two stacked jars together.",
        "SCENE. A cool mid-grey seamless studio background and a matching matte surface, no horizon line visible. Soft cool key light from the upper left with a broad fill, and a single soft shadow pooling beneath the tower and the bottle. Restrained and cold.",
        "FRAME. Camera straight on at the height of the seam between the two jars. The tower and the bottle are fully inside the frame with clear margin above and to both sides; nothing is cut by any edge. Square format. Sharp focus across all three front labels, every line legible.",
        ALL_THREE, ALL_THREE_S, True, [STACK_PHYSICS],
    ),
    (
        "b6-b-precarious-offset-stack",
        "ARRANGEMENT. The two jars are STACKED, the day jar on the bottom and the night jar on top, but the upper jar is ROTATED about thirty degrees around the vertical axis and pushed slightly off centre, so the tower reads as deliberately, elegantly precarious rather than neatly squared up. Both front labels still face the camera closely enough to be fully legible. The serum bottle stands upright a little apart from the tower, straight and square, its label to the camera - the calm element beside the tilted one.",
        "SCENE. A cool pale-grey seamless background and matching surface. ONE hard directional light from the upper left, so the tower throws a single long crisp-edged shadow away to the lower right and the offset of the top jar reads clearly in that shadow too. Graphic and spare.",
        "FRAME. Camera straight on, slightly below the seam so the tower reads as tall. The tower, the bottle and the full length of the shadow are fully inside the frame; nothing is cut by any edge. Square format. Sharp focus across all three front labels, every line legible.",
        ALL_THREE, ALL_THREE_S, True, [STACK_PHYSICS],
    ),
    (
        "b6-c-three-tier-tower",
        "ARRANGEMENT. All three products form ONE TOWER of three tiers: the day jar on the bottom, the night jar squarely on top of it, and the serum bottle standing upright and centred on top of the night jar's lid, its pipette at the very top. All three are axis-aligned and all three front labels face the camera and stay fully legible. Nothing else is in the picture.",
        "SCENE. A deep cool graphite background falling to near-black at the corners, and a dark matte surface beneath. Cool rim light from behind on both sides draws a bright edge down the flank of every tier, with a soft frontal fill just strong enough to keep all three labels readable. Monumental and quiet.",
        "FRAME. Camera LOW, below the base of the tower, angled slightly UP so the three tiers stack away above the lens. The whole tower from base to pipette is fully inside the frame with clear dark space above it; nothing is cut by any edge. Square format. Sharp focus across all three front labels, every line legible.",
        ALL_THREE, ALL_THREE_S, True, [STACK_PHYSICS],
    ),
    (
        "b6-d-levitating-column",
        "ARRANGEMENT. The three products FLOAT in a vertical column, one above the other with a clear gap of empty air between each - the day jar lowest, the night jar above it, the serum bottle highest - all three level and axis-aligned as though a tower had been gently pulled apart. NOTHING supports them: no rod, no wire, no stand, no hand, no visible join. All three front labels face the camera and stay fully legible.",
        "SCENE. A soft cool pale-grey gradient background, lighter at the centre and falling away at the corners, with no horizon line and no surface. A single soft elliptical shadow lies on the empty ground far below the lowest jar, small and diffuse, so the height reads. Cool even light from the front.",
        "FRAME. Camera straight on at the height of the middle object. All three products and the ground shadow are fully inside the frame with clear margin at top and bottom; nothing is cut by any edge. Square format. Sharp focus across all three front labels, every line legible.",
        ALL_THREE, ALL_THREE_S, True, None,
    ),
    (
        "b6-e-tumbled-pile",
        "ARRANGEMENT. The three are PILED loosely on each other, as if set down in a heap rather than arranged: the day jar lies on its side at the bottom with its front label turned up towards the camera; the night jar rests ON the day jar, tilted at an angle against it and also label-up; the serum bottle lies across them both, its shoulder propped on the night jar and its base on the surface. The pile is relaxed and slightly untidy, nothing is level, and all three front labels are still turned enough to be fully legible.",
        "SCENE. A cool pale-grey matte surface and a soft cool grey background, out of focus. Soft directional light from the upper left, with the shadows between the piled containers left soft rather than crushed. Casual and tactile.",
        "FRAME. Camera above the pile at a three-quarter angle, looking down across it. All three products are fully inside the frame with clear surface visible around the pile; nothing is cut by any edge. Square format. Sharp focus across all three front labels, every line legible.",
        ALL_THREE, ALL_THREE_S, True, None,
    ),
    (
        "b6-f-serum-bridge",
        "ARRANGEMENT. The two jars stand upright and apart, a little further apart than the length of the serum bottle, their front labels facing the camera. The SERUM BOTTLE LIES HORIZONTALLY ACROSS THE TOP OF BOTH, spanning the gap like a lintel, its base resting on the day jar's lid and its shoulder on the night jar's lid, its front label turned up and towards the camera so it stays fully legible. The three together make a simple bridge shape with a clear opening beneath it.",
        "SCENE. A cool mid-grey seamless background and matching matte surface. Even cool light from the front and slightly above, with soft shadows under each jar and a gentle shadow cast into the opening beneath the bridge. Architectural and calm.",
        "FRAME. Camera straight on at the height of the jar lids, level with the span. All three products are fully inside the frame with clear margin above the bridge and to both sides; nothing is cut by any edge. Square format. Sharp focus across all three front labels, every line legible.",
        ALL_THREE, ALL_THREE_S, True, [STACK_PHYSICS],
    ),
    (
        "b6-g-model-jars-together-close",
        "ARRANGEMENT. The model holds BOTH CREAM JARS together in front of her, one in each hand and the two jars almost touching, raised to just below her chin so her face and both jars are in the same picture. Both front labels face the camera square on and stay fully legible - the day jar on the left of frame, the night jar on the right. Her fingers curl around the sides and cover no part of either label. Both jars are closed. She looks straight at the camera.",
        "SCENE. A calm modern bathroom thrown gently out of focus behind her: pale grey textured plaster and a round steel-rimmed mirror. Soft cool daylight from the left, even across her face and both jars.",
        "FRAME. Camera at her chin height, closer than a portrait - she is framed from the shoulders up and the two jars fill the lower third. Both jars and her whole head are fully inside the frame; nothing of either jar is cut by any edge. Both jars and her eyes are sharp. Square format. Every line of both front labels legible.",
        BOTH_JARS, BOTH_JARS_S, False, [MODEL], [MODEL_S],
    ),
    (
        "b6-h-model-one-jar-raised",
        "ARRANGEMENT. The model holds the DAY JAR raised beside her cheek at eye level, close to her face but not touching it, its front label turned square to the camera and fully legible. Her other hand holds the NIGHT JAR lower, at about chest height, also turned label-forward and fully legible. Both jars are closed. She looks towards the camera with a calm, faint smile. Her fingers cover no part of either label.",
        "SCENE. A calm modern bathroom thrown gently out of focus behind her: pale grey textured plaster, a light oak shelf and soft cool daylight from the left.",
        "FRAME. Camera at her eye height, framed from mid-chest up. Her whole head and both jars are fully inside the frame; nothing of either jar is cut by any edge. Her face and both jars are sharp. Square format. Every line of both front labels legible.",
        BOTH_JARS, BOTH_JARS_S, False, [MODEL], [MODEL_S],
    ),
    (
        "b6-i-model-seated-vanity",
        "ARRANGEMENT. The model sits at a vanity, turned slightly towards the camera, holding one cream jar in each hand resting lightly on the counter in front of her - the day jar under her left hand at the left of frame, the night jar under her right at the right of frame. Both jars stand upright with their front labels square to the camera and fully legible, and her fingers rest around them without covering any lettering. Both jars are closed. She looks down at the jars.",
        "SCENE. A pale grey stone vanity top, pale grey textured plaster wall behind, a large frameless mirror at one side reflecting soft light. Cool daylight from the left, calm and even.",
        "FRAME. Camera at counter height and slightly to one side, framed so the counter runs across the lower frame and she fills the upper. Both jars and her head are fully inside the frame; nothing of either jar is cut by any edge. Both jars are sharp and she is very slightly softer. Square format. Every line of both front labels legible.",
        BOTH_JARS, BOTH_JARS_S, False, [MODEL], [MODEL_S],
    ),
    (
        "b6-j-model-three-quarter-presenting",
        "ARRANGEMENT. The model stands turned about thirty degrees away from the camera, her shoulders at a three-quarter angle, but she PRESENTS BOTH CREAM JARS forward towards the lens - one held in each hand at chest height, both turned square to the camera even though her body is not, both front labels fully legible. Both jars are closed. Her face is turned back towards the camera over her leading shoulder, calm and unforced.",
        "SCENE. A calm modern bathroom thrown well out of focus behind her: pale grey textured plaster and a soft bright window at one side. Cool daylight from that window, modelling one side of her face.",
        "FRAME. Camera at her chest height, framed from the waist up. Her whole head and both jars are fully inside the frame; nothing of either jar is cut by any edge. Both jars are sharp. Square format. Every line of both front labels legible.",
        BOTH_JARS, BOTH_JARS_S, False, [MODEL], [MODEL_S],
    ),
    (
        "b6-k-model-cupped-in-two-hands",
        "ARRANGEMENT. The model holds BOTH CREAM JARS cradled together in her two cupped hands in front of her chest, the day jar on the left and the night jar on the right, sitting side by side and touching, both front labels tipped up and forward towards the camera and both fully legible. Both jars are closed. Her fingers support them from beneath and behind and cover no lettering. She looks down at the two jars rather than at the camera.",
        "SCENE. A calm modern bathroom thrown gently out of focus behind her: pale grey textured plaster and soft cool daylight from the left, falling onto her hands and both lids.",
        "FRAME. Camera slightly above her hands, looking gently down so the two lids and both labels read together. Her hands, both jars and her face from the chin up are fully inside the frame; nothing of either jar is cut by any edge. Both jars are sharp. Square format. Every line of both front labels legible.",
        BOTH_JARS, BOTH_JARS_S, False, [MODEL], [MODEL_S],
    ),
]

#: Same negative as round 5 - product and label bars kept, set-dressing and people bars dropped.
#: Adds the supports a levitation or stack shot invites, since `b6-d` asks for objects to hold
#: position in mid-air and the honest way to render that is with a rig the brief must forbid.
NEGATIVE = (
    "rose-gold, copper-coloured metal, champagne metal, brass, gold, warm-tinted metal, chrome "
    "mirror finish, any printed word not listed in the brief, ingredient list, benefit lines, "
    "ALL SKIN TYPES, colour names printed as text, trademark symbol, registered trademark "
    "symbol, copyright symbol, watermark, signature, duplicate products, two identical jars, "
    "cardboard cartons, boxes, packaging boxes, text overlay, caption, cropped product, "
    "product touching the frame edge, blurry label, illegible lettering, misspelled lettering, "
    "visible support, stand, rod, wire, string, fishing line, clamp, prop holding a product, "
    "containers merged into one vessel, floating gap between stacked containers, "
    "airbrushed plastic skin, waxy skin, heavy make-up, long painted fingernails, jewellery, "
    "distorted hands, extra fingers, malformed fingers"
)


def build():
    slots = []
    for c in COMPOSITIONS:
        slot_id, arrangement, scene, frame, prods, prods_s, sep, extra = c[:8]
        extra_short = c[8] if len(c) > 8 else None
        slots.append(build_slot(slot_id, OPENING, arrangement, scene, frame,
                                products=prods, products_short=prods_s, separation=sep,
                                extra=extra, extra_short=extra_short))

    cfg = {
        "_comment": (
            "Copper Peptide stacked/piled + more model shots, round 6, 2026-09-11. GENERATED by "
            "scripts/build-copper-peptide-stacked-model-batch6.py; edit the builder, not this "
            "file. Malcolm: a batch where the products are piled or stacked on each other, "
            "researched and creative, plus more model shots holding the two cream jars. "
            "b6-a..b6-f are the stacks: two-jar tower, precarious offset, three-tier tower, "
            "levitating column, tumbled pile, and a serum bridge across both jars. b6-g..b6-k "
            "are five more of the model with both jars. The research on gravity-defying work is "
            "almost entirely about RIG - fishing line, rods, wire, painted out afterwards - "
            "which does not transfer to a brief, so what is briefed is the LOOK each rig exists "
            "to produce. Every stacking slot states that the upper container's base rests ON the "
            "lid beneath it, in contact, because left unstated engines merge two jars into one "
            "vessel or float the upper one."
        ),
        "wave": "copper-peptide-stacked-model-batch6-2026-09-11",
        "defaults": {"negative_global": NEGATIVE},
        "slots": slots,
    }
    OUT.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")

    print(f"{OUT.relative_to(ROOT)}\n{len(slots)} slots\n")
    for s in slots:
        print(f"  {s['id']:<34} prompt={len(s['prompt']):>5}  luma={len(s['prompt_luma']):>5}")
    missing = [r for r in REF_FILES if not (ROOT / r).exists()]
    if missing:
        raise SystemExit(f"missing reference files: {missing}")
    print(f"\n  5 suppliers x 2 candidates x {len(slots)} slots = {len(slots) * 10} candidates")


if __name__ == "__main__":
    build()
