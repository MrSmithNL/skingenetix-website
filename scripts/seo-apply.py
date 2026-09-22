#!/usr/bin/env python3
"""Apply a declarative SEO title/description change set to the Skingenetix store.

Author: Claude (Opus 5) for Malcolm Smith · 2026-09-22
Purpose: Phase 1 of docs/content-plan-2026.md — retitle pages, collections and
products from a reviewed spec file, with a snapshot, read-back and live check.

    python3 scripts/seo-apply.py configs/seo-changes/phase1-2026-09-22.json            # dry run
    python3 scripts/seo-apply.py configs/seo-changes/phase1-2026-09-22.json --apply    # write
    python3 scripts/seo-apply.py configs/seo-changes/phase1-2026-09-22.json --verify-live
    python3 scripts/seo-apply.py configs/seo-changes/phase1-2026-09-22.json --rollback SNAPSHOT.json

Spec format: {"pages"|"collections"|"products": {handle_or_unique_prefix: {"title", "description"}}}
Omitted fields are left exactly as they are.

Three traps this handles, each met before on this store or its sister:
  * ProductInput.seo / CollectionInput.seo REPLACE the whole object — sending
    only a title blanks the description. Both fields are always sent, with the
    current value carried over for whichever one the spec omits.
  * Page SEO is not a field on Page; it lives in the global.title_tag /
    global.description_tag metafields, with fixed types.
  * The storefront caches HTML briefly, so the live check retries before it
    declares a mismatch.

English source only. Translate & Adapt keeps serving the other locales'
existing translations until they are refreshed — deliberate (English first,
German second), and harmless here because the old translations are accurate.
"""
import argparse, datetime as dt, html, importlib.util, json, pathlib, re, sys, time, urllib.error, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://www.skingenetix.com"
TITLE_MAX, DESC_MAX = 60, 160
ROUTE = {"pages": "pages", "collections": "collections", "products": "products"}

_s = importlib.util.spec_from_file_location("uti", ROOT / "scripts/upload-theme-images.py")
_uti = importlib.util.module_from_spec(_s); _s.loader.exec_module(_uti)
_env = _uti.env(); STORE = _env["SHOPIFY_SKINGENETIX_STORE"]; TOKEN = _uti.token(_env)


def gql(query, variables=None):
    r = urllib.request.Request(f"https://{STORE}/admin/api/2025-07/graphql.json",
                               data=json.dumps({"query": query, "variables": variables or {}}).encode(),
                               method="POST", headers={"X-Shopify-Access-Token": TOKEN,
                                                       "Content-Type": "application/json"})
    d = json.loads(urllib.request.urlopen(r, timeout=90).read())
    if d.get("errors"):
        raise RuntimeError(json.dumps(d["errors"])[:400])
    return d["data"]


MF = ('t:metafield(namespace:"global",key:"title_tag"){value} '
      'd:metafield(namespace:"global",key:"description_tag"){value}')


def current():
    """Read every page, collection and product's live SEO values."""
    out = {"pages": {}, "collections": {}, "products": {}}
    for n in gql('{ pages(first:250){ nodes{ id handle %s } } }' % MF)["pages"]["nodes"]:
        out["pages"][n["handle"]] = {"id": n["id"], "title": (n["t"] or {}).get("value"),
                                     "description": (n["d"] or {}).get("value")}
    for n in gql('{ collections(first:250){ nodes{ id handle seo{title description} } } }')["collections"]["nodes"]:
        out["collections"][n["handle"]] = {"id": n["id"], **n["seo"]}
    for n in gql('{ products(first:250){ nodes{ id handle seo{title description} } } }')["products"]["nodes"]:
        out["products"][n["handle"]] = {"id": n["id"], **n["seo"]}
    return out


def resolve(kind, key, cur):
    if key in cur[kind]:
        return key
    hits = [h for h in cur[kind] if h.startswith(key)]
    if len(hits) != 1:
        sys.exit(f"  ✗ {kind}/{key}: matches {len(hits)} handles — make the prefix unique")
    return hits[0]


