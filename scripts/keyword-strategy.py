#!/usr/bin/env python3
"""Build the Skingenetix keyword strategy: pull, de-bucket, enrich, score, assign.

    python3 scripts/keyword-strategy.py pull      --out configs/keyword-data/strategy
    python3 scripts/keyword-strategy.py analyse   --dir configs/keyword-data/strategy

WHY THIS EXISTS, AND THE ONE THING IT FIXES
-------------------------------------------
Google Ads search volume is modelled and *bucketed*: many phrasings share one
figure, so a keyword list reads as far bigger than the demand behind it. On this
catalogue the distortion is not marginal:

    ghk copper peptide   Ads 135,000  →  clickstream    757   (178x inflated)
    copper peptide       Ads  33,100  →  clickstream  1,362   ( 24x)
    pdrn                 Ads  49,500  →  clickstream 19,734   (  2.5x)

Ranking families by Ads volume puts copper peptide first. Ranking by *observed*
clickstream puts PDRN first by a wide margin. This script therefore treats
clickstream as the traffic signal and Ads volume as corroboration only.

SCORING
-------
    opportunity = observed_volume x relevance x winnability

  observed   clickstream volume (falls back to Ads/3 when clickstream is absent,
             which is roughly the median ratio measured on this catalogue)
  relevance  1.0  names an ingredient we actually sell
             0.6  generic category term we could plausibly win
             0.15 competitor-branded (real demand, not our audience)
             0.0  off-intent - injections, oral, hair, lab reagent, conditions
  winnable   1.0 at KD<=10, tapering to 0.3 at KD>=40

PAGE ASSIGNMENT
---------------
    transactional  + names a product we sell  -> PRODUCT page
    transactional  + category/plural          -> COLLECTION page
    commercial     ("best X", comparisons)    -> ARTICLE (commercial guide)
    informational  + head term                -> HUB page
    informational  + long tail                -> ARTICLE (spoke)

Read-only against DataForSEO and Shopify. Writes only the JSON you ask for.
"""
import argparse, base64, json, pathlib, re, sys, time, urllib.request, urllib.error
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parent.parent
TOOLKIT = pathlib.Path.home() / "Claude Code/Projects/seo-toolkit/.env"

MARKETS = [
    ("US", 2840, "en"), ("GB", 2826, "en"), ("DE", 2276, "de"),
    ("NL", 2528, "nl"), ("FR", 2250, "fr"), ("ES", 2724, "es"), ("IT", 2380, "it"),
]

# Seeds grouped by the product family they serve. Kept here rather than derived
# from Shopify titles because the titles are long marketing strings; these are
# the words people actually type.
FAMILIES = {
    "pdrn":        ["pdrn", "polynucleotide skin", "salmon dna skin"],
    "copper":      ["copper peptide", "ghk-cu"],
    "argireline":  ["argireline", "acetyl hexapeptide"],
    "matrixyl":    ["matrixyl 3000", "palmitoyl tripeptide"],
    "glutathione": ["glutathione serum", "glutathione skin"],
    "generic":     ["peptide serum", "peptide cream", "peptide skincare"],
    "concern":     ["fine lines wrinkles serum", "skin firming serum",
                    "skin brightening serum", "skin repair serum"],
    "brand":       ["skingenetix"],
}

OFF_INTENT = re.compile(
    r"inject|injectab|\boral\b|capsule|kapsel|tablet|supplement|iv drip|bodybuild|"
    r"calculator|reconstitut|dosage|\bmg\b|vial|peptide therapy|research chemical|"
    r"hair loss|hair growth|scalp|beard|haar|haare|cheveux|capelli|cabello|hair density|"
    r"weight loss|semaglutide|bpc.?157|"
    r"tb.?500|skin tag|skin cancer|\bmole\b|psoriasis|eczema|acne treatment|laser|"
    r"keratin|whitening (strip|pill)|glutathione (injection|iv|pill|capsule|drip)|"
    r"before and after injection|\bfiller\b|botox injection", re.I)

