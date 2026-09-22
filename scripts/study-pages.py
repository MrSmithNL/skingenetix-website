#!/usr/bin/env python3
"""Publish Evidence Library study pages (metaobject `study`, /pages/study/<handle>) in all six languages.

Author: Claude (Opus 5) for Malcolm Smith · 2026-09-22
Purpose: docs/research-2026-study-hubs-credibility.md §3 — one appraisal page per qualifying human study.
Template: templates/metaobject/study.json (stock rich-text sections reading the metaobject's fields).

    python3 scripts/study-pages.py configs/studies/<handle>.json            # dry run: word counts, checks
    python3 scripts/study-pages.py configs/studies/<handle>.json --apply    # create/update + translate + publish
    python3 scripts/study-pages.py configs/studies/<handle>.json --verify-live

Content file: {"handle", "seo": {loc: {"title","description"}}, "pubmed_url", "hub_handle", "jsonld": {...},
               "fields": {"intro"|"key_facts"|"body"|"reference": {loc: [blocks]}}}
Blocks: ["h1", text] ["h2", text] ["p", markup] ["ul", [markup, ...]]; markup supports **bold**, *italic*
and [label](url). Internal /pages|/products|/collections links get the locale prefix automatically.

Rules enforced (research §3.4): one <h1>, the H1 must not start with the bare ingredient head term, a PubMed
or DOI link in the key-facts box, every locale present for every field, 700–1,500 English words.
"""
import argparse, html as H, importlib.util, json, pathlib, re, sys, time, urllib.error, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://www.skingenetix.com"
LOCALES = ["de", "nl", "fr", "es", "it"]
_s = importlib.util.spec_from_file_location("hu", ROOT / "scripts/hub-upgrade.py")
hu = importlib.util.module_from_spec(_s)
_argv, sys.argv = sys.argv, [sys.argv[0]]
_s.loader.exec_module(hu)
sys.argv = _argv
gql = hu.gql
INLINE = re.compile(r"\*\*(.+?)\*\*|\*(.+?)\*|\[([^\]]+)\]\(([^)]+)\)")


def localise(url, loc):
    if loc != "en" and re.match(r"^/(pages|products|collections|blogs)/", url):
        return f"/{loc}{url}"
    return url


def inline(markup, loc):
    out, pos = [], 0
    for m in INLINE.finditer(markup):
        if m.start() > pos:
            out.append({"type": "text", "value": markup[pos:m.start()]})
        if m.group(1):
            out.append({"type": "text", "value": m.group(1), "bold": True})
        elif m.group(2):
            out.append({"type": "text", "value": m.group(2), "italic": True})
        else:
            out.append({"type": "link", "url": localise(m.group(4), loc), "target": "_blank" if m.group(4).startswith("http") else None,
                        "children": [{"type": "text", "value": m.group(3)}]})
            if out[-1]["target"] is None:
                del out[-1]["target"]
        pos = m.end()
    if pos < len(markup):
        out.append({"type": "text", "value": markup[pos:]})
    return out


def rich(blocks, loc):
    nodes = []
    for kind, content in blocks:
        if kind in ("h1", "h2", "h3"):
            nodes.append({"type": "heading", "level": int(kind[1]), "children": inline(content, loc)})
        elif kind == "p":
            nodes.append({"type": "paragraph", "children": inline(content, loc)})
        elif kind == "ul":
            nodes.append({"type": "list", "listType": "unordered",
                          "children": [{"type": "list-item", "children": inline(i, loc)} for i in content]})
    return json.dumps({"type": "root", "children": nodes}, ensure_ascii=False, separators=(",", ":"))


def words(blocks):
    t = " ".join(c if isinstance(c, str) else " ".join(c) for _, c in blocks)
    return len(re.findall(r"\w+", INLINE.sub(lambda m: m.group(1) or m.group(2) or m.group(3), t)))


def check(cfg):
    errs = []
    for f, per in cfg["fields"].items():
        for l in ["en"] + LOCALES:
            if l not in per:
                errs.append(f"{f}: missing {l}")
    h1s = [c for b in cfg["fields"].values() for l, blocks in b.items() if l == "en" for k, c in blocks if k == "h1"]
    if len(h1s) != 1:
        errs.append(f"expected exactly one h1, found {len(h1s)}")
    elif re.match(r"(?i)^(pdrn|argireline|copper peptide|ghk-cu|matrixyl|glutathione)\b", h1s[0]):
        errs.append("H1 leads with the bare ingredient term (cannibalises the hub)")
    kf = json.dumps(cfg["fields"]["key_facts"]["en"])
    if "pubmed" not in kf and "doi.org" not in kf:
        errs.append("key facts box has no PubMed/DOI link")
    n = sum(words(cfg["fields"][f]["en"]) for f in cfg["fields"])
    if not 700 <= n <= 1500:
        errs.append(f"English length {n} words (target 700–1,500)")
    return errs, n


def values(cfg, loc):
    v = {f: rich(cfg["fields"][f][loc], loc) for f in cfg["fields"]}
    v["h1"] = next(c for k, c in cfg["fields"]["intro"][loc] if k == "h1")
    v["seo_title"] = cfg["seo"][loc]["title"]
    v["seo_description"] = cfg["seo"][loc]["description"]
    return v


