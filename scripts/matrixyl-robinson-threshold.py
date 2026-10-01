#!/usr/bin/env python3
"""Add Robinson 2005's significance threshold to the three live Matrixyl hub texts, six languages, as a set-only spec.

Author: Claude (Opus 5.5) for Malcolm Smith · 2026-10-01
Decision: Malcolm, 2026-10-01 ("agree on both"): the live /pages/matrixyl-3000-research says Robinson 2005 was
"significant" in three places without saying the paper counted p <= 0.10 as significant (docs/claims/matrixyl-3000.md,
claim 6). The Robinson article and the rebuild's card f2 state it; this makes the live hub agree.

    python3 scripts/matrixyl-robinson-threshold.py            # check + show the new sentences, writes nothing
    python3 scripts/matrixyl-robinson-threshold.py --write    # write the set-only spec and keep three older specs in step
    python3 scripts/hub-upgrade.py configs/hub-upgrades/matrixyl-3000-research-robinson-threshold-2026-10-01.json --apply

Why a set-only spec: re-applying the owning spec (matrixyl-3000-research.json) would also push drift the live page does
not have (section order and backgrounds, charts CSS, references JSON-LD); the 2026-10-01 study-link spec set its one
setting the same way. The older specs that carry these texts are updated in step, so re-applying any of them gives the
same words: matrixyl-3000-research.json (evidence, usage, evidence_table), -stats-top-2026-09-23.json (usage,
evidence_table) and -study-link-2026-10-01.json (evidence).

Refuses unless every anchor occurs exactly once per locale, the specs agree with one another before the edit, and the
result keeps each locale's tag counts.
"""
import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
HU = ROOT / "configs/hub-upgrades"
BASE = HU / "matrixyl-3000-research.json"
STATS = HU / "matrixyl-3000-research-stats-top-2026-09-23.json"
LINK = HU / "matrixyl-3000-research-study-link-2026-10-01.json"
OUT = HU / "matrixyl-3000-research-robinson-threshold-2026-10-01.json"
LOCALES = ["en", "de", "nl", "fr", "es", "it"]

# The threshold, worded as the live Robinson article words it (configs/studies/matrixyl-wrinkle-trial-robinson-2005.json,
# limits "What 'significant' means here") and as the rebuild's card f2 (92bde04).
MEANS = {
    "en": "“Significant” here is the paper's own, looser bar (p ≤ 0.10; the usual bar is p ≤ 0.05).",
    "de": "„Signifikant“ heißt hier: nach der eigenen, lockereren Schwelle der Arbeit (p ≤ 0,10; üblich ist p ≤ 0,05).",
    "nl": "‘Significant’ betekent hier: volgens de eigen, ruimere grens van het artikel (p ≤ 0,10; gebruikelijk is p ≤ 0,05).",
    "fr": "« Significatif » renvoie ici au seuil propre à l'article, plus souple (p ≤ 0,10 ; le seuil habituel est p ≤ 0,05).",
    "es": "«Significativo» se refiere aquí al criterio propio del artículo, más laxo (p ≤ 0,10; el habitual es p ≤ 0,05).",
    "it": "“Significativo” si riferisce qui alla soglia dell'articolo stesso, più permissiva (p ≤ 0,10; quella abituale è p ≤ 0,05).",
}
# usage/u1: the clause joins the existing sentence ("… at weeks 8 and 12" + clause + ".")
CLAUSE = {
    "en": "by the paper's own, looser bar (p ≤ 0.10; the usual bar is p ≤ 0.05)",
    "de": "nach der eigenen, lockereren Schwelle der Arbeit (p ≤ 0,10; üblich ist p ≤ 0,05)",
    "nl": "volgens de eigen, ruimere grens van het artikel (p ≤ 0,10; gebruikelijk is p ≤ 0,05)",
    "fr": "selon le seuil propre à l'article, plus souple (p ≤ 0,10 ; le seuil habituel est p ≤ 0,05)",
    "es": "según el criterio propio del artículo, más laxo (p ≤ 0,10; el habitual es p ≤ 0,05)",
    "it": "secondo la soglia dell'articolo stesso, più permissiva (p ≤ 0,10; quella abituale è p ≤ 0,05)",
}
U1_END = {"en": "at weeks 8 and 12.", "de": "in Woche 8 und 12.", "nl": "in week 8 en 12.", "fr": "aux semaines 8 et 12.",
          "es": "en las semanas 8 y 12.", "it": "alle settimane 8 e 12."}
