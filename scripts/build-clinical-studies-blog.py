#!/usr/bin/env python3
"""The Clinical studies blog: /blogs/clinical-studies, one article per appraised study.

Author: Claude (Opus 5.5) for Malcolm Smith · 2026-09-29
Decision: docs/decision-clinical-studies-blog-2026-09-29.md (amends ADR-2026-09-29-C).

    python3 scripts/build-clinical-studies-blog.py                 # dry run: what would be written
    python3 scripts/build-clinical-studies-blog.py --preview       # also write the hidden-preview list spec
    python3 scripts/build-clinical-studies-blog.py --apply         # blog + list template + articles
    python3 scripts/build-clinical-studies-blog.py --verify-live [--preview]   # the list page in six languages
    python3 scripts/build-clinical-studies-blog.py --cutover       # retire /pages/study/*: 301s, web pages off

HOW THE PIECES FIT
  * The study itself stays a `study` metaobject, built by scripts/build-study-page.py. Its fields and their
    six-locale translations are untouched by the move.
  * Each blog article is a SHELL — title, excerpt, card image, date, ingredient tag, SEO fields — with one
    metafield, study.entry, pointing at the metaobject. templates/article.clinical-study.json (built by
    `study-template-build.py --article`) renders the study's designed layout through that reference.
  * The list page is the theme's stock main-blog section (templates/blog.clinical-studies.json, built through
    hub-upgrade.py so its words are translated in the same change), under a stock image band that carries the
    title, the intro and a search form scoped to the studies, with main-blog's ingredient label row under it and
    a stock rich-text band under the list linking every hub's evidence table (layout: Malcolm, 2026-09-29).
  * --preview writes the same list page as a hidden template (templates/blog.clinical-studies-preview.json),
    seen at /blogs/clinical-studies?view=clinical-studies-preview, so it is checked before visitors see it.
  * --cutover turns off the metaobject definition's web pages and redirects each /pages/study/<handle> to
    /blogs/clinical-studies/<handle>. Run it only after the articles are verified live.
"""
import argparse
import glob
import html as H
import importlib.util
import json
import pathlib
import re
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://www.skingenetix.com"
LOCALES = ["en", "de", "nl", "fr", "es", "it"]
BLOG = "clinical-studies"
BLOG_TPL = "templates/blog.clinical-studies.json"
PREVIEW = "clinical-studies-preview"
SPEC = ROOT / "configs/hub-upgrades/clinical-studies-blog.json"
PREVIEW_SPEC = ROOT / "configs/hub-upgrades/clinical-studies-blog-preview.json"
PHRASES = json.loads((ROOT / "configs/hub-i18n/clinical-studies.json").read_text())
CARDS = json.loads((ROOT / "configs/banners/clinical-studies-article-cards-2026-09-29.json").read_text())
AUTHOR = "Malcolm Smith"
# One ingredient label per article: the card badge and the label row above the list. Article tags are not
# translatable (the ARTICLE resource exposes title, body_html, summary_html, handle, meta_title and
# meta_description only), so a label must read the same in all six languages: "Copper peptide" showed in
# English on /de/, and GHK-Cu is the ingredient's own name in every locale (2026-09-29).
TAGS = {"copper": "GHK-Cu", "argireline": "Argireline", "acetyl": "Argireline", "pdrn": "PDRN",
        "matrixyl": "Matrixyl 3000", "palmitoyl": "Matrixyl 3000", "glutathione": "Glutathione"}
