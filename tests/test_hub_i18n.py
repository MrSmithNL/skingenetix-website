"""Offline tests for scripts/hub-i18n.py — phrase-substitution translation of custom-html sections.

No Shopify calls. The last test is the regression proof: the generalised tool must rebuild, byte for
byte, the five translations the 2026-09-23 Argireline recipe put live (commit 636c674).

Run:  python3 -m pytest tests/ -q
"""
import importlib.util
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
_s = importlib.util.spec_from_file_location("hi", ROOT / "scripts/hub-i18n.py")
hi = importlib.util.module_from_spec(_s)
_s.loader.exec_module(hi)
_r = importlib.util.spec_from_file_location("sr", ROOT / "scripts/set-reviewer.py")
sr = importlib.util.module_from_spec(_r)
_r.loader.exec_module(sr)

RV = json.loads((ROOT / "configs/reviewers/esther-bodde.json").read_text())
LOCALES = ["de", "nl", "fr", "es", "it"]


def test_date_sentence_matches_set_reviewers_date_marker_in_every_locale():
    # set-reviewer.py finds the byline by this marker; a date it cannot match strands the credit
    for loc in ["en"] + LOCALES:
        s = hi.date_sentence("2026-09-23", loc)
        assert re.search(RV["date_marker"][loc], s), (loc, s)
    assert hi.date_sentence("2026-09-23", "en") == "Last reviewed 23 September 2026."
    assert hi.date_sentence("2026-09-23", "de") == "Zuletzt geprüft am 23. September 2026."
    assert hi.date_sentence("2026-09-23", "es") == "Última revisión el 23 de septiembre de 2026."


def test_localise_substitutes_longest_phrase_first():
    phrases = {"Shop": {l: "S-" + l for l in LOCALES},
               "Shop Argireline": {l: "SA-" + l for l in LOCALES}}
    out = hi.localise("<a>Shop Argireline</a><a>Shop</a>", "de", phrases, {}, {})
    assert out == "<a>SA-de</a><a>S-de</a>"


def test_localise_prefixes_internal_links_only():
    html = ('<a href="/pages/x">a</a><a href="#rba-f1">b</a>'
            '<a href="https://pubmed.ncbi.nlm.nih.gov/1/">c</a><a href="/de/pages/y">d</a>')
    out = hi.localise(html, "de", {}, {}, {})
    assert 'href="/de/pages/x"' in out
    assert 'href="#rba-f1"' in out
    assert 'href="https://pubmed.ncbi.nlm.nih.gov/1/"' in out
    assert 'href="/de/pages/y"' in out and "/de/de/" not in out


def test_check_refuses_a_structure_change():
    en = "<ul><li>One</li><li>Two</li></ul>"
    problems = hi.check(en, "<ul><li>Eins Zwei</li></ul>", "de", hi.keep_pattern([]), [])
    assert any("<li" in p for p in problems)


def test_check_flags_english_left_behind_but_not_allowed_english():
    en = "<p>Hello world</p><p>Argireline</p><p>The anti-wrinkle efficacy of a synthetic hexapeptide</p>"
    v = "<p>Hello world</p><p>Argireline</p><p>The anti-wrinkle efficacy of a synthetic hexapeptide</p>"
    problems = hi.check(en, v, "de", hi.keep_pattern(["Argireline"]),
                        ["The anti-wrinkle efficacy of a synthetic hexapeptide"])
    assert len(problems) == 1 and "Hello world" in problems[0]


def test_check_flags_cyrillic_lookalikes():
    # 2026-09-23: the Italian step 1 read "deterсa" with a Cyrillic с and а — identical on screen
    problems = hi.check("<p>cleanser</p>", "<p>deterса</p>", "it", hi.keep_pattern([]), [])
    assert any("Cyrillic" in p for p in problems)


def test_byline_keeps_set_reviewers_exact_sentence_so_remove_still_works():
    for loc in ["en"] + LOCALES:
        b = hi.bylines(RV, {l: "Checked." for l in ["en"] + LOCALES}, "2026-09-23")[loc]
        html = f"<p><em>{b}</em></p>"
        assert "Esther Bodde" in html
        assert "Esther Bodde" not in sr.remove_from_byline(html, loc, RV), loc


LD = ('<script type="application/ld+json" id="sgx-webpage-jsonld">\n'
      '{"@type": "WebPage", "@id": "https://www.skingenetix.com/pages/x#webpage", '
      '"url": "https://www.skingenetix.com/pages/x", "name": "Hello", "inLanguage": "en"}\n</script>')


def test_jsonld_is_localised_and_never_phrase_substituted():
    # 2026-09-24: the Argireline template served inLanguage "en" and the English URL on /de/ pages
    phrases = {"Hello": {l: "Hallo-" + l for l in LOCALES}}
    out = hi.localise("<p>Hello</p>" + LD, "de", phrases, {}, {"de": {"name": "Name DE"}})
    ld = json.loads(re.search(r"<script[^>]*>(.*?)</script>", out, re.S).group(1))
    assert "<p>Hallo-de</p>" in out
    assert ld["inLanguage"] == "de" and ld["name"] == "Name DE"
    assert ld["url"] == "https://www.skingenetix.com/de/pages/x"
    assert ld["@id"] == "https://www.skingenetix.com/de/pages/x#webpage"
    assert hi.localise("<p>Hello</p>" + LD, "fr", phrases, {}, {}).count('"name": "Hello"') == 1


