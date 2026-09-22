#!/usr/bin/env python3
"""Restructure a top-level main-menu item and its Impact mega-menu — all six languages in one change.

Author: Claude (Opus 5) for Malcolm Smith · 2026-09-22
Purpose: rename "Learn" to "Science", fold "Discover" into it, and group the submenu into columns.

    python3 scripts/menu-apply.py configs/menus/<plan>.json            # dry run: prints the new tree
    python3 scripts/menu-apply.py configs/menus/<plan>.json --apply
    python3 scripts/menu-apply.py configs/menus/<plan>.json --rollback

Why it works this way:
  * Impact attaches a mega-menu by matching the header block's `menu_item` setting to the menu item's
    TRANSLATED title. The label and the block setting must change together in every locale, or the
    mega-menu silently vanishes in that language (it was broken in 4 locales until 2026-09-22).
  * Menu items keep their IDs where the plan reuses them (matched by URL), so their existing
    translations survive; every title the plan sets is translated in the same change.
  * menuUpdate replaces the whole tree, so the full previous menu, header group and all their
    translations are snapshotted to backups/ first.
"""
import argparse, datetime as dt, glob, importlib.util, json, pathlib, sys, time

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOCALES = ["de", "nl", "fr", "es", "it"]
_s = importlib.util.spec_from_file_location("hu", ROOT / "scripts/hub-upgrade.py")
hu = importlib.util.module_from_spec(_s)
_argv, sys.argv = sys.argv, [sys.argv[0]]
_s.loader.exec_module(hu)
sys.argv = _argv
gql = hu.gql
HEADER = "sections/header-group.json"
HEADER_RID = f"gid://shopify/OnlineStoreThemeSectionGroup/header-group?theme_id={hu.THEME.rsplit('/', 1)[1]}"
ITEM_FIELDS = "id title url type resourceId tags"


def load_menu(handle):
    q = '{ menus(first:20){ nodes{ id handle title items{ %s items{ %s items{ %s } } } } } }' % ((ITEM_FIELDS,) * 3)
    return next(m for m in gql(q)["menus"]["nodes"] if m["handle"] == handle)


def tr_all(rid):
    out = {}
    for l in LOCALES:
        out[l] = gql('query($id:ID!,$l:String!){ translatableResource(resourceId:$id){ translations(locale:$l){ key value } } }',
                     {"id": rid, "l": l})["translatableResource"]["translations"]
    return out


def register(rid, key_base, values):
    for _ in range(8):
        tc = gql('query($id:ID!){ translatableResource(resourceId:$id){ translatableContent{ key value digest } } }',
                 {"id": rid})["translatableResource"]["translatableContent"]
        c = next((x for x in tc if x["key"].split(":")[0] == key_base and x["value"] == values["en"]), None)
        if c:
            break
        time.sleep(4)
    else:
        raise RuntimeError(f"{rid} {key_base}: live value never became {values['en']!r}")
    r = gql('mutation($id:ID!,$t:[TranslationInput!]!){ translationsRegister(resourceId:$id, translations:$t){ userErrors{ message } } }',
            {"id": rid, "t": [{"locale": l, "key": c["key"], "value": values[l], "translatableContentDigest": c["digest"]}
                              for l in LOCALES]})["translationsRegister"]
    if r["userErrors"]:
        raise RuntimeError(r["userErrors"])


def to_input(it):
    d = {"id": it["id"], "title": it["title"], "type": it["type"], "url": it["url"], "tags": it.get("tags") or [],
         "items": [to_input(c) for c in it.get("items", [])]}
    if it.get("resourceId"):
        d["resourceId"] = it["resourceId"]
    return d


def build(plan, menu):
    """Return (new top-level item list as MenuItemUpdateInput, [(path, titles-dict)] to translate)."""
    top = {i["title"]: i for i in menu["items"]}
    src = top[plan["replace"]["match_title"]]
    pool = {}                                  # url -> existing leaf, from the replaced + removed items
    for t in [src] + [top[x] for x in plan.get("remove", [])]:
        for c in t["items"]:
            pool.setdefault(c["url"], c)
            for g in c["items"]:
                pool.setdefault(g["url"], g)
    todo = []

    def node(spec, path):
        if "match_url" in spec:
            base = dict(pool.pop(spec["match_url"]))
            base["items"] = []
        else:
            base = {"id": None, "type": "HTTP", "url": spec.get("url", "#"), "resourceId": None, "tags": []}
        if "title" in spec:
            base["title"] = spec["title"]["en"]
            todo.append((path + [spec["title"]["en"]], spec["title"]))
        base["items"] = [node(c, path + [base["title"]]) for c in spec.get("children", [])]
        return base

    w = plan["replace"]["with"]
    new_top = {**src, "title": w["title"]["en"], "url": w.get("url", src["url"]), "items": []}
    todo.append(([w["title"]["en"]], w["title"]))
    new_top["items"] = [node(c, [w["title"]["en"]]) for c in w["children"]]
    items = []
    for i in menu["items"]:
        if i["title"] in plan.get("remove", []):
            continue
        items.append(new_top if i is src else i)
    if pool:
        print(f"  note: not placed in the new tree (dropped): {sorted(pool)}")
    return items, todo


