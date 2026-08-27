#!/usr/bin/env python3
"""Turn every main-menu dropdown except Shop into a row of image tiles.

    python3 scripts/menu-image-tiles.py --dry-run
    python3 scripts/menu-image-tiles.py
    python3 scripts/menu-image-tiles.py --restore backups/header-group-<stamp>.json \
                                        --key sections/header-group.json

WHY IT IS DONE THIS WAY
-----------------------
Impact renders a mega menu as: a column of text sub-links on the left
(`ul.mega-menu__nav`, built from the Shopify menu's children) and up to three
"promo" images on the right. The three is a hard cap — `for i in (1..3)` in both
`snippets/mega-menu-horizontal.liquid` and `snippets/navigation-promo-block.liquid`,
and the schema defines image_1..image_3 and nothing more.

Scientific Research has five children and Skin Solutions four, so the promo slots
cannot carry the tiles. Using them would also mean deleting the children from the
Shopify menu, which is what feeds the mobile drawer and the Translate & Adapt
resources.

So the sub-links themselves become the tiles: each `.mega-menu__nav > li > a` gets
a square background image keyed off its own href, its title laid over a scrim, and
the (now empty) promo column is hidden. Any number of tiles, no Liquid touched
(.claude/rules/shopify.md rules 2 and 3), menu data and mobile navigation intact.

Two of the four menus — Skin Solutions and Support — had no mega_menu block at all
and rendered as plain dropdowns, so this adds one for each. Shop is left exactly
as it is.

Author: Claude Code, 2026-08-27.
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
HEADER_KEY = "sections/header-group.json"
FOOTER_KEY = "sections/footer-group.json"

# The store's file CDN. Tiles are cropped square by the CDN rather than by CSS, so
# what ships is exactly what was judged on the contact sheet.
CDN = "https://cdn.shopify.com/s/files/1/0932/8679/3601/files/"
CROP = "?width=560&height=560&crop=center"

# href -> image file. The href is matched with $= so a locale-prefixed URL
# (/de/pages/...) still matches once more languages are published.
# Malcolm's picks, 2026-08-27. Two rules run through them: Skin Solutions reuses
# the SAME masters as the homepage `skin_concerns` tiles so the two surfaces agree,
# and Scientific Research reuses the per-ingredient research squares from
# `page.science.json` → `ingredients_overview`. Everything here is already square,
# so the CDN crop takes nothing off the subject.
TILES = {
    # --- Skin Solutions: the homepage solution tiles (templates/index.json →
    # `skin_concerns`), so the menu and the homepage show the same picture.
    "/pages/fine-lines-wrinkles": "skingenetix-concern-fine-lines-wrinkles-2026.jpg",
    "/pages/firming-skin-density": "skingenetix-skin-firming-density-peptide-treatment.jpg",
    "/pages/skin-repair-renewal": "skingenetix-concern-skin-repair-renewal-2026.jpg",
    # The one deliberate departure from the homepage set: Malcolm picked this frame
    # off the options sheet rather than the homepage's brightening-glow-2026 tile.
    "/pages/brightening-glow": "skingenetix-brightening-glow-luminous-radiant-complexion-close-up.jpg",

    # --- Scientific Research: the key-ingredient research squares already used on
    # /pages/the-science. All five are 1400px+ square masters.
    "/pages/copper-peptide-research": "skingenetix-copper-peptide-ghk-cu-fibroblast-collagen-matrix.jpg",
    "/pages/matrixyl-3000-research": "skingenetix-matrixyl-3000-collagen-matrix-structure-laboratory.jpg",
    "/pages/acetyl-hexapeptide-8-research": "skingenetix-acetyl-hexapeptide-8-skin-cell-microscopy-research.jpg",
    "/pages/pdrn-research": "skingenetix-pdrn-polynucleotide-dna-helix-skin-research.jpg",
    "/pages/glutathione-research": "skingenetix-glutathione-antioxidant-skin-cell-microscopy-research.jpg",

    # --- Discover
    # The microscope frame that was the Discover mega menu's own promo image before
    # this rebuild — Malcolm asked for it back.
    "/pages/the-science": "skingenetix-menu-scientific-research-2026-v3.jpg",
    "/pages/ingredients": "skingenetix-copper-peptide-ghk-cu-blue-crystals-laboratory.jpg",
    # Malcolm's pick off the model head-shot sheet, 2026-08-27. Note this frame is
    # also the homepage `skin_concerns` Brightening & Glow tile, so the same
    # photograph reads as two different things on two surfaces. Flagged, not
    # changed — it was chosen on sight.
    "/pages/our-philosophy": "skingenetix-concern-brightening-glow-2026.jpg",

    # --- Support
    "/pages/faq": "skingenetix-skincare-faq-questions-answered-mobile.jpg",
    # Purpose-made: candidate 2 of the 24-image dermatologist batch
    # (configs/banners/menu-contact-dermatologist.json, CONTACT-A-listening / gpt_image),
    # chosen by Malcolm and published via configs/banners/menu-contact-tile-publish.json.
    # Replaces a bathroom-vanity stand-in. The only file the store had named for this
    # job, skingenetix-contact-banner.jpg, is unusable: the generation brief is printed
    # across it and it shows an unbranded competitor-looking bottle.
    "/pages/contact": "skingenetix-dermatologist-skin-consultation-client-conversation.jpg",
    "/pages/shipping-returns": "skingenetix-skincare-order-packed-white-shipping-box.jpg",
}

# One signature link per tiled menu, used to scope the CSS to that menu's
# .mega-menu container. Scoping by structure ("menus whose links have no
# children") or by a block count has bitten this store before; a link that exists
# in exactly one menu cannot drift. None of these appear under Shop, whose
# children are all /collections/*.
SIGNATURES = [
    "/pages/fine-lines-wrinkles",       # Skin Solutions
    "/pages/copper-peptide-research",   # Scientific Research
    "/pages/our-philosophy",            # Discover
    "/pages/shipping-returns",          # Support
]

MARK_START = "/* === SGX MENU IMAGE TILES START === */"
MARK_END = "/* === SGX MENU IMAGE TILES END === */"


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
    for attempt in range(6):
        try:
            with urllib.request.urlopen(r, timeout=90) as res:
                out = json.loads(res.read())
            time.sleep(0.5)
            return out
        except urllib.error.HTTPError as ex:
            if ex.code != 429:
                # custom-html rejects some payloads with the real reason buried in
                # the body rather than the status line.
                sys.stderr.write(ex.read().decode(errors="replace")[:2000] + "\n")
                raise
            time.sleep(2 ** attempt)
    raise RuntimeError(path)


def build_css():
    scope = ",\n".join(
        f'.mega-menu:has(.mega-menu__nav > li > a[href$="{h}"])' for h in SIGNATURES)
    tile_scope = ",\n".join(
        f'.mega-menu:has(.mega-menu__nav > li > a[href$="{h}"]) .mega-menu__nav > li > a'
        for h in SIGNATURES)
    nav_scope = ",\n".join(
        f'.mega-menu:has(.mega-menu__nav > li > a[href$="{h}"]) .mega-menu__nav'
        for h in SIGNATURES)
    promo_scope = ",\n".join(
        f'.mega-menu:has(.mega-menu__nav > li > a[href$="{h}"]) .navigation-promo__wrapper'
        for h in SIGNATURES)
    scrim_scope = ",\n".join(
        f'.mega-menu:has(.mega-menu__nav > li > a[href$="{h}"]) .mega-menu__nav > li > a::after'
        for h in SIGNATURES)
    hover_scope = ",\n".join(
        f'.mega-menu:has(.mega-menu__nav > li > a[href$="{h}"]) .mega-menu__nav > li > a:hover'
        for h in SIGNATURES)
    hover_after_scope = ",\n".join(
        f'.mega-menu:has(.mega-menu__nav > li > a[href$="{h}"]) '
        f'.mega-menu__nav > li > a:hover::after'
        for h in SIGNATURES)
    span_scope = ",\n".join(
        f'.mega-menu:has(.mega-menu__nav > li > a[href$="{h}"]) .mega-menu__nav > li > a > span'
        for h in SIGNATURES)

    images = "\n".join(
        f'.mega-menu__nav > li > a[href$="{h}"] '
        + "{ background-image: url(\"" + CDN + f + CROP + "\"); }"
        for h, f in TILES.items())

    return f"""{MARK_START}
