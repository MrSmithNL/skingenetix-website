#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""What do study pages actually win, and what demand exists for ours?

Two free reads, no paid keyword data:
  A) the query shapes Hairgenetix's study articles already rank for — the best available
     predictor of what a Skingenetix study page could win
  B) Skingenetix's own impressions by ingredient, to weight the build
"""
import datetime as dt, pathlib, re, warnings
warnings.filterwarnings("ignore")
from google.oauth2 import service_account
from googleapiclient.discovery import build

creds = service_account.Credentials.from_service_account_file(
    str(pathlib.Path.home() / ".config/ga4/service-account.json"),
    scopes=["https://www.googleapis.com/auth/webmasters.readonly"])
svc = build("searchconsole", "v1", credentials=creds)
end = dt.date.today() - dt.timedelta(days=3)
start = end - dt.timedelta(days=89)

def q(site, dims, limit=25000, filters=None):
    body = {"startDate": str(start), "endDate": str(end), "dimensions": dims,
            "rowLimit": limit, "type": "web"}
    if filters:
        body["dimensionFilterGroups"] = [{"filters": filters}]
    return svc.searchanalytics().query(siteUrl=site, body=body).execute().get("rows", [])

STUDY = re.compile(r"/(study|studies|research)/|-study-|-trial-")
print(f"A) HAIRGENETIX — what query SHAPES its study pages win   ({start} to {end})")
rows = q("sc-domain:hairgenetix.com", ["page", "query"])
srows = [r for r in rows if STUDY.search(r["keys"][0])]
print(f"   {len(srows)} page+query pairs on study URLs")

SHAPES = [
    ("study / research / trial named", re.compile(r"\bstudy|studies|trial|research|clinical\b", re.I)),
    ("does it work / effectiveness",   re.compile(r"does .* work|effective|efficacy|results|proven", re.I)),
    ("before and after",               re.compile(r"before and after|before & after", re.I)),
    ("is it safe / side effects",      re.compile(r"safe|side effect|danger|harmful", re.I)),
    ("how / how to / how long",        re.compile(r"^how |how to|how long|how much", re.I)),
    ("what is / definition",           re.compile(r"^what is|^what are|^what does", re.I)),
    ("vs / comparison",                re.compile(r"\bvs\b|versus|compared|better than", re.I)),
    ("dosage / percentage",            re.compile(r"\b\d+\s?%|percent|concentration|dosage|dose", re.I)),
    ("brand / product name",           re.compile(r"hairgenetix|skingenetix", re.I)),
]
tot_i = sum(r["impressions"] for r in srows) or 1
print(f"   {'query shape':<34} {'impr':>8} {'share':>7} {'clicks':>7} {'avg pos':>8}")
for label, rx in SHAPES:
    m = [r for r in srows if rx.search(r["keys"][1])]
    i = sum(r["impressions"] for r in m); c = sum(r["clicks"] for r in m)
    p = (sum(r["position"] * r["impressions"] for r in m) / i) if i else 0
    print(f"   {label:<34} {i:>8} {i/tot_i:>6.1%} {c:>7} {p:>8.1f}")

print("\n   top 12 individual queries reaching a study page:")
for r in sorted(srows, key=lambda r: -r["impressions"])[:12]:
    print(f"     {r['impressions']:>6} impr {r['clicks']:>3} clk  pos {r['position']:5.1f}  {r['keys'][1][:62]}")

print(f"\nB) SKINGENETIX — impressions by ingredient   ({start} to {end})")
sk = q("sc-domain:skingenetix.com", ["query"])
ING = {"PDRN": r"pdrn|polynucleotide", "Copper peptide": r"copper|ghk",
       "Argireline": r"argireline|hexapeptide", "Matrixyl 3000": r"matrixyl",
       "Glutathione": r"glutathion"}
tot = sum(r["impressions"] for r in sk) or 1
print(f"   site total: {tot} impressions, {sum(r['clicks'] for r in sk)} clicks, {len(sk)} queries")
for ing, pat in ING.items():
    rx = re.compile(pat, re.I)
    m = [r for r in sk if rx.search(r["keys"][0])]
    i = sum(r["impressions"] for r in m); c = sum(r["clicks"] for r in m)
    p = (sum(r["position"] * r["impressions"] for r in m) / i) if i else 0
    print(f"   {ing:<16} {i:>6} impr {i/tot:>6.1%}  {c:>4} clicks  pos {p:>5.1f}  ({len(m)} queries)")
mstudy = [r for r in sk if re.search(r"stud|trial|research|clinical|proven|does .* work", r["keys"][0], re.I)]
print(f"   evidence-shaped queries already reaching us: {len(mstudy)} queries, "
      f"{sum(r['impressions'] for r in mstudy)} impressions")
for r in sorted(mstudy, key=lambda r: -r["impressions"])[:8]:
    print(f"     {r['impressions']:>5} impr  pos {r['position']:5.1f}  {r['keys'][0][:60]}")
