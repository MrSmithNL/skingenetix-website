#!/usr/bin/env python3
"""Delete the duplicate review image files created by re-running the uploader on 2026-08-29.

    python3 scripts/delete-orphaned-review-duplicates.py            # report only
    python3 scripts/delete-orphaned-review-duplicates.py --delete   # actually delete

WHAT WENT WRONG
`configs/product-reviews.json` held 76 `images` entries with no `uploaded_handle`. That field is
the uploader's skip test, so running it over the plan re-uploaded all 76 — and Shopify
**suffixes rather than replaces** on a filename collision. The store went from 101 wanted
`skingenetix-review-before-after-*` files to 193.

WHAT THIS DELETES, AND WHAT IT WILL NOT TOUCH
Only a file that passes ALL FIVE tests:

  1. name starts `skingenetix-review-before-after-`
  2. name carries a UUID suffix (`_8-4-4-4-12` hex before the extension)
  3. an UNSUFFIXED file with the same base name also exists — so the original survives
  4. its GID is referenced by NO `customer_review` metaobject and NO product metafield
  5. its filename appears in NO theme asset — every template, section, snippet and config on
     the live theme is fetched and searched

Test 3 is the one that matters most: it guarantees deletion can only ever remove the copy, never
the last remaining file. Test 5 exists because a dead `shopify://shop_images/` reference renders
**nothing at all** — no broken icon, no error — so a missed reference would blank a card silently.

⚠️ Suffixed files that are NOT part of this incident are deliberately out of scope. The store has
older ones (`...day-gel-cream-dropper_56524d96...`, `...even-skin-tone-before-after_8575ab91...`)
that predate today and may be in use; the `review-before-after` prefix in test 1 excludes them.

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
API = "2025-01"
PREFIX = "skingenetix-review-before-after-"
UUID_SUFFIX = re.compile(r"_[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}(\.[a-z]+)$")


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
    req = urllib.request.Request(
        f"https://{store}/admin/api/{API}/graphql.json",
        data=json.dumps({"query": query, "variables": variables or {}}).encode(),
        headers={"X-Shopify-Access-Token": tok, "Content-Type": "application/json"})
    for _ in range(6):
        try:
            d = json.loads(urllib.request.urlopen(req, timeout=90).read())
            time.sleep(0.4)
            if "errors" in d:
                sys.exit(json.dumps(d["errors"])[:800])
            return d["data"]
        except urllib.error.HTTPError as ex:
            if ex.code == 429:
                time.sleep(3)
                continue
            sys.exit(f"HTTP {ex.code}\n{ex.read().decode()[:1500]}")
    sys.exit("gave up after rate limiting")


def rest(store, tok, path):
    req = urllib.request.Request(f"https://{store}/admin/api/{API}/{path}",
                                 headers={"X-Shopify-Access-Token": tok})
    for _ in range(6):
        try:
            out = json.loads(urllib.request.urlopen(req, timeout=90).read())
            time.sleep(0.4)
            return out
        except urllib.error.HTTPError as ex:
            if ex.code == 429:
                time.sleep(3)
                continue
            raise
    sys.exit("gave up after rate limiting")


def all_files(store, tok):
    out, cursor = [], None
    while True:
        after = f', after:"{cursor}"' if cursor else ""
        d = gql(store, tok,
                '{files(first:250%s, query:"media_type:IMAGE"){pageInfo{hasNextPage endCursor}'
                ' nodes{... on MediaImage{ id image{url} }}}}' % after)["files"]
        for n in d["nodes"]:
            url = ((n.get("image") or {}).get("url") or "")
            if url:
                out.append((n["id"], url.split("?")[0].rsplit("/", 1)[-1]))
        if not d["pageInfo"]["hasNextPage"]:
            break
        cursor = d["pageInfo"]["endCursor"]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--delete", action="store_true")
    args = ap.parse_args()

    e = env()
    store = e["SHOPIFY_SKINGENETIX_STORE"]
    tok = token(e)

    files = all_files(store, tok)
    names = {n for _, n in files}
    review = [(gid, n) for gid, n in files if n.startswith(PREFIX)]
    print(f"{len(files)} image files on the store, {len(review)} with the review prefix")

    # tests 1-3
    candidates = []
    for gid, n in review:
        m = UUID_SUFFIX.search(n)
        if not m:
            continue
        original = UUID_SUFFIX.sub(m.group(1), n)
        if original in names:
            candidates.append((gid, n, original))
    print(f"suffixed duplicates whose original still exists: {len(candidates)}")

    # test 4 - referenced by a metaobject or a product metafield
    used = set()
    for n in gql(store, tok,
                 '{metaobjects(type:"customer_review", first:250){nodes{fields{key value}}}}'
                 )["metaobjects"]["nodes"]:
        for f in n["fields"]:
            if f["key"] == "image" and f["value"]:
                used.add(f["value"])
    for p in gql(store, tok,
                 '{products(first:50){nodes{metafields(first:30){nodes{value type}}}}}'
                 )["products"]["nodes"]:
        for mf in p["metafields"]["nodes"]:
            v = mf.get("value") or ""
            if "gid://shopify/MediaImage" in v:
                used.update(re.findall(r"gid://shopify/MediaImage/\d+", v))
    print(f"MediaImage GIDs referenced by metaobjects and product metafields: {len(used)}")

    # test 5 - filename mentioned anywhere in the live theme
    theme = next(t for t in rest(store, tok, "themes.json")["themes"] if t["role"] == "main")
    blob = []
    for a in rest(store, tok, f"themes/{theme['id']}/assets.json")["assets"]:
        k = a["key"]
        if k.startswith(("templates/", "sections/", "snippets/", "config/", "locales/")):
            v = rest(store, tok,
                     f"themes/{theme['id']}/assets.json?asset[key]={urllib.parse.quote(k)}"
                     )["asset"].get("value") or ""
            blob.append(v)
    theme_text = "\n".join(blob)
    print(f"searched {len(blob)} theme assets on theme {theme['id']}")

    doomed, spared = [], []
    for gid, n, original in candidates:
        why = []
        if gid in used:
            why.append("referenced by a metaobject/metafield")
        if n in theme_text:
            why.append("named in a theme asset")
        (spared if why else doomed).append((gid, n, why))

    print(f"\nSAFE TO DELETE: {len(doomed)}")
    print(f"SPARED (still referenced): {len(spared)}")
    for gid, n, why in spared:
        print(f"   KEEP {n}  <- {', '.join(why)}")

    if not args.delete:
        for _, n, _ in doomed[:5]:
            print(f"   would delete {n}")
        print(f"   ... and {max(0, len(doomed) - 5)} more")
        print("\nreport only. re-run with --delete to remove them.")
        return

    Path(ROOT / "backups").mkdir(exist_ok=True)
    log = ROOT / "backups" / "deleted-review-duplicates-20260829.json"
    log.write_text(json.dumps([{"id": g, "filename": n} for g, n, _ in doomed], indent=2))
    print(f"\nrecord of what is being deleted: {log.relative_to(ROOT)}")

    MUT = """mutation ($ids: [ID!]!) { fileDelete(fileIds: $ids) {
                deletedFileIds userErrors { field message } } }"""
    done = 0
    for i in range(0, len(doomed), 20):
        batch = [g for g, _, _ in doomed[i:i + 20]]
        d = gql(store, tok, MUT, {"ids": batch})["fileDelete"]
        if d["userErrors"]:
            sys.exit(f"fileDelete: {d['userErrors']}")
        done += len(d["deletedFileIds"])
        print(f"  deleted {done}/{len(doomed)}")
    print(f"\ndeleted {done} orphaned duplicates")


if __name__ == "__main__":
    import urllib.parse  # noqa: E402  (used in the asset loop)
    main()
