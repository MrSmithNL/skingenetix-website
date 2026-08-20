#!/usr/bin/env python3
"""Upload chosen images to a Shopify product, replacing its existing media.

Order of operations is deliberate: ADD the new media and wait for Shopify to
finish processing it, THEN delete the old, THEN set the exact order. Deleting
first would leave the live product with no images if an upload failed halfway.

Gallery order and alt text are Malcolm's decisions, not derivable from a
filename, so both live in a per-product plan under `upload-plans/`. Alt text is
read by search engines and screen readers, and "Pdrn collagen copper peptide
deep renewal repair skin cream hero whitebg" serves neither.

Usage:
    python3 scripts/finals/shopify-replace-media.py <finals-dir> <plan.json> [--dry-run]

`--dry-run` resolves and prints the exact order and alt text without
authenticating or touching the store. Run it before every live upload.

Author: Claude Code, 2026-08-20.
"""
import json
import mimetypes
import os
import sys
import time
import urllib.request
from collections import namedtuple

API = "2025-01"

Pick = namedtuple("Pick", "filename upload_name shot alt")


def resolve_picks(filenames, plan):
    """Map Malcolm's `__`-marked files onto the plan's ordered shot list.

    Every mismatch raises rather than falling back to a default, because the
    fallback would publish a wrongly-ordered or generically-described image to a
    live product page and nothing downstream would notice.
    """
    picks_by_shot = {}
    for f in filenames:
        matched = [s["shot"] for s in plan["order"] if f"_{s['shot']}_" in f]
        if not matched:
            raise ValueError(
                f"{f} matches no shot in the plan - add the shot to the plan, "
                f"or the image was renamed after the plan was written")
        if len(matched) > 1:
            raise ValueError(f"{f} matches {len(matched)} shots ({', '.join(matched)}) "
                             f"- shot keys must be unambiguous")
        shot = matched[0]
        if shot in picks_by_shot:
            raise ValueError(f"two files claim shot '{shot}': "
                             f"{picks_by_shot[shot]} and {f}")
        picks_by_shot[shot] = f

    if not picks_by_shot:
        raise ValueError("no images selected - nothing marked '__' in the finals folder")

    out = []
    for entry in plan["order"]:
        f = picks_by_shot.get(entry["shot"])
        if f is None:
            continue  # planned shot Malcolm did not pick; not an error
        out.append(Pick(filename=f,
                        upload_name=f.lstrip("_"),
                        shot=entry["shot"],
                        alt=f"{plan['product_label']} — {entry['alt']}"))
    return out


def token(store, cid, sec):
    body = json.dumps({"client_id": cid, "client_secret": sec,
                       "grant_type": "client_credentials"}).encode()
    req = urllib.request.Request(f"https://{store}/admin/oauth/access_token", data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())["access_token"]


def gql(store, tok, query, variables=None):
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(f"https://{store}/admin/api/{API}/graphql.json", data=body,
                                 headers={"Content-Type": "application/json",
                                          "X-Shopify-Access-Token": tok})
    with urllib.request.urlopen(req, timeout=180) as r:
        d = json.loads(r.read())
    if d.get("errors"):
        raise RuntimeError(d["errors"])
    return d["data"]


