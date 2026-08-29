#!/usr/bin/env python3
"""Rebalance the per-product review allocation to nine each, and add Malcolm's 25 new photographs.

    python3 scripts/product-reviews-rebalance.py --show
    python3 scripts/product-reviews-rebalance.py

Rewrites `configs/product-reviews.json` in place (a timestamped copy of the old one is kept
beside it). Then:

    python3 scripts/upload-theme-images.py configs/product-reviews.json
    python3 scripts/product-reviews-publish.py

THE ARITHMETIC
76 cards were live, spread 9/8/8/7/7/7/7/7/5/4 — the Glutathione serum had 5 and the Copper Day
Gel-Cream only 4. Drop the two duplicate photographs, add the 25 new ones, and it comes to
exactly 99, which is 9 per product across all 11. No product needed padding and none had to be
thinned; the numbers landed on their own.

THE TWO DROPS ARE DUPLICATE PHOTOGRAPHS, NOT WEAK ONES
A content hash over all 102 files in Drive finds three photographs filed under two customer names
each. Two of those pairs were BOTH live, which puts one woman on the site as two different
customers:

    General/Romy-S   == Wrinkles/Heather-S   -> Heather-S dropped, Romy-S kept
    General/Selma-D  == Wrinkles/Megan-A     -> Megan-A dropped, Selma-D kept
    Brightening/Regita-G == Brightening/Rowena-G  -> Regita-G never used, Rowena-G already live

Both drops happened to sit on the same product, which is why the Copper Renewal Serum needs three
new ones rather than one. The dropped entries are removed from the product lists but their
metaobjects are NOT deleted — the publish script's own warning applies: an entry carries its
translations, and delete-and-recreate drops every locale silently.

THE ONE MOVE
Dana-T goes from the Matrixyl Firming Serum to the Glutathione Brightening Serum. Hers is the
clearest mismatch in the set: the visible change is tone evenness on deeper skin, which is the
glutathione story, not firmness. Everything else stays where the original allocation put it —
the rest of the placements read as reasonable, and re-shuffling 76 cards on my own judgement from
thumbnails would be more likely to make it worse than better.

HOW THE 25 NEW ONES WERE PLACED
By the dominant visible change in the photograph, not by which Drive folder it arrived in. The
folders are a rough concern grouping, not a product mapping — several "Firming" images are really
tone or texture stories, and two "Wrinkles" images are redness. The per-card note below records
what was actually seen.

Author: Claude Code, 2026-08-29.
"""
import argparse
import json
import re
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLAN = ROOT / "configs" / "product-reviews.json"
DRIVE = Path.home() / ("Library/CloudStorage/GoogleDrive-msmithnl@gmail.com/My Drive/"
                       "Skingenetix/Images/Reviews ")

DROP = ["Heather-S", "Megan-A"]                       # duplicate photographs, see above
MOVE = {"Dana-T": "glutathione-brightening-serum"}    # tone, not firmness

