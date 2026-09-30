"""Offline tests for scripts/build-clinical-studies-blog.py — config → article mapping and the list-page spec.

Run:  python3 -m pytest tests/ -q
"""
import importlib.util
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
_s = importlib.util.spec_from_file_location("bcb", ROOT / "scripts/build-clinical-studies-blog.py")
bcb = importlib.util.module_from_spec(_s)
_argv, sys.argv = sys.argv, [sys.argv[0]]
_s.loader.exec_module(bcb)
sys.argv = _argv

STOCK = json.loads((ROOT / "configs/studies/argireline-forehead-roughness-trial-raikou-2017.json").read_text())
PILOT = json.loads((ROOT / "configs/studies/argireline-crows-feet-trial-wang-2013.json").read_text())


def test_a_stock_template_config_maps_to_an_article():
    f = bcb.article_fields(STOCK)
    assert list(f) == ["en"]                                         # Raikou is English-only so far
    assert f["en"]["title"] == STOCK["h1"]["en"]
    assert f["en"]["summary"] == STOCK["seo_description"]["en"] and len(f["en"]["summary"]) <= 160


def test_a_pilot_config_maps_to_an_article_in_all_six_languages():
    f = bcb.article_fields(PILOT)
    assert sorted(f) == sorted(bcb.LOCALES)
    assert f["de"]["title"] == next(c for k, c in PILOT["fields"]["intro"]["de"] if k == "h1")
    assert f["en"]["seo_title"] == PILOT["seo"]["en"]["title"]


def test_tags_dates_and_card_images():
    assert bcb.tag_for("argireline-crows-feet-trial-wang-2013") == "Argireline"
    # article tags cannot be translated (not in the ARTICLE translatable keys), so a label must read the same in
    # all six languages: "Copper peptide" showed in English on /de/ (2026-09-29)
    assert bcb.tag_for("copper-peptide-wrinkle-trial-badenhorst-2016") == "GHK-Cu"
    assert bcb.published(STOCK) == STOCK["published"] and bcb.published(PILOT) == "2026-09-22"
    c = bcb.card_for("pdrn-vs-retinol-split-face-trial-ye-2026")
    assert c["url"].endswith("skingenetix-clinical-study-pdrn-vs-retinol-split-face-trial-ye-2026-card.jpg") and c["altText"]


def _section(spec, sid):
    return next(a["section"] for a in spec["add_sections"] if a["id"] == sid)


def test_the_list_page_is_the_stock_blog_with_one_h1_and_translated_words():
    spec = bcb.blog_spec()
    main = _section(spec, "main")
    assert main["type"] == "main-blog" and main["settings"]["show_newsletter_form"] is False
    band = _section(spec, "grading")["blocks"]["t"]["settings"]["content"]
    assert 'href="/de/pages/glutathione-research#evidence-sources">Glutathion</a>' in band["de"]
    assert "<h1" not in json.dumps(spec)                               # main-blog's banner carries the only H1


def test_the_evidence_band_has_no_grade_key():
    """Malcolm, 2026-09-30: "yes remove grade key" — no card shows a grade, so the key explained nothing (critic F6).
    The band keeps the links to each ingredient's graded evidence, under an already-translated heading."""
    band = _section(bcb.blog_spec(), "grading")["blocks"]["t"]["settings"]["content"]
    for l in bcb.LOCALES:
        assert "<strong>A</strong>" not in band[l] and bcb.p("grading_title", l) not in band[l]
        assert band[l].startswith(f"<h2>{bcb.p('index_title', l)}</h2>")
    assert "Studien nach Wirkstoff" in band["de"] and "research-page" not in band["en"]


