#!/usr/bin/env python3
"""Remove a top-level item from a Shopify navigation menu, reversibly.

    python3 scripts/menu-item-hide.py --menu main-menu --item Reviews --dry-run
    python3 scripts/menu-item-hide.py --menu main-menu --item Reviews
    python3 scripts/menu-item-hide.py --restore backups/menu-main-menu-<stamp>.json

WHY THE MENU AND NOT CSS
------------------------
Hiding the link with `display: none` would leave it in the markup: crawlers still
follow it, and it would still be read out by anything that ignores CSS. Taking it
out of the menu removes it from the desktop nav and the mobile drawer at once, and
is what the Shopify admin itself would do.

WHY THIS IS SAFE TO DO WHOLESALE
--------------------------------
`menuUpdate` replaces the whole item list, so every item is re-submitted. Two
things make that harmless here, and both were checked before writing this:

  * MenuItemUpdateInput accepts `id`, so every surviving item is sent back with
    its existing id and keeps it. Nothing is recreated.
  * The store publishes only `en` and the menu carries no translations, so there
    is no Translate & Adapt content keyed to these items to lose. If a second
    locale is ever published, re-check that before running this again.

The page itself is untouched. /pages/reviews stays published and stays linked from
the homepage review slider's "See All Customer Reviews" button and from
templates/product.json — and the sitewide slider CSS scopes on
`a[href$="/pages/reviews"]` inside that slider, which this does not touch.

Author: Claude Code, 2026-08-29.
"""
import argparse
import json
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "2025-01"
BACKUPS = ROOT / "backups"

TREE = """
query($handle:String!){
  menus(first:1, query:$handle){
    nodes{
      id handle title
      items{ id title type url resourceId tags
        items{ id title type url resourceId tags
          items{ id title type url resourceId tags } } }
    }
  }
}"""

UPDATE = """
mutation($id:ID!, $title:String!, $handle:String!, $items:[MenuItemUpdateInput!]!){
  menuUpdate(id:$id, title:$title, handle:$handle, items:$items){
    menu{ id handle items{ id title } }
    userErrors{ field message }
  }
}"""


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


def to_input(node, keep_ids=True):
    """A fetched item -> a MenuItemUpdateInput. `url` and `resourceId` are mutually
    exclusive per type: sending a url on a PAGE/COLLECTION item is rejected."""
    out = {"title": node["title"], "type": node["type"]}
    if keep_ids and node.get("id"):
        out["id"] = node["id"]
    if node.get("resourceId"):
        out["resourceId"] = node["resourceId"]
    elif node.get("url"):
        out["url"] = node["url"]
    if node.get("tags"):
        out["tags"] = node["tags"]
    kids = node.get("items") or []
    if kids:
        out["items"] = [to_input(k, keep_ids) for k in kids]
    return out


def show(items, indent=2):
    for i in items:
        print(" " * indent + f"- {i['title']}  ({i['type']}) {i.get('url') or ''}")
        for k in i.get("items") or []:
            print(" " * (indent + 4) + f"- {k['title']}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--menu", default="main-menu")
    ap.add_argument("--item", help="exact top-level title to remove (case-insensitive)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--restore", help="a backup file written by a previous run")
    args = ap.parse_args()

    e = env()
    store = e["SHOPIFY_SKINGENETIX_STORE"]
    tok = token(e)
    print(f"Store : {store}\n")

    if args.restore:
        saved = json.loads((ROOT / args.restore).read_text())
        # Restoring re-creates the removed item, so it has no id to preserve; the
        # survivors keep theirs.
        items = [to_input(i) for i in saved["items"]]
        data = gql(store, tok, UPDATE, {"id": saved["id"], "title": saved["title"],
                                        "handle": saved["handle"], "items": items})
        errs = data["menuUpdate"]["userErrors"]
        if errs:
            sys.exit(f"menuUpdate: {errs}")
        print(f"RESTORED {saved['handle']} from {args.restore}")
        show(data["menuUpdate"]["menu"]["items"])
        return

    if not args.item:
        sys.exit("--item is required unless --restore is given")

    nodes = gql(store, tok, TREE, {"handle": f"handle:{args.menu}"})["menus"]["nodes"]
    if not nodes:
        sys.exit(f"no menu with handle {args.menu}")
    menu = nodes[0]

    print(f"Menu  : {menu['handle']} ({menu['title']})")
    print("Before:")
    show(menu["items"])

    target = args.item.strip().lower()
    keep = [i for i in menu["items"] if i["title"].strip().lower() != target]
    if len(keep) == len(menu["items"]):
        sys.exit(f"\nno top-level item titled {args.item!r} — nothing removed")

    BACKUPS.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = BACKUPS / f"menu-{menu['handle']}-{stamp}.json"
    backup.write_text(json.dumps(menu, indent=2))
    print(f"\nBackup    : {backup.relative_to(ROOT)}")
    print(f"Undo with : python3 scripts/menu-item-hide.py --restore "
          f"{backup.relative_to(ROOT)}")

    removed = [i for i in menu["items"] if i["title"].strip().lower() == target]
    print(f"\nRemoving  : {', '.join(i['title'] for i in removed)}")
    print("After:")
    show(keep)

    if args.dry_run:
        print("\nDRY RUN — nothing pushed")
        return

    data = gql(store, tok, UPDATE, {"id": menu["id"], "title": menu["title"],
                                    "handle": menu["handle"],
                                    "items": [to_input(i) for i in keep]})
    errs = data["menuUpdate"]["userErrors"]
    if errs:
        sys.exit(f"menuUpdate: {errs}")
    live = data["menuUpdate"]["menu"]["items"]
    print(f"\nPUSHED — menu now has {len(live)} top-level items: "
          f"{', '.join(i['title'] for i in live)}")


if __name__ == "__main__":
    main()