# The photo band above the list. Section Custom CSS refuses `background` / `background-image` (tested
# 2026-09-29), and main-blog's banner is colour-only and always renders <h1>{{ blog.title }}</h1>. So the
# visible title, the intro and the search form sit on this stock image band, and main-blog's banner text is
# hidden VISUALLY only (still the page's one <h1>, read by screen readers and crawlers), which leaves its
# label row (LABELS_LIQUID) under the photo. Borrowed from /pages/ingredients until Malcolm picks the dedicated banner from
# the science banner sheets.
BANNER = "shopify://shop_images/skingenetix-peptide-laboratory-glassware-blue-pink-serum-actives.jpg"
BANNER_MOBILE = "shopify://shop_images/skingenetix-peptide-laboratory-glassware-blue-pink-actives-mobile.jpg"
# The visible title: the blog's own title (translated with the blog), hidden from screen readers because they
# read the real <h1> in main-blog's banner a few lines later.
TITLE_LIQUID = '<p class="h1" aria-hidden="true">{{ blog.title | escape }}</p>'
# Search scoped to articles. The header's predictive search returns no articles (its request names no
# resource types), so without this a visitor cannot search the studies from the list. Theme-styled
# (.search-input, as on /search) and worded by the theme's own translated strings. A liquid setting cannot
# {% render %} a snippet, so the magnifier is inline.
SEARCH_ICON = ('<svg aria-hidden="true" focusable="false" fill="none" width="22" viewBox="0 0 24 24">'
               '<path d="m21 21-4.5-4.5M18.5 10.75a7.75 7.75 0 1 1-15.5 0 7.75 7.75 0 0 1 15.5 0Z" '
               'stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>')
SEARCH_LIQUID = ('<form class="search-input" action="{{ routes.search_url }}" method="get" role="search">'
                 '<input type="hidden" name="type" value="article">'
                 '<input type="hidden" name="options[prefix]" value="last">'
                 '<input type="search" name="q" placeholder="{{ \'search.general.search_placeholder\' | t }}" '
                 'aria-label="{{ \'search.general.title\' | t | escape }}" autocomplete="off" spellcheck="false">'
                 '<button type="submit" aria-label="{{ \'search.general.title\' | t | escape }}">'
                 + SEARCH_ICON + '</button></form>')
# The label row under the photo: main-blog's own markup (theme-styled, "All posts" in the theme's translation,
# the selected state from current_tags) with a FIXED list: every study's label, from the configs. main-blog's
# own row (show_tags) reads blog.all_tags, which this store's storefront returns empty on some requests and full on
# others: the stock row showed on 6 of 18 loads across the six locales (2026-09-29, after re-saving the blog).
# A tag page's blog.articles is already filtered, so it cannot be the source either.
LABELS_LIQUID = """{%- assign labels = '__LABELS__' | split: '|' -%}
<div class="scroll-area bleed sm:unbleed justify-items-center">
  <div class="nav-categories">
    <ul class="h-stack bold text-base" role="tablist">
      <li role="tab" aria-selected="{% if current_tags == blank %}true{% else %}false{% endif %}"><a href="{{ blog.url }}">{{ 'blog.general.all_posts' | t }}</a></li>
      {%- for tag in labels -%}
      <li role="tab" aria-selected="{% if current_tags contains tag %}true{% else %}false{% endif %}">{%- if current_tags contains tag -%}{{ tag | link_to_remove_tag: tag }}{%- else -%}{{ tag | link_to_tag: tag }}{%- endif -%}</li>
      {%- endfor -%}
    </ul>
  </div>
</div>"""
HUB_LINKS = [("label_copper", "copper-peptide-research"), ("Matrixyl 3000", "matrixyl-3000-research"),
             ("Argireline®", "acetyl-hexapeptide-8-research"), ("PDRN", "pdrn-research"),
             ("label_glutathione", "glutathione-research")]


def pre(loc):
    return "" if loc == "en" else f"/{loc}"


def p(key, loc, **kw):
    s = PHRASES[key][loc]
    for k, v in kw.items():
        s = s.replace("{" + k + "}", str(v))
    return s


# ---------------------------------------------------------------- pure mapping (tested offline)

