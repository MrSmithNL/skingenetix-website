"""Offline tests for the MARKETING checks in scripts/page-audit.py — no network, no browser.

Run:  python3 -m pytest tests/ -q
"""
import importlib.util
import pathlib
import re

from lxml import html as LH

ROOT = pathlib.Path(__file__).resolve().parent.parent
_s = importlib.util.spec_from_file_location("pa", ROOT / "scripts/page-audit.py")
pa = importlib.util.module_from_spec(_s)
_s.loader.exec_module(pa)

TGT = {"primary": "glutathione", "secondary": ["glutathione for skin"], "type": "hub"}


def run(body):
    raw = f"<html><body><main>{body}</main></body></html>"
    doc = LH.fromstring(raw)
    main = doc.find(".//main")
    text = re.sub(r"\s+", " ", main.text_content()).strip()
    rep = pa.Report()
    pa.audit_marketing("/pages/glutathione-research", rep, raw, main, text, TGT, ["Glutathione for Skin"])
    return {i["check"]: i for i in rep.items}


def test_a_published_citation_title_is_not_our_medicinal_wording():
    body = ('<h1>Glutathione for Skin</h1><p>Brighter-looking skin in 10 weeks.</p>'
            '<div class="sgref"><div class="sgref__r"><p class="sgref__ti">Skin-whitening effects of topical '
            'oxidized glutathione</p><p class="sgref__me">Watanabe F et al., 2014</p></div></div>')
    r = run(body)
    assert r["No medicinal wording (EU cosmetic-claims rules)"]["ok"]


def test_whitening_in_our_own_prose_is_still_flagged():
    body = '<h1>Glutathione for Skin</h1><p>A skin whitening serum for brighter skin.</p>'
    r = run(body)
    assert not r["No medicinal wording (EU cosmetic-claims rules)"]["ok"]
    assert "whitening" in r["No medicinal wording (EU cosmetic-claims rules)"]["detail"]


def test_a_figure_beside_the_word_placebo_counts_as_sourced():
    body = ('<h1>Glutathione for Skin</h1><p>Brighter skin.</p>'
            '<p>Brighter-looking skin vs placebo: pigment −10.7% vs −3.1% (p &lt; 0.001)</p>')
    r = run(body)
    assert r["Every result figure sits next to its source"]["ok"]


def test_a_bare_figure_with_no_source_word_or_link_is_unsourced():
    body = '<h1>Glutathione for Skin</h1><p>Brighter skin.</p><p>Pigment down 10.7% in 10 weeks.</p>'
    r = run(body)
    assert not r["Every result figure sits next to its source"]["ok"]


# ── the written report passes the repo's markdownlint gate (2026-09-26) ─────────────────────────────────────
# The gate (.husky/pre-commit: markdownlint, MD013 300 chars outside tables, MD033 no raw HTML) refused the copper
# report: its check names say "Exactly one <h1>" and the served outline was a 355-character list item.

def written_report(tmp_path):
    rep = pa.Report()
    rep.add("SEO", "Exactly one <h1>", True, "Copper Peptide (GHK-Cu)")
    rep.add("SEO", "Topic headings are real <h2> (≥ 3)", True, "13 <h2>: ['a', 'b']")
    data = {"h1": "Copper Peptide (GHK-Cu)", "h2": [f"Heading number {n} of the page" for n in range(30)],
            "pseudo_headings": ["<p> styled"], "schema_types": ["WebPage"], "extracted_words": 10, "main_words": 12}
    design = {"desktop": {"rows": [{"top": 0, "h": 10, "id": "hero", "type": "custom-html", "bg": "rgb(255, 255, 255)"}]}}
    pa.write("/pages/x", rep, data, design, tmp_path)
    return next(tmp_path.glob("pages-x-*.md")).read_text()


def outside_code(line):
    return re.sub(r"`[^`]*`", "", line)


def test_report_has_no_raw_html_tags(tmp_path):
    md = written_report(tmp_path)
    assert not [l for l in md.splitlines() if re.search(r"<[a-z/]", outside_code(l))]
    assert "&lt;h1&gt;" in md


def test_report_lines_outside_tables_stay_under_the_lint_limit(tmp_path):
    md = written_report(tmp_path)
    assert not [l for l in md.splitlines() if not l.startswith("|") and len(l) > 300]
    assert re.search(r"^\| H2 \| .*Heading number 29 of the page", md, re.M)
