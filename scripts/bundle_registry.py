"""Which Skingenetix products are in which bundle — the one place that mapping lives.

Importable module, not a script. Consumers: `scripts/build-bundle-set.py`, and the publish
step, which needs `gid` and `label`.

The product lists were read off each bundle's OWN live Shopify description on 2026-09-11 (the
`<li>` items name the constituents), not inferred from the handle. Handles are lossy:
`skin-repair-renewal-serum-duo-set-pdrn-1-copper-peptide-ghk-cu-2` sounds like two serums and
is actually the PDRN serum with the Copper Peptide DAY GEL-CREAM.

`short` is used for filenames and wave ids. `gid` is the Shopify product, needed only at
publish time; all ten bundles are DRAFT with no media except the Copper trio, which shipped
2026-09-11.

Author: Claude Code, 2026-09-11.
"""

BUNDLES = {
    "complete-copper-peptide-ghk-cu-day-night-skincare-routine": dict(
        short="copper-peptide-routine", products=["cp_serum", "cp_day", "cp_night"],
        gid="gid://shopify/Product/15527281361281",
        label="Skingenetix Complete Copper Peptide (GHK-Cu) Day & Night Skincare Routine",
        done="published 2026-09-11 — 4 on the product, 8 in Files, 1 on the FAQ"),
    "day-night-copper-peptide-ghk-cu-duo-set": dict(
        short="copper-peptide-duo", products=["cp_day", "cp_night"],
        gid="gid://shopify/Product/15527302136193",
        label="Skingenetix Day & Night Copper Peptide (GHK-Cu) Duo Set"),
    "pdrn-1-serum-cream-full-set": dict(
        short="pdrn-ritual", products=["pdrn_serum", "pdrn_cream"],
        gid="gid://shopify/Product/15527306101121",
        label="Skingenetix Full PDRN 1% Ritual - Serum & Cream"),
    "full-matrixyl-3000-ritual-serum-cream": dict(
        short="matrixyl-ritual", products=["mat_serum", "mat_cream"],
        gid="gid://shopify/Product/15527306625409",
        label="Skingenetix Full Matrixyl 3000 Ritual - Serum & Cream"),
    "brightening-glow-duo-set-glutathione-serum-copper-peptide-ghk-cu-day-gel-cream": dict(
        short="brightening-duo", products=["glut_serum", "cp_day"],
        gid="gid://shopify/Product/15527315800449",
        label=("Skingenetix Brightening & Glow Duo Set - Glutathione Serum & "
               "Copper Peptide (GHK-Cu) Day Gel-Cream")),
    "skin-repair-renewal-serum-duo-set-pdrn-1-copper-peptide-ghk-cu-2": dict(
        short="repair-renewal-duo", products=["pdrn_serum", "cp_day"],
        gid="gid://shopify/Product/15527315964289",
        label=("Skingenetix Skin Repair & Renewal Duo Set - PDRN 1% Serum & "
               "Copper Peptide (GHK-Cu) Day Gel-Cream")),
    "complete-skin-repair-renewal-routine-pdrn-1-serum-copper-peptide-ghk-cu-serum-pdrn-collagen-cream": dict(
        short="repair-renewal-routine", products=["pdrn_serum", "cp_day", "pdrn_cream"],
        gid="gid://shopify/Product/15527316128129",
        label=("Skingenetix Complete Skin Repair & Renewal Day & Night Routine - PDRN 1% "
               "Serum, Copper Peptide (GHK-Cu) Day Gel-Cream & PDRN Collagen Night Cream")),
    "complete-fine-lines-wrinkles-routine-acetyl-hexapeptide-8-matrixyl-3000-serum-copper-peptide-ghk-cu-day-gel-cream": dict(
        short="wrinkles-routine", products=["acetyl_serum", "mat_serum", "cp_day"],
        gid="gid://shopify/Product/15527317143937",
        label=("Skingenetix Complete Fine Lines & Wrinkles Routine - Acetyl Hexapeptide-8 & "
               "Matrixyl 3000 Serum & Copper Peptide (GHK-Cu) Day Gel-Cream")),
    "complete-firming-skin-density-day-night-routine-matrixyl-3000-pro-collagen-cream-night-cream": dict(
        short="firming-routine", products=["mat_serum", "mat_cream", "cp_night"],
        gid="gid://shopify/Product/15527317504385",
        label=("Skingenetix Complete Firming & Skin Density Day & Night Routine - "
               "Matrixyl 3000, Pro-Collagen Cream & Night Cream")),
    "fine-lines-wrinkles-peptide-duo-set-matrixyl-3000-acetyl-hexapeptide-8-serums": dict(
        short="wrinkles-duo", products=["acetyl_serum", "mat_serum"],
        gid="gid://shopify/Product/15527323861377",
        label=("Skingenetix Fine Lines & Wrinkles Peptide Duo Set - Matrixyl 3000 + "
               "Acetyl Hexapeptide-8 Serums")),
}

#: The two the pilot runs, and why. Matrixyl serum+cream is the mildest collision - one colour,
#: two forms - so it proves the SHAPE clause. Acetyl+Matrixyl serums is the worst case in the
#: whole range: same colour, same form, same contents, separable only by label text. If that
#: one works, every other bundle does.
PILOT = ["full-matrixyl-3000-ritual-serum-cream",
         "fine-lines-wrinkles-peptide-duo-set-matrixyl-3000-acetyl-hexapeptide-8-serums"]
