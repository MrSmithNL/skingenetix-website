# Study-page template

**Date:** 2026-09-24 · **Rewritten:** 2026-09-26 (this file described the deleted custom-HTML build until then)
**Reference build:** `/pages/study/copper-peptide-wrinkle-trial-badenhorst-2016`
**Companion to:** `docs/science-page-template.md` (the hub template).
**Decisions:** ADR-2026-09-24-P (positive results, hubs), ADR-2026-09-26-L (study pages: appraisal kept and reframed, no null-study pages).

---

## 1. What a study page is

One article per qualifying human trial, at **`/blogs/clinical-studies/<handle>`** (since 2026-09-29; the old `/pages/study/<handle>`
addresses 301 here). The content is a `study` metaobject; the blog article is a shell whose `study.entry` metafield points at it, and
`templates/article.clinical-study.json` renders it (`python3 scripts/study-template-build.py --article --apply`). The metaobject's own web
pages are switched off; `templates/metaobject/study.json` is kept only as the source the article template is derived from. Articles are
created by `scripts/build-clinical-studies-blog.py`. The page appraises one paper in plain language: what was tested, what it found, how to read the
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

## 3. Structure — 12 stock sections

Built by `scripts/study-template-build.py`. Every section is one the hubs already use.

| #   | Section   | Stock type                   | Carries                                                                      |
| --- | --------- | ---------------------------- | ---------------------------------------------------------------------------- |
| 1   | banner    | `image-with-text-overlay`    | eyebrow, H1 and deck over the per-study banner image                         |
| 2   | figures   | `impact-text`                | three key numbers, the hubs' serif stat treatment                            |
| 3   | answer    | `rich-text`                  | byline, definition, the quotable answer paragraph, our verdict               |
| 4   | glance    | `specification-table`        | nine rows; labels static, values per study                                   |
| 5   | chart     | `rich-text` + `liquid` block | the bar chart and its `<table>` from `scripts/hub_charts.py`                 |
| 6   | story     | `media-with-text`            | "What the researchers did", image left                                       |
| 7   | limits    | `media-with-text`            | **"How to read this result"**, image right                                   |
| 8   | context   | `media-with-text`            | "Where this trial sits in the evidence", image left                          |
| 9   | faq       | `faq`                        | four fixed questions, answers per study, FAQPage schema                      |
| 9a  | safety    | `rich-text` + `liquid` block | **"Before you try it"** note (2026-09-30), words from the theme locale files |
| 10  | means     | `rich-text` + two buttons    | what it means for our products                                               |
| 11  | reference | `rich-text`                  | citation, read-at-source note, JSON-LD                                       |

**Two pieces of section code, both forced (rung 4):** a `liquid` block in the banner sets the key-figure colour to the
study's ingredient accent, chosen from the metaobject handle (a colour setting cannot read a field, and the definition has no
free field); and section Custom CSS on the answer, means and reference sections centres a 66-character reading column and sets
the answer paragraph at 20px (17px on phones). Both added after the 2026-09-26 design critique.

**Static in the template, identical on every study page** (they translate once, as template resources): the nine at-a-glance labels
(Design, Participants, What was applied, Compared with, Duration, How it was measured, Concentration, Funding, Our evidence grade), every section
title, the four FAQ questions and the two button labels. This is forced as well as chosen: a metaobject definition allows 40 fields and 37 are
used.

**The safety note (2026-09-30, Malcolm's go; research `docs/research-2026-09-30-safety-notes-on-study-articles.md`).**
Every study article carries a "Before you try it" block right before the product buttons: use guidance only (patch test, stop if
irritated, ask a doctor if pregnant, breastfeeding or on prescription skin treatment), and on PDRN studies a fish-allergy line (PDRN is
salmon-derived). Its six-language words live in **`configs/study-safety-note.json`** and are uploaded to the theme locale files
(`skingenetix.study_safety`) with `python3 scripts/study-template-build.py --safety-locales --apply`. **Never write "safe", "proven
safe", "hypoallergenic" or "dermatologically tested"** — under EU Reg 655/2013 each is a claim that needs evidence (a test
refuses them). New studies get the note automatically; nothing to do per study.