def test_the_label_row_filters_the_list_by_ingredient():
    """Malcolm, 2026-09-29: labels show and the list sorts by label, as on the Hairgenetix blog (supersedes "tags off
    until ~12 articles"). main-blog's own row (show_tags) reads blog.all_tags, which this store's storefront returns
    empty on some requests (the stock row showed on 6 of 18 loads, 2026-09-29), and a tag page's blog.articles is
    already filtered. blogs[blog.handle].articles is not (checked on /tagged/pdrn), so the labels are every live
    article's tags: no hand-typed list, no label that opens an empty page (critic F12)."""
    spec = bcb.blog_spec()
    assert [a["id"] for a in spec["add_sections"]] == ["hero", "labels", "main", "grading"]
    main = _section(spec, "main")
    assert main["settings"]["show_tags"] is False and main["settings"]["show_category"] is True
    row = _section(spec, "labels")
    assert row["type"] == "custom-liquid"
    liquid = row["settings"]["liquid"]
    assert "blogs[blog.handle].articles" in liquid and "all_tags" not in liquid
    assert "/tagged/{{ tag | handleize }}" in liquid and "aria-current" in liquid and "current_tags contains tag" in liquid


def test_the_label_row_is_readable_and_tappable():
    """Critic F1/F13/F16: full-ink labels (the theme's 50% ones measured 3.24:1), the current one underlined,
    44px targets, a visible focus ring, wrapping instead of a clipped scroll row, and plain links in a <nav>, not tabs.
    link_to_tag is not used: it adds a "Show products matching tag" tooltip, in English, on every locale."""
    liquid = _section(bcb.blog_spec(), "labels")["settings"]["liquid"]
    assert "<nav" in liquid and 'role="tab' not in liquid and "link_to_tag" not in liquid
    assert "min-height: 44px" in liquid and "focus-visible" in liquid and "flex-wrap: wrap" in liquid
    assert "opacity" not in liquid
    assert "Alle Studien" in liquid and "Studien nach Wirkstoff filtern" in liquid   # its own words, six languages


def test_interface_words_are_written_per_locale():
    """Liquid settings are not translatable, so the list's own words are a case on the storefront locale."""
    case = bcb.by_locale("search_studies")
    assert case.startswith("{%- case request.locale.iso_code -%}") and case.endswith("{%- endcase -%}")
    for loc in ("de", "nl", "fr", "es", "it"):
        assert f"{{%- when '{loc}' -%}}{bcb.p('search_studies', loc)}" in case
    assert "{%- else -%}Search the studies" in case


def test_the_title_sits_on_the_photo_and_the_one_h1_stays_in_main_blog():
    """Malcolm, 2026-09-29: the title showed in a grey band under the photo instead of on it. main-blog's banner
    is colour-only and always renders <h1>{{ blog.title }}</h1>, so the visible title moves onto the stock image
    band (hidden from screen readers, which read the real H1) and main-blog's banner text is hidden visually only:
    the page keeps exactly one <h1>, the blog's own translated title, and main-blog's banner keeps the label row."""
    spec = bcb.blog_spec()
    hero = _section(spec, "hero")
    assert hero["type"] == "image-with-text-overlay" and hero["settings"]["image"].startswith("shopify://shop_images/")
    assert hero["block_order"] == ["title", "intro", "search"]
    title = hero["blocks"]["title"]
    assert title["type"] == "liquid" and "{{ blog.title" in title["settings"]["liquid"]
    assert 'aria-hidden="true"' in title["settings"]["liquid"] and "<h1" not in title["settings"]["liquid"]
    assert 'class="h0"' in title["settings"]["liquid"]              # critic F8: the page's largest type
    assert sorted(hero["blocks"]["intro"]["settings"]["content"]) == sorted(bcb.LOCALES)
    assert _section(spec, "main")["settings"]["content"] == ""         # the intro moved onto the photo
    css = " ".join(spec["section_css"]["main"])
    assert ".blog-banner-content" in css and "display: none" not in css and "clip-path: inset(50%)" in css