def plan(spec, cur):
    rows, problems = [], []
    for kind in ("pages", "collections", "products"):
        for key, want in (spec.get(kind) or {}).items():
            h = resolve(kind, key, cur)
            old = cur[kind][h]
            new = {"title": want.get("title", old["title"]),
                   "description": want.get("description", old["description"])}
            for f, lim in (("title", TITLE_MAX), ("description", DESC_MAX)):
                v = new[f] or ""
                if f in want and len(v) > lim:
                    problems.append(f"{kind}/{h} {f} is {len(v)} chars (max {lim})")
                if f in want and "—" in v:
                    problems.append(f"{kind}/{h} {f} contains an em-dash")
            rows.append((kind, h, old, new))
    return rows, problems


def apply_row(kind, h, old, new):
    if kind == "pages":
        mfs = []
        if new["title"] != old["title"]:
            mfs.append({"ownerId": old["id"], "namespace": "global", "key": "title_tag",
                        "type": "single_line_text_field", "value": new["title"]})
        if new["description"] != old["description"]:
            mfs.append({"ownerId": old["id"], "namespace": "global", "key": "description_tag",
                        "type": "multi_line_text_field", "value": new["description"]})
        if not mfs:
            return
        r = gql('mutation($m:[MetafieldsSetInput!]!){ metafieldsSet(metafields:$m){ userErrors{field message} } }',
                {"m": mfs})["metafieldsSet"]
    elif kind == "collections":
        r = gql('mutation($i:CollectionInput!){ collectionUpdate(input:$i){ userErrors{field message} } }',
                {"i": {"id": old["id"], "seo": {"title": new["title"], "description": new["description"]}}}
                )["collectionUpdate"]
    else:
        r = gql('mutation($p:ProductUpdateInput!){ productUpdate(product:$p){ userErrors{field message} } }',
                {"p": {"id": old["id"], "seo": {"title": new["title"], "description": new["description"]}}}
                )["productUpdate"]
    if r["userErrors"]:
        raise RuntimeError(f"{kind}/{h}: {r['userErrors']}")


def live(kind, h):
    url = f"{BASE}/{ROUTE[kind]}/{h}?seocheck={int(time.time())}"
    # The storefront answers a burst of requests with 503/429; that is throttling,
    # not a broken page, so back off rather than report a failure.
    for attempt in range(6):
        try:
            page = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}),
                                          timeout=40).read().decode("utf-8", "ignore")
            break
        except urllib.error.HTTPError as e:
            if e.code not in (429, 503) or attempt == 5:
                raise
            time.sleep(10 * (attempt + 1))
    time.sleep(1.5)
    t = re.search(r"<title>(.*?)</title>", page, re.S)
    d = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', page)
    norm = lambda s: re.sub(r"\s+", " ", html.unescape(s or "")).strip()
    return norm(t.group(1) if t else ""), norm(d.group(1) if d else "")


def translations(path, cur, verify_only=False):
    """Register product meta_title translations, then check each locale live.

    Needed whenever an English SEO title is set where none existed before: with
    no translation to fall back on, every locale serves the English string.
    Translations are registered against the CURRENT source digest, so they are
    marked current rather than outdated.
    """
    spec = json.loads(pathlib.Path(path).read_text())
    bad = 0
    for key, per_locale in spec["products"].items():
        h = resolve("products", key, cur)
        pid = cur["products"][h]["id"]
        if not verify_only:
            tc = gql('query($id:ID!){ translatableResource(resourceId:$id){ translatableContent{ key digest } } }',
                     {"id": pid})["translatableResource"]["translatableContent"]
            digest = next(c["digest"] for c in tc if c["key"] == "meta_title")
            r = gql('mutation($id:ID!,$t:[TranslationInput!]!){ translationsRegister(resourceId:$id, translations:$t){ userErrors{field message} } }',
                    {"id": pid, "t": [{"locale": l, "key": "meta_title", "value": v,
                                       "translatableContentDigest": digest} for l, v in per_locale.items()]}
                    )["translationsRegister"]
            if r["userErrors"]:
                raise RuntimeError(f"{h}: {r['userErrors']}")
        for loc, want in per_locale.items():
            for attempt in range(6):
                t, _ = live_locale(loc, h)
                if t == want:
                    break
                time.sleep(10)
            ok = t == want
            bad += not ok
            print(f"  {'✓' if ok else '✗'} {loc} {h[:48]:<48} {t if not ok else ''}")
    print(f"\n  {'all' if not bad else bad} {'verified live' if not bad else 'mismatches'}")
    return 1 if bad else 0


