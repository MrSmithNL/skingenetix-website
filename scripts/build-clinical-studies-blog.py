#!/usr/bin/env python3
"""The Clinical studies blog: /blogs/clinical-studies, one article per appraised study.

Author: Claude (Opus 5.5) for Malcolm Smith · 2026-09-29
Decision: docs/decision-clinical-studies-blog-2026-09-29.md (amends ADR-2026-09-29-C).

    python3 scripts/build-clinical-studies-blog.py                 # dry run: what would be written
    python3 scripts/build-clinical-studies-blog.py --apply         # blog + list template + articles
    python3 scripts/build-clinical-studies-blog.py --cutover       # retire /pages/study/*: 301s, web pages off

HOW THE PIECES FIT
  * The study itself stays a `study` metaobject, built by scripts/build-study-page.py. Its fields and their
    six-locale translations are untouched by the move.
  * Each blog article is a SHELL — title, excerpt, card image, date, ingredient tag, SEO fields — with one
    metafield, study.entry, pointing at the metaobject. templates/article.clinical-study.json (built by
    `study-template-build.py --article`) renders the study's designed layout through that reference.
  * The list page is the theme's stock main-blog section (templates/blog.clinical-studies.json, built through
    hub-upgrade.py so its words are translated in the same change), with the banner image set by the
    section's own Custom CSS and a stock rich-text band under the list linking every hub's evidence table.
  * --cutover turns off the metaobject definition's web pages and redirects each /pages/study/<handle> to
    /blogs/clinical-studies/<handle>. Run it only after the articles are verified live.
"""
import argparse
import glob
import importlib.util
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOCALES = ["en", "de", "nl", "fr", "es", "it"]
BLOG = "clinical-studies"
BLOG_TPL = "templates/blog.clinical-studies.json"
SPEC = ROOT / "configs/hub-upgrades/clinical-studies-blog.json"
PHRASES = json.loads((ROOT / "configs/hub-i18n/clinical-studies.json").read_text())
CARDS = json.loads((ROOT / "configs/banners/clinical-studies-article-cards-2026-09-29.json").read_text())
AUTHOR = "Malcolm Smith"
TAGS = {"copper": "Copper peptide", "argireline": "Argireline", "acetyl": "Argireline", "pdrn": "PDRN",
        "matrixyl": "Matrixyl 3000", "palmitoyl": "Matrixyl 3000", "glutathione": "Glutathione"}
# The picture band above the list. Section Custom CSS refuses `background` / `background-image` (tested
# 2026-09-29), and hiding main-blog's own banner would leave a second, hidden <h1>; so the image is a stock
# image band with no text, and main-blog's banner below it stays the page's one <h1>. Borrowed from
# /pages/ingredients until Malcolm picks the dedicated banner from the science banner sheets.
BANNER = "shopify://shop_images/skingenetix-peptide-laboratory-glassware-blue-pink-serum-actives.jpg"
BANNER_MOBILE = "shopify://shop_images/skingenetix-peptide-laboratory-glassware-blue-pink-actives-mobile.jpg"
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


def published(cfg):
    """The date the study page first went live: the config's own date, else the pilot launch (2026-09-22)."""
    return cfg.get("published") or "2026-09-22"


def card_for(handle):
    img = next(i for i in CARDS["images"] if f"-{handle}-card." in i["filename"])
    return {"url": f"https://www.skingenetix.com/cdn/shop/files/{img['filename']}", "altText": img["alt"]}


def blog_spec():
    """The list page: a stock image band, stock main-blog, and a stock rich-text band under it."""
    links = {l: ", ".join(f'<a href="{pre(l)}/pages/{hub}#evidence-sources">{PHRASES[k][l] if k in PHRASES else k}</a>'
                          for k, hub in HUB_LINKS) for l in LOCALES}
    band = {l: (f'<h2>{p("grading_title", l)}</h2><p>{p("grading", l)}</p><p>{p("all_evidence", l, links=links[l])}</p>'
                f'<p>{p("shop", l, shop_link=f"""<a href="{pre(l)}/collections/all">{p("shop_link", l)}</a>""")}</p>')
            for l in LOCALES}
    return {
        "_about": "GENERATED by scripts/build-clinical-studies-blog.py — the Clinical studies blog list page.",
        "template": BLOG_TPL,
        "page": BLOG,
        "add_sections": [
            {"id": "hero", "after": None, "section": {
                "type": "image-with-text-overlay", "blocks": {}, "block_order": [],
                "settings": {"full_width": True, "allow_transparent_header": False, "enable_parallax": False,
                             "image_size": "auto", "image": BANNER, "mobile_image": BANNER_MOBILE,
                             "overlay_color": "#1A1A1A", "overlay_opacity": 0}}},
            {"id": "main", "after": "hero", "section": {
                "type": "main-blog",
                "settings": {"allow_transparent_header": False, "show_newsletter_form": False, "show_tags": False,
                             "articles_per_page": 12, "feature_first_article": True, "show_excerpt": True,
                             "show_date": True, "show_author": False, "show_comments_count": False,
                             "show_category": True, "banner_text_color": "#1A1A1A", "banner_background": "#F0F0F0",
                             "content": {l: f"<p>{p('blog_intro', l)}</p>" for l in LOCALES}}}},
            {"id": "grading", "after": "main", "section": {
                "type": "rich-text",
                "blocks": {"t": {"type": "richtext", "settings": {"content": band}}},
                "block_order": ["t"],
                "settings": {"full_width": True, "content_width": "medium", "text_position": "start",
                             "background": "#F0F0F0"}}},
        ],
        "remove_sections": ["start"],
        "section_css": {
            # the ingredient label on each card: the theme's primary badge is purple, off-brand here
            "main": [".badge--primary {background-color: #E4E6E7; color: #2E3233;}"],
            "grading": [".rich-text {justify-content: center;}", ".prose {max-width: 66ch; margin-inline: auto;}"]},
    }


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
    a = ap.parse_args()
    configs = [json.loads(pathlib.Path(f).read_text()) for f in sorted(glob.glob(str(ROOT / "configs/studies/*.json")))]
    spec = blog_spec()
    SPEC.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n")
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
