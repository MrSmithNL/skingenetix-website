#!/usr/bin/env python3
"""Swap ONE image on a product for a new file, keeping its position in the gallery.

    python3 scripts/replace-product-image.py <handle> <old-filename-fragment> <new-file> \
        --name <seo-name.jpg> --alt "<alt text>" [--apply]

WHY NOT shopify-merge-media.py: that one is plan-driven and decides, per live image, whether it
is retired - right for swapping several at once. This is the single-image case: Malcolm names one
live photograph and one replacement, and the new image must land in the SAME slot so the gallery
order he chose is preserved.

ORDER OF OPERATIONS, and it is not interchangeable: add, wait for READY, delete the old, then
reorder. Deleting first would leave a live product page with a hole in it if the upload failed
halfway. Reordering before READY sets positions against a list Shopify is still changing.

UPLOAD ONCE. Shopify SUFFIXES rather than replaces on a filename collision and then keeps serving
the OLD file, which has bitten this project three times - so the new image must not reuse the
retired name, and this refuses if the name is already on the store.

Optimisation is upload-theme-images.optimise, not a second implementation.

Author: Claude Code, 2026-09-15.
"""
import argparse
import importlib.util
import json
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "2025-01"
_spec = importlib.util.spec_from_file_location("uti", ROOT / "scripts" / "upload-theme-images.py")
uti = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(uti)


def gql(store, tok, q, v=None):
    body = json.dumps({"query": q, "variables": v or {}}).encode()
    req = urllib.request.Request(f"https://{store}/admin/api/{API}/graphql.json", data=body,
                                 method="POST",
                                 headers={"X-Shopify-Access-Token": tok,
                                          "Content-Type": "application/json"})
    for attempt in range(5):
        try:
            d = json.loads(urllib.request.urlopen(req, timeout=180).read())
            break
        except urllib.error.HTTPError as ex:
            if ex.code not in (429, 502, 503) or attempt == 4:
                raise
            time.sleep(4 * (attempt + 1))
    if "errors" in d:
        sys.exit(d["errors"])
    return d["data"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("handle"); ap.add_argument("old_fragment"); ap.add_argument("new_file")
    ap.add_argument("--name", required=True); ap.add_argument("--alt", required=True)
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    e = uti.env(); store = e["SHOPIFY_SKINGENETIX_STORE"]; tok = uti.token(e)
    p = gql(store, tok, '''query($h:String!){ productByHandle(handle:$h){ id title status
          media(first:50){ nodes{ ... on MediaImage { id alt image{ url } } } } } }''',
            {"h": a.handle})["productByHandle"]
    nodes = p["media"]["nodes"]
    names = [n["image"]["url"].split("/")[-1].split("?")[0] for n in nodes]
    hits = [i for i, f in enumerate(names) if a.old_fragment in f]
    if len(hits) != 1:
        sys.exit(f"{'no' if not hits else 'ambiguous'} match for {a.old_fragment!r}: "
                 + ", ".join(names[i] for i in hits))
    idx = hits[0]
    if a.name in names:
        sys.exit(f"{a.name} is already on this product - pick a different name, Shopify suffixes")

    print(f'{p["title"][:60]}\n  status   : {p["status"]}'
          f'{"   *** LIVE ***" if p["status"] == "ACTIVE" else ""}')
    print(f'  replacing: {names[idx]}  (position {idx + 1} of {len(nodes)})')
    print(f'  with     : {a.name}\n  alt      : {a.alt}')
    if not a.apply:
        print("\nDRY RUN - pass --apply")
        return 0

    work = ROOT / ".web-optimised" / a.name
    src = uti.optimise(Path(a.new_file), work)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = ROOT / "backups" / f"image-replace-{stamp}.json"
    backup.parent.mkdir(exist_ok=True)
    backup.write_text(json.dumps({"product": p["id"], "handle": a.handle,
                                  "retired_media": nodes[idx]["id"],
                                  "retired_name": names[idx], "retired_alt": nodes[idx]["alt"],
                                  "position": idx, "new_name": a.name}, indent=2))
    print(f"\n  backup   : {backup.relative_to(ROOT)}")

    # 1. ADD
    res = gql(store, tok, '''mutation($i:[StagedUploadInput!]!){ stagedUploadsCreate(input:$i){
              stagedTargets{ url resourceUrl parameters{ name value } } userErrors{ message } } }''',
              {"i": [{"filename": a.name, "mimeType": "image/jpeg",
                      "resource": "IMAGE", "httpMethod": "POST"}]})["stagedUploadsCreate"]
    t = res["stagedTargets"][0]
    # parameters is a LIST of {name, value}, not a dict - post_multipart iterates it
    uti.post_multipart(t["url"], t["parameters"], src, a.name)
    d = gql(store, tok, '''mutation($id:ID!,$m:[CreateMediaInput!]!){
              productCreateMedia(productId:$id, media:$m){
                media{ ... on MediaImage { id } } mediaUserErrors{ message } } }''',
            {"id": p["id"], "m": [{"originalSource": t["resourceUrl"],
                                   "mediaContentType": "IMAGE", "alt": a.alt}]})
    if d["productCreateMedia"]["mediaUserErrors"]:
        sys.exit(d["productCreateMedia"]["mediaUserErrors"])
    new_id = d["productCreateMedia"]["media"][0]["id"]
    print(f"  added    : {new_id.split('/')[-1]}")

    # 2. WAIT FOR READY - never reorder against media Shopify is still processing
    for _ in range(60):
        st = gql(store, tok, '''query($id:ID!){ node(id:$id){ ... on MediaImage { status } } }''',
                 {"id": new_id})["node"]["status"]
        if st == "READY":
            break
        time.sleep(5)
    print(f"  status   : {st}")
    if st != "READY":
        sys.exit("new media never reached READY - old image left in place deliberately")

    # 3. DELETE THE OLD
    gql(store, tok, '''mutation($id:ID!,$m:[ID!]!){ productDeleteMedia(productId:$id, mediaIds:$m){
          deletedMediaIds mediaUserErrors{ message } } }''',
        {"id": p["id"], "m": [nodes[idx]["id"]]})
    print(f"  deleted  : {names[idx]}")

    # 4. REORDER into the retired image's slot
    order = [n["id"] for i, n in enumerate(nodes) if i != idx]
    order.insert(idx, new_id)
    gql(store, tok, '''mutation($id:ID!,$m:[MoveInput!]!){ productReorderMedia(id:$id, moves:$m){
          job{ id } userErrors{ message } } }''',
        {"id": p["id"], "m": [{"id": mid, "newPosition": str(i)} for i, mid in enumerate(order)]})
    time.sleep(6)

    chk = gql(store, tok, '''query($h:String!){ productByHandle(handle:$h){
              media(first:50){ nodes{ ... on MediaImage { image{ url } } } } } }''',
              {"h": a.handle})["productByHandle"]["media"]["nodes"]
    print("\n  gallery now:")
    for i, n in enumerate(chk, 1):
        f = n["image"]["url"].split("/")[-1].split("?")[0]
        print(f'    {i}. {"<-- new" if f == a.name else "       "} {f}')
    return 0


if __name__ == "__main__":
    sys.exit(main())