def staged_upload(store, tok, path, upload_name):
    q = """mutation($input:[StagedUploadInput!]!){ stagedUploadsCreate(input:$input){
      stagedTargets{ url resourceUrl parameters{ name value } }
      userErrors{ field message } } }"""
    d = gql(store, tok, q, {"input": [{"filename": upload_name,
                                       "mimeType": mimetypes.guess_type(upload_name)[0],
                                       "resource": "IMAGE", "httpMethod": "POST"}]})
    errs = d["stagedUploadsCreate"]["userErrors"]
    if errs:
        raise RuntimeError(errs)
    t = d["stagedUploadsCreate"]["stagedTargets"][0]

    boundary = "----skingenetix" + str(int(time.time() * 1000))
    parts = []
    for p in t["parameters"]:
        parts.append(f"--{boundary}\r\nContent-Disposition: form-data; "
                     f"name=\"{p['name']}\"\r\n\r\n{p['value']}\r\n")
    head = "".join(parts).encode()
    head += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; "
             f"filename=\"{upload_name}\"\r\nContent-Type: image/jpeg\r\n\r\n").encode()
    with open(path, "rb") as fh:
        payload = head + fh.read() + f"\r\n--{boundary}--\r\n".encode()
    req = urllib.request.Request(t["url"], data=payload,
                                 headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    with urllib.request.urlopen(req, timeout=300) as r:
        r.read()
    return t["resourceUrl"]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry_run = "--dry-run" in sys.argv
    if len(args) != 2:
        print(__doc__)
        return 2
    finals_dir, plan_path = args

    with open(plan_path) as fh:
        plan = json.load(fh)

    selected = sorted(f for f in os.listdir(finals_dir) if f.startswith("__"))
    picks = resolve_picks(selected, plan)

    print(f"product : {plan['product_label']}")
    print(f"gid     : {plan['product_gid']}")
    print(f"selected: {len(selected)} marked '__' -> {len(picks)} resolved\n")
    for i, p in enumerate(picks, 1):
        print(f"  {i}. {p.upload_name}")
        print(f"     alt: {p.alt}")

    if dry_run:
        print("\nDRY RUN - store not contacted, nothing changed.")
        return 0

    store = os.environ["SHOPIFY_SKINGENETIX_STORE"].replace("https://", "").rstrip("/")
    tok = token(store, os.environ["SHOPIFY_SKINGENETIX_CLIENT_ID"],
                os.environ["SHOPIFY_SKINGENETIX_CLIENT_SECRET"])
    print("\nauth OK")

    existing = gql(store, tok, """query($id:ID!){ product(id:$id){ title
        media(first:100){ edges{ node{ ... on MediaImage { id } } } } } }""",
                   {"id": plan["product_gid"]})["product"]
    old_ids = [e["node"]["id"] for e in existing["media"]["edges"] if e["node"].get("id")]
    print(f"product: {existing['title']}  ({len(old_ids)} existing media)")

    new_media = []
    for p in picks:
        resource = staged_upload(store, tok, os.path.join(finals_dir, p.filename),
                                 p.upload_name)
        d = gql(store, tok, """mutation($id:ID!,$media:[CreateMediaInput!]!){
              productCreateMedia(productId:$id, media:$media){
                media{ ... on MediaImage { id } } mediaUserErrors{ field message } } }""",
                {"id": plan["product_gid"],
                 "media": [{"originalSource": resource, "alt": p.alt,
                            "mediaContentType": "IMAGE"}]})
        errs = d["productCreateMedia"]["mediaUserErrors"]
        if errs:
            raise RuntimeError(f"{p.upload_name}: {errs}")
        new_media.append(d["productCreateMedia"]["media"][0]["id"])
        print(f"  + {p.upload_name}")

    print("\nwaiting for Shopify to finish processing...")
    for _ in range(60):
        st = gql(store, tok, """query($id:ID!){ product(id:$id){ media(first:100){ edges{ node{
              ... on MediaImage { id status } } } } } }""", {"id": plan["product_gid"]})
        by = {e["node"]["id"]: e["node"].get("status") for e in st["product"]["media"]["edges"]}
        if all(by.get(m) == "READY" for m in new_media):
            print("  all new media READY")
            break
        time.sleep(5)
    else:
        print("  WARNING: some media not READY yet; not deleting the old ones")
        return 1

    if old_ids:
        gql(store, tok, """mutation($id:ID!,$ids:[ID!]!){
              productDeleteMedia(productId:$id, mediaIds:$ids){
                deletedMediaIds mediaUserErrors{ field message } } }""",
            {"id": plan["product_gid"], "ids": old_ids})
        print(f"  removed {len(old_ids)} old media")

    moves = [{"id": m, "newPosition": str(i)} for i, m in enumerate(new_media)]
    gql(store, tok, """mutation($id:ID!,$moves:[MoveInput!]!){
          productReorderMedia(id:$id, moves:$moves){ userErrors{ field message } } }""",
        {"id": plan["product_gid"], "moves": moves})
    print("  order set")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
