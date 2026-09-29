#!/usr/bin/env python3
"""Build the before/after waves for glutathione findings cards f1, f2 and f3 (science-page template).

    python3 scripts/build-glutathione-cards-before-after-config.py              # round 3, the current round
    → configs/banners/before-after-glutathione-cards-r3.json (card f3, Wahab 2021)
    python3 scripts/build-glutathione-cards-before-after-config.py --round r1   # re-proves round 1
    python3 scripts/build-glutathione-cards-before-after-config.py --round r2   # re-proves rounds 1 and 2
    → write NOTHING; assert that configs/banners/before-after-glutathione-cards-r1.json / -r2.json
      (committed) are reproduced byte for byte. Every r3 build runs both checks first, so an r3 edit that
      leaks into an earlier brief fails the build instead of silently rewriting a committed record.
      (Until 2026-09-29 `--round r2` WROTE the r2 file; it now only proves it, as r1 did once r2 existed.)

    python3 -u scripts/generate-multi.py configs/banners/before-after-glutathione-cards-r3.json \
        --candidates 1 --only <slot-id>[,<slot-id>]
    python3 scripts/wave-contact-sheet.py before-after-glutathione-cards-r3 \
        --stable-labels configs/banners/before-after-glutathione-cards-r3.json --expect 5 --tile 400

⚠️ `--candidates 1` IS NOT OPTIONAL: generate-multi.py never reads `defaults.candidates` and its flag
defaults to 2, which silently doubles the spend.

BYTE-IDENTICAL MEANS "AFTER PRETTIER". The pre-commit hook runs Prettier over every JSON file, and Prettier
folds short arrays onto one line, so the committed r1 file is json.dumps() output plus that one reflow.
The builder pipes its output through the repo's own node_modules/.bin/prettier before comparing or
writing; without Prettier it falls back to comparing the parsed JSON and says so.

=====================================================================================================
ROUND 1 (2026-09-26) - the record below is unchanged; round 2 is at the end of this docstring.
=====================================================================================================

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

=====================================================================================================
ROUND 2 (2026-09-29) - configs/banners/before-after-glutathione-cards-r2.json, slot ids glub2--*
=====================================================================================================
Malcolm, 2026-09-29, verbatim: "the befoe and after images for the Glutathione trials need to be made
again. this time with caucasian women - and the clothes should be random. now they are the same tshirt
and same colors. these need to vary. also lets not use women with warts - as very few women have them -
and we use them in nearly all images." That order is also the approval for the spend (all suppliers).

Everything in round 1 stands (walls, crops, viewpoints, gaze, tone-pair light, honesty rules, §8.5)
EXCEPT these five changes. Each is an exact-string swap into the round-3 skeleton or an r2 copy of an r1
field; r1's own tables are never edited, which is what keeps r1 reproducible.
  1. CASTING: CAUCASIAN WOMEN WITH LIGHT-OLIVE, MEDITERRANEAN-TYPE SKIN (WOMEN_R2). The page says the
     trials did not cover fair skin, so the nearest honest Caucasian casting is the complexion that tans
     easily: Italian, Greek, Spanish, Portuguese, southern French, Croatian; late thirties to mid-forties;
     six different hair colours and styles (bob, low ponytail, loose waves, short crop, low bun, plait).
     Skin is described in words - a roman numeral is text an engine can print. f1's tan becomes "a light,
     even tan over light-olive skin" (still no "sun": asserted). r1's casting negatives (no Caucasian /
     European / fair-skinned model) are dropped; `no non-white model` stays removed; casting is stated
     positively.
  2. NO MOLES, WARTS, SKIN TAGS OR BEAUTY MARKS, ANYWHERE. Round 1 gave every woman "one small, pale mole"
     as her identity anchor, and Malcolm reads them as warts. Removed from every subject, from rule ONE,
     from the identity lock, from the side-lock ("with the same marks on it", "every mole and mark sits on
     the same side"), from the point-of-change restatement, from SKIN, from the Luma brief and from two
     negatives ("no moles disappearing ..."). Identity is now held by FACE SHAPE, NOSE, BROWS, HAIRLINE,
     EARS AND HAIR COLOUR, and the identity lock says so. The marks are NAMED ONLY IN THE NEGATIVES
     (describe-the-thing-dont-name-it: a named noun gets drawn); the positive text says her skin carries
     nothing but pores, fine hairs and fine lines. Asserted: no mole / wart / skin tag / beauty mark /
     freckle word in anything an engine reads as a positive. Realism still comes from pores, vellus hair
     and fine lines, and SKIN_R2 says a smooth, poreless face reads as a filter.
  3. CLOTHES VARY, ACROSS SLOTS AND BETWEEN THE TWO PANELS (GARMENTS_R2). Round 1 dressed all 35 candidates
     in "a grey one on one day and a navy one on the other". Each slot now draws two different garments
     (different type AND different colour family) from GARMENT_POOL, by a seeded shuffle (GARMENT_SEED) so
     the build is reproducible; no garment is used twice in the wave. FAIRNESS RULES, asserted:
       f1 (tone): the right-panel garment is the same depth of colour or DARKER than the left, never white
       or near-white (a pale top bounces light onto the face and would fake the brightening); both
       garments muted (a strong colour tints the jaw); both open at the neck (the paler skin under her jaw
       is the ceiling a viewer checks, so no roll-neck or zipped collar).
       f2 (crow's feet): any colours, but the right-panel garment is never white or near-white.
     Nothing printed or branded on any garment (negatives), and the brief says the two are different
     garments, not one top in another colour.
  4. f2 "SAME BRIGHTNESS" IS NOW A MATCHING REQUIREMENT, stated the way f1's is (round-1 QA: nbp_pro and
     nbp_flash lit or exposed the f2 right panel lighter on d and f). Rule FOUR, the light paragraph, the
     point-of-change restatement and the Luma brief say: exposure, white balance and skin brightness MATCH
     between the panels, and the proof is what does not change - the whites of her eyes, her hair and her
     lips; only the crow's-feet lines differ.
  5. SLOT IDS glub2--f1-tone-a/b/c, glub2--f2-crowsfeet-d/e/f. Asserted: no id prefixes another, and no r2
     id prefixes an r1 id or the reverse (generate-multi --only and the uploader both match by prefix).

SMOKE LOG, r2: R2_SMOKE_LOG beside SMOKE_SLOTS_R2 below (slot a; two brief faults found and fixed for b-f).

FULL WAVE, r2, 2026-09-29: 36 of 36, no refusals (slot a on the smoke brief, b-f on the revised one; run
folder assets/ai-generated/2026-08-22-multi-before-after-glutathione-cards-r2, manifests manifest-smoke-a.json
and manifest.json). Sheet: ~/Desktop/skingenetix-glutathione-before-after-r2.png, rows A-F from this config
(stable labels), columns 1-6 = flux2, gpt_image, luma, nbp_flash, nbp_pro, seedream in every row.
  THE FOUR NEW RULES: casting held on 30 of 36 (not flux2); no mole, wart, skin tag or beauty mark on any of
  the 36 at 100% (tiny pale raised bumps on luma F3 and seedream E6/F6, a pale dot at gpt_image D2's inner eye
  corner); the briefed garment pair on 30 of 36 (flux2 undressed on all six); every dressed f1 tile's
  right-panel top is the same depth or darker, muted, never white.
  STILL OPEN: luma overshoots the f1 ceiling and drifts pale-grey even after smoke fix 2 (B3 reads as a paler
  woman; C3 a pale ring round the eye); nbp_flash still lightens the f2 right panel and nearly erases the lines
  (D4, E4) - round 1's leak, not closed by change 4 on that engine; luma and the nbp engines still border most
  pairs; seedream drew crow's feet as black ink strokes again (E6) and a blotchy, red-nosed f1 left panel (A6);
  nbp_pro broke the side-lock on E5; flux2 stayed pale, older and undressed. gpt_image held every rule on all
  six slots.
Author: Claude Code, 2026-09-29. Candidates only; nothing is uploaded or published by this file.

=====================================================================================================
ROUND 3 (2026-09-29) - configs/banners/before-after-glutathione-cards-r3.json, slot ids glub3--f3-tone-g/h/i
=====================================================================================================
Malcolm, 2026-09-29: "New wave, all suppliers" for card 3 (the approval for the spend). Card f3 is the
independent trial, Wahab et al. 2021 (register §8.1): 46 Indonesian women aged 20-44 (mean 30); every woman
put a serum with 2% glutathione and vitamin C on one cheek and a matching placebo serum on the other, morning
and evening for 8 weeks, with SPF each morning. On the serum side the melanin index fell 10.8% while the
placebo side rose 1.8% (p = 0.029), and skin lightness (L*) improved (p = 0.046). So the pair is a TONE pair
exactly like f1: a MODEST, even, whole-cheek brightening; plainly the same woman and skin tone; never lighter
than the skin under her own jaw; no change in evenness, spots, redness, pores, texture or lines (§8.5 f1).

REUSE, NOT A COPY. Round 2's f1 block, skeleton swaps, light (LIGHT_TONE_R2), skin (SKIN_R2, with both r2
smoke fixes), crops, identity lock, side-lock, no-marks rules, negatives and garment fairness rules are used
as they are. The r2 helpers p9_r2 / luma_dressed_r2 / swaps_r2 / luma_swaps_r2 / _garment_pair_ok gained
optional parameters (the garment table, the block table) and a TONE_KEYS set that adds f3's keys g-i; r2's
keys a-f are untouched, and the r2 byte check proves it. What round 3 changes:
  1. THE CARD: block f3, study wahab-2021, label "After 8 weeks" (a theme setting, never pixels).
  2. AGE: EARLY TO MID THIRTIES (the trial's mean was 30, range 20-44), not late thirties to mid-forties.
     The age paragraph is new and the age negatives follow it (no woman in her early twenties, none over
     forty); every other f1 negative is kept.
  3. THREE NEW WOMEN (WOMEN_RD3): Caucasian, light-olive Mediterranean-type skin with a light, even tan, as
     round 2 (Malcolm's casting), but MALTESE, CYPRIOT and ALBANIAN - no nationality, hair style or garment
     from round 2 is repeated (asserted for nationality and garments). Their `before` lines are round 2's,
     matched by crop.
  4. CLOTHES: drawn by a seeded shuffle (GARMENT_SEED_RD3) from the garments round 2 did not use plus
     GARMENT_EXTRA_RD3 (new muted, open-necked ones), under round 2's f1 fairness rules: two different types
     and colour families per slot, the right-panel top never lighter and never white, both muted, both open
     at the neck. GARMENT_POOL itself is unchanged, so round 2's draw cannot move.
  5. WALLS AND VIEWPOINTS: new light-neutral walls (left panel white-ish, right panel pale grey, so the
     right panel's surroundings are never the brighter), right panel turned a touch LESS towards the camera,
     light leaning towards the near cheek on the left panel only - every difference runs against the
     improvement, as in round 2. Side lock varies by slot (L, R, L).
  NAMING: this file already imports the under-eye builder as `r3` and names its sentences R3_*; round 3's
  own names therefore end in _RD3 to keep the two apart.

SMOKE LOG, r3: RD3_SMOKE_LOG beside SMOKE_SLOTS_RD3 below (slot g; three brief faults found and fixed for h-i).

FULL WAVE, r3, 2026-09-29: 18 of 18 (slot g on the smoke brief, its nbp_flash and flux2 from an immediate
retry after provider 503s; h-i on the revised brief, no failure). Run folder
assets/ai-generated/2026-08-22-multi-before-after-glutathione-cards-r3 (manifests manifest-smoke-g.json,
manifest-smoke-g-retry.json, manifest.json). Sheet: ~/Desktop/skingenetix-glutathione-card3-before-after-r3.png,
rows A-C = slots g-i (stable labels), columns 1-6 = flux2, gpt_image, luma, nbp_flash, nbp_pro, seedream.
Centre-panel skin L* change (left -> right), round 2's card-1 pick for scale = +8.8:
  gpt_image +7.0 / +3.0 / +5.6    nbp_flash +4.3 / +6.6 / +9.1    nbp_pro +9.8 / +6.2 / +15.6
  seedream +11.2 / +5.1 / +11.3   luma +14.9 / +14.1 / +10.8      flux2 -5.4 / -2.1 / -3.3 (darker)
  HELD: no mole, wart, skin tag or beauty mark on any dressed tile; the briefed garment pair on 15 of 18 (flux2
  undressed); every right-panel top the same depth or darker; after the smoke fixes, casting held on 10 of 12
  (not flux2) and h-i read as thirties on gpt_image, nbp_flash and nbp_pro.
  FAILURES OF A RULE: nbp_pro C5 burned "DAY 1" / "DAY 2" captions into the panels; nbp_pro B5 has a phone edge
  and fingertip at the right edge of the right panel; seedream A6 is two different East-Asian-looking women
  (smoke brief); seedream C6 and all three luma overshoot the ceiling (right panel reads fairer, R/B falls
  about 0.4-0.6) and luma borders every pair; flux2 is pale, freckled and undressed on all three and mirrors
  A1. gpt_image and nbp_flash held every rule on all three slots.
"""
import argparse
import importlib.util
import json
import random
import re
import shutil
import subprocess
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


