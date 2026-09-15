#!/usr/bin/env python3
"""Build configs/banners/serum-dropper-faces.json.

Round 4, 2026-09-15. Malcolm: "we need a new batch of these images - with the same model
briefing. but with close up application of the clear serum being applied to the face - similar
to the one i have just saved to the downloads folder."

The reference he saved is a MACRO: a clear glass pipette angled in from the upper right, one
drop hanging at its tip and one already resting on the cheekbone, the frame holding roughly one
eye and the cheek, skin texture and pores plainly visible, graphite ground.

WHY A SIBLING BUILDER AND NOT A FLAG ON r3 - and this is the whole reason this file exists:

    r3's clear-serum brief NEGATES the shot Malcolm has just asked for.

Its negative list carries "raised bead of liquid, droplet sitting alone on the cheek, single
round drop, untouched drop, drop about to fall, dome of liquid", because in r3 the serum had to
read as an already-spread film under her fingertips. Those clauses were earned - r3's smoke test
returned untouched droplets on three of five engines - but here the droplet IS the subject.
Re-running r3 with a different framing string would have briefed the subject out and produced a
confusing near-miss. Same judgement r3 itself made about round 2's opaque-swatch prose.

CARRIED OVER VERBATIM by import, so it exists once: WOMEN (the same ten women, same casting
prose, same hair), BEAUTY, EXPRESSION and GROUND. The substance is CLEAR for every slot, so the
woman is the only variable.

REPLACED: framing (much tighter), the swatch paragraph (a dropper and two drops, not a smear),
the fingertip paragraph (dropped entirely - no fingers touch the serum here), and the camera.

NO REFERENCE IMAGE and NO PRODUCT PROSE. Nothing branded is in frame - the pipette is bare
glass. Sending a product reference would only drag the framing back to the reference's distance,
and describing a labelled bottle invites one into the picture. flux2 is included for once, since
the bar on it applies to shots where branding is legible and it is strong on skin studies.

Author: Claude Code, 2026-09-15.
"""
import importlib.util
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "configs/banners/serum-dropper-faces.json"

_s = importlib.util.spec_from_file_location("r3", ROOT / "scripts/build-cream-application-faces-r3.py")
r3 = importlib.util.module_from_spec(_s)
_s.loader.exec_module(r3)

FRAMING = (
    "Extreme close-up beauty macro, square format, of the face of {person}, between thirty five "
    "and forty years old, turned three quarters away so her near cheek is presented flat to the "
    "lens. THE FRAME IS TIGHT: it holds only the outer corner of her near eye at the top left, "
    "the side of her nose at the lower left, and her cheek and cheekbone filling the whole "
    "centre and right of the picture. Her mouth, chin, hairline and jaw are all OUTSIDE the "
    "frame. Her skin is the subject: real texture, visible pores across the cheek, fine vellus "
    "hair catching the light along the jaw edge, a few small natural moles and a light freckle "
    "or two. Not retouched smooth, not plastic, not airbrushed."
)

DROPPER = (
    "A CLEAR GLASS PIPETTE enters from the upper right and angles down toward her cheekbone, "
    "held between the thumb and first finger of her own hand, of which only the fingertips and "
    "part of two fingers are in frame at the top right corner. The pipette is PLAIN UNMARKED "
    "GLASS - a slim transparent tube with a slight taper to a rounded tip, entirely colourless, "
    "carrying no printing, no measuring lines, no numbers and no label of any kind, and it is "
    "not attached to any bottle. Its tip stops a short distance clear of her skin, roughly one "
    "fingernail's width away, and does not touch her. "
    "TWO DROPS OF SERUM APPEAR, and no more than two. One hangs from the tip of the pipette, "
    "just about to fall, stretched very slightly by its own weight. The second has already "
    "landed on her cheekbone below it and rests there as a small round bead, no wider than half "
    "her fingernail, holding its own domed shape on the skin."
)

