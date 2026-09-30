# Audit tracker — skingenetix.com

Open issues from the central SEO / GEO / AISO audit (`seo-toolkit`, criteria v2), triaged by the
`seo-aiso-validator` loop rules. Fixes that change a published page go live only with Malcolm's go.

## Clinical-study articles — first audit, 2026-09-29

Four articles under `/blogs/clinical-studies/`, audited twice (engine before and after the fixes this run prompted).
Reports: `page-audit-2026-09-29-*.md` / `.json` (run 1) and `…-run2.txt` / `.json` (run 2); both runs read together:
`summary-2026-09-29-clinical-studies-run2.md`. Every finding was checked on the live page by hand.

| Article                                  | Score (run 1 → run 2) | Confirmed failures                                                       |
| ---------------------------------------- | --------------------- | ------------------------------------------------------------------------ |
| Wang 2013 — Argireline, crow's feet      | 8.93 → 8.99           | duplicated study + four empty sections · safety · no link to its sibling |
| Raikou 2017 — Argireline, forehead lines | 9.10 → 9.22           | safety · the hub does not link to it                                     |
| Badenhorst 2016 — copper peptide         | 8.73 → 9.26           | keyword not in the title (safety: split 2–2 in run 2)                    |
| Ye 2026 — PDRN vs retinol                | 8.47 → 8.79           | duplicated study + empty sections · safety                               |

A difference under ~0.9 is within the audit's measured noise. The score is a diagnostic, not a ranking forecast.

**The bar (Malcolm, 2026-09-30, ADR-2026-09-30-Q).** A page is done when all gates pass, there are no confirmed failures, **and** the
score is 9.0 or more.

### Re-audit, 2026-09-30

| Article                                         | Score    | Gates                        | Coverage          | Confirmed failures       | Report                                                                  |
| ----------------------------------------------- | -------- | ---------------------------- | ----------------- | ------------------------ | ----------------------------------------------------------------------- |
| Badenhorst 2016 (the reference format, Malcolm) | **9.78** | 5 pass, hreflang not checked | 39 of 51 assessed | **none**; contested none | `page-audit-2026-09-30-copper-peptide-wrinkle-trial-badenhorst-2016.md` |

- **Status:** done, with no fix round needed. Dimension scores: query fit 9.64, content 9.44, and 10.0 on the other six.
- **Lone objections:** one judge each marked Q3 (intent), C2 (facts) and C4 (consistency) unmet, with no reasons recorded. They are
  not confirmed, so there is nothing to fix.
- **Cost:** USD 1.08.
- **Next:** Raikou, Wang and Ye are audited after they are rebuilt in this format (Malcolm: "the others aren't yet").

### Done — live 2026-09-30 (Malcolm: "yes")

| #   | Issue                                                                                     | What changed                                                                                                                                                                                       | Verified                                                                                  |
| --- | ----------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| 1   | Pilot studies (Wang, Ye) rendered twice with seven empty headings and the reference twice | New `templates/article.clinical-study-pilot.json` (banner, body, note, JSON-LD); both articles switched; the blog builder now assigns it to pilots. Undo: template suffix back to `clinical-study` | EN + DE live: no duplicated or empty sections                                             |
| 2   | The Argireline hub did not link to Raikou                                                 | "…and our appraisal of the forehead-lines trial" added to the evidence section's "Read …" sentence, through `hub-i18n.py`                                                                          | Six locales live, locale-prefixed                                                         |
| 3   | Wang linked Raikou only to PubMed                                                         | Appraisal link added after the PubMed citation (`scripts/link-pilot-sibling.py`)                                                                                                                   | Six locales live                                                                          |
| 5   | No safety guidance on study articles                                                      | "Before you try it" note on every study (`configs/study-safety-note.json`; research `docs/research-2026-09-30-safety-notes-on-study-articles.md`); fish-allergy line on PDRN only                  | 4 articles × 6 locales. **Translations pending native review**                            |
| 6   | Study keywords undecided                                                                  | Researched: each article owns its own trial's question; "does X work?" goes to the hub (`docs/keyword-ownership-analysis-2026-09-30.md` §4, `keyword-strategy-2026.md` §4)                         | Badenhorst retitled "Badenhorst 2016: Can a Copper Peptide Serum Reduce Wrinkles?" (live) |

### Waiting for Malcolm

