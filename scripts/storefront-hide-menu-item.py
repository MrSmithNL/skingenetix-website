#!/usr/bin/env python3
"""Hide a navigation item from the storefront while leaving it in the Shopify menu.

    python3 scripts/storefront-hide-menu-item.py --url /pages/reviews --dry-run
    python3 scripts/storefront-hide-menu-item.py --url /pages/reviews
    python3 scripts/storefront-hide-menu-item.py --unhide

WHY THIS EXISTS
---------------
Shopify menus have no active/inactive flag — an item either exists in Navigation
or it does not. So "keep it in the back end but do not show it" cannot be done in
the menu itself; it has to be done in the theme. This adds a marked CSS block to
the sitewide `brand_layout_css` custom-html section that hides the matching item
in both places it renders: the desktop header nav and the mobile drawer.

Malcolm's call, 2026-08-29, after the item had been removed from the menu outright
and he asked for it back. The trade-off he is accepting, stated once and not
re-argued: a CSS-hidden link is still in the HTML, so crawlers still see the href.
`display: none` does remove it from the accessibility tree, so screen readers will
not announce it.

SCOPING
-------
Matched on the item's own href with `$=`, so a locale-prefixed URL
(/de/pages/reviews) still matches once more languages are published, and scoped to
the header nav and the drawer by their own containers. It deliberately does NOT
match the href anywhere else: /pages/reviews is also linked from the homepage
review slider's button and from templates/product.json, and the sitewide slider
CSS keys off `a[href$="/pages/reviews"]` inside `.media-with-text__item`. A rule
that hid every link to that page would take the slider's own CTA with it.

Author: Claude Code, 2026-08-29.
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
FOOTER_KEY = "sections/footer-group.json"
MARK_START = "/* === SGX HIDDEN MENU ITEMS START === */"
MARK_END = "/* === SGX HIDDEN MENU ITEMS END === */"


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
                sys.stderr.write(ex.read().decode(errors="replace")[:2000] + "\n")
                raise
            time.sleep(2 ** attempt)
    raise RuntimeError(path)


def build_css(urls):
    rules = []
    for u in urls:
        rules.append(f"""/* {u} — in the Shopify menu, not shown on the storefront. */
nav.header__link-list > ul > li:has(> a[href$="{u}"]),
nav.header__link-list > ul > li:has(> details > summary[data-url$="{u}"]) {{
  display: none !important;
}}
#header-sidebar-menu li:has(> a[href$="{u}"]),
#header-sidebar-menu li:has(> button[data-panel][data-url$="{u}"]) {{
  display: none !important;
}}""")
    return (f"{MARK_START}\n"
            "/* Storefront-hidden navigation items — Claude Code, 2026-08-29.\n"
            "   Shopify menus have no active/inactive flag, so an item that must stay in\n"
            "   Navigation but not appear on the site is hidden here instead.\n\n"
            "   Scoped to the header nav and the mobile drawer by their own containers,\n"
            "   and matched on the item's own href with $= so a locale-prefixed URL still\n"
            "   matches. NOT a blanket rule on the href: /pages/reviews is also the\n"
            "   homepage review slider's own CTA, and the sitewide slider CSS keys off\n"
            "   that same href — hiding every link to the page would take the slider's\n"
            "   button with it. */\n"
            + "\n".join(rules) + f"\n{MARK_END}")


def upsert(html, css):
    if MARK_START in html and MARK_END in html:
        head = html.split(MARK_START)[0]
        tail = html.split(MARK_END, 1)[1]
        return head + css + tail if css else (head.rstrip() + "\n" + tail.lstrip())
    if not css:
        return html
    idx = html.rfind("</style>")
    if idx == -1:
        raise SystemExit("brand_layout_css has no </style> to append before")
    return html[:idx] + "\n" + css + "\n" + html[idx:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", action="append", default=[],
                    help="menu item href to hide, e.g. /pages/reviews (repeatable)")
    ap.add_argument("--unhide", action="store_true", help="remove the block entirely")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not args.url and not args.unhide:
        sys.exit("give --url <href> (repeatable) or --unhide")

    e = env()
    store = e["SHOPIFY_SKINGENETIX_STORE"]
    tok = token(e)
    theme = next(t for t in call(store, tok, "themes.json")["themes"] if t["role"] == "main")
    tid = theme["id"]
    print(f"Store      : {store}")
    print(f"Live theme : {theme['name']} (id {tid})\n")

    raw = call(store, tok, f"themes/{tid}/assets.json?asset[key]={FOOTER_KEY}")["asset"]["value"]
    BACKUPS.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = BACKUPS / f"footer-group-{stamp}.json"
    backup.write_text(raw)
    print(f"Backup     : {backup.relative_to(ROOT)}")
    print(f"Undo with  : python3 scripts/menu-image-tiles.py --restore "
          f"{backup.relative_to(ROOT)} --key {FOOTER_KEY}\n")

    doc = json.loads(raw)
    sec = doc["sections"].get("brand_layout_css")
    if not sec:
        sys.exit("footer-group.json has no brand_layout_css section to extend")
    before = sec["settings"]["html"]
    sec["settings"]["html"] = upsert(before, "" if args.unhide else build_css(args.url))

    if args.unhide:
        print("Removing the hidden-items block — every menu item becomes visible again.")
    else:
        for u in args.url:
            print(f"Hiding from the storefront (still in the Shopify menu): {u}")
    print(f"brand_layout_css: {len(sec['settings']['html']) - len(before):+d} chars")

    if "{{" in sec["settings"]["html"]:
        sys.exit("refusing to push: custom-html rejects '{{' in its html setting")

    new = json.dumps(doc, indent=2)
    if args.dry_run:
        out = BACKUPS / f"footer-group-PROPOSED-{stamp}.json"
        out.write_text(new)
        print(f"\nDRY RUN — proposal at {out.relative_to(ROOT)}, nothing pushed")
        return

    call(store, tok, f"themes/{tid}/assets.json", "PUT",
         {"asset": {"key": FOOTER_KEY, "value": new}})
    print(f"\nPUSHED {FOOTER_KEY}")


if __name__ == "__main__":
    main()
