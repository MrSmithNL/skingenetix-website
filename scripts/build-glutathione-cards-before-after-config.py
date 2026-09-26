#!/usr/bin/env python3
"""Build the before/after wave for glutathione findings cards f1 and f2 (round 1, science-page template).

    python3 scripts/build-glutathione-cards-before-after-config.py
    → configs/banners/before-after-glutathione-cards-r1.json

    python3 scripts/generate-multi.py configs/banners/before-after-glutathione-cards-r1.json \
        --candidates 1 --only <slot-id>[,<slot-id>]

⚠️ `--candidates 1` IS NOT OPTIONAL: generate-multi.py never reads `defaults.candidates` and its flag
defaults to 2, which silently doubles the spend.

WHY THIS FILE HAS A NEW NAME. `scripts/build-glutathione-before-after-config.py` is the August builder
(r1/r2, commit db6001b): the tone-pair record the round-3 builder names as its structural source. It is
kept as it is, so this builder is named after the config it writes.

Malcolm, 2026-09-26 (register docs/claims/glutathione.md §8.7 decision 3): "New wave, all suppliers" - a
new before/after pair for each of the two Watanabe 2014 cards, with a subject who matches the trial.
§8.5 is the brief's source of truth, including "the picture must NOT show".

REUSE, NOT A COPY. The skeleton, the honesty rules, the identity lock, the side-lock wording, the
distance guard, the walls-not-rooms rule and the caption-bait guard come from the round-3 builder
(scripts/build-under-eye-forehead-before-after-config.py), and card f2 reuses the copper builder's
crow's-feet block and crops (scripts/build-copper-before-after-config.py; Malcolm picked its crow's-feet
A2 gpt_image). This file supplies the glutathione cards, the Filipino subjects, the viewpoints, and the
TONE-PAIR changes to the skeleton for f1.

THE TWO CARDS, AND WHAT EACH PICTURE MAY CLAIM (register §8.5)
  f1 tone        Watanabe 2014: 30 Filipino women aged 30-50 (mean 36), skin types III-IV, all "tan", even
                 colour at baseline; 2% GSSG lotion twice a day for 10 weeks, split-face; melanin index
                 -10.7% vs -3.1% placebo; the visible grade is "moderate", which the authors define as
                 less than 50% lightening. So: a MODEST, even, whole-cheek brightening; plainly the same
                 skin tone; NO change in evenness, spots, freckles, redness, pores, blemishes, texture or
                 lines; nothing that reads as bleaching. Site: the cheekbone.
  f2 crow's feet Same trial: a third of the women rated "moderate" improvement at the outer eye corner,
                 none on placebo. The SAME lines, a little shallower and softer, never erased; NO change
                 in tone or brightness between the panels (that is f1's result), eye bags, lids or brow;
                 the same neutral expression in both panels.
  Treated side   randomised per person, so the side varies by slot and is stated in picture terms.

WHAT CHANGES AGAINST THE ROUND-3 SKELETON, AND WHY
  1. f1 IS A TONE PAIR, SO FOUR SENTENCES OF THE SKELETON ARE SWAPPED (memory
     a-tone-pair-inverts-the-lighting-rule-of-a-wrinkle-pair). Raking light lays a shadow gradient
     across a cheek and a shadow gradient reads as darker skin, so the light is bright, soft and broad
     from roughly in front; rule TWO ("same complexion ... not lighter-skinned") would forbid the finding
     itself, so it is re-cut: plainly the same skin tone, and the face never lighter than the paler skin
     under her own jaw (the ceiling a viewer can check in the picture); rule FOUR (grazing light) becomes
     a MATCHING requirement for exposure and white balance, with the proof named - the whites of her eyes,
     her hair and her lips do not change. Each swap is an exact-string replacement that must match once,
     so a later edit to the round-3 text breaks this build loudly instead of silently.
  2. THE WHITE-BALANCE TELL GOES ON BOTH CARDS. "White balance a little differently wrong on each day"
     would be a tone change between the panels, which f2 may not show either. The amateur read is bought
     with framing instead (crooked, off eye level, imperfect focus, shadow noise).
  3. NO UNEVEN PIGMENT ANYWHERE (memory realism-marks-become-the-problem-on-a-pigmentation-page). Both
     cards sit on a brightening page, so the round-3 skin paragraph's "pigment is uneven" is replaced on
     both: realism comes from pores, vellus hair and fine lines, and each woman has ONE small, pale mark,
     away from the cheekbone, as her identity anchor.
  4. CASTING FOLLOWS THE TRIAL: Filipino women in their late thirties to early forties with medium, tan
     skin. The round-3 casting negative `no non-white model` is REMOVED from the global negatives (it would
     fight the brief), and the casting is stated positively.
  5. EVERY LIGHT OR ANGLE DIFFERENCE RUNS AGAINST THE IMPROVEMENT. f1: the left panel's light leans a
     little towards the near cheek, the right panel's is straight on or leans away, and her face is turned
     a touch LESS towards the camera in the right panel - so a brighter right cheek can never be the light.
     f2: both days' light falls from high on the near side; the right panel's is higher, which grazes the
     eye-corner lines harder, so softer lines can never be the light. Light sides are stated relative to
     the camera ("the side of her face nearest the camera"), never as her own left or right.
  6. WALLS ARE LIGHT NEUTRALS on both cards (whites, greys, one beige, one oatmeal): a saturated wall
     throws its colour onto the skin, which on this page is a tone difference the product did not cause.

SUPPLIERS: all six (website-imagery rule 1). Smoke-test one slot first.

SMOKE LOG, 2026-09-26 (slot a, f1 tone; 6 of 6 returned; gpt_image resolved to gpt-image-2.5-sunburst).
  HELD: no text on any tile; Filipino casting on five of six; the side-lock and the jaw mole on five of six;
  a plain wall on five of six.
  THREE BRIEF FAULTS, FIXED FOR SLOTS b-f (slot a is not re-run; its brief is at SMOKE_BRIEF):
    1. "SUN-DEEPENED TAN" DREW SUN DAMAGE. luma read it as mottled, freckled pigmentation across the cheek -
       the concern, not the result - and cleared much of it in the right panel; gpt_image's left panel
       carried more small dark speckles than its right. The word "sun" is gone from every prompt (asserted),
       and spots, freckles and patches are no longer NAMED in the positive text (naming draws them): the
       skin is described as "clear, even" instead. The names stay in the negatives.
    2. BARE SHOULDERS on nbp_pro and nbp_flash (both pulled back to head-and-shoulders, the known trait):
       she is now dressed, in a grey top one day and a navy top the other.
    3. NOTHING HELD THE SURFACE OR THE UNDERTONE. seedream's right panel went dewy and glowing; on five of six
       engines the right panel's skin lost red against blue (centre R/B about 1.7 -> 1.5), partly the finding
       (a lighter tan is less orange) but on gpt_image the whole left panel, eye whites included, was warmer.
       The honesty rule now says the surface looks just as it did (same slight oiliness, soft matte cheek,
       no new sheen) and the magnitude says the undertone does not shift (not pinker, greyer or cooler).
  KNOWN SUPPLIER TRAITS, NOT BRIEF FAULTS: flux2 cast a pale, older East Asian woman with spot clusters and
  mirrored the pair (its 0/8 tone-pair record); luma and nbp_flash framed the pair with a white border (Luma
  now gets an edge-to-edge sentence, since it sees no negatives); no engine honoured the close crop.

FULL WAVE, 2026-09-26: 35 of 36 (slots b-f on the revised brief). luma refused slot f: HTTP 422
content_moderated (body read on a second, identical call; 5,192 characters, so not the length cap).
Sheet: ~/Desktop/skingenetix-glutathione-before-after-r1.png (rows A-F from this config, stable labels).
  STILL OPEN AFTER THE REVISION: the right panel of a crow's-feet pair still came back lighter on nbp_pro
  and nbp_flash (d, f) - f1's result leaking into f2; seedream drew crow's feet as black ink strokes (d) and
  winged eyeliner (e); luma and the two nbp engines still bordered most pairs; flux2 stayed pale and older
  on every slot. gpt_image held casting, side, anchors and matched colour most often.
Author: Claude Code, 2026-09-26. Candidates only; nothing is uploaded or published by this file.
"""
import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