| #   | Item                                                                                                                                                                                                                                                               | Where                                                |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------- |
| 4   | **Ask Google to recrawl the four new addresses.** Search Console → URL inspection → Request indexing, for each `/blogs/clinical-studies/<handle>` (Wang, Raikou, Badenhorst, Ye). There is no API for this button, and no Search Console credential in this setup. | Manual, about 2 minutes                              |
| 7   | **Product vs hub keyword ownership** — recommendation: Argireline hub keeps "argireline", product takes "argireline serum"; Matrixyl product keeps "matrixyl 3000", hub takes the science terms; a collection owns "peptide skincare"                              | `docs/keyword-ownership-analysis-2026-09-30.md` §1–3 |
| 8   | **Product pages carry no precautions** (checked on the PDRN serum: no patch-test, irritation or fish-allergy text). The safety research found product-page precautions near-universal among premium brands and expected for EU online listings                     | Decision + wording, six languages                    |

### Proposals from the keyword research

- **Spoke article "Argireline and Matrixyl 3000 together"** — "matrixyl and argireline" has 858 searches a month (US)
  and page one is only forum threads.
- **A "Does Argireline work?" section on the Argireline hub** — 656 a month (US), page one is forums.
- **Rebuild the two pilot studies in the stock format** — the pilot template is the interim fix; the rebuild gives them
  the figures, chart and FAQ the other two have (six languages).

### Not fixed — by the loop's rules

- **Q4 ("covers the searchers' follow-up questions") in run 1** asked study pages to answer ingredient-wide questions
  the strategy gives the hub. An audit defect, fixed in the engine; Q4 was MET in run 2.
- **Q3 on Ye (contested 2–2).** The panel split, so it is not fixed on this evidence.

### Not assessed yet (engine gaps, not page faults)

Rendered checks (layout on a phone, main content prominence, accessibility), backlinks, field Core Web Vitals (too
little traffic for Chrome's data), and hreflang reciprocity across the six locales.

## Clinical studies list page, `/blogs/clinical-studies` (2026-09-30)

Keyword: "skincare clinical studies" (Malcolm). Page note with the Rule 27 checks: `2026-09-30-clinical-studies-list-optimisation.md`.

| Run            | Gates  | Score    | Confirmed failures | Report                                                 |
| -------------- | ------ | -------- | ------------------ | ------------------------------------------------------ |
| 1 (no keyword) | 5 pass | 6.65     | Q7 · R6 · V1       | `page-audit-2026-09-30-blogs-clinical-studies.md`      |
| 2              | 6 pass | **9.18** | **C3**             | `page-audit-2026-09-30-blogs-clinical-studies-run2.md` |

**Fixed between the runs, all live in six languages:**

- **Q7:** an SEO title and a meta description.
- **R6:** four payment Q&As on the FAQ, plus a footer "Payment" link, site-wide.
- **V1:** the approved "Before you try it" note on the list (Malcolm).
- **Design critic cycle 2:** the page-level fixes.

**Open:**

- **C3.** The card summaries should state each trial's size. **Malcolm said yes (2026-09-30).**
  - Raikou is **live**: "In a randomised trial of 24 women, …", in its meta description, JSON-LD and card.
  - Badenhorst already said 40 women.
  - Wang and Ye are in the d1 window's rebuild drafts (commit `edc6676`: "60 adults", "31 women") and reach the cards when
    they go live.
  - **Re-audit the list after that.** Before then, two cards still lack the size, so C3 would likely stay confirmed.
- **C11** was contested, so it is not fixed.

### 2026-09-30 (later): Wang and Ye live in the new layout; list re-audit (run 3)

| Page                            | Score    | Gates  | Confirmed failures        | Report                                                                   |
| ------------------------------- | -------- | ------ | ------------------------- | ------------------------------------------------------------------------ |
| Wang 2013 (live, six languages) | **9.82** | 6 pass | none                      | `page-audit-2026-09-30-argireline-crows-feet-trial-wang-2013-live.md`    |
| Ye 2026 (live, six languages)   | **9.64** | 6 pass | none (Q3 contested)       | `page-audit-2026-09-30-pdrn-vs-retinol-split-face-trial-ye-2026-live.md` |
| Clinical studies list, run 3    | **9.37** | 6 pass | **R6** (C3 now contested) | `page-audit-2026-09-30-blogs-clinical-studies-run3.md`                   |

Wang and Ye meet ADR-2026-09-30-Q. C3 cleared once all four cards carried the trial size: it is contested, not confirmed.

**R6 oscillates, and is handed to Malcolm under the loop's guard.**

- The fix is in place:
  - four payment Q&As on /pages/faq;
  - a "Payment → /pages/faq" footer link in six languages. The engine's link list does include it (checked in the run-3 JSON).
- The same page passed R6 in run 2 (2 met / 1 unmet) and failed in run 3 (1 met / 2 unmet). Nothing changed in between.
- The judges do not open the linked page. A "Payment" link that lands on the general FAQ reads to them as the FAQ.
- **The honest improvement is a link straight to the payment answers**, e.g. their own FAQ group with a stable anchor, or a short payment help
  page. It needs Malcolm's go: it is a new group with a picture, or a new page.