COMPETITOR = re.compile(
    r"medicube|anua|the ordinary|ordinary|niod|timeless|cosrx|beauty of joseon|olay|no7|"
    r"paula|inkey|naturium|bioeffect|skin biology|dr ?rashel|mixsoon|isntree|torriden|"
    r"round lab|haruharu|axis-y|mary kay|avon|jumiso|goodal|numbuzin|tirtir|skin1004|"
    r"revox|hanskin|abib|some by mi|vt cosmetics|perricone|manyo|aplb|rejuran|maruderm|"
    r"nivea|loreal|l'oreal|garnier|vichy|eucerin|cerave|revolution|deciem|sephora|douglas|"
    r"amazon|idealo|notino|boots|superdrug", re.I)

# Ingredient words that mean "we sell this"
OURS = re.compile(r"pdrn|polynucleotide|salmon dna|copper peptide|ghk|argireline|"
                  r"acetyl hexapeptide|matrixyl|palmitoyl|glutathion", re.I)

# A named competitor list can never be complete — this catalogue surfaced Theramid,
# Rejuall, Dr Althea, Centellian, Geek & Gorgeous and Lico, none of which were on it.
# So instead: anything OUTSIDE a known cosmetic/question vocabulary is treated as a
# brand token. Generic across all seven languages, and fails safe (an unknown word
# downgrades relevance rather than inflating it).
VOCAB = set("""
pdrn polynucleotide polynucleotides salmon dna copper peptide peptides ghk cu argireline
acetyl hexapeptide matrixyl palmitoyl tripeptide tetrapeptide oligopeptide glutathione
serum serums cream creams creme crema cremes gel lotion ampoule essence toner booster mask
skin skincare face facial wrinkle wrinkles line lines fine anti aging ageing age firming
firm bright brightening glow repair renewal renew collagen elasticity pores pore dark spot
spots eye eyes neck day night routine set duo
best top good better review reviews compare comparison vs versus alternative alternatives
what is are how to use does do can why which when where benefits benefit side effects safe
work works meaning guide price buy shop online kopen kaufen acheter comprar comprare
und oder mit fur für was ist wie wirkung erfahrungen creme haut gesicht falten
voor met huid gezicht rimpels wat hoe werking
pour avec peau visage rides quest quel comment fonctionne
para con piel rostro arrugas que como funciona
per con pelle viso rughe cosa come funziona
the a an of for with and or in on my your s percent to no 10 30 50
""".split())

def brandish(kw):
    """True when the phrase carries a token that is not cosmetic vocabulary."""
    toks = re.findall(r"[a-z\u00e0-\u00ff0-9]+", kw.lower())
    # >=2 not >2: two-letter brand prefixes are common in K-beauty ("vt pdrn").
    unknown = [x for x in toks if x not in VOCAB and not x.isdigit() and len(x) >= 2]
    return len(unknown) > 0


# ---------------------------------------------------------------- transport
def auth():
    t = TOOLKIT.read_text()
    l = re.search(r'^DATAFORSEO_LOGIN=(.+)$', t, re.M).group(1).strip().strip('"\'')
    p = re.search(r'^DATAFORSEO_PASSWORD=(.+)$', t, re.M).group(1).strip().strip('"\'')
    return base64.b64encode(f"{l}:{p}".encode()).decode()


def post(path, payload, a, retries=3):
    for n in range(retries):
        r = urllib.request.Request(f"https://api.dataforseo.com/v3/{path}",
                                   data=json.dumps([payload]).encode(), method="POST",
                                   headers={"Authorization": f"Basic {a}",
                                            "Content-Type": "application/json"})
        try:
            d = json.loads(urllib.request.urlopen(r, timeout=180).read())
            tk = d["tasks"][0]
            if tk.get("status_code") != 20000:
                print(f"     task {tk.get('status_code')}: {tk.get('status_message')}")
                return None, 0.0
            return (tk.get("result") or [None])[0], d.get("cost", 0.0)
        except urllib.error.HTTPError as e:
            if e.code == 429 and n < retries - 1:
                time.sleep(5 * (n + 1)); continue
            print(f"     HTTP {e.code}: {e.read()[:160].decode(errors='replace')}")
            return None, 0.0
        except Exception as e:
            if n < retries - 1:
                time.sleep(3); continue
            print(f"     {type(e).__name__}: {str(e)[:120]}")
            return None, 0.0
    return None, 0.0


