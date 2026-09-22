#!/usr/bin/env python3
"""Upgrade an ingredient research page into a hub — standard sections, all locales at once.

Author: Claude (Opus 5) for Malcolm Smith · 2026-09-22
Purpose: Phase 2 of docs/content-plan-2026.md. One spec per hub in configs/hub-upgrades/.

    python3 scripts/hub-upgrade.py configs/hub-upgrades/pdrn-research.json            # dry run
    python3 scripts/hub-upgrade.py configs/hub-upgrades/pdrn-research.json --apply
    python3 scripts/hub-upgrade.py configs/hub-upgrades/pdrn-research.json --verify-live
    python3 scripts/hub-upgrade.py configs/hub-upgrades/pdrn-research.json --rollback

Spec keys:
  set             [{"at": "section/block/setting", "values": {"en": ..., "de": ..., ...}}]
  remove_blocks   ["section/block"]
  insert_sections [{"id", "after", "type", "settings", "block", "values": {"en": ..., ...}}]
                  — a stock section (e.g. rich-text) with one richtext block
  jsonld          an object, emitted as a custom-html section named schema_markup
                  (the pattern /pages/the-science already uses)

Why each rule exists:
  * Semantic <h2> lives INSIDE the richtext: Impact renders section headings as
    <p class="h2">, so a heading block gives no document outline.
  * Every new or rewritten setting is translated in the same change. A setting
    with no translation is served in English on all five other locales — met on
    this store with the product SEO titles on 2026-09-22.
  * Translations are registered against the digest of the value just uploaded,
    so Translate & Adapt marks them current, not outdated.
  * Translated hrefs must carry the locale prefix (/de/pages/...). Hardcoded
    links in richtext are not localised by Shopify.
"""
import argparse, datetime as dt, glob, html as H, importlib.util, json, pathlib, re, sys, time, urllib.error, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://www.skingenetix.com"
THEME = "gid://shopify/OnlineStoreTheme/184835965313"
LOCALES = ["de", "nl", "fr", "es", "it"]

_s = importlib.util.spec_from_file_location("uti", ROOT / "scripts/upload-theme-images.py")
_uti = importlib.util.module_from_spec(_s); _s.loader.exec_module(_uti)
_env = _uti.env(); STORE = _env["SHOPIFY_SKINGENETIX_STORE"]; TOKEN = _uti.token(_env)


def gql(query, variables=None):
    r = urllib.request.Request(f"https://{STORE}/admin/api/2025-07/graphql.json",
                               data=json.dumps({"query": query, "variables": variables or {}}).encode(),
                               method="POST", headers={"X-Shopify-Access-Token": TOKEN,
                                                       "Content-Type": "application/json"})
    d = json.loads(urllib.request.urlopen(r, timeout=120).read())
    if d.get("errors"):
        raise RuntimeError(json.dumps(d["errors"])[:400])
    return d["data"]


def read_file(name):
    n = gql('query($id:ID!,$f:[String!]!){ theme(id:$id){ files(filenames:$f){ nodes{ '
            'body{ ... on OnlineStoreThemeFileBodyText{ content } } } } } }', {"id": THEME, "f": [name]})
    return n["theme"]["files"]["nodes"][0]["body"]["content"]


def split(raw):
    m = re.match(r"\s*(/\*.*?\*/)\s*", raw, re.S)
    return (m.group(1) if m else ""), json.loads(raw[m.end():] if m else raw)


def upload(name, hdr, j):
    body = (hdr + "\n" if hdr else "") + json.dumps(j, indent=2, ensure_ascii=False)
    r = gql('mutation($t:ID!,$f:[OnlineStoreThemeFilesUpsertFileInput!]!){ themeFilesUpsert(themeId:$t, files:$f)'
            '{ userErrors{field message} } }', {"t": THEME, "f": [{"filename": name, "body": {"type": "TEXT", "value": body}}]})
    if r["themeFilesUpsert"]["userErrors"]:
        raise RuntimeError(r["themeFilesUpsert"]["userErrors"])


def check_values(label, values):
    missing = [l for l in ["en"] + LOCALES if l not in values]
    if missing:
        sys.exit(f"  ✗ {label}: missing locales {missing} — every new text ships in all six languages")
    for l in LOCALES:
        for href in re.findall(r'href="(/[^"]*)"', values[l]):
            if not href.startswith(f"/{l}/"):
                sys.exit(f"  ✗ {label} [{l}]: link {href} lacks the /{l}/ prefix")
        if values[l].count("<h2>") != values["en"].count("<h2>"):
            sys.exit(f"  ✗ {label} [{l}]: heading count differs from English")


def build(spec, j):
    """Apply the spec's English values to the template JSON. Returns [(key_suffix, values)] to translate."""
    to_translate = []
    for rb in spec.get("remove_blocks", []):
        sec, blk = rb.split("/")
        s = j["sections"][sec]
        s["blocks"].pop(blk, None)
        s["block_order"] = [b for b in s.get("block_order", []) if b != blk]
    for item in spec.get("set", []):
        sec, blk, key = item["at"].split("/")
        check_values(item["at"], item["values"])
        j["sections"][sec]["blocks"][blk]["settings"][key] = item["values"]["en"]
        to_translate.append((f"{sec}.{blk}.{key}", item["values"]))
    for ins in spec.get("insert_sections", []):
        check_values(ins["id"], ins["values"])
        if ins["id"] in j["sections"]:
            j["order"].remove(ins["id"])
        j["sections"][ins["id"]] = {"type": ins["type"], "settings": ins["settings"],
                                   "blocks": {ins["block"]: {"type": "richtext",
                                                             "settings": {"content": ins["values"]["en"]}}},
                                   "block_order": [ins["block"]]}
        j["order"].insert(j["order"].index(ins["after"]) + 1, ins["id"])
        to_translate.append((f"{ins['id']}.{ins['block']}.content", ins["values"]))
    if spec.get("jsonld"):
        html_ = '<script type="application/ld+json">\n' + json.dumps(spec["jsonld"], indent=2, ensure_ascii=False) + "\n</script>"
        j["sections"]["schema_markup"] = {"type": "custom-html", "settings": {"html": html_}}
        if "schema_markup" not in j["order"]:
            j["order"].insert(0, "schema_markup")
    return to_translate


