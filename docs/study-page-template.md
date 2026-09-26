# Study-page template

**Date:** 2026-09-24 · **Rewritten:** 2026-09-26 (this file described the deleted custom-HTML build until then)
**Reference build:** `/pages/study/copper-peptide-wrinkle-trial-badenhorst-2016`
**Companion to:** `docs/science-page-template.md` (the hub template).
**Decisions:** ADR-2026-09-24-P (positive results, hubs), ADR-2026-09-26-L (study pages: appraisal kept and reframed, no null-study pages).

---

## 1. What a study page is

One page per qualifying human trial, at `/pages/study/<handle>`: a `study` metaobject rendered by
`templates/metaobject/study.json`. The page appraises one paper in plain language: what was tested, what it found, how to read the
result, and what it means for our products. It never passes the paper off as ours. The appraisal is the reason the page exists: Google's rater
guidelines rate a summary of an abstract as _Lowest_, and any competitor can generate one (`docs/research-2026-study-hubs-credibility.md`).

## 2. How it got here

| Date       | Build                                                       | Outcome                                                                                                            |
| ---------- | ----------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| 2026-09-22 | Pilot: four centred rich-text sections                      | Wang 2013 and Ye 2026 published in six languages; read as documents, not designed pages                            |
| 2026-09-24 | ~18,000 characters of custom HTML in one field, seven bands | 100/100 on every internal axis. Malcolm: "its terrible!" It had no header banner and fought the theme's typography |
| 2026-09-24 | **11 stock Impact sections fed by metaobject fields**       | Current. Zero custom-html sections, zero custom CSS                                                                |
| 2026-09-24 | Limits band moved off black                                 | Malcolm: no black backgrounds; the three media rows are identical                                                  |
| 2026-09-26 | Limits section retitled "How to read this result"           | ADR-2026-09-26-L                                                                                                   |

The lever for the stock route: Liquid is evaluated inside section settings on a metaobject template, so a stock section can read
`{{ metaobject.<field>.value }}`. Shopify validates the reference on upload ("must end with '.value' when not using a metafield filter").

## 3. Structure — 11 stock sections

Built by `scripts/study-template-build.py`. Every section is one the hubs already use.

| #   | Section   | Stock type                   | Carries                                                        |
| --- | --------- | ---------------------------- | -------------------------------------------------------------- |
| 1   | banner    | `image-with-text-overlay`    | eyebrow, H1 and deck over the per-study banner image           |
| 2   | figures   | `impact-text`                | three key numbers, the hubs' serif stat treatment              |
| 3   | answer    | `rich-text`                  | byline, definition, the quotable answer paragraph, our verdict |
| 4   | glance    | `specification-table`        | nine rows; labels static, values per study                     |
| 5   | chart     | `rich-text` + `liquid` block | the bar chart and its `<table>` from `scripts/hub_charts.py`   |
| 6   | story     | `media-with-text`            | "What the researchers did", image left                         |
| 7   | limits    | `media-with-text`            | **"How to read this result"**, image right                     |
| 8   | context   | `media-with-text`            | "Where this trial sits in the evidence", image left            |
| 9   | faq       | `faq`                        | four fixed questions, answers per study, FAQPage schema        |
| 10  | means     | `rich-text` + two buttons    | what it means for our products                                 |
| 11  | reference | `rich-text`                  | citation, read-at-source note, JSON-LD                         |

**Static in the template, identical on every study page** (they translate once, as template resources): the nine at-a-glance labels
(Design, Participants, What was applied, Compared with, Duration, How it was measured, Concentration, Funding, Our evidence grade), every section
title, the four FAQ questions and the two button labels. This is forced as well as chosen: a metaobject definition allows 40 fields and 37 are
used.

## 4. Hard rules

- **One `<h1>`**, and it must not open with the bare ingredient term. The builder rejects that, because it cannibalises the hub. Lead with the
  question.
