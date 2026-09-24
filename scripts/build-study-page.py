#!/usr/bin/env python3
"""Build and publish a designed study page from configs/studies/<handle>.json.

Author: Claude (Opus 5) for Malcolm Smith · 2026-09-24
Template: docs/study-page-template.md · Reference build: Badenhorst 2016 (copper peptide)

    python3 scripts/build-study-page.py configs/studies/<handle>.json           # dry run + local checks
    python3 scripts/build-study-page.py configs/studies/<handle>.json --apply   # publish (English + any locale present)
    python3 scripts/build-study-page.py configs/studies/<handle>.json --verify-live

WHY THIS AND NOT study-pages.py
study-pages.py publishes the pilot shape: four rich-text fields, all six locales required for
every field, no chart, table or image (Shopify richtext strips classes). It still owns those
four fields. This script writes the fifth — `sections_html`, raw HTML rendered unescaped by a
liquid block — which is where the designed body lives, and it publishes English first so a page
can be reviewed before it is translated.

WHAT IT ENFORCES before anything goes live
  * exactly one H1, and it may not open with the bare ingredient term (that cannibalises the hub)
  * SEO title <= 60 characters, description <= 160, per locale
  * every probe in the config's "checks" list present in the rendered HTML — the verified figures
  * no Liquid delimiter in the output (study_sections.render refuses)
"""
import argparse
import html as H
import importlib.util
import json
import pathlib
import re
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://www.skingenetix.com"


def _load(name, path):
    s = importlib.util.spec_from_file_location(name, ROOT / path)
    m = importlib.util.module_from_spec(s)
    argv, sys.argv = sys.argv, [sys.argv[0]]        # these modules parse args at import
    s.loader.exec_module(m)
    sys.argv = argv
    return m


spg = _load("spg", "scripts/study-pages.py")
sx = _load("sx", "scripts/study_sections.py")
gql = spg.gql
HEAD_TERM = re.compile(r"(?i)^(pdrn|argireline|copper peptide|ghk-cu|matrixyl|glutathione|acetyl)\b")


def locales(cfg):
    """Which locales this config actually carries — English first, translations as they arrive."""
    return [l for l in sx.LOCALES if l == "en" or l in cfg["h1"]]


def jsonld(cfg, loc):
    url = f"{BASE}{'' if loc == 'en' else '/' + loc}/pages/study/{cfg['handle']}"
    h1, desc = sx.t(cfg["h1"], loc), sx.t(cfg["seo_description"], loc)
    s = cfg["scholarly"]
    return {"@context": "https://schema.org", "@type": "WebPage", "@id": url + "#webpage", "url": url,
            "name": h1, "description": desc, "inLanguage": loc,
            "lastReviewed": cfg["read_at_source"],
            "datePublished": cfg.get("published", cfg["read_at_source"]),
            "dateModified": cfg["read_at_source"],
            "citation": [{"@type": "ScholarlyArticle", "name": s["name"], "url": cfg["source_url"],
                          "identifier": s["identifier"], "datePublished": s["datePublished"]}],
            "reviewedBy": {"@type": "Person", "name": "Esther Bodde", "honorificPrefix": "Dr",
                           "jobTitle": "Cosmetic & Medical Physician"},
            "author": {"@type": "Person", "name": "Malcolm Smith", "jobTitle": "Founder, Skingenetix"},
            "publisher": {"@type": "Organization", "name": "Skingenetix", "url": BASE},
            "isPartOf": {"@type": "WebSite", "url": BASE},
            # our page is an appraisal OF the paper; it is never itself a ScholarlyArticle
            "mainEntity": {"@type": "Article", "headline": h1, "inLanguage": loc,
                           "isBasedOn": {"@type": "ScholarlyArticle", "name": s["name"],
                                         "identifier": s["identifier"], "url": cfg["source_url"],
                                         "datePublished": s["datePublished"],
                                         "publication": {"@type": "Periodical", "name": s["journal"]}}}}


def fields(cfg, loc):
    intro = [("h1", sx.t(cfg["h1"], loc)),
             ("p", "*" + sx.t(cfg["byline"], loc) + "*"),
             ("p", sx.t(cfg["answer"], loc)),
             ("p", sx.t(cfg["verdict"], loc))]
    return {"h1": sx.t(cfg["h1"], loc),
            "intro": spg.rich(intro, loc),
            "reference": "",   # the citation is band 7 now; see study_sections.reference
            "sections_html": sx.render(cfg, loc),
            "seo_title": sx.t(cfg["seo_title"], loc),
            "seo_description": sx.t(cfg["seo_description"], loc),
            "jsonld": '<script type="application/ld+json">'
                      + json.dumps(jsonld(cfg, loc), ensure_ascii=False) + "</script>"}


