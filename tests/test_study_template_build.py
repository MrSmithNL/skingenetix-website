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


def test_the_stock_article_template_keeps_its_sections_and_prints_the_reference_once():
    """The full order, with the result and how-it-works sections added 2026-10-01, is asserted further down."""
    j = stb.build_article()
    for k in ["banner", "figures", "answer", "glance", "chart", "story", "limits",
              "context", "faq", "safety", "means", "reference"]:
        assert k in j["order"], k
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


# ── the draft template (Malcolm, 2026-09-30): rebuild a live, translated article English-first ──────────────────
# Wang 2013 and Ye 2026 are live in six languages on the pilot template. Their stock-format rebuild is written to a
# separate study entry, `<handle>-draft`, which the article reaches through a second metafield, study.draft. This
# template reads only that, so /blogs/clinical-studies/<handle>?view=clinical-study-draft shows the draft and the live
# article (study.entry) does not change until go-live.

def test_the_draft_template_reads_the_draft_entry_and_never_the_live_one():
    import json
    s = json.dumps(stb.build_draft_article())
    assert "article.metafields.study.draft.value." in s and "study.entry" not in s
    assert stb.build_draft_article()["order"] == stb.build_article()["order"]


def test_the_chart_heading_is_chosen_by_locale():
    """A liquid setting is not translatable: "What the measurements showed" showed in English on /de…/it once Wang 2013
    and Ye 2026 went live translated on this template (2026-09-30). The heading is a case on the storefront locale."""
    liquid = stb.build_article()["sections"]["chart"]["blocks"]["c"]["settings"]["liquid"]
    assert "{%- case request.locale.iso_code -%}" in liquid and "{%- when 'de' -%}" in liquid
    assert "{%- else -%}What the measurements showed{%- endcase -%}" in liquid


# ── one section per proven result, and "how it works" blocks (Malcolm, 2026-10-01) ─────────────────────────────────
# "every study blog article should have separate content sections for each of the proven trial outcomes with before
# and after images where this can be used (similar to the ingredient science pages). And these should also be separate
# content blocks for the proven working active effects of what was tested". The study entry is full (40 of 40 fields,
# read live 2026-10-01), so both read a companion `study_detail` entry through the article metafield study.detail, and
# both reuse the science pages' own research-before-after section (key_findings_ba on the hubs).

_d = importlib.util.spec_from_file_location("bsp_detail", ROOT / "scripts/build-study-page.py")
bsp = importlib.util.module_from_spec(_d)
_d.loader.exec_module(bsp)
DETAIL = "article.metafields.study.detail.value."


def test_results_follow_the_glance_and_how_it_works_follows_the_method():
    assert stb.build_article()["order"] == ["banner", "figures", "answer", "glance", "outcomes", "chart", "story",
                                            "mechanism", "limits", "context", "faq", "safety", "means", "reference"]


def test_each_result_is_its_own_labelled_before_after_block_read_from_the_detail_entry():
    s = stb.build_article()["sections"]["outcomes"]
    assert s["type"] == "research-before-after" and s["block_order"] == ["o1", "o2", "o3", "o4"]
    assert s["settings"]["title"] == "{{ " + DETAIL + "outcomes_heading.value }}"
    for i, k in enumerate(s["block_order"], 1):
        b = s["blocks"][k]
        st = b["settings"]
        assert b["type"] == "finding"
        assert st["image"] == "{{ " + DETAIL + f"o{i}_image.value }}}}"
        assert st["title"] == "{{ " + DETAIL + f"o{i}_title.value }}}}"
        for label in ("before", "after", "result"):
            assert st[f"{label}_label"] == "{{ " + DETAIL + f"o{i}_{label}.value }}}}"
        assert st["content"] == "<p>{{ " + DETAIL + f"o{i}_body.value }}}}</p>"
        assert st["note_label"] == ""                           # Malcolm, 2026-09-22: "No AI disclosure please."
    assert [s["blocks"][k]["settings"]["media_position"] for k in s["block_order"]] == ["start", "end", "start", "end"]


def test_how_it_works_blocks_carry_no_before_after_labels():
    s = stb.build_article()["sections"]["mechanism"]
    assert s["type"] == "research-before-after" and s["block_order"] == ["m1", "m2", "m3"]
    assert s["settings"]["title"] == "{{ " + DETAIL + "mechanism_heading.value }}"
    for k in s["block_order"]:
        st = s["blocks"][k]["settings"]
        assert st["before_label"] == st["after_label"] == st["result_label"] == st["note_label"] == ""
        assert st["title"] == "{{ " + DETAIL + f"{k}_title.value }}}}"
        assert st["image"] == "{{ " + DETAIL + f"{k}_image.value }}}}"
        assert st["content"] == "<p>{{ " + DETAIL + f"{k}_body.value }}}}</p>"


def test_the_draft_template_reads_the_draft_detail_and_never_the_live_one():
    s = json.dumps(stb.build_draft_article())
    assert "article.metafields.study.draft_detail.value.o1_title.value" in s
    assert "study.detail." not in s and "study.entry." not in s


def test_the_pilot_and_metaobject_templates_carry_no_detail_sections():
    """The metaobject template cannot reach the companion entry (the study has no free field to reference it), and
    the pilot template keeps only what a pilot fills."""
    for j in (stb.build_pilot_article(), stb.build()):
        assert "outcomes" not in j["sections"] and "mechanism" not in j["sections"]
        assert "detail" not in json.dumps(j)


def test_every_detail_field_the_template_reads_is_defined_and_the_definition_fits():
    refs = set(re.findall(r"study\.detail\.value\.(\w+)\.value", json.dumps(stb.build_article())))
    defined = [k for k, _ in bsp.DETAIL_FIELDS]
    assert refs == set(defined)                                 # nothing read that is not defined, nothing defined unread
    assert len(defined) == len(set(defined)) <= 40              # Shopify's per-definition limit


def test_the_section_draws_nothing_for_an_empty_slot():
    """A study with two results leaves two of the four slots empty. Unguarded, an empty slot drew the theme's grey
    placeholder box, and a section with no filled slot drew its heading over nothing. Every block on the science
    pages has a heading, so they are unaffected."""
    liquid = (ROOT / "theme/sections/research-before-after.liquid").read_text()
    assert "if rba_filled > 0" in liquid
    assert "if block.settings.title == blank and block.settings.image == blank -%}{%- continue" in liquid
    assert liquid.index("if rba_filled > 0") < liquid.index("<style>")   # the style block is inside the guard too
