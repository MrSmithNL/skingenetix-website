#!/usr/bin/env python3
"""Publish a study page into the theme's stock sections, from configs/studies/<handle>.json.

Author: Claude (Opus 5) for Malcolm Smith · 2026-09-24
Template: scripts/study-template-build.py · Spec: docs/study-page-template.md

    python3 scripts/build-study-page.py configs/studies/<handle>.json           # dry run
    python3 scripts/build-study-page.py configs/studies/<handle>.json --apply   # publish
    python3 scripts/build-study-page.py configs/studies/<handle>.json --apply --draft   # save, not public
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
  * every PubMed / PMC / DOI link resolves to a paper whose authors and year match its label, and the
    JSON-LD isBasedOn title is that identifier's own title (network: NCBI + Crossref; fails closed)
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
# Studies are articles in the Clinical studies blog since 2026-09-29 (docs/decision-clinical-studies-blog-2026-09-29.md);
# the old /pages/study/<handle> addresses redirect here.
PATH = "/blogs/clinical-studies/"
PHRASES = json.loads((ROOT / "configs/hub-i18n/clinical-studies.json").read_text())
# breadcrumb's last step: the ingredient, named as its hub names it, linking to the hub
CRUMB = {"copper": ("label_copper", "copper-peptide-research"), "argireline": ("Argireline®", "acetyl-hexapeptide-8-research"),
         "acetyl": ("Argireline®", "acetyl-hexapeptide-8-research"), "pdrn": ("PDRN", "pdrn-research"),
         "matrixyl": ("Matrixyl 3000", "matrixyl-3000-research"), "palmitoyl": ("Matrixyl 3000", "matrixyl-3000-research"),
         "glutathione": ("label_glutathione", "glutathione-research")}
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
        ext = url.startswith("http") and "skingenetix.com" not in url   # our own pages stay in the tab
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


def _pre(loc):
    return "" if loc == "en" else "/" + loc


def crumb_parts(cfg, loc):
    key, hub = next(v for k, v in CRUMB.items() if cfg["handle"].startswith(k))
    label = PHRASES[key][loc] if key in PHRASES else key
    return [(PHRASES["science"][loc], f"{_pre(loc)}/pages/the-science"),
            (PHRASES["title"][loc], f"{_pre(loc)}/blogs/clinical-studies"),
            (label, f"{_pre(loc)}/pages/{hub}")]


def jsonld(cfg, loc):
    url = f"{BASE}{_pre(loc)}{PATH}{cfg['handle']}"
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
            # from the config, so `set-reviewer.py --remove` can take it off (it was hard-coded until 2026-09-26)
            **({"reviewedBy": cfg["reviewer"]} if cfg.get("reviewer") else {}),
            "author": {"@type": "Person", "name": "Malcolm Smith", "jobTitle": "Founder, Skingenetix"},
            "publisher": {"@type": "Organization", "name": "Skingenetix", "url": BASE},
            "isPartOf": {"@type": "Blog", "name": PHRASES["title"][loc], "url": f"{BASE}{_pre(loc)}/blogs/clinical-studies"},
            "breadcrumb": {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": i, "name": n, "item": BASE + u}
                for i, (n, u) in enumerate([("Skingenetix", _pre(loc) + "/")] + crumb_parts(cfg, loc)[:2]
                                           + [(h1, url[len(BASE):])], 1)]},
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
        # Science › Clinical studies › ingredient — in the banner field, so it translates with the banner
        "hero_text": ('<p class="sg-crumb">' + " › ".join(f'<a href="{u}">{n}</a>' for n, u in crumb_parts(cfg, loc))
                      + f"</p><h1>{inline(cfg['h1'], loc)}</h1>" + ps([cfg["deck"]], loc)),
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


# ---------------------------------------------------------------- one section per result, and "how it works"
# Malcolm, 2026-10-01: "every study blog article should have separate content sections for each of the proven trial
# outcomes with before and after images where this can be used (similar to the ingredient science pages). And these
# should also be separate content blocks for the proven working active effects of what was tested".
#
# The study entry is full (40 of 40 fields, read live 2026-10-01), so both live in a companion entry of type
# `study_detail`, under the study's own handle, which the article reaches through the metafield study.detail
# (study.draft_detail on the English-first route). The template has fixed slots; a slot this study does not use is
# written empty, and the research-before-after section draws nothing for an empty slot.
#
# Config keys (both optional; a config with neither builds exactly as before and writes no companion entry):
#   "outcomes":   {"heading": {...}, "items": [{"title", "body": [...], "image",
#                                               "before_after": true, "after": {...}, "result": {...}}]}
#   "mechanisms": {"heading": {...}, "items": [{"title", "body": [...], "image", "evidence"}]}
# To take the sections off a study that had them, keep the keys with "items": [] — every slot is then cleared.

OUTCOME_SLOTS, MECHANISM_SLOTS = 4, 3
DETAIL_TYPE = "study_detail"
_TEXT, _PROSE, _FILE = "single_line_text_field", "multi_line_text_field", "file_reference"
DETAIL_FIELDS = ([("outcomes_heading", _TEXT), ("mechanism_heading", _TEXT)]
                 + [(f"o{i}_{k}", kind) for i in range(1, OUTCOME_SLOTS + 1)
                    for k, kind in (("title", _TEXT), ("before", _TEXT), ("after", _TEXT), ("result", _TEXT),
                                    ("body", _PROSE), ("image", _FILE))]
                 + [(f"m{j}_{k}", kind) for j in range(1, MECHANISM_SLOTS + 1)
                    for k, kind in (("title", _TEXT), ("body", _PROSE), ("image", _FILE))])
# the science pages' own words for the label (configs/hub-upgrades/acetyl-hexapeptide-8-evidence-merge-2026-09-23.json)
BEFORE = {"en": "Before", "de": "Vorher", "nl": "Voor", "fr": "Avant", "es": "Antes", "it": "Prima"}
# Malcolm, 2026-09-24: every content image on an ingredient's page names that ingredient in its filename
INGREDIENT_TERMS = {"copper": ("copper-peptide", "ghk-cu"), "argireline": ("argireline", "acetyl-hexapeptide"),
                    "acetyl": ("argireline", "acetyl-hexapeptide"), "pdrn": ("pdrn", "polynucleotide"),
                    "matrixyl": ("matrixyl", "palmitoyl"), "palmitoyl": ("matrixyl", "palmitoyl"),
                    "glutathione": ("glutathione", "gssg")}
# Where a mechanism was shown, and the words its English text must use to say so. The claims registers keep mechanism
# detail "framed as laboratory findings" — never as what happens in the reader's skin.
EVIDENCE = {"laboratory": ("laborator",), "skin samples": ("skin sample", "laborator"), "people": ()}
RESULT_MAX = 64          # the result pill is one line over a 660px picture at desktop width


def _items(cfg, key):
    return (cfg.get(key) or {}).get("items") or []


def detail_fields(cfg, loc):
    """The companion entry's text fields for one locale, or None for a config with neither key."""
    if "outcomes" not in cfg and "mechanisms" not in cfg:
        return None
    outs, mechs = _items(cfg, "outcomes"), _items(cfg, "mechanisms")
    f = {"outcomes_heading": html_to_md(t(cfg["outcomes"].get("heading", ""), loc)) if outs else "",
         "mechanism_heading": html_to_md(t(cfg["mechanisms"].get("heading", ""), loc)) if mechs else ""}
    for i in range(1, OUTCOME_SLOTS + 1):
        o = outs[i - 1] if i <= len(outs) else {}
        pair = bool(o.get("before_after"))
        f[f"o{i}_title"] = html_to_md(t(o.get("title", ""), loc))
        f[f"o{i}_before"] = BEFORE[loc] if pair else ""
        f[f"o{i}_after"] = html_to_md(t(o.get("after", ""), loc)) if pair else ""
        f[f"o{i}_result"] = html_to_md(t(o.get("result", ""), loc)) if pair else ""
        f[f"o{i}_body"] = inline_ps(o.get("body", []), loc)
    for j in range(1, MECHANISM_SLOTS + 1):
        m = mechs[j - 1] if j <= len(mechs) else {}
        f[f"m{j}_title"] = html_to_md(t(m.get("title", ""), loc))
        f[f"m{j}_body"] = inline_ps(m.get("body", []), loc)
    return f


