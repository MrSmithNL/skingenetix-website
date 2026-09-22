"""Offline tests for scripts/hub-upgrade.py build() — no Shopify calls.

Run:  python3 -m pytest tests/ -q
"""
import copy
import importlib.util
import json
import pathlib

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
_s = importlib.util.spec_from_file_location("hu", ROOT / "scripts/hub-upgrade.py")
hu = importlib.util.module_from_spec(_s)
_s.loader.exec_module(hu)

L6 = ["en", "de", "nl", "fr", "es", "it"]


def six(text):
    return {l: text if l == "en" else f"[{l}] {text}" for l in L6}


REF_HTML = ('<style>.sgref{}</style><div class="sgref"><h2 class="sgref__h">Published References</h2>'
            '<div class="sgref__list"><div class="sgref__r"><div><p class="sgref__ti">Old</p></div>'
            '<a class="sgref__lk" href="https://pubmed.ncbi.nlm.nih.gov/1/">View on PubMed &rarr;</a></div></div></div>')


def template():
    return {"sections": {
        "overview": {"type": "rich-text", "settings": {"background": "#ffffff"},
                     "blocks": {"op": {"type": "richtext", "settings": {"content": "<p>old</p>"}}}, "block_order": ["op"]},
        "references": {"type": "custom-html", "settings": {"html": REF_HTML}},
        "faq": {"type": "faq", "settings": {"title": "FAQ"},
                "blocks": {"q1": {"type": "item", "settings": {"title": "a", "content": "<p>b</p>"}}}, "block_order": ["q1"]},
    }, "order": ["overview", "references", "faq"]}


def keys(tt):
    return [k for k, _ in tt]


def test_add_section_extracts_every_translatable_setting():
    spec = {"add_sections": [{"id": "stats", "after": "overview", "section": {
        "type": "impact-text", "settings": {"background": "#F0F0F0"},
        "blocks": {"s1": {"type": "item", "settings": {"title": "−39%", "subheading": six("Deep-wrinkle area"),
                                                      "content": six("<p>2 months</p>")}}},
        "block_order": ["s1"]}}]}
    j = template()
    tt = hu.build(spec, j)
    assert j["order"] == ["overview", "stats", "references", "faq"]
    b = j["sections"]["stats"]["blocks"]["s1"]["settings"]
    assert b["subheading"] == "Deep-wrinkle area" and b["title"] == "−39%"
    assert set(keys(tt)) == {"stats.s1.subheading", "stats.s1.content"}


def test_add_section_is_idempotent_on_rerun():
    spec = {"add_sections": [{"id": "stats", "after": "overview", "section": {
        "type": "rich-text", "settings": {}, "blocks": {}, "block_order": []}}]}
    j = template()
    hu.build(copy.deepcopy(spec), j)
    hu.build(copy.deepcopy(spec), j)
    assert j["order"].count("stats") == 1


def test_section_level_set_uses_two_part_path():
    tt = hu.build({"set": [{"at": "faq/title", "values": six("Matrixyl 3000 FAQ")}]}, j := template())
    assert j["sections"]["faq"]["settings"]["title"] == "Matrixyl 3000 FAQ"
    assert keys(tt) == ["faq.title"]


def test_add_block_after_an_existing_block():
    spec = {"add_blocks": [{"section": "faq", "id": "q2", "after": "q1",
                            "block": {"type": "item", "settings": {"title": six("Is it safe?"), "content": six("<p>Yes.</p>")}}}]}
    tt = hu.build(spec, j := template())
    assert j["sections"]["faq"]["block_order"] == ["q1", "q2"]
    assert set(keys(tt)) == {"faq.q2.title", "faq.q2.content"}


def test_missing_locale_is_refused():
    bad = six("x")
    del bad["it"]
    with pytest.raises(SystemExit):
        hu.build({"set": [{"at": "faq/title", "values": bad}]}, template())


def test_references_rows_added_once_and_translated():
    spec = {"references_add": [{"title": "New paper", "meta": "Doe J et al., 2020", "url": "https://doi.org/10.1/x",
                                "link": "View study &rarr;"}],
            "references_i18n": {l: {"Published References": f"Refs-{l}", "View study &rarr;": f"Study-{l}",
                                    "View on PubMed &rarr;": f"PubMed-{l}"} for l in L6[1:]}}
    j = template()
    hu.build(copy.deepcopy(spec), j)
    tt = hu.build(copy.deepcopy(spec), j)          # second run must not duplicate the row
    h = j["sections"]["references"]["settings"]["html"]
    assert h.count("https://doi.org/10.1/x") == 1
    assert h.index("New paper") > h.index("Old")   # appended inside the list, after existing rows
    vals = dict(tt)["references.html"]
    assert "Refs-de" in vals["de"] and "Study-de" in vals["de"] and "PubMed-de" in vals["de"]
    assert "Published References" in vals["en"]


def test_jsonld_is_localised_per_locale():
    spec = {"jsonld": {"@type": "WebPage", "@id": "https://www.skingenetix.com/pages/x#webpage",
                       "url": "https://www.skingenetix.com/pages/x", "name": "EN name", "description": "EN d"},
            "jsonld_i18n": {l: {"name": f"name-{l}", "description": f"d-{l}"} for l in L6[1:]},
            "references_i18n": {l: {} for l in L6[1:]}}
    tt = hu.build(spec, template())
    de = dict(tt)["references.html"]["de"]
    ld = json.loads(de.split('id="sgx-webpage-jsonld">', 1)[1].split("</script>")[0])
    assert ld["name"] == "name-de" and ld["inLanguage"] == "de"
    assert ld["url"] == "https://www.skingenetix.com/de/pages/x"
    en = dict(tt)["references.html"]["en"]
    assert json.loads(en.split('id="sgx-webpage-jsonld">', 1)[1].split("</script>")[0])["inLanguage"] == "en"


def test_chart_placeholder_expands_to_six_locales():
    spec = {"charts": {"c1": {"kind": "bars", "title": six("Collagen I"), "caption": six("<p>Lab</p>"),
                              "unit": "%", "domain": [-20, 260], "series": [{"key": "a", "label": six("Change"), "color": "#016569"}],
                              "rows": [{"label": six("Both"), "values": {"a": 256}}]}},
            "add_sections": [{"id": "fig", "after": "overview", "section": {
                "type": "custom-html", "settings": {"html": {"$chart": ["c1"]}}}}]}
    tt = hu.build(spec, j := template())
    vals = dict(tt)["fig.html"]
    assert set(vals) == set(L6)
    assert "+256%" in vals["en"] and "[de] Collagen I" in vals["de"]
    for d in ("{{", "}}", "{%", "%}"):                        # custom-html rejects all four (422)
        assert all(d not in v for v in vals.values()), d