r3 = _load("r3", "scripts/build-under-eye-forehead-before-after-config.py")
copper = _load("copper", "scripts/build-copper-before-after-config.py")

WAVE = "before-after-glutathione-cards-r1"
OUT = ROOT / "configs" / "banners" / f"{WAVE}.json"
ROUND = "r1"
SMOKE_SLOTS = {"a"}
#: slot a ran on the smoke brief; that config is preserved beside its candidates (the run folder is
#: gitignored, so the brief's differences are also listed in SMOKE LOG below).
SMOKE_BRIEF = "assets/ai-generated/2026-08-22-multi-before-after-glutathione-cards-r1/smoke-brief-r1-a.json"
PAGE = "/pages/glutathione-research"
TEMPLATE = "templates/page.glutathione-research.json"

# --------------------------------------------------------------------------------------
# Walls, one pair per slot, stated per panel. Light neutrals only (docstring point 6). The light
# direction is part of the wall entry because the skeleton reads it from there.
# --------------------------------------------------------------------------------------
NEAR = "the side of her face nearest the camera"
FAR = "the far side of her face"
WALLS = [
    # f1 tone - soft, broad, from roughly in front; left panel leans to the near cheek
    ("a plain CHALK WHITE painted wall", f"in front of her, softly, leaning a little towards {NEAR}"),     # 0 a-L
    ("a plain PALE GREY painted wall", "straight in front of her and a little above, softly"),            # 1 a-R
    ("a plain OFF-WHITE painted wall", f"in front of her, softly, leaning a little towards {NEAR}"),       # 2 b-L
    ("a plain LIGHT STONE-GREY painted wall", "straight in front of her and a little above, softly"),     # 3 b-R
    ("a plain SOFT WHITE painted wall", "straight in front of her and a little above, softly"),           # 4 c-L
    ("a plain PALE DOVE-GREY painted wall", f"in front of her, softly, leaning a little towards {FAR}"),   # 5 c-R
    # f2 crow's feet - from high on the near side on both days; the right panel's from higher still
    ("a plain WARM WHITE painted wall", f"high up on {NEAR}"),                                            # 6 d-L
    ("a plain PALE GREY painted wall", f"above her, a little towards {NEAR}"),                            # 7 d-R
    ("a plain SOFT BEIGE painted wall", f"high up on {NEAR}"),                                            # 8 e-L
    ("a plain OFF-WHITE painted wall", f"above her, a little towards {NEAR}"),                            # 9 e-R
    ("a plain PALE OATMEAL painted wall", f"high up on {NEAR}"),                                          # 10 f-L
    ("a plain LIGHT STONE-GREY painted wall", f"above her, a little towards {NEAR}"),                     # 11 f-R
]