SERUM_LOOK = (
    "THE SERUM IS COMPLETELY TRANSPARENT AND COLOURLESS - water-clear, never milky, never "
    "cloudy, never white, never pearlescent and never tinted. It is visible ONLY as optics: one "
    "small bright specular highlight on the top of each drop, a bright refractive rim around "
    "the edge where it bends the light, and a faint soft shadow cast on the skin beneath the "
    "bead. Her skin shows THROUGH both drops, unchanged in colour, with the pores beneath the "
    "resting bead visibly magnified a little by its curve. That magnification and the highlight "
    "are what prove it is a clear liquid and not a pale substance."
)

CAMERA = (
    "100mm macro at f5.6, focus on the resting bead and the skin texture around it, the pipette "
    "tip a touch softer, the background thrown fully out. Fine film grain, natural skin tones, "
    "quiet and expensive."
)

NEGATIVE = (
    # the clear liquid going wrong - the one failure this brief must not repeat
    "milky serum, white lotion, opaque liquid, cloudy liquid, pearlescent, coloured serum, "
    "tinted serum, pink liquid, blue liquid, honey, syrup, oil, amber drop, golden drop, "
    # too much liquid
    "many drops, scattered droplets, spray, mist, water droplets all over the face, running "
    "down the cheek, dripping down the face, puddle, large drop, drop the size of her eye, "
    "wet face, sweat, tears, "
    # the pipette going wrong. NOTE: printed graduation digits are a known FLUX.2 trait on
    # glassware - it renders 100/50/10 and 500ml even when negated - so the pipette is asserted
    # as unmarked in the prompt body as well, not left to the negative alone.
    "graduation marks, measuring lines, printed numbers on the glass, scale markings, syringe, "
    "needle, plastic dropper, coloured dropper, rubber bulb in frame, bottle in frame, jar in "
    "frame, product packaging, label, logo, printed text, brand name, watermark, "
    # framing
    "full face, whole head, both eyes, mouth in frame, chin in frame, wide shot, portrait at a "
    "distance, two people, hand covering the cheek, fingers touching the serum, "
    # skin
    "plastic skin, airbrushed skin, poreless skin, heavy makeup, foundation, glitter, shimmer, "
    "acne, rash, redness, blemish, wrinkle filter, beauty filter"
)


def build():
    slots = []
    for slot_id, _key, short, person, hair in r3.WOMEN:
        prompt = " ".join([
            FRAMING.format(person=person),
            DROPPER,
            SERUM_LOOK,
            r3.EXPRESSION,
            r3.BEAUTY.format(hair=hair),
            r3.GROUND,
            CAMERA,
        ])
        slots.append({
            "id": f"SERUM-DROP-{slot_id}",
            "title": f"{short} - clear serum from a dropper, macro",
            "substance": "serum",
            "substance_source": "clear serum, no product in frame",
            "class": "B",
            "width": 2048,
            "height": 2048,
            "target_slot": "homepage review carousel - square macro set",
            "prompt": prompt,
            "negative_extra": NEGATIVE,
        })
    return {
        "wave": "serum-dropper-faces",
        "created": "2026-09-15",
        "doc": __doc__.strip().splitlines()[0],
        "note": ("Round 4. Same ten women as cream-application-faces-r3, clear serum only, "
                 "macro framing with a dropper. r3's anti-droplet negatives are deliberately "
                 "ABSENT - they would forbid the subject."),
        "defaults": {"class": "B"},
        "slots": slots,
    }


if __name__ == "__main__":
    cfg = build()
    OUT.write_text(json.dumps(cfg, indent=2) + "\n")
    print(f"{OUT.relative_to(ROOT)}")
    print(f"  slots      : {len(cfg['slots'])}")
    print(f"  prompt len : {min(len(s['prompt']) for s in cfg['slots'])}-"
          f"{max(len(s['prompt']) for s in cfg['slots'])} chars")
    print(f"  ref_files  : none (nothing branded is in frame)")