def detail_images(cfg):
    """(field, file stem) for every image slot; None where the slot is unused."""
    outs, mechs = _items(cfg, "outcomes"), _items(cfg, "mechanisms")
    stem = lambda item: item["image"].rsplit(".", 1)[0] if item.get("image") else None   # noqa: E731
    return ([(f"o{i}_image", stem(outs[i - 1]) if i <= len(outs) else None) for i in range(1, OUTCOME_SLOTS + 1)]
            + [(f"m{j}_image", stem(mechs[j - 1]) if j <= len(mechs) else None)
               for j in range(1, MECHANISM_SLOTS + 1)])


def _missing_locales(v, locs):
    """Locales a localisable value lacks. A plain string serves every locale (an image name, a flag)."""
    return [l for l in locs if isinstance(v, dict) and l not in v]


def check_detail(cfg, english_only=False):
    """Problems with the results and how-it-works sections, before anything is written.

    english_only: the English-first preview. Otherwise every text must carry each of the study's languages: t() falls
    back to English, and an English-only block on a six-language study would be registered as five "translations".
    """
    outs, mechs = _items(cfg, "outcomes"), _items(cfg, "mechanisms")
    if not outs and not mechs:
        return []
    errs = []
    locs = [] if english_only else [l for l in locales(cfg) if l != "en"]
    for key, items in (("outcomes", outs), ("mechanisms", mechs)):
        lack = _missing_locales(cfg[key].get("heading", ""), locs) if items else []
        errs += [f"{key}: heading has no {', '.join(lack)}"] if lack else []
    for slot, item in [(f"o{i}", o) for i, o in enumerate(outs, 1)] + [(f"m{j}", m) for j, m in enumerate(mechs, 1)]:
        for k in ("title", "after", "result"):
            lack = _missing_locales(item.get(k, ""), locs)
            errs += [f"{slot}: {k} has no {', '.join(lack)}"] if lack else []
        lack = sorted({l for p in item.get("body", []) for l in _missing_locales(p, locs)})
        errs += [f"{slot}: body has no {', '.join(lack)}"] if lack else []
    if len(outs) > OUTCOME_SLOTS:
        errs.append(f"{len(outs)} results: the template has {OUTCOME_SLOTS} slots")
    if len(mechs) > MECHANISM_SLOTS:
        errs.append(f"{len(mechs)} mechanisms: the template has {MECHANISM_SLOTS} slots")
    for key, items in (("outcomes", outs), ("mechanisms", mechs)):
        if items and not t(cfg[key].get("heading", ""), "en"):
            errs.append(f"{key}: no section heading")
    terms = next((v for k, v in INGREDIENT_TERMS.items() if cfg["handle"].startswith(k)), ())
    on_page = [cfg["banner"], cfg["banner_mobile"], cfg["media"]["image"].rsplit(".", 1)[0]]
    for slot, item in [(f"o{i}", o) for i, o in enumerate(outs, 1)] + [(f"m{j}", m) for j, m in enumerate(mechs, 1)]:
        errs += [f"{slot}: no {need}" for need in ("title", "body", "image") if not item.get(need)]
        img = (item.get("image") or "").rsplit(".", 1)[0]
        if img and terms and not any(x in img.lower() for x in terms):
            errs.append(f"{slot}: image {img!r} does not name the ingredient ({' / '.join(terms)})")
        on_page += [img] if img else []
    for i, o in enumerate(outs, 1):
        if not o.get("before_after"):
            if o.get("after") or o.get("result"):
                errs.append(f"o{i}: after/result labels on a plain photograph (set before_after only for a before/after picture)")
            continue
        errs += [f"o{i}: a before/after needs its {need} label" for need in ("after", "result") if not o.get(need)]
        result = o.get("result") or {}
        for loc, label in (result.items() if isinstance(result, dict) else [("en", result)]):
            if len(html_to_md(label)) > RESULT_MAX:
                errs.append(f"o{i} {loc}: result label is {len(html_to_md(label))} characters (max {RESULT_MAX})")
    for j, m in enumerate(mechs, 1):
        ev = m.get("evidence")
        if ev not in EVIDENCE:
            errs.append(f"m{j}: evidence must be one of: {', '.join(EVIDENCE)}")
        elif EVIDENCE[ev]:
            text = " ".join(t(p, "en") for p in m.get("body", [])).lower()
            if not any(w in text for w in EVIDENCE[ev]):
                errs.append(f"m{j}: a {ev} finding must say so in its text ('{EVIDENCE[ev][0]}…')")
    twice = sorted({x for x in on_page if on_page.count(x) > 1})
    if twice:
        errs.append(f"image used twice on the page: {', '.join(twice)}")
    return errs


