#!/usr/bin/env python3
"""Build the before/after wave for the two Matrixyl 3000 science-page cards (round 1).

    python3 scripts/build-matrixyl-before-after-config.py
    → configs/banners/before-after-matrixyl-cards-r1.json

    set -a; source ~/.claude/config/image-credentials.env; set +a
    python3 scripts/generate-multi.py configs/banners/before-after-matrixyl-cards-r1.json \
        --candidates 1 --only <slot-id>[,<slot-id>]

Malcolm, 2026-09-26: every science page needs "at least 2 sections that show the best proven results from
studies - with a before and after image", in his round-3 look (Caucasian, close-up, plain wall). For
Matrixyl he chose the pentapeptide-4 trial for card 2 (docs/claims/matrixyl-3000.md §8.7, decision 1).

REUSE, NOT A COPY: the brief skeleton, walls, honesty rules, identity and side lock, negatives and the
caption-bait guard come from scripts/build-under-eye-forehead-before-after-config.py (round 3), exactly as
the copper builder does. This file supplies only the Matrixyl cards, crops, viewpoints, gaze and women.

THE TWO CARDS, AND WHAT EACH PICTURE MAY CLAIM (register §8.5)
  matrixyl-deepwrinkles  /pages/matrixyl-3000-research key_findings_ba f1 - "Deep-Wrinkle Area −39% in 2
                    Months". Sederma's half-face study: 23 women aged 42-67, 3% cream against placebo cream,
                    2 months, profilometry. The AREA taken up by deep wrinkles fell 39%; main-wrinkle DEPTH fell
                    only about a fifth (−19.9%). The brochure's own photo pair is the outer eye corner, so the
                    picture is the crow's feet. Briefed as: every deep line still there and still visible, each
                    about four-fifths as deep, and the deepest stretches shorter. No lift, no firmer lids, no
                    tone or colour change, same neutral expression. Which half was treated is not published:
                    her LEFT side is locked for this card (the copper card uses her right).
  matrixyl-finelines  same page, f2 - "Fine Lines Reduced vs Placebo in 12 Weeks: Palmitoyl Pentapeptide-4".
                    Robinson 2005: double-blind, placebo-controlled, split-face, 93 women aged 35-55, 12 weeks;
                    "small, but significant at weeks 8 and 12". No percentage published and the facial area is
                    not stated, so a SMALL change seen at a modest distance: one side of the face from the eye
                    to the cheek, fine lines a little softer. No change in deep folds, sagging, spots or dark
                    circles. Serum only (the cream has no pentapeptide-4); the card says so.

CAMERA HEIGHT RUNS AGAINST THE IMPROVEMENT (inherited rule): the right panel is level or a touch LOWER.

SUPPLIERS: all six (website-imagery rule 1). Smoke-test one slot per card first (a and d).

SMOKE LOG, 2026-09-26 (slots a and d, 12 of 12 returned; gpt_image resolved to gpt-image-2.5-sunburst).
  HELD: no text, caption, window, hand or phone on any tile; Caucasian casting; every "after" panel keeps its lines;
  the side lock on most engines.
  SUPPLIER TRAITS, NOT BRIEF FAULTS (the same as the copper smoke log, so the brief was not changed): flux2 split one
  face into mirrored halves on slot d; seedream turned the right panel of slot a to face the other way; luma and
  nbp_pro framed the pair with a white border; no engine honoured the eye-corner crop - all returned a three-quarter
  portrait (engines-return-a-portrait-whatever-crop-you-ask-for), so crop the winner in post. luma cast slot a older
  than the brief. Slots b, c, e and f ran on the unchanged brief.
Author: Claude Code, 2026-09-26. Candidates only; nothing is uploaded or published by this file.
"""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_s = importlib.util.spec_from_file_location("r3", ROOT / "scripts/build-under-eye-forehead-before-after-config.py")
r3 = importlib.util.module_from_spec(_s)
_s.loader.exec_module(r3)
_c = importlib.util.spec_from_file_location("cu", ROOT / "scripts/build-copper-before-after-config.py")
cu = importlib.util.module_from_spec(_c)
_c.loader.exec_module(cu)

WAVE = "before-after-matrixyl-cards-r1"
OUT = ROOT / "configs" / "banners" / f"{WAVE}.json"
ROUND = "r1"
SMOKE_SLOTS = {"a", "d"}