# --------------------------------------------------------------------------------------
# Crops. f1 keeps the underside of her jaw in frame: it is the reference a viewer checks the ceiling
# against (her face is never lighter than it). f2 reuses copper's three crow's-feet crops unchanged.
# Engines pull tight crops back to a portrait (engines-return-a-portrait-whatever-crop-you-ask-for):
# crop the winner in post.
# --------------------------------------------------------------------------------------
CROPS = {
    "tone_three_quarter": dict(
        selfie=True, label="close three-quarter, cheekbone and jaw",
        text=("HER FACE FILLS THE PANEL, IN A CLOSE THREE-QUARTER VIEW. The phone is so close that the top of "
              "her head is cut off: the frame runs from her eyebrows at the top down to just below her jaw at "
              "the bottom, where a little of the underside of her jaw and the top of her neck show. THE NEAR "
              "CHEEK AND CHEEKBONE are the largest things in the picture and sit in the middle of the panel; "
              "the far side of her face turns away. THE COLOUR AND BRIGHTNESS OF THE SKIN ACROSS HER NEAR "
              "CHEEKBONE are what the picture is of, with the paler skin under her jaw just in view below it. "
              "The plain wall shows only as a narrow strip beside the back of her head."),
    ),
    "tone_cheek": dict(
        selfie=False, label="one cheek, close",
        text=("HER NEAR CHEEK FILLS THE PANEL. The frame runs from her eyebrow at the top down to just below her "
              "jawline at the bottom, and across from the side of her nose to her ear and the edge of her hair. "
              "Only one eye is in the picture. Skin fills almost the whole panel, with at most a thin sliver of "
              "plain wall past her hair at one edge. THE SKIN OVER HER CHEEKBONE sits in the middle of the panel "
              "and is what the picture is of; a little of the underside of her jaw shows along the bottom edge. "
              "An ordinary close photograph taken at home, sharp across the cheek - not a studio or clinical "
              "photograph."),
    ),
    "tone_face": dict(
        selfie=True, label="close three-quarter, whole face",
        text=("HER FACE FILLS THE PANEL, IN A CLOSE THREE-QUARTER VIEW. The frame runs from her hairline at the "
              "top down to just below her chin, where the top of her neck shows, with her ears at or past the "
              "side edges. Her face is turned far enough that her far cheek is mostly hidden beyond the line of "
              "her nose, so the NEAR CHEEK AND CHEEKBONE are the largest area of skin in the picture. THE COLOUR "
              "AND BRIGHTNESS OF THAT CHEEK, seen against the paler skin under her jaw and on her neck, are what "
              "the picture is of. The plain wall shows only as a narrow strip beside her head."),
    ),
    "cf_three_quarter": copper.CROPS["cf_three_quarter"],
    "cf_eye_corner": copper.CROPS["cf_eye_corner"],
    "cf_steep": copper.CROPS["cf_steep"],
}

# --------------------------------------------------------------------------------------
# The two blocks. f2 is copper's crow's-feet block with the trial-specific fields replaced.
# --------------------------------------------------------------------------------------
_CU = copper.BLOCKS["copper-crowsfeet"]