**English-first rebuild of a live article (2026-09-30).** A live, translated article cannot be rebuilt in place: `build-study-page.py --apply` blanks
`sections_html` and rewrites every shared field. `--preview` writes the stock-format config (kept in `configs/studies/drafts/`, which the blog builder
does not read) to a second entry, `<handle>-draft`, links it through the article metafield `study.draft`, and
`templates/article.clinical-study-draft.json` (`study-template-build.py --article-draft`) renders it at `<article url>?view=clinical-study-draft`. The
live article is untouched. **Go-live:** move the draft config over the live one, add the five locales, run `build-study-page.py <config> --apply` (the
real handle, with translations), `build-clinical-studies-blog.py --apply` (the article switches to `clinical-study` and takes the new title, summary
and SEO fields), verify ×6, then delete the `-draft` entry and clear `study.draft`.

**English-first preview of a NEW study (2026-09-30).** A study with no live article has no `?view=` to borrow, and hosting it on another study's
article would audit it under that article's title and description. So `build-study-page.py configs/studies/drafts/<handle>.json --apply --preview`
writes the entry under its **own** handle (nothing references it yet) and publishes an article in a hidden, unlinked blog,
`/blogs/clinical-studies-drafts/<handle>`, on the real `clinical-study` template, with its own title, summary and SEO fields and `seo.hidden = 1`
(noindex, out of the sitemap). The route is chosen automatically: a handle already live in `clinical-studies` gets the draft-entry route above, and
the drafts-blog route refuses any handle that exists in another blog. Audit the drafts-blog URL; its canonical points at itself, so read the
uncapped score. **Go-live:** move the config to `configs/studies/<handle>.json`, add the five locales, `build-study-page.py <config> --apply`
(same entry, now with translations), add the handle's card image to `configs/banners/clinical-studies-article-cards-*.json`, then
`build-clinical-studies-blog.py --apply` creates the real article in `clinical-studies`. Verify ×6, delete the draft article from the drafts blog,
and re-audit live.

**Template words in six languages (2026-09-30).** The template's static words are translated as template resources:

- `configs/translations/article-clinical-study-template-labels-2026-09-30.json`: the nine at-a-glance labels, the FAQ title and
  questions, and the two buttons;
- `…-section-headings-2026-09-30.json`: the story, limits and context headings, with their Liquid unchanged;
- the chart heading sits in a liquid block, which cannot be translated, so `study-template-build.py` writes it as a
  `request.locale.iso_code` case.

Re-register the two plans if those English words ever change.

**Pilot template (interim).** Wang 2013 and Ye 2026 still hold pilot content in `sections_html` with every stock field empty, so they use
`templates/article.clinical-study-pilot.json` (banner, body, safety, JSON-LD; `study-template-build.py --article-pilot`). Under the
stock template they showed seven empty headings and their reference twice (central audit, 2026-09-29). `build-clinical-studies-blog.py`
assigns the pilot template to pilot configs; switch an article back to `clinical-study` once its study is rebuilt.

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
8. **Keyword first:** add the article to `configs/page-targets.json` (`"type": "study"`, its `primary` = the trial's own question,
   its `hub`), following `docs/keyword-strategy-2026.md` §4 "Clinical-study articles". The title asks the trial's question, never
   the ingredient-wide "does X work?" (that belongs to the hub). Then regenerate the audit's keyword map in seo-toolkit
   (`configs/skingenetix.config.json`, from `page-targets.json`).
9. **Audit with the central auditor, v2** (the `seo-aiso-validator` skill; never a local copy):
   `cd ~/"Claude Code/Projects/seo-toolkit" && .venv/bin/python scripts/audit_page.py "https://www.skingenetix.com/blogs/clinical-studies/<handle>" --criteria v2 --page-type evidence --keyword "<primary>" --serp --market en-US --json <out>.json --out docs/audits/page-audit-<date>-<handle>.md`.
   Read gates · score · coverage, then **CONFIRMED FAILURES** — that list is the fix list; never fix CONTESTED. Check every "missing X"
   verdict on the raw page first. Fix, re-audit. **Done = all gates pass, no confirmed failures AND a score of 9.0 or more**
   (Malcolm, 2026-09-30, ADR-2026-09-30-Q). Below 9 with nothing confirmed, keep improving the page honestly for its readers,
   re-audit, and report to Malcolm; never pad, never fabricate, never add hidden text. Several articles:
   `scripts/audit_summary.py <jsons>` shows the shared (template) causes. Budget ≈ USD 1 per audit, standing approval ≈ USD 3.
   `scripts/page-audit.py` stays for its live-browser design checks only (1440/390), and the `design-critic` agent runs in a fresh context.
