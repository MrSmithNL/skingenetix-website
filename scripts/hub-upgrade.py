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
  remove_sections ["section_id"]
  _retired        "why, and which spec replaced it" — --apply then refuses (2026-09-24)
  section_settings {"section_id": {"setting": value}} — e.g. backgrounds, for alternation
  jsonld          an object, emitted as <script id="sgx-webpage-jsonld"> INSIDE the existing
                  custom-html section named by `jsonld_host` (default "references").
                  ⚠️ Never as its own section: a custom-html section with no visible content
                  still renders a padded .section wrapper — at the top of /pages/pdrn-research
                  it left a 160px blank band above the hero (2026-09-22).

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

_c = importlib.util.spec_from_file_location("hub_charts", ROOT / "scripts/hub_charts.py")
_charts = importlib.util.module_from_spec(_c); _c.loader.exec_module(_charts)
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
        for tag in ("h1", "h2"):
            # counts classed headings too — a bare "<h2>" count missed every <h2 class="…"> (fixed 2026-09-24)
            count = lambda s: len(re.findall(rf"<{tag}[\s>]", s))
            if count(values[l]) != count(values["en"]):
                sys.exit(f"  ✗ {label} [{l}]: <{tag}> count differs from English")


def expand_charts(node, charts):
    """Replace every {"$chart": [...]} placeholder with a six-locale dict of rendered HTML."""
    if isinstance(node, dict):
        if "$chart" in node:
            return {l: _charts.render_group(node, charts, l) for l in ["en"] + LOCALES}
        return {k: expand_charts(v, charts) for k, v in node.items()}
    if isinstance(node, list):
        return [expand_charts(v, charts) for v in node]
    return node


def lift_translatables(settings, key_prefix, to_translate):
    """A setting whose value is {"en": ..., "de": ...} is translatable: keep English, queue the rest."""
    for k, v in list(settings.items()):
        if isinstance(v, dict) and "en" in v:
            check_values(f"{key_prefix}.{k}", v)
            settings[k] = v["en"]
            to_translate.append((f"{key_prefix}.{k}", v))


def ref_row(r):
    return ('<div class="sgref__r">' + REF_ICON + f'<div><p class="sgref__ti">{r["title"]}</p>'
            f'<p class="sgref__me">{r["meta"]}</p></div><a class="sgref__lk" href="{r["url"]}" target="_blank" '
            f'rel="noopener">{r["link"]}</a></div>')


REF_ICON = ('<svg class="sgref__ico" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6 2.75h7.5L18.5 7.75V21.25H6z" '
            'fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M13.25 2.75V8h5.25" fill="none" '
            'stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M8.75 12.5h6.5M8.75 15.75h6.5M8.75 19h4" '
            'stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>')


def localise_jsonld(ld, loc, i18n):
    ld = json.loads(json.dumps(ld))
    ld["inLanguage"] = loc
    if loc != "en":
        ld.update(i18n.get(loc, {}))
        for k in ("url", "@id"):
            if k in ld:
                ld[k] = ld[k].replace(f"{BASE}/pages/", f"{BASE}/{loc}/pages/")
    return ld


def build(spec, j):
    """Apply the spec's English values to the template JSON. Returns [(key_suffix, values)] to translate."""
    to_translate = []
    spec = expand_charts(spec, spec.get("charts", {}))
    for rb in spec.get("remove_blocks", []):
        sec, blk = rb.split("/")
        s = j["sections"][sec]
        s["blocks"].pop(blk, None)
        s["block_order"] = [b for b in s.get("block_order", []) if b != blk]
    for item in spec.get("set", []):
        parts = item["at"].split("/")
        check_values(item["at"], item["values"])
        if len(parts) == 2:                       # section-level setting, e.g. "faq/title"
            j["sections"][parts[0]].setdefault("settings", {})[parts[1]] = item["values"]["en"]
        else:
            sec, blk, key = parts
            j["sections"][sec]["blocks"][blk]["settings"][key] = item["values"]["en"]
        to_translate.append((".".join(parts), item["values"]))
    for ab in spec.get("add_blocks", []):
        s = j["sections"][ab["section"]]
        blk = json.loads(json.dumps(ab["block"]))
        lift_translatables(blk.setdefault("settings", {}), f"{ab['section']}.{ab['id']}", to_translate)
        s["blocks"][ab["id"]] = blk
        s["block_order"] = [b for b in s.get("block_order", []) if b != ab["id"]]
        s["block_order"].insert(s["block_order"].index(ab["after"]) + 1 if ab.get("after") else len(s["block_order"]), ab["id"])
    for add in spec.get("add_sections", []):
        sec = json.loads(json.dumps(add["section"]))
        lift_translatables(sec.setdefault("settings", {}), add["id"], to_translate)
        for bid, blk in sec.get("blocks", {}).items():
            lift_translatables(blk.setdefault("settings", {}), f"{add['id']}.{bid}", to_translate)
        if add["id"] in j["order"]:
            j["order"].remove(add["id"])
        j["sections"][add["id"]] = sec
        j["order"].insert(j["order"].index(add["after"]) + 1, add["id"])
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
    for sid in spec.get("remove_sections", []):
        j["sections"].pop(sid, None)
        j["order"] = [x for x in j["order"] if x != sid]
    for sid, settings in spec.get("section_settings", {}).items():
        j["sections"][sid].setdefault("settings", {}).update(settings)
    host = spec.get("jsonld_host", "references")
    tag = '<script type="application/ld+json" id="sgx-webpage-jsonld">'
    if spec.get("references_add"):
        h = j["sections"][host]["settings"]["html"]
        body_end = h.find("<script") if "<script" in h else len(h)
        new = "".join(ref_row(r) for r in spec["references_add"] if r["url"] not in h[:body_end])
        close = h.rfind("</div></div>", 0, body_end)       # end of .sgref__list, then .sgref
        j["sections"][host]["settings"]["html"] = h[:close] + new + h[close:]
    if spec.get("jsonld"):
        h = j["sections"][host]["settings"]["html"]
        h = re.sub(re.escape(tag) + r".*?</script>", "", h, flags=re.S).rstrip()
        ld = localise_jsonld(spec["jsonld"], "en", {})
        j["sections"][host]["settings"]["html"] = h + "\n" + tag + "\n" + json.dumps(ld, indent=2, ensure_ascii=False) + "\n</script>"
        j["sections"].pop("schema_markup", None)          # retire the old padded host
        j["order"] = [x for x in j["order"] if x != "schema_markup"]
    if "references_i18n" in spec:
        # The references block (heading, link labels, JSON-LD) had NO translations on any hub until
        # 2026-09-22: every locale served the English block. Paper titles stay in English — they are
        # the published titles — but the page's own words and the JSON-LD are localised.
        en = j["sections"][host]["settings"]["html"]
        values = {"en": en}
        for l in LOCALES:
            v = en
            for a, b in spec["references_i18n"].get(l, {}).items():
                v = v.replace(a, b)
            if spec.get("jsonld"):
                ld = localise_jsonld(spec["jsonld"], l, spec.get("jsonld_i18n", {}))
                v = re.sub(re.escape(tag) + r".*?</script>",
                           lambda _m: tag + "\n" + json.dumps(ld, indent=2, ensure_ascii=False) + "\n</script>", v, flags=re.S)
            values[l] = v
        to_translate.append((f"{host}.html", values))
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


