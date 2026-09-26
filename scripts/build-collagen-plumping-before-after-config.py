#!/usr/bin/env python3
"""Build the before/after wave for the two proof cards on the collagen & skin-plumping concern page (round 1).

    python3 scripts/build-collagen-plumping-before-after-config.py
    → configs/banners/before-after-collagen-plumping-r1.json

    set -a; source ~/.claude/config/image-credentials.env; set +a
    python3 scripts/generate-multi.py configs/banners/before-after-collagen-plumping-r1.json \
        --candidates 1 --only <slot-id>[,<slot-id>]

Malcolm, 2026-09-26, on /pages/collagen-skin-plumping: "lets also add 2 content sections (text and before and after
image) where we show the proven benefits of what peptides can do for that topic of skin concern. we can create new
study before and after images for these sections."

REUSE, NOT A COPY. The brief machinery is the round-3 builder (scripts/build-under-eye-forehead-before-after-config.py)
and the face-cream card, its crops and its light are the copper builder's (scripts/build-copper-before-after-config.py),
both imported unchanged. This file supplies only what is new: the Matrixyl 3000 deep-wrinkle card, the viewpoints,
gaze and the six women (none of them the copper page's women), and the concern-page targets.

THE TWO CARDS, AND WHAT EACH PICTURE MAY CLAIM
  matrixyl-deepwrinkles  f1 - Matrixyl 3000, the manufacturer's half-face study (docs/claims/matrixyl-3000.md §8.5):
                         23 women aged 42-67, 3% cream on one half and placebo on the other, 2 months. Area taken up
                         by deep wrinkles -39.4% from the start (p<0.01); main-wrinkle depth -19.9%. The brochure's
                         own photo pair is the outer eye corner, so show that. Depth fell by about a fifth, so the
                         deepest lines stay visible, only shallower, with fewer stretches that read as deep creases.
                         NOT allowed (§8.5): wrinkles erased, a lift or firmer lids, a change in tone, colour, pigment,
                         eye bags or brow position, or plumping. The treated side is not published: her LEFT side is
                         locked (nose to the left-hand edge), the opposite of the copper page's right-side pair.
  copper-firmness        f2 - the 2002 copper-peptide face-cream study, 71 women, 12 weeks, known from published
                         reviews: "improved skin laxity, clarity, and appearance, reduced fine lines and the depth of
                         wrinkles, and increased skin density and thickness" (docs/claims/copper-peptide-ghk-cu.md §8).
                         No numbers were published, so the copper builder's face-cream brief (a MODEST change, nothing
                         lifted, tightened, filled or slimmed) is used exactly as it is.

SUPPLIERS: all six (website-imagery rule 1). Smoke-test slots a and d first.
Author: Claude Code, 2026-09-26. Candidates only; nothing is uploaded or published by this file.
"""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


cu = _load("cu", "scripts/build-copper-before-after-config.py")
r3 = cu.r3

WAVE = "before-after-collagen-plumping-r1"
OUT = ROOT / "configs" / "banners" / f"{WAVE}.json"
ROUND = "r1"
SMOKE_SLOTS = {"a", "d"}
PAGE, TEMPLATE, SECTION = "/pages/collagen-skin-plumping", "templates/page.collagen-skin-plumping.json", "proof"

CROPS = {k: v for k, v in cu.CROPS.items()}