- **Positive framing, appraisal kept** (ADR-2026-09-26-L). The limits section is titled "How to read this result". Each point is a plain fact:
  what was compared, what the paper does not report, who funded it. Where a point has a positive side it leads with it ("reduced volume 31.6% more
  (p = 0.0044); the depth difference did not reach significance"). No "does not show" or "failed" framing.
- **No page for a null study.** Henseler 2023 was dropped from tier 1 for this reason.
- **Every figure read at source**, from the tables and methods, not the abstract. The reference section states the date and which parts were
  read. **Exception:** Robinson 2005 is built from the abstract, PubMed record and the CIR 2012 summary. Its full text is paywalled, so its key
  figures are design facts, it has no chart, and its source note says so.
- **The concentration row is mandatory**, even when the paper never gives one.
- **Every citation identifier must belong to the paper named beside it.** Enforced by the builder since 2026-09-26 (§6).
- **Prose fields are `multi_line_text_field` holding HTML, emitted with `.value`.** `| metafield_tag` wraps rich text in a div that trafilatura,
  and so AI crawlers, discards (214 words extracted with it, 941 without).
- **In-prose internal links**: a theme button is not an `<a>` an extractor keeps. Link the hub, the science hub and the product in prose.
- **SEO title ≤ 60 characters, description ≤ 160; answer paragraph 35–75 words.** Asserted before publishing.
- **Schema:** `WebPage` carrying `author`, `reviewedBy` (from the config's `reviewer` key), `lastReviewed`, with `mainEntity` → `Article` →
  `isBasedOn` → `ScholarlyArticle`. Our page is never typed `ScholarlyArticle`.
- **All six languages** before the page is linked from anywhere (standing rule). Badenhorst is still English only (open, §8).

## 5. The config — `configs/studies/<handle>.json`

Every localisable value is `{"en": "…", "de": "…", …}`. A locale is published when `h1` carries it. Keys, in page order:

| Key                                                                    | Goes to                                                                                                                             |
| ---------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `eyebrow`, `h1`, `deck`, `banner`, `banner_mobile`                     | the banner                                                                                                                          |
| `figures[3]` → `n`, `label`, `note`                                    | the key figures                                                                                                                     |
| `byline`, `definition`, `answer`, `verdict`                            | the answer section                                                                                                                  |
| `glance.rows[9]` → `v`                                                 | the at-a-glance values, in the fixed order                                                                                          |
| `measurements.chart`                                                   | `title`, `subtitle`, `unit`, `decimals`, `domain`, `ticks`, `value_width`, `series`, `rows`, `table_head`, **`caption`** (required) |
| `media` → `image`, `alt`, `body`                                       | "What the researchers did"                                                                                                          |
| `limits.items`                                                         | "How to read this result"                                                                                                           |
| `context.body`                                                         | "Where this trial sits in the evidence"                                                                                             |
| `faq.answers[4]`                                                       | the four fixed questions                                                                                                            |
| `meaning` → `heading`, `body`, `ctas[2]`                               | "What it means for our products"; the CTA hrefs become the two button URLs                                                          |
| `citation`, `source_note`, `source_url`, `read_at_source`, `scholarly` | the reference section and the JSON-LD                                                                                               |
| `seo_title`, `seo_description`                                         | SEO fields                                                                                                                          |
| `reviewer`                                                             | `reviewedBy`; set and removed by `scripts/set-reviewer.py`                                                                          |
| `checks`                                                               | strings that must survive into the published fields (the verified figures)                                                          |

## 6. Build sequence

1. Read the paper at source. Record design, n, what was applied, comparators, duration, measurement, concentration, funding, and every figure
   with its p-value.
2. Update the ingredient's claims register (`docs/claims/<ingredient>.md`) if anything differs.
3. Write the config. Paraphrase conditions and mechanisms in our own prose: the EU wording scan treats a disease name in our sentence as our
   claim, whatever the sentence reports.
4. Dry run: `python3 scripts/build-study-page.py configs/studies/<handle>.json`. This checks lengths, the H1, the answer length and the `checks`
   probes, and **resolves every PubMed / PMC / DOI link** (NCBI esummary, Crossref). It refuses if an identifier fails to resolve, names other
   authors or a year more than one off, or if the `scholarly` title is not the identifier's own title. It fails closed when a lookup fails.
5. Publish: `--apply` (English first; translations when the config carries them).
6. Verify live with **curl**, not Python: Cloudflare throttles Python's urllib. Check one H1, the sections, the table count, the JSON-LD and no
   unrendered Liquid.
7. Capture 1440 and 390, tile to `~/Desktop/skingenetix-renders.png`, `open` it.
8. `python3 scripts/page-audit.py /pages/study/<handle>` (internal checklist), the `design-critic` agent on the deployed URL in a fresh context,
   then the central auditor (`seo-toolkit/scripts/audit_page.py`, quote `weighted_score`) until it clears 9.
9. Credit the reviewer: add the config to `configs/reviewers/esther-bodde.json` → `studies`.

## 7. Traps

| Trap                                                                              | What happens                                                                                                  |
| --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| Shopify prepends **several** `/* */` comments to metaobject templates             | Strip them all before parsing (`study-template-build.py` does).                                               |
| Empty sections still render their padding                                         | Remove unused sections rather than leaving them blank.                                                        |
| `media-with-text` has no section background setting                               | Shopify drops it silently; the three media rows share a ground. Accepted.                                     |
| `specification-table` value and `media-with-text` content validate top-level tags | Wrap the Liquid in a literal `<p>` (`rtp()`); never the `metafield_tag` filter.                               |
| `custom-html`'s `html` setting refuses Liquid                                     | The chart is a `liquid` block in a stock `rich-text` section instead.                                         |
| The theme's faq section ships support copy                                        | "Our customer support is available Monday to Friday" leaked onto a research page; the settings are blanked.   |
| **Clearing a field drops its translations**                                       | Read and re-register translations before clearing a source, or rebuild them from the config.                  |
| **A citation can point at the wrong paper**                                       | "Pickart et al., 2015" went live linked to a dental paper (PMID 26236125). The builder now refuses this (§6). |
| Heavy storefront fetching earns HTTP 429                                          | One verification at a time, with pauses; curl, not Python.                                                    |

## 8. Status (2026-09-26)

| Page                                             | State                                                                                                                                                                                                          |
| ------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Badenhorst 2016 (copper)                         | Live on the stock template, English only. Limits reframed 2026-09-26. Central audit 6.33 before the internal-link and citation fixes; not re-scored (the central auditor is being rebuilt, seo-toolkit F-012). |
| Wang 2013 (Argireline)                           | Live in six languages on pilot content (the `sections_html` fallback block); no figures, chart or glance. Carries the Henseler null sentence. To be rebuilt on the template (ADR-2026-09-26-L).                |
| Ye 2026 (PDRN)                                   | Live in six languages on pilot content; to be rebuilt on the template.                                                                                                                                         |
| Raikou 2017 (Argireline)                         | Next. Full PDF read; register §6 re-checked 2026-09-24.                                                                                                                                                        |
| Robinson 2005 (Matrixyl)                         | Planned, from the abstract (ADR-2026-09-26-L decision 3).                                                                                                                                                      |
| Evidence Library index `/pages/evidence-library` | Not built (404).                                                                                                                                                                                               |

## 9. The files

| File                              | Role                                                                                                                                  |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `scripts/study-template-build.py` | Builds and uploads `templates/metaobject/study.json` (11 stock sections). Dry run by default; `--apply` backs up the live file first. |
| `scripts/build-study-page.py`     | Checks (including citation identity), publishes and verifies one study from its config.                                               |
| `configs/studies/<handle>.json`   | One study (§5).                                                                                                                       |
| `scripts/hub_charts.py`           | The chart renderer, shared with the hubs.                                                                                             |
| `scripts/set-reviewer.py`         | Adds or removes the medical-reviewer credit; reads both pilot and stock-template configs.                                             |
| `scripts/study-pages.py`          | The pilot tool. Owns the old `intro` / `key_facts` / `body` / `reference` shape; do not use it for new pages.                         |
| `tests/test_build_study_page.py`  | Offline tests for the reviewer schema and the citation check.                                                                         |

Related: `docs/study-inventory-2026-09-24.md` (which studies and why), `docs/research-2026-study-hubs-credibility.md` (the qualifying criteria).
