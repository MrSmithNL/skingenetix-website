#!/usr/bin/env python3
"""Add one customer_review card to one product's carousel, at a chosen position.

    python3 scripts/add-review-card.py --plan configs/banners/<plan>.json --dry-run
    python3 scripts/add-review-card.py --plan configs/banners/<plan>.json
    python3 scripts/add-review-card.py --restore backups/review-order-<stamp>.json

WHY NOT product-reviews-publish.py
That script is the bulk publisher: it upserts all 99 cards from `configs/product-reviews.json`
and rewrites every product's list in allocation order. Running it to add a single card would
overwrite anything changed since that config was written. As of 2026-08-31 that config still
names Jennifer T, Lucia M and Martine M, whose entries now display Casandra C, Trudie T and
Stephanie G, and it knows nothing about the manual Bri E / Stephanie G position swap — so a
bulk publish today would silently undo a day's work. This script touches one metaobject and
one product's list, and nothing else.

UPSERT BY HANDLE, NEVER DELETE-AND-RECREATE. The handle is the identity: translations key off
it, so recreating an entry drops every locale. That mistake cost the sister brand its German
mega-menu (production-safety incident log, 2026-03-14). Re-running this plan updates the same
entry in place.

The backup captures the product's previous list, so --restore removes the card again by
putting the old order back. It does not delete the metaobject; a card that is not referenced
by any product does not render.

Author: Claude Code, 2026-08-31.
"""
import argparse
import json
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "2025-01"
BACKUPS = ROOT / "backups"

FETCH = """
query($handle:String!){
  productByHandle(handle:$handle){
    id
    metafield(namespace:"custom", key:"customer_reviews"){
      value
      references(first:50){ nodes{ ... on Metaobject { id handle fields{ key value } } } }
    }
  }
}"""

FILE_ID = """
query($q:String!){ files(first:10, query:$q){ nodes{ ... on MediaImage { id image{ url } } } } }"""

UPSERT = """
mutation($handle:MetaobjectHandleInput!, $metaobject:MetaobjectUpsertInput!){
  metaobjectUpsert(handle:$handle, metaobject:$metaobject){
    metaobject{ id handle }
    userErrors{ field message code }
  }
}"""

WRITE = """
mutation($metafields:[MetafieldsSetInput!]!){
  metafieldsSet(metafields:$metafields){
    metafields{ id }
    userErrors{ field message code }
  }
}"""


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
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(f"https://{store}/admin/api/{API}/graphql.json",
                                 data=body, method="POST",
                                 headers={"X-Shopify-Access-Token": tok,
                                          "Content-Type": "application/json"})
    out = json.loads(urllib.request.urlopen(req, timeout=90).read())
    if out.get("errors"):
        sys.exit(f"GraphQL: {out['errors']}")
    return out["data"]


def file_gid(store, tok, filename):
    stem = filename.rsplit(".", 1)[0]
    nodes = gql(store, tok, FILE_ID, {"q": f"filename:{stem}*"})["files"]["nodes"]
    for n in nodes:
        if n["image"]["url"].split("/")[-1].split("?")[0] == filename:
            return n["id"]
    sys.exit(f"no uploaded file named {filename} — run upload-theme-images.py first")


def push_order(store, tok, owner_id, gids):
    data = gql(store, tok, WRITE, {"metafields": [{
        "ownerId": owner_id, "namespace": "custom", "key": "customer_reviews",
        "type": "list.metaobject_reference", "value": json.dumps(gids)}]})
    errs = data["metafieldsSet"]["userErrors"]
    if errs:
        sys.exit(f"metafieldsSet: {errs}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan")
    ap.add_argument("--restore")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    e = env()
    store = e["SHOPIFY_SKINGENETIX_STORE"]
    tok = token(e)
    print(f"Store : {store}\n")

    if args.restore:
        saved = json.loads((ROOT / args.restore).read_text())
        push_order(store, tok, saved["product_id"], saved["order"])
        print(f"RESTORED {saved['product']} to {len(saved['order'])} cards")
        return

    plan = json.loads((ROOT / args.plan).read_text())
    card = plan["card"]
    product_handle = plan["product"]
    position = plan.get("position", 0)

    p = gql(store, tok, FETCH, {"handle": product_handle})["productByHandle"]
    if not p:
        sys.exit(f"no product with handle {product_handle}")
    mf = p.get("metafield")
    order = [n["id"] for n in mf["references"]["nodes"]] if mf else []
    handles = [n["handle"] for n in mf["references"]["nodes"]] if mf else []

    BACKUPS.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = BACKUPS / f"review-order-{stamp}.json"
    backup.write_text(json.dumps(
        {"product": product_handle, "product_id": p["id"], "order": order,
         "handles": handles}, indent=2))
    print(f"Backup    : {backup.relative_to(ROOT)}")
    print(f"Undo with : python3 scripts/add-review-card.py --restore "
          f"{backup.relative_to(ROOT)}\n")

    gid_img = file_gid(store, tok, card["image_filename"])
    fields = [
        {"key": "image", "value": gid_img},
        {"key": "author", "value": card["author"]},
        {"key": "rating", "value": str(card.get("rating", 5))},
        {"key": "title", "value": card["title"]},
        {"key": "body", "value": card["body"]},
        {"key": "before_label", "value": card.get("before_label", "Before")},
        {"key": "after_label", "value": card.get("after_label", "After")},
        {"key": "verified", "value": "true" if card.get("verified", True) else "false"},
        {"key": "concern", "value": card["concern"]},
    ]

    print(f"{card['handle']}   ({'already present' if card['handle'] in handles else 'NEW'})")
    print(f"   author  {card['author']}")
    print(f"   title   {card['title']}")
    print(f"   body    {card['body'][:70]}...")
    print(f"   image   {card['image_filename']}")
    print(f"   concern {card['concern']}\n")
    print(f"{product_handle}: inserting at position {position}")
    preview = handles[:]
    if card["handle"] in preview:
        preview.remove(card["handle"])
    preview.insert(position, card["handle"] + "   <-- new")
    for i, h in enumerate(preview):
        print(f"  {i}  {h}")

    if args.dry_run:
        print("\nDRY RUN — nothing pushed")
        return

    data = gql(store, tok, UPSERT, {
        "handle": {"type": "customer_review", "handle": card["handle"]},
        "metaobject": {"fields": fields}})
    errs = data["metaobjectUpsert"]["userErrors"]
    if errs:
        sys.exit(f"metaobjectUpsert: {errs}")
    new_gid = data["metaobjectUpsert"]["metaobject"]["id"]
    print(f"\n  upserted {card['handle']} -> {new_gid}")

    if new_gid in order:
        order.remove(new_gid)
    order.insert(position, new_gid)
    push_order(store, tok, p["id"], order)
    print(f"  list now {len(order)} cards\n\nPUSHED")


if __name__ == "__main__":
    main()
