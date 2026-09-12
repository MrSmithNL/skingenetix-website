#!/usr/bin/env python3
"""Emit a generate-multi wave config for one bundle product.

    python3 scripts/build-bundle-set.py <bundle-handle|short> [--out-date YYYY-MM-DD]
    python3 scripts/build-bundle-set.py --list
    python3 scripts/build-bundle-set.py --all

Then:
    set -a; source ~/.claude/config/image-credentials.env; set +a
    python3 scripts/generate-multi.py configs/banners/bundle-<short>-<date>.json \\
        --suppliers seedream,gpt_image,nbp_pro,nbp_flash --candidates 2

LUMA IS NOT BRIEFED on bundle waves. It scored 0 selections out of 36 across the whole Copper
Peptide run and 422'd out of a slot entirely; Malcolm dropped it on 2026-09-11. That also
removes its 6000-character cap, which is the only reason the Copper spec carried a second,
hand-trimmed copy of every product block. So these slots have no `prompt_luma` — passing
`--suppliers` without luma is part of the documented run command above, not an afterthought.
flux2 is skipped automatically wherever `ref_files` are present.

WHAT THIS ASSEMBLES
  product blocks   read from each product's own configs/<product>.json `product_desc`
  separation       computed per COLOUR CLUSTER by bundle_set_spec.separation()
  compositions     the 14 that earned a selection, filtered by what the bundle can serve
  placeholders     {A}/{B}/{C}, {BOTTLE}, {JAR}/{JAR2}, {ALL} resolved to this bundle

Every placeholder must resolve. A brief that still contains a literal brace is a brief that
names a product the bundle does not contain, and this exits rather than shipping it.

Author: Claude Code, 2026-09-11.
"""
import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bundle_compositions import COMPOSITIONS, applicable  # noqa: E402
from bundle_registry import BUNDLES  # noqa: E402
from bundle_set_spec import (  # noqa: E402
    MODEL, PRODUCTS, accent, build_slot, strategy,
)

ROOT = Path(__file__).resolve().parent.parent
#: The registry's `label` already begins with "Skingenetix" — it is the alt-text prefix used at
#: publish time — so the opening must not add it again.
OPENING = "A premium skincare product photograph of the {LABEL} set."


def resolve_handle(arg):
    if arg in BUNDLES:
        return arg
    for h, b in BUNDLES.items():
        if b["short"] == arg:
            return h
    sys.exit(f"unknown bundle {arg!r}. --list to see them.")


def placeholders(keys, label, ground, palette):
    """Map every placeholder a composition may use to this bundle's real product names.

    Products are ordered bottles-first so {A} is the tall element in a mixed bundle, which is
    what the pyramid and plinth compositions assume when they put {A} at the apex or centre.
    """
    ordered = sorted(keys, key=lambda k: 0 if PRODUCTS[k]["form"] == "bottle" else 1)
    names = [PRODUCTS[k]["name"] for k in ordered]
    jars = [PRODUCTS[k]["name"] for k in ordered if PRODUCTS[k]["form"] == "jar"]
    bottles = [PRODUCTS[k]["name"] for k in ordered if PRODUCTS[k]["form"] == "bottle"]
    # Count-aware wording. "at the centre" implies a symmetric row of three or more, and the
    # first two-product brief phrased that way came back with a duplicated third bottle.
    sub = {
        "LABEL": label,
        "ALL": (" and ".join(names) if len(names) == 2
                else ", ".join(names[:-1]) + " and " + names[-1]),
        "LEAD_POS": "on the left" if len(names) == 2 else "at the centre",
        "OTHERS": "the other product" if len(names) == 2 else "the others",
        "SIT": "sits" if len(names) == 2 else "sit",
        # A coloured ground is read off the products' own label accent rules, never a fixed
        # brand blue - Malcolm, 2026-09-12: the Matrixyl set should sit on teal, not blue.
        "ACCENT": ground,
        "ACCENT_PALETTE": palette,
        # Two hands hold two products; a third has to go somewhere she can still present it.
        "MODEL_HOLD": (
            f"The model holds {names[0]} in one hand and {names[1]} in the other, raised to "
            "about chest height and turned so both front labels face the camera."
            if len(names) == 2 else
            f"The model holds {names[0]} in one hand and {names[1]} in the other at about "
            f"chest height, with {names[2]} standing on the counter in front of her, all "
            "turned so every front label faces the camera."),
        # Only mention a third object when there IS one - "any further product"
        # is an invitation to invent one in a two-product bundle.
        "THIRD_LYING": ("" if len(names) < 3 else
                        f"{names[2]} lies ON ITS SIDE in the front centre with its "
                        "front label turned up. "),
    }
    for i, n in enumerate(names):
        sub["ABC"[i]] = n
    if bottles:
        sub["BOTTLE"] = bottles[0]
    if jars:
        sub["JAR"] = jars[0]
    if len(jars) > 1:
        sub["JAR2"] = jars[1]
    return sub, ordered


