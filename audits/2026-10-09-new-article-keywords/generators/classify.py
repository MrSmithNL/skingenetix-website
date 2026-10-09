"""Classify adjacent-topic candidates against everything already claimed on the site or in the plan.

Reads audits/2026-10-09-new-article-keywords/candidates-{US,GB}.json and configs/page-targets.json; writes
audits/2026-10-09-new-article-keywords/classified.json. Scratch analysis for the 2026-10-09 article plan.
"""
import json, pathlib, re, sys

R = pathlib.Path("/Users/malcolmsmith/Claude Code/Projects/skingenetix-website")
D = R / "audits/2026-10-09-new-article-keywords"

def toks(s):
    s = s.lower().replace("’", "'").replace("crow's", "crows").replace("-", " ")
    s = re.sub(r"\bpeptides\b", "peptide", s)
    s = re.sub(r"\bserums\b", "serum", s); s = re.sub(r"\bcreams\b", "cream", s)
    s = re.sub(r"\bwrinkles\b", "wrinkle", s)
    return frozenset(t for t in re.findall(r"[a-z0-9]+", s) if t not in {"the", "a", "an", "for", "to", "of", "in", "on", "your", "my", "is", "are", "do", "does"})

claims = {}
pt = json.loads((R / "configs/page-targets.json").read_text())
for url, v in pt.items():
    if url.startswith("_"): continue
    for t in [v["primary"]] + v.get("secondary", []):
        claims.setdefault(toks(t), []).append(f"owner:{url}")

PLAN = {  # website-traffic-and-performance-plan-2026-10-08 Part 3 proposals, hub sections, planned spokes
    "plan-proposal": ["brightening serum", "wrinkle serum", "skin firming cream", "firming serum", "peptides for skin",
        "peptides in skincare", "what is matrixyl 3000", "glutathione for skin", "pdrn microneedling", "topical glutathione",
        "peptide cream", "kupferpeptide", "peptide hautpflege", "ghk-cu cream", "copper peptide cream", "pdrn cream",
        "glutathione serum", "copper peptide skincare", "microneedling stamp", "fine lines and wrinkles", "why skin loses firmness",
        "dull skin", "uneven skin tone", "collagen serum", "collagen cream", "does argireline work", "does copper peptide serum work",
        "matrixyl and argireline", "argireline and matrixyl", "matrixyl vs argireline", "argireline crows feet", "argireline before and after",
        "matrixyl vs copper peptides", "acetyl hexapeptide-3", "palmitoyl pentapeptide-4", "pdrn vs retinol", "what are peptides in skincare",
        "what is peptide in skincare", "skin repair cream", "glow serum", "do collagen creams work", "does pdrn work", "does pdrn really work"],
    "hub-section": ["what is salmon pdrn", "pdrn benefits", "what does pdrn do for skin", "what is pdrn in skincare", "is pdrn salmon sperm",
        "what is copper peptide", "copper peptide benefits", "what does argireline do", "what is argireline", "what does matrixyl 3000 do",
        "what is pdrn", "pdrn meaning", "what does pdrn do", "salmon dna pdrn", "what does copper peptide do for skin", "what does copper peptide do",
        "glutathione benefits for skin", "what does glutathione do for skin", "what does pdrn stand for", "what is pdrn made of",
        "acetyl hexapeptide 8", "argireline peptide", "what is matrixyl"],
    "planned-spoke": ["how to use pdrn serum", "can you use pdrn with retinol", "best pdrn serum", "pdrn vs polynucleotides", "polynucleotides vs pdrn",
        "vegan pdrn", "copper peptide with vitamin c", "copper peptide and vitamin c", "copper peptide and retinol", "copper peptide with retinol",
        "best copper peptide serum", "copper peptide side effects", "is copper peptide safe", "argireline vs botox", "matrixyl 3000 vs synthe 6",
        "glutathione side effects skin", "glutathione side effects", "peptide serum with vitamin c", "peptide and vitamin c serum", "peptide moisturizer",
        "pdrn with vitamin c"],
    "excluded": ["best peptide serum", "copper peptide before and after", "argireline before and after", "matrixyl 3000 before and after"],
}
for kind, terms in PLAN.items():
    for t in terms:
        claims.setdefault(toks(t), []).append(f"{kind}:{t}")

