"""Offline tests for scripts/study-template-build.py — the article templates.

Run:  python3 -m pytest tests/ -q

Found by the central audit on 2026-09-29: the two pilot studies (Wang 2013, Ye 2026) keep their whole
designed body in `sections_html` and leave every stock field empty, so the shared article template printed
seven empty section headings under them and the reference twice. The pilots get their own template: banner,
their body, and the structured data — nothing that reads an empty field.
"""
import importlib.util
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
_s = importlib.util.spec_from_file_location("stb", ROOT / "scripts/study-template-build.py")
stb = importlib.util.module_from_spec(_s)
_argv, sys.argv = sys.argv, [sys.argv[0]]
_s.loader.exec_module(stb)
sys.argv = _argv


def test_the_pilot_template_keeps_only_what_a_pilot_fills():
    j = stb.build_pilot_article()
    assert j["order"] == ["banner", "answer", "safety", "reference"]
    assert set(j["sections"]) == {"banner", "answer", "safety", "reference"}


def test_the_pilot_template_prints_the_reference_once():
    """The pilot body already carries its reference; the section keeps only the JSON-LD."""
    ref = stb.build_pilot_article()["sections"]["reference"]
    assert ref["block_order"] == ["ld"] and set(ref["blocks"]) == {"ld"}
    assert "jsonld" in ref["blocks"]["ld"]["settings"]["liquid"]


def test_the_pilot_template_reads_the_study_through_the_article():
    j = stb.build_pilot_article()
    body = j["sections"]["answer"]["blocks"]["l"]["settings"]["liquid"]
    assert body == "{{ article.metafields.study.entry.value.sections_html.value }}"
    assert "metaobject." not in str(j)


def test_the_stock_article_template_is_unchanged():
    j = stb.build_article()
    assert j["order"] == ["banner", "figures", "answer", "glance", "chart", "story", "limits",
                          "context", "faq", "safety", "means", "reference"]
    assert j["sections"]["reference"]["block_order"] == ["r", "ld"]


# --- scripts/link-pilot-sibling.py (audit 2026-09-29: Wang linked Raikou only to PubMed) ---

_l = importlib.util.spec_from_file_location("lps", ROOT / "scripts/link-pilot-sibling.py")
lps = importlib.util.module_from_spec(_l)
_argv, sys.argv = sys.argv, [sys.argv[0]]
_l.loader.exec_module(lps)
sys.argv = _argv


def test_the_appraisal_link_follows_the_pubmed_citation_with_the_locale_prefix():
    html = f"<p>… on placebo ({lps.CITATION}). An independent…</p>"
    en = lps.linked(html, "en")
    assert lps.CITATION in en  # the PubMed citation stays
    assert f'{lps.CITATION} — <a href="/{lps.TARGET}">our appraisal of the forehead-lines trial</a>' in en
    assert f'<a href="/de/{lps.TARGET}">unsere Bewertung der Stirnfalten-Studie</a>' in lps.linked(html, "de")


def test_linking_twice_changes_nothing():
    once = lps.linked(f"<p>({lps.CITATION})</p>", "en")
    assert lps.linked(once, "en") == once


# --- the "Before you try it" safety note (Malcolm, 2026-09-30; research 2026-09-30) -----------

import json  # noqa: E402
import re  # noqa: E402

NOTE = json.loads((ROOT / "configs/study-safety-note.json").read_text())
LOCALES = ["en", "de", "nl", "fr", "es", "it"]


def test_the_note_exists_in_all_six_languages_with_all_three_strings():
    for loc in LOCALES:
        assert set(NOTE[loc]) == {"title", "body", "pdrn"}, loc
        assert all(NOTE[loc][k].strip() for k in NOTE[loc]), loc


def test_the_note_makes_no_safety_claim():
    """EU claims rules (Reg 655/2013): a safety statement is itself a claim needing evidence.
    The research lists the words to avoid in every language."""
    banned = r"\b(safe|safely|proven|hypoallergenic|dermatologically tested|sicher|veilig|sûr|seguro|sicuro)\b"
    for loc in LOCALES:
        for k, v in NOTE[loc].items():
            assert not re.search(banned, v, re.I), (loc, k, re.search(banned, v, re.I))


def test_the_pdrn_line_names_fish_not_seafood():
    fish = {"en": "fish", "de": "Fisch", "nl": "vis", "fr": "poisson", "es": "pescado", "it": "pesce"}
    for loc in LOCALES:
        assert fish[loc] in NOTE[loc]["pdrn"], loc
        assert not re.search(r"shellfish|seafood|Meeresfrüchte|zeevruchten|fruits de mer|marisco|frutti di mare",
                             NOTE[loc]["pdrn"], re.I), loc


def test_both_article_templates_carry_the_note_before_the_product_link():
    stock = stb.build_article()["order"]
    assert stock.index("safety") < stock.index("means")
    assert stb.build_pilot_article()["order"] == ["banner", "answer", "safety", "reference"]


def test_the_note_reads_its_words_from_the_locale_files_and_pdrn_only_on_pdrn():
    liquid = stb.build_article()["sections"]["safety"]["blocks"]["n"]["settings"]["liquid"]
    for key in ("title", "body", "pdrn"):
        assert f"'skingenetix.study_safety.{key}' | t" in liquid
    assert "assign h = article.handle" in liquid and "if h contains 'pdrn'" in liquid


def test_merging_the_note_into_a_locale_file_keeps_everything_else():
    raw = '/* header */\n{"general": {"a": "b"}, "skingenetix": {"other": "x"}}'
    out = stb.merge_locale(raw, NOTE["de"])
    assert out.startswith("/* header */")
    body = json.loads(out[out.index("{"):])
    assert body["general"] == {"a": "b"} and body["skingenetix"]["other"] == "x"
    assert body["skingenetix"]["study_safety"]["title"] == "Bevor Sie es ausprobieren"
