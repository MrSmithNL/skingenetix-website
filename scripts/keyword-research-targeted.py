#!/usr/bin/env python3
"""Targeted keyword research: seed groups the 2026-09-22 strategy pull never covered.

    python3 scripts/keyword-research-targeted.py --out configs/keyword-data/targeted-2026-09-30

Why: the strategy pull (scripts/keyword-strategy.py) was seeded on ingredient head terms, so the long-tail
questions the clinical-study articles answer ("argireline crow's feet", "pdrn vs retinol") were never
collected, and the product-vs-hub decisions rested on one SERP per term. Malcolm, 2026-09-30: "the keyword
research and keyword strategy should decide this … do a full analysis". This pulls, per seed group:

  1. keyword suggestions (DataForSEO Labs, phrase match) — every keyword containing the seed
  2. observed clickstream volume for those keywords (the strategy's traffic signal, not Ads buckets)
  3. live Google top 10 for the decision terms (page type per result)
  4. what skingenetix.com ranks for today (Labs ranked keywords)

Reuses keyword-strategy.py's auth/post/norm/relevance/winnability so scores stay comparable. Read-only
against DataForSEO; writes only JSON under --out. Prints the spend.
"""
import argparse
import importlib.util
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
_s = importlib.util.spec_from_file_location("ks", ROOT / "scripts/keyword-strategy.py")
ks = importlib.util.module_from_spec(_s)
_argv, sys.argv = sys.argv, [sys.argv[0]]
_s.loader.exec_module(ks)
sys.argv = _argv

MARKETS = [("US", 2840, "en"), ("GB", 2826, "en")]

# What each clinical-study article answers: (head term, words any of which the keyword must contain).
# A contiguous seed ("argireline crow") found nothing and misses word-order variants ("argireline for crows
# feet") — probed 2026-09-30 — so each study is one head-term pull filtered to its words.
STUDY_SEEDS = {
    "wang-2013 (argireline, crow's feet)": [("argireline", ["crow", "eye", "wrinkle", "result", "work",
                                                             "before", "study", "clinical"])],
    "raikou-2017 (argireline, forehead)": [("argireline", ["forehead", "frown", "expression", "line"]),
                                           ("forehead lines", ["peptide", "serum", "cream"])],
    "badenhorst-2016 (copper peptide, wrinkles)": [("copper peptide", ["wrinkle", "result", "work", "before",
                                                                        "study", "clinical", "line", "aging"]),
                                                    ("ghk", ["wrinkle", "result", "work", "before", "study",
                                                             "line", "aging", "skin"])],
    "ye-2026 (pdrn vs retinol)": [("pdrn", ["retinol", " vs", "versus", "result", "before", "study",
                                            "wrinkle", "crow"])],
}
# The pages that claim one term, and the alternatives each could own instead.
CLASH_SEEDS = {
    "argireline": ["argireline", "acetyl hexapeptide 8", "acetyl hexapeptide-8"],
    "matrixyl": ["matrixyl", "palmitoyl tripeptide", "palmitoyl tetrapeptide"],
    "peptide skincare": ["peptide skincare", "peptide skin care"],
}
SERP_TERMS = ["argireline", "argireline serum", "acetyl hexapeptide 8", "matrixyl 3000",
              "matrixyl 3000 serum", "matrixyl", "matrixyl serum", "peptide skincare"]


def suggestions(seed, loc, lang, a, words=None):
    """Keywords containing `seed`; with `words`, only those also containing any of them."""
    payload = {"keyword": seed, "location_code": loc, "language_code": lang, "limit": 200,
               "include_serp_info": False, "order_by": ["keyword_info.search_volume,desc"]}
    if words:
        cond = []
        for w in words[:8]:                      # DataForSEO allows up to 8 conditions
            cond += [["keyword", "like", f"%{w}%"], "or"]
        payload["filters"] = cond[:-1]
    res, cost = ks.post("dataforseo_labs/google/keyword_suggestions/live", payload, a)
    return ks.norm((res or {}).get("items")), cost or 0.0


