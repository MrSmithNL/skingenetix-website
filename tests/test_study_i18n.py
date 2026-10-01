"""Offline tests for scripts/study-i18n.py — extract a study config's English strings, merge five translations back.

Run:  python3 -m pytest tests/test_study_i18n.py -q
"""
import copy
import importlib.util
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
_s = importlib.util.spec_from_file_location("si", ROOT / "scripts/study-i18n.py")
si = importlib.util.module_from_spec(_s)
_s.loader.exec_module(si)

CFG = {
    "_note": {"en": "internal, never translated"},
    "handle": "pdrn-microneedling-split-face-trial-yogya-2022",
    "h1": {"en": "Does PDRN microneedling smooth wrinkles faster?"},
    "byline": {"en": "Appraised by the Skingenetix research team. Medically reviewed by Dr Esther Bodde, Cosmetic & Medical "
                     "Physician. Last reviewed 30 September 2026."},
    "figures": [{"n": {"en": "&minus;14%"}, "label": {"en": "Wrinkle indentation at 2 months"}}],
    "faq": {"answers": [{"en": "See the [PDRN hub](https://www.skingenetix.com/pages/pdrn-research) and "
                               "[the paper](https://doi.org/10.1007/s13555-022-00729-7)."}]},
    "checks": ["10.3 to 8.9"],
    "scholarly": {"name": "Efficacy and Safety of Using Noninsulated Microneedle Radiofrequency"},
    "meaning": {"ctas": [{"href": "/pages/pdrn-research", "label": {"en": "Read the evidence"}}]},
}


def test_strings_are_every_english_leaf_except_notes_checks_citation_and_byline():
    s = si.strings(CFG)
    assert set(s) == {"/h1", "/figures/0/n", "/figures/0/label", "/faq/answers/0", "/meaning/ctas/0/label"}
    assert s["/figures/0/n"] == "&minus;14%"


def test_internal_links_get_the_locale_prefix_and_external_ones_do_not():
    t = si.localise_links("[hub](https://www.skingenetix.com/pages/pdrn-research), "
                          "<a href='/products/pdrn-renewal-serum'>serum</a>, [p](https://doi.org/10.1/x), "
                          "[study](https://www.skingenetix.com/blogs/clinical-studies/a-b)", "de")
    assert "https://www.skingenetix.com/de/pages/pdrn-research" in t
    assert "href='/de/products/pdrn-renewal-serum'" in t
    assert "https://www.skingenetix.com/de/blogs/clinical-studies/a-b" in t
    assert "https://doi.org/10.1/x" in t
    assert si.localise_links(t, "de") == t                      # idempotent: never /de/de/


def test_numbers_survive_decimal_commas_and_thousand_spaces():
    assert si.problems("10.7% of 1,500 kDa, p = 0.006", "10,7 % von 1 500 kDa, p = 0,006", "fr") == []
    assert si.problems("fell 10.7% in 10 weeks", "a baissé de 10 % en 10 semaines", "fr")   # 10.7 lost


def test_markup_and_links_must_match_english():
    en = "<strong>Depth.</strong> See [the hub](https://www.skingenetix.com/pages/pdrn-research)."
    assert si.problems(en, "<strong>Tiefe.</strong> Siehe [den Hub](https://www.skingenetix.com/pages/pdrn-research).", "de") == []
    assert si.problems(en, "Tiefe. Siehe [den Hub](https://www.skingenetix.com/pages/pdrn-research).", "de")          # tag lost
    assert si.problems(en, "<strong>Tiefe.</strong> Siehe den Hub.", "de")                                           # link lost


def test_merge_writes_prefixed_translations_and_composes_the_byline():
    tr = {"/h1": "Glättet PDRN-Microneedling Falten schneller?", "/figures/0/n": "&minus;14 %",
          "/figures/0/label": "Faltentiefe nach 2 Monaten",
          "/faq/answers/0": "Siehe den [PDRN-Hub](https://www.skingenetix.com/pages/pdrn-research) und "
                            "[die Studie](https://doi.org/10.1007/s13555-022-00729-7).",
          "/meaning/ctas/0/label": "Die Evidenz lesen"}
    ref = {"de": "Bewertet vom Skingenetix-Forschungsteam. Medizinisch geprüft von Dr. Esther Bodde (Cosmetic & Medical "
                 "Physician). Zuletzt geprüft am 23. September 2026."}
    cfg, errs = si.merge(copy.deepcopy(CFG), {"de": tr}, ref_byline=ref)
    assert errs == []
    assert cfg["faq"]["answers"][0]["de"].count("https://www.skingenetix.com/de/pages/pdrn-research") == 1
    assert cfg["byline"]["de"].endswith("Zuletzt geprüft am 30. September 2026.")
    assert cfg["h1"]["en"] == CFG["h1"]["en"]                    # English untouched


def test_merge_refuses_a_missing_key_or_a_broken_string():
    tr = {"/h1": "Glättet PDRN-Microneedling Falten schneller?"}
    _, errs = si.merge(copy.deepcopy(CFG), {"de": tr}, ref_byline={"de": "x 23. September 2026."})
    assert any("missing" in e for e in errs)


def test_the_byline_date_is_rewritten_in_every_locale_format():
    en = "Appraised by the team. Last reviewed 30 September 2026."
    for ref, want in [("Zuletzt geprüft am 23. September 2026.", "am 30. September 2026."),
                      ("Última revisión: 23 de septiembre de 2026.", "30 de septiembre de 2026."),
                      ("Ultima revisione: 23 settembre 2026.", "30 settembre 2026.")]:
        assert si.byline(en, ref).endswith(want)


def test_the_builders_length_rules_hold_in_every_locale():
    cfg = {**copy.deepcopy(CFG), "seo_title": {"en": "Yogya 2022: Does PDRN Microneedling Smooth Wrinkles?"},
           "answer": {"en": " ".join(["word"] * 50)}}
    good = {**{k: v for k, v in [("/h1", "Glättet PDRN-Microneedling Falten schneller?"), ("/figures/0/n", "&minus;14 %"),
                                 ("/figures/0/label", "Faltentiefe nach 2 Monaten"), ("/meaning/ctas/0/label", "Die Evidenz lesen"),
                                 ("/faq/answers/0", "Siehe den [Hub](https://www.skingenetix.com/pages/pdrn-research) und "
                                                    "[die Studie](https://doi.org/10.1007/s13555-022-00729-7).")]},
            "/seo_title": "Yogya 2022: Glättet PDRN-Microneedling Falten schneller?", "/answer": " ".join(["Wort"] * 50)}
    ref = {"de": "Bewertet. Zuletzt geprüft am 23. September 2026."}
    assert si.merge(copy.deepcopy(cfg), {"de": good}, ref_byline=ref)[1] == []
    long_title = {**good, "/seo_title": "Yogya 2022: " + "x" * 60}
    assert any("SEO title" in e for e in si.merge(copy.deepcopy(cfg), {"de": long_title}, ref_byline=ref)[1])
    short_answer = {**good, "/answer": "Zu kurz."}
    assert any("answer" in e for e in si.merge(copy.deepcopy(cfg), {"de": short_answer}, ref_byline=ref)[1])
