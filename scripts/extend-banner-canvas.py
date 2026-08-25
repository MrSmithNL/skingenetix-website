#!/usr/bin/env python3
"""Widen a banner shot by extending its background off the left edge.

    python3 scripts/extend-banner-canvas.py --preview
    python3 scripts/extend-banner-canvas.py

The /collections/pdrn source is 2048x848 (2.41:1) with the model hard right. The
collection banner wants a wider frame with clear space on the left for the heading,
so the canvas grows leftward to 3:1 and the new area is filled with the shot's own
backdrop -- no crop, so the full height still shows in the header.

Padding flat charcoal would not survive a look, because the subject TOUCHES the
left edge: below y=632 the shoulder runs off frame. Repeating that edge column
would smear the shoulder into a horizontal bar. So the fill is built in two parts
and stitched at the shoulder line:

  background   the smooth backdrop, held at its own vertical gradient, which is
               extrapolated below y=632 from the clean rows above it
  shoulder     the edge profile SHEARED down as it travels left, continuing the
               real slope of the shoulder (~0.5px down per px left) so it sinks
               out of the bottom-left corner the way the actual shoulder does

Grain is resampled from the real backdrop -- a smoothed profile repeated across
500px reads as a flat plate next to film-grained pixels -- and a slight vignette
falls off to the left, which is how the original backdrop is already lit and keeps
white heading text clean.

Author: Claude Code, 2026-08-24.
"""
import argparse
import re
import numpy as np
from PIL import Image
from pathlib import Path
from scipy import ndimage

ROOT = Path(__file__).resolve().parent.parent

#: 3000 is the widest the pipeline keeps (upload-theme-images.py caps the long edge
#: there). The banner box is a FIXED height, so a wider frame is strictly better:
#: object-fit cover scales it by height alone and the surplus width becomes croppable
#: margin, which the template's object-position aims at the extension. Widening the
#: master is what lets these banners keep the theme's standard header height.
TARGET_WIDTH = 3000
#: Per-banner override, because "wide enough" is a property of the widest VIEWPORT the
#: banner has to survive, not of the pipeline. The box is 100vw x 440px, so its aspect
#: is viewport/440: 3.27:1 at 1440, 3.44:1 at 1512, 4.36:1 at 1920. A master narrower
#: than the box crops the HEIGHT. Measured live on /collections/copper-peptide at
#: 3000x848 (3.54:1): 100% of the height survived at 1440 and 1512 and only 81% at
#: 1920. To keep full height at 1920 the master has to reach ~4.36:1.
#: Going wider is close to free: object-position is anchored to the subject side, so
#: the surplus is cropped off the EXTENSION, never off the model.

QUALITY = 95            # matches .claude/rules/website-imagery.md rule 5: the CDN,
                        # not this script, does the compressing. No ICC is embedded
                        # either -- upload-theme-images.py strips metadata anyway.
EDGE_COLS = 6           # columns averaged into the edge profile
VIGNETTE = 0.13         # how far the far-left edge is darkened

