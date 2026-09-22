# Decision: one learning centre, two layers — keep the science pages and the blog separate, link them as one

**Date:** 2026-09-22 · **Status:** Decided (Malcolm approved the `learn` handle and asked for the science
question to be settled on evidence) · **Supersedes:** content-plan §8 decision 1
**Feeds:** `docs/content-plan-2026.md` §4–§5 · `docs/keyword-strategy-2026.md` §4

---

## The question

Skingenetix has a *science layer* — `/pages/the-science`, `/pages/ingredients` and five ingredient
research pages (`/pages/pdrn-research` etc.). It is about to launch a blog at `/blogs/learn/` with
practical articles. Should the two be **combined** into one section, or **kept separate**?

## Decision

**Keep the URLs separate. Run them as one system.**

| Layer | Lives at | Job | Intent it owns |
|---|---|---|---|
| **Ingredient hubs** | `/pages/<ingredient>-research` (unchanged) | The reference page for each ingredient: what it is, how it works, what the evidence shows | Definitional + evidence: `pdrn`, `what is pdrn`, `argireline`, `copper peptide` |
| **Learn articles** | `/blogs/learn/<article>` (renamed from `news`) | Practical and comparative questions the hub does not answer | How-to, layering, safety, head-to-head, "best X compared" |
| **Front door** | `/pages/the-science` → retitled and relabelled **Learn** in the menu | Index of both layers | Brand/navigation, not a search target |
| **Reference** | `/pages/ingredients` (unchanged) | Full INCI per product | Compliance/reference |

**Merge only where intent collides — per page, never per section.** That is the one kind of
consolidation the evidence supports, and it applies here to six planned articles (below).

---

## Why — the evidence

### 1. The folder does not move rankings

- Google's SEO Starter Guide: keywords in the URL path *"have hardly any effect beyond appearing in
  breadcrumbs"*; folder organisation matters mainly for crawling sites with *"more than a few thousand
  URLs"*. **[primary]** — developers.google.com/search/docs/fundamentals/seo-starter-guide
- Mueller: URL structure is *"a very, very lightweight ranking factor"*. **[reputable secondary]**
- Measured on the live SERPs for our own target terms (12 pulls): winners use every structure —
  SkinCeuticals `/pdrn.html` (#1 `what is pdrn`), Cult Beauty `/blog/what-is-pdrn/`, INKEY List
  `/pages/pdrn`, Paula's Choice `/ingredient-dictionary/`. Tally of brand/retailer results: 20 root-level,
  17 blog, 3 static page, 6 product, 2 collection. **No structure wins.** **[primary, observed]**

➡️ Moving the research pages into the blog would **gain nothing measurable**.

### 2. Moving them would cost a great deal

- Each research page is a **custom-designed page with its own theme template**
  (`page.research-copper-peptide.json` and four siblings) — FAQ, references, key-findings, before/after
  sections. Their content lives in template settings, not the page body (`body_html` is 19–2,775 chars).
  An article cannot carry that layout without being rebuilt.
- All seven are **translated into six live locales**. A move means re-translating, plus a 301 per page
  per locale, plus Google re-assessing each merged page from scratch (Mueller warns merged pages take
  time to settle). **[reputable secondary]**
- One of them — `/pages/acetyl-hexapeptide-8-research` — carries **1,014 of the site's 2,065
  impressions.** Re-assessment would put the only traction the site has at risk.

### 3. The ingredient-led brands separate the two layers and cross-link them

Observed live on 2026-09-22 from each site's sitemap and HTML **[primary]**:

| Brand | Reference layer | Editorial layer | Linked both ways? |
|---|---|---|---|
| **The INKEY List** (Shopify) | `/pages/pdrn`, `/pages/peptides` + ~16 more, FAQPage schema | `/blogs/news/` (263 posts), e.g. `pdrn-vs-retinol` | **Yes** — hub ↔ article |
| **Paula's Choice** | `/ingredient-dictionary/` (2,542 URLs) | `/expert-advice/` (254) | Yes |
| **Naturium** (Shopify) | `/pages/ingredient-library` | `/blogs/the-lab-journal/` | Yes |
| Versed (Shopify) | none | `/blogs/learn/` only | — |
| Cult Beauty | none | `/blog/` only | — |

**The INKEY List is our structure almost exactly** — Shopify, ingredient hubs as pages, practical articles
in a blog, cross-linked — and it ranks #5 for `pdrn serum` and #11 for `what is pdrn`. The brands that use
a single blog (Versed, Cult Beauty) are general-content brands, not ingredient-led ones.

### 4. What moves AI citation is on the page, not in the folder

- Ahrefs 2026 (863k keywords, 4M AI Overview URLs): only **38%** of cited pages rank in the top 10, down
  from 76% in July 2025, attributed to query fan-out — which rewards covering a *topic*, joined up by
  internal links. **[reputable secondary]**
- Google's own AI-features guidance lists *"making your content easily findable through internal
  links"*. **[primary]**
- DeltaV Digital (25,337 citations, Apr–Jul 2026): comparison pages have the highest citation rate
  (1.87), articles 1.43, how-to 1.32. No study we found classifies pages by *folder*. **[reputable
  secondary]**
- Ahrefs: AI-cited content is on average **25.7% fresher** than Google's organic results. **[reputable
  secondary]**