def locale_texts(node):
    """Every six-locale value in the spec (charts expanded), for the live checks."""
    if isinstance(node, dict):
        if "en" in node and all(l in node for l in LOCALES) and isinstance(node["en"], str):
            return [node]
        return [t for v in node.values() for t in locale_texts(v)]
    if isinstance(node, list):
        return [t for v in node for t in locale_texts(v)]
    return []


def wanted_headings(texts, loc, tag):
    """Heading text in the spec's values for one locale — classed (<h2 class="evd__h">) as well as bare.

    Until 2026-09-24 this matched bare <h2> only, so on the custom-html science-page template it expected
    no headings at all and reported "0/0 headings live" as a pass.
    """
    return [re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", "", h))).strip()
            for t in texts for h in re.findall(rf"<{tag}(?:\s[^>]*)?>(.*?)</{tag}>", t[loc], re.S)]


def missing_anchors(texts, loc, page):
    """#fragment links in the spec's values whose target id is not on the live page.

    A broken in-page anchor still returns 200, so the link check alone can never catch one.
    """
    frags = dict.fromkeys(f for t in texts for f in re.findall(r'href="#([^"]+)"', t[loc]))
    return [f"#{f}" for f in frags if not re.search(rf'id="{re.escape(f)}"', page)]


def verify(spec):
    texts = locale_texts({k: v for k, v in expand_charts(spec, spec.get("charts", {})).items()
                          if k not in ("charts", "references_i18n", "jsonld_i18n")})
    bad = 0
    for loc in ["en"] + LOCALES:
        page = fetch(f"{BASE}{'' if loc == 'en' else '/' + loc}/pages/{spec['page']}?hub={int(time.time())}")
        live_h2 = [re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", "", x))).strip() for x in re.findall(r"<h2[^>]*>(.*?)</h2>", page, re.S)]
        want = wanted_headings(texts, loc, "h2")
        missing = [w for w in want if w not in live_h2]
        live_h1 = [re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", "", x))).strip() for x in re.findall(r"<h1[^>]*>(.*?)</h1>", page, re.S)]
        want_h1 = wanted_headings(texts, loc, "h1")
        no_target = missing_anchors(texts, loc, page)
        h1_problem = f"expected one <h1> {want_h1[0]!r}, found {live_h1}" if want_h1 and live_h1 != want_h1[:1] else ""
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
        ok = not missing and not dead and ld_ok and not h1_problem and not no_target
        bad += not ok
        anchors = len(set(re.findall(r'href="#([^"]+)"', " ".join(t[loc] for t in texts))))
        print(f"  {'✓' if ok else '✗'} {loc}: {len(want) - len(missing)}/{len(want)} headings live as <h2>, "
              f"{len(links) - len(dead)}/{len(links)} links resolve, {anchors - len(no_target)}/{anchors} anchors land"
              f"{', JSON-LD WebPage ok' if loc == 'en' and ld_ok and spec.get('jsonld') else ''}")
        for m in missing: print(f"      missing heading: {m}")
        for f in no_target: print(f"      anchor with no target on the page: {f}")
        if h1_problem: print(f"      {h1_problem}")
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
    if spec.get("_retired") and a.apply:
        # a superseded spec rewrites sections a later spec now owns — one section, one owning spec
        sys.exit(f"  ✗ this spec is retired and must never be re-applied: {spec['_retired']}")
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