CROPS = {
    # ---- matrixyl-deepwrinkles: the copper eye-corner crops, reused unchanged ------------------------------
    "dw_three_quarter": cu.CROPS["cf_three_quarter"],
    "dw_eye_corner": cu.CROPS["cf_eye_corner"],
    "dw_steep": cu.CROPS["cf_steep"],
    # ---- matrixyl-finelines: eye to cheek at a modest distance (the trial's facial area is not stated) ------
    "fl_eye_cheek": dict(
        selfie=True, label="three-quarter, eye to cheek",
        text=("ONE SIDE OF HER FACE, FROM THE EYE DOWN TO THE CHEEK, FILLS MOST OF THE PANEL, SEEN IN A "
              "THREE-QUARTER VIEW AT AN ORDINARY CLOSE DISTANCE - not a macro. The frame runs from her eyebrows "
              "at the top down to about the corner of her mouth at the bottom. The near eye, the skin beneath "
              "and beside it and the near cheek are the largest things in the picture. THE FINE LINES ON THAT "
              "SIDE OF HER FACE - beside the eye, under it and across the upper cheek - and the texture of the "
              "skin are what the picture is of. The plain wall shows only as a strip beside her head."),
    ),
    "fl_face": cu.CROPS["lf_face"],
    "fl_side": dict(
        selfie=True, label="steep three-quarter, eye and cheek",
        text=("HER FACE IS SEEN FROM THE SIDE AT AN ORDINARY CLOSE DISTANCE, TURNED WELL AWAY, so the camera "
              "looks along the near side of her face: the near eye, its outer corner, the temple and the upper "
              "cheek fill most of the panel, and the far eye is only just visible beyond the bridge of her nose. "
              "The frame runs from her forehead down to her chin. THE FINE LINES AT THE EYE CORNER AND ACROSS THE "
              "UPPER CHEEK, and the skin's texture, are what the picture is of. The plain wall shows only as a "
              "narrow strip at one edge."),
    ),
}

