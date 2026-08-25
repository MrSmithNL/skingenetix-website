#!/usr/bin/env python3
"""Build configs/banners/cream-application-faces.json.

Round 2, 2026-08-25. Malcolm: "lets use beautiful models. and lets pay attention
to the swatch and the delicate application with their fingertips. also the dark
blue cream should be the same color as our Copper Peptide Day care cream. And
lets use 60% caucasian women. Lets also make sure we use women with different
complections and hair and eye color"

Written as a builder rather than hand-edited JSON for one reason: this wave holds
framing, lighting, ground, gesture and styling IDENTICAL across every slot, and
only the woman and the cream colour change. Ten hand-copied prompts drift. Here
the shared prose exists once and every slot interpolates it, so the invariant is
structural instead of a thing a session has to remember.
"""

import json
import pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "configs/banners/cream-application-faces.json"

# --------------------------------------------------------------- cream colours
# Lifted VERBATIM from the product configs, not paraphrased. The dark blue is the
# Copper Peptide DAY cream - and Day is the DARK one, which reads backwards
# against the usual convention and has caught a previous session.
#   configs/copper-peptide-day-repair-cream.json   -> #2F4C9B
#   configs/copper-peptide-night-repair-cream.json -> #A6C4E0
#   configs/matrixyl-3000-pro-collagen-cream.json  -> #F4F2EF
CREAMS = {
    "WHITE": {
        "name": "CLEAN NEUTRAL WHITE",
        "hex": "#F4F2EF",
        "source": "Matrixyl 3000 Pro-Collagen cream",
        "appearance": (
            "It is an opaque cream of a clean neutral white, colour #F4F2EF, smooth and "
            "satin rather than glossy, holding soft peaks"
        ),
        "never": "yellow, ivory, beige, golden, amber, pink, blue, teal, green, or any visible colour cast",
    },
    "LIGHTBLUE": {
        "name": "SOFT PALE LIGHT BLUE",
        "hex": "#A6C4E0",
        "source": "Copper Peptide NIGHT Repair cream",
        "appearance": (
            "It is an opaque cream of a soft light blue, colour #A6C4E0, pale and powdery and "
            "clearly not navy, smooth and satin rather than glossy - lightly tinted by the "
            "GHK-Cu copper peptides it carries"
        ),
        "never": "white, off-white, ivory, cream-coloured, navy, dark blue, golden, amber, yellow, pink",
    },
    "DARKBLUE": {
        "name": "DEEP SATURATED DARK BLUE",
        "hex": "#2F4C9B",
        "source": "Copper Peptide DAY Repair cream",
        "appearance": (
            "It is an opaque cream of a deep, saturated dark blue, colour #2F4C9B - a soft "
            "blue with light in it, not a flat navy and not black - smooth and satin rather "
            "than glossy, richly tinted by the GHK-Cu copper peptides it carries"
        ),
        "never": "white, off-white, ivory, cream-coloured, pale blue, powder blue, black, golden, amber, yellow, pink",
    },
}