def hub_id(handle):
    n = gql('query($q:String!){ pages(first:1, query:$q){ nodes{ id handle } } }', {"q": f"handle:{handle}"})["pages"]["nodes"]
    return n[0]["id"]


def apply(cfg):
    en = values(cfg, "en")
    ld = '<script type="application/ld+json">' + json.dumps(cfg["jsonld"], ensure_ascii=False) + "</script>"
    fields = [{"key": k, "value": v} for k, v in en.items()] + [
        {"key": "jsonld", "value": ld}, {"key": "pubmed_url", "value": cfg["pubmed_url"]},
        {"key": "hub", "value": hub_id(cfg["hub_handle"])}]
    existing = gql('query($h:MetaobjectHandleInput!){ metaobjectByHandle(handle:$h){ id } }',
                   {"h": {"type": "study", "handle": cfg["handle"]}})["metaobjectByHandle"]
    if existing:
        r = gql('mutation($id:ID!,$m:MetaobjectUpdateInput!){ metaobjectUpdate(id:$id, metaobject:$m){ metaobject{ id } userErrors{ field message } } }',
                {"id": existing["id"], "m": {"fields": fields, "capabilities": {"publishable": {"status": "ACTIVE"}}}})["metaobjectUpdate"]
    else:
        r = gql('mutation($m:MetaobjectCreateInput!){ metaobjectCreate(metaobject:$m){ metaobject{ id } userErrors{ field message } } }',
                {"m": {"type": "study", "handle": cfg["handle"], "fields": fields, "capabilities": {"publishable": {"status": "ACTIVE"}}}})["metaobjectCreate"]
    if r["userErrors"]:
        sys.exit(f"  ✗ {r['userErrors']}")
    rid = r["metaobject"]["id"]
    time.sleep(3)
    tc = {c["key"]: c for c in gql('query($id:ID!){ translatableResource(resourceId:$id){ translatableContent{ key value digest } } }',
                                   {"id": rid})["translatableResource"]["translatableContent"]}
    t = []
    for loc in LOCALES:
        lv = values(cfg, loc)
        for k, v in lv.items():
            if k in tc:
                t.append({"locale": loc, "key": k, "value": v, "translatableContentDigest": tc[k]["digest"]})
    for i in range(0, len(t), 50):
        rr = gql('mutation($id:ID!,$t:[TranslationInput!]!){ translationsRegister(resourceId:$id, translations:$t){ userErrors{ message } } }',
                 {"id": rid, "t": t[i:i + 50]})["translationsRegister"]
        if rr["userErrors"]:
            sys.exit(f"  ✗ translations: {rr['userErrors']}")
    print(f"  ✓ {cfg['handle']}: {'updated' if existing else 'created'}, ACTIVE, {len(t)} translations registered")


def verify(cfg):
    bad = 0
    for loc in ["en"] + LOCALES:
        url = f"{BASE}{'' if loc == 'en' else '/' + loc}/pages/study/{cfg['handle']}"
        html = _get(url + f"?v={time.time()}")
        h1 = [H.unescape(re.sub(r"<[^>]+>", "", x)).strip() for x in re.findall(r"<h1[^>]*>(.*?)</h1>", html, re.S)]
        page = re.sub(r"<style\b.*?</style>", "", html, flags=re.S)   # CSS attribute selectors are not links
        want = next(c for k, c in cfg["fields"]["intro"][loc] if k == "h1")
        ld = all(json.loads(b) for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S))
        dead = [h for h in set(re.findall(r'href="(/[a-z]{2}/(?:pages|products|collections)/[^"#?]+|/(?:pages|products|collections)/[^"#?]+)"', page))
                if h.count("/") <= 4 and "study/" not in h and _status(BASE + h) != 200][:3]
        ok = h1 == [want] and ld and not dead
        bad += not ok
        print(f"  {'✓' if ok else '✗'} {loc}: h1 {'ok' if h1 == [want] else h1}, JSON-LD {'valid' if ld else 'INVALID'}{', dead: ' + str(dead) if dead else ''}")
        time.sleep(1)
    return bad


def _get(u):
    for a in range(6):
        try:
            return urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=40).read().decode()
        except urllib.error.HTTPError as e:
            if e.code != 429 or a == 5:
                raise
            time.sleep(8 * (a + 1))


def _status(u):
    for a in range(6):
        try:
            time.sleep(0.6)
            return urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=30).status
        except urllib.error.HTTPError as e:
            if e.code != 429:
                return e.code
            time.sleep(8 * (a + 1))
        except Exception:
            return 0
    return 429


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--verify-live", action="store_true")
    a = ap.parse_args()
    cfg = json.loads(pathlib.Path(a.config).read_text())
    if a.verify_live:
        return 1 if verify(cfg) else 0
    errs, n = check(cfg)
    print(f"  {cfg['handle']}: {n} English words")
    for e in errs:
        print("  ✗", e)
    if errs:
        return 1
    if a.apply:
        apply(cfg)
    else:
        print("  dry run — nothing written.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