BANNERS = {
    "pdrn": {
        "src": (ROOT / "assets/ai-generated/2026-08-22-multi-banner-library-pdrn-collagen-repair-cream"
                     / "pdrn-collagen-repair-cream--B-face-full-prod-right"
                     / "pdrn-collagen-repair-cream--B-face-full-prod-right-gpt_image_01.png"),
        "out": ROOT / "assets/publish-ready/collection-pdrn-banner",
        "desktop": "skingenetix-pdrn-collagen-repair-deep-renewal-cream.jpg",
        "mobile": "skingenetix-pdrn-collagen-repair-cream-face-mobile.jpg",
        #: right-anchored so the crop stays put however far the canvas grows
        "mobile_crop": (123, 721),      # (inset from right edge, width)
        "bg_fit": (380, 560),           # clean backdrop rows modelling the gradient
        "texture_box": (0, 555, 0, 820),
        #: the backdrop cloth has real weave and blotches worth carrying across
        "texture_mode": "tile",
        #: The model's shoulder TOUCHES the left edge below this row.
        "shoulder": {
            "y": 632,
            "skin_box": (662, None, 0, 460),
        },
    },
    # /pages/skin-repair-renewal -- the V1 frame, and READ THIS BEFORE "CORRECTING" IT
    # BACK. Malcolm picks from contact sheets on his Desktop named library-<product>-N.
    # "library-pdrncream-1" is a FILE, not a folder, and the batch it tiles is the v1
    # wave now sitting in assets/ai-generated/_superseded/pdrn-cream-v1-PORN-label/.
    # The current library folder holds the v2 REGENERATION, which is a different
    # photograph with the same shot id. A first pass read the folder instead of the
    # sheet and published the v2 frame; this is the correction.
    #
    # Same shot id, three places, all different pictures:
    #   _superseded/pdrn-cream-v1-PORN-label/...B-face-full-prod-right-gpt_image_01  <- this
    #   2026-08-22-multi-banner-library-pdrn-collagen-repair-cream/...same id        <- v2
    #   2026-08-22-multi-banner-library-pdrn-skin-repair-serum/...same id            <- serum
    #
    # THE BATCH NAME SAYS PORN-LABEL AND THIS FRAME IS STILL FINE. The fault hit "most
    # frames", not all; this one reads PDRN COLLAGEN REPAIR / DEEP RENEWAL TREATMENT /
    # PREMIUM FORMULA cleanly at 100% and at rendered size. Verify per frame, never per
    # batch - the folder name is a warning, not a verdict.
    #
    # Geometry is this photograph's own, not the v2 entry's:
    #   shoulder y=846  her shoulder only clips the last two rows of the left edge,
    #                   which is why the edge measures 17-18 all the way down and then
    #                   47.8 at row 847. Left as a shoulder rather than None precisely
    #                   so those two lit rows get replaced by the modelled backdrop
    #                   ramp - repeated across 1702px they would draw a bright hairline
    #                   along the bottom of the extension.
    #   shear 0.82      measured off the real edge: y=847 at x=0 to y=601 at x=300.
    #                   Steeper than pdrn v2's 0.62 and the day cream's 0.48, so the
    #                   shoulder leaves frame at the corner and nothing is carried.
    #   texture_box     (0,550,0,400) reads max 29. The v2 entry's (0,555,0,820) reads
    #                   max 195 on THIS frame - it clips her shoulder crest, and
    #                   mirror-tiling that is what printed ghosts on the day cream.
    "skin-repair-renewal": {
        "src": (ROOT / "assets/ai-generated/_superseded/pdrn-cream-v1-PORN-label"
                     / "pdrn-collagen-repair-cream--B-face-full-prod-right"
                     / "pdrn-collagen-repair-cream--B-face-full-prod-right-gpt_image_01.png"),
        "out": ROOT / "assets/publish-ready/page-skin-repair-renewal-banner",
        #: NEW filenames, not edits of the ones already uploaded. Shopify Files suffixes
        #: on a name collision rather than replacing, so re-using a name keeps serving
        #: the OLD picture - that has bitten this project three times.
        "desktop": "skingenetix-pdrn-collagen-repair-cream-skin-renewal-treatment.jpg",
        "mobile": "skingenetix-pdrn-collagen-repair-cream-renewal-mobile.jpg",
        "mobile_crop": (50, 950),
        "target_width": 3750,
        "bg_fit": (300, 550),
        "texture_box": (0, 550, 0, 400),
        "texture_mode": "tile",
        "shear": 0.82,
        "shoulder": {
            "y": 846,
            "skin_box": (800, None, 0, 300),
        },
    },
    # /collections/creams-moisturizers -- the copper peptide NIGHT cream frame, and the
    # tightest of the set so far, because this crop has no empty ground anywhere in it.
    #
    # WHICH EDGE. Measured both before choosing, and the answer is not obvious from
    # looking: the RIGHT edge is entirely lit - mean 137, minimum 48.9 - because her hand
    # and the jar occupy it top to bottom. The LEFT edge reads 2-27 for rows 0-660 (her
    # hair, near-black) and only then runs into her forearm. So left, despite the jar
    # already sitting on the right.
    #
    # THE ARM RISES AS IT LEAVES FRAME, which is why shear is NEGATIVE here and positive
    # everywhere else. Measured off the real edge: the arm's top is y=727 at x=150 and
    # y=680 at x=0, so travelling LEFT it climbs 47px over 150 - a shear of -0.31.
    # shear_curve is zeroed with it; the default 0.0035 is a downward steepening that
    # would fight the measured direction and swing the arm back down into frame.
    #
    # HOW MUCH ROOM THIS ACTUALLY BUYS. The clear zone is fixed by the original crop, not
    # by the extension - the window's left edge and the subject move together - so it is
    # 243px at 1280 and 403px at 1440 measured to the first original column. Her hair is
    # near-black for the first ~150px of that content though, and white text reads over
    # it perfectly well, which lifts the usable measure to roughly 321px and 480px.
    # That is the whole budget for this banner's heading; there is no widening it.
    "creams-moisturizers": {
        "src": (ROOT / "assets/publish-ready/collection-creams-moisturizers-banner"
                     / "_master-1999x848.png"),
        "out": ROOT / "assets/publish-ready/collection-creams-moisturizers-banner",
        "desktop": "skingenetix-copper-peptide-advanced-night-repair-cream-moisturizer.jpg",
        "mobile": "skingenetix-copper-peptide-night-repair-cream-moisturizer-mobile.jpg",
        #: right-anchored; keeps the jar (x 1378-1857 of 1999) with her whole face
        "mobile_crop": (49, 950),
        "target_width": 3750,
        #: rows 300-520 are the flattest, darkest run on this edge (2.3 down to 1.8),
        #: so the fitted ramp lands at ~1 where the real backdrop measures ~3. Fitting
        #: on 400-620 instead put it at 22 and printed a visibly lighter rectangle.
        "bg_fit": (300, 520),
        #: this edge is HAIR, never backdrop - see flat_backdrop in edge_profile()
        "flat_backdrop": True,
        #: rows 430-610 of the leftmost 70 columns: max 63, mean 3.8. Reaching wider or
        #: higher catches her hair highlight at 121-226, and mirror-tiling a highlight is
        #: what printed ghosts across the day cream banner.
        "texture_box": (430, 610, 0, 70),
        #: near-black at mean 3.8, so there is no weave worth carrying - scatter, as on
        #: the "all" banner, whose tiles drew faint vertical lines instead.
        "texture_mode": "scatter",
        "shear": -0.31,
        "shear_curve": 0.0,
        "shoulder": {
            "y": 680,
            "skin_box": (700, None, 0, 400),
        },
    },
    # /collections/copper-peptide -- the DAY CREAM frame Malcolm chose. Unlike the
    # serum frame tried first, her ARM touches this left edge: the leftmost columns
    # read backdrop (mean 16) down to row 739 and then jump to mean 87-141. So this
    # takes the pdrn treatment, with its own measured numbers rather than pdrn's.
    # /pages/brightening-glow -- subject and bottle on the LEFT, so the room is made
    # on the RIGHT. Measured before assuming: the rightmost columns read mean 24-31
    # with a max of 32 from top to bottom, i.e. flat backdrop, so nothing has to be
    # sheared out of frame.
    "brightening-glow": {
        "src": (ROOT / "assets/ai-generated/2026-08-22-multi-banner-library-glutathione-brightening-serum"
                     / "glutathione-brightening-serum--A-face-full-prod-left"
                     / "glutathione-brightening-serum--A-face-full-prod-left-gpt_image_01.png"),
        "out": ROOT / "assets/publish-ready/page-brightening-glow-banner",
        "desktop": "skingenetix-glutathione-brightening-radiant-glow-serum.jpg",
        "mobile": "skingenetix-glutathione-brightening-radiant-glow-serum-mobile.jpg",
        "side": "right",
        #: inset from the LEFT edge for a right-extended banner - the subject side.
        #: Keeps the bottle (x 60-350 of 2048) with her whole face.
        "mobile_crop": (0, 1000),
        #: 4.42:1, past the 4.36:1 the 100vw x 440px header reaches at a 1920 viewport
        "target_width": 3750,
        "bg_fit": (100, 700),
        #: ORIGINAL-frame coordinates, like every other banner: rows 0-400 across the
        #: last 700px (x 1348-2048) reads max 39 against a backdrop of ~31. Clean.
        "texture_box": (0, 400, 1348, 2048),
        "texture_mode": "tile",
        #: nothing touches the right edge - max 32 over the full height
        "shoulder": None,
    },
    "copper-peptide": {
        "src": (ROOT / "assets/ai-generated/2026-08-22-multi-banner-library-copper-peptide-day-repair-cream"
                     / "copper-peptide-day-repair-cream--D-face-full-eyes-open-right"
                     / "copper-peptide-day-repair-cream--D-face-full-eyes-open-right-gpt_image_01.png"),
        "out": ROOT / "assets/publish-ready/collection-copper-peptide-banner",
        "desktop": "skingenetix-copper-peptide-advanced-day-repair-cream.jpg",
        "mobile": "skingenetix-copper-peptide-day-repair-cream-face-mobile.jpg",
        #: right-anchored; keeps the jar (x 1132-1818 of 2048) with most of the face
        "mobile_crop": (150, 950),
        #: 4.42:1, past the 4.36:1 the 100vw x 440px box reaches at a 1920 viewport.
        #: Measured on the live page at 3.54:1: full height at 1440 and 1512, 81% at 1920.
        "target_width": 3750,
        "bg_fit": (300, 650),              # clean backdrop rows, well above the arm
        #: MEASURED, not eyeballed. (0,650,0,600) looked like backdrop and is not -
        #: it clips her shoulder (max luminance 174 against a backdrop of ~16), and
        #: mirror-tiling that across 1702px printed two dark lens-shaped ghosts in
        #: the extension. The subject first intrudes into cols 0-700 at row ~550,
        #: so the box stops at 400. Verified max 23.
        "texture_box": (0, 400, 0, 700),
        "texture_mode": "tile",
        #: measured off this photograph: the arm's top edge runs y=742 at x=0 to
        #: y=601 at x=290, i.e. 0.48 px down per px travelled left. pdrn's 0.62 would
        #: be the wrong angle for it.
        "shear": 0.48,
        "shoulder": {
            "y": 739,
            "skin_box": (760, None, 0, 460),
        },
    },
    # /collections/acetyl-hexapeptide-8 -- the easy case, and measured to confirm it:
    # the leftmost columns read mean 11-15 with a max of 16 from top to bottom, so
    # nothing touches this edge and no arm has to be sheared out of frame.
    # /collections/acetyl-hexapeptide-8 -- round 2 frame: the library original showed
    # only three of the label's seven elements and an opaque white fill, so it was
    # regenerated with the full label quoted and the serum described as a liquid.
    # Malcolm picked AHP8-R2-B-BIGGER nbp_pro_03.
    "acetyl-hexapeptide-8": {
        "src": (ROOT / "assets/ai-generated/2026-08-22-multi-collection-ahp8-r2"
                     / "AHP8-R2-B-BIGGER" / "AHP8-R2-B-BIGGER-nbp_pro_03.png"),
        "out": ROOT / "assets/publish-ready/collection-acetyl-hexapeptide-8-banner",
        "desktop": "skingenetix-acetyl-hexapeptide-8-argireline-anti-wrinkle-serum.jpg",
        "mobile": "skingenetix-acetyl-hexapeptide-8-argireline-serum-mobile.jpg",
        #: native 6336x2688; every measurement below is in working pixels
        "work_height": 848,
        #: right-anchored - the subject side - keeping the bottle with her face
        "mobile_crop": (30, 1050),
        "target_width": 3750,
        "bg_fit": (100, 400),
        #: measured on this frame at working size: rows 0-420 across cols 0-690 reads
        #: max 39 against a backdrop of ~22. The wider (0,940,0,2851) native box looks
        #: like backdrop and is not - max 150, her hair.
        "texture_box": (0, 420, 0, 690),
        #: scatter, not tile. Mirror-tiling this backdrop left a visible seam at the
        #: tile boundary: the largest column-to-column step in the extension measured
        #: 0.52 levels at x=698, which is the 690px tile width. The backdrop here is
        #: near-featureless, so there is no weave worth preserving anyway - the same
        #: conclusion the "all" banner reached.
        "texture_mode": "scatter",
        #: left edge is backdrop top to bottom, mean 17.9 max 21
        "shoulder": None,
    },
    # /collections/serums -- Malcolm replaced the J-pose frame with the A-face-full-prod-left
    # nbp_flash frame on 2026-08-25, and the swap FLIPS THE WHOLE BANNER.
    #
    # WHY THIS FRAME. Its label is the only reference-quality one in the acetyl set:
    # all six elements present, correctly spelled and cleanly drawn - helix as dots and
    # dashes, ACETYL HEXAPEPTIDE-8 with the hyphen, ANTI-WRINKLE with a real W, PREMIUM
    # FORMULA, and 10% ACETYL HEXAPEPTIDE-8 | 30ML. The same product's label failed twice
    # on 2026-08-25 elsewhere: the fine-lines banner dropped its last two lines entirely,
    # and SERUMS-R2-A seedream_01 mangled five of six.
    #
    # WHY THE SIDE CHANGED. The previous frame extended RIGHT. This one cannot: its right
    # edge is her neck and shoulder, mean luminance 160 with a minimum of 115 - lit skin
    # from the top row to the bottom, nothing to sample. The LEFT edge is the opposite,
    # measuring 21.3 to 26.4 with nothing above 45 anywhere down it, and a texture box
    # spanning the FULL height at max 30. So the canvas grows left, the heading moves to
    # the left with it, and object-position flips to right center.
    #
    # Projected heading ground after extension: 336px at 1280, 496px at 1440, 975px at
    # 1920 - roomier than any other banner published this week.
    "serums": {
        "src": (ROOT / "assets/ai-generated/2026-08-22-multi-banner-library-acetyl-hexapeptide-8-serum"
                     / "acetyl-hexapeptide-8-serum--A-face-full-prod-left"
                     / "acetyl-hexapeptide-8-serum--A-face-full-prod-left-nbp_flash_01.png"),
        "out": ROOT / "assets/publish-ready/collection-serums-banner",
        #: NEW filenames - Shopify Files suffixes on a name collision rather than
        #: replacing, so re-using the old pair would keep serving the OLD picture.
        "desktop": "skingenetix-acetyl-hexapeptide-8-anti-wrinkle-peptide-face-serum.jpg",
        "mobile": "skingenetix-acetyl-hexapeptide-8-anti-wrinkle-face-serum-mobile.jpg",
        #: native is 6336x2688; every measurement below is in working pixels
        "work_height": 848,
        #: inset from the RIGHT edge - the subject side for a LEFT-extended banner.
        #: Keeps the bottle (x 179-540 of 1999) with her whole face.
        "mobile_crop": (560, 1250),
        "target_width": 3750,
        "bg_fit": (100, 700),
        #: the full height is clean on this edge - cols 0-120 reads max 30 against a
        #: backdrop of ~24 - so the box does not have to stop short of a limb the way
        #: the previous frame's did.
        "texture_box": (0, 848, 0, 120),
        #: SCATTER, NOT TILE, and the max luminance is why that is not obvious. This box
        #: reads max 30 against a backdrop of 24, which looks clean by every threshold
        #: test - but it carries a faint vertical structure, and mirror-tiling it across
        #: 1751px printed seven evenly spaced dark lens shapes straight down the middle
        #: of the extension. Tiling amplifies structure that a max-luminance check cannot
        #: see, because the eye finds repetition long before it finds contrast.
        #: Independent per-pixel resampling has no tile boundaries to line up.
        "texture_mode": "scatter",
        #: nothing touches the left edge, which is the edge being extended
        "shoulder": None,
    },
    # /pages/the-science -- Malcolm's pick from the blue-glassware wave, 2026-08-24.
    # The easy case for the extender: measured across the left 400 columns the bench
    # runs mean 77.3, max 104, sd 7.9, and row 400 holds ~80 from x=0 out to x=500,
    # so nothing touches this edge and no arm has to be sheared out of frame. The
    # bench does carry a real vertical gradient (42 at the top, 88 at y=560, 70 at the
    # bottom), which edge_profile reproduces as measured rather than modelling.
    "the-science": {
        "src": (ROOT / "assets/ai-generated/2026-08-22-multi-banner-the-science-microscope"
                     / "the-science-scope--C-over-stage-type-left"
                     / "the-science-scope--C-over-stage-type-left-gpt_image_02.png"),
        "out": ROOT / "assets/publish-ready/page-the-science-banner",
        "desktop": "skingenetix-peptide-science-laboratory-research-banner.jpg",
        "mobile": "skingenetix-peptide-science-laboratory-research-mobile.jpg",
        #: right-anchored; keeps the glassware and the microscope stage together
        "mobile_crop": (648, 800),
        #: 4.42:1, past the 4.36:1 the 100vw x 440px box reaches at a 1920 viewport
        "target_width": 3750,
        "bg_fit": (150, 650),
        "texture_box": (150, 650, 0, 400),
        #: tile, not scatter. The bench's texture is mid-frequency MOTTLE, blobs of
        #: tens of pixels, and scatter resamples per pixel -- it turns that mottle into
        #: fine noise and the fill reads smooth against a textured original, which
        #: leaves the join visible even after the tone matches to 0.3 of a level.
        "texture_mode": "tile",
        #: This edge IS backdrop, so the measured profile is kept -- it just needs
        #: smoothing hard, because the bench's mottle was printing as horizontal
        #: stripes across the 1702px fill. flat_backdrop was tried and is wrong here:
        #: its straight-line ramp cannot follow a gradient that rises then falls, and
        #: it washed the far left several levels too light.
        "profile_smooth": 30.0,
        "shoulder": None,
    },
    # /pages/the-science, "Our Transparency Commitment" band. Malcolm's pick from the
    # evidence+microscope wave, 2026-08-25. Easiest edge of the set: the leftmost
    # column runs min 24, max 34, and column means hold 27-33 all the way out to
    # x=700, so nothing touches it and there is barely a gradient to preserve.
    "the-science-transparency": {
        "src": (ROOT / "assets/ai-generated/2026-08-22-multi-banner-the-science-evidence-scope"
                     / "the-science-eviscope--A-scope-behind-type-left"
                     / "the-science-eviscope--A-scope-behind-type-left-gpt_image_02.png"),
        "out": ROOT / "assets/publish-ready/page-the-science-transparency-banner",
        "desktop": "skingenetix-peptide-research-transparency-laboratory-banner.jpg",
        "mobile": "skingenetix-peptide-research-transparency-laboratory-mobile.jpg",
        #: right-anchored; keeps the gloved hands and the plate
        "mobile_crop": (40, 800),
        #: 4.42:1, past the 4.36:1 the 100vw x 440px box reaches at a 1920 viewport
        "target_width": 3750,
        "bg_fit": (100, 700),
        #: rows 0-848 cols 0-250 measures mean 31.0, max 39, sd 2.6 - flat dark bench
        "texture_box": (0, 848, 0, 250),
        #: scatter: at sd 2.6 there is no mottle structure worth tiling, and scatter
        #: cannot produce the mirror seams that tiling would over a 1702px fill.
        "texture_mode": "scatter",
        #: mild. The edge is nearly flat (10 levels top to bottom) so there is little
        #: gradient to lose, but the profile is still repeated across every column and
        #: the science bench showed what happens when row variation survives into it.
        "profile_smooth": 15.0,
        "shoulder": None,
    },
    # /collections/firming-skin-density -- jar right, so the canvas grows LEFT. The
    # right edge is 400 of 848 rows of lit skin (her arm), the left edge is backdrop
    # except the bottom 10 rows where her shoulder clips the corner - handled as a
    # shoulder so those rows are not dragged left as a streak.
    "firming-skin-density-collection": {
        "src": (ROOT / "assets/ai-generated/2026-08-22-multi-banner-library-matrixyl-3000-pro-collagen-cream"
                     / "matrixyl-3000-pro-collagen-cream--D-face-full-eyes-open-right"
                     / "matrixyl-3000-pro-collagen-cream--D-face-full-eyes-open-right-gpt_image_01.png"),
        "out": ROOT / "assets/publish-ready/collection-firming-skin-density-banner",
        "desktop": "skingenetix-matrixyl-3000-pro-collagen-full-firming-treatment.jpg",
        "mobile": "skingenetix-matrixyl-3000-collagen-firming-treatment-mobile.jpg",
        #: right-anchored - the subject side - keeping the jar with her face
        "mobile_crop": (30, 1000),
        "target_width": 3750,
        "bg_fit": (100, 700),
        #: rows 0-400 across cols 0-700 reads max 41 against a backdrop of ~29.
        #: (0,500,0,500) and (0,650,0,400) both look like backdrop and are not -
        #: max 172 and 187, her shoulder.
        "texture_box": (0, 400, 0, 700),
        #: scatter: this backdrop is near-featureless, and mirror-tiling one like it
        #: left a measurable seam at the tile boundary on the acetyl banner.
        "texture_mode": "scatter",
        #: only the last 10 rows, but left unhandled they smear across 1702px
        "shoulder": {
            "y": 836,
            "skin_box": (836, None, 0, 400),
        },
    },
    "all": {
        "src": ROOT / "assets/publish-ready/collection-all-banner/_master-retouched.png",
        "out": ROOT / "assets/publish-ready/collection-all-banner",
        "desktop": "skingenetix-peptide-skincare-copper-peptide-pdrn-range.jpg",
        "mobile": "skingenetix-copper-peptide-pdrn-serums-mobile-crop.jpg",
        "mobile_crop": (722, 620),
        "bg_fit": (80, 640),
        "texture_box": (0, 700, 0, 700),
        #: near-black and featureless, so there is no structure worth preserving --
        #: and mirror-tiling it drew faint vertical lines at every tile boundary.
        "texture_mode": "scatter",
        #: nothing touches this edge - it measures a mean luminance of 3 - so the
        #: extension is plain backdrop and no shoulder has to be carried.
        "shoulder": None,
    },
    # /collections/glutathione -- the EASY case, and only because it has already been
    # extended once. The library frame ran the forearm to the left edge, and seedream
    # was asked to widen it generatively to 4096x1256; that extension faded the arm
    # out, so this second pass starts from an edge that is pure backdrop. Measured on
    # the seedream master: the leftmost 6 columns run 2-36 (the 36 is the table at the
    # bottom, not skin) and the first column holding anything above 40 is x=123. So no
    # shoulder has to be carried and no shear applies.
    #
    # Downscaled to 848 tall FIRST, which is the height every other banner on this
    # store uses, so the five collection headers are one system rather than four plus
    # an odd one. It costs 4096 -> 2765 across the subject; the theme's srcset tops out
    # at 3000w, so none of that resolution was ever requested.
    "glutathione": {
        "src": (ROOT / "assets/publish-ready/collection-glutathione-banner"
                     / "_master-2766x848.png"),
        "out": ROOT / "assets/publish-ready/collection-glutathione-banner",
        "desktop": "skingenetix-glutathione-brightening-radiant-glow-serum.jpg",
        "mobile": "skingenetix-glutathione-brightening-serum-face-mobile.jpg",
        #: right-anchored; keeps the bottle (x 979-1958 of 2765) with most of the face
        "mobile_crop": (800, 950),
        #: 4.42:1, matching copper-peptide, so the full height survives to a 1920
        #: viewport. The live page measured at 3.26:1 keeps its height at 1440 and
        #: loses the bottle's base beyond ~1600.
        "target_width": 3750,
        "bg_fit": (250, 450),              # unused while shoulder is None; kept for shape
        #: MEASURED. (0,600,0,200) reads max 105 - that is the tip of her forearm, and
        #: resampling it into the extension would scatter skin-toned speckle across the
        #: dark. Stopping at x=120, three columns short of the arm, reads max 23.
        "texture_box": (0, 700, 0, 120),
        #: near-black at mean 9, so there is no weave worth mirror-tiling - the same
        #: reasoning as the "all" banner, whose tiles drew faint vertical lines.
        "texture_mode": "scatter",
        "shoulder": None,
    },
    # /pages/firming-skin-density -- the Matrixyl cream A-face-full-prod-left frame
    # Malcolm chose. NOT a collection page, but the hero is measured at exactly the
    # same 100vw x 440px box (checked live at a 1440 viewport: the band runs y=159 to
    # y=598), so the same 4.42:1 target applies unchanged.
    #
    # THE POSE NAME SAYS "prod-left" AND THE EXTENSION STILL GOES LEFT. That reads
    # backwards and is right: "left" describes where the jar sits inside the ORIGINAL
    # frame, and the right edge of that frame is 100% lit skin - her neck and shoulder
    # run off it at a mean luminance of 174 from the top row to the bottom. There is no
    # backdrop on that side to extend into, so a rightward extension would have to
    # invent shoulder, which is generative work this script cannot do honestly.
    # The left edge is the opposite: mean 22.5, max 24.9, nothing above 25 anywhere
    # down it, and the jar's own first column is x=121. So the canvas grows left, the
    # jar lands at 47-62% of the new frame, and the heading takes the dark it vacates.
    "firming-skin-density": {
        "src": (ROOT / "assets/publish-ready/page-firming-skin-density-banner"
                     / "_master-1999x848.png"),
        "out": ROOT / "assets/publish-ready/page-firming-skin-density-banner",
        "desktop": "skingenetix-matrixyl-3000-pro-collagen-firming-cream-skin-density.jpg",
        "mobile": "skingenetix-matrixyl-3000-firming-cream-face-mobile.jpg",
        #: right-anchored; keeps the jar (x 121-560 of 1999) with the whole face
        "mobile_crop": (760, 1000),
        "target_width": 3750,
        "bg_fit": (200, 600),              # unused while shoulder is None; kept for shape
        #: cols 0-100 measure max 28 over the FULL height, so the box can run the whole
        #: frame rather than stopping short of a limb the way the day cream's had to.
        "texture_box": (0, 848, 0, 100),
        #: near-black at mean 23 - no weave worth mirror-tiling, and tiling near-black
        #: drew faint vertical lines on the "all" banner.
        "texture_mode": "scatter",
        "shoulder": None,
    },
    # /collections/fine-lines-wrinkles -- the REPAIRED acetyl frame. The banner that
    # shipped here had a label missing its last two lines (PREMIUM FORMULA and the
    # 10% ACETYL HEXAPEPTIDE-8 | 30ML line); FLWFIX-nbp_flash_01 is the repair Malcolm
    # picked, chosen on two axes rather than one - a clean label is worthless if the
    # repair restaged the shot, and this one drifts only 4.40 mean abs from the original
    # against 7.6-9.1 for the gpt-image and seedream attempts.
    #
    # Extends RIGHT, matching the banner this replaces: her shoulder runs off the LEFT
    # edge (that edge measures mean 81.5 with a max of 183.8 - lit skin), while the right
    # edge is clean end to end at 26.1 to 33.3 with nothing above 45 anywhere down it.
    #
    # texture_box is written in ORIGINAL-frame coordinates and the script mirrors it for
    # a right-side extension. It has to stop at x=1899: her fingers reach x=1975, and the
    # boxes one step wider read max 212 where this one reads 36.
    "fine-lines-wrinkles": {
        "src": (ROOT / "assets/ai-generated/2026-08-22-multi-flw-bottle-text-fix"
                     / "FLWFIX" / "FLWFIX-nbp_flash_01.png"),
        "out": ROOT / "assets/publish-ready/collection-fine-lines-wrinkles-banner",
        #: NEW filenames - Shopify Files suffixes on collision rather than replacing, so
        #: re-using the old pair would keep serving the OLD, faulty-label picture.
        "desktop": "skingenetix-acetyl-hexapeptide-8-fine-lines-wrinkles-serum-banner.jpg",
        "mobile": "skingenetix-acetyl-hexapeptide-8-fine-lines-wrinkles-serum-mobile.jpg",
        "side": "right",
        "work_height": 848,
        #: inset from the LEFT edge - the subject side for a right-extended banner.
        #: Holds her face (x 600-1100) together with the bottle (x 1500-1760 of 1999).
        "mobile_crop": (550, 1300),
        "target_width": 3750,
        "bg_fit": (100, 700),
        "texture_box": (0, 300, 1899, 1999),
        #: SCATTER. This box reads max 36 against a backdrop of 32 - clean by every
        #: threshold - but the serums banner proved a box passing exactly that test can
        #: still carry faint vertical structure that mirror-tiling turns into evenly
        #: spaced dark lens shapes. Scatter has no tile boundaries to line up.
        "texture_mode": "scatter",
        #: nothing touches the right edge, which is the edge being extended
        "shoulder": None,
    },
    # /collections/brightening-glow -- NOT the same thing as the "brightening-glow"
    # entry above, which publishes to the PAGE /pages/brightening-glow using the
    # gpt_image frame. This one is the COLLECTION, which had no dedicated banner at all,
    # and Malcolm picked the nbp_flash frame of the same pose for it.
    #
    # EXTENDS LEFT, which is the opposite of the page entry's direction, because a
    # different engine's frame has different edges. Measured: the RIGHT edge carries her
    # neck and shoulder from row 264 to the bottom (mean 119.6, max 194.6), so there is
    # nothing to sample there; the LEFT edge is clean end to end at 18.1 to 24.0 with
    # nothing above 45 anywhere. Same pose, same product, opposite treatment - the edge
    # decides, not the pose name.
    #
    # KNOWN FAULT IN THIS FRAME, carried knowingly: the concentration line reads
    # '25i GLUTATHIONE | 30ML' where the product is 2%. At the rendered 440px band that
    # line is about 4px of cap height, so it is sub-legible - but it is still a wrong
    # concentration on a skincare product, and configs/banners/glut-a-bottle-text-fix.json
    # is the repair wave. Swap the src to the chosen repair when one is picked.
    #
    # texture_box has to stop at x=120: her fingers reach x=65 in the lower rows, and the
    # boxes one step wider read max 173-185 where this one reads 27.
    "brightening-glow-collection": {
        "src": (ROOT / "assets/ai-generated/2026-08-22-multi-banner-library-glutathione-brightening-serum"
                     / "glutathione-brightening-serum--A-face-full-prod-left"
                     / "glutathione-brightening-serum--A-face-full-prod-left-nbp_flash_01.png"),
        "out": ROOT / "assets/publish-ready/collection-brightening-glow-banner",
        #: deliberately distinct from the PAGE banner's filenames, which are
        #: skingenetix-glutathione-brightening-radiant-glow-serum{,-mobile}.jpg. Shopify
        #: Files suffixes on collision rather than replacing, so a near-miss name would
        #: quietly serve the page's picture here.
        "desktop": "skingenetix-brightening-glow-glutathione-radiant-serum-banner.jpg",
        "mobile": "skingenetix-brightening-glow-glutathione-radiant-serum-mobile.jpg",
        "work_height": 848,
        #: inset from the RIGHT edge - the subject side for a LEFT-extended banner.
        #: Holds the bottle (x 65-500 of 1999) together with her face.
        "mobile_crop": (620, 1350),
        "target_width": 3750,
        "bg_fit": (100, 700),
        "texture_box": (0, 400, 0, 120),
        #: scatter, per the serums banner: a box passing the max-luminance test can still
        #: carry vertical structure that mirror-tiling turns into repeated lens shapes.
        "texture_mode": "scatter",
        #: nothing touches the left edge, which is the edge being extended
        "shoulder": None,
    },
}