BLOCKS = {
    "f1-tone": dict(
        page=PAGE, template=TEMPLATE, block="f1", heading="Brighter-Looking Skin: Pigment -10.7% in 10 Weeks",
        study="watanabe-2014", after_label="After 10 weeks", kind="tone",
        expression=("Her face is at rest on both days: eyes open normally, mouth closed and relaxed, lips "
                    "together, NOT SMILING. A smile lifts and rounds the cheek and catches the light differently "
                    "on it, so a smile in one panel and not the other would change the very skin being compared - "
                    "her cheeks are in the same relaxed resting state in both panels. No hand touches her face."),
        honesty=("THE CHANGE IS IN BRIGHTNESS ONLY, NOT IN EVENNESS, TEXTURE OR SHEEN. Her skin was already one "
                 "clear, even colour in the left panel and it is exactly as clear and even in the right, and her "
                 "pores, her skin texture and the fine lines at the corner of her eye are exactly the same. The "
                 "surface of her skin looks just as it did - the same slight oiliness at the nose, the same soft "
                 "matte cheek, no new sheen or glow. What has changed is that the whole "
                 "cheek is a shade lighter and brighter, evenly across it - but she is PLAINLY THE SAME MEDIUM, "
                 "TAN-SKINNED WOMAN, with the same warm undertone, and the skin of her face is never lighter than "
                 "the paler skin under her jaw."),
        luma_honesty=("Her skin is exactly as clear and even as in the left panel, with the same pores, texture, "
                      "lines and the same soft matte surface. Plainly the same medium, tan-skinned woman with "
                      "the same warm undertone."),
        luma_magnitude=("The whole cheek is a shade lighter and brighter, evenly, as if a little of her tan has "
                        "lifted, with the same warm golden undertone - about a third of the way towards the paler skin under her jaw, never half. "
                        "Still one even colour. Anyone seeing this panel alone would still say she has medium, "
                        "tan skin."),
        # Luma's short forms (its 6,000-character cap): the same constraints, without the reasoning.
        luma_expression=("Her face is at rest on both days: eyes open, mouth closed and relaxed, not smiling, her "
                         "cheeks relaxed the same way in both panels. No hand touches her face."),
        luma_nothing_else=("Nothing but the brightness of her face skin has changed: pores, texture, lines, "
                           "under-eyes, lips, the whites of her eyes, brows and hair are the same, and the skin "
                           "under her jaw and on her neck is the same colour in both panels."),
        feature=("HER TAN IS ONE CLEAR, EVEN, UNIFORM COLOUR ACROSS THE WHOLE CHEEK, soft and natural. It reads by "
                 "its overall colour alone."),
        nothing_else=("NOTHING BUT THE BRIGHTNESS OF THE SKIN OF HER FACE HAS CHANGED. Her pores, her skin "
                      "texture, the fine lines at the corner of her eye and beside her mouth, the skin under her "
                      "eyes, her lips, the whites of her eyes, her brows and her hair look exactly the same in both "
                      "panels, and the skin under her jaw and down her neck is exactly the same colour in both."),
        age=("SHE IS IN HER LATE THIRTIES OR EARLY FORTIES, AND THAT GOVERNS WHAT HER SKIN CAN HONESTLY LOOK LIKE. "
             "Fine lines are starting at the outer corners of her eyes, and hers is the everyday skin of a woman "
             "who works indoors and out. She is NOT young - clearly not in her twenties - and NOT old: no deep "
             "lines, no sagging, no slackness."),
        subject=("IN THE LEFT PANEL, THE COLOUR AND BRIGHTNESS OF THE SKIN ACROSS HER NEAR CHEEKBONE ARE THE "
                 "SUBJECT OF THE PICTURE. "),
        magnitude=("THE SKIN OF HER FACE IS A SHADE LIGHTER AND BRIGHTER IN THE RIGHT PANEL, EVENLY ACROSS THE "
                   "WHOLE CHEEK AND CHEEKBONE, as if a little of her tan has lifted. It has moved about A THIRD "
                   "OF THE WAY from its tan towards the paler skin under her jaw - never as much as half the way - "
                   "so it is still plainly deeper than the skin under her jaw. It looks a little clearer and "
                   "livelier, less dull. It is still one even colour, exactly as even as it was. THE UNDERTONE DOES "
                   "NOT SHIFT: the lighter skin is the same warm golden-brown, only lighter - not pinker, not "
                   "greyer, not cooler.\n\n"
                   "THE SIZE OF THE CHANGE IS NARROW AT BOTH ENDS. It must be VISIBLE: someone comparing the two "
                   "panels should see that her cheek is a little brighter in the right one and be able to point "
                   "to where. But it is MODEST: anyone looking at the right panel on its own would still say this "
                   "woman has medium, tan skin. She has not become a fairer, paler or different-looking person, "
                   "and her skin has not turned pale, chalky or ashen. A right panel in which she looks "
                   "fair-skinned is a failure, not a success."),
        negatives=("no smiling, no squinting, no hand on the face, no foundation, no tinted moisturiser, no colour "
                   "correcting makeup, no skin whitening, no bleached skin, no chalky white skin, no pale skin in "
                   "the right panel, no fair-skinned woman in the right panel, no grey pallor, no ashen skin, no "
                   "different ethnicity between the panels, no different undertone between the panels, no pink "
                   "skin in the right panel, no change of neck colour between the panels, no lighter neck in the "
                   "right panel, no dark spots, no melasma, no patches of pigmentation, no blotchy skin, no "
                   "freckles on the cheek, no sun spots on the cheek, no acne, no pimples, no blemishes, no "
                   "redness, no flushed cheeks, no rosy cheeks in the right panel, no smoother skin in the right "
                   "panel, no smaller pores in the right panel, no fewer lines in the right panel, no dewy glow in "
                   "the right panel, no shinier skin in the right panel, no highlighter, no glow filter, no mole "
                   "disappearing between the panels, no hard raking sidelight, no strong shadow gradient across "
                   "the cheek, no shadow across the cheek, no different exposure between the panels, no different "
                   "white balance between the panels, no warm cast on one panel only, no cool cast on one panel "
                   "only, no colour cast, no orange cast, no blue cast, no yellow cast, no green cast, "
                   "no woman under thirty, no woman over fifty, no elderly woman"),
    ),
    "f2-crowsfeet": dict(
        _CU,
        page=PAGE, template=TEMPLATE, block="f2", heading="Softer-Looking Crow's Feet: 1 in 3 Women, None on Placebo",
        study="watanabe-2014", after_label="After 10 weeks", kind="wrinkle",
        # §8.5: "the SAME lines, a little shallower and softer, never erased". Copper's magnitude, honesty,
        # expression and feature carry that exactly and are kept; only the parts that name copper's trial
        # population or leave tone unguarded are replaced.
        nothing_else=("NOTHING OUTSIDE THE EYE CORNER HAS CHANGED, AND HER SKIN IS EXACTLY THE SAME COLOUR AND "
                      "BRIGHTNESS IN BOTH PANELS. Her forehead, her brows, her eyelids, the skin and the soft "
                      "fullness under her eyes, the lines beside her nose and mouth, her cheeks and her jaw look "
                      "exactly the same in both panels, and her skin is the same shade, not brighter or clearer, "
                      "in the right one; only the lines at the outer corner of her eye are different."),
        age=("SHE IS IN HER LATE THIRTIES OR EARLY FORTIES, AND THAT GOVERNS WHAT HER SKIN CAN HONESTLY LOOK LIKE. "
             "The lines at the corners of her eyes are fine but established - they stay with her face at rest, "
             "from years of everyday expressions - and the skin there is thin and finely crinkled. She is "
             "NOT old: no deep folds, no hooded drooping lids, no heavy bags; and not young either - clearly not "
             "in her twenties."),
        luma_expression=("Her face is at rest and the same in both panels: eyes open normally, mouth closed, NOT "
                         "smiling and NOT squinting - either one creases the eye corner by itself."),
        luma_nothing_else=("Nothing outside the eye corner has changed, and her skin is exactly the same colour and "
                           "brightness in both panels; only the eye-corner lines differ."),
        negatives=(_CU["negatives"].replace(", no woman under forty, no elderly woman", "") +
                   ", no brighter skin in the right panel, no lighter skin in the right panel, no change of skin "
                   "tone between the panels, no different white balance between the panels, no warm cast on one "
                   "panel only, no cool cast on one panel only, no lifted brow in the right panel, no different "
                   "eyelid between the panels, no dark spots, no melasma, no blotchy skin, no freckles on the "
                   "cheek, no acne, no woman under thirty, no woman over fifty, no elderly woman"),
    ),
}
assert "no woman under forty" not in BLOCKS["f2-crowsfeet"]["negatives"], "copper's age negative survived"

