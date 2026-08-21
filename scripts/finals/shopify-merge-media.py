#!/usr/bin/env python3
"""Add chosen images to a product, retiring only the ones they supersede.

    python3 scripts/finals/shopify-merge-media.py <finals-dir> <plan.json> [--dry-run]

`shopify-replace-media.py` swaps a product's whole gallery. That is right when
every live image carries a retired label, and wrong when only some do: on the
Copper Peptide Renewal Serum, three of seven live shots have a direct
replacement among the new set and four have none. Replacing all seven would
throw away four compositions that nothing else covers.

So this MERGES. The plan names, per live image, whether it is retired; anything
not named is kept exactly as it is, alt text included. The new images are added,
and the final gallery order interleaves both.

Order of operations is the same as the replace script and for the same reason:
add, wait for READY, THEN delete, then reorder. Deleting first risks a live
product page with holes in it if an upload fails halfway.

Author: Claude Code, 2026-08-21.
"""
import json
import mimetypes
import os
import sys
import time
import urllib.request

API = "2025-01"


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


def staged_upload(store, tok, path, name):
    q = """mutation($input:[StagedUploadInput!]!){ stagedUploadsCreate(input:$input){
      stagedTargets{ url resourceUrl parameters{ name value } }
      userErrors{ field message } } }"""
    d = gql(store, tok, q, {"input": [{"filename": name,
                                       "mimeType": mimetypes.guess_type(name)[0],
                                       "resource": "IMAGE", "httpMethod": "POST"}]})
    if d["stagedUploadsCreate"]["userErrors"]:
        raise RuntimeError(d["stagedUploadsCreate"]["userErrors"])
    t = d["stagedUploadsCreate"]["stagedTargets"][0]
    boundary = "----skingenetix" + str(int(time.time() * 1000))
    parts = [f"--{boundary}\r\nContent-Disposition: form-data; name=\"{p['name']}\"\r\n\r\n{p['value']}\r\n"
             for p in t["parameters"]]
    head = "".join(parts).encode()
    head += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; "
             f"filename=\"{name}\"\r\nContent-Type: image/jpeg\r\n\r\n").encode()
    with open(path, "rb") as fh:
        payload = head + fh.read() + f"\r\n--{boundary}--\r\n".encode()
    req = urllib.request.Request(t["url"], data=payload,
                                 headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    with urllib.request.urlopen(req, timeout=300) as r:
        r.read()
    return t["resourceUrl"]


def resolve(finals_dir, plan):
    """Map each `shot` entry in the plan's order to exactly one marked file."""
    picks = sorted(f for f in os.listdir(finals_dir) if f.startswith("__"))
    out = []
    used = set()
    for entry in plan["order"]:
        if "keep" in entry:
            out.append(entry)
            continue
        matched = [f for f in picks if f"_{entry['shot']}_" in f]
        if len(matched) != 1:
            raise ValueError(f"shot '{entry['shot']}' matched {len(matched)} files: {matched}")
        f = matched[0]
        if f in used:
            raise ValueError(f"{f} claimed twice")
        used.add(f)
        out.append({**entry, "file": f, "upload_name": f.lstrip("_")})
    # A marked file missing from the plan usually means Malcolm chose something
    # and it was forgotten - worth refusing over. But on a follow-up merge the
    # already-published picks are still marked locally and appear in the plan as
    # `keep` media ids, so the plan can opt out with a stated reason.
    unclaimed = [f for f in picks if f not in used]
    if unclaimed:
        why = plan.get("allow_unclaimed_marks")
        if not why:
            raise ValueError(
                f"marked '__' but not in the plan order: {unclaimed}. Add them to the "
                f"order, or set `allow_unclaimed_marks` to say why they are excluded.")
        print(f"\nnote: {len(unclaimed)} marked file(s) not in this plan - {why}")
        for f in unclaimed:
            print(f"   . {f.lstrip('_')}")
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv
    if len(args) != 2:
        print(__doc__)
        return 2
    finals_dir, plan_path = args
    with open(plan_path) as fh:
        plan = json.load(fh)
    steps = resolve(finals_dir, plan)

    retire = {r["media_id"]: r.get("why", "") for r in plan.get("retire", [])}
    print(f"product : {plan['product_label']}")
    print(f"gid     : {plan['product_gid']}")
    print(f"\nretiring {len(retire)} live image(s):")
    for mid, why in retire.items():
        print(f"   - {mid.split('/')[-1]}  {why}")
    print(f"\nfinal gallery ({len(steps)}):")
    for i, s in enumerate(steps, 1):
        if "keep" in s:
            print(f"  {i:>2}. KEEP  {s['keep'].split('/')[-1]}  {s.get('note','')}")
        else:
            print(f"  {i:>2}. NEW   {s['upload_name']}")
            print(f"      alt: {plan['product_label']} - {s['alt']}")
    if dry:
        print("\nDRY RUN - store not contacted, nothing changed.")
        return 0

    store = os.environ["SHOPIFY_SKINGENETIX_STORE"].replace("https://", "").rstrip("/")
    tok = token(store, os.environ["SHOPIFY_SKINGENETIX_CLIENT_ID"],
                os.environ["SHOPIFY_SKINGENETIX_CLIENT_SECRET"])
    print("\nauth OK")

    live = gql(store, tok, """query($id:ID!){ product(id:$id){ media(first:60){ edges{ node{
          ... on MediaImage { id } } } } } }""", {"id": plan["product_gid"]})
    live_ids = {e["node"]["id"] for e in live["product"]["media"]["edges"]}
    for mid in retire:
        if mid not in live_ids:
            raise RuntimeError(f"{mid} is not on this product - refusing to run")
    for s in steps:
        if "keep" in s and s["keep"] not in live_ids:
            raise RuntimeError(f"{s['keep']} is not on this product - refusing to run")

    added = []
    for s in steps:
        if "keep" in s:
            continue
        res = staged_upload(store, tok, os.path.join(finals_dir, s["file"]), s["upload_name"])
        d = gql(store, tok, """mutation($id:ID!,$media:[CreateMediaInput!]!){
              productCreateMedia(productId:$id, media:$media){
                media{ ... on MediaImage { id } } mediaUserErrors{ field message } } }""",
                {"id": plan["product_gid"],
                 "media": [{"originalSource": res,
                            "alt": f"{plan['product_label']} - {s['alt']}",
                            "mediaContentType": "IMAGE"}]})
        if d["productCreateMedia"]["mediaUserErrors"]:
            raise RuntimeError(f"{s['upload_name']}: {d['productCreateMedia']['mediaUserErrors']}")
        s["media_id"] = d["productCreateMedia"]["media"][0]["id"]
        added.append(s["media_id"])
        print(f"  + {s['upload_name']}")

    print("\nwaiting for Shopify to finish processing...")
    for _ in range(60):
        st = gql(store, tok, """query($id:ID!){ product(id:$id){ media(first:60){ edges{ node{
              ... on MediaImage { id status } } } } } }""", {"id": plan["product_gid"]})
        by = {e["node"]["id"]: e["node"].get("status") for e in st["product"]["media"]["edges"]}
        if all(by.get(m) == "READY" for m in added):
            print("  all new media READY")
            break
        time.sleep(5)
    else:
        print("  WARNING: some media not READY; nothing deleted")
        return 1

    if retire:
        gql(store, tok, """mutation($id:ID!,$ids:[ID!]!){
              productDeleteMedia(productId:$id, mediaIds:$ids){
                deletedMediaIds mediaUserErrors{ field message } } }""",
            {"id": plan["product_gid"], "ids": list(retire)})
        print(f"  retired {len(retire)} superseded image(s)")

    moves = [{"id": (s["keep"] if "keep" in s else s["media_id"]), "newPosition": str(i)}
             for i, s in enumerate(steps)]
    gql(store, tok, """mutation($id:ID!,$moves:[MoveInput!]!){
          productReorderMedia(id:$id, moves:$moves){ userErrors{ field message } } }""",
        {"id": plan["product_gid"], "moves": moves})
    print("  order set")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
