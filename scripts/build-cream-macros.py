#!/usr/bin/env python3
"""Build configs/banners/<product>-cream-macros.json for any of the four cream products.

    python3 scripts/build-cream-macros.py --all
    python3 scripts/build-cream-macros.py matrixyl-3000-pro-collagen-cream

2026-09-15. Malcolm: "a batch of matrixyl cream shots that are very close up - and show the open
pot with - variations of these shots: finger tip with a small swatch of white cream on it / a
small swatch of white cream from the pot on a small metalic silver spoon/cream dispensor device
(for extracting a small bit of cream from the pot without contaminating it with fingers) / the
pot open and a close up of the white cream inside."

THREE FAMILIES, three variations each, and the variable inside a family is only the framing.

BRANDING DECIDES THE REFERENCE, PER SLOT, and this is the part that is easy to get wrong here:

  * Where the jar's front label is legible, the slot carries ref_files AND the verbatim
    product_desc, because an unspecified label is an invented one - PDRN came back as PORN once.
  * Where nothing branded is in frame - the pure macros of a fingertip, a spatula, or the cream
    surface itself - the slot carries NEITHER. A reference pulls the framing back to its own
    distance, which is exactly wrong for a macro of what is INSIDE the product, and shipping the
    label prose to a shot with no label invites one into the picture.

generate-multi auto-skips flux2 wherever ref_files are present, so flux2 is included in the
supplier list and will run only on the reference-free slots - the material it is actually good
at. No special-casing needed at the command line.

THE SWATCH SIZE IS ANCHORED TO SOMETHING IN FRAME, never to an adjective. "A small swatch" is
how the r3 wave got dollops; the fix that worked was comparing it to the fingernail beside it.
The same device is used for the spatula, whose bowl is the yardstick there.

Substance and jar geometry are lifted from configs/matrixyl-3000-pro-collagen-cream.json rather
than restated, so a correction to the product spec reaches this wave too.

Author: Claude Code, 2026-09-15.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
#: slug -> output stem. All four creams share the shot list; only the product changes.
PRODUCTS = {
    "matrixyl-3000-pro-collagen-cream": "matrixyl",
    "copper-peptide-day-repair-cream": "copper-day",
    "copper-peptide-night-repair-cream": "copper-night",
    "pdrn-collagen-repair-cream": "pdrn",
}

#: THE GROUND IS CHOSEN BY CONTRAST, NOT BY BRAND PALETTE - and this is not a stylistic call.
#: Each product's `palette` is a SCENE colour, right for a lifestyle or hero shot. In a macro the
#: substance IS the subject, and two of the four palettes make it disappear: the PDRN cream is
#: #F3BFC2 and its palette ground is ALSO #F3BFC2, identical; the Copper DAY cream is a dark navy
#: #2F4C9B against a clinical blue #014EB1. Measured relative luminance picks the ground instead,
#: so a light cream gets graphite and a dark cream gets a pale ground. Every pairing clears
#: 4.5:1 - white 15.6, night blue 9.6, pink 10.8, day navy 6.6.
GRAPHITE = ("#1A1A1A", "a seamless deep graphite ground, colour #1A1A1A, falling to near-black "
            "at the edges - graphite throughout, never warm brown and never pale grey")
PALE = ("#E8EAEC", "a seamless pale cool grey ground, colour #E8EAEC, clean and even and "
        "lifting slightly toward white at the edges - never warm, never cream, never beige")


def _lum(h):
    r, g, b = (int(h.lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)
CREAM_T = (
    "THE CREAM IS {appearance_upper}, colour {hex}. It is exactly the same colour everywhere it "
    "appears in the frame - in the pot, on the fingertip, on the spatula - with no colour shift "
    "between them. Never {never}."
)



OPEN_JAR = (
    "THE JAR IS OPEN. Its brushed silver lid is OFF and lies beside it, upturned so its inner "
    "face shows, slightly out of focus. The jar's mouth is a wide circle and the cream inside "
    "reaches close to the rim."
)

SPATULA = (
    "A SMALL COSMETIC SPATULA is in frame - a slim hygiene scoop for lifting cream out of the "
    "pot without fingers. Describe it by shape: a straight slender handle no thicker than a "
    "matchstick opening into a shallow rounded bowl about the size of a little fingernail, the "
    "whole thing in NEUTRAL SILVER-GREY brushed satin metal with a fine grain, never chrome "
    "mirror, never gold, never plastic and never coloured. It carries no branding, no engraving "
    "and no text of any kind."
)

GROUND_T = (
    "Behind it {ground}. One large soft key from the upper left, one dim cool fill on the shadow "
    "side, so the cream keeps its form and the metal keeps its grain."
)

CAMERA = (
    "100mm macro at f5.6, focus on the cream itself, everything behind it thrown well out of "
    "focus. Fine film grain, natural colour, quiet and expensive."
)

NEG_COMMON = (
    "yellow cream, ivory cream, beige cream, golden cream, amber, pink cream, blue cream, teal "
    "cream, green cream, any colour cast in the cream, glossy wet-looking cream, runny cream, "
    "melted cream, foam, mousse, whipped peaks like meringue, glitter, shimmer, "
    "dirty cream, cream smeared on the jar rim, cream on the outside of the glass, fingerprints "
    "on the glass, dusty surface, hair in the cream, "
    "two jars, duplicate jars, a second pot, bottle in frame, dropper in frame, box in frame"
)
NEG_UNBRANDED = (
    ", label, logo, printed text, brand name, lettering, watermark, packaging, a jar with "
    "writing on it"
)
NEG_HAND = ", long nails, coloured nail polish, chipped polish, jewellery, rings, wet hands"

#: (id, short, branded, framing)
SHOTS = [
    # ---------------------------------------------------------------- fingertip
    ("FINGER-01", "fingertip swatch, jar behind", True,
     "Extreme close-up product macro, square format. A single index FINGERTIP fills the upper "
     "middle of the frame, tip angled down toward the lens, with a small swatch of the cream "
     "sitting on the pad of it. THE SWATCH IS TINY: no wider than the fingernail on that same "
     "finger, which is visible in the frame for comparison, standing barely proud of the skin - "
     "a soft rounded dab with one gentle peak where it lifted away, not a blob and not a scoop. "
     "Lower and behind, well out of focus, the open jar."),
    ("FINGER-02", "fingertip lifting from the pot", True,
     "Extreme close-up product macro, square format. A fingertip has just lifted out of the open "
     "jar and is rising away from the cream surface, a small swatch on its pad and a fine short "
     "thread of cream still connecting the dab to the surface below, about as long as the "
     "fingernail is wide. The jar mouth and the cream surface fill the lower third, sharp enough "
     "to read; the finger and its swatch are the focus."),
    ("FINGER-03", "fingertip swatch alone", False,
     "Extreme close-up macro, square format, of a single fingertip held up against a plain dark "
     "ground with a small swatch of white cream on the pad. NOTHING ELSE IS IN FRAME - no jar, "
     "no lid, no packaging, no surface. The fingertip fills the middle of the picture, skin "
     "texture and the fine ridges of the print clearly visible, the swatch no wider than the "
     "fingernail beside it."),
    # ------------------------------------------------------------------ spatula
    ("SPATULA-01", "spatula held above the open jar", True,
     "Extreme close-up product macro, square format. The small silver spatula is held "
     "horizontally across the upper half of the frame, its shallow bowl carrying a small swatch "
     "of the cream - the cream fills the bowl and sits barely proud of its rim, it does not "
     "mound above it and does not overhang the edges. Below and behind, softly out of focus, the "
     "open jar it was lifted from."),
    ("SPATULA-02", "spatula resting on the jar rim", True,
     "Extreme close-up product macro, square format, looking slightly down. The small silver "
     "spatula rests across the open mouth of the jar, its handle on the near rim and its bowl "
     "over the cream, a small swatch in the bowl. The jar's rim, the cream surface inside and "
     "the spatula are all sharp; the lid lies beside the jar, out of focus."),
    ("SPATULA-03", "spatula and cream alone", False,
     "Extreme close-up macro, square format, of the small silver spatula alone against a plain "
     "dark ground, held at a slight angle so the shallow bowl faces the lens with a small swatch "
     "of white cream in it. NOTHING ELSE IS IN FRAME - no jar, no lid, no hand, no packaging. "
     "The brushed grain of the metal and the satin surface of the cream are both readable."),
    # ----------------------------------------------------------------- open pot
    ("POT-01", "open pot, cream surface, three quarter", True,
     "Extreme close-up product macro, square format, looking down into the OPEN jar at about "
     "forty five degrees. The jar's mouth and the untouched cream surface inside fill most of "
     "the frame, the far rim and a little of the frosted glass body visible at the edges. The "
     "cream surface is smooth and level with a soft satin sheen, undisturbed, with no scoop "
     "taken out of it. The lid lies beside it, out of focus."),
    ("POT-02", "straight down into the pot", False,
     "Extreme close-up macro, square format, shot STRAIGHT DOWN directly over the open jar so "
     "the mouth of it forms a circle filling almost the whole frame, with only a thin ring of "
     "the jar's rim visible at the edges and no label or lettering anywhere in view. The white "
     "cream fills that circle edge to edge, its surface smooth and satin with the faintest "
     "concentric sweep from filling, undisturbed."),
    ("POT-03", "one scoop taken out", True,
     "Extreme close-up product macro, square format, looking down into the OPEN jar at about "
     "forty five degrees. ONE SMALL SCOOP HAS BEEN TAKEN from the cream surface, leaving a "
     "single shallow crescent hollow no wider than a fingernail near one side, its edges soft "
     "and slightly glossy where the cream was lifted. The rest of the surface is smooth and "
     "untouched. The lid lies beside the jar, out of focus."),
]


def build(slug):
    cfg = json.loads((ROOT / f"configs/{slug}.json").read_text())
    f = cfg["formulation"]
    ground_hex, ground_prose = GRAPHITE if _lum(f["hex"]) > 0.35 else PALE
    cream = CREAM_T.format(appearance_upper=f["appearance"].upper(), hex=f["hex"],
                           never=f["never"])
    jar = f"THE PRODUCT. {cfg['product_desc']}"
    ground = GROUND_T.format(ground=ground_prose)
    ref = f"assets/images/_refs-2026-08-19/{slug}/product_tight_norm.png"
    stem = PRODUCTS[slug]

    slots = []
    for slot_id, short, branded, framing in SHOTS:
        parts = [framing]
        if branded:
            parts += [jar, OPEN_JAR]
        parts += [cream]
        if "SPATULA" in slot_id:
            parts.append(SPATULA)
        parts += [ground, CAMERA]
        neg = NEG_COMMON + ("" if branded else NEG_UNBRANDED)
        if "FINGER" in slot_id:
            neg += NEG_HAND
        slot = {
            "id": f"{stem.upper().replace('-', '')}-CREAM-{slot_id}",
            "title": f"{stem} cream macro - {short}",
            "substance": "cream",
            "substance_hex": f["hex"],
            "ground_hex": ground_hex,
            "branding_in_frame": branded,
            "class": "B",
            "width": 2048,
            "height": 2048,
            "target_slot": f"{slug} - macro set",
            "prompt": " ".join(parts),
            "negative_extra": neg,
        }
        if branded:
            slot["ref_files"] = [ref]
        slots.append(slot)

    return {
        "wave": f"{stem}-cream-macros",
        "created": "2026-09-15",
        "product": slug,
        "note": ("Three families x three framings. Slots with the label legible carry the "
                 "reference and the verbatim product_desc; the pure macros carry neither and "
                 "negate lettering instead. flux2 auto-skips the referenced slots. The ground "
                 "is picked by MEASURED contrast against the cream, not from the brand palette "
                 "- two of the four palettes would have hidden the substance entirely."),
        "defaults": {"class": "B"},
        "slots": slots,
    }


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("product", nargs="?")
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    todo = list(PRODUCTS) if a.all else [a.product]
    for slug in todo:
        if slug not in PRODUCTS:
            raise SystemExit(f"unknown product {slug!r}; choose from {list(PRODUCTS)}")
        cfg = build(slug)
        out = ROOT / f"configs/banners/{PRODUCTS[slug]}-cream-macros.json"
        out.write_text(json.dumps(cfg, indent=2) + "\n")
        b = sum(1 for x in cfg["slots"] if x.get("ref_files"))
        print(f"{out.relative_to(ROOT)}")
        print(f"   cream {cfg['slots'][0]['substance_hex']} on ground "
              f"{cfg['slots'][0]['ground_hex']}   {len(cfg['slots'])} slots "
              f"({b} referenced, {len(cfg['slots']) - b} macro-only)")
