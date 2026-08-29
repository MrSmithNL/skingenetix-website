#!/usr/bin/env python3
"""Create the customer_review metaobject entries and attach them to their products.

    python3 scripts/product-reviews-publish.py --dry-run
    python3 scripts/product-reviews-publish.py
    python3 scripts/product-reviews-publish.py --clear     # detach from all products

Reads `configs/product-reviews.json` (written by product-reviews-build-plan.py, then filled in
with `uploaded_handle` by upload-theme-images.py) and:

  1. resolves each uploaded filename to its MediaImage GID
  2. UPSERTS one `customer_review` metaobject entry per card, by deterministic handle
  3. sets each product's `custom.customer_reviews` list, in allocation order

IDEMPOTENT BY HANDLE. Every entry gets a stable handle — `review-<concern>-<person>` — and is
written with metaobjectUpsert. Re-running updates in place rather than creating a second copy,
which matters twice over: duplicate entries would double the cards on a page, and Malcolm's
translations key off the entry, so a delete-and-recreate would silently drop every locale.
That exact mistake cost the sister brand its German mega-menu (production-safety incident log,
2026-03-14). Never delete an entry to "refresh" it.

⚠️ `shopify://shop_images/...` IS NOT A METAFIELD VALUE. That form resolves against Content ›
Files for THEME references only. A `file_reference` metafield needs the MediaImage GID, so the
handles the uploader wrote back are re-resolved here against the Files API. Writing the
shopify:// string into the metafield is accepted and renders nothing.

Author: Claude Code, 2026-08-29.
"""
import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLAN = ROOT / "configs" / "product-reviews.json"
API = "2025-01"
MO_TYPE = "customer_review"


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


def gql(store, tok, query, variables=None):
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    req = urllib.request.Request(
        f"https://{store}/admin/api/{API}/graphql.json", data=json.dumps(payload).encode(),
        headers={"X-Shopify-Access-Token": tok, "Content-Type": "application/json"})
    for _ in range(6):
        try:
            out = json.loads(urllib.request.urlopen(req, timeout=90).read())
            break
        except urllib.error.HTTPError as ex:
            if ex.code == 429:
                time.sleep(3)
                continue
            sys.exit(f"HTTP {ex.code}\n{ex.read().decode()[:3000]}")
    else:
        sys.exit("gave up after rate limiting")
    if "errors" in out:
        sys.exit("GraphQL errors:\n" + json.dumps(out["errors"], indent=2)[:2000])
    time.sleep(0.25)
    return out["data"]


def entry_handle(card):
    slug = re.sub(r"[^a-z0-9]+", "-", f"{card['concern']}-{card['person']}".lower()).strip("-")
    return f"review-{slug}"


def resolve_files(store, tok, filenames):
    """filename -> MediaImage GID, looked up in batches.

    Matched on the exact filename rather than on `first: N` ordering: Shopify's file search is
    a fuzzy match, so a query for `...-wrinkles-fiona-c.jpg` also returns the Brightening
    Fiona. Taking the first hit would attach one woman's photograph to another product.
    """
    found = {}
    q = """
    query ($q: String!) {
      files(first: 25, query: $q) {
        nodes { ... on MediaImage { id image { url } } }
      }
    }"""
    for name in filenames:
        stem = name.rsplit(".", 1)[0]
        d = gql(store, tok, q, {"q": f"filename:{stem}"})
        for n in d["files"]["nodes"]:
            url = ((n.get("image") or {}).get("url") or "")
            base = url.split("?")[0].rsplit("/", 1)[-1]
            if base == name:
                found[name] = n["id"]
                break
    return found


UPSERT = """
mutation ($handle: MetaobjectHandleInput!, $metaobject: MetaobjectUpsertInput!) {
  metaobjectUpsert(handle: $handle, metaobject: $metaobject) {
    metaobject { id handle }
    userErrors { field message code }
  }
}"""