# --------------------------------------------------------------------------------------
# Viewpoints. Side varies by slot (Watanabe randomised the treated side per person), stated in picture
# terms. Every difference runs AGAINST the improvement (docstring point 5).
# --------------------------------------------------------------------------------------
R, L = r3.SIDE_NOSE_RIGHT, r3.SIDE_NOSE_LEFT
VIEWPOINTS = {
    # f1 tone - right panel turned a touch LESS towards the camera, so the near cheek faces the light less
    "a": dict(side=R,
              a=dict(cam="held at her eye line, a little off to the side",
                     turn="her face turned about thirty degrees towards the right-hand edge of the picture, level",
                     dist="framed very close", place="her near cheekbone sits centred and a little high"),
              b=dict(cam="held just above her eye line and angled slightly down",
                     turn="her face turned about twenty-five degrees towards the right-hand edge of the picture, level",
                     dist="framed a touch less close, but still close", place="her near cheekbone sits slightly left of centre")),
    "b": dict(side=L,
              a=dict(cam="held at her cheekbone level, a hand's width from her face",
                     turn="her face turned about thirty-five degrees towards the left-hand edge of the picture, level",
                     dist="framed very close", place="the cheekbone sits centred"),
              b=dict(cam="held a little above her cheekbone level and angled slightly down",
                     turn="her face turned about thirty degrees towards the left-hand edge of the picture, level",
                     dist="framed a touch closer still", place="the cheekbone sits a little low and right of centre")),
    "c": dict(side=R,
              a=dict(cam="held a little above her eye line and angled slightly down",
                     turn="her face turned about thirty-five degrees towards the right-hand edge of the picture, chin level",
                     dist="framed close", place="her face sits centred"),
              b=dict(cam="held at her eye line",
                     turn="her face turned about thirty degrees towards the right-hand edge of the picture, chin level",
                     dist="framed a touch closer", place="her face sits a little left of centre")),
    # f2 crow's feet - right panel level or a touch LOWER (copper's rule)
    "d": dict(side=L,
              a=dict(cam="held just above her eye line and a little off to the side, angled slightly down",
                     turn="her face turned about twenty-five degrees towards the left-hand edge of the picture, level",
                     dist="framed very close", place="the corner of her near eye sits high and slightly right of centre"),
              b=dict(cam="held at her eye line, off to the same side",
                     turn="her face turned about thirty degrees towards the left-hand edge of the picture, level",
                     dist="framed a touch less close, but still close", place="the corner of her near eye sits centred")),
    "e": dict(side=R,
              a=dict(cam="held at her eye line, a hand's width from the outer corner of her right eye",
                     turn="her face turned about thirty degrees towards the right-hand edge of the picture, level",
                     dist="framed very close", place="the eye corner sits high and left of centre"),
              b=dict(cam="held just below her eye line and tilted up slightly",
                     turn="her face turned about thirty-five degrees towards the right-hand edge of the picture, level",
                     dist="framed a touch closer still", place="the eye corner sits centred and a little low")),
    "f": dict(side=L,
              a=dict(cam="held at her eye line, well out to the side",
                     turn="her face turned about forty-five degrees towards the left-hand edge of the picture, level",
                     dist="framed close", place="her near eye sits high and right of centre"),
              b=dict(cam="held a little below her eye line, well out to the same side, tilted up",
                     turn="her face turned about fifty degrees towards the left-hand edge of the picture, level",
                     dist="framed a touch closer", place="her near eye sits centred")),
}
# Gaze is the free axis: subtle on four slots, noticeable on two (a, e).
GAZE = {
    "a": ("her eyes are on the lens", "her eyes look a little away from the lens, off to the side"),
    "b": ("her eye looks straight ahead, just past the lens", "her eye looks a fraction to one side of the lens"),
    "c": ("her eyes look ahead, past the camera", "her eyes glance a little towards the lens"),
    "d": ("her eyes are on the lens", "her eyes are a little off the lens, towards the far side"),
    "e": ("her eye looks straight ahead, just past the lens", "her eye looks a little down and away"),
    "f": ("her eyes are just off the lens to one side", "her eyes are on the lens"),
}

# --------------------------------------------------------------------------------------
# The six women: Filipino, late thirties to early forties, medium tan skin (types III-IV, described in
# words - a roman numeral is text an engine can print). One small, pale, flat mole each, on the side
# her crop shows and away from the cheekbone: the identity anchor.
# --------------------------------------------------------------------------------------
WOMEN = [
    # ---- f1 tone · Watanabe 2014 · cheekbone ----------------------------------------------
    dict(block="f1-tone", key="a", crop="tone_three_quarter", walls=(0, 1),
         who=("a FILIPINO woman of about thirty-nine, with straight black shoulder-length hair tucked behind her "
              "ear, medium tan skin - a warm golden light-brown - dark brown "
              "eyes, natural dark brows, and one small flat pale-brown mole on the right side of her jaw, just "
              "below her right ear"),
         before=("Across her near cheek and cheekbone the skin is one clear, even tan - a uniform warm "
                 "light-brown all over - a shade deeper and a little duller than the "
                 "paler, shaded skin under her jaw and down the front of her neck. The colour is the same all "
                 "over the cheek; it simply sits a shade darker and flatter than her own untanned skin.")),
    dict(block="f1-tone", key="b", crop="tone_cheek", walls=(2, 3),
         who=("a FILIPINO woman of about forty-two, with black hair showing a few grey strands, pulled back in a "
              "low ponytail, medium tan skin - a warm light-to-mid brown with a golden undertone, evenly "
              "and clear - dark brown eyes, and one small flat pale-brown mole on her left temple at the "
              "hairline"),
         before=("The skin over her near cheekbone is an even, uniform tan, the same warm light-to-mid brown all "
                 "across it, clear and smooth-toned. It reads a shade deeper and a little less bright than the "
                 "skin under her jaw.")),
    dict(block="f1-tone", key="c", crop="tone_face", walls=(4, 5),
         who=("a FILIPINO woman of about thirty-seven, with dark brown-black hair cut to the jaw, a round face, "
              "medium-deep tan skin - a warm mid-brown with a golden undertone, clear and even - dark "
              "brown eyes, and one small flat pale-brown mole high on her right temple near the hairline"),
         before=("Her face carries an even tan: the near cheek and cheekbone are one clear, uniform warm "
                 "mid-brown, a shade deeper and a little duller than the paler skin "
                 "under her chin and on her neck.")),
    # ---- f2 crow's feet · Watanabe 2014 · outer eye corner ---------------------------------
    dict(block="f2-crowsfeet", key="d", crop="cf_three_quarter", walls=(6, 7),
         who=("a FILIPINO woman of about forty-three, with black shoulder-length hair with a few grey strands, "
              "tucked behind her ear, medium tan skin with a warm golden undertone, dark brown eyes, natural dark "
              "brows, and one small flat pale-brown mole on her left temple beside the end of her eyebrow"),
         before=("At the outer corner of the near eye a fan of four or five fine lines spreads out towards the "
                 "temple, the middle two the longest and clearest, one curving up towards the end of the brow and "
                 "one running down towards the top of the cheek. The thin skin between them is finely crinkled, "
                 "and each line casts a small shadow where the light grazes it.")),
    dict(block="f2-crowsfeet", key="e", crop="cf_eye_corner", walls=(8, 9),
         who=("a FILIPINO woman of about forty, with long straight black hair pulled back into a loose bun, medium "
              "tan skin - a warm light-brown with a golden undertone - dark brown eyes, and one tiny flat "
              "pale-brown mole on her right temple near the hairline"),
         before=("From the outer corner of her right eye three clear fine lines fan out across the temple, with a "
                 "few shorter, finer ones between them and a faintly crinkled texture over the area. The longest "
                 "reaches about halfway to her hairline.")),
    dict(block="f2-crowsfeet", key="f", crop="cf_steep", walls=(10, 11),
         who=("a FILIPINO woman of about forty-one, with wavy black hair to the shoulder pulled loosely back, "
              "medium-deep tan skin with a warm undertone, dark brown eyes, and one small flat pale-brown mole on "
              "her left cheek just in front of her ear, low and well away from the cheekbone"),
         before=("Seen from the side, a clear fan of fine lines spreads from the outer corner of the near eye "
                 "across the side of her face, three of them longer, with finer crinkles between them and a "
                 "couple of short lines running down towards the cheekbone.")),
]

