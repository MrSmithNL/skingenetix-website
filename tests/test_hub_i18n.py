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
    out = hi.localise("<a>Shop Argireline</a><a>Shop</a>", "de", phrases, {})
    assert out == "<a>SA-de</a><a>S-de</a>"


def test_localise_prefixes_internal_links_only():
    html = ('<a href="/pages/x">a</a><a href="#rba-f1">b</a>'
            '<a href="https://pubmed.ncbi.nlm.nih.gov/1/">c</a><a href="/de/pages/y">d</a>')
    out = hi.localise(html, "de", {}, {})
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


def test_rebuilds_the_live_argireline_translations_exactly():
    cfg = json.loads((ROOT / "configs/hub-i18n/acetyl-hexapeptide-8-research.json").read_text())
    values, problems = hi.build(cfg, ROOT)
    assert problems == []
    assert sorted(values) == ["evidence", "evidence_sources", "overview", "usage"]
    for sid, spec_path in cfg["sections"].items():
        spec = json.loads((ROOT / spec_path).read_text())
        live = next(a for a in spec["add_sections"] if a["id"] == sid)["section"]["settings"]["html"]
        for loc in ["en"] + LOCALES:
            assert values[sid][loc] == live[loc], (sid, loc)