def test_check_flags_jsonld_in_the_wrong_language():
    problems = hi.check("<p>x</p>" + LD, "<p>y</p>" + LD, "de", hi.keep_pattern([]), [])
    assert any("JSON-LD" in p for p in problems)


def _strip_ld(h):
    return re.sub(r'<script type="application/ld\+json".*?</script>', "", h, flags=re.S)


def test_rebuilds_the_live_argireline_translations_exactly():
    # byte for byte outside the JSON-LD, which the 2026-09-23 recipe left in English on every locale
    cfg = json.loads((ROOT / "configs/hub-i18n/acetyl-hexapeptide-8-research.json").read_text())
    values, problems = hi.build(cfg, ROOT)
    assert problems == []
    assert sorted(values) == ["evidence", "evidence_sources", "overview", "usage"]
    for sid, spec_path in cfg["sections"].items():
        spec = json.loads((ROOT / spec_path).read_text())
        live = next(a for a in spec["add_sections"] if a["id"] == sid)["section"]["settings"]["html"]
        for loc in ["en"] + LOCALES:
            assert _strip_ld(values[sid][loc]) == _strip_ld(live[loc]), (sid, loc)
    assert values["evidence_sources"]["en"] == next(
        a for a in json.loads((ROOT / cfg["sections"]["evidence_sources"]).read_text())["add_sections"]
        if a["id"] == "evidence_sources")["section"]["settings"]["html"]["en"]


def test_check_refuses_liquid_delimiters_that_shopify_rejects():
    # 2026-09-24: "margin:0 auto}}" in a nested @media rule made themeFilesUpsert refuse the whole template
    en = "<style>@media(min-width:9px){.a{b:c} }</style><p>x</p>"
    v = "<style>@media(min-width:9px){.a{b:c}}</style><p>y</p>"
    assert any("Liquid" in p for p in hi.check(en, v, "de", hi.keep_pattern([]), []))


# ---- block targets (2026-09-25): card and FAQ settings translated from the same phrase table ----

def _tmp_page(tmp_path):
    spec = {"template": "templates/page.x.json", "page": "x",
            "add_sections": [{"id": "key_findings_ba", "after": "evidence", "section": {
                "type": "research-before-after", "settings": {}, "block_order": ["f1"],
                "blocks": {"f1": {"type": "finding", "settings": {
                    "title": "Wrinkles Down in 8 Weeks",
                    "content": '<p>A trial in <a href="/pages/y">40 women</a>.</p>'}}}}}],
            "set": [{"at": "faq/q1/answer", "values": {"en": "<p>Twice a day.</p>"}}]}
    (tmp_path / "configs").mkdir()
    (tmp_path / "configs/spec.json").write_text(json.dumps(spec))
    (tmp_path / "configs/rv.json").write_text((ROOT / "configs/reviewers/esther-bodde.json").read_text())
    phrases = {"Wrinkles Down in 8 Weeks": {l: f"Falten-{l}" for l in LOCALES},
               "A trial in": {l: f"Studie-{l} mit" for l in LOCALES},
               "40 women": {l: f"40 Frauen-{l}" for l in LOCALES},
               "Twice a day.": {l: f"Zweimal-{l}." for l in LOCALES}}
    return {"reviewer": "configs/rv.json", "reviewed": "2026-09-25", "process_sentence": {l: "" for l in ["en"] + LOCALES},
            "keep_english": [], "verbatim_fragments": [], "phrases": phrases,
            "sections": {"key_findings_ba/f1/title": "configs/spec.json",
                         "key_findings_ba/f1/content": "configs/spec.json",
                         "faq/q1/answer": "configs/spec.json"}}


def test_block_setting_targets_are_translated_and_checked(tmp_path):
    cfg = _tmp_page(tmp_path)
    values, problems = hi.build(cfg, tmp_path)
    assert problems == []
    assert values["key_findings_ba/f1/title"]["it"] == "Falten-it"
    assert values["key_findings_ba/f1/content"]["de"] == '<p>Studie-de mit <a href="/de/pages/y">40 Frauen-de</a>.</p>'
    assert values["faq/q1/answer"]["fr"] == "<p>Zweimal-fr.</p>"


def test_block_target_with_an_untranslated_phrase_is_refused(tmp_path):
    cfg = _tmp_page(tmp_path)
    del cfg["phrases"]["Wrinkles Down in 8 Weeks"]
    _, problems = hi.build(cfg, tmp_path)
    assert any("key_findings_ba/f1/title" in p and "English left behind" in p for p in problems)


def test_write_puts_six_locale_values_into_block_settings_and_set_items(tmp_path):
    cfg = _tmp_page(tmp_path)
    values, _ = hi.build(cfg, tmp_path)
    hi.write_values(cfg, values, tmp_path)
    spec = json.loads((tmp_path / "configs/spec.json").read_text())
    blk = spec["add_sections"][0]["section"]["blocks"]["f1"]["settings"]
    assert blk["title"] == values["key_findings_ba/f1/title"] and set(blk["title"]) == {"en", *LOCALES}
    assert spec["set"][0]["values"]["nl"] == "<p>Zweimal-nl.</p>"
