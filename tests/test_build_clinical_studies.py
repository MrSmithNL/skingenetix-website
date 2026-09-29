"""Offline tests for scripts/build-clinical-studies.py — the transforms that turn a hub's evidence table
into a block of the Clinical studies index. No Shopify calls.

Run:  python3 -m pytest tests/ -q
"""
import importlib.util
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
_s = importlib.util.spec_from_file_location("bcs", ROOT / "scripts/build-clinical-studies.py")
bcs = importlib.util.module_from_spec(_s)
_argv, sys.argv = sys.argv, [sys.argv[0]]
_s.loader.exec_module(bcs)
sys.argv = _argv

HUB_TABLE = (
    '<style>.est{}</style>\n<div class="est" id="evidence-sources">\n'
    '<h2 class="est__h">Argireline Evidence &amp; Sources</h2>\n'
    '<p class="est__lead">Every study this page relies on. Graded <strong>A</strong> controlled.</p>\n'
    '<div class="est__wrap"><table><thead><tr><th>Study</th><th>Grade</th><th>What it found</th></tr></thead><tbody>'
    '<tr><td class="est__study"><p class="sgref__ti est__ti">The efficacy study of the combination</p>'
    '<p class="est__me">Raikou et al., 2017 &middot; J Cosmet Dermatol</p>'
    '<a class="est__lk" href="https://pubmed.ncbi.nlm.nih.gov/28150423/">View on PubMed &rarr;</a></td>'
    '<td class="est__grade">A</td><td>24 women.</td></tr>'
    '<tr><td class="est__study"><p class="sgref__ti est__ti">In vitro skin penetration</p>'
    '<p class="est__me">Kraeling et al., 2015 &middot; Cutan Ocul Toxicol</p>'
    '<a class="est__lk" href="https://pubmed.ncbi.nlm.nih.gov/24303801/">View on PubMed &rarr;</a></td>'
    '<td class="est__grade">C</td><td>Lab.</td></tr>'
    '</tbody></table></div>\n<p class="est__key">Published titles are quoted exactly.</p>\n</div>\n'
    '<script type="application/ld+json" id="sgx-webpage-jsonld">{"@type": "WebPage", "url": "hub"}</script>'
)
KEYS = [("Raikou", "2017", "argireline-forehead-roughness-trial-raikou-2017"),
        ("Wang", "2013", "argireline-crows-feet-trial-wang-2013")]


def run(loc="en", last=False):
    return bcs.transform(HUB_TABLE, loc, "argireline", "Argireline®", "acetyl-hexapeptide-8-research",
                         "#3E4A52", "#E9ECEE", KEYS, last)


def test_the_hubs_own_webpage_schema_is_stripped():
    """Left in, the index would carry five other pages' WebPage JSON-LD."""
    h, _ = run()
    assert "ld+json" not in h and '"WebPage"' not in h


def test_rows_are_counted_and_the_lead_links_the_hub_with_its_head_term():
    h, n = run()
    assert n == 2
    assert '<p class="est__lead">2 studies, graded.' in h
    assert 'on the <a href="/pages/acetyl-hexapeptide-8-research">Argireline®</a> research page.' in h
    assert "Graded <strong>A</strong>" not in h            # the legend moves to the intro, once


def test_a_study_with_its_own_page_gets_the_appraisal_link_and_one_without_does_not():
    h, _ = run()
    raikou, kraeling = h.split("Kraeling")[0], h.split("Kraeling")[1]
    assert 'href="/pages/study/argireline-forehead-roughness-trial-raikou-2017">Read our appraisal →</a>' in raikou
    assert "Read our appraisal" not in kraeling


def test_translated_links_carry_the_locale_prefix():
    h, _ = run("de")
    assert 'href="/de/pages/acetyl-hexapeptide-8-research"' in h
    assert 'href="/de/pages/study/argireline-forehead-roughness-trial-raikou-2017">Unsere Bewertung lesen →' in h
    assert "Argireline®: Studien" in h


def test_the_block_takes_its_jump_id_and_accent():
    h, _ = run()
    assert 'id="argireline"' in h and 'id="evidence-sources"' not in h
    assert '<div class="est" style="--sg-accent:#3E4A52;--sg-accent-tint:#E9ECEE"' in h


def test_the_footnote_stays_only_on_the_last_table():
    assert "est__key" not in run(last=False)[0]
    assert "est__key" in run(last=True)[0]


def test_scholarly_items_read_title_and_source():
    assert bcs.scholarly_items(HUB_TABLE) == [
        ("The efficacy study of the combination", "https://pubmed.ncbi.nlm.nih.gov/28150423/"),
        ("In vitro skin penetration", "https://pubmed.ncbi.nlm.nih.gov/24303801/")]


def test_appraisal_keys_read_both_config_shapes():
    stock = json.loads((ROOT / "configs/studies/argireline-forehead-roughness-trial-raikou-2017.json").read_text())
    pilot = json.loads((ROOT / "configs/studies/argireline-crows-feet-trial-wang-2013.json").read_text())
    assert bcs.appraisal_keys([stock, pilot]) == [
        ("Raikou", "2017", "argireline-forehead-roughness-trial-raikou-2017"),
        ("Wang", "2013", "argireline-crows-feet-trial-wang-2013")]


def test_the_page_schema_is_a_collection_with_a_breadcrumb():
    ld = bcs.jsonld("de", [("T", "https://x")], ["a"], 32)
    page, crumb = ld["@graph"]
    assert page["@type"] == "CollectionPage" and page["url"].endswith("/de/pages/clinical-studies")
    assert page["mainEntity"]["numberOfItems"] == 1 and page["hasPart"][0]["url"].endswith("/de/pages/study/a")
    assert [i["name"] for i in crumb["itemListElement"]] == ["Skingenetix", "Wissenschaft", "Klinische Studien"]