def detail_link_key(draft):
    """The article metafield that points at the companion entry: the live one, or the English-first draft's."""
    return "draft_detail" if draft else "detail"


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
        # the result and how-it-works blocks are on the page too, so a verified figure may live there alone
        blob = json.dumps({**v, **(detail_fields(cfg, loc) or {})}, ensure_ascii=False)
        missing = [p for p in cfg.get("checks", []) if p not in blob and html_to_md(p) not in blob]
        if loc == "en" and missing:
            errs.append(f"en: verified figures missing from the page: {missing}")
        print(f"  {loc:3} {len(v)} fields · chart {len(v['chart_html']):>6} chars · "
              f"glance {len(cfg['glance']['rows'])} rows · limits {len(cfg['limits']['items'])} · "
              f"results {len(_items(cfg, 'outcomes'))} · how it works {len(_items(cfg, 'mechanisms'))} · "
              f"seo {len(v['seo_title'])}/{len(v['seo_description'])}")
    return errs


# ---------------------------------------------------------------- citation identity
# Added 2026-09-26. On 2026-09-25 "Pickart et al., 2015" went live linked to PMID 26236125, a dental
# paper, on the one section of a YMYL page that tells readers where the evidence sits. Nothing checked
# that an identifier belongs to the paper named beside it, so this refuses to publish until every
# PubMed / PMC / DOI link resolves to a record whose authors and year match its label, and the
# JSON-LD `isBasedOn` title is the identifier's own title.
# Rule 12 note: seo-toolkit's content_engine/adapters/pubmed_adapter.py searches PubMed but does not
# verify an identifier; this belongs there once two projects use it (docs/todo.md STUDY-CITE).

_CITE = re.compile(r"\[([^\]]+)\]\((https?://(?:pubmed\.ncbi\.nlm\.nih\.gov/(\d+)|(?:dx\.)?doi\.org/(10\.[^)\s]+?)"
                   r"|pmc\.ncbi\.nlm\.nih\.gov/articles/(PMC\d+)|www\.ncbi\.nlm\.nih\.gov/pmc/articles/(PMC\d+))/?)\)")
_LABEL = re.compile(r"^\s*([A-ZÀ-Ý][\w'’À-ÿ-]+).*?\b((?:19|20)\d{2})\b")


def _strings(node):
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for k, v in node.items():
            if k == "en" or not (len(k) == 2 and k in LOCALES):   # translations share the English URLs
                yield from _strings(v)
    elif isinstance(node, list):
        for v in node:
            yield from _strings(v)


def citation_links(cfg):
    """(label, kind, id) for every PubMed, PMC and DOI link in the config, markdown or raw <a>."""
    out = []
    for s in _strings(cfg):
        for m in _CITE.finditer(html_to_md(s)):
            if m.group(3):
                out.append((m.group(1), "pmid", m.group(3)))
            elif m.group(4):
                out.append((m.group(1), "doi", m.group(4)))
            else:
                out.append((m.group(1), "pmc", m.group(5) or m.group(6)))
    return out