def show(items, depth=0):
    for i in items:
        print(f"  {'   ' * depth}- {i['title']}  {i['url']}{'  (new)' if not i.get('id') else ''}")
        show(i.get("items", []), depth + 1)


def strip_ids(d):
    if not d.get("id"):
        d.pop("id", None)
    for c in d.get("items", []):
        strip_ids(c)
    return d


def find(items, path):
    for i in items:
        if i["title"] == path[0]:
            return i if len(path) == 1 else find(i.get("items", []), path[1:])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plan")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--rollback", action="store_true")
    a = ap.parse_args()
    plan = json.loads(pathlib.Path(a.plan).read_text())
    tag = pathlib.Path(a.plan).stem

    if a.rollback:
        bk = json.loads(pathlib.Path(sorted(glob.glob(str(ROOT / f"backups/menu-{tag}-*.json")))[-1]).read_text())
        m = bk["menu"]
        r = gql('mutation($id:ID!,$t:String!,$h:String!,$i:[MenuItemUpdateInput!]!){ menuUpdate(id:$id,title:$t,handle:$h,items:$i){ userErrors{ message } } }',
                {"id": m["id"], "t": m["title"], "h": m["handle"], "i": [strip_ids(to_input(i)) for i in m["items"]]})
        print("  menu restored", r["menuUpdate"]["userErrors"] or "✓")
        hdr, j = hu.split(bk["header_raw"])
        hu.upload(HEADER, hdr, j)
        print("  header restored — re-register header/menu translations from the backup file if any locale label is wrong")
        return 0

    menu = load_menu(plan["menu"])
    items, todo = build(plan, menu)
    show(items)
    if not a.apply:
        print("  dry run — nothing written.")
        return 0

    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    links = {}

    def collect(its):
        for i in its:
            links[i["id"]] = tr_all(f"gid://shopify/Link/{i['id'].rsplit('/', 1)[1]}")
            collect(i.get("items", []))
    collect(menu["items"])
    (ROOT / f"backups/menu-{tag}-{stamp}.json").write_text(json.dumps(
        {"menu": menu, "link_translations": links, "header_raw": hu.read_file(HEADER),
         "header_translations": tr_all(HEADER_RID)}, ensure_ascii=False, indent=1))

    r = gql('mutation($id:ID!,$t:String!,$h:String!,$i:[MenuItemUpdateInput!]!){ menuUpdate(id:$id,title:$t,handle:$h,items:$i)'
            '{ menu{ items{ id title items{ id title items{ id title } } } } userErrors{ field message } } }',
            {"id": menu["id"], "t": menu["title"], "h": menu["handle"], "i": [strip_ids(to_input(i)) for i in items]})["menuUpdate"]
    if r["userErrors"]:
        raise RuntimeError(r["userErrors"])
    live = r["menu"]["items"]
    for path, titles in todo:
        it = find(live, path)
        register(f"gid://shopify/Link/{it['id'].rsplit('/', 1)[1]}", "title", titles)
        print(f"  ✓ {' › '.join(path):<45} 6 languages")

    h = plan["header"]
    hdr, j = hu.split(hu.read_file(HEADER))
    sec = j["sections"][h["section"]]
    sec["blocks"][h["block"]]["settings"]["menu_item"] = h["menu_item"]["en"]
    for b in h.get("remove_blocks", []):
        sec["blocks"].pop(b, None)
        sec["block_order"] = [x for x in sec["block_order"] if x != b]
    hu.upload(HEADER, hdr, j)
    register(HEADER_RID, f"section.{HEADER}.{h['section']}.{h['block']}.menu_item", h["menu_item"])
    print(f"  ✓ header {h['block']}.menu_item = {h['menu_item']} (backup {stamp})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