def r1_config() -> dict:
    """Round 1's config, exactly as committed on 2026-09-26 (537cae6). Returns it; never writes it."""
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
    return cfg


# ======================================================================================
# ROUND 2 (2026-09-29). Everything below is new; nothing above it changed except r1_config()'s name and
# its return (it used to write the file). See the ROUND 2 section of the docstring.
# ======================================================================================
WAVE_R2 = "before-after-glutathione-cards-r2"
OUT_R2 = ROOT / "configs" / "banners" / f"{WAVE_R2}.json"
ID_PREFIX_R1, ID_PREFIX_R2 = "glub1--", "glub2--"
#: r2 smoke-test slot(s): candidates generated from the brief in effect at smoke time.
SMOKE_SLOTS_R2 = {"a"}
SMOKE_BRIEF_R2 = ("assets/ai-generated/2026-08-22-multi-before-after-glutathione-cards-r2/"
                  "smoke-brief-r2-a.json")
R2_SMOKE_LOG = """
SMOKE LOG, 2026-09-29 (slot a, f1 tone; 6 of 6 returned; gpt_image resolved to gpt-image-2.5-sunburst).
Judged at 100% (panel crops and cheek crops) and at render size (~500 px). Slot a is NOT re-run; its brief
is at SMOKE_BRIEF_R2 (gitignored run folder), and the differences are the two fixes below.
  HELD - THE FOUR NEW RULES:
    Casting: a light-olive Mediterranean woman in her late thirties to forties on five of six (flux2: pale,
      older, heavily freckled - its known trait on this brief family).
    No marks: no mole, wart, skin tag, beauty mark or raised spot on any of the six at 100% (flux2 has one
      tiny pale bump beside the eye).
    Clothes: gpt_image, nbp_pro, nbp_flash, seedream and luma all wore the two briefed garments (a buttoned
      dusty-blue cardigan, then a sage-green round-neck jumper; nbp_pro wore the cardigan open). flux2: bare
      shoulders, no clothing.
    f1 fairness: both garments muted and of equal depth on every dressed tile; no right panel lighter-dressed.
  ALSO HELD: side-lock on five of six (flux2 flipped); no text anywhere; plain walls; no hand or phone.
  TWO BRIEF FAULTS, FIXED FOR SLOTS b-f:
    1. FLAT DARK FLECKS ON THE CHEEK AND NOSE. luma drew brown flecks across the left panel's cheek and nose
       that faded with the tan in the right panel - a change in freckles, which §8.5 forbids; gpt_image
       carried faint flecks (equal in both panels); flux2 heavy freckling. The positive text said the skin
       has "nothing on its surface but pores, fine hairs and fine lines", but never that the COLOUR is
       unbroken, and Luma sees no negatives. SKIN_R2 and LUMA_SKIN_R2 now say the colour is unbroken across
       cheeks, nose and forehead, each pore the same colour as the skin around it (described, not named).
    2. LUMA'S UNDERTONE WENT PINK-GREY and overshot the one-third ceiling (centre-face R/B 1.84 -> 1.58, the
       largest shift of the six). Its short magnitude lacked the main brief's "not pinker, not greyer"; it
       now has it. To stay under LUMA_CAP, Luma's copy of the lock line and of the dressed line were shortened
       ("her shoulders are never bare" is cut from Luma's copy only; Luma dressed her without it).
  NOT BRIEF FAULTS (known supplier traits, recorded, not changed): luma and nbp_flash framed the pair with a
  white border; seedream drew the left panel blotchy with a red nose and cleared it on the right (its
  clinical-"before" habit - a change in evenness and redness); nbp_flash's left cheek is shinier than its
  right; nbp_pro's brightening is the strongest of the credible five and its hair is pulled back, not a bob;
  flux2 older, pale, freckled, undressed, side flipped, right panel darker.
"""

# --------------------------------------------------------------------------------------
# Change 3: clothes. A pool of ordinary garments, each with the facts the fairness rules need:
#   depth  1 white or near-white, 2 light, 3 mid, 4 deep, 5 very deep / black
#   muted  True for soft, greyed colours; False for a strong colour that could tint the jaw on f1
#   open   True if the neck and the underside of the jaw stay visible (f1 needs them: the ceiling)
#   family the colour family, so the two panels of a pair are never the same colour in another shade
# Every phrase is plain everyday clothing; nothing is printed or branded (negatives).
# --------------------------------------------------------------------------------------
GARMENT_POOL = [
    # phrase                                               type          depth muted  open   family
    ("a sage-green knitted jumper with a round neck",      "jumper",       3, True,  True,  "green"),
    ("a charcoal-grey crew-neck T-shirt",                  "tee",          4, True,  True,  "grey"),
    ("a rust-coloured linen shirt, open at the neck",      "shirt",        3, False, True,  "orange"),
    ("a buttoned dusty-blue cardigan",                     "cardigan",     3, True,  True,  "blue"),
    ("a camel roll-neck jumper",                           "rollneck",     3, True,  False, "brown"),
    ("a burgundy blouse with a small collar",              "blouse",       4, False, True,  "red"),
    ("a navy-and-cream striped Breton top",                "breton",       3, False, True,  "navy"),
    ("a faded denim shirt",                                "shirt",        3, True,  True,  "blue"),
    ("an oatmeal hooded sweatshirt with the hood down",    "hoodie",       2, True,  True,  "neutral"),
    ("a black vest top under a thin black cardigan",       "vest",         5, True,  True,  "black"),
    ("a mustard-yellow ribbed jumper",                     "jumper",       2, False, True,  "yellow"),
    ("a soft lilac T-shirt",                               "tee",          2, False, True,  "purple"),
    ("a chocolate-brown knitted cardigan",                 "cardigan",     4, True,  True,  "brown"),
    ("a heather-grey sweatshirt",                          "sweatshirt",   2, True,  True,  "grey"),
    ("a white cotton shirt",                               "shirt",        1, True,  True,  "white"),
    ("a cobalt-blue fine-knit top",                        "top",          3, False, True,  "blue"),
    ("an olive-green utility shirt",                       "shirt",        4, True,  True,  "green"),
    ("a coral-red T-shirt",                                "tee",          3, False, True,  "red"),
    ("a teal wrap top",                                    "wrap",         3, False, True,  "teal"),
    ("a cream cable-knit jumper",                          "jumper",       1, True,  True,  "neutral"),
    ("a taupe V-neck jumper",                              "jumper",       3, True,  True,  "brown"),
    ("a slate-blue polo shirt",                            "polo",         3, True,  True,  "blue"),
    ("a forest-green zip-up fleece",                       "fleece",       4, False, False, "green"),
    ("a dove-grey long-sleeved top",                       "top",          2, True,  True,  "grey"),
]
GARMENT_SEED = 20260929
SLOT_KEYS_R2 = ("a", "b", "c", "d", "e", "f")
F1_KEYS = {"a", "b", "c"}
#: Round 3 (card f3) is a tone pair too. Its keys g-i join the tone rules; r2's keys a-f are unaffected.
F3_KEYS_RD3 = {"g", "h", "i"}
TONE_KEYS = F1_KEYS | F3_KEYS_RD3