def article_fields(cfg):
    """{locale: {title, summary, seo_title, seo_description}} from either study-config shape.

    Stock-template configs carry h1 / seo_title / seo_description per locale; the two pilots carry
    fields.intro (whose h1 block is the title) and seo[loc]. The excerpt is the SEO description: it is
    already written as the one-line answer, and it is ≤ 160 characters by the builders' own checks."""
    out = {}
    if "h1" in cfg:
        for loc in LOCALES:
            if loc in cfg["h1"]:
                out[loc] = {"title": cfg["h1"][loc], "summary": cfg["seo_description"][loc],
                            "seo_title": cfg["seo_title"][loc], "seo_description": cfg["seo_description"][loc]}
    else:
        for loc in LOCALES:
            if loc in cfg["seo"]:
                h1 = next(c for k, c in cfg["fields"]["intro"][loc] if k == "h1")
                out[loc] = {"title": h1, "summary": cfg["seo"][loc]["description"],
                            "seo_title": cfg["seo"][loc]["title"], "seo_description": cfg["seo"][loc]["description"]}
    return out


def tag_for(handle):
    return next(v for k, v in TAGS.items() if handle.startswith(k))


def study_configs():
    return [json.loads(pathlib.Path(f).read_text()) for f in sorted(glob.glob(str(ROOT / "configs/studies/*.json")))]


def study_labels():
    """Every study's ingredient label, once, in alphabetical order: the label row."""
    return sorted({tag_for(c["handle"]) for c in study_configs()})



def published(cfg):
    """The date the study page first went live: the config's own date, else the pilot launch (2026-09-22)."""
    return cfg.get("published") or "2026-09-22"


def card_for(handle):
    img = next(i for i in CARDS["images"] if f"-{handle}-card." in i["filename"])
    return {"url": f"https://www.skingenetix.com/cdn/shop/files/{img['filename']}", "altText": img["alt"]}


def blog_spec(preview=False):
    """The list page: a stock image band (title, intro, search), stock main-blog with its label row, and a
    stock rich-text band under it. preview=True targets the hidden template seen through ?view=."""
    links = {l: ", ".join(f'<a href="{pre(l)}/pages/{hub}#evidence-sources">{PHRASES[k][l] if k in PHRASES else k}</a>'
                          for k, hub in HUB_LINKS) for l in LOCALES}
    band = {l: (f'<h2>{p("grading_title", l)}</h2><p>{p("grading", l)}</p><p>{p("all_evidence", l, links=links[l])}</p>'
                f'<p>{p("shop", l, shop_link=f"""<a href="{pre(l)}/collections/all">{p("shop_link", l)}</a>""")}</p>')
            for l in LOCALES}
    spec = {
        "_about": "GENERATED by scripts/build-clinical-studies-blog.py — the Clinical studies blog list page"
                  + (" (hidden preview, seen through ?view=)." if preview else "."),
        "template": f"templates/blog.{PREVIEW}.json" if preview else BLOG_TPL,
        "page": BLOG,
    }
    if preview:
        spec.update({"create": True, "view": PREVIEW})
    spec.update({
        "add_sections": [
            {"id": "hero", "after": None, "section": {
                "type": "image-with-text-overlay",
                "blocks": {
                    "title": {"type": "liquid", "settings": {"liquid": TITLE_LIQUID}},
                    "intro": {"type": "richtext",
                              "settings": {"content": {l: f"<p>{p('blog_intro', l)}</p>" for l in LOCALES}}},
                    "search": {"type": "liquid", "settings": {"liquid": SEARCH_LIQUID}}},
                "block_order": ["title", "intro", "search"],
                # the study pages' own banner (templates/article.clinical-study.json): same height, overlay,
                # white text, left on desktop and top-centre on phones
                "settings": {"full_width": True, "allow_transparent_header": False, "enable_parallax": False,
                             "image_size": "sm", "image": BANNER, "mobile_image": BANNER_MOBILE,
                             "mobile_text_position": "place-self-start-center text-center",
                             "desktop_text_position": "sm:place-self-center-start sm:text-start",
                             "text_color": "#ffffff", "overlay_color": "#1A1A1A", "overlay_opacity": 28}}},
            {"id": "labels", "after": "hero", "section": {
                "type": "custom-liquid",
                "settings": {"liquid": LABELS_LIQUID.replace("__LABELS__", "|".join(study_labels())),
                             "full_width": True, "remove_vertical_spacing": True, "remove_horizontal_spacing": False}}},
            {"id": "main", "after": "labels", "section": {
                "type": "main-blog",
                "settings": {"allow_transparent_header": False, "show_newsletter_form": False, "show_tags": False,
                             "articles_per_page": 12, "feature_first_article": True, "show_excerpt": True,
                             "show_date": True, "show_author": False, "show_comments_count": False,
                             "show_category": True, "banner_text_color": "#1A1A1A", "banner_background": "#F0F0F0",
                             "content": ""}}},
            {"id": "grading", "after": "main", "section": {
                "type": "rich-text",
                "blocks": {"t": {"type": "richtext", "settings": {"content": band}}},
                "block_order": ["t"],
                "settings": {"full_width": True, "content_width": "medium", "text_position": "start",
                             "background": "#F0F0F0"}}},
        ],
        "remove_sections": ["start"],
        "section_css": {
            # phones: the science pages' darker overlay (60) under white text; the search field under the intro
            "hero": ["@media screen and (max-width: 699px) { .content-over-media::before { background-color: rgb(26 26 26 / 0.6); } }",
                     ".search-input {max-width: 26rem; margin-block-start: var(--spacing-6); border-color: rgb(255 255 255 / 0.7);}",
                     "@media screen and (max-width: 699px) { .search-input {margin-inline: auto;} }",
                     # the theme's 50% placeholder measured 2.7:1 over the phone photo's blue flask (2026-09-29)
                     ".search-input > input::placeholder {color: rgb(255 255 255 / 0.85);}"],
            # the ingredient label on each card: the theme's primary badge is purple, off-brand here. The banner's
            # <h1> is hidden visually only (the title shows on the photo); the label row is its own section (LABELS_LIQUID).
            "main": [".badge--primary {background-color: #E4E6E7; color: #2E3233;}",
                     ".blog-banner-content {position: absolute; width: 1px; height: 1px; overflow: hidden; clip-path: inset(50%); white-space: nowrap;}"],
            "grading": [".rich-text {justify-content: center;}", ".prose {max-width: 66ch; margin-inline: auto;}"]},
    })
    return spec