def fill(text, sub, slot_id):
    out = text
    for k, v in sub.items():
        out = out.replace("{" + k + "}", v)
    left = re.findall(r"\{([A-Z0-9]+)\}", out)
    if left:
        sys.exit(f"{slot_id}: unresolved placeholder(s) {sorted(set(left))} — this composition "
                 f"names something the bundle does not contain")
    return out


def build(handle, stamp):
    b = BUNDLES[handle]
    keys = b["products"]
    n_jars = sum(1 for k in keys if PRODUCTS[k]["form"] == "jar")
    n_bottles = len(keys) - n_jars
    ground, palette = accent(keys)
    sub, ordered = placeholders(keys, b["label"], ground, palette)

    slots = []
    skipped = []
    for c in COMPOSITIONS:
        if not applicable(c, len(keys), n_jars, n_bottles):
            skipped.append(c["id"])
            continue
        sid = f"{b['short']}-{c['id']}"
        slots.append(build_slot(
            sid,
            fill(OPENING, sub, sid),
            ordered,
            fill(c["arrangement"], sub, sid),
            fill(c["scene"], sub, sid),
            fill(c["frame"], sub, sid),
            extra=[MODEL] if c.get("model") else None))

    out = ROOT / "configs" / "banners" / f"bundle-{b['short']}-{stamp}.json"
    cfg = {
        "_comment": (
            f"{b['label']} — bundle set shots, {stamp}. GENERATED by "
            f"scripts/build-bundle-set.py; edit the builder or the composition library, not "
            f"this file. Products: {', '.join(keys)}. Separation strategy (worst collision in "
            f"this bundle): {strategy(keys)}. Only the compositions that earned a selection in "
            f"the Copper Peptide run are briefed — 31 of that run's 51 slots earned nothing, "
            f"so repeating all of them would spend most of the budget on measured rejects. "
            f"RUN WITHOUT LUMA: --suppliers seedream,gpt_image,nbp_pro,nbp_flash."),
        "wave": f"bundle-{b['short']}-{stamp}",
        "bundle_handle": handle,
        "product_gid": b["gid"],
        "product_label": b["label"],
        "defaults": {"negative_global": ""},
        "slots": slots,
    }
    out.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")

    print(f"{out.relative_to(ROOT)}")
    print(f"  {b['label']}")
    print(f"  products : {', '.join(PRODUCTS[k]['name'] for k in ordered)}")
    print(f"  jars     : {n_jars}   separation: {strategy(keys)}")
    print(f"  slots    : {len(slots)}" + (f"   (skipped {', '.join(skipped)})" if skipped else ""))
    lo = min(len(s["prompt"]) for s in slots)
    hi = max(len(s["prompt"]) for s in slots)
    print(f"  prompts  : {lo}-{hi} chars")
    print(f"  candidates at 4 suppliers x 2 = {len(slots) * 8}")
    return len(slots)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("bundle", nargs="?")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--out-date", default=date.today().isoformat())
    a = ap.parse_args()

    if a.list:
        for h, b in BUNDLES.items():
            n_jars = sum(1 for k in b["products"] if PRODUCTS[k]["form"] == "jar")
            n_bot = len(b["products"]) - n_jars
            n = sum(1 for c in COMPOSITIONS
                    if applicable(c, len(b["products"]), n_jars, n_bot))
            done = f"   [{b['done']}]" if b.get("done") else ""
            print(f"  {b['short']:<24} {len(b['products'])}p {n_jars}jar  "
                  f"{strategy(b['products']):<6} {n:>2} slots{done}")
        return 0

    targets = ([h for h, b in BUNDLES.items() if not b.get("done")] if a.all
               else [resolve_handle(a.bundle)] if a.bundle else [])
    if not targets:
        ap.print_help()
        return 2
    total = 0
    for h in targets:
        total += build(h, a.out_date)
        print()
    if len(targets) > 1:
        print(f"TOTAL {total} slots, {total * 8} candidates across {len(targets)} bundles")
    return 0


if __name__ == "__main__":
    sys.exit(main())