def _garment_pair_ok(key: str, left: tuple, right: tuple) -> bool:
    if left[1] == right[1] or left[5] == right[5]:        # different type AND different colour family
        return False
    if right[2] < 2:                                     # no white or near-white right-panel top (f1 and f2)
        return False
    if key in TONE_KEYS:                                 # tone fairness: right no lighter, muted, neck open
        return right[2] >= left[2] and left[3] and right[3] and left[4] and right[4]
    return True


def pick_garments() -> dict:
    """Deterministic 'random' clothes: a seeded shuffle of the pool, re-drawn until every slot's pair
    passes the fairness rules. No garment is used twice in the wave."""
    rng = random.Random(GARMENT_SEED)
    for _ in range(100000):
        pool = list(GARMENT_POOL)
        rng.shuffle(pool)
        pairs = {k: (pool[2 * i], pool[2 * i + 1]) for i, k in enumerate(SLOT_KEYS_R2)}
        if all(_garment_pair_ok(k, *p) for k, p in pairs.items()):
            return pairs
    raise AssertionError("no garment draw satisfies the fairness rules")


GARMENTS_R2 = pick_garments()


def p9_r2(key: str, garments: dict = None) -> str:
    """Paragraph 9 for one slot: two named garments, different, dressed on both days. `garments` is
    round 3's table (GARMENTS_RD3); round 2 passes nothing."""
    left, right = (garments or GARMENTS_R2)[key]
    if key in TONE_KEYS:
        depth = ("The right-hand garment is the deeper colour of the two" if right[2] > left[2] else
                 "The two garments are about equally deep in colour")
        rule = (f"{depth}, and both are soft, muted colours: a pale or bright top throws its light and colour "
                "up onto her face, and a brighter face must never be the clothes.")
    else:
        rule = "The right-hand garment is a mid or deep colour, never a pale one."
    return (f"SHE IS DRESSED ON BOTH DAYS, AND IN DIFFERENT CLOTHES EACH DAY. In the left panel she is wearing "
            f"{left[0]}; in the right panel she is wearing {right[0]}. They are two plainly different "
            f"garments - not the same top in another colour - and both are plain everyday clothes with no "
            f"branding. {rule} Wherever the picture reaches down far enough, the garment is plainly there at "
            "the bottom edge; her shoulders are never bare. ALSO DIFFERENT BETWEEN THE TWO DAYS: her hair, "
            "the same cut and colour but falling or tied a little differently.")


def luma_dressed_r2(key: str, garments: dict = None) -> str:
    left, right = (garments or GARMENTS_R2)[key]
    tail = (" - two different garments, the right one no lighter" if key in TONE_KEYS else
            " - two different garments, the right one not pale")
    # (Luma kept her dressed on the smoke slot without the "shoulders never bare" clause's help; the clause
    # was cut from Luma's copy only, to make room for the smoke fixes under LUMA_CAP. The main brief keeps it.)
    return f"Hair a little different. Left panel: she wears {left[0]}; right panel: {right[0]}{tail}."


# --------------------------------------------------------------------------------------
# Change 1: the six women. Caucasian, light-olive Mediterranean-type skin, late thirties to mid-forties,
# different hair colours and styles. No mark of any kind on the skin (change 2).
# f1 women carry a light, even tan over light-olive skin (the trial's women were all "tan").
# --------------------------------------------------------------------------------------
WOMEN_R2 = [
    # ---- f1 tone · Watanabe 2014 · cheekbone ----------------------------------------------
    dict(block="f1-tone", key="a", crop="tone_three_quarter", walls=(0, 1),
         who=("an ITALIAN woman of about thirty-nine, with dark brown hair in a chin-length bob tucked behind "
              "her near ear, light-olive skin with a warm golden undertone and a light, even tan, hazel-brown "
              "eyes and natural dark brows"),
         before=("Across her near cheek and cheekbone the skin is one clear, even light tan - a uniform warm "
                 "golden-olive all over - a shade deeper and a little duller than the paler, shaded skin under "
                 "her jaw and down the front of her neck. The colour is the same all over the cheek; it simply "
                 "sits a shade darker and flatter than her own untanned skin.")),
    dict(block="f1-tone", key="b", crop="tone_cheek", walls=(2, 3),
         who=("a GREEK woman of about forty-four, with black hair showing a few grey strands at the temple, "
              "pulled back in a low ponytail, light-olive skin with a warm golden undertone and a light, even "
              "tan, dark brown eyes and thick natural dark brows"),
         before=("The skin over her near cheekbone is an even, uniform light tan, the same warm golden-olive all "
                 "across it, clear and smooth-toned. It reads a shade deeper and a little less bright than the "
                 "skin under her jaw.")),
    dict(block="f1-tone", key="c", crop="tone_face", walls=(4, 5),
         who=("a SPANISH woman of about forty-one, with chestnut-brown hair in loose shoulder-length waves pushed "
              "back off her face, an oval face, light-olive skin with a warm golden undertone and a light, even "
              "tan, brown eyes and natural brows"),
         before=("Her face carries a light, even tan: the near cheek and cheekbone are one clear, uniform warm "
                 "golden-olive, a shade deeper and a little duller than the paler skin under her chin and on "
                 "her neck.")),
    # ---- f2 crow's feet · Watanabe 2014 · outer eye corner ---------------------------------
    dict(block="f2-crowsfeet", key="d", crop="cf_three_quarter", walls=(6, 7),
         who=("a PORTUGUESE woman of about forty-five, with near-black hair cut short in a layered crop, a few "
              "grey strands at the temple, light-olive skin with a warm undertone, dark brown eyes and natural "
              "dark brows"),
         before=None),
    dict(block="f2-crowsfeet", key="e", crop="cf_eye_corner", walls=(8, 9),
         who=("a southern FRENCH woman of about forty-three, with mid-brown hair with a few grey strands at the "
              "parting, pulled back into a loose low bun, light-olive skin with a warm golden undertone, "
              "green-brown eyes and soft natural brows"),
         before=None),
    dict(block="f2-crowsfeet", key="f", crop="cf_steep", walls=(10, 11),
         who=("a CROATIAN woman of about forty-two, with long, very dark brown hair in a loose plait down her "
              "back, light-olive skin with a warm undertone, grey-green eyes and natural dark brows"),
         before=None),
]
# f2's `before` (what her crow's feet look like) is round 1's text, unchanged: it names no mark.
_R1_BEFORE = {w["key"]: w["before"] for w in WOMEN}
for _w in WOMEN_R2:
    if _w["before"] is None:
        _w["before"] = _R1_BEFORE[_w["key"]]

# --------------------------------------------------------------------------------------
# The r2 blocks: r1's blocks with the casting, age and mark text replaced, and f2's brightness match.
# --------------------------------------------------------------------------------------
_F1, _F2 = BLOCKS["f1-tone"], BLOCKS["f2-crowsfeet"]
_MOLE_NEG = "no mole disappearing between the panels, "
assert _F1["negatives"].count(_MOLE_NEG) == 1, "r1 f1 negatives changed"
CLOTHES_NEG_F1 = (", no white top in the right panel, no light-coloured top in the right panel, no paler "
                  "clothing in the right panel, no bright or saturated clothing, no same top in both panels, "
                  "no roll-neck, no polo neck, no turtleneck, no scarf")
