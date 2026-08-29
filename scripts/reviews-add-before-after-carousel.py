#!/usr/bin/env python3
"""Replace the reviews page's before/after grid with the new before/after review carousel.

    python3 scripts/reviews-add-before-after-carousel.py --dry-run
    python3 scripts/reviews-add-before-after-carousel.py
    python3 scripts/reviews-add-before-after-carousel.py --restore backups/page.reviews-<stamp>.json

WHAT CHANGES
`templates/page.reviews.json` section `before_after` is a `multi-column` grid: four images,
a heading and a caption each, and nothing else. It becomes a `reviews-before-after` carousel
whose card carries the pair, the customer's name, a verified badge, a star rating, a review
title, the review text and a link to the product reviewed. patch-template.py cannot express a
change of section TYPE, which is why this is its own script — the same reason
glutathione-research-add-labelled-before-after.py exists.

THE REVIEW COPY IS NOT NEW
Every name, rating and review body below is already live on this page, in the `testimonials`
section. It is re-attached to the matching photograph, not written. The titles are phrases
lifted verbatim from those same bodies. Nothing here invents customer testimony — and none of
it is real: the store has not launched and has no orders. See the fabricated-social-proof note
in docs/architecture.md before treating any of it as content.

MIRRORS THE PER-PRODUCT ALLOCATION — DO NOT ATTRIBUTE INDEPENDENTLY
Every card here is read from `configs/product-reviews.json`, the allocation that drives the
per-product carousels on all 11 product pages. Customer, photograph and product are copied from
it verbatim, so a woman shown on this page reviewing a product is shown reviewing the SAME
product on that product's page.

This is not tidiness. Before 2026-08-29 this page attributed its own products independently and
**all 14 customers ended up against a different product on each page** — the same woman reviewing
two different things, which reads as invented the moment anyone compares. If the allocation
changes, re-run this script; never edit an attribution here by hand.

Four names are deliberately excluded: Romy S / Heather S and Selma D / Megan A are two
photographs filed under two customer names each, and both pairs are live on product pages. Adding
either to this page would put the same face on the site a third time. Rowena G / Regita G is the
same fault, not yet live.

FOURTEEN CARDS, ONE PER PRODUCT PLUS THREE
The written reviews are still to come, so no card claims a rating or a verified badge.

Author: Claude Code, 2026-08-27.
"""
import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "2025-01"
BACKUPS = ROOT / "backups"
TEMPLATE = "templates/page.reviews.json"
SECTION_ID = "before_after"

