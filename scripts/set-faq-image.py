#!/usr/bin/env python3
"""Point a product's FAQ section at the image published for it.

    python3 scripts/set-faq-image.py <gallery-plan.json> [--apply]

WHY THIS IS SEPARATE
`publish-product-gallery.py` uploads the FAQ image to Content > Files but does not wire it -
`product-faq-layout.py` sets `custom.faq_image` only for the nine main products, in bulk, so
bundles were being wired by hand.

IT MUST BE THE MediaImage GID. `sections/product-faq.liquid` reads
`product.metafields.custom.faq_image` as a `file_reference`. Writing a
`shopify://shop_images/<name>` handle into it SUCCEEDS - Shopify stores it happily as a string -
and then the section resolves nothing and the FAQ renders no image, with no error anywhere. The
GID is read back from the plan's `_published.files`, which publish-product-gallery records.

WHY IT IS IN FILES AND NOT PRODUCT MEDIA: a theme section can reference a file, but it cannot
reference product media. That is the whole reason the plan splits gallery from files_only.

Author: Claude Code, 2026-09-14.
"""
import argparse
import importlib.util
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "2025-01"
_spec = importlib.util.spec_from_file_location("uti", ROOT / "scripts" / "upload-theme-images.py")
uti = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(uti)


def gql(store, tok, query, variables=None):
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(f"https://{store}/admin/api/{API}/graphql.json", data=body,
                                 method="POST",
                                 headers={"X-Shopify-Access-Token": tok,
                                          "Content-Type": "application/json"})
    d = json.loads(urllib.request.urlopen(req, timeout=120).read())
    if "errors" in d:
        sys.exit(d["errors"])
    return d["data"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plan")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    plan = json.loads((ROOT / a.plan).read_text())
    files = (plan.get("_published") or {}).get("files") or []
    if not files:
        sys.exit("no _published.files in the plan - publish the gallery first")
    faq = next((f for f in files
                if any(x.get("earmarked", "").startswith("FAQ")
                       and x["file"] == f.get("stored_name") for x in plan["files_only"])), files[0])
    gid = faq["id"]
    if not gid.startswith("gid://shopify/MediaImage/"):
        sys.exit(f"refusing to write {gid!r} - the section needs a MediaImage GID")

    e = uti.env(); store = e["SHOPIFY_SKINGENETIX_STORE"]; tok = uti.token(e)
    print(f'product : {plan["product_label"]}\nfile    : {faq.get("stored_name")}\ngid     : {gid}')
    if not a.apply:
        print("\nDRY RUN - pass --apply to set the metafield")
        return 0

    d = gql(store, tok, """mutation($m:[MetafieldsSetInput!]!){ metafieldsSet(metafields:$m){
              metafields{ id key value } userErrors{ field message } } }""",
            {"m": [{"ownerId": plan["product_gid"], "namespace": "custom",
                    "key": "faq_image", "type": "file_reference", "value": gid}]})
    if d["metafieldsSet"]["userErrors"]:
        sys.exit(d["metafieldsSet"]["userErrors"])

    # Read back and RESOLVE it, rather than trusting that the write returned cleanly - a string
    # that cannot resolve is exactly the failure this script exists to prevent.
    chk = gql(store, tok, """query($id:ID!){ product(id:$id){
              metafield(namespace:"custom", key:"faq_image"){ value type
                reference{ ... on MediaImage { id image{ url width height } } } } } }""",
              {"id": plan["product_gid"]})["product"]["metafield"]
    ref = chk.get("reference") if chk else None
    print(f'\nstored  : {chk["value"]}  ({chk["type"]})')
    if not ref:
        sys.exit("WROTE BUT DOES NOT RESOLVE - the FAQ section will render nothing")
    print(f'resolves: {ref["image"]["width"]}x{ref["image"]["height"]}  '
          f'{ref["image"]["url"].split("/")[-1].split("?")[0]}')
    return 0


if __name__ == "__main__":
    sys.exit(main())
