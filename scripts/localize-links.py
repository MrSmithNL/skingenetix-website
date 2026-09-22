#!/usr/bin/env python3
"""Make every internal link stay in the reader's language — all six locales.

Author: Claude (Opus 5) for Malcolm Smith · 2026-09-22
Purpose: the 2026-09-22 link audit (scripts/link-audit.py) found internal links in 155 of 324 page×locale
views that dropped a translated page's reader into English. Two causes, two fixes:

  A. URL settings in theme JSON (buttons, tiles, "Read Research" cards) held literal paths ("/pages/x").
     Shopify does not localise a literal path; it DOES localise a resource reference. A literal path is
     rewritten to "shopify://pages/x" (…/collections/…, …/products/…, …/blogs/…) — verified live 2026-09-22:
     the same setting then renders /de/pages/x on /de. One change fixes all five locales.
  B. Hand-written links inside translated text (richtext settings, product descriptions, rich-text
     metafields, metaobjects, collection/page bodies) carry no locale prefix. Each CURRENT translation is
     rewritten to /<locale>/… and re-registered against the digest it already matches.
  C. OUTDATED translations are never touched (re-registering them would mark stale text current); they are
     listed so they can be re-translated — that is where the English-only prose links live.

    python3 scripts/localize-links.py            # dry run: counts per resource type
    python3 scripts/localize-links.py --apply    # backups/localize-links-<stamp>.json first
"""
import argparse, datetime as dt, importlib.util, json, pathlib, re, sys, time, urllib.error, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOCALES = ["de", "nl", "fr", "es", "it"]
_s = importlib.util.spec_from_file_location("hu", ROOT / "scripts/hub-upgrade.py")
hu = importlib.util.module_from_spec(_s)
_argv, sys.argv = sys.argv, [sys.argv[0]]
_s.loader.exec_module(hu)
sys.argv = _argv
gql = hu.gql
PATH = re.compile(r"^/(pages|collections|products|blogs)/([a-z0-9][a-z0-9\-]*)$")
KINDS = ["ONLINE_STORE_THEME_JSON_TEMPLATE", "ONLINE_STORE_THEME_SECTION_GROUP", "PRODUCT", "COLLECTION", "PAGE",
         "METAFIELD", "METAOBJECT", "ARTICLE"]


def exists(path):
    try:
        urllib.request.urlopen(urllib.request.Request("https://www.skingenetix.com" + path,
                                                      headers={"User-Agent": "Mozilla/5.0"}), timeout=30)
        return True
    except urllib.error.HTTPError:
        return False


# ---------- A: literal URL settings → resource references ----------

def theme_json_files():
    names, after = [], None
    while True:
        f = gql('query($id:ID!,$a:String){ theme(id:$id){ files(first:250, after:$a, filenames:["templates/*.json","sections/*.json"]){ nodes{ filename } pageInfo{ hasNextPage endCursor } } } }',
                {"id": hu.THEME, "a": after})["theme"]["files"]
        names += [n["filename"] for n in f["nodes"]]
        if not f["pageInfo"]["hasNextPage"]:
            return names
        after = f["pageInfo"]["endCursor"]


def plan_a():
    out, dead = {}, set()
    checked = {}
    for name in theme_json_files():
        raw = hu.read_file(name)
        try:
            hdr, j = hu.split(raw)
        except Exception:
            continue
        hits = []

        def walk(x, path):
            if isinstance(x, dict):
                for k, v in x.items():
                    walk(v, path + [k])
            elif isinstance(x, list):
                for i, v in enumerate(x):
                    walk(v, path + [i])
            elif isinstance(x, str) and PATH.match(x) and path and path[-2:-1] == ["settings"] or \
                    (isinstance(x, str) and PATH.match(x) and len(path) >= 2 and path[-2] == "settings"):
                if x not in checked:
                    checked[x] = exists(x)
                    time.sleep(0.2)
                if checked[x]:
                    hits.append((path, x))
                else:
                    dead.add((name, x))
        walk(j, [])
        if hits:
            out[name] = {"raw": raw, "hits": hits}
    return out, dead