# ------------------------------------------------------------- the ten women
# 6 of 10 White European = 60% exactly, as Malcolm asked. Complexion, hair and
# eye colour are named per slot and no two repeat - left unnamed, every engine
# returns its own default face six times over.
WOMEN = [
    ("01-EURO-FAIR-RED", "WHITE",
     "Fair, freckled, red hair, green eyes",
     "one White European woman, Irish in colouring, with very fair cool-toned skin that "
     "flushes easily, a light scatter of freckles across the nose and cheekbones, "
     "coppery red hair, and clear green eyes",
     "swept back off the face and loosely pinned"),

    ("02-EURO-FAIR-ASHBLONDE", "LIGHTBLUE",
     "Fair, ash-blonde, pale blue eyes",
     "one White European woman, Scandinavian in colouring, with fair cool-toned skin, "
     "ash-blonde hair, and pale blue eyes",
     "worn straight and tucked behind the ear"),

    ("03-EURO-OLIVE-BRUNETTE", "DARKBLUE",
     "Light olive, dark brown hair, hazel eyes",
     "one White European woman, French in colouring, with light olive skin, dark brown "
     "hair, and hazel eyes",
     "swept back into a low loose knot"),

    ("04-EURO-MEDIUM-CHESTNUT", "DARKBLUE",
     "Medium neutral, chestnut hair, grey-blue eyes",
     "one White European woman, English in colouring, with medium neutral-toned skin, "
     "chestnut brown hair, and grey-blue eyes",
     "worn loose and pushed back from the face"),

    ("05-EURO-OLIVE-BLACKHAIR", "LIGHTBLUE",
     "Warm olive, near-black hair, deep brown eyes",
     "one White European woman, Southern Italian in colouring, with warm olive skin, "
     "thick near-black hair, and deep brown eyes",
     "swept back off the face and loosely pinned"),

    ("06-EURO-FAIR-HONEYBLONDE", "WHITE",
     "Fair-medium warm, honey-blonde, amber eyes",
     "one White European woman, Dutch in colouring, with fair-to-medium warm-toned skin, "
     "honey-blonde hair, and light amber-brown eyes",
     "worn straight and tucked behind the ear"),

    ("07-EAST-ASIAN", "WHITE",
     "East Asian, light warm, black hair, dark brown eyes",
     "one East Asian woman, Korean in colouring, with light warm-toned skin, straight "
     "black hair, and dark brown eyes",
     "worn straight and tucked behind the ear"),

    ("08-WEST-AFRICAN", "LIGHTBLUE",
     "West African, deep brown, coiled black hair, dark brown eyes",
     "one Black woman of West African heritage, with deep richly pigmented brown skin, "
     "tightly coiled black hair worn close, and dark brown eyes",
     "worn close to the head and away from the face"),

    ("09-SOUTH-ASIAN", "DARKBLUE",
     "South Asian, warm mid-brown, near-black hair, dark brown eyes",
     "one South Asian woman of Indian heritage, with warm mid-brown skin, thick "
     "near-black hair, and dark brown eyes",
     "swept back into a low loose knot"),

    ("10-MIDDLE-EASTERN", "DARKBLUE",
     "Middle Eastern, light olive, dark brown hair, light hazel-green eyes",
     "one Middle Eastern woman, Lebanese in colouring, with light olive skin, dark brown "
     "hair, and striking light hazel-green eyes",
     "swept back off the face and loosely pinned"),
]

# --------------------------------------------------------- the invariant prose
FRAMING = (
    "Editorial beauty photograph, square format, close on the face of {person}, between "
    "thirty five and forty years old, turned three quarters toward the camera so her near "
    "cheek faces the lens. The frame holds her from just above the eyebrows to the base of "
    "the neck, her cheek filling the middle of the picture."
)

# Round 1 produced plain, unstyled faces because the brief asked for exactly that -
# "almost no makeup", "bare lips", and heavy makeup / glossy lips / lipstick / jewellery
# all sat in the negatives. Luxury beauty imagery is real texture AND campaign styling,
# not realism pushed until it reads as unkempt.
BEAUTY = (
    "She is a professional beauty-campaign model - genuinely beautiful, with fine balanced "
    "features, clearly defined cheekbones and a long neck, the calibre of face a luxury "
    "skincare house books for a campaign. Her skin is luminous and dewy and visibly well "
    "cared for, and it is still real skin: pores visible across the nose and cheek, fine "
    "expression lines at the outer eye, a few natural small marks, and fine down catching "
    "the light along the jaw, with an uneven sheen so some areas read matte and others "
    "softly lit. The texture never resolves into swirls, whorls, concentric rings or any "
    "repeating pattern anywhere, least of all on the cheek. Her makeup is the invisible "
    "kind used on beauty campaigns: the skin evened but never covered, brows groomed and "
    "defined, lashes darkened but her own, and lips softly tinted with a low natural sheen. "
    "Her hair is {hair}, clear of the cheek she is touching."
)

EXPRESSION = (
    "Her expression is calm, self-possessed and unposed, eyes open and looking softly past "
    "the camera just off the lens, lips closed and relaxed."
)

# The swatch. Round 1 came back as flat painted discs on several engines and, in dark
# blue, as opaque navy paint that read as a clay mask or a bruise. The fix is geometry
# stated as a measured ratio plus an explicit statement that it is a substance sitting
# on the face, not a colour applied to it. "A swab of cream" gets a cotton bud.
SWATCH = (
    "She is applying a tiny dab of {colour_name} cream to that cheekbone. {appearance}. "
    "The dab is very small and low: no wider than one of her own fingertips, about one "
    "tenth the width of her cheek, and standing barely a millimetre proud of the skin - a "
    "small flat-domed smear, not a blob and not a dollop. It has a soft slightly irregular "
    "edge and casts its own faint shadow, so it reads as a substance resting on her face "
    "rather than a colour painted onto it, and there is far more bare cheek visible around "
    "it than cream."
)

