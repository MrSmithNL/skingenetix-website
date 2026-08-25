#!/usr/bin/env python3
"""Build one generation wave per key ingredient for /pages/the-science.

    python3 scripts/build-science-ingredient-configs.py                    # all five
    python3 scripts/build-science-ingredient-configs.py copper-peptide
    python3 scripts/build-science-ingredient-configs.py --register cell    # microscopy

Writes configs/banners/science-ingredient-<slug>[-cell].json, ready for
generate-multi.py.

TWO REGISTERS. `material` is the original: a dish of the solution, a macro of the
substance, a pipette and droplet. `cell` is the second pass Malcolm asked for on
2026-08-25 — "lets try more cell level images" — after the material wave produced a
usable Copper Peptide and Matrixyl but a weak Acetyl and PDRN.

WHAT THESE FILL. The `ingredients_overview` section of templates/page.science.json
carries five `item` blocks, one per active. All five are wearing placeholders today:
two are mega-menu thumbnails and two were lifted off the philosophy page. The theme
asks for 1400x1400; the art direction generates 1:1 tiles at 2048 (doc §4).

NO RESERVED TYPE ZONE, and that is a deliberate departure from rule 2 of the five
production constraints. That rule exists for frames that carry overlaid type; a
multi-column item renders its title, body and link BELOW the image, so the whole
square is picture and reserving 40% of it would just throw away the subject.

CLASS B, ALL FIFTEEN. No product appears, so no brief carries a product description
or any brand identity — the failure that rule prevents is on record: on 2026-08-19
five text-to-image shots were handed the product description without references and
all thirty candidates invented a branded bottle with a mangled helix.

BUT THE CLASS B NEGATIVE LIST HAD TO BE REWRITTEN, not reused. The standard list bars
"no bottle, no jar, no dropper bottle" — and two of the three concepts here have
laboratory glass as their SUBJECT. Reusing it verbatim would have forbidden the very
thing being asked for, which is exactly how four rounds of weak homepage models were
produced (the `the-brief-caused-the-plainness` memory). The list below bars *cosmetic
packaging and printed identity* precisely, and permits plain unmarked lab glass.

DESCRIBED, NEVER NAMED — WITH ONE DELIBERATE EXCEPTION. Naming a noun lets every
supplier fill the gap from its own stock idea, which is the single root cause behind
four separate image faults on this project, so no material-register brief says "DNA",
"helix", "collagen fibre" or "polynucleotide".

The exception is PDRN in the cell register. There, the stock idea IS the subject —
PDRN is sodium DNA, as the page's own copy says — so the brief names the double helix
AND describes its geometry, which pins the form without inviting clip-art. That is
unrelated to the brand's helix MARK, which stays dots-and-dashes and never appears in
a Class B frame at all.

Colour per ingredient is NOT invented here. Each takes the scene colour already agreed
for its product photography (`configs/<product>.json`, and the concern-to-colour table
in docs/visual-identity/03-art-direction-and-briefs.md §1.2), so these tiles belong to
the same world as the product shots rather than a parallel one.

Negatives are kept SHORT on purpose: Luma has no negative-prompt field, so the list is
folded into the prompt body against a 6000-character cap, and a long one trips its
content filter and loses the backend silently (`luma-constraints` memory).

Author: Claude Code, 2026-08-25.
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "configs" / "banners"

#: 1:1 at 2048 — the art direction's tile spec (§4). gpt-image and FLUX.2 both cap
#: here, and 2048 is divisible by 16, which gpt-image requires or it 400s.
SIZE = 2048

#: Bars cosmetic packaging and printed identity, permits plain laboratory glass.
NEGATIVE = (
    "cosmetic packaging, product bottle, dropper bottle with a cap, jar, tube, "
    "label, logo, brand mark, lettering, text, numbers, watermark, signature, "
    "botanicals, leaves, flowers, herbs, fruit, wood, rough stone, linen, "
    "water splash, lens flare, bokeh sparkle, border, collage, multi-panel, "
    "flat-lay, clutter, more than one subject, hands, people, face"
)

#: The cell register needs more. Real microscopy is published WITH scale bars,
#: arrows, channel labels and grid overlays, so every supplier's idea of "under a
#: microscope" tends to arrive annotated — and an annotated tile is a diagram, not a
#: photograph. Fluorescence imaging is also conventionally garish, several channels
#: at once, which would wreck the one-ground-colour rule the whole system rests on.
NEGATIVE_CELL = NEGATIVE + (
    ", scale bar, annotation, arrow, callout, grid overlay, diagram, chart, "
    "microscope eyepiece, circular vignette frame, split channel panel, "
    "rainbow colours, multicoloured fluorescence, green and red channels together"
)

#: substance colour and scene ground for each active, carried over from the product
#: configs so the tiles match the product photography rather than restating it.
INGREDIENTS = {
    "copper-peptide": {
        "title": "Copper Peptide GHK-Cu",
        "block": "ingredient_1",
        "ground": "a saturated clinical blue (#014EB1)",
        "liquid": ("a clear, lightly viscous liquid carrying a distinct medium-blue tint, "
                   "the colour reading as depth in the liquid itself rather than as a dye"),
        "droplet": "a single pendant droplet of clear medium-blue liquid",
        "material": ("a small mound of fine crystalline solid in a deep saturated blue, "
                     "its facets catching the key light in hard individual glints"),
    },
    "acetyl-hexapeptide-8": {
        "title": "Acetyl Hexapeptide-8",
        "block": "ingredient_2",
        "ground": "a soft pearl grey (#D8D6D4)",
        "liquid": ("a completely transparent, colourless liquid — water-clear and lightly "
                   "viscous, visible only as refraction, edge caustics and highlight"),
        "droplet": "a single pendant droplet of completely clear colourless liquid",
        "material": ("a flat rectangular glass microscope slide carrying a thin smear of "
                     "colourless crystalline material, lit from beneath so the crystals "
                     "read as bright structure against the dark of the slide's edge"),
    },
    "matrixyl-3000": {
        "title": "Matrixyl 3000",
        "block": "ingredient_3",
        "ground": "a deep emerald-teal (#016569)",
        "liquid": ("a completely transparent, colourless liquid — water-clear and lightly "
                   "viscous, visible only as refraction and highlight"),
        "droplet": "a single pendant droplet of completely clear colourless liquid",
        "material": ("an extremely fine mesh of pale translucent filaments, each thinner "
                     "than a hair, crossing and interlocking in several layers so the "
                     "nearest are sharp and the deeper ones fall away into shadow"),
    },
    "pdrn": {
        "title": "PDRN",
        "block": "ingredient_4",
        "ground": "a soft blush pink (#F3BFC2)",
        "liquid": ("a translucent liquid carrying a soft rose-pink tint — clearer and "
                   "thinner than a cream, but visibly pink rather than colourless"),
        "droplet": "a single pendant droplet of translucent rose-pink liquid",
        "material": ("long, fine, translucent threads suspended in a clear rose-tinted "
                     "fluid, drifting and curling loosely past one another, the nearest "
                     "few in sharp focus and the rest softening into the depth"),
    },
    "glutathione": {
        "title": "Glutathione",
        "block": "ingredient_5",
        "ground": "a warm champagne gold (#DFC08F)",
        "liquid": ("a completely transparent, colourless liquid — water-clear and lightly "
                   "viscous, visible only as refraction and highlight"),
        "droplet": "a single pendant droplet of completely clear colourless liquid",
        "material": ("a small heap of very fine white crystalline powder, its surface "
                     "broken into soft peaks, individual grains resolving at the lit edge"),
    },
}

#: One hard key, one soft fill, a real shadow, a committed ground — rules 3 and 4 of
#: the five production constraints, written into every prompt rather than assumed.
LIGHT = ("A single hard key light from the upper left rakes across the subject and lays "
         "one crisp shadow down to the lower right; a soft fill lifts the core of that "
         "shadow just enough to hold detail. The look is clinical, rigorous and "
         "expensive — a research laboratory, not a spa.")


#: Cell-register subjects. Malcolm, 2026-08-25: "lets try more cell level images",
#: and "PDRN is Salmon DNA - so lets use a DNA image".
#:
#: PDRN IS THE ONE CASE ON THIS PROJECT WHERE NAMING THE THING IS CORRECT. The
#: standing rule is describe-don't-name, because a named noun gets filled in from each
#: supplier's own stock idea. Here the stock idea IS the subject: PDRN is sodium DNA,
#: so the brief names the double helix AND describes its geometry, which pins the form
#: without inviting clip-art. Note this is unrelated to the brand's helix MARK, which
#: must stay dots-and-dashes and never appears in a Class B frame.
CELL = {
    #: Copper Peptide's cell story is the FIBROBLAST — GHK-Cu is studied for prompting
    #: fibroblasts to lay down matrix. That earns it a different cell shape from the
    #: others: fibroblasts are elongated and spindle-shaped with long tapering
    #: processes, where the acetyl and glutathione briefs ask for rounded polygonal
    #: skin cells. Without that distinction three of the five tiles would be the same
    #: field of round cells in three colours, which is the exact failure the material
    #: register already had with its colourless-liquid concepts.
    "copper-peptide": [
        ("D-fibroblast-field", "A field of spindle-shaped cells",
         "a wide field of elongated spindle-shaped cells seen through a microscope, each "
         "tapering to fine processes at both ends and loosely aligned with its neighbours, "
         "overlapping in several layers and tiling away into shallow focus"),
        ("E-single-fibroblast", "One spindle cell, close",
         "one single elongated spindle-shaped cell filling the frame diagonally, a denser "
         "rounded body at its middle and long fine processes tapering away from both ends "
         "toward the frame edges, its boundary crisp and faintly luminous"),
        ("F-cell-and-matrix", "A cell reaching into the surrounding network",
         "one elongated spindle-shaped cell embedded in a surrounding network of extremely "
         "fine filaments, its long processes reaching out and merging into that network, the "
         "cell sharp and the filament web falling away into depth around it"),
    ],
    "acetyl-hexapeptide-8": [
        ("D-cell-field", "A field of cells seen through a microscope",
         "a wide field of living skin cells seen through a microscope, each cell a rounded "
         "polygon pressed against its neighbours with a denser, brighter body at its centre, "
         "the whole sheet tiling away into shallow focus"),
        ("E-single-cell", "One cell, close",
         "one single skin cell filling most of the frame, its outer boundary crisp and faintly "
         "luminous, its interior showing a denser rounded body and fine granular structure "
         "around it, neighbouring cells falling away out of focus at the edges"),
        ("F-surface-electron", "Skin surface at cell scale, electron-microscope register",
         "the surface of skin at cell scale in the manner of a scanning electron micrograph — "
         "overlapping flattened plates like dry riverbed scales, every ridge and edge rendered "
         "in fine relief, monochrome and sculptural rather than coloured"),
    ],
    "pdrn": [
        ("D-double-helix", "A single DNA double helix",
         "one DNA double helix running diagonally across the frame: two smooth strands winding "
         "around a common axis in a regular repeating twist, joined at even intervals by short "
         "straight rungs between them, the near turns sharp and the far ones softening into "
         "depth. A clean scientific rendering of the molecule, not a decorative ribbon"),
        ("E-helix-field", "Several strands drifting in fluid",
         "several DNA double helices suspended and drifting in a clear fluid at different depths "
         "and angles, each a pair of strands winding around a common axis with regular rungs "
         "between them, the nearest sharp and the rest dissolving into the depth"),
        ("F-nucleus", "A cell nucleus, where the material lives",
         "one cell seen through a microscope with its nucleus dominant — a dense rounded body "
         "near the centre, brighter than the surrounding cell and finely threaded through with "
         "coiled strand-like structure, the cell's outer boundary soft around it"),
    ],
    "glutathione": [
        ("D-cell-field", "A field of cells seen through a microscope",
         "a wide field of living skin cells seen through a microscope, each cell a rounded "
         "polygon pressed against its neighbours with a denser, brighter body at its centre, "
         "the whole sheet tiling away into shallow focus"),
        ("E-single-cell-lit", "One cell, lit from within",
         "one single skin cell filling most of the frame, lit as though from within so its "
         "interior glows warmly outward through its boundary, small bright rounded bodies "
         "suspended inside it, the surrounding cells dark and out of focus"),
        ("F-radical-scatter", "Bright points scattering off a cell boundary",
         "the boundary of one cell crossing the frame, with a scatter of very small bright "
         "points drifting against it — some settling along the boundary, some falling away out "
         "of focus, each a hard tiny highlight rather than a soft bloom"),
    ],
}


def cell_concepts(slug: str, ing: dict) -> list[dict]:
    """Microscopy register. Ground colour still governs; annotation is barred."""
    g = ing["ground"]
    out = []
    for cid, title, subject in CELL[slug]:
        out.append({
            "id": cid,
            "title": title,
            "prompt": (
                f"Scientific microscopy photograph, one subject only, filling the frame: "
                f"{subject}. Everything is rendered in {g} and its own lighter and darker "
                f"values — a single colour family across the whole frame, no second hue "
                f"anywhere. The background falls away into deep shadow at the frame edges. "
                f"Depth of field is shallow, so the nearest structure is razor sharp and the "
                f"rest dissolves. This is a clean photographic plate: no annotation, no "
                f"measurement marks, no circular eyepiece framing. {LIGHT}"
            ),
        })
    return out


def concepts(ing: dict) -> list[dict]:
    g, liq, mat, drop = ing["ground"], ing["liquid"], ing["material"], ing["droplet"]
    return [
        {
            "id": "A-dish-of-solution",
            "title": "Shallow laboratory dish holding the solution, on the ground colour",
            "prompt": (
                f"Laboratory still-life photograph, one subject only. A shallow circular "
                f"borosilicate glass dish, plain and entirely unmarked, sits on a smooth "
                f"seamless surface of {g}. The dish holds a shallow pool of {liq}, roughly "
                f"eight millimetres deep, its surface perfectly still so the rim throws a "
                f"clean elliptical caustic onto the floor of the dish. Photographed from "
                f"about thirty degrees above, the dish centred and filling roughly sixty "
                f"percent of the frame width, the ground running out to all four edges. "
                f"Colour is restricted to the ground, the glass and the liquid. {LIGHT}"
            ),
        },
        {
            "id": "B-material-macro",
            "title": "Macro study of the material itself",
            "prompt": (
                f"Extreme macro photograph, one subject only, filling the frame: {mat}. "
                f"Behind it, a smooth seamless surface of {g} shows only at the very "
                f"edges of the frame. Focus falls off steeply with depth, so the "
                f"nearest structure is razor sharp and the rest dissolves. Colour is "
                f"restricted to the ground and the material. {LIGHT}"
            ),
        },
        {
            "id": "C-pipette-and-droplet",
            "title": "Glass pipette releasing a single droplet",
            "prompt": (
                f"Laboratory still-life photograph, one subject only. A slender straight "
                f"glass pipette, plain and entirely unmarked, enters from the top of the "
                f"frame and hangs vertically, its drawn tip at about the upper third. "
                f"{drop.capitalize()} hangs from the tip, elongated and about to fall, "
                f"caught sharp. Behind it a smooth seamless surface of {g} runs out to all "
                f"four edges. The pipette occupies a narrow vertical band at the centre and "
                f"the ground is otherwise unbroken. Colour is restricted to the ground, the "
                f"glass and the liquid. {LIGHT}"
            ),
        },
    ]


def build(slug: str, register: str = "material") -> Path:
    ing = INGREDIENTS[slug]
    cell = register == "cell"
    if cell and slug not in CELL:
        raise SystemExit(f"no cell-register concepts written for {slug}")
    suffix = "-cell" if cell else ""
    cfg = {
        "wave": f"science-ingredient-{slug}{suffix}",
        "created": "2026-08-25",
        "doc": "docs/visual-identity/03-art-direction-and-briefs.md",
        "note": (
            f"Ingredient tile for {ing['title']} on /pages/the-science, section "
            f"`ingredients_overview`, block `{ing['block']}`. Square 1:1 at {SIZE}; the "
            f"theme asks for 1400x1400 and the art direction generates tiles at 2048.\n\n"
            f"Replaces a placeholder — all five ingredient tiles are currently wearing "
            f"mega-menu thumbnails or images borrowed from the philosophy page.\n\n"
            f"CLASS B: no product in frame, so no product description and no brand "
            f"identity is supplied. The Class B negative list was rewritten rather than "
            f"reused — the standard one bars bottles and jars outright, and plain "
            f"laboratory glass is the subject of two of these three concepts.\n\n"
            f"Ground colour is {ing['ground']}, taken from this active's existing scene "
            f"colour rather than invented, so the tile matches the product photography.\n\n"
            + ("Nothing is named that can be described: no brief here says DNA, helix, "
               "collagen fibre or polynucleotide."
               if not cell else
               "CELL REGISTER, Malcolm 2026-08-25: 'lets try more cell level images'. The "
               "material-macro wave produced a usable Copper Peptide and Matrixyl but a weak "
               "Acetyl — several suppliers gave a black slide against a beige ground, losing "
               "the committed pearl-grey entirely — and a PDRN whose 'fine translucent threads' "
               "read as hair or fishing line on about half the candidates.\n\n"
               "The negative list is EXTENDED for this register. Real microscopy is published "
               "with scale bars, arrows, channel labels and grid overlays, so every supplier's "
               "idea of 'under a microscope' arrives annotated, and an annotated tile is a "
               "diagram rather than a photograph. Multi-channel fluorescence is also "
               "conventionally garish, which would wreck the one-ground-colour rule.\n\n"
               "PDRN NAMES ITS SUBJECT, WHICH IS A DELIBERATE EXCEPTION. The standing rule on "
               "this project is describe-don't-name, because a named noun gets filled in from "
               "each supplier's own stock idea. Here the stock idea IS the subject — PDRN is "
               "sodium DNA, as the page's own copy says — so the brief names the double helix "
               "AND describes its geometry, pinning the form without inviting clip-art. This "
               "has nothing to do with the brand's helix MARK, which stays dots-and-dashes and "
               "never appears in a Class B frame.")
        ),
        "defaults": {"candidates": 2,
                     "negative_global": NEGATIVE_CELL if cell else NEGATIVE},
        "slots": [
            {
                "id": f"{ing['block']}--{c['id']}",
                "title": c["title"],
                "class": "B",
                #: INTEGERS, not strings. Every supplier adapter does arithmetic on
                #: these -- flux2 compares against its cap, gpt-image divides to snap
                #: to a multiple of 16 -- so a quoted value dies with a TypeError deep
                #: inside the adapter. generate-multi.py catches per-supplier
                #: exceptions so one dead backend cannot kill a run, which means the
                #: run still exits 0 and still prints a total: the first attempt at
                #: this wave lost five of six suppliers and reported "6 images across
                #: 6 suppliers". Read the per-supplier lines, never the total.
                "width": SIZE,
                "height": SIZE,
                "target_slot": f"page.science:ingredients_overview.{ing['block']}",
                "prompt": c["prompt"],
                "negative_extra": "",
            }
            for c in (cell_concepts(slug, ing) if cell else concepts(ing))
        ],
    }
    p = OUT / f"science-ingredient-{slug}{suffix}.json"
    p.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")
    return p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug", nargs="?", choices=sorted(INGREDIENTS))
    ap.add_argument("--register", choices=("material", "cell"), default="material",
                    help="material = dish / macro / pipette; cell = microscopy register")
    args = ap.parse_args()
    pool = sorted(CELL) if args.register == "cell" else sorted(INGREDIENTS)
    for slug in ([args.slug] if args.slug else pool):
        p = build(slug, args.register)
        n = len(json.loads(p.read_text())["slots"])
        print(f"  {p.relative_to(ROOT)}  {n} concepts x 6 suppliers x 2 candidates")


if __name__ == "__main__":
    main()
