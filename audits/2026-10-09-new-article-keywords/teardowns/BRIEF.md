# Brief for the top-3 teardowns (2026-10-09)

**Job:** for each keyword below, an in-depth teardown of the pages holding positions 1 to 3 on Google today, so the article
we plan for that keyword can beat them. Positions are literal: a Reddit thread, a YouTube video or an Instagram post at #2
is torn down as what it is (title, what it says, why Google ranks it), not skipped.

## Evidence already in this folder (read it, do not re-pull)

- `serp/serp.json`: the live SERPs, 2026-10-09, desktop, depth 10, with AI Overview sources (`aio_refs`) and SERP blocks.
- `serp/raw/<market>-<slug>.json`: the full response per SERP (People Also Ask, related searches, video, forums).
- `serp/paa-related.json`: People Also Ask and related searches per SERP.
- `serp/pages.json`: the skill's page measurements (top 4 non-UGC per SERP: words, H2, tables, FAQ, video, answer-first,
  author line, dateModified, citations, schema, cloaking check).
- `serp/authority.json` (when present): referring domains per domain and per URL.
- `teardowns/measurements.jsonl`: the deep measurement of the literal top 3 (H1, H2 text, first 80 words, words, byline,
  dates, citations, named-study mentions, schema, tables, FAQ, video, product links, price, our-ingredient mentions,
  Botox/filler mentions, before/after). The `byline` field is a noisy regex: confirm the author by reading the page.
  Pages with 0 to 6 words are JavaScript-rendered: read them with WebFetch instead.
- `candidates-US.json`, `candidates-GB.json`, `classified.json`: observed monthly searches (DataForSEO clickstream).
- Earlier teardowns for format and for terms already covered: `../2026-10-07-visibility-forensics/teardown-*.md`,
  `../2026-10-08-competitor-gap-per-page/teardown-*.md`.

Fetch competitor pages with curl or WebFetch to read their content (what they cover, their angle, what they get wrong).
Never fetch skingenetix.com from Python (Cloudflare rate-limits Python; other windows are auditing). Never write to the
Shopify store. Write only your one output file.

## Format (match the 2026-10-08 compact form)

Start with a one-line tag legend (VERIFIED / PLAUSIBLE / NOT ESTABLISHED; [SERP] [FETCH] [VOL] [BL]). Then, per keyword:

1. `### "<keyword>" (<market>: observed searches a month; secondary terms with their volumes)`
2. **SERP:** organic shape (who holds 1 to 10 by type: clinic, brand, editorial, medical publisher, UGC, marketplace,
   spam), SERP features, AI Overview present and its cited sources in order, the People Also Ask questions.
3. **Top 3 factor table**, columns #1 / #2 / #3: URL and type, title, H1, opening (does it answer in the first two
   sentences?), words, H2 outline (the actual headings, shortened), named studies or citations, author and reviewer,
   dates, schema, tables, FAQ, video, images, product links or price, what they say about topical skincare vs
   procedures, referring domains (domain and page) where `authority.json` has them.
4. **Why they win** (authority, intent match, format, freshness, SERP features), each line VERIFIED or PLAUSIBLE.
5. **The gap:** what none of the three answers, answers badly, or gets wrong; which People Also Ask questions none
   answers; where the AI Overview's sources are weak.
6. **Our edge:** only what we actually have (below). If we have no real edge, say so.
7. **Recommended article:** working title (≤ 60 characters for the SEO title), the one primary keyword and 2 to 4
   secondaries, the searcher's job, an H2 outline that maps to the People Also Ask (6 to 9 H2s), the opening two
   sentences as a direction (not final copy), the table or figure that no competitor has, internal links (up to the
   parent page and the ingredient hub in the first 150 words, sideways to the study article, down to one product),
   length 800 to 1,500 words, and the safety block it needs.
8. **Claims guardrails** for this article, from the register rules below.
9. **Cannibalisation check:** which existing page or planned page could compete, and why this one does not (or does).
10. **Winnable? Target:** page one / top 3 / first, with a horizon (3, 6 or 12 months), and the one thing that decides it.

End with a short ranked summary table: keyword | demand | winnable | edge | verdict (build / build later / section on an
existing page / do not build).

## Our assets (the only ones that count as an edge)

Study articles already live in `/blogs/clinical-studies/` (appraisals of single human trials):

