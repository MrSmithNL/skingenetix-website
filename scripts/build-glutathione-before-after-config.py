#!/usr/bin/env python3
"""Build the before/after wave for the two clinical blocks on /pages/glutathione-research.

    python3 scripts/build-glutathione-before-after-config.py
    → configs/banners/block-glutathione-research-before-after.json

WHY A BUILDER AND NOT HAND-WRITTEN JSON. Eight slots share one sixteen-part skeleton and
differ in five fields (woman, two rooms, crop, block, magnitude). Hand-copying a 7,000-character
prompt eight times is how a stale clause survives a round — on this project a negative that
banned the ethnicity the casting was asking for lived through two waves precisely because
nobody re-reads a prompt that looks right. One skeleton, eight substitutions, and a length
assertion for Luma's 6,000-character cap.

WHAT THIS BRIEF INHERITS from `docs/clinical-trial-before-after-images.md` (fifteen waves on
the acetyl page): two sessions rather than two frames; one prompt per slot so each pair gets
its own room pair; no baked-in text of any kind; the identity lock; the visible-improvement
floor; no hand or phone in frame; nbp_pro excluded on evidence.

WHAT IT DELIBERATELY INVERTS, because this page measures TONE and that page measured LINE DEPTH:

  1. LIGHTING. The acetyl brief demanded raking sidelight, because an expression line reads by
     the shadow it casts and flat frontal light hides it. That instruction is actively wrong
     here. Raking light lays a shadow gradient across the cheek, and a shadow gradient is
     indistinguishable from a patch of uneven pigment — it would manufacture in the left panel
     the very thing the right panel is supposed to have improved, and a viewer could fairly say
     the difference was the lamp. Tone reads under bright, soft, broad daylight arriving from
     roughly the front.

  2. WHITE BALANCE. "Indoor white balance a little wrong" was one of the acetyl brief's best
     amateur tells. It cannot survive on a page about colour: a warm cast in one panel and a
     cool cast in the other is a tone difference the product did not cause. The amateur read is
     bought instead with crooked framing, an off-eye-level angle, mild shadow noise and
     imperfect focus, and both files are briefed as cleanly exposed and neutral.

  3. THE MARKS. `realism-marks-become-the-problem-on-a-pigmentation-page` — moles and freckles
     are this store's standard defence against plastic AI skin, and on a brightening page they
     illustrate the concern instead of the result. Here the resolution is not to remove them but
     to split them in two: the DIFFUSE mottling is the deliberate subject of the left panel and
     is what evens out, while DISCRETE moles and freckles are identity anchors and may not
     disappear. Slot `d` casts a densely freckled woman on purpose — it is the sharpest test of
     that line in the batch.

  4. THE HONESTY CLAUSE. The acetyl brief negated "no lighter skin in the right panel" outright.
     That cannot stand unmodified when the trial's own endpoint is a reduced melanin index. The
     line is re-cut instead: the PATCHES converge toward her own surrounding tone, and her
     baseline complexion — the skin between the patches, under the jaw, down the neck — is
     identical in both panels. She has not become a paler person. Stated positively in the body,
     because a ban that contradicts the brief is the hardest kind of instruction to notice.

MALCOLM, 2026-08-27: amateur, normal-looking Caucasian women aged 45–55; different backgrounds
and lighting; and "slightly different head position and eye gaze, so that the before and after
images are clearly (subtly) different images". Crop varies across the batch — some full face,
some half face, some closer still.

Author: Claude Code, 2026-08-27.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WAVE = "block-glutathione-research-before-after-r2"
OUT = ROOT / "configs" / "banners" / f"{WAVE}.json"

# Luma answers anything over 6,000 characters with a bare HTTP 422 that reads exactly like a
# content refusal. The assertion is set below the real cap deliberately: r2's longest Luma brief
# came in 122 characters under it, which is close enough that any later edit to the shared
# skeleton would silently push a slot over and lose the backend with a misleading error.
LUMA_CAP = 5700

# --------------------------------------------------------------------------------------
# ROUND 1 WAS A ONE-SLOT SMOKE TEST ACROSS ALL FIVE SUPPLIERS, AND IT PAID FOR ITSELF.
# Output preserved at assets/ai-generated/2026-08-22-multi-block-glutathione-research-before-after-r1,
# brief preserved at configs/banners/block-glutathione-research-before-after-r1.json.
# Four faults, three of them systematic. What r2 changes, and why:
#
#   1. THE FRECKLES DISAPPEARED. gpt_image, nbp_flash and seedream all cleared the discrete
#      freckles and sun spots out of the right panel, not just the diffuse mottling. The rule
#      was in the brief and lost anyway, because it sat in the seventeenth paragraph and the
#      engine's own prior — brightening means removing spots — got there first. It is now the
#      THIRD thing in the prompt, before the rooms and before the crop, and it is restated
#      inside the right-panel paragraph where the change is actually described. Position, not
#      wording, was the problem: r1's wording was already explicit.
#
#   2. THE TWO HALVES HAD DIFFERENT COLOUR CASTS. seedream went warm-to-cool and luma did the
#      same. `no colour cast` in the negative list did not hold it, and on a page about the
#      colour of skin this is the single most damaging fault available: it hands a viewer a
#      reason to say the difference was the light. Now stated as a matching requirement between
#      the halves rather than a property of each, and with the failure named.
#
#   3. THE MAGNITUDE OVERSHOT ON f1. seedream's right panel had cleared the patch almost
#      entirely. "Much closer in colour" was read as "gone". f1's magnitude now carries its own
#      ceiling — the same patches must still be findable in the same places.
#
#   4. flux2 DID WHAT THE PROJECT MEMORY SAYS IT DOES: one room in both panels, the same head
#      angle and gaze, no visible difference at all, and a woman who read mid-sixties. It stays
#      in the run because rule 1 of website-imagery.md is that every image goes to every
#      supplier and it costs little, but it is the first place to check identity and age.
#      The age band is now stated positively as well as negated.
#
# Author: Claude Code, 2026-08-27.
# --------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------
# Rooms. Sixteen, so no pair repeats and no pair shares a room with another pair. Each is a
# wall colour + a light direction + ONE soft unidentifiable element: a bare wall left nothing
# for the model to place at the edge and nbp_flash supplied a phone instead (wave 15).
# --------------------------------------------------------------------------------------
ROOMS = [
    ("a WARM WHITE wall", "broad daylight arriving from in front of her and a little to her left",
     "the soft vertical edge of a doorframe"),
    ("a PALE GREY wall", "broad daylight arriving from in front of her and a little to her right",
     "the faint corner where two walls meet"),
    ("a SOFT BEIGE wall", "soft daylight arriving from in front of her and slightly above",
     "the blurred top of a chair back"),
    ("an OFF-WHITE wall", "even daylight arriving from in front of her and a little to her right",
     "the pale rectangle of a picture frame with nothing readable in it"),
    ("a PALE GREIGE wall", "broad soft daylight arriving from in front of her and to her left",
     "the shape of a lampshade that is switched off"),
    ("a MUTED SAGE-GREY wall", "even daylight arriving from in front of her and to her right",
     "the vertical fall of a plain curtain"),
    ("a SOFT TAUPE wall", "soft daylight arriving from in front of her and a little to her left",
     "the pale line of a skirting board meeting the floor"),
    ("a PLAIN CREAM wall", "broad daylight arriving from in front of her and to her right",
     "the soft dark shape of a coat on a hook"),
    ("a PALE BLUE-GREY wall", "even daylight arriving from in front of her and slightly above right",
     "the faint horizontal line of a shelf with nothing identifiable on it"),
    ("a CHALK WHITE wall", "soft broad daylight arriving from in front of her and to her left",
     "the soft upright of a door architrave"),
    ("a PALE OATMEAL wall", "even daylight arriving from in front of her and a little to her left",
     "the blurred edge of a door standing open"),
    ("a LIGHT STONE-GREY wall", "broad daylight arriving from in front of her and to her right",
     "the soft pale line where the wall meets the ceiling"),
    ("a SOFT CLAY-PINK wall", "soft daylight arriving from in front of her and slightly to her left",
     "the out-of-focus back of a dining chair"),
    ("a WARM IVORY wall", "even broad daylight arriving from in front of her and to her right",
     "the soft dark line of a picture rail"),
    ("a PALE PUTTY wall", "broad soft daylight arriving from in front of her and to her left",
     "the blurred vertical edge of a wardrobe"),
    ("a COOL LINEN-WHITE wall", "even daylight arriving from in front of her and a little to her right",
     "the soft fall of a plain window blind"),
]

# --------------------------------------------------------------------------------------
# Crops. Malcolm asked for variety across the batch. Each panel of the square master is a
# 1:2 tall strip, so every one of these has to work in portrait.
#
# `selfie` is False on the two closest crops for a reason that is not fussiness: nobody can
# hold a phone close enough for a cheek macro and still have it in focus, so briefing "selfie"
# there asks for something that cannot happen and invites a hand or a phone back into frame.
# --------------------------------------------------------------------------------------
CROPS = {
    "full": dict(
        selfie=True,
        text=(
            "THE WHOLE OF HER HEAD IS IN VIEW. The panel holds her from just above the top of her "
            "hair down to her collarbones, with the tops of her shoulders in the bottom corners and a "
            "hand's width of plain wall showing past her head on each side. Her face fills a little "
            "over half the height of the panel, so the whole of it - forehead, both eyes, nose, mouth, "
            "jaw and the front of her neck - is clearly readable at once, and the skin of her neck and "
            "the top of her chest is visible below it."
        ),
    ),
    "close": dict(
        selfie=True,
        text=(
            "HER FACE COMPLETELY FILLS THE PANEL. The frame cuts across her forehead just below the "
            "hairline at the top and at the point of her chin at the bottom, and her cheeks run all the "
            "way to both edges and are slightly cut off by them. Her whole forehead, both eyes, her nose "
            "and her whole mouth are still in view, but there is essentially no space left around her "
            "face - only narrow slivers of the room past her at the very edges. Because the lens is this "
            "close it visibly distorts: her nose and chin read large and her forehead looms."
        ),
    ),
    "half": dict(
        selfie=False,
        text=(
            "ONLY HALF OF HER FACE IS IN THE PANEL, AND IT FILLS IT. The frame is a vertical slice "
            "running from the centre line of her nose outwards past her ear: one eye and its outer "
            "corner, one whole cheek and cheekbone, one temple, one eyebrow, one corner of her mouth and "
            "part of that side of her jaw. The other half of her face is outside the frame entirely and "
            "is not visible. Her head is turned very slightly so that the cheek presents itself almost "
            "flat to the camera, and that cheek is the largest thing in the picture. This is an ordinary "
            "close photograph taken at home in daylight, not a selfie and not a studio portrait."
        ),
    ),
    "macro": dict(
        selfie=False,
        text=(
            "THIS IS A VERY CLOSE PICTURE OF ONE CHEEK AND SKIN IS ALMOST THE ENTIRE FRAME. The panel is "
            "filled by the area from just beneath the lower lashes at the top, across the whole cheekbone, "
            "in to the side of the nose at one edge and down to the line of the jaw at the bottom. The "
            "outer corner of one eye and a few lower lashes are just inside the top of the frame so it is "
            "unmistakably a face and not an abstract surface, but there is no whole face in view and no "
            "mouth. Pores, fine surface texture and the colour of the skin are what the picture is of. "
            "This is an ordinary close photograph taken at home in daylight, not a selfie and not a "
            "studio portrait, and it is sharp enough on the cheekbone to read the skin."
        ),
    ),
}

# --------------------------------------------------------------------------------------
# The eight women, four per block. Caucasian, 45-55, ordinary. `before` is the specific,
# per-woman description of what her uneven tone actually looks like - the picture's subject,
# and the thing engines invent badly when it is left to "uneven skin tone".
# --------------------------------------------------------------------------------------
WOMEN = [
    # ---- f1 · Watanabe 2014 · 2% GSSG, 10 weeks, clearly visible -------------------------
    dict(block="f1", key="a", crop="full", rooms=(0, 1),
         who=("a white ENGLISH woman of about fifty-two, with mid-brown hair going grey at the "
              "parting and cut to the shoulder, fair skin, grey-blue eyes and sparse brows"),
         before=("Her tone is visibly uneven and tired-looking: soft brown mottling spread across "
                 "both cheekbones and out towards the temples, a duller sallow cast over the "
                 "mid-face and forehead compared with the clearer skin of her neck, and a few "
                 "small flat sun spots high on each cheek. The mottling has soft edges and no two "
                 "patches are the same shape or in mirrored positions.")),
    dict(block="f1", key="b", crop="close", rooms=(2, 3),
         who=("a white DANISH woman of about forty-eight, very fair, with pale ash-blonde hair, "
              "light blue eyes and pale sandy brows and lashes"),
         before=("Her tone is visibly uneven and tired-looking: a dull greyish-sallow cast over the "
                 "whole mid-face, diffuse patchy discolouration at both temples and along the sides "
                 "of the forehead, and a faint brownish shadowing beneath the eyes that is part "
                 "pigment and not only shade. The patches have soft edges, differ in shape and are "
                 "not mirrored from one side to the other.")),
    dict(block="f1", key="c", crop="half", rooms=(4, 5),
         who=("a white woman of about fifty-one from southern ITALY, with near-black hair pulled "
              "back, olive skin, dark brown eyes and heavy dark brows"),
         before=("Her tone is visibly uneven: a soft-edged brown patch of pigmentation spread over "
                 "the cheekbone and up towards the temple, a duller band of darker tone above the "
                 "upper lip, and a general muddiness across that side of the face compared with the "
                 "even olive of her jaw and neck. The patch has no hard border and is not mirrored "
                 "on the other side of her face.")),
    dict(block="f1", key="d", crop="macro", rooms=(6, 7),
         who=("a white IRISH woman of about forty-six, with coppery red hair faded at the parting, "
              "very fair densely freckled skin and green eyes"),
         before=("Her freckles are dense across the cheekbone and they sit in a field that is itself "
                 "blotchy and unevenly darkened - patches of duller, browner tone between and around "
                 "them, a faint reddish unevenness lower on the cheek, and an overall dull cast that "
                 "makes the whole area read muddy rather than clear.")),
    # ---- f3 · Khanna 2025 · systematic review, pooled, modest ---------------------------
    dict(block="f3", key="e", crop="full", rooms=(8, 9),
         who=("a white FRENCH woman of about fifty-three, with chestnut brunette hair greying at the "
              "temples, fair skin with an olive undertone and hazel eyes"),
         before=("Her tone is uneven and a little tired-looking: a dull greyish cast across the "
                 "mid-face, soft patchy discolouration over both cheekbones, and skin that reads flat "
                 "and lacklustre next to the more even tone of her neck. The patches are soft-edged, "
                 "irregular and not mirrored side to side.")),
    dict(block="f3", key="f", crop="close", rooms=(10, 11),
         who=("a white POLISH woman of about forty-seven, with ash-blonde hair, broad cheekbones, "
              "fair skin with a distinctly olive undertone and grey eyes"),
         before=("Her tone is uneven: patchy sallowness across the mid-face and either side of the "
                 "nose, a duller yellowish cast on the forehead, and a scatter of small flat "
                 "pigmented marks over the cheekbones. The patches are soft-edged, differ in shape "
                 "and are not mirrored.")),
    dict(block="f3", key="g", crop="half", rooms=(12, 13),
         who=("a white AMERICAN woman of about fifty from the Midwest, with dull dishwater-blonde "
              "hair pulled back in a clip, fair skin and pale blue eyes"),
         before=("Her tone is uneven: blotchy high colour spreading unevenly across the cheek, small "
                 "flat sun spots over the cheekbone and the side of the nose, and a duller, greyer "
                 "cast on that side of the forehead. The blotching is irregular, soft-edged and not "
                 "mirrored on the other side of her face.")),
    dict(block="f3", key="h", crop="macro", rooms=(14, 15),
         who=("a white GREEK woman of about forty-nine, with almost-black brunette hair, warm olive "
              "skin and dark brown eyes"),
         before=("Her tone is uneven across the cheekbone: a soft-edged band of darker sun pigment "
                 "running along the top of the cheekbone and out to the temple, a duller muddier cast "
                 "over the rest of the cheek, and a few small flat brown marks. Nothing is mirrored "
                 "and nothing has a hard edge.")),
]

# --------------------------------------------------------------------------------------
# Magnitude, per block. Both a floor and a ceiling, and they are deliberately narrow —
# f3's finding is a pooled review conclusion, not a single trial's percentage, so an
# emphatic change there would be the same class of overstatement the acetyl f3 cap exists
# to prevent.
# --------------------------------------------------------------------------------------
MAGNITUDE = {
    "f1": ("The change is CLEARLY VISIBLE. The diffuse mottling and the patchy areas have evened out a "
           "great deal - much closer in colour to the clear skin around them - and the dull cast has "
           "lifted, so the whole area reads clearer, fresher and softly luminous rather than flat and "
           "tired. The skin also looks a little better hydrated and smoother, with a soft healthy sheen "
           "rather than an oily shine. BUT THERE IS A CEILING ON THIS AND IT IS AS IMPORTANT AS THE "
           "FLOOR: the patches are FAINTER, NOT GONE. Every one of them is still findable in exactly "
           "the same place, with the same shape and the same soft edges - a viewer looking from one "
           "panel to the other must be able to match them up one for one. A right panel with clear, "
           "clean, patch-free skin is a failure, not a success."),
    "f3": ("The change is REAL BUT MODEST, and the ceiling matters as much as the floor here. The "
           "patchy areas are somewhat more even and the dull cast has lifted a little, so the area "
           "reads slightly clearer and fresher. Someone should have to look from one panel to the "
           "other to see it - and should then be able to point to exactly which areas are more even. "
           "It must NOT be dramatic, the skin must not look transformed or newly radiant, and the "
           "patches are still plainly present, just less pronounced."),
}


def build_prompt(w: dict) -> str:
    crop = CROPS[w["crop"]]
    r1, r2 = ROOMS[w["rooms"][0]], ROOMS[w["rooms"][1]]
    kind = "phone selfies" if crop["selfie"] else "close photographs"

    selfie_para = (
        "IT MUST BE OBVIOUS AT A GLANCE THAT SHE TOOK THIS HERSELF - BUT THE PHONE AND HER HANDS ARE "
        "NEVER IN THE PICTURE. This is the view THROUGH the front camera of the phone she is holding, "
        "so the hand holding it cannot appear in its own frame, and neither can the phone. NO HAND, NO "
        "FINGERS, NO ARM, NO ELBOW, NO PHONE, NO PHONE CASE, NO MIRROR AND NO REFLECTION anywhere in "
        "either panel.\n\n"
        if crop["selfie"] else
        "NOTHING OF WHOEVER HELD THE CAMERA IS IN THE PICTURE. No hand, no fingers, no arm, no elbow, "
        "no phone, no phone case, no mirror and no reflection anywhere in either panel - only her and "
        "the room behind her.\n\n"
    )

    return (
        # 1 — the frame
        f"Two ordinary {kind} of THE SAME WOMAN, taken WEEKS APART at home, placed side by side to "
        "fill one square frame edge to edge: TWO PANELS OF EXACTLY EQUAL WIDTH meeting at one crisp "
        "vertical edge precisely at the centre. Each panel is a tall portrait. The left panel is the "
        "earlier one, the right panel is the later one.\n\n"

        # 2 — expression
        "Her expression is flat and unposed on both days, mouth closed, not smiling.\n\n"

        # 3 — THE THREE RULES, HOISTED. In round 1 these lived near the end and lost to the
        # engine's own idea of what "brightening" means. They are now the first substantive
        # instruction in the prompt.
        "BEFORE ANYTHING ELSE, THREE THINGS THAT MUST BE TRUE OF THE RIGHT-HAND PANEL, BECAUSE THEY "
        "ARE WHAT MAKE THIS PAIR HONEST RATHER THAN AN ADVERTISEMENT:\n\n"
        "ONE. EVERY MOLE AND EVERY FRECKLE SHE HAS IS STILL THERE IN THE RIGHT PANEL, in the same "
        "place, the same size and the same number, and every one of them is still plainly visible and "
        "countable. This is not a picture about removing spots. Her freckles do not fade, her moles do "
        "not vanish and her sun spots are not cleared away. What evens out is the SOFT, DIFFUSE, "
        "BLOTCHY MOTTLING BETWEEN AND AROUND THEM - the patchy, muddy, uneven background colour of the "
        "skin. The distinct marks stay; the cloudiness lifts.\n\n"
        "TWO. SHE IS NOT A PALER PERSON IN THE RIGHT PANEL. Her complexion is exactly the same "
        "complexion. The clear skin between the patches, the skin under her jaw and the skin of her "
        "neck are precisely the same colour in both panels. Her skin has not been lightened, bleached "
        "or whitened and has not gone chalky, pale or grey.\n\n"
        "THREE. THE TWO HALVES MATCH EACH OTHER FOR COLOUR AND BRIGHTNESS. Neither half is warmer, "
        "cooler, darker or brighter than the other - no yellow or orange cast on one side and grey or "
        "blue on the other. This picture is about the colour of her skin, so if one half is tinted "
        "differently from the other the whole picture has failed, because nobody could tell whether "
        "the difference came from her skin or from the light.\n\n"

        # 4 — two occasions
        "THESE ARE TWO SEPARATE OCCASIONS, NOT TWO COPIES OF ONE FRAME. Everything that identifies "
        "her stays the same, and everything a different day would change is different.\n\n"

        # 4 — identity lock
        "UNMISTAKABLY THE SAME WOMAN: the same face shape and jawline, the same nose, the same eye "
        "colour, the same brow shape, the same hair colour and cut, and her moles and freckles in the "
        "same places on her skin.\n\n"

        # 5 — two rooms
        f"THE TWO PLACES ARE DIFFERENT ROOMS. On the earlier day she is in an ordinary room with "
        f"{r1[0]} behind her and, far out of focus at one edge, {r1[2]}; {r1[1]}. On the later day she "
        f"is in an ordinary room with {r2[0]} behind her and, well out of focus at one edge, {r2[2]}; "
        f"{r2[1]}. Two plainly different neutral interiors - a different wall colour and a different "
        "light direction each time. Apart from that one soft out-of-focus thing at the edge, nothing "
        "is in view behind her but the painted wall: no furniture, no pictures, no shelves, no "
        "appliances, no window in shot, no clutter.\n\n"

        # 6 — head position and gaze (Malcolm, 2026-08-27)
        "HER HEAD IS HELD DIFFERENTLY AND SHE IS LOOKING SOMEWHERE DIFFERENT ON THE TWO DAYS, AND THIS "
        "IS WHAT STOPS THE PAIR LOOKING LIKE ONE PICTURE EDITED TWICE. On one day her head is turned a "
        "few degrees to one side and tipped very slightly down, and her eyes are on the camera. On the "
        "other day it is turned a few degrees the other way and tipped very slightly up, and her eyes "
        "are just off the camera. The difference is small - she is recognisably in the same kind of "
        "pose both times - but it is unmistakable when the halves are compared, exactly as two "
        "photographs of the same person weeks apart would differ.\n\n"

        # 7 — also different
        "ALSO DIFFERENT BETWEEN THE TWO DAYS: the height and angle the camera is held at; a completely "
        "different everyday garment; and her hair, the same cut but unstyled and falling differently.\n\n"

        # 8 — hands and phone
        + selfie_para +

        # 9 — the crop
        crop["text"] + "\n\n"

        # 10 — amateur tells, but NOT colour ones
        "IT IS AN AMATEUR PICTURE OFF A PHONE, AND THE TELLS ARE IN THE FRAMING, NOT IN THE COLOUR. The "
        "angle is not eye level, the frame is a few degrees crooked and off-centre, the focus is not "
        "perfect and there is a little noise in the shadows. BUT BOTH PICTURES ARE CLEANLY EXPOSED AND "
        "NEUTRAL IN COLOUR - no orange indoor cast, no blue cast, no filter, nothing warmer or cooler "
        "in one panel than the other. This picture is about the colour of her skin, so a colour cast "
        "in one half and not the other would ruin it.\n\n"

        # 11 — the woman
        f"She is {w['who']}. She wears no makeup at all on either day - no foundation, no concealer, "
        "no powder, nothing that could even out her skin - her brows are natural and unshaped, and her "
        "hair is unstyled. She is an ordinary person, not a model, and neither picture makes any "
        "attempt to flatter her.\n\n"

        # 12 — age. Stated positively as well as bounded: round 1 drifted a decade older on two
        # of five engines despite the negative list, and a woman in her sixties changes what the
        # picture is claiming.
        "SHE IS BETWEEN FORTY-FIVE AND FIFTY-FIVE - MIDDLE-AGED, CLEARLY NOT YET SIXTY - AND THAT "
        "GOVERNS WHAT HER SKIN CAN HONESTLY LOOK LIKE. Her expression lines are well established and "
        "stay put with her face at rest, and some grey at the parting and temples is right and "
        "expected. But she is NOT elderly and must not read as elderly: her jaw is still defined, her "
        "neck is still firm, and she has none of the deep folds, heavy jowls or crepe-textured skin of "
        "a woman in her sixties or seventies.\n\n"

        # 13 — lighting (the inversion)
        "THE LIGHT ON BOTH DAYS IS BRIGHT, SOFT AND BROAD, AND IT COMES FROM ROUGHLY IN FRONT OF HER. "
        "This matters more than anything else about the lighting and it is the opposite of what a "
        "picture about wrinkles would want: hard light raking across a cheek lays down a gradient of "
        "shadow, and a gradient of shadow looks exactly like a patch of uneven colour, so it would "
        "invent the very thing this picture exists to show. Soft frontal daylight from a window lights "
        "the skin evenly and lets its actual colour be seen. Bright, clean, well exposed, no dark room, "
        "no heavy shadow across the face, no flash. The direction and warmth of the daylight differ a "
        "little between the two days, but the brightness, the softness and the exposure do not.\n\n"

        # 14 — skin realism, tone-page version
        "THE SKIN MUST HOLD UP AS REAL AND UNFLATTERED. Pores are clearly visible and vary in size and "
        "density by zone - open across the nose and inner cheeks, finer at the temples and jaw - "
        "several individually larger than their neighbours. Fine vellus hairs catch the light along the "
        "jaw. Fine expression lines are present at the outer corners of the eyes. The skin is a little "
        "greasy across the nose and drier at the outer cheeks. Real skin, photographed honestly, with "
        "no smoothing of any kind.\n\n"

        # 15 — the left panel
        f"ON THE EARLIER DAY, IN THE LEFT PANEL, THE UNEVENNESS OF HER SKIN IS THE SUBJECT OF THE "
        f"PICTURE. {w['before']}\n\n"

        # 16 — the right panel: what changed
        "ON THE LATER DAY, IN THE RIGHT PANEL, HER SKIN TONE IS MORE EVEN. " + MAGNITUDE[w["block"]] +
        "\n\n"

        # 17 — the honesty clause restated AT THE POINT OF CHANGE. It is already the third
        # paragraph; it is repeated here because round 1 proved that describing the improvement
        # is exactly the moment an engine reaches for its own idea of what improvement means.
        "AND AT THE SAME TIME, IN THAT SAME RIGHT PANEL: EVERY MOLE, EVERY FRECKLE AND EVERY DISTINCT "
        "SUN SPOT IS STILL THERE, in the same place and the same number, and not one has been removed "
        "or faded away. Count them in the left panel and they are all still countable in the right. "
        "They may sit a little less harshly against the calmer skin around them, but they are all "
        "plainly visible. Her complexion is the same complexion and she is not a paler person. Her "
        "expression lines are the same lines in the same places. She has not been made younger, "
        "slimmer, prettier or better groomed, and she is wearing no makeup in either panel. And both "
        "halves of the picture still match each other exactly for colour balance and brightness.\n\n"

        # 18 — the floor
        "THERE MUST BE A VISIBLE DIFFERENCE BETWEEN THE TWO PANELS. This is the entire purpose of the "
        "pair. Someone comparing them must be able to see that her skin tone is more even in the later "
        "one and point to which areas. Two panels that look the same are a complete failure.\n\n"

        "A snapshot off a phone, not a photograph - honest, unretouched, and completely unfiltered."
    )


def build_prompt_luma(w: dict) -> str:
    """Luma's short brief. Under 6,000 characters or it returns a bare HTTP 422.

    Luma also drops the negative list entirely (it has no negative field and folding one into
    the body has tripped its content filter before), so everything load-bearing has to be said
    positively here. What is cut is the reasoning, never a constraint.
    """
    crop = CROPS[w["crop"]]
    r1, r2 = ROOMS[w["rooms"][0]], ROOMS[w["rooms"][1]]
    kind = "phone selfies" if crop["selfie"] else "close photographs"
    return (
        f"Two ordinary {kind} of THE SAME WOMAN taken weeks apart at home, side by side filling one "
        "square frame: two panels of exactly equal width meeting at one crisp vertical edge at the "
        "centre. Left panel earlier, right panel later. Flat unposed expression both days, mouth "
        "closed, not smiling.\n\n"
        "THREE THINGS THAT MUST BE TRUE OF THE RIGHT PANEL, BEFORE ANYTHING ELSE. ONE: every mole, "
        "every freckle and every distinct sun spot she has is still there, in the same place and the "
        "same number, all still plainly visible and countable. This is not a picture about removing "
        "spots - what evens out is the soft, diffuse, blotchy mottling BETWEEN and AROUND them. TWO: "
        "she is not a paler person. Her complexion is the same complexion, and the skin between the "
        "patches, under her jaw and on her neck is exactly the same colour in both panels - no "
        "lightening, no bleaching, nothing chalky or grey. THREE: the two halves match each other for "
        "colour and brightness, with no warm cast on one side and cool on the other, because this "
        "picture is about the colour of her skin and a tinted half would ruin it.\n\n"
        "Two separate occasions, not two copies of one frame. Same face, jawline, nose, eye colour, "
        "brow shape, hair colour and cut, and the same moles and freckles in the same places.\n\n"
        f"Different rooms: earlier, {r1[0]} with {r1[2]} far out of focus at one edge, {r1[1]}. Later, "
        f"{r2[0]} with {r2[2]} out of focus at one edge, {r2[1]}. Bare painted walls otherwise.\n\n"
        "Her head is held differently and her eyes look somewhere different on the two days - turned a "
        "few degrees one way and tipped slightly down with her eyes on the camera in one, a few degrees "
        "the other way and tipped slightly up with her eyes just off the camera in the other. A small "
        "difference, but unmistakable. Different garment and different hair fall too.\n\n"
        "Nothing of whoever held the camera is in shot: no hand, no fingers, no arm, no phone, no "
        "mirror, no reflection.\n\n"
        + crop["text"] + "\n\n"
        "An amateur picture off a phone - not eye level, a few degrees crooked, imperfect focus, a "
        "little shadow noise. But both panels are cleanly exposed and neutral in colour, with no warm "
        "or cool cast in either, because this picture is about the colour of her skin.\n\n"
        f"She is {w['who']}. No makeup at all on either day, natural unshaped brows, unstyled hair. An "
        "ordinary person, not a model. Forty-five to fifty-five, middle-aged and clearly not yet "
        "sixty: established expression lines and some grey at the parting, but a still-defined jaw and "
        "a firm neck, and none of the deep folds or jowls of a woman in her sixties.\n\n"
        "Bright, soft, broad daylight from roughly in front of her on both days, so her skin is lit "
        "evenly and its actual colour can be seen. No hard raking light, no heavy shadow across the "
        "cheek, no flash. Direction and warmth differ a little between the days; brightness and "
        "exposure do not.\n\n"
        "Real unflattered skin: visible pores varying by zone, vellus hair along the jaw, fine lines at "
        "the outer eye corners, slightly greasy at the nose. No smoothing.\n\n"
        f"IN THE LEFT PANEL the unevenness of her skin is the subject. {w['before']}\n\n"
        "IN THE RIGHT PANEL her skin tone is more even. " + MAGNITUDE[w["block"]] + "\n\n"
        # Shorter than the main brief's restatement on purpose: the three rules are already at the
        # top of this version and Luma's 6,000-character cap leaves no room to say them twice at
        # length. Every constraint is still named.
        "And in that same right panel all three rules above still hold: every mole and freckle still "
        "there and countable, the same complexion, and the two halves still matching for colour and "
        "brightness. Same expression lines in the same places, not younger or prettier, no makeup.\n\n"
        "There must be a visible difference between the panels - two panels that look the same are a "
        "complete failure. Honest, unretouched, unfiltered."
    )


NEGATIVE_GLOBAL = (
    # Text — the whole label system depends on there being none in the pixels.
    "no text, no lettering of any kind, no words, no letters, no numbers, no percentages, no captions, "
    "no labels, no watermark, no printed text overlay, no logo, no signature, no timestamp, no date "
    "stamp, "
    # Product and props.
    "no bottle, no jar, no dropper, no packaging, no product, no botanicals, no jewellery, no "
    "spectacles, "
    # Makeup — anything that could evens tone by itself destroys the comparison.
    "no makeup, no foundation, no powder, no concealer, no colour correcting makeup, no tinted "
    "moisturiser, no eyeliner, no mascara, no false lashes, no eyeshadow, no lipstick, no glitter, "
    # Filtered skin.
    "no beauty-filter smoothing, no frequency separation, no airbrushed skin, no plastic skin, no waxy "
    "skin, no porcelain skin, no uniform skin texture, no repeating texture pattern, no retouching, no "
    "skin smoothing filter, no snapchat filter, no instagram filter, "
    # Medical / cosmetic territory this is not.
    "no wound, no bruise, no rash, no acne, no blood, no needle, no drawn lines on the skin, no painted "
    "marks, no dermatologist marker, "
    # Photographer's limbs and kit.
    "no hand, no fingers, no arm, no elbow, no phone, no smartphone, no selfie stick, no mirror, no "
    "reflection, "
    # Studio production values — this has to read as a real person at home.
    "no studio backdrop, no seamless paper, no professional lighting, no softbox, no beauty dish, no "
    "ring light circle in the eyes, no fashion photograph, no glamour, no styled hair, no salon "
    "blow-dry, no bokeh portrait mode, no model, no supermodel, "
    # Casting.
    "no elderly woman, no woman over fifty-five, no woman under forty, no heavy jowls, no sagging neck, "
    "no non-Caucasian model, "
    # Exposure. Note that dullness and sallowness are NOT negated here — they are the subject
    # of the left panel. Only genuine underexposure is.
    "no dark room, no dim room, no underexposed picture, no night, no darkness, no camera flash, no "
    "flash shadow on a wall, no orange tungsten glow, no colour cast, no blue cast, no orange cast, "
    # Places that keep turning up uninvited.
    "no car interior, no seatbelt, no tiled bathroom wall, no bathroom, no radiator, no towel rail, no "
    "fluorescent strip light, no neon tube, no garden, no outdoors, no bookcase, no shelves of books, "
    "no plant, no kitchen appliance, no washing machine, no patterned wall, no wallpaper, no "
    "photographs on the wall, no posters, no clutter, no busy background, "
    # The diptych form itself.
    "no three panels, no four panels, no grid of panels, no picture frame, no border, no vignette, no "
    "gap between panels, no white gutter between panels, no slider handle, no drag handle"
)

NEGATIVE_EXTRA = (
    # The pair.
    "no identical backgrounds between the panels, no same room in both panels, no different woman "
    "between the panels, no zero difference between the panels, no identical head angle between the "
    "panels, no identical gaze between the panels, no identical framing between the panels, "
    # The honesty line. Note what is NOT here: "no lighter skin in the right panel" would
    # contradict the finding, so the constraint is carried positively in the prompt body and
    # only the dishonest extremes are banned.
    "no skin whitening, no bleached skin, no chalky white skin, no grey pallor, no different ethnicity "
    "between the panels, no different skin colour between the panels on the neck or jaw, "
    "no mole disappearing between the panels, no freckle disappearing between the panels, "
    "no younger woman in the right panel, no makeup appearing in the right panel, "
    # Lighting — the inversion.
    "no hard raking sidelight, no strong shadow gradient across the cheek, no shadow mistaken for "
    "pigment, no different exposure between the panels, "
    # Pose.
    "no smiling, no teeth, no tongue"
)


def main() -> None:
    slots = []
    for w in WOMEN:
        prompt = build_prompt(w)
        prompt_luma = build_prompt_luma(w)
        assert len(prompt_luma) < LUMA_CAP, (
            f"{w['block']}-{w['key']}: luma prompt is {len(prompt_luma)} chars, cap is {LUMA_CAP}")
        study = "watanabe-2014" if w["block"] == "f1" else "khanna-2025"
        slots.append({
            "id": f"glu8--{w['block']}-{study}-{w['key']}",
            "title": (f"{w['block']} · {study} · {w['crop']} crop — "
                      f"{w['who'].split(',')[0].replace('a white ', '')}"),
            "class": "B",
            "width": 2048,
            "height": 2048,
            "target_slot": f"/pages/glutathione-research key_findings {w['block']}",
            "ref_files": [],
            "prompt": prompt,
            "prompt_luma": prompt_luma,
            "label": {
                "left": "Before",
                "right": "After 10 weeks" if w["block"] == "f1" else "After",
                "figure": "",
                "measure": "(labels are theme settings, never pixels)",
                "cite": study,
            },
            "negative_extra": NEGATIVE_EXTRA,
        })

    cfg = {
        "wave": WAVE,
        "created": "2026-08-27",
        "doc": ("docs/clinical-trial-before-after-images.md, .claude/rules/website-imagery.md, "
                "built by scripts/build-glutathione-before-after-config.py"),
        "note": (
            "BEFORE/AFTER DIPTYCHS FOR THE TWO CLINICAL BLOCKS ON /pages/glutathione-research - f1 "
            "(Watanabe 2014, 2% GSSG, 10 weeks) and f3 (Khanna 2025 systematic review). Both blocks "
            "currently carry unrelated placeholder photographs: f1 a laboratory shot, f3 the "
            "philosophy-research image.\n\n"
            "MALCOLM, 2026-08-27: amateur, normal-looking Caucasian women aged 45-55; different "
            "backgrounds AND lighting; and slightly different head position and eye gaze, so the "
            "before and after are clearly, subtly, different photographs. Crop varies across the "
            "batch - two full face, two face-filling, two half face, two very close on one cheek.\n\n"
            "INHERITED FROM THE FIFTEEN ACETYL WAVES (docs/clinical-trial-before-after-images.md): "
            "two sessions rather than two frames; one prompt per slot so no two pairs share a room "
            "pair; nine-to-eight slots at candidates 1; the identity lock; the visible-improvement "
            "floor; no hand or phone in frame; and NO BAKED-IN TEXT, because Translate & Adapt "
            "reaches theme JSON but cannot touch pixels.\n\n"
            "THREE THINGS ARE DELIBERATELY INVERTED BECAUSE THIS PAGE MEASURES TONE, NOT LINE DEPTH.\n"
            "(1) LIGHTING. The acetyl brief demanded raking sidelight so every line cast its own "
            "shadow. That is actively wrong here: a shadow gradient across a cheek is "
            "indistinguishable from a patch of uneven pigment, so raking light would manufacture in "
            "the left panel the thing the right panel is meant to have improved. Bright, soft, broad "
            "frontal daylight instead.\n"
            "(2) WHITE BALANCE. 'Indoor white balance a little wrong' was one of the best amateur "
            "tells on the acetyl page and cannot survive on a page about colour - a warm cast in one "
            "panel and a cool one in the other is a tone difference the product did not cause. Both "
            "panels are briefed as cleanly exposed and neutral; the amateur read is bought with "
            "crooked framing, an off-eye-level angle, soft focus and shadow noise.\n"
            "(3) THE MARKS. Moles and freckles are this store's standard defence against plastic AI "
            "skin, and on a brightening page they illustrate the concern rather than the result (see "
            "the project memory entry realism-marks-become-the-problem-on-a-pigmentation-page). The "
            "fix is to split them: DIFFUSE mottling is the deliberate subject of the left panel and "
            "is what evens out; DISCRETE moles and freckles are identity anchors and may not "
            "disappear. Slot d casts a densely freckled Irish woman on purpose - it is the sharpest "
            "test of that line in the batch.\n\n"
            "THE HONESTY CLAUSE IS RE-CUT AND THIS IS THE MOST IMPORTANT PARAGRAPH IN THE BRIEF. The "
            "acetyl wave simply negated 'no lighter skin in the right panel'. That cannot stand when "
            "the trial's own endpoint is a reduced melanin index. So the line moves: the PATCHES "
            "converge toward her own surrounding tone, while her baseline complexion - the skin "
            "between the patches, under the jaw, down the neck - is identical in both panels, and "
            "every mole and freckle is still there and countable. She is not a paler person. It is "
            "stated positively in the prompt body because a ban that contradicts the brief is the "
            "hardest kind of instruction to notice; only the dishonest extremes (whitening, "
            "bleaching, chalky or grey skin, a changed ethnicity) are negated.\n\n"
            "MAGNITUDE DIFFERS BY BLOCK AND f3 IS CAPPED. f1 is a single randomised split-face trial "
            "with p < 0.001 on the melanin index over ten weeks, so a clearly visible evening is "
            "defensible. f3 is a POOLED SYSTEMATIC REVIEW with no percentage attached - an emphatic "
            "before/after there would be the same class of overstatement that the acetyl f3 cap "
            "exists to prevent, so its change is briefed as real but modest, requiring a careful "
            "comparison to see and rewarding one.\n\n"
            "TWO THINGS FOR MALCOLM. First, Watanabe 2014 was a SPLIT-FACE trial - one face, treated "
            "side against placebo side - and these diptychs read as week 0 against week 10. That is "
            "how the paper reports each side against its own baseline and it is the form the section "
            "labels support, but it is an illustration of the trial, not a depiction of it. Second, "
            "f3 illustrates a REVIEW rather than a trial, which is a weaker fit for a before/after "
            "than a single study is; the alternative would be a non-photographic block there.\n\n"
            "WHAT ROUND 1 BOUGHT. r1 was a ONE-SLOT SMOKE TEST across all five suppliers before "
            "spending on the other seven, and all five returned. Output is preserved at "
            "assets/ai-generated/2026-08-22-multi-block-glutathione-research-before-after-r1 and the "
            "brief at configs/banners/block-glutathione-research-before-after-r1.json. Four faults, "
            "three systematic:\n"
            "(a) THE FRECKLES DISAPPEARED. gpt_image, nbp_flash and seedream all cleared the discrete "
            "freckles and sun spots out of the right panel rather than only the diffuse mottling. The "
            "rule was already in the brief, explicitly, and lost anyway because it sat in the "
            "seventeenth paragraph and the engine's own prior - brightening means removing spots - got "
            "there first. It is now the THIRD paragraph, ahead of the rooms and the crop, and is "
            "restated inside the right-panel paragraph. Position was the fault, not wording.\n"
            "(b) THE HALVES CARRIED DIFFERENT COLOUR CASTS. seedream and luma both went warm on the "
            "left and cool on the right. `no colour cast` in the negative list did not hold it, and on "
            "a page about the colour of skin this is the most damaging fault available - it hands a "
            "viewer a reason to say the difference was the light. Now framed as a MATCHING requirement "
            "between the halves rather than a property of each, with the failure named.\n"
            "(c) f1's MAGNITUDE OVERSHOT. seedream's right panel had cleared the patch almost "
            "entirely; 'much closer in colour' was read as 'gone'. f1 now carries a ceiling as well as "
            "a floor: the same patches must still be findable in the same places, one for one.\n"
            "(d) flux2 did exactly what the project memory predicts - one room in both panels, the "
            "same head angle and gaze, no visible difference at all, and a woman reading mid-sixties. "
            "It stays in the run under rule 1 of website-imagery.md, but it is the first place to "
            "check identity and age. The age band is now stated positively as well as negated.\n\n"
            "SUPPLIERS: nbp_pro excluded on evidence (seven waves of invented burnt-in captions in "
            "this brief family). flux2 is the engine that has drifted onto a different, older woman "
            "in the right panel before - check identity there first. Luma gets its own shorter "
            "prompt_luma under its 6,000-character cap, and it drops the negative list entirely, so "
            "everything load-bearing is stated positively in that version too. CLASS B, no reference "
            "images, 2048x2048 square - media-with-text and research-before-after both take the row "
            "height from the master's own aspect, and the labels are placed at the 50% split."
        ),
        "target_template": "templates/page.glutathione-research.json",
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
        print(f"  {s['id']:<40} prompt {len(s['prompt']):>5}  luma {len(s['prompt_luma']):>5}")
    print(f"  negative_global {len(NEGATIVE_GLOBAL)} + negative_extra {len(NEGATIVE_EXTRA)} chars")


if __name__ == "__main__":
    main()