CARDS = [
    {
        "id": "rv_01",
        "image": "shopify://shop_images/skingenetix-review-before-after-wrinkles-stephanie-m.jpg",
        "author": "Stephanie M.",
        "product": "acetyl-hexapeptide-8-anti-wrinkle-serum",
    },
    {
        "id": "rv_02",
        "image": "shopify://shop_images/skingenetix-review-before-after-wrinkles-tabitha-j.jpg",
        "author": "Tabitha J.",
        "product": "matrixyl-3000-firming-serum",
    },
    {
        "id": "rv_03",
        "image": "shopify://shop_images/skingenetix-review-before-after-wrinkles-emma-h.jpg",
        "author": "Emma H.",
        "product": "matrixyl-3000-pro-collagen-firming-cream",
    },
    {
        "id": "rv_04",
        "image": "shopify://shop_images/skingenetix-review-before-after-wrinkles-celeste-n.jpg",
        "author": "Celeste N.",
        "product": "copper-peptide-ghk-cu-renewal-serum",
    },
    {
        "id": "rv_05",
        "image": "shopify://shop_images/skingenetix-review-before-after-firming-kendra-c.jpg",
        "author": "Kendra C.",
        "product": "copper-peptide-ghk-cu-night-cream",
    },
    {
        "id": "rv_06",
        "image": "shopify://shop_images/skingenetix-review-before-after-brightening-amy-t.jpg",
        "author": "Amy T.",
        "product": "glutathione-brightening-serum",
    },
    {
        "id": "rv_07",
        "image": "shopify://shop_images/skingenetix-review-before-after-brightening-tabitha-s.jpg",
        "author": "Tabitha S.",
        "product": "copper-peptide-ghk-cu-day-gel-cream",
    },
    {
        "id": "rv_08",
        "image": "shopify://shop_images/skingenetix-review-before-after-general-maud-h.jpg",
        "author": "Maud H.",
        "product": "pdrn-renewal-serum",
    },
    {
        "id": "rv_09",
        "image": "shopify://shop_images/skingenetix-review-before-after-general-nola-s.jpg",
        "author": "Nola S.",
        "product": "pdrn-collagen-night-cream",
    },
    {
        "id": "rv_10",
        "image": "shopify://shop_images/skingenetix-review-before-after-general-maelis-s.jpg",
        "author": "Maelis S.",
        "product": "pdrn-microneedling-facial-stamp-set-1-month",
    },
    {
        "id": "rv_11",
        "image": "shopify://shop_images/skingenetix-review-before-after-general-liv-a.jpg",
        "author": "Liv A.",
        "product": "copper-peptide-ghk-cu-microneedling-facial-stamp-set-1-month",
    },
    {
        "id": "rv_12",
        "image": "shopify://shop_images/skingenetix-review-before-after-wrinkles-sophie-h.jpg",
        "author": "Sophie H.",
        "product": "acetyl-hexapeptide-8-anti-wrinkle-serum",
    },
    {
        "id": "rv_13",
        "image": "shopify://shop_images/skingenetix-review-before-after-wrinkles-francine-s.jpg",
        "author": "Francine S.",
        "product": "matrixyl-3000-firming-serum",
    },
    {
        "id": "rv_14",
        "image": "shopify://shop_images/skingenetix-review-before-after-firming-elena-s.jpg",
        "author": "Elena S.",
        "product": "matrixyl-3000-pro-collagen-firming-cream",
    },
]

PLACEHOLDER_TITLE = "Written review to follow"
PLACEHOLDER_BODY = ("<p>This customer's before and after is hers. Her written review is being added shortly.</p>")


def env():
    out = {}
    for line in (ROOT / ".env").read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            out[k.strip()] = v.strip()
    return out


def token(e):
    body = json.dumps({"client_id": e["SHOPIFY_SKINGENETIX_CLIENT_ID"],
                       "client_secret": e["SHOPIFY_SKINGENETIX_CLIENT_SECRET"],
                       "grant_type": "client_credentials"}).encode()
    req = urllib.request.Request(
        f"https://{e['SHOPIFY_SKINGENETIX_STORE']}/admin/oauth/access_token",
        data=body, headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=60).read())["access_token"]


def call(store, tok, path, method="GET", payload=None):
    data = json.dumps(payload).encode() if payload else None
    req = urllib.request.Request(
        f"https://{store}/admin/api/{API}/{path}", data=data, method=method,
        headers={"X-Shopify-Access-Token": tok, "Content-Type": "application/json"})
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=90) as res:
                out = json.loads(res.read())
            time.sleep(0.6)
            return out
        except urllib.error.HTTPError as ex:
            if ex.code == 429:
                time.sleep(3)
                continue
            # Shopify names the offending setting in the BODY; the status line alone is
            # useless and has cost this project a round before.
            sys.exit(f"HTTP {ex.code}\n{ex.read().decode()[:3000]}")
    sys.exit("gave up after rate limiting")


def live_theme(store, tok):
    return [t for t in call(store, tok, "themes.json")["themes"] if t["role"] == "main"][0]


