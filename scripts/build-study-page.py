#!/usr/bin/env python3
"""Publish a study page into the theme's stock sections, from configs/studies/<handle>.json.

Author: Claude (Opus 5) for Malcolm Smith · 2026-09-24
Template: scripts/study-template-build.py · Spec: docs/study-page-template.md

    python3 scripts/build-study-page.py configs/studies/<handle>.json           # dry run
    python3 scripts/build-study-page.py configs/studies/<handle>.json --apply   # publish
    python3 scripts/build-study-page.py configs/studies/<handle>.json --verify-live

The page is nine stock Impact sections (image-with-text-overlay, impact-text, rich-text,
specification-table, media-with-text) whose settings read this study's metaobject fields.
Nothing is custom HTML except the chart, and that is a stock `liquid` block.

So this script's job is: take the config's structured content, turn each piece into the field
type its section setting expects, and write all of them.

  rich_text_field    Shopify rich-text JSON, via study-pages.rich(); markdown **bold**, *italic*
                     and [label](url) are parsed, HTML is NOT — html_to_md() converts first
  single_line / url  plain text
  multi_line         raw HTML (the chart only)
  file_reference     a MediaImage gid

WHAT IT ENFORCES before anything goes live
  * exactly one H1, and it may not open with the bare ingredient term (cannibalises the hub)
  * SEO title <= 60 characters, description <= 160, per locale
  * the answer paragraph is 35-75 words — the block an AI engine lifts whole
  * every probe in the config's "checks" list survives into the published fields
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
LOCALES = ["en", "de", "nl", "fr", "es", "it"]
HEAD_TERM = re.compile(r"(?i)^(pdrn|argireline|copper peptide|ghk-cu|matrixyl|glutathione|acetyl)\b")


def _load(name, path):
    s = importlib.util.spec_from_file_location(name, ROOT / path)
    m = importlib.util.module_from_spec(s)
    argv, sys.argv = sys.argv, [sys.argv[0]]        # these modules parse args at import
    s.loader.exec_module(m)
    sys.argv = argv
    return m


spg = _load("spg", "scripts/study-pages.py")
gql = spg.gql
hc = _load("hc", "scripts/hub_charts.py")


# ---------------------------------------------------------------- content conversion

def t(v, loc):
    """A localisable value: {"en": ...} or a plain string used for every locale."""
    if isinstance(v, dict):
        return v[loc] if loc in v else v["en"]
    return v


def html_to_md(s):
    """The configs were written for raw HTML; rich_text fields want markdown and real characters."""
    s = re.sub(r"<a [^>]*href=['\"]([^'\"]+)['\"][^>]*>(.*?)</a>", r"[\2](\1)", s, flags=re.S)
    s = re.sub(r"</?(strong|b)>", "**", s)
    s = re.sub(r"</?(em|i)>", "*", s)
    s = re.sub(r"<br\s*/?>", " ", s)
    s = re.sub(r"</?p>", "", s)
    return H.unescape(s).strip()


def para(v, loc):
    return ("p", html_to_md(t(v, loc)))


# --- HTML emitters -------------------------------------------------------------------------
# The prose fields are multi_line_text_field holding HTML, NOT rich_text_field. Shopify's
# `| metafield_tag` filter wraps rich text in <div class="metafield-rich_text_field">, and
# trafilatura — what AI crawlers and our auditor read — discards that div wholesale. Measured
# on the live page 2026-09-24: 214 words extracted with the wrapper, 941 without it.

_MD = re.compile(r"\*\*(.+?)\*\*|\*(.+?)\*|\[([^\]]+)\]\(([^)]+)\)")


def md_html(s):
    """Markdown -> inline HTML. The configs are authored in markdown, like the rest of the store."""
    def sub(m):
        if m.group(1):
            return f"<strong>{m.group(1)}</strong>"
        if m.group(2):
            return f"<em>{m.group(2)}</em>"
        url = m.group(4)
        ext = url.startswith("http")
        return (f'<a href="{url}"{" target=_blank rel=noopener" if ext else ""}>{m.group(3)}</a>')
    return _MD.sub(sub, s)


def ps(items, loc):
    """Paragraphs."""
    return "".join(f"<p>{md_html(html_to_md(t(v, loc)))}</p>" for v in items)


def inline(v, loc):
    """Inline markup with no wrapping <p> — for settings that supply their own."""
    return md_html(html_to_md(t(v, loc)))


def inline_ps(items, loc):
    """Several paragraphs for a setting that wraps the first and last itself."""
    return "</p><p>".join(md_html(html_to_md(t(v, loc))) for v in items)


# ---------------------------------------------------------------- the field set

def locales(cfg):
    return [l for l in LOCALES if l == "en" or l in cfg["h1"]]


def jsonld(cfg, loc):
    url = f"{BASE}{'' if loc == 'en' else '/' + loc}/pages/study/{cfg['handle']}"
    h1, desc = t(cfg["h1"], loc), t(cfg["seo_description"], loc)
    s = cfg["scholarly"]
    cite = {"@type": "ScholarlyArticle", "name": s["name"], "url": cfg["source_url"],
            "identifier": s["identifier"], "datePublished": s["datePublished"]}
    return {"@context": "https://schema.org", "@type": "WebPage", "@id": url + "#webpage", "url": url,
            "name": h1, "description": desc, "inLanguage": loc,
            "lastReviewed": cfg["read_at_source"],
            "datePublished": cfg.get("published", cfg["read_at_source"]),
            "dateModified": cfg["read_at_source"],
            "citation": [cite],
            "reviewedBy": {"@type": "Person", "name": "Esther Bodde", "honorificPrefix": "Dr",
                           "jobTitle": "Cosmetic & Medical Physician"},
            "author": {"@type": "Person", "name": "Malcolm Smith", "jobTitle": "Founder, Skingenetix"},
            "publisher": {"@type": "Organization", "name": "Skingenetix", "url": BASE},
            "isPartOf": {"@type": "WebSite", "url": BASE},
            # our page appraises the paper; it is never itself a ScholarlyArticle
            "hasPart": {"@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": t(q, loc),
                 "acceptedAnswer": {"@type": "Answer",
                                    "text": re.sub(r"<[^>]+>", "", html_to_md(t(a, loc)))}}
                for q, a in zip(cfg["faq"]["questions"], cfg["faq"]["answers"])]},
            "mainEntity": {"@type": "Article", "headline": h1, "inLanguage": loc,
                           "isBasedOn": {**cite, "publication": {"@type": "Periodical",
                                                                 "name": s["journal"]}}}}


def fields(cfg, loc):
    """Every translatable field, keyed as the template's section settings read them."""
    f = {
        "eyebrow": t(cfg["eyebrow"], loc),
        # the banner carries the question and a one-line deck; the byline sits below it
        "hero_text": f"<h1>{inline(cfg['h1'], loc)}</h1>" + ps([cfg["deck"]], loc),
        # definition first: the auditors scored the page 3/10 for having none, and it is the
        # sentence an engine quotes when asked "what is copper peptide"
        "intro": (f"<p><em>{inline(cfg['byline'], loc)}</em></p>"
                  + ps([cfg["definition"], cfg["answer"], cfg["verdict"]], loc)),
        "seo_title": t(cfg["seo_title"], loc),
        "seo_description": t(cfg["seo_description"], loc),
        "chart_html": hc.render_group({"$chart": ["c"]}, {"c": cfg["measurements"]["chart"]}, loc),
        "story": inline_ps(cfg["media"]["body"], loc),
        # the heading is the media block's own title and the <ol> is in the template
        "limits": "".join(f"<li>{inline(x, loc)}</li>" for x in cfg["limits"]["items"]),
        "meaning": (f"<h2>{inline(cfg['meaning']['heading'], loc)}</h2>"
                    + ps(cfg["meaning"]["body"], loc)),
        "context_html": inline_ps(cfg["context"]["body"], loc),
        "reference": f"<h2>{ {'en':'Reference','de':'Quelle','nl':'Bron','fr':'Référence','es':'Referencia','it':'Fonte'}[loc] }</h2>"
                     + ps([cfg["citation"], cfg["source_note"]], loc),
        "jsonld": '<script type="application/ld+json">'
                  + json.dumps(jsonld(cfg, loc), ensure_ascii=False) + "</script>",
    }
    for i, ans in enumerate(cfg["faq"]["answers"], 1):
        f[f"faq_a{i}"] = inline(ans, loc)
    for i, fig in enumerate(cfg["figures"], 1):
        f[f"fig{i}_value"] = html_to_md(t(fig["n"], loc))
        f[f"fig{i}_label"] = html_to_md(t(fig["label"], loc))
        f[f"fig{i}_body"] = inline(fig["note"], loc)
    for i, row in enumerate(cfg["glance"]["rows"], 1):
        f[f"g{i}"] = inline(row["v"], loc)
    return f


