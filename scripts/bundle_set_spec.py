"""Set-shot spec for ANY bundle of Skingenetix products — the generalised successor to
`copper_peptide_set_spec.py`.

Importable module, not a script. Consumer: `scripts/build-bundle-set.py`.

WHY THIS REPLACES THE COPPER-ONLY MODULE
`copper_peptide_set_spec.py` hardcodes three products, their label text and one three-blue
separation paragraph. Nine more bundles need the same treatment across all nine products, and
copying that module per line would put the label spec in a dozen files. Here the per-product
block is READ from `configs/<product>.json`, which already quotes every front label verbatim,
line by line, with the "ink colours are never printed as words" clause. Nothing is restated.

DROPPING LUMA IS WHAT MADE THAT POSSIBLE. Luma caps at 6000 characters, which forced a second,
hand-trimmed copy of every product spec purely to fit — the exact duplication this module
exists to remove. Malcolm dropped luma for the bundle rollout on 2026-09-11 after it scored
0 selections from 36 across the whole Copper Peptide run, so there is now one spec per product
and it is the one already on disk.

THE SEPARATION CLAUSE IS THE PART THAT ACTUALLY MATTERS, and it is not one paragraph any more.
A set shot's default failure is that the engine makes the products look alike. How you fight
that depends entirely on how the real products differ, and the range has three distinct cases:

  LADDER   — the products differ in what they READ AS. Name them darkest to lightest and
             forbid a match. This is the proven Copper Peptide wording.
  SHAPE    — the products genuinely SHARE a colour and differ only in form. The clause must
             say the shared colour is CORRECT, or an engine "helpfully" tints one to tell
             them apart.
  LABEL    — same colour AND same form. Matrixyl, Glutathione and Acetyl serums are all the
             same frosted CLEAR glass with the same silver collar and the same colourless
             contents, so all three read transparent. They differ only in printed label text
             and accent-rule colour. Hardest case in the range: no colour lever at all.

A fourth clause rides alongside these: CLEAR vs OPAQUE. Every bottle here is frosted CLEAR
glass and takes its apparent colour from the liquid inside, so the colourless serums read
see-through while every cream jar reads solid. A bundle mixing the two must say so, or the
clear bottle renders as a solid white one.

WHY THE LABEL CASE NEEDS ITS OWN NEGATIVE. Acetyl's accent is deliberately monochrome silver-
grey. That is exactly what an engine produces when it garbles a coloured rule — so a Matrixyl
bottle whose teal rule fails does not look broken, it looks like a correct Acetyl bottle. The
fault is invisible unless you read the label text. `separation()` therefore returns a negative
fragment as well as a prompt paragraph, and the builder must append it.

Author: Claude Code, 2026-09-11.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REFS = ROOT / "assets" / "images" / "_refs-2026-08-19"

#: key -> everything a brief needs about one product.
#:   config  the per-product photography spec; `product_desc` is the verbatim label block
#:   name    how a composition refers to it, e.g. "{A}" resolves to this
#:   form    bottle | jar. Decides which compositions can apply and drives SHAPE separation.
#:   body    colourless | tinted | opaque — THE CONTENTS, never the glass. A serum is a
#:           translucent liquid (tinted or not); a cream is opaque. The glass is frosted
#:           on all nine.
#:   colour  what the filled container READS AS. Drives LADDER separation.
#:   value   0 = darkest, 100 = lightest/clearest. Only used to order a ladder; never printed.
#:   accent  the accent-rule colour on the label. The only lever LABEL separation has.
#:
#: THE GLASS IS FROSTED ON ALL NINE PRODUCTS. That is the constant, and it took two
#: corrections from Malcolm to state it correctly.
#:
#: What varies is the LIQUID INSIDE, and the frosted glass takes its apparent colour from it.
#: Copper Peptide reads blue because its serum is blue; PDRN reads pink because its serum is
#: pink; Matrixyl, Glutathione and Acetyl read pale and neutral because their liquid is
#: COLOURLESS — not because the glass is white. Every cream jar reads solid because opaque
#: cream fills it.
#:
#: Two wrong versions preceded this one, and the second was worse than the first. Version one
#: took `colour` from the phrase "frosted NEUTRAL WHITE glass" in each product_desc and so
#: recorded the Matrixyl serum and cream as sharing one colour — briefing them as
#: interchangeable whites. Malcolm: "the Matrixyl serum is transparent. the cream is white."
#: Version two then swung too far and called those three bottles CLEAR AND SEE-THROUGH, with a
#: clause telling every engine the background must be visible THROUGH the glass. Malcolm again:
#: "the glass of the bottle ... are all frosted glass - the same as the other products. Its only
#: the color of the liquid inside that is transparent." Clear see-through glass is a different
#: product from frosted glass, so that brief was as wrong as the first, in the opposite
#: direction.
#:
#: `body` therefore describes THE CONTENTS, never the glass: `colourless` or `opaque`.
PRODUCTS = {
    "cp_serum": dict(
        config="copper-peptide-repair-serum", name="THE COPPER PEPTIDE SERUM BOTTLE",
        form="bottle", body="tinted", colour="deep blue", value=30,
        accent="light cornflower-blue"),
    "cp_day": dict(
        config="copper-peptide-day-repair-cream", name="THE COPPER PEPTIDE DAY CREAM JAR",
        form="jar", body="opaque", colour="deep navy blue", value=15,
        accent="light sky-blue"),
    "cp_night": dict(
        config="copper-peptide-night-repair-cream", name="THE COPPER PEPTIDE NIGHT CREAM JAR",
        form="jar", body="opaque", colour="pale ice-blue", value=70,
        accent="strong royal-blue"),
    "pdrn_serum": dict(
        config="pdrn-skin-repair-serum", name="THE PDRN SERUM BOTTLE",
        form="bottle", body="tinted", colour="dusty rose-pink", value=55,
        accent="soft rose-pink"),
    "pdrn_cream": dict(
        config="pdrn-collagen-repair-cream", name="THE PDRN NIGHT CREAM JAR",
        form="jar", body="opaque", colour="pale rose-pink", value=65,
        accent="soft rose-pink"),
    "mat_serum": dict(
        config="matrixyl-3000-pro-collagen-serum", name="THE MATRIXYL 3000 SERUM BOTTLE",
        form="bottle", body="colourless", colour="pale neutral, untinted", value=100,
        accent="deep emerald-teal"),
    "mat_cream": dict(
        config="matrixyl-3000-pro-collagen-cream", name="THE MATRIXYL 3000 CREAM JAR",
        form="jar", body="opaque", colour="opaque white", value=85,
        accent="deep emerald-teal"),
    "glut_serum": dict(
        config="glutathione-brightening-serum", name="THE GLUTATHIONE SERUM BOTTLE",
        form="bottle", body="colourless", colour="pale neutral, untinted", value=100,
        accent="champagne gold"),
    "acetyl_serum": dict(
        config="acetyl-hexapeptide-8-serum", name="THE ACETYL HEXAPEPTIDE-8 SERUM BOTTLE",
        form="bottle", body="colourless", colour="pale neutral, untinted", value=100,
        accent="monochrome silver-grey, with no coloured accent at all"),
}

#: Emitted whenever a bundle mixes see-through and solid containers. Without it an engine
#: renders a clear bottle as an opaque white one, which is the specific fault Malcolm caught.
#: Emitted whenever a bundle mixes colourless and opaque CONTENTS. The glass is frosted on
#: every product, so this says nothing about the glass — only about what is behind it.
CONTENTS_CLAUSE = (
    "WHAT IS INSIDE EACH CONTAINER, WHICH IS WHAT GIVES IT ITS COLOUR. Every container here is "
    "the same FROSTED glass - softly matte and translucent, never clear see-through glass and "
    "never opaque plastic. {parts} That difference comes from the CONTENTS: do not change the "
    "glass itself, and do not tint anything to exaggerate it."
)

ALL_COLOURLESS_CLAUSE = (
    "WHAT IS INSIDE EACH CONTAINER. Every container here is the same FROSTED glass - softly "
    "matte and translucent, never clear see-through glass and never opaque plastic - and every "
    "one holds a COLOURLESS liquid. With no tint behind the frosting they read pale and "
    "neutral. Do not give the glass or the liquid any colour, and do not render them as solid "
    "milky white plastic."
)

#: How each contents type reads through frosted glass, phrased for the brief. Two forms,
#: because one product takes a singular verb and several take a plural one, and a brief that
#: reads "THE SERUM BOTTLE hold a colourless liquid" is a brief someone will stop trusting.
CONTENTS_PHRASE = {
    "colourless": ("hold{s} a COLOURLESS liquid, so there is no tint behind the frosting and "
                   "{they} read{r} pale and neutral, lighter and less dense than the others"),
    "tinted": ("hold{s} a TRANSLUCENT TINTED liquid, so the frosted glass takes that colour and "
               "read{r} as a soft, light-filled colour rather than a flat painted one"),
    "opaque": "{is} filled with OPAQUE cream, so {they} read{r} solid and dense",
}


def _agree(phrase, n):
    return phrase.format(s="s" if n == 1 else "", r="s" if n == 1 else "",
                         they="it" if n == 1 else "they", **{"is": "is" if n == 1 else "are"})

#: The scene accent for a bundle, taken from the products' own label accent rules.
#:
#: Malcolm, 2026-09-12: "the blue colored background should be the color that best fits the
#: product. in the case of matryxil it should be teal. The colors used for the line and the
#: colored text on the labels of the products should be used as a guide for the appropriate
#: background or setting accent colors."
#:
#: So a coloured ground is never a fixed brand blue any more - it is read off the accent rule
#: printed on the label. Where a bundle mixes accents, the first COLOURED one wins: Acetyl's
#: accent is deliberately monochrome silver-grey, and a bundle pairing it with Matrixyl should
#: take the teal rather than fall back to grey. A bundle of only monochrome products gets cool
#: graphite, which is its actual identity rather than a default.
ACCENT_SCENE = {
    "light cornflower-blue": ("deep cornflower blue", "cool blues and steel greys"),
    "light sky-blue": ("deep sky blue", "cool blues and steel greys"),
    "strong royal-blue": ("deep royal blue", "cool blues and pale ice tones"),
    "soft rose-pink": ("soft dusty rose-pink", "blush pinks, warm rose neutrals and soft ivories"),
    "deep emerald-teal": ("deep emerald-teal", "deep teals, cool sea greens and pale cool greys"),
    "champagne gold": ("warm champagne gold", "champagne golds, soft ivories and pale sand"),
}
MONOCHROME_SCENE = ("cool graphite grey", "pearl silvers, cool greys and soft graphite")


def accent(keys):
    """(ground colour, palette phrase) for this bundle, from its labels' accent rules."""
    for k in keys:
        hit = ACCENT_SCENE.get(PRODUCTS[k]["accent"])
        if hit:
            return hit
    return MONOCHROME_SCENE