#: Duplicate keys in a dict literal are legal Python - the last one silently wins.
#: On 2026-08-25 a second "firming-skin-density" entry was added for the collection
#: while one already existed for the page, and the build ran the PAGE's source and
#: wrote the PAGE's filenames with no error at all. Two sessions edit this file, so
#: the collision is checked rather than trusted.
_keys = re.findall(r'^    "([a-z0-9-]+)": \{', Path(__file__).read_text(), re.M)
_dupes = {k for k in _keys if _keys.count(k) > 1}
if _dupes:
    raise SystemExit(f"duplicate banner keys in BANNERS: {sorted(_dupes)} - "
                     f"the later definition would silently win")

#: The arm is NOT extended across the new canvas. Dragging its edge profile sideways
#: gave a long, featureless ramp with no deltoid curve and no collarbone hollow -- it
#: read as a smeared arm, because a 1-D profile translated sideways has by
#: construction no variation along its length. Instead it leaves frame the way it
#: physically would: steeply, on a curve, falling out of the key light into the dark
#: backdrop. ARM_FADE is the distance over which it is gone.
#: Defaults measured off the pdrn shot. Each is a property of the PHOTOGRAPH, not of
#: the method, so a banner whose arm leaves at a different angle overrides them per
#: entry -- the copper-peptide day cream measures 0.48, and shearing it at 0.62 would
#: walk its arm out of frame at an angle the real one never had.
SHEAR = 0.62            # px down per px left at the join, measured off the real line
SHEAR_CURVE = 0.0035    # the line steepens as it recedes; drops it out by d~175
ARM_FADE = 190          # px over which the arm dissolves into backdrop shadow
JOIN_BLEND = 40         # columns over which the extension is matched to the original


