#!/usr/bin/env python3
"""Swap the product template's generic before/after grid for the per-product carousel.

    python3 scripts/product-reviews-add-section.py --dry-run
    python3 scripts/product-reviews-add-section.py
    python3 scripts/product-reviews-add-section.py --restore backups/product.json-<stamp>.json

WHAT CHANGES
`templates/product.json` section `before_after` is a `multi-column`: three static image tiles
under the heading "Verified Customer Results", the SAME three on all eleven products because
they all share this one template. It becomes `product-reviews-before-after`, which resolves
its cards from the product's own `custom.customer_reviews` metafield — so each product page
shows its own customers.

REPLACED IN PLACE, KEEPING THE SECTION ID. Not appended: two before/after sections on one
product page is worse than the generic one on its own. Keeping the id `before_after` also
holds the section's position in `order` (between `reasons_why` and the Klaviyo block) without
touching the order array. This is exactly what reviews-add-before-after-carousel.py did to the
reviews page on 2026-08-27, and it exists as its own script for the same reason: patch-template.py
cannot express a change of section TYPE.

⚠️ A TYPE SWAP ORPHANS THAT SECTION'S TRANSLATIONS. The old settings keys
(`section.product.json.before_after.title:<hash>` and the three block titles) stop existing, so
any translation attached to them is dropped. Only `en` is published today, so nothing is lost
right now — but this is the reason to settle wording before translating, not after.

⚠️ WHAT THIS DOES NOT TOUCH, DELIBERATELY. The `customer_reviews` section further down the same
template is a `testimonials` block carrying four invented quotes — "Sarah M. - Verified
Customer" and three more — on a store with zero orders. It is the standing fabricated-social-
proof problem (docs/todo.md REVIEW-001) and removing it is Malcolm's call, not a side effect of
this change. Note it will now sit directly below a second set of review cards making the same
claim. Also untouched: the Klaviyo Reviews product-reviews app block, which is ALREADY
INSTALLED on this template — the real review corpus has somewhere to land when orders exist.

Author: Claude Code, 2026-08-29.
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
TEMPLATE = "templates/product.json"
SECTION_ID = "before_after"
NEW_TYPE = "product-reviews-before-after"

SETTINGS = {
    "full_width": False,
    "subheading": "Real results",
    "title": "Before and after",
    "content": "<p>Photographed by customers at home, weeks apart.</p>",
    "verified_label": "Verified Customer",
    "link_text": "",
    "link_url": "",
    "background": "#f7f5f2",
    "text_color": "#1a1a1a",
    "heading_color": "#0f2f2b",
    "card_background": "#ffffff",
    "card_text_color": "#1a1a1a",
    "label_background": "#0f2f2b",
    "label_text_color": "#ffffff",
    "verified_color": "#0f7b6c",
}


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
    for _ in range(6):
        try:
            with urllib.request.urlopen(req, timeout=90) as res:
                out = json.loads(res.read())
            time.sleep(0.5)
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--restore")
    args = ap.parse_args()

    e = env()
    store = e["SHOPIFY_SKINGENETIX_STORE"]
    tok = token(e)
    theme = live_theme(store, tok)

    if args.restore:
        raw = Path(args.restore).read_text()
        call(store, tok, f"themes/{theme['id']}/assets.json", "PUT",
             {"asset": {"key": TEMPLATE, "value": raw}})
        print(f"restored {TEMPLATE} from {args.restore}")
        return

    raw = call(store, tok,
               f"themes/{theme['id']}/assets.json?asset[key]={TEMPLATE}")["asset"]["value"]
    doc = json.loads(raw)

    old = doc["sections"].get(SECTION_ID)
    if old is None:
        sys.exit(f"section `{SECTION_ID}` not found in {TEMPLATE}")
    print(f"theme      : {theme['id']} {theme['name']}")
    print(f"section    : {SECTION_ID}  {old['type']} -> {NEW_TYPE}")
    print(f"old blocks : {len(old.get('blocks', {}))} (dropped; the new section has none)")

    doc["sections"][SECTION_ID] = {"type": NEW_TYPE, "settings": SETTINGS}

    if args.dry_run:
        print("\n--dry-run, nothing written. New section JSON:")
        print(json.dumps(doc["sections"][SECTION_ID], indent=2)[:600])
        return

    BACKUPS.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    bak = BACKUPS / f"product.json-{stamp}.json"
    bak.write_text(raw)

    call(store, tok, f"themes/{theme['id']}/assets.json", "PUT",
         {"asset": {"key": TEMPLATE, "value": json.dumps(doc, indent=2, ensure_ascii=False)}})

    print(f"\nwritten. order unchanged: {doc['order']}")
    print(f"UNDO: python3 scripts/product-reviews-add-section.py --restore {bak.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
