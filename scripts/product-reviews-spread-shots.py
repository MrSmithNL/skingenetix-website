#!/usr/bin/env python3
"""Even out the shot types across the eleven carousels by swapping photographs between them.

    python3 scripts/product-reviews-spread-shots.py --show
    python3 scripts/product-reviews-spread-shots.py --apply
    python3 scripts/product-reviews-reorder.py --apply
    python3 scripts/product-reviews-publish.py

Malcolm, 2026-08-29: "we should not have 2 of the same type of shots next to each other (half
face, neck, forehead, close up etc) also make sure the type of shot vary on each product review
carousel."

⚠️ THE FIRST HALF OF THAT CANNOT BE DONE, AND IT IS THE POOL'S FAULT, NOT THE ORDERING'S.
72 of the 99 photographs are ordinary close-ups. A nine-card carousel therefore holds six to
eight of them, and any arrangement of eight closes in nine positions puts two side by side.
Ordering cannot fix a supply problem. What CAN be fixed:

  - the 27 distinctive shots (half-face, neck, forehead, eye, macro) are currently bunched:
    the Matrixyl firming cream holds six of them and the Copper stamp set holds NONE, so one
    carousel is all variety and another is nine near-identical head-and-shoulders.
  - no two of the same DISTINCTIVE type need ever be adjacent, and after this they are not.

So this script moves photographs between products until every carousel has two or three
distinctive shots, and product-reviews-reorder.py then spaces them out.

WHAT MOVES AND WHAT DOES NOT
Only the PHOTOGRAPH moves. Each card keeps the review text it already has, because the text is
bound to its product — a Copper day cream review cannot follow a photograph onto a PDRN serum.

⚠️ CARDS CARRYING AN AGE ARE NEVER SWAPPED. Nine reviews say "I'm 48" or "I'm 58", and those
were matched by eye against the woman in the photograph earlier today. Moving either half of
that pair would silently undo the match, which is the kind of change that looks like nothing
and reads as a lie.

Author: Claude Code, 2026-08-29.
"""
import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLAN = ROOT / "configs" / "product-reviews.json"

#: Photograph swaps Malcolm asked for by name, applied after the automatic spread.
#: Only the photograph moves; each card keeps the review text bound to its product.
MANUAL_PHOTO_SWAPS = [
    ("Amanda-P", "Adriana-A"),      # Malcolm, 2026-08-29
    # Malcolm, 2026-08-29: Fenna-S and June-K are plainly wrinkle photographs, so they belong
    # on the anti-wrinkle serum. Gabrielle-D (a firming neck crop) and Elizabeth-L go back the
    # other way, which also keeps every photograph in use exactly once.
    ("Fenna-S", "Elizabeth-L"),
    ("June-K", "Gabrielle-D"),
]

TARGET_MIN = 2          # distinctive shots every carousel should end up with
AGE_RE = re.compile(r"I'm (\d\d)|I am (\d\d)|I just turned (\d\d)|My (\d\d)-year-old")


def shots():
    """Reuse the tags in the reorder script — one table, not two that can drift apart."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "reorder", ROOT / "scripts" / "product-reviews-reorder.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return {k: v[2] for k, v in mod.TAGS.items()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--show", action="store_true")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    SHOT = shots()
    plan = json.loads(PLAN.read_text())
    cards = plan["cards"]

    def shot_of(c):
        return SHOT.get(c["person"], "close")

    def aged(c):
        return bool(AGE_RE.search(c["body"]))

    by_product = defaultdict(list)
    for c in cards:
        by_product[c["product"]].append(c)

    def distinctive(prod):
        return [c for c in by_product[prod] if shot_of(c) != "close"]

    print("before:")
    for p in by_product:
        print(f"  {p[:50]:<52} {len(distinctive(p))} distinctive "
              f"{sorted(shot_of(c) for c in distinctive(p))}")

    # Repeatedly move one distinctive photograph from the richest carousel to the poorest.
    moves = []
    for _ in range(40):
        rich = max(by_product, key=lambda p: len(distinctive(p)))
        poor = min(by_product, key=lambda p: len(distinctive(p)))
        if len(distinctive(rich)) - len(distinctive(poor)) <= 1:
            break
        if len(distinctive(poor)) >= TARGET_MIN and len(distinctive(rich)) <= TARGET_MIN + 1:
            break
        # a distinctive card in `rich` whose own text carries no age...
        give = next((c for c in distinctive(rich) if not aged(c)), None)
        # ...traded against a plain close-up in `poor`, likewise age-free
        take = next((c for c in by_product[poor]
                     if shot_of(c) == "close" and not aged(c)), None)
        if not give or not take:
            break
        # `author` moves with the face. It is derived from the person, so leaving it behind
        # labels one woman's photograph with another woman's name — which is exactly what
        # happened on the Amanda-P / Adriana-A swap and is invisible in the JSON diff.
        for f in ("person", "concern", "filename"):
            give[f], take[f] = take[f], give[f]
        give["author"] = give["person"].replace("-", " ")
        take["author"] = take["person"].replace("-", " ")
        moves.append((rich, poor, take["person"], give["person"]))

    print("\nmoves (photograph only; text stays with its product):")
    for rich, poor, moved, back in moves:
        print(f"  {moved:<14} {rich[:34]:<36} -> {poor[:34]}")
    print(f"\n{len(moves)} photographs moved")

    print("\nafter:")
    for p in by_product:
        print(f"  {p[:50]:<52} {len(distinctive(p))} distinctive "
              f"{sorted(shot_of(c) for c in distinctive(p))}")

    if args.show or not args.apply:
        return
    PLAN.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n")
    print(f"\nwrote {PLAN.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
