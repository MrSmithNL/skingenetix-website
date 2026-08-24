#!/usr/bin/env python3
"""Give /collections/all its own template so its banner can be tuned alone.

    python3 scripts/publish-collection-all-template.py --dry-run
    python3 scripts/publish-collection-all-template.py
    python3 scripts/publish-collection-all-template.py --restore

Every collection currently shares templates/collection.json, so changing the
banner there would change /collections/serums, /collections/pdrn and ten others.
This copies that template verbatim to templates/collection.all.json, edits only
the banner section in the copy, and points the "all" collection at it via
templateSuffix. Nothing else on the page moves and no Liquid is touched
(.claude/rules/shopify.md rules 2 and 3).

Why the banner settings change:

  enable_parallax false  parallax renders the image at 130% and only ever shows
                         77% of its height, which cut the bottle bases off.
  image_size "auto"      the box is a FIXED pixel height (375/400/440) across a
                         full-bleed width, so its aspect runs from ~1.0 on a
                         phone to ~5.8 on a wide monitor and no single crop
                         survives. "auto" is the theme's own no-crop option.
  image / mobile_image   an explicit pair beats one image centre-cropped to a
                         near-square on phones.
  overlay_opacity 25     was 50, which greyed the products out. The heading moves
                         to the left, where the shot is already dark, so it stays
                         legible at 25.

Backs up the source template and the collection's previous templateSuffix before
writing, and --restore puts both back.

Author: Claude Code, 2026-08-24.
"""
import argparse
import json
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "2025-01"
BACKUPS = ROOT / "backups"
PLAN = ROOT / "configs/banners/collection-all-banner.json"
HANDLE = "all"
SUFFIX = "all"
TEMPLATE = f"templates/collection.{SUFFIX}.json"

BANNER_SETTINGS = {
    "enable_parallax": False,
    "image_size": "auto",
    "overlay_opacity": 25,
    "desktop_text_position": "sm:place-self-center-start sm:text-start",
    # On a phone the crop is two bottles filling the frame, so centred text lands
    # on them. Bottom-centre puts it in the scrim added below instead.
    "mobile_text_position": "place-self-end-center text-center",
}

# collection-banner has no content-width setting (the hero's content_max_width is a
# slideshow-only setting), and at full width the description ran across the bottle.
# Measured rather than eyeballed, the same way as the 2026-08-21 hero fix: with the
# 25% overlay applied, mean column luminance in the text rows stays under 120 out to
# x=515 of 1440, then climbs into the lit background. 515 less the 48px page gutter
# and a ~40px gap gives ~430px at that width, which is 30vw -- expressed as vw so it
# tracks the image on wider screens instead of pinning to one viewport.
#
# Keep the braces apart. Shopify validates the `html` setting for Liquid and
# rejects the asset with a 422 if it ever sees "{{" or "}}" -- which minified CSS
# produces the moment a rule closes inside a media query (";}}").
#
# Target the section's CLASS, not its id. Sections in a JSON template render as
# "shopify-section-template--<numeric theme id>__banner", so an id selector built
# from the section key silently matches nothing.
#
# The theme paints its overlay as a flat tint on .collection-banner::before. On a
# phone that is not enough: raising it far enough to carry white text over two lit
# bottles would flatten the whole shot. Layering a bottom-up gradient onto the same
# pseudo-element keeps the top of the frame clean and darkens only the strip the
# text sits in. background-color stays, background-image rides on top of it.
#
# image_size "auto" leaves the image height as `auto`, and because it is a grid item
# spanning every row that means "as tall as the overlaid text". Whenever the text is
# taller than the image's natural height at that width, the grid stretches it and
# object-fit: cover then crops the SIDES -- which is what cut the fourth product off
# at 768px. So between 700 and 1099, where natural height is only width/3, the type
# is scaled down to stay inside it.
BANNER_CSS = "\n".join([
    "@media screen and (min-width: 700px) {",
    "  .collection-banner .v-stack { max-width: clamp(320px, 30vw, 620px); }",
    "}",
    "@media screen and (min-width: 700px) and (max-width: 1099px) {",
    "  .collection-banner h1 { font-size: clamp(30px, 4.4vw, 50px); }",
    "  .collection-banner .prose { font-size: 0.85rem; line-height: 1.45; }",
    "  .collection-banner .v-stack { max-width: 34vw; gap: 0.6rem; }",
    "}",
    "@media screen and (max-width: 699px) {",
    "  .collection-banner::before {",
    "    background-image: linear-gradient(to top,",
    "      rgba(10, 14, 22, 0.85) 0%,",
    "      rgba(10, 14, 22, 0.62) 22%,",
    "      rgba(10, 14, 22, 0.00) 58%);",
    "  }",
    "}",
])
CSS_SECTION = "banner_text_width"


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


