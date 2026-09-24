#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the master inventory of every study Skingenetix cites.

Sources, in order of authority:
  1. the five claims registers' evidence tables  — graded, read at source
  2. the live hub pages                          — what a visitor/crawler actually sees
  3. configs/studies/*.json                      — the two pages already built

Emits a JSON index. No judgement here beyond parsing; qualification and ranking come after.
"""
import json, pathlib, re, sys

ROOT = pathlib.Path("/Users/malcolmsmith/Claude Code/Projects/skingenetix-website")
OUT = pathlib.Path(__file__).parent / "studies.json"
REG = {"argireline-acetyl-hexapeptide-8": "Argireline", "copper-peptide-ghk-cu": "Copper peptide",
       "glutathione": "Glutathione", "matrixyl-3000": "Matrixyl 3000", "pdrn": "PDRN"}

def table_rows(md, heading_re):
    """Rows of the first markdown table under a heading matching heading_re."""
    m = re.search(heading_re, md, re.M)
    if not m:
        return []
    seg = md[m.end():]
    nxt = re.search(r"^## ", seg, re.M)
    seg = seg[:nxt.start()] if nxt else seg
    rows = []
    for line in seg.splitlines():
        line = line.strip()
        if not line.startswith("|") or re.match(r"^\|[\s\-:|]+\|$", line):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 3 or cells[0].lower() in ("study", "source", "#"):
            continue
        rows.append(cells)
    return rows

studies = []
for slug, ingredient in REG.items():
    md = (ROOT / f"docs/claims/{slug}.md").read_text()
    rows = table_rows(md, r"^## \d+\. Evidence table.*$")
    for cells in rows:
        raw = " | ".join(cells)
        # some tables lead with a row-number column; the study is the first non-numeric cell
        idx = 1 if re.fullmatch(r"\d+", cells[0].strip()) and len(cells) > 1 else 0
        name = re.sub(r"\*\*", "", cells[idx])
        name = re.sub(r"\s*—.*$", "", name)          # drop the trailing description
        name = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", name).strip()
        pmids = (re.findall(r"pubmed\.ncbi\.nlm\.nih\.gov/(\d+)", raw)
                 or re.findall(r"PMID[:\s]+(\d+)", raw))
        pmcs = re.findall(r"(PMC\d+)", raw)
        dois = (re.findall(r"doi\.org/([^\s\)\]]+)", raw)
                or re.findall(r"DOI[:\s]+(10\.[^\s,\|\)]+)", raw))
        # grade is not always the last column (some tables end with "Read at source?")
        gcell = next((re.sub(r"\*\*", "", c).strip() for c in reversed(cells)
                      if re.match(r"^(A|B|C|D|X|review|Review)\b", re.sub(r"\*\*", "", c).strip())), "")
        grade = gcell or re.sub(r"\*\*", "", cells[-1]).strip()
        studies.append({
            "ingredient": ingredient, "name": name,
            "pmid": pmids[0] if pmids else None,
            "pmc": pmcs[0] if pmcs else None,
            "doi": dois[0] if dois else None,
            "grade_raw": grade,
            "design": re.sub(r"\*\*", "", cells[idx+1])[:180] if len(cells) > idx+1 else "",
            "n": re.sub(r"\*\*", "", cells[idx+2])[:90] if len(cells) > idx+2 else "",
            "row": raw[:700],
        })

# de-duplicate on (ingredient, pmid or name)
seen, uniq = set(), []
for s in studies:
    k = (s["ingredient"], s["pmid"] or s["doi"] or s["name"].lower())
    if k in seen:
        continue
    seen.add(k); uniq.append(s)

# what is already built
built = {}
for f in sorted((ROOT / "configs/studies").glob("*.json")):
    d = json.loads(f.read_text())
    built[f.stem] = {"handle": f.stem, "title": str(d.get("title", ""))[:90]}

OUT.write_text(json.dumps({"studies": uniq, "built": built}, indent=1, ensure_ascii=False))
print(f"parsed {len(studies)} rows -> {len(uniq)} distinct studies")
by = {}
for s in uniq:
    by.setdefault(s["ingredient"], []).append(s)
for ing in sorted(by):
    withid = sum(1 for s in by[ing] if s["pmid"] or s["doi"] or s["pmc"])
    print(f"  {ing:<16} {len(by[ing]):>3} studies   {withid:>3} with a PMID/DOI/PMC")
print(f"\nalready built as pages: {list(built)}")