def _fold(s):
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c)).lower()


def _title_key(s):
    return re.sub(r"[^a-z0-9]+", " ", _fold(H.unescape(re.sub(r"<[^>]+>", "", s)))).strip()


def check_citations(cfg, resolve):
    """Errors for every identifier that fails to resolve, names other authors or another year, and for a
    JSON-LD title that is not its identifier's title. `resolve(kind, id)` -> {title, surnames, year} | None."""
    errs, seen = [], set()
    for label, kind, ident in citation_links(cfg):
        if (label, kind, ident) in seen:
            continue
        seen.add((label, kind, ident))
        rec = resolve(kind, ident)
        if not rec:
            errs.append(f"citation {kind}:{ident} ({label!r}) did not resolve")
            continue
        m = _LABEL.match(label)
        if not m:                                     # "doi:10.…" names no author: resolving is the check
            continue
        who, year = _fold(m.group(1)), int(m.group(2))
        names = [_fold(n) for n in rec["surnames"]]
        if not any(who == n or who in n.replace("-", " ").split() for n in names):
            errs.append(f"citation {kind}:{ident} is labelled {label!r} but its authors are "
                        f"{', '.join(rec['surnames'][:3])} — {rec['title'][:80]!r}")
        elif abs(rec["year"] - year) > 1:
            errs.append(f"citation {kind}:{ident} is labelled {label!r} but was published in {rec['year']}")
    s = cfg.get("scholarly")
    if s:
        ident = re.sub(r"(?i)^(pmid:?\s*|doi:?\s*|https?://(dx\.)?doi\.org/)", "", s["identifier"]).strip()
        kind = "pmid" if ident.isdigit() else "pmc" if ident.upper().startswith("PMC") else "doi"
        rec = resolve(kind, ident)
        if not rec:
            errs.append(f"JSON-LD isBasedOn {kind}:{ident} did not resolve")
        elif _title_key(rec["title"]) != _title_key(s["name"]):
            errs.append(f"JSON-LD isBasedOn title is not the title of {kind}:{ident} — "
                        f"the record's title is {rec['title']!r}")
    return errs


def resolve_live(kind, ident, _cache={}):
    """NCBI esummary for PubMed and PMC, Crossref for a DOI. None on any failure: the check fails closed."""
    import urllib.parse
    import urllib.request
    if (kind, ident) in _cache:
        return _cache[(kind, ident)]
    rec = None
    for attempt in range(3):                       # one blip from NCBI must not block a publish (2026-09-29)
        rec = _lookup(kind, ident)
        if rec:
            break
        time.sleep(2 * (attempt + 1))
    _cache[(kind, ident)] = rec
    return rec


def _lookup(kind, ident):
    import urllib.parse
    import urllib.request
    rec = None
    try:
        if kind in ("pmid", "pmc"):
            db, uid = ("pubmed", ident) if kind == "pmid" else ("pmc", ident[3:])
            time.sleep(0.4)                           # NCBI allows three requests a second without a key
            u = ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?"
                 + urllib.parse.urlencode({"db": db, "id": uid, "retmode": "json"}))
            r = json.loads(urllib.request.urlopen(u, timeout=30).read())["result"].get(uid)
            if r and not r.get("error"):
                y = re.search(r"(19|20)\d{2}", r.get("pubdate", "") or r.get("epubdate", ""))
                rec = {"title": r["title"], "year": int(y.group()) if y else 0,
                       "surnames": [a["name"].rsplit(" ", 1)[0] for a in r.get("authors", [])
                                    if a.get("authtype", "Author") == "Author"]}
        else:
            u = "https://api.crossref.org/works/" + urllib.parse.quote(ident)
            req = urllib.request.Request(u, headers={"User-Agent": "skingenetix-study-builder (mailto:info@skingenetix.com)"})
            m = json.loads(urllib.request.urlopen(req, timeout=30).read())["message"]
            parts = (m.get("issued") or m.get("published-print") or m.get("published-online") or {}).get("date-parts", [[0]])
            rec = {"title": (m.get("title") or [""])[0], "year": int(parts[0][0] or 0),
                   "surnames": [a.get("family", "") for a in m.get("author", [])]}
    except Exception as e:                            # noqa: BLE001 — any failure means "not verified"
        print(f"  · {kind}:{ident} lookup failed: {e}")
    return rec


# ---------------------------------------------------------------- publish

def media_gid(stem):
    for n in gql('query($q:String!){ files(first:20, query:$q){ nodes{ ... on MediaImage '
                 '{ id image{ url } } } } }', {"q": stem})["files"]["nodes"]:
        if stem in ((n.get("image") or {}).get("url") or ""):
            return n["id"]
    sys.exit(f"REFUSING: no media file matching {stem!r}")


PREVIEW_VIEW = "clinical-study-draft"      # templates/article.clinical-study-draft.json, reading study.draft


def draft_handle(cfg):
    """The study entry an English-first rebuild is written to, beside the live one (Malcolm, 2026-09-30)."""
    return cfg["handle"] + "-draft"


def page_url(cfg, loc, view=None, blog=None):
    path = f"/blogs/{blog}/" if blog else PATH
    return f"{BASE}{_pre(loc)}{path}{cfg['handle']}?" + (f"view={view}&" if view else "") + f"v={time.time()}"


