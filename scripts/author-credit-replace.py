#!/usr/bin/env python3
"""Replace the named writer credit with the team credit on the eight study articles and the study metaobjects.

Author: Claude (Fable 5.1) for Malcolm Smith · 2026-10-08
Why: Malcolm, 2026-10-08: "Remove my name from all pages as the writer. And replace with a more generic term."
The inventory (scratchpad author-credit-inventory.md) found the name in: the Shopify `author.name` of the eight
clinical-studies articles and their hidden drafts (Shopify's own Article JSON-LD emits it), and the `jsonld` field of
the `study` metaobjects (8 live, 8 `-draft` twins, with five locale translations each). The hub bylines are handled
separately through six-language set-only specs. The generators were changed in the same commit.

    python3 scripts/author-credit-replace.py              # dry run: lists every hit
    python3 scripts/author-credit-replace.py --apply      # backs up to backups/author-credit-<stamp>.json, then writes

Replacement: visible/platform author name -> "Skingenetix Research Team"; JSON-LD author object ->
{"@type": "Organization", "name": "Skingenetix", "url": "https://www.skingenetix.com"}. The reviewer (Dr Bodde) and the
research credit (the study's own authors, ADR-2026-10-02-U) are untouched.
"""
import argparse, datetime as dt, importlib.util, json, pathlib, re, sys, time

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOCALES = ["de", "nl", "fr", "es", "it"]
TEAM = "Skingenetix Research Team"
ORG = {"@type": "Organization", "name": "Skingenetix", "url": "https://www.skingenetix.com"}


def _load(name, path):
    s = importlib.util.spec_from_file_location(name, ROOT / path)
    m = importlib.util.module_from_spec(s)
    argv, sys.argv = sys.argv, [sys.argv[0]]
    s.loader.exec_module(m)
    sys.argv = argv
    return m


gql = _load("hu", "scripts/hub-upgrade.py").gql


def swap_author(jsonld_text):
    """Replace every JSON-LD author object naming the person with the organisation; return (new_text, count)."""
    # the study field wraps its JSON in a <script type="application/ld+json"> tag (verified 2026-10-08)
    m = re.match(r"^(\s*<script[^>]*>)(.*)(</script>\s*)$", jsonld_text, re.S)
    pre, body, post = (m.group(1), m.group(2), m.group(3)) if m else ("", jsonld_text, "")
    try:
        data = json.loads(body)
    except Exception:
        return jsonld_text, 0
    n = 0

    def walk(o):
        nonlocal n
        if isinstance(o, dict):
            for k, v in list(o.items()):
                if k in ("author", "creator") and isinstance(v, dict) and "Malcolm" in json.dumps(v):
                    o[k] = dict(ORG); n += 1
                else:
                    walk(v)
        elif isinstance(o, list):
            for x in o:
                walk(x)
    walk(data)
    return pre + json.dumps(data, ensure_ascii=False) + post, n


def articles():
    out = []
    after = None
    while True:
        r = gql('query($a:String){ articles(first:50, after:$a){ nodes{ id handle title author{ name } blog{ handle } } pageInfo{ hasNextPage endCursor } } }', {"a": after})["articles"]
        out += r["nodes"]
        if not r["pageInfo"]["hasNextPage"]:
            break
        after = r["pageInfo"]["endCursor"]
    return [a for a in out if "Malcolm" in (a["author"] or {}).get("name", "")]


def studies():
    out = []
    after = None
    while True:
        r = gql('query($a:String){ metaobjects(type:"study", first:50, after:$a){ nodes{ id handle fields{ key value } } pageInfo{ hasNextPage endCursor } } }', {"a": after})["metaobjects"]
        out += r["nodes"]
        if not r["pageInfo"]["hasNextPage"]:
            break
        after = r["pageInfo"]["endCursor"]
    hits = []
    for m in out:
        f = next((x for x in m["fields"] if x["key"] == "jsonld"), None)
        if f and f["value"] and "Malcolm" in f["value"]:
            hits.append({"id": m["id"], "handle": m["handle"], "jsonld": f["value"]})
    return hits