FORMAT_NOT_SOLD = re.compile(r"eye ?patch|\bmask\b|toner|essence|\bpad|lash|brow|eyelash|mist|spray|balm|stick|shot\b|ampoule|jelly|cleanser|sunscreen|\bspf\b|lip\b|body|hand cream|foundation|tinted", re.I)
WHITENING = re.compile(r"whiten|lighten|bleach|fairness|skin colou?r", re.I)
CONDITION = re.compile(r"acne|scar|rosacea|eczema|melasma|hyperpigment|psoria|dermatitis|wound|stretch mark|cellulite|keloid|vitiligo|fungal", re.I)
INJECT = re.compile(r"inject|filler|botox(?! alternative)|\bprp\b|treatment cost|price|near me|clinic|facial cost|\bcost\b|laser|hifu|morpheus|radiofrequency|\brf\b", re.I)
HAIR = re.compile(r"hair|scalp|beard|lash|brow", re.I)
BEFORE = re.compile(r"before and after|before after|before & after|results pictures", re.I)
BRANDS = re.compile(r"ordinary|medicube|anua|inkey|cosrx|olay|no7|paula|naturium|timeless|biodance|abib|mixsoon|dr althea|vt |torriden|isntree|skinceuticals|lancome|lancôme|la roche|cerave|neutrogena|drunk elephant|peter thomas|strivectin|niod|nip|fab|elemis|clinique|estee|estée|shiseido|sk ii|sk-ii|sulwhasoo|tatcha|glow recipe|kiehl|murad|obagi|skinbetter|zo |rejuran|dermalogica|eucerin|vichy|garnier|l'oreal|loreal|nivea|aveeno|boots|superdrug|amazon|sephora|ulta|reddit|tiktok|youtube|dior|chanel|clarins|kylie|pixi|good molecules|byoma|beauty of joseon|skin1004|round lab|numbuzin|axis y|some by mi|purito|dr\.? ?jart|innisfree|laneige|tirtir|manyo|celimax|ma:nyo|goodal|haruharu|jumiso|mary kay|avon|revox|e\.l\.f|elf |cosmedix|revision|alastin|sente|dermaquest|image skincare|eltamd|osmosis|hydropeptide|perricone|ole henriksen|first aid|tula|dennis gross|sunday riley|versed|bubble|naturium|medik8|geek|ageineer|mary and may|dizzy panda|shaishaishai|genabelle|reedle", re.I)

out = {}
for mk in ["US", "GB"]:
    rows = json.loads((D / f"candidates-{mk}.json").read_text())
    for r in rows:
        kw = r["keyword"]; tk = toks(kw)
        flags = []
        if FORMAT_NOT_SOLD.search(kw): flags.append("format-not-sold")
        if WHITENING.search(kw): flags.append("whitening")
        if CONDITION.search(kw): flags.append("condition")
        if INJECT.search(kw): flags.append("injectable/clinic")
        if HAIR.search(kw): flags.append("hair")
        if BEFORE.search(kw): flags.append("before-after")
        if BRANDS.search(kw): flags.append("brand")
        exact = claims.get(tk, [])
        near = [c for t, cs in claims.items() for c in cs if len(t) >= 2 and (t <= tk) and t != tk and len(tk - t) <= 1]
        r["claimed_exact"] = exact; r["claimed_near"] = near[:4]; r["flags"] = flags
        out.setdefault(kw, {"keyword": kw, "markets": {}, "sources": r.get("sources", []), "flags": flags,
                             "claimed_exact": exact, "claimed_near": near[:4], "kd": r.get("kd"), "intent": r.get("intent")})
        out[kw]["markets"][mk] = {"observed": r["observed"], "clickstream": r["clickstream"], "ads": r["ads"], "opp": r["opportunity"], "kd": r.get("kd")}
res = sorted(out.values(), key=lambda x: -sum(m["observed"] or 0 for m in x["markets"].values()))
(D / "classified.json").write_text(json.dumps(res, indent=1))
free = [x for x in res if not x["flags"] and not x["claimed_exact"]]
print(len(res), "keywords;", len(free), "unflagged and unclaimed")
lim = int(sys.argv[1]) if len(sys.argv) > 1 else 250
for x in free[:lim]:
    us = x["markets"].get("US", {}); gb = x["markets"].get("GB", {})
    print(f'{us.get("observed","-")!s:>6} {gb.get("observed","-")!s:>6} kd={x["kd"]!s:>4} {(x["intent"] or "")[:5]:<5} {x["keyword"]:<55} {"NEAR:"+x["claimed_near"][0] if x["claimed_near"] else ""}')