#: One casting, shared by every bundle wave that puts a person in frame, so she does not change
#: age, colouring or styling between bundles. Copied forward from the Copper Peptide waves,
#: where it was bought with two rounds: an unqualified "beautiful woman" renders as airbrushed
#: plastic on every engine, and pores, texture and a few freckles are what buy realism back.
MODEL = (
    "THE MODEL is a White European woman of about 35 with natural, believable skin - visible "
    "pores, fine texture and a few small freckles, not airbrushed and not plastic. Light "
    "natural make-up, clean groomed brows, hair loosely gathered back off her face. Her "
    "expression is calm and unforced, a faint closed-mouth smile at most. She wears a simple "
    "cream or pale grey vest top with narrow straps. Her hands are clean with short natural "
    "nails and no nail polish, no rings, no bracelets and no watch."
)

SHARED_RULES = (
    "SHARED RULES FOR EVERY PRODUCT IN FRAME. Every metal part is NEUTRAL SILVER-GREY brushed "
    "satin aluminium with a fine grain - never rose-gold, copper, champagne, brass or "
    "warm-tinted, and never a chrome mirror. Reproduce each front label exactly as in the "
    "supplied reference, every character verbatim. The Skingenetix wordmark is spelled with a "
    "capital S and the rest lower case, with no trademark, registered or copyright symbol "
    "anywhere. The ink colours described below name the INK each line is printed in and are "
    "NEVER themselves printed as words - no colour name appears as text anywhere. Each "
    "container carries ONLY the lines listed for it: no benefit lines, no 'ALL SKIN TYPES', no "
    "ingredient list."
)