def list_page_problems(page, title, handles):
    """What is wrong with one locale's rendered list page: one <h1> (the blog title), the title on the photo,
    the label row, the article search form, and a link to every article."""
    page = H.unescape(page)
    text = lambda s: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()
    out = []
    h1 = [text(x) for x in re.findall(r"<h1[^>]*>(.*?)</h1>", page, re.S)]
    if h1 != [title]:
        out.append(f"expected one <h1> {title!r}, found {h1}")
    if not re.search(r'aria-hidden="true"[^>]*>\s*' + re.escape(title) + r"\s*<", page):
        out.append("the title on the photo is missing")
    if "nav-categories" not in page:
        out.append("no label row")
    if not ('role="search"' in page and 'name="type" value="article"' in page):
        out.append("no search form scoped to the studies")
    out += [f"article {h} not listed" for h in handles if f"/blogs/{BLOG}/{h}" not in page]
    return out


def verify_live(handles, preview=False, intro=True):
    """The list page in six languages, read with curl (Cloudflare throttles Python's client)."""
    bad = 0
    for loc in LOCALES:
        url = f"{BASE}{pre(loc)}/blogs/{BLOG}" + (f"?view={PREVIEW}&" if preview else "?") + f"v={int(time.time())}"
        page = subprocess.run(["curl", "-s", "-L", "-A", "Mozilla/5.0", url], capture_output=True,
                              timeout=60).stdout.decode("utf-8", "ignore")
        problems = list_page_problems(page, p("title", loc), handles)
        if intro and p("blog_intro", loc) not in H.unescape(page):
            problems.append(f"the intro is not in {loc}")
        bad += bool(problems)
        print(f"  {'✓' if not problems else '✗'} {loc}: {url}")
        for x in problems:
            print(f"      {x}")
    return bad


