#!/usr/bin/env python3
"""Make the shared shot templates colour-neutral, so colour comes per product.

Three faults are being fixed, all found on 2026-08-20 after Malcolm rejected the
Glutathione and Copper Peptide drop and swatch shots:

  1. `t2i_material` hard-codes "Clear golden-tinted cosmetic serum liquid" - and
     cream_jar.json carries the SERUM's copy of it, so every cream texture shot
     was being asked for golden serum.
  2. `language.contents` describes the substance with no colour, so the model
     defaults to white cream and water-clear serum.
  3. Individual briefs assert colours outright - "clear-golden" serum drops,
     terracotta and teal grounds - shared across every product regardless of
     what colour that product actually is.

After this patch the templates say WHAT is in shot; the product config says what
colour it is. `{formulation}` and `{palette_scene}` are filled by
templates.compose_prompt from the config's `formulation` / `palette` blocks.

`shows_formulation` marks the shots where the substance is actually visible, so
the formulation directive is not attached to a closed-jar hero - saying "the
cream is blue" on a shot with no cream in it only argues for tinting the glass.

Idempotent: run it twice and the second run reports no changes.

Author: Claude Code, 2026-08-20.
"""
import json
import os
import sys

TPL = ("/Users/malcolmsmith/Claude Code/Projects/smith-os/packages/forge/"
       "skills/product-photography/scripts/templates")

# Shots where the substance itself is visible in frame.
SHOWS = {
    "serum_bottle.json": {4, 9, 10, 11, 34, 41, 42, 43, 44, 45},
    "cream_jar.json": {8, 10, 11, 12, 13, 15, 27, 30, 33, 35, 36, 37, 38, 39},
}

# Exact substring replacements per template, per shot number.
EDITS = {
    "serum_bottle.json": {
        9: [("A clear gel droplet clings to the glass tip",
             "A droplet of the serum clings to the glass tip")],
        10: [("a single amber-clear drop falling from the tip. Warm saturated ground",
              "a single drop of the serum falling from the tip. Saturated "
              "{palette_scene} ground")],
        12: [("a saturated horizontal band",
              "a saturated {palette_scene} horizontal band")],
        14: [("Warm terracotta or apricot colour-block ground",
              "Colour-block ground in {palette_scene}")],
        22: [("bottle on a coloured water surface (blush or pale blue)",
              "bottle on a coloured water surface in {palette_scene}")],
        39: [("Bold saturated colour ground",
              "Bold saturated {palette_scene} ground")],
        41: [("a single large clear-golden cosmetic serum droplet",
              "a single large droplet of the serum")],
        44: [("Three or four clear-golden serum drops",
              "Three or four drops of the serum")],
    },
    "cream_jar.json": {
        9: [("a moody teal-grey gradient", "a moody {palette_scene} gradient")],
        15: [("Saturated single-colour ground.",
              "Saturated single-colour ground in {palette_scene}.")],
        24: [("a deep saturated ground (forest green or charcoal)",
              "a deep saturated ground in {palette_scene} or charcoal")],
        25: [("Jar on warm veined marble", "Jar on veined marble in {palette_scene}"),
             ("Warm, tactile, luxurious.", "Tactile and luxurious.")],
    },
}

# Template-level strings. The substance is named by the template (a cream
# template makes cream), the colour by the product.
T2I = {
    "serum_bottle.json": (
        "{formulation} Photographed as material only. NO bottle, NO packaging, NO "
        "label, NO logo and NO text anywhere in frame - this shot is about the "
        "liquid, the skin and the light, nothing else."),
    "cream_jar.json": (
        "{formulation} Photographed as material only. NO jar, NO packaging, NO "
        "label, NO logo and NO text anywhere in frame - this shot is about the "
        "cream, the skin and the light, nothing else."),
}
CONTENTS = {
    "serum_bottle.json": "{formulation} visible through the glass",
    "cream_jar.json": "{formulation} visible inside the open jar",
}

# The serum template's mandatory line was written for the Glutathione bottle,
# whose frosted glass really is neutral white, and then applied to every serum.
# On the Copper Peptide serum it contradicts that product's own description
# ("frosted DEEP BLUE glass") inside the same prompt. The intent - ambient light
# does not re-dye the glass - is right; the hard-coded colour is not. cream_jar
# already words this correctly, so only the serum needs the edit.
MANDATORY = {
    "serum_bottle.json": [
        ("The frosted glass stays NEUTRAL WHITE under every lighting setup - warm "
         "light, dark grounds and gold surroundings light it, they do not dye it. "
         "Never render the glass or its contents amber, gold or yellow.",
         "The frosted glass keeps its OWN colour under every lighting setup - warm "
         "light, dark grounds and coloured surroundings light it, they do not "
         "re-dye it. Never let the surroundings tint the glass or its contents."),
    ],
    "cream_jar.json": [],
}


def patch(name: str) -> int:
    path = os.path.join(TPL, name)
    with open(path) as fh:
        tpl = json.load(fh)
    changes = []

    if tpl.get("t2i_material") != T2I[name]:
        tpl["t2i_material"] = T2I[name]
        changes.append("t2i_material -> product-driven")
    if tpl["language"].get("contents") != CONTENTS[name]:
        tpl["language"]["contents"] = CONTENTS[name]
        changes.append("language.contents -> product-driven")

    for old, new in MANDATORY[name]:
        mand = tpl["language"].get("mandatory", "")
        if new in mand:
            continue
        if old not in mand:
            print(f"  !! {name}: mandatory line not as expected, left alone")
            continue
        tpl["language"]["mandatory"] = mand.replace(old, new)
        changes.append("language.mandatory -> glass colour no longer hard-coded white")

    marked = 0
    for shot in tpl["shots"]:
        want = shot["n"] in SHOWS[name]
        if want and not shot.get("shows_formulation"):
            shot["shows_formulation"] = True
            marked += 1
        elif not want and "shows_formulation" in shot:
            del shot["shows_formulation"]
    if marked:
        changes.append(f"marked {marked} shot(s) shows_formulation")

    for n, pairs in EDITS[name].items():
        shot = next((s for s in tpl["shots"] if s["n"] == n), None)
        if shot is None:
            print(f"  !! {name}: no shot {n}")
            continue
        for old, new in pairs:
            if new in shot["brief"]:
                continue
            if old not in shot["brief"]:
                print(f"  !! {name} shot {n}: could not find {old[:52]!r}")
                continue
            shot["brief"] = shot["brief"].replace(old, new)
            changes.append(f"shot {n} {shot['name']}: colour removed")

    if not changes:
        print(f"  = {name} already current")
        return 0
    with open(path, "w") as fh:
        json.dump(tpl, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"  + {name}")
    for c in changes:
        print(f"      {c}")
    return len(changes)


def main() -> int:
    total = sum(patch(n) for n in ("serum_bottle.json", "cream_jar.json"))
    print(f"\n{total} change(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
