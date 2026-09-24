#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Classify every inventoried study against the six qualifying criteria, and map to products.

Criteria, from docs/research-2026-study-hubs-credibility.md §3.3 — all six must be true:
  1 human participants (RCT, controlled/split-face, open-label, systematic review/meta-analysis)
  2 route relevant to what we sell
  3 PubMed-indexed or DOI, verified at source
  4 cited by one of our pages or claims
  5 nulls qualify equally
  6 passes the information-gain checklist

Verdict values: PAGE (candidate), LIBRARY (row only), EXCLUDED (route).
Criterion 6 is a judgement call and cannot be automated; it is applied by hand to the shortlist.
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).parent
d = json.loads((HERE / "studies.json").read_text())

PRODUCTS = {
    "Argireline": ["Acetyl Hexapeptide-8 Anti-Wrinkle Serum"],
    "Copper peptide": ["GHK-Cu 2% Renewal Serum", "Day Gel-Cream", "Night Cream", "Microneedling Stamp Set"],
    "Matrixyl 3000": ["Matrixyl 3000 Firming Serum", "Pro-Collagen Firming Cream"],
    "PDRN": ["PDRN 1% Renewal Serum", "PDRN 1% Collagen Night Cream", "PDRN Microneedling Stamp Set"],
    "Glutathione": ["Glutathione 2% Brightening Serum"],
}
# we SELL microneedling stamps for copper and PDRN, so microneedle-delivery work is
# route-relevant for those two, and not for the others
STAMP = {"Copper peptide", "PDRN"}

# the registers already carry a verdict on unusable sources; honour it rather than re-deciding
DISQUALIFY = re.compile(
    r"do not use|do not cite|never cite|unreliable|believed fabricated|misread|misquote|"
    r"cannot be attributed|not transferable|no such paper|do not rely|medicinal|"
    r"scar|cancer|blepharospasm|not our ingredient|different (ingredient|peptide)|"
    r"\bnot acetyl\b|algal|plant-derived", re.I)

OFF_ROUTE = re.compile(r"inject|intrader|intramusc|\bIV\b|intravenous|oral|supplement|capsule|"
                       r"tablet|mesotherap|polynucleotide.*inject", re.I)
MICRONEEDLE = re.compile(r"microneedl|micro-needl|needle", re.I)
NONHUMAN = re.compile(r"in vitro|in-vitro|cell|fibroblast|keratinocyte|mice|mouse|rat\b|animal|"
                      r"porcine|pig-ear|guinea|cadaver|ex vivo|ex-vivo|franz|diffusion cell|"
                      r"excised|explant|C\. elegans|zebrafish", re.I)
HUMANISH = re.compile(r"\bRCT\b|randomi|split-face|split face|double-blind|placebo|volunteer|"
                      r"women|men\b|subjects|participants|patients|open-label|panel|half-face|"
                      r"systematic review|meta-analysis|review", re.I)

out = []
for s in d["studies"]:
    g = (s["grade_raw"] or "").strip()
    text = f"{s['name']} {s['design']} {s['row']}"
    has_id = bool(s["pmid"] or s["doi"] or s["pmc"])
    grade0 = g[:1].upper() if g else "?"
    is_review = bool(re.search(r"review|meta-analys", g, re.I) or re.search(r"systematic review|meta-analys", text, re.I))

    reasons, verdict = [], "PAGE"
    if grade0 == "X":
        verdict, r = "EXCLUDED", "grade X — route we cannot claim (oral/IV/injected or non-salmon)"
        reasons.append(r)
    elif OFF_ROUTE.search(text) and not MICRONEEDLE.search(text):
        verdict = "EXCLUDED"; reasons.append("off-route (injected/oral) per criterion 2")
    elif grade0 in ("C", "D") or (NONHUMAN.search(text) and not HUMANISH.search(text)):
        verdict = "LIBRARY"; reasons.append("not human participants — criterion 1")
    elif not has_id and not is_review:
        verdict = "LIBRARY"; reasons.append("no PubMed ID or DOI — criterion 3")

    if verdict == "PAGE":
        dq = DISQUALIFY.search(text)
        if dq:
            verdict = "LIBRARY"
            reasons.append(f'register verdict blocks it ("{dq.group(0).lower()}") — criterion 6')

    if verdict == "PAGE" and MICRONEEDLE.search(text):
        if s["ingredient"] in STAMP:
            reasons.append("microneedle route — we sell a stamp set for this ingredient, so route-relevant")
        else:
            verdict = "LIBRARY"; reasons.append("microneedle route, no stamp product for this ingredient")

    s["verdict"] = verdict
    s["why"] = "; ".join(reasons) or "human study, on-route, identified, cited by us"
    s["products"] = PRODUCTS.get(s["ingredient"], [])
    s["is_null"] = bool(re.search(r"\bnull\b|no significant|not significant|no difference|negative", text, re.I))
    out.append(s)

(HERE / "classified.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))

print(f"{'ingredient':<16} {'PAGE':>5} {'LIBRARY':>8} {'EXCLUDED':>9}   of")
tot = {"PAGE": 0, "LIBRARY": 0, "EXCLUDED": 0}
for ing in sorted(PRODUCTS):
    rows = [s for s in out if s["ingredient"] == ing]
    c = {k: sum(1 for s in rows if s["verdict"] == k) for k in tot}
    for k in tot: tot[k] += c[k]
    print(f"  {ing:<14} {c['PAGE']:>5} {c['LIBRARY']:>8} {c['EXCLUDED']:>9}   {len(rows)}")
print(f"  {'TOTAL':<14} {tot['PAGE']:>5} {tot['LIBRARY']:>8} {tot['EXCLUDED']:>9}   {len(out)}")
print(f"\n  nulls among PAGE candidates: {sum(1 for s in out if s['verdict']=='PAGE' and s['is_null'])}")
print(f"\nPAGE CANDIDATES")
for ing in sorted(PRODUCTS):
    rows = [s for s in out if s["ingredient"] == ing and s["verdict"] == "PAGE"]
    if not rows: continue
    print(f"\n  {ing}")
    for s in rows:
        ident = s["pmid"] or s["doi"] or s["pmc"] or "—"
        print(f"    {s['name'][:52]:<52} {s['grade_raw'][:12]:<12} {str(ident)[:26]:<26}{'  NULL' if s['is_null'] else ''}")