def edge_profile(im, bg_fit, shoulder, flat_backdrop=False, smooth=2.0):
    """Left-edge colour profile, and the backdrop lighting to use behind it.

    Above the shoulder the profile IS backdrop, so it is used as measured -- that
    is what makes the join invisible, since the column next to the original then
    reproduces the original's own edge exactly. Only below the shoulder line, where
    the real profile is skin, does the backdrop have to be modelled: a straight
    ramp fitted on clean rows and carried down into the area the shoulder vacates.

    flat_backdrop MODELS THE WHOLE COLUMN INSTEAD, for the case that assumption
    fails: a crop where the extended edge is never backdrop at any height. The night
    cream D frame is one -- its left edge is her HAIR down to row 660 and her forearm
    below that, so "the profile is backdrop above the shoulder" is simply untrue, and
    using it repeats hair structure across every column of the extension. Measured on
    that frame: 22.7 luminance levels peak-to-peak of horizontal streaking, against
    the ~4 that a real backdrop edge produces. The ramp is still fitted on bg_fit
    rows, so it keeps the shot's own vertical falloff; it just carries no subject.

    The join stays invisible because JOIN_BLEND ramps the last columns onto the
    original's true edge regardless, and because a frame that needs this has a
    near-black edge anyway -- hair at 2-27 against a modelled backdrop at ~3.
    """
    #: `smooth` is for a DIFFERENT failure from flat_backdrop, and the two are not
    #: interchangeable. flat_backdrop is for an edge that is not backdrop at all, and
    #: replaces the profile with a fitted ramp. `smooth` is for an edge that IS
    #: backdrop but carries tonal mottle: the profile is repeated across every column
    #: of the fill, so any row-to-row variation left in it prints as a horizontal
    #: stripe the full width of the extension. Six averaged columns was not enough on
    #: the science bench and its 1702px fill came out banded.
    #: Reach for `smooth` first. flat_backdrop's ramp is a straight line, and on a
    #: profile that rises then falls -- this bench runs 42 at the top, 88 at y=560, 70
    #: at the bottom -- extrapolating that line washes the far edge several levels too
    #: light, which is exactly what it did here before this was separated out.
    prof = ndimage.gaussian_filter1d(im[:, :EDGE_COLS].mean(axis=1), smooth, axis=0)
    rows = np.arange(im.shape[0])
    if shoulder is None and not flat_backdrop:
        return prof, prof          # nothing on this edge but backdrop

    ys = np.arange(*bg_fit)
    ramp = np.stack([np.polyval(np.polyfit(ys, prof[ys, c], 1), rows) for c in range(3)],
                    axis=-1)
    if flat_backdrop:
        return prof, ramp
    hand_over = np.clip((rows - (shoulder["y"] - 40)) / 40.0, 0, 1)[:, None]
    return prof, prof * (1 - hand_over) + ramp * hand_over