CLOTHES_NEG_F2 = ", no white top in the right panel, no pale top in the right panel, no same top in both panels"
BLOCKS_R2 = {
    "f1-tone": dict(
        _F1,
        honesty=("THE CHANGE IS IN BRIGHTNESS ONLY, NOT IN EVENNESS, TEXTURE OR SHEEN. Her skin was already one "
                 "clear, even colour in the left panel and it is exactly as clear and even in the right, and her "
                 "pores, her skin texture and the fine lines at the corner of her eye are exactly the same. The "
                 "surface of her skin looks just as it did - the same slight oiliness at the nose, the same soft "
                 "matte cheek, no new sheen or glow. What has changed is that the whole "
                 "cheek is a shade lighter and brighter, evenly across it - but she is PLAINLY THE SAME "
                 "LIGHT-OLIVE-SKINNED WOMAN WITH A LIGHT TAN, with the same warm golden undertone, and the skin "
                 "of her face is never lighter than the paler skin under her jaw."),
        luma_honesty=("Her skin is exactly as clear and even as in the left panel, with the same pores, texture, "
                      "lines and the same soft matte surface. Plainly the same light-olive-skinned woman with a "
                      "light tan and the same warm undertone."),
        # Smoke fault 2 (r2, slot a): luma's right panel went pink-grey; its short form lacked the clause.
        luma_magnitude=("The whole cheek is a shade lighter and brighter, evenly, as if a little of her light tan "
                        "has lifted, with the same warm golden-olive undertone, not pinker or greyer - about a "
                        "third of the way towards "
                        "the paler skin under her jaw, never half. Still one even colour. Anyone seeing this panel "
                        "alone would still say she has light-olive, lightly tanned skin."),
        feature=("HER LIGHT TAN IS ONE CLEAR, EVEN, UNIFORM COLOUR ACROSS THE WHOLE CHEEK, soft and natural. It "
                 "reads by its overall colour alone."),
        age=("SHE IS IN HER LATE THIRTIES TO MID-FORTIES, AND THAT GOVERNS WHAT HER SKIN CAN HONESTLY LOOK LIKE. "
             "Fine lines are starting at the outer corners of her eyes, and hers is the everyday skin of a woman "
             "who works indoors and out. She is NOT young - clearly not in her twenties - and NOT old: no deep "
             "lines, no sagging, no slackness."),
        magnitude=("THE SKIN OF HER FACE IS A SHADE LIGHTER AND BRIGHTER IN THE RIGHT PANEL, EVENLY ACROSS THE "
                   "WHOLE CHEEK AND CHEEKBONE, as if a little of her light tan has lifted. It has moved about A "
                   "THIRD OF THE WAY from its tan towards the paler skin under her jaw - never as much as half the "
                   "way - so it is still plainly deeper than the skin under her jaw. It looks a little clearer and "
                   "livelier, less dull. It is still one even colour, exactly as even as it was. THE UNDERTONE DOES "
                   "NOT SHIFT: the lighter skin is the same warm golden-olive, only lighter - not pinker, not "
                   "greyer, not cooler.\n\n"
                   "THE SIZE OF THE CHANGE IS NARROW AT BOTH ENDS. It must be VISIBLE: someone comparing the two "
                   "panels should see that her cheek is a little brighter in the right one and be able to point "
                   "to where. But it is MODEST: anyone looking at the right panel on its own would still say this "
                   "woman has light-olive, lightly tanned skin. She has not become a fairer, paler or "
                   "different-looking person, and her skin has not turned pale, pink, chalky or ashen. A right "
                   "panel in which she looks fair-skinned is a failure, not a success."),
        negatives=_F1["negatives"].replace(_MOLE_NEG, "") + CLOTHES_NEG_F1,
    ),
    "f2-crowsfeet": dict(
        _F2,
        nothing_else=("NOTHING OUTSIDE THE EYE CORNER HAS CHANGED, AND HER SKIN IS EXACTLY THE SAME COLOUR AND "
                      "BRIGHTNESS IN BOTH PANELS. Her forehead, her brows, her eyelids, the skin and the soft "
                      "fullness under her eyes, the lines beside her nose and mouth, her cheeks and her jaw look "
                      "exactly the same in both panels, and her skin is the same shade, not brighter, paler or "
                      "clearer, in the right one - just as the whites of her eyes, her hair and her lips are "
                      "unchanged; only the lines at the outer corner of her eye are different."),
        luma_nothing_else=("Nothing outside the eye corner has changed, and her skin is exactly the same colour and "
                           "brightness in both panels, as are the whites of her eyes, her hair and her lips; only "
                           "the eye-corner lines differ."),
        age=("SHE IS IN HER LATE THIRTIES TO MID-FORTIES, AND THAT GOVERNS WHAT HER SKIN CAN HONESTLY LOOK LIKE. "
             "The lines at the corners of her eyes are fine but established - they stay with her face at rest, "
             "from years of everyday expressions - and the skin there is thin and finely crinkled. She is "
             "NOT old: no deep folds, no hooded drooping lids, no heavy bags; and not young either - clearly not "
             "in her twenties."),
        negatives=(_F2["negatives"] + ", no paler face in the right panel, no brighter exposure in the right "
                   "panel, no washed-out right panel" + CLOTHES_NEG_F2),
    ),
}

# --------------------------------------------------------------------------------------
# Change 2 (and 4): exact-string swaps into the round-3 skeleton for r2. Each must match exactly once.
# --------------------------------------------------------------------------------------
R3_ONE = ("ONE. EVERY MOLE, FRECKLE AND DISTINCT MARK SHE HAS IS STILL THERE IN THE RIGHT PANEL, in the same "
          "place, the same size and the same number. Her identity is anchored to those marks and they do not "
          "fade, move or vanish.")
ONE_R2 = ("ONE. SHE IS RECOGNISABLY THE SAME WOMAN BY THE SHAPE OF HER FACE: the same face shape, the same "
          "nose, the same brows, the same hairline, the same ears and the same hair colour in the right panel. "
          "Her skin is clear on both days - nothing on its surface but pores, fine hairs and fine lines - and "
          "that is exactly as true in the right panel as in the left.")
R3_LOCK = ("UNMISTAKABLY THE SAME WOMAN: the same face shape, the same nose, the same eye shape and eyelids, the "
           "same eye colour, the same skin colour, the same brow shape, the same hair colour and cut, and her "
           "moles and marks in the same places on her skin.")


def lock_r2(tone: bool) -> str:
    skin = "the same skin type and undertone" if tone else "the same skin colour"
    return ("UNMISTAKABLY THE SAME WOMAN, AND WHAT HOLDS HER IDENTITY IS THE SHAPE OF HER FACE: the same face "
            f"shape, the same nose, the same eye shape and eyelids, the same eye colour, {skin}, the same brow "
            "shape, the same hairline, the same ears, and the same hair colour and cut.")


R3_P19 = "Every mole and mark is still there in the same place, and the light is no kinder than in the left panel."


def p19_r2(tone: bool) -> str:
    match = ("exposure and colour balance" if tone else
             "exposure, white balance and skin brightness - the whites of her eyes, her hair and her lips are "
             "unchanged")
    return ("Her face shape, nose, brows, hairline, ears and hair colour are the same, and the light is no "
            f"kinder than in the left panel: the two panels match each other exactly for {match}.")


SIDE_MARKS = "the same side, with the same marks on it, on both days"
SIDE_MARKS_R2 = "the same side on both days"
NOT_MIRRORED_R2 = ("The two panels are NEVER mirror images of each other: her hair is parted on the same side, "
                   "and the ear and cheek nearest the camera are the same ones, in both")
R3_TWO = ("TWO. SHE IS THE SAME PERSON, THE SAME AGE AND THE SAME COMPLEXION IN BOTH PANELS. She has not been made "
          "younger, slimmer, prettier, better groomed or lighter-skinned, and she wears no makeup on either day.")
TWO_TONE_R2 = ("TWO. SHE IS THE SAME PERSON, THE SAME AGE AND PLAINLY THE SAME SKIN TONE IN BOTH PANELS - the "
               "same light-olive complexion with a light tan and the same warm golden undertone. She has not been "
               "made younger, slimmer, prettier or better groomed, she has not become a paler or fairer person, "
               "and she wears no makeup on either day.")
R3_FOUR = ("FOUR. THE RIGHT PANEL IS NOT LIT MORE KINDLY. It is not brighter, softer, warmer or more frontally lit "
           "than the left: in both, daylight grazes down across her from high on one side, equally strongly. If "
           "the right panel were lit more kindly, the improvement would just be the light.")
FOUR_TONE = SWAPS_TONE[4][1]
assert SWAPS_TONE[4][0] == R3_FOUR and SWAPS_TONE[3][0] == R3_TWO, "r1 tone swap order changed"
# Change 4: f2's brightness stated as a matching requirement, with the proof named, as f1's is.
FOUR_CF_R2 = ("FOUR. THE RIGHT PANEL IS NOT LIT MORE KINDLY, AND THE TWO PANELS MATCH EACH OTHER FOR EXPOSURE, "
              "WHITE BALANCE AND SKIN BRIGHTNESS. In both, daylight grazes down across her from high on the side "
              "of her face nearest the camera, equally strongly, and neither panel is brighter, paler, warmer, "
              "cooler or more washed-out than the other. THE PROOF IS IN WHAT DOES NOT CHANGE: the whites of her "
              "eyes, her hair and the colour of her lips look exactly the same in both panels, and so do the "
              "colour and brightness of her skin. Only the lines at the outer corner of her eye differ. If the "
              "right panel were lit, exposed or tinted differently, the difference would just be the camera.")
# r1's tone light names "the black of her hair" (Filipino casting); r2's women are brown, chestnut or black.
assert LIGHT_TONE.count("the black of her hair") == 1, "r1 LIGHT_TONE changed"
LIGHT_TONE_R2 = LIGHT_TONE.replace("the black of her hair", "the colour of her hair")
LIGHT_WRINKLE_R2 = LIGHT_WRINKLE + (
    "\n\n⚠️ AND THE TWO PICTURES ARE EXPOSED THE SAME, WITH THE SAME WHITE BALANCE. Her skin is exactly as bright "
    "and exactly the same colour in both panels - the right-hand picture is not lighter, paler, warmer or cooler "
    "than the left-hand one. THE PROOF IS IN WHAT DOES NOT CHANGE: the whites of her eyes, her hair, her brows "
    "and the colour of her lips look exactly the same in both panels. Only the lines at the corner of her eye "
    "are different.")
SKIN_R2 = (
    "THE SKIN MUST HOLD UP AS REAL AND UNFLATTERED, and at this crop it is most of the picture. Pores are "
    "clearly visible and vary in size by zone - open across the nose and inner cheek, finer at the temple - "
    "several larger than their neighbours. Fine vellus hairs catch the light along the cheek and jaw, and fine "
    "lines sit where her age puts them. The skin is a little greasy at the nose and forehead and drier at the "
    "outer cheek. HER SKIN IS CLEAR AND EVEN: one smooth, uniform colour across her cheeks and her whole face, "
    "with nothing on its surface but pores, fine hairs and fine lines. " + (
        # Smoke fault 1 (r2, slot a): see R2_SMOKE_LOG. Said without naming what it excludes.
        "THE COLOUR IS UNBROKEN ACROSS HER CHEEKS, HER NOSE AND HER FOREHEAD: each pore is a tiny pit the same "
        "colour as the skin around it, and nothing darker sits on the skin between them. ") +
    "That texture is what makes it real - a smooth, poreless face reads as a filter. Real skin, photographed "
    "honestly, with no smoothing of any kind."
)
#: Luma's forms of the smoke-1 and smoke-2 fixes (Luma receives no negatives at all).
LUMA_SKIN_R2 = ("Real skin: visible pores, vellus hair and fine lines, nothing else on it; one clear colour, "
                "unbroken across her cheeks and nose, each pore the same colour as the skin around it. No "
                "smoothing.")


