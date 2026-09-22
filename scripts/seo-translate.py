#!/usr/bin/env python3
"""Register translated SEO descriptions/titles to match an English change applied by seo-apply.py.

Author: Claude (Opus 5) for Malcolm Smith · 2026-09-22
Purpose: seo-apply.py writes English only. When the old translations are no longer accurate (e.g. they
repeat a claim that was just removed), the five locales must be updated in the same change — otherwise
Translate & Adapt keeps serving the old text, marked outdated.

    python3 scripts/seo-translate.py configs/seo-changes/<name>.translations.json [--key meta_description]

File: {"products"|"collections"|"pages": {handle: {"de": ..., "nl": ..., "fr": ..., "es": ..., "it": ...}}}
Each value is registered against the digest of the English value currently live, after the English
change has been applied and read back.
"""
import argparse, importlib.util, json, pathlib, sys, time

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOCALES = ["de", "nl", "fr", "es", "it"]
_s = importlib.util.spec_from_file_location("hu", ROOT / "scripts/hub-upgrade.py")
hu = importlib.util.module_from_spec(_s)
_argv, sys.argv = sys.argv, [sys.argv[0]]
_s.loader.exec_module(hu)
sys.argv = _argv
gql = hu.gql
Q = {"products": "products", "collections": "collections", "pages": "pages"}


def resource_id(kind, handle):
    n = gql('query($q:String!){ %s(first:1, query:$q){ nodes{ id handle } } }' % Q[kind], {"q": f"handle:{handle}"})[Q[kind]]["nodes"]
    if not n or n[0]["handle"] != handle:
        sys.exit(f"  ✗ {kind} not found: {handle}")
    return n[0]["id"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--key", default="meta_description")
    a = ap.parse_args()
    data = json.loads(pathlib.Path(a.file).read_text())
    for kind, items in data.items():
        for handle, vals in items.items():
            rid = resource_id(kind, handle)
            tc = gql('query($id:ID!){ translatableResource(resourceId:$id){ translatableContent{ key value digest } } }',
                     {"id": rid})["translatableResource"]["translatableContent"]
            c = next((x for x in tc if x["key"] == a.key), None)
            if not c:
                sys.exit(f"  ✗ {handle}: no translatable {a.key}")
            r = gql('mutation($id:ID!,$t:[TranslationInput!]!){ translationsRegister(resourceId:$id, translations:$t){ userErrors{ message } } }',
                    {"id": rid, "t": [{"locale": l, "key": a.key, "value": vals[l], "translatableContentDigest": c["digest"]} for l in LOCALES]})
            errs = r["translationsRegister"]["userErrors"]
            print(f"  {'✗ ' + str(errs) if errs else '✓'} {kind[:-1]} {handle:<45} {a.key} × 5  (English: {c['value'][:60]}…)")
            time.sleep(0.3)
    return 0


if __name__ == "__main__":
    sys.exit(main())
