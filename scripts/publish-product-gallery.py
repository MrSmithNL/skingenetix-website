#!/usr/bin/env python3
"""Put a chosen, ordered set of images on a product, and park the rest in Shopify Files.

    python3 scripts/publish-product-gallery.py <plan.json> --dry-run
    python3 scripts/publish-product-gallery.py <plan.json>
    python3 scripts/publish-product-gallery.py --undo backups/product-gallery-<stamp>.json

WHY NOT scripts/finals/shopify-merge-media.py
That script resolves its picks by scanning a finals directory for files marked `__` and
matching a `_<shot>_` fragment in the filename. Neither convention exists here: Malcolm marked
this selection with a SINGLE underscore and the filenames are grid references, not shot names.
Bending the files to fit the tool would mean renaming his marked files, and on this project
every tool that has touched a finals folder has had a mark-handling bug - four of them. The
marks are left exactly as he wrote them and the plan names files explicitly instead.

TWO DESTINATIONS, AND THEY ARE NOT THE SAME PLACE
  gallery[]    -> product media, via stagedUploadsCreate(resource IMAGE) + productCreateMedia.
                  These are what a shopper sees, in the plan's order.
  files_only[] -> Content > Files, via stagedUploadsCreate(resource FILE) + fileCreate.
                  A theme section can reference these as shopify://shop_images/<name>;
                  product media CANNOT be referenced that way, which is why the split exists
                  rather than uploading everything once and hiding some.

ORDER OF OPERATIONS: add, wait for READY, then reorder. Never reorder against media Shopify is
still processing - the positions land against a list that is still changing.

UPLOAD ONCE. Shopify SUFFIXES rather than replaces on a filename collision, so a second run
over the same names leaves duplicate files and the theme keeps serving the OLD one. This has
bitten the project three times. `--undo` therefore deletes what this run created rather than
re-uploading over it.

Author: Claude Code, 2026-09-11.
"""
import argparse
import importlib.util
import json
import mimetypes
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "2025-01"
BACKUPS = ROOT / "backups"

# Reuse the store's own optimiser and credential handling rather than restating either.
_spec = importlib.util.spec_from_file_location("uti", ROOT / "scripts" / "upload-theme-images.py")
uti = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(uti)


def gql(store, tok, query, variables=None):
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(f"https://{store}/admin/api/{API}/graphql.json", data=body,
                                 method="POST",
                                 headers={"X-Shopify-Access-Token": tok,
                                          "Content-Type": "application/json"})
    d = json.loads(urllib.request.urlopen(req, timeout=180).read())
    if d.get("errors"):
        sys.exit(f"GraphQL: {d['errors']}")
    return d["data"]