# A NEW study has no live article whose ?view= could show its draft (2026-09-30). Its English draft is published as an
# article in a hidden, unlinked blog, on the real study template and with its own title and description, so the page
# the audit judges is the page it will become. `seo.hidden` keeps the draft out of search and the sitemap. At go-live
# the list builder creates the real article in the clinical-studies blog from the finished config, and this draft
# article is deleted (docs/study-page-template.md §3).
DRAFTS_BLOG = "clinical-studies-drafts"


def live_article(cfg):
    """The study's article in the live clinical-studies blog, or None for a study not yet published."""
    return next((a for a in gql('query($q:String!){ articles(first:10, query:$q){ nodes{ id handle blog{ handle } } } }',
                                {"q": f"handle:{cfg['handle']}"})["articles"]["nodes"]
                 if a["handle"] == cfg["handle"] and a["blog"]["handle"] == PATH.strip("/").split("/")[1]), None)


def drafts_blog_id():
    b = next((n for n in gql('query{ blogs(first:50){ nodes{ id handle } } }')["blogs"]["nodes"]
              if n["handle"] == DRAFTS_BLOG), None)
    if b:
        return b["id"]
    r = gql('mutation($b:BlogCreateInput!){ blogCreate(blog:$b){ blog{ id } userErrors{ field message } } }',
            {"b": {"title": "Clinical studies", "handle": DRAFTS_BLOG, "commentPolicy": "CLOSED"}})["blogCreate"]
    if r["userErrors"]:
        sys.exit(f"  ✗ drafts blog: {r['userErrors']}")
    # the blog's own index page lists every draft: noindex it as well (verified 2026-09-30: robots noindex,nofollow)
    h = gql('mutation($m:[MetafieldsSetInput!]!){ metafieldsSet(metafields:$m){ userErrors{ field message } } }',
            {"m": [{"ownerId": r["blog"]["id"], "namespace": "seo", "key": "hidden", "type": "number_integer",
                    "value": "1"}]})["metafieldsSet"]
    if h["userErrors"]:
        sys.exit(f"  ✗ drafts blog seo.hidden: {h['userErrors']}")
    return r["blog"]["id"]


def preview_article(cfg, detail_id=None):
    """Publish or update a new study's English draft in the hidden drafts blog. Refuses a study that is live.

    detail_id: the study's companion study_detail entry (results and how-it-works sections), linked as study.detail."""
    handle = cfg["handle"]
    found = [a for a in gql('query($q:String!){ articles(first:10, query:$q){ nodes{ id handle blog{ handle } } } }',
                            {"q": f"handle:{handle}"})["articles"]["nodes"] if a["handle"] == handle]
    elsewhere = [a["blog"]["handle"] for a in found if a["blog"]["handle"] != DRAFTS_BLOG]
    if elsewhere:
        sys.exit(f"  ✗ {handle} is already an article in {elsewhere}: preview it with ?view={PREVIEW_VIEW} instead")
    blog_id = drafts_blog_id()
    mo = gql('query($h:MetaobjectHandleInput!){ metaobjectByHandle(handle:$h){ id } }',
             {"h": {"type": "study", "handle": handle}})["metaobjectByHandle"]
    if not mo:
        sys.exit(f"  ✗ {handle}: no study entry to preview")
    art = {"title": t(cfg["h1"], "en"), "summary": t(cfg["seo_description"], "en"), "body": ps([cfg["answer"]], "en"),
           "author": {"name": "Malcolm Smith"}, "templateSuffix": "clinical-study", "isPublished": True,
           "metafields": [
               {"namespace": "study", "key": "entry", "type": "metaobject_reference", "value": mo["id"]},
               {"namespace": "global", "key": "title_tag", "type": "single_line_text_field",
                "value": t(cfg["seo_title"], "en")},
               {"namespace": "global", "key": "description_tag", "type": "multi_line_text_field",
                "value": t(cfg["seo_description"], "en")},
               {"namespace": "seo", "key": "hidden", "type": "number_integer", "value": "1"}]}
    if detail_id:
        art["metafields"].append({"namespace": "study", "key": detail_link_key(False), "type": "metaobject_reference",
                                  "value": detail_id})
    mine = next((a for a in found if a["blog"]["handle"] == DRAFTS_BLOG), None)
    if mine:
        r = gql('mutation($id:ID!,$a:ArticleUpdateInput!){ articleUpdate(id:$id, article:$a)'
                '{ article{ id } userErrors{ field message } } }', {"id": mine["id"], "a": art})["articleUpdate"]
    else:
        r = gql('mutation($a:ArticleCreateInput!){ articleCreate(article:$a){ article{ id } userErrors{ field message } } }',
                {"a": {**art, "blogId": blog_id, "handle": handle}})["articleCreate"]
    if r["userErrors"]:
        sys.exit(f"  ✗ {handle}: {r['userErrors']}")
    print(f"  ✓ draft article {'updated' if mine else 'created'} (hidden, English); preview: "
          f"{page_url(cfg, 'en', blog=DRAFTS_BLOG).split('?')[0]}")


