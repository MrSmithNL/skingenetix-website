#!/usr/bin/env python3
"""Upload chosen banner images to Shopify Files so the theme can reference them.

    python3 scripts/upload-theme-images.py configs/banners/homepage-publish.json

Theme sections reference imagery as `shopify://shop_images/<filename>`, which resolves
against Content > Files — NOT against product media. So this uses the Files API
(stagedUploadsCreate -> POST -> fileCreate) rather than the productCreateMedia path
that scripts/finals/shopify-*-media.py use.

New filenames only. Per .claude/rules/shopify.md rule 7 an existing image is never
renamed or re-uploaded, because Langify keys translations off the URL; these are
additional files and the originals are left untouched.

Writes the resolved shopify:// handles back into the plan file so the patch step
cannot guess a filename Shopify silently sanitised.

Author: Claude Code, 2026-08-21.
"""
import json
import mimetypes
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "2025-01"


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
    req = urllib.request.Request(f"https://{e['SHOPIFY_SKINGENETIX_STORE']}/admin/oauth/access_token",
                                 data=body, headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=60).read())["access_token"]


def gql(store, tok, query, variables=None):
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(f"https://{store}/admin/api/{API}/graphql.json", data=body,
                                 headers={"X-Shopify-Access-Token": tok,
                                          "Content-Type": "application/json"})
    res = json.loads(urllib.request.urlopen(req, timeout=120).read())
    if res.get("errors"):
        raise RuntimeError(res["errors"])
    return res["data"]


STAGED = """
mutation($input:[StagedUploadInput!]!){
  stagedUploadsCreate(input:$input){
    stagedTargets{ url resourceUrl parameters{ name value } }
    userErrors{ field message }
  }
}"""

CREATE = """
mutation($files:[FileCreateInput!]!){
  fileCreate(files:$files){
    files{ id fileStatus alt ... on MediaImage { image { url } } }
    userErrors{ field message }
  }
}"""

POLL = """
query($q:String!){
  files(first:20, query:$q){
    edges{ node{ id fileStatus alt ... on MediaImage { image { url } } } }
  }
}"""


def post_multipart(url, params, filepath, filename):
    boundary = "----skingenetix" + str(int(time.time()))
    body = b""
    for p in params:
        body += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"{p['name']}\"\r\n\r\n"
                 f"{p['value']}\r\n").encode()
    ctype = mimetypes.guess_type(filename)[0] or "image/jpeg"
    body += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; "
             f"filename=\"{filename}\"\r\nContent-Type: {ctype}\r\n\r\n").encode()
    body += Path(filepath).read_bytes() + f"\r\n--{boundary}--\r\n".encode()
    req = urllib.request.Request(url, data=body,
                                 headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return r.status


def main():
    plan_path = ROOT / sys.argv[1]
    plan = json.loads(plan_path.read_text())
    e = env()
    store = e["SHOPIFY_SKINGENETIX_STORE"]
    tok = token(e)

    items = [i for i in plan["images"] if not i.get("uploaded_handle")]
    if not items:
        print("Every image in the plan already has a handle — nothing to upload.")
        return

    print(f"Store : {store}")
    print(f"Upload: {len(items)} images\n")

    # 1. staged targets
    staged_in = []
    for it in items:
        src = ROOT / it["source"]
        if not src.exists():
            sys.exit(f"missing source: {it['source']}")
        staged_in.append({"resource": "FILE", "filename": it["filename"],
                          "mimeType": mimetypes.guess_type(it["filename"])[0] or "image/jpeg",
                          "httpMethod": "POST", "fileSize": str(src.stat().st_size)})

    data = gql(store, tok, STAGED, {"input": staged_in})
    errs = data["stagedUploadsCreate"]["userErrors"]
    if errs:
        sys.exit(f"stagedUploadsCreate: {errs}")
    targets = data["stagedUploadsCreate"]["stagedTargets"]

    # 2. push bytes, 3. register
    files_in = []
    for it, tgt in zip(items, targets):
        src = ROOT / it["source"]
        print(f"  uploading {it['filename']} ...", end=" ", flush=True)
        post_multipart(tgt["url"], tgt["parameters"], src, it["filename"])
        print("ok")
        files_in.append({"originalSource": tgt["resourceUrl"], "contentType": "IMAGE",
                         "alt": it["alt"]})

    data = gql(store, tok, CREATE, {"files": files_in})
    errs = data["fileCreate"]["userErrors"]
    if errs:
        sys.exit(f"fileCreate: {errs}")
    print(f"\n  registered {len(data['fileCreate']['files'])} files, waiting for READY")

    # 4. poll until Shopify has processed them, and read back the REAL filename
    for attempt in range(30):
        time.sleep(4)
        done = 0
        for it in items:
            stem = it["filename"].rsplit(".", 1)[0]
            res = gql(store, tok, POLL, {"q": f"filename:{stem}*"})
            for edge in res["files"]["edges"]:
                node = edge["node"]
                if node["fileStatus"] != "READY" or not node.get("image"):
                    continue
                real = node["image"]["url"].split("?")[0].split("/")[-1]
                if real.rsplit(".", 1)[0].startswith(stem[:40]):
                    it["uploaded_handle"] = f"shopify://shop_images/{real}"
                    it["cdn_url"] = node["image"]["url"]
                    done += 1
                    break
        print(f"    ready {done}/{len(items)}")
        if done == len(items):
            break
    else:
        sys.exit("timed out waiting for files to reach READY")

    plan_path.write_text(json.dumps(plan, indent=2) + "\n")
    print("\nResolved handles:")
    for it in plan["images"]:
        if it.get("uploaded_handle"):
            print(f"  {it['slot']:<26} {it['uploaded_handle']}")
    print(f"\nWrote handles back into {sys.argv[1]}")


if __name__ == "__main__":
    main()