def scatter(im, box, sigma, h, w, seed):
    """Detail lifted from a real region, resampled pixel-wise at random.

    Used for the extended shoulder. Mirror-tiling skin drew a faint diamond across
    it -- the tile boundaries line up into an outline the eye finds immediately,
    and shrinking the detail scale only made it fainter, never absent. Independent
    sampling has no boundaries to line up; the light blur afterwards puts the grain
    back to roughly pore size.
    """
    y0, y1, x0, x1 = box
    patch = im[y0:y1, x0:x1].astype(np.float64)
    detail = patch - ndimage.gaussian_filter(patch, (sigma, sigma, 0))
    rng = np.random.default_rng(seed)
    ys = rng.integers(0, detail.shape[0], size=h)
    xs = rng.integers(0, detail.shape[1], size=w)
    return ndimage.gaussian_filter(detail[np.ix_(ys, xs)], (0.8, 0.8, 0))


def texture(im, box, sigma, h, w):
    """Detail lifted from a real region of the shot, mirror-tiled to (h, w).

    A smoothed profile repeated 500px reads as a plate, so the actual grain is
    carried across and relit. Two regions get sampled: the backdrop's cloth weave,
    and the shoulder's skin, because an extension with no pores against real pores
    shows a seam even when the tone matches exactly.

    The backdrop patch stops well clear of the shoulder -- reading down to
    SHOULDER_Y caught its crest at y=581 and mirror-tiling that lump of lit skin
    dropped a floating leaf shape into the dark.
    """
    y0, y1, x0, x1 = box
    patch = im[y0:y1, x0:x1].astype(np.float64)
    detail = patch - ndimage.gaussian_filter(patch, (sigma, sigma, 0))
    ph, pw, _ = detail.shape
    ys = np.arange(h) % (2 * ph)
    ys = np.where(ys < ph, ys, 2 * ph - 1 - ys)
    xs = np.arange(w) % (2 * pw)
    xs = np.where(xs < pw, xs, 2 * pw - 1 - xs)
    return detail[np.ix_(ys, xs)]