# --------------------------------------------------------------------------------------
# Light and skin paragraphs, per card.
# --------------------------------------------------------------------------------------
LIGHT_TONE = (
    "THE LIGHT ON BOTH DAYS IS BRIGHT, SOFT AND BROAD, AND IT FALLS ON HER FROM ROUGHLY IN FRONT. This matters "
    "more than anything else about the lighting, and it is the opposite of what a picture about wrinkles would "
    "want: hard light raking across a cheek lays down a gradient of shadow, and a gradient of shadow looks "
    "exactly like a patch of darker skin, so it would invent a difference in colour that is not in her skin. "
    "Soft light from the front lights the skin evenly and lets its real colour be seen. Bright, clean and well "
    "exposed, no dark room, no heavy shadow across her face, no flash. The direction of the daylight differs a "
    "little between the two days, as the wall does.\n\n"
    "⚠️ THE TWO DAYS ARE LIT AND EXPOSED THE SAME. The brightness and softness of the light, the exposure of "
    "the picture and the colour of the light are the same in both panels. The right-hand picture is NOT "
    "exposed brighter, lit more strongly, lit more from the front, or warmer or cooler than the left-hand one, "
    "and its light does not favour her near cheek more. THE PROOF IS IN WHAT DOES NOT CHANGE: the whites of her "
    "eyes, the black of her hair, her brows and the colour of her lips look exactly the same in both panels. "
    "Only the skin of her face is a shade brighter. If the whole right-hand picture were brighter, the "
    "improvement would simply be the exposure and the pair would be a lie."
)
# Copper's paragraph, but its light changes SIDE between the days; here both days light the near side
# (the eye corner must not fall into the shaded side on either day) and the height changes instead.
_OLD_SIDE = "The light comes from a different side and the wall is different"
assert copper.LIGHT.count(_OLD_SIDE) == 1, "copper LIGHT paragraph changed"
LIGHT_WRINKLE = copper.LIGHT.replace(
    _OLD_SIDE, "On both days the light falls on the side of her face nearest the camera, from a slightly "
               "different height, and the wall is different")

SKIN_GLUT = (
    "THE SKIN MUST HOLD UP AS REAL AND UNFLATTERED, and at this crop it is most of the picture. Pores are "
    "clearly visible and vary in size by zone - open across the nose and inner cheek, finer at the temple - "
    "several larger than their neighbours. Fine vellus hairs catch the light along the cheek and jaw. The skin "
    "is a little greasy at the nose and forehead and drier at the outer cheek. HER SKIN COLOUR IS CLEAR AND "
    "EVEN: one smooth, uniform colour across her cheeks and her whole face, and the one small, pale mole she "
    "has sits well away from her cheekbone. Real skin, photographed honestly, with no "
    "smoothing of any kind."
)

# --------------------------------------------------------------------------------------
# Exact-string swaps into the round-3 skeleton (docstring points 1-3). Each must match exactly once.
# --------------------------------------------------------------------------------------
R3_AMATEUR = (
    "IT IS AN AMATEUR PICTURE TAKEN AT HOME, NOT A PROFESSIONAL PHOTOGRAPH. The frame is a few degrees crooked "
    "and off-centre, the focus is good on the skin that matters but not perfect everywhere, there is a little "
    "noise in the shadows, and the indoor white balance is a little wrong - a little differently wrong on each "
    "day. Both pictures are nonetheless bright and cleanly exposed.")
AMATEUR_NEUTRAL = (
    "IT IS AN AMATEUR PICTURE TAKEN AT HOME, AND THE TELLS ARE IN THE FRAMING, NOT IN THE COLOUR. The frame is a "
    "few degrees crooked and off-centre, the camera is not quite at eye level, the focus is good on the skin "
    "that matters but not perfect everywhere, and there is a little noise in the shadows. BUT BOTH PICTURES ARE "
    "BRIGHT, CLEANLY EXPOSED AND NEUTRAL IN COLOUR, AND THEY MATCH EACH OTHER: no orange indoor cast, no blue "
    "cast, no filter, nothing warmer or cooler in one panel than in the other. A colour difference between the "
    "panels would read as a change in her skin tone.")