def swaps_r2(w: dict, tone: bool, garments: dict = None) -> list:
    common = [(R3_AMATEUR, AMATEUR_NEUTRAL), (R3_P9, p9_r2(w["key"], garments)), (R3_ONE, ONE_R2),
              (R3_LOCK, lock_r2(tone)), (R3_P19, p19_r2(tone)), (SIDE_MARKS, SIDE_MARKS_R2),
              (r3.NOT_MIRRORED, NOT_MIRRORED_R2)]
    return common + ([(R3_TWO, TWO_TONE_R2), (R3_FOUR, FOUR_TONE)] if tone else [(R3_FOUR, FOUR_CF_R2)])


R3_LUMA_RIGHT = ("THE RIGHT PANEL, FIRST OF ALL: every mole and mark still there in the same place; the same "
                 "person, same age, same complexion, no makeup. ")
R3_LUMA_LOCK = "Same face, nose, eye shape and eyelids, eye colour, skin colour, brows, hair colour and cut."
R3_LUMA_KIND = "It is not lit more kindly - not brighter, softer or more frontal than the left. "


#: Luma's short form of NOT_MIRRORED_R2 (its 6,000-character cap; LUMA_CAP holds 5,700).
NOT_MIRRORED_LUMA_R2 = "Never mirror images: her parting and the near ear and cheek are the same in both"


def luma_swaps_r2(w: dict, tone: bool, blocks: dict = None, garments: dict = None) -> list:
    b = (blocks or BLOCKS_R2)[w["block"]]
    # The identity anchors live in the lock line two sentences on; f1's complexion is in luma_honesty.
    right = ("THE RIGHT PANEL, FIRST OF ALL: the same person, same age, "
             + ("" if tone else "same complexion, ") + "no makeup. ")
    lock = ("Same face shape, nose, eyes and eyelids, "
            + ("skin type and undertone" if tone else "skin colour")
            + ", brows, hairline, ears, hair colour and cut: her identity.")
    pairs = [LUMA_AMATEUR,
             ("Real skin: visible pores, vellus hair, uneven pigment. No smoothing.", LUMA_SKIN_R2),
             ("Hair a little different.", luma_dressed_r2(w["key"], garments)),
             LUMA_EDGES,
             (R3_LUMA_RIGHT, right), (R3_LUMA_LOCK, lock),
             (SIDE_MARKS, SIDE_MARKS_R2), (r3.NOT_MIRRORED, NOT_MIRRORED_LUMA_R2)]
    if tone:
        pairs += [(R3_LUMA_KIND, LUMA_SWAPS_TONE[-2][1]), LUMA_SWAPS_TONE[-1]]
        assert LUMA_SWAPS_TONE[-2][0] == R3_LUMA_KIND, "r1 luma tone swap order changed"
    else:
        pairs += [(R3_LUMA_KIND, "It is not lit more kindly, and the two panels match for exposure, white balance "
                                 "and skin brightness - the whites of her eyes, her hair and her lips look the same; "
                                 "only the eye-corner lines differ. ")]
    return pairs + [(b["expression"], b["luma_expression"]), (b["nothing_else"], b["luma_nothing_else"])]


NEGATIVE_GLOBAL_R2 = (r3.NEGATIVE_GLOBAL.replace("no non-white model, ", "") +
                      ", no mole, no moles, no wart, no warts, no skin tag, no beauty mark, no beauty spot, no raised "
                      "spot, no raised bump on the skin, no very pale skin, no pink-toned fair skin, no freckles, "
                      "no logo on clothing, no print on clothing, no writing on clothing, no graphic T-shirt, no "
                      "bare shoulders")
_PAIR_MOLE = "no moles disappearing between the panels, "


def negative_pair_r2(kind: str) -> str:
    neg = negative_pair(kind)
    assert neg.count(_PAIR_MOLE) == 1, "round-3 pair negative changed"
    return neg.replace(_PAIR_MOLE, "")


def build_r2(w: dict) -> tuple:
    b = BLOCKS_R2[w["block"]]
    tone = b["kind"] == "tone"
    r3.CROPS, r3.BLOCKS, r3.VIEWPOINTS, r3.GAZE, r3.WALLS = CROPS, BLOCKS_R2, VIEWPOINTS, GAZE, WALLS
    r3.LIGHT = LIGHT_TONE_R2 if tone else LIGHT_WRINKLE_R2
    r3.SKIN = SKIN_R2
    prompt = swap(r3.build_prompt(w), swaps_r2(w, tone), f"r2 {w['key']} prompt")
    luma = swap(r3.build_prompt_luma(w), luma_swaps_r2(w, tone), f"r2 {w['key']} luma")
    return prompt, luma


#: Anything an engine reads as a POSITIVE must not name a mark (describe-the-thing-dont-name-it).
MARK_WORDS = re.compile(r"\bmoles?\b|\bwarts?\b|skin tags?|beauty (?:marks?|spots?)|\bfreckl|\bmarks? on\b|"
                        r"distinct mark|same marks|moles and marks", re.I)
NATIONALITIES = ("ITALIAN", "GREEK", "SPANISH", "PORTUGUESE", "FRENCH", "CROATIAN")


def r2_config() -> dict:
    slots = []
    r1_ids = [f"{ID_PREFIX_R1}{w['block']}-{w['key']}" for w in WOMEN]
    for w in WOMEN_R2:
        b = BLOCKS_R2[w["block"]]
        tone = b["kind"] == "tone"
        prompt, prompt_luma = build_r2(w)
        negative_extra = negative_pair_r2(b["kind"]) + ", " + b["negatives"]
        both = prompt + prompt_luma
        k = w["key"]
        # --- round-1 guards, all still binding
        assert len(prompt_luma) < r3.LUMA_CAP, f"{k}: luma prompt {len(prompt_luma)} chars"
        assert not any(ch.isdigit() for ch in both), f"{k}: digit in prompt"
        bait = r3.caption_bait(both + NEGATIVE_GLOBAL_R2 + negative_extra)
        assert not bait, f"{k}: caption bait {bait}"
        assert "window" not in both.lower(), f"{k}: 'window' in prompt"
        assert "white balance is a little wrong" not in both and "slightly off" not in both, k
        assert "uneven pigment" not in both and "Pigment is uneven" not in both, k
        assert not re.search(r"\bsun", both, re.I), f"{k}: 'sun' in prompt"
        if tone:
            for gone in ("grazes down", "grazes DOWN", "lighter-skinned", "SAME COMPLEXION"):
                assert gone not in both, f"{k}: wrinkle-pair text survived in a tone brief: {gone!r}"
        # --- change 1: casting
        assert "FILIPINO" not in both.upper() and "medium, tan" not in both.lower(), f"{k}: r1 casting survived"
        assert "light-olive" in w["who"] and sum(n in w["who"] for n in NATIONALITIES) == 1, k
        assert "light-olive" in prompt and "light-olive" in prompt_luma, k
        # --- change 2: no marks named in any positive text; named in the negatives
        m = MARK_WORDS.search(both)
        assert not m, f"{k}: a mark is named in a positive: {m.group(0)!r}"
        for neg in ("no mole", "no wart", "no skin tag", "no beauty mark", "no raised spot"):
            assert neg in NEGATIVE_GLOBAL_R2, neg
        assert "moles disappearing" not in negative_extra and "mole disappearing" not in negative_extra, k
        assert "HAIRLINE, EARS" in prompt.upper() or "hairline, the same ears" in prompt, k
        # --- change 3: clothes
        left, right = GARMENTS_R2[k]
        assert left[0] in prompt and right[0] in prompt, f"{k}: garment missing from prompt"
        assert left[0] in prompt_luma and right[0] in prompt_luma, f"{k}: garment missing from luma"
        assert "grey one on one day and a navy one" not in both and "grey on one day and navy" not in both, k
        assert _garment_pair_ok(k, left, right), k
        if tone:
            assert right[2] >= left[2] and right[2] >= 2 and left[3] and right[3], f"{k}: f1 clothing unfair"
        else:
            assert right[2] >= 2, f"{k}: f2 right-panel top is white or near-white"
        # --- smoke fixes (R2_SMOKE_LOG): unbroken colour in both briefs; Luma's undertone clause on f1
        assert "COLOUR IS UNBROKEN" in prompt and "unbroken across her cheeks and nose" in prompt_luma, k
        if tone:
            assert "not pinker or greyer" in prompt_luma, k
        # --- change 4: f2's brightness match, with its proof
        if not tone:
            assert both.count("whites of her eyes") >= 4, f"{k}: f2 brightness match not stated"
        slots.append({
            "id": f"{ID_PREFIX_R2}{w['block']}-{k}",
            "title": (f"{b['block']} {w['block'].split('-', 1)[1]} · {b['study']} · {CROPS[w['crop']]['label']} — "
                      f"{re.sub(r'^an? ', '', w['who'].split(',')[0])}"),
            "class": "B", "width": r3.SIZE, "height": r3.SIZE,
            "target_slot": f"{b['page']} key_findings_ba {b['block']} ({b['heading']})",
            "generated_from": (f"r2 smoke brief - {SMOKE_BRIEF_R2} (not re-run)"
                               if k in SMOKE_SLOTS_R2 and SMOKE_BRIEF_R2 else "r2"),
            "garments": {"left": left[0], "right": right[0]},
            "ref_files": [], "prompt": prompt, "prompt_luma": prompt_luma,
            "label": {"left": "Before", "right": b["after_label"], "figure": "",
                      "measure": "(labels are theme settings, never pixels)", "cite": b["study"]},
            "negative_extra": negative_extra,
        })
    ids = [s["id"] for s in slots]
    # --- change 5: generate-multi's --only and the uploader both match by PREFIX.
    assert not any(a != c and c.startswith(a) for a in ids for c in ids), "an r2 slot id prefixes another"
    assert not any(a.startswith(c) or c.startswith(a) for a in ids for c in r1_ids), "r2 and r1 ids collide"
    garments = [g[0] for p in GARMENTS_R2.values() for g in p]
    assert len(set(garments)) == len(garments) == 12, "a garment is used twice"
    assert "no Caucasian model" not in NEGATIVE_GLOBAL_R2 and "non-white" not in NEGATIVE_GLOBAL_R2

    return {
        "wave": WAVE_R2, "created": "2026-09-29", "round": "r2",
        "doc": ("docs/claims/glutathione.md §8.5 (source of truth), docs/clinical-trial-before-after-images.md, "
                ".claude/rules/website-imagery.md; built by scripts/build-glutathione-cards-before-after-config.py "
                "(round 2) on the round-3 brief machinery, f2 from the copper crow's-feet block"),
        "note": ("GLUTATHIONE SCIENCE PAGE, FINDINGS CARDS f1 AND f2, ROUND 2 (Watanabe 2014: 2% GSSG lotion, "
                 "split-face, 10 weeks). f1 tone (slots a-c): a MODEST, even brightening of the cheekbone - no "
                 "change in evenness, spots, redness, pores, texture or lines; tone-pair light (soft, broad, "
                 "frontal; exposure and white balance matched). f2 crow's feet (slots d-f): the same lines a little "
                 "shallower and softer, never erased; exposure, white balance and skin brightness MATCHED between "
                 "the panels. MALCOLM, 2026-09-29: 'the befoe and after images for the Glutathione trials need to "
                 "be made again. this time with caucasian women - and the clothes should be random. now they are "
                 "the same tshirt and same colors. these need to vary. also lets not use women with warts - as very "
                 "few women have them - and we use them in nearly all images.' So: Caucasian women with "
                 "light-olive, Mediterranean-type skin (the trials did not cover fair skin), late 30s to mid-40s; "
                 "no moles, warts, skin tags or beauty marks (identity held by face shape, nose, brows, hairline, "
                 "ears, hair colour); two different garments per slot, none repeated (f1: right-panel top never "
                 "lighter and never white, muted colours; f2: right-panel top never white). CANDIDATES ONLY; "
                 "Malcolm picks with _ / __. Smoke test: slot a on all six suppliers first."),
        "target_templates": [TEMPLATE],
        "labels_are_composited": "NOT composited. Labels are text settings on the theme section.",
        "defaults": {"candidates": 1, "negative_global": NEGATIVE_GLOBAL_R2, "negative_class_b": ""},
        "slots": slots,
    }


