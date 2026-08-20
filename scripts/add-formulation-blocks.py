#!/usr/bin/env python3
"""Add `formulation` and `palette` blocks to the product configs.

Why this exists (2026-08-20): the substance inside the container was never
described anywhere. `product_desc` covers the glass, the collar and the pipette
in forensic detail and stops there, so on any shot showing a drop or a swatch
the model invented a colour - white cream and clear serum every time. Malcolm
rejected most of the Glutathione drop shots for exactly that, then the Copper
Peptide ones, whose serum and cream are BLUE because GHK-Cu is blue.

`palette` is the second half of the same fault: scene tints were hard-coded into
the shared shot briefs, so every product got the same terracotta, amber and teal
regardless of its own colour.

Both are data, not code, so a product cannot be run until someone has said what
colour its contents are - see the preflight guard in templates.py.

Author: Claude Code, 2026-08-20.
"""
import json
import os
import sys

# Brand colours read off Malcolm's own swatches in
# Drive/Skingenetix/Images/Products/_Colors/ - not invented, not eyeballed.
BLOCKS = {
    "copper-peptide-repair-serum": {
        "formulation": {
            "substance": "serum",
            "appearance": ("a clear, lightly viscous liquid with a distinct medium-blue "
                           "tint - the natural colour of GHK-Cu copper peptides"),
            "hex": "#2F6FD0",
            "never": ("white, milky, cream-coloured, opaque, golden, amber, yellow, "
                      "or colourless water-clear"),
        },
        "palette": {
            "name": "clinical blue",
            "hex": "#014EB1",
            "scene": "cool blues, steel greys, clean whites and pale ice tones",
            "never": "terracotta, amber, gold, peach, warm brown, blush pink, teal, green",
        },
    },
    "copper-peptide-day-repair-cream": {
        "formulation": {
            "substance": "cream",
            "appearance": ("an opaque cream of a soft pale blue, smooth and satin rather "
                           "than glossy - tinted by the GHK-Cu copper peptides it carries"),
            "hex": "#8FB4E3",
            "never": "white, off-white, ivory, cream-coloured, golden, amber, yellow, pink",
        },
        "palette": {
            "name": "clinical blue",
            "hex": "#014EB1",
            "scene": "cool blues, steel greys, clean whites and pale ice tones",
            "never": "terracotta, amber, gold, peach, warm brown, blush pink, teal, green",
        },
    },
    "copper-peptide-night-repair-cream": {
        "formulation": {
            "substance": "cream",
            "appearance": ("an opaque cream of a soft blue, a shade deeper than the day "
                           "cream, smooth and satin rather than glossy - tinted by the "
                           "GHK-Cu copper peptides it carries"),
            "hex": "#6F9BD1",
            "never": "white, off-white, ivory, cream-coloured, golden, amber, yellow, pink",
        },
        "palette": {
            "name": "clinical blue",
            "hex": "#014EB1",
            "scene": "cool blues, deep midnight blues, steel greys and clean whites",
            "never": "terracotta, amber, gold, peach, warm brown, blush pink, teal, green",
        },
    },
    "glutathione-brightening-serum": {
        "formulation": {
            "substance": "serum",
            "appearance": ("a completely transparent, colourless liquid - water-clear and "
                           "lightly viscous, reading only as refraction and highlight"),
            "hex": None,
            "never": ("white, milky, opaque, cream-coloured, golden, amber, yellow, "
                      "or any visible tint at all"),
        },
        "palette": {
            "name": "champagne gold",
            "hex": "#DFC08F",
            "scene": "warm champagne golds, soft ivories, pale sand and clean whites",
            "never": "blue, teal, green, purple, terracotta, hot pink",
        },
    },
    "pdrn-collagen-repair-cream": {
        "formulation": {
            "substance": "cream",
            "appearance": ("an opaque cream of a soft blush pink, smooth and satin rather "
                           "than glossy"),
            "hex": "#F3BFC2",
            "never": "white, off-white, ivory, golden, amber, yellow, blue, green",
        },
        "palette": {
            "name": "blush pink",
            "hex": "#F3BFC2",
            "scene": "blush pinks, warm rose neutrals, soft ivories and clean whites",
            "never": "blue, teal, green, purple, terracotta, amber, gold",
        },
    },
}


def main() -> int:
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    changed = 0
    for slug, blocks in BLOCKS.items():
        path = os.path.join(root, "configs", f"{slug}.json")
        if not os.path.exists(path):
            print(f"  !! no config for {slug}")
            continue
        with open(path) as fh:
            cfg = json.load(fh)
        before = json.dumps(cfg, sort_keys=True)
        cfg["formulation"] = blocks["formulation"]
        cfg["palette"] = blocks["palette"]
        if json.dumps(cfg, sort_keys=True) == before:
            print(f"  = {slug} already current")
            continue
        with open(path, "w") as fh:
            json.dump(cfg, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        f = blocks["formulation"]
        print(f"  + {slug}")
        print(f"      {f['substance']}: {f['appearance'][:66]}...")
        print(f"      palette: {blocks['palette']['name']} {blocks['palette']['hex']}")
        changed += 1
    print(f"\n{changed} config(s) updated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