def norm(items):
    out = []
    for i in items or []:
        ki = i.get("keyword_info") or {}
        kp = i.get("keyword_properties") or {}
        si = i.get("search_intent_info") or {}
        kw = i.get("keyword")
        if not kw:
            continue
        out.append({"keyword": kw,
                    "ads": ki.get("search_volume"),
                    "cpc": ki.get("cpc"),
                    "competition": ki.get("competition"),
                    "kd": kp.get("keyword_difficulty"),
                    "intent": si.get("main_intent")})
    return out


# ---------------------------------------------------------------- pull
def cmd_pull(a):
    A = auth()
    out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
    spent = 0.0
    for code, loc, lang in MARKETS:
        if a.markets and code not in a.markets:
            continue
        path = out / f"raw-{code}.json"
        if path.exists() and not a.force:
            print(f"  {code}: cached ({len(json.loads(path.read_text()))} kw) — use --force to re-pull")
            continue
        seen, rows = set(), []
        for fam, seeds in FAMILIES.items():
            for s in seeds:
                res, cost = post("dataforseo_labs/google/keyword_suggestions/live",
                                 {"keyword": s, "location_code": loc, "language_code": lang,
                                  "limit": a.limit, "include_serp_info": False,
                                  "filters": [["keyword_info.search_volume", ">=", 10]],
                                  "order_by": ["keyword_info.search_volume,desc"]}, A)
                spent += cost or 0
                got = norm((res or {}).get("items"))
                fresh = [r for r in got if r["keyword"] not in seen]
                for r in fresh:
                    seen.add(r["keyword"]); r["family"] = fam
                rows += fresh
        path.write_text(json.dumps(rows, indent=1))
        print(f"  {code}: {len(rows):>5} keywords   (running cost ${spent:.2f})")
    print(f"\n  total DataForSEO spend this run: ${spent:.2f}")
    return 0


# ---------------------------------------------------------------- de-bucket
def bucket(rows):
    """Collapse Ads volume buckets.

    Ads returns identical volume+cpc for phrasings it treats as one bucket
    ('copper peptide serum' / 'serum with copper peptide'). Grouping on
    (volume, cpc, token-set) collapses them; the canonical form is the shortest
    natural phrasing, which is what a title tag should use.
    """
    groups = defaultdict(list)
    for r in rows:
        if not r.get("ads"):
            continue
        key = (r["ads"], round(r.get("cpc") or 0, 2), frozenset(re.findall(r"[a-z0-9]+", r["keyword"].lower())))
        groups[key].append(r)
    out = []
    for key, members in groups.items():
        members.sort(key=lambda r: (len(r["keyword"]), r["keyword"]))
        canon = dict(members[0])
        canon["variants"] = [m["keyword"] for m in members[1:]]
        canon["bucket_size"] = len(members)
        out.append(canon)
    return out


def relevance(kw):
    if OFF_INTENT.search(kw):
        return 0.0
    if COMPETITOR.search(kw) or brandish(kw):
        return 0.15
    if OURS.search(kw):
        return 1.0
    return 0.6


def winnability(kd):
    if kd is None:
        return 0.7
    if kd <= 10:
        return 1.0
    if kd >= 40:
        return 0.3
    return 1.0 - (kd - 10) * (0.7 / 30)


def page_type(r):
    kw, it = r["keyword"].lower(), (r.get("intent") or "")
    if re.search(r"\bbest\b|\bvs\b|\bversus\b|compare|alternative|review", kw):
        return "ARTICLE (commercial guide)"
    if it == "informational" or re.match(r"^(what|why|how|does|is|are|can|was|wie|welche|qu|come|cosa|que|qué)\b", kw):
        return "HUB" if len(kw.split()) <= 4 else "ARTICLE (spoke)"
    if it in ("transactional", "commercial"):
        if re.search(r"\bserums\b|\bcreams\b|\bproducts\b|skincare|\bpeptides\b|"
                     r"\bcremes\b|\bproducten\b|\bprodukte\b|\bproduits\b", kw):
            return "COLLECTION"
        return "PRODUCT"
    return "ARTICLE (spoke)"