def check(cfg):
    errs = []
    for loc in locales(cfg):
        v = fields(cfg, loc)
        if len(v["seo_title"]) > 60:
            errs.append(f"{loc}: SEO title {len(v['seo_title'])} chars (max 60)")
        if len(v["seo_description"]) > 160:
            errs.append(f"{loc}: SEO description {len(v['seo_description'])} chars (max 160)")
        words = len(sx.t(cfg["answer"], loc).split())
        if not 35 <= words <= 75:
            errs.append(f"{loc}: answer paragraph {words} words (want 40-60, hard 35-75)")
        if v["intro"].count('"level":1') != 1:
            errs.append(f"{loc}: expected exactly one h1")
        if loc == "en" and HEAD_TERM.match(v["h1"]):
            errs.append("H1 leads with the bare ingredient term (cannibalises the hub)")
        missing = [p for p in cfg.get("checks", []) if p not in v["sections_html"]]
        if loc == "en" and missing:
            errs.append(f"en: verified figures missing from the page: {missing}")
        print(sx.report(cfg, loc, v["sections_html"]) + f" · seo {len(v['seo_title'])}/{len(v['seo_description'])}")
    return errs


def apply(cfg):
    locs = locales(cfg)
    en = fields(cfg, "en")
    payload = [{"key": k, "value": v} for k, v in en.items()]
    payload += [{"key": "pubmed_url", "value": cfg["source_url"]},
                {"key": "hub", "value": spg.hub_id(cfg["hub"])}]
    cap = {"publishable": {"status": "ACTIVE"}}
    ex = gql('query($h:MetaobjectHandleInput!){ metaobjectByHandle(handle:$h){ id } }',
             {"h": {"type": "study", "handle": cfg["handle"]}})["metaobjectByHandle"]
    if ex:
        r = gql('mutation($id:ID!,$m:MetaobjectUpdateInput!){ metaobjectUpdate(id:$id, metaobject:$m)'
                '{ metaobject{ id } userErrors{ field message } } }',
                {"id": ex["id"], "m": {"fields": payload, "capabilities": cap}})["metaobjectUpdate"]
    else:
        r = gql('mutation($m:MetaobjectCreateInput!){ metaobjectCreate(metaobject:$m)'
                '{ metaobject{ id } userErrors{ field message } } }',
                {"m": {"type": "study", "handle": cfg["handle"], "fields": payload,
                       "capabilities": cap}})["metaobjectCreate"]
    if r["userErrors"]:
        sys.exit(f"  ✗ {r['userErrors']}")
    rid = r["metaobject"]["id"]
    print(f"  ✓ {cfg['handle']}: {'updated' if ex else 'created'}, ACTIVE, English")

    trans = [l for l in locs if l != "en"]
    if not trans:
        print("  · no translations in this config yet — English serves every locale until they land")
        return
    time.sleep(3)   # the translatable index lags the write
    tc = {c["key"]: c for c in gql(
        'query($id:ID!){ translatableResource(resourceId:$id){ translatableContent{ key value digest } } }',
        {"id": rid})["translatableResource"]["translatableContent"]}
    t = [{"locale": l, "key": k, "value": v, "translatableContentDigest": tc[k]["digest"]}
         for l in trans for k, v in fields(cfg, l).items() if k in tc]
    for i in range(0, len(t), 50):
        rr = gql('mutation($id:ID!,$t:[TranslationInput!]!){ translationsRegister(resourceId:$id, translations:$t)'
                 '{ userErrors{ message } } }', {"id": rid, "t": t[i:i + 50]})["translationsRegister"]
        if rr["userErrors"]:
            sys.exit(f"  ✗ translations: {rr['userErrors']}")
    print(f"  ✓ {len(t)} translations registered across {len(trans)} locales")


def verify(cfg):
    bad = 0
    for loc in locales(cfg):
        url = f"{BASE}{'' if loc == 'en' else '/' + loc}/pages/study/{cfg['handle']}"
        html = spg._get(url + f"?v={time.time()}")
        h1 = [H.unescape(re.sub(r"<[^>]+>", "", x)).strip() for x in re.findall(r"<h1[^>]*>(.*?)</h1>", html, re.S)]
        want = sx.t(cfg["h1"], loc)
        bands = html.count('<section class="sty__band')
        ld = all(json.loads(b) for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S))
        page = re.sub(r"<(style|script)\b.*?</\1>", "", html, flags=re.S)   # a CSS selector is not a link
        dead = [h for h in set(re.findall(
            r'href="(/[a-z]{2}/(?:pages|products|collections)/[^"#?]+|/(?:pages|products|collections)/[^"#?]+)"', page))
            if h.count("/") <= 4 and "study/" not in h and spg._status(BASE + h) != 200][:3]
        ok = h1 == [want] and bands == 6 and ld and not dead
        bad += not ok
        print(f"  {'✓' if ok else '✗'} {loc}: h1 {'ok' if h1 == [want] else h1}, bands {bands}/6, "
              f"tables {page.count('<table')}, JSON-LD {'valid' if ld else 'INVALID'}"
              + (f", dead: {dead}" if dead else ""))
        time.sleep(1)
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--verify-live", action="store_true")
    a = ap.parse_args()
    cfg = json.loads(pathlib.Path(a.config).read_text())
    print(f"  {cfg['handle']} · locales {', '.join(locales(cfg))}")
    if a.verify_live:
        return 1 if verify(cfg) else 0
    errs = check(cfg)
    for e in errs:
        print("  ✗", e)
    if errs:
        return 1
    print("  ✓ all checks pass")
    if a.apply:
        apply(cfg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