# ======================================================================================
# ROUND 3 (2026-09-29): card f3, Wahab 2021. Everything below is new; above it, only the r2 helpers gained
# optional parameters and TONE_KEYS (see the ROUND 3 section of the docstring). Names end in _RD3 because
# `r3` / R3_* already mean the under-eye skeleton in this file.
# ======================================================================================
WAVE_RD3 = "before-after-glutathione-cards-r3"
OUT_RD3 = ROOT / "configs" / "banners" / f"{WAVE_RD3}.json"
ID_PREFIX_RD3 = "glub3--"
SLOT_KEYS_RD3 = ("g", "h", "i")
assert set(SLOT_KEYS_RD3) == F3_KEYS_RD3
#: r3 smoke-test slot: its candidates came from the brief in effect at smoke time (preserved beside them).
SMOKE_SLOTS_RD3 = {"g"}
SMOKE_BRIEF_RD3 = ("assets/ai-generated/2026-08-22-multi-before-after-glutathione-cards-r3/"
                   "smoke-brief-r3-g.json")
RD3_SMOKE_LOG = """
SMOKE LOG, 2026-09-29 (slot g, f3 tone; gpt_image resolved to gpt-image-2.5-sunburst). First pass 4 of 6:
nbp_flash HTTP 503 Service Unavailable and flux2 fal "downstream_service_unavailable" - provider outages,
not refusals; both returned on an immediate retry of those two suppliers on the SAME brief, so 6 of 6.
Manifests: manifest-smoke-g.json, manifest-smoke-g-retry.json. Judged at 100% (each panel at full
resolution) and at render size (500 px). Slot g is NOT re-run; its brief is at SMOKE_BRIEF_RD3.
  HELD: no text on any tile; no mole, wart, skin tag or beauty mark on any; the briefed garments (cream
  cable-knit, then charcoal T-shirt) on five of six, the right-panel top darker on every dressed tile; plain
  walls. SIZE OF THE CHANGE, as centre-panel skin L* (left -> right): gpt_image +7.0, nbp_flash +4.3, nbp_pro
  +9.8, seedream +11.2, luma +14.9 - round 2's band (Malcolm's card-1 pick, r2 A5 nbp_pro, is +8.8), except
  luma, which overshoots as it did in r2 (B3 +15).
  THREE BRIEF FAULTS, FIXED FOR SLOTS h-i:
    1. SHE CAME OUT OLDER THAN EARLY-TO-MID THIRTIES on five of six (about forty on gpt_image, nbp_pro and
       luma; fifty-ish on seedream's left panel; only nbp_flash looked thirty-ish). The age paragraph said
       "early to mid thirties" but nothing an engine could check, and round 2's nothing_else kept "the fine
       lines ... beside her mouth", a forties sign. AGE_RD3 now gives checkable signs (a full, youthful face,
       smooth forehead, no lines between the brows or from nose to mouth; "anyone would put her at thirty to
       thirty-five, never forty"), NOTHING_ELSE_RD3 drops the mouth lines, and Luma (which has no age
       paragraph) gets a one-line form.
    2. SEEDREAM CAST TWO DIFFERENT, EAST-ASIAN-LOOKING WOMEN for "a MALTESE woman" (identity and casting both
       broken). Unlike round 2's Italian or Greek, Maltese, Cypriot and Albanian carry no look an engine
       knows; every `who` line now adds "Southern European in her looks".
    3. LUMA'S RIGHT PANEL WAS FLECKED ALL OVER (forehead, nose, cheeks) - round 2's smoke fault 1 back on
       Luma despite LUMA_SKIN_R2. Luma's skin line now ends "not one darker dot or fleck anywhere". To stay
       under LUMA_CAP, Luma's copy drops two sentences that repeat others in the same brief (the crop
       paragraph's wall-strip sentence; the amateur line's "the two panels match for colour balance").
  NOT BRIEF FAULTS (known supplier traits, recorded, not changed): nbp_pro and luma framed the pair with a
  white border; nbp_pro held one side on both panels but the wrong one (nose to the right); luma's left
  panel has an orange, patchy cast (a white-balance difference between the panels) and overshoots; flux2
  mirrored the pair, freckled her and left her undressed; gpt_image carries faint brown flecks on the nose
  and cheek, equal in both panels; nbp_flash straightened her curls in the right panel.
"""

# --- change 4: clothes. The garments round 2 did not use, plus new muted, open-necked ones. -------------
_USED_R2 = {g[0] for pair in GARMENTS_R2.values() for g in pair}
GARMENT_EXTRA_RD3 = [
    # phrase                                                  type          depth muted  open   family
    ("a plum-coloured fine-knit cardigan over a plain top",   "cardigan",     4, True,  True,  "purple"),
    ("a stone-coloured linen shirt, open at the neck",        "shirt",        2, True,  True,  "neutral"),
    ("a khaki crew-neck T-shirt",                             "tee",          3, True,  True,  "green"),
    ("a deep-navy scoop-neck long-sleeved top",               "top",          5, True,  True,  "navy"),
    ("a mid-grey marl V-neck jumper",                         "jumper",       3, True,  True,  "grey"),
    ("a petrol-blue boat-neck jumper",                        "jumper",       4, True,  True,  "teal"),
    ("a dusky-mauve crew-neck sweatshirt",                    "sweatshirt",   3, True,  True,  "purple"),
    ("a dark-brown corduroy shirt, open at the neck",         "shirt",        4, True,  True,  "brown"),
]
# No polo shirt: the f1 negatives kept for f3 say "no polo neck", and a garment the negatives appear to ban
# is a fight the engine resolves its own way (the first r3 draw put a slate-blue polo shirt on slot i).
GARMENT_POOL_RD3 = [g for g in GARMENT_POOL if g[0] not in _USED_R2 and g[1] != "polo"] + GARMENT_EXTRA_RD3
assert not {g[0] for g in GARMENT_POOL_RD3} & _USED_R2, "a round-2 garment is back in the round-3 pool"
GARMENT_SEED_RD3 = 2026092903


def pick_garments_rd3() -> dict:
    """As pick_garments(), for f3's three tone slots, from the round-3 pool."""
    rng = random.Random(GARMENT_SEED_RD3)
    for _ in range(100000):
        pool = list(GARMENT_POOL_RD3)
        rng.shuffle(pool)
        pairs = {k: (pool[2 * i], pool[2 * i + 1]) for i, k in enumerate(SLOT_KEYS_RD3)}
        if all(_garment_pair_ok(k, *p) for k, p in pairs.items()):
            return pairs
    raise AssertionError("no round-3 garment draw satisfies the fairness rules")