def link_draft(cfg, detail_id=None):
    """Point the live article's study.draft metafield at the draft entry (creating the definition once), and
    study.draft_detail at the draft's companion entry when it has one."""
    study_def = gql('query{ metaobjectDefinitionByType(type:"study"){ id } }')["metaobjectDefinitionByType"]["id"]
    have = gql('query{ metafieldDefinitions(first:50, ownerType:ARTICLE, namespace:"study"){ nodes{ key } } }')
    if "draft" not in [n["key"] for n in have["metafieldDefinitions"]["nodes"]]:
        r = gql('mutation($d:MetafieldDefinitionInput!){ metafieldDefinitionCreate(definition:$d){ userErrors{ message } } }',
                {"d": {"name": "Study (draft preview)", "namespace": "study", "key": "draft", "ownerType": "ARTICLE",
                       "type": "metaobject_reference", "validations": [{"name": "metaobject_definition_id", "value": study_def}]}})
        if r["metafieldDefinitionCreate"]["userErrors"]:
            sys.exit(f"  ✗ {r['metafieldDefinitionCreate']['userErrors']}")
    mo = gql('query($h:MetaobjectHandleInput!){ metaobjectByHandle(handle:$h){ id } }',
             {"h": {"type": "study", "handle": draft_handle(cfg)}})["metaobjectByHandle"]
    art = next((a for a in gql('query($q:String!){ articles(first:5, query:$q){ nodes{ id handle blog{ handle } } } }',
                              {"q": f"handle:{cfg['handle']}"})["articles"]["nodes"] if a["blog"]["handle"] == "clinical-studies"), None)
    if not (mo and art):
        sys.exit(f"  ✗ link_draft: draft entry {bool(mo)}, article {bool(art)}")
    r = gql('mutation($m:[MetafieldsSetInput!]!){ metafieldsSet(metafields:$m){ userErrors{ message } } }',
            {"m": [{"ownerId": art["id"], "namespace": "study", "key": "draft", "type": "metaobject_reference", "value": mo["id"]}]})
    if r["metafieldsSet"]["userErrors"]:
        sys.exit(f"  ✗ {r['metafieldsSet']['userErrors']}")
    if detail_id:
        link_detail(art["id"], detail_id, draft=True)
    print(f"  ✓ article study.draft → {draft_handle(cfg)}; preview: {page_url(cfg, 'en', PREVIEW_VIEW).split('&v=')[0]}")


def apply(cfg, status="ACTIVE", entry_handle=None, english_only=False):
    """Write the study entry. entry_handle/english_only: an English-first preview written beside the live entry."""
    handle = entry_handle or cfg["handle"]
    payload = [{"key": k, "value": v} for k, v in {**fields(cfg, "en"), **links(cfg, "en")}.items()]
    for key, stem in (("banner", cfg["banner"]), ("banner_mobile", cfg["banner_mobile"]),
                      ("story_image", cfg["media"]["image"].rsplit(".", 1)[0])):
        payload.append({"key": key, "value": media_gid(stem)})
    # the old single-blob field is retired by this template; blank it so nothing stale can render
    payload.append({"key": "sections_html", "value": ""})

    cap = {"publishable": {"status": status}}   # DRAFT: saved and validated, not on the storefront
    ex = gql('query($h:MetaobjectHandleInput!){ metaobjectByHandle(handle:$h){ id } }',
             {"h": {"type": "study", "handle": handle}})["metaobjectByHandle"]
    if ex:
        r = gql('mutation($id:ID!,$m:MetaobjectUpdateInput!){ metaobjectUpdate(id:$id, metaobject:$m)'
                '{ metaobject{ id } userErrors{ field message } } }',
                {"id": ex["id"], "m": {"fields": payload, "capabilities": cap}})["metaobjectUpdate"]
    else:
        r = gql('mutation($m:MetaobjectCreateInput!){ metaobjectCreate(metaobject:$m)'
                '{ metaobject{ id } userErrors{ field message } } }',
                {"m": {"type": "study", "handle": handle, "fields": payload,
                       "capabilities": cap}})["metaobjectCreate"]
    if r["userErrors"]:
        sys.exit(f"  ✗ {r['userErrors']}")
    rid = r["metaobject"]["id"]
    print(f"  ✓ {handle}: {'updated' if ex else 'created'}, {status}, {len(payload)} fields (English)")

    register(rid, [] if english_only else [l for l in locales(cfg) if l != "en"], lambda l: fields(cfg, l))


def register(rid, trans, values):
    """Register one entry's translations: `values(locale)` -> {field: text}. Empty fields have nothing to translate."""
    if not trans:
        print("  · no translations in this config yet — English serves every locale until they land")
        return
    time.sleep(3)                                    # the translatable index lags the write
    tc = {c["key"]: c for c in gql(
        'query($id:ID!){ translatableResource(resourceId:$id){ translatableContent{ key value digest } } }',
        {"id": rid})["translatableResource"]["translatableContent"]}
    t_in = [{"locale": l, "key": k, "value": v, "translatableContentDigest": tc[k]["digest"]}
            for l in trans for k, v in values(l).items() if k in tc and v]
    for i in range(0, len(t_in), 50):
        rr = gql('mutation($id:ID!,$t:[TranslationInput!]!){ translationsRegister(resourceId:$id, translations:$t)'
                 '{ userErrors{ message } } }', {"id": rid, "t": t_in[i:i + 50]})["translationsRegister"]
        if rr["userErrors"]:
            sys.exit(f"  ✗ translations: {rr['userErrors']}")
    print(f"  ✓ {len(t_in)} translations across {len(trans)} locales")


