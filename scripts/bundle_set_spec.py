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
#:   body    clear | opaque. See the note below — this is the field that was wrong.
#:   colour  what the container READS AS in a photograph. Drives LADDER separation.
#:   value   0 = darkest, 100 = lightest/clearest. Only used to order a ladder; never printed.
#:   accent  the accent-rule colour on the label. The only lever LABEL separation has.
#:
#: THE COLOUR FIELD DESCRIBES WHAT YOU SEE, NOT WHAT THE SPEC PROSE SAYS, and the difference
#: cost a wrong brief. Every bottle in the range is the same frosted CLEAR glass; what gives a
#: container its colour is the LIQUID INSIDE IT. Copper Peptide reads blue because the serum is
#: blue, PDRN reads pink because the serum is pink, and Matrixyl, Glutathione and Acetyl read
#: TRANSPARENT because their contents are colourless. The cream jars read opaque because cream
#: is opaque.
#:
#: The first version of this table took `colour` from the phrase "frosted NEUTRAL WHITE glass"
#: in each config's product_desc and recorded the Matrixyl serum and the Matrixyl cream as
#: sharing one colour. Malcolm caught it: "the Matrixyl serum is transparent, the cream is
#: white." Verified against every product_tight.png reference on 2026-09-11 — the background
#: shows straight through the serum bottles and not at all through the cream jars. The
#: consequence was not cosmetic: that bundle was being briefed with a SHAPE clause asserting
#: "both are neutral white and that is CORRECT, do not tint either to tell them apart", which
#: would have driven the serum to render as an opaque white bottle.
PRODUCTS = {
    "cp_serum": dict(
        config="copper-peptide-repair-serum", name="THE COPPER PEPTIDE SERUM BOTTLE",
        form="bottle", body="opaque", colour="deep blue", value=30,
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
        form="bottle", body="opaque", colour="dusty rose-pink", value=55,
        accent="soft rose-pink"),
    "pdrn_cream": dict(
        config="pdrn-collagen-repair-cream", name="THE PDRN NIGHT CREAM JAR",
        form="jar", body="opaque", colour="pale rose-pink", value=65,
        accent="soft rose-pink"),
    "mat_serum": dict(
        config="matrixyl-3000-pro-collagen-serum", name="THE MATRIXYL 3000 SERUM BOTTLE",
        form="bottle", body="clear", colour="clear and transparent", value=100,
        accent="deep emerald-teal"),
    "mat_cream": dict(
        config="matrixyl-3000-pro-collagen-cream", name="THE MATRIXYL 3000 CREAM JAR",
        form="jar", body="opaque", colour="opaque white", value=85,
        accent="deep emerald-teal"),
    "glut_serum": dict(
        config="glutathione-brightening-serum", name="THE GLUTATHIONE SERUM BOTTLE",
        form="bottle", body="clear", colour="clear and transparent", value=100,
        accent="champagne gold"),
    "acetyl_serum": dict(
        config="acetyl-hexapeptide-8-serum", name="THE ACETYL HEXAPEPTIDE-8 SERUM BOTTLE",
        form="bottle", body="clear", colour="clear and transparent", value=100,
        accent="monochrome silver-grey, with no coloured accent at all"),
}

#: Emitted whenever a bundle mixes see-through and solid containers. Without it an engine
#: renders a clear bottle as an opaque white one, which is the specific fault Malcolm caught.
CLEAR_VS_OPAQUE = (
    "CLEAR CONTAINERS AND SOLID CONTAINERS IN ONE FRAME. {clear} — the glass is frosted but "
    "SEE-THROUGH and the liquid inside is colourless, so the background is visible THROUGH the "
    "bottle and it must never be rendered as a solid white or milky object. {opaque} — solid "
    "and not see-through, because opaque product fills them. This difference must be obvious "
    "in the photograph."
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
    out = []
    for k in keys:
        r = REFS / PRODUCTS[k]["config"] / "product_tight.png"
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

    # 0. See-through vs solid, before anything about hue. This is the distinction an engine
    # loses first: a colourless serum in frosted clear glass renders as a solid white bottle
    # unless the transparency is asserted.
    clear = [k for k in keys if PRODUCTS[k]["body"] == "clear"]
    opaque = [k for k in keys if PRODUCTS[k]["body"] == "opaque"]
    if clear and opaque:
        parts.append(CLEAR_VS_OPAQUE.format(
            clear=" and ".join(names[k] for k in clear) +
                  (" is" if len(clear) == 1 else " are") + " CLEAR AND SEE-THROUGH",
            opaque=" and ".join(names[k] for k in opaque) +
                   (" is" if len(opaque) == 1 else " are") + " OPAQUE"))
        negs.append("a clear see-through bottle rendered as solid white or milky, "
                    "an opaque jar rendered as transparent")
    elif clear and not opaque:
        who = " and ".join(names[k] for k in clear)
        parts.append(
            f"EVERY CONTAINER IN THIS FRAME IS CLEAR AND SEE-THROUGH. {who} — frosted but "
            "transparent glass holding a colourless liquid, so the background is visible "
            "THROUGH each bottle. Never render them as solid white, milky or opaque objects.")
        negs.append("solid white bottle, milky bottle, opaque glass, coloured liquid")

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
                f"{who} ARE DELIBERATELY IDENTICAL CONTAINERS and that is CORRECT: same "
                f"{colour} frosted glass, same shape and size, same brushed satin aluminium "
                "collar, same white rubber-bulb pipette, and the same water-clear colourless "
                "liquid inside. Do NOT tint the glass, the liquid or the metal to tell them "
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
