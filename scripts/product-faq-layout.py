#!/usr/bin/env python3
"""Give the product FAQ the research-page layout, move it under the before/after
reviews, and bind a per-product photograph to it.

    python3 scripts/product-faq-layout.py --dry-run
    python3 scripts/product-faq-layout.py
    python3 scripts/product-faq-layout.py --restore backups/product-<stamp>.json

Three things happen, all reversible:

  1. `templates/product.json` — `product_faq` moves to sit directly after
     `before_after`, and its settings are re-pointed at the research-page layout
     (text_position `end` = questions left / image right, full_width off, plus the
     same support-hours and answer-time lines the research pages carry).
  2. Each product gets `custom.faq_image` set to its own uploaded photograph.
  3. Nothing else on the template moves.

All 11 products share this one template — the per-product templates were
consolidated away — which is why the image is a product metafield rather than a
section setting. See sections/product-faq.liquid for why the stock `faq` section
was not used: it would have flattened 66 per-product questions to one generic set
and dropped the FAQPage structured data.

Author: Claude Code, 2026-08-30.
"""
import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "2025-01"
BACKUPS = ROOT / "backups"
TEMPLATE = "templates/product.json"

# The research pages' own FAQ settings, so the two surfaces match.
FAQ_SETTINGS = {
    "full_width": False,
    "subheading": "",
    "title": "Frequently Asked Questions",
    "text_position": "end",
    "team_avatar_width": 350,
    "support_hours": "<p>Our customer support is available Monday to Friday: 8am-8:30pm.</p>",
    "answer_time": "Average answer time: 24h",
}

SET_MF = """
mutation($mf:[MetafieldsSetInput!]!){
  metafieldsSet(metafields:$mf){ metafields{ key ownerType } userErrors{ field message } }
}"""

PRODUCTS = """{ products(first:50){ nodes{ id handle
  metafield(namespace:"custom", key:"faq_image"){ value } } } }"""

FILE_ID = """query($q:String!){ files(first:5, query:$q){ nodes{ ... on MediaImage { id image{ url } } } } }"""


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


def call(store, tok, path, method="GET", payload=None):
    data = json.dumps(payload).encode() if payload else None
    r = urllib.request.Request(f"https://{store}/admin/api/{API}/{path}", data=data,
                               method=method,
                               headers={"X-Shopify-Access-Token": tok,
                                        "Content-Type": "application/json"})
    for a in range(6):
        try:
            with urllib.request.urlopen(r, timeout=90) as res:
                out = json.loads(res.read())
            time.sleep(0.5)
            return out
        except urllib.error.HTTPError as ex:
            if ex.code != 429:
                sys.stderr.write(ex.read().decode(errors="replace")[:1500] + "\n")
                raise
            time.sleep(2 ** a)
    raise RuntimeError(path)


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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--restore")
    ap.add_argument("--plan", default="configs/banners/product-faq-images.json")
    args = ap.parse_args()

    e = env()
    store = e["SHOPIFY_SKINGENETIX_STORE"]
    tok = token(e)
    theme = next(t for t in call(store, tok, "themes.json")["themes"] if t["role"] == "main")
    tid = theme["id"]
    print(f"Store      : {store}")
    print(f"Live theme : {theme['name']} (id {tid})\n")

    if args.restore:
        body = (ROOT / args.restore).read_text()
        call(store, tok, f"themes/{tid}/assets.json", "PUT",
             {"asset": {"key": TEMPLATE, "value": body}})
        print(f"RESTORED {TEMPLATE} from {args.restore}")
        return

    # ---------------------------------------------------------------- template
    raw = call(store, tok, f"themes/{tid}/assets.json?asset[key]={TEMPLATE}")["asset"]["value"]
    BACKUPS.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = BACKUPS / f"product-{stamp}.json"
    backup.write_text(raw)
    print(f"Backup     : {backup.relative_to(ROOT)}")
    print(f"Undo with  : python3 scripts/product-faq-layout.py --restore "
          f"{backup.relative_to(ROOT)}\n")

    doc = json.loads(raw)
    order = doc.get("order") or list(doc["sections"])
    if "product_faq" not in order or "before_after" not in order:
        sys.exit(f"expected product_faq and before_after in {order}")

    print(f"Order before: {' -> '.join(order)}")
    order.remove("product_faq")
    order.insert(order.index("before_after") + 1, "product_faq")
    doc["order"] = order
    print(f"Order after : {' -> '.join(order)}\n")

    sec = doc["sections"]["product_faq"]
    print("product_faq settings:")
    for k, v in FAQ_SETTINGS.items():
        old = sec.setdefault("settings", {}).get(k, "<unset>")
        sec["settings"][k] = v
        if old != v:
            print(f"   {k:20} {str(old)[:34]:34} -> {str(v)[:40]}")
    new = json.dumps(doc, indent=2)

    # ---------------------------------------------------------------- images
    plan = json.loads((ROOT / args.plan).read_text())
    by_slot = {i["slot"]: i for i in plan["images"]}
    missing = [s for s, i in by_slot.items() if not i.get("uploaded_handle")]
    if missing:
        sys.exit(f"no uploaded handle for: {missing}")

    prods = {p["handle"]: p for p in gql(store, tok, PRODUCTS)["products"]["nodes"]}
    sets = []
    print("\nPer-product FAQ image:")
    for handle, item in by_slot.items():
        p = prods.get(handle)
        if not p:
            sys.exit(f"no product with handle {handle}")
        fn = item["filename"]
        nodes = gql(store, tok, FILE_ID, {"q": f"filename:{Path(fn).stem}"})["files"]["nodes"]
        exact = [n for n in nodes
                 if n.get("image") and n["image"]["url"].split("/")[-1].split("?")[0] == fn]
        if not exact:
            sys.exit(f"uploaded file not found by exact name: {fn}")
        sets.append({"ownerId": p["id"], "namespace": "custom", "key": "faq_image",
                     "type": "file_reference", "value": exact[0]["id"]})
        print(f"   {handle:44} {fn}")

    if args.dry_run:
        out = BACKUPS / f"product-PROPOSED-{stamp}.json"
        out.write_text(new)
        print(f"\nDRY RUN — proposed template at {out.relative_to(ROOT)}, nothing pushed")
        return

    data = gql(store, tok, SET_MF, {"mf": sets})
    errs = data["metafieldsSet"]["userErrors"]
    if errs:
        sys.exit(f"metafieldsSet: {errs}")
    print(f"\nSET {len(sets)} product faq_image metafields")

    call(store, tok, f"themes/{tid}/assets.json", "PUT",
         {"asset": {"key": TEMPLATE, "value": new}})
    print(f"PUSHED {TEMPLATE}")


if __name__ == "__main__":
    main()
