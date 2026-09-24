#!/usr/bin/env python3
"""Build the before/after wave for two science-page cards: PDRN under-eye and Argireline forehead.

    python3 scripts/build-under-eye-forehead-before-after-config.py
    → configs/banners/before-after-undereye-forehead-r3.json

    python3 scripts/generate-multi.py configs/banners/before-after-undereye-forehead-r3.json \
        --candidates 1 --only <slot-id>[,<slot-id>]

ROUND 3 IS WHAT THIS FILE NOW BUILDS. Malcolm, 2026-09-24: "Lets make a new batch - using caucasian
women - and lets keep the face close up so not much background is shown - and lets keep the
background a plain wall with no extra details". Earlier rounds are records, not live code:
  r1 (smoke)  configs/banners/before-after-undereye-forehead-r1-smoke.json
  r2          configs/banners/before-after-undereye-forehead.json - built by this file at commit
              4bff479 (`git show 4bff479:scripts/build-under-eye-forehead-before-after-config.py`)
What r3 changes against r2, and why:
  1. CASTING: Caucasian women aged 40-55, six different women with different hair and colouring.
     This replaces the trial-population casting (points 4 and 6 below are the r1/r2 reasoning).
     A casting negative (`no non-white model`) is now safe, because nothing in the brief asks for
     anyone else.
  2. CLOSE-UPS ONLY. Every crop has the face filling the panel with a strip of wall at most. The
     under-eye slots all keep ONE side on show (split-face trial). r2's frontal both-eyes slot is
     gone, which also retires the open question it raised.
  3. A PLAIN WALL, NOTHING ELSE. ROOMS lost their "one soft element" and became WALLS: a flat
     colour plus the window direction, which still changes between the two days. KNOWN RISK
     (acetyl wave 15): a bare edge left nothing for the engine to place there and nbp_flash drew
     in a phone. The answer is the tight crop and an explicit sentence in paragraph 1 that nothing but
     her face, hair and the wall is in frame, plus a long negative list of room objects.
  4. NO CAPTION BAIT. In r2 nbp_pro burnt "WEEK 1 / WEEK 6", "WEEKS EARLIER / WEEKS LATER" and
     "EARLIER DAY / LATER DAY" into three slots - the brief's own words, turned into captions.
     r3 names the panels only as LEFT and RIGHT, never states a time gap in weeks, and states
     "no writing anywhere" as the second paragraph. main() asserts that no prompt, Luma prompt or
     negative list contains earlier / later / week / month / before / after.

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
WAVE = "before-after-undereye-forehead-r3"
OUT = ROOT / "configs" / "banners" / f"{WAVE}.json"
SIZE = 2048   # square: research-before-after takes the row height from the master, labels at 50%

# Luma answers anything over 6,000 characters with a bare HTTP 422 that reads like a content
# refusal. Held below the real cap on purpose, as in the glutathione builder, so a later edit to
# the shared text trips this assertion rather than silently losing the backend.
LUMA_CAP = 5700

# --------------------------------------------------------------------------------------
# SMOKE-TEST LOG (r1 -> r2), 2026-09-24.
# One slot per block - pdrn-undereye-b and argireline-forehead-d - ran across all six suppliers
# before the other four slots were paid for. 11 of 12 returned. The r1 brief is preserved exactly
# as run at configs/banners/before-after-undereye-forehead-r1-smoke.json; b and d are NOT re-run
# (re-running-a-slot-destroys-the-chosen-candidate), so their candidates stay r1 and the other four
# slots are r2. Five faults, four of them systematic:
#
#   1. THE CEILING DID NOT HOLD (gpt_image and nbp_pro on the under-eye, nbp_flash nearly; nbp_pro
#      on the forehead). "About a fifth less full" was read as "gone": the bags all but vanished,
#      and nbp_pro rejuvenated the whole face. r2 LEADS the right-panel paragraph with what STAYS,
#      gives the size as a ratio of what remains (four-fifths of the bulge; lines nine-tenths as
#      deep), and adds a single-panel test: look at the right panel alone and she still has bags /
#      still has forehead lines. A FIVE rule - nothing outside the region changes - is hoisted.
#   2. THE RIGHT PANEL WAS LIT MORE KINDLY (nbp_pro, nbp_flash, gpt_image): brighter, softer,
#      warmer, and on the under-eye the skin itself went lighter. The guard sat in paragraph 15 and
#      lost; it is now rule FOUR in paragraph 3 and restated at the point of change.
#   3. THE SIDE-LOCK BROKE IN TWO WAYS. gpt_image MIRRORED the face between panels (the cheek marks
#      jumped to the other cheek); nbp_pro held one side but the wrong one; flux2 on the forehead
#      made the two panels the LEFT AND RIGHT HALVES OF ONE FACE. The side is now stated in picture
#      terms (which edge of the panel her nose points to) instead of "her own left", every side
#      carries "never mirror images", and paragraph 1 says each panel is a complete photograph and
#      not half a face.
#   4. SEEDREAM DREW THE FAULT AS AN INJURY on both cards - a red, inflamed, bruise-like lower lid
#      that cleared in the right panel (a colour change the trial never measured), and a raw orange
#      CRACK across the forehead. Each block now carries a `feature` sentence stating the fault is
#      skin-coloured shape and shadow, never red, purple, a crack or a cut; "well cut" is gone from
#      slot f. Negatives name the injury forms.
#   5. LUMA REFUSED THE FOREHEAD BRIEF with `content_moderated` (read from the 422 body - NOT the
#      length cap; the brief was 5,029 characters, and the under-eye brief passed). Three free
#      probes - without "taut / frozen", then also with a neutral expression paragraph - were all
#      refused, so it is the subject, not one word. "Taut / frozen" are kept out of every Luma
#      text anyway; if e and f are refused too, Luma does not do this forehead brief.
#
# What held on r1 and is unchanged: no burnt-in text on any engine (nbp_pro included), no hand or
# phone, same woman across panels on five of six engines (flux2 the exception, as recorded), the
# forehead-band crop honoured by gpt_image and flux2. Every engine except flux2 pulled the
# under-eye crops back to a half-face or head-and-shoulders portrait - the known behaviour in
# engines-return-a-portrait-whatever-crop-you-ask-for; crop the winner in post.
# --------------------------------------------------------------------------------------
# (r2's own smoke slots were b and d, generated from the r1 brief.)

# --------------------------------------------------------------------------------------
# R3_SMOKE_LOG, 2026-09-24. Slots a (close three-quarter) and d (close forehead band) ran on all six
# suppliers first: 12 of 12 returned; OpenAI resolved to gpt-image-2.5-sunburst. The brief as run
# is preserved at configs/banners/before-after-undereye-forehead-r3-smoke.json; a and d are NOT
# re-run, so their candidates are the smoke brief and b, c, e, f are the revised one.
#
# HELD: no caption on any engine - nbp_pro included - so the caption-bait purge worked; Caucasian
# casting on all twelve; the side-lock on five of six (seedream mirrored slot a).
#
# TWO SYSTEMATIC FAULTS, FIXED:
#   1. WINDOWS AND A DOORFRAME APPEARED IN FOUR OF TWELVE TILES (nbp_pro a, luma a and d, nbp_flash
#      d). The brief said "the daylight comes from a WINDOW high on her left" and "the window itself
#      is never in the picture" - it named the object, and named objects get drawn (Luma sees no
#      negatives at all). The word "window" is now gone from everything an engine reads (asserted
#      in main()), the light is described only by where it falls from, and the list of forbidden
#      room objects left the positive text for the negative list.
#   2. NOT CLOSE ON THREE OF TWELVE (nbp_pro on both slots, nbp_flash d): head-and-shoulders with a
#      lot of wall. Paragraph 1c now carries a checkable geometry rule - her face spans nearly the
#      whole width of each panel, the top of her head is cut off, no shoulders in the picture -
#      rather than "close-up" alone (measure-geometry-dont-describe-it).
#
# NOT SYSTEMATIC, NOT CHANGED: seedream again drew the under-eye bag as a purple, bruise-like
# swelling and mirrored the face (it did the same in r2 - a fixed seedream trait on this subject);
# flux2 wore a headband despite `no headband` and an earring on slot a, and gave near-identical
# panels; nbp_pro framed slot d's panels as rounded cards with a white border; luma's slot d left
# panel reads as brows raised.
# --------------------------------------------------------------------------------------
ROUND = "r3"
#: r3 smoke-test slots - their candidates came from SMOKE_CONFIG, and the config says so per slot.
SMOKE_SLOTS = {"a", "d"}
SMOKE_CONFIG = "configs/banners/before-after-undereye-forehead-r3-smoke.json"

#: Words nbp_pro has turned into burnt-in captions (r2). None may appear in anything an engine reads.
CAPTION_BAIT = ("earlier", "later", "week", "weeks", "month", "months", "before", "after",
                "afterwards")

# --------------------------------------------------------------------------------------
# Walls. r3 (Malcolm): "a plain wall with no extra details". Twelve, so no two slots share one and
# the two days of every pair are different walls. Each is a flat colour plus where the daylight
# falls from. (The r3 smoke brief said "from a WINDOW high on her left" and four tiles drew the
# window - the light is now described without naming its source.) r1/r2's "one soft element" (doorframe, chair
# back, curtain...) is gone. It was there because on acetyl wave 15 a bare edge made nbp_flash draw
# a phone, so r3 relies on the close crop plus paragraph 1c instead. CHECK EVERY TILE FOR STRAY OBJECTS.
#
# EVERY WINDOW IS HIGH OR ABOVE. The features on both cards are horizontal, and only light arriving
# from above casts their shadows. The SIDE alternates within each pair, so the two days are plainly
# differently lit.
# --------------------------------------------------------------------------------------
WALLS = [
    ("a plain WARM WHITE painted wall", "high on her left"),
    ("a plain PALE GREY painted wall", "high on her right"),
    ("a plain SOFT BEIGE painted wall", "above her and to her right"),
    ("a plain MUTED SAGE-GREEN painted wall", "above her and to her left"),
    ("a plain SOFT TAUPE painted wall", "high on her left"),
    ("a plain PALE BLUE-GREY painted wall", "high on her right"),
    ("a plain OFF-WHITE painted wall", "above her and to her left"),
    ("a plain PALE OATMEAL painted wall", "above her and to her right"),
    ("a plain DUSTY PINK painted wall", "high on her right"),
    ("a plain CHALK WHITE painted wall", "high on her left"),
    ("a plain WARM IVORY painted wall", "above her and to her left"),
    ("a plain LIGHT STONE-GREY painted wall", "above her and to her right"),
]

# --------------------------------------------------------------------------------------
# Crops. r3: CLOSE-UPS ONLY - the face fills the panel, with at most a strip of wall. Three per
# block, so the six pairs do not stack up as one framing; each panel of the square master is a 1:2
# tall strip, so every crop works in portrait.
#
# The under-eye crops all show ONE side (split-face trial): a close three-quarter, one eye, and a
# steep three-quarter that shows the bulge standing out from the cheek almost in profile - the view
# closest to what the trial's 3D imaging measured. The forehead crops keep the whole forehead,
# hairline to brows, in frame with the eyes visible below it.
#
# `selfie` False on the one-eye crop: nobody holds a phone that close to their own eye and keeps it
# in focus, so "selfie" there invites a hand into frame. Engines have pulled every tight crop back
# to a half-face portrait before (engines-return-a-portrait-whatever-crop-you-ask-for); these crops
# are bounded by FEATURES, the one kind of tight crop some engines honour, and winners crop in post.
# --------------------------------------------------------------------------------------
CROPS = {
    # ---- pdrn-undereye ---------------------------------------------------------------
    "pdrn_three_quarter": dict(
        selfie=True,
        label="close three-quarter, one side",
        text=(
            "HER FACE FILLS THE PANEL, IN A CLOSE THREE-QUARTER VIEW. The phone is held so close that "
            "the top of her head and her chin are both cut off by the edges of the panel: the frame "
            "runs from her upper forehead at the top down to just below her mouth at the bottom. The "
            "near eye and the cheek beneath it are the largest things in the picture and sit in the "
            "upper middle of the panel; the far side of her face turns away. The plain wall shows only "
            "as a narrow strip beside the back of her head. THE UNDER-EYE OF THE NEAR EYE - the puffy "
            "bulge along the lower lid and the hollow groove below it - is what the picture is of."
        ),
    ),
    "pdrn_one_eye": dict(
        selfie=False,
        label="one eye, close",
        text=(
            "ONE EYE AND THE SKIN AROUND IT FILL THE PANEL. The frame runs from her eyebrow at the top "
            "down to about the level of her nostrils at the bottom, and across from the bridge of her "
            "nose on one side to her temple and the edge of her hair on the other. Only that one eye is "
            "in the picture; the other is outside the frame. Skin fills almost the whole panel, with at "
            "most a thin sliver of plain wall past her hair at one edge. THE LOWER EYELID, THE SOFT "
            "PUFFY BULGE BENEATH IT AND THE HOLLOW GROOVE THAT RUNS DOWN AND OUT FROM THE INNER CORNER "
            "OF THE EYE sit in the middle of the panel and are what the picture is of. An ordinary close "
            "photograph taken at home, sharp across the under-eye - not a studio or clinical photograph."
        ),
    ),
    "pdrn_steep": dict(
        selfie=True,
        label="close, steep three-quarter",
        text=(
            "HER FACE IS SEEN CLOSE AND STEEPLY FROM THE SIDE, AND FILLS THE PANEL. Her head is turned "
            "well away, so the camera looks along her cheek: the near eye, the near cheekbone and the "
            "side of her nose fill most of the panel, the far eye is only just visible beyond the "
            "bridge of her nose, and the frame runs from her upper forehead down to the corner of her "
            "mouth. From this angle THE PUFFY BULGE UNDER THE NEAR EYE STANDS OUT FROM THE LINE OF THE "
            "CHEEK, almost in profile, and the hollow groove below it shows as a dip - that is what the "
            "picture is of. The plain wall shows only as a narrow strip at one edge."
        ),
    ),
    # ---- argireline-forehead ---------------------------------------------------------
    "forehead_band": dict(
        selfie=True,
        label="close forehead band",
        text=(
            "HER FOREHEAD FILLS MOST OF THE PANEL, SEEN CLOSE AND SQUARE ON. The frame runs from just "
            "above her hairline at the top - a thin band of her pulled-back hair is in view - down to "
            "just below her eyes at the bottom, and her temples run off both side edges. Her eyebrows "
            "and both eyes are inside the bottom of the frame, but her nose tip, mouth and chin are "
            "outside it. There is almost no background: at most a thin sliver of plain wall above her "
            "hair. THE HORIZONTAL LINES ACROSS HER FOREHEAD AND THE FINE TEXTURE OF THE SKIN BETWEEN "
            "THEM ARE WHAT THE PICTURE IS OF, and the whole forehead, hairline to brows, is in frame."
        ),
    ),
    "upper_face": dict(
        selfie=True,
        label="close upper face",
        text=(
            "THE UPPER HALF OF HER FACE FILLS THE PANEL, SEEN CLOSE. The frame runs from just above her "
            "hairline - a little of her pulled-back hair is in view - down to the tip of her nose, with "
            "her temples running off both side edges. Her mouth and chin are outside the frame. The "
            "whole of her forehead is in view and is the largest thing in the picture, with both eyes "
            "clearly visible below it: ITS HORIZONTAL LINES AND THE TEXTURE OF THE SKIN BETWEEN THEM "
            "ARE WHAT THE PICTURE IS OF. The plain wall shows only as thin slivers at the top corners. "
            "Because the phone is close, her forehead looms a little."
        ),
    ),
    "forehead_three_quarter": dict(
        selfie=True,
        label="close forehead and temple, three-quarter",
        text=(
            "HER FOREHEAD AND ONE TEMPLE FILL THE PANEL, IN A CLOSE THREE-QUARTER VIEW. Her head is "
            "turned a little so the camera sees her forehead slightly from one side: the frame runs "
            "from just above her hairline at the top down to her cheekbones at the bottom, with the "
            "near temple and brow large in the frame and both eyes visible below the forehead. The "
            "whole forehead is in frame. The plain wall shows only as a narrow strip beside her face "
            "on one side. THE HORIZONTAL LINES RUNNING ACROSS HER FOREHEAD AND ROUND TOWARDS THE NEAR "
            "TEMPLE, and the texture of the skin between them, are what the picture is of."
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
            "SHE IS BETWEEN FORTY AND FIFTY-FIVE - MIDDLE-AGED, CLEARLY NOT YET SIXTY - AND THAT "
            "GOVERNS WHAT HER SKIN CAN HONESTLY LOOK LIKE. The puffiness and hollows under her "
            "eyes are established and stay put with her face at rest, fine lines sit on the lower "
            "lids and at the outer corners, and some grey in her hair is normal. But she is NOT "
            "elderly: no heavy hanging bags, no deeply sunken eyes, no drooping upper lids, none of "
            "the slackness of a woman in her seventies."
        ),
        # Luma's short form of `honesty` - the full clause pushed slot a's Luma brief to 6,251
        # characters in r2. Same constraints, no reasoning.
        # r3: "as far as before" became "as far as in the left panel" - no caption-bait words.
        luma_magnitude=("She STILL HAS under-eye bags and hollows - the same ones, plainly visible, only "
                        "somewhat smaller: each bulge stands out about four-fifths as far as in the "
                        "left panel and the groove is a little shallower. Visible when the panels are compared, but "
                        "anyone seeing this panel alone would still say she has under-eye bags."),
        luma_honesty=("Same eyes and eyelids. Every bulge and hollow under her eyes is still there, "
                      "only less pronounced, and the skin under her eyes is the same colour - a change "
                      "of shape, not of colour."),
        # r2: seedream drew r1's "puffy bulge" as a red, inflamed, bruise-like swelling that then
        # cleared in the right panel - an eye condition, and a colour change the trial never
        # measured. Same class as describe-the-thing-dont-name-it: the colour is now stated.
        feature=("THE PUFFINESS IS THE ORDINARY SOFT FULLNESS OF A TIRED, MIDDLE-AGED UNDER-EYE, THE "
                 "SAME COLOUR AS THE REST OF HER SKIN - not red, not pink, not purple, not inflamed, "
                 "and nothing like an allergy, an infection or a bruise. It shows by its SHAPE and by "
                 "the soft shadow beneath it, never by a colour."),
        nothing_else=("NOTHING OUTSIDE THE UNDER-EYE HAS CHANGED. Her forehead, her brows, the lines "
                      "beside her nose and mouth, her cheeks and her jaw look exactly the same in both "
                      "panels; only the area under her eye is different."),
        # r3: panels are named LEFT / RIGHT only - "EARLIER DAY / LATER DAY" became nbp_pro captions.
        subject=("IN THE LEFT PANEL, THE PUFFINESS AND THE HOLLOWS UNDER HER EYE ARE THE SUBJECT OF THE "
                 "PICTURE. "),
        # r2: r1's "about a fifth less full" was read as "gone" by gpt_image and nbp_pro and
        # overshot on nbp_flash - the bag all but vanished. The paragraph now LEADS with what stays,
        # gives the size as a checkable ratio of what remains (measure-geometry-dont-describe-it),
        # and ends on the single-panel test: glance at the right panel alone and she still has bags.
        magnitude=(
            "SHE STILL HAS UNDER-EYE BAGS AND HOLLOWS IN THE RIGHT PANEL - THE SAME ONES, PLAINLY "
            "VISIBLE, ONLY SOMEWHAT SMALLER. Most of each bulge is still there: it stands out from the "
            "cheek about FOUR-FIFTHS as far as it did, so the small curved shadow beneath it is only "
            "a little shorter and lighter. The hollow groove running down from the inner corner of "
            "the eye is a little shallower and holds a slightly softer shadow. The fine crinkled lines "
            "on the lower lid are a little softer.\n\n"
            "THE SIZE OF THE CHANGE IS NARROW AT BOTH ENDS. It must be VISIBLE: a viewer comparing "
            "the two panels should see that the under-eye is a little smoother and less hollow in the "
            "right one and be able to point to where. But it is MODEST: anyone looking at the right "
            "panel on its own would still say this woman has under-eye bags. The under-eye has not "
            "been filled, tightened or made young. A right panel with a flat, smooth, hollow-free "
            "under-eye is a failure, not a success."
        ),
        negatives=(
            "no smiling, no squinting, no closed eye, no wide staring eyes, no eye makeup, "
            "no change of eye shape between the panels, no change of eyelid shape between the panels, "
            "no double eyelid appearing, no filler look, no smooth hollow-free under-eye in the right "
            "panel, no bag disappearing completely, no lighter under-eye skin in the right panel, "
            "no concealer, no dark circles appearing, no bruise under the eye, no swollen eyes, "
            "no red eyelid, no inflamed eyelid, no pink under-eye, no purple under-eye, "
            "no allergic reaction, no stye, no eye infection, no brighter under-eye in the right panel, "
            "no smoother forehead in the right panel, "
            "no left eye beside right eye comparison, no one eye better than the other, "
            "no woman under forty, no elderly woman, no heavy hanging eye bags"
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
        # r2: "taut or frozen-looking" removed from every text Luma sees (it answered the r1 forehead
        # brief with content_moderated); "frozen" survives in the negative list, which Luma never
        # receives. Probing showed the refusal was not those words alone - see SMOKE_TEST_LOG.
        honesty=(
            "EVERY LINE ON HER FOREHEAD IS STILL THERE IN THE RIGHT PANEL - the same number of lines, "
            "each the same length and in the same place, and each still clearly visible as a line. "
            "None has disappeared, and the forehead has NOT become smooth or shiny. What has changed "
            "is small: the fine texture of the skin surface between and along the lines is a little "
            "finer and less rough, and the lines are a touch softer."
        ),
        luma_magnitude=("Every line is still there and nearly as deep - about nine-tenths. Mostly the "
                        "fine, dry, crosshatched surface texture is a little finer and calmer. Visible "
                        "when the panels are compared, but anyone seeing this panel alone would still "
                        "say she has forehead lines."),
        luma_honesty=("Every forehead line is still there - same number, length and place, still "
                      "clearly visible; only the fine surface texture is a little smoother and the "
                      "lines a touch softer."),
        # r2: seedream drew r1's deepest line as a raw ORANGE CRACK across the forehead, like a cut.
        feature=("HER FOREHEAD LINES ARE ORDINARY SOFT CREASES IN THE SKIN, THE SAME COLOUR AS THE REST "
                 "OF HER SKIN. They show as fine lines of shadow where the light grazes them - never as "
                 "cracks, cuts, scars or red or orange marks."),
        # r2: nbp_pro improved her whole face in r1 - under-eyes, the lines beside the nose - not
        # just the forehead the finding is about.
        nothing_else=("NOTHING OUTSIDE THE FOREHEAD HAS CHANGED. Her eyes, the skin under her eyes, "
                      "her cheeks and the lines beside her nose and mouth look exactly the same in both "
                      "panels; only her forehead is different."),
        age=(
            "SHE IS BETWEEN FORTY AND FIFTY-FIVE - MIDDLE-AGED, CLEARLY NOT YET SIXTY - AND THAT "
            "GOVERNS WHAT HER SKIN CAN HONESTLY LOOK LIKE. Her forehead lines are established and "
            "stay put with her face at rest, and some grey at the parting and temples is normal. But "
            "she is NOT elderly: no deep folds, no heavy brow, none of the crepe-papery slackness of "
            "a woman in her seventies."
        ),
        subject=("IN THE LEFT PANEL, THE LINES AND THE ROUGH SURFACE TEXTURE OF HER FOREHEAD ARE THE "
                 "SUBJECT OF THE PICTURE. "),
        # r2: leads with what stays, and gives the lines a ratio (nine-tenths as deep), because
        # nbp_pro's r1 right panel read as a rested, younger face.
        magnitude=(
            "EVERY LINE IS STILL THERE AND STILL CLEARLY VISIBLE IN THE RIGHT PANEL - the same number, "
            "the same length, the same place, and nearly as deep: each holds a shadow about "
            "NINE-TENTHS as dark and as long as in the left panel. What has changed is mostly the "
            "SURFACE: the "
            "fine, dry, crosshatched texture between and along the lines is a little finer and calmer, "
            "so the skin catches the grazing light a little more evenly and looks a little less rough "
            "and dry.\n\n"
            "THE CEILING MATTERS AS MUCH AS THE FLOOR. It must be VISIBLE: someone looking from one "
            "panel to the other should be able to see that the forehead surface in the right panel is "
            "smoother and point to where it has calmed. But it is SUBTLE - a viewer has to compare to see it, and "
            "anyone looking at the right panel on its own would still say this woman has forehead "
            "lines. The forehead does not read smooth, shiny, rested or younger. A right panel with "
            "a smooth, line-free forehead is a failure, not a success."
        ),
        negatives=(
            "no raised eyebrows, no frowning, no surprised expression, no brows in different "
            "positions between the panels, no smooth line-free forehead in the right panel, "
            "no line disappearing between the panels, no shiny forehead, no frozen forehead, "
            "no taut stretched forehead, no fringe, no bangs, no hair across the forehead, no hat, "
            "no headband, no woman under forty, no elderly woman, "
            "no crack in the skin, no cut, no scar, no incision, no red line, no orange line, "
            "no sunburn, no rested younger face in the right panel, no smaller eye bags in the right "
            "panel"
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
# r2: the side-lock is stated in PICTURE terms (which edge of the panel her nose points to), not
# in anatomical ones. r1 said "her own left" and gpt_image mirrored the whole face between the
# panels - the cheek marks jumped to the other cheek - while nbp_pro held one side but the wrong
# one. "Her own left" is a mental rotation the engine does not do reliably; "her nose points to
# the right-hand edge of the picture" is something it can see in its own output.
NOT_MIRRORED = ("The two panels are NEVER mirror images of each other: every mole and mark sits on "
                "the same side of her face in both")
SIDE_FRONT = ("SHE IS FACING THE CAMERA MORE OR LESS SQUARE ON IN BOTH PANELS - the FRONT of her "
              "face is what the camera sees on both days. " + NOT_MIRRORED)
SIDE_LEFT_EYE = ("IT IS THE SAME EYE IN BOTH PANELS: HER LEFT EYE, which in the picture has the bridge "
                 "of her nose at the LEFT-HAND EDGE of the panel and her temple at the RIGHT-HAND EDGE "
                 "- in BOTH panels. It is never one eye in one panel and her other eye in the other - "
                 "those are two different under-eyes, with different bulges, hollows and marks, and "
                 "there would be nothing to compare. " + NOT_MIRRORED)
# r3: the two three-quarter sides name the EYE as well as the cheek, because the under-eye slots
# now turn too - r2's three-quarter lock held on all six engines, so the wording is otherwise kept.
SIDE_NOSE_RIGHT = ("IN BOTH PANELS HER FACE IS TURNED TOWARDS THE RIGHT-HAND EDGE OF THE PICTURE - her "
                   "nose points to the right - so the eye, cheek and temple nearest the camera, on the "
                   "LEFT of the picture, are her right side: the same side, with the same marks on it, "
                   "on both days. Her face never points right in one panel and left in the other. "
                   + NOT_MIRRORED)
SIDE_NOSE_LEFT = ("IN BOTH PANELS HER FACE IS TURNED TOWARDS THE LEFT-HAND EDGE OF THE PICTURE - her "
                  "nose points to the left - so the eye, cheek, temple and side of the forehead nearest "
                  "the camera, on the RIGHT of the picture, are her left side: the same side, with the "
                  "same marks on it, on both days. Her face never points left in one panel and right in "
                  "the other. " + NOT_MIRRORED)

# r3: distances are all close now - "very close" against "a touch less close" - so the pair still
# varies without either panel leaving the close-up. The height rule is unchanged: later under-eye
# panel level or LOWER, later forehead panel level or HIGHER.
VIEWPOINTS = {
    # PDRN — right panel level or LOWER
    "a": dict(side=SIDE_NOSE_RIGHT,
              a=dict(cam="held just above her eye line and a little off to the side, angled slightly down",
                     turn="her face turned about twenty-five degrees towards the right-hand edge of the picture, level",
                     dist="framed very close", place="her near eye sits high and slightly right of centre"),
              b=dict(cam="held at her eye line, off to the same side",
                     turn="her face turned about thirty degrees towards the right-hand edge of the picture and tipped a little up",
                     dist="framed a touch less close, but still close", place="her near eye sits centred")),
    "b": dict(side=SIDE_LEFT_EYE,
              a=dict(cam="held at her eye line, a hand's width from her left eye",
                     turn="her face turned about ten degrees towards the left-hand edge of the picture, level",
                     dist="framed very close", place="the eye sits high and left of centre"),
              b=dict(cam="held just below her eye line and tilted up slightly",
                     turn="her face turned about twenty degrees towards the left-hand edge of the picture, level",
                     dist="framed a touch closer still", place="the eye sits centred and a little low")),
    "c": dict(side=SIDE_NOSE_LEFT,
              a=dict(cam="held at her eye line, well out to the side",
                     turn="her face turned about forty degrees towards the left-hand edge of the picture, level",
                     dist="framed close", place="her near eye sits high and right of centre"),
              b=dict(cam="held a little below her eye line, well out to the same side, tilted up",
                     turn="her face turned about fifty degrees towards the left-hand edge of the picture, level",
                     dist="framed a touch closer", place="her near eye sits centred")),
    # ARGIRELINE — right panel level or HIGHER
    "d": dict(side=SIDE_FRONT,
              a=dict(cam="held at her eye line",
                     turn="her head square to the camera, level",
                     dist="framed very close", place="her forehead sits high and right of centre"),
              b=dict(cam="held a little above her eye line and tilted down towards her forehead",
                     turn="her head square to the camera and tipped very slightly down",
                     dist="framed a touch less close, but still close", place="her forehead sits low and left of centre")),
    "e": dict(side=SIDE_FRONT,
              a=dict(cam="held a little below her eye line and tilted up slightly",
                     turn="her head square to the camera, level",
                     dist="framed a touch less close, but still close", place="her face sits centred and high"),
              b=dict(cam="held at her eye line",
                     turn="her head square to the camera, level",
                     dist="framed very close", place="her face sits left of centre")),
    "f": dict(side=SIDE_NOSE_LEFT,
              a=dict(cam="held at her eye line, off to one side",
                     turn="her face turned about twenty degrees towards the left-hand edge of the picture, level",
                     dist="framed very close", place="her forehead sits right of centre"),
              b=dict(cam="held a little above her eye line, off to the same side, angled down",
                     turn="her face turned about thirty degrees towards the left-hand edge of the picture, tipped very slightly down",
                     dist="framed a touch less close, but still close", place="her forehead sits high and centred")),
}

# Gaze — the free axis. Subtle on four slots, noticeable on two (a, e).
GAZE = {
    "a": ("her eyes are on the lens", "her eyes are well away from the lens, looking off to the side"),
    "b": ("her eye looks straight ahead, just past the lens", "her eye looks a fraction to one side of the lens"),
    "c": ("her eyes look ahead, past the camera", "her eyes glance a little towards the lens"),
    "d": ("her eyes are just off the lens to one side", "her eyes are on the lens"),
    "e": ("her eyes are lowered, looking a little down and away", "her eyes are straight down the lens"),
    "f": ("her eyes are on the lens", "her eyes are a fraction off the lens, towards the far side"),
}

# --------------------------------------------------------------------------------------
# The six women. r3 (Malcolm): Caucasian, 40-55, ordinary - six different women with different hair,
# colouring and features. `before` is the specific description of what the fault looks like on HER:
# the highest-value string per slot, because a generic "eye bags" or "forehead lines" is where an
# engine substitutes its own stock face. Each carries a named mark ON THE SIDE HER CROP SHOWS, as an
# identity anchor.
# --------------------------------------------------------------------------------------
WOMEN = [
    # ---- pdrn-undereye · Ye 2026 · ages 35-55 in the trial; cast 44-52 ---------------------
    dict(block="pdrn-undereye", key="a", crop="pdrn_three_quarter", walls=(0, 1),
         who=("a white ENGLISH woman of about forty-eight, with shoulder-length mid-brown hair going "
              "grey at the parting, tucked behind her ear, fair skin with a pinkish undertone, blue-grey "
              "eyes, sparse fair brows, and one small flat brown mole on her right cheekbone below the "
              "outer corner of her right eye"),
         before=("Under the near eye there is a soft, rounded, puffy bulge along the lower eyelid, full "
                 "enough to catch the light on its top and cast a small curved shadow beneath it. Below "
                 "and inside it a hollow groove runs down and outward from the inner corner of the eye "
                 "along the bone of the eye socket, holding its own soft shadow, so the under-eye reads "
                 "tired. Fine crinkled lines run across the thin skin of the lower lid, and a few short "
                 "creases fan from the outer corner.")),
    dict(block="pdrn-undereye", key="b", crop="pdrn_one_eye", walls=(2, 3),
         who=("a white AMERICAN woman of about fifty-two from the Midwest, with dull dishwater-blonde "
              "hair cut to the jaw, fair skin with a scatter of pale freckles across the cheekbones and "
              "the bridge of her nose, pale blue eyes, pale sparse brows, and a small flat brown mole at "
              "the outer end of her left eyebrow"),
         before=("Along her lower eyelid sits a distinct pouch of puffy skin, heavier towards the outer "
                 "half, with a soft crease beneath it where it meets the cheek. A clear hollow runs from "
                 "the inner corner of her eye diagonally down across the top of the cheek, deep enough to "
                 "hold a line of shadow. The skin of the lower lid is finely crinkled, with established "
                 "creases at the outer corner of the eye.")),
    dict(block="pdrn-undereye", key="c", crop="pdrn_steep", walls=(4, 5),
         who=("a white SCOTTISH woman of about forty-four, with coppery auburn hair faded at the "
              "parting and pulled loosely back, very fair skin with fine freckles, green eyes, pale "
              "reddish brows, and a tiny dark mole high on her left cheekbone"),
         before=("Seen from the side, a soft rounded bulge of puffy skin sits along the lower eyelid of "
                 "the near eye and stands out from the line of the cheek, with a small shadow tucked "
                 "beneath it. Below it the hollow groove along the bone of the eye socket dips in, and "
                 "then the cheek rises again. Fine crinkled lines cross the lower lid.")),
    # ---- argireline-forehead · Raikou 2017 · ages 30-60 in the trial; cast 43-54 -----------
    dict(block="argireline-forehead", key="d", crop="forehead_band", walls=(6, 7),
         who=("a white ITALIAN-AMERICAN woman of about forty-nine, with near-black hair pulled straight "
              "back into a clip, olive skin, dark brown eyes, heavy dark brows, and a small mole just "
              "above the outer end of her right eyebrow"),
         before=("Three long horizontal lines run across her forehead for most of its width, the middle "
                 "one the deepest and slightly wavy, with a shorter broken fourth line near the "
                 "hairline. Between and along them the skin has a fine, dry, crosshatched surface "
                 "texture that shows where the grazing light catches it, with a few visible pores "
                 "above the brows. A faint pair of short vertical creases sits between the brows.")),
    dict(block="argireline-forehead", key="e", crop="upper_face", walls=(8, 9),
         who=("a white DANISH woman of about forty-three, with pale ash-blonde hair tied back in a "
              "loose knot, very fair skin, a few faint freckles across the bridge of her nose, light "
              "blue eyes and pale sandy brows"),
         before=("Two horizontal lines run across her forehead - one long and clear across the middle, "
                 "one shorter and fainter above it - and the skin between and around them has a fine, "
                 "dry, slightly rough texture of tiny crisscrossing lines that shows where the light "
                 "grazes it. Pores are visible at the centre of the forehead.")),
    dict(block="argireline-forehead", key="f", crop="forehead_three_quarter", walls=(10, 11),
         who=("a white POLISH woman of about fifty-four, with dark-blonde hair greying at the temples "
              "and pulled back off her face, fair skin weathered by years of sun, grey eyes, fairly "
              "thick natural brows, and a small mole just below her hairline on the left side of her "
              "forehead"),
         before=("Four horizontal lines cross her forehead, the lower two long and clear, the upper two "
                 "shorter and broken, curving slightly downwards towards the near temple. The whole "
                 "forehead has a weathered, slightly rough, finely crosshatched surface from years of "
                 "sun, with visible pores along the brow.")),
]

# The light paragraph. The same grazing character on both days, and the guard that neither day is
# the kind one - on a volume subject soft frontal light makes a bag vanish by itself.
LIGHT = (
    "BOTH PICTURES ARE BRIGHT AND WELL EXPOSED, AND IN BOTH THE DAYLIGHT FALLS ON HER FROM HIGH UP "
    "ON ONE SIDE AND GRAZES DOWN ACROSS HER FACE. This matters more than anything else about the "
    "lighting. The features this picture is about run ACROSS her face - lines across the forehead, "
    "the bulge along the lower eyelid, the groove beneath it - and they only show when the light "
    "crosses them from above: then every line, every bulge and every hollow casts its own small "
    "shadow downwards. Flat light from the front would wash all of it away and hide what the picture "
    "exists to show. Bright and clean, her eyes clearly visible and not lost in shadow, no dark room, "
    "no flash - but definitely DIRECTIONAL, with a lit side and a softer shaded side.\n\n"
    "⚠️ NEITHER DAY IS LIT MORE KINDLY THAN THE OTHER. The light comes from a different side and the "
    "wall is different, but the right-hand picture is NOT lit more softly, more frontally or more "
    "evenly than the left-hand one - the light grazes across her just as strongly on both days. If "
    "the right-hand picture were lit more flatly, the improvement would simply be the light and the "
    "pair would be a lie."
)

SKIN = (
    "THE SKIN MUST HOLD UP AS REAL AND UNFLATTERED, and at this crop it is most of the picture. Pores "
    "are visible and vary in size by zone, several larger than their neighbours. Pigment is uneven "
    "and asymmetric, never mirrored from one side to the other. Fine vellus hairs catch the light. "
    "The skin is a little greasy at the nose and forehead and drier at the outer cheek. Real skin, "
    "photographed honestly, with no smoothing of any kind."
)


def build_prompt(w: dict) -> str:
    """Assemble one slot's full brief. Paragraph order is load-bearing: the no-writing and
    close-up/plain-wall rules open the brief (r3), and the honesty rules follow before the engine
    forms its own idea of what the improvement looks like."""
    b = BLOCKS[w["block"]]
    crop = CROPS[w["crop"]]
    v = VIEWPOINTS[w["key"]]
    g1, g2 = GAZE[w["key"]]
    w1, w2 = WALLS[w["walls"][0]], WALLS[w["walls"][1]]
    kind = "close-up phone selfies" if crop["selfie"] else "close-up photographs"

    hands = (
        "IT MUST BE OBVIOUS AT A GLANCE THAT SHE TOOK THIS HERSELF, HOLDING THE PHONE CLOSE - BUT THE "
        "PHONE AND HER HANDS ARE NEVER IN THE PICTURE. This is the view THROUGH the front camera of the "
        "phone she is holding, so the hand holding it cannot appear in its own frame, and neither can "
        "the phone. NO HAND, NO FINGERS, NO ARM, NO PHONE, NO PHONE CASE, NO MIRROR AND NO REFLECTION "
        "anywhere in either panel.\n\n"
        if crop["selfie"] else
        "NOTHING OF WHOEVER HELD THE CAMERA IS IN THE PICTURE - at this distance there is no room in "
        "the frame for it. No hand, no fingers, no arm, no phone, no phone case, no mirror and no "
        "reflection anywhere in either panel.\n\n"
    )

    return (
        # 1 — the frame. r3: the panels are LEFT and RIGHT only; no time gap in weeks (caption bait).
        f"Two ordinary {kind} of THE SAME WOMAN, taken at home on two different days, the left one "
        "first. They are placed side by side to fill one square frame edge to edge: TWO PANELS OF "
        "EXACTLY EQUAL WIDTH meeting at one crisp vertical edge precisely at the centre, with no gap "
        "and no dividing line. Each panel is a tall portrait and A COMPLETE PHOTOGRAPH OF HER ON ITS "
        "OWN - the two panels are NOT the left and right halves of one face.\n\n"

        # 1b — r3: the no-text rule restated at the top, because nbp_pro captioned three r2 slots.
        "THERE IS NO WRITING ANYWHERE IN THE PICTURE. No words, no letters, no numbers, no captions "
        "and no labels, and no strips, bars or boxes above, below or across the panels - nothing is "
        "written on it at all. It is just the two photographs, edge to edge.\n\n"

        # 1c — r3 (Malcolm): close-up, plain wall, nothing else in frame.
        "BOTH PHOTOGRAPHS ARE CLOSE-UPS: HER FACE FILLS EACH PANEL. It is so close to the camera that "
        "it spans nearly the whole width of the panel, the top of her head is cut off by the top edge, "
        "and her shoulders are not in the picture at all. The only background is a narrow strip of "
        "plain painted wall at one edge. NOTHING BUT HER FACE, HER HAIR AND THE PLAIN WALL IS IN THE "
        "FRAME.\n\n"

        # 2 — expression: the confound on this card
        + b["expression"] + "\n\n"

        # 3 — honesty rules, hoisted (r2: FOUR and FIVE moved up here, where rules hold).
        "FIRST OF ALL, THE THINGS THAT MUST BE TRUE OF THE RIGHT-HAND PANEL, BECAUSE THEY ARE WHAT "
        "MAKE THIS PAIR HONEST RATHER THAN AN ADVERTISEMENT:\n\n"
        "ONE. EVERY MOLE, FRECKLE AND DISTINCT MARK SHE HAS IS STILL THERE IN THE RIGHT PANEL, in the "
        "same place, the same size and the same number. Her identity is anchored to those marks and "
        "they do not fade, move or vanish.\n\n"
        "TWO. SHE IS THE SAME PERSON, THE SAME AGE AND THE SAME COMPLEXION IN BOTH PANELS. She has not "
        "been made younger, slimmer, prettier, better groomed or lighter-skinned, and she wears no "
        "makeup on either day.\n\n"
        f"THREE. {b['honesty']}\n\n"
        "FOUR. THE RIGHT PANEL IS NOT LIT MORE KINDLY. It is not brighter, softer, warmer or more "
        "frontally lit than the left: in both, daylight grazes down across her from high on one side, "
        "equally strongly. If the right panel were lit more kindly, the improvement would just be the "
        "light.\n\n"
        f"FIVE. {b['nothing_else']}\n\n"

        # 4 — two occasions
        "THESE ARE TWO SEPARATE OCCASIONS, NOT TWO COPIES OF ONE FRAME. Everything that identifies her "
        "stays the same, and everything a different day would change is different.\n\n"

        # 5 — identity lock
        "UNMISTAKABLY THE SAME WOMAN: the same face shape, the same nose, the same eye shape and "
        "eyelids, the same eye colour, the same skin colour, the same brow shape, the same hair colour "
        "and cut, and her moles and marks in the same places on her skin.\n\n"

        # 6 — per-panel viewpoint
        "THE CAMERA IS IN A PLAINLY DIFFERENT PLACE ON THE TWO DAYS. Two photographs taken on "
        "different days are never framed the same way twice, and a pair framed identically reads as "
        "one picture retouched. So:\n\n"
        f"IN THE LEFT PANEL: the camera is {v['a']['cam']}. She has {v['a']['turn']}, and {g1}. She "
        f"is {v['a']['dist']}, and {v['a']['place']} in the panel.\n\n"
        f"IN THE RIGHT PANEL: the camera is {v['b']['cam']}. She has {v['b']['turn']}, and {g2}. She "
        f"is {v['b']['dist']}, and {v['b']['place']} in the panel.\n\n"
        "These differences must be obvious when the two halves are compared - but in both panels the "
        "picture is a close-up and her face fills it.\n\n"

        # 6b — the side lock, in picture terms (r2)
        f"BUT ONE THING ABOUT THE VIEW DOES NOT CHANGE. {v['side']}. THE SAME AREA OF SKIN MUST BE ON "
        "SHOW IN BOTH PANELS, because the whole point of the pair is to compare one patch of her face "
        "against the same patch on a different day. The camera moves; the part of her face it looks at "
        "does not.\n\n"

        # 7 — the distance and angle guard
        "AND THE CHANGE MUST NEVER BE EXPLAINABLE BY THE CAMERA. The skin this picture is about is "
        "FULLY AND EQUALLY READABLE IN BOTH PANELS - the same sharpness, the same level of detail. The "
        "right panel is not further away, softer, blurrier, lower in contrast or shot from a more "
        "flattering angle. If a viewer could say 'it only looks better because of the camera or the "
        "light', the picture has failed completely.\n\n"

        # 8 — r3: two plain walls, nothing on or in front of them
        f"THE BACKGROUND IS A PLAIN PAINTED WALL, AND IT IS A DIFFERENT WALL ON EACH DAY. In the left "
        f"panel it is {w1[0]}, and the daylight falls on her from {w1[1]}. In the right panel it is "
        f"{w2[0]}, and the daylight falls on her from {w2[1]}. Each wall is one flat, even colour - "
        "no pattern, no texture, nothing hung on it and nothing standing in front of it, only the soft "
        "natural fall-off of the daylight across it. Because the camera is so close, the wall shows "
        "only as a narrow strip at the edge of each panel, and it is EMPTY: nothing but her face, her "
        "hair and the plain wall is in the frame, and there is no object of any kind at any edge."
        "\n\n"

        # 9 — also different
        "ALSO DIFFERENT BETWEEN THE TWO DAYS: her hair, the same cut and colour but falling or tied a "
        "little differently; and, if any of her clothing shows at the very bottom edge, a different "
        "everyday top in a different colour.\n\n"

        # 10 — hands and phone
        + hands +

        # 11 — the crop
        crop["text"] + "\n\n"

        # 12 — amateur tells (a line page, so the white-balance tell stays)
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

        # 17 — the left panel; `feature` says the fault is skin-coloured shape and shadow (r2)
        + b["subject"] + w["before"] + " " + b["feature"] + "\n\n"

        # 18 — the right panel: floor and ceiling
        "IN THE RIGHT PANEL: " + b["magnitude"] + "\n\n"

        # 19 — honesty restated at the point of change
        "AND AT THE SAME TIME, IN THAT SAME RIGHT PANEL: " + b["honesty"] + " " + b["nothing_else"] +
        " Every mole and mark is still there in the same place, and the light is no kinder than in the "
        "left panel. She has not been made younger, slimmer, prettier or better groomed, and she is "
        "wearing no makeup in either panel.\n\n"

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
    w1, w2 = WALLS[w["walls"][0]], WALLS[w["walls"][1]]
    kind = "close-up phone selfies" if crop["selfie"] else "close-up photographs"
    return (
        f"Two ordinary {kind} of THE SAME WOMAN, taken at home on two different days, the left one "
        "first, side by side filling one square frame: two panels of exactly equal width meeting at "
        "one crisp vertical edge at the centre. Each panel is a complete photograph of her, not one "
        "half of a face. No writing anywhere in the picture - no words, numbers, captions, labels or "
        "bars.\n\n"
        "Both are close-ups: her face spans nearly the whole width of each panel, the top of her head "
        "is cut off, no shoulders, only a narrow strip of plain painted wall at one edge. Nothing but "
        "her face, her hair and the plain wall is in the frame.\n\n"
        + b["expression"] + "\n\n"
        "THE RIGHT PANEL, FIRST OF ALL: every mole and mark still there in the same place; the same "
        "person, same age, same complexion, no makeup. " + b["luma_honesty"] + " It is not lit more "
        "kindly - not brighter, softer or more frontal than the left. " + b["nothing_else"] + "\n\n"
        "Two separate occasions, not two copies of one frame. Same face, nose, eye shape and eyelids, "
        "eye colour, skin colour, brows, hair colour and cut.\n\n"
        f"Left panel: camera {v['a']['cam']}; she has {v['a']['turn']}; {g1}; {v['a']['dist']}. "
        f"Right panel: camera {v['b']['cam']}; she has {v['b']['turn']}; {g2}; {v['b']['dist']}. "
        f"{v['side']}. The skin that matters is equally sharp in both panels.\n\n"
        f"Plain empty painted walls, one flat colour each: left, {w1[0]}, daylight falling from "
        f"{w1[1]}; right, {w2[0]}, daylight falling from {w2[1]}. Hair a little different.\n\n"
        "No hand, no phone and no mirror in shot.\n\n"
        + crop["text"] + "\n\n"
        "Amateur picture: a little crooked, focus not perfect, white balance slightly off, but "
        "bright.\n\n"
        f"She is {w['who']}. No makeup, natural brows, unstyled hair. An ordinary person, not a "
        "model.\n\n"
        "Daylight from high up on one side grazes DOWN across her face on both days, so every "
        "line, bulge and hollow casts its own small shadow. Bright, eyes clearly visible.\n\n"
        "Real skin: visible pores, vellus hair, uneven pigment. No smoothing.\n\n"
        + b["subject"] + w["before"] + " " + b["feature"] + "\n\n"
        "IN THE RIGHT PANEL: " + b["luma_magnitude"] + "\n\n"
        "Two panels that look the same are a complete failure. Honest, unretouched, unfiltered."
    )


NEGATIVE_GLOBAL = (
    # Text — the whole label system depends on there being none in the pixels. r3: the caption
    # forms nbp_pro produced in r2 are named (strips, bars), and "before and after wording" is gone,
    # because naming the words puts them in front of the engine.
    "no text, no lettering of any kind, no words, no letters, no numbers, no percentages, no captions, "
    "no labels, no caption strip, no caption bar, no label bar, no white bar under the panels, no "
    "title, no heading, no date, no watermark, no stock photo watermark, no printed text overlay, no "
    "logo, no signature, no timestamp, no date stamp, no arrows, no callout lines, no measurement "
    "scale, no grid overlay, "
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
    "no hand, no fingers, no arm, no elbow, no phone, no phone case, no smartphone, no selfie stick, "
    "no mirror, no reflection, "
    # Studio production values.
    "no studio backdrop, no seamless paper, no professional lighting, no softbox, no beauty dish, "
    "no ring light circle in the eyes, no fashion photograph, no glamour, no styled hair, no salon "
    "blow-dry, no bokeh portrait mode, no model, no supermodel, "
    # Exposure.
    "no dark room, no dim room, no murky lighting, no underexposed picture, no night, no camera "
    "flash, no flash shadow on a wall, "
    # r3 (Malcolm): a plain wall and nothing else. Every room object an engine has placed at an
    # edge on this project, by name - the bare-wall risk from acetyl wave 15.
    "no door, no doorframe, no door architrave, no open doorway, no window in shot, no window frame, "
    "no curtain, no blind, no furniture, no chair, no sofa, no headboard, no lamp, no lampshade, "
    "no picture frame on the wall, no painting, no photographs on the wall, no posters, no shelf, "
    "no bookcase, no coat, no coat hook, no plant, no light switch, no plug socket, no skirting "
    "board, no ceiling, no corner of the room, no object at the edge of the frame, no patterned "
    "wall, no wallpaper, no textured wall, no tiled wall, no bathroom, no car interior, no outdoors, "
    "no clutter, no busy background, no large area of background, "
    # r3 casting: Caucasian women only, so a casting ban no longer fights the brief.
    "no non-white model, "
    # The diptych form, and the close-up.
    "no three panels, no four panels, no grid of panels, no picture frame, no border, no vignette, "
    "no gap between panels, no dividing line of any colour, no full body, no distant framing, "
    "no head and shoulders shot, no shoulders, no upper body, no wide shot"
)

# The pair — shared by both blocks, then each block adds its own.
NEGATIVE_PAIR = (
    "no identical backgrounds between the panels, no same wall colour in both panels, no identical "
    "framing between the panels, no copy of the left panel, no mirror image of the left panel, no "
    "flipped view, no different side of the face between the panels, no different woman between the "
    "panels, no younger woman in the right panel, no makeup appearing in the right panel, no change "
    "of skin colour between the panels, no moles disappearing between the panels, no zero difference "
    "between the panels, no softer light in the right panel, no flatter light in the right panel, no "
    "flat frontal lighting, no shadowless face, no blurrier right panel, "
    # r2: nbp_pro / nbp_flash / gpt_image lit the r1 right panel brighter and kinder; flux2 made
    # the two panels the left and right halves of ONE face - the left-vs-right picture the side-lock
    # exists to prevent.
    "no brighter right panel, no warmer kinder light in the right panel, no split face composition, "
    "no two halves of one face, no left half and right half of the same face"
)


def caption_bait(text: str) -> list:
    """The CAPTION_BAIT words present in `text` (whole words, any case)."""
    import re
    return sorted({m.group(0).lower() for m in
                   re.finditer(r"\b(" + "|".join(CAPTION_BAIT) + r")\b", text, re.I)})


def main() -> None:
    slots = []
    for w in WOMEN:
        b = BLOCKS[w["block"]]
        prompt = build_prompt(w)
        prompt_luma = build_prompt_luma(w)
        negative_extra = NEGATIVE_PAIR + ", " + b["negatives"]
        assert len(prompt_luma) < LUMA_CAP, (
            f"{w['block']}-{w['key']}: luma prompt is {len(prompt_luma)} chars, cap is {LUMA_CAP}")
        # No digits anywhere in a prompt: a number in the brief is a number nbp_pro can print.
        assert not any(ch.isdigit() for ch in prompt + prompt_luma), f"{w['key']}: digit in prompt"
        # r3: no word nbp_pro has turned into a caption - gpt_image and nbp read the negatives too.
        bait = caption_bait(prompt + prompt_luma + NEGATIVE_GLOBAL + negative_extra)
        assert not bait, f"{w['key']}: caption bait {bait}"
        # r3 smoke: naming the window drew the window on four tiles. The negatives may name it
        # (that is what they are for); nothing in the positive text may.
        assert "window" not in (prompt + prompt_luma).lower(), f"{w['key']}: 'window' in prompt"
        slots.append({
            # Subject in the id (slot-letters-restart-per-wave), and a round prefix so an r3 name
            # can never be confused with the r2 slot of the same letter.
            "id": f"uef3--{w['block']}-{w['key']}",
            "title": (f"{w['block']} · {b['study']} · {CROPS[w['crop']]['label']} — "
                      f"{w['who'].split(',')[0].replace('a ', '', 1)}"),
            "class": "B",
            "width": SIZE,
            "height": SIZE,
            "target_slot": f"{b['page']} key_findings_ba {b['block']} ({b['heading']})",
            "generated_from": (f"r3 smoke brief - {SMOKE_CONFIG}"
                               if w["key"] in SMOKE_SLOTS else f"{ROUND}, revised after the smoke test"),
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
            "negative_extra": negative_extra,
        })

    cfg = {
        "wave": WAVE,
        "created": "2026-09-24",
        "round": ROUND,
        "doc": ("docs/clinical-trial-before-after-images.md §12-13, .claude/rules/website-imagery.md, "
                "built by scripts/build-under-eye-forehead-before-after-config.py"),
        "note": (
            "ROUND 3 - BEFORE/AFTER DIPTYCHS FOR THE SAME TWO SCIENCE-PAGE CARDS. pdrn-undereye "
            "(slots a-c) -> /pages/pdrn-research key_findings_ba f4, 'Under-Eye Bags: About 2x the "
            "Retinol Change' (Ye 2026, split-face, women 35-55, 0.1% PDRN eye cream vs retinol, 28 "
            "days). argireline-forehead (slots d-f) -> /pages/acetyl-hexapeptide-8-research "
            "(templates/page.research-argireline.json) key_findings_ba f5, 'Forehead Roughness -7.4% "
            "by Day 20' (Raikou 2017, placebo-controlled, women 30-60, 10% Argireline).\n\n"
            "MALCOLM, 2026-09-24: 'Lets make a new batch - using caucasian women - and lets keep the "
            "face close up so not much background is shown - and lets keep the background a plain wall "
            "with no extra details'. So: six different Caucasian women aged 40-55 (replacing r2's "
            "trial-population casting); close-up crops only; a plain painted wall in one flat colour, "
            "different on each day, with nothing on or in front of it.\n\n"
            "CANDIDATES ONLY. Malcolm picks with _ / __ in place. Nothing here is uploaded.\n\n"
            "KEPT FROM r2: honesty rules first (no kinder light in the right panel; modest change - "
            "four-fifths of each bag remains, forehead lines nine-tenths as deep, and the right panel "
            "alone still shows bags or lines; nothing outside the region changes); identity lock; two "
            "sessions, not two frames; the side-lock in picture terms; light from high on one side "
            "grazing down; every camera-height difference against the improvement.\n\n"
            "NEW IN r3: all three under-eye slots show ONE side (split-face), so r2's frontal both-eyes "
            "question does not arise; panels named only LEFT and RIGHT and no week/month/earlier/later/"
            "before/after anywhere an engine reads (nbp_pro captioned three r2 slots from those words), "
            "asserted by the builder; 'no writing anywhere' is paragraph two. KNOWN RISK: on acetyl wave "
            "15 a bare wall made nbp_flash draw a phone at the edge. Paragraph three says nothing but her "
            "face, hair and the wall is in frame, and room objects are negated by name. Check every tile "
            "for stray objects.\n\n"
            "SMOKE TEST: slots a and d ran from the brief preserved at "
            "configs/banners/before-after-undereye-forehead-r3-smoke.json and are not re-run. It found "
            "windows or a doorframe drawn into four of twelve tiles - the brief had named 'a window' as "
            "the light source - and three tiles not close. b, c, e, f run on this revised brief: the "
            "word window is gone from every prompt, and paragraph 1c states the closeness as geometry "
            "(face spans nearly the whole panel width, top of the head cut off, no shoulders).\n\n"
            "SUPPLIERS: all six (rule 1). gpt_image resolves to the account's latest full-quality model "
            "(generate-multi.py d5de768). Check nbp_pro for captions, flux2 for identity and age, luma "
            "for a content_moderated refusal."
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