BASE_NEGATIVE = (
    "rose-gold, copper-coloured metal, champagne metal, brass, gold, warm-tinted metal, chrome "
    "mirror finish, any printed word not listed in the brief, ingredient list, benefit lines, "
    "ALL SKIN TYPES, colour names printed as text, trademark symbol, registered trademark "
    "symbol, copyright symbol, watermark, signature, extra bottles, extra jars, duplicate "
    "products, cardboard cartons, boxes, packaging boxes, hands, fingers, people, faces, text "
    "overlay, caption, cropped product, product touching the frame edge, blurry label, "
    "illegible lettering, misspelled lettering"
)


def product_block(key):
    """The verbatim per-product spec, read from the product's own config.

    `product_desc` in configs/<product>.json already carries the geometry, the container
    colour, every front-label line in order, and the ink each is printed in. It is the same
    content that was hand-copied into the Copper module; reading it means a correction to a
    product's spec reaches every bundle brief automatically.
    """
    p = PRODUCTS[key]
    cfg = json.loads((ROOT / "configs" / f"{p['config']}.json").read_text())
    return f"{p['name']} — {cfg['product_desc']}"


def substance_block(key):
    """What is INSIDE, for any shot that opens a lid.

    No spec on this project describes the substance unless asked, which is why serum bottles
    kept arriving milky white. Read from the same config so it cannot drift.
    """
    p = PRODUCTS[key]
    cfg = json.loads((ROOT / "configs" / f"{p['config']}.json").read_text())
    f = cfg["formulation"]
    return (f"THE SUBSTANCE INSIDE {p['name']} is {f['appearance']}. "
            f"Never {f['never']}.")


