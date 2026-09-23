"""Offline tests for scripts/set-reviewer.py — byline and JSON-LD edits, no Shopify calls.

Run:  python3 -m pytest tests/ -q
"""
import importlib.util
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
_s = importlib.util.spec_from_file_location("sr", ROOT / "scripts/set-reviewer.py")
sr = importlib.util.module_from_spec(_s)
_s.loader.exec_module(sr)

CFG = json.loads((ROOT / "configs/reviewers/esther-bodde.json").read_text())

HUB_EN = ("<h2>What Is PDRN?</h2><p>Body.</p>"
          "<p><em>Last updated 22 September 2026. Sources: five published studies, listed below.</em></p>")
HUB_DE = ("<h2>Was ist PDRN?</h2><p>Text.</p>"
          "<p><em>Zuletzt aktualisiert am 22. September 2026. Quellen: fünf veröffentlichte Studien.</em></p>")
MX_EN = ("<p>Def.</p><p><em>By Skingenetix. Every figure on this page was checked against its original source. "
         "Last reviewed 22 September 2026.</em></p>")
MX_IT = ("<p>Def.</p><p><em>A cura di Skingenetix. Ogni dato di questa pagina è stato verificato. "
         "Ultima revisione: 22 settembre 2026.</em></p>")


def test_adds_author_and_reviewer_when_the_byline_has_no_author():
    out = sr.add_to_byline(HUB_EN, "en", CFG)
    assert "<p><em>By Skingenetix. Medically reviewed by Dr Esther Bodde, Cosmetic &amp; Medical Physician. Last updated" in out
    assert out.count("Esther Bodde") == 1


def test_inserts_after_an_existing_author_sentence():
    out = sr.add_to_byline(MX_EN, "en", CFG)
    assert "<p><em>By Skingenetix. Medically reviewed by Dr Esther Bodde" in out
    assert out.count("Skingenetix.") == 1          # the author sentence is not duplicated
    out_it = sr.add_to_byline(MX_IT, "it", CFG)
    assert "<p><em>A cura di Skingenetix. Revisione medica della dott.ssa Esther Bodde" in out_it


def test_translation_gets_its_own_locale_sentence():
    out = sr.add_to_byline(HUB_DE, "de", CFG)
    assert "Von Skingenetix. Medizinisch geprüft von Dr. Esther Bodde (Cosmetic &amp; Medical Physician). Zuletzt" in out


def test_adding_twice_changes_nothing():
    once = sr.add_to_byline(HUB_EN, "en", CFG)
    assert sr.add_to_byline(once, "en", CFG) == once


def test_remove_takes_out_only_the_reviewer_sentence():
    added = sr.add_to_byline(HUB_EN, "en", CFG)
    removed = sr.remove_from_byline(added, "en", CFG)
    assert "Esther Bodde" not in removed
    assert "<p><em>By Skingenetix. Last updated 22 September 2026." in removed   # the author line stays


def test_no_byline_found_returns_none():
    assert sr.add_to_byline("<p>No dated byline here.</p>", "en", CFG) is None


def test_jsonld_gets_reviewer_and_date_and_can_lose_them_again():
    html = ('<div>refs</div>\n<script type="application/ld+json" id="sgx-webpage-jsonld">\n'
            + json.dumps({"@type": "WebPage", "name": "X", "dateModified": "2026-09-22"}, indent=2) + "\n</script>")
    out = sr.jsonld_edit(html, CFG, add=True)
    ld = json.loads(out.split('id="sgx-webpage-jsonld">', 1)[1].split("</script>")[0])
    assert ld["reviewedBy"]["@type"] == "Person" and ld["reviewedBy"]["name"] == "Esther Bodde"
    assert ld["lastReviewed"] == CFG["reviewed"]
    assert "}}" not in out                        # custom-html rejects Liquid-like delimiters
    back = sr.jsonld_edit(out, CFG, add=False)
    ld2 = json.loads(back.split('id="sgx-webpage-jsonld">', 1)[1].split("</script>")[0])
    assert "reviewedBy" not in ld2


def test_study_markup_gets_the_sentence_after_the_first_sentence():
    p = ["p", "*Appraised by the Skingenetix research team. Last reviewed 22 September 2026.*"]
    out = sr.add_to_study_markup(p[1], "en", CFG)
    assert out == ("*Appraised by the Skingenetix research team. Medically reviewed by Dr Esther Bodde, "
                   "Cosmetic & Medical Physician. Last reviewed 22 September 2026.*")
    assert sr.add_to_study_markup(out, "en", CFG) == out
    assert sr.remove_from_study_markup(out, "en", CFG) == p[1]


def test_a_hub_can_carry_its_own_review_date():
    """The glutathione hub was rebuilt on 2026-09-23; its JSON-LD lastReviewed must not be pulled back to the
    config-wide date of the other four hubs (found live 2026-09-23: byline said 23 September, schema said 22)."""
    hub = {"spec": "x.json", "byline": "overview.op.content", "jsonld_host": "references", "reviewed": "2026-09-23"}
    assert sr.hub_cfg(CFG, hub)["reviewed"] == "2026-09-23"
    assert sr.hub_cfg(CFG, {"spec": "y.json"})["reviewed"] == CFG["reviewed"]
    html = '<script type="application/ld+json" id="sgx-webpage-jsonld">{"@type": "WebPage"}</script>'
    out = sr.jsonld_edit(html, sr.hub_cfg(CFG, hub), True)
    assert '"lastReviewed": "2026-09-23"' in out


# A hub whose byline lives in a section-level custom-html setting (the Argireline hub after
# its 2026-09-23 layout pass) must still resolve, or --remove cannot take the credit off it.
TPL = {"sections": {
    "overview_rt": {"blocks": {"op": {"settings": {"content": MX_EN}}}},
    "overview_html": {"settings": {"html": MX_EN}},
}}


def test_three_part_byline_path_resolves_a_block_setting():
    settings, key = sr.byline_settings(TPL, "overview_rt.op.content")
    assert key == "content"
    assert settings[key] == MX_EN


def test_two_part_byline_path_resolves_a_section_setting():
    settings, key = sr.byline_settings(TPL, "overview_html.html")
    assert key == "html"
    assert settings[key] == MX_EN