def stage(store, tok, path: Path, name: str, resource: str) -> str:
    q = """mutation($input:[StagedUploadInput!]!){ stagedUploadsCreate(input:$input){
      stagedTargets{ url resourceUrl parameters{ name value } }
      userErrors{ field message } } }"""
    d = gql(store, tok, q, {"input": [{
        "filename": name, "mimeType": mimetypes.guess_type(name)[0] or "image/jpeg",
        "resource": resource, "httpMethod": "POST", "fileSize": str(path.stat().st_size)}]})
    if d["stagedUploadsCreate"]["userErrors"]:
        sys.exit(f"stagedUploadsCreate: {d['stagedUploadsCreate']['userErrors']}")
    t = d["stagedUploadsCreate"]["stagedTargets"][0]
    boundary = "----skingenetix" + str(int(time.time() * 1000))
    head = "".join(
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"{p['name']}\"\r\n\r\n"
        f"{p['value']}\r\n" for p in t["parameters"]).encode()
    head += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; "
             f"filename=\"{name}\"\r\nContent-Type: image/jpeg\r\n\r\n").encode()
    payload = head + path.read_bytes() + f"\r\n--{boundary}--\r\n".encode()
    req = urllib.request.Request(
        t["url"], data=payload,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    urllib.request.urlopen(req, timeout=600).read()
    return t["resourceUrl"]


def undo(store, tok, saved):
    if saved.get("media_ids"):
        gql(store, tok, """mutation($id:ID!,$ids:[ID!]!){
              productDeleteMedia(productId:$id, mediaIds:$ids){
                deletedMediaIds mediaUserErrors{ field message } } }""",
            {"id": saved["product_gid"], "ids": saved["media_ids"]})
        print(f"  removed {len(saved['media_ids'])} product image(s)")
    if saved.get("file_ids"):
        gql(store, tok, """mutation($ids:[ID!]!){ fileDelete(fileIds:$ids){
              deletedFileIds userErrors{ field message } } }""",
            {"ids": saved["file_ids"]})
        print(f"  removed {len(saved['file_ids'])} file(s)")
    print("UNDONE")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plan", nargs="?")
    ap.add_argument("--undo")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    e = uti.env()
    store = e["SHOPIFY_SKINGENETIX_STORE"]
    tok = uti.token(e)
    print(f"Store : {store}\n")

    if args.undo:
        return undo(store, tok, json.loads((ROOT / args.undo).read_text()))

    plan = json.loads((ROOT / args.plan).read_text())
    src_dir = ROOT / plan["source_dir"]
    gallery = plan["gallery"]
    files_only = plan["files_only"]

    print(f"product : {plan['product_label']}")
    print(f"gid     : {plan['product_gid']}\n")
    print(f"GALLERY — {len(gallery)} images, visible on the product page, in this order:")
    for i, g in enumerate(gallery, 1):
        p = src_dir / g["file"]
        print(f"  {i}. {g['file']}  ({p.stat().st_size/1024:.0f}K)")
        print(f"       alt: {plan['product_label']} - {g['alt']}")
    print(f"\nFILES ONLY — {len(files_only)} images, uploaded but NOT on the product page:")
    for f in files_only:
        p = src_dir / f["file"]
        print(f"  . {f['file']}  ({p.stat().st_size/1024:.0f}K)")

    for it in gallery + files_only:
        p = src_dir / it["file"]
        if not p.exists():
            sys.exit(f"missing: {p}")
        warn = uti.check_seo_name(it["file"])
        if warn:
            print(f"\n  SEO name on {it['file']}: {'; '.join(warn)}")

    # Refuse to add to a product that already has media. This plan assumes an empty gallery;
    # on a product that already has images the right tool is shopify-merge-media.py, which
    # decides per live image whether it is retired.
    cur = gql(store, tok, """query($id:ID!){ product(id:$id){ title status
          media(first:50){ nodes{ ... on MediaImage { id } } } } }""",
              {"id": plan["product_gid"]})["product"]
    print(f"\nproduct currently has {len(cur['media']['nodes'])} media, status {cur['status']}")
    if cur["media"]["nodes"]:
        sys.exit("product already has media — use scripts/finals/shopify-merge-media.py instead")

    if args.dry_run:
        print("\nDRY RUN — nothing uploaded")
        return 0

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    BACKUPS.mkdir(exist_ok=True)
    backup = BACKUPS / f"product-gallery-{stamp}.json"
    saved = {"product_gid": plan["product_gid"], "product_handle": plan["product_handle"],
             "media_ids": [], "file_ids": []}
    backup.write_text(json.dumps(saved, indent=2))
    print(f"\nBackup    : {backup.relative_to(ROOT)}")
    print(f"Undo with : python3 scripts/publish-product-gallery.py --undo "
          f"{backup.relative_to(ROOT)}\n")

    print("uploading gallery to product media")
    for g in gallery:
        res = stage(store, tok, src_dir / g["file"], g["file"], "IMAGE")
        d = gql(store, tok, """mutation($id:ID!,$media:[CreateMediaInput!]!){
              productCreateMedia(productId:$id, media:$media){
                media{ ... on MediaImage { id } } mediaUserErrors{ field message } } }""",
                {"id": plan["product_gid"],
                 "media": [{"originalSource": res, "mediaContentType": "IMAGE",
                            "alt": f"{plan['product_label']} - {g['alt']}"}]})
        if d["productCreateMedia"]["mediaUserErrors"]:
            sys.exit(f"{g['file']}: {d['productCreateMedia']['mediaUserErrors']}")
        g["media_id"] = d["productCreateMedia"]["media"][0]["id"]
        saved["media_ids"].append(g["media_id"])
        backup.write_text(json.dumps(saved, indent=2))
        print(f"  + {g['file']}")

    print("\nuploading the rest to Content > Files")
    staged = []
    for f in files_only:
        res = stage(store, tok, src_dir / f["file"], f["file"], "FILE")
        staged.append({"originalSource": res, "contentType": "IMAGE", "alt": f["alt"]})
        print(f"  + {f['file']}")
    d = gql(store, tok, """mutation($files:[FileCreateInput!]!){ fileCreate(files:$files){
          files{ id fileStatus ... on MediaImage { image{ url } } }
          userErrors{ field message } } }""", {"files": staged})
    if d["fileCreate"]["userErrors"]:
        sys.exit(f"fileCreate: {d['fileCreate']['userErrors']}")
    saved["file_ids"] = [f["id"] for f in d["fileCreate"]["files"]]
    backup.write_text(json.dumps(saved, indent=2))

    print("\nwaiting for Shopify to finish processing")
    ids = [g["media_id"] for g in gallery]
    for _ in range(80):
        st = gql(store, tok, """query($id:ID!){ product(id:$id){ media(first:50){ nodes{
              ... on MediaImage { id status } } } } }""", {"id": plan["product_gid"]})
        by = {n["id"]: n.get("status") for n in st["product"]["media"]["nodes"]}
        if all(by.get(i) == "READY" for i in ids):
            print("  all gallery media READY")
            break
        time.sleep(5)
    else:
        sys.exit("gallery media did not reach READY — order NOT set; rerun --undo and retry")

    # Reorder only once everything is READY: positions applied against a list Shopify is still
    # building land in the wrong places.
    moves = [{"id": g["media_id"], "newPosition": str(i)} for i, g in enumerate(gallery)]
    d = gql(store, tok, """mutation($id:ID!,$moves:[MoveInput!]!){
          productReorderMedia(id:$id, moves:$moves){ userErrors{ field message } } }""",
            {"id": plan["product_gid"], "moves": moves})
    if d["productReorderMedia"]["userErrors"]:
        sys.exit(f"reorder: {d['productReorderMedia']['userErrors']}")
    print("  gallery order set")

    # Read back the REAL filenames Shopify stored. It sanitises names and SUFFIXES on
    # collision, so the name that comes back is authoritative - and it is what a theme
    # section must reference as shopify://shop_images/<name>. Guessing the name is how a
    # section ends up pointing at a file that does not exist and renders nothing at all.
    stored = gql(store, tok, """query($ids:[ID!]!){ nodes(ids:$ids){
          ... on MediaImage { id fileStatus image{ url } } } }""",
                 {"ids": saved["file_ids"]})["nodes"]
    files_out = []
    for n in stored:
        url = ((n or {}).get("image") or {}).get("url") or ""
        name = url.split("/")[-1].split("?")[0]
        files_out.append({"id": n["id"], "stored_name": name,
                          "handle": f"shopify://shop_images/{name}" if name else None})
    plan["_published"] = {
        "at": stamp,
        "backup": str(backup.relative_to(ROOT)),
        "gallery": [{"file": g["file"], "media_id": g["media_id"]} for g in gallery],
        "files": files_out,
    }
    for f in files_out:
        print(f"  file -> {f['stored_name']}")
    (ROOT / args.plan).write_text(json.dumps(plan, indent=2) + "\n")
    print(f"\nPUBLISHED — {len(gallery)} on the product, {len(files_only)} in Files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
