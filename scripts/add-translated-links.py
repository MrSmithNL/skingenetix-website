#!/usr/bin/env python3
"""Give translated pages the in-prose links their English already has.

Author: Claude (Opus 5) for Malcolm Smith · 2026-09-22
Purpose: the Phase 1 prose links were written into English only, so /de /nl /fr /es /it served the same
paragraphs with no link (scripts/link-audit.py, 2026-09-22). Driven by
configs/link-changes/translated-prose-links-2026-09-22.json.

    python3 scripts/add-translated-links.py <config>            # dry run
    python3 scripts/add-translated-links.py <config> --apply

Per item: if the English paragraph is being improved (`en` != `old`), the English is updated first; then each
locale's current translation gets the locale's paragraph appended — unless it already links to the target —
and is registered against the digest of the English now live. Backups in backups/translated-links-<stamp>.json.
"""
import argparse, datetime as dt, importlib.util, json, pathlib, sys, time

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOCALES = ["de", "nl", "fr", "es", "it"]
_s = importlib.util.spec_from_file_location("hu", ROOT / "scripts/hub-upgrade.py")
hu = importlib.util.module_from_spec(_s)
_argv, sys.argv = sys.argv, [sys.argv[0]]
_s.loader.exec_module(hu)
sys.argv = _argv
gql = hu.gql
TID = hu.THEME.rsplit("/", 1)[1]


def target(it):
    kind, ident = it["resource"].split(":", 1) if it["resource"].startswith("template:") else ("collection", it["resource"].split("/")[1])
    if kind == "template":
        return {"rid": f"gid://shopify/OnlineStoreThemeJsonTemplate/{ident}?theme_id={TID}",
                "base": f"section.{ident}.json.{it['key']}", "file": f"templates/{ident}.json"}
    return {"rid": f"gid://shopify/Collection/{ident}", "base": "body_html", "file": None}


def content(rid, base):
    tc = gql('query($id:ID!){ translatableResource(resourceId:$id){ translatableContent{ key value digest } } }',
             {"id": rid})["translatableResource"]["translatableContent"]
    return next(c for c in tc if c["key"].split(":")[0] == base)


def translation(rid, key, loc):
    tr = gql('query($id:ID!,$l:String!){ translatableResource(resourceId:$id){ translations(locale:$l){ key value } } }',
             {"id": rid, "l": loc})["translatableResource"]["translations"]
    return next((t["value"] for t in tr if t["key"] == key), None)


def write_en(it, t, new_value):
    if t["file"]:
        hdr, j = hu.split(hu.read_file(t["file"]))
        sec, blk, setting = it["key"].split(".")
        j["sections"][sec]["blocks"][blk]["settings"][setting] = new_value
        hu.upload(t["file"], hdr, j)
    else:
        r = gql('mutation($c:CollectionInput!){ collectionUpdate(input:$c){ userErrors{ message } } }',
                {"c": {"id": t["rid"], "descriptionHtml": new_value}})["collectionUpdate"]
        if r["userErrors"]:
            raise RuntimeError(r["userErrors"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    items = json.loads(pathlib.Path(a.config).read_text())["items"]
    backup, plan = [], []
    for it in items:
        t = target(it)
        c = content(t["rid"], t["base"])
        if it["old"] not in c["value"]:
            sys.exit(f"  ✗ {it['resource']} {it['key']}: English paragraph not found live — config is stale")
        new_en = c["value"].replace(it["old"], it["en"])
        locs = {}
        for loc in LOCALES:
            cur = translation(t["rid"], c["key"], loc)
            if cur is None:
                continue
            locs[loc] = cur if it["target"] in cur else cur.rstrip() + it[loc]
        backup.append({"resource": it["resource"], "key": c["key"], "en": c["value"],
                       **{l: translation(t["rid"], c["key"], l) for l in LOCALES}})
        plan.append((it, t, c, new_en, locs))
        print(f"  {it['resource']:<42} {it['key']:<30} English {'changed' if new_en != c['value'] else 'same   '} · "
              f"link added in {sum(1 for l, v in locs.items() if it['target'] not in (translation(t['rid'], c['key'], l) or ''))}/5 locales")
    if not a.apply:
        print("  dry run — nothing written.")
        return 0
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    (ROOT / f"backups/translated-links-{stamp}.json").write_text(json.dumps(backup, ensure_ascii=False, indent=1))
    for it, t, c, new_en, locs in plan:
        if new_en != c["value"]:
            write_en(it, t, new_en)
        for _ in range(8):
            live = content(t["rid"], t["base"])
            if live["value"] == new_en:
                break
            time.sleep(4)
        else:
            raise RuntimeError(f"{it['resource']}: English never updated")
        r = gql('mutation($id:ID!,$t:[TranslationInput!]!){ translationsRegister(resourceId:$id, translations:$t){ userErrors{ message } } }',
                {"id": t["rid"], "t": [{"locale": l, "key": live["key"], "value": v, "translatableContentDigest": live["digest"]}
                                        for l, v in locs.items()]})["translationsRegister"]
        print(f"  {'✗ ' + str(r['userErrors']) if r['userErrors'] else '✓'} {it['resource']:<42} {it['key']}")
    print(f"  backup {stamp}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
