"""Tests for scripts/harvest-translations.py — pairing a page's live English with its approved translations.

Author: Claude (Opus 5.5) for Malcolm Smith · 2026-09-25
Offline: the pairing and checking functions are pure; nothing here calls Shopify.
"""
import importlib.util
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
_s = importlib.util.spec_from_file_location("harvest", ROOT / "scripts/harvest-translations.py")
harvest = importlib.util.module_from_spec(_s)
_s.loader.exec_module(harvest)

LOCS = ["de", "nl", "fr", "es", "it"]


def six(en, other):
    return {"en": en, **{l: other.replace("X", l) for l in LOCS}}


def test_pairs_by_element_when_structure_matches():
    v = {"en": "<p>First <a href='/a'>link</a>.</p><ul><li>One</li><li>Two</li></ul>"}
    for l in LOCS:
        v[l] = f"<p>Erst-{l} <a href='/{l}/a'>L</a>.</p><ul><li>Eins-{l}</li><li>Zwei-{l}</li></ul>"
    pairs = harvest.pair_elements(v)
    assert [p["en"] for p in pairs] == ["First <a href='/a'>link</a>.", "One", "Two"]
    assert pairs[1]["de"] == "Eins-de" and pairs[2]["it"] == "Zwei-it"


def test_whole_value_when_there_are_no_elements():
    pairs = harvest.pair_elements(six("Before", "Vorher-X"))
    assert pairs == [{"en": "Before", **{l: f"Vorher-{l}" for l in LOCS}}]


def test_skips_a_value_whose_element_count_differs_in_any_locale():
    v = six("<p>A</p><p>B</p>", "<p>A-X</p><p>B-X</p>")
    v["fr"] = "<p>A et B</p>"
    assert harvest.pair_elements(v) == []


def test_numbers_agree_ignores_separators_and_decimal_commas():
    assert harvest.numbers_agree("1,500 people, 7.4% and 20 days", "1500 Personen, 7,4 % und 20 Tage")
    assert harvest.numbers_agree("2% GHK-Cu", "2 % GHK-Cu")


def test_numbers_disagree_on_a_changed_figure():
    assert not harvest.numbers_agree("fell 7.4% by day 20", "sank um 7,1 % bis Tag 20")
    assert not harvest.numbers_agree("in 24 women", "bei 42 Frauen")


def test_harvest_keeps_only_current_translations_in_all_five_locales():
    content = [{"key": "section.x.body.content:abc", "value": "<p>Hello</p>"},
               {"key": "section.x.title:def", "value": "Title"}]
    tr = {l: [{"key": "section.x.body.content:abc", "value": f"<p>Hallo-{l}</p>", "outdated": False}] for l in LOCS}
    tr["nl"].append({"key": "section.x.title:def", "value": "Titel", "outdated": False})   # only one locale
    tr["it"][0]["outdated"] = True
    out = harvest.harvest(content, tr)
    assert out["pairs"] == []                          # it is outdated, so the body is not usable
    assert {s["key"] for s in out["skipped"]} == {"section.x.body.content:abc", "section.x.title:def"}


def test_flags_number_mismatch_instead_of_dropping():
    content = [{"key": "k:1", "value": "<p>7.4% by day 20</p>"}]
    tr = {l: [{"key": "k:1", "value": "<p>7,4 % bis Tag 20</p>", "outdated": False}] for l in LOCS}
    tr["es"][0]["value"] = "<p>7,1 % al día 20</p>"
    pair = harvest.harvest(content, tr)["pairs"][0]
    assert pair["numbers_ok"] is False and pair["number_mismatch"] == ["es"]