def links(cfg, loc):
    """URL fields. Not translatable, so the locale prefix is baked in per locale."""
    pre = "" if loc == "en" else "/" + loc
    return {"hub_url": BASE + pre + cfg["meaning"]["ctas"][0]["href"],
            "product_url": BASE + pre + cfg["meaning"]["ctas"][1]["href"]}


# ---------------------------------------------------------------- checks

def check(cfg):
    errs = []
    for loc in locales(cfg):
        v = fields(cfg, loc)
        if len(v["seo_title"]) > 60:
            errs.append(f"{loc}: SEO title {len(v['seo_title'])} chars (max 60)")
        if len(v["seo_description"]) > 160:
            errs.append(f"{loc}: SEO description {len(v['seo_description'])} chars (max 160)")
        if v["hero_text"].count("<h1") != 1:
            errs.append(f"{loc}: expected exactly one h1 in the banner")
        words = len(t(cfg["answer"], loc).split())
        if not 35 <= words <= 75:
            errs.append(f"{loc}: answer paragraph {words} words (want 40-60)")
        if loc == "en" and HEAD_TERM.match(t(cfg["h1"], loc)):
            errs.append("H1 leads with the bare ingredient term (cannibalises the hub)")
        blob = json.dumps(v, ensure_ascii=False)
        missing = [p for p in cfg.get("checks", []) if p not in blob and html_to_md(p) not in blob]
        if loc == "en" and missing:
            errs.append(f"en: verified figures missing from the page: {missing}")
        print(f"  {loc:3} {len(v)} fields · chart {len(v['chart_html']):>6} chars · "
              f"glance {len(cfg['glance']['rows'])} rows · limits {len(cfg['limits']['items'])} · "
              f"seo {len(v['seo_title'])}/{len(v['seo_description'])}")
    return errs


