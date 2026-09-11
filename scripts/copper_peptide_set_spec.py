"""The Copper Peptide three-product SET spec — written once, imported by every set builder.

Importable module, not a script. Consumers:
    scripts/build-copper-peptide-set-batch2.py      (10 studio/lifestyle compositions)
    scripts/build-copper-peptide-bathroom-batch3.py (10 close bathroom scenes)

WHY THIS EXISTS
Round 1 hand-wrote the three product blocks into all five of its slots. Round 2 moved them
into its own builder, which fixed the duplication inside that wave and did nothing about the
NEXT wave. By round 3 the label spec would have existed in three files, and the first time one
of them was corrected without the others, candidates from different waves would stop being
comparable - the whole point of fanning one brief across suppliers. So it lives here.

THE LABEL TEXT IS THE PART THAT CANNOT DRIFT. An unspecified label is an invented one; on this
project PDRN once came back as PORN. Every line of every container is quoted verbatim below
with the ink it is printed in, and the ink colours are explicitly marked as describing ink
rather than as words to set in type, because "BODY COPY" and "WHITE" have both been printed as
label text here before.

THE THREE BLUES ARE THE STANDING RISK. The line shares one carton blue but three different
CONTAINER blues - serum deep blue, Day cream deep navy, Night cream pale ice-blue. A
single-product shot cannot conflate them. A set shot does it by default, picking one blue and
painting all three, so SEPARATION is emitted into every slot rather than left to the
composition text to imply.

THE PRODUCTS ARE NAMED, NOT PLACED. Round 1 said LEFT / CENTRE / RIGHT inside the product
description, which welded the spec to a left-to-right row and made it useless for flat-lays,
clusters and pyramids. Each unit is identified here as THE DAY JAR / THE SERUM BOTTLE / THE
NIGHT JAR, and a composition places them by that name.

NEGATIVES DO NOT HOLD ON SCENE PROPS. Measured 2026-09-10: `set-e-vanity-daylight` returned a
sage-green bowl and a warm beige counter with "green" and "warm colour cast" both barred by
name in the negative. The bar works on the PRODUCTS and leaks on the SET DRESSING, so a
composition must state its surface and its palette as positive requirements and never rely on
the negative list to keep warmth out of a scene.

Author: Claude Code, 2026-09-11.
"""

REFS = "assets/images/_refs-2026-08-19"

REF_FILES = [
    f"{REFS}/copper-peptide-repair-serum/product_tight.png",
    f"{REFS}/copper-peptide-day-repair-cream/product_tight.png",
    f"{REFS}/copper-peptide-night-repair-cream/product_tight.png",
]

SHARED_RULES = (
    "SHARED RULES FOR ALL THREE. Every metal part is NEUTRAL SILVER-GREY brushed satin "
    "aluminium with a fine grain, staying neutral next to the blue glass - never rose-gold, "
    "copper, champagne, brass or warm-tinted, and never a chrome mirror. Reproduce each front "
    "label exactly as in the supplied reference, every character verbatim. The Skingenetix "
    "wordmark is spelled with a capital S and the rest lower case, with no trademark, "
    "registered or copyright symbol anywhere. On each container a narrow vertical rule sits to "
    "the left of the text block. The ink colours given below describe the INK each line is "
    "printed in and are NEVER themselves printed as words - no colour name appears as text "
    "anywhere. Each container carries ONLY the lines listed for it: no benefit lines, no "
    "'ALL SKIN TYPES', no ingredient list."
)

DAY_JAR = (
    "THE DAY JAR is a 50ml frosted DEEP NAVY BLUE glass cosmetic jar, wide and squat, about "
    "1.15 times wider than its full height, with a deep brushed satin aluminium screw lid "
    "standing about a third of the jar's total height and roughly half the height of the glass "
    "body beneath it - a tall band, not a thin disc. Its glass is rich deep navy at the top "
    "fading downward to pale frosted white at the base. Its label lines, in this order: (1) the "
    "Skingenetix DNA-helix mark with the wordmark 'Skingenetix'; (2) 'COPPER PEPTIDE' in bold "
    "capitals on one line; (3) 'ADVANCED DAY REPAIR'; (4) 'PREMIUM FORMULA'; (5) a small sun "
    "glyph then 'DAY CREAM  |  2% GHK-CU  |  50ML'. Inks: the mark, the wordmark, line 2, line "
    "4 and line 5 in white; line 3 and the vertical rule in light sky-blue."
)