BLOCKS = {
    "matrixyl-deepwrinkles": dict(
        page=PAGE, template=TEMPLATE, block="f1", heading="Deep-Wrinkle Area -39% in 2 Months", study="sederma-2013-halfface",
        after_label="After 2 months",
        expression=cu.BLOCKS["copper-crowsfeet"]["expression"],
        honesty=("EVERY LINE AT THE OUTER CORNER OF HER EYE IS STILL THERE IN THE RIGHT PANEL - the same lines, each in the "
                 "same place and the same direction, and the deepest of them still clearly visible as creases. None has "
                 "disappeared and the skin there has NOT become smooth, tight, lifted or shiny. What has changed is that the "
                 "deep creases are a little shallower, so fewer stretches of them read as deep lines: parts of them now read "
                 "as fine lines, holding a softer, narrower shadow."),
        luma_magnitude=("Every eye-corner line is still there; the deep creases are a little shallower, so fewer stretches "
                        "of them read as deep lines. Visible when the panels are compared, but anyone seeing this panel "
                        "alone would still say she has lines at the corner of her eye."),
        luma_honesty=("Every line at the corner of her eye is still there - same place and direction, the deepest still "
                      "clearly visible; they are only a little shallower. Nothing lifted, tightened or filled."),
        feature=cu.BLOCKS["copper-crowsfeet"]["feature"],
        nothing_else=("NOTHING OUTSIDE THE EYE CORNER HAS CHANGED. Her eyelids, her brows and their height, the skin under "
                      "her eyes, her skin tone and colour, any marks or spots, her cheeks and her jaw look exactly the same "
                      "in both panels; only the depth of the lines at the outer corner of her eye is different."),
        age=("SHE IS BETWEEN FIFTY AND SIXTY-FOUR - MIDDLE-AGED TO OLDER MIDDLE AGE - AND THAT GOVERNS WHAT HER SKIN CAN "
             "HONESTLY LOOK LIKE. The lines at the corners of her eyes are deep and established, two or three of them "
             "true creases that stay with her face at rest, with finer crinkles between them; some grey in her hair is "
             "normal. But she is NOT elderly: no hooded drooping lids, no deep sagging, none of the slackness of a woman "
             "in her late seventies."),
        subject=("IN THE LEFT PANEL, THE DEEP CREASES FANNING OUT FROM THE OUTER CORNER OF HER EYE ARE THE SUBJECT OF THE "
                 "PICTURE. "),
        magnitude=("THE SAME LINES FAN OUT FROM THE CORNER OF HER EYE IN THE RIGHT PANEL, IN THE SAME PLACES. The deepest "
                   "creases are a little SHALLOWER - each about four-fifths as deep - so they hold a narrower, softer "
                   "shadow, and FEWER STRETCHES OF THEM READ AS DEEP CREASES: along part of their length they now read as "
                   "fine lines. The finer crinkles between them are about the same.\n\n"
                   "THE SIZE OF THE CHANGE IS NARROW AT BOTH ENDS. It must be VISIBLE: someone comparing the two panels "
                   "should see that the deep creases at the eye corner are shallower in the right one and be able to point "
                   "to where. But it is MODEST: anyone looking at the right panel on its own would still say this woman has "
                   "deep lines at the corners of her eyes. The eye corner has not been smoothed, lifted, filled or made "
                   "young. A right panel with a smooth, line-free eye corner is a failure, not a success."),
        negatives=("no smiling, no squinting, no laughing, no closed eyes, no eye makeup, no change of eye shape between the "
                   "panels, no lifted eyelid in the right panel, no raised brow in the right panel, no smooth line-free eye "
                   "corner in the right panel, no line disappearing between the panels, no shiny skin at the eye corner, "
                   "no filler look, no plumped skin, no brighter or more even skin tone in the right panel, no fewer spots "
                   "in the right panel, no smaller eye bags in the right panel, no smoother forehead in the right panel, "
                   "no rested younger face in the right panel, no crack in the skin, no cut, no scar, no red line, "
                   "no woman under forty-five, no elderly woman, no hooded drooping eyelids"),
    ),
    "copper-firmness": dict(cu.BLOCKS["copper-facecream"], page=PAGE, template=TEMPLATE, block="f2",
                            heading="Firmer, Denser-Looking Skin in 12 Weeks"),
}