# The application. Round 1 gave flattened palms and fingers pressing into the cheek on
# several slots. Delicacy has to be described as contact pressure, not as an adverb.
FINGERTIPS = (
    "Her index and middle fingertips are touching the cream: the pads of those two fingers "
    "are in direct contact with the near edge of the dab, cream meeting skin, with no gap "
    "whatever between her fingers and it - she has this moment begun to spread it. The "
    "contact is light. She is touching the cream, not pressing into the cheek, and the skin "
    "beneath stays undisturbed and undimpled. Her hand is open and relaxed with the wrist "
    "low and the fingers gently curved and a little apart, so it frames the cheek from "
    "below without covering the face or hiding the cream. Her nails are short with a clean "
    "natural manicure."
)

GROUND = (
    "Behind her a seamless deep graphite backdrop, colour #1A1A1A, falling to near-black at "
    "the edges - graphite throughout, never warm brown and never pale grey. One large soft "
    "key from the upper left models the cheekbone and jaw, with one dim cool fill on the "
    "shadow side{deep_skin}."
)

CAMERA = (
    "85mm at f4, very shallow depth of field with the cheek and the cream sharp, fine film "
    "grain, natural skin tones, quiet and expensive."
)

NEGATIVE_GLOBAL = (
    # what the swab must never become
    "cotton bud, cotton swab on a stick, applicator stick, spatula, brush, warpaint, "
    "painted stripe, wide smear across the face, flat disc of colour, painted-on patch, "
    "paint, pigment, ink, dye, clay mask, mud mask, bruise, "
    # where the cream must never be
    "cream on the nose, cream on the forehead, cream on the lips, mask of cream, cream "
    "covering the cheek, dripping cream, runny cream, foam, glitter, shimmer, "
    # too much cream - round 2's smoke test came back with dollops on four of five engines
    "large blob of cream, dollop, generous scoop, thick swipe, whipped peak, cream covering "
    "a third of the cheek, cream wider than her fingertips, cream the size of her eye, "
    # how the hand must never sit - "barely in contact" was read as "not in contact"
    "fingers away from the cream, gap between the fingers and the cream, hand not touching "
    "the cream, fingers pressing into the cheek, dimpled skin, hand flattened against the "
    "face, palm over the cheek, fingers hiding the cream, cream already rubbed in, "
    # the whorl artefact Malcolm caught on the PDRN hero - the cheek is the subject here
    "swirling fingerprint whorls on the skin, concentric wavy micro-lines, repeating crepe "
    "pattern, plastic retouched skin, waxy skin, smoothed-away pores, mannequin, doll, "
    # bad makeup only - NOT makeup as such, which is what flattened round 1
    "cakey foundation, heavy contouring, obvious false lashes, dark matte lipstick, long "
    "nails, brightly painted nails, "
    # no product in frame, so nothing to invent a brand on. "numbers" is a FLUX.2 trait.
    "bottle, jar, tube, packaging, product, label, logo, brand mark, text, lettering, "
    "numbers, watermark, signature, "
    # casting and ground
    "teenager, child, elderly, grey hair, harsh flash, bright white background, pale grey "
    "background, warm brown background, cluttered background, two people"
)

