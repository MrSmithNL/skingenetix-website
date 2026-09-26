#!/usr/bin/env python3
"""Build the before/after wave for the two copper-peptide science-page cards (round 1).

    python3 scripts/build-copper-before-after-config.py
    → configs/banners/before-after-copper-cards-r1.json

    set -a; source ~/.claude/config/image-credentials.env; set +a
    python3 scripts/generate-multi.py configs/banners/before-after-copper-cards-r1.json \
        --candidates 1 --only <slot-id>[,<slot-id>]

Malcolm, 2026-09-26: "we also need to add at least 2 sections that show the best proven results from
studies - with a before and after image", then chose a NEW batch in his round-3 look (Caucasian,
close-up, plain wall) over the 27 August candidates, and the 71-woman face-cream study for card 2.

REUSE, NOT A COPY. The brief skeleton, the walls, the honesty rules, the identity lock, the side-lock
wording, the negatives and the caption-bait guard all come from the round-3 builder
(scripts/build-under-eye-forehead-before-after-config.py), which carries every lesson of fifteen
acetyl waves and the PDRN/Argireline rounds. This file only supplies what is copper-specific - the
two cards, their crops, viewpoints, gaze, the six women and a light paragraph that names the right
features - and injects them into that module before calling its build_prompt / build_prompt_luma.

THE TWO CARDS, AND WHAT EACH PICTURE MAY CLAIM (docs/claims/copper-peptide-ghk-cu.md §8)
  copper-crowsfeet  /pages/copper-peptide-research, key_findings_ba f1 - "Crow's-Feet Wrinkle Volume
                    −24.1% in 8 Weeks". Badenhorst 2016: randomised, double-blind, split-face, 40 women
                    aged 40-65, PRIMOS 3D. The GHK-Cu serum ALWAYS went on the RIGHT side of the face,
                    so the picture shows her right-side crow's feet: in picture terms her nose points to
                    the RIGHT-HAND edge (register §8.4). −24.1% is a VOLUME change from the start on the
                    serum side: briefed as every line still there, each about three-quarters as full.
  copper-facecream  same page, f2 - "Firmer-Looking Skin and Fewer Fine Lines in 12 Weeks". The 2002
                    face-cream study, 71 women, 12 weeks, known from published reviews: "improved skin
                    laxity, clarity, and appearance, reduced fine lines and the depth of wrinkles, and
                    increased skin density and thickness". No numbers were published, so the change is
                    briefed as MODEST: fine lines on the cheek softer, the skin a little clearer and
                    firmer-looking; the jawline and any softness along it essentially unchanged.

CAMERA HEIGHT RUNS AGAINST THE IMPROVEMENT (inherited rule). Crow's feet read about the same from any
height, so the right panel is level or a touch LOWER. A lower face reads FIRMER from above (the jaw
line tightens) and SLACKER from below, so the right face-cream panel is level or slightly LOWER, and
her chin is never lifted in the right panel.

SUPPLIERS: all six (website-imagery rule 1). Smoke-test one slot per card first.

SMOKE LOG, 2026-09-26 (slots a and d, 12 of 12 returned; gpt_image resolved to gpt-image-2.5-sunburst).
  HELD: no text, caption, window, hand or phone on any tile; Caucasian casting; the right-side lock on
  card 1 on five of six engines.
  KNOWN SUPPLIER TRAITS, NOT BRIEF FAULTS (so the brief was not changed): flux2 mirrored the face
  between the panels on card 1 (its recorded habit); seedream turned card 2's right panel into a full
  profile facing the other way; luma and nbp_pro framed the pair with a white border. Card 2's
  lower-face crop was honoured by NO engine - all returned a three-quarter face, forehead to chin
  (engines-return-a-portrait-whatever-crop-you-ask-for): crop the winner in post.
  Slots b, c, e and f ran on the unchanged brief.
Author: Claude Code, 2026-09-26. Candidates only; nothing is uploaded or published by this file.
"""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_s = importlib.util.spec_from_file_location("r3", ROOT / "scripts/build-under-eye-forehead-before-after-config.py")
r3 = importlib.util.module_from_spec(_s)
_s.loader.exec_module(r3)

WAVE = "before-after-copper-cards-r1"
OUT = ROOT / "configs" / "banners" / f"{WAVE}.json"
ROUND = "r1"
SMOKE_SLOTS = {"a", "d"}