SET_MF = """
mutation ($metafields: [MetafieldsSetInput!]!) {
  metafieldsSet(metafields: $metafields) {
    metafields { id key }
    userErrors { field message code }
  }
}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--clear", action="store_true",
                    help="empty every product's list; entries are left alone")
    args = ap.parse_args()

    plan = json.loads(PLAN.read_text())
    cards = plan["cards"]
    e = env()
    store = e["SHOPIFY_SKINGENETIX_STORE"]
    tok = token(e)

    # product handle -> GID
    d = gql(store, tok, "{ products(first:50){nodes{id handle}} }")
    products = {n["handle"]: n["id"] for n in d["products"]["nodes"]}
    missing = sorted({c["product"] for c in cards} - set(products))
    if missing:
        sys.exit(f"unknown product handles: {missing}")

    if args.clear:
        mfs = [{"ownerId": products[h], "namespace": "custom", "key": "customer_reviews",
                "type": "list.metaobject_reference", "value": json.dumps([])}
               for h in sorted({c["product"] for c in cards})]
        if args.dry_run:
            print(f"would clear {len(mfs)} products")
            return
        res = gql(store, tok, SET_MF, {"metafields": mfs})["metafieldsSet"]
        if res["userErrors"]:
            sys.exit(json.dumps(res["userErrors"], indent=2))
        print(f"cleared {len(mfs)} products")
        return

    print(f"resolving {len(cards)} uploaded files to GIDs...")
    gids = resolve_files(store, tok, [c["filename"] for c in cards])
    absent = [c["filename"] for c in cards if c["filename"] not in gids]
    if absent:
        sys.exit(f"{len(absent)} uploaded files not found in Files, first few: {absent[:3]}")
    print(f"  resolved {len(gids)}/{len(cards)}")

    if args.dry_run:
        by_product = {}
        for c in cards:
            by_product.setdefault(c["product"], []).append(entry_handle(c))
        for h, hs in by_product.items():
            print(f"  {h:<62} {len(hs)} entries  e.g. {hs[0]}")
        print(f"\nwould upsert {len(cards)} entries and set {len(by_product)} metafields")
        return

    created = {}
    for i, c in enumerate(cards, 1):
        h = entry_handle(c)
        fields = [
            {"key": "image", "value": gids[c["filename"]]},
            {"key": "author", "value": c["author"]},
            {"key": "rating", "value": str(c["rating"])},
            {"key": "title", "value": c["title"]},
            {"key": "body", "value": c["body"]},
            {"key": "before_label", "value": c["before_label"]},
            {"key": "after_label", "value": c["after_label"]},
            {"key": "verified", "value": "true" if c["verified"] else "false"},
            {"key": "concern", "value": c["concern"]},
        ]
        res = gql(store, tok, UPSERT, {
            "handle": {"type": MO_TYPE, "handle": h},
            "metaobject": {"fields": fields, "capabilities": {}},
        })["metaobjectUpsert"]
        if res["userErrors"]:
            sys.exit(f"{h}: " + json.dumps(res["userErrors"], indent=2))
        created[h] = res["metaobject"]["id"]
        if i % 10 == 0 or i == len(cards):
            print(f"  {i}/{len(cards)} entries")

    by_product = {}
    for c in cards:
        by_product.setdefault(c["product"], []).append(created[entry_handle(c)])

    mfs = [{"ownerId": products[h], "namespace": "custom", "key": "customer_reviews",
            "type": "list.metaobject_reference", "value": json.dumps(ids)}
           for h, ids in by_product.items()]
    # metafieldsSet takes at most 25 per call.
    for i in range(0, len(mfs), 25):
        res = gql(store, tok, SET_MF, {"metafields": mfs[i:i + 25]})["metafieldsSet"]
        if res["userErrors"]:
            sys.exit(json.dumps(res["userErrors"], indent=2))
    for h, ids in by_product.items():
        print(f"  {h:<62} {len(ids)} reviews")
    print(f"\n{len(created)} entries, {len(by_product)} products wired")


if __name__ == "__main__":
    main()
