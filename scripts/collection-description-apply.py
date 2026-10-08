#!/usr/bin/env python3
"""Apply a six-language collection description from a config, with a backup and a verify.

Author: Claude (Fable 5.1) for Malcolm Smith · 2026-10-08
Why: the Creams & Moisturizers description ended in "Coming soon." in six languages while five creams
were live (found by the 2026-10-08 per-page teardown). A collection description is a translatable
resource, so an English-only edit would leave five locales serving the old sentence (memory:
an-outdated-translation-is-still-served). This script changes the English and registers the five
translations against the new digest in one run.

    python3 scripts/collection-description-apply.py configs/copy/<name>.json            # dry run
    python3 scripts/collection-description-apply.py configs/copy/<name>.json --apply
    python3 scripts/collection-description-apply.py configs/copy/<name>.json --verify-live

Config: {"collection": <handle>, "field": "body_html", "before": {locale: text}, "after": {locale: text}}.
The run refuses to start if the live values differ from "before" (the config was built from a stale read).
Backup: backups/collection-description-<handle>-<stamp>.json. Undo: swap before/after and --apply.
"""
import argparse, datetime as dt, importlib.util, json, pathlib, sys, time

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOCALES = ["de", "nl", "fr", "es", "it"]


def _load(name, path):
    s = importlib.util.spec_from_file_location(name, ROOT / path)
    m = importlib.util.module_from_spec(s)
    argv, sys.argv = sys.argv, [sys.argv[0]]
    s.loader.exec_module(m)
    sys.argv = argv
    return m


hu = _load("hu", "scripts/hub-upgrade.py")
gql = hu.gql


def live(handle, field):
    c = gql('query($h:String!){ collectionByHandle(handle:$h){ id descriptionHtml } }', {"h": handle})["collectionByHandle"]
    out = {"id": c["id"], "en": c["descriptionHtml"], "digest": None, "locales": {}}
    for loc in LOCALES:
        r = gql('query($id:ID!,$l:String!){ translatableResource(resourceId:$id){ translatableContent{ key value digest } '
                'translations(locale:$l){ key value outdated } } }', {"id": c["id"], "l": loc})["translatableResource"]
        en = next(x for x in r["translatableContent"] if x["key"] == field)
        out["digest"] = en["digest"]
        t = next((x for x in r["translations"] if x["key"] == field), None)
        out["locales"][loc] = t["value"] if t else None
        time.sleep(0.3)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--verify-live", action="store_true")
    a = ap.parse_args()
    cfg = json.loads(pathlib.Path(a.config).read_text())
    handle, field = cfg["collection"], cfg["field"]
    cur = live(handle, field)
    want = cfg["after"] if a.verify_live else cfg["before"]
    diffs = [l for l in ["en"] + LOCALES if (cur["en"] if l == "en" else cur["locales"][l]) != want[l]]
    if a.verify_live:
        print("  ✓ live matches 'after' in six languages" if not diffs else f"  ✗ differs in {diffs}")
        return 1 if diffs else 0
    if diffs:
        sys.exit(f"  ✗ live values differ from the config's 'before' in {diffs}; re-read before applying")
    print(f"  {handle}.{field}: six languages match 'before'")
    if not a.apply:
        print("  dry run; add --apply")
        return 0
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    (ROOT / "backups" / f"collection-description-{handle}-{stamp}.json").write_text(json.dumps(cur, indent=1, ensure_ascii=False))
    r = gql('mutation($c:CollectionInput!){ collectionUpdate(input:$c){ userErrors{ field message } } }',
            {"c": {"id": cur["id"], "descriptionHtml": cfg["after"]["en"]}})["collectionUpdate"]
    if r["userErrors"]:
        sys.exit(f"  ✗ collectionUpdate: {r['userErrors']}")
    time.sleep(1)
    fresh = live(handle, field)
    trans = [{"locale": l, "key": field, "value": cfg["after"][l], "translatableContentDigest": fresh["digest"]} for l in LOCALES]
    r = gql('mutation($id:ID!,$t:[TranslationInput!]!){ translationsRegister(resourceId:$id, translations:$t){ userErrors{ field message } } }',
            {"id": cur["id"], "t": trans})["translationsRegister"]
    if r["userErrors"]:
        sys.exit(f"  ✗ translationsRegister: {r['userErrors']}")
    time.sleep(1)
    after = live(handle, field)
    bad = [l for l in LOCALES if after["locales"][l] != cfg["after"][l]] + (["en"] if after["en"] != cfg["after"]["en"] else [])
    print("  ✓ applied and verified in six languages" if not bad else f"  ✗ verify failed in {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
