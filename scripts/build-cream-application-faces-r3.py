#!/usr/bin/env python3
"""Build configs/banners/cream-application-faces-r3.json.

Round 3, 2026-08-31. Malcolm: "on the homepage - for the review carousel - we need
a new batch of images - showing close up face shots of beautiful caucasian women
models (are 35-40) gently applying a small swatch of light blue cream / dark blue
cream / pink cream / white cream / transparent serum - with their finger tip(s) -
to their face."

Round 2 (scripts/build-cream-application-faces.py) is the parent. It is left
untouched as the record of that round; this is a sibling because three things
change at once and they are not compatible with re-running round 2:

  1. CASTING is now 100% White European (round 2 was 60%, with East Asian, West
     African, South Asian and Middle Eastern slots that this brief excludes).
  2. TWO NEW SUBSTANCES - blush pink, and a transparent serum.
  3. The transparent serum needs its OWN swatch prose. Round 2's swatch paragraph
     asserts an OPAQUE substance that is "satin rather than glossy", which is the
     precise opposite of a clear serum, so reusing it would brief the fault in.

Everything that round 2 proved is carried over VERBATIM - framing, beauty/casting
prose, expression, fingertip contact, ground, camera, and the negative list. The
one-variable-at-a-time discipline is the whole point of the builder: shared prose
exists exactly once, and only the woman and the substance change per slot.
"""

import json
import pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "configs/banners/cream-application-faces-r3.json"