10. Credit the reviewer: add the config to `configs/reviewers/esther-bodde.json` → `studies`.

## 7. Traps

| Trap                                                                              | What happens                                                                                                                                                                                                                               |
| --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Shopify prepends **several** `/* */` comments to metaobject templates             | Strip them all before parsing (`study-template-build.py` does).                                                                                                                                                                            |
| Empty sections still render their padding                                         | Remove unused sections rather than leaving them blank.                                                                                                                                                                                     |
| `media-with-text` has no section background setting                               | Shopify drops it silently; the three media rows share a ground. Accepted.                                                                                                                                                                  |
| `specification-table` value and `media-with-text` content validate top-level tags | Wrap the Liquid in a literal `<p>` (`rtp()`); never the `metafield_tag` filter.                                                                                                                                                            |
| `custom-html`'s `html` setting refuses Liquid                                     | The chart is a `liquid` block in a stock `rich-text` section instead.                                                                                                                                                                      |
| The theme's faq section ships support copy                                        | "Our customer support is available Monday to Friday" leaked onto a research page; the settings are blanked.                                                                                                                                |
| **Clearing a field drops its translations**                                       | Read and re-register translations before clearing a source, or rebuild them from the config.                                                                                                                                               |
| **A citation can point at the wrong paper**                                       | "Pickart et al., 2015" went live linked to a dental paper (PMID 26236125). The builder now refuses this (§6).                                                                                                                              |
| The figures band's wrapper also carries `.text-custom`                            | A colour override on `.shopify-section--impact-text .text-custom` turned every label and note blue. Target `.impact-text__text .text-custom` (the number only).                                                                            |
| `text_position: start` moves the column as well as the text                       | The rich-text flex container becomes `justify-start` and the column hugs the left edge. Add `.rich-text {justify-content: center;}`.                                                                                                       |
| A `liquid` block wraps its output in a bare `<div>`                               | `.prose > p` matches nothing; use `.prose div > p`. Read the emitted markup before writing a selector.                                                                                                                                     |
| Text over a busy banner                                                           | Judged legible by eye at 1440, it measured 2.60–2.70:1. Measure the 99.5th-percentile pixel under the text after the 28% overlay; fix with a scrim baked into a copy of the image (`configs/banners/study-banners-scrim-2026-09-26.json`). |
| Heavy storefront fetching earns HTTP 429                                          | One verification at a time, with pauses; curl, not Python.                                                                                                                                                                                 |

## 8. Status (2026-09-30)