# ---------------------------------------------------------------- Shopify side

def _load(name, path):
    s = importlib.util.spec_from_file_location(name, ROOT / path)
    m = importlib.util.module_from_spec(s)
    argv, sys.argv = sys.argv, [sys.argv[0]]
    s.loader.exec_module(m)
    sys.argv = argv
    return m


def ensure_blog(gql):
    b = gql('query{ blogs(first:20){ nodes{ id handle templateSuffix } } }')["blogs"]["nodes"]
    hit = next((x for x in b if x["handle"] == BLOG), None)
    if hit:
        return hit["id"]
    r = gql('mutation($b:BlogCreateInput!){ blogCreate(blog:$b){ blog{ id } userErrors{ field message } } }',
            {"b": {"title": p("title", "en"), "handle": BLOG, "templateSuffix": BLOG, "commentPolicy": "CLOSED"}})["blogCreate"]
    if r["userErrors"]:
        sys.exit(f"  ✗ blogCreate: {r['userErrors']}")
    print("  ✓ blog created")
    return r["blog"]["id"]


def register(gql, rid, values_by_key):
    """values_by_key: {key: {locale: value}} — registered against the current digests."""
    tc = {c["key"]: c for c in gql('query($id:ID!){ translatableResource(resourceId:$id){ translatableContent{ key value digest } } }',
                                   {"id": rid})["translatableResource"]["translatableContent"]}
    t = [{"locale": l, "key": k, "value": v, "translatableContentDigest": tc[k]["digest"]}
         for k, per in values_by_key.items() if k in tc for l, v in per.items() if l != "en" and v]
    for i in range(0, len(t), 50):
        r = gql('mutation($id:ID!,$t:[TranslationInput!]!){ translationsRegister(resourceId:$id, translations:$t)'
                '{ userErrors{ message } } }', {"id": rid, "t": t[i:i + 50]})["translationsRegister"]
        if r["userErrors"]:
            sys.exit(f"  ✗ translations {rid}: {r['userErrors']}")
    return len(t)


def upsert_article(gql, blog_id, cfg):
    handle = cfg["handle"]
    f = article_fields(cfg)
    mo = gql('query($h:MetaobjectHandleInput!){ metaobjectByHandle(handle:$h){ id } }',
             {"h": {"type": "study", "handle": handle}})["metaobjectByHandle"]
    if not mo:
        sys.exit(f"  ✗ {handle}: no study metaobject")
    fields = {"title": f["en"]["title"], "summary": f["en"]["summary"], "body": "",
              "author": {"name": AUTHOR}, "image": card_for(handle), "tags": [tag_for(handle)],
              "templateSuffix": "clinical-study", "isPublished": True, "publishDate": published(cfg) + "T09:00:00Z",
              "metafields": [
                  {"namespace": "study", "key": "entry", "type": "metaobject_reference", "value": mo["id"]},
                  {"namespace": "global", "key": "title_tag", "type": "single_line_text_field", "value": f["en"]["seo_title"]},
                  {"namespace": "global", "key": "description_tag", "type": "multi_line_text_field",
                   "value": f["en"]["seo_description"]}]}
    ex = gql('query($q:String!){ articles(first:5, query:$q){ nodes{ id handle blog{ handle } } } }',
             {"q": f"handle:{handle}"})["articles"]["nodes"]
    ex = next((a for a in ex if a["blog"]["handle"] == BLOG), None)
    if ex:
        r = gql('mutation($id:ID!,$a:ArticleUpdateInput!){ articleUpdate(id:$id, article:$a){ article{ id } userErrors{ field message } } }',
                {"id": ex["id"], "a": fields})["articleUpdate"]
    else:
        r = gql('mutation($a:ArticleCreateInput!){ articleCreate(article:$a){ article{ id } userErrors{ field message } } }',
                {"a": {**fields, "blogId": blog_id, "handle": handle}})["articleCreate"]
    if r["userErrors"]:
        sys.exit(f"  ✗ {handle}: {r['userErrors']}")
    aid = r["article"]["id"]
    n = register(gql, aid, {"title": {l: v["title"] for l, v in f.items()},
                            "summary_html": {l: v["summary"] for l, v in f.items()},
                            "meta_title": {l: v["seo_title"] for l, v in f.items()},
                            "meta_description": {l: v["seo_description"] for l, v in f.items()}})
    print(f"  ✓ {handle}: {'updated' if ex else 'created'} · {len(f)} locale(s) · {n} translations · tag {tag_for(handle)}")
    return aid