NOSE_LEFT = r3.SIDE_NOSE_LEFT          # her LEFT side toward the camera, locked in both panels
VIEWPOINTS = {
    # matrixyl-deepwrinkles — her left side; right panel level or a touch LOWER (crow's feet read the same from any height)
    "a": dict(side=NOSE_LEFT,
              a=dict(cam="held just above her eye line and a little off to the side, angled slightly down",
                     turn="her face turned about twenty-five degrees towards the left-hand edge of the picture, level",
                     dist="framed very close", place="the corner of her near eye sits high and slightly right of centre"),
              b=dict(cam="held at her eye line, off to the same side",
                     turn="her face turned about thirty degrees towards the left-hand edge of the picture, level",
                     dist="framed a touch less close, but still close", place="the corner of her near eye sits centred")),
    "b": dict(side=NOSE_LEFT,
              a=dict(cam="held at her eye line, a hand's width from the outer corner of her left eye",
                     turn="her face turned about thirty degrees towards the left-hand edge of the picture, level",
                     dist="framed very close", place="the eye corner sits high and right of centre"),
              b=dict(cam="held just below her eye line and tilted up slightly",
                     turn="her face turned about thirty-five degrees towards the left-hand edge of the picture, level",
                     dist="framed a touch closer still", place="the eye corner sits centred and a little low")),
    "c": dict(side=NOSE_LEFT,
              a=dict(cam="held at her eye line, well out to the side",
                     turn="her face turned about forty-five degrees towards the left-hand edge of the picture, level",
                     dist="framed close", place="her near eye sits high and right of centre"),
              b=dict(cam="held a little below her eye line, well out to the same side, tilted up",
                     turn="her face turned about fifty degrees towards the left-hand edge of the picture, level",
                     dist="framed a touch closer", place="her near eye sits centred")),
    # copper-firmness — one side locked per woman; right panel level or LOWER, chin never lifted (copper rule)
    "d": dict(side=r3.SIDE_NOSE_RIGHT,
              a=dict(cam="held at her mouth level, a little off to the side",
                     turn="her face turned about twenty-five degrees towards the right-hand edge of the picture, chin level",
                     dist="framed very close", place="her near cheek sits centred and high"),
              b=dict(cam="held a little below her mouth level and tilted up slightly",
                     turn="her face turned about thirty degrees towards the right-hand edge of the picture, chin level",
                     dist="framed a touch less close, but still close", place="her near cheek sits right of centre")),
    "e": dict(side=r3.SIDE_NOSE_LEFT,
              a=dict(cam="held at her cheekbone level, well out to the side",
                     turn="her face turned about fifty degrees towards the left-hand edge of the picture, chin level",
                     dist="framed close", place="her jaw sits in the lower third of the panel"),
              b=dict(cam="held at her mouth level, well out to the same side",
                     turn="her face turned about fifty-five degrees towards the left-hand edge of the picture, chin level",
                     dist="framed a touch closer", place="her jaw sits a little lower in the panel")),
    "f": dict(side=r3.SIDE_NOSE_RIGHT,
              a=dict(cam="held a little above her eye line and angled down slightly",
                     turn="her face turned about twenty degrees towards the right-hand edge of the picture, chin level",
                     dist="framed very close", place="her face sits centred"),
              b=dict(cam="held at her eye line",
                     turn="her face turned about twenty-five degrees towards the right-hand edge of the picture, chin level",
                     dist="framed a touch less close, but still close", place="her face sits a little left of centre")),
}
GAZE = cu.GAZE

WOMEN = [
    # ---- matrixyl-deepwrinkles · Sederma half-face study · women 42-67; cast 52-63 -------------
    dict(block="matrixyl-deepwrinkles", key="a", crop="cf_three_quarter", walls=(1, 2),
         who=("a white DUTCH woman of about fifty-eight, with a chin-length silver-blonde bob tucked behind her ear, fair "
              "skin with a warm undertone, light blue eyes, fair brows, and one small flat brown mole on her left temple "
              "beside the corner of her left eye"),
         before=("At the outer corner of the near eye three deep creases fan out towards the temple, the middle one the "
                 "longest and deepest, with finer crinkles running between them and a couple of short lines dropping onto "
                 "the top of the cheek. Each deep crease casts a clear shadow where the light grazes it.")),
    dict(block="matrixyl-deepwrinkles", key="b", crop="cf_eye_corner", walls=(3, 4),
         who=("a white SCOTTISH woman of about sixty-two, with short silver-grey hair, very fair skin with fine freckles "
              "across the cheekbones, green-grey eyes, pale brows, and a small flat brown mole on the top of her left "
              "cheekbone below the outer corner of her left eye"),
         before=("From the outer corner of her left eye two long, deep creases run out across the temple, a third deep "
                 "line curves down onto the cheekbone, and fine crinkled lines fill the thin skin between them.")),
    dict(block="matrixyl-deepwrinkles", key="c", crop="cf_steep", walls=(5, 6),
         who=("a white ITALIAN woman of about fifty-four, with thick dark-brown hair streaked with grey, pulled back, "
              "lightly olive skin, brown eyes, dark brows, and a tiny dark mole high on her left cheek"),
         before=("Seen from the side, deep creases spread from the outer corner of the near eye across the side of her "
                 "face, three of them long and clearly etched, with finer crinkles between them and short lines running "
                 "down onto the cheekbone.")),
    # ---- copper-firmness · the 2002 face-cream study, 71 women; cast 48-56 ---------------------
    dict(block="copper-firmness", key="d", crop="lf_three_quarter", walls=(7, 8),
         who=("a white POLISH woman of about fifty-one, with shoulder-length ash-brown hair tucked behind her ear, fair "
              "skin with a neutral undertone, grey-blue eyes, and one small flat brown mole on her right cheek near the "
              "corner of her mouth"),
         before=("The skin of her near cheek has a scatter of fine lines running down and forward towards the corner of "
                 "her mouth, and a slightly loose, crepey texture that shows where the light grazes it. The line from her "
                 "nose to the corner of her mouth is established, and the contour where the cheek meets the jaw is a "
                 "little soft.")),
    dict(block="copper-firmness", key="e", crop="lf_cheek_jaw", walls=(9, 10),
         who=("a white AUSTRIAN woman of about fifty-five, with light-brown hair in a low knot, fair skin with a few faint "
              "sun spots on the cheekbone, hazel eyes, and a small flat brown mole on her left cheek just above the "
              "jawline"),
         before=("Along the near cheek, from the cheekbone down to the jaw, the skin has fine lines and a slightly crepey "
                 "texture that catches the grazing light, and the line of the jaw has begun to soften, with a gentle "
                 "fullness just in front of the ear.")),
    dict(block="copper-firmness", key="f", crop="lf_face", walls=(11, 0),
         who=("a white BELGIAN woman of about forty-eight, with wavy honey-blonde shoulder-length hair, fair skin with a "
              "light golden undertone, brown eyes, natural brows, and a small mole on her right cheekbone"),
         before=("Her cheeks have fine lines and a slightly loose, uneven texture, a little clearer on the near side where "
                 "the light grazes it, and the lines from her nose to the corners of her mouth are established. Her "
                 "jawline has begun to soften a little.")),
]


