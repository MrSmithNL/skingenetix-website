#!/usr/bin/env python3
"""Put the real review copy onto the cards, and report exactly what is still missing.

    python3 scripts/product-reviews-fill-copy.py --report      # counts only, writes nothing
    python3 scripts/product-reviews-fill-copy.py --apply       # writes configs/product-reviews.json

Then publish the change:
    python3 scripts/product-reviews-publish.py

⚠️ DOES NOT REGENERATE THE ALLOCATION. It edits `title` and `body` on the cards already in
configs/product-reviews.json and touches nothing else. `product-reviews-build-plan.py` is now
STALE — its ALLOCATION still says 76 cards spread 9/8/8/7/7/5/4/7/7/7/7, while the live
allocation is 99 at nine per product, rebalanced by product-reviews-rebalance.py on 2026-08-29.
Running the old builder would silently revert the round. Use the rebalance script if the
allocation itself ever needs changing.

MATCHING RULES, in order:
  1. A text may only go on the product its section names. A review that says "day cream"
     cannot sit on a serum, and a review naming copper peptides cannot sit on a PDRN product.
  2. Texts stating an AGE are held back for a second pass, because they also have to match the
     woman in the photograph. They are listed by --report rather than placed blind.
  3. The `general` pool — reviews naming no product at all — fills whatever is left over,
     product-agnostic by construction.
  4. Anything still unfilled keeps its PLACEHOLDER text, which is deliberately obvious.

Author: Claude Code, 2026-08-29.
"""
import argparse
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLAN = ROOT / "configs" / "product-reviews.json"
TEXTS = ROOT / "configs" / "review-texts.json"
PLACEHOLDER = "PLACEHOLDER"

#: Age corrections, applied after assignment: (person_a, person_b) exchange their copy.
#:
#: The nine age-stating reviews were checked against the BEFORE frame of each woman's
#: photograph, which is the face a reader judges an age from. Eight read plausibly. Elena-S
#: drew "I'm 44" and does not: her frame is a jaw-and-neck crop showing real slackness and
#: marionette lines, and she reads mid-fifties. Emma-H sits on the same product and is the
#: younger-looking of the two, so they exchange — Emma-H takes the 44 and Elena-S the 52.
#:
#: Both cards keep their own photograph. Only the words move.
AGE_SWAPS = [
    ("Emma-H", "Elena-S"),          # 44 <-> 52, checked 2026-08-29
]


def load():
    plan = json.loads(PLAN.read_text())
    texts = json.loads(TEXTS.read_text())
    return plan, texts


def assign(plan, texts, place_aged=False):
    s2p = texts["section_to_product"]
    pool = defaultdict(list)          # product handle (or None) -> [review]
    for r in texts["reviews"]:
        if r.get("age") and not place_aged:
            continue
        pool[s2p[r["section"]]].append(r)

    cards = plan["cards"]
    by_product = defaultdict(list)
    for c in cards:
        by_product[c["product"]].append(c)

    assigned, used = {}, set()
    # 1-2. section-matched
    for handle, group in by_product.items():
        avail = pool.get(handle, [])
        for card, review in zip(group, avail):
            assigned[id(card)] = review
            used.add(id(review))
    # 3. the general pool mops up whatever is still placeholder
    generals = [r for r in pool.get(None, []) if id(r) not in used]
    gi = 0
    for handle, group in by_product.items():
        for card in group:
            if id(card) in assigned:
                continue
            if gi < len(generals):
                assigned[id(card)] = generals[gi]
                used.add(id(generals[gi]))
                gi += 1
    return assigned, by_product


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--place-aged", action="store_true",
                    help="also place the age-stating reviews (only after the photographs "
                         "have been checked against the ages)")
    args = ap.parse_args()

    plan, texts = load()
    assigned, by_product = assign(plan, texts, place_aged=args.place_aged)
    s2p = texts["section_to_product"]

    supply = defaultdict(int)
    for r in texts["reviews"]:
        supply[s2p[r["section"]]] += 1
    aged = [r for r in texts["reviews"] if r.get("age")]

    print(f"{'product':<58}{'slots':>6}{'filled':>7}{'gap':>5}")
    total_slots = total_filled = 0
    gaps = {}
    for handle in sorted(by_product, key=lambda h: -len(by_product[h])):
        group = by_product[handle]
        filled = sum(1 for c in group if id(c) in assigned)
        gap = len(group) - filled
        total_slots += len(group)
        total_filled += filled
        gaps[handle] = gap
        flag = "  <<<" if gap else ""
        print(f"  {handle[:56]:<56}{len(group):>6}{filled:>7}{gap:>5}{flag}")
    print(f"  {'TOTAL':<56}{total_slots:>6}{total_filled:>7}{total_slots-total_filled:>5}")

    unused = [r for r in texts["reviews"]
              if id(r) not in {id(v) for v in assigned.values()} and not r.get("age")]
    print(f"\ntexts transcribed        : {len(texts['reviews'])}")
    print(f"placed                   : {len(set(id(v) for v in assigned.values()))}")
    print(f"held back (state an age) : {len(aged)}  -> ages {sorted(r['age'] for r in aged)}")
    print(f"surplus, product-matched : {len(unused)}")
    if unused:
        for r in unused:
            print(f"    [{r['section']}] {r['title']}")

    if args.report or not args.apply:
        return

    for card in plan["cards"]:
        r = assigned.get(id(card))
        if r:
            card["title"] = r["title"]
            card["body"] = r["body"]

    by_person = {c["person"]: c for c in plan["cards"]}
    for a, b in AGE_SWAPS:
        if a in by_person and b in by_person:
            ca, cb = by_person[a], by_person[b]
            ca["title"], cb["title"] = cb["title"], ca["title"]
            ca["body"], cb["body"] = cb["body"], ca["body"]
            print(f"  age swap: {a} <-> {b}")
    PLAN.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n")
    still = sum(1 for c in plan["cards"] if c["title"].startswith(PLACEHOLDER))
    print(f"\nwrote {PLAN.relative_to(ROOT)} — {still} cards still on placeholder copy")


if __name__ == "__main__":
    main()