CROPS = {
    # ---- copper-crowsfeet -------------------------------------------------------------
    "cf_three_quarter": dict(
        selfie=True, label="close three-quarter, eye corner and temple",
        text=("HER FACE FILLS THE PANEL, IN A CLOSE THREE-QUARTER VIEW. The phone is so close that the top "
              "of her head and her chin are both cut off: the frame runs from her upper forehead down to "
              "just below her nose. The OUTER CORNER OF THE NEAR EYE, the temple beside it and the top of "
              "the cheek below it are the largest things in the picture and sit in the middle of the "
              "panel; the far side of her face turns away. THE FAN OF FINE LINES SPREADING OUT FROM THE "
              "OUTER CORNER OF THE NEAR EYE towards the temple and down onto the cheek is what the picture "
              "is of. The plain wall shows only as a narrow strip beside the back of her head."),
    ),
    "cf_eye_corner": dict(
        selfie=False, label="one eye corner, close",
        text=("ONE EYE AND THE SKIN BESIDE ITS OUTER CORNER FILL THE PANEL. The frame runs from her eyebrow "
              "at the top down to about the level of her nostrils at the bottom, and across from the middle "
              "of that eye to her temple and the edge of her hair. Only that one eye is in the picture. Skin "
              "fills almost the whole panel, with at most a thin sliver of plain wall past her hair. THE "
              "LINES FANNING OUT FROM THE OUTER CORNER OF THE EYE, and the texture of the skin between "
              "them, sit in the middle of the panel and are what the picture is of. An ordinary close "
              "photograph taken at home, sharp across the eye corner - not a studio or clinical photograph."),
    ),
    "cf_steep": dict(
        selfie=True, label="close, steep three-quarter",
        text=("HER FACE IS SEEN CLOSE AND STEEPLY FROM THE SIDE, AND FILLS THE PANEL. Her head is turned "
              "well away, so the camera looks along her cheek towards her temple: the near eye, its outer "
              "corner, the temple and the near cheekbone fill most of the panel, and the far eye is only "
              "just visible beyond the bridge of her nose. The frame runs from her upper forehead down to "
              "the corner of her mouth. From this angle THE FAN OF LINES AT THE OUTER CORNER OF THE NEAR "
              "EYE spreads across the side of her face and is what the picture is of. The plain wall shows "
              "only as a narrow strip at one edge."),
    ),
    # ---- copper-facecream -------------------------------------------------------------
    "lf_three_quarter": dict(
        selfie=True, label="close three-quarter, lower face",
        text=("THE LOWER HALF OF HER FACE FILLS THE PANEL, IN A CLOSE THREE-QUARTER VIEW. The frame runs "
              "from just below her eyes at the top down to just below her jawline at the bottom, so her "
              "forehead is out of the picture and only the top of her neck shows. The near cheek, the "
              "corner of her mouth and the line of her jaw are the largest things in the picture. THE SKIN "
              "OF THE NEAR CHEEK - its fine lines, its texture and how firm it looks - and THE CONTOUR "
              "WHERE THE CHEEK MEETS THE JAW are what the picture is of. The plain wall shows only as a "
              "narrow strip beside her face."),
    ),
    "lf_cheek_jaw": dict(
        selfie=True, label="close cheek and jaw, steep three-quarter",
        text=("HER CHEEK AND JAWLINE FILL THE PANEL, SEEN CLOSE AND STEEPLY FROM THE SIDE. Her head is "
              "turned well away, so the camera looks along the side of her face: the near cheek from the "
              "cheekbone down, the corner of her mouth, the line of the jaw and the top of the neck fill "
              "the panel, and her eyes are at or just above the top edge. THE CHEEK SKIN AND THE LINE OF "
              "THE JAW, seen almost in profile, are what the picture is of. The plain wall shows only as a "
              "narrow strip at one edge."),
    ),
    "lf_face": dict(
        selfie=True, label="close three-quarter, whole face",
        text=("HER FACE FILLS THE PANEL, IN A CLOSE THREE-QUARTER VIEW. The frame runs from her hairline "
              "at the top down to just below her chin, with her ears at or past the side edges. Her face "
              "is turned a little, so the near cheek and the near side of the jaw are the largest area of "
              "skin in the picture. HOW FIRM AND SMOOTH HER CHEEKS LOOK, THE FINE LINES ON THEM, and the "
              "contour of her jaw are what the picture is of. The plain wall shows only as a narrow strip "
              "beside her head."),
    ),
}