# person, Drive folder, product, and what the photograph actually shows
NEW = [
    # --- pigment and tone -> Glutathione -------------------------------------------------
    ("Lucia-M",     "Brightening", "glutathione-brightening-serum",            "melasma across both cheeks clearing to an even tone"),
    ("Joyce-G",     "Brightening", "glutathione-brightening-serum",            "a dull, sallow complexion brightening"),
    ("Martine M",   "Brightening", "glutathione-brightening-serum",            "sun-damage pigment on the cheek evening out"),
    # --- daytime tone, radiance, mild texture -> Copper Day Gel-Cream ---------------------
    ("Sage-D",      "Brightening", "copper-peptide-ghk-cu-day-gel-cream",      "uneven freckled tone becoming more even"),
    ("Helen-S",     "Brightening", "copper-peptide-ghk-cu-day-gel-cream",      "under-eye tone and brightness"),
    ("Kimberly-N",  "Brightening", "copper-peptide-ghk-cu-day-gel-cream",      "cheek redness calming to an even tone"),
    ("Isabella-E",  "Firming",     "copper-peptide-ghk-cu-day-gel-cream",      "mid-face brightness and clarity"),
    ("Catalina-B",  "Brightening", "copper-peptide-ghk-cu-day-gel-cream",      "overall brightness, forehead softening"),
    # --- repair, renewal, texture -> Copper Renewal Serum ---------------------------------
    ("Samantha-F",  "Wrinkles",    "copper-peptide-ghk-cu-renewal-serum",      "overall texture on mature skin"),
    ("Ashley-H",    "Brightening", "copper-peptide-ghk-cu-renewal-serum",      "blemishes and redness on the cheek clearing"),
    ("Bianca-P",    "Wrinkles",    "copper-peptide-ghk-cu-renewal-serum",      "mid-face lines and overall smoothness"),
    # --- overnight repair, nasolabial, jowl -> Copper Night Cream --------------------------
    ("Mei-W",       "Firming",     "copper-peptide-ghk-cu-night-cream",        "nasolabial fold and jowl lifting"),
    ("Gillian-L",   "Wrinkles",    "copper-peptide-ghk-cu-night-cream",        "nasolabial and marionette lines softening"),
    # --- firmness, jawline, neck -> Matrixyl Pro-Collagen Cream ---------------------------
    ("Alexandra-B", "Firming",     "matrixyl-3000-pro-collagen-firming-cream", "jawline and neck laxity tightening"),
    ("Gabrielle-D", "Firming",     "matrixyl-3000-pro-collagen-firming-cream", "jaw and neck in macro, marionette lines"),
    # --- firmness with fine lines -> Matrixyl Firming Serum -------------------------------
    ("Caroline-D",  "Firming",     "matrixyl-3000-firming-serum",              "jowls firming across the lower face"),
    ("Evelyn-L",    "Firming",     "matrixyl-3000-firming-serum",              "nasolabial and cheek firmness"),
    # --- barrier, redness, regeneration -> PDRN Renewal Serum ------------------------------
    ("Josephine-R", "Wrinkles",    "pdrn-renewal-serum",                       "pronounced facial redness calming"),
    ("Robin-J",     "Firming",     "pdrn-renewal-serum",                       "tired, hollow under-eye looking fresher"),
    # --- deep renewal, plumpness -> PDRN Collagen Night Cream ------------------------------
    ("Danielle-S",  "Firming",     "pdrn-collagen-night-cream",                "jaw and cheek laxity plumping"),
    ("Madeline-W",  "Firming",     "pdrn-collagen-night-cream",                "jaw and neck firmness"),
    # --- microneedling: forehead lines and texture -> the two stamp sets --------------------
    ("Adriana-A",   "Wrinkles",    "pdrn-microneedling-facial-stamp-set-1-month", "forehead and glabellar lines in macro"),
    ("Valentina-L", "Wrinkles",    "pdrn-microneedling-facial-stamp-set-1-month", "forehead lines softening"),
    ("Sandra-P",    "Wrinkles",    "copper-peptide-ghk-cu-microneedling-facial-stamp-set-1-month", "forehead and glabellar lines, overall texture"),
    ("Beth-H",      "Wrinkles",    "copper-peptide-ghk-cu-microneedling-facial-stamp-set-1-month", "nasolabial and under-eye smoothing"),
]


def slug(person: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", person.lower()).strip("-")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--show", action="store_true", help="print the result, write nothing")
    args = ap.parse_args()

    plan = json.loads(PLAN.read_text())
    cards = [c for c in plan["cards"] if c["person"] not in DROP]
    dropped = len(plan["cards"]) - len(cards)

    for c in cards:
        if c["person"] in MOVE:
            c["product"] = MOVE[c["person"]]

    have = {c["person"] for c in cards}
    for person, concern, product, seen in NEW:
        if person in have:
            continue
        fn = f"skingenetix-review-before-after-{concern.lower()}-{slug(person)}.jpg"
        src = DRIVE / concern / f"{person}.png"
        if not src.exists():
            raise SystemExit(f"missing source: {src}")
        cards.append({
            "product": product, "concern": concern, "person": person, "filename": fn,
            "title": "PLACEHOLDER — review headline",
            "body": "PLACEHOLDER — the customer's review text goes here. This card has not been written yet.",
            "author": person.replace("-", " "), "rating": 5, "verified": True,
            "before_label": "Before", "after_label": "After",
            "_seen": seen,
        })
        plan["images"].append({
            "source": str(src), "filename": fn,
            "alt": f"Before and after photographs from a Skingenetix customer, showing {seen}",
        })

    from collections import Counter
    counts = Counter(c["product"] for c in cards)
    print(f"dropped {dropped} duplicate photographs, moved {len(MOVE)}, added {len(NEW)}")
    print(f"total cards: {len(cards)}\n")
    for p, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"  {n:>2}  {p}")
    spread = set(counts.values())
    print(f"\nspread: {sorted(spread)}  {'EVEN' if len(spread) == 1 else 'UNEVEN'}")

    if args.show:
        print("\n--show, nothing written")
        return

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    shutil.copy2(PLAN, PLAN.with_name(f"product-reviews-{stamp}.json"))
    plan["cards"] = cards
    PLAN.write_text(json.dumps(plan, indent=2) + "\n")
    print(f"\nwritten. previous plan kept at configs/product-reviews-{stamp}.json")


if __name__ == "__main__":
    main()