def study_translations(mid):
    r = gql('query($id:ID!){ translatableResource(resourceId:$id){ translatableContent{ key value digest } } }', {"id": mid})["translatableResource"]
    en = next((c for c in r["translatableContent"] if c["key"] == "jsonld"), None)
    per = {}
    for loc in LOCALES:
        t = gql('query($id:ID!,$l:String!){ translatableResource(resourceId:$id){ translations(locale:$l){ key value } } }', {"id": mid, "l": loc})["translatableResource"]["translations"]
        v = next((x["value"] for x in t if x["key"] == "jsonld"), None)
        if v and "Malcolm" in v:
            per[loc] = v
        time.sleep(0.2)
    return en, per


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    arts = articles()
    studs = studies()
    print(f"  articles with the name as author: {len(arts)}")
    for x in arts:
        print(f"    {x['blog']['handle']:<26} {x['handle']}")
    print(f"  study entries with the name in jsonld: {len(studs)}")
    plan = []
    for s in studs:
        en, per = study_translations(s["id"])
        new_en, n = swap_author(s["jsonld"])
        plan.append({**s, "new": new_en, "swaps": n, "locales": {l: swap_author(v)[0] for l, v in per.items()}, "digest": en["digest"] if en else None})
        print(f"    {s['handle']:<52} author objects: {n}  locales to re-register: {sorted(per)}")
    if not a.apply:
        print("  dry run; add --apply")
        return 0
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    (ROOT / "backups" / f"author-credit-{stamp}.json").write_text(json.dumps({"articles": arts, "studies": [{k: v for k, v in p.items() if k != 'new'} for p in plan]}, indent=1, ensure_ascii=False))
    for x in arts:
        r = gql('mutation($id:ID!,$a:ArticleUpdateInput!){ articleUpdate(id:$id, article:$a){ userErrors{ field message } } }', {"id": x["id"], "a": {"author": {"name": TEAM}}})["articleUpdate"]
        if r["userErrors"]:
            sys.exit(f"  ✗ {x['handle']}: {r['userErrors']}")
        time.sleep(0.3)
    print(f"  ✓ {len(arts)} article authors -> {TEAM}")
    for p in plan:
        r = gql('mutation($id:ID!,$m:MetaobjectUpdateInput!){ metaobjectUpdate(id:$id, metaobject:$m){ userErrors{ field message } } }', {"id": p["id"], "m": {"fields": [{"key": "jsonld", "value": p["new"]}]}})["metaobjectUpdate"]
        if r["userErrors"]:
            sys.exit(f"  ✗ {p['handle']}: {r['userErrors']}")
        time.sleep(0.5)
        if p["locales"]:
            fresh = gql('query($id:ID!){ translatableResource(resourceId:$id){ translatableContent{ key digest } } }', {"id": p["id"]})["translatableResource"]["translatableContent"]
            digest = next(c["digest"] for c in fresh if c["key"] == "jsonld")
            t = [{"locale": l, "key": "jsonld", "value": v, "translatableContentDigest": digest} for l, v in p["locales"].items()]
            r = gql('mutation($id:ID!,$t:[TranslationInput!]!){ translationsRegister(resourceId:$id, translations:$t){ userErrors{ field message } } }', {"id": p["id"], "t": t})["translationsRegister"]
            if r["userErrors"]:
                sys.exit(f"  ✗ translations {p['handle']}: {r['userErrors']}")
        time.sleep(0.3)
    print(f"  ✓ {len(plan)} study entries' JSON-LD author -> Organization (translations re-registered)")
    left = articles(), studies()
    print(f"  verify: articles still naming the person {len(left[0])}, study entries {len(left[1])}")
    return 0 if not (left[0] or left[1]) else 1


if __name__ == "__main__":
    sys.exit(main())
