#!/usr/bin/env python3
"""DataForSEO keyword research for Skingenetix.

Usage:
    python3 scripts/keyword-research.py --seeds seeds.txt --loc 2528 --lang nl
    python3 scripts/keyword-research.py --ideas "copper peptide serum" --loc 2840 --lang en --limit 200
    python3 scripts/keyword-research.py --volume-file terms.txt --loc 2840 --lang en

Locations: 2840 US · 2826 GB · 2528 NL · 2276 DE · 2724 ES · 2250 FR · 2380 IT

Three hard rules, each learned the expensive way on Hairgenetix:

  1. Exclude NON-TOPICAL intent, don't demand a skin word. Hairgenetix's rule
     was "every keyword needs a hair qualifier", because there "ghk cu" leaked
     to skin. Applied literally here it throws away "copper peptides" — which
     IS the head term for a skin brand. The real enemy on this store is
     injections, oral supplements, bodybuilding and lab-reagent intent.
  2. NEVER sum Google Ads volumes across variants. Ads buckets many phrasings
     onto one figure, so nine variants "each" at 12,100 is one bucket counted
     nine times. A "113,300/mo opportunity" there was bucket repetition.
  3. Clickstream beats Ads volume for naming decisions. Ads volume is modelled;
     clickstream is observed. Where they disagree on a product name, trust
     clickstream.

Credentials come from seo-toolkit/.env (DATAFORSEO_LOGIN / DATAFORSEO_PASSWORD).
Read-only against DataForSEO; writes only the local JSON you ask for.
"""
import argparse, base64, json, pathlib, re, sys, urllib.request, urllib.error

TOOLKIT = pathlib.Path.home() / "Claude Code/Projects/seo-toolkit/.env"
# Intent we never want: not topical skincare. Cheaper and more accurate than
# demanding a skin word, which would discard the head terms themselves.
OFF_INTENT = re.compile(
    r"inject|injectab|oral|capsule|tablet|supplement|iv drip|bodybuild|"
    r"calculator|reconstitut|dosage|mg\b|vial|peptide therapy|research chemical|"
    r"hair loss|hair growth|scalp|beard|weight loss|semaglutide|bpc.?157|tb.?500|"
    r"skin tag|skin cancer|mole|psoriasis|eczema|acne treatment|laser|keratin|"
    r"whitening (strip|pill)|glutathione (injection|iv|pill|capsule|drip)", re.I)


def creds():
    t = TOOLKIT.read_text()
    l = re.search(r'^DATAFORSEO_LOGIN=(.+)$', t, re.M).group(1).strip().strip('"\'')
    p = re.search(r'^DATAFORSEO_PASSWORD=(.+)$', t, re.M).group(1).strip().strip('"\'')
    return base64.b64encode(f"{l}:{p}".encode()).decode()


def post(path, payload, auth):
    r = urllib.request.Request(f"https://api.dataforseo.com/v3/{path}",
                               data=json.dumps([payload]).encode(), method="POST",
                               headers={"Authorization": f"Basic {auth}",
                                        "Content-Type": "application/json"})
    try:
        d = json.loads(urllib.request.urlopen(r, timeout=120).read())
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read()[:300].decode(errors='replace')}")
    task = d["tasks"][0]
    if task.get("status_code") != 20000:
        sys.exit(f"task error {task.get('status_code')}: {task.get('status_message')}")
    return (task.get("result") or [{}])[0]


def qualified(kw):
    """True when the term reads as topical skincare intent."""
    return not OFF_INTENT.search(kw)


def show(rows, limit, label):
    print(f"\n  === {label} — {len(rows)} keywords ===")
    print(f"  {'VOL':>7} {'CPC':>6} {'COMP':>5} {'DIFF':>5}  {'Q':<2} KEYWORD")
    for r in rows[:limit]:
        q = "✅" if qualified(r["keyword"]) else "⚠️"
        print(f"  {r['volume'] or 0:>7} {(r['cpc'] or 0):>6.2f} {(r['competition'] or 0):>5.2f} "
              f"{(r['difficulty'] if r['difficulty'] is not None else -1):>5}  {q:<2} {r['keyword'][:52]}")
    unq = [r for r in rows if not qualified(r["keyword"])]
    if unq:
        print(f"\n  ⚠️ {len(unq)} dropped as non-topical intent (rule 1). "
              f"Top: {', '.join(r['keyword'] for r in unq[:4])}")


def norm(items):
    out = []
    for i in items or []:
        ki = i.get("keyword_info") or {}
        kp = i.get("keyword_properties") or {}
        out.append({"keyword": i.get("keyword"),
                    "volume": ki.get("search_volume"),
                    "cpc": ki.get("cpc"),
                    "competition": ki.get("competition"),
                    "difficulty": kp.get("keyword_difficulty"),
                    "intent": ((i.get("search_intent_info") or {}).get("main_intent"))})
    return [r for r in out if r["keyword"]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ideas", help="seed keyword to expand semantically")
    ap.add_argument("--suggest", action="store_true",
                    help="use keyword_suggestions (terms CONTAINING the seed) "
                         "instead of keyword_ideas (semantically related)")
    ap.add_argument("--seeds", help="file of seed keywords, one per line")
    ap.add_argument("--loc", type=int, default=2840)
    ap.add_argument("--lang", default="en")
    ap.add_argument("--limit", type=int, default=60)
    ap.add_argument("--min-volume", type=int, default=10)
    ap.add_argument("--json", help="write full results here")
    a = ap.parse_args()
    auth = creds()

    seeds = []
    if a.ideas:
        seeds = [a.ideas]
    elif a.seeds:
        seeds = [l.strip() for l in pathlib.Path(a.seeds).read_text().split("\n") if l.strip()]
    else:
        sys.exit("give --ideas or --seeds")

    allrows, seen = [], set()
    for s in seeds:
        if a.suggest:
            res = post("dataforseo_labs/google/keyword_suggestions/live",
                       {"keyword": s, "location_code": a.loc, "language_code": a.lang,
                        "limit": 700, "include_serp_info": False,
                        "filters": [["keyword_info.search_volume", ">=", a.min_volume]],
                        "order_by": ["keyword_info.search_volume,desc"]}, auth)
        else:
            res = post("dataforseo_labs/google/keyword_ideas/live",
                       {"keywords": [s], "location_code": a.loc, "language_code": a.lang,
                        "limit": 700, "include_serp_info": False,
                        "filters": [["keyword_info.search_volume", ">=", a.min_volume]],
                        "order_by": ["keyword_info.search_volume,desc"]}, auth)
        rows = norm(res.get("items"))
        fresh = [r for r in rows if r["keyword"] not in seen]
        for r in fresh:
            seen.add(r["keyword"])
        allrows += fresh
        print(f"  seed {s!r:<42} → {len(rows):>4} ideas ({len(fresh)} new)")

    allrows.sort(key=lambda r: -(r["volume"] or 0))
    show(allrows, a.limit, f"loc {a.loc} / {a.lang}")
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(allrows, indent=1))
        print(f"\n  wrote {a.json}  ({len(allrows)} keywords)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
