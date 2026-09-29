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
    assert bcb.tag_for("copper-peptide-wrinkle-trial-badenhorst-2016") == "Copper peptide"
    assert bcb.published(STOCK) == STOCK["published"] and bcb.published(PILOT) == "2026-09-22"
    c = bcb.card_for("pdrn-vs-retinol-split-face-trial-ye-2026")
    assert c["url"].endswith("skingenetix-clinical-study-pdrn-vs-retinol-split-face-trial-ye-2026-card.jpg") and c["altText"]


def test_the_list_page_is_the_stock_blog_with_one_h1_and_translated_words():
    spec = bcb.blog_spec()
    main = next(a["section"] for a in spec["add_sections"] if a["id"] == "main")
    assert main["type"] == "main-blog" and main["settings"]["show_newsletter_form"] is False
    assert main["settings"]["show_tags"] is False                     # tag archives stay off (thin pages)
    assert sorted(main["settings"]["content"]) == sorted(bcb.LOCALES)
    band = next(a["section"] for a in spec["add_sections"] if a["id"] == "grading")["blocks"]["t"]["settings"]["content"]
    assert 'href="/de/pages/glutathione-research#evidence-sources">Glutathion</a>' in band["de"]
    assert "<h1" not in json.dumps(spec)                               # the blog banner carries the only H1


def test_the_picture_band_sits_above_the_list_and_carries_no_heading():
    """Section CSS refuses background images (2026-09-29), so the image is a stock band with no text above
    main-blog, whose own banner stays the page's one <h1>."""
    spec = bcb.blog_spec()
    order = [a["id"] for a in spec["add_sections"]]
    assert order == ["hero", "main", "grading"]
    hero = spec["add_sections"][0]["section"]
    assert hero["type"] == "image-with-text-overlay" and hero["blocks"] == {}
    assert hero["settings"]["image"].startswith("shopify://shop_images/")
    assert spec["section_css"]["main"] == [".badge--primary {background-color: #E4E6E7; color: #2E3233;}"]