def clickstream(keywords, loc, a):
    out, spent = {}, 0.0
    for i in range(0, len(keywords), 1000):
        res, cost = ks.post("keywords_data/clickstream_data/bulk_search_volume/live",
                            {"keywords": keywords[i:i + 1000], "location_code": loc}, a)
        spent += cost or 0.0
        for it in (res or {}).get("items") or []:
            out[it.get("keyword")] = it.get("search_volume")
    return out, spent


def serp(term, loc, lang, a):
    res, cost = ks.post("serp/google/organic/live/advanced",
                        {"keyword": term, "location_code": loc, "language_code": lang, "depth": 10}, a)
    items = [{"rank": i.get("rank_group"), "url": i.get("url"), "domain": i.get("domain"),
              "title": i.get("title")} for i in (res or {}).get("items") or [] if i.get("type") == "organic"]
    features = sorted({i.get("type") for i in (res or {}).get("items") or []} - {"organic"})
    return {"organic": items[:10], "features": features}, cost or 0.0


def ranked(loc, lang, a):
    res, cost = ks.post("dataforseo_labs/google/ranked_keywords/live",
                        {"target": "skingenetix.com", "location_code": loc, "language_code": lang,
                         "limit": 200, "order_by": ["keyword_data.keyword_info.search_volume,desc"]}, a)
    rows = []
    for it in (res or {}).get("items") or []:
        kd = it.get("keyword_data") or {}
        se = (it.get("ranked_serp_element") or {}).get("serp_item") or {}
        rows.append({"keyword": kd.get("keyword"), "ads": (kd.get("keyword_info") or {}).get("search_volume"),
                     "rank": se.get("rank_group"), "url": se.get("url")})
    return rows, cost or 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    auth, spent = ks.auth(), 0.0
    data = {"studies": {}, "clashes": {}, "serps": {}, "ranked": {}}
    for code, loc, lang in MARKETS:
        for section, seeds_by in (("studies", STUDY_SEEDS), ("clashes", CLASH_SEEDS)):
            for group, seeds in seeds_by.items():
                rows, seen = [], set()
                for seed in seeds:
                    seed, words = seed if isinstance(seed, tuple) else (seed, None)
                    got, cost = suggestions(seed, loc, lang, auth, words)
                    spent += cost
                    for r in got:
                        if r["keyword"] not in seen:
                            seen.add(r["keyword"])
                            r["seed"] = seed
                            rows.append(r)
                cs, cost = clickstream([r["keyword"] for r in rows], loc, auth)
                spent += cost
                for r in rows:
                    r["clickstream"] = cs.get(r["keyword"])
                    r["observed"] = r["clickstream"] if r["clickstream"] is not None else round((r["ads"] or 0) / 3)
                    r["relevance"] = ks.relevance(r["keyword"])
                    r["winnability"] = ks.winnability(r["kd"])
                    r["opportunity"] = round(r["observed"] * r["relevance"] * r["winnability"])
                rows.sort(key=lambda r: -r["opportunity"])
                data[section].setdefault(group, {})[code] = rows
                print(f"  {code} {section:8} {group:44} {len(rows):4} keywords (running ${spent:.3f})")
        for term in SERP_TERMS:
            data["serps"][f"{term}|{code}"], cost = serp(term, loc, lang, auth)
            spent += cost
        data["ranked"][code], cost = ranked(loc, lang, auth)
        spent += cost
        print(f"  {code} serps + ranked keywords (running ${spent:.3f})")
    data["spend_usd"] = round(spent, 4)
    (out / "targeted.json").write_text(json.dumps(data, indent=1, ensure_ascii=False))
    print(f"\n  wrote {out / 'targeted.json'} · DataForSEO spend ${spent:.3f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