def test_the_search_box_searches_the_studies_only():
    """Malcolm, 2026-09-29: every study searchable. The header's predictive search returns no articles, so the
    band carries a theme-styled search form scoped to articles, named for what it searches (critic F7), with a
    visible focus mark and 44px targets (critic F3)."""
    liquid = _section(bcb.blog_spec(), "hero")["blocks"]["search"]["settings"]["liquid"]
    assert 'action="{{ routes.search_url }}"' in liquid and 'name="type" value="article"' in liquid
    assert 'type="search" name="q"' in liquid and "Studien durchsuchen" in liquid
    assert "search_placeholder" not in liquid                          # the theme's German says "Gib etwas ein..."
    assert ":focus-within" in liquid and "min-height: 44px" in liquid
    assert "{% render" not in liquid                                   # liquid settings cannot render snippets


def test_each_article_body_carries_its_searchable_text():
    """Critic F2: Shopify's search found "raikou", "badenhorst" and "hexapeptide" nowhere, because every article
    body was empty (the study lives in a metaobject the search does not read). The body is never rendered by
    templates/article.clinical-study.json, so it carries the study's own approved words for search: the answer,
    the definition and the citation, or the pilot's verdict and reference, as plain text."""
    b = bcb.search_body(STOCK)
    assert list(b) == ["en"] and "Raikou" in b["en"] and "hexapeptide" in b["en"].lower()
    assert "**" not in b["en"] and "](" not in b["en"] and b["en"].startswith("<p>")
    w = bcb.search_body(PILOT)
    assert sorted(w) == sorted(bcb.LOCALES) and "Wang Y" in w["de"]
    assert "Appraised by" not in w["en"] and "<h2" not in w["en"]


def test_section_css_stays_within_what_shopify_accepts():
    for sid, rules in bcb.blog_spec()["section_css"].items():
        assert sum(len(r) for r in rules) <= 500, sid
        assert not any(__import__("re").search(r"(?<![\w-])content\s*:", r) for r in rules), sid


def test_the_preview_spec_builds_a_hidden_template_seen_through_view():
    spec = bcb.blog_spec(preview=True)
    assert spec["template"] == "templates/blog.clinical-studies-preview.json"
    assert spec["create"] is True and spec["view"] == "clinical-studies-preview"
    live = bcb.blog_spec()
    assert "create" not in live and "view" not in live and live["template"] == bcb.BLOG_TPL
    assert spec["add_sections"] == live["add_sections"]


def test_list_page_problems_reads_one_h1_the_labels_and_the_search_form():
    good = ('<h1 class="h0">Klinische Studien</h1><p class="h1" aria-hidden="true">Klinische Studien</p>'
            '<nav class="sgx-labels"><a href="/de/blogs/clinical-studies">Alle Studien</a>'
            '<a href="/de/blogs/clinical-studies/tagged/pdrn">PDRN</a></nav>'
            '<form action="/de/search" method="get" role="search"><input type="hidden" name="type" value="article">'
            '<a href="/de/blogs/clinical-studies/x-2013">')
    assert bcb.list_page_problems(good, "Klinische Studien", ["x-2013"]) == []
    two = good.replace('<p class="h1"', '<h1 class="h1"').replace("</p>", "</h1>", 1)
    assert "one <h1>" in bcb.list_page_problems(two, "Klinische Studien", ["x-2013"])[0]
    bad = bcb.list_page_problems(good.replace("sgx-labels", "x").replace('value="article"', ""),
                                 "Klinische Studien", ["x-2013", "y-2016"])
    assert any("label row" in p for p in bad) and any("search" in p for p in bad) and any("y-2016" in p for p in bad)


def test_a_pilot_study_gets_the_pilot_article_template():
    """The stock template printed seven empty headings and the reference twice under a pilot (audit
    2026-09-29); a re-run of this builder must not switch the pilots back to it."""
    assert bcb.template_suffix(PILOT) == "clinical-study-pilot"
    assert bcb.template_suffix(STOCK) == "clinical-study"
