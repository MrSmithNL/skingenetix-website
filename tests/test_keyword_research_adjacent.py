"""Offline tests for scripts/keyword-research-adjacent.py (no DataForSEO calls).

Author: Claude (Opus 5.5) for Malcolm Smith · 2026-10-09
Why: the pull merges keywords across seeds and methods, and the enrich step decides which keywords count as demand; both
feed the article plan's numbers, so a silent merge or fallback error would misstate every volume in it.
"""
import argparse
import importlib.util
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
_s = importlib.util.spec_from_file_location("kra", ROOT / "scripts/keyword-research-adjacent.py")
kra = importlib.util.module_from_spec(_s)
_argv, sys.argv = sys.argv, [sys.argv[0]]
_s.loader.exec_module(kra)
sys.argv = _argv


def item(kw, vol, kd=5, intent="informational"):
    return {"keyword": kw, "keyword_info": {"search_volume": vol, "cpc": 1.0, "competition": 0.5},
            "keyword_properties": {"keyword_difficulty": kd}, "search_intent_info": {"main_intent": intent}}


def test_pull_merges_seeds_and_sends_regex_only_for_questions(tmp_path, monkeypatch):
    (tmp_path / "seeds.json").write_text(json.dumps({
        "question_regex": "(how |what )",
        "groups": {"g": {"suggest": ["crows feet"], "q": ["pdrn"], "related": ["pdrn serum"]}}}))
    calls = []

    def fake_post(path, payload, a):
        calls.append((path, payload))
        if path.endswith("related_keywords/live"):
            return {"items": [{"keyword_data": item("crows feet", 9000)}, {"keyword_data": item("salmon sperm", 1700)}]}, 0.01
        if payload["keyword"] == "pdrn":
            return {"items": [item("how to use pdrn", 50)]}, 0.01
        return {"items": [item("crows feet", 9000), item("crows feet meaning", 500)]}, 0.01

    monkeypatch.setattr(kra.ks, "post", fake_post)
    monkeypatch.setattr(kra.ks, "auth", lambda: "x")
    monkeypatch.setattr(kra, "MARKETS", [("US", 2840, "en")])
    kra.cmd_pull(argparse.Namespace(dir=str(tmp_path), force=True, markets=None))

    rows = {r["keyword"]: r for r in json.loads((tmp_path / "raw-US.json").read_text())}
    assert set(rows) == {"crows feet", "crows feet meaning", "how to use pdrn", "salmon sperm"}
    assert rows["crows feet"]["sources"] == ["g:suggest:crows feet", "g:related:pdrn serum"]
    regex_calls = [p for path, p in calls if any(f == ["keyword", "regex", "(how |what )"] for f in p.get("filters", []))]
    assert [p["keyword"] for p in regex_calls] == ["pdrn"]


def test_enrich_falls_back_to_a_third_of_ads_and_drops_off_intent(tmp_path, monkeypatch):
    raw = [{"keyword": "crows feet", "ads": 12000, "cpc": 1.0, "competition": 0.5, "kd": 10, "intent": "informational"},
           {"keyword": "copper uglies", "ads": 900, "cpc": 1.0, "competition": 0.5, "kd": 0, "intent": "informational"},
           {"keyword": "bpc 157 injection", "ads": 5000, "cpc": 1.0, "competition": 0.5, "kd": 0, "intent": "informational"},
           {"keyword": "tiny term", "ads": 10, "cpc": 1.0, "competition": 0.5, "kd": 0, "intent": "informational"}]
    (tmp_path / "raw-US.json").write_text(json.dumps(raw))

    def fake_post(path, payload, a):
        assert "bpc 157 injection" not in payload["keywords"] and "tiny term" not in payload["keywords"]
        return {"items": [{"keyword": "crows feet", "search_volume": 9714}]}, 0.02

    monkeypatch.setattr(kra.ks, "post", fake_post)
    monkeypatch.setattr(kra.ks, "auth", lambda: "x")
    monkeypatch.setattr(kra, "MARKETS", [("US", 2840, "en")])
    kra.cmd_enrich(argparse.Namespace(dir=str(tmp_path), min_ads=20, markets=None))

    out = {r["keyword"]: r for r in json.loads((tmp_path / "candidates-US.json").read_text())}
    assert set(out) == {"crows feet", "copper uglies"}
    assert out["crows feet"]["observed"] == 9714
    assert out["copper uglies"]["clickstream"] is None and out["copper uglies"]["observed"] == 300


def test_markets_flag_selects_from_the_strategys_seven():
    picked = kra.markets(argparse.Namespace(markets=["DE", "NL"]))
    assert [m[0] for m in picked] == ["DE", "NL"] and picked[0][2] == "de"
    assert kra.markets(argparse.Namespace(markets=None)) == kra.MARKETS