T3_END = {"en": "by expert graders.", "de": "von Fachgutachtern.", "nl": "deskundige beoordelaars.", "fr": "évaluateurs experts.",
          "es": "evaluadores expertos.", "it": "valutatori esperti."}
EV_END = "Robinson et al., 2005</a>). "          # the citation closes the Robinson sentence in every locale


def once(s, anchor, where):
    n = s.count(anchor)
    if n != 1:
        sys.exit(f"REFUSING: {where}: anchor {anchor!r} occurs {n} times")


def tags(s):
    return {t: len(re.findall(rf"<{t}\b", s)) for t in ("p", "a", "strong", "h2", "li")}


def transform(kind, values):
    out = {}
    for l in LOCALES:
        v = values[l]
        if MEANS[l] in v or CLAUSE[l] in v:
            sys.exit(f"REFUSING: {kind}/{l} already carries the threshold")
        if kind == "evidence":
            once(v, EV_END, f"{kind}/{l}")
            new = v.replace(EV_END, EV_END + MEANS[l] + " ")
        elif kind == "usage":
            once(v, U1_END[l], f"{kind}/{l}")
            new = v.replace(U1_END[l], U1_END[l][:-1] + ", " + CLAUSE[l] + ".")
        else:
            once(v, T3_END[l], f"{kind}/{l}")
            new = v.replace(T3_END[l], T3_END[l] + " " + MEANS[l])
        if tags(new) != tags(v):
            sys.exit(f"REFUSING: {kind}/{l} changed its markup")
        out[l] = new
    return out


def sec(spec, sid):
    return next(a for a in spec["add_sections"] if a["id"] == sid)["section"]


# The unreleased template rebuild repeats two of the texts (usage step 2, evidence row). Its custom-html sections are
# translated from a phrase table (scripts/hub-i18n.py), so the edit is to the English in the spec and to the phrase
# keys with their five translations; `hub-i18n.py … --write` then regenerates the locales. Without this, the rebuild
# going live would bring the unqualified wording back.
PHRASES = ROOT / "configs/hub-i18n/matrixyl-3000-research.json"
MERGE = HU / "matrixyl-3000-research-evidence-merge-2026-09-26.json"
DRAFT_USAGE_END = {"en": "from week 8.<", "de": "ab Woche 8.<", "nl": "vanaf week 8.<", "fr": "dès la semaine 8.<",
                   "es": "a partir de la semana 8.<", "it": "dalla settimana 8.<"}
DRAFT_ROW_END = {"en": "expert grading. ", "de": "Expertenbewertung. ", "nl": "door deskundigen. ", "fr": "par des experts. ",
                 "es": "evaluación de expertos. ", "it": "valutazione di esperti. "}


def draft_edit(s, l, kind):
    if kind == "usage":
        once(s, DRAFT_USAGE_END[l], f"draft {kind}/{l}")
        return s.replace(DRAFT_USAGE_END[l], DRAFT_USAGE_END[l][:-2] + ", " + CLAUSE[l] + ".<")
    once(s, DRAFT_ROW_END[l], f"draft {kind}/{l}")
    return s.replace(DRAFT_ROW_END[l], DRAFT_ROW_END[l] + MEANS[l] + " ")


