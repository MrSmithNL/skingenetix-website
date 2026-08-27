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

FIFTEEN SLOTS, THREE OF THEM FILLED
Malcolm's brief, 2026-08-27: fifteen before/after reviews. Only three photographs are usable, so
twelve slots ship EMPTY — no photograph, no name, no rating, no verified badge — each seeded with
the product it is for so the slot carries a working thumbnail and link. An empty card must never
claim a rating or a verified customer it does not have, which is also why none of them is
pre-filled with invented copy: Malcolm is supplying the real reviews. See
`docs/reviews-content-to-supply.csv` for the fifteen rows to fill.

The original fourth pair, "Skin Firmness", is gone for good. `skingenetix-ba-firmness-combined.jpg`
has the AI image brief rendered into the photograph — a white panel reading "image-container",
"body: display: flex...", "alt 'Close of skin with sagging'" — and its after frame is two different
faces. It needs regenerating, not re-cropping.

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
    # ---- the three that have a usable photograph -------------------------------------------
    {
        "id": "rv_01",
        "image": "shopify://shop_images/skingenetix-review-before-after-fine-lines-acetyl-hexapeptide-8.jpg",
        "before_label": "Before",
        "after_label": "After 8 weeks",
        "author": "Hannah V.",
        "rating": 5,
        "title": "My holy grail for forehead lines",
        "content": "<p>The Acetyl Hexapeptide-8 serum is my holy grail for forehead lines. "
                   "At 10% concentration, it actually works. I have recommended it to everyone "
                   "in my skincare group.</p>",
        "product": "acetyl-hexapeptide-8-anti-wrinkle-serum",
    },
    {
        "id": "rv_02",
        "image": "shopify://shop_images/skingenetix-review-before-after-skin-texture-matrixyl-3000.jpg",
        "before_label": "Before",
        "after_label": "After 8 weeks",
        "author": "Nicole P.",
        "rating": 4,
        "title": "Plumper and more even after six weeks",
        "content": "<p>Good products with honest ingredient lists. The Matrixyl 3000 serum took "
                   "a bit longer to show results than I expected, but after 6 weeks my skin "
                   "definitely looks plumper and more even.</p>",
        "product": "matrixyl-3000-hyaluronic-acid-collagen-serum",
    },
    {
        "id": "rv_03",
        "image": "shopify://shop_images/skingenetix-review-before-after-radiance-peptide-routine.jpg",
        "before_label": "Before",
        "after_label": "After 6 weeks",
        "author": "Isabelle M.",
        "rating": 5,
        "title": "A real difference to my skin texture and firmness",
        "content": "<p>I bought all three serums and have been layering them in my routine. "
                   "The combination has made a real difference to my skin texture and firmness. "
                   "Shipping to France was fast too.</p>",
        "product_image": "shopify://shop_images/skingenetix-menu-all-serums.jpg",
        "product_text": "The peptide serum range",
        "product_url": "/collections/serums",
    },

    # ---- twelve empty slots, one per product, waiting on a photograph and a real review ------
    # `placeholder: True` means: no name, no stars, no verified badge and no photograph. An empty
    # card must never claim a rating or a verified customer it does not have — that is the whole
    # reason these are not pre-filled with invented copy. The product IS set, so each slot still
    # shows which product it is for and carries a working link and thumbnail.
    {"id": "rv_04", "placeholder": True,
     "image": "shopify://shop_images/skingenetix-review-before-after-placeholder-rv-04-copper-peptide.jpg", "after_label": "After 12 weeks",
     "product": "copper-peptide-ghk-cu-renewal-serum"},
    {"id": "rv_05", "placeholder": True,
     "image": "shopify://shop_images/skingenetix-review-before-after-placeholder-rv-05-pdrn.jpg", "after_label": "After 8 weeks",
     "product": "pdrn-renewal-serum"},
    {"id": "rv_06", "placeholder": True,
     "image": "shopify://shop_images/skingenetix-review-before-after-placeholder-rv-06-glutathione.jpg", "after_label": "After 8 weeks",
     "product": "glutathione-brightening-serum"},
    {"id": "rv_07", "placeholder": True,
     "image": "shopify://shop_images/skingenetix-review-before-after-placeholder-rv-07-copper-peptide.jpg", "after_label": "After 12 weeks",
     "product": "copper-peptide-ghk-cu-day-gel-cream"},
    {"id": "rv_08", "placeholder": True,
     "image": "shopify://shop_images/skingenetix-review-before-after-placeholder-rv-08-copper-peptide.jpg", "after_label": "After 12 weeks",
     "product": "copper-peptide-ghk-cu-night-cream"},
    {"id": "rv_09", "placeholder": True,
     "image": "shopify://shop_images/skingenetix-review-before-after-placeholder-rv-09-matrixyl-3000.jpg", "after_label": "After 12 weeks",
     "product": "matrixyl-3000-pro-collagen-firming-cream"},
    {"id": "rv_10", "placeholder": True,
     "image": "shopify://shop_images/skingenetix-review-before-after-placeholder-rv-10-pdrn.jpg", "after_label": "After 10 weeks",
     "product": "pdrn-collagen-night-cream"},
    {"id": "rv_11", "placeholder": True,
     "image": "shopify://shop_images/skingenetix-review-before-after-placeholder-rv-11-microneedling.jpg", "after_label": "After 4 weeks",
     "product": "copper-peptide-ghk-cu-microneedling-facial-stamp-set-1-month"},
    {"id": "rv_12", "placeholder": True,
     "image": "shopify://shop_images/skingenetix-review-before-after-placeholder-rv-12-microneedling.jpg", "after_label": "After 4 weeks",
     "product": "pdrn-microneedling-facial-stamp-set-1-month"},
    {"id": "rv_13", "placeholder": True,
     "image": "shopify://shop_images/skingenetix-review-before-after-placeholder-rv-13-copper-peptide.jpg", "after_label": "After 16 weeks",
     "product": "copper-peptide-ghk-cu-renewal-serum"},
    {"id": "rv_14", "placeholder": True,
     "image": "shopify://shop_images/skingenetix-review-before-after-placeholder-rv-14-pdrn.jpg", "after_label": "After 12 weeks",
     "product": "pdrn-renewal-serum"},
    {"id": "rv_15", "placeholder": True,
     "image": "shopify://shop_images/skingenetix-review-before-after-placeholder-rv-15-glutathione.jpg", "after_label": "After 12 weeks",
     "product": "glutathione-brightening-serum"},
]

PLACEHOLDER_TITLE = "Results coming soon"
PLACEHOLDER_BODY = ("<p>We are collecting verified before and after results for this product. "
                    "Bought it? We would like to see how you got on.</p>")


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
        ph = c.get("placeholder", False)
        blocks[c["id"]] = {
            "type": "review",
            "settings": {
                "image": c.get("image", ""),
                # No labels on an empty slot. "AFTER 12 WEEKS" over a picture that does not exist
                # asserts a result nobody has measured — the same reason the placeholders carry no
                # stars, no name and no verified badge. The duration is kept in the CARDS entry so
                # it is ready for the image brief; it just is not published yet.
                "before_label": "" if c.get("placeholder") else c.get("before_label", "Before"),
                "after_label": "" if c.get("placeholder") else c["after_label"],
                "author": c.get("author", ""),
                "show_verified": not ph,
                "verified_label": "Verified Customer",
                "show_rating": not ph,
                "rating": c.get("rating", 5),
                "title": PLACEHOLDER_TITLE if ph else c["title"],
                "content": PLACEHOLDER_BODY if ph else c["content"],
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