SERUM_BOTTLE = (
    "THE SERUM BOTTLE is a 30ml frosted DEEP BLUE glass dropper bottle, straight-sided with "
    "square shoulders, fitted with a brushed satin aluminium collar and a white rubber-bulb "
    "pipette, and it stands taller than either jar. Its glass is a rich deep blue at the top "
    "fading downward to pale frosted at the base. The white rubber bulb is an ELONGATED CAPSULE "
    "about 1.6 times taller than wide, standing about one third the height of the glass body; "
    "bulb plus collar together about two thirds of it - never short, squat, stubby or "
    "ball-shaped. Its label lines, in this order: (1) the Skingenetix DNA-helix mark with the "
    "wordmark 'Skingenetix'; (2) 'COPPER PEPTIDE' in bold capitals on one line; (3) 'ADVANCED' "
    "then 'REPAIR SERUM' on two lines; (4) 'PREMIUM FORMULA'; (5) '2% GHK-CU  |  30ML' in small "
    "capitals. Inks: the mark, the wordmark, line 2, line 4 and line 5 in white; line 3 and the "
    "vertical rule in light cornflower-blue."
)

NIGHT_JAR = (
    "THE NIGHT JAR is a 50ml frosted PALE ICE-BLUE glass cosmetic jar of exactly the same shape "
    "and proportion as the day jar - about 1.15 times wider than its full height, same tall "
    "brushed satin aluminium lid. Its glass is a soft pale ice-blue, slightly deeper at the "
    "shoulders and lighter towards the base. Its label lines, in this order: (1) the Skingenetix "
    "DNA-helix mark with the wordmark 'Skingenetix'; (2) 'COPPER PEPTIDE' in bold capitals on "
    "one line; (3) 'ADVANCED NIGHT REPAIR'; (4) 'PREMIUM FORMULA'; (5) a small crescent-moon "
    "glyph then 'NIGHT CREAM  |  2% GHK-CU  |  50ML'. Inks: the mark, the wordmark, line 2, "
    "line 4 and line 5 in BLACK; line 3 and the vertical rule in strong royal-blue."
)

SEPARATION = (
    "THE THREE BLUES ARE THREE DIFFERENT BLUES AND MUST READ AS THREE IN ONE FRAME. The day jar "
    "is the darkest - a deep saturated navy. The serum bottle is a rich mid deep-blue, clearly "
    "lighter than the day jar and clearly darker than the night jar. The night jar is a soft "
    "pale ice-blue, the palest object of the three by a wide margin. Do not settle them into "
    "one shared blue and do not make any two of them match."
)

#: Luma has no negative-prompt field, so negatives fold into the prompt body and a long list
#: trips its content filter; it also caps at 6000 characters and answers a longer prompt with a
#: bare HTTP 422 that reads exactly like a content refusal. The trimmed spec below keeps every
#: LABEL LINE - those are the part that cannot be dropped without inviting an invented label -
#: and sheds the geometry prose.
SHARED_RULES_S = (
    "All metal is NEUTRAL SILVER-GREY brushed satin aluminium - never rose-gold, copper, "
    "champagne or a chrome mirror. Reproduce each front label exactly as in the supplied "
    "reference, every character verbatim. The wordmark is 'Skingenetix', capital S then lower "
    "case, no trademark or copyright symbol. A narrow vertical rule sits left of each text "
    "block. Ink colours below describe the INK and are NEVER printed as words. Each container "
    "carries ONLY its listed lines - no benefit lines, no 'ALL SKIN TYPES', no ingredient list."
)

DAY_JAR_S = (
    "THE DAY JAR is a 50ml frosted DEEP NAVY BLUE glass jar, about 1.15 times wider than its "
    "full height, with a tall brushed satin aluminium screw lid. Lines: the Skingenetix "
    "DNA-helix mark with 'Skingenetix'; 'COPPER PEPTIDE'; 'ADVANCED DAY REPAIR'; 'PREMIUM "
    "FORMULA'; a small sun glyph then 'DAY CREAM  |  2% GHK-CU  |  50ML'. Mark, wordmark, lines "
    "2, 4 and 5 in white; line 3 and the rule in light sky-blue."
)