| Trial                                                                                                                           | What it measured (register wording)                                                                                                                                                                                                                                                                                                                                                                      | Page                                                                      |
| ------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| Wang 2013, Argireline, 45 people, 4 weeks, placebo                                                                              | "Nearly 1 in 2 saw clearly smoother-looking crow's feet in 4 weeks. On placebo: no one." (22 of 45; a count, never "48.9% reduction")                                                                                                                                                                                                                                                                    | `/blogs/clinical-studies/argireline-crows-feet-trial-wang-2013`           |
| Raikou 2017, Argireline                                                                                                         | forehead roughness −7.4% vs +4.3% on placebo at day 20, P = .022 (day 20 only)                                                                                                                                                                                                                                                                                                                           | `/blogs/clinical-studies/argireline-forehead-roughness-trial-raikou-2017` |
| Tadini 2015                                                                                                                     | firmness, only when attributed to the authors                                                                                                                                                                                                                                                                                                                                                            | `.../argireline-skin-firmness-trial-tadini-2015`                          |
| Ye 2026, PDRN, 31 women with self-reported sensitive skin, 0.1% PDRN eye cream vs 0.1% retinol, split-face, 28 days, no placebo | crow's feet down about 20 to 23%; "more than three times the crow's-feet improvement" of retinol (−23.0% vs −6.6%); visible by day 14; elasticity +44.0% vs +24.8%; firmness 29.6% vs 16.3%; eye-bag volume −14.8% vs −10.2% (never "twice"); "well tolerated by sensitive skin in clinical testing" for the ingredient only; always footnote that the 0.1% study tested the ingredient, not our product | `.../pdrn-vs-retinol-split-face-trial-ye-2026`                            |
| Yogya 2022, polynucleotide with microneedling, split-face (clinic)                                                              | call its ingredient "polynucleotide"                                                                                                                                                                                                                                                                                                                                                                     | `.../pdrn-microneedling-split-face-trial-yogya-2022`                      |
| Badenhorst 2016, GHK-Cu, 40 women, 8 weeks, double-blind, funded by the maker                                                   | "reduced wrinkle volume 55.8% more than the plain serum base"; "31.6% more than a Matrixyl 3000 product" (volume only, never name the brand); well tolerated by 39 of 40                                                                                                                                                                                                                                 | `.../copper-peptide-wrinkle-trial-badenhorst-2016`                        |
| Robinson 2005, palmitoyl pentapeptide-4 ("Matrixyl", never "Matrixyl 3000"), 93 women, 12 weeks, P&G                            | serum only; must carry the p ≤ 0.10 threshold                                                                                                                                                                                                                                                                                                                                                            | `.../matrixyl-wrinkle-trial-robinson-2005`                                |
| Watanabe 2014, 2% glutathione (GSSG) lotion, 30 women, 10 weeks, maker-run                                                      | pigment −10.7% vs −3.1%; 77% vs 23% saw brighter-looking skin; crow's feet visibly softer in 1 in 3 vs none (ratings only)                                                                                                                                                                                                                                                                               | `.../glutathione-skin-brightening-trial-watanabe-2014`                    |

Also: Sederma's own 2-month study of Matrixyl 3000 at 3%, 23 women: deep-wrinkle **area** −39.4% (maker's study; say so).
Li 2015: 134 nmol of GHK-Cu passed through microneedled excised skin (amount, not depth). Product facts: PDRN 1% (10,000
ppm, stated on the label), salmon-derived sodium DNA, serum 30 ml, night cream 50 ml; GHK-Cu 2% in the serum, day
gel-cream and night cream; Argireline serum, Matrixyl 3000 serum and cream; glutathione 2% serum; PDRN and copper
microneedling stamp sets (pre-order status unresolved). Hubs: `/pages/pdrn-research`, `/pages/acetyl-hexapeptide-8-research`,
`/pages/copper-peptide-research`, `/pages/matrixyl-3000-research`, `/pages/glutathione-research`. Concern pages:
`/pages/skin-concerns` (parent), `/pages/fine-lines-wrinkles`, `/pages/firming-skin-density`. Author is the team credit
"Skingenetix Research Team"; reviewer Dr Bodde.

## Wording rules (from `docs/claims/*.md`; an article that breaks one is not buildable)

- Claims are about the ingredient as studied, never "our serum is clinically proven". Strongest supported claim, worded
  positively. Positive results only; no article built on a null study.
- Never: Botox or injection equivalence ("Botox in a bottle", "Botox-like", "alternative to injections", "Rejuran in a
  bottle", "same as injections"); relaxes muscles / blocks nerves; DNA repair, regeneration, stem cells; reaches the
  dermis / penetrates deep; stimulates or boosts collagen (as our claim); heals, repairs, wounds, scars; medical conditions
  (acne, rosacea, eczema, melasma, hyperpigmentation); whitening or lightening (glutathione is "brightening /
  brighter-looking" only); "safe", "hypoallergenic", "suitable for sensitive skin", "pregnancy-safe"; "clinically proven";
  comparisons with retinol or tretinoin beyond PDRN's framed Ye result; naming competitor brands; synergy claims.
- Allowed when framed "different, does not transfer": explaining what an injection or clinic treatment is, as context,
  without equating a topical to it. Procedures can be named as the options a reader may consider with a professional.
- Safety block on every article: patch test; not tested in pregnancy, ask a doctor or pharmacist; what not to combine
  (copper: pure L-ascorbic acid, strong acids and high-strength retinol at a different time of day, no combination
  trialled; PDRN: not on broken skin, not with a fish allergy); when to see a professional.
- Microneedling: no register covers its safety; the Argireline register says never suggest using the serum with DIY
  microneedling, while the copper register sells the stamp with GHK-Cu. Flag this conflict in any microneedling article.
- Excluded topics: before-and-after pages (our images are illustrations), "best peptide serum", whitening, injectables
  or clinic treatments as the subject, oral supplements, hair.