➡️ The levers are **internal links, comparison content and visible freshness** — all achievable
without moving anything.

### 5. Our own data says the research pages have a *title* problem, not a *location* problem

The science layer holds **56% of the site's impressions but 2 of 21 clicks** — a 0.16% CTR against
1.93% for the rest of the site. The queries it attracts are *"pubmed acetyl hexapeptide-8 topical
randomized trial wrinkles"*. The titles are *"PDRN (Sodium DNA) Research and Studies"* — a title that
promises a bibliography, so it draws researchers. Moving that page into a blog would carry the same
title and the same problem with it. **Retitling fixes it; relocating does not.**

---

## What changes

### A. Blog

- Rename handle `news` → **`learn`**, title **Learn**. Zero articles today, so no redirects needed.
- **Tag every article with its ingredient** (`pdrn`, `copper-peptide`, `argireline`, `matrixyl-3000`,
  `glutathione`). The tag drives the hub's article list.

### B. The five research pages become the hubs

1. **Retitle** from *"X Research and Studies"* to the buyer's question with the answer's substance —
   e.g. *"What Is PDRN? Salmon DNA Skincare and What the Studies Show"*. Handles stay unchanged.
2. **Absorb the six colliding article topics as H2 sections** (see D).
3. **Link down in prose** to each practical article, and add an automatic *"More on PDRN"* list driven by
   the blog tag. Prose links count; the list is navigation, not the linking strategy (boilerplate is
   discounted as a block).
4. **Add the page-type signals pages lack.** Shopify emits Article schema for blog articles but **none
   for pages**, and pages have no author or feed. So each hub gets a visible *"Last reviewed [date] by
   [name]"* line and hand-written JSON-LD with `dateModified`, `author` and `citation`, driven by page
   metafields.

### C. `/pages/the-science` becomes the front door

It currently ranks for nothing (13 impressions, position 29.6, for a misspelling of another company's
name), has 800 words and **no citations**. Make it the index of both layers: the five hubs, then the
latest articles, then the INCI reference. Menu label **Learn**. Keep the handle — it has no equity to
protect and no value to gain from renaming. Fix the hardcoded 2026-03-11 JSON-LD date while there.

### D. Six planned articles are folded into their hubs

Each duplicated the hub's own intent, so publishing it would have split the hub's signals:

| Was a planned article | Now |
|---|---|
| What salmon DNA actually is (`what is salmon pdrn`) | H2 in the PDRN hub |
| PDRN concentrations — what 1% means (`pdrn benefits`) | H2 in the PDRN hub |
| What GHK-Cu is and what the trials measured (`what is copper peptide`) | H2 in the copper hub |
| Copper peptide benefits, by evidence strength | H2 in the copper hub |
| What argireline does to expression lines | H2 in the argireline hub |
| What Matrixyl 3000 is | H2 in the Matrixyl hub |

They are replaced by practical questions the hubs do not answer — safety, layering and head-to-head
comparisons — drawn from the keyword data. The revised list is in `content-plan-2026.md` §5.

### E. "Before and after" searches are excluded

`copper peptide before and after` (880), `argireline before and after` (590) and
`matrixyl 3000 before and after` (110) are real demand. **They are not in the plan.** The before/after
images on this store are AI-generated illustrations of published trial findings
(`docs/clinical-trial-before-after-images.md`), and an article ranking for *"before and after"* would
present them as results. That is the same problem as the synthetic reviews unpublished on 2026-09-21.
Reopen only if genuine customer or clinical photography exists.

---

## How we will know if this was wrong

GSC baseline for the five research pages is captured in
`configs/keyword-data/gsc-baseline-2026-09-22.json`. Compare **8–12 weeks after** the retitles and the
first articles ship. Two failure signals:

- A learn article starts outranking its hub for the hub's head term → the intent split failed; merge.
- Hub CTR does not move after retitling → the problem was not the title; revisit placement.

---

## Evidence that did not survive checking

Found while researching this and **excluded** — recorded so they are not imported later:

| Claim in circulation | Status |
|---|---|
| "Ahrefs deleted 266 posts, traffic up 89% in 3 months" | Not on Ahrefs' site; an undated Medium self-report, about deletion not merging, pre-2025 |
| "Consolidation: up to +92% impressions / +70% clicks" | Untraceable to any source |
| "Topic clusters drive 30% more traffic / 3.2× AI citations" | Untraceable |
| "Dec 2025 Helpful Content Update: +23% / −18%" | No such Google publication exists |
| "Authority Hacker: internal linking +40%" | Untraceable |

**No controlled study tests hub-and-spoke placement for a store this size.** This decision rests on
Google's primary guidance, observed competitor structures and our own GSC data — strong, but not a
controlled test. Hence the measurement check above.