# Smoke: nbp_pro and nbp_flash pulled back to head-and-shoulders with BARE shoulders - the skeleton only
# said "if any of her clothing shows". Clothing is now stated, in muted neutrals (a bright top throws
# colour onto the jaw, which on this page is a tone change the product did not cause).
R3_P9 = ("ALSO DIFFERENT BETWEEN THE TWO DAYS: her hair, the same cut and colour but falling or tied a little "
         "differently; and, if any of her clothing shows at the very bottom edge, a different everyday top in a "
         "different colour.")
P9_DRESSED = ("SHE IS DRESSED ON BOTH DAYS, in a plain everyday round-necked top in a muted colour - a grey one on "
              "one day and a navy one on the other. Wherever the picture reaches down far enough, the top is "
              "plainly there at the bottom edge; her shoulders are never bare. ALSO DIFFERENT BETWEEN THE TWO DAYS: "
              "her hair, the same cut and colour but falling or tied a little differently.")
# These women have no freckles, and a named noun gets drawn (describe-the-thing-dont-name-it).
R3_MARKS = ("ONE. EVERY MOLE, FRECKLE AND DISTINCT MARK SHE HAS IS STILL THERE", "ONE. EVERY MOLE AND DISTINCT MARK "
            "SHE HAS IS STILL THERE")
SWAPS_BOTH = [(R3_AMATEUR, AMATEUR_NEUTRAL), (R3_P9, P9_DRESSED), R3_MARKS]
SWAPS_TONE = SWAPS_BOTH + [
    ("TWO. SHE IS THE SAME PERSON, THE SAME AGE AND THE SAME COMPLEXION IN BOTH PANELS. She has not been made "
     "younger, slimmer, prettier, better groomed or lighter-skinned, and she wears no makeup on either day.",
     "TWO. SHE IS THE SAME PERSON, THE SAME AGE AND PLAINLY THE SAME SKIN TONE IN BOTH PANELS - the same medium, "
     "tan complexion with the same warm undertone. She has not been made younger, slimmer, prettier or "
     "better groomed, she has not become a paler or fairer person, and she wears no makeup on either day."),
    ("FOUR. THE RIGHT PANEL IS NOT LIT MORE KINDLY. It is not brighter, softer, warmer or more frontally lit "
     "than the left: in both, daylight grazes down across her from high on one side, equally strongly. If the "
     "right panel were lit more kindly, the improvement would just be the light.",
     "FOUR. THE TWO PANELS MATCH EACH OTHER FOR LIGHT, EXPOSURE AND COLOUR BALANCE. In both, bright, soft, broad "
     "daylight falls on her face from roughly in front, equally bright, and the white balance is the same - "
     "neither panel is warmer, cooler, pinker, greener or more yellow than the other, and neither is exposed "
     "brighter. The whites of her eyes, her hair and her lips look exactly the same in both. If one panel were "
     "lit, exposed or tinted differently, the difference in her skin would just be the light."),
    # the identity lock: "the same skin colour" would forbid the finding; the TYPE and undertone are what stay
    ("the same eye colour, the same skin colour, the same brow shape",
     "the same eye colour, the same skin type and undertone, the same brow shape"),
    ("Every mole and mark is still there in the same place, and the light is no kinder than in the left panel.",
     "Every mole and mark is still there in the same place, and the light is no kinder than in the left panel: "
     "the two panels match each other exactly for exposure and colour balance."),
]
LUMA_AMATEUR = ("Amateur picture: a little crooked, focus not perfect, white balance slightly off, but bright.",
                "Amateur picture: a little crooked, not quite at eye level, focus not perfect - but bright, cleanly "
                "exposed and neutral in colour, and the two panels match for colour balance.")
LUMA_SKIN = ("Real skin: visible pores, vellus hair, uneven pigment. No smoothing.",
             "Real skin: visible pores and fine vellus hair; one clear, even skin colour all over her face. No "
             "smoothing.")
LUMA_DRESSED = ("Hair a little different.",
                "Hair a little different. She wears a plain round-necked top, grey on one day and navy on the "
                "other; her shoulders are never bare.")
# Smoke: luma (and nbp_flash) framed the pair with a white border; Luma sees no negatives.
LUMA_EDGES = ("side by side filling one square frame: two panels",
              "side by side filling one square frame right out to all four edges: two panels")
LUMA_SWAPS_BOTH = [LUMA_AMATEUR, LUMA_SKIN, LUMA_DRESSED, LUMA_EDGES]
LUMA_SWAPS_TONE = LUMA_SWAPS_BOTH + [
    ("eye colour, skin colour, brows", "eye colour, skin type and undertone, brows"),
    ("the same person, same age, same complexion, no makeup. ",
     "the same person, same age, plainly the same medium tan skin tone, no makeup. "),
    ("It is not lit more kindly - not brighter, softer or more frontal than the left. ",
     "The two panels match exactly for light, exposure and white balance - the whites of her eyes, her hair and "
     "her lips look the same; only her skin is a shade brighter. "),
    ("Daylight from high up on one side grazes DOWN across her face on both days, so every line, bulge and "
     "hollow casts its own small shadow. Bright, eyes clearly visible.",
     "Bright, soft, broad daylight from roughly in front of her on both days, so her skin is lit evenly and its "
     "real colour shows. No hard light and no shadow across the cheek, no flash."),
]


def swap(text: str, pairs: list, where: str) -> str:
    for old, new in pairs:
        n = text.count(old)
        assert n == 1, f"{where}: expected the round-3 sentence once, found {n}: {old[:70]!r}"
        text = text.replace(old, new)
    return text


def negative_pair(kind: str) -> str:
    """The round-3 pair negatives. For a tone pair, the four that forbid the finding itself (a skin
    colour change, a brighter right panel) or the tone-pair light (frontal, shadowless) are removed -
    a ban that fights the brief is the hardest instruction to notice."""
    neg = r3.NEGATIVE_PAIR
    if kind == "tone":
        for phrase in ("no change of skin colour between the panels, ", "no brighter right panel, ",
                       "no flat frontal lighting, ", "no shadowless face, "):
            assert neg.count(phrase) == 1, f"round-3 pair negative changed: {phrase!r}"
            neg = neg.replace(phrase, "")
    return neg