BLOCKS = {
    "matrixyl-deepwrinkles": dict(
        page="/pages/matrixyl-3000-research", template="templates/page.research-matrixyl.json",
        block="f1", heading="Deep-Wrinkle Area -39% in 2 Months", study="sederma-2013-brochure",
        after_label="After 2 months",
        expression=cu.BLOCKS["copper-crowsfeet"]["expression"],
        honesty=("EVERY LINE AT THE OUTER CORNER OF HER EYE IS STILL THERE IN THE RIGHT PANEL - the same number, "
                 "each in the same place and the same direction, and the deepest ones still clearly visible as "
                 "deep lines. None has disappeared and the skin there has NOT become smooth, tight or shiny. What "
                 "has changed is that the deep lines are a little shallower and their deepest stretches a little "
                 "shorter, so each holds a slightly softer, shorter shadow."),
        luma_magnitude=("Every deep eye-corner line is still there, only a little shallower - about four-fifths as "
                        "deep, with its deepest stretch a little shorter. Visible when the panels are compared, "
                        "but anyone seeing this panel alone would still say she has deep lines at the eye corner."),
        luma_honesty=("Every line at the corner of her eye is still there - same number, place and direction, the "
                      "deep ones still clearly deep; each is only a little shallower and shorter in its deepest part."),
        feature=cu.BLOCKS["copper-crowsfeet"]["feature"],
        nothing_else=cu.BLOCKS["copper-crowsfeet"]["nothing_else"],
        age=("SHE IS BETWEEN FORTY-EIGHT AND SIXTY-TWO - MIDDLE-AGED - AND THAT GOVERNS WHAT HER SKIN CAN HONESTLY "
             "LOOK LIKE. The lines at the corners of her eyes are DEEP and established - several of them are real "
             "creases that stay with her face at rest, not just fine crinkles - and some grey in her hair is "
             "normal. But she is NOT elderly: no deep sagging folds, no hooded drooping lids, none of the "
             "slackness of a woman in her seventies."),
        subject=("IN THE LEFT PANEL, THE DEEP LINES FANNING OUT FROM THE OUTER CORNER OF HER EYE ARE THE SUBJECT "
                 "OF THE PICTURE. "),
        magnitude=("EVERY LINE AT THE CORNER OF HER EYE IS STILL THERE AND STILL CLEARLY VISIBLE IN THE RIGHT PANEL "
                   "- the same number, the same place and the same direction. The deep ones are a little shallower: "
                   "each holds a shadow about FOUR-FIFTHS as dark, and the deepest stretch of each is a little "
                   "shorter, so less of the eye corner is taken up by deep creases. The fine crinkled texture "
                   "between them is the same.\n\n"
                   "THE SIZE OF THE CHANGE IS NARROW AT BOTH ENDS. It must be VISIBLE: someone comparing the two "
                   "panels should see that the deep lines at the eye corner are softer and shorter in the right one "
                   "and be able to point to where. But it is MODEST: anyone looking at the right panel on its own "
                   "would still say this woman has deep lines at the corners of her eyes. The eye corner has not "
                   "been smoothed, filled or made young. A right panel with a smooth or line-free eye corner is a "
                   "failure, not a success."),
        negatives=cu.BLOCKS["copper-crowsfeet"]["negatives"] + ", no lifted eyelids in the right panel, "
                  "no brighter skin in the right panel, no change of skin tone"),
    "matrixyl-finelines": dict(
        page="/pages/matrixyl-3000-research", template="templates/page.research-matrixyl.json",
        block="f2", heading="Fine Lines Reduced vs Placebo in 12 Weeks: Palmitoyl Pentapeptide-4", study="robinson-2005",
        after_label="After 12 weeks",
        expression=("Her face is at rest on both days: eyes open normally, mouth closed and relaxed, NOT SMILING AND "
                    "NOT SQUINTING. A smile or a squint creases the skin around the eyes and cheeks, so either one in "
                    "one panel and not the other would manufacture the whole difference. HER HEAD IS HELD THE SAME "
                    "WAY IN BOTH PANELS and her chin is never lifted in the right one. No hand touches her face."),
        honesty=("EVERY FINE LINE ON HER FACE IS STILL THERE IN THE RIGHT PANEL, in the same place and the same "
                 "direction, only a little softer. Her deeper folds, the line from her nose to the corner of her "
                 "mouth, any softness along her jaw, any spots and any shadows under her eyes are EXACTLY THE SAME. "
                 "Nothing has been lifted, tightened, filled or brightened."),
        luma_magnitude=("The fine lines beside and under her eye and across her upper cheek are a little softer - "
                        "every one still there. A small change: visible only when the two panels are compared."),
        luma_honesty=("Every fine line still there, only a little softer; deeper folds, spots, under-eye shadows and "
                      "face shape exactly the same; nothing lifted, filled or brightened."),
        feature=("THE FINE LINES ARE ORDINARY SOFT CREASES IN THE SKIN, THE SAME COLOUR AS THE REST OF HER SKIN. They "
                 "show as fine lines of shadow where the light grazes them - never as cracks, scars or red marks."),
        nothing_else=("NOTHING BUT THE FINE LINES HAS CHANGED. Her deeper folds, her jaw, her eyes, the shadows under "
                      "her eyes, any spots, her lips, her face shape and her hair look exactly the same in both "
                      "panels; only the fine lines are a little softer."),
        age=("SHE IS BETWEEN FORTY-TWO AND FIFTY-FOUR - EARLY MIDDLE AGE - AND THAT GOVERNS WHAT HER SKIN CAN "
             "HONESTLY LOOK LIKE. She has fine lines beside and under her eyes and a few across her upper cheek, "
             "and the line from her nose to the corner of her mouth is beginning to show. But her skin is still "
             "fairly firm: no deep creases, no sagging, none of the slackness of an older woman."),
        subject=("IN THE LEFT PANEL, THE FINE LINES BESIDE AND UNDER HER EYE AND ACROSS HER UPPER CHEEK ARE THE "
                 "SUBJECT OF THE PICTURE. "),
        magnitude=("THE FINE LINES BESIDE AND UNDER HER EYE AND ACROSS HER UPPER CHEEK ARE A LITTLE SOFTER IN THE "
                   "RIGHT PANEL - each holds a slightly fainter, finer shadow - but every one of them is still there, "
                   "in the same place.\n\n"
                   "THE CHANGE IS SMALL, AND IT MUST STAY SMALL. It must be VISIBLE: someone comparing the two panels "
                   "closely should see that the fine lines are a little softer in the right one and be able to point "
                   "to where. But it is SMALL: anyone looking at the right panel on its own would see exactly the "
                   "same woman with the same lines. Her face has not been smoothed, filled, lifted or made young. A "
                   "right panel with visibly smoother, younger skin is a failure, not a success."),
        negatives=("no smiling, no squinting, no laughing, no closed eyes, no lifted chin, no chin raised in the "
                   "right panel, no hand on the face, no smooth line-free skin in the right panel, no line "
                   "disappearing between the panels, no shiny skin, no filler look, no plumped cheeks, no lifted "
                   "face, no sharper jaw, no smaller eye bags in the right panel, no lighter under-eye shadows in "
                   "the right panel, no fewer spots in the right panel, no brighter skin in the right panel, no "
                   "rested younger face in the right panel, no makeup, no woman under thirty-five, no elderly woman"),
    ),
}