def cutover(gql, handles):
    d = gql('query{ metaobjectDefinitionByType(type:"study"){ id } }')["metaobjectDefinitionByType"]["id"]
    for h in handles:
        r = gql('mutation($r:UrlRedirectInput!){ urlRedirectCreate(urlRedirect:$r){ urlRedirect{ id } userErrors{ field message } } }',
                {"r": {"path": f"/pages/study/{h}", "target": f"/blogs/{BLOG}/{h}"}})["urlRedirectCreate"]
        print(f"  {'✓' if not r['userErrors'] else '·'} /pages/study/{h} → /blogs/{BLOG}/{h} {r['userErrors'] or ''}")
    r = gql('mutation($id:ID!,$d:MetaobjectDefinitionUpdateInput!){ metaobjectDefinitionUpdate(id:$id, definition:$d)'
            '{ metaobjectDefinition{ capabilities{ onlineStore{ enabled } } } userErrors{ field message } } }',
            {"id": d, "d": {"capabilities": {"onlineStore": {"enabled": False}}}})["metaobjectDefinitionUpdate"]
    print("  web pages for study entries:", r["metaobjectDefinition"]["capabilities"]["onlineStore"] if not r["userErrors"] else r["userErrors"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--cutover", action="store_true")
    ap.add_argument("--preview", action="store_true", help="also write the hidden-preview list spec")
    ap.add_argument("--verify-live", action="store_true", help="check the list page in six languages")
    a = ap.parse_args()
    configs = study_configs()
    if a.verify_live:
        return 1 if verify_live([c["handle"] for c in configs], preview=a.preview) else 0
    spec = blog_spec()
    SPEC.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n")
    if a.preview:
        PREVIEW_SPEC.write_text(json.dumps(blog_spec(preview=True), indent=2, ensure_ascii=False) + "\n")
        print(f"  preview spec written to {PREVIEW_SPEC.relative_to(ROOT)}: python3 scripts/hub-upgrade.py "
              f"{PREVIEW_SPEC.relative_to(ROOT)} --apply, then /blogs/{BLOG}?view={PREVIEW}")
    for c in configs:
        f = article_fields(c)
        print(f"  {c['handle']:<52} {len(f)} locale(s) · {tag_for(c['handle'])} · {published(c)} · {f['en']['title'][:60]}")
    if not (a.apply or a.cutover):
        print(f"  list-page spec written to {SPEC.relative_to(ROOT)} — dry run, nothing else written")
        return 0
    hu = _load("hu", "scripts/hub-upgrade.py")
    if a.cutover:
        cutover(hu.gql, [c["handle"] for c in configs])
        return 0
    blog_id = ensure_blog(hu.gql)
    register(hu.gql, blog_id, {"title": {l: p("title", l) for l in LOCALES}})
    try:
        hu.read_file(BLOG_TPL)
    except IndexError:
        hu.upload(BLOG_TPL, "", {"sections": {"start": {"type": "rich-text", "blocks": {}, "block_order": [], "settings": {}}},
                                 "order": ["start"]})
    for c in configs:
        upsert_article(hu.gql, blog_id, c)
    print(f"  next: python3 scripts/hub-upgrade.py {SPEC.relative_to(ROOT)} --apply   (the list page)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