GARMENTS_RD3 = pick_garments_rd3()

# --- change 5: walls (left white-ish, right pale grey) and viewpoints (right turned a touch less). -------
WALLS_RD3 = [
    ("a plain BRIGHT WHITE painted wall", f"in front of her, softly, leaning a little towards {NEAR}"),  # 0 g-L
    ("a plain PALE ASH-GREY painted wall", "straight in front of her and a little above, softly"),       # 1 g-R
    ("a plain LINEN-WHITE painted wall", "straight in front of her and a little above, softly"),         # 2 h-L
    ("a plain PALE PEBBLE-GREY painted wall", f"in front of her, softly, leaning a little towards {FAR}"),  # 3 h-R
    ("a plain CLEAN WHITE painted wall", f"in front of her, softly, leaning a little towards {NEAR}"),   # 4 i-L
    ("a plain LIGHT SILVER-GREY painted wall", "straight in front of her and a little above, softly"),   # 5 i-R
]
VIEWPOINTS_RD3 = {
    "g": dict(side=L,
              a=dict(cam="held at her eye line, a hand's width off to the side",
                     turn="her face turned about thirty-five degrees towards the left-hand edge of the picture, level",
                     dist="framed very close", place="her near cheekbone sits centred"),
              b=dict(cam="held a little above her eye line and angled slightly down",
                     turn="her face turned about thirty degrees towards the left-hand edge of the picture, level",
                     dist="framed a touch less close, but still close",
                     place="her near cheekbone sits a little right of centre")),
    "h": dict(side=R,
              a=dict(cam="held a little above her eye line and angled slightly down",
                     turn="her face turned about forty degrees towards the right-hand edge of the picture, chin level",
                     dist="framed close", place="her face sits centred and a little high"),
              b=dict(cam="held at her eye line, a little further off to the side",
                     turn="her face turned about thirty-five degrees towards the right-hand edge of the picture, chin level",
                     dist="framed a touch closer", place="her face sits a little left of centre")),
    "i": dict(side=L,
              a=dict(cam="held at her cheekbone level, a hand's width from her face",
                     turn="her face turned about thirty-five degrees towards the left-hand edge of the picture, level",
                     dist="framed very close", place="the cheekbone sits centred"),
              b=dict(cam="held just above her cheekbone level and angled slightly down",
                     turn="her face turned about thirty degrees towards the left-hand edge of the picture, level",
                     dist="framed a touch closer still", place="the cheekbone sits a little low and right of centre")),
}
GAZE_RD3 = {
    "g": ("her eyes look just past the lens", "her eyes are on the lens"),
    "h": ("her eyes are on the lens", "her eyes look a little down and away from the lens"),
    "i": ("her eye looks straight ahead, past the lens", "her eye glances a little towards the lens"),
}

# --- change 2: age. The trial's volunteers averaged thirty (twenty to forty-four). -----------------------
# Smoke fault 1 (RD3_SMOKE_LOG): five of six engines aged her to forty-plus. The age is now stated with
# signs an engine can check in its own output, and round 2's "lines beside her mouth" (a forties sign) is
# dropped from what must stay the same (NOTHING_ELSE_RD3).
AGE_RD3 = ("SHE IS IN HER EARLY TO MID THIRTIES, AND SHE LOOKS IT - anyone would put her at thirty to "
           "thirty-five, never forty. Her face is youthful and full: firm cheeks, a firm jawline, a smooth "
           "forehead at rest, no lines between her brows and no lines running from her nose to the corners of "
           "her mouth. The only lines are the faintest fine creases at the outer corners of her eyes. Her skin "
           "is firm and healthy, the everyday skin of a woman who works indoors and out. She is NOT a girl or a "
           "woman in her early twenties, and NOT middle-aged: no deep lines, no sagging, no slackness.")
_MOUTH_LINES = "the fine lines at the corner of her eye and beside her mouth"
assert BLOCKS_R2["f1-tone"]["nothing_else"].count(_MOUTH_LINES) == 1, "r2 f1 nothing_else changed"
NOTHING_ELSE_RD3 = BLOCKS_R2["f1-tone"]["nothing_else"].replace(
    _MOUTH_LINES, "the faint fine creases at the corners of her eyes")
#: Luma has no age paragraph; its short form of the same signs.
LUMA_AGE_RD3 = ("An ordinary person, not a model.",
                "An ordinary person, not a model. Early thirties: a youthful face, no lines from nose to mouth.")
#: Smoke fault 3: Luma's right panel came back flecked all over (round 2's smoke fault 1, back on Luma).
LUMA_SKIN_RD3 = (LUMA_SKIN_R2, LUMA_SKIN_R2.replace(
    "the same colour as the skin around it.",
    "the same colour as the skin around it; not one darker dot or fleck anywhere."))
assert LUMA_SKIN_RD3[0] != LUMA_SKIN_RD3[1], "LUMA_SKIN_R2 changed"
#: Room for the three fixes under LUMA_CAP: in Luma's copy only, the crop paragraph's closing sentence about
#: the wall strip goes - Luma's paragraph 1c already says "only a narrow strip of plain painted wall at one edge".
LUMA_CROP_CUTS_RD3 = (" The plain wall shows only as a narrow strip beside the back of her head.",
                      " The plain wall shows only as a narrow strip beside her head.")
#: ...and the amateur line's closing clause, which repeats the match already stated in Luma's right-panel rules.
_LUMA_MATCH_TAIL = ", and the two panels match for colour balance."
assert LUMA_AMATEUR[1].count(_LUMA_MATCH_TAIL) == 1, "LUMA_AMATEUR changed"
LUMA_AMATEUR_RD3 = (LUMA_AMATEUR[1], LUMA_AMATEUR[1].replace(_LUMA_MATCH_TAIL, "."))
_AGE_NEG_R2 = "no woman under thirty, no woman over fifty, no elderly woman"
assert BLOCKS_R2["f1-tone"]["negatives"].count(_AGE_NEG_R2) == 1, "r2 f1 age negatives changed"
AGE_NEG_RD3 = ("no teenager, no girl, no woman in her early twenties, no woman over forty, no middle-aged woman, "
               "no elderly woman")

# --- change 1: the card. Round 2's f1 block with the card, study, label and age replaced. ----------------
BLOCKS_RD3 = {
    "f3-tone": dict(
        BLOCKS_R2["f1-tone"],
        block="f3", heading="Independent Trial: a Glutathione and Vitamin C Serum Lowered Skin Pigment 10.8%",
        study="wahab-2021", after_label="After 8 weeks",
        age=AGE_RD3, nothing_else=NOTHING_ELSE_RD3,
        negatives=BLOCKS_R2["f1-tone"]["negatives"].replace(_AGE_NEG_R2, AGE_NEG_RD3),
    ),
}

# --- change 3: the three women. `before` is round 2's line for the same crop. -----------------------------
# Smoke fault 2 (RD3_SMOKE_LOG): seedream cast two different East-Asian-looking women for "MALTESE". Unlike
# "Italian", these nationalities carry no look an engine knows, so each line names the look as well.
_R2_BEFORE = {w["crop"]: w["before"] for w in WOMEN_R2 if w["block"] == "f1-tone"}
WOMEN_RD3 = [
    dict(block="f3-tone", key="g", crop="tone_three_quarter", walls=(0, 1),
         who=("a MALTESE woman of about thirty-three, Southern European in her looks, with near-black hair in "
              "loose natural curls, pushed back off her face, light-olive skin with a warm golden undertone and "
              "a light, even tan, dark brown eyes and full natural dark brows")),
    dict(block="f3-tone", key="h", crop="tone_face", walls=(2, 3),
         who=("a CYPRIOT woman of about thirty-five, Southern European in her looks, with long, straight, dark "
              "chestnut hair pulled up into a high ponytail, light-olive skin with a warm golden undertone and a "
              "light, even tan, hazel-green eyes and straight natural brows")),
    dict(block="f3-tone", key="i", crop="tone_cheek", walls=(4, 5),
         who=("an ALBANIAN woman of about thirty-one, Southern European in her looks, with a short mid-brown "
              "pixie cut swept to one side, off her face, light-olive skin with a warm golden undertone and a "
              "light, even tan, light brown eyes and soft natural brows")),
]
for _w in WOMEN_RD3:
    _w["before"] = _R2_BEFORE[_w["crop"]]
NATIONALITIES_RD3 = ("MALTESE", "CYPRIOT", "ALBANIAN")


def build_rd3(w: dict) -> tuple:
    r3.CROPS, r3.BLOCKS, r3.VIEWPOINTS, r3.GAZE, r3.WALLS = CROPS, BLOCKS_RD3, VIEWPOINTS_RD3, GAZE_RD3, WALLS_RD3
    r3.LIGHT = LIGHT_TONE_R2
    r3.SKIN = SKIN_R2
    prompt = swap(r3.build_prompt(w), swaps_r2(w, True, GARMENTS_RD3), f"r3 {w['key']} prompt")
    crop_cut = [(s, "") for s in LUMA_CROP_CUTS_RD3 if s in CROPS[w["crop"]]["text"]]
    luma = swap(r3.build_prompt_luma(w), luma_swaps_r2(w, True, BLOCKS_RD3, GARMENTS_RD3) +
                [LUMA_AGE_RD3, LUMA_SKIN_RD3, LUMA_AMATEUR_RD3] + crop_cut, f"r3 {w['key']} luma")
    return prompt, luma