def draft(write):
    table, merge = json.loads(PHRASES.read_text()), json.loads(MERGE.read_text())
    ph = table["phrases"]
    for kind, needle in (("usage", "found significant results from week 8.<"),
                         ("row", "significantly more than placebo from week 8, by image analysis and expert grading. ")):
        keys = [k for k in ph if needle in k]
        if len(keys) != 1:
            sys.exit(f"REFUSING: draft {kind}: {len(keys)} phrase keys match")
        old = keys[0]
        new_key = draft_edit(old, "en", kind)
        new_vals = {l: draft_edit(v, l, kind) for l, v in ph[old].items()}
        # the spec's English must contain the old key verbatim (hub-i18n substitutes by key)
        hits = [a for a in merge["add_sections"] if old in a["section"].get("settings", {}).get("html", {}).get("en", "")]
        if len(hits) != 1:
            sys.exit(f"REFUSING: draft {kind}: the key occurs in {len(hits)} evidence-merge sections")
        hits[0]["section"]["settings"]["html"]["en"] = hits[0]["section"]["settings"]["html"]["en"].replace(old, new_key)
        ph = {(new_key if k == old else k): (new_vals if k == old else v) for k, v in ph.items()}   # keep the order
        print(f"  draft {kind} ({hits[0]['id']}): …{re.sub(r'<[^>]+>', '', new_key)[-150:]}")
    table["phrases"] = ph
    if write:
        PHRASES.write_text(json.dumps(table, indent=2, ensure_ascii=False) + "\n")
        MERGE.write_text(json.dumps(merge, indent=2, ensure_ascii=False) + "\n")
        print(f"  wrote {PHRASES.name} and {MERGE.name}; now: python3 scripts/hub-i18n.py {PHRASES.relative_to(ROOT)} --write")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--draft", action="store_true", help="the unreleased rebuild's two repeats (phrase table + spec English)")
    a = ap.parse_args()
    if a.draft:
        draft(a.write)
        return 0
    base, stats, link = (json.loads(p.read_text()) for p in (BASE, STATS, LINK))
    ev = sec(base, "evidence")["blocks"]["body"]["settings"]["content"]
    u1 = sec(base, "usage")["blocks"]["u1"]["settings"]["content"]
    t3 = sec(base, "evidence_table")["blocks"]["t3"]["settings"]["value"]
    link_item = next(i for i in link["set"] if i["at"] == "evidence/body/content")
    # the specs must agree before the edit, or "in step" would copy a drift
    if link_item["values"] != ev:
        sys.exit("REFUSING: the study-link spec's evidence text differs from the base spec's")
    if sec(stats, "usage")["blocks"]["u1"]["settings"]["content"] != u1 \
            or sec(stats, "evidence_table")["blocks"]["t3"]["settings"]["value"] != t3:
        sys.exit("REFUSING: the stats-top spec's usage / evidence_table text differs from the base spec's")
    new = {"evidence/body/content": transform("evidence", ev), "usage/u1/content": transform("usage", u1),
           "evidence_table/t3/value": transform("table", t3)}
    for at, vals in new.items():
        print(f"  {at}")
        for l in LOCALES:
            s = re.sub(r"<[^>]+>", "", vals[l])
            i = s.find(MEANS[l]) if MEANS[l] in s else s.find(CLAUSE[l])
            print(f"    {l}: …{s[max(0, i - 90):i + len(MEANS[l]) + 2]}")
    if not a.write:
        print("  check only — nothing written. --write writes the spec and the three older specs in step.")
        return 0
    spec = {"_about": "GENERATED by scripts/matrixyl-robinson-threshold.py (2026-10-01, Malcolm: 'agree on both'). Sets three "
                      "settings only, each now saying Robinson 2005 counted p <= 0.10 as significant (docs/claims/matrixyl-3000.md, "
                      "claim 6). Set-only for the reason given in the study-link spec; the base, stats-top and study-link specs "
                      "carry the same words. The template rebuild (layout + evidence-merge 2026-09-26) carries them too.",
            "template": "templates/page.research-matrixyl.json", "page": link["page"],
            "set": [{"at": at, "values": vals} for at, vals in new.items()]}
    OUT.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n")
    sec(base, "evidence")["blocks"]["body"]["settings"]["content"] = new["evidence/body/content"]
    sec(base, "usage")["blocks"]["u1"]["settings"]["content"] = new["usage/u1/content"]
    sec(base, "evidence_table")["blocks"]["t3"]["settings"]["value"] = new["evidence_table/t3/value"]
    sec(stats, "usage")["blocks"]["u1"]["settings"]["content"] = new["usage/u1/content"]
    sec(stats, "evidence_table")["blocks"]["t3"]["settings"]["value"] = new["evidence_table/t3/value"]
    link_item["values"] = new["evidence/body/content"]
    for p, d in ((BASE, base), (STATS, stats), (LINK, link)):
        p.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n")
    print(f"  wrote {OUT.relative_to(ROOT)} and kept {BASE.name}, {STATS.name}, {LINK.name} in step")
    return 0


if __name__ == "__main__":
    sys.exit(main())