def ensure_detail_definition():
    """The study_detail definition and the two article metafields that point at it, created once (2026-10-01).

    Mirrors the study definition: translatable, publishable, admin-only (Liquid reads it through the article).
    A field added to DETAIL_FIELDS later is added to the live definition here.
    """
    d = gql('query($t:String!){ metaobjectDefinitionByType(type:$t){ id fieldDefinitions{ key } } }',
            {"t": DETAIL_TYPE})["metaobjectDefinitionByType"]
    defs = [{"key": k, "name": k.replace("_", " ").capitalize(), "type": kind} for k, kind in DETAIL_FIELDS]
    if not d:
        r = gql('mutation($d:MetaobjectDefinitionCreateInput!){ metaobjectDefinitionCreate(definition:$d)'
                '{ metaobjectDefinition{ id } userErrors{ field message } } }',
                {"d": {"type": DETAIL_TYPE, "name": "Study detail", "fieldDefinitions": defs,
                       "capabilities": {"publishable": {"enabled": True}, "translatable": {"enabled": True}}}}
                )["metaobjectDefinitionCreate"]
        if r["userErrors"]:
            sys.exit(f"  ✗ {DETAIL_TYPE} definition: {r['userErrors']}")
        d = {"id": r["metaobjectDefinition"]["id"], "fieldDefinitions": [{"key": k} for k, _ in DETAIL_FIELDS]}
        print(f"  ✓ created the {DETAIL_TYPE} definition ({len(defs)} fields)")
    have = {f["key"] for f in d["fieldDefinitions"]}
    new = [x for x in defs if x["key"] not in have]
    if new:
        r = gql('mutation($id:ID!,$d:MetaobjectDefinitionUpdateInput!){ metaobjectDefinitionUpdate(id:$id, definition:$d)'
                '{ userErrors{ field message } } }',
                {"id": d["id"], "d": {"fieldDefinitions": [{"create": x} for x in new]}})["metaobjectDefinitionUpdate"]
        if r["userErrors"]:
            sys.exit(f"  ✗ {DETAIL_TYPE} fields: {r['userErrors']}")
    links = gql('query{ metafieldDefinitions(first:50, ownerType:ARTICLE, namespace:"study"){ nodes{ key } } }')
    for key, name in ((detail_link_key(False), "Study detail"), (detail_link_key(True), "Study detail (draft preview)")):
        if key in [n["key"] for n in links["metafieldDefinitions"]["nodes"]]:
            continue
        r = gql('mutation($d:MetafieldDefinitionInput!){ metafieldDefinitionCreate(definition:$d){ userErrors{ message } } }',
                {"d": {"name": name, "namespace": "study", "key": key, "ownerType": "ARTICLE",
                       "type": "metaobject_reference", "validations": [{"name": "metaobject_definition_id", "value": d["id"]}]}})
        if r["metafieldDefinitionCreate"]["userErrors"]:
            sys.exit(f"  ✗ study.{key}: {r['metafieldDefinitionCreate']['userErrors']}")
        print(f"  ✓ created the article metafield study.{key}")
    return d["id"]


def apply_detail(cfg, entry_handle=None, english_only=False, status="ACTIVE"):
    """Write the study's companion study_detail entry; returns its id, or None (and touches nothing) for a config
    with neither `outcomes` nor `mechanisms`."""
    en = detail_fields(cfg, "en")
    if en is None:
        return None
    ensure_detail_definition()
    handle = entry_handle or cfg["handle"]
    ex = gql('query($h:MetaobjectHandleInput!){ metaobjectByHandle(handle:$h){ id } }',
             {"h": {"type": DETAIL_TYPE, "handle": handle}})["metaobjectByHandle"]
    payload = [{"key": k, "value": v} for k, v in en.items()]
    for key, stem in detail_images(cfg):
        if stem:
            payload.append({"key": key, "value": media_gid(stem)})
        elif ex:                                     # a slot the study no longer uses: clear its picture
            payload.append({"key": key, "value": ""})
    cap = {"publishable": {"status": status}}
    if ex:
        r = gql('mutation($id:ID!,$m:MetaobjectUpdateInput!){ metaobjectUpdate(id:$id, metaobject:$m)'
                '{ metaobject{ id } userErrors{ field message } } }',
                {"id": ex["id"], "m": {"fields": payload, "capabilities": cap}})["metaobjectUpdate"]
    else:
        r = gql('mutation($m:MetaobjectCreateInput!){ metaobjectCreate(metaobject:$m)'
                '{ metaobject{ id } userErrors{ field message } } }',
                {"m": {"type": DETAIL_TYPE, "handle": handle, "fields": payload, "capabilities": cap}})["metaobjectCreate"]
    if r["userErrors"]:
        sys.exit(f"  ✗ {DETAIL_TYPE} {handle}: {r['userErrors']}")
    rid = r["metaobject"]["id"]
    print(f"  ✓ {DETAIL_TYPE} {handle}: {'updated' if ex else 'created'}, {len(_items(cfg, 'outcomes'))} results, "
          f"{len(_items(cfg, 'mechanisms'))} how-it-works blocks")
    register(rid, [] if english_only else [l for l in locales(cfg) if l != "en"], lambda l: detail_fields(cfg, l))
    return rid