BLOCKS = {
    "copper-crowsfeet": dict(
        page="/pages/copper-peptide-research", template="templates/page.research-copper-peptide.json",
        block="f1", heading="Crow's-Feet Wrinkle Volume -24.1% in 8 Weeks", study="badenhorst-2016",
        after_label="After 8 weeks",
        expression=("Her face is completely at rest on both days: eyes open normally, mouth closed, NOT "
                    "SMILING AND NOT SQUINTING. A smile or a squint pulls the outer corner of the eye into "
                    "deep creases of its own, so either one in one panel and not the other would manufacture "
                    "the whole difference - her eyes and cheeks are in the same relaxed resting state in both "
                    "panels, and the lines at her eye corner are the ones that stay there at rest."),
        honesty=("EVERY LINE AT THE OUTER CORNER OF HER EYE IS STILL THERE IN THE RIGHT PANEL - the same "
                 "number of lines, each in the same place and the same direction, and each still clearly "
                 "visible as a line. None has disappeared and the skin there has NOT become smooth, tight or "
                 "shiny. What has changed is that each line is a little shallower and a little less full, so "
                 "it holds a slightly softer, shorter shadow."),
        luma_magnitude=("Every eye-corner line is still there, only a little shallower - each about "
                        "three-quarters as full. Visible when the panels are compared, but anyone seeing this "
                        "panel alone would still say she has lines at the corner of her eye."),
        luma_honesty=("Every line at the corner of her eye is still there - same number, place and direction, "
                      "still clearly visible; each is only a little shallower."),
        feature=("THESE LINES ARE ORDINARY SOFT CREASES IN THE SKIN, THE SAME COLOUR AS THE REST OF HER SKIN. "
                 "They show as fine lines of shadow where the light grazes them - never as cracks, cuts, scars "
                 "or red marks."),
        nothing_else=("NOTHING OUTSIDE THE EYE CORNER HAS CHANGED. Her forehead, her brows, the skin under her "
                      "eyes, the lines beside her nose and mouth, her cheeks and her jaw look exactly the same "
                      "in both panels; only the lines at the outer corner of her eye are different."),
        age=("SHE IS BETWEEN FORTY-FIVE AND SIXTY - MIDDLE-AGED - AND THAT GOVERNS WHAT HER SKIN CAN HONESTLY "
             "LOOK LIKE. The lines at the corners of her eyes are established and stay with her face at rest, "
             "the skin there is thin and finely crinkled, and some grey in her hair is normal. But she is NOT "
             "elderly: no deep folds, no hooded drooping lids, none of the slackness of a woman in her "
             "seventies."),
        subject=("IN THE LEFT PANEL, THE LINES FANNING OUT FROM THE OUTER CORNER OF HER EYE ARE THE SUBJECT OF "
                 "THE PICTURE. "),
        magnitude=("EVERY LINE AT THE CORNER OF HER EYE IS STILL THERE AND STILL CLEARLY VISIBLE IN THE RIGHT "
                   "PANEL - the same number, the same length, the same place and the same direction. Each one is "
                   "a little shallower and less full: it holds a shadow about THREE-QUARTERS as dark and as long "
                   "as in the left panel, and the fine crinkled texture between the lines is a little calmer.\n\n"
                   "THE SIZE OF THE CHANGE IS NARROW AT BOTH ENDS. It must be VISIBLE: someone comparing the two "
                   "panels should see that the lines at the eye corner are softer in the right one and be able "
                   "to point to where. But it is MODEST: anyone looking at the right panel on its own would still "
                   "say this woman has lines at the corners of her eyes. The eye corner has not been smoothed, "
                   "filled or made young. A right panel with a smooth, line-free eye corner is a failure, not a "
                   "success."),
        negatives=("no smiling, no squinting, no laughing, no closed eyes, no eye makeup, no change of eye "
                   "shape between the panels, no smooth line-free eye corner in the right panel, no line "
                   "disappearing between the panels, no shiny skin at the eye corner, no filler look, "
                   "no smaller eye bags in the right panel, no smoother forehead in the right panel, "
                   "no rested younger face in the right panel, no crack in the skin, no cut, no scar, "
                   "no red line, no woman under forty, no elderly woman, no hooded drooping eyelids"),
    ),
    "copper-facecream": dict(
        page="/pages/copper-peptide-research", template="templates/page.research-copper-peptide.json",
        block="f2", heading="Firmer-Looking Skin and Fewer Fine Lines in 12 Weeks", study="leyden-2002-face",
        after_label="After 12 weeks",
        expression=("Her face is at rest on both days, mouth closed and relaxed, lips together, not smiling "
                    "and not pursing. HER HEAD IS HELD THE SAME WAY IN BOTH PANELS - her chin is NOT lifted in "
                    "either picture, and never lifted in the right one: raising the chin stretches the skin of "
                    "the cheek and jaw taut, so a lifted chin in one panel and not the other would manufacture "
                    "the whole difference. No hand touches her face."),
        honesty=("SHE HAS THE SAME FACE SHAPE AND THE SAME JAW IN BOTH PANELS. Every fine line on her cheek is "
                 "still there in the right panel, in the same place, only a little softer, and any softness "
                 "along her jawline is still there too, essentially unchanged. The skin looks a little firmer, "
                 "smoother and clearer - it has NOT been lifted, tightened, filled, contoured or slimmed."),
        luma_magnitude=("Her cheek skin looks a little firmer, smoother and clearer, and the fine lines on it "
                        "are a little softer - each still there. The jaw and face shape are the same. Visible "
                        "when compared, but anyone seeing this panel alone would still see a woman of her age."),
        luma_honesty=("Same face shape and jaw; every fine line on her cheek still there, only a little softer; "
                      "nothing lifted, tightened, filled or slimmed."),
        feature=("THE FINE LINES AND THE SLIGHTLY LOOSE, CREPEY TEXTURE OF HER CHEEK ARE ORDINARY SKIN OF HER "
                 "AGE, THE SAME COLOUR AS THE REST OF HER SKIN. They show by texture and fine shadow where the "
                 "light grazes the cheek - never as redness, scars, blemishes or marks."),
        nothing_else=("NOTHING OUTSIDE THE CHEEK AND JAW HAS CHANGED. Her eyes, the skin under her eyes, her "
                      "forehead, her lips, her face shape and her hair look exactly the same in both panels; only "
                      "the skin of her cheek is a little different."),
        age=("SHE IS BETWEEN FORTY-FIVE AND FIFTY-EIGHT - MIDDLE-AGED - AND THAT GOVERNS WHAT HER SKIN CAN "
             "HONESTLY LOOK LIKE. Her cheek has fine lines and a slightly loose, crepey texture, the line from "
             "her nose to the corner of her mouth is established, and her jawline has begun to soften. But she "
             "is NOT elderly: no jowls hanging below the jaw, no deep folds, none of the slackness of a woman "
             "in her seventies."),
        subject=("IN THE LEFT PANEL, THE SKIN OF HER CHEEK - ITS FINE LINES, ITS TEXTURE AND HOW FIRM IT LOOKS - "
                 "IS THE SUBJECT OF THE PICTURE. "),
        magnitude=("HER CHEEK SKIN LOOKS A LITTLE FIRMER, SMOOTHER AND CLEARER IN THE RIGHT PANEL, AND THE FINE "
                   "LINES ON IT ARE A LITTLE SOFTER - but every one of them is still there, in the same place. The "
                   "crepey texture is a little finer and the skin catches the grazing light a little more evenly. "
                   "The shape of her face and the line of her jaw are the same.\n\n"
                   "THE SIZE OF THE CHANGE IS NARROW AT BOTH ENDS. It must be VISIBLE: someone comparing the two "
                   "panels should see that the cheek skin looks firmer and smoother in the right one and be able to "
                   "point to where. But it is MODEST: anyone looking at the right panel on its own would still see "
                   "the lines and the texture of a woman of her age. Her face has not been lifted, slimmed, filled "
                   "or made young. A right panel with smooth, taut, line-free cheeks or a sharper jaw is a "
                   "failure, not a success."),
        negatives=("no smiling, no pursed lips, no lifted chin, no chin raised in the right panel, no head tilted "
                   "back, no hand on the face, no face lift look, no tightened jaw, no sharper jawline in the "
                   "right panel, no slimmer face in the right panel, no contouring, no filler, no plumped cheeks, "
                   "no smooth line-free cheek in the right panel, no shiny cheek, no brighter skin in the right "
                   "panel, no rested younger face in the right panel, no smaller eye bags in the right panel, "
                   "no smoother forehead in the right panel, no acne, no scar, no redness, no woman under forty, "
                   "no elderly woman, no hanging jowls"),
    ),
}