def live_locale(loc, h):
    """Fetch a product on its locale path. Locales may translate the handle and
    redirect; urllib follows the redirect, which is what a shopper sees."""
    url = f"{BASE}/{loc}/products/{h}?seocheck={int(time.time())}"
    for attempt in range(6):
        try:
            page = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}),
                                          timeout=40).read().decode("utf-8", "ignore")
            break
        except urllib.error.HTTPError as e:
            if e.code not in (429, 503) or attempt == 5:
                raise
            time.sleep(10 * (attempt + 1))
    time.sleep(1.5)
    t = re.search(r"<title>(.*?)</title>", page, re.S)
    return re.sub(r"\s+", " ", html.unescape(t.group(1) if t else "")).strip(), None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--verify-live", action="store_true")
    ap.add_argument("--rollback", metavar="SNAPSHOT")
    ap.add_argument("--translations", metavar="FILE", help="register + live-check product meta_title translations")
    ap.add_argument("--verify-only", action="store_true", help="with --translations: check live, write nothing")
    a = ap.parse_args()
    spec = json.loads(pathlib.Path(a.spec).read_text())
    cur = current()

    if a.translations:
        return translations(a.translations, cur, a.verify_only)

    if a.rollback:
        snap = json.loads(pathlib.Path(a.rollback).read_text())
        for kind in ("pages", "collections", "products"):
            for key in (spec.get(kind) or {}):
                h = resolve(kind, key, cur)
                apply_row(kind, h, cur[kind][h], snap[kind][h])
                print(f"  ↺ {kind}/{h}")
        return 0

    rows, problems = plan(spec, cur)
    if problems:
        print("  ✗ spec rejected:\n    " + "\n    ".join(problems)); return 1

    if a.verify_live:
        bad = 0
        for kind, h, _old, new in rows:
            for attempt in range(8):
                t, d = live(kind, h)
                ok_t = t == (new["title"] or "").strip()
                ok_d = (not new["description"]) or d == new["description"].strip()
                if ok_t and ok_d:
                    break
                time.sleep(15)
            mark = "✓" if ok_t and ok_d else "✗"
            bad += mark == "✗"
            print(f"  {mark} {kind}/{h[:52]:<52} title{'✓' if ok_t else '✗'} desc{'✓' if ok_d else '✗'}")
            if mark == "✗":
                print(f"      live title: {t!r}\n      live desc : {d[:120]!r}")
        print(f"\n  {len(rows) - bad}/{len(rows)} verified live")
        return 1 if bad else 0

    changed = [(k, h, o, n) for k, h, o, n in rows if (o["title"], o["description"]) != (n["title"], n["description"])]
    print(f"  {len(changed)} of {len(rows)} entries change\n")
    for kind, h, old, new in changed:
        print(f"  {kind}/{h}")
        for f in ("title", "description"):
            if old[f] != new[f]:
                print(f"    {f[:5]}  - {old[f]}\n           + {new[f]}")
    if not a.apply:
        print("\n  dry run — nothing written. Add --apply to write.")
        return 0

    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    snap = ROOT / f"configs/seo-snapshots/seo-before-{pathlib.Path(a.spec).stem}-{stamp}.json"
    snap.write_text(json.dumps(cur, indent=1))
    print(f"\n  snapshot → {snap.relative_to(ROOT)}")
    for kind, h, old, new in changed:
        apply_row(kind, h, old, new)
        time.sleep(0.3)
    after = current()
    bad = [(k, h) for k, h, _o, n in changed
           if (after[k][h]["title"], after[k][h]["description"]) != (n["title"], n["description"])]
    print(f"  applied {len(changed)}; API read-back mismatches: {len(bad)} {bad[:5] if bad else ''}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