def extend_left(im, extra, cfg):
    h = im.shape[0]
    shear = cfg.get("shear", SHEAR)
    shear_curve = cfg.get("shear_curve", SHEAR_CURVE)
    arm_fade = cfg.get("arm_fade", ARM_FADE)
    shoulder = cfg["shoulder"]
    prof, backdrop = edge_profile(im, cfg["bg_fit"], shoulder,
                                  cfg.get("flat_backdrop", False),
                                  cfg.get("profile_smooth", 2.0))
    out = np.zeros((h, extra, 3), dtype=np.float64)
    alpha = np.zeros((h, extra, 1), dtype=np.float64)
    rows = np.arange(h)

    for x in range(extra):
        d = extra - x                      # distance left of the original edge
        col = backdrop.copy()
        if shoulder is not None:
            shift = shear * d + shear_curve * d * d
            src = np.clip(rows - shift, 0, h - 1)
            lo = np.floor(src).astype(int)
            f = (src - lo)[:, None]
            sheared = prof[lo] * (1 - f) + prof[np.clip(lo + 1, 0, h - 1)] * f

            # Two things retire the arm together: the shoulder line dives out of the
            # bottom of the frame, and what is still in frame loses the key light.
            # Without the second, the surviving wedge is a flat ramp with no form.
            lit = max(0.0, 1.0 - d / arm_fade) ** 1.4
            a = np.clip((rows - (shoulder["y"] + shift)) / 8.0 + 0.5, 0, 1)[:, None] * lit
            col = backdrop * (1 - a) + sheared * a
            alpha[:, x] = a
        col = col * (1.0 - VIGNETTE * (d / extra) ** 2)
        out[:, x] = col

    # .get, not [], so adding a banner without this key degrades to the safer of the
    # two rather than dying with a KeyError three functions deep.
    if cfg.get("texture_mode", "scatter") == "tile":
        grain = texture(im, cfg["texture_box"], 25, h, extra)
    else:
        grain = scatter(im, cfg["texture_box"], 25, h, extra, seed=20260824)
    out += grain * (1 - alpha)

    # Null the join. The edge profile is an average of several columns, so it never
    # equals the original's actual first column, and the residual step reads as a
    # faint vertical line -- noise the eye ignores, a straight edge it does not.
    # Ramping the difference in over the last few columns removes it exactly.
    correction = im[:, 0] - out[:, -1]
    # Smoothed, and applied to BACKDROP only. A per-row correction ramped across 40
    # columns holds each row's value constant along its length, so where it lands on
    # skin it draws a comb of short horizontal lines -- clearly visible on the acetyl
    # shoulder. The backdrop is where a residual step actually shows as a line, and
    # there the correction has no fine detail to smear.
    correction = ndimage.gaussian_filter1d(correction, 3.0, axis=0)
    ramp = np.linspace(0.0, 1.0, JOIN_BLEND)
    backdrop_only = 1.0 - alpha[:, -JOIN_BLEND:]
    out[:, -JOIN_BLEND:] += correction[:, None, :] * ramp[None, :, None] * backdrop_only
    if shoulder is not None:
        y0, y1, x0, x1 = shoulder["skin_box"]
        box = (y0, h if y1 is None else y1, x0, x1)
        out += scatter(im, box, 5, h, extra, seed=20260824) * alpha
    return np.clip(out, 0, 255)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("banner", choices=sorted(BANNERS))
    ap.add_argument("--preview", action="store_true", help="write a PNG, skip the jpgs")
    args = ap.parse_args()
    cfg = BANNERS[args.banner]

    src = Image.open(cfg["src"]).convert("RGB")
    # Some library frames are far larger than the others (the acetyl J-pose is
    # 6336x2688). Bring the source to the working height FIRST: every measurement in
    # a banner's config -- shoulder row, texture box, mobile crop -- is in working
    # pixels, and extending at native size would build an 11k-wide float array to
    # reach the same aspect.
    work_h = cfg.get("work_height")
    if work_h and src.height != work_h:
        src = src.resize((round(src.width * work_h / src.height), work_h), Image.LANCZOS)
        print(f"source scaled to working height {work_h} -> {src.width}x{src.height}")

    im = np.array(src).astype(np.float64)
    h, w, _ = im.shape
    target = cfg.get("target_width", TARGET_WIDTH)
    extra = target - w
    if extra <= 0:
        raise SystemExit(f"source is already {w}px wide — nothing to extend")

    # Some frames put the subject on the LEFT, so the room has to be made on the
    # right. Rather than write a mirrored copy of extend_left -- its edge profile,
    # shear, texture tiling and join blend are all tuned and all assume a left edge --
    # the frame is flipped, extended, and flipped back. The result is identical in
    # orientation to the source, label included.
    side = cfg.get("side", "left")
    work = im[:, ::-1] if side == "right" else im
    # Every x in a banner's config is measured on the ORIGINAL frame, because that is
    # what a person looks at when writing one. extend_left sees the MIRRORED frame, so
    # those x ranges have to be mirrored with it. Forgetting this sampled the bottle
    # and hand as "clean backdrop" on the serums banner and tiled them across the
    # extension as ghosts.
    cfg = dict(cfg)
    if side == "right":
        def flip(box):
            y0, y1, x0, x1 = box
            return (y0, y1, w - x1, w - x0)
        cfg["texture_box"] = flip(cfg["texture_box"])
        if cfg.get("shoulder"):
            sh = dict(cfg["shoulder"])
            y0, y1, x0, x1 = sh["skin_box"]
            sh["skin_box"] = (y0, y1, w - x1, w - (x0 or 0))
            cfg["shoulder"] = sh
    wide = np.concatenate([extend_left(work, extra, cfg), work], axis=1)
    if side == "right":
        wide = wide[:, ::-1]
    final = Image.fromarray(wide.astype(np.uint8))
    print(f"{w}x{h} ({w/h:.2f}:1)  ->  {target}x{h} ({target/h:.2f}:1), "
          f"added {extra}px of backdrop on the {side}")

    out = cfg["out"]
    out.mkdir(parents=True, exist_ok=True)
    if args.preview:
        p = out / "_preview-extended.png"
        final.save(p)
        print(f"preview -> {p.relative_to(ROOT)}")
        return

    jpeg = dict(format="JPEG", quality=QUALITY, optimize=True, progressive=True,
                subsampling=0)
    final.save(out / cfg["desktop"], **jpeg)

    # Portrait crop for phones, measured in from the SUBJECT side so it stays on the
    # same part of the shot no matter how far the canvas grew. That is the right edge
    # for a left-extended banner and the left edge for a right-extended one -- anchor
    # it to the extension instead and the phone crop is a rectangle of empty backdrop.
    inset, cw = cfg["mobile_crop"]
    if side == "right":
        final.crop((inset, 0, inset + cw, h)).save(out / cfg["mobile"], **jpeg)
    else:
        right = target - inset
        final.crop((right - cw, 0, right, h)).save(out / cfg["mobile"], **jpeg)
    final.save(out / "_master-extended.png", optimize=True)

    for name in (cfg["desktop"], cfg["mobile"]):
        p = out / name
        iw, ih = Image.open(p).size
        print(f"{name:<56} {iw}x{ih}  {p.stat().st_size / 1024:>6.0f} KB")


if __name__ == "__main__":
    main()
