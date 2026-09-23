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
