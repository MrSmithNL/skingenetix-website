#!/usr/bin/env python3
"""Add an image to a product and set the WHOLE gallery order explicitly.

    python3 scripts/insert-product-image.py <handle> <file> --name <seo.jpg> --alt "<text>" \
        --order "frag1,frag2,NEW,frag3,..." [--apply]

WHY THE ORDER IS SPELLED OUT RATHER THAN INFERRED
Malcolm asked for a new third image while "the current 4th image stays where it is". Those two
constraints cannot both be met by inserting and letting everything else slide - the image being
displaced has to jump PAST the one that is pinned. An --insert-at N flag would have quietly
produced the wrong result and looked right. So the caller names the final order, the literal
token NEW marks the new image's slot, and a dry run prints the result to check before anything
is uploaded.

Order of operations is the same as replace-product-image.py and for the same reasons: add, wait
for READY, then reorder. Never reorder against media Shopify is still processing.

Nothing is deleted here - this only adds. Use replace-product-image.py when an image is retired.

Author: Claude Code, 2026-09-15.
"""
import argparse, importlib.util, json, sys, time, urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "2025-01"
_s = importlib.util.spec_from_file_location("uti", ROOT / "scripts" / "upload-theme-images.py")
uti = importlib.util.module_from_spec(_s); _s.loader.exec_module(uti)


def gql(store, tok, q, v=None):
    body = json.dumps({"query": q, "variables": v or {}}).encode()
    req = urllib.request.Request(f"https://{store}/admin/api/{API}/graphql.json", data=body,
                                 method="POST", headers={"X-Shopify-Access-Token": tok,
                                                         "Content-Type": "application/json"})
    for i in range(5):
        try:
            d = json.loads(urllib.request.urlopen(req, timeout=180).read()); break
        except urllib.error.HTTPError as ex:
            if ex.code not in (429, 502, 503) or i == 4: raise
            time.sleep(4 * (i + 1))
    if "errors" in d: sys.exit(d["errors"])
    return d["data"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("handle"); ap.add_argument("file")
    ap.add_argument("--name", required=True); ap.add_argument("--alt", required=True)
    ap.add_argument("--order", required=True,
                    help="final gallery order as filename fragments, NEW marks the new image")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    e = uti.env(); store = e["SHOPIFY_SKINGENETIX_STORE"]; tok = uti.token(e)
    p = gql(store, tok, '''query($h:String!){ productByHandle(handle:$h){ id title status
          media(first:50){ nodes{ ... on MediaImage { id image{ url } } } } } }''',
            {"h": a.handle})["productByHandle"]
    nodes = p["media"]["nodes"]
    names = [n["image"]["url"].split("/")[-1].split("?")[0] for n in nodes]
    if a.name in names:
        sys.exit(f"{a.name} is already on this product - Shopify suffixes, pick another name")

    wanted = [f.strip() for f in a.order.split(",") if f.strip()]
    # every existing image must be named exactly once, or the reorder would silently drop one
    resolved, used = [], set()
    for frag in wanted:
        if frag == "NEW":
            resolved.append(None); continue
        hits = [i for i, f in enumerate(names) if frag in f and i not in used]
        if len(hits) != 1:
            sys.exit(f"--order fragment {frag!r} matched {len(hits)} images")
        used.add(hits[0]); resolved.append(hits[0])
    missing = [names[i] for i in range(len(names)) if i not in used]
    if missing:
        sys.exit("--order does not account for: " + ", ".join(missing))
    if resolved.count(None) != 1:
        sys.exit("--order must contain exactly one NEW")

    print(f'{p["title"][:60]}\n  status: {p["status"]}'
          f'{"   *** LIVE ***" if p["status"] == "ACTIVE" else ""}')
    print(f'  {len(nodes)} media now -> {len(wanted)} after\n\n  final order:')
    for i, idx in enumerate(resolved, 1):
        print(f'    {i}. {"<-- NEW  " + a.name if idx is None else names[idx]}')
    if not a.apply:
        print("\nDRY RUN - pass --apply")
        return 0

    src = uti.optimise(Path(a.file), ROOT / ".web-optimised" / a.name)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    bk = ROOT / "backups" / f"image-insert-{stamp}.json"
    bk.parent.mkdir(exist_ok=True)
    bk.write_text(json.dumps({"product": p["id"], "handle": a.handle,
                              "order_before": names, "new_name": a.name}, indent=2))
    print(f"\n  backup: {bk.relative_to(ROOT)}")

    t = gql(store, tok, '''mutation($i:[StagedUploadInput!]!){ stagedUploadsCreate(input:$i){
              stagedTargets{ url resourceUrl parameters{ name value } } } }''',
            {"i": [{"filename": a.name, "mimeType": "image/jpeg",
                    "resource": "IMAGE", "httpMethod": "POST"}]})["stagedUploadsCreate"]["stagedTargets"][0]
    uti.post_multipart(t["url"], t["parameters"], src, a.name)
    d = gql(store, tok, '''mutation($id:ID!,$m:[CreateMediaInput!]!){
              productCreateMedia(productId:$id, media:$m){ media{ ... on MediaImage { id } }
              mediaUserErrors{ message } } }''',
            {"id": p["id"], "m": [{"originalSource": t["resourceUrl"],
                                   "mediaContentType": "IMAGE", "alt": a.alt}]})
    if d["productCreateMedia"]["mediaUserErrors"]: sys.exit(d["productCreateMedia"]["mediaUserErrors"])
    new_id = d["productCreateMedia"]["media"][0]["id"]
    print(f"  added : {new_id.split('/')[-1]}")

    for _ in range(60):
        st = gql(store, tok, 'query($id:ID!){ node(id:$id){ ... on MediaImage { status } } }',
                 {"id": new_id})["node"]["status"]
        if st == "READY": break
        time.sleep(5)
    print(f"  status: {st}")
    if st != "READY": sys.exit("never reached READY - order left untouched")

    order = [new_id if idx is None else nodes[idx]["id"] for idx in resolved]
    gql(store, tok, '''mutation($id:ID!,$m:[MoveInput!]!){ productReorderMedia(id:$id, moves:$m){
          job{ id } userErrors{ message } } }''',
        {"id": p["id"], "m": [{"id": m, "newPosition": str(i)} for i, m in enumerate(order)]})
    time.sleep(6)
    chk = gql(store, tok, '''query($h:String!){ productByHandle(handle:$h){ media(first:50){
              nodes{ ... on MediaImage { image{ url } } } } } }''',
              {"h": a.handle})["productByHandle"]["media"]["nodes"]
    print("\n  gallery now:")
    for i, n in enumerate(chk, 1):
        f = n["image"]["url"].split("/")[-1].split("?")[0]
        print(f'    {i}. {"<-- new" if f == a.name else "       "} {f}')
    return 0


if __name__ == "__main__":
    sys.exit(main())