def ref_files(keys):
    """Reference image per product, preferring the rebuilt one where it exists.

    `product_tight_norm.png` is written by `scripts/normalise-serum-ref.py` and is preferred
    whenever present. On 2026-09-14 three of the five serum references were found to be teaching
    the engines a TRUNCATED bottle - `build-refs-2026-08-19.py` cropped each product
    independently - which is why the two serum bottles kept coming back different heights. The
    rebuilt refs use the Drive renders uncropped on one shared frame.

    Preferred, not forced: a product with no `_norm` simply keeps its original, so dropping a
    corrected render in and re-running the normaliser is all that is needed to adopt it.
    """
    out = []
    for k in keys:
        d = REFS / PRODUCTS[k]["config"]
        r = d / "product_tight_norm.png"
        if not r.exists():
            r = d / "product_tight.png"
        if not r.exists():
            raise SystemExit(f"missing reference for {k}: {r}")
        out.append(str(r.relative_to(ROOT)))
    return out


def _colour_clusters(keys):
    """Group the bundle's products by CONTAINER COLOUR, preserving order."""
    out = {}
    for k in keys:
        out.setdefault(PRODUCTS[k]["colour"], []).append(k)
    return out


def strategy(keys):
    """The HARDEST separation problem present in this bundle.

    Reported per bundle for planning, but never used to write the clause: a bundle can
    contain more than one kind of collision at once, and treating it as uniform is what made
    the first version of this assert that a pale ice-blue jar of light blue cream was 'the
    same neutral white frosted glass ... water-clear colourless liquid'. That paragraph would
    have instructed every engine to render the product wrong.
    """
    worst = "ladder"
    for members in _colour_clusters(keys).values():
        if len(members) == 1:
            continue
        forms = {PRODUCTS[k]["form"] for k in members}
        worst = "label" if len(forms) < len(members) else (
            "shape" if worst == "ladder" else worst)
    return worst


