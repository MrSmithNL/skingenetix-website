#!/usr/bin/env python3
"""Build the twelve copper-peptide before/after waves: 3 shot types x 4 concerns x 8 women.

    python3 scripts/build-copper-peptide-before-after-configs.py
    python3 scripts/build-copper-peptide-before-after-configs.py --list

Writes twelve configs to configs/banners/block-copper-peptide-ba-<concern>-<shot>.json,
eight slots each, one candidate per slot per supplier. Run them with:

    set -a; source ~/.claude/config/image-credentials.env; set +a
    python3 scripts/generate-multi.py configs/banners/<wave>.json \
        --suppliers seedream,gpt_image,nbp_flash --candidates 1

⚠️ `--candidates 1` IS NOT OPTIONAL. generate-multi.py reads `args.candidates` and NEVER
reads `defaults.candidates` from the config, so the config's own "candidates": 1 is
decorative. The flag defaults to 2, which doubles a 96-slot run from about $8.60 to about
$17.20 without saying so.

WHY THIS EXISTS
Malcolm, 2026-08-27: a new batch of before/after pairs for the copper-peptide clinical
research, in three shot types across four concerns, eight amateur women each. The brief is
the fifteen-wave skeleton in docs/clinical-trial-before-after-images.md with ONE structural
change, which is the reason he asked for the round:

    "the position, pose, distance from camera and head position were too similar - so it
     looked like the image was a duplicate."

THE CAUSE, AND IT IS NOT A WORDING FAULT
The acetyl skeleton's step 8 pins the framing IDENTICALLY in both panels - "the phone is
held right up close and her face completely fills the panel, the frame cuts across her
forehead just below the hairline and at the point of her chin". That paragraph is applied to
the earlier day AND the later day. Every other axis was already briefed to vary - room, wall
colour, light direction, garment, hair - but head size and head position in frame are what
most say "same photograph", and they were the two things held constant. The glutathione r2
builder added a head-and-gaze paragraph on 2026-08-27, but hedged it: "the difference is
small - she is recognisably in the same kind of pose both times". That hedge is what is
removed here.

So VIEWPOINTS is new, it is per slot, and it is stated per panel: camera height, camera
tilt, head turn, head tip, gaze, distance and where her head sits in the frame, all named
separately for the earlier and the later day.

⚠️ THE TRAP IN DOING THAT, AND THE GUARD
If the later panel is further away or softer, the lines look shallower BECAUSE OF THE
DISTANCE, and the pair stops being evidence of anything. The naive fix - always put the
later panel closer - is worse, because across 96 images "the after is always the close one"
becomes its own visible tell. So distance varies in BOTH directions, bounded so the region
of interest stays fully resolved in both panels, and paragraph 19 states outright that the
change may not be attributable to distance, softness or blur.

FOUR CONCERNS, AND ONE OF THEM INVERTS THE LIGHTING
Per docs/clinical-trial-before-after-images.md §10, a pair about TONE needs the opposite
lighting from a pair about LINE DEPTH:

  - fine lines, firming, repair -> RAKING SIDELIGHT, so every line casts its own shadow.
  - brightening -> SOFT BROAD FRONTAL LIGHT. Raking light lays a shadow gradient across a
    cheek, and a shadow gradient is indistinguishable from a patch of pigment, so it invents
    the very fault the picture exists to show.

Brightening also drops the "indoor white balance a little wrong" camera tell and requires
the two halves to MATCH for colour and brightness. This partially overrides Malcolm's
"different lighting for each before and after": on the brightening batch the light DIRECTION
still differs between the days, but colour temperature and exposure may not, or the
comparison is corrupted. Flagged to him 2026-08-27.

ONE CELL OF THE TWELVE DOES NOT WORK AS ASKED
Firmness is contour - jaw, cheek, the line under the chin. A cheek macro has no contour in
it, so "firming x macro" cannot show its own subject. That cell uses a JAWLINE-AND-NECK
close crop instead of a cheek macro, which is the tightest framing that can still carry the
finding. Named honestly rather than quietly substituted.

THIRTY-TWO WOMEN, NOT NINETY-SIX
Eight per concern, each photographed in all three shot types. Within any one batch the eight
are all different, which is what Malcolm asked for. Thirty-two richly written castings beat
ninety-six thin ones - the specificity of the `who` and `before` strings is what stops an
engine reaching for its own idea of a middle-aged woman, and that specificity does not
survive being spread ninety-six ways. Overrule by setting UNIQUE_PER_SHOT = True.

AGE BAND IS 40-60 THIS ROUND, UP FROM 45-55, and the negative list is corrected to match.
`no woman over fifty-five` sat in every previous config; left alone it would have fought the
casting on all 96 slots. A stale negative is the hardest kind to notice, because nobody
reads the negative list when the prompt looks right.

SUPPLIERS: seedream, gpt_image, nbp_flash. nbp_pro is excluded on seven waves of invented
captions; flux2 went 0/8 on the glutathione before/after family and fabricates a stock-photo
watermark; luma answers this brief family with a bare HTTP 422. That is an evidence-based
exclusion of three backends, not a shortcut around rule 1 of .claude/rules/website-imagery.md.

Author: Claude Code, 2026-08-27.
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "configs" / "banners"

UNIQUE_PER_SHOT = False   # see docstring, "THIRTY-TWO WOMEN"
SIZE = 2048               # square: media-with-text takes its row height from the master

# --------------------------------------------------------------------------------------
# Rooms. Twenty-four, so that no batch repeats a room and no pair shares a room with the
# other pair in its own batch. Each is a wall colour + a light direction + ONE soft
# unidentifiable element, because a bare wall left nothing for the model to place at the
# edge and nbp_flash supplied a phone instead (acetyl wave 15).
#
# The light direction here is deliberately written WITHOUT a side bias, because the concern
# supplies the lighting character: a wrinkle pair rakes the light across her, a tone pair
# puts it broad and in front. Only the ORIGIN differs per room.
# --------------------------------------------------------------------------------------
ROOMS = [
    ("a WARM WHITE wall", "from a window to her left", "the soft vertical edge of a doorframe"),
    ("a PALE GREY wall", "from a window to her right", "the faint corner where two walls meet"),
    ("a SOFT BEIGE wall", "from a window high on her left", "the blurred top of a chair back"),
    ("an OFF-WHITE wall", "from a window low on her right", "a pale picture frame with nothing readable in it"),
    ("a PALE GREIGE wall", "from a window behind and to her left", "the shape of a lampshade that is switched off"),
    ("a MUTED SAGE-GREY wall", "from a window to her right and slightly above", "the vertical fall of a plain curtain"),
    ("a SOFT TAUPE wall", "from a window to her left and slightly below", "the pale line of a skirting board meeting the floor"),
    ("a PLAIN CREAM wall", "from a wide window to her right", "the soft dark shape of a coat on a hook"),
    ("a PALE BLUE-GREY wall", "from a window high on her right", "the faint horizontal line of an empty shelf"),
    ("a CHALK WHITE wall", "from a tall window to her left", "the soft upright of a door architrave"),
    ("a PALE OATMEAL wall", "from a window to her left and above", "the blurred edge of a door standing open"),
    ("a LIGHT STONE-GREY wall", "from a window to her right and below", "the soft pale line where the wall meets the ceiling"),
    ("a SOFT CLAY-PINK wall", "from a window to her left", "the out-of-focus back of a dining chair"),
    ("a WARM IVORY wall", "from a wide window to her right", "the soft dark line of a picture rail"),
    ("a PALE PUTTY wall", "from a window high on her left", "the blurred vertical edge of a wardrobe"),
    ("a COOL LINEN-WHITE wall", "from a window to her right", "the soft fall of a plain window blind"),
    ("a SOFT MUSHROOM wall", "from a window low on her left", "the blurred upright of a radiator pipe"),
    ("a PALE SAND wall", "from a window to her right and above", "the soft edge of a plain roller blind"),
    ("a DUSTY LILAC-GREY wall", "from a window to her left and above", "the faint vertical seam of two wallpaper drops"),
    ("a BONE WHITE wall", "from a wide window to her left", "the blurred corner of a plain mirror frame"),
    ("a PALE MOSS-GREY wall", "from a window to her right", "the soft dark edge of an open doorway"),
    ("a WARM PLASTER wall", "from a window high on her right", "the out-of-focus line of a curtain pole end"),
    ("a COOL PEBBLE-GREY wall", "from a window to her left and below", "the blurred top corner of a chest of drawers"),
    ("a SOFT ALMOND wall", "from a window to her right and slightly below", "the faint soft edge of a hanging towel"),
]

# --------------------------------------------------------------------------------------
# VIEWPOINTS — the reason this round exists.
#
# Twelve pairs. Each pair is two genuinely different vantage points on the same woman:
# camera height, camera tilt, degree of head turn, distance and position in frame all differ
# between the earlier and the later day.
#
# ⚠️ `side` IS THE CONSTRAINT THAT MAKES THE PAIR COMPARABLE, and it was missing from the
# first version of this file. Malcolm, 2026-08-27:
#
#     "it should always be showing the same part of the face - so if showing the front then
#      it should be the front, if showing the left side then show the left side of the face
#      in the before and after. Not before: left side of face and After: right side."
#
# The first version turned her head in OPPOSITE directions between the panels on eight of the
# twelve pairs, which presents her left cheek in one panel and her right cheek in the other.
# Those are two different areas of skin with different lines, different pigmentation and
# different moles on them, so there is nothing to compare and the pair proves nothing - it is
# the same class of fault as the panels being two different women. The turn now always runs
# the SAME WAY within a pair and only its DEGREE changes.
#
# Four pairs present the front, four her left cheek, four her right cheek.
#
# `dist` is a RELATIVE nudge inside the shot type, never a change of shot type: a macro that
# steps back is still a macro. Six pairs are closer on the later day and six on the earlier
# day, so "the after is the close one" never becomes a pattern across the 96.
# --------------------------------------------------------------------------------------
VIEWPOINTS = [
    # ---- FRONT: she faces the camera in both panels ------------------------------------
    dict(side=("SHE IS FACING THE CAMERA MORE OR LESS SQUARE ON IN BOTH PANELS - the FRONT of her "
               "face is what the camera sees on both days"),
         a=dict(cam="held low, clearly below her eye line and tilted up towards her",
                turn="her head square to the camera and tipped a little down",
                dist="framed a little further back", place="her head sits low and left of centre"),
         b=dict(cam="held above her eye line and tilted down towards her",
                turn="her head still square to the camera but tipped a little up",
                dist="framed noticeably closer in", place="her head sits high and right of centre")),

    dict(side=("SHE IS FACING THE CAMERA MORE OR LESS SQUARE ON IN BOTH PANELS - the FRONT of her "
               "face is what the camera sees on both days"),
         a=dict(cam="held high, well above her eye line, looking down onto her",
                turn="her head square to the camera and tipped up towards it",
                dist="framed noticeably closer in", place="her head sits high and slightly right of centre"),
         b=dict(cam="held at about chest height and tilted up towards her",
                turn="her head square to the camera and level",
                dist="framed further back", place="her head sits centred but low")),

    dict(side=("SHE IS FACING THE CAMERA MORE OR LESS SQUARE ON IN BOTH PANELS - the FRONT of her "
               "face is what the camera sees on both days"),
         a=dict(cam="held at eye line, directly in front of her",
                turn="her head square to the camera, level",
                dist="framed closer in", place="her head sits centred"),
         b=dict(cam="held below her chin and tilted steeply up",
                turn="her head square to the camera and tipped back a little",
                dist="framed further back", place="her head sits low and centred")),

    dict(side=("SHE IS FACING THE CAMERA MORE OR LESS SQUARE ON IN BOTH PANELS - the FRONT of her "
               "face is what the camera sees on both days"),
         a=dict(cam="held just below eye line and tilted up slightly",
                turn="her head square to the camera and tipped very slightly down",
                dist="framed further back", place="her head sits centred and a little high"),
         b=dict(cam="held well above her and angled steeply down",
                turn="her head square to the camera and tipped up to meet it",
                dist="framed closer in", place="her head sits low and right of centre")),

    # ---- HER LEFT CHEEK: head turned to HER OWN RIGHT in both panels --------------------
    dict(side=("THE SAME SIDE OF HER FACE IS TOWARDS THE CAMERA IN BOTH PANELS: HER LEFT CHEEK. On "
               "both days her head is turned towards her own RIGHT, so the camera sees the LEFT side "
               "of her face. It is never the right side in one panel and the left in the other"),
         a=dict(cam="held at eye line and off to her left",
                turn="her head turned about twenty degrees to her own right, level",
                dist="framed further back", place="her head sits right of centre"),
         b=dict(cam="held above her eye line and off to her left, tilted down",
                turn="her head turned about thirty-five degrees to her own right and tipped slightly up",
                dist="framed closer in", place="her head sits high and centred")),

    dict(side=("THE SAME SIDE OF HER FACE IS TOWARDS THE CAMERA IN BOTH PANELS: HER LEFT CHEEK. On "
               "both days her head is turned towards her own RIGHT, so the camera sees the LEFT side "
               "of her face. It is never the right side in one panel and the left in the other"),
         a=dict(cam="held high and off to her left, angled down across her face",
                turn="her head turned about thirty degrees to her own right and tipped down",
                dist="framed closer in", place="her head sits high and left of centre"),
         b=dict(cam="held low and off to her left, angled up along her jaw",
                turn="her head turned about twenty degrees to her own right and tipped back",
                dist="framed further back", place="her head sits low and centred")),

    dict(side=("THE SAME SIDE OF HER FACE IS TOWARDS THE CAMERA IN BOTH PANELS: HER LEFT CHEEK. On "
               "both days her head is turned towards her own RIGHT, so the camera sees the LEFT side "
               "of her face. It is never the right side in one panel and the left in the other"),
         a=dict(cam="held at eye line, well out to her left so the view is clearly three-quarter",
                turn="her head turned about thirty-five degrees to her own right",
                dist="framed further back", place="her head sits centred"),
         b=dict(cam="held just below eye line and closer to her left shoulder",
                turn="her head turned about twenty-five degrees to her own right and tipped a little down",
                dist="framed closer in", place="her head sits high and right of centre")),

    dict(side=("THE SAME SIDE OF HER FACE IS TOWARDS THE CAMERA IN BOTH PANELS: HER LEFT CHEEK. On "
               "both days her head is turned towards her own RIGHT, so the camera sees the LEFT side "
               "of her face. It is never the right side in one panel and the left in the other"),
         a=dict(cam="held low and well out to her left, tilted up",
                turn="her head turned about twenty-five degrees to her own right and tipped up",
                dist="framed closer in", place="her head sits low and left of centre"),
         b=dict(cam="held at eye line and further out to her left",
                turn="her head turned about forty degrees to her own right, level",
                dist="framed further back", place="her head sits centred and high")),

    # ---- HER RIGHT CHEEK: head turned to HER OWN LEFT in both panels --------------------
    dict(side=("THE SAME SIDE OF HER FACE IS TOWARDS THE CAMERA IN BOTH PANELS: HER RIGHT CHEEK. On "
               "both days her head is turned towards her own LEFT, so the camera sees the RIGHT side "
               "of her face. It is never the left side in one panel and the right in the other"),
         a=dict(cam="held at eye line and off to her right",
                turn="her head turned about twenty degrees to her own left, level",
                dist="framed closer in", place="her head sits left of centre"),
         b=dict(cam="held high and off to her right, tilted down onto her cheekbone",
                turn="her head turned about thirty-five degrees to her own left and tipped down",
                dist="framed further back", place="her head sits low and centred")),

    dict(side=("THE SAME SIDE OF HER FACE IS TOWARDS THE CAMERA IN BOTH PANELS: HER RIGHT CHEEK. On "
               "both days her head is turned towards her own LEFT, so the camera sees the RIGHT side "
               "of her face. It is never the left side in one panel and the right in the other"),
         a=dict(cam="held low and close to her right shoulder, angled up",
                turn="her head turned about thirty degrees to her own left and tipped back a little",
                dist="framed further back", place="her head sits centred and low"),
         b=dict(cam="held at eye line, directly out to her right",
                turn="her head turned about twenty degrees to her own left, level",
                dist="framed closer in", place="her head sits high and left of centre")),

    dict(side=("THE SAME SIDE OF HER FACE IS TOWARDS THE CAMERA IN BOTH PANELS: HER RIGHT CHEEK. On "
               "both days her head is turned towards her own LEFT, so the camera sees the RIGHT side "
               "of her face. It is never the left side in one panel and the right in the other"),
         a=dict(cam="held above her eye line and out to her right, angled down",
                turn="her head turned about forty degrees to her own left and tipped down",
                dist="framed closer in", place="her head sits high and right of centre"),
         b=dict(cam="held just below eye line and out to her right",
                turn="her head turned about twenty-five degrees to her own left and tipped up slightly",
                dist="framed further back", place="her head sits centred")),

    dict(side=("THE SAME SIDE OF HER FACE IS TOWARDS THE CAMERA IN BOTH PANELS: HER RIGHT CHEEK. On "
               "both days her head is turned towards her own LEFT, so the camera sees the RIGHT side "
               "of her face. It is never the left side in one panel and the right in the other"),
         a=dict(cam="held at eye line, well out to her right so the view is clearly three-quarter",
                turn="her head turned about thirty-five degrees to her own left",
                dist="framed further back", place="her head sits low and right of centre"),
         b=dict(cam="held low and nearer to her, angled up along her jaw",
                turn="her head turned about twenty-five degrees to her own left and tipped back",
                dist="framed closer in", place="her head sits high and centred")),
]

# --------------------------------------------------------------------------------------
# Gaze. Malcolm, 2026-08-27: "eye gaze should be subtly different on all, and noticeably
# different on 30% of them."
#
# Kept as its own axis rather than folded into VIEWPOINTS, because the head turn is now
# locked to one side within a pair and the gaze is the one thing left that can move freely
# without changing which part of her face is being compared. She can look anywhere while her
# head stays where it is.
#
# Roughly three slots in every ten get the NOTICEABLE pair; the rest get the SUBTLE pair.
# --------------------------------------------------------------------------------------
GAZE_SUBTLE = [
    ("her eyes are on the lens", "her eyes are very slightly off the lens, a fraction to one side"),
    ("her eyes are a fraction above the lens", "her eyes are on the lens"),
    ("her eyes are just off the lens to one side", "her eyes are just off the lens to the other side"),
    ("her eyes are on the lens", "her eyes are a fraction below the lens"),
]

GAZE_NOTICEABLE = [
    ("her eyes are straight down the lens", "her eyes are well away from the lens, off to one side and "
     "clearly not looking at the camera at all"),
    ("her eyes are turned right away from the camera, looking off to the side",
     "her eyes are straight down the lens"),
    ("her eyes are lowered, looking down and away from the lens",
     "her eyes are up and level, straight at the lens"),
    ("her eyes are on the lens", "her eyes are raised well above it, looking up and away"),
]

# --------------------------------------------------------------------------------------
# Shot types. Malcolm's three, mapped onto the crops the glutathione build proved out.
#
# `selfie` is False on `macro` and `half` and that is not fussiness: nobody can hold a phone
# close enough for a cheek macro and still have it in focus, so briefing "selfie" there asks
# for something that cannot happen and invites a hand or a phone back into frame. It is also
# the fix for the failure recorded in docs/clinical-trial-before-after-images.md §10, where a
# cheek macro was pulled back to a half-face portrait by all five engines - the engines were
# resolving a contradiction, not disobeying.
#
# The crop text says what the shot IS and what must stay readable. It deliberately does NOT
# pin the exact head size, because the viewpoint supplies the per-panel distance. That
# division of labour is the whole point of this round.
# --------------------------------------------------------------------------------------
SHOTS = {
    "macro": dict(
        selfie=False,
        label="very close - skin only",
        text=(
            "THIS IS A VERY CLOSE PICTURE OF HER SKIN AND SKIN IS ALMOST THE ENTIRE FRAME. The panel is "
            "filled by the area from just beneath the lower lashes at the top, across the whole cheekbone "
            "and cheek, in to the side of the nose at one edge and down to the line of the jaw at the "
            "bottom. The outer corner of one eye and a few lower lashes are just inside the top of the "
            "frame so it is unmistakably a face and not an abstract surface, but there is no whole face "
            "in view and no mouth. Pores, fine surface texture and the colour of the skin are what the "
            "picture is OF, and the picture is sharp enough across the cheekbone to read them. This is an "
            "ordinary close photograph taken at home in daylight - not a selfie, not a studio portrait, "
            "and not a medical or dermatological photograph."
        ),
    ),
    "half": dict(
        selfie=False,
        label="close - part of the face",
        text=(
            "ONLY PART OF HER FACE IS IN THE PANEL, AND IT FILLS IT. The frame is a vertical slice running "
            "from about the centre line of her nose outwards past her ear: one eye and its outer corner, "
            "one whole cheek and cheekbone, one temple, one eyebrow, one corner of her mouth and part of "
            "that side of her jaw. The other side of her face is outside the frame entirely and is not "
            "visible. That cheek is the largest thing in the picture. This is an ordinary close photograph "
            "taken at home in daylight, not a selfie and not a studio portrait."
        ),
    ),
    "close": dict(
        selfie=True,
        label="close - the whole face",
        text=(
            "HER WHOLE FACE IS IN THE PANEL AND FILLS IT. Her forehead, both eyes, her nose, her whole "
            "mouth and her jaw are all in view and all clearly readable at once, with her cheeks running "
            "close to both edges and only narrow slivers of the room showing past her. The frame sits "
            "roughly between the top of her forehead and just under her chin. There is very little space "
            "left around her face, and because the lens is close it distorts a little: her nose and chin "
            "read large and her forehead looms."
        ),
    ),
    # The substitution. See the docstring: a cheek macro has no contour in it, and firmness IS
    # contour, so this cell would otherwise be a picture that cannot show its own subject.
    "macro_jaw": dict(
        selfie=False,
        label="very close - jaw and neck",
        text=(
            "THIS IS A VERY CLOSE PICTURE OF THE LINE OF HER JAW AND THE SKIN BENEATH IT, AND SKIN IS "
            "ALMOST THE ENTIRE FRAME. The panel is filled by the area from the corner of her mouth and the "
            "lower cheek at the top, down along the whole edge of the jaw, under the chin, and onto the "
            "front of the upper neck at the bottom. Part of the mouth corner is just inside the frame so "
            "it is unmistakably a face and not an abstract surface, but there is no whole face in view and "
            "no eyes. THE EDGE OF THE JAW AGAINST THE NECK IS WHAT THE PICTURE IS OF - how cleanly that "
            "line is drawn, how the soft tissue sits along it and under the chin, and the texture and tone "
            "of the skin over it. This is an ordinary close photograph taken at home in daylight, not a "
            "selfie and not a studio portrait."
        ),
    ),
}


# --------------------------------------------------------------------------------------
# REGION BANDS. Added 2026-08-28 from seven real before/after pairs Malcolm supplied as
# reference. They are the single most useful thing anyone has handed this brief, because
# they show what the successful examples actually ARE, and it is not what this round has
# been generating.
#
# NONE of the seven is a head-and-shoulders portrait and none is a cheek macro. Every one is
# a HORIZONTAL ANATOMICAL BAND, framed frontally, cropped at features rather than at an
# arbitrary distance:
#
#   - brow to hairline, eyes just inside the bottom edge          (the two forehead pairs)
#   - under the nose to the collarbones                            (the lip/chin/neck pair)
#   - mid-forehead to the top lip                                  (the under-eye pairs)
#
# That is the same reason the jaw-and-neck crop was the one tight framing gpt_image honoured
# while every engine refused a cheek macro: a band bounded by FEATURES can be briefed, because
# the engine can find both edges on the face. "A very close picture of one cheek" gives it
# nothing to anchor to, so it falls back to the portrait it knows.
#
# These are frontal, so they are restricted to the four FRONT viewpoint pairs - a forehead
# band cannot survive a forty-degree head turn - and the camera still varies by height, tilt,
# distance and placement between the panels.
# --------------------------------------------------------------------------------------
SHOTS["forehead"] = dict(
    selfie=True,
    label="forehead band",
    text=(
        "THE PANEL IS A BAND ACROSS THE UPPER FACE AND THE FOREHEAD IS ALMOST ALL OF IT. The frame "
        "runs from her hairline at the top down to just below her eyes at the bottom, and out past "
        "both temples at the sides. Her eyebrows and both eyes are inside the bottom of the frame so "
        "it is unmistakably a face, but there is NO nose tip, NO mouth and NO chin in view at all - "
        "they are outside the frame entirely. THE HORIZONTAL LINES ACROSS HER FOREHEAD, the fine "
        "crosshatching between them and the vertical creases between her brows ARE WHAT THE PICTURE "
        "IS OF, and they run the full width of the panel."
    ),
)

SHOTS["lower"] = dict(
    selfie=True,
    label="mouth, jaw and neck",
    text=(
        "THE PANEL IS A BAND ACROSS THE LOWER FACE AND THE NECK. The frame runs from just under her "
        "nose at the top - the nostrils are just inside the top edge, the eyes are NOT in the picture "
        "at all - down over her mouth, chin and jaw and on down the neck to her collarbones at the "
        "bottom, with the sides of her jaw running out to both edges. She is square to the camera. "
        "THE VERTICAL LINES ON HER LIPS, THE LINES RUNNING DOWN FROM THE CORNERS OF HER MOUTH, THE "
        "LINE OF THE JAW AGAINST THE NECK, THE SOFTNESS UNDER THE CHIN AND THE SLACK VERTICAL "
        "BANDING DOWN THE FRONT OF THE NECK ARE WHAT THE PICTURE IS OF."
    ),
)

SHOTS["eyes"] = dict(
    selfie=True,
    label="eyes and mid-face",
    text=(
        "THE PANEL IS A BAND ACROSS THE MIDDLE OF THE FACE. The frame runs from the middle of her "
        "forehead at the top down to her top lip at the bottom, and out past both cheekbones at the "
        "sides. Both eyes, both brows, the whole of her nose and the tops of both cheeks are in view; "
        "her mouth and chin are NOT in the picture. She is square to the camera and both sides of her "
        "face are in frame. THE CREASES AT THE OUTER CORNERS OF BOTH EYES, THE LOOSE PUFFY SKIN AND "
        "SHADOW UNDER THEM, AND THE LINES BEGINNING TO RUN DOWN FROM EACH SIDE OF THE NOSE ARE WHAT "
        "THE PICTURE IS OF."
    ),
)

#: Frontal bands only - see the comment above. Run on the two concerns Malcolm asked for.
REGION_SHOTS = ["forehead", "lower", "eyes"]
REGION_CONCERNS = ["fine-lines", "firming"]

SHOT_ORDER = ["macro", "half", "close"]

# --------------------------------------------------------------------------------------
# THE AMATEUR / BAD-PHOTOGRAPH STYLE. Malcolm, 2026-08-28:
#
#   "add another batch that is noticeably bad quality photo (not the detail - but clearly a
#    home made selfie photo with bad lighting), and with more variation in the variables
#    that make the before and after unique from each other. Quality of the realism should
#    stay as real as possible. This is a new type of image we are trying out."
#
# ⚠️ THE CENTRAL DISTINCTION, AND THE WHOLE REASON THIS NEEDS ITS OWN CODE PATH:
# THE PHOTOGRAPH IS BAD. THE IMAGE IS NOT. Told simply to make a bad photo, every engine
# degrades the RENDER — soft mush, low detail, smeared faces, obvious artefacts — which
# destroys the only thing these pictures exist to show. What is wanted is a sharp,
# high-fidelity, entirely believable image OF a badly-taken snapshot: the light is wrong,
# the framing is careless, the phone struggled, but the skin is still real skin with real
# pores in it. Paragraph 12a states that separation in as many words, and the negative list
# bans the degradation words rather than the darkness words.
#
# ⚠️ BAD LIGHT CAN FABRICATE THE ENTIRE RESULT, and this is a worse risk here than the
# distance confound was. If the earlier panel gets harsh raking light and the later panel
# gets soft kind light, the "improvement" is the lamp. It would also be almost invisible as
# a fault, because bad lighting is *supposed* to differ between the two days. So the brief
# requires both panels to be badly lit TO A SIMILAR DEGREE, with neither one flattering, and
# the lines readable in both despite it.
#
# ⚠️ THE NEGATIVE LIST HAD TO BE REBUILT. The standard list bans `no dark room, no dim room,
# no murky lighting, no underexposed picture, no camera flash, no orange tungsten glow, no
# heavy shadow across the face, no bathroom, no fluorescent strip light` — every one of which
# forbids exactly what this batch asks for. Left in place they would have fought the brief on
# all eight slots, which is the stale-negative trap these configs keep warning about.
#
# HANDS AND ARMS COME BACK. Acetyl wave 11 found that banning arms is precisely why several
# waves read as portraits taken by somebody else: "the raised near arm is the strongest tell
# there is." It is allowed here. The phone itself still cannot appear — this is the view
# through its own front camera — and no mirrors, or the phone comes with them.
# --------------------------------------------------------------------------------------
AMATEUR_SCENES = [
    ("a cramped hallway with a scuffed off-white wall",
     "the ceiling light directly overhead and nothing else, throwing hard shadows straight down "
     "into her eye sockets and under her nose and chin",
     "evening", "the edge of a door architrave"),
    ("a small bedroom with a plain painted wall",
     "one warm bedside lamp low and off to one side, so everything is orange and the far half of "
     "her face falls away into shadow",
     "night", "the corner of a headboard"),
    ("a kitchen with a plain wall",
     "a bright window directly behind her, so she is backlit and her whole face is underexposed "
     "while the wall beyond her blows out to white",
     "the middle of the day", "the blurred edge of a worktop"),
    ("a landing at the top of the stairs",
     "a dim overcast window a long way off, so the picture is dark and the phone has pushed its "
     "sensitivity right up",
     "a grey late afternoon", "the vertical line of a bannister rail"),
    ("a sitting room with a plain wall",
     "one harsh window very close on one side, blowing that cheek out to almost pure white while "
     "the other side of her face drops to near black",
     "morning", "the out-of-focus back of a sofa"),
    ("a bathroom with a plain painted wall",
     "a strip light above the mirror, flat and slightly green, greying her skin and flattening "
     "her face completely",
     "early morning", "the soft edge of a hanging towel"),
    ("a hallway by the front door",
     "a ceiling spotlight set slightly behind her, so the top of her head is bright and her face "
     "sits in its own shadow",
     "evening", "the dark edge of a coat hanging up"),
    ("a bedroom with a plain wall",
     "the cold light of an overcast window on one side mixed with a warm lamp on the other, so "
     "one half of her face reads blue and the other orange",
     "afternoon", "the blurred upright of a wardrobe door"),
    ("a spare room with a bare magnolia wall",
     "a single bulb with no shade, close and above, burning out her forehead and the bridge of "
     "her nose while the rest goes muddy",
     "night", "the corner of an empty shelf"),
    ("a dining room with a plain wall",
     "low evening sun coming in almost horizontally and hitting one side of her face far too "
     "hard, with a hard-edged shadow across the other",
     "early evening", "the blurred top of a chair back"),
    ("a hallway with a plain wall",
     "the light from a screen off to one side, cold and bluish, with the rest of the room dark "
     "around her",
     "night", "the faint line where the wall meets the ceiling"),
    ("a bedroom with a plain painted wall",
     "an overcast window straight in front of her, flat and grey and far too dim, so the picture "
     "is dull and noisy throughout",
     "a wet morning", "the soft fall of a curtain"),
    ("a utility area with a plain wall",
     "a bare ceiling fitting behind and above her, leaving her face in a broad soft shadow with "
     "the wall brighter than she is",
     "evening", "the blurred edge of a doorframe"),
    ("a small study with a plain wall",
     "a desk lamp pointing up at her from below and off to one side, lighting her from underneath "
     "so the shadows all run the wrong way",
     "night", "the out-of-focus corner of a desk"),
    ("a bedroom with a plain wall",
     "bright hard midday sun coming through an uncovered window and striking her at a steep angle, "
     "clipping the highlights on her cheek to white",
     "midday", "the blurred vertical of a wardrobe edge"),
    ("a hallway with a plain painted wall",
     "one dim wall light a long way off, so almost nothing reaches her and the phone has lifted "
     "the whole picture until it is grainy",
     "late evening", "the soft dark shape of a coat on a hook"),
]

# The negative list for the amateur batch. Note what it does NOT ban compared with
# NEGATIVE_GLOBAL: darkness, dimness, murk, underexposure, flash, tungsten, strip lights,
# bathrooms, heavy facial shadow and hands are all now WANTED. What it bans instead is the
# thing an engine reaches for when it hears "bad photo" — a degraded RENDER.
NEGATIVE_GLOBAL_AMATEUR = (
    "no text, no lettering of any kind, no words, no letters, no numbers, no percentages, "
    "no captions, no labels, no watermark, no stock photo watermark, no printed text overlay, "
    "no logo, no signature, no timestamp, no date stamp, "
    "no illustration, no drawing, no painting, no render, no 3d render, no cgi, no video game "
    "character, no cartoon, no anime, no doll, no mannequin, no waxwork, "
    "no low resolution, no pixelated image, no blocky compression destroying the face, "
    "no heavily degraded image, no unusable blur, no motion blur across the whole face, "
    "no smeared face, no melted features, no distorted anatomy, no extra fingers, "
    "no plastic skin, no waxy skin, no airbrushed skin, no beauty-filter smoothing, "
    "no frequency separation, no uniform skin texture, no poreless skin, "
    "no bottle, no jar, no dropper, no packaging, no product, no jewellery, no spectacles, "
    "no makeup, no foundation, no powder, no concealer, no eyeliner, no mascara, no false "
    "lashes, no eyeshadow, no lipstick, no glitter, "
    "no wound, no bruise, no rash, no blood, no needle, no drawn lines on the skin, "
    "no clinical disease, no dermatological condition, no lesion, "
    "no phone, no smartphone, no phone case, no selfie stick, no mirror, no reflection, "
    "no studio backdrop, no seamless paper, no professional lighting, no softbox, no beauty "
    "dish, no fashion photograph, no glamour, no styled hair, no salon blow-dry, no retouching, "
    "no model, no supermodel, no bokeh portrait mode, "
    "no elderly woman, no woman over sixty, no woman under forty, no full head of white hair, "
    "no heavy jowls, no badly sagging neck, "
    "no three panels, no four panels, no grid of panels, no picture frame, no border, "
    "no vignette, no gap between panels, no dividing line of any colour, "
    "no non-white model, no black model, no asian model, no south asian model, "
    "no readable object, no text on the wall, no photographs on the wall, no posters, "
    "no full body, no distant framing"
)

NEGATIVE_AMATEUR_EXTRA = (
    "no identical backgrounds between the panels, no same room in both panels, "
    "no identical framing between the panels, no same camera angle in both panels, "
    "no same head position in both panels, no same distance in both panels, "
    "no same lighting in both panels, no mirrored pose, no copy of the left panel, "
    "no different side of the face between the panels, no left cheek in one panel and right "
    "cheek in the other, no mirror image of the left panel, no flipped view, "
    "no flattering light in the right panel, no soft kind light in the right panel, "
    "no better lit right panel, no studio light in either panel, "
    "no unchanged skin between the panels, no zero difference between the panels, "
    "no different woman between the panels, no younger woman in the right panel, "
    "no makeup appearing in the right panel, no change of skin colour between the panels, "
    "no moles disappearing between the panels, no freckles disappearing between the panels, "
    "no face hidden in shadow, no eyes lost in darkness, no unreadable face, "
    "no smiling, no teeth"
)


# --------------------------------------------------------------------------------------
# Magnitude strengths. Malcolm, 2026-08-28, chose to generate BOTH and decide from images
# rather than from a number, after seeing that his seven reference pairs show far more change
# than the 30% he had specified.
#
# ⚠️ Worth keeping attached to the m50 set: those references are captioned "after 1 / 3 / 6 /
# 10 TREATMENTS" - they are clinic device courses (RF, microneedling), not a topical cream.
# A cream matching that result is a stronger claim than the research on this page carries;
# Miller 2006 measured self-reported satisfaction with appearance, and Pickart 2018 and Kang
# 2009 are a literature review and a cell-culture study. The m30 set is what the evidence
# supports. The m50 set is a commercial decision, taken with that on the record.
# --------------------------------------------------------------------------------------
STRENGTHS = {
    "m30": dict(
        label="~30%",
        DEGREE="about A THIRD",
        DEGREECAPS="ABOUT A THIRD",
        FIRM="a little more firmly",
        FIRMDEG="slightly more",
    ),
    "m50": dict(
        label="~50%",
        DEGREE="about A HALF",
        DEGREECAPS="ABOUT A HALF",
        FIRM="clearly more firmly",
        FIRMDEG="noticeably more",
    ),
}


# --------------------------------------------------------------------------------------
# The four concerns.
#
# `light` is the whole lighting paragraph and it is where brightening inverts.
# `subject` introduces the left panel. `magnitude` is both the floor and the ceiling on the
# right panel. `honesty` is the clause restated at the point of change, which is the moment
# an engine reaches for its own idea of what improvement means.
# --------------------------------------------------------------------------------------
CONCERNS = {
    "fine-lines": dict(
        title="Fine Lines & Wrinkles",
        macro_shot="macro",
        light=(
            "BOTH PICTURES ARE BRIGHT AND WELL EXPOSED, AND IN BOTH THE DAYLIGHT ARRIVES FROM ONE SIDE AND "
            "RAKES ACROSS HER. This matters more than anything else about the lighting: flat frontal light "
            "flatters skin and hides what this picture exists to show, while light coming across her face "
            "rakes over the surface so every line casts its own small shadow. Bright, clean, no dark room, "
            "no murk, no heavy shadow swallowing half the face, no flash - but definitely DIRECTIONAL, "
            "with a clear light side and a softer shaded side. The direction and quality of the light "
            "differ between the two days; the raking, sidelit character does not."
        ),
        subject=(
            "ON THE EARLIER DAY, IN THE LEFT PANEL, HER EXPRESSION LINES ARE THE SUBJECT OF THE PICTURE. "
        ),
        # Malcolm, 2026-08-28: "the whole point is that there should be a noticeable (though
        # subtle - maybe 30%) improvement in reduction of fine wrinkles AND firmer skin in the
        # after image." Two changes from what shipped in the first twelve waves: the magnitude
        # comes down from a half to about a third, and FIRMNESS is now part of the result on
        # this concern as well as on `firming`, because copper peptide claims both.
        magnitude=(
            "TWO THINGS HAVE IMPROVED, AND BOTH MUST BE THERE.\n\n"
            "FIRST, THE LINES ARE SHALLOWER. Each one is {DEGREE} less deep, holding a lighter and "
            "shorter shadow.\n\n"
            "SECOND, HER SKIN LOOKS FIRMER AND BETTER SUPPORTED. It sits {FIRM} over the bone, with "
            "{FIRMDEG} of a cushioned, resilient quality and less of a thin, slack one - most readable "
            "along the jaw and the outer cheek.\n\n"
            "THE SIZE OF THE CHANGE IS THE POINT AND IT IS NARROW AT BOTH ENDS. It must be NOTICEABLE - "
            "a viewer looking at the two halves should SEE that the later one is better without being "
            "told to look for it, and should be able to point to which lines are softer and where the "
            "skin sits differently. But it is {DEGREECAPS}, NOT A TRANSFORMATION: every single line is "
            "STILL THERE, in the same place and the same number, and not one has disappeared. A viewer "
            "must be able to match them up one for one between the panels. Her face is the same shape, "
            "the same width and the same weight - nothing lifted, slimmed, tightened or contoured. A "
            "right panel with smooth, line-free skin, or one that reads as a facelift, is a failure, "
            "not a success."
        ),
        honesty=(
            "AND AT THE SAME TIME, IN THAT SAME RIGHT PANEL: the number and position of her lines is "
            "unchanged and NOT ONE HAS DISAPPEARED. Every mole, freckle and mark is still there, in the "
            "same place and the same number. What has changed is the DEPTH of the lines and how firmly "
            "her skin sits - not the shape of her face, not her age and not her weight."
        ),
        negatives=("no line disappearing between the panels, no smooth line-free skin in the right panel, "
                   "no flat frontal lighting, no shadowless face"),
    ),
    "firming": dict(
        title="Firming & Skin Density",
        macro_shot="macro_jaw",
        light=(
            "BOTH PICTURES ARE BRIGHT AND WELL EXPOSED, AND IN BOTH THE DAYLIGHT ARRIVES FROM ONE SIDE AND "
            "RAKES ACROSS HER. Directional light is what makes contour readable: it models the cheek and "
            "draws the edge of the jaw against the neck, where flat frontal light would flatten both away "
            "and hide what this picture exists to show. Bright, clean, no dark room, no murk, no heavy "
            "shadow swallowing half the face, no flash - but definitely DIRECTIONAL, with a clear light "
            "side and a softer shaded side. The direction and quality of the light differ between the two "
            "days; the raking, sidelit character does not."
        ),
        subject=(
            "ON THE EARLIER DAY, IN THE LEFT PANEL, THE SLACKNESS AND THINNESS OF HER SKIN IS THE SUBJECT "
            "OF THE PICTURE. "
        ),
        # Same instruction as on `fine-lines` (Malcolm, 2026-08-28), led the other way round:
        # firmness first because that is this batch's subject, with the line softening carried
        # alongside it. The previous wording — "a viewer should HAVE TO LOOK from one panel to
        # the other to see it" — was too quiet for what he asked for and is now "noticeable".
        magnitude=(
            "TWO THINGS HAVE IMPROVED, AND BOTH MUST BE THERE.\n\n"
            "FIRST, HER SKIN IS FIRMER AND BETTER SUPPORTED. It sits {FIRM} over the bone, the softness "
            "along the jaw is less pronounced so the edge of the jaw is drawn {FIRMDEG} cleanly against "
            "the neck, and the surface has a resilient, cushioned quality where it was thin and "
            "papery.\n\n"
            "SECOND, HER FINE LINES ARE SHALLOWER - {DEGREE} less deep, each holding a lighter and "
            "shorter shadow.\n\n"
            "THE SIZE OF THE CHANGE IS THE POINT AND IT IS NARROW AT BOTH ENDS. It must be NOTICEABLE - "
            "a viewer looking at the two halves should SEE that the later one is better without being "
            "told to look for it, and should be able to point to where the skin sits differently and "
            "which lines are softer. But it is {DEGREECAPS}, NOT A TRANSFORMATION, and this is the "
            "most easily overstated change in the whole set: her face has NOT been lifted, tightened, "
            "slimmed or contoured, her jaw is the SAME JAW and the same shape, her cheekbones have not "
            "become more prominent, and she has not lost any weight. Every fold and every line she has "
            "is still there, in the same place and the same number. Anything that reads as a facelift "
            "is a complete failure."
        ),
        honesty=(
            "AND AT THE SAME TIME, IN THAT SAME RIGHT PANEL: her face is the SAME SHAPE - the same jaw, "
            "the same cheekbones, the same weight, the same width. Nothing has been slimmed, lifted or "
            "sculpted. Every mole, freckle and mark is still there in the same place, and every line she "
            "has is still there, just less deeply cut. She is the same age and the same person."
        ),
        negatives=("no facelift, no tightened face, no slimmer face, no contoured cheekbones, no weight "
                   "loss between the panels, no jawline reshaped, no flat frontal lighting, no shadowless "
                   "face"),
    ),
    "repair": dict(
        title="Skin Repair & Renewal",
        macro_shot="macro",
        light=(
            "BOTH PICTURES ARE BRIGHT AND WELL EXPOSED, AND IN BOTH THE DAYLIGHT ARRIVES FROM ONE SIDE AND "
            "RAKES ACROSS HER. Light coming across the skin at an angle is what makes SURFACE TEXTURE "
            "readable - roughness, flaking and unevenness all catch it, where flat frontal light would "
            "smooth them away and hide what this picture exists to show. Bright, clean, no dark room, no "
            "murk, no heavy shadow swallowing half the face, no flash - but definitely DIRECTIONAL, with a "
            "clear light side and a softer shaded side. The direction and quality of the light differ "
            "between the two days; the raking, sidelit character does not."
        ),
        subject=(
            "ON THE EARLIER DAY, IN THE LEFT PANEL, THE POOR CONDITION OF HER SKIN'S SURFACE IS THE "
            "SUBJECT OF THE PICTURE. "
        ),
        magnitude=(
            "The surface of her skin is VISIBLY IN BETTER CONDITION - the rough, dry, flaking patches have "
            "calmed and smoothed, the reddened irritated areas are quieter and less angry, and the skin "
            "looks better hydrated and more comfortable, with a soft healthy sheen rather than either a "
            "dull chalky dryness or an oily shine. BUT THE CEILING MATTERS AS MUCH AS THE FLOOR: this is "
            "the same skin in better condition, not new skin. Her pores are the same size and in the same "
            "places, her texture is still real and varied, her lines are all still there, and every mole, "
            "freckle and mark is still exactly where it was. A right panel with flawless, poreless, "
            "uniform skin is a failure, not a success."
        ),
        honesty=(
            "AND AT THE SAME TIME, IN THAT SAME RIGHT PANEL: her pores are the same pores, the same size, "
            "in the same places and still plainly visible. Every mole, freckle and distinct mark is still "
            "there in the same place and the same number. Her expression lines are the same lines. What "
            "has changed is the CONDITION of the surface - the roughness, the flaking and the irritation - "
            "and nothing else."
        ),
        negatives=("no poreless skin, no flawless skin in the right panel, no uniform skin texture, no "
                   "airbrushed skin, no flat frontal lighting, no shadowless face"),
    ),
    "brightening": dict(
        title="Brightening & Glow",
        macro_shot="macro",
        # THE INVERSION. See docs/clinical-trial-before-after-images.md §10.
        light=(
            "THE LIGHT ON BOTH DAYS IS BRIGHT, SOFT AND BROAD, AND IT COMES FROM ROUGHLY IN FRONT OF HER. "
            "This matters more than anything else about the lighting and IT IS THE OPPOSITE OF WHAT A "
            "PICTURE ABOUT WRINKLES WOULD WANT: hard light raking across a cheek lays down a gradient of "
            "shadow, and a gradient of shadow looks exactly like a patch of uneven colour, so it would "
            "invent the very thing this picture exists to show. Soft frontal daylight lights the skin "
            "evenly and lets its actual colour be seen. Bright, clean, well exposed, no dark room, no "
            "heavy shadow across the face, no flash. The direction of the daylight differs a little "
            "between the two days, but the brightness, the softness, the exposure and the colour "
            "temperature DO NOT."
        ),
        subject=(
            "ON THE EARLIER DAY, IN THE LEFT PANEL, THE UNEVENNESS AND DULLNESS OF HER SKIN TONE IS THE "
            "SUBJECT OF THE PICTURE. "
        ),
        magnitude=(
            "Her tone is VISIBLY MORE EVEN - the diffuse mottling and the patchy areas have evened out a "
            "good deal, much closer in colour to the clear skin around them, and the dull cast has lifted, "
            "so the whole area reads clearer, fresher and softly luminous rather than flat and tired. BUT "
            "THE CEILING MATTERS AS MUCH AS THE FLOOR: the patches are FAINTER, NOT GONE. Every one of "
            "them is still findable in exactly the same place, with the same shape and the same soft "
            "edges - a viewer must be able to match them up one for one. A right panel with clear, clean, "
            "patch-free skin is a failure, not a success."
        ),
        honesty=(
            "AND AT THE SAME TIME, IN THAT SAME RIGHT PANEL: EVERY MOLE, EVERY FRECKLE AND EVERY DISTINCT "
            "SUN SPOT IS STILL THERE, in the same place and the same number, and not one has been removed "
            "or faded away. Count them in the left panel and they are all still countable in the right. "
            "This is not a picture about removing spots: what evens out is the soft, diffuse, blotchy "
            "mottling BETWEEN and AROUND them. She is not a paler person - the clear skin between the "
            "patches, the skin under her jaw and the skin of her neck are precisely the same colour in "
            "both panels, not lightened, bleached, whitened, chalky or grey."
        ),
        negatives=("no lighter skin in the right panel, no bleached skin, no whitened skin, no chalky "
                   "skin, no patch-free skin in the right panel, no freckles fading between the panels, "
                   "no moles disappearing, no colour cast on one panel, no warm panel beside a cool "
                   "panel, no raking sidelight, no hard shadow across the cheek"),
    ),
}

CONCERN_ORDER = ["fine-lines", "firming", "repair", "brightening"]

#: Concerns the bad-photograph style is run on. Brightening is deliberately excluded - see
#: the comment in main().
AMATEUR_CONCERNS = ["fine-lines", "firming"]

# --------------------------------------------------------------------------------------
# The thirty-two women, eight per concern. Caucasian, 40-60, ordinary, unglamorous.
#
# `before` is the specific, per-woman description of what the fault actually looks like on
# HER. It is the single highest-value string in the file: "uneven skin tone" or "wrinkles"
# left generic is where an engine substitutes its own stock idea, and that is what produced
# the interchangeable faces of the earlier waves.
# --------------------------------------------------------------------------------------
WOMEN = {
    "fine-lines": [
        dict(key="a", who=("a white AMERICAN woman of about fifty-two from the Midwest, with dull "
                           "dishwater-blonde hair pulled back in a clip and a few greys at the parting, "
                           "fair skin, pale blue eyes and sparse fair brows"),
             before=("A fan of four or five creases at the outer corner of each eye that stay put with her "
                     "face at rest, three horizontal lines across the forehead, a pair of short vertical "
                     "creases between the brows, and a line beginning to run down from each side of the "
                     "nose. In the raking light each one holds a clear shadow along its length.")),
        dict(key="b", who=("a white IRISH-AMERICAN woman of about fifty-seven, with faded auburn hair, "
                           "very fair skin densely freckled across the nose and cheeks, green-hazel eyes "
                           "and pale reddish brows"),
             before=("Deep-set crow's feet radiating well past the outer corner of each eye, four "
                     "horizontal forehead lines of uneven length, fine crosshatched lines on the upper "
                     "cheeks, and clear nose-to-mouth lines. Each holds a distinct shadow in the "
                     "sidelight.")),
        dict(key="c", who=("a white woman of about forty-three from northern FRANCE, with chestnut brunette "
                           "hair cut short, fair skin with an olive undertone and hazel eyes"),
             before=("Fine but clearly established lines: a close fan of three at each outer eye corner, "
                     "two faint horizontal forehead lines, and a single vertical crease between the brows "
                     "that sits deeper than the rest. They are shallower than an older woman's but they do "
                     "not go away when her face is at rest.")),
        dict(key="d", who=("a white DANISH woman of about fifty-nine, very fair, with pale ash-blonde hair "
                           "gone mostly grey, light blue eyes and pale sandy brows and lashes"),
             before=("Well-established lines across the whole face: a dense fan at both outer eye corners, "
                     "four forehead lines running the full width, vertical creases between the brows, fine "
                     "vertical lines above the upper lip, and clear folds from nose to mouth corner. Each "
                     "casts its own shadow in the raking light.")),
        dict(key="e", who=("a white woman of about forty-seven from southern ITALY, with near-black hair "
                           "pulled back, olive skin, dark brown eyes and heavy dark brows"),
             before=("A fan of four creases at each outer eye corner, two horizontal forehead lines, a "
                     "single deep vertical crease between the brows, and pronounced nose-to-mouth lines "
                     "that read strongly on olive skin in sidelight.")),
        dict(key="f", who=("a white POLISH woman of about fifty-four, with ash-blonde hair going grey, "
                           "broad cheekbones, fair skin with an olive undertone and grey eyes"),
             before=("A wide fan of five creases at each outer eye corner reaching towards the temple, "
                     "three deep horizontal forehead lines, and fine crosshatching over the cheekbones "
                     "where the skin has been sun-exposed. All hold shadow at rest.")),
        dict(key="g", who=("a white AMERICAN woman of about forty-one from the South, with mid-brown "
                           "shoulder-length hair, fair skin visibly weathered by sun with an uneven tan "
                           "line at the hairline, and brown eyes"),
             before=("Early but real lines: a fan of three fine creases at each outer eye corner, two faint "
                     "forehead lines, and the beginnings of a line from each side of the nose. Sun "
                     "exposure has brought them on younger than her age would suggest.")),
        dict(key="h", who=("a white ENGLISH woman of about fifty-five, with mid-brown hair going grey at "
                           "the parting and cut to the shoulder, fair skin, grey-blue eyes and sparse "
                           "brows"),
             before=("A fan of four or five creases at each outer eye corner, three horizontal forehead "
                     "lines, vertical creases between the brows, and clear nose-to-mouth folds. Fine "
                     "crepe-like lines have begun on the upper cheeks. Each holds a shadow at rest.")),
    ],
    "firming": [
        dict(key="a", who=("a white ENGLISH woman of about fifty-eight, with mid-brown hair going grey and "
                           "cut to the jaw, fair skin and grey-blue eyes"),
             before=("The edge of her jaw has lost its clean line: the soft tissue sits a little forward of "
                     "the bone and blurs the outline where jaw meets neck, there is a slight fullness "
                     "beginning under the chin, and the skin over the whole area reads thin and papery "
                     "rather than cushioned, with fine crepe texture catching the sidelight.")),
        dict(key="b", who=("a white DANISH woman of about fifty-three, very fair, with pale ash-blonde hair "
                           "and light blue eyes"),
             before=("Her cheeks have flattened and dropped slightly, so the skin sits loosely over the "
                     "bone rather than firmly across it, the jaw line is softened and indistinct at its "
                     "back half, and the skin has a thin, undersupported quality with fine crepe texture "
                     "on the lower cheek.")),
        dict(key="c", who=("a white woman of about forty-six from southern ITALY, with near-black hair, "
                           "olive skin and dark brown eyes"),
             before=("The skin along her jaw has begun to soften and hang very slightly, the line from ear "
                     "to chin is no longer crisp, and the surface reads thinner and less resilient than "
                     "the firmer skin higher on the cheekbone.")),
        dict(key="d", who=("a white POLISH woman of about fifty-nine, with ash-blonde hair gone grey, broad "
                           "cheekbones, fair olive-undertoned skin and grey eyes"),
             before=("Clear slackening: soft tissue sitting forward of the jaw bone and breaking its "
                     "outline in two places, a distinct fullness under the chin, and thin crepe-textured "
                     "skin over the whole jaw and upper neck that folds finely when the light rakes it.")),
        dict(key="e", who=("a white AMERICAN woman of about forty-four from the Midwest, with dishwater "
                           "blonde hair and pale blue eyes"),
             before=("Early loss of firmness: the jaw line is still mostly clean but has begun to soften "
                     "towards the back, the cheek sits a little lower than it did, and the skin has lost "
                     "some of its cushioned quality without yet being slack.")),
        dict(key="f", who=("a white IRISH woman of about fifty-one, with coppery red hair faded at the "
                           "parting, very fair densely freckled skin and green eyes"),
             before=("Thin, fine, fair skin that shows undersupport clearly: the jaw outline is soft and "
                     "interrupted, there is fine crepe texture along the jaw and onto the upper neck, and "
                     "the whole area reads papery rather than resilient.")),
        dict(key="g", who=("a white woman of about fifty-six from northern FRANCE, with chestnut brunette "
                           "hair greying at the temples, fair skin with an olive undertone and hazel eyes"),
             before=("Softening along the whole lower face: the jaw edge is blurred rather than drawn, "
                     "there is slight fullness beneath the chin, and the skin over the jaw has a thin, "
                     "loosely-sitting quality with visible fine texture.")),
        dict(key="h", who=("a white GREEK woman of about forty-nine, with almost-black brunette hair, warm "
                           "olive skin and dark brown eyes"),
             before=("The jaw line has softened at its back half and the skin sits a little loosely over "
                     "it, with a faint fullness under the chin and a thinner, less cushioned quality to "
                     "the surface than the firmer skin on the cheekbone above.")),
    ],
    "repair": [
        dict(key="a", who=("a white IRISH woman of about fifty, with coppery red hair faded at the parting, "
                           "very fair densely freckled skin and green eyes"),
             before=("Her skin is in poor condition: rough dry patches flaking finely across the cheek and "
                     "beside the nose, angry pink irritated areas around the nostrils and on the chin, a "
                     "general reddened blotchiness over the cheekbone, and a dull chalky dryness that "
                     "catches the raking light as broken, uneven texture.")),
        dict(key="b", who=("a white ENGLISH woman of about forty-two, with mid-brown hair, fair skin and "
                           "grey-blue eyes"),
             before=("Dry, rough, dehydrated skin: fine flaking across both cheeks, tight-looking patches "
                     "at the outer cheek and temple, some reddened irritation along the sides of the nose, "
                     "and a surface that reads dull and lifeless rather than comfortable.")),
        dict(key="c", who=("a white POLISH woman of about fifty-seven, with ash-blonde hair going grey, "
                           "broad cheekbones and fair olive-undertoned skin"),
             before=("Rough, weathered, uncomfortable-looking skin: flaking dryness over the cheekbone, "
                     "persistent redness across the mid-face, small rough bumps in the skin's surface, and "
                     "a coarse uneven texture that the sidelight breaks across unevenly.")),
        dict(key="d", who=("a white DANISH woman of about forty-five, very fair, with pale ash-blonde hair "
                           "and light blue eyes"),
             before=("Sensitised, reddened skin: diffuse pink irritation over both cheeks and across the "
                     "nose, dry flaking patches at the outer cheeks, small broken capillaries, and a "
                     "surface that looks sore and stripped rather than healthy.")),
        dict(key="e", who=("a white AMERICAN woman of about fifty-four from the South, with mid-brown hair "
                           "and brown eyes, her skin visibly weathered by sun"),
             before=("Sun-damaged skin in poor condition: coarse rough texture over the cheekbone, dry "
                     "flaking at the outer cheek, patchy redness, and small hardened rough spots. The "
                     "raking light finds a surface that is broken and uneven everywhere.")),
        dict(key="f", who=("a white woman of about forty-eight from southern ITALY, with near-black hair, "
                           "olive skin and dark brown eyes"),
             before=("Congested, uneven skin: rough bumpy texture across the cheek and jaw, some reddened "
                     "irritated areas, enlarged and blocked-looking pores over the cheekbone and beside "
                     "the nose, and a dull tired surface.")),
        dict(key="g", who=("a white woman of about fifty-nine from northern FRANCE, with chestnut brunette "
                           "hair greying at the temples and fair skin with an olive undertone"),
             before=("Thin, dry, poorly-conditioned skin: fine flaking across the cheek, crepe-like "
                     "roughness at the outer eye and temple, patchy dull areas, and reddened irritation "
                     "along the nose and chin.")),
        dict(key="h", who=("a white GREEK woman of about forty-three, with almost-black brunette hair, warm "
                           "olive skin and dark brown eyes"),
             before=("Rough and irritated skin: dry flaking patches beside the nose and on the chin, "
                     "reddened inflamed areas across the cheek, uneven bumpy texture, and a surface that "
                     "reads stressed and uncomfortable under the raking light.")),
    ],
    "brightening": [
        dict(key="a", who=("a white ENGLISH woman of about fifty-two, with mid-brown hair going grey at the "
                           "parting and cut to the shoulder, fair skin, grey-blue eyes and sparse brows"),
             before=("Her tone is visibly uneven and tired-looking: soft brown mottling spread across both "
                     "cheekbones and out towards the temples, a duller sallow cast over the mid-face "
                     "compared with the clearer skin of her neck, and a few small flat sun spots high on "
                     "each cheek. The mottling has soft edges and no two patches are the same shape or in "
                     "mirrored positions.")),
        dict(key="b", who=("a white DANISH woman of about forty-eight, very fair, with pale ash-blonde "
                           "hair, light blue eyes and pale sandy brows and lashes"),
             before=("A dull greyish-sallow cast over the whole mid-face, diffuse patchy discolouration at "
                     "both temples and along the sides of the forehead, and a faint brownish shadowing "
                     "beneath the eyes that is part pigment and not only shade. The patches have soft "
                     "edges, differ in shape and are not mirrored side to side.")),
        dict(key="c", who=("a white woman of about fifty-seven from southern ITALY, with near-black hair "
                           "pulled back, olive skin, dark brown eyes and heavy dark brows"),
             before=("A soft-edged brown patch of pigmentation spread over the cheekbone and up towards the "
                     "temple, a duller band of darker tone above the upper lip, and a general muddiness "
                     "across that side of the face compared with the even olive of her jaw and neck. The "
                     "patch has no hard border and is not mirrored.")),
        dict(key="d", who=("a white IRISH woman of about forty-four, with coppery red hair faded at the "
                           "parting, very fair densely freckled skin and green eyes"),
             before=("Her freckles are dense across the cheekbone and they sit in a field that is itself "
                     "blotchy and unevenly darkened - patches of duller, browner tone between and around "
                     "them, a faint reddish unevenness lower on the cheek, and an overall dull cast that "
                     "makes the whole area read muddy rather than clear.")),
        dict(key="e", who=("a white woman of about fifty-nine from northern FRANCE, with chestnut brunette "
                           "hair greying at the temples, fair skin with an olive undertone and hazel eyes"),
             before=("A dull greyish cast across the mid-face, soft patchy discolouration over both "
                     "cheekbones, and skin that reads flat and lacklustre next to the more even tone of "
                     "her neck. The patches are soft-edged, irregular and not mirrored side to side.")),
        dict(key="f", who=("a white POLISH woman of about forty-one, with ash-blonde hair, broad "
                           "cheekbones, fair skin with a distinctly olive undertone and grey eyes"),
             before=("Patchy sallowness across the mid-face and either side of the nose, a duller yellowish "
                     "cast on the forehead, and a scatter of small flat pigmented marks over the "
                     "cheekbones. The patches are soft-edged, differ in shape and are not mirrored.")),
        dict(key="g", who=("a white AMERICAN woman of about fifty-five from the Midwest, with dull "
                           "dishwater-blonde hair pulled back in a clip, fair skin and pale blue eyes"),
             before=("Blotchy high colour spreading unevenly across the cheek, small flat sun spots over "
                     "the cheekbone and the side of the nose, and a duller, greyer cast on that side of "
                     "the forehead. The blotching is irregular, soft-edged and not mirrored.")),
        dict(key="h", who=("a white GREEK woman of about forty-seven, with almost-black brunette hair, warm "
                           "olive skin and dark brown eyes"),
             before=("A soft-edged band of darker sun pigment running along the top of the cheekbone and "
                     "out to the temple, a duller muddier cast over the rest of the cheek, and a few small "
                     "flat brown marks. Nothing is mirrored and nothing has a hard edge.")),
    ],
}

# --------------------------------------------------------------------------------------
# Negatives. AGE BOUNDS CORRECTED TO THE 40-60 BAND: every previous config in this family
# carried `no woman over fifty-five`, which would now contradict the casting on more than a
# third of the slots. The ban on non-Caucasian models is stated once here and positively per
# slot in the prompt body, which has consistently held better than a ban list.
# --------------------------------------------------------------------------------------
NEGATIVE_GLOBAL = (
    "no text, no lettering of any kind, no words, no letters, no numbers, no percentages, no captions, "
    "no labels, no watermark, no stock photo watermark, no printed text overlay, no logo, no signature, "
    "no timestamp, no date stamp, "
    "no bottle, no jar, no dropper, no packaging, no product, no botanicals, no jewellery, no spectacles, "
    "no makeup, no foundation, no powder, no concealer, no eyeliner, no mascara, no false lashes, "
    "no eyeshadow, no lipstick, no glitter, no specular speckle, no white flecks, "
    "no beauty-filter smoothing, no frequency separation, no airbrushed skin, no plastic skin, "
    "no waxy skin, no porcelain skin, no uniform skin texture, no repeating texture pattern, "
    "no wound, no bruise, no rash, no blood, no needle, no drawn lines on the skin, no painted marks, "
    "no clinical disease, no dermatological condition, no lesion, "
    "no hand, no fingers, no arm, no elbow, no phone, no smartphone, no selfie stick, "
    "no studio backdrop, no seamless paper, no professional lighting, no softbox, no beauty dish, "
    "no ring light circle in the eyes, no fashion photograph, no glamour, no styled hair, "
    "no salon blow-dry, no retouching, no skin smoothing filter, no snapchat filter, "
    "no bokeh portrait mode, no model, no supermodel, "
    "no elderly woman, no woman over sixty, no woman under forty, no full head of white hair, "
    "no heavy jowls, no badly sagging neck, "
    "no dark room, no dim room, no murky lighting, no underexposed picture, no night, no darkness, "
    "no orange tungsten glow, no camera flash, no flash shadow on a wall, "
    "no car, no car interior, no seatbelt, no tiled bathroom wall, no bathroom, no radiator, "
    "no fluorescent strip light, no neon tube, no garden, no outdoors, no fence, no shrubbery, "
    "no bookcase, no bookshelf, no shelves of books, "
    "no three panels, no four panels, no grid of panels, no picture frame, no border, no vignette, "
    "no gap between panels, no dividing line of any colour, "
    "no non-white model, no black model, no asian model, no south asian model, "
    "no clutter, no busy background, no readable object, no text on the wall, no photographs on the "
    "wall, no posters, no patterned wall, no wallpaper, no plant, no kitchen appliance, "
    "no full body, no distant framing, no head and shoulders wide shot"
)

NEGATIVE_SHARED_EXTRA = (
    "no identical backgrounds between the panels, no same room in both panels, "
    "no identical framing between the panels, no same camera angle in both panels, "
    "no same head position in both panels, no same distance in both panels, "
    "no mirrored pose, no copy of the left panel, "
    "no different side of the face between the panels, no left cheek in one panel and right cheek in "
    "the other, no mirror image of the left panel, no flipped view, "
    "no unchanged skin between the panels, no zero difference between the panels, "
    "no different woman between the panels, no younger woman in the right panel, "
    "no makeup appearing in the right panel, no change of skin colour between the panels, "
    "no moles disappearing between the panels, no freckles disappearing between the panels, "
    "no smiling, no teeth, no mirror, no reflection"
)


def _fill(text: str, strength: str) -> str:
    """Substitute the magnitude tokens. Concerns without tokens pass through unchanged."""
    for k, v in STRENGTHS[strength].items():
        if k != "label":
            text = text.replace("{" + k + "}", v)
    return text


def build_prompt(concern_key: str, shot_key: str, woman: dict, rooms: tuple,
                 view: dict, gaze: tuple, style: str = "clean",
                 strength: str = "m30") -> str:
    """Assemble one slot's brief.

    Paragraph order is load-bearing. The honesty rules sit at paragraph 3, before the engine
    has formed its own idea of what the improvement looks like: the glutathione round proved
    that the identical rule at paragraph 17 lost to the engine's prior on every backend, and
    moving it to paragraph 3 fixed it on all of them. Position beat wording.
    """
    c = CONCERNS[concern_key]
    shot = SHOTS[shot_key]
    amateur_style = style == "amateur"
    if amateur_style:
        r1, r2 = AMATEUR_SCENES[rooms[0]], AMATEUR_SCENES[rooms[1]]
    else:
        r1, r2 = ROOMS[rooms[0]], ROOMS[rooms[1]]
    v1, v2 = view["a"], view["b"]
    g1, g2 = gaze
    kind = "phone selfies" if (shot["selfie"] or amateur_style) else "close photographs"

    if amateur_style and shot_key.startswith("macro"):
        # The arm cannot be in a macro. At this crop skin fills the panel, so demanding a
        # raised shoulder in the corner asks for two incompatible things at once - and a
        # brief that contradicts itself is how the cheek macro became a portrait on eight
        # engine-runs. The self-taken feel is carried by the closeness and the bad light
        # instead, and the phone and mirror stay banned for the same reason as everywhere.
        hands = (
            "SHE IS HOLDING THE PHONE HERSELF, RIGHT UP CLOSE. Because the frame is filled with her "
            "skin there is no room for anything else in it: NO HAND, NO FINGERS, NO ARM, NO "
            "SHOULDER, NO PHONE, NO PHONE CASE, NO MIRROR AND NO REFLECTION anywhere in either "
            "panel. Just her skin, and a sliver of the room at the very edge.\n\n"
        )
    elif amateur_style:
        # Acetyl wave 11: banning arms is precisely why several waves read as portraits taken
        # by somebody else. "The raised near arm is the strongest tell there is." The phone
        # still cannot appear - it is the thing taking the picture - and nor can a mirror,
        # because a mirror brings the phone with it.
        hands = (
            "IT MUST BE UNMISTAKABLE THAT SHE TOOK THIS HERSELF ON HER OWN PHONE. The arm holding "
            "the phone is raised, and the top of that near shoulder and the upper arm come into "
            "the bottom corner of the frame at an angle, close to the lens and a little soft - the "
            "single strongest sign that nobody else is in the room. BUT THE PHONE ITSELF IS NEVER "
            "VISIBLE: this is the view through its own front camera, so the phone cannot appear in "
            "its own picture, and there is NO MIRROR and NO REFLECTION anywhere, because a mirror "
            "would put the phone back in shot.\n\n"
        )
    elif shot["selfie"]:
        hands = (
            "IT MUST BE OBVIOUS AT A GLANCE THAT SHE TOOK THIS HERSELF - BUT THE PHONE AND HER HANDS ARE "
            "NEVER IN THE PICTURE. This is the view THROUGH the front camera of the phone she is holding, "
            "so the hand holding it cannot appear in its own frame, and neither can the phone. NO HAND, "
            "NO FINGERS, NO ARM, NO ELBOW, NO PHONE, NO PHONE CASE, NO MIRROR AND NO REFLECTION anywhere "
            "in either panel.\n\n"
        )
    else:
        hands = (
            "NOTHING OF WHOEVER HELD THE CAMERA IS IN THE PICTURE. No hand, no fingers, no arm, no elbow, "
            "no phone, no phone case, no mirror and no reflection anywhere in either panel - only her and "
            "the room behind her.\n\n"
        )

    # The amateur batch pushes every camera fault hard - and then spends a whole paragraph
    # separating the BAD PHOTOGRAPH from a BAD IMAGE, because that is the one place this
    # brief can destroy itself. An engine told to make a bad photo degrades the render.
    if amateur_style:
        amateur = (
            "THIS IS A BADLY TAKEN PHOTOGRAPH AND IT SHOULD LOOK LIKE ONE. Nobody set this up. The "
            "frame is properly crooked - several degrees off level, not a token tilt - and badly "
            "centred, with her head jammed towards one edge or one corner and either far too much "
            "empty space above her or the top of her head clipped off. The phone got the exposure "
            "wrong: some of it is blown out to featureless white and some is blocked up into "
            "shadow. The white balance is well off, and off in a different direction on each of the "
            "two days. The autofocus has not quite landed - it is a touch soft on the eye - and in "
            "the low light the sensor has been pushed hard, so there is real luminance grain "
            "through the shadows and the phone's noise reduction has left the flatter areas "
            "slightly waxy and smeared. It has the look of a picture that has been sent to somebody "
            "over a messaging app: a little compressed, a little rough.\n\n"

            "⚠️ BUT THE PHOTOGRAPH IS BAD, NOT THE IMAGE, AND THIS IS THE MOST IMPORTANT SENTENCE "
            "IN THIS BRIEF. This is a SHARP, HIGH-RESOLUTION, COMPLETELY BELIEVABLE PHOTOGRAPH OF A "
            "BADLY TAKEN SNAPSHOT. Every fault above belongs to the PHOTOGRAPHER, THE ROOM AND THE "
            "PHONE - the light was wrong, the framing was careless, the camera struggled. NONE of "
            "them is a fault in the picture's fidelity. Her skin is still real skin, rendered "
            "faithfully and in full detail: individual pores, fine vellus hair, the actual texture "
            "of a real face. It is NOT low resolution, NOT mushy, NOT smeared across the features, "
            "NOT an illustration and NOT obviously artificial. A real person really photographed, "
            "badly, on a real phone - and every part of her that IS in focus and IS properly "
            "exposed holds up completely at full size.\n\n"
        )
    # The brightening batch keeps colour matched between the halves; the other three want the
    # ordinary amateur white-balance error. See CONCERNS[...]['light'] and §10 of the doc.
    elif concern_key == "brightening":
        amateur = (
            "IT IS AN AMATEUR PICTURE, AND THE TELLS ARE IN THE FRAMING, NOT IN THE COLOUR. The angle is "
            "not eye level, the frame is a few degrees crooked and off-centre, the focus is not perfect "
            "and there is a little noise in the shadows. BUT BOTH PICTURES ARE CLEANLY EXPOSED AND "
            "NEUTRAL IN COLOUR - no orange indoor cast, no blue cast, no filter, and nothing warmer, "
            "cooler, darker or brighter in one panel than in the other. This picture is about the COLOUR "
            "of her skin, so a colour cast in one half and not the other would ruin it completely: nobody "
            "could then tell whether the difference came from her skin or from the light.\n\n"
        )
    else:
        amateur = (
            "IT IS AN AMATEUR PICTURE TAKEN AT HOME, NOT A PHOTOGRAPH. The frame is a few degrees crooked "
            "and off-centre, the focus is not perfect, there is a little noise in the shadows and the "
            "indoor white balance is a little wrong - and a little differently wrong on each of the two "
            "days. Both pictures are nonetheless bright and cleanly exposed.\n\n"
        )

    return (
        # 1 — the frame
        f"Two ordinary {kind} of THE SAME WOMAN, taken WEEKS APART at home, placed side by side to fill "
        "one square frame edge to edge: TWO PANELS OF EXACTLY EQUAL WIDTH meeting at one crisp vertical "
        "edge precisely at the centre, with no gap and no dividing line. Each panel is a tall portrait. "
        "The left panel is the earlier one, the right panel is the later one.\n\n"

        # 2 — expression
        "Her expression is flat and unposed on both days, mouth closed, not smiling.\n\n"

        # 3 — the honesty rules, hoisted to the front. Position beat wording, twice.
        "BEFORE ANYTHING ELSE, THE THINGS THAT MUST BE TRUE OF THE RIGHT-HAND PANEL, BECAUSE THEY ARE "
        "WHAT MAKE THIS PAIR HONEST RATHER THAN AN ADVERTISEMENT:\n\n"
        "ONE. EVERY MOLE, FRECKLE AND DISTINCT MARK SHE HAS IS STILL THERE IN THE RIGHT PANEL, in the "
        "same place, the same size and the same number, and every one is still plainly visible and "
        "countable. Her identity is anchored to those marks and they do not fade, move or vanish.\n\n"
        "TWO. SHE IS THE SAME PERSON, THE SAME AGE AND THE SAME COMPLEXION IN BOTH PANELS. She has not "
        "been made younger, slimmer, prettier, better groomed or lighter-skinned, and she wears no "
        "makeup on either day.\n\n"
        f"THREE. {c['honesty']}\n\n"

        # 4 — two occasions
        "THESE ARE TWO SEPARATE OCCASIONS, NOT TWO COPIES OF ONE FRAME. Everything that identifies her "
        "stays the same, and everything a different day would change is different.\n\n"

        # 5 — identity lock
        "UNMISTAKABLY THE SAME WOMAN: the same face shape and jawline, the same nose, the same eye "
        "colour, the same skin colour, the same brow shape, the same hair colour and cut, and her moles "
        "and freckles in the same places on her skin.\n\n"

        # 6 — THE VIEWPOINT BLOCK. The reason this round exists. Malcolm, 2026-08-27.
        "THE CAMERA IS IN A PLAINLY DIFFERENT PLACE ON THE TWO DAYS, AND THIS IS THE SINGLE MOST "
        "IMPORTANT THING IN THIS BRIEF. In the batches before this one the pose, the head position and "
        "the distance from the camera were so alike between the two panels that the pair read as ONE "
        "PICTURE DUPLICATED AND RETOUCHED, which destroys it. Two photographs taken weeks apart are "
        "never framed the same way twice. So:\n\n"
        f"ON THE EARLIER DAY, IN THE LEFT PANEL: the camera is {v1['cam']}. She has {v1['turn']}, and "
        f"{g1}. She is {v1['dist']}, and {v1['place']} of the panel.\n\n"
        f"ON THE LATER DAY, IN THE RIGHT PANEL: the camera is {v2['cam']}. She has {v2['turn']}, and "
        f"{g2}. She is {v2['dist']}, and {v2['place']} of the panel.\n\n"
        "THESE DIFFERENCES MUST BE OBVIOUS AT A GLANCE, not subtle. Someone looking at the pair should "
        "see immediately that these are two different photographs of one woman rather than one "
        "photograph used twice - the height and angle of the camera, how far away she is and where she "
        "sits in the frame are all visibly different.\n\n"

        # 6b — the constraint that makes the pair comparable at all. Malcolm, 2026-08-27.
        f"BUT ONE THING ABOUT THE VIEW DOES NOT CHANGE, AND IT IS AS IMPORTANT AS EVERYTHING ABOVE. "
        f"{view['side']}. THE SAME AREA OF SKIN MUST BE ON SHOW IN BOTH PANELS. The whole point of the "
        "pair is that a viewer can compare one patch of her face against the same patch weeks later, so "
        "if the earlier panel showed one side of her face and the later panel showed the other, there "
        "would be nothing to compare - those are different areas of skin, with different lines, "
        "different marks and different pigmentation on them, and the picture would prove nothing. The "
        "camera moves; the side of her face it is looking at does not.\n\n"

        # 7 — the bound on the distance change. Without this the round is worse than useless.
        "BUT THE DIFFERENCE IN DISTANCE HAS A LIMIT, AND THE LIMIT IS NOT NEGOTIABLE: the skin this "
        "picture is about must be FULLY AND EQUALLY READABLE IN BOTH PANELS - the same sharpness, the "
        "same level of detail, close enough in both to see the surface clearly. THE CHANGE BETWEEN THE "
        "TWO PANELS MUST NEVER BE EXPLAINABLE BY THE CAMERA. It may not come from the later panel being "
        "further away, softer, blurrier, lower in contrast or less sharply focused. If a viewer could "
        "say 'it only looks better because it is further back or out of focus', the picture has failed "
        "completely. The improvement is IN HER SKIN and must survive being looked at just as closely as "
        "the earlier panel.\n\n"

        # 8 — two rooms
        + (
            f"THE TWO PLACES ARE COMPLETELY DIFFERENT, AND SO IS THE TIME OF DAY. On the earlier "
            f"day she is in {r1[0]}, {r1[2]}, and the only light on her is {r1[1]}; at one edge, "
            f"well out of focus, {r1[3]}. On the later day she is in {r2[0]}, {r2[2]}, and the only "
            f"light on her is {r2[1]}; at one edge, out of focus, {r2[3]}. Two different rooms in "
            "the house, on two different days, at two different times, lit by whatever happened to "
            "be on. Nothing is in view behind her but the wall and that one soft thing at the edge."
            if amateur_style else
            f"THE TWO PLACES ARE DIFFERENT ROOMS. On the earlier day she is in an ordinary room with "
            f"{r1[0]} behind her and, far out of focus at one edge, {r1[2]}; the daylight comes "
            f"{r1[1]}. On the later day she is in an ordinary room with {r2[0]} behind her and, well "
            f"out of focus at one edge, {r2[2]}; the daylight comes {r2[1]}. Two plainly different "
            "plain interiors - a different wall colour and a different light direction each time. "
            "Apart from that one soft out-of-focus thing at the edge, nothing is in view behind her "
            "but the painted wall: no furniture, no pictures, no shelves, no appliances, no window "
            "in shot, no clutter."
        ) + "\n\n"

        # 9 — also different. The amateur style pushes this further: Malcolm asked for MORE
        # variation in the things that separate the two days, so hair goes up on one day and
        # down on the other, and the garment changes kind rather than just colour.
        + ("ALSO COMPLETELY DIFFERENT BETWEEN THE TWO DAYS, AND NOT SUBTLY: a completely different "
           "kind of everyday garment each time - a t-shirt one day and a jumper, hoodie, dressing "
           "gown or vest the other, in different colours with different necklines; and her hair "
           "worn differently, the same cut and colour but scraped up out of the way on one day and "
           "loose and unbrushed on the other. She has clearly just picked up her phone on two "
           "unrelated days and taken a picture of herself.\n\n"
           if amateur_style else
           "ALSO COMPLETELY DIFFERENT BETWEEN THE TWO DAYS: her clothing, if any of it is in view - a "
           "different everyday garment in a different colour and a different neckline each time, nothing "
           "smart or styled; and her hair, the same cut and colour but unstyled and falling differently.\n\n")

        # 10 — hands and phone
        + hands +

        # 11 — the shot type
        shot["text"] + "\n\n"

        # 12 — amateur tells
        + amateur +

        # 13 — the woman
        f"She is {woman['who']}. She wears no makeup at all on either day - no foundation, no concealer, "
        "no powder, nothing that could even out her skin - her brows are natural and unshaped, and her "
        "hair is unstyled. She is an ordinary person, not a model, and neither picture makes any attempt "
        "to flatter her.\n\n"

        # 14 — age, stated positively as well as bounded. Round 1 of the glutathione build drifted
        # a decade older on two of five engines despite the negative list.
        "SHE IS BETWEEN FORTY AND SIXTY - MIDDLE-AGED, CLEARLY AN ADULT WOMAN WELL PAST THIRTY AND "
        "CLEARLY NOT YET SEVENTY - AND THAT GOVERNS WHAT HER SKIN CAN HONESTLY LOOK LIKE. Her expression "
        "lines are established and stay put with her face at rest, and some grey at the parting and "
        "temples is right and expected. But she is NOT elderly and must not read as elderly: she has "
        "none of the deep folds, heavy jowls or crepe-papery slackness of a woman in her seventies.\n\n"

        # 15 — lighting. Brightening inverts it; the amateur style replaces it outright, and
        # carries the guard that stops bad light fabricating the whole result.
        + (
            "THE LIGHTING IS BAD ON BOTH DAYS, AND THAT IS DELIBERATE. This is whatever light "
            "happened to be on in that room at that time, falling on her however it fell. It is "
            "unflattering, it is uneven, and it is nothing anybody would choose - one side too "
            "bright and the other too dark, or coming from above or below or behind her, or simply "
            "too dim for the room. The two days are lit by completely different bad light, from "
            "different directions and in different colours.\n\n"

            "⚠️ BUT NEITHER DAY IS THE FLATTERING ONE, AND THIS IS WHAT KEEPS THE PAIR HONEST. Both "
            "photographs are badly lit TO THE SAME DEGREE. The later one is NOT softer, NOT kinder, "
            "NOT more even and NOT better exposed than the earlier one - if it were, the "
            "improvement in her skin would just be the better light, and the picture would be a "
            "lie. If anything the later day's light is the harsher of the two. AND IN SPITE OF THE "
            "BAD LIGHT, THE SKIN THIS PICTURE IS ABOUT MUST STILL BE CLEARLY READABLE IN BOTH "
            "PANELS: her lines and the surface of her skin are visible and comparable in each, not "
            "buried in shadow, not lost in a blown-out highlight, and not hidden by the murk. A "
            "panel where her face has disappeared into darkness is a failed picture.\n\n"
            if amateur_style else
            c["light"] + "\n\n"
        )

        # 16 — skin realism
        + "THE SKIN MUST HOLD UP AS REAL AND UNFLATTERED, and at this crop it is most of the picture. Pores "
        "are clearly visible and vary in size and density by zone - open across the nose and inner "
        "cheeks, finer at the temples and jaw - with several individually larger than their neighbours. "
        "Pigmentation is uneven and asymmetric, never mirrored from one side to the other. Fine vellus "
        "hairs catch the light along the jaw and upper lip. The skin is a little greasy across the nose "
        "and drier at the outer cheeks. Real skin, photographed honestly, with no smoothing of any "
        "kind.\n\n"

        # 17 — the left panel, per woman
        + c["subject"] + woman["before"] + "\n\n"

        # 18 — the right panel: floor and ceiling
        "ON THE LATER DAY, IN THE RIGHT PANEL: "
        + _fill(c["magnitude"], strength) + "\n\n"

        # 19 — the honesty clause restated at the point of change, because describing the
        # improvement is exactly the moment an engine reaches for its own idea of improvement.
        + c["honesty"] + " She has not been made younger, slimmer, prettier or better groomed, and she "
        "is wearing no makeup in either panel.\n\n"

        # 20 — the floor, last word
        "THERE MUST BE A VISIBLE DIFFERENCE BETWEEN THE TWO PANELS. This is the entire purpose of the "
        "pair. Someone comparing them must be able to see the improvement in the later one and point to "
        "exactly where it is. TWO PANELS THAT LOOK THE SAME ARE A COMPLETE FAILURE - and so are two "
        "panels that differ only because the camera moved.\n\n"

        "An honest amateur snapshot, unretouched and completely unfiltered."
    )


def build_wave(concern_key: str, shot_key: str, style: str = "clean",
               strength: str = "m30") -> dict:
    c = CONCERNS[concern_key]
    amateur_style = style == "amateur"
    shot_name = c["macro_shot"] if shot_key == "macro" else shot_key
    shot = SHOTS[shot_name]
    women = WOMEN[concern_key]
    wave = f"block-copper-peptide-ba-{concern_key}-{shot_key}"
    if amateur_style:
        wave += "-amateur"
    if shot_key in REGION_SHOTS:
        wave += f"-{strength}"
    scenes = AMATEUR_SCENES if amateur_style else ROOMS

    # Room and viewpoint offsets are advanced per shot type so that a woman photographed in
    # all three batches is never in the same room, at the same angle, twice.
    # Region bands are not in SHOT_ORDER; give them their own offsets so their room and
    # viewpoint allocation does not collide with the three standard shot types.
    if shot_key in REGION_SHOTS:
        shot_index = 3 + REGION_SHOTS.index(shot_key)
    else:
        shot_index = SHOT_ORDER.index(shot_key)
    concern_index = CONCERN_ORDER.index(concern_key)

    slots = []
    for i, w in enumerate(women):
        # Rooms are allocated in disjoint ADJACENT PAIRS - (0,1), (2,3), (4,5) ... - so the
        # sixteen rooms a batch uses are all different and no two women in a batch ever stand
        # in the same room. An earlier version advanced r_b by the shot index, which quietly
        # made one woman's LATER room another woman's EARLIER room inside the same batch, and
        # that is precisely the fault the nine-slot structural fix exists to prevent
        # (docs/clinical-trial-before-after-images.md §4, "the structural fix").
        # The shot offset then shifts the whole allocation, so a woman photographed in all
        # three batches is never in a room she has already been in.
        r_a = (i * 2 + shot_index * 8) % len(scenes)
        r_b = (r_a + 1) % len(scenes)
        if shot_key in REGION_SHOTS:
            # Frontal bands only. A forehead band cannot survive a forty-degree head turn,
            # and a lower-face band needs her square on or the jaw line is not comparable.
            # VIEWPOINTS[0:4] are the four front pairs; the camera still varies by height,
            # tilt, distance and placement between the two panels.
            view = VIEWPOINTS[(i + shot_index) % 4]
        else:
            view = VIEWPOINTS[(i + shot_index * 4) % len(VIEWPOINTS)]

        # Gaze strength: subtle on every slot, NOTICEABLY different on roughly three in ten.
        # Indexed globally across all 96 so the 30% holds over the round rather than being
        # rounded up or down inside each batch of eight.
        gi = concern_index * 24 + shot_index * 8 + i
        # The amateur batch takes the NOTICEABLE gaze on every slot: Malcolm asked for more
        # difference between the two days on this style, not the round's usual 30%.
        if amateur_style or gi % 10 < 3:
            gaze = GAZE_NOTICEABLE[gi % len(GAZE_NOTICEABLE)]
            gaze_note = "noticeable"
        else:
            gaze = GAZE_SUBTLE[gi % len(GAZE_SUBTLE)]
            gaze_note = "subtle"

        slots.append({
            "id": f"cpba-{concern_key}-{shot_key}-{w['key']}",
            "title": f"{c['title']} · {shot['label']} · {STRENGTHS[strength]['label']} · "
                     f"{w['key'].upper()} · gaze {gaze_note}",
            "class": "B",
            "width": SIZE,
            "height": SIZE,
            "target_slot": f"copper-peptide before/after library — {c['title']} — {shot['label']}",
            "ref_files": [],
            "prompt": build_prompt(concern_key, shot_name, w, (r_a, r_b), view, gaze, style, strength),
            "label": {
                "left": "BEFORE",
                "right": "AFTER",
                "figure": "",
                "measure": "(labels added in the theme, never in the pixels)",
                "cite": "miller-2006 / pickart-2018 / kang-2009 — block not yet assigned",
            },
            "negative_extra": ((NEGATIVE_AMATEUR_EXTRA if amateur_style else NEGATIVE_SHARED_EXTRA)
                               + ", " + c["negatives"]),
        })

    return {
        "wave": wave,
        "created": "2026-08-27",
        "doc": ("docs/clinical-trial-before-after-images.md, .claude/rules/website-imagery.md, "
                "scripts/build-copper-peptide-before-after-configs.py"),
        "note": (
            (("⚠️ THE BAD-PHOTOGRAPH STYLE TEST. Malcolm, 2026-08-28: a batch that is noticeably bad "
              "quality as a PHOTOGRAPH - clearly a home-made selfie with bad lighting - while the "
              "REALISM of the rendering stays as high as possible, plus more difference between the "
              "two days than the standard waves carry.\n\n"
              "The distinction is the whole brief and it has its own paragraph: the light is wrong, "
              "the framing is careless and the phone struggled, but the IMAGE is sharp, "
              "high-resolution and faithful - real pores, real vellus hair, nothing mushy or "
              "smeared. An engine told simply to make a bad photo degrades the render instead, "
              "which would destroy the only thing these pictures exist to show.\n\n"
              "⚠️ BAD LIGHT CAN FABRICATE THE WHOLE RESULT, and that risk is worse here than the "
              "distance confound. If the earlier panel gets harsh light and the later panel gets "
              "kind light, the improvement is the lamp. Both panels are badly lit to the same "
              "degree, the later one is never the more flattering, and the skin must stay readable "
              "in both in spite of it.\n\n"
              "THE NEGATIVE LIST IS REBUILT for this batch. The standard one bans no dark room, no "
              "dim room, no murky lighting, no underexposed picture, no camera flash, no orange "
              "tungsten glow, no heavy shadow across the face, no bathroom and no fluorescent strip "
              "light - every one of which forbids what this batch is for. It bans the degradation "
              "words instead. Hands and the raised near arm are ALLOWED here (acetyl wave 11: the "
              "raised near arm is the strongest selfie tell there is); the phone and mirrors still "
              "are not.\n\n"
              "Noticeable gaze difference on all eight, not the round's usual 30%.\n\n")
             if amateur_style else "")
            + f"{c['title']} — {shot['label']} — eight amateur women, 40-60, one before/after diptych each. "
            "Part of the twelve-wave copper-peptide round (3 shot types x 4 concerns x 8 women = 96 "
            "diptychs) briefed by Malcolm on 2026-08-27.\n\n"
            "THE CHANGE THAT DEFINES THIS ROUND: the camera position, head position, eye gaze and "
            "distance from the camera are stated SEPARATELY AND DIFFERENTLY for the two panels. Earlier "
            "waves pinned the framing identically in both panels and briefed only the room, light, "
            "garment and hair to vary, which is why those pairs read as one photograph retouched twice. "
            "Paragraph 6 of every prompt now names camera height, camera tilt, head turn, head tip, gaze, "
            "distance and position in frame per panel, and paragraph 7 bounds it so the change can never "
            "be explained by the camera having moved.\n\n"
            + ("LIGHTING IS INVERTED ON THIS CONCERN. A pair about TONE needs soft broad frontal daylight, "
               "not raking sidelight: a shadow gradient across a cheek is indistinguishable from a patch "
               "of pigment and would invent the very fault the picture exists to show. The two halves must "
               "also MATCH for colour temperature and brightness, which partially overrides the "
               "'different lighting for each before and after' instruction — flagged to Malcolm "
               "2026-08-27. See docs/clinical-trial-before-after-images.md §10.\n\n"
               if concern_key == "brightening" else
               "Raking sidelight on both days, so the surface casts its own shadows and the finding is "
               "actually visible.\n\n")
            + ("THE SHOT TYPE IS SUBSTITUTED ON THIS CELL. Malcolm's shot type 1 is a skin-only macro, but "
               "firmness IS contour — jaw, cheek, the line under the chin — and a cheek macro has no "
               "contour in it, so that cell would be a picture unable to show its own subject. This wave "
               "uses a very close JAW-AND-NECK crop instead: the tightest framing that can still carry the "
               "finding.\n\n"
               if shot_name == "macro_jaw" else "")
            + "AGE BAND IS 40-60 THIS ROUND, up from 45-55, and the negative list is corrected to match — "
            "every earlier config in this family carried 'no woman over fifty-five', which would have "
            "fought the casting on more than a third of these slots.\n\n"
            "SUPPLIERS: seedream, gpt_image, nbp_flash. nbp_pro excluded (seven waves of invented "
            "captions burnt into the image); flux2 excluded (0/8 on the glutathione before/after family, "
            "and it fabricates a stock-photo watermark); luma answers this brief family with HTTP 422.\n\n"
            "⚠️ RUN WITH `--candidates 1`. generate-multi.py never reads defaults.candidates from this "
            "file — it uses the --candidates flag, which defaults to 2 and would silently double the "
            "cost of the round.\n\n"
            "CLASS B, no reference images, no product in frame, 2048x2048 square."
        ),
        "target_template": "(not yet assigned — Malcolm to choose the blocks after review)",
        "labels_are_composited": "NOT composited. No text of any kind in the pixels: the theme's own text "
                                 "settings carry the labels so Translate & Adapt can translate them.",
        "defaults": {
            "candidates": 1,
            "negative_global": NEGATIVE_GLOBAL_AMATEUR if amateur_style else NEGATIVE_GLOBAL,
            "negative_class_b": "",
        },
        "slots": slots,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true",
                    help="print the twelve wave names and slot counts, write nothing")
    args = ap.parse_args()

    waves = []
    for concern_key in CONCERN_ORDER:
        for shot_key in SHOT_ORDER:
            waves.append(build_wave(concern_key, shot_key))

    # The bad-photograph style test. Malcolm, 2026-08-28: "do all of them for wrinkle
    # reduction and for skin firming" - so all three shot types on those two concerns.
    #
    # It is NOT run on brightening, and that is not an omission. A tone pair needs the two
    # halves matched for colour and brightness or the comparison is corrupted
    # (docs/clinical-trial-before-after-images.md §10), and this style's whole point is
    # wrong light that differs between the days. The two briefs contradict each other.
    # `repair` is left out simply because it was not asked for.
    for concern_key in AMATEUR_CONCERNS:
        for shot_key in SHOT_ORDER:
            waves.append(build_wave(concern_key, shot_key, style="amateur"))

    # The region bands, from Malcolm's seven reference pairs (2026-08-28): "we don't need any
    # more repair and brightening waves, we need more lines/wrinkle reduction and skin
    # firming." Frontal anatomical bands, on those two concerns only.
    for concern_key in REGION_CONCERNS:
        for shot_key in REGION_SHOTS:
            for strength in ("m30", "m50"):
                waves.append(build_wave(concern_key, shot_key, strength=strength))

    total = sum(len(w["slots"]) for w in waves)
    if args.list:
        for w in waves:
            print(f"{w['wave']:<52} {len(w['slots'])} slots")
        print(f"\n{len(waves)} waves, {total} slots")
        return

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for w in waves:
        path = OUT_DIR / f"{w['wave']}.json"
        path.write_text(json.dumps(w, indent=2, ensure_ascii=False) + "\n")
        print(f"wrote {path.relative_to(ROOT)}  ({len(w['slots'])} slots)")

    print(f"\n{len(waves)} waves, {total} slots, 1 candidate each across 3 suppliers "
          f"= {total * 3} images")
    print("Run each with:")
    print("  set -a; source ~/.claude/config/image-credentials.env; set +a")
    print("  python3 scripts/generate-multi.py configs/banners/<wave>.json \\")
    print("      --suppliers seedream,gpt_image,nbp_flash --candidates 1")


if __name__ == "__main__":
    main()
