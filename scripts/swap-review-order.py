#!/usr/bin/env python3
"""Transpose two review cards in one product's carousel. Nothing else moves.

    python3 scripts/swap-review-order.py --product glutathione-brightening-serum \
        --a review-brightening-bri-e --b review-brightening-martine-m --dry-run
    python3 scripts/swap-review-order.py --product ... --a ... --b ...
    python3 scripts/swap-review-order.py --restore backups/review-order-<stamp>.json

WHY THIS EXISTS ALONGSIDE product-reviews-reorder.py
That script lays out a whole carousel algorithmically, costing adjacency so similar-looking
women do not sit next to each other. It is the right tool for "this page looks repetitive"
and the wrong one for "put these two the other way round": re-running it would move every
other card as a side effect of moving the two that were asked for.

This writes the same `custom.customer_reviews` list with exactly two positions exchanged.

⚠️ ASK BY HANDLE, NOT BY NAME. A metaobject handle is fixed at creation and does NOT follow
the author. After the 2026-08-31 swaps, `review-brightening-martine-m` displays "Stephanie G"
and `review-brightening-jennifer-t` displays "Casandra C". The handle is deliberately stable —
translations key off it, so renaming one would orphan every locale. The dry run prints the
displayed author beside each handle so the pairing can be eyeballed before anything is written.

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
      id value
      references(first:50){ nodes{ ... on Metaobject { id handle fields{ key value } } } }
    }
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


def push(store, tok, owner_id, gids):
    data = gql(store, tok, WRITE, {"metafields": [{
        "ownerId": owner_id, "namespace": "custom", "key": "customer_reviews",
        "type": "list.metaobject_reference", "value": json.dumps(gids)}]})
    errs = data["metafieldsSet"]["userErrors"]
    if errs:
        sys.exit(f"metafieldsSet: {errs}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--product")
    ap.add_argument("--a")
    ap.add_argument("--b")
    ap.add_argument("--restore")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    e = env()
    store = e["SHOPIFY_SKINGENETIX_STORE"]
    tok = token(e)
    print(f"Store : {store}\n")

    if args.restore:
        saved = json.loads((ROOT / args.restore).read_text())
        push(store, tok, saved["product_id"], saved["order"])
        print(f"RESTORED {saved['product']} to its previous order "
              f"({len(saved['order'])} cards)")
        return

    if not (args.product and args.a and args.b):
        sys.exit("need --product, --a and --b (or --restore)")

    p = gql(store, tok, FETCH, {"handle": args.product})["productByHandle"]
    if not p:
        sys.exit(f"no product with handle {args.product}")
    mf = p.get("metafield")
    if not mf:
        sys.exit(f"{args.product} has no custom.customer_reviews metafield")

    nodes = mf["references"]["nodes"]
    order = [n["id"] for n in nodes]
    handles = [n["handle"] for n in nodes]
    author = {n["handle"]: next((f["value"] for f in n["fields"] if f["key"] == "author"), "?")
              for n in nodes}

    for h in (args.a, args.b):
        if h not in handles:
            sys.exit(f"{h} is not on {args.product}. Present: {', '.join(handles)}")

    ia, ib = handles.index(args.a), handles.index(args.b)

    BACKUPS.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = BACKUPS / f"review-order-{stamp}.json"
    backup.write_text(json.dumps(
        {"product": args.product, "product_id": p["id"], "order": order,
         "handles": handles}, indent=2))
    print(f"Backup    : {backup.relative_to(ROOT)}")
    print(f"Undo with : python3 scripts/swap-review-order.py --restore "
          f"{backup.relative_to(ROOT)}\n")

    order[ia], order[ib] = order[ib], order[ia]
    new_handles = handles[:]
    new_handles[ia], new_handles[ib] = new_handles[ib], new_handles[ia]

    print(f"{args.product}: position {ia} <-> {ib}\n")
    for i, (was, now) in enumerate(zip(handles, new_handles)):
        mark = "  <--" if was != now else ""
        if was == now:
            print(f"  {i}  {author[now]:<14} {now}")
        else:
            print(f"  {i}  {author[was]:<14} -> {author[now]:<14} {now}{mark}")

    if args.dry_run:
        print("\nDRY RUN — nothing pushed")
        return

    push(store, tok, p["id"], order)
    print("\nPUSHED")


if __name__ == "__main__":
    main()