SERUM_BOTTLE_S = (
    "THE SERUM BOTTLE is a 30ml frosted DEEP BLUE glass dropper bottle, square shoulders, "
    "brushed satin aluminium collar, white rubber-bulb pipette, taller than either jar; the bulb "
    "an elongated capsule about 1.6 times taller than wide, never squat or ball-shaped. Lines: "
    "the Skingenetix DNA-helix mark with 'Skingenetix'; 'COPPER PEPTIDE'; 'ADVANCED' then "
    "'REPAIR SERUM'; 'PREMIUM FORMULA'; '2% GHK-CU  |  30ML'. Mark, wordmark, lines 2, 4 and 5 "
    "in white; line 3 and the rule in light cornflower-blue."
)

NIGHT_JAR_S = (
    "THE NIGHT JAR is a 50ml frosted PALE ICE-BLUE glass jar of the same shape as the day jar. "
    "Lines: the Skingenetix DNA-helix mark with 'Skingenetix'; 'COPPER PEPTIDE'; 'ADVANCED "
    "NIGHT REPAIR'; 'PREMIUM FORMULA'; a small crescent-moon glyph then 'NIGHT CREAM  |  2% "
    "GHK-CU  |  50ML'. Mark, wordmark, lines 2, 4 and 5 in BLACK; line 3 and the rule in strong "
    "royal-blue."
)

SEPARATION_S = (
    "THREE DIFFERENT BLUES, AND THEY MUST READ AS THREE: the day jar the darkest deep navy, the "
    "serum bottle a rich mid deep-blue, the night jar a soft pale ice-blue and the palest of the "
    "three by a wide margin. Never one shared blue, never two matching."
)

#: One casting, shared by every wave that puts a person in frame, so the woman does not change
#: age, colouring or styling between waves and the candidates stay comparable. Malcolm asked
#: for 35. The skin instruction is deliberate: an unqualified "beautiful woman" renders as
#: airbrushed plastic on every engine, and pores, texture and a few freckles are what buy
#: realism back. No jewellery and short unpainted nails keep the eye on the product and remove
#: the hand detail engines most often mangle.
MODEL = (
    "THE MODEL is a White European woman of about 35 with natural, believable skin - visible "
    "pores, fine texture and a few small freckles, not airbrushed and not plastic. Light "
    "natural make-up, clean groomed brows, hair loosely gathered back off her face. Her "
    "expression is calm and unforced, a faint closed-mouth smile at most. She wears a simple "
    "cream or pale grey vest top with narrow straps. Her hands are clean with short natural "
    "nails and no nail polish, no rings, no bracelets and no watch."
)

MODEL_S = (
    "THE MODEL is a White European woman of about 35 with natural believable skin - visible "
    "pores and a few small freckles, not airbrushed. Light make-up, hair loosely gathered back. "
    "Calm unforced expression. A simple pale vest top. Clean hands, short natural nails, no "
    "polish and no jewellery."
)

NEGATIVE = (
    "rose-gold, copper-coloured metal, champagne metal, brass, gold, warm-tinted metal, chrome "
    "mirror finish, terracotta, amber, peach, blush pink, warm brown, teal, green, purple, warm "
    "colour cast, yellow lighting, all three containers rendered in the same shade of blue, "
    "matching blue containers, any printed word not listed in the brief, ingredient list, "
    "benefit lines, ALL SKIN TYPES, colour names printed as text, trademark symbol, registered "
    "trademark symbol, copyright symbol, watermark, signature, extra bottles, extra jars, "
    "duplicate products, more than three products, cardboard cartons, boxes, packaging boxes, "
    "hands, fingers, people, faces, text overlay, caption, flowers, leaves, plants, towels, "
    "cropped product, product touching the frame edge, blurry label, illegible lettering, "
    "misspelled lettering"
)

LUMA_CAP = 6000


