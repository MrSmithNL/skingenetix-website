"""Offline tests for scripts/hub_charts.py — the research-page bar charts.

Author: Claude (Opus 5.5) for Malcolm Smith · 2026-09-26
Purpose: the 200% zoom reflow found by the design critic on the copper page (cycle 2): at a 195px viewport the
value column (70px) and the card padding left the bars 0px wide, the axis labels printed over each other and the
data table ran 45px past the screen (WCAG 1.4.10).

Run:  python3 -m pytest tests/ -q
"""
import importlib.util
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
_s = importlib.util.spec_from_file_location("hub_charts", ROOT / "scripts/hub_charts.py")
hc = importlib.util.module_from_spec(_s)
_s.loader.exec_module(hc)

CHART = {
    "title": {"en": "T"}, "subtitle": {"en": "S"}, "unit": "%", "domain": [-30, 2], "ticks": [-20, -10, 0],
    "series": [{"key": "a", "color": "#014EB1", "label": {"en": "A"}}],
    "rows": [{"label": {"en": "Row"}, "values": {"a": -24.1}}],
    "table_head": {"en": "Measure"}, "caption": {"en": "<p>C</p>"},
}


def narrow_block(css):
    m = re.search(r"@media \(max-width:360px\)\{(.*)\}\s*$", css)
    return m.group(1) if m else ""


def test_narrow_screens_give_the_bar_the_whole_card_width():
    block = narrow_block(hc.CSS)
    assert block, "no reflow block for 200% zoom (a 390px phone zoomed to 195px)"
    assert re.search(r"\.sgfig-line,\.sgfig-axis\{grid-template-columns:1fr;", block)
    assert ".sgfig-axis>span{display:none;}" in block


def test_narrow_screens_keep_the_table_inside_the_card():
    block = narrow_block(hc.CSS)
    assert "overflow-wrap:anywhere" in block
    assert re.search(r"\.sgfig-card\{padding:16px 10px 14px;\}", block)


def test_reflow_block_comes_last_so_it_wins_the_cascade():
    # equal specificity: the later rule wins, so the narrow-screen block must follow every base rule
    assert hc.CSS.rstrip().endswith("}}")
    assert hc.CSS.rfind("@media (max-width:360px)") > hc.CSS.rfind(".sgfig-caption p{")


def test_rendered_group_never_carries_liquid_braces():
    out = hc.render_group({"$chart": ["a", "b"]}, {"a": CHART, "b": CHART}, "en")
    assert "}}" not in out and "{{" not in out
    assert "@media (max-width:360px)" in out