NOT_MIRRORED = r3.NOT_MIRRORED
SIDE_RIGHT_SIDE = (r3.SIDE_NOSE_RIGHT)            # her RIGHT side toward the camera (the treated side)
VIEWPOINTS = {
    # copper-crowsfeet — her right side, both panels; right panel level or a touch LOWER
    "a": dict(side=SIDE_RIGHT_SIDE,
              a=dict(cam="held just above her eye line and a little off to the side, angled slightly down",
                     turn="her face turned about twenty-five degrees towards the right-hand edge of the picture, level",
                     dist="framed very close", place="the corner of her near eye sits high and slightly left of centre"),
              b=dict(cam="held at her eye line, off to the same side",
                     turn="her face turned about thirty degrees towards the right-hand edge of the picture, level",
                     dist="framed a touch less close, but still close", place="the corner of her near eye sits centred")),
    "b": dict(side=SIDE_RIGHT_SIDE,
              a=dict(cam="held at her eye line, a hand's width from the outer corner of her right eye",
                     turn="her face turned about thirty degrees towards the right-hand edge of the picture, level",
                     dist="framed very close", place="the eye corner sits high and left of centre"),
              b=dict(cam="held just below her eye line and tilted up slightly",
                     turn="her face turned about thirty-five degrees towards the right-hand edge of the picture, level",
                     dist="framed a touch closer still", place="the eye corner sits centred and a little low")),
    "c": dict(side=SIDE_RIGHT_SIDE,
              a=dict(cam="held at her eye line, well out to the side",
                     turn="her face turned about forty-five degrees towards the right-hand edge of the picture, level",
                     dist="framed close", place="her near eye sits high and left of centre"),
              b=dict(cam="held a little below her eye line, well out to the same side, tilted up",
                     turn="her face turned about fifty degrees towards the right-hand edge of the picture, level",
                     dist="framed a touch closer", place="her near eye sits centred")),
    # copper-facecream — one side locked; right panel level or LOWER, chin never lifted
    "d": dict(side=r3.SIDE_NOSE_LEFT,
              a=dict(cam="held at her mouth level, a little off to the side",
                     turn="her face turned about twenty-five degrees towards the left-hand edge of the picture, chin level",
                     dist="framed very close", place="her near cheek sits centred and high"),
              b=dict(cam="held a little below her mouth level and tilted up slightly",
                     turn="her face turned about thirty degrees towards the left-hand edge of the picture, chin level",
                     dist="framed a touch less close, but still close", place="her near cheek sits left of centre")),
    "e": dict(side=r3.SIDE_NOSE_RIGHT,
              a=dict(cam="held at her cheekbone level, well out to the side",
                     turn="her face turned about fifty degrees towards the right-hand edge of the picture, chin level",
                     dist="framed close", place="her jaw sits in the lower third of the panel"),
              b=dict(cam="held at her mouth level, well out to the same side",
                     turn="her face turned about fifty-five degrees towards the right-hand edge of the picture, chin level",
                     dist="framed a touch closer", place="her jaw sits a little lower in the panel")),
    "f": dict(side=r3.SIDE_NOSE_LEFT,
              a=dict(cam="held a little above her eye line and angled down slightly",
                     turn="her face turned about twenty degrees towards the left-hand edge of the picture, chin level",
                     dist="framed very close", place="her face sits centred"),
              b=dict(cam="held at her eye line",
                     turn="her face turned about twenty-five degrees towards the left-hand edge of the picture, chin level",
                     dist="framed a touch less close, but still close", place="her face sits a little right of centre")),
}
GAZE = {
    "a": ("her eyes are on the lens", "her eyes look a little away from the lens, off to the side"),
    "b": ("her eye looks straight ahead, just past the lens", "her eye looks a fraction to one side of the lens"),
    "c": ("her eyes look ahead, past the camera", "her eyes glance a little towards the lens"),
    "d": ("her eyes are on the lens", "her eyes are a little off the lens, towards the far side"),
    "e": ("her eyes look ahead, past the camera", "her eyes look a little down and away"),
    "f": ("her eyes are just off the lens to one side", "her eyes are on the lens"),
}
WOMEN = [
    # ---- copper-crowsfeet · Badenhorst 2016 · ages 40-65 in the trial; cast 46-58 -----------
    dict(block="copper-crowsfeet", key="a", crop="cf_three_quarter", walls=(0, 1),
         who=("a white BRITISH woman of about fifty-two, with shoulder-length light-brown hair going grey at "
              "the temples, tucked behind her ear, fair skin with a pinkish undertone, hazel eyes, fair brows, "
              "and one small flat brown mole on her right temple beside the corner of her right eye"),
         before=("At the outer corner of the near eye a fan of five or six fine lines spreads out towards the "
                 "temple, the middle two long and clear, the upper ones curving up towards the end of the brow "
                 "and the lower ones running down onto the top of the cheek. The thin skin between them is "
                 "finely crinkled, and each line casts a small shadow where the light grazes it.")),
    dict(block="copper-crowsfeet", key="b", crop="cf_eye_corner", walls=(2, 3),
         who=("a white GERMAN woman of about fifty-six, with short ash-blonde hair, fair skin with a few faint "
              "freckles across the cheekbones, pale blue-grey eyes, pale brows, and a small flat brown mole on "
              "the top of her right cheekbone below the outer corner of her right eye"),
         before=("From the outer corner of her right eye four clear lines fan out across the temple and a few "
                 "shorter, finer ones run between them, with a crinkled, slightly crepey texture over the whole "
                 "area. The longest line reaches almost to her hairline.")),
    dict(block="copper-crowsfeet", key="c", crop="cf_steep", walls=(4, 5),
         who=("a white IRISH woman of about forty-seven, with shoulder-length dark-brown hair pulled loosely "
              "back, very fair skin with fine freckles, green eyes, dark brows, and a tiny dark mole high on her "
              "right cheek"),
         before=("Seen from the side, a clear fan of lines spreads from the outer corner of the near eye across "
                 "the side of her face, three of them long, with finer crinkles between them and a couple of "
                 "short lines running down onto the cheekbone.")),
    # ---- copper-facecream · the 2002 face-cream study, 71 women; cast 47-57 -----------------
    dict(block="copper-facecream", key="d", crop="lf_three_quarter", walls=(6, 7),
         who=("a white FRENCH woman of about fifty-three, with chin-length dark-blonde hair tucked behind her "
              "ear, fair skin with a light olive undertone, grey-green eyes, and one small flat brown mole on "
              "her left cheek near the corner of her mouth"),
         before=("The skin of her near cheek has a scatter of fine lines running down and forward towards the "
                 "corner of her mouth, and a slightly loose, crepey texture that shows where the light grazes "
                 "it. The line from her nose to the corner of her mouth is established, and the contour where "
                 "the cheek meets the jaw is a little soft.")),
    dict(block="copper-facecream", key="e", crop="lf_cheek_jaw", walls=(8, 9),
         who=("a white SWEDISH woman of about fifty-seven, with straight light-blonde hair cut to the shoulder "
              "and tucked back, fair skin with a few faint sun spots on the cheekbone, blue eyes, and a small "
              "flat brown mole on her right cheek just above the jawline"),
         before=("Along the near cheek, from the cheekbone down to the jaw, the skin has fine lines and a "
                 "slightly crepey texture that catches the grazing light, and the line of the jaw has begun to "
                 "soften, with a gentle fullness just in front of the ear.")),
    dict(block="copper-facecream", key="f", crop="lf_face", walls=(10, 11),
         who=("a white SPANISH woman of about forty-nine, with dark-brown shoulder-length hair pulled back, "
              "olive skin, dark brown eyes, dark natural brows, and a small mole on her left cheekbone"),
         before=("Her cheeks have fine lines and a slightly loose, uneven texture, a little clearer on the "
                 "near side where the light grazes it, and the lines from her nose to the corners of her mouth "
                 "are established. Her jawline has begun to soften a little.")),
]