VIEWPOINTS = {
    # matrixyl-deepwrinkles — her LEFT side, both panels; right panel level or a touch LOWER
    "a": dict(side=r3.SIDE_NOSE_LEFT,
              a=dict(cam="held just above her eye line and a little off to the side, angled slightly down",
                     turn="her face turned about twenty-five degrees towards the left-hand edge of the picture, level",
                     dist="framed very close", place="the corner of her near eye sits high and slightly right of centre"),
              b=dict(cam="held at her eye line, off to the same side",
                     turn="her face turned about thirty degrees towards the left-hand edge of the picture, level",
                     dist="framed a touch less close, but still close", place="the corner of her near eye sits centred")),
    "b": dict(side=r3.SIDE_NOSE_LEFT,
              a=dict(cam="held at her eye line, a hand's width from the outer corner of her left eye",
                     turn="her face turned about thirty degrees towards the left-hand edge of the picture, level",
                     dist="framed very close", place="the eye corner sits high and right of centre"),
              b=dict(cam="held just below her eye line and tilted up slightly",
                     turn="her face turned about thirty-five degrees towards the left-hand edge of the picture, level",
                     dist="framed a touch closer still", place="the eye corner sits centred and a little low")),
    "c": dict(side=r3.SIDE_NOSE_LEFT,
              a=dict(cam="held at her eye line, well out to the side",
                     turn="her face turned about forty-five degrees towards the left-hand edge of the picture, level",
                     dist="framed close", place="her near eye sits high and right of centre"),
              b=dict(cam="held a little below her eye line, well out to the same side, tilted up",
                     turn="her face turned about fifty degrees towards the left-hand edge of the picture, level",
                     dist="framed a touch closer", place="her near eye sits centred")),
    # matrixyl-finelines — one side locked per woman; right panel level or LOWER, chin never lifted
    "d": dict(side=r3.SIDE_NOSE_RIGHT,
              a=dict(cam="held at her eye line, a little off to the side",
                     turn="her face turned about twenty-five degrees towards the right-hand edge of the picture, chin level",
                     dist="framed close", place="her near eye and cheek sit centred"),
              b=dict(cam="held a little below her eye line and tilted up slightly",
                     turn="her face turned about thirty degrees towards the right-hand edge of the picture, chin level",
                     dist="framed a touch less close, but still close", place="her near cheek sits a little left of centre")),
    "e": dict(side=r3.SIDE_NOSE_LEFT,
              a=dict(cam="held a little above her eye line and angled down slightly",
                     turn="her face turned about twenty degrees towards the left-hand edge of the picture, chin level",
                     dist="framed close", place="her face sits centred"),
              b=dict(cam="held at her eye line",
                     turn="her face turned about twenty-five degrees towards the left-hand edge of the picture, chin level",
                     dist="framed a touch less close, but still close", place="her face sits a little right of centre")),
    "f": dict(side=r3.SIDE_NOSE_RIGHT,
              a=dict(cam="held at her eye line, well out to the side",
                     turn="her face turned about forty-five degrees towards the right-hand edge of the picture, chin level",
                     dist="framed close", place="her near eye sits high and left of centre"),
              b=dict(cam="held a little below her eye line, well out to the same side",
                     turn="her face turned about fifty degrees towards the right-hand edge of the picture, chin level",
                     dist="framed a touch closer", place="her near eye sits centred")),
}
GAZE = {
    "a": ("her eyes are on the lens", "her eyes look a little away from the lens, off to the side"),
    "b": ("her eye looks straight ahead, just past the lens", "her eye looks a fraction to one side of the lens"),
    "c": ("her eyes look ahead, past the camera", "her eyes glance a little towards the lens"),
    "d": ("her eyes are on the lens", "her eyes are a little off the lens, towards the far side"),
    "e": ("her eyes are just off the lens to one side", "her eyes are on the lens"),
    "f": ("her eyes look ahead, past the camera", "her eyes look a little down and away"),
}
WOMEN = [
    # ---- matrixyl-deepwrinkles · Sederma 2013 · ages 42-67 in the study; cast 50-61 ------------------------
    dict(block="matrixyl-deepwrinkles", key="a", crop="dw_three_quarter", walls=(0, 1),
         who=("a white DUTCH woman of about fifty-eight, with short silver-blonde hair swept back from her face, "
              "fair skin with a cool pink undertone, pale blue eyes, light brows, and one small flat brown mole on "
              "her left temple beside the corner of her left eye"),
         before=("At the outer corner of the near eye three deep lines fan out towards the temple - real creases "
                 "that stay there at rest, each casting a clear shadow - with finer crinkles between and below them "
                 "running down onto the top of the cheek.")),
    dict(block="matrixyl-deepwrinkles", key="b", crop="dw_eye_corner", walls=(2, 3),
         who=("a white AUSTRIAN woman of about sixty-one, with chin-length grey-brown hair tucked behind her ear, "
              "fair skin with a warm undertone and a few faint sun freckles on the cheekbone, grey-green eyes, "
              "and a small flat brown mole just below the outer corner of her left eye"),
         before=("From the outer corner of her left eye two long, deep creases run out across the temple and a "
                 "third curves down onto the cheekbone, with shorter fine lines and a crepey texture between them.")),
    dict(block="matrixyl-deepwrinkles", key="c", crop="dw_steep", walls=(4, 5),
         who=("a white BELGIAN woman of about fifty-three, with shoulder-length chestnut-brown hair pulled loosely "
              "back, fair skin, brown eyes, dark brows, and a tiny dark mole high on her left cheek"),
         before=("Seen from the side, a fan of deep lines spreads from the outer corner of the near eye across the "
                 "side of her face - three of them deep and long, casting clear shadows - with finer crinkles "
                 "between them.")),
    # ---- matrixyl-finelines · Robinson 2005 · ages 35-55 in the trial; cast 43-53 -------------------------
    dict(block="matrixyl-finelines", key="d", crop="fl_eye_cheek", walls=(6, 7),
         who=("a white DANISH woman of about forty-seven, with straight dark-blonde hair cut to the shoulder and "
              "tucked back, fair skin with a few freckles across the nose, blue eyes, and one small flat brown mole "
              "on her right cheek"),
         before=("Fine lines fan out from the outer corner of her near eye, two or three faint lines run under the "
                 "eye, and a few fine lines cross the upper cheek, visible where the light grazes the skin.")),
    dict(block="matrixyl-finelines", key="e", crop="fl_face", walls=(8, 9),
         who=("a white ITALIAN woman of about fifty, with wavy dark-brown hair pulled back, light olive skin, dark "
              "brown eyes, dark natural brows, and a small mole on her left cheekbone"),
         before=("Fine lines sit beside and under her eyes and a few cross her upper cheeks, a little clearer on the "
                 "near side where the light grazes the skin; the lines from her nose to the corners of her mouth are "
                 "just beginning to show.")),
    dict(block="matrixyl-finelines", key="f", crop="fl_side", walls=(10, 11),
         who=("a white ENGLISH woman of about fifty-two, with a light-brown bob tucked behind her ear, fair skin "
              "with a pinkish undertone, hazel eyes, and a small flat brown mole on her right temple"),
         before=("Seen from the side, fine lines fan out from the outer corner of the near eye and a few run across "
                 "the upper cheek, with a fine, slightly crinkled texture that catches the grazing light.")),
]
LIGHT = cu.LIGHT