/* Main-menu image tiles — Claude Code, 2026-08-27.
   Every top-level dropdown EXCEPT Shop shows its sub-links as square photo tiles
   with the link title laid over the image, and no text column beside them.

   Additive only. No theme Liquid or CSS file is touched
   (.claude/rules/shopify.md rules 2 and 3); this restyles markup the theme
   already emits.

   WHY NOT THE THEME'S OWN PROMO IMAGES: the promo block is capped at three
   images (`for i in (1..3)` in mega-menu-horizontal.liquid and
   navigation-promo-block.liquid, and image_1..image_3 in the header schema).
   Scientific Research needs five tiles and Skin Solutions four. Using the promo
   slots would also mean deleting the sub-links from the Shopify menu, and those
   sub-links are what the mobile drawer and the Translate & Adapt resources read.

   SCOPE: one signature href per menu, not a structural test and not a block
   count. A "menus whose links have no grandchildren" rule would silently drop
   the tiles the day a grandchild is added; a count rule has already broken five
   pages on this store once.

   The desktop nav itself only exists above 1150px — below that the header shows
   the hamburger drawer, whose text list is deliberately left alone.
   Cropping is done by the Shopify CDN (width=560&height=560&crop=center), not by
   CSS, so the delivered pixels are the ones that were judged.

   !important on the custom properties is required, not decorative:
   mega-menu-horizontal.liquid writes --mega-menu-nav-column-max-width,
   --mega-menu-justify-content and --column-list-max-width into an inline
   <style> block keyed on #mega-menu-<block-id>, and an id selector outranks
   anything a class rule here can say. */
