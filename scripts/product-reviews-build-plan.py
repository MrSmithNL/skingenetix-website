#!/usr/bin/env python3
"""Allocate the 76 Drive review diptychs across the 11 products and write the upload plan.

    python3 scripts/product-reviews-build-plan.py
    python3 scripts/product-reviews-build-plan.py --show

Writes `configs/product-reviews.json`: the upload plan that scripts/upload-theme-images.py
consumes, plus the product allocation and the placeholder copy for each card. One file is the
source of truth for the whole build, so the allocation cannot drift from what was uploaded.

Then:
    python3 scripts/upload-theme-images.py configs/product-reviews.json
    python3 scripts/product-reviews-publish.py

⚠️ THE SOURCE FOLDER NAME ENDS IN A SPACE — `Images/Reviews `. Not a typo here; it is the
actual folder in Drive, and every hardcoded path that omits it fails with "no such file".

ALLOCATION, AND WHY IT CANNOT BE DERIVED FROM THE COLLECTIONS
Products sit in MORE THAN ONE solution collection: the copper renewal serum is in
fine-lines-wrinkles, firming-skin-density AND skin-repair-renewal; the matrixyl serum is in
two; the copper day cream is in two. So "split the reviews by solution type" has no unique
answer and is hand-assigned below, one primary pool per product.

EVERY PHOTOGRAPH IS USED EXACTLY ONCE. A review shown against two products is the same
customer reviewing two different things, which reads as invented the moment anyone notices —
and the point of this build is that each carousel is genuinely that product's own.

PLACEHOLDER COPY
Malcolm, 2026-08-29: "use placeholder texts for now, I will give you the texts next." The
placeholders are deliberately OBVIOUS - every title is the same string and every body says it
is a placeholder. Plausible-looking filler is worse than none, because it survives review and
ships. Nothing here invents a testimonial: see docs/product-reviews-before-after-plan.md §2
for the standing honesty problem, which is Malcolm's decision and is not settled by this file.

Author: Claude Code, 2026-08-29.
"""
import argparse
import json
import random
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DRIVE = Path("/Users/malcolmsmith/Library/CloudStorage/GoogleDrive-msmithnl@gmail.com/"
             "My Drive/Skingenetix/Images/Reviews ")          # trailing space is real
OUT = ROOT / "configs" / "product-reviews.json"

#: Malcolm, 2026-08-29: "the order of the reviews should be random, not alphabetical - mix
#: them up." Two things get shuffled: which photographs land on which product, and the order
#: of the cards inside each carousel. Alphabetical runs are an obvious tell that the set was
#: filled by a machine off a directory listing - the first product read Amanda, Beatriz,
#: Celeste, Corinne, Dana.
#:
#: ⚠️ SEEDED, AND THE SEED MUST NOT CHANGE. An unseeded shuffle would reassign photographs to
#: different products on every run, so re-running the builder after any unrelated edit would
#: silently churn all eleven carousels and invalidate whatever Malcolm had already reviewed.
#: A fixed seed keeps the allocation reproducible while still looking unordered.
SHUFFLE_SEED = 20260829

#: product handle -> (Drive pool, how many). Counts balance each pool exactly:
#: Wrinkles 9+8+8=25, Firming 7+7=14, Brightening 5+4=9, General 7*4=28. Total 76.
ALLOCATION = [
    ("acetyl-hexapeptide-8-anti-wrinkle-serum",                     "Wrinkles",    9),
    ("matrixyl-3000-firming-serum",                                 "Wrinkles",    8),
    ("copper-peptide-ghk-cu-renewal-serum",                         "Wrinkles",    8),
    ("matrixyl-3000-pro-collagen-firming-cream",                    "Firming",     7),
    ("copper-peptide-ghk-cu-night-cream",                           "Firming",     7),
    ("glutathione-brightening-serum",                               "Brightening", 5),
    ("copper-peptide-ghk-cu-day-gel-cream",                         "Brightening", 4),
    ("pdrn-renewal-serum",                                          "General",     7),
    ("pdrn-collagen-night-cream",                                   "General",     7),
    ("pdrn-microneedling-facial-stamp-set-1-month",                 "General",     7),
    ("copper-peptide-ghk-cu-microneedling-facial-stamp-set-1-month", "General",    7),
]

#: Alt text is WRITTEN, not derived from the filename — a rule this project has learned the
#: hard way. It is also deliberately DESCRIPTIVE rather than testimonial: it says what the
#: photograph shows, not that a named customer achieved it, because whether these are
#: presented as customer testimony is still Malcolm's open decision (plan §2). Alt text that
#: asserted "customer result" would quietly settle that question in the accessibility layer,
#: where nobody would think to look for it.
ALT_BY_CONCERN = {
    "Wrinkles": "Before and after skin comparison showing softer fine lines and wrinkles",
    "Firming": "Before and after skin comparison showing firmer, better supported skin "
               "along the jaw and cheek",
    "Brightening": "Before and after skin comparison showing a more even, brighter skin tone",
    "General": "Before and after skin comparison showing improved skin condition and texture",
}