# ------------------------------------------------------------------ substances
# Every appearance/never string below is lifted VERBATIM from the product config
# that owns it, never paraphrased - the same rule the product photography runs on.
#   configs/copper-peptide-day-repair-cream.json    -> #2F4C9B  DARKBLUE
#   configs/copper-peptide-night-repair-cream.json  -> #A6C4E0  LIGHTBLUE
#   configs/matrixyl-3000-pro-collagen-cream.json   -> #F4F2EF  WHITE
#   configs/pdrn-collagen-repair-cream.json         -> #F3BFC2  PINK      (new)
#   configs/glutathione-brightening-serum.json      -> clear    CLEAR     (new)
#
# Day is the DARK blue and Night is the LIGHT blue. That reads backwards against
# the usual convention and has caught a session before - see the memory entry
# product-colours-2026-08. Each names the other as an explicit `never` so they
# cannot drift together.
SUBSTANCES = {
    "WHITE": {
        "word": "cream",
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
        "word": "cream",
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
        "word": "cream",
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
    # NEW this round.
    "PINK": {
        "word": "cream",
        "name": "SOFT BLUSH PINK",
        "hex": "#F3BFC2",
        "source": "PDRN Collagen Repair cream",
        "appearance": (
            "It is an opaque cream of a soft blush pink, colour #F3BFC2 - a gentle warm rose "
            "with plenty of light in it, clearly pink and clearly not white, and never a hot "
            "or fluorescent pink - smooth and satin rather than glossy"
        ),
        "never": "white, off-white, ivory, cream-coloured, hot pink, magenta, fuchsia, coral, red, "
                 "salmon, orange, golden, amber, yellow, blue, green",
    },
}

# NEW this round, and the one genuinely different problem in the wave. A clear
# serum is not a pale cream: it is a liquid, and every engine's default for
# "serum" is milky white (see the memory entry the-specs-never-describe-the-liquid).
# So transparency is asserted as something VERIFIABLE in the picture - her skin is
# visible THROUGH it - rather than as the adjective "transparent", which an engine
# can satisfy with a translucent white.
SERUM = {
    "word": "serum",
    "name": "COMPLETELY TRANSPARENT COLOURLESS",
    "hex": None,
    "source": "Glutathione / Matrixyl / Acetyl serum (all three are identical and untinted)",
    "appearance": (
        "It is a completely transparent, colourless liquid - water-clear and lightly viscous, "
        "reading only as refraction and highlight. Her own skin is plainly visible THROUGH it, "
        "with the pores and fine lines beneath it showing through undimmed and only slightly "
        "magnified, because there is no pigment in it at all - it has no colour of its own and "
        "adds none to the skin"
    ),
    "never": "white, milky, opaque, cream-coloured, cloudy, pearlescent, foamy, golden, amber, "
             "yellow, blue, pink, or any visible tint at all",
}

# ------------------------------------------------------------- the ten women
# All ten White European, per this brief. Complexion, hair colour, hair styling and
# eye colour are named per slot and no two repeat - left unnamed, every engine
# returns its own default face ten times over. Six are carried over unchanged from
# round 2 (they were well differentiated and had already been through a casting
# correction); four are new to bring the set to ten without repeating a colouring.
WOMEN = [
    # -- carried over from round 2 --
    ("01-FAIR-RED", "PINK",
     "Fair, freckled, red hair, green eyes",
     "one White European woman, Irish in colouring, with very fair cool-toned skin that "
     "flushes easily, a light scatter of freckles across the nose and cheekbones, "
     "coppery red hair, and clear green eyes",
     "swept back off the face and loosely pinned"),

    ("02-FAIR-ASHBLONDE", "LIGHTBLUE",
     "Fair, ash-blonde, pale blue eyes",
     "one White European woman, Scandinavian in colouring, with fair cool-toned skin, "
     "ash-blonde hair, and pale blue eyes",
     "worn straight and tucked behind the ear"),

    ("03-OLIVE-BRUNETTE", "DARKBLUE",
     "Light olive, dark brown hair, hazel eyes",
     "one White European woman, French in colouring, with light olive skin, dark brown "
     "hair, and hazel eyes",
     "swept back into a low loose knot"),

    ("04-MEDIUM-CHESTNUT", "WHITE",
     "Medium neutral, chestnut hair, grey-blue eyes",
     "one White European woman, English in colouring, with medium neutral-toned skin, "
     "chestnut brown hair, and grey-blue eyes",
     "worn loose and pushed back from the face"),

    ("05-OLIVE-BLACKHAIR", "LIGHTBLUE",
     "Warm olive, near-black hair, deep brown eyes",
     "one White European woman, Southern Italian in colouring, with warm olive skin, "
     "thick near-black hair, and deep brown eyes",
     "swept back off the face and loosely pinned"),

    ("06-FAIR-HONEYBLONDE", "WHITE",
     "Fair-medium warm, honey-blonde, amber eyes",
     "one White European woman, Dutch in colouring, with fair-to-medium warm-toned skin, "
     "honey-blonde hair, and light amber-brown eyes",
     "worn straight and tucked behind the ear"),

    # -- new this round --
    ("07-FAIR-DARKBLONDE", "CLEAR",
     "Fair cool, dark blonde, clear blue eyes",
     "one White European woman, German in colouring, with fair cool-toned skin, dark "
     "blonde hair, and clear blue eyes",
     "drawn back into a low ponytail well clear of the face"),

    ("08-FAIR-LIGHTBROWN", "DARKBLUE",
     "Fair neutral, light brown hair, blue-grey eyes",
     "one White European woman, Polish in colouring, with fair neutral-toned skin, light "
     "brown hair, and blue-grey eyes",
     "swept back into a low loose knot"),

    ("09-OLIVE-DARKCHESTNUT", "CLEAR",
     "Light-medium olive, dark chestnut hair, dark brown eyes",
     "one White European woman, Spanish in colouring, with light-to-medium olive skin, "
     "dark chestnut hair, and dark brown eyes",
     "worn loose and pushed back from the face"),

    ("10-VERYFAIR-PLATINUM", "PINK",
     "Very fair porcelain, platinum-ash blonde, ice-blue eyes",
     "one White European woman, Baltic in colouring, with very fair porcelain cool-toned "
     "skin, platinum-ash blonde hair, and pale ice-blue eyes",
     "worn close to the head and tucked behind both ears"),
]

# --------------------------------------------------------- the invariant prose
# Carried over verbatim from round 2. The age range is already what this brief asks
# for. NOTE the framing is deliberately NOT tighter than this: eight engine-runs
# across two brief families have shown a crop tighter than head-and-shoulders
# cannot be briefed on a face - the engine resolves it its own way and returns a
# portrait. Tighter crops are bought in post, on the winners only.
FRAMING = (
    "Editorial beauty photograph, square format, close on the face of {person}, between "
    "thirty five and forty years old, turned three quarters toward the camera so her near "
    "cheek faces the lens. The frame holds her from just above the eyebrows to the base of "
    "the neck, her cheek filling the middle of the picture."
)

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

# The OPAQUE swatch, carried over from round 2 AS CORRECTED. Round 2's first attempt
# gave the dab height, a soft peak and a crown highlight; four of five engines
# returned a whipped blob over a third of the cheek. Volume language reads as MORE
# CREAM. What worked was shrinking the yardstick to a fingertip, stating flatness
# outright, and stating the ratio of bare skin to cream. Exactly one piece of
# dimensionality survives - its own faint cast shadow - because without it round 1
# came back as flat painted discs and, in dark blue, as a clay mask.
SWATCH_CREAM = (
    "She is applying a tiny dab of {colour_name} cream to that cheekbone. {appearance}. "
    "The dab is TINY: smaller than her own fingernail, which is right beside it in the "
    "frame for comparison, and standing barely a millimetre proud of the skin - a small "
    "flat smear, not a blob, not a dollop and not a thick swipe. It has a soft slightly "
    "irregular edge and casts its own faint shadow, so it reads as a substance resting on "
    "her face rather than a colour painted onto it, and there is far more bare cheek "
    "visible around it than cream."
)

# The TRANSPARENT swatch. Same size discipline as the cream - the fingertip yardstick,
# the one-tenth ratio, the bare-skin ratio, the single cast shadow - but the optics are
# inverted. A cream is opaque and satin; a serum is clear and WET, so it is allowed the
# one bright specular highlight that would read as a whipped peak on a cream, and it is
# allowed to be flatter because a liquid slumps. Transparency is stated as a thing you
# can check in the picture (skin visible through it) rather than as an adjective.
SWATCH_SERUM = (
    "She is applying a tiny smear of {colour_name} serum to that cheekbone. {appearance}. "
    "It is ALREADY SPREAD ON HER SKIN, under her fingers - a thin wet film lying flat "
    "against the cheek, not a drop that has just fallen and not a raised bead sitting up "
    "on its own. It is TINY: smaller than her own fingernail, which is right beside it in "
    "the frame for comparison. It is wet and glossy where the cream version would be "
    "satin: one small bright specular highlight sits on it, its edge is a soft wet rim, "
    "and it casts its own faint shadow, so it reads as a clear liquid resting on her face "
    "rather than a pale substance smeared onto it. Because it is colourless, the ONLY "
    "things that reveal it are that highlight, the soft refraction at its rim, and the wet "
    "sheen - the skin underneath shows through it unchanged in colour. There is far more "
    "bare cheek visible around it than serum."
)

# The application. Round 2 briefed the fingertips as "resting against the near edge of
# the dab, barely in contact" and three of five engines put the hand near the cheek with
# a visible gap and the cream floating on its own: a qualifier attached to a verb weakens
# the verb. Fixed by asserting contact FIRST and qualifying pressure in a separate
# sentence afterwards.
FINGERTIPS = (
    "Her index and middle fingertips are touching the {word}: the pads of those two fingers "
    "OVERLAP its near edge and rest ON it, so the {word} passes underneath her fingertips "
    "and is partly hidden by them where they meet, with no gap whatever between her fingers "
    "and it - she has this moment begun to spread it. The "
    "contact is light. She is touching the {word}, not pressing into the cheek, and the skin "
    "beneath stays undisturbed and undimpled. Her hand is open and relaxed with the wrist "
    "low and the fingers gently curved and a little apart, so it frames the cheek from "
    "below without covering the face or hiding the {word}. Her nails are short with a clean "
    "natural manicure."
)

GROUND = (
    "Behind her a seamless deep graphite backdrop, colour #1A1A1A, falling to near-black at "
    "the edges - graphite throughout, never warm brown and never pale grey. One large soft "
    "key from the upper left models the cheekbone and jaw, with one dim cool fill on the "
    "shadow side."
)

CAMERA = (
    "85mm at f4, very shallow depth of field with the cheek and the {word} sharp, fine film "
    "grain, natural skin tones, quiet and expensive."
)

# Carried over verbatim from round 2, which earned every clause of it.
NEGATIVE_GLOBAL = (
    # what the swatch must never become
    "cotton bud, cotton swab on a stick, applicator stick, spatula, brush, warpaint, "
    "painted stripe, wide smear across the face, flat disc of colour, painted-on patch, "
    "paint, pigment, ink, dye, clay mask, mud mask, bruise, "
    # where it must never be
    "cream on the nose, cream on the forehead, cream on the lips, mask of cream, cream "
    "covering the cheek, dripping cream, runny cream, foam, glitter, shimmer, "
    # too much - round 2's smoke test came back with dollops on four of five engines, and
    # r3's own smoke test came back oversized on three of five AT NATIVE PIXELS
    "large blob of cream, dollop, generous scoop, thick swipe, whipped peak, cream covering "
    "a third of the cheek, cream wider than her fingertips, cream the size of her eye, "
    "cream larger than her fingernail, thick raised disc of cream, mound of cream, "
    # how the hand must never sit - "barely in contact" was read as "not in contact" in
    # round 2, and in r3's smoke test three of five still left a visible gap
    "fingers away from the cream, gap between the fingers and the cream, hand not touching "
    "the cream, cream sitting alone untouched on the cheek, fingers hovering above the "
    "cream, fingers pressing into the cheek, dimpled skin, hand flattened against the "
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
    "Square face close-ups, round 3, for the HOMEPAGE REVIEW CAROUSEL. Ten White European "
    "women aged 35-40, each applying a small swatch to the cheekbone. Five substances, two "
    "women each. 1:1, 2048x2048.\n\n"
    "PARENT: scripts/build-cream-application-faces.py (round 2, 2026-08-25), left untouched "
    "as the record of that round. Framing, beauty/casting prose, expression, fingertip "
    "contact, ground, camera and the whole negative list are carried over from it VERBATIM. "
    "Only casting policy and the substance set change.\n\n"
    "ONE VARIABLE AT A TIME. The shared prose exists exactly once in the builder, so only "
    "two things differ between slots: who she is, and what she is applying. Ten hand-copied "
    "prompts drift, and if the framing moved as well there would be no way to tell which "
    "difference was doing the work.\n\n"
    "CASTING IS 100% WHITE EUROPEAN this round, per Malcolm's brief - round 2's East Asian, "
    "West African, South Asian and Middle Eastern slots are deliberately absent. Ten "
    "colourings, no two sharing a complexion, hair colour or eye colour: left unnamed, every "
    "engine returns its own default face ten times over. Six are carried over from round 2 "
    "and four are new.\n\n"
    "EACH SUBSTANCE RUNS ON ONE FAIRER AND ONE OLIVE COMPLEXION, deliberately. How a pale "
    "blue or a blush pink reads is a function of the skin behind it, and the transparent "
    "serum is the extreme case - on very fair skin it has almost nothing to refract against. "
    "Pairing the complexions means the choice is informed rather than lucky.\n\n"
    "THE SWATCH IS MEASURED, AND MEASURED SMALL. Round 2's first attempt gave the dab "
    "height, a soft peak and a crown highlight, and four of five engines returned a whipped "
    "blob covering a third of the cheek: VOLUME LANGUAGE READS AS MORE CREAM. The corrected "
    "wording is what is carried here - the yardstick is a fingertip rather than an eye "
    "(smaller, and far less elastic), flatness is stated outright, the ratio of bare cheek "
    "to cream is stated, and the failure is negated by name. Exactly one piece of "
    "dimensionality survives, its own faint cast shadow, because without it round 1 came "
    "back as flat painted discs and in dark blue as a clay mask.\n\n"
    "THE APPLICATION IS CONTACT PRESSURE, NOT AN ADVERB. 'Delicate' does not survive five "
    "engines, and round 2's 'barely in contact' was resolved by three of them as NOT in "
    "contact, with the cream floating on its own. Contact is asserted first and the pressure "
    "qualified in a separate sentence after it.\n\n"
    "THE TRANSPARENT SERUM IS THE ONE REAL UNKNOWN and it gets its own swatch paragraph. "
    "Round 2's runs entirely on an OPAQUE substance that is 'satin rather than glossy', "
    "which is the exact opposite of a clear serum - reusing it would have briefed the fault "
    "in. Every engine's default for 'serum' is a milky white liquid, so transparency is "
    "asserted as something CHECKABLE in the rendered picture - her pores and fine lines are "
    "visible THROUGH it, undimmed - rather than as the adjective 'transparent', which an "
    "engine can satisfy with a translucent white. It is also allowed the one bright specular "
    "highlight and the wet meniscus that would read as a whipped peak on a cream.\n\n"
    "SUBSTANCE COLOURS ARE REAL PRODUCTS, lifted verbatim from the product configs rather "
    "than paraphrased. Dark blue is the Copper Peptide DAY cream #2F4C9B and light blue the "
    "NIGHT cream #A6C4E0 - Day is the DARK one, which reads backwards against convention and "
    "has caught a session before, so each names the other as an explicit never. White is the "
    "Matrixyl 3000 cream #F4F2EF. Pink is the PDRN Collagen Repair cream #F3BFC2 and is new "
    "this round. The clear serum is the Glutathione / Matrixyl / Acetyl formulation, which "
    "is the same untinted liquid in all three configs.\n\n"
    "NO PRODUCT IN FRAME, so there is no label to render, no reference image is sent, and "
    "nothing for FLUX.2 to invent a brand on - it is included, and this is the reference-free "
    "skin work it is actually good for. A reference would also drag the framing back to its "
    "own subject distance, which is wrong for a face this close.\n\n"
    "LUMA IS EXCLUDED. It refused this exact subject family throughout the 2026-08-25 session "
    "and costs three to four minutes per attempt to rediscover that. This is a documented "
    "bypass of the all-suppliers rule, not an oversight.\n\n"
    "SMOKE-TEST THE TWO NEW SUBSTANCES FIRST - slots 09 (CLEAR, olive) and 01 (PINK, fair) - "
    "across every supplier before fanning out the remaining eight. Round 2's own lesson: five "
    "images caught two brief faults and saved re-running forty.\n\n"
    "WHAT THE FIRST SMOKE TEST FOUND (2026-08-31, 10 images, 5 suppliers). The transparent "
    "serum WORKED on all five - no engine returned the milky white that was the main risk, and "
    "at native pixels the pores and fine lines read clearly THROUGH the fluid. The casting, "
    "graphite ground and beauty styling all held. Two faults, both recurrences of round 2's "
    "known failure modes, and BOTH INVISIBLE ON THE CONTACT SHEET - a 640px tile passed all "
    "ten images; only the native-pixel cheek crop showed them:\n"
    "  (a) SIZE. Three of five returned a swatch far larger than briefed - seedream a thick "
    "raised disc, nbp_flash a thick whipped swipe, flux2 a broad smear. The round-2 fingertip "
    "yardstick was being resolved upward. Two competing yardsticks were given ('no wider than "
    "a fingertip' AND 'one tenth the width of her cheek') and engines took the looser one, so "
    "the ratio is now dropped and the yardstick is HER OWN FINGERNAIL - a small hard object "
    "already in the frame, right beside the swatch, which makes the size checkable rather than "
    "asserted.\n"
    "  (b) CONTACT. Three of five left a visible gap, with the swatch sitting alone on the "
    "cheek - round 2's 'barely in contact' fault returning even though contact was asserted "
    "first. Adjacency is not contact: the fix is to require OVERLAP, so the swatch passes "
    "underneath her fingertips and is partly HIDDEN by them. A thing partly hidden by a finger "
    "cannot also be floating away from it.\n"
    "  (c) The serum specifically was described as a 'bead' 'domed by its own surface tension'. "
    "That is a pre-application droplet - a noun that means not-yet-touched - and it is why the "
    "serum drew the untouched-drop fault harder than the cream did. It is now a thin wet film "
    "ALREADY SPREAD under her fingers. Volume language reads as more substance; droplet "
    "language reads as an untouched one.\n"
    "  Only gpt_image hit both size and contact on the first pass. NOTE this fault may be "
    "latent in round 2 as well - that round was judged on contact sheets, at which all of this "
    "is invisible."
)


def build():
    slots = []
    for slot_id, key, short, person, hair in WOMEN:
        sub = SERUM if key == "CLEAR" else SUBSTANCES[key]
        word = sub["word"]
        swatch = SWATCH_SERUM if key == "CLEAR" else SWATCH_CREAM

        prompt = " ".join([
            FRAMING.format(person=person),
            swatch.format(colour_name=sub["name"], appearance=sub["appearance"]),
            FINGERTIPS.format(word=word),
            EXPRESSION,
            BEAUTY.format(hair=hair),
            GROUND,
            CAMERA.format(word=word),
        ])

        extra = [f"{word} that is {sub['never']}"]
        if key == "CLEAR":
            # The default failure for "serum" is a milky white liquid, so it is
            # negated in its own right as well as via the never string above.
            extra.append(
                "white lotion instead of a clear liquid, milky serum, opaque serum, "
                "cloudy serum, pearlescent serum, coloured serum, tinted serum, "
                "serum you cannot see through, skin hidden under the serum, "
                # r3 smoke test: three of five returned a raised untouched droplet, and
                # seedream's read faintly amber - a honey drop rather than a clear film
                "raised bead of liquid, droplet sitting alone on the cheek, single round "
                "drop, untouched drop, drop about to fall, dome of liquid, "
                "honey, syrup, oil, amber drop, golden drop"
            )
        if key == "PINK":
            # Guard the two ways a blush pink goes wrong: too hot, or bleached to white.
            extra.append("hot pink cream, fluorescent pink cream, magenta cream, white cream")
        extra.append("hand covering the face, smiling broadly, open mouth, teeth showing")

        slots.append({
            "id": f"CREAM-R3-{slot_id}-{key}",
            "title": f"{short} - {sub['name'].lower()} {word}",
            "substance": word,
            "substance_source": sub["source"],
            "substance_hex": sub["hex"],
            "class": "B",
            "width": 2048,
            "height": 2048,
            "target_slot": "homepage review carousel - square face close-up set",
            "prompt": prompt,
            "negative_extra": ", ".join(extra),
        })

    return {
        "wave": "cream-application-faces-r3",
        "created": "2026-08-31",
        "round": 3,
        "generated_by": "scripts/build-cream-application-faces-r3.py",
        "parent": "configs/banners/cream-application-faces.json",
        "doc": "docs/visual-identity/03-art-direction-and-briefs.md",
        "target_template": "templates/index.json",
        "target_section": "reviews",
        "note": NOTE,
        "defaults": {"candidates": 1, "negative_global": NEGATIVE_GLOBAL},
        "slots": slots,
    }


if __name__ == "__main__":
    cfg = build()
    OUT.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {OUT}  ({len(cfg['slots'])} slots)")
    by = {}
    for s in cfg["slots"]:
        by.setdefault(s["id"].rsplit("-", 1)[-1], []).append(s["title"])
    for k, v in by.items():
        print(f"  {k:10} x{len(v)}")