def main() -> None:
    # inject this wave's parts into the round-3 builder, then use its brief machinery unchanged
    r3.CROPS, r3.BLOCKS, r3.VIEWPOINTS, r3.GAZE, r3.LIGHT = CROPS, BLOCKS, VIEWPOINTS, GAZE, cu.LIGHT
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
            "id": f"cpb1--{w['block']}-{w['key']}",
            "title": f"{w['block']} · {b['study']} · {CROPS[w['crop']]['label']} — {w['who'].split(',')[0].replace('a ', '', 1)}",
            "class": "B", "width": r3.SIZE, "height": r3.SIZE,
            "target_slot": f"{b['page']} {SECTION} {b['block']} ({b['heading']})",
            "generated_from": f"{ROUND}{' smoke slot' if w['key'] in SMOKE_SLOTS else ''}",
            "ref_files": [], "prompt": prompt, "prompt_luma": prompt_luma,
            "label": {"left": "Before", "right": b["after_label"], "figure": "",
                      "measure": "(labels are theme settings, never pixels)", "cite": b["study"]},
            "negative_extra": negative_extra,
        })
    cfg = {
        "wave": WAVE, "created": "2026-09-26", "round": ROUND,
        "doc": ("docs/clinical-trial-before-after-images.md, .claude/rules/website-imagery.md, built by "
                "scripts/build-collagen-plumping-before-after-config.py on the round-3 brief machinery"),
        "note": ("COLLAGEN & SKIN-PLUMPING CONCERN PAGE, TWO PROOF CARDS (new research-before-after section 'proof'). "
                 "matrixyl-deepwrinkles (slots a-c) -> f1, Sederma half-face study (23 women aged 42-67, 3% cream, placebo "
                 "half, deep-wrinkle area -39.4%, depth -19.9%; her LEFT side locked). copper-firmness (slots d-f) -> f2, "
                 "the 2002 face-cream study (71 women, 12 weeks; no numbers published, so a modest change). MALCOLM, "
                 "2026-09-26: 'we can create new study before and after images for these sections'. CANDIDATES ONLY; "
                 "Malcolm picks with _ / __. Smoke test: slots a and d on all six suppliers first."),
        "target_templates": [TEMPLATE],
        "labels_are_composited": "NOT composited. Labels are text settings on the theme section.",
        "defaults": {"candidates": 1, "negative_global": r3.NEGATIVE_GLOBAL, "negative_class_b": ""},
        "slots": slots,
    }
    OUT.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {OUT.relative_to(ROOT)} — {len(slots)} slots")
    for s in slots:
        print(f"  {s['id']:<40} prompt {len(s['prompt']):>5}  luma {len(s['prompt_luma']):>5}")


if __name__ == "__main__":
    main()