| Page                        | State                                                                                                                                                                                                                                                                                                                                                                                                  |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Badenhorst 2016 (copper)    | Live, English only. Central audit v2 (2026-09-29): 9.26, one finding (title) — retitled "Badenhorst 2016: Can a Copper Peptide Serum Reduce Wrinkles?" (2026-09-30). Translations wait until the English is complete (Malcolm, 2026-09-30)                                                                                                                                                             |
| Wang 2013 (Argireline)      | Live in six languages on the **pilot template**. **Rebuilt on the stock template as an English draft (2026-09-30)**: `configs/studies/drafts/…wang-2013.json`, preview `?view=clinical-study-draft`. Audit v2 on the preview: uncapped **9.55**; the only failures (canonical gate, S1) are preview artefacts that go-live clears. Next: Malcolm's review, translation, go-live                        |
| Ye 2026 (PDRN)              | Live in six languages on the **pilot template**. **Rebuilt on the stock template as an English draft (2026-09-30)**, re-read in the full text (PMC). Preview `?view=clinical-study-draft`. Audit v2 on the preview: uncapped **9.45**; failures are preview artefacts only. Next: Malcolm's review, translation, go-live                                                                               |
| Raikou 2017 (Argireline)    | Live in English. **Audit v2 2026-09-30: 9.82, all gates, 0 confirmed failures — done** (ADR-2026-09-30-Q); the Argireline hub links to it                                                                                                                                                                                                                                                              |
| Yogya 2022 (PDRN)           | **New, English draft (2026-09-30)** on the hidden drafts blog. RF microneedling + 0.3% polynucleotide serum vs saline, split-face, 29 women; primary `pdrn microneedling`. Read in full (PMC9110589); corrected the register (elasticity gap at 2 months, not 6; outcome periorbital; PN source not stated). Next: audit, Malcolm's review                                                             |
| Tadini 2015 (Argireline)    | **New, English draft (2026-09-30).** Publicly funded (FAPESP), vehicle-controlled, 40 women. **It measured no wrinkles:** face anisotropy (a firmness signal) fell about a third vs the plain cream. Primary `acetyl hexapeptide-3` (the paper's name). Register corrected: side effects are not reported (not "none"). Next: audit, review                                                            |
| Robinson 2005 (Matrixyl)    | **New, English draft (2026-09-30).** Palmitoyl pentapeptide-4 (the original Matrixyl, not Matrixyl 3000), 93 women, 12 weeks, P&G. Full text paywalled: read from the abstract, CIR 2012/2024, Abu Samah 2011 and Aldag 2016. Lines significant at the paper's p ≤ 0.10 only; texture (wk 4) and age spots (wk 12) at p ≤ 0.05. Chart = check-ups ahead of placebo. Primary `palmitoyl pentapeptide-4` |
| Watanabe 2014 (glutathione) | **New, English draft (2026-09-30).** 2% GSSG lotion vs placebo, split-face, 30 women, 10 weeks; melanin index −10.7% vs −3.1%. Maker-run (Kyowa), graded A−. Register wording: "brighter-looking", never lighten/whiten in our prose. Primary `glutathione brighten skin`                                                                                                                              |
| Index                       | Replaced by the blog list `/blogs/clinical-studies` (2026-09-29)                                                                                                                                                                                                                                                                                                                                       |

**Design critique cycle 1 (2026-09-26, `docs/audits/2026-09-26-study-pages-design-critique.md`): FIX, Raikou 5.60, Badenhorst
5.49.** Fixed the same day and verified by computed style: both banner contrast failures (now 6.87:1 and 6.60:1), the key-figure
accent, the centred 102-character prose (now a 66ch left-aligned column, answer 20/17px), the three appraisal titles as real `<h2>`,
phone buttons 39 → 48px, the chart grey 2.56 → 3.14:1, Raikou's key-figure units and "0", Badenhorst's repeated definition, and
internal links opening new tabs. **Open, for Malcolm:** the heading scale and one spacing value on every section (T2, T3), the
rounded-card look and the FAQ card-in-card (T6), the shared microscope and AI-scientist images (T7), the middle-dot eyebrow (T11),
and whether study pages get their own art direction: the critic expects fixes alone to level off around 6.5.

## 9. The files

| File                                     | Role                                                                                                                                                                                                                             |
| ---------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `scripts/study-template-build.py`        | Builds and uploads `templates/metaobject/study.json` (11 stock sections). Dry run by default; `--apply` backs up the live file first.                                                                                            |
| `scripts/build-study-page.py`            | Checks (including citation identity), publishes and verifies one study from its config.                                                                                                                                          |
| `scripts/build-clinical-studies-blog.py` | The Clinical studies blog: the list page spec, one article shell per study config, `--cutover` (301s, metaobject web pages off). `build-study-page.py` writes the breadcrumb into `hero_text` and the blog URL into the JSON-LD. |
| `configs/studies/<handle>.json`          | One study (§5).                                                                                                                                                                                                                  |
| `scripts/hub_charts.py`                  | The chart renderer, shared with the hubs.                                                                                                                                                                                        |
| `scripts/set-reviewer.py`                | Adds or removes the medical-reviewer credit; reads both pilot and stock-template configs.                                                                                                                                        |
| `scripts/study-pages.py`                 | The pilot tool. Owns the old `intro` / `key_facts` / `body` / `reference` shape; do not use it for new pages.                                                                                                                    |
| `tests/test_build_study_page.py`         | Offline tests for the reviewer schema and the citation check.                                                                                                                                                                    |

Related: `docs/study-inventory-2026-09-24.md` (which studies and why), `docs/research-2026-study-hubs-credibility.md` (the qualifying criteria).