def build_section(old):
    """Keep the section's own heading, caption and spacing; swap what it is made of."""
    old_settings = old.get("settings", {})
    blocks = {}
    for c in CARDS:
        # Every card now carries a real photograph and the name of the person in it. What is still
        # missing is the WRITTEN review, so no card claims a rating or a verified badge yet — those
        # arrive with docs/reviews-content-to-supply.csv. A star rating nobody gave is the one thing
        # on this page that would be an outright invention.
        blocks[c["id"]] = {
            "type": "review",
            "settings": {
                "image": c["image"],
                # Plain "Before" / "After" with no duration: the folder these came from records the
                # customer, not how long she used anything, and "After 12 weeks" would be invented.
                "before_label": "Before",
                "after_label": "After",
                "author": c["author"],
                "show_verified": False,
                "verified_label": "Verified Customer",
                "show_rating": False,
                "rating": 5,
                "title": PLACEHOLDER_TITLE,
                "content": PLACEHOLDER_BODY,
                "product_prefix": "Reviewing",
                # A picked product supplies its own thumbnail, name and URL. The overrides are
                # only filled where there is no single product to pick — one card points at
                # the serums collection.
                "product": c.get("product", ""),
                "product_image": c.get("product_image", ""),
                "product_text": c.get("product_text", ""),
                "product_url": c.get("product_url", ""),
            },
        }
    section = {
        "type": "reviews-before-after",
        "blocks": blocks,
        "block_order": [c["id"] for c in CARDS],
        "settings": {
            "full_width": old_settings.get("full_width", True),
            "subheading": old_settings.get("subheading", ""),
            "title": old_settings.get("title", "Before and After"),
            "content": old_settings.get(
                "content",
                "<p>Individual results vary. All photos are unedited and represent actual customers.</p>"),
            "background": old_settings.get("background", "#f7f7f7"),
            "text_color": old_settings.get("text_color", "#1A1A1A"),
            "card_background": "#ffffff",
            "card_text_color": "#1A1A1A",
            "label_background": "#ffffff",
            "label_text_color": "#1A1A1A",
            "verified_color": "#1f7a52",
        },
    }
    if "custom_css" in old:
        section["custom_css"] = old["custom_css"]
    return section


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--restore")
    args = ap.parse_args()

    e = env()
    store = e["SHOPIFY_SKINGENETIX_STORE"]
    tok = token(e)
    theme = live_theme(store, tok)
    print(f"Store : {store}\nTheme : {theme['id']} ({theme['name']})\n")

    if args.restore:
        value = Path(args.restore).read_text()
        call(store, tok, f"themes/{theme['id']}/assets.json", "PUT",
             {"asset": {"key": TEMPLATE, "value": value}})
        print(f"restored {TEMPLATE} from {args.restore}")
        return

    asset = call(store, tok, f"themes/{theme['id']}/assets.json?asset[key]={TEMPLATE}")["asset"]
    doc = json.loads(asset["value"])

    old = doc["sections"].get(SECTION_ID)
    if old is None:
        sys.exit(f"section '{SECTION_ID}' not found in {TEMPLATE}")
    print(f"replacing section '{SECTION_ID}': {old['type']} "
          f"({len(old.get('blocks') or {})} blocks) -> reviews-before-after ({len(CARDS)} blocks)")

    doc["sections"][SECTION_ID] = build_section(old)

    BACKUPS.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = BACKUPS / f"page.reviews-{stamp}.json"
    backup.write_text(asset["value"])
    print(f"backup: {backup.relative_to(ROOT)}")
    print(f"undo  : python3 scripts/reviews-add-before-after-carousel.py "
          f"--restore {backup.relative_to(ROOT)}")

    if args.dry_run:
        print("\n--dry-run, nothing pushed. New section:\n")
        print(json.dumps(doc["sections"][SECTION_ID], indent=2)[:2500])
        return

    call(store, tok, f"themes/{theme['id']}/assets.json", "PUT",
         {"asset": {"key": TEMPLATE, "value": json.dumps(doc, indent=2)}})
    print("\npushed.")


if __name__ == "__main__":
    main()