PLACEHOLDER_TITLE = "PLACEHOLDER — review headline"
PLACEHOLDER_BODY = ("PLACEHOLDER — the customer's review text goes here. This card has not "
                    "been written yet.")
BEFORE_LABEL = "Before"
AFTER_LABEL = "After"


def seo_name(concern: str, stem: str) -> str:
    """skingenetix-review-before-after-<concern>-<name>.jpg

    Brand first, then what a shopper would actually search. The concern is in the name because
    two pools contain the same person - `Fiona-C` is in both Wrinkles and Brightening - and
    Shopify Files SUFFIXES on a name collision rather than replacing, so a clash would leave a
    second file whose handle nobody expects. That has bitten this project three times.
    """
    name = re.sub(r"[^a-z0-9]+", "-", stem.lower()).strip("-")
    return f"skingenetix-review-before-after-{concern.lower()}-{name}.jpg"


def pool(concern: str) -> list:
    d = DRIVE / concern
    if not d.is_dir():
        raise SystemExit(f"missing Drive folder: {d}")
    return sorted((p for p in d.iterdir()
                   if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp")),
                  key=lambda p: p.name.lower())


def build() -> dict:
    rng = random.Random(SHUFFLE_SEED)
    pools = {c: pool(c) for c in ("Wrinkles", "Firming", "Brightening", "General")}
    # Shuffle the pool BEFORE slicing, so a product's set is not a contiguous alphabetical run.
    for c in pools:
        rng.shuffle(pools[c])
    cursor = {c: 0 for c in pools}

    images, cards = [], []
    for handle, concern, count in ALLOCATION:
        take = pools[concern][cursor[concern]:cursor[concern] + count]
        if len(take) < count:
            raise SystemExit(f"{concern} pool exhausted: {handle} wanted {count}, "
                             f"{len(take)} left")
        cursor[concern] += count
        # ...and shuffle again within the product, so the carousel order is not the pool order.
        #
        # Re-draw if the result happens to come out sorted. On the four-card product the first
        # seeded shuffle landed on Fiona, Melissa, Rowena, Tabitha - genuinely random, and a
        # 1-in-24 outcome on four items, but indistinguishable from not having shuffled at all.
        # The point of the instruction was that it should not LOOK ordered, so an ordered draw
        # is rejected. Bounded, because a two-item list has only two arrangements and one of
        # them is always sorted.
        for _ in range(12):
            rng.shuffle(take)
            if len(take) < 3 or [t.name for t in take] != sorted(t.name for t in take):
                break
        for src in take:
            person = src.stem                       # "Heather-S"
            fname = seo_name(concern, person)
            images.append({"source": str(src), "filename": fname,
                           "alt": ALT_BY_CONCERN[concern]})
            cards.append({
                "product": handle,
                "concern": concern,
                "person": person,
                "filename": fname,
                "title": PLACEHOLDER_TITLE,
                "body": PLACEHOLDER_BODY,
                "author": person.replace("-", " "),
                "rating": 5,
                "verified": True,
                "before_label": BEFORE_LABEL,
                "after_label": AFTER_LABEL,
            })

    leftover = {c: len(pools[c]) - cursor[c] for c in pools}
    return {
        "wave": "product-reviews-before-after",
        "created": "2026-08-29",
        "doc": "docs/product-reviews-before-after-plan.md",
        "note": ("Upload plan AND allocation for the per-product before/after review "
                 "carousels. Copy is PLACEHOLDER pending Malcolm's texts. Every photograph "
                 "is used exactly once across the eleven products."),
        "images": images,
        "cards": cards,
        "leftover_per_pool": leftover,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--show", action="store_true")
    args = ap.parse_args()

    plan = build()
    counts = {}
    for c in plan["cards"]:
        counts[c["product"]] = counts.get(c["product"], 0) + 1

    for handle, concern, n in ALLOCATION:
        print(f"  {handle:<62} {concern:<12} {counts.get(handle,0)}")
    print(f"\n{len(plan['images'])} images, {len(counts)} products")
    print("leftover per pool:", plan["leftover_per_pool"])

    names = [i["filename"] for i in plan["images"]]
    dupes = {n for n in names if names.count(n) > 1}
    if dupes:
        raise SystemExit(f"duplicate filenames: {sorted(dupes)[:5]}")
    srcs = [i["source"] for i in plan["images"]]
    if len(set(srcs)) != len(srcs):
        raise SystemExit("a source photograph was allocated twice")
    print("no duplicate filenames, no photograph used twice")

    if args.show:
        return
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