def cmd_analyse(a):
    A = auth()
    d = pathlib.Path(a.dir)
    files = sorted(d.glob("raw-*.json"))
    if not files:
        sys.exit(f"no raw-*.json in {d} — run `pull` first")

    enriched_all = {}
    for f in files:
        code = f.stem.split("-")[1]
        loc, lang = next((l, g) for c, l, g in MARKETS if c == code)
        rows = json.loads(f.read_text())
        buckets = bucket(rows)
        buckets = [b for b in buckets if relevance(b["keyword"]) > 0]
        buckets.sort(key=lambda r: -(r["ads"] or 0))
        head = buckets[:a.top]

        # Clickstream: observed volume. Cached, so re-analysis costs nothing.
        cache_p = d / f"clickstream-{code}.json"
        cs = json.loads(cache_p.read_text()) if cache_p.exists() else {}
        head = [b for b in head if True]
        missing = [b["keyword"] for b in head if b["keyword"] not in cs]
        if missing:
            print(f"     {code}: fetching clickstream for {len(missing)} new keywords")
        for i in range(0, len(missing), 700):
            chunk = missing[i:i + 700]
            res, _ = post("keywords_data/clickstream_data/bulk_search_volume/live",
                          {"keywords": chunk, "location_code": loc, "language_code": lang}, A)
            for it in (res or {}).get("items", []):
                cs[it.get("keyword")] = it.get("search_volume")
        cache_p.write_text(json.dumps(cs))

        for b in head:
            b["clickstream"] = cs.get(b["keyword"])
            observed = b["clickstream"] if b["clickstream"] is not None else round((b["ads"] or 0) / 3)
            b["observed"] = observed
            b["relevance"] = relevance(b["keyword"])
            b["winnability"] = round(winnability(b.get("kd")), 2)
            b["opportunity"] = round(observed * b["relevance"] * b["winnability"])
            b["page"] = page_type(b)
            b["inflation"] = round((b["ads"] or 0) / observed, 1) if observed else None
        enriched_all[code] = head
        print(f"  {code}: {len(rows)} raw → {len(buckets)} buckets → enriched top {len(head)}")

    outp = d / "strategy.json"
    outp.write_text(json.dumps(enriched_all, indent=1))
    print(f"\n  wrote {outp}")

    for code, rows in enriched_all.items():
        rows = [r for r in rows if r["opportunity"] > 0]
        rows.sort(key=lambda r: -r["opportunity"])
        print(f"\n  ══════ {code} — top {min(a.show, len(rows))} by opportunity ══════")
        print(f"  {'OPP':>7}{'OBS':>7}{'ADS':>8}{'INFL':>6}{'KD':>4}  {'PAGE':<26} KEYWORD")
        for r in rows[:a.show]:
            print(f"  {r['opportunity']:>7}{r['observed']:>7}{r['ads'] or 0:>8}"
                  f"{(str(r['inflation'])+'x' if r['inflation'] else '—'):>6}"
                  f"{(r.get('kd') if r.get('kd') is not None else -1):>4}  {r['page']:<26} {r['keyword'][:44]}")
    return 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("pull"); p.add_argument("--out", default="configs/keyword-data/strategy")
    p.add_argument("--limit", type=int, default=700); p.add_argument("--force", action="store_true")
    p.add_argument("--markets", nargs="*")
    q = sub.add_parser("analyse"); q.add_argument("--dir", default="configs/keyword-data/strategy")
    q.add_argument("--top", type=int, default=400); q.add_argument("--show", type=int, default=30)
    a = ap.parse_args()
    return cmd_pull(a) if a.cmd == "pull" else cmd_analyse(a)


if __name__ == "__main__":
    sys.exit(main())