def rd3_config() -> dict:
    slots = []
    earlier_ids = ([f"{ID_PREFIX_R1}{w['block']}-{w['key']}" for w in WOMEN] +
                   [f"{ID_PREFIX_R2}{w['block']}-{w['key']}" for w in WOMEN_R2])
    for w in WOMEN_RD3:
        b = BLOCKS_RD3[w["block"]]
        prompt, prompt_luma = build_rd3(w)
        negative_extra = negative_pair_r2("tone") + ", " + b["negatives"]
        both = prompt + prompt_luma
        k = w["key"]
        # --- every round-1 and round-2 guard still binds
        assert len(prompt_luma) < r3.LUMA_CAP, f"{k}: luma prompt {len(prompt_luma)} chars"
        assert not any(ch.isdigit() for ch in both), f"{k}: digit in prompt"
        bait = r3.caption_bait(both + NEGATIVE_GLOBAL_R2 + negative_extra)
        assert not bait, f"{k}: caption bait {bait}"
        assert "window" not in both.lower(), f"{k}: 'window' in prompt"
        assert "white balance is a little wrong" not in both and "slightly off" not in both, k
        assert "uneven pigment" not in both and "Pigment is uneven" not in both, k
        assert not re.search(r"\bsun", both, re.I), f"{k}: 'sun' in prompt"
        for gone in ("grazes down", "grazes DOWN", "lighter-skinned", "SAME COMPLEXION"):
            assert gone not in both, f"{k}: wrinkle-pair text survived in a tone brief: {gone!r}"
        assert "FILIPINO" not in both.upper() and "medium, tan" not in both.lower(), f"{k}: r1 casting survived"
        assert "light-olive" in w["who"] and "light-olive" in prompt and "light-olive" in prompt_luma, k
        m = MARK_WORDS.search(both)
        assert not m, f"{k}: a mark is named in a positive: {m.group(0)!r}"
        assert "moles disappearing" not in negative_extra and "mole disappearing" not in negative_extra, k
        assert "hairline, the same ears" in prompt, k
        assert "COLOUR IS UNBROKEN" in prompt and "unbroken across her cheeks and nose" in prompt_luma, k
        assert "not pinker or greyer" in prompt_luma, k
        # --- round 3: casting (new nationalities), age, clothes, card
        assert sum(n in w["who"] for n in NATIONALITIES_RD3) == 1, f"{k}: nationality"
        assert not any(n in w["who"].upper() for n in NATIONALITIES), f"{k}: a round-2 nationality is repeated"
        assert "EARLY TO MID THIRTIES" in prompt and "MID-FORTIES" not in prompt, f"{k}: age"
        # --- r3 smoke fixes (RD3_SMOKE_LOG)
        assert "beside her mouth" not in prompt and "no lines from nose to mouth" in prompt_luma, f"{k}: age signs"
        assert "Southern European" in prompt and "Southern European" in prompt_luma, f"{k}: casting anchor"
        assert "not one darker dot or fleck anywhere" in prompt_luma, f"{k}: luma fleck line"
        assert "The two panels match exactly for light, exposure and white balance" in prompt_luma, k
        assert "no woman under thirty" not in negative_extra and "no woman over forty" in negative_extra, k
        left, right = GARMENTS_RD3[k]
        assert left[0] in prompt and right[0] in prompt, f"{k}: garment missing from prompt"
        assert left[0] in prompt_luma and right[0] in prompt_luma, f"{k}: garment missing from luma"
        assert _garment_pair_ok(k, left, right), k
        assert right[2] >= left[2] and right[2] >= 2 and left[3] and right[3] and left[4] and right[4], \
            f"{k}: f3 clothing unfair"
        assert left[0] not in _USED_R2 and right[0] not in _USED_R2, f"{k}: a round-2 garment is repeated"
        slots.append({
            "id": f"{ID_PREFIX_RD3}{w['block']}-{k}",
            "title": (f"{b['block']} {w['block'].split('-', 1)[1]} · {b['study']} · {CROPS[w['crop']]['label']} — "
                      f"{re.sub(r'^an? ', '', w['who'].split(',')[0])}"),
            "class": "B", "width": r3.SIZE, "height": r3.SIZE,
            "target_slot": f"{b['page']} key_findings_ba {b['block']} ({b['heading']})",
            "generated_from": (f"r3 smoke brief - {SMOKE_BRIEF_RD3} (not re-run)"
                               if k in SMOKE_SLOTS_RD3 and SMOKE_BRIEF_RD3 else "r3"),
            "garments": {"left": left[0], "right": right[0]},
            "ref_files": [], "prompt": prompt, "prompt_luma": prompt_luma,
            "label": {"left": "Before", "right": b["after_label"], "figure": "",
                      "measure": "(labels are theme settings, never pixels)", "cite": b["study"]},
            "negative_extra": negative_extra,
        })
    ids = [s["id"] for s in slots]
    assert not any(a != c and c.startswith(a) for a in ids for c in ids), "an r3 slot id prefixes another"
    assert not any(a.startswith(c) or c.startswith(a) for a in ids for c in earlier_ids), "r3 ids collide"
    garments = [g[0] for p in GARMENTS_RD3.values() for g in p]
    assert len(set(garments)) == len(garments) == 6, "a garment is used twice"
    assert all(s["label"]["right"] == "After 8 weeks" for s in slots)

    return {
        "wave": WAVE_RD3, "created": "2026-09-29", "round": "r3",
        "doc": ("docs/claims/glutathione.md §8.1 (Wahab 2021) and §8.5 (the f1 tone-pair rules, applied to f3), "
                "docs/clinical-trial-before-after-images.md, .claude/rules/website-imagery.md; built by "
                "scripts/build-glutathione-cards-before-after-config.py (round 3) on round 2's tone-pair machinery"),
        "note": ("GLUTATHIONE SCIENCE PAGE, FINDINGS CARD f3, ROUND 3 (Wahab et al. 2021, the independent trial: a "
                 "serum with 2% glutathione and vitamin C on one cheek and a placebo serum on the other, twice a "
                 "day for 8 weeks, SPF each morning; melanin index -10.8% on the serum side against +1.8% on "
                 "placebo, lightness improved). Slots g-i: a MODEST, even brightening of the cheekbone - plainly "
                 "the same woman and skin tone, never lighter than the skin under her jaw; no change in evenness, "
                 "spots, redness, pores, texture or lines; tone-pair light (soft, broad, frontal; exposure and "
                 "white balance matched). MALCOLM, 2026-09-29: 'New wave, all suppliers'. Casting as round 2 "
                 "(Caucasian, light-olive Mediterranean-type skin with a light tan) but early-to-mid thirties, as "
                 "the trial's volunteers averaged 30; new women (Maltese, Cypriot, Albanian); no moles, warts, "
                 "skin tags or beauty marks; two different garments per slot, none from round 2 (right-panel top "
                 "never lighter, never white, muted, open at the neck). Label: 'After 8 weeks' (theme setting). "
                 "CANDIDATES ONLY; Malcolm picks. Smoke test: slot g on all six suppliers first."),
        "target_templates": [TEMPLATE],
        "labels_are_composited": "NOT composited. Labels are text settings on the theme section.",
        "defaults": {"candidates": 1, "negative_global": NEGATIVE_GLOBAL_R2, "negative_class_b": ""},
        "slots": slots,
    }


PRETTIER = ROOT / "node_modules" / ".bin" / "prettier"


def render(cfg: dict, path: Path) -> tuple:
    """json.dumps, then the repo's own Prettier (what the pre-commit hook applies). (text, prettified?)"""
    text = json.dumps(cfg, indent=2, ensure_ascii=False) + "\n"
    if PRETTIER.exists() and shutil.which("node"):
        res = subprocess.run([str(PRETTIER), "--stdin-filepath", str(path)], input=text, capture_output=True,
                             text=True, cwd=ROOT)
        if res.returncode == 0:
            return res.stdout, True
    return text, False


def check_r1() -> None:
    """Round 1 must still come out of this file exactly as committed. Writes nothing."""
    text, pretty = render(r1_config(), OUT)
    committed = OUT.read_text()
    if pretty:
        assert text == committed, f"{OUT.name} is no longer reproduced byte for byte - an r2 edit leaked into r1"
        print(f"r1 check: {OUT.relative_to(ROOT)} reproduced byte for byte (after Prettier)")
    else:
        assert json.loads(text) == json.loads(committed), f"{OUT.name} is no longer reproduced"
        print(f"r1 check: {OUT.relative_to(ROOT)} reproduced as parsed JSON (Prettier unavailable, bytes unchecked)")


def check_r2() -> None:
    """Round 2 must still come out of this file exactly as committed (31e99c2). Writes nothing."""
    text, pretty = render(r2_config(), OUT_R2)
    committed = OUT_R2.read_text()
    if pretty:
        assert text == committed, f"{OUT_R2.name} is no longer reproduced byte for byte - an r3 edit leaked into r2"
        print(f"r2 check: {OUT_R2.relative_to(ROOT)} reproduced byte for byte (after Prettier)")
    else:
        assert json.loads(text) == json.loads(committed), f"{OUT_R2.name} is no longer reproduced"
        print(f"r2 check: {OUT_R2.relative_to(ROOT)} reproduced as parsed JSON (Prettier unavailable, bytes unchecked)")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--round", choices=("r1", "r2", "r3"), default="r3",
                    help="r3 (default) writes the round-3 config; r1 and r2 only prove the committed rounds")
    args = ap.parse_args()
    check_r1()
    if args.round == "r1":
        return
    check_r2()
    if args.round == "r2":
        return
    cfg = rd3_config()
    text, _ = render(cfg, OUT_RD3)
    OUT_RD3.write_text(text)
    print(f"wrote {OUT_RD3.relative_to(ROOT)} — {len(cfg['slots'])} slots")
    for s in cfg["slots"]:
        print(f"  {s['id']:<24} prompt {len(s['prompt']):>5}  luma {len(s['prompt_luma']):>5}   "
              f"L: {s['garments']['left']}  |  R: {s['garments']['right']}")


if __name__ == "__main__":
    main()