def apply_a(plan):
    for name, p in plan.items():
        hdr, j = hu.split(p["raw"])
        for path, val in p["hits"]:
            node = j
            for k in path[:-1]:
                node = node[k]
            m = PATH.match(val)
            node[path[-1]] = f"shopify://{m.group(1)}/{m.group(2)}"
        hu.upload(name, hdr, j)
        print(f"  A ✓ {name:<55} {len(p['hits'])} link setting(s) → resource references")


# ---------- B/C: locale prefixes inside translated text ----------

def prefix(val, loc):
    val2 = re.sub(r'(href=\\?["\'])/(?!(?:de|nl|fr|es|it)/)(pages|collections|products|blogs)/', rf"\1/{loc}/\2/", val)
    val2 = re.sub(r'("url"\s*:\s*")/(?!(?:de|nl|fr|es|it)/)(pages|collections|products|blogs)/', rf"\1/{loc}/\2/", val2)
    return val2


def plan_b():
    fixes, outdated = [], []
    for kind in KINDS:
        after = None
        while True:
            d = gql('query($t:TranslatableResourceType!,$a:String){ translatableResources(resourceType:$t, first:100, after:$a){ '
                    'nodes{ resourceId translatableContent{ key value digest } } pageInfo{ hasNextPage endCursor } } }',
                    {"t": kind, "a": after})["translatableResources"]
            for n in d["nodes"]:
                en = {c["key"]: c for c in n["translatableContent"]}
                if not any(re.search(r'(href=\\?["\']|"url"\s*:\s*")/(pages|collections|products|blogs)/', c["value"] or "")
                           for c in en.values()):
                    continue
                for loc in LOCALES:
                    trs = gql('query($id:ID!,$l:String!){ translatableResource(resourceId:$id){ translations(locale:$l){ key value outdated } } }',
                              {"id": n["resourceId"], "l": loc})["translatableResource"]["translations"]
                    for t in trs:
                        new = prefix(t["value"] or "", loc)
                        if new == t["value"] or t["key"] not in en:
                            continue
                        if t["outdated"]:
                            outdated.append((kind, n["resourceId"], t["key"], loc))
                        else:
                            fixes.append({"kind": kind, "rid": n["resourceId"], "key": t["key"], "locale": loc,
                                          "old": t["value"], "new": new, "digest": en[t["key"]]["digest"]})
            if not d["pageInfo"]["hasNextPage"]:
                break
            after = d["pageInfo"]["endCursor"]
    return fixes, outdated


def apply_b(fixes):
    by = {}
    for f in fixes:
        by.setdefault(f["rid"], []).append(f)
    for rid, fs in by.items():
        r = gql('mutation($id:ID!,$t:[TranslationInput!]!){ translationsRegister(resourceId:$id, translations:$t){ userErrors{ message } } }',
                {"id": rid, "t": [{"locale": f["locale"], "key": f["key"], "value": f["new"], "translatableContentDigest": f["digest"]} for f in fs]})
        errs = r["translationsRegister"]["userErrors"]
        print(f"  B {'✗ ' + str(errs) if errs else '✓'} {rid.split('/')[-1][:60]:<61} {len(fs)} translation(s)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    pa, dead = plan_a()
    print(f"  A: {sum(len(p['hits']) for p in pa.values())} literal link settings in {len(pa)} theme files")
    for n, v in sorted(dead):
        print(f"  A ⚠ dead link setting left unchanged — fix by hand: {n}: {v}")
    fb, outdated = plan_b()
    print(f"  B: {len(fb)} current translations with unprefixed links")
    print(f"  C: {len(outdated)} OUTDATED translations with unprefixed links (not touched — need re-translation)")
    if not a.apply:
        return 0
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    (ROOT / f"backups/localize-links-{stamp}.json").write_text(json.dumps(
        {"a": {k: v["raw"] for k, v in pa.items()}, "b": fb, "outdated": outdated}, ensure_ascii=False, indent=1))
    apply_a(pa)
    apply_b(fb)
    (ROOT / "docs/audits/links").mkdir(parents=True, exist_ok=True)
    (ROOT / f"docs/audits/links/outdated-translations-{dt.date.today()}.json").write_text(json.dumps(outdated, indent=1))
    print(f"  backup {stamp}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