# ---------------------------------------------------------------- publish

def media_gid(stem):
    for n in gql('query($q:String!){ files(first:20, query:$q){ nodes{ ... on MediaImage '
                 '{ id image{ url } } } } }', {"q": stem})["files"]["nodes"]:
        if stem in ((n.get("image") or {}).get("url") or ""):
            return n["id"]
    sys.exit(f"REFUSING: no media file matching {stem!r}")


def apply(cfg):
    payload = [{"key": k, "value": v} for k, v in {**fields(cfg, "en"), **links(cfg, "en")}.items()]
    for key, stem in (("banner", cfg["banner"]), ("banner_mobile", cfg["banner_mobile"]),
                      ("story_image", cfg["media"]["image"].rsplit(".", 1)[0])):
        payload.append({"key": key, "value": media_gid(stem)})
    # the old single-blob field is retired by this template; blank it so nothing stale can render
    payload.append({"key": "sections_html", "value": ""})

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
    print(f"  ✓ {cfg['handle']}: {'updated' if ex else 'created'}, ACTIVE, {len(payload)} fields (English)")

    trans = [l for l in locales(cfg) if l != "en"]
    if not trans:
        print("  · no translations in this config yet — English serves every locale until they land")
        return
    time.sleep(3)                                    # the translatable index lags the write
    tc = {c["key"]: c for c in gql(
        'query($id:ID!){ translatableResource(resourceId:$id){ translatableContent{ key value digest } } }',
        {"id": rid})["translatableResource"]["translatableContent"]}
    t_in = [{"locale": l, "key": k, "value": v, "translatableContentDigest": tc[k]["digest"]}
            for l in trans for k, v in fields(cfg, l).items() if k in tc]
    for i in range(0, len(t_in), 50):
        rr = gql('mutation($id:ID!,$t:[TranslationInput!]!){ translationsRegister(resourceId:$id, translations:$t)'
                 '{ userErrors{ message } } }', {"id": rid, "t": t_in[i:i + 50]})["translationsRegister"]
        if rr["userErrors"]:
            sys.exit(f"  ✗ translations: {rr['userErrors']}")
    print(f"  ✓ {len(t_in)} translations across {len(trans)} locales")


def verify(cfg):
    bad = 0
    for loc in locales(cfg):
        url = f"{BASE}{'' if loc == 'en' else '/' + loc}/pages/study/{cfg['handle']}"
        html = spg._get(url + f"?v={time.time()}")
        h1 = [H.unescape(re.sub(r"<[^>]+>", "", x)).strip() for x in re.findall(r"<h1[^>]*>(.*?)</h1>", html, re.S)]
        want = t(cfg["h1"], loc)
        page = re.sub(r"<(style|script)\b.*?</\1>", "", html, flags=re.S)
        ld = all(json.loads(b) for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S))
        banner = cfg["banner"] in html
        leftover = "{{ metaobject" in page          # a setting that did not resolve
        dead = [h for h in set(re.findall(
            r'href="(/[a-z]{2}/(?:pages|products|collections)/[^"#?]+|/(?:pages|products|collections)/[^"#?]+)"', page))
            if h.count("/") <= 4 and "study/" not in h and spg._status(BASE + h) != 200][:3]
        ok = h1 == [want] and ld and banner and not leftover and not dead
        bad += not ok
        print(f"  {'✓' if ok else '✗'} {loc}: h1 {'ok' if h1 == [want] else h1}, banner "
              f"{'ok' if banner else 'MISSING'}, tables {page.count('<table')}, "
              f"JSON-LD {'valid' if ld else 'INVALID'}"
              + (", UNRENDERED LIQUID" if leftover else "") + (f", dead: {dead}" if dead else ""))
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
