#!/usr/bin/env python3
"""Repoint one review card at an updated photograph from Drive.

    python3 scripts/product-reviews-refresh-image.py --person Arantxa-R --dry-run
    python3 scripts/product-reviews-refresh-image.py --person Arantxa-R

Malcolm edits a photograph in Drive and wants the live card to use it. Three steps: upload the
new file, repoint the `customer_review` entry's `image` field at it, and record the new
filename in the builder so a rebuild does not undo the change.

⚠️ WHY IT UPLOADS UNDER A DIFFERENT FILENAME, WHICH LOOKS WRONG BUT ISN'T
Shopify Files **suffixes on a name collision rather than replacing**. Re-uploading
`...-arantxa-r.jpg` produces a second file and the ORIGINAL keeps being served everywhere it
is referenced — the update appears to have silently failed. This project has been bitten by it
three times (memory: shopify-file-uploads-are-suffixed-not-replaced). The alternative, deleting
the old file first, is a hard boundary: deleting data from an external service needs Malcolm's
explicit go-ahead, so it is NOT done here. The old file is left in place, orphaned, and named
in the output so he can decide.

The replacement name must still earn its place in a search result, so it is not a `-v2` or a
date stamp — those describe the revision, not the subject, and the uploader's own SEO check
flags them. `NEW_NAMES` below carries a hand-picked alternative built from real keywords.

Author: Claude Code, 2026-08-29.
"""
import argparse
import json
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLAN = ROOT / "configs" / "product-reviews.json"
API = "2025-01"

#: person -> the SEO filename to use for the REPLACEMENT upload. Built from real keywords
#: ("brightening-glow" is the collection this product sits in), never a version marker.
#: Mirrored into IMAGE_RENAMES in product-reviews-build-plan.py so a rebuild keeps it.
NEW_NAMES = {
    "Arantxa-R": "skingenetix-review-before-after-brightening-glow-arantxa-r.jpg",
    "Petra-J": "skingenetix-review-before-after-fine-lines-petra-j.jpg",
    "Janine-L": "skingenetix-review-before-after-fine-lines-janine-l.jpg",
    "Shannon-P": "skingenetix-review-before-after-skin-repair-shannon-p.jpg",
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


def gql(store, tok, query, variables=None):
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    req = urllib.request.Request(
        f"https://{store}/admin/api/{API}/graphql.json", data=json.dumps(payload).encode(),
        headers={"X-Shopify-Access-Token": tok, "Content-Type": "application/json"})
    try:
        out = json.loads(urllib.request.urlopen(req, timeout=90).read())
    except urllib.error.HTTPError as ex:
        sys.exit(f"HTTP {ex.code}\n{ex.read().decode()[:2500]}")
    if "errors" in out:
        sys.exit("GraphQL errors:\n" + json.dumps(out["errors"], indent=2)[:2000])
    return out["data"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--person", required=True, help="e.g. Arantxa-R")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    plan = json.loads(PLAN.read_text())
    card = next((c for c in plan["cards"] if c["person"] == args.person), None)
    if card is None:
        sys.exit(f"no card for {args.person}")
    src = next((i for i in plan["images"] if i["filename"] == card["filename"]), None)
    if src is None:
        sys.exit(f"no image entry for {card['filename']}")

    new_name = NEW_NAMES.get(args.person)
    if not new_name:
        sys.exit(f"add an SEO filename for {args.person} to NEW_NAMES first "
                 f"(current: {card['filename']})")

    source = Path(src["source"])
    if not source.exists():
        sys.exit(f"missing Drive source: {source}")

    e = env()
    store = e["SHOPIFY_SKINGENETIX_STORE"]
    tok = token(e)

    handle = f"review-{card['concern'].lower()}-{args.person.lower().replace('-', '-')}"
    print(f"person   : {args.person}")
    print(f"product  : {card['product']}")
    print(f"entry    : {handle}")
    print(f"old file : {card['filename']}   (left in place, orphaned)")
    print(f"new file : {new_name}")
    print(f"source   : {source.name}  {source.stat().st_size:,} bytes")

    if args.dry_run:
        print("\n--dry-run, nothing uploaded or changed")
        return

    # 1. upload through the project's own uploader, so the web-ready and SEO-name rules are
    #    enforced rather than remembered.
    tmp_plan = ROOT / "configs" / f".refresh-{args.person.lower()}.json"
    tmp_plan.write_text(json.dumps({
        "wave": f"refresh-{args.person}",
        "images": [{"source": str(source), "filename": new_name, "alt": src["alt"]}],
    }, indent=2))
    r = subprocess.run([sys.executable, "scripts/upload-theme-images.py",
                        str(tmp_plan.relative_to(ROOT))], cwd=ROOT,
                       capture_output=True, text=True)
    # The uploader's final summary print expects a `slot` key that a plan like this has no
    # reason to carry, so it traces AFTER writing handles back. Check the handle, not the
    # exit code.
    written = json.loads(tmp_plan.read_text())["images"][0].get("uploaded_handle")
    if not written:
        sys.exit("upload produced no handle:\n" + (r.stdout + r.stderr)[-2000:])
    print(f"uploaded : {written}")
    tmp_plan.unlink()

    # 2. resolve to a MediaImage GID. `shopify://` is a THEME reference and is not a valid
    #    file_reference metafield value — it is accepted and renders nothing.
    stem = new_name.rsplit(".", 1)[0]
    d = gql(store, tok,
            "query($q:String!){ files(first:25, query:$q){ nodes{ ... on MediaImage "
            "{ id image { url } } } } }", {"q": f"filename:{stem}"})
    gid = None
    for n in d["files"]["nodes"]:
        url = ((n.get("image") or {}).get("url") or "")
        if url.split("?")[0].rsplit("/", 1)[-1] == new_name:
            gid = n["id"]
            break
    if not gid:
        sys.exit(f"uploaded but could not resolve {new_name} to a MediaImage GID")
    print(f"gid      : {gid}")

    # 3. repoint the entry. UPDATE, never delete-and-recreate: translations key off the entry.
    d = gql(store, tok, """
      mutation ($handle: MetaobjectHandleInput!, $metaobject: MetaobjectUpsertInput!) {
        metaobjectUpsert(handle: $handle, metaobject: $metaobject) {
          metaobject { id handle }
          userErrors { field message code }
        }
      }""", {
        "handle": {"type": "customer_review", "handle": handle},
        "metaobject": {"fields": [{"key": "image", "value": gid}]},
    })["metaobjectUpsert"]
    if d["userErrors"]:
        sys.exit(json.dumps(d["userErrors"], indent=2))
    print(f"repointed: {d['metaobject']['handle']}")

    # 4. AND update the plan, or the next publish silently undoes all of the above.
    #    product-reviews-publish.py resolves each card's image from its `filename`, so a card
    #    still naming the superseded file repoints the entry straight back to it. Repointing
    #    the metaobject alone looks like a complete job and is not one.
    old_name = card["filename"]
    card["filename"] = new_name
    for img in plan.get("images", []):
        if img.get("filename") == old_name:
            img["filename"] = new_name
            img.pop("uploaded_handle", None)
    PLAN.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n")
    print(f"plan     : card + image entry now name {new_name}")
    print("\nNOTE: the old file is still in Shopify Files and is now unreferenced.")
    print(f"      {card['filename']}  — deleting it needs Malcolm's go-ahead.")


if __name__ == "__main__":
    main()
