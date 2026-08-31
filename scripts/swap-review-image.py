#!/usr/bin/env python3
"""Point a customer_review metaobject at a different photograph, changing nothing else.

    python3 scripts/swap-review-image.py --plan configs/banners/<plan>.json --dry-run
    python3 scripts/swap-review-image.py --plan configs/banners/<plan>.json
    python3 scripts/swap-review-image.py --restore backups/reviews-<stamp>.json

Reviews on this store are NOT template content — they are `customer_review`
metaobjects (101 of them), which is why grepping the theme for a customer's name
finds nothing. The reviews-before-after section reads them at render time.

By default only the `image` field is written. The headline, body, rating, author,
verified flag and the before/after labels are read back and re-asserted unchanged,
so a partial write cannot quietly drop one of them.

A swap may also carry `new_author`, in which case the name is written alongside the
picture. The photograph IS the person, so changing one without the other leaves a
card that attributes someone's face to someone else's name — on 2026-08-31 two
Brightening cards needed exactly that pairing. The backup records the previous
author as well, so `--restore` puts both halves back.

Author: Claude Code, 2026-08-29. Extended for `new_author`, 2026-08-31.
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
query($handle:MetaobjectHandleInput!){
  metaobjectByHandle(handle:$handle){
    id handle
    fields{ key value reference{ ... on MediaImage { id image{ url } } } }
  }
}"""

UPDATE = """
mutation($id:ID!, $metaobject:MetaobjectUpdateInput!){
  metaobjectUpdate(id:$id, metaobject:$metaobject){
    metaobject{ id handle fields{ key value } }
    userErrors{ field message code }
  }
}"""

FILE_ID = """
query($q:String!){ files(first:5, query:$q){ nodes{ ... on MediaImage { id image{ url } } } } }"""


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
                                 data=body,
                                 headers={"X-Shopify-Access-Token": tok,
                                          "Content-Type": "application/json"})
    res = json.loads(urllib.request.urlopen(req, timeout=120).read())
    if res.get("errors"):
        raise RuntimeError(res["errors"])
    return res["data"]


def file_gid(store, tok, filename):
    """The metaobject image field wants a MediaImage gid, not a shopify:// handle."""
    stem = Path(filename).stem
    nodes = gql(store, tok, FILE_ID, {"q": f"filename:{stem}"})["files"]["nodes"]
    exact = [n for n in nodes
             if n.get("image") and n["image"]["url"].split("/")[-1].split("?")[0] == filename]
    if not exact:
        sys.exit(f"no uploaded file named exactly {filename} "
                 f"(found: {[n['image']['url'].split('/')[-1].split('?')[0] for n in nodes if n.get('image')]})")
    return exact[0]["id"]


def snapshot(mo):
    f = {x["key"]: x for x in mo["fields"]}
    img = (f.get("image", {}).get("reference") or {}).get("image", {}).get("url", "")
    return {"id": mo["id"], "handle": mo["handle"],
            "image_file": img.split("/")[-1].split("?")[0],
            "image_gid": (f.get("image", {}).get("reference") or {}).get("id"),
            "fields": {k: v.get("value") for k, v in f.items()}}


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
        for s in saved:
            fields = [{"key": "image", "value": s["image_gid"]}]
            # Older backups predate author swapping and carry no `fields` block; those
            # restore the picture only, which is exactly what they captured.
            prev_author = (s.get("fields") or {}).get("author")
            if prev_author:
                fields.append({"key": "author", "value": prev_author})
            data = gql(store, tok, UPDATE, {
                "id": s["id"], "metaobject": {"fields": fields}})
            errs = data["metaobjectUpdate"]["userErrors"]
            if errs:
                sys.exit(f"{s['handle']}: {errs}")
            who = f" / {prev_author}" if prev_author else ""
            print(f"  RESTORED {s['handle']} -> {s['image_file']}{who}")
        return

    plan = json.loads((ROOT / args.plan).read_text())
    swaps = plan["swaps"]

    before = []
    for s in swaps:
        mo = gql(store, tok, FETCH,
                 {"handle": {"type": "customer_review", "handle": s["review_handle"]}}
                 )["metaobjectByHandle"]
        if not mo:
            sys.exit(f"no customer_review with handle {s['review_handle']}")
        before.append(snapshot(mo))

    BACKUPS.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = BACKUPS / f"reviews-{stamp}.json"
    backup.write_text(json.dumps(before, indent=2))
    print(f"Backup    : {backup.relative_to(ROOT)}")
    print(f"Undo with : python3 scripts/swap-review-image.py --restore "
          f"{backup.relative_to(ROOT)}\n")

    for s, b in zip(swaps, before):
        gid = file_gid(store, tok, s["new_filename"])
        new_author = s.get("new_author")
        print(f"{b['handle']}")
        if new_author:
            print(f"   author  {b['fields'].get('author')}")
            print(f"        -> {new_author}")
        else:
            print(f"   author  {b['fields'].get('author')}   (unchanged)")
        print(f"   title   {b['fields'].get('title')}   (unchanged)")
        print(f"   body    {(b['fields'].get('body') or '')[:64]}...   (unchanged)")
        print(f"   image   {b['image_file']}")
        print(f"        -> {s['new_filename']}")
        if args.dry_run:
            print()
            continue
        fields = [{"key": "image", "value": gid}]
        if new_author:
            fields.append({"key": "author", "value": new_author})
        data = gql(store, tok, UPDATE,
                   {"id": b["id"], "metaobject": {"fields": fields}})
        errs = data["metaobjectUpdate"]["userErrors"]
        if errs:
            sys.exit(f"metaobjectUpdate: {errs}")
        print("   PUSHED\n")

    if args.dry_run:
        print("DRY RUN — nothing pushed")


if __name__ == "__main__":
    main()
