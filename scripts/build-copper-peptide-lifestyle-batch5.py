#!/usr/bin/env python3
"""Emit round 5 — open jars, styled shelves and a model, rebuilt from Malcolm's own references.

    python3 scripts/build-copper-peptide-lifestyle-batch5.py
    set -a; source ~/.claude/config/image-credentials.env; set +a
    python3 scripts/generate-multi.py configs/banners/copper-peptide-lifestyle-batch5-2026-09-11.json

Malcolm, 2026-09-11, after rejecting most of the bathroom wave: recreate scenes more like two
images already live on the store, show one of the pots open, and add a shot with a 35-year-old
woman model showing both the night and the day cream pot.

THE REFERENCES OVERTURN MY OWN BRIEF, AND THAT IS THE POINT OF THIS FILE.
The two he linked are `..._bathroom_shelf_lifestyle_6_...` and `..._2_...`. Fetched and read:

  ref 6 - a CLOSE hero of the jar OPEN. Lid off and lying flat beside it, deep blue cream
          peaked in a soft swirl at the rim, and a SMEAR OF THE CREAM on the marble in front.
          Behind, thrown well out of focus: a bathroom, a steel soap dispenser, a green plant,
          and a woman applying cream to her cheek.
  ref 2 - a styled LIGHT OAK floating shelf against textured pale grey plaster. A beige
          ceramic reed diffuser, a framed black-line figure drawing, a round mirror above, a
          shower behind in soft focus. One jar, small in frame.

Round 3's negative barred, by name: "wooden vanity", "wood panelling", "houseplant", "potted
plant", "soap dispenser", "folded towels", "clutter", plus "hands, fingers, people, faces" in
the shared list - every single one of which appears in the two pictures he is pointing at. I
had read the cool-palette rule as governing the whole scene and it does not; it governs the
PRODUCT and the colour grade. His own live imagery is styled with warm oak and beige ceramic
and reads perfectly cool overall. So this wave carries its OWN negative, keeping every bar
that protects the product and the label and dropping every bar on set dressing and people.

WHAT IS INSIDE THE JAR IS NOW SPECIFIED. The moment a lid comes off, the substance is in shot,
and no spec on this project has ever described it - which is how serum bottles kept coming back
milky white. Day cream is a deep saturated dark blue, night cream a soft light blue, and they
must differ as plainly as their glass does.

THE MODEL SLOTS CARRY THE TWO FAULTS THE FACE WAVES KEPT RETURNING. A swatch is sized against
her own FINGERNAIL, in frame beside it, because two competing yardsticks let engines take the
looser one. And a fingertip must OVERLAP the cream so the cream is partly hidden by it -
adjacency is not contact, and "barely touching" renders as hovering.

Author: Claude Code, 2026-09-11.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from copper_peptide_set_spec import (  # noqa: E402
    DAY_CREAM_SUBSTANCE, DAY_JAR, DAY_JAR_S, NIGHT_CREAM_SUBSTANCE, NIGHT_JAR, NIGHT_JAR_S,
    MODEL, MODEL_S, OPEN_JAR, REF_FILES, SERUM_BOTTLE, SERUM_BOTTLE_S, build_slot,
    open_jar,
)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "configs" / "banners" / "copper-peptide-lifestyle-batch5-2026-09-11.json"

BOTH_JARS = [DAY_JAR, NIGHT_JAR]
BOTH_JARS_S = [DAY_JAR_S, NIGHT_JAR_S]
ALL_THREE = [DAY_JAR, SERUM_BOTTLE, NIGHT_JAR]
ALL_THREE_S = [DAY_JAR_S, SERUM_BOTTLE_S, NIGHT_JAR_S]

#: (id, ARRANGEMENT, SCENE, FRAME, products, products_short, separation, extra)
COMPOSITIONS = [
    (
        "b5-a-open-day-jar-swatch-model",
        "ARRANGEMENT. ALL THREE PRODUCTS ARE IN FRAME TOGETHER as a set. The day jar stands OPEN and nearest the camera, slightly right of centre and largest in frame, its front label square to the lens and fully legible; its lid lies flat on the surface behind and to the left of it, top face up. The serum bottle stands CLOSED just behind and to the left of the open jar, taller than it, its own front label facing the camera. The night jar stands CLOSED behind and to the right, turned a few degrees inward, its front label also facing the camera. On the surface in front of the open jar, a single generous SMEAR of the deep blue cream has been drawn across the stone with a palette knife, thick at one end and thinning to a tapered edge. All three front labels stay legible.",
        "SCENE. A pale grey-white marble surface with fine soft veining. Behind it, thrown well out of focus, a bright modern bathroom: a brushed steel soap dispenser at the left, a small green plant in a white pot behind it, and further back a woman standing at a mirror with her fingertips at her cheek, so soft she reads as atmosphere rather than as a subject. Cool clean daylight, bright and airy.",
        "FRAME. Camera low and very close, at the height of the jar's label. The open jar is fully inside the frame with its whole label visible; nothing of the jar is cut by any edge. Everything behind the jar is strongly out of focus while the jar, its rim, the cream inside it and the smear in front are all razor sharp. Square format. Every line of the front label legible.",
        ALL_THREE, ALL_THREE_S, True, [open_jar('DAY JAR'), DAY_CREAM_SUBSTANCE],
    ),
    (
        "b5-b-open-night-jar-swatch-model",
        "ARRANGEMENT. ALL THREE PRODUCTS ARE IN FRAME TOGETHER as a set. The night jar stands OPEN and nearest the camera, slightly right of centre and largest in frame, its front label square to the lens and fully legible; its lid lies flat on the surface behind and to the left of it, top face up. The serum bottle stands CLOSED just behind and to the left of the open jar, taller than it, its own front label facing the camera. The day jar stands CLOSED behind and to the right, turned a few degrees inward, its front label also facing the camera. On the surface in front of the open jar, a single generous SMEAR of the soft light blue cream has been drawn across the stone with a palette knife, thick at one end and thinning to a tapered edge. All three front labels stay legible.",
        "SCENE. A pale grey-white marble surface with fine soft veining. Behind it, thrown well out of focus, a calm modern bathroom in cooler evening light: a brushed steel soap dispenser at the left, a small green plant in a white pot behind it, and further back a woman standing at a mirror with her fingertips at her cheek, so soft she reads as atmosphere rather than as a subject. Cool, quiet, low-key but not dark.",
        "FRAME. Camera low and very close, at the height of the jar's label. The open jar is fully inside the frame with its whole label visible; nothing of the jar is cut by any edge. Everything behind the jar is strongly out of focus while the jar, its rim, the cream inside it and the smear in front are all razor sharp. Square format. Every line of the front label legible.",
        ALL_THREE, ALL_THREE_S, True, [open_jar('NIGHT JAR'), NIGHT_CREAM_SUBSTANCE],
    ),
    (
        "b5-c-open-day-jar-swatch-clean",
        "ARRANGEMENT. ALL THREE PRODUCTS ARE IN FRAME TOGETHER as a set. The day jar stands OPEN and nearest the camera at the centre, largest in frame, its front label square to the lens and fully legible, its lid lying flat on the surface behind it. The serum bottle stands CLOSED behind and to the left, taller than it, and the night jar stands CLOSED behind and to the right, both with their front labels facing the camera. A single SMEAR of the deep blue cream is drawn across the stone in front of the open jar, and a second much smaller dab sits apart from it. All three front labels stay legible.",
        "SCENE. A pale grey-white marble surface with fine soft veining, and behind it a plain bright bathroom wall thrown completely out of focus into a soft pale wash with no identifiable object in it at all. Cool clean daylight from the left, bright and airy.",
        "FRAME. Camera low and very close, at the height of the jar's label. The open jar is fully inside the frame with its whole label visible; nothing of the jar is cut by any edge. The jar, its rim, the cream inside and the smear are razor sharp against a completely soft background. Square format. Every line of the front label legible.",
        ALL_THREE, ALL_THREE_S, True, [open_jar('DAY JAR'), DAY_CREAM_SUBSTANCE],
    ),
    (
        "b5-d-oak-shelf-trio-styled",
        "ARRANGEMENT. The three products stand together on a light oak floating shelf, grouped a little right of centre with the serum bottle at the middle. To their left on the same shelf stands a small matte beige ceramic bottle vase holding six slim natural reed diffuser sticks. To their right, leaning against the wall, a framed print - a black continuous-line drawing of a female figure on plain white, in a slim black frame. All three front labels face the camera and stay fully legible.",
        "SCENE. A wall of pale grey plaster with a fine sandy texture, and a light oak floating shelf with a square front edge and visible straight grain, cantilevered from it with no brackets. A round mirror with a slim brushed steel rim hangs on the wall above the shelf, partly in frame. Soft even daylight from the left. Calm, modern, styled and uncluttered.",
        "FRAME. Camera straight on at shelf height, close enough that the shelf runs across the lower third and the textured wall fills the upper frame. All three products are fully inside the frame; nothing is cut by any edge. Square format. Sharp focus across all three front labels, every line legible.",
        ALL_THREE, ALL_THREE_S, True, None,
    ),
    (
        "b5-e-oak-shelf-day-jar-open",
        "ARRANGEMENT. The day jar stands OPEN at the centre of a light oak floating shelf, its lid lying flat on the oak beside it, its front label square to the camera and fully legible, the deep blue cream visible at the rim. The night jar stands closed a little to the right, turned a few degrees inward, its own label also fully legible. To the left, a small matte beige ceramic bottle vase holds six slim natural reed diffuser sticks.",
        "SCENE. A wall of pale grey plaster with a fine sandy texture and a light oak floating shelf with a square front edge and visible straight grain. A framed black-line figure drawing on plain white leans against the wall at the far right, partly in frame. Soft even daylight from the left, bright and calm.",
        "FRAME. Camera straight on and close, at the height of the jar labels. Both jars are fully inside the frame with their whole labels visible; nothing is cut by any edge. Square format. Sharp focus on both front labels and on the cream at the open rim, every line legible.",
        BOTH_JARS, BOTH_JARS_S, False, [open_jar('DAY JAR'), DAY_CREAM_SUBSTANCE],
    ),
    (
        "b5-f-oak-shelf-wider-room",
        "ARRANGEMENT. The three products stand together on a light oak floating shelf, small in the frame and positioned about a third of the way in from the left, with a beige ceramic reed diffuser beside them and a framed black-line figure drawing leaning at the right. All three front labels face the camera and stay legible despite their size in frame.",
        "SCENE. A wider view of a calm modern bathroom: pale grey textured plaster walls, the light oak shelf, a round steel-rimmed mirror above it, and to one side a walk-in shower with a slim steel rain head and a frameless glass screen, all softly out of focus. A wall-mounted steel tap and the edge of a square white basin sit in the lower corner. Cool bright daylight.",
        "FRAME. Camera straight on, further back than a product shot, so the room reads and the shelf sits in the middle distance. All three products are fully inside the frame; nothing is cut by any edge. The products stay sharp while the room falls gently out of focus. Square format. Every line of all three front labels legible.",
        ALL_THREE, ALL_THREE_S, True, None,
    ),
    (
        "b5-g-model-holding-both-jars",
        "ARRANGEMENT. The model holds ONE JAR IN EACH HAND, raised to about chest height and turned so BOTH front labels face the camera square on and stay fully legible - the day jar in her right hand at the left of frame, the night jar in her left hand at the right of frame. Her fingers curl around the sides of each jar and do not cover any part of either label. Both jars are closed. She looks towards the camera, calm and at ease.",
        "SCENE. A calm modern bathroom thrown gently out of focus behind her: pale grey textured plaster, a light oak shelf, a round steel-rimmed mirror. Soft cool daylight from the left falling evenly across her face and both jars. Bright, clean and airy.",
        "FRAME. Camera at her chest height, close enough that she is framed from mid-chest to just above her head. Both jars and both her hands are fully inside the frame; her head is fully inside the frame and nothing of either jar is cut by any edge. Both jars are in sharp focus and so is her face. Square format. Every line of both front labels legible.",
        BOTH_JARS, BOTH_JARS_S, False, [MODEL], [MODEL_S],
    ),
    (
        "b5-h-model-open-jar-fingertip",
        "ARRANGEMENT. The model holds the OPEN day jar in her left hand at about chest height, its front label turned square to the camera and fully legible, the lid absent from her hands. With the index finger of her right hand she has just lifted a small dab of the deep blue cream from the surface of the cream in the jar; the dab sits ON HER FINGERTIP and the fingertip is still OVERLAPPING the cream in the jar, partly hidden by the rim, so the two are plainly in contact and not merely near each other. THE DAB IS SMALL - no larger than her own fingernail, which is visible in the same frame as the yardstick. She looks down at the jar.",
        "SCENE. A calm modern bathroom thrown gently out of focus behind her: pale grey textured plaster and soft cool daylight from the left. Bright, clean and airy.",
        "FRAME. Camera at the height of her hands, close enough that the jar, both hands and her face from the chin up are in frame. The jar is fully inside the frame with its whole label visible; nothing of it is cut by any edge. The jar rim, the cream inside and the dab on her fingertip are all razor sharp. Square format. Every line of the front label legible.",
        [DAY_JAR], [DAY_JAR_S], False, [MODEL, OPEN_JAR, DAY_CREAM_SUBSTANCE],
        [MODEL_S, OPEN_JAR, DAY_CREAM_SUBSTANCE],
    ),
    (
        "b5-i-model-vanity-both-jars",
        "ARRANGEMENT. The model stands behind a vanity top on which BOTH JARS stand side by side in the near foreground, closed, both front labels square to the camera and fully legible, the day jar on the left and the night jar on the right. She rests one hand lightly on the counter beside them and looks down towards the jars. She is behind and above them, softer than they are.",
        "SCENE. A calm modern bathroom: a pale grey stone vanity top, pale grey textured plaster behind, a round steel-rimmed mirror on the wall. Soft cool daylight from the left. Bright and uncluttered.",
        "FRAME. Camera at counter height looking slightly up past the jars to her. Both jars are fully inside the frame and fully sharp in the foreground; she is behind them, from the waist up and gently out of focus, her head fully inside the frame. Nothing of either jar is cut by any edge. Square format. Every line of both front labels legible.",
        BOTH_JARS, BOTH_JARS_S, False, [MODEL], [MODEL_S],
    ),
    (
        "b5-j-both-jars-open-pair",
        "ARRANGEMENT. BOTH JARS STAND OPEN side by side and close together, the day jar on the left and the night jar on the right, both front labels square to the camera and fully legible, each lid lying flat on the surface behind its own jar. The two creams are visible at both rims and THE TWO ARE PLAINLY DIFFERENT: the left jar holds a deep saturated dark blue cream and the right jar a soft light blue one, the difference obvious at a glance. In front of each jar, a short smear of that jar's own cream is drawn on the stone, the two smears clearly different in colour.",
        "SCENE. A pale grey-white marble surface with fine soft veining, and behind it a plain bright wall thrown completely out of focus into a soft pale wash. Cool clean daylight from above and slightly left, even across both jars.",
        "FRAME. Camera low and close, at the height of the jar labels, framed so both open rims are visible. Both jars are fully inside the frame with their whole labels visible; nothing is cut by any edge. Both rims, both creams and both smears are razor sharp. Square format. Every line of both front labels legible.",
        BOTH_JARS, BOTH_JARS_S, False, [OPEN_JAR, DAY_CREAM_SUBSTANCE, NIGHT_CREAM_SUBSTANCE],
    ),
]

#: This wave's OWN negative. It keeps every bar that protects the product and the label and
#: DROPS every bar on set dressing and people, because round 3's negative barred wooden
#: shelves, plants, diffusers, soap dispensers, hands and faces - all of which appear in the
#: two reference pictures Malcolm is asking us to match. "cropped product" is kept: a jar
#: bleeding off the frame cannot sit in a square gallery slot.
LIFESTYLE_NEGATIVE = (
    "rose-gold, copper-coloured metal, champagne metal, brass, gold, warm-tinted metal, chrome "
    "mirror finish, any printed word not listed in the brief, ingredient list, benefit lines, "
    "ALL SKIN TYPES, colour names printed as text, trademark symbol, registered trademark "
    "symbol, copyright symbol, watermark, signature, duplicate products, two identical jars, "
    "cardboard cartons, boxes, packaging boxes, text overlay, caption, cropped product, "
    "product touching the frame edge, blurry label, illegible lettering, misspelled lettering, "
    "white cream, ivory cream, off-white cream, both creams the same colour, "
    "airbrushed plastic skin, waxy skin, heavy make-up, long painted fingernails, jewellery, "
    "distorted hands, extra fingers, malformed fingers"
)


def build():
    slots = []
    for c in COMPOSITIONS:
        slot_id, arrangement, scene, frame, prods, prods_s, sep, extra = c[:8]
        extra_short = c[8] if len(c) > 8 else None
        slots.append(build_slot(
            slot_id,
            "A premium skincare lifestyle photograph for Skingenetix Copper Peptide.",
            arrangement, scene, frame,
            products=prods, products_short=prods_s, separation=sep,
            extra=extra, extra_short=extra_short))

    cfg = {
        "_comment": (
            "Copper Peptide lifestyle round 5, 2026-09-11. GENERATED by "
            "scripts/build-copper-peptide-lifestyle-batch5.py; edit the builder, not this file. "
            "Rebuilt from two images already live on the store that Malcolm linked as the "
            "target: a close hero of the jar OPEN with its lid beside it, cream peaked at the "
            "rim and a smear on the marble, a bathroom and a woman soft behind; and a styled "
            "LIGHT OAK floating shelf with a ceramic reed diffuser, a framed line drawing and a "
            "round mirror. Round 3's negative barred wooden shelves, plants, diffusers, soap "
            "dispensers, hands and faces by name - every one of which is in those two pictures. "
            "So this wave carries its OWN negative that keeps the product and label bars and "
            "drops the set-dressing and people bars. What is INSIDE the jars is specified for "
            "the first time, because a lid coming off puts the substance in shot and no spec "
            "here has ever described it. Three slots carry a 35-year-old model, per his brief."
        ),
        "wave": "copper-peptide-lifestyle-batch5-2026-09-11",
        "defaults": {"negative_global": LIFESTYLE_NEGATIVE},
        "slots": slots,
    }
    OUT.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")

    print(f"{OUT.relative_to(ROOT)}\n{len(slots)} slots\n")
    for s in slots:
        print(f"  {s['id']:<32} prompt={len(s['prompt']):>5}  luma={len(s['prompt_luma']):>5}")
    missing = [r for r in REF_FILES if not (ROOT / r).exists()]
    if missing:
        raise SystemExit(f"missing reference files: {missing}")
    print(f"\n  5 suppliers x 2 candidates x {len(slots)} slots = {len(slots) * 10} candidates")


if __name__ == "__main__":
    build()