#: What is actually INSIDE each jar, for any shot where a lid comes off. Taken verbatim from
#: the `formulation` blocks of configs/copper-peptide-{day,night}-repair-cream.json. Stated
#: because the specs never describe the liquid and every engine's default for an unnamed
#: skincare substance is milky white - which would make the day cream and the night cream
#: identical, the same conflation the container colours already have to fight.
DAY_CREAM_SUBSTANCE = (
    "THE DAY CREAM ITSELF is an opaque cream of a DEEP, SATURATED DARK BLUE, smooth and satin "
    "rather than glossy - richly tinted by the copper peptides it carries. Never white, "
    "off-white, ivory, cream-coloured, pale blue, golden or pink."
)

NIGHT_CREAM_SUBSTANCE = (
    "THE NIGHT CREAM ITSELF is an opaque cream of a SOFT LIGHT BLUE, clearly paler than the day "
    "cream, smooth and satin rather than glossy - lightly tinted by the copper peptides it "
    "carries. Never white, off-white, ivory, navy, dark blue, golden or pink."
)

OPEN_JAR = (
    "THE JAR IS OPEN. Its brushed satin aluminium lid is off, resting flat on the surface beside "
    "and slightly behind the jar with its top face showing. The glass rim and the screw thread "
    "are visible, and the cream inside comes right up to the rim and is peaked into a soft swirl "
    "where a fingertip has lifted some out, so it reads as a substance and not a flat disc."
)


def open_jar(which):
    """The OPEN_JAR paragraph, but naming WHICH jar is open.

    Needed the moment more than one product is in frame: `OPEN_JAR` says "THE JAR", which is
    unambiguous in a single-product shot and an invitation to open the wrong one - or all of
    them - in a set shot. Malcolm, 2026-09-11: the open-jar scenes must show all three products
    together with ONE pot open, so every set shot that opens a lid must say which lid.
    """
    return (
        f"THE {which} IS OPEN AND IT IS THE ONLY ONE THAT IS OPEN - every other product in the "
        f"frame stays closed with its lid on. The {which.lower()}'s brushed satin aluminium lid "
        "is off, resting flat on the surface beside and slightly behind it with its top face "
        "showing. Its glass rim and screw thread are visible, and the cream inside comes right "
        "up to the rim and is peaked into a soft swirl where a fingertip has lifted some out, "
        "so it reads as a substance and not a flat disc."
    )


def build_slot(slot_id, opening, arrangement, scene, frame, width=2048, height=2048,
               products=None, products_short=None, separation=True, extra=None,
               extra_short=None):
    """Assemble one generate-multi.py slot from the shared spec plus this composition's parts.

    `arrangement`, `scene` and `frame` are kept as three separate strings by every caller so a
    composition can be retuned on one axis without disturbing the other two - the lesson from
    the bundle-shot geometry, where three knobs all rode on one ratio and each only became
    visible once the one before it was freed.
    """
    # `products` lets a slot carry a SUBSET - the two jars without the serum, or one jar alone.
    # The three-way SEPARATION paragraph is only meaningful when all three are in frame, and on
    # a two-product shot it actively misleads by naming an object that is not there, so it is
    # switchable. Default stays all three, which is what waves 1-4 all want.
    prods = [DAY_JAR, SERUM_BOTTLE, NIGHT_JAR] if products is None else products
    prods_s = ([DAY_JAR_S, SERUM_BOTTLE_S, NIGHT_JAR_S]
               if products_short is None else products_short)
    sep = [SEPARATION] if separation else []
    sep_s = [SEPARATION_S] if separation else []

    prompt = "\n\n".join(
        [opening, SHARED_RULES] + prods + (extra or []) + sep + [arrangement, scene, frame])
    prompt_luma = "\n\n".join(
        [opening, SHARED_RULES_S] + prods_s + (extra_short if extra_short is not None else (extra or []))
        + sep_s + [arrangement, scene, frame])
    # Fail at build time, not an hour into a run: over the cap Luma returns a bare 422 that is
    # indistinguishable from a content refusal, and the backend is lost silently.
    if len(prompt_luma) >= LUMA_CAP:
        raise SystemExit(
            f"{slot_id}: prompt_luma is {len(prompt_luma)} chars, over Luma's {LUMA_CAP} cap")
    return {
        "id": slot_id,
        "width": width,
        "height": height,
        "class": "product-set",
        "ref_files": REF_FILES,
        "prompt": prompt,
        "prompt_luma": prompt_luma,
    }