NEGATIVE_GLOBAL = r3.NEGATIVE_GLOBAL.replace("no non-white model, ", "")
assert "non-white" not in NEGATIVE_GLOBAL, "round-3 casting negative would fight the Filipino casting"
NEGATIVE_GLOBAL += ", no Caucasian model, no European model, no fair-skinned model"


def build(w: dict) -> tuple:
    b = BLOCKS[w["block"]]
    tone = b["kind"] == "tone"
    r3.CROPS, r3.BLOCKS, r3.VIEWPOINTS, r3.GAZE, r3.WALLS = CROPS, BLOCKS, VIEWPOINTS, GAZE, WALLS
    r3.LIGHT = LIGHT_TONE if tone else LIGHT_WRINKLE
    r3.SKIN = SKIN_GLUT
    prompt = swap(r3.build_prompt(w), SWAPS_TONE if tone else SWAPS_BOTH, f"{w['key']} prompt")
    short = [(b["expression"], b["luma_expression"]), (b["nothing_else"], b["luma_nothing_else"])]
    luma = swap(r3.build_prompt_luma(w), (LUMA_SWAPS_TONE if tone else LUMA_SWAPS_BOTH) + short,
                f"{w['key']} luma")
    return prompt, luma


def main() -> None:
    slots = []
    for w in WOMEN:
        b = BLOCKS[w["block"]]
        prompt, prompt_luma = build(w)
        negative_extra = negative_pair(b["kind"]) + ", " + b["negatives"]
        both = prompt + prompt_luma
        assert len(prompt_luma) < r3.LUMA_CAP, f"{w['key']}: luma prompt {len(prompt_luma)} chars"
        assert not any(ch.isdigit() for ch in both), f"{w['key']}: digit in prompt"
        bait = r3.caption_bait(both + NEGATIVE_GLOBAL + negative_extra)
        assert not bait, f"{w['key']}: caption bait {bait}"
        assert "window" not in both.lower(), f"{w['key']}: 'window' in prompt"
        assert "white balance is a little wrong" not in both and "slightly off" not in both, w["key"]
        assert "uneven pigment" not in both and "Pigment is uneven" not in both, w["key"]
        # Smoke: "sun-deepened tan" came back as mottled sun damage on luma - the concern, not the result.
        assert not re.search(r"\bsun", both, re.I), f"{w['key']}: 'sun' in prompt"
        if b["kind"] == "tone":
            for gone in ("grazes down", "grazes DOWN", "lighter-skinned", "SAME COMPLEXION"):
                assert gone not in both, f"{w['key']}: wrinkle-pair text survived in a tone brief: {gone!r}"
        slots.append({
            "id": f"glub1--{w['block']}-{w['key']}",
            "title": (f"{b['block']} {w['block'].split('-', 1)[1]} · {b['study']} · {CROPS[w['crop']]['label']} — "
                      f"{w['who'].split(',')[0].replace('a ', '', 1)}"),
            "class": "B", "width": r3.SIZE, "height": r3.SIZE,
            "target_slot": f"{b['page']} key_findings_ba {b['block']} ({b['heading']})",
            "generated_from": (f"{ROUND} smoke brief - {SMOKE_BRIEF} (not re-run)" if w["key"] in SMOKE_SLOTS
                               else f"{ROUND}, revised after the smoke test"),
            "ref_files": [], "prompt": prompt, "prompt_luma": prompt_luma,
            "label": {"left": "Before", "right": b["after_label"], "figure": "",
                      "measure": "(labels are theme settings, never pixels)", "cite": b["study"]},
            "negative_extra": negative_extra,
        })
    ids = [s["id"] for s in slots]
    # generate-multi's --only matches by prefix, and upload binds by stem prefix: no id may prefix another.
    assert not any(a != c and c.startswith(a) for a in ids for c in ids), "a slot id prefixes another"

    cfg = {
        "wave": WAVE, "created": "2026-09-26", "round": ROUND,
        "doc": ("docs/claims/glutathione.md §8.5 (source of truth), docs/clinical-trial-before-after-images.md, "
                ".claude/rules/website-imagery.md; built by scripts/build-glutathione-cards-before-after-config.py "
                "on the round-3 brief machinery, f2 from the copper crow's-feet block"),
        "note": ("GLUTATHIONE SCIENCE PAGE, FINDINGS CARDS f1 AND f2 (Watanabe 2014: 30 Filipino women aged 30-50, "
                 "skin types III-IV, 2% GSSG lotion, split-face, 10 weeks). f1 tone (slots a-c): a MODEST, even "
                 "brightening of the cheekbone (melanin index -10.7% vs -3.1% placebo; 'moderate' = under 50% "
                 "lightening) - no change in evenness, spots, redness, pores, texture or lines; tone-pair light "
                 "(soft, broad, frontal; exposure and white balance matched). f2 crow's feet (slots d-f): the same "
                 "lines a little shallower and softer, never erased; no tone or brightness change between panels. "
                 "MALCOLM, 2026-09-26: 'New wave, all suppliers', subject matching the trial (Southeast Asian, "
                 "medium to tan skin, late 30s to early 40s). CANDIDATES ONLY; Malcolm picks with _ / __. Smoke "
                 "test: slot a on all six suppliers first."),
        "target_templates": [TEMPLATE],
        "labels_are_composited": "NOT composited. Labels are text settings on the theme section.",
        "defaults": {"candidates": 1, "negative_global": NEGATIVE_GLOBAL, "negative_class_b": ""},
        "slots": slots,
    }
    OUT.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {OUT.relative_to(ROOT)} — {len(slots)} slots")
    for s in slots:
        print(f"  {s['id']:<26} prompt {len(s['prompt']):>5}  luma {len(s['prompt_luma']):>5}")


if __name__ == "__main__":
    main()
