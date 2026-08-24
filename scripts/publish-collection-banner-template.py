#!/usr/bin/env python3
"""Give a collection its own template so its banner can be tuned alone.

    python3 scripts/publish-collection-banner-template.py pdrn --dry-run
    python3 scripts/publish-collection-banner-template.py pdrn
    python3 scripts/publish-collection-banner-template.py pdrn --restore

Every collection shares templates/collection.json, so editing the banner there would
change all thirteen. This copies that template verbatim to templates/collection.<h>.json,
edits only the banner in the copy, and points the collection at it with templateSuffix.
Nothing else on the page moves and no Liquid is touched (.claude/rules/shopify.md 2, 3).

The shared defaults actively damage a designed shot, so every page here turns them off:

  enable_parallax false  parallax renders the image at 130% and only ever reveals 77%
                         of its height, which cut the bottom off both banners.
  image_size "auto"      the box is a FIXED pixel height (375/400/440) across a
                         full-bleed width, so its aspect runs from ~1.0 on a phone to
                         ~5.8 on a wide monitor and no single crop survives. "auto" is
                         the theme's own no-crop option.
  image / mobile_image   an explicit pair beats one image centre-cropped to a
                         near-square on phones.
  overlay_opacity        50 greyed the products out; each page carries its own value.

THREE TRAPS, each of which cost a round (see ADR-005):

  * "auto" leaves the image height as `auto`, and it is a grid item spanning every
    row -- so it stretches to the height of the overlaid TEXT, and object-fit: cover
    then crops the SIDES. Between 700 and 1099px the natural height is only width/3
    and default type overflows it. Every page's CSS scales type down across that band.
  * Section ids render as "shopify-section-template--<theme id>__<key>", so an id
    selector built from the section key silently matches nothing. Target the class.
  * Shopify rejects the `html` setting with a 422 if it contains "{{" or "}}" --
    which minified CSS produces the moment a rule closes inside a media query
    (";}}"). Keep the braces apart.

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
CSS_SECTION = "banner_text_width"


TABLET_RATIO = 1.62   # the crop shape used between 700 and 1099px


def css(text_width, scrim_from, cdn_url, crop, master_h, text_max="620px",
        tablet_width="34vw"):
    """Scoped CSS for one banner.

    text_width  : desktop measure, as a vw figure sized to the shot's clear zone
    scrim_from  : "bottom" or "top" -- which edge the phone text sits against. The
                  theme paints a flat tint on .collection-banner::before; raising it
                  enough to carry white text over a lit subject would flatten the
                  whole shot, so a gradient is layered onto the same pseudo-element
                  and darkens only the strip the text occupies.
    cdn_url     : the desktop file, used to build a server-side crop for tablets
    crop        : Shopify crop anchor -- which part of the shot to keep
    master_h    : the master's pixel height. The crop is sized from it because
                  Shopify will not upscale: ask for a height above the source and
                  it quietly ignores the crop and returns the full frame resized,
                  which background-size: cover then centre-crops -- losing the jar
                  entirely on /collections/pdrn.

    THE TABLET CROP IS NOT COSMETIC. Squeezing a 3:1 banner into 700-1099px shrinks
    the jar labels to ~3px per character, and at that size "PDRN" resolves as "PORN"
    -- the exact failure .claude/rules/website-imagery.md rule 3 was written about,
    reproduced here on both banners. Serving a bigger source does NOT fix it: the
    limit is the display size, not the delivery (a forced 1600w source rendered the
    same misread). Only enlarging the subject does, so this band gets a 1.62:1 crop
    where the labels come back to ~6px per character -- the same density as the
    1440px desktop view, which reads correctly. Shopify crops it on the fly, so no
    extra file is uploaded. DPR2 devices were never affected; they already pull a
    source big enough.
    """
    direction = "to top" if scrim_from == "bottom" else "to bottom"
    tablet = (f"{cdn_url}&width={round(master_h * TABLET_RATIO)}"
              f"&height={master_h}&crop={crop}")
    return "\n".join([
        "@media screen and (min-width: 700px) {",
        f"  .collection-banner .v-stack {{ max-width: clamp(320px, {text_width}, {text_max}); }}",
        "}",
        "@media screen and (min-width: 700px) and (max-width: 1099px) {",
        "  .collection-banner h1 { font-size: clamp(30px, 4.4vw, 50px); }",
        "  .collection-banner .prose { font-size: 0.85rem; line-height: 1.45; }",
        f"  .collection-banner .v-stack {{ max-width: {tablet_width}; gap: 0.6rem; }}",
        "  .collection-banner > picture { display: none; }",
        "  .collection-banner {",
        f"    min-height: {100 / TABLET_RATIO:.2f}vw;",
        f'    background-image: url("{tablet}");',
        "    background-size: cover;",
        "    background-position: center;",
        "  }",
        "}",
        "@media screen and (max-width: 699px) {",
        "  .collection-banner::before {",
        f"    background-image: linear-gradient({direction},",
        "      rgba(10, 14, 22, 0.85) 0%,",
        "      rgba(10, 14, 22, 0.62) 22%,",
        "      rgba(10, 14, 22, 0.00) 58%);",
        "  }",
        "}",
    ])


PAGES = {
    # /collections/all -- lit background sweep begins at x=515 of 1440, so the text
    # has to stay narrow. Phone crop is two bottles filling the frame, text sits
    # bottom-centre in the scrim.
    "all": {
        "plan": "configs/banners/collection-all-banner.json",
        "desktop": "collection_all_desktop",
        "mobile": "collection_all_mobile",
        "overlay": 25,
        "mobile_text": "place-self-end-center text-center",
        # centre keeps three of the four products; a right crop would halve the
        # copper-peptide bottle, which is the hero of the shot.
        "css": dict(text_width="30vw", scrim_from="bottom", crop="center", master_h=724),
    },
    # /collections/pdrn -- canvas extended left, so backdrop stays dark out to x=894
    # of 1440 and the text can breathe. The jar's label sits low in the phone crop,
    # so the text goes top-centre; a bottom scrim would have covered the product name.
    "pdrn": {
        "plan": "configs/banners/collection-pdrn-banner.json",
        "desktop": "collection_pdrn_desktop",
        "mobile": "collection_pdrn_mobile",
        "overlay": 22,
        "mobile_text": "place-self-start-center text-center",
        # right keeps the face and the jar together, which is the whole shot.
        "css": dict(text_width="40vw", scrim_from="top", text_max="640px",
                    crop="right", master_h=848),
    },
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


def rest(store, tok, path, method="GET", payload=None):
    data = json.dumps(payload).encode() if payload else None
    req = urllib.request.Request(f"https://{store}/admin/api/{API}/{path}", data=data,
                                 method=method,
                                 headers={"X-Shopify-Access-Token": tok,
                                          "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=90) as res:
            out = json.loads(res.read())
    except urllib.error.HTTPError as ex:
        sys.exit(f"HTTP {ex.code} on {method} {path}\n{ex.read().decode()[:600]}")
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
    ap.add_argument("handle", choices=sorted(PAGES), help="collection handle to publish")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--restore", action="store_true")
    args = ap.parse_args()
    page = PAGES[args.handle]

    e = env()
    store = e["SHOPIFY_SKINGENETIX_STORE"]
    tok = token(e)
    theme = [t for t in rest(store, tok, "themes.json")["themes"] if t["role"] == "main"][0]
    col = gql(store, tok, COLLECTION, {"handle": args.handle})["collectionByHandle"]
    if not col:
        sys.exit(f"no collection with handle {args.handle!r}")
    print(f"Theme     : {theme['id']} {theme['name']}")
    print(f"Collection: {col['title']}  templateSuffix={col['templateSuffix']!r}\n")

    template = f"templates/collection.{args.handle}.json"

    if args.restore:
        gql(store, tok, UPDATE, {"input": {"id": col["id"], "templateSuffix": None}})
        print(f"Restored: {args.handle} is back on the shared collection template.")
        print(f"{template} was left in place; delete it in the theme editor if unwanted.")
        return

    plan = json.loads((ROOT / page["plan"]).read_text())
    handles = {i["slot"]: i.get("uploaded_handle") for i in plan["images"]}
    missing = [k for k, v in handles.items() if not v]
    if missing:
        sys.exit(f"plan has no uploaded_handle for {missing} — run upload-theme-images.py first")
    cdn = {i["slot"]: i.get("cdn_url") for i in plan["images"]}[page["desktop"]]
    if not cdn:
        sys.exit(f"plan has no cdn_url for {page['desktop']} — needed for the tablet crop")
    page_css = css(cdn_url=cdn.split("&")[0], **page["css"])

    base = rest(store, tok,
                f"themes/{theme['id']}/assets.json?asset[key]=templates/collection.json")["asset"]
    tpl = json.loads(base["value"])

    BACKUPS.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    snap = BACKUPS / f"collection-{args.handle}-{stamp}.json"
    snap.write_text(json.dumps({"source_template": tpl,
                                "previous_template_suffix": col["templateSuffix"]},
                               indent=2) + "\n")
    print(f"Backed up source template + previous suffix -> {snap.relative_to(ROOT)}")

    banner = tpl["sections"]["banner"]["settings"]
    before = dict(banner)
    banner.update({
        "enable_parallax": False,
        "image_size": "auto",
        "overlay_opacity": page["overlay"],
        "desktop_text_position": "sm:place-self-center-start sm:text-start",
        "mobile_text_position": page["mobile_text"],
        "image": handles[page["desktop"]],
        "mobile_image": handles[page["mobile"]],
    })

    print("\nBanner settings:")
    for k in sorted(set(banner) - set()):
        if before.get(k) != banner[k]:
            print(f"  {k:<24} {before.get(k)!r}  ->  {banner[k]!r}")

    # Appended, never prepended: the banner sets allow_transparent_header, which the
    # theme only applies to the FIRST section. A <style> works from anywhere.
    tpl["sections"][CSS_SECTION] = {
        "type": "custom-html",
        "settings": {"full_width": True, "remove_vertical_spacing": True,
                     "remove_horizontal_spacing": True,
                     "html": f"<style>{page_css}</style>"},
    }
    if CSS_SECTION not in tpl["order"]:
        tpl["order"].append(CSS_SECTION)
    print(f"  {'text width':<24} added {CSS_SECTION} (custom-html <style>)")

    if args.dry_run:
        print("\n--dry-run: nothing written.")
        return

    rest(store, tok, f"themes/{theme['id']}/assets.json", "PUT",
         {"asset": {"key": template, "value": json.dumps(tpl, indent=2)}})
    print(f"\nWrote {template}")

    res = gql(store, tok, UPDATE, {"input": {"id": col["id"],
                                             "templateSuffix": args.handle}})
    errs = res["collectionUpdate"]["userErrors"]
    if errs:
        sys.exit(f"collectionUpdate: {errs}")
    print(f"Pointed /collections/{args.handle} at collection.{args.handle}")
    print(f"\nUndo:  python3 scripts/publish-collection-banner-template.py "
          f"{args.handle} --restore")


if __name__ == "__main__":
    main()