def main() -> None:
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
            "id": f"mxb1--{w['block']}-{w['key']}",
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
                "scripts/build-matrixyl-before-after-config.py on the round-3 brief machinery"),
        "note": ("MATRIXYL 3000 SCIENCE PAGE, TWO BEFORE/AFTER CARDS. matrixyl-deepwrinkles (slots a-c) -> "
                 "/pages/matrixyl-3000-research key_findings_ba f1, Sederma's half-face study (23 women aged 42-67, "
                 "2 months; deep-wrinkle area -39%, depth about a fifth; her LEFT side locked). matrixyl-finelines "
                 "(slots d-f) -> f2, Robinson 2005 pentapeptide-4 (93 women, 12 weeks, a small effect; no numbers). "
                 "MALCOLM, 2026-09-26: the round-3 look (Caucasian, close-up, plain wall); card 2 = pentapeptide-4. "
                 "CANDIDATES ONLY; Malcolm picks with _ / __. Smoke test: slots a and d on all six suppliers first."),
        "target_templates": ["templates/page.research-matrixyl.json"],
        "labels_are_composited": "NOT composited. Labels are text settings on the theme section.",
        "defaults": {"candidates": 1, "negative_global": r3.NEGATIVE_GLOBAL, "negative_class_b": ""},
        "slots": slots,
    }
    OUT.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {OUT.relative_to(ROOT)} — {len(slots)} slots")
    for s in slots:
        print(f"  {s['id']:<38} prompt {len(s['prompt']):>5}  luma {len(s['prompt_luma']):>5}")


if __name__ == "__main__":
    main()