@media screen and (min-width: 1150px) {{
{scope} {{
  --mega-menu-nav-column-max-width: clamp(150px, 15.5vw, 232px) !important;
  --column-list-max-width: none !important;
  --mega-menu-justify-content: center !important;
  --mega-menu-gap: 0 !important;
}}
{nav_scope} {{
  max-width: none !important;
  flex: 0 1 auto;
  justify-content: center;
  gap: var(--spacing-4, 1rem);
}}
/* The promo column is empty once the image_1..3 settings are cleared, but the
   snippet still emits its wrapper. A zero-content flex child would still take
   the gap. */
{promo_scope} {{
  display: none !important;
}}
{tile_scope} {{
  display: flex;
  align-items: flex-end;
  position: relative;
  isolation: isolate;
  aspect-ratio: 1 / 1;
  width: 100%;
  padding: var(--spacing-4, 1rem);
  overflow: hidden;
  border-radius: 6px;
  background-color: #efece7;
  /* 100% 100% rather than `cover` on purpose: the tile is exactly square and the
     CDN crop is exactly square, so the two are identical here — but a percentage
     is animatable and the `cover` keyword is not, which is what makes the hover
     zoom below possible. */
  background-size: 100% 100%;
  background-position: center;
  background-repeat: no-repeat;
  /* The theme's own image hover, lifted verbatim from `.zoom-image` in theme.css
     (scale 1.06 over 1.5s, same easing) so the tiles and Shop's promo images
     behave identically. Driven off background-size rather than `transform`
     because a transform on this anchor measurably does NOT apply, however the
     rule is written: Chrome reports the anchor matching :hover and lists the rule
     among the matched styles, yet the computed transform stays at identity at
     200ms, 600ms, 1.2s and 2s, on every menu. An injected `transform ... !important`
     on the same node DOES apply, so the element is transformable — the hover rule
     specifically is not honoured. background-size is, and it is verified live. */
  transition: background-size 1.5s cubic-bezier(.22, 1, .36, 1);
}}
{hover_scope} {{
  background-size: 106% 106%;
}}
/* RESTING: the brand overlay. #1a1a1a at 22% is not a taste choice — it is the
   value every collection banner and the science hero already use, so the menu and
   the banners read as one system.
   HOVER: the flat overlay lifts to zero and the picture brightens. Malcolm's call,
   2026-08-27.
   The bottom gradient is NOT part of that lift and stays constant. Without it the
   label would lose its contrast at exactly the moment the overlay disappears, and
   label contrast on this store is bought with a local scrim, never by flattening
   the whole photograph. */
{scrim_scope} {{
  content: "";
  position: absolute;
  inset: 0;
  z-index: -1;
  background:
    linear-gradient(to top,
      rgba(0, 0, 0, .58) 0%,
      rgba(0, 0, 0, .26) 32%,
      rgba(0, 0, 0, .04) 60%,
      rgba(0, 0, 0, 0) 78%),
    rgba(26, 26, 26, .22);
  transition: background .35s ease-in-out;
}}
{hover_after_scope} {{
  background:
    linear-gradient(to top,
      rgba(0, 0, 0, .58) 0%,
      rgba(0, 0, 0, .26) 32%,
      rgba(0, 0, 0, .04) 60%,
      rgba(0, 0, 0, 0) 78%),
    rgba(26, 26, 26, 0);
}}
{span_scope} {{
  color: #fff;
  text-shadow: 0 1px 8px rgba(0, 0, 0, .45);
  line-height: 1.25;
}}
/* Per-tile artwork. Unscoped by menu on purpose: an href appears in exactly one
   menu, and keeping these flat makes the list readable and easy to re-point. */
{images}
}}
{MARK_END}"""


def upsert_css(html):
    """Replace the marked block if present, else append before </style>."""
    css = build_css()
    if MARK_START in html and MARK_END in html:
        head = html.split(MARK_START)[0]
        tail = html.split(MARK_END, 1)[1]
        return head + css + tail
    idx = html.rfind("</style>")
    if idx == -1:
        raise SystemExit("brand_layout_css has no </style> to append before")
    return html[:idx] + "\n" + css + "\n" + html[idx:]


def blank_promo(block, label):
    """Clear the promo images on a tiled menu so no stray photo renders beside
    the tiles. Shop keeps its own."""
    changed = []
    for i in (1, 2, 3):
        for key in (f"image_{i}", f"image_heading_{i}", f"image_link_{i}"):
            if block["settings"].get(key):
                changed.append(key)
                block["settings"][key] = ""
    if changed:
        print(f"  {label}: cleared {', '.join(changed)}")
    return block


def new_block(menu_item):
    return {
        "type": "mega_menu",
        "settings": {
            "menu_item": menu_item,
            "layout": "horizontal_center",
            "submenu_style": "bold_heading",
            "image_1": "", "image_heading_1": "", "image_link_1": "",
            "image_text_color_1": "#ffffff",
            "image_2": "", "image_heading_2": "", "image_link_2": "",
            "image_text_color_2": "#ffffff",
            "image_3": "", "image_heading_3": "", "image_link_3": "",
            "image_text_color_3": "#ffffff",
            "product": "",
            "product_card_background": "",
            "product_card_text_color": "",
            "promo_content_layout": "grid",
            "stretch_promo": False,
            "drawer_link_image": "hide",
        },
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--restore")
    ap.add_argument("--key", help="asset key to restore into")
    args = ap.parse_args()

    e = env()
    store = e["SHOPIFY_SKINGENETIX_STORE"]
    tok = token(e)
    theme = next(t for t in call(store, tok, "themes.json")["themes"] if t["role"] == "main")
    tid = theme["id"]
    print(f"Store      : {store}")
    print(f"Live theme : {theme['name']} (id {tid})\n")

    if args.restore:
        if not args.key:
            sys.exit("--restore needs --key (sections/header-group.json or "
                     "sections/footer-group.json)")
        body = (ROOT / args.restore).read_text()
        call(store, tok, f"themes/{tid}/assets.json", "PUT",
             {"asset": {"key": args.key, "value": body}})
        print(f"RESTORED {args.key} from {args.restore}")
        return

    BACKUPS.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    # ---------------------------------------------------------------- header
    raw = call(store, tok, f"themes/{tid}/assets.json?asset[key]={HEADER_KEY}")["asset"]["value"]
    hb = BACKUPS / f"header-group-{stamp}.json"
    hb.write_text(raw)
    print(f"Backup     : {hb.relative_to(ROOT)}")
    print(f"Undo with  : python3 scripts/menu-image-tiles.py --restore "
          f"{hb.relative_to(ROOT)} --key {HEADER_KEY}\n")

    doc = json.loads(raw)
    header = doc["sections"]["header"]
    blocks = header["blocks"]
    order = header.get("block_order") or list(blocks.keys())

    print("Header blocks:")
    have = {b["settings"].get("menu_item", "").strip().lower(): bid
            for bid, b in blocks.items()}
    for menu_item, bid in (("Skin Solutions", "mega_menu_solutions"),
                           ("Support", "mega_menu_support")):
        if menu_item.strip().lower() in have:
            print(f"  {menu_item}: already has a mega menu block "
                  f"({have[menu_item.strip().lower()]}) — left alone")
            continue
        blocks[bid] = new_block(menu_item)
        order.append(bid)
        print(f"  {menu_item}: added block {bid} (was a plain text dropdown)")

    # Shop keeps its promo images; every tiled menu loses them.
    for bid, b in blocks.items():
        item = b["settings"].get("menu_item", "").strip().lower()
        if item == "shop":
            print("  Shop: left exactly as it is")
            continue
        blank_promo(b, b["settings"].get("menu_item", bid))

    # Menu order, not block order, drives the header; keep the blocks in the same
    # order as the menu so the theme editor reads sensibly.
    wanted = ["shop", "skin solutions", "scientific research", "discover", "support"]
    order.sort(key=lambda bid: wanted.index(
        blocks[bid]["settings"].get("menu_item", "").strip().lower())
        if blocks[bid]["settings"].get("menu_item", "").strip().lower() in wanted else 99)
    header["block_order"] = order
    print(f"  block_order: {' -> '.join(order)}")
    header_new = json.dumps(doc, indent=2)

    # ---------------------------------------------------------------- footer
    raw_f = call(store, tok, f"themes/{tid}/assets.json?asset[key]={FOOTER_KEY}")["asset"]["value"]
    fb = BACKUPS / f"footer-group-{stamp}.json"
    fb.write_text(raw_f)
    print(f"\nBackup     : {fb.relative_to(ROOT)}")
    print(f"Undo with  : python3 scripts/menu-image-tiles.py --restore "
          f"{fb.relative_to(ROOT)} --key {FOOTER_KEY}")

    fdoc = json.loads(raw_f)
    css_section = fdoc["sections"].get("brand_layout_css")
    if not css_section:
        sys.exit("footer-group.json has no brand_layout_css section to extend")
    before = css_section["settings"]["html"]
    css_section["settings"]["html"] = upsert_css(before)
    action = "replaced" if MARK_START in before else "appended"
    print(f"\nbrand_layout_css: tile CSS {action} "
          f"({len(css_section['settings']['html']) - len(before):+d} chars)")
    footer_new = json.dumps(fdoc, indent=2)

    if "{{" in css_section["settings"]["html"]:
        sys.exit("refusing to push: custom-html rejects '{{' in its html setting")

    print(f"\nTiles: {len(TILES)} across {len(SIGNATURES)} menus")

    if args.dry_run:
        (BACKUPS / f"header-group-PROPOSED-{stamp}.json").write_text(header_new)
        (BACKUPS / f"footer-group-PROPOSED-{stamp}.json").write_text(footer_new)
        print(f"\nDRY RUN — proposals in backups/, nothing pushed")
        return

    call(store, tok, f"themes/{tid}/assets.json", "PUT",
         {"asset": {"key": HEADER_KEY, "value": header_new}})
    print(f"\nPUSHED {HEADER_KEY}")
    call(store, tok, f"themes/{tid}/assets.json", "PUT",
         {"asset": {"key": FOOTER_KEY, "value": footer_new}})
    print(f"PUSHED {FOOTER_KEY}")


if __name__ == "__main__":
    main()
