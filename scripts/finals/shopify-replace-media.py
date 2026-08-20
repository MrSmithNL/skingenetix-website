#!/usr/bin/env python3
"""Upload chosen images to a Shopify product, replacing its existing media.

Order of operations is deliberate: ADD the new media and wait for Shopify to
finish processing it, THEN delete the old, THEN set the exact order. Deleting
first would leave the live product with no images if an upload failed halfway.

Alt text is written per shot rather than derived from the filename - alt text is
read by search engines and screen readers, and "Pdrn collagen copper peptide
deep renewal repair skin cream hero whitebg" serves neither.
"""
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.request

API = "2025-01"

PRODUCT = "Skingenetix PDRN Collagen Repair Deep Renewal Treatment cream, 50ml"
ALT = {
    "hero_whitebg": f"{PRODUCT} — jar on a white background",
    "open_jar_swatch": f"{PRODUCT} — open jar with a swatch of the pink cream",
    "product_and_box_angled": f"{PRODUCT} — jar beside its pink and silver carton",
    "silk_wrap": f"{PRODUCT} — jar resting on cream silk",
    "colourblock_pedestal_bold": f"{PRODUCT} — jar on a colour-block pedestal",
    "range_stacked_jars": f"{PRODUCT} — stacked jars from the Skingenetix range",
    "applying_to_cheek_closeup": f"{PRODUCT} — close-up of the cream applied to a cheek",
    "model_face": f"{PRODUCT} — model with the cream applied",
}


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


def staged_upload(store, tok, path):
    q = """mutation($input:[StagedUploadInput!]!){ stagedUploadsCreate(input:$input){
      stagedTargets{ url resourceUrl parameters{ name value } }
      userErrors{ field message } } }"""
    name = os.path.basename(path)
    d = gql(store, tok, q, {"input": [{"filename": name, "mimeType": mimetypes.guess_type(name)[0],
                                       "resource": "IMAGE", "httpMethod": "POST"}]})
    errs = d["stagedUploadsCreate"]["userErrors"]
    if errs:
        raise RuntimeError(errs)
    t = d["stagedUploadsCreate"]["stagedTargets"][0]

    boundary = "----skingenetix" + str(int(time.time() * 1000))
    parts = []
    for p in t["parameters"]:
        parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"{p['name']}\"\r\n\r\n{p['value']}\r\n")
    head = "".join(parts).encode()
    head += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{name}\"\r\n"
             f"Content-Type: image/jpeg\r\n\r\n").encode()
    with open(path, "rb") as fh:
        payload = head + fh.read() + f"\r\n--{boundary}--\r\n".encode()
    req = urllib.request.Request(t["url"], data=payload,
                                 headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    with urllib.request.urlopen(req, timeout=300) as r:
        r.read()
    return t["resourceUrl"]


def main():
    cfg_dir, product_gid = sys.argv[1], sys.argv[2]
    store = os.environ["SHOPIFY_SKINGENETIX_STORE"].replace("https://", "").rstrip("/")
    tok = token(store, os.environ["SHOPIFY_SKINGENETIX_CLIENT_ID"],
                os.environ["SHOPIFY_SKINGENETIX_CLIENT_SECRET"])
    print("auth OK")

    picks = sorted(f for f in os.listdir(cfg_dir) if f.startswith("__"))
    order = ["hero_whitebg", "open_jar_swatch", "product_and_box_angled", "silk_wrap",
             "colourblock_pedestal_bold", "range_stacked_jars",
             "applying_to_cheek_closeup", "model_face"]

    def rank(f):
        for i, k in enumerate(order):
            if f"_{k}_" in f:
                return i
        return len(order)
    picks.sort(key=rank)

    print(f"\nuploading {len(picks)} images in this order:")
    for i, f in enumerate(picks, 1):
        print(f"  {i}. {f.lstrip('_')}")

    existing = gql(store, tok, """query($id:ID!){ product(id:$id){ title
        media(first:100){ edges{ node{ ... on MediaImage { id } } } } } }""",
                   {"id": product_gid})["product"]
    old_ids = [e["node"]["id"] for e in existing["media"]["edges"] if e["node"].get("id")]
    print(f"\nproduct: {existing['title']}  ({len(old_ids)} existing media)")

    new_media = []
    for f in picks:
        path = os.path.join(cfg_dir, f)
        clean = f.lstrip("_")
        shot = next((k for k in order if f"_{k}_" in f), None)
        resource = staged_upload(store, tok, path)
        d = gql(store, tok, """mutation($id:ID!,$media:[CreateMediaInput!]!){
              productCreateMedia(productId:$id, media:$media){
                media{ ... on MediaImage { id } } mediaUserErrors{ field message } } }""",
                {"id": product_gid,
                 "media": [{"originalSource": resource, "alt": ALT.get(shot, PRODUCT),
                            "mediaContentType": "IMAGE"}]})
        errs = d["productCreateMedia"]["mediaUserErrors"]
        if errs:
            raise RuntimeError(f"{clean}: {errs}")
        mid = d["productCreateMedia"]["media"][0]["id"]
        new_media.append(mid)
        print(f"  + {clean}")

    print("\nwaiting for Shopify to finish processing...")
    for _ in range(60):
        st = gql(store, tok, """query($id:ID!){ product(id:$id){ media(first:100){ edges{ node{
              ... on MediaImage { id status } } } } } }""", {"id": product_gid})
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
            {"id": product_gid, "ids": old_ids})
        print(f"  removed {len(old_ids)} old media")

    moves = [{"id": m, "newPosition": str(i)} for i, m in enumerate(new_media)]
    d = gql(store, tok, """mutation($id:ID!,$moves:[MoveInput!]!){
          productReorderMedia(id:$id, moves:$moves){ userErrors{ field message } } }""",
            {"id": product_gid, "moves": moves})
    print("  order set")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
