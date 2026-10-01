"""Offline tests for scripts/matrixyl-robinson-threshold.py (2026-10-01).

Run:  python3 -m pytest tests/ -q
"""
import importlib.util
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
_s = importlib.util.spec_from_file_location("mrt", ROOT / "scripts/matrixyl-robinson-threshold.py")
mrt = importlib.util.module_from_spec(_s)
_argv, sys.argv = sys.argv, [sys.argv[0]]
_s.loader.exec_module(mrt)
sys.argv = _argv


def _six(make):
    return {l: make(l) for l in mrt.LOCALES}


def test_each_text_gains_the_threshold_once_in_every_language():
    ev = _six(lambda l: f"<p>x (<a href='u'>Robinson et al., 2005</a>). Next.</p>")
    u1 = _six(lambda l: f"<p>trial {mrt.U1_END[l]}</p>")
    t3 = _six(lambda l: f"<p>graded {mrt.T3_END[l]}</p>")
    for kind, vals in (("evidence", ev), ("usage", u1), ("table", t3)):
        out = mrt.transform(kind, vals)
        for l in mrt.LOCALES:
            # usage joins the clause into its sentence; the others add the whole sentence (which, in de and nl,
            # contains the clause verbatim, so count the phrase each one uses)
            phrase = mrt.CLAUSE[l] if kind == "usage" else mrt.MEANS[l]
            assert out[l].count(phrase) == 1, (kind, l)
            assert mrt.tags(out[l]) == mrt.tags(vals[l])
    assert mrt.transform("usage", u1)["en"] == "<p>trial at weeks 8 and 12, " + mrt.CLAUSE["en"] + ".</p>"


def test_it_refuses_an_ambiguous_anchor_and_a_second_run():
    twice = _six(lambda l: f"<p>{mrt.T3_END[l]} {mrt.T3_END[l]}</p>")
    with pytest.raises(SystemExit):
        mrt.transform("table", twice)
    done = mrt.transform("table", _six(lambda l: f"<p>graded {mrt.T3_END[l]}</p>"))
    with pytest.raises(SystemExit):
        mrt.transform("table", done)


def test_the_wording_matches_the_live_robinson_article():
    """The hub must say what the article says: the paper's own bar p <= 0.10, the usual p <= 0.05."""
    for l in mrt.LOCALES:
        sep = "." if l == "en" else ","
        assert f"0{sep}10" in mrt.MEANS[l] and f"0{sep}05" in mrt.MEANS[l]
        assert f"0{sep}10" in mrt.CLAUSE[l] and f"0{sep}05" in mrt.CLAUSE[l]