def link_detail(article_id, detail_id, draft=False):
    """Point an article at its companion entry (study.detail, or study.draft_detail for the English-first preview)."""
    r = gql('mutation($m:[MetafieldsSetInput!]!){ metafieldsSet(metafields:$m){ userErrors{ message } } }',
            {"m": [{"ownerId": article_id, "namespace": "study", "key": detail_link_key(draft),
                    "type": "metaobject_reference", "value": detail_id}]})
    if r["metafieldsSet"]["userErrors"]:
        sys.exit(f"  ✗ {r['metafieldsSet']['userErrors']}")
    print(f"  ✓ article study.{detail_link_key(draft)} → {detail_id}")


def verify(cfg, view=None, blog=None):
    bad = 0
    for loc in (["en"] if view or blog else locales(cfg)):  # a preview is English-first
        html = spg._get(page_url(cfg, loc, view, blog))
        h1 = [H.unescape(re.sub(r"<[^>]+>", "", x)).strip() for x in re.findall(r"<h1[^>]*>(.*?)</h1>", html, re.S)]
        want = t(cfg["h1"], loc)
        page = re.sub(r"<(style|script)\b.*?</\1>", "", html, flags=re.S)
        ld = all(json.loads(b) for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S))
        banner = cfg["banner"] in html
        leftover = "{{ metaobject" in page          # a setting that did not resolve
        dead = [h for h in set(re.findall(
            r'href="(/[a-z]{2}/(?:pages|products|collections)/[^"#?]+|/(?:pages|products|collections)/[^"#?]+)"', page))
            if h.count("/") <= 4 and "study/" not in h and spg._status(BASE + h) != 200][:3]
        # the results and how-it-works blocks: every heading on the page, and no empty slot drawn as a grey box
        d = detail_fields(cfg, loc) or {}
        lost = [v for k, v in d.items() if k.endswith("_title") and v and v not in H.unescape(page)]
        boxes = page.count("<svg class=\"placeholder\"") if d else 0   # placeholder_svg_tag: 'placeholder'
        ok = h1 == [want] and ld and banner and not leftover and not dead and not lost and not boxes
        bad += not ok
        print(f"  {'✓' if ok else '✗'} {loc}: h1 {'ok' if h1 == [want] else h1}, banner "
              f"{'ok' if banner else 'MISSING'}, tables {page.count('<table')}, "
              f"JSON-LD {'valid' if ld else 'INVALID'}"
              + (f", result/how-it-works blocks {sum(1 for k, v in d.items() if k.endswith('_title') and v)}" if d else "")
              + (", UNRENDERED LIQUID" if leftover else "") + (f", dead: {dead}" if dead else "")
              + (f", MISSING BLOCKS: {lost}" if lost else "") + (f", {boxes} EMPTY-SLOT PLACEHOLDERS" if boxes else ""))
        time.sleep(1)
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--verify-live", action="store_true")
    ap.add_argument("--draft", action="store_true", help="with --apply: save as DRAFT (not on the storefront)")
    ap.add_argument("--preview", action="store_true",
                    help="English-first preview. A live article: write <handle>-draft, link it as the article's "
                         "study.draft, verify through ?view=clinical-study-draft (the live article is untouched). "
                         f"A new study: write its entry and a hidden, noindexed article in /blogs/{DRAFTS_BLOG}/")
    a = ap.parse_args()
    cfg = json.loads(pathlib.Path(a.config).read_text())
    print(f"  {cfg['handle']} · locales {', '.join(locales(cfg))}" + (" · PREVIEW (English, draft entry)" if a.preview else ""))
    # a live study previews through its draft entry and ?view=; a new one through the hidden drafts blog
    route = ({"view": PREVIEW_VIEW} if live_article(cfg) else {"blog": DRAFTS_BLOG}) if a.preview else {}
    if a.verify_live:
        return 1 if verify(cfg, **route) else 0
    errs = check(cfg) + check_detail(cfg, english_only=a.preview) + check_citations(cfg, resolve_live)
    for e in errs:
        print("  ✗", e)
    if errs:
        return 1
    print("  ✓ all checks pass")
    if a.apply and a.preview and "blog" in route:
        # not live yet: the entry is written under its own handle (nothing references it until the draft article)
        apply(cfg, "ACTIVE", english_only=True)
        preview_article(cfg, detail_id=apply_detail(cfg, english_only=True))
    elif a.apply and a.preview:
        # ACTIVE, not DRAFT: a storefront reference to a draft entry renders nothing. The study definition's own web
        # pages are off, so the entry has no public page; it is reached only through ?view=clinical-study-draft.
        apply(cfg, "ACTIVE", entry_handle=draft_handle(cfg), english_only=True)
        link_draft(cfg, detail_id=apply_detail(cfg, entry_handle=draft_handle(cfg), english_only=True))
    elif a.apply:
        apply(cfg, "DRAFT" if a.draft else "ACTIVE")
        did = apply_detail(cfg, status="DRAFT" if a.draft else "ACTIVE")
        art = live_article(cfg) if did else None
        if art:                                      # a study not yet live is linked by build-clinical-studies-blog.py
            link_detail(art["id"], did)
    return 0


if __name__ == "__main__":
    sys.exit(main())
