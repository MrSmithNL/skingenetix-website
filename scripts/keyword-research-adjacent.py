#!/usr/bin/env python3
"""Adjacent-topic keyword pull: the topics the ingredient-seeded strategy pull could not see.

    python3 scripts/keyword-research-adjacent.py pull    --dir audits/2026-10-09-new-article-keywords
    python3 scripts/keyword-research-adjacent.py enrich  --dir audits/2026-10-09-new-article-keywords

Why: scripts/keyword-strategy.py (2026-09-22) used phrase-match suggestions on ingredient names, so a keyword
had to contain "pdrn", "copper peptide" etc. to be collected, and each seed stopped at its top 700 by Ads
volume. Polynucleotides, peptides in general, retinol alternatives, at-home microneedling, concern questions
and routines were never pulled, nor the question long tail of the ingredient terms. Malcolm, 2026-10-09:
"do deep research to understand what other relevant keywords we should write content for".

Seeds live in <dir>/seeds.json (three methods per group: phrase-match `suggest`, question-filtered `q`, and
Google's related-searches graph `related`). Reuses keyword-strategy.py's auth, transport, de-bucketing,
relevance and winnability, so the scores compare with the strategy's. Read-only against DataForSEO; writes
only JSON under --dir. Prints the spend.
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


def suggestions(seed, loc, lang, a, limit, regex=None):
    filters = [["keyword_info.search_volume", ">=", 10]]
    if regex:
        filters += ["and", ["keyword", "regex", regex]]
    res, cost = ks.post("dataforseo_labs/google/keyword_suggestions/live",
                        {"keyword": seed, "location_code": loc, "language_code": lang, "limit": limit,
                         "include_serp_info": False, "filters": filters,
                         "order_by": ["keyword_info.search_volume,desc"]}, a)
    return ks.norm((res or {}).get("items")), cost or 0.0


def related(seed, loc, lang, a, limit):
    res, cost = ks.post("dataforseo_labs/google/related_keywords/live",
                        {"keyword": seed, "location_code": loc, "language_code": lang, "depth": 2,
                         "limit": limit}, a)
    items = [i.get("keyword_data") or {} for i in (res or {}).get("items") or []]
    return ks.norm(items), cost or 0.0


def cmd_pull(a):
    d = pathlib.Path(a.dir)
    seeds = json.loads((d / "seeds.json").read_text())
    regex = seeds["question_regex"]
    A = ks.auth()
    spent = 0.0
    for code, loc, lang in MARKETS:
        path = d / f"raw-{code}.json"
        if path.exists() and not a.force:
            print(f"  {code}: cached — use --force to re-pull")
            continue
        rows = {}
        for group, g in seeds["groups"].items():
            jobs = ([("suggest", s) for s in g.get("suggest", [])] + [("q", s) for s in g.get("q", [])]
                    + [("related", s) for s in g.get("related", [])])
            for method, seed in jobs:
                if method == "suggest":
                    got, cost = suggestions(seed, loc, lang, A, 400)
                elif method == "q":
                    got, cost = suggestions(seed, loc, lang, A, 700, regex)
                else:
                    got, cost = related(seed, loc, lang, A, 300)
                spent += cost
                for r in got:
                    row = rows.setdefault(r["keyword"], {**r, "sources": []})
                    row["sources"].append(f"{group}:{method}:{seed}")
                print(f"  {code} {group:<17} {method:<8} {seed:<28} {len(got):>4} kw  (${spent:.2f})")
        path.write_text(json.dumps(list(rows.values()), indent=1))
        print(f"  {code}: {len(rows)} unique keywords")
    print(f"\n  DataForSEO spend this run: ${spent:.2f}")
    return 0


def cmd_enrich(a):
    d = pathlib.Path(a.dir)
    A = ks.auth()
    spent = 0.0
    for code, loc, lang in MARKETS:
        rows = json.loads((d / f"raw-{code}.json").read_text())
        buckets = [b for b in ks.bucket(rows) if ks.relevance(b["keyword"]) > 0 and (b["ads"] or 0) >= a.min_ads]
        cache_p = d / f"clickstream-{code}.json"
        cs = json.loads(cache_p.read_text()) if cache_p.exists() else {}
        missing = [b["keyword"] for b in buckets if b["keyword"] not in cs]
        for i in range(0, len(missing), 700):
            res, cost = ks.post("keywords_data/clickstream_data/bulk_search_volume/live",
                                {"keywords": missing[i:i + 700], "location_code": loc, "language_code": lang}, A)
            spent += cost or 0
            for it in (res or {}).get("items", []):
                cs[it.get("keyword")] = it.get("search_volume")
        cache_p.write_text(json.dumps(cs))
        for b in buckets:
            b["clickstream"] = cs.get(b["keyword"])
            b["observed"] = b["clickstream"] if b["clickstream"] is not None else round((b["ads"] or 0) / 3)
            b["relevance"] = ks.relevance(b["keyword"])
            b["winnability"] = round(ks.winnability(b.get("kd")), 2)
            b["opportunity"] = round(b["observed"] * b["relevance"] * b["winnability"])
            b["page"] = ks.page_type(b)
        buckets.sort(key=lambda r: -r["opportunity"])
        (d / f"candidates-{code}.json").write_text(json.dumps(buckets, indent=1))
        print(f"  {code}: {len(rows)} raw → {len(buckets)} buckets enriched (clickstream cache {len(cs)})")
    print(f"\n  DataForSEO spend this run: ${spent:.2f}")
    return 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("pull"); p.add_argument("--dir", required=True); p.add_argument("--force", action="store_true")
    q = sub.add_parser("enrich"); q.add_argument("--dir", required=True)
    q.add_argument("--min-ads", type=int, default=20)
    a = ap.parse_args()
    return {"pull": cmd_pull, "enrich": cmd_enrich}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