def separation(keys):
    """Return (prompt_paragraph, negative_fragment) for this set of products.

    Composed per COLOUR CLUSTER rather than per bundle, because the two can differ: a bundle
    may hold one pair that collides and a third product that does not, and a clause that
    describes the whole set uniformly is false for the odd one out.
    """
    names = {k: PRODUCTS[k]["name"] for k in keys}
    clusters = _colour_clusters(keys)
    parts, negs = [], []

    # 0. Contents, before anything about hue. The glass is frosted on every product; what an
    # engine loses first is what is BEHIND that frosting - and a serum is a translucent liquid,
    # tinted or not, while a cream is opaque. Calling a tinted serum "opaque" is as wrong as
    # calling frosted glass "clear".
    by_body = {}
    for k in keys:
        by_body.setdefault(PRODUCTS[k]["body"], []).append(k)
    if len(by_body) > 1:
        bits = []
        for body in ("colourless", "tinted", "opaque"):
            members = by_body.get(body)
            if not members:
                continue
            who = " and ".join(names[k] for k in members)
            bits.append(f"{who} {_agree(CONTENTS_PHRASE[body], len(members))}.")
        parts.append(CONTENTS_CLAUSE.format(parts=" ".join(bits)))
        negs.append("clear see-through glass, opaque plastic container, "
                    "a colourless liquid rendered as milky white, tinted liquid on a "
                    "colourless product")
    elif "colourless" in by_body:
        parts.append(ALL_COLOURLESS_CLAUSE)
        negs.append("clear see-through glass, opaque plastic container, "
                    "a colourless liquid rendered as milky white, tinted liquid")

    # 1. Across colours — only meaningful when more than one colour is present.
    if len(clusters) > 1:
        ordered = sorted(clusters, key=lambda c: min(PRODUCTS[k]["value"] for k in clusters[c]))
        bits = []
        for colour in ordered:
            members = clusters[colour]
            who = " and ".join(names[k] for k in members)
            forms = "/".join(sorted({PRODUCTS[k]["form"] for k in members}))
            bits.append(f"{who} — {colour} ({forms})")
        parts.append(
            "THE PRODUCTS IN THIS FRAME ARE NOT ALL THE SAME COLOUR AND MUST NOT BE RENDERED "
            "AS IF THEY WERE. From darkest to lightest: " + "; ".join(bits) + ". Do not settle "
            "them into one shared colour and do not make two different colours match.")
        negs.append("all containers rendered in the same colour, matching container colours")

    # 2. Within each colour cluster that holds more than one product.
    for colour, members in clusters.items():
        if len(members) == 1:
            continue
        forms = {PRODUCTS[k]["form"] for k in members}
        who = ", ".join(names[k] for k in members)
        if len(forms) == len(members):
            # Shared colour, different forms — say the sharing is CORRECT, or an engine will
            # "helpfully" tint one to differentiate them.
            bits = [f"{names[k]} is the {PRODUCTS[k]['form']}" for k in members]
            parts.append(
                f"{who} DELIBERATELY SHARE ONE COLOUR — both are {colour}, and that is CORRECT. "
                "Do not tint, shade or recolour either of them to tell them apart, and do not "
                "make one warmer or cooler than the other. They are told apart by SHAPE: "
                + "; ".join(bits) + ". A dropper bottle is tall and straight-sided with a "
                "pipette; a cream jar is wide and squat with a broad screw lid.")
            negs.append("one container tinted differently from another of the same colour, "
                        "recoloured glass")
        else:
            # Same colour AND same form — the label is the only lever left.
            bits = [f"{names[k]}, whose accent rule is {PRODUCTS[k]['accent']}" for k in members]
            parts.append(
                f"{who} ARE DELIBERATELY IDENTICAL CONTAINERS and that is CORRECT: the same "
                "FROSTED glass, the same shape and size, the same brushed satin aluminium "
                "collar, the same white rubber-bulb pipette, and the same colourless liquid "
                "inside. Do NOT tint the glass, the liquid or the metal to tell them "
                "apart. THE ONLY DIFFERENCES ARE THE PRINTED LABEL TEXT AND THE COLOUR OF THE "
                "NARROW ACCENT RULE beside it: " + "; ".join(bits) + ". Every line of both "
                "labels must therefore be sharp and fully legible, because the label is the "
                "only thing telling these two products apart in this photograph.")
            # Acetyl's accent is legitimately monochrome silver, which is exactly what an
            # engine produces when it garbles a coloured rule - so a failed teal rule does not
            # look broken, it looks like a correct Acetyl bottle. Bar it by name.
            negs.append("tinted glass, coloured glass, coloured liquid, a grey or silver accent "
                        "rule on a bottle whose rule should be coloured, swapped label text")

    return "\n\n".join(parts), ", ".join(dict.fromkeys(negs))


def build_slot(slot_id, opening, keys, arrangement, scene, frame,
               width=2048, height=2048, extra=None, negative_extra=None):
    """Assemble one generate-multi.py slot for a bundle of `keys`.

    No luma variant: luma is not briefed on bundle waves, so there is no 6000-character cap to
    trim for and no second copy of any product spec to keep in sync.
    """
    # THE COUNT MUST BE STATED POSITIVELY, and this was bought with a smoke test: the first
    # two-product brief came back with THREE bottles - the Matrixyl serum duplicated at both
    # ends of the row with the Acetyl between them - even though "duplicate products" was in
    # the negative. The bar does not hold against a composition that implies a count, and
    # "{A} at the centre" implies a symmetric row of at least three. So the number is asserted
    # up front, the products are named, and repetition is forbidden by name.
    n = len(keys)
    word = {1: "ONE", 2: "TWO", 3: "THREE", 4: "FOUR"}.get(n, str(n))
    names = [PRODUCTS[k]["name"] for k in keys]
    listed = (" and ".join(names) if n == 2 else ", ".join(names[:-1]) + " and " + names[-1])
    count = (f"EXACTLY {word} PRODUCTS APPEAR IN THIS PHOTOGRAPH AND NO OTHERS: {listed}. "
             f"There are {word} containers in total. Do not add another container, do not "
             f"repeat any of them, and do not show two copies of the same product.")

    sep_body, sep_neg = separation(keys)
    prompt = "\n\n".join(
        [opening, SHARED_RULES, count]
        + [product_block(k) for k in keys]
        + (extra or [])
        + ([sep_body] if sep_body else [])
        + [arrangement, scene, frame])
    neg = ", ".join(x for x in (BASE_NEGATIVE, sep_neg, negative_extra) if x)
    return {
        "id": slot_id,
        "width": width,
        "height": height,
        "class": "product-set",
        "ref_files": ref_files(keys),
        "prompt": prompt,
        "negative_extra": neg,
    }