def rest(store, tok, path, method="GET", payload=None):
    data = json.dumps(payload).encode() if payload else None
    req = urllib.request.Request(f"https://{store}/admin/api/{API}/{path}", data=data,
                                 method=method,
                                 headers={"X-Shopify-Access-Token": tok,
                                          "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=90) as res:
        out = json.loads(res.read())
    time.sleep(0.6)
    return out


def gql(store, tok, query, variables=None):
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(f"https://{store}/admin/api/{API}/graphql.json",
                                 data=body,
                                 headers={"X-Shopify-Access-Token": tok,
                                          "Content-Type": "application/json"})
    res = json.loads(urllib.request.urlopen(req, timeout=90).read())
    if res.get("errors"):
        raise RuntimeError(res["errors"])
    time.sleep(0.6)
    return res["data"]


COLLECTION = """
query($handle:String!){ collectionByHandle(handle:$handle){ id title templateSuffix } }"""

UPDATE = """
mutation($input:CollectionInput!){
  collectionUpdate(input:$input){
    collection{ id handle templateSuffix }
    userErrors{ field message }
  }
}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--restore", action="store_true")
    args = ap.parse_args()

    e = env()
    store = e["SHOPIFY_SKINGENETIX_STORE"]
    tok = token(e)
    theme = [t for t in rest(store, tok, "themes.json")["themes"] if t["role"] == "main"][0]
    col = gql(store, tok, COLLECTION, {"handle": HANDLE})["collectionByHandle"]
    print(f"Theme     : {theme['id']} {theme['name']}")
    print(f"Collection: {col['title']}  templateSuffix={col['templateSuffix']!r}\n")

    if args.restore:
        gql(store, tok, UPDATE, {"input": {"id": col["id"], "templateSuffix": None}})
        print(f"Restored: {HANDLE} is back on the shared collection template.")
        print(f"{TEMPLATE} was left in place; delete it in the theme editor if unwanted.")
        return

    plan = json.loads(PLAN.read_text())
    handles = {i["slot"]: i.get("uploaded_handle") for i in plan["images"]}
    missing = [k for k, v in handles.items() if not v]
    if missing:
        sys.exit(f"plan has no uploaded_handle for {missing} — run upload-theme-images.py first")

    base = rest(store, tok,
                f"themes/{theme['id']}/assets.json?asset[key]=templates/collection.json")["asset"]
    tpl = json.loads(base["value"])

    BACKUPS.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    snap = BACKUPS / f"collection-all-{stamp}.json"
    snap.write_text(json.dumps({"source_template": tpl,
                                "previous_template_suffix": col["templateSuffix"]},
                               indent=2) + "\n")
    print(f"Backed up source template + previous suffix -> {snap.relative_to(ROOT)}")

    banner = tpl["sections"]["banner"]["settings"]
    before = dict(banner)
    banner.update(BANNER_SETTINGS)
    banner["image"] = handles["collection_all_desktop"]
    banner["mobile_image"] = handles["collection_all_mobile"]

    print("\nBanner settings:")
    for k in sorted(set(BANNER_SETTINGS) | {"image", "mobile_image"}):
        print(f"  {k:<24} {before.get(k)!r}  ->  {banner[k]!r}")

    # Constrain the overlaid text with a scoped <style>, the same custom-html
    # pattern the homepage already uses for its FAQ JSON-LD. Spacing is removed
    # so the section occupies no layout of its own.
    tpl["sections"][CSS_SECTION] = {
        "type": "custom-html",
        "settings": {"full_width": True, "remove_vertical_spacing": True,
                     "remove_horizontal_spacing": True,
                     "html": f"<style>{BANNER_CSS}</style>"},
    }
    # Appended, never prepended: the banner sets allow_transparent_header, which the
    # theme only applies to the FIRST section. A <style> works from anywhere.
    if CSS_SECTION not in tpl["order"]:
        tpl["order"].append(CSS_SECTION)
    print(f"  {'text width':<24} added {CSS_SECTION} (custom-html <style>)")

    if args.dry_run:
        print("\n--dry-run: nothing written.")
        return

    rest(store, tok, f"themes/{theme['id']}/assets.json", "PUT",
         {"asset": {"key": TEMPLATE, "value": json.dumps(tpl, indent=2)}})
    print(f"\nWrote {TEMPLATE}")

    res = gql(store, tok, UPDATE, {"input": {"id": col["id"], "templateSuffix": SUFFIX}})
    errs = res["collectionUpdate"]["userErrors"]
    if errs:
        sys.exit(f"collectionUpdate: {errs}")
    print(f"Pointed /collections/{HANDLE} at collection.{SUFFIX}")
    print("\nUndo:  python3 scripts/publish-collection-all-template.py --restore")


if __name__ == "__main__":
    main()