def register(spec, to_translate):
    rid = f"gid://shopify/OnlineStoreThemeJsonTemplate/{spec['template'].split('templates/', 1)[1].rsplit('.json', 1)[0]}?theme_id={THEME.rsplit('/', 1)[1]}"
    for attempt in range(6):
        tc = gql('query($id:ID!){ translatableResource(resourceId:$id){ translatableContent{ key value digest } } }',
                 {"id": rid})["translatableResource"]["translatableContent"]
        prefix = f"section.{spec['template'].split('templates/', 1)[1]}."
        index = {c["key"].split(":")[0][len(prefix):]: c for c in tc if c["key"].startswith(prefix)}
        if all(k in index and index[k]["value"] == v["en"] for k, v in to_translate):
            break
        time.sleep(5)   # the translatable index lags the upload by a few seconds
    for k, v in to_translate:
        c = index.get(k)
        if not c or c["value"] != v["en"]:
            raise RuntimeError(f"translatable key {k} not found or stale")
        r = gql('mutation($id:ID!,$t:[TranslationInput!]!){ translationsRegister(resourceId:$id, translations:$t)'
                '{ userErrors{field message} } }',
                {"id": rid, "t": [{"locale": l, "key": c["key"], "value": v[l],
                                   "translatableContentDigest": c["digest"]} for l in LOCALES]})
        errs = r["translationsRegister"]["userErrors"]
        print(f"    {k:<32} {'✗ ' + str(errs) if errs else '5 locales ✓'}")
        if errs:
            raise RuntimeError(errs)


def fetch(url):
    for attempt in range(6):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}),
                                          timeout=40).read().decode("utf-8", "ignore")
        except urllib.error.HTTPError as e:
            if e.code not in (429, 503) or attempt == 5:
                raise
            time.sleep(10 * (attempt + 1))


def verify(spec):
    texts = [v["values"] for v in spec.get("set", []) if "content" in v["at"]] + [i["values"] for i in spec.get("insert_sections", [])]
    bad = 0
    for loc in ["en"] + LOCALES:
        page = fetch(f"{BASE}{'' if loc == 'en' else '/' + loc}/pages/{spec['page']}?hub={int(time.time())}")
        live_h2 = [re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", "", x))).strip() for x in re.findall(r"<h2[^>]*>(.*?)</h2>", page, re.S)]
        want = [re.sub(r"<[^>]+>", "", h) for t in texts for h in re.findall(r"<h2>(.*?)</h2>", t[loc])]
        missing = [w for w in want if H.unescape(w) not in live_h2]
        links = sorted(set(h for t in texts for h in re.findall(r'href="(/[^"]*)"', t[loc])))
        dead = []
        for href in links:
            try:
                urllib.request.urlopen(urllib.request.Request(BASE + href, headers={"User-Agent": "Mozilla/5.0"}), timeout=30)
            except urllib.error.HTTPError as e:
                dead.append(f"{href} {e.code}")
            time.sleep(0.5)
        ld_ok = True
        if loc == "en" and spec.get("jsonld"):
            blocks = re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', page, re.S)
            try:
                types = [json.loads(b).get("@type") for b in blocks]
                ld_ok = "WebPage" in types
            except Exception:
                ld_ok = False
        ok = not missing and not dead and ld_ok
        bad += not ok
        print(f"  {'✓' if ok else '✗'} {loc}: {len(want) - len(missing)}/{len(want)} headings live as <h2>, "
              f"{len(links) - len(dead)}/{len(links)} links resolve{', JSON-LD WebPage ok' if loc == 'en' and ld_ok and spec.get('jsonld') else ''}")
        for m in missing: print(f"      missing heading: {m}")
        for d_ in dead: print(f"      dead link: {d_}")
        if loc == "en" and not ld_ok: print("      JSON-LD WebPage missing or invalid")
        time.sleep(1.5)
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--verify-live", action="store_true")
    ap.add_argument("--rollback", action="store_true")
    a = ap.parse_args()
    spec = json.loads(pathlib.Path(a.spec).read_text())
    name = spec["template"]
    tag = name.replace("/", "__")

    if a.rollback:
        bk = sorted(glob.glob(str(ROOT / f"backups/hub-upgrade-{tag}-*.json")))
        if not bk:
            sys.exit("  no backup")
        hdr, j = split(pathlib.Path(bk[-1]).read_text())
        upload(name, hdr, j)
        print(f"  restored {name} from {pathlib.Path(bk[-1]).name} (translations of removed keys remain registered but unused)")
        return 0

    if a.verify_live:
        return 1 if verify(spec) else 0

    raw = read_file(name)
    hdr, j = split(raw)
    before = list(j["order"])
    to_translate = build(spec, j)
    print(f"  {name}\n  order before: {before}\n  order after : {j['order']}")
    print(f"  texts to translate: {[k for k, _ in to_translate]}")
    if not a.apply:
        print("  dry run — nothing written.")
        return 0
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    (ROOT / f"backups/hub-upgrade-{tag}-{stamp}.json").write_text(raw)
    upload(name, hdr, j)
    print(f"  uploaded (backup {stamp}); registering translations:")
    register(spec, to_translate)
    return 0


if __name__ == "__main__":
    sys.exit(main())
