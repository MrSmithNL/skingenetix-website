#!/usr/bin/env python3
"""Build the before/after wave for two science-page cards: PDRN under-eye and Argireline forehead.

    python3 scripts/build-under-eye-forehead-before-after-config.py
    → configs/banners/before-after-undereye-forehead.json

    python3 scripts/generate-multi.py configs/banners/before-after-undereye-forehead.json \
        --candidates 1 --only <slot-id>[,<slot-id>]

⚠️ `--candidates 1` IS NOT OPTIONAL: generate-multi.py never reads `defaults.candidates`, and its
flag defaults to 2, which silently doubles the spend.

THE TWO CARDS, AND WHAT EACH PICTURE MAY CLAIM
  pdrn-undereye        /pages/pdrn-research, section key_findings_ba, block f4 -
                       "Under-Eye Bags: About 2x the Retinol Change". Ye 2026 (PLOS ONE e0350905):
                       randomised, double-blind, SPLIT-FACE, 31 Chinese women aged 35-55 (mean 47.5)
                       with self-reported sensitive skin, 0.1% PDRN eye cream against 0.1% retinol in
                       the same base, 28 days. Antera 3D: eye-bag volume and tear-trough depth
                       improved about twice as much on the PDRN side. The paper gives the ratio, not
                       an absolute percentage, so the picture is briefed as a MODEST change - each
                       bulge about a fifth less full, each hollow about a fifth shallower - in line
                       with the ~20% crow's-feet change the same trial measured and the crow's-feet
                       card beside it on the same page.
  argireline-forehead  /pages/acetyl-hexapeptide-8-research (templates/page.research-argireline.json),
                       section key_findings_ba, block f5 - "Forehead Roughness -7.4% by Day 20".
                       Raikou 2017 (J Cosmet Dermatol 16:271): randomised, placebo-controlled, 24
                       women aged 30-60, 10% Argireline cream twice daily, run in Athens. Visioscan
                       cR2 is a SURFACE-ROUGHNESS measure, so the change is mostly in fine texture,
                       and 7.4% is small: briefed as visibly but subtly better, every line still there.

WHAT THIS BRIEF INHERITS (docs/clinical-trial-before-after-images.md, fifteen acetyl waves plus
the glutathione and copper-peptide rounds): two sessions not two frames; one prompt per slot so
each pair has its own room pair (six slots, six women, candidates 1); the identity lock; the
honesty rules HOISTED to paragraph 3, because at paragraph 17 they lost to the engine's own prior
on every backend (glutathione r1 -> r2); the visible-improvement floor AND a ceiling; no hand or
phone in frame; no baked-in text, because Translate & Adapt reaches theme JSON and cannot touch
pixels; describing the panels by what changed rather than naming them, so nbp_pro has no caption
words to render; per-panel camera height, tilt, turn, distance and placement (copper-peptide,
Malcolm 2026-08-27: pairs looked like duplicates); THE SIDE-LOCK (the camera moves, the side of the
face it looks at does not); the distance guard; and, for the one-eye crop, framing by FEATURES,
because a band bounded by features is the only tight crop engines honour.

STRUCTURE copied from scripts/build-glutathione-before-after-config.py: one skeleton plus per-slot
substitutions, ROOMS, CROPS, per-woman `before` strings, a shorter Luma brief, and a length
assertion under Luma's 6,000-character cap (LUMA_CAP).

WHAT IT CHANGES, AND WHY
  1. LIGHTING GOES BACK TO THE ACETYL (LINE / VOLUME) LOGIC, NOT GLUTATHIONE'S. The glutathione
     builder inverted the light for a TONE page; these are line and volume subjects, so the light
     is directional again. But not merely "from the side": every feature on both cards is
     HORIZONTAL - forehead lines, the bulge along the lower lid, the tear-trough groove below it -
     and a horizontal line only casts a shadow when light CROSSES it. Pure sidelight runs along
     a horizontal line and flattens it. So every room's window is HIGH on one side and the light
     grazes DOWN across her face.
  2. BAD LIGHT OR A KIND ANGLE CAN FABRICATE A VOLUME RESULT, so a guard sits on both. Soft
     frontal light makes an under-eye bag vanish on its own, and a camera held above the eye
     foreshortens it away; a camera held below the brow foreshortens a forehead. So both days
     carry the same grazing character, neither is the flattering one, and every camera-height
     difference in VIEWPOINTS runs AGAINST the improvement: the later under-eye panel is shot from
     level or slightly lower (bags read MORE from below), the later forehead panel from level or
     slightly higher (lines read MORE from above).
  3. EXPRESSION IS A CONFOUND ON BOTH CARDS AND IS LOCKED. Raised brows fold the forehead into
     deep lines; a smile or a squint bunches the lower lid. Either, in one panel and not the
     other, manufactures the whole difference. Both are stated in paragraph 2 and negated.
  4. CASTING FOLLOWS THE TRIAL POPULATION. pdrn-undereye casts CHINESE women aged mid-forties to
     early fifties, matching Ye 2026 and the live crow's-feet card on the same page (block
     `block-pdrn-research-crows-feet`, Chinese casting, already decided). argireline-forehead casts
     GREEK women, because Raikou 2017 was run in Athens; that is also inside Malcolm's
     acetyl-page instruction (Caucasian, middle-aged, ordinary). THE ETHNICITY BANS IN THE COPPER
     NEGATIVE LIST ("no asian model" ...) ARE NOT CARRIED OVER - on this wave they would fight the
     PDRN casting on three slots. Casting is stated positively instead.
  5. MOLES AND FRECKLES ARE ANCHORS, NOT A PROBLEM. This is not a pigment page
     (realism-marks-become-the-problem-on-a-pigmentation-page does not apply), so each woman
     carries one or two named marks as identity anchors. What must NOT change is the COLOUR under
     the eye: the under-eye claim is shape (volume, depth), so the brief says the hollow holds
     less SHADOW, never that the skin gets lighter - a lighter under-eye would be a tone claim the
     trial did not make.
  6. SPLIT-FACE, AND THE ONE CROP THAT SHOWS BOTH EYES. Ye 2026 treated one side with PDRN and
     the other with retinol. Slots a and b lock ONE side (one under-eye, the same one in both
     panels), exactly as the live crow's-feet card does. Slot c is a frontal band with BOTH
     under-eyes, because Malcolm's own under-eye reference pairs (2026-08-28, copper-peptide
     round) were frontal bands and they are the framing engines honour; both eyes are briefed to
     look alike in each panel so the picture can never read as PDRN-side against retinol-side.
     It illustrates using the cream rather than depicting the split-face design, and that is
     flagged for Malcolm in the config note.

SUPPLIERS: all six, per rule 1 of .claude/rules/website-imagery.md (every image goes to every
supplier). The recorded exclusions still stand as WARNINGS, not as bans: nbp_pro has burnt
captions into seven acetyl waves, luma has answered this family with HTTP 422 (it did pass on
glutathione r2 with a short prompt_luma), flux2 went 0/8 on glutathione. Check those first.

Author: Claude Code, 2026-09-24.
Purpose: candidates for Malcolm to choose from; nothing is uploaded or published by this file.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WAVE = "before-after-undereye-forehead"
OUT = ROOT / "configs" / "banners" / f"{WAVE}.json"
SIZE = 2048   # square: research-before-after takes the row height from the master, labels at 50%

# Luma answers anything over 6,000 characters with a bare HTTP 422 that reads like a content
# refusal. Held below the real cap on purpose, as in the glutathione builder, so a later edit to
# the shared text trips this assertion rather than silently losing the backend.
LUMA_CAP = 5700

# --------------------------------------------------------------------------------------
# SMOKE-TEST LOG. One slot per block (pdrn-undereye-b, argireline-forehead-d) was run across
# all six suppliers BEFORE the other four slots. What it found, and what changed, is recorded
# here after the run - see SMOKE_TEST_LOG at the bottom of the constants.
# --------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------
# Rooms. Twelve, so no two slots share a room and no pair repeats one. Wall colour + where the
# window is + ONE soft unidentifiable element (a bare edge left nothing for the engine to place
# there, and nbp_flash supplied a phone instead - acetyl wave 15).
#
# EVERY WINDOW IS HIGH OR ABOVE. See docstring point 1: the features on both cards are
# horizontal, and only light arriving from above casts their shadows. The SIDE alternates within
# each pair so the two days are plainly differently lit.
# --------------------------------------------------------------------------------------
ROOMS = [
    ("a WARM WHITE wall", "high on her left", "the soft vertical edge of a doorframe"),
    ("a PALE GREY wall", "high on her right", "the faint corner where two walls meet"),
    ("a SOFT BEIGE wall", "above her and to her right", "the blurred top of a chair back"),
    ("a MUTED SAGE-GREY wall", "above her and to her left", "the vertical fall of a plain curtain"),
    ("a SOFT TAUPE wall", "high on her left", "the pale line where the wall meets the ceiling"),
    ("a PALE BLUE-GREY wall", "high on her right", "the soft dark shape of a coat on a hook"),
    ("an OFF-WHITE wall", "above her and to her left", "the blurred edge of a door standing open"),
    ("a PALE OATMEAL wall", "above her and to her right", "the shape of a lampshade that is switched off"),
    ("a SOFT CLAY-PINK wall", "high on her right", "the out-of-focus back of a dining chair"),
    ("a CHALK WHITE wall", "high on her left", "the soft upright of a door architrave"),
    ("a WARM IVORY wall", "above her and to her left", "the soft dark line of a picture rail"),
    ("a LIGHT STONE-GREY wall", "above her and to her right", "the soft fall of a plain window blind"),
]

# --------------------------------------------------------------------------------------
# Crops. Three per block, so the six pairs do not stack up as one framing. Each panel of the
# square master is a 1:2 tall strip, so every crop has to work in portrait.
#
# `selfie` False on the one-eye crop: nobody holds a phone that close to their own eye and keeps
# it in focus, so "selfie" there asks for the impossible and invites a hand back into frame.
# The one-eye and forehead crops are bounded by FEATURES (brow / nose tip; hairline / below the
# eyes) because that is the only kind of tight crop engines have honoured on this project.
# --------------------------------------------------------------------------------------
CROPS = {
    # ---- pdrn-undereye ---------------------------------------------------------------
    "eye_tight": dict(
        selfie=False,
        label="one eye, close",
        text=(
            "ONE EYE AND THE SKIN BENEATH IT FILL THE PANEL. The frame runs from her eyebrow at the "
            "top down to about the level of the tip of her nose at the bottom, and across from the "
            "bridge of her nose on one side to her temple on the other. Only that one eye is in the "
            "picture; the other eye is outside the frame. THE LOWER EYELID, THE SOFT PUFFY BULGE "
            "BENEATH IT AND THE HOLLOW GROOVE THAT RUNS DOWN AND OUT FROM THE INNER CORNER OF THE EYE "
            "ALONG THE BONE BELOW IT sit in the middle of the panel and are what the picture is of. "
            "This is an ordinary close photograph taken at home in daylight - not a selfie, not a "
            "studio portrait and not a clinical photograph - and it is sharp across the under-eye."
        ),
    ),
    "half": dict(
        selfie=True,
        label="three-quarter, one side",
        text=(
            "ONE SIDE OF HER FACE, IN A CLOSE THREE-QUARTER VIEW, FILLS THE PANEL. The frame runs "
            "from her brow at the top down to the corner of her mouth at the bottom, with the near "
            "eye high in the frame and the cheek below it; the far side of her face turns away and "
            "is mostly out of the frame. THE UNDER-EYE OF THE NEAR EYE - the puffy bulge along the "
            "lower lid and the hollow groove below it - sits in the upper middle of the panel, large "
            "enough to read clearly, and is what the picture is of."
        ),
    ),
    "band": dict(
        selfie=True,
        label="mid-face band, both eyes",
        text=(
            "THE PANEL IS A BAND ACROSS THE MIDDLE OF HER FACE. The frame runs from the middle of her "
            "forehead at the top down to her top lip at the bottom, and out past both cheekbones at "
            "the sides. Both eyes, both brows, her nose and the tops of both cheeks are in view; her "
            "mouth and chin are NOT in the picture. THE PUFFY BULGES UNDER BOTH EYES AND THE HOLLOW "
            "GROOVES BELOW THEM are what the picture is of. Her two under-eyes look like each other "
            "in each panel - one side is never better or worse than the other."
        ),
    ),
    # ---- argireline-forehead ---------------------------------------------------------
    "forehead_band": dict(
        selfie=True,
        label="forehead band",
        text=(
            "THE PANEL IS A BAND ACROSS THE UPPER FACE AND THE FOREHEAD IS ALMOST ALL OF IT. The "
            "frame runs from her hairline at the top down to just below her eyes at the bottom, and "
            "out past both temples at the sides. Her eyebrows and both eyes are inside the bottom of "
            "the frame so it is unmistakably a face, but there is NO nose tip, NO mouth and NO chin "
            "in view - they are outside the frame entirely. THE HORIZONTAL LINES ACROSS HER FOREHEAD "
            "AND THE FINE TEXTURE OF THE SKIN BETWEEN THEM ARE WHAT THE PICTURE IS OF, and they run "
            "the full width of the panel."
        ),
    ),
    "upper_face": dict(
        selfie=True,
        label="upper half of the face",
        text=(
            "THE UPPER HALF OF HER FACE FILLS THE PANEL. The frame runs from just above her hairline "
            "at the top - a little of her pulled-back hair is in view - down to the tip of her nose "
            "at the bottom, with her temples running to both edges. Her mouth and chin are outside "
            "the frame. The whole of her forehead is in view and is the largest thing in the "
            "picture: ITS HORIZONTAL LINES AND THE TEXTURE OF THE SKIN BETWEEN THEM ARE WHAT THE "
            "PICTURE IS OF. Because the phone is close, her forehead looms a little."
        ),
    ),
    "three_quarter": dict(
        selfie=True,
        label="forehead and temple, three-quarter",
        text=(
            "HER FOREHEAD AND ONE TEMPLE, IN A CLOSE THREE-QUARTER VIEW. Her head is turned so the "
            "camera sees her forehead from a little to one side: the frame runs from her hairline at "
            "the top down to her cheekbone at the bottom, with the near temple and brow large in the "
            "frame and the far side of her forehead running away from the camera. THE HORIZONTAL "
            "LINES RUNNING ACROSS HER FOREHEAD AND ROUND TOWARDS THE NEAR TEMPLE, and the texture of "
            "the skin between them, are what the picture is of."
        ),
    ),
}

# --------------------------------------------------------------------------------------
# Per-block text. `expression` is paragraph 2 (the confound on each card, docstring point 3).
# `honesty` is rule THREE at paragraph 3 and is restated at the point of change. `magnitude` is
# the floor AND the ceiling on the right panel.
# --------------------------------------------------------------------------------------
BLOCKS = {
    "pdrn-undereye": dict(
        page="/pages/pdrn-research",
        template="templates/page.pdrn-research.json",
        block="f4",
        heading="Under-Eye Bags: About 2x the Retinol Change",
        study="ye-2026",
        after_label="After 28 days",
        expression=(
            "Her face is completely at rest on both days: eyes open normally, mouth closed, not "
            "smiling, not squinting and not wide-eyed. A smile pushes the cheek up and bunches the "
            "lower eyelid, and a squint does the same, so either one would change the very thing "
            "being compared - her eyes and cheeks are in the same relaxed resting state in both "
            "panels."
        ),
        honesty=(
            "THE SHAPE OF HER EYES IS UNCHANGED - the same eyelids, the same eyelid crease or lack "
            "of one, the same lashes, the same eye opening. Every bulge and every hollow under her "
            "eyes is STILL THERE in the right panel, in the same place and the same shape, only less "
            "pronounced. And this is a change of SHAPE, NOT OF COLOUR: the skin under her eyes is the "
            "same colour in both panels. The bulge is flatter and the groove shallower, so they hold "
            "less shadow - nothing has been lightened, concealed or brightened."
        ),
        age=(
            "SHE IS IN HER MID-FORTIES TO EARLY FIFTIES - MIDDLE-AGED, CLEARLY NOT YET SIXTY - AND "
            "THAT GOVERNS WHAT HER SKIN CAN HONESTLY LOOK LIKE. The puffiness and hollows under her "
            "eyes are established and stay put with her face at rest, fine lines sit on the lower "
            "lids and at the outer corners, and some grey in her hair is normal. But she is NOT "
            "elderly: no heavy hanging bags, no deeply sunken eyes, no drooping upper lids, none of "
            "the slackness of a woman in her seventies."
        ),
        subject=("ON THE EARLIER DAY, IN THE LEFT PANEL, THE PUFFINESS AND THE HOLLOWS UNDER HER EYES "
                 "ARE THE SUBJECT OF THE PICTURE. "),
        magnitude=(
            "THE UNDER-EYE IS SMOOTHER AND LESS HOLLOW, AND THE CHANGE IS MODEST AND BELIEVABLE. The "
            "puffy bulge along the lower lid is somewhat flatter - about a fifth less full - so the "
            "small curved shadow beneath it is shorter and lighter. The hollow groove running down "
            "from the inner corner of the eye is somewhat shallower and holds a softer, lighter "
            "shadow, so the under-eye reads less tired. The fine crinkled lines on the lower lid are "
            "a little softer.\n\n"
            "THE SIZE OF THE CHANGE IS NARROW AT BOTH ENDS. It must be VISIBLE: a viewer looking "
            "from one panel to the other should see that the under-eye is smoother and less hollow "
            "in the later one and be able to point to where. But it is NOT A TRANSFORMATION: the "
            "bulge and the groove are both still plainly there, in the same place and the same "
            "shape, just less pronounced. The under-eye has not been filled, tightened or made "
            "young. A right panel with a flat, smooth, hollow-free under-eye is a failure, not a "
            "success."
        ),
        negatives=(
            "no smiling, no squinting, no closed eye, no wide staring eyes, no eye makeup, "
            "no change of eye shape between the panels, no change of eyelid shape between the panels, "
            "no double eyelid appearing, no filler look, no smooth hollow-free under-eye in the right "
            "panel, no bag disappearing completely, no lighter under-eye skin in the right panel, "
            "no concealer, no dark circles appearing, no bruise under the eye, no swollen eyes, "
            "no left eye beside right eye comparison, no one eye better than the other, "
            "no woman under thirty-five, no elderly woman, no heavy hanging eye bags"
        ),
    ),
    "argireline-forehead": dict(
        page="/pages/acetyl-hexapeptide-8-research",
        template="templates/page.research-argireline.json",
        block="f5",
        heading="Forehead Roughness -7.4% by Day 20",
        study="raikou-2017",
        after_label="After 20 days",
        expression=(
            "Her face is at rest on both days, mouth closed, not smiling. HER EYEBROWS ARE RELAXED "
            "AND IN EXACTLY THE SAME RESTING POSITION IN BOTH PANELS - never raised and never "
            "frowning. Raising the brows is what folds the forehead into deep lines, so brows raised "
            "in one panel and relaxed in the other would manufacture the whole difference; the lines "
            "in both panels are the ones that stay in her forehead at rest. Her hair is pulled back "
            "off her forehead on both days so none of it is covered - no fringe and no loose strands "
            "across it."
        ),
        honesty=(
            "EVERY LINE ON HER FOREHEAD IS STILL THERE IN THE RIGHT PANEL - the same number of lines, "
            "each the same length and in the same place, and each still clearly visible as a line. "
            "None has disappeared, and the forehead has NOT become smooth, shiny, taut or "
            "frozen-looking. What has changed is small: the fine texture of the skin surface between "
            "and along the lines is a little finer and less rough, and the lines are a touch softer."
        ),
        age=(
            "SHE IS BETWEEN FORTY AND FIFTY-FIVE - MIDDLE-AGED, CLEARLY NOT YET SIXTY - AND THAT "
            "GOVERNS WHAT HER SKIN CAN HONESTLY LOOK LIKE. Her forehead lines are established and "
            "stay put with her face at rest, and some grey at the parting and temples is normal. But "
            "she is NOT elderly: no deep folds, no heavy brow, none of the crepe-papery slackness of "
            "a woman in her seventies."
        ),
        subject=("ON THE EARLIER DAY, IN THE LEFT PANEL, THE LINES AND THE ROUGH SURFACE TEXTURE OF "
                 "HER FOREHEAD ARE THE SUBJECT OF THE PICTURE. "),
        magnitude=(
            "HER FOREHEAD IS A LITTLE SMOOTHER, AND THE CHANGE IS SMALL. The fine, dry, crosshatched "
            "texture between and along the lines is a little finer and calmer, so the surface catches "
            "the grazing light more evenly and looks a little less rough and dry. Each horizontal "
            "line is a touch softer, its shadow slightly lighter and slightly shorter.\n\n"
            "THE CEILING MATTERS AS MUCH AS THE FLOOR. It must be VISIBLE: someone looking from one "
            "panel to the other should be able to see that the later forehead is smoother and point "
            "to where the surface has calmed. But it is SUBTLE - a viewer has to compare to see it. "
            "Every line is still there and still reads clearly as a forehead line; the deeper lines "
            "are barely changed at all. The forehead does not read smooth, lifted, frozen, shiny or "
            "younger. A right panel with a smooth, line-free forehead is a failure, not a success."
        ),
        negatives=(
            "no raised eyebrows, no frowning, no surprised expression, no brows in different "
            "positions between the panels, no smooth line-free forehead in the right panel, "
            "no line disappearing between the panels, no shiny forehead, no frozen forehead, "
            "no taut stretched forehead, no fringe, no bangs, no hair across the forehead, no hat, "
            "no headband, no woman under thirty-five, no elderly woman"
        ),
    ),
}

# --------------------------------------------------------------------------------------
# Viewpoints, one per slot, stated per panel (copper-peptide round). `side` is the lock.
#
# RULE FOR THIS WAVE: every camera-height difference runs AGAINST the improvement. Under-eye
# bags read MORE from below and LESS from above, so the later under-eye panel is shot from level
# or slightly lower. Forehead lines read MORE from above (the forehead faces the lens) and LESS
# from below (it foreshortens away), so the later forehead panel is shot from level or slightly
# higher. The picture can then never owe its improvement to the angle. Distance alternates in
# both directions, bounded by the distance guard in paragraph 7.
# --------------------------------------------------------------------------------------
SIDE_FRONT = ("SHE IS FACING THE CAMERA MORE OR LESS SQUARE ON IN BOTH PANELS - the FRONT of her "
              "face is what the camera sees on both days")
SIDE_LEFT_EYE = ("IT IS THE SAME EYE IN BOTH PANELS: HER LEFT EYE. It is never her left eye in one "
                 "panel and her right eye in the other - those are two different under-eyes, with "
                 "different bulges, hollows and marks, and there would be nothing to compare")
SIDE_RIGHT = ("THE SAME SIDE OF HER FACE IS TOWARDS THE CAMERA IN BOTH PANELS: HER RIGHT SIDE. On "
              "both days her head is turned towards her own LEFT, so the camera sees the RIGHT side "
              "of her face. It is never the right side in one panel and the left in the other")
SIDE_LEFT = ("THE SAME SIDE OF HER FACE IS TOWARDS THE CAMERA IN BOTH PANELS: HER LEFT SIDE. On "
             "both days her head is turned towards her own RIGHT, so the camera sees the LEFT side "
             "of her forehead and her left temple. It is never the right side in one panel and the "
             "left in the other")

VIEWPOINTS = {
    # PDRN — later panel level or LOWER
    "a": dict(side=SIDE_LEFT_EYE,
              a=dict(cam="held at her eye line, a little out to her left",
                     turn="her head turned about ten degrees to her own right, level",
                     dist="framed a little further back", place="the eye sits high and left of centre"),
              b=dict(cam="held just below her eye line and tilted up slightly",
                     turn="her head turned about twenty degrees to her own right, level",
                     dist="framed a little closer in", place="the eye sits centred and a little low")),
    "b": dict(side=SIDE_RIGHT,
              a=dict(cam="held a little above her eye line and out to her right, angled slightly down",
                     turn="her head turned about twenty-five degrees to her own left, level",
                     dist="framed closer in", place="her eye sits high and right of centre"),
              b=dict(cam="held at her eye line, out to her right",
                     turn="her head turned about thirty-five degrees to her own left and tipped a little up",
                     dist="framed a little further back", place="her eye sits centred")),
    "c": dict(side=SIDE_FRONT,
              a=dict(cam="held at her eye line, directly in front of her",
                     turn="her head square to the camera, level",
                     dist="framed a little further back", place="her face sits centred and a little high"),
              b=dict(cam="held a little below her eye line and tilted up towards her",
                     turn="her head square to the camera and tipped very slightly down",
                     dist="framed a little closer in", place="her face sits low and left of centre")),
    # ARGIRELINE — later panel level or HIGHER
    "d": dict(side=SIDE_FRONT,
              a=dict(cam="held at her eye line",
                     turn="her head square to the camera, level",
                     dist="framed a little closer in", place="her forehead sits high and right of centre"),
              b=dict(cam="held a little above her eye line and tilted down towards her forehead",
                     turn="her head square to the camera and tipped very slightly down",
                     dist="framed a little further back", place="her forehead sits low and left of centre")),
    "e": dict(side=SIDE_FRONT,
              a=dict(cam="held a little below her eye line and tilted up slightly",
                     turn="her head square to the camera, level",
                     dist="framed a little further back", place="her face sits centred and high"),
              b=dict(cam="held at her eye line",
                     turn="her head square to the camera, level",
                     dist="framed a little closer in", place="her face sits left of centre")),
    "f": dict(side=SIDE_LEFT,
              a=dict(cam="held at her eye line, out to her left",
                     turn="her head turned about twenty-five degrees to her own right, level",
                     dist="framed closer in", place="her forehead sits right of centre"),
              b=dict(cam="held a little above her eye line and out to her left, angled down",
                     turn="her head turned about thirty-five degrees to her own right, tipped very slightly down",
                     dist="framed a little further back", place="her forehead sits high and centred")),
}

# Gaze — the free axis. Subtle on four slots, noticeable on two (b, e): Malcolm's copper round
# asked for subtly different on all and noticeably different on about 30%.
GAZE = {
    "a": ("her eye looks straight ahead, just past the lens", "her eye looks a fraction to one side of the lens"),
    "b": ("her eyes are on the lens", "her eyes are well away from the lens, looking off to the side"),
    "c": ("her eyes are on the lens", "her eyes are a fraction above the lens"),
    "d": ("her eyes are just off the lens to one side", "her eyes are on the lens"),
    "e": ("her eyes are lowered, looking a little down and away", "her eyes are straight down the lens"),
    "f": ("her eyes are on the lens", "her eyes are a fraction off the lens, towards the far side"),
}

# --------------------------------------------------------------------------------------
# The six women. `before` is the specific description of what the fault looks like on HER - the
# highest-value string per slot, because a generic "eye bags" or "forehead lines" is where an
# engine substitutes its own stock face. Each carries a named mark as an identity anchor.
# --------------------------------------------------------------------------------------
WOMEN = [
    # ---- pdrn-undereye · Ye 2026 · Chinese, mean age 47.5 ---------------------------------
    dict(block="pdrn-undereye", key="a", crop="eye_tight", rooms=(0, 1),
         who=("a CHINESE woman of about forty-nine from Hangzhou, with shoulder-length straight black "
              "hair showing some grey at the parting, tucked behind her ear, fair skin with a cool "
              "undertone and a little faint redness across the cheek, dark brown eyes with single "
              "eyelids, natural unshaped brows, and one small flat brown mark on the cheekbone below "
              "the outer corner of her left eye"),
         before=("Under her left eye there is a soft, rounded, puffy bulge along the lower eyelid, full "
                 "enough to catch the light on its top and cast a small curved shadow beneath it. "
                 "Below and inside it a hollow groove runs down and outward from the inner corner of "
                 "the eye along the bone of the eye socket, holding its own soft shadow, so the "
                 "under-eye reads tired. Fine crinkled lines run across the thin skin of the lower "
                 "lid, and a few short creases fan from the outer corner.")),
    dict(block="pdrn-undereye", key="b", crop="half", rooms=(2, 3),
         who=("a CHINESE woman of about fifty-three from Guangzhou, with short black hair going grey "
              "at the temples, medium warm-toned skin with two small flat brown marks high on her "
              "right cheekbone, dark brown eyes with a narrow double-eyelid crease, and natural "
              "unshaped brows"),
         before=("Along her lower eyelid sits a distinct pouch of puffy skin, heavier towards the outer "
                 "half, with a soft crease beneath it where it meets the cheek. A clear hollow runs "
                 "from the inner corner of her eye diagonally down across the top of the cheek, deep "
                 "enough to hold a line of shadow. The skin of the lower lid is finely crinkled, and "
                 "there are established creases at the outer corner of the eye.")),
    dict(block="pdrn-undereye", key="c", crop="band", rooms=(4, 5),
         who=("a CHINESE woman of about forty-six from Beijing, with long straight dark brown hair "
              "pulled back in a low ponytail, fair neutral-toned skin with one tiny dark mole just "
              "below the outer corner of her left eye, dark brown eyes, and natural unshaped brows"),
         before=("Under both eyes there is a mild but definite puffiness along the lower lids - soft "
                 "rounded bulges that make her look tired - and beneath each one a shallow hollow "
                 "runs down from the inner corner of the eye, holding a faint shadow. The thin skin "
                 "of the lower lids has fine crinkled lines, and faint creases run from the outer "
                 "corners. Her two under-eyes look much like each other.")),
    # ---- argireline-forehead · Raikou 2017 · Athens, women 30-60 ---------------------------
    dict(block="argireline-forehead", key="d", crop="forehead_band", rooms=(6, 7),
         who=("a GREEK woman of about forty-eight from Athens, with almost-black hair clipped back off "
              "her face, warm olive skin, dark brown eyes, heavy dark brows, and a small mole just "
              "above the outer end of her right eyebrow"),
         before=("Three long horizontal lines run across her forehead for most of its width, the middle "
                 "one the deepest and slightly wavy, with a shorter broken fourth line near the "
                 "hairline. Between and along them the skin has a fine, dry, crosshatched surface "
                 "texture that shows where the grazing light catches it, with a few visible pores "
                 "above the brows. A faint pair of short vertical creases sits between the brows.")),
    dict(block="argireline-forehead", key="e", crop="upper_face", rooms=(8, 9),
         who=("a GREEK woman of about forty-two from Thessaloniki, with mid-brown hair tied back in a "
              "loose knot, fair skin with a light olive undertone, a few faint freckles across the "
              "bridge of her nose, hazel eyes and natural brows"),
         before=("Two horizontal lines run across her forehead - one long and clear across the middle, "
                 "one shorter and fainter above it - and the skin between and around them has a fine, "
                 "dry, slightly rough texture of tiny crisscrossing lines that shows where the light "
                 "grazes it. Pores are visible at the centre of the forehead.")),
    dict(block="argireline-forehead", key="f", crop="three_quarter", rooms=(10, 11),
         who=("a GREEK woman of about fifty-four from Crete, with dark brown hair greying at the "
              "temples and pulled back off her face, sun-weathered olive skin, brown eyes, thick "
              "natural brows, and a small mole just below her hairline on the left side of her "
              "forehead"),
         before=("Four horizontal lines cross her forehead, the lower two long and well cut, the upper "
                 "two shorter and broken, curving slightly downwards towards her left temple. The "
                 "whole forehead has a weathered, slightly rough, finely crosshatched surface from "
                 "years of sun, with visible pores along the brow.")),
]

# The light paragraph. The same grazing character on both days, and the guard that neither day is
# the kind one - on a volume subject soft frontal light makes a bag vanish by itself.
LIGHT = (
    "BOTH PICTURES ARE BRIGHT AND WELL EXPOSED, AND IN BOTH THE DAYLIGHT COMES FROM A WINDOW HIGH UP "
    "ON ONE SIDE AND GRAZES DOWN ACROSS HER FACE. This matters more than anything else about the "
    "lighting. The features this picture is about run ACROSS her face - lines across the forehead, "
    "the bulge along the lower eyelid, the groove beneath it - and they only show when the light "
    "crosses them from above: then every line, every bulge and every hollow casts its own small "
    "shadow downwards. Flat light from the front would wash all of it away and hide what the picture "
    "exists to show. Bright and clean, her eyes clearly visible and not lost in shadow, no dark room, "
    "no flash - but definitely DIRECTIONAL, with a lit side and a softer shaded side.\n\n"
    "⚠️ NEITHER DAY IS LIT MORE KINDLY THAN THE OTHER. The window is on a different side and the "
    "room is different, but the later picture is NOT lit more softly, more frontally or more evenly "
    "than the earlier one - the light grazes across her just as strongly on both days. If the later "
    "picture were lit more flatly, the improvement would simply be the light and the pair would be a "
    "lie."
)

SKIN = (
    "THE SKIN MUST HOLD UP AS REAL AND UNFLATTERED, and at this crop it is most of the picture. Pores "
    "are visible and vary in size by zone, several larger than their neighbours. Pigment is uneven "
    "and asymmetric, never mirrored from one side to the other. Fine vellus hairs catch the light. "
    "The skin is a little greasy at the nose and forehead and drier at the outer cheek. Real skin, "
    "photographed honestly, with no smoothing of any kind."
)


def build_prompt(w: dict) -> str:
    """Assemble one slot's full brief. Paragraph order is load-bearing: the honesty rules sit at
    paragraph 3, before the engine forms its own idea of what the improvement looks like."""
    b = BLOCKS[w["block"]]
    crop = CROPS[w["crop"]]
    v = VIEWPOINTS[w["key"]]
    g1, g2 = GAZE[w["key"]]
    r1, r2 = ROOMS[w["rooms"][0]], ROOMS[w["rooms"][1]]
    kind = "phone selfies" if crop["selfie"] else "close photographs"

    hands = (
        "IT MUST BE OBVIOUS AT A GLANCE THAT SHE TOOK THIS HERSELF - BUT THE PHONE AND HER HANDS ARE "
        "NEVER IN THE PICTURE. This is the view THROUGH the front camera of the phone she is holding, "
        "so the hand holding it cannot appear in its own frame, and neither can the phone. NO HAND, NO "
        "FINGERS, NO ARM, NO ELBOW, NO PHONE, NO PHONE CASE, NO MIRROR AND NO REFLECTION anywhere in "
        "either panel.\n\n"
        if crop["selfie"] else
        "NOTHING OF WHOEVER HELD THE CAMERA IS IN THE PICTURE - at this distance there is no room in "
        "the frame for it. No hand, no fingers, no arm, no phone, no phone case, no mirror and no "
        "reflection anywhere in either panel.\n\n"
    )

    return (
        # 1 — the frame. Panels described by position, never named with caption words.
        f"Two ordinary {kind} of THE SAME WOMAN, taken WEEKS APART at home, placed side by side to "
        "fill one square frame edge to edge: TWO PANELS OF EXACTLY EQUAL WIDTH meeting at one crisp "
        "vertical edge precisely at the centre, with no gap and no dividing line. Each panel is a tall "
        "portrait. The left panel is the earlier one, the right panel is the later one.\n\n"

        # 2 — expression: the confound on this card
        + b["expression"] + "\n\n"

        # 3 — honesty rules, hoisted
        "BEFORE ANYTHING ELSE, THE THINGS THAT MUST BE TRUE OF THE RIGHT-HAND PANEL, BECAUSE THEY ARE "
        "WHAT MAKE THIS PAIR HONEST RATHER THAN AN ADVERTISEMENT:\n\n"
        "ONE. EVERY MOLE, FRECKLE AND DISTINCT MARK SHE HAS IS STILL THERE IN THE RIGHT PANEL, in the "
        "same place, the same size and the same number. Her identity is anchored to those marks and "
        "they do not fade, move or vanish.\n\n"
        "TWO. SHE IS THE SAME PERSON, THE SAME AGE AND THE SAME COMPLEXION IN BOTH PANELS. She has not "
        "been made younger, slimmer, prettier, better groomed or lighter-skinned, and she wears no "
        "makeup on either day.\n\n"
        f"THREE. {b['honesty']}\n\n"

        # 4 — two occasions
        "THESE ARE TWO SEPARATE OCCASIONS, NOT TWO COPIES OF ONE FRAME. Everything that identifies her "
        "stays the same, and everything a different day would change is different.\n\n"

        # 5 — identity lock
        "UNMISTAKABLY THE SAME WOMAN: the same face shape, the same nose, the same eye shape and "
        "eyelids, the same eye colour, the same skin colour, the same brow shape, the same hair colour "
        "and cut, and her moles and marks in the same places on her skin.\n\n"

        # 6 — per-panel viewpoint
        "THE CAMERA IS IN A PLAINLY DIFFERENT PLACE ON THE TWO DAYS. Two photographs taken weeks apart "
        "are never framed the same way twice, and a pair framed identically reads as one picture "
        "retouched. So:\n\n"
        f"ON THE EARLIER DAY, IN THE LEFT PANEL: the camera is {v['a']['cam']}. She has "
        f"{v['a']['turn']}, and {g1}. She is {v['a']['dist']}, and {v['a']['place']} in the panel.\n\n"
        f"ON THE LATER DAY, IN THE RIGHT PANEL: the camera is {v['b']['cam']}. She has "
        f"{v['b']['turn']}, and {g2}. She is {v['b']['dist']}, and {v['b']['place']} in the panel.\n\n"
        "These differences must be obvious when the two halves are compared, not identical.\n\n"

        # 6b — the side lock
        f"BUT ONE THING ABOUT THE VIEW DOES NOT CHANGE. {v['side']}. THE SAME AREA OF SKIN MUST BE ON "
        "SHOW IN BOTH PANELS, because the whole point of the pair is to compare one patch of her face "
        "against the same patch weeks later. The camera moves; the part of her face it looks at does "
        "not.\n\n"

        # 7 — the distance and angle guard
        "AND THE CHANGE MUST NEVER BE EXPLAINABLE BY THE CAMERA. The skin this picture is about is "
        "FULLY AND EQUALLY READABLE IN BOTH PANELS - the same sharpness, the same level of detail. The "
        "later panel is not further away, softer, blurrier, lower in contrast or shot from a more "
        "flattering angle. If a viewer could say 'it only looks better because of the camera or the "
        "light', the picture has failed completely.\n\n"

        # 8 — two rooms
        f"THE TWO PLACES ARE DIFFERENT ROOMS. On the earlier day she is in an ordinary room with "
        f"{r1[0]} behind her and, far out of focus at one edge, {r1[2]}; the daylight comes from a "
        f"window {r1[1]}. On the later day she is in an ordinary room with {r2[0]} behind her and, "
        f"well out of focus at one edge, {r2[2]}; the daylight comes from a window {r2[1]}. At this "
        "distance only a sliver of each room shows, and apart from that one soft thing at the edge it "
        "is bare painted wall: no furniture, no pictures, no shelves, no window in shot, no clutter.\n\n"

        # 9 — also different
        "ALSO DIFFERENT BETWEEN THE TWO DAYS: her clothing, where any of it is in view - a different "
        "everyday garment in a different colour each time, nothing smart or styled; and her hair, the "
        "same cut and colour but arranged a little differently.\n\n"

        # 10 — hands and phone
        + hands +

        # 11 — the crop
        crop["text"] + "\n\n"

        # 12 — amateur tells (a line page, so the white-balance tell is allowed back)
        "IT IS AN AMATEUR PICTURE TAKEN AT HOME, NOT A PROFESSIONAL PHOTOGRAPH. The frame is a few "
        "degrees crooked and off-centre, the focus is good on the skin that matters but not perfect "
        "everywhere, there is a little noise in the shadows, and the indoor white balance is a little "
        "wrong - a little differently wrong on each day. Both pictures are nonetheless bright and "
        "cleanly exposed.\n\n"

        # 13 — the woman
        f"She is {w['who']}. She wears no makeup at all on either day - no foundation, no concealer, "
        "no powder, no mascara - her brows are natural and unshaped, and her hair is unstyled. She is "
        "an ordinary person, not a model, and neither picture makes any attempt to flatter her.\n\n"

        # 14 — age
        + b["age"] + "\n\n"

        # 15 — lighting and the no-kinder-light guard
        + LIGHT + "\n\n"

        # 16 — skin realism
        + SKIN + "\n\n"

        # 17 — the left panel
        + b["subject"] + w["before"] + "\n\n"

        # 18 — the right panel: floor and ceiling
        "ON THE LATER DAY, IN THE RIGHT PANEL: " + b["magnitude"] + "\n\n"

        # 19 — honesty restated at the point of change
        "AND AT THE SAME TIME, IN THAT SAME RIGHT PANEL: " + b["honesty"] + " Every mole and mark is "
        "still there in the same place. She has not been made younger, slimmer, prettier or better "
        "groomed, and she is wearing no makeup in either panel.\n\n"

        # 20 — the floor, last word
        "THERE MUST BE A VISIBLE DIFFERENCE BETWEEN THE TWO PANELS. This is the entire purpose of the "
        "pair. TWO PANELS THAT LOOK THE SAME ARE A COMPLETE FAILURE - and so are two panels that "
        "differ only because the camera or the light changed.\n\n"

        "An honest amateur snapshot, unretouched and completely unfiltered."
    )


def build_prompt_luma(w: dict) -> str:
    """Luma's short brief: under 6,000 characters or it returns a bare HTTP 422. Luma has no
    negative field, so everything load-bearing is stated positively. What is cut is the
    reasoning, never a constraint."""
    b = BLOCKS[w["block"]]
    crop = CROPS[w["crop"]]
    v = VIEWPOINTS[w["key"]]
    g1, g2 = GAZE[w["key"]]
    r1, r2 = ROOMS[w["rooms"][0]], ROOMS[w["rooms"][1]]
    kind = "phone selfies" if crop["selfie"] else "close photographs"
    return (
        f"Two ordinary {kind} of THE SAME WOMAN taken weeks apart at home, side by side filling one "
        "square frame: two panels of exactly equal width meeting at one crisp vertical edge at the "
        "centre. Left panel earlier, right panel later.\n\n"
        + b["expression"] + "\n\n"
        "THE RIGHT PANEL, BEFORE ANYTHING ELSE: every mole and mark still there in the same place; the "
        "same person, same age, same complexion, no makeup. " + b["honesty"] + "\n\n"
        "Two separate occasions, not two copies of one frame. Same face, nose, eye shape and eyelids, "
        "eye colour, skin colour, brows, hair colour and cut.\n\n"
        f"Earlier: camera {v['a']['cam']}; she has {v['a']['turn']}; {g1}; {v['a']['dist']}. "
        f"Later: camera {v['b']['cam']}; she has {v['b']['turn']}; {g2}; {v['b']['dist']}. "
        f"{v['side']}. The skin that matters is equally sharp and readable in both panels; the later "
        "one is not further away, softer or shot from a kinder angle.\n\n"
        f"Different rooms: earlier, {r1[0]} with {r1[2]} out of focus at one edge, daylight from a "
        f"window {r1[1]}. Later, {r2[0]} with {r2[2]} out of focus at one edge, daylight from a "
        f"window {r2[1]}. Bare painted walls otherwise. Different garment and hair arranged "
        "differently.\n\n"
        "Nothing of whoever held the camera is in shot: no hand, no fingers, no phone, no mirror.\n\n"
        + crop["text"] + "\n\n"
        "Amateur picture: a few degrees crooked, focus not perfect everywhere, a little shadow noise, "
        "white balance slightly off. Bright and cleanly exposed.\n\n"
        f"She is {w['who']}. No makeup at all, natural brows, unstyled hair. An ordinary person, not a "
        "model.\n\n"
        "Daylight from a window high up on one side grazes DOWN across her face on both days, so every "
        "line, bulge and hollow casts its own small shadow. Directional, bright, eyes clearly visible. "
        "The later day is NOT lit more softly or more frontally than the earlier one.\n\n"
        "Real unflattered skin: visible pores varying by zone, vellus hair, asymmetric pigment. No "
        "smoothing.\n\n"
        + b["subject"] + w["before"] + "\n\n"
        "IN THE RIGHT PANEL: " + b["magnitude"].split("\n\n")[0] + " Visible when the halves are "
        "compared, but modest - never a transformation.\n\n"
        "Two panels that look the same are a complete failure. Honest, unretouched, unfiltered."
    )


NEGATIVE_GLOBAL = (
    # Text — the whole label system depends on there being none in the pixels.
    "no text, no lettering of any kind, no words, no letters, no numbers, no percentages, no captions, "
    "no labels, no before and after wording, no watermark, no stock photo watermark, no printed text "
    "overlay, no logo, no signature, no timestamp, no date stamp, no arrows, no callout lines, no "
    "measurement scale, no grid overlay, "
    # Product and props.
    "no bottle, no jar, no dropper, no packaging, no product, no botanicals, no jewellery, no earrings, "
    "no spectacles, "
    # Makeup.
    "no makeup, no foundation, no powder, no concealer, no eyeliner, no mascara, no false lashes, "
    "no eyeshadow, no lipstick, no glitter, no specular speckle, no white flecks, "
    # Filtered skin.
    "no beauty-filter smoothing, no frequency separation, no airbrushed skin, no plastic skin, "
    "no waxy skin, no porcelain skin, no poreless skin, no uniform skin texture, no repeating texture "
    "pattern, no retouching, no skin smoothing filter, "
    # Medical territory this is not.
    "no wound, no bruise, no rash, no blood, no needle, no syringe, no injection, no drawn lines on "
    "the skin, no painted marks, no clinical disease, no lesion, "
    # Photographer's limbs and kit.
    "no hand, no fingers, no arm, no elbow, no phone, no smartphone, no selfie stick, no mirror, "
    "no reflection, "
    # Studio production values.
    "no studio backdrop, no seamless paper, no professional lighting, no softbox, no beauty dish, "
    "no ring light circle in the eyes, no fashion photograph, no glamour, no styled hair, no salon "
    "blow-dry, no bokeh portrait mode, no model, no supermodel, "
    # Exposure and places that turn up uninvited.
    "no dark room, no dim room, no murky lighting, no underexposed picture, no night, no camera "
    "flash, no flash shadow on a wall, no car interior, no bathroom, no tiled wall, no outdoors, "
    "no bookcase, no plant, no clutter, no busy background, no patterned wall, no wallpaper, "
    "no photographs on the wall, no posters, "
    # The diptych form itself.
    "no three panels, no four panels, no grid of panels, no picture frame, no border, no vignette, "
    "no gap between panels, no dividing line of any colour, no full body, no distant framing"
)

# The pair — shared by both blocks, then each block adds its own.
NEGATIVE_PAIR = (
    "no identical backgrounds between the panels, no same room in both panels, no identical framing "
    "between the panels, no copy of the left panel, no mirror image of the left panel, no flipped "
    "view, no different side of the face between the panels, no different woman between the panels, "
    "no younger woman in the right panel, no makeup appearing in the right panel, no change of skin "
    "colour between the panels, no moles disappearing between the panels, no zero difference between "
    "the panels, no softer light in the right panel, no flatter light in the right panel, no flat "
    "frontal lighting, no shadowless face, no blurrier right panel"
)


def main() -> None:
    slots = []
    for w in WOMEN:
        b = BLOCKS[w["block"]]
        prompt = build_prompt(w)
        prompt_luma = build_prompt_luma(w)
        assert len(prompt_luma) < LUMA_CAP, (
            f"{w['block']}-{w['key']}: luma prompt is {len(prompt_luma)} chars, cap is {LUMA_CAP}")
        # No digits anywhere in a prompt: a number in the brief is a number nbp_pro can print.
        assert not any(ch.isdigit() for ch in prompt + prompt_luma), f"{w['key']}: digit in prompt"
        slots.append({
            # Subject in the id (slot-letters-restart-per-wave): the short name on the sheet reads
            # "pdrn-undereye-b", never a bare letter.
            "id": f"uef--{w['block']}-{w['key']}",
            "title": (f"{w['block']} · {b['study']} · {CROPS[w['crop']]['label']} — "
                      f"{w['who'].split(',')[0].replace('a ', '', 1)}"),
            "class": "B",
            "width": SIZE,
            "height": SIZE,
            "target_slot": f"{b['page']} key_findings_ba {b['block']} ({b['heading']})",
            "ref_files": [],
            "prompt": prompt,
            "prompt_luma": prompt_luma,
            "label": {
                "left": "Before",
                "right": b["after_label"],
                "figure": "",
                "measure": "(labels are theme settings, never pixels)",
                "cite": b["study"],
            },
            "negative_extra": NEGATIVE_PAIR + ", " + b["negatives"],
        })

    cfg = {
        "wave": WAVE,
        "created": "2026-09-24",
        "doc": ("docs/clinical-trial-before-after-images.md, .claude/rules/website-imagery.md, "
                "built by scripts/build-under-eye-forehead-before-after-config.py"),
        "note": (
            "BEFORE/AFTER DIPTYCHS FOR TWO SCIENCE-PAGE CARDS. pdrn-undereye (slots a-c) -> "
            "/pages/pdrn-research key_findings_ba f4, 'Under-Eye Bags: About 2x the Retinol Change' "
            "(Ye 2026, split-face, 31 Chinese women 35-55, 0.1% PDRN eye cream vs retinol, 28 days, "
            "Antera 3D eye-bag volume and tear-trough depth ~2x the retinol change). "
            "argireline-forehead (slots d-f) -> /pages/acetyl-hexapeptide-8-research "
            "(templates/page.research-argireline.json) key_findings_ba f5, 'Forehead Roughness -7.4% "
            "by Day 20' (Raikou 2017, placebo-controlled, 24 women 30-60, 10% Argireline, Visioscan "
            "cR2). Both cards currently carry non-before/after images.\n\n"
            "CANDIDATES ONLY. Malcolm picks with _ / __ in place. Nothing here is uploaded.\n\n"
            "LIGHT: line/volume subjects, so the acetyl logic, not glutathione's flat light - but "
            "from HIGH on one side, grazing DOWN, because every feature on both cards is horizontal "
            "and pure sidelight runs along a horizontal line. Neither day may be lit more kindly, and "
            "every camera-height difference runs AGAINST the improvement (later under-eye panel level "
            "or lower; later forehead panel level or higher).\n\n"
            "CASTING follows the trial population: Chinese women on the PDRN card (as the live "
            "crow's-feet card on the same page), Greek women on the Argireline card (Raikou was run "
            "in Athens). No ethnicity bans in the negatives.\n\n"
            "MAGNITUDE: PDRN about a fifth (the paper gives only the 2x ratio; the same trial's "
            "crow's-feet change was ~20%). Argireline small and textural - 7.4% on a roughness "
            "measure; every line still there.\n\n"
            "FOR MALCOLM'S DECISION: slot pdrn-undereye-c is a frontal band showing BOTH under-eyes. "
            "Ye 2026 was split-face (PDRN one side, retinol the other), so a picture of both eyes "
            "improving illustrates using the cream rather than depicting the trial. Slots a and b "
            "lock one under-eye, as the live crow's-feet card does. Both are briefed to look alike in "
            "each panel so the picture can never read as PDRN side against retinol side.\n\n"
            "SUPPLIERS: all six (rule 1). Known risks from this brief family - check first: nbp_pro "
            "burns captions in; luma has returned HTTP 422 (prompt_luma is under the cap); flux2 went "
            "0/8 on glutathione and has drifted to a different, older woman."
        ),
        "target_templates": sorted({b["template"] for b in BLOCKS.values()}),
        "labels_are_composited": "NOT composited. Labels are text settings on the theme section.",
        "defaults": {
            "candidates": 1,
            "negative_global": NEGATIVE_GLOBAL,
            "negative_class_b": "",
        },
        "slots": slots,
    }

    OUT.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {OUT.relative_to(ROOT)} — {len(slots)} slots")
    for s in slots:
        print(f"  {s['id']:<32} prompt {len(s['prompt']):>5}  luma {len(s['prompt_luma']):>5}")
    print(f"  negative_global {len(NEGATIVE_GLOBAL)} chars")


if __name__ == "__main__":
    main()