LIGHT = (
    "BOTH PICTURES ARE BRIGHT AND WELL EXPOSED, AND IN BOTH THE DAYLIGHT FALLS ON HER FROM HIGH UP ON ONE "
    "SIDE AND GRAZES DOWN AND ACROSS HER FACE. This matters more than anything else about the lighting. The "
    "features this picture is about - fine lines and the texture of the skin - only show when light grazes "
    "across them: then every line casts its own small shadow and the texture catches the light. Flat light "
    "from the front would wash all of it away and hide what the picture exists to show. Bright and clean, "
    "her eyes clearly visible and not lost in shadow, no dark room, no flash - but definitely DIRECTIONAL, "
    "with a lit side and a softer shaded side.\n\n"
    "⚠️ NEITHER DAY IS LIT MORE KINDLY THAN THE OTHER. The light comes from a different side and the wall is "
    "different, but the right-hand picture is NOT lit more softly, more frontally or more evenly than the "
    "left-hand one - the light grazes across her just as strongly on both days. If the right-hand picture "
    "were lit more flatly, the improvement would simply be the light and the pair would be a lie."
)


def main() -> None:
    # inject the copper-specific parts into the round-3 builder, then use its brief machinery unchanged
    r3.CROPS, r3.BLOCKS, r3.VIEWPOINTS, r3.GAZE, r3.LIGHT = CROPS, BLOCKS, VIEWPOINTS, GAZE, LIGHT
    slots = []
    for w in WOMEN:
        b = BLOCKS[w["block"]]
        prompt, prompt_luma = r3.build_prompt(w), r3.build_prompt_luma(w)
        negative_extra = r3.NEGATIVE_PAIR + ", " + b["negatives"]
        assert len(prompt_luma) < r3.LUMA_CAP, f"{w['key']}: luma prompt {len(prompt_luma)} chars"
        assert not any(ch.isdigit() for ch in prompt + prompt_luma), f"{w['key']}: digit in prompt"
        bait = r3.caption_bait(prompt + prompt_luma + r3.NEGATIVE_GLOBAL + negative_extra)
        assert not bait, f"{w['key']}: caption bait {bait}"
        assert "window" not in (prompt + prompt_luma).lower(), f"{w['key']}: 'window' in prompt"
        slots.append({
            "id": f"cub1--{w['block']}-{w['key']}",
            "title": f"{w['block']} · {b['study']} · {CROPS[w['crop']]['label']} — {w['who'].split(',')[0].replace('a ', '', 1)}",
            "class": "B", "width": r3.SIZE, "height": r3.SIZE,
            "target_slot": f"{b['page']} key_findings_ba {b['block']} ({b['heading']})",
            "generated_from": f"{ROUND}{' smoke slot' if w['key'] in SMOKE_SLOTS else ''}",
            "ref_files": [], "prompt": prompt, "prompt_luma": prompt_luma,
            "label": {"left": "Before", "right": b["after_label"], "figure": "",
                      "measure": "(labels are theme settings, never pixels)", "cite": b["study"]},
            "negative_extra": negative_extra,
        })
    cfg = {
        "wave": WAVE, "created": "2026-09-26", "round": ROUND,
        "doc": ("docs/clinical-trial-before-after-images.md, .claude/rules/website-imagery.md, built by "
                "scripts/build-copper-before-after-config.py on the round-3 brief machinery"),
        "note": ("COPPER PEPTIDE SCIENCE PAGE, TWO BEFORE/AFTER CARDS. copper-crowsfeet (slots a-c) -> "
                 "/pages/copper-peptide-research key_findings_ba f1, Badenhorst 2016 (double-blind split-face, "
                 "40 women aged 40-65, 8 weeks; the serum always on the RIGHT side, so her right-side crow's "
                 "feet, nose pointing to the right-hand edge). copper-facecream (slots d-f) -> f2, the 2002 "
                 "face-cream study (71 women, 12 weeks; no numbers published, so a modest change). MALCOLM, "
                 "2026-09-26: a new batch in the round-3 look (Caucasian, close-up, plain wall) and the 71-woman "
                 "face-cream study for card 2. CANDIDATES ONLY; Malcolm picks with _ / __. Smoke test: slots a "
                 "and d on all six suppliers first."),
        "target_templates": ["templates/page.research-copper-peptide.json"],
        "labels_are_composited": "NOT composited. Labels are text settings on the theme section.",
        "defaults": {"candidates": 1, "negative_global": r3.NEGATIVE_GLOBAL, "negative_class_b": ""},
        "slots": slots,
    }
    OUT.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {OUT.relative_to(ROOT)} — {len(slots)} slots")
    for s in slots:
        print(f"  {s['id']:<34} prompt {len(s['prompt']):>5}  luma {len(s['prompt_luma']):>5}")


if __name__ == "__main__":
    main()
