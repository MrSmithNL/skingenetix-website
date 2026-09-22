#!/usr/bin/env python3
# Author: Claude (Opus 5) for Malcolm Smith · 2026-09-22 — one-off: undo the column split made by
# configs/menus/main-menu-science-2026-09-22.json and keep ONLY the label change Learn → Science.
"""Restore the pre-change main menu exactly, except the Learn label becomes Science (Malcolm: do not split)."""
import sys, importlib.util, pathlib, json, glob
ROOT = pathlib.Path("/Users/malcolmsmith/Claude Code/Projects/skingenetix-website")
s = importlib.util.spec_from_file_location("ma", ROOT / "scripts/menu-apply.py"); ma = importlib.util.module_from_spec(s)
sys.argv = [sys.argv[0]]; s.loader.exec_module(ma)
gql, hu = ma.gql, ma.hu
bk = json.loads(pathlib.Path(sorted(glob.glob(str(ROOT / "backups/menu-main-menu-science-2026-09-22-*.json")))[0]).read_text())
old = bk["menu"]
SCI = {"en": "Science", "de": "Wissenschaft", "nl": "Wetenschap", "fr": "Science", "es": "Ciencia", "it": "Scienza"}


def live_ids(items, acc):
    for i in items:
        acc.add(i["id"]); live_ids(i.get("items", []), acc)
    return acc
now = live_ids(ma.load_menu("main-menu")["items"], set())

recreated = {}
def prep(it):
    d = ma.to_input(it)
    def fix(x, src):
        if x.get("id") not in now:
            recreated[src["title"]] = src["id"]; x.pop("id", None)
        for xc, sc in zip(x["items"], src.get("items", [])):
            fix(xc, sc)
    fix(d, it)
    if it["title"] == "Learn":
        d["title"] = "Science"
    return d

items = [prep(i) for i in old["items"]]
r = gql('mutation($id:ID!,$t:String!,$h:String!,$i:[MenuItemUpdateInput!]!){ menuUpdate(id:$id,title:$t,handle:$h,items:$i)'
        '{ menu{ items{ id title items{ id title } } } userErrors{ field message } } }',
        {"id": old["id"], "t": old["title"], "h": old["handle"], "i": items})["menuUpdate"]
if r["userErrors"]:
    sys.exit(r["userErrors"])
live = r["menu"]["items"]
print("menu:", [(i["title"], [c["title"] for c in i["items"]]) for i in live])

def restore_link(new_id, old_id, en_title):
    trs = bk["link_translations"].get(old_id, {})
    vals = {"en": en_title}
    for l in ma.LOCALES:
        v = next((t["value"] for t in trs.get(l, []) if t["key"] == "title"), None)
        if v: vals[l] = v
    if len(vals) == 6:
        ma.register(f"gid://shopify/Link/{new_id.rsplit('/', 1)[1]}", "title", vals)
        print(f"  translations restored: {en_title} → {vals}")

# recreated items (Discover) and the relabelled acetyl leaf get their original translations back
for top in live:
    for it in [top] + top["items"]:
        if it["title"] in recreated:
            restore_link(it["id"], recreated[it["title"]], it["title"])
learn_old = next(i for i in old["items"] if i["title"] == "Learn")
acet_old = next(c for c in learn_old["items"] if "Acetyl" in c["title"])
restore_link(acet_old["id"], acet_old["id"], acet_old["title"])
sci = next(i for i in live if i["title"] == "Science")
ma.register(f"gid://shopify/Link/{sci['id'].rsplit('/', 1)[1]}", "title", SCI)

# header: the original file, with only the research block's label changed
hdr, j = hu.split(bk["header_raw"])
j["sections"]["header"]["blocks"]["mega_menu_research"]["settings"]["menu_item"] = "Science"
hu.upload(ma.HEADER, hdr, j)
ma.register(ma.HEADER_RID, f"section.{ma.HEADER}.header.mega_menu_research.menu_item", SCI)
disc = {"en": "Discover"}
for l in ma.LOCALES:
    disc[l] = next(t["value"] for t in bk["header_translations"][l] if "mega_menu_discover.menu_item" in t["key"])
ma.register(ma.HEADER_RID, f"section.{ma.HEADER}.header.mega_menu_discover.menu_item", disc)
print("  header restored, research label = Science, discover =", disc)