NOTE = (
    "Square face close-ups, round 2. Ten women, each applying a small dab of cream to the "
    "cheekbone. 1:1.\n\n"
    "ONE VARIABLE AT A TIME. Framing, lighting, ground, gesture and styling are held "
    "IDENTICAL across all ten slots and only two things change: who she is, and the colour "
    "of the cream. This config is generated by scripts/build-cream-application-faces.py so "
    "that the shared prose exists exactly once - ten hand-copied prompts drift, and if the "
    "framing moved as well there would be no way to tell which difference was doing the "
    "work.\n\n"
    "CASTING IS NAMED PER SLOT. Six of the ten are White European (60%, per Malcolm) and "
    "no two of those six share a complexion, a hair colour or an eye colour. Left to the "
    "engine, 'different backgrounds' returns ten versions of its own default face.\n\n"
    "BEAUTIFUL, AND WHY ROUND 1 WAS NOT. Round 1 asked for 'almost no makeup' and 'bare "
    "lips' and negated heavy makeup, glossy lips, lipstick and jewellery - so every engine "
    "returned a plain, unstyled person, exactly as briefed. The negatives were forbidding "
    "the quality being asked for. This round casts explicit beauty-campaign models with "
    "campaign styling, and narrows the negatives to BAD makeup rather than makeup itself, "
    "while keeping the anti-plastic ones that stop it going waxy.\n\n"
    "THE SWATCH IS MEASURED, NOT NAMED. 'A swab of cream' returns a cotton bud or a "
    "warpaint stripe. Round 1 fixed that but still came back as flat painted discs on "
    "several engines, and in dark blue as opaque navy paint reading as a clay mask or a "
    "bruise. So the dab is now given a ratio - as wide as her eye is long, about one fifth "
    "of the cheek - plus height, a crown highlight and its own cast shadow, so it reads as "
    "a substance resting on the face rather than a colour painted onto it.\n\n"
    "THE APPLICATION IS CONTACT PRESSURE, NOT AN ADVERB. 'Delicate' does not survive five "
    "engines. The fingertips touch the cream and not the cheek, the skin beneath is "
    "undimpled, and the hand frames from below without covering.\n\n"
    "CREAM COLOURS ARE REAL PRODUCTS. Dark blue is the Copper Peptide DAY cream #2F4C9B, "
    "per Malcolm - and Day is the DARK one, which reads backwards against convention and "
    "has caught a session before. Light blue is the Copper Peptide NIGHT cream #A6C4E0 and "
    "white is the Matrixyl 3000 cream #F4F2EF. All three appearance strings are lifted "
    "verbatim from the product configs. Dark blue runs 4 times, light blue and white 3 "
    "each.\n\n"
    "NO PRODUCT IN FRAME, so there is no label to render and nothing for FLUX.2 to invent a "
    "brand on - it is included, and this is the reference-free skin work it is actually "
    "good for. Luma is left out: it refused this subject family throughout the 08-25 "
    "session and costs three to four minutes per attempt to find that out again."
)


def build():
    slots = []
    for slot_id, cream_key, short, person, hair in WOMEN:
        cream = CREAMS[cream_key]
        deep_skin = (
            ", lit so deep skin keeps its full range rather than being underexposed"
            if "WEST-AFRICAN" in slot_id else ""
        )
        prompt = " ".join([
            FRAMING.format(person=person),
            SWATCH.format(colour_name=cream["name"], appearance=cream["appearance"]),
            FINGERTIPS,
            EXPRESSION,
            BEAUTY.format(hair=hair),
            GROUND.format(deep_skin=deep_skin),
            CAMERA,
        ])
        extra = [f"cream that is {cream['never']}"]
        if "WEST-AFRICAN" in slot_id:
            extra.append("lightened skin, ashy skin, underexposed face")
        if "SOUTH-ASIAN" in slot_id:
            extra.append("bindi, decorative face markings")
        if "MIDDLE-EASTERN" in slot_id:
            extra.append("headscarf, hijab, veil")
        extra.append("hand covering the face, smiling broadly, open mouth, teeth showing")

        slots.append({
            "id": f"CREAM-{slot_id}-{cream_key}",
            "title": f"{short} - {cream['name'].lower()} cream",
            "cream_source": cream["source"],
            "cream_hex": cream["hex"],
            "class": "B",
            "width": 2048,
            "height": 2048,
            "target_slot": "square face close-up set",
            "prompt": prompt,
            "negative_extra": ", ".join(extra),
        })

    return {
        "wave": "cream-application-faces",
        "created": "2026-08-25",
        "round": 2,
        "generated_by": "scripts/build-cream-application-faces.py",
        "doc": "docs/visual-identity/03-art-direction-and-briefs.md",
        "note": NOTE,
        "defaults": {"candidates": 1, "negative_global": NEGATIVE_GLOBAL},
        "slots": slots,
    }


if __name__ == "__main__":
    cfg = build()
    OUT.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {OUT}  ({len(cfg['slots'])} slots)")
