# Content Structure & Build Plan — Skingenetix, 2026

**Date:** 2026-09-22 · **Status:** Ready to build, pending the two decisions in §8
**Built on:** `keyword-strategy-2026.md` (the hero map and scoring — authoritative on demand) ·
`keyword-research-2026-09-22.md` (first-pass demand) ·
`research-2026-ai-search-and-content-hubs.md` (evidence) · `content-hub-strategy-2026.md` (architecture)

This is the *what to build* document. The strategy doc says why; this says which pages, which terms,
in which order.

> **▶ Updated 2026-09-22 by `docs/keyword-strategy-2026.md`.** A full 7-market study with *observed
> clickstream* replaced the Google Ads volumes this document was first written on, and the change is not
> cosmetic: **`ghk copper peptide` reads as 135,000 in Ads and 757 in observed search — 178× inflated.**
> Copper peptide was named "the volume hub" below on the strength of that number. It is not.
> **PDRN is 68% of all qualified opportunity, 8× the next family.** The hero map in the keyword strategy
> supersedes §2 here where the two differ.

---

## 1. The governing facts

Six things decide every choice below. All measured, not assumed.

1. **PDRN is the biggest opportunity and it is not close.** On *observed* search: `pdrn` **19,734** ·
   `what is pdrn` **5,602** · `pdrn serum` **3,936** · `pdrn cream` **2,321**. Across seven markets PDRN
   is **76,717 of ~113,000 total opportunity — 68%, and 8× the next family.** The live DE SERP for
   `pdrn serum` is small affiliate blogs and marketplaces; the GB SERP is led by a Boots *collection*
   page. Genuinely winnable.
2. **Brand-owned ingredient explainers do rank.** On `what is pdrn` (US), **SkinCeuticals sits at #2**
   and **The INKEY List at #11** — doing exactly what our five research pages already do.
3. **We already have the impression-rich, click-poor problem.**
   `/pages/acetyl-hexapeptide-8-research` carries **1,014 of the site's 2,065 impressions** at position
   **8.4** and earns **1 click** — a 0.10% CTR. Fixing that page beats writing a new one.
4. **The US searches informationally; Germany searches commercially.** The entire German keyword set
   contains **two** question terms. DE volume sits on `pdrn serum`, `copper peptide serum`,
   `peptide serum`. This splits the plan cleanly by market.
5. **Competitors own branded product terms, never the category.** The Ordinary owns
   *"multi-peptide serum"*; Medicube owns *"PDRN Pink Peptide Serum"*. Nobody owns *"what is PDRN"*.
6. **⚠️ In this category, AI Overviews reach the commercial terms too.** `pdrn`, `what is pdrn`,
   `pdrn serum`, `pdrn skincare`, `argireline`, `copper peptide serum` and `matrixyl 3000` **all** carry
   an AI Overview in the US. `peptide serum` and GB `pdrn serum` do not. PDRN is a trend term and Google
   is treating it as explanatory, so the "commercial intent is safe" rule does **not** hold here.

---

## 2. The hero map — one page per keyword *and intent*

The rule that Hairgenetix proved the hard way: differentiating two pages by *format* fails; only
**intent** works. Every term below has exactly one owner.

### PDRN — the flagship hub

| Term | Vol (US/DE/NL) | KD | Owner | Intent |
|---|---|---|---|---|
| `pdrn serum` | **3,936** / 2,049 / 845 obs | 1 | **`/products/pdrn-renewal-serum`** | transactional |
| `pdrn cream` | **2,321** / 1,024 / 634 obs | 2 | **`/products/pdrn-collagen-night-cream`** | transactional |
| `pdrn skincare` | **1,817** / 1,182 obs | **0** | **`/collections/pdrn`** — Boots ranks #1 in GB with exactly this page type | commercial browse |
| **`pdrn`** | **19,734** / 6,462 / 4,650 obs | 6 | **`/pages/pdrn-research`** | **informational head** |
| **`what is pdrn`** | **5,602** / 2,285 obs | **7** | same hub page | informational |
| `pdrn meaning` | 1,665 obs · 2,116 opp | 15 | same hub page | informational |
| `salmon dna pdrn` · `salmon pdrn` | 1,368 opp | **0** | same hub page | informational |
| `pdrn benefits` · `what does pdrn do` | 1,177 opp | 9–11 | same hub page | informational |
| `best pdrn serum` | 656 obs · 1,042 opp | **3** | commercial guide spoke | commercial |
| `how to use pdrn serum` | low but KD 0 | 0 | spoke | how-to |
| `can you use pdrn with retinol` / `with vitamin c` | low but KD 0 | 0 | one layering spoke | how-to |

⚠️ **`what is pdrn in skincare` (1,425 opp) and `what does pdrn do for skin` (629) do not get their own
articles.** Same intent as the hub — separate pages would cannibalise it. They become **H2 sections
inside the PDRN hub**.

### Copper peptide — third, not second ⚠️ **corrected**

⚠️ **This family was sized on a phantom.** `ghk copper peptide` shows **135,000** in Google Ads and
**757** in observed clickstream — a **178× bucket artefact**. `copper peptide` is 33,100 Ads against
**1,362** observed. Copper peptide is the **third** family by real demand, not the first.

| Term | Observed (US/GB/DE) | Opportunity | KD | Owner |
|---|---|---|---|---|
| `copper peptide serum` | 2,977 / 1,339 / 634 | **5,496** | 3 | `/products/copper-peptide-ghk-cu-renewal-serum` |
| `copper peptide` | 1,362 / 394 / 105 | 2,204 | 9 | `/pages/copper-peptide-research` |
| `best copper peptide serum` | 403 / 78 / — | 532 | 5 | commercial guide spoke |
| ~~`ghk copper peptide`~~ | **757 observed, not 135,000** | — | 14 | not a target in its own right |

### The remaining three — sized to their demand

| Hub | Head term | Observed US/GB/DE | Opp | Owner | Investment |
|---|---|---|---|---|---|
| **Argireline / AH-8** | `argireline` | 3,734 / 1,103 / 845 | **7,149** | `/pages/acetyl-hexapeptide-8-research` | **Medium — and see §3, this page needs fixing first** |
| | `argireline serum` | 605 / — / 211 | 991 | `/products/acetyl-hexapeptide-8-anti-wrinkle-serum` | |
| **Matrixyl 3000** | `matrixyl 3000` | 2,725 / 1,339 / 211 | **5,127** | `/products/matrixyl-3000-firming-serum` — transactional, not the hub | Low–medium |
| **Glutathione** | `glutathione for skin` | 1,211 / 472 / 422 | 1,631 | `/pages/glutathione-research` | **Lowest — do not over-invest** |
| | `glutathione serum` | 555 / 236 / — | 953 | `/products/glutathione-brightening-serum` | |

### Cross-family

| Term | Observed US/GB/DE | Opp | KD | Owner |
|---|---|---|---|---|
| `peptide serum` | 3,129 / 1,418 / 1,056 | **4,016** | 0 | **`/collections/serums`** — a category SERP (Forbes #1, Amazon, Timeless), so a collection, never a single product |
| `peptide cream` | 504 / 472 / — | 627 | 4 | `/products/matrixyl-3000-pro-collagen-firming-cream` |
| `peptide skincare` | 100 / 157 / 211 | 312 | 9 | a peptide collection |

✅ **`l argireline` resolved.** It showed 74,000 in Ads and does not survive de-bucketing or clickstream
enrichment — it was the artefact it looked like. Not a target.

**A product gap the keyword data found:** ~3,100 of qualified opportunity sits on PDRN formats we do not
sell — `pdrn toner` (1,157), `pdrn essence` (1,168), `pdrn mask` (811). That is a range decision for
Malcolm, not a content one, but it is the clearest product-development signal in the data.

---

## 3. Phase 1 — fix what already earns impressions *(before writing anything new)*

This is the highest-ROI work on the site and it creates no new pages.

**The acetyl research page is the whole case.** 1,014 impressions, position 8.4, **one click**. Getting
that page from 0.10% CTR to a normal 3% would roughly **triple the site's total clicks** with no new
content and no new links.

| # | Action | Why |
|---|---|---|
| 1 | **Retitle and re-meta the 5 research pages.** Lead with the specific number or outcome, phrased as the user's question — not the ingredient's formal name | Position 4–10 CTR is where the lever is. Ours is 0.10% on the page that matters |
| 2 | **Resolve the 4 concern-handle collisions.** `/pages/` and `/collections/` both 200, both self-canonical, near-identical titles | Live cannibalisation on `fine-lines-wrinkles`, `firming-skin-density`, `skin-repair-renewal`, `brightening-glow` |
| 3 | **Meta titles + descriptions everywhere.** None exist on any page or product | ⚠️ `ProductInput.seo` replaces the whole object — always send title *and* description |
| 4 | **Cross-link research ↔ solution pages, in prose** | Currently zero cross-family links. Zyppy: 0–4 inbound → ~2 clicks, 40–44 → ~8. Anchor variety was the strongest effect in that study |
| 5 | **Even out hub depth** — glutathione has 1 key finding, copper peptide has 3 | |
| 6 | Fix logged defects: `/pages/skin-concerns` lists 4 of 5 concerns; `/pages/brightening-glow` has a dead CSS block; `/pages/the-science` JSON-LD has a hardcoded 2026-03-11 date | |

**Exit:** every page has a meta title and description; no duplicate-intent titles; every research page
carries ≥2 inbound in-prose links; the acetyl page CTR is measurably moving.

---

## 4. Phase 2 — turn the 5 research pages into real hubs

They already exist, already carry PubMed citations, and already rank. They need three things:

1. **A front-loaded definition block at the very top.** 44.2% of AI citations come from the first 30% of
   a page, and this is the one structural finding that survives controlled scrutiny. Answer
   *"what is PDRN"* in the first 40–60 words, before anything else.
2. **Links down to every spoke, across to sibling hubs, down to products below the fold.**
   ⚠️ A hub published without links retrofitted into its spokes is wasted — Hairgenetix's pillar shipped
   with 1 inbound link and sat at position 10.6 for a month.
3. **Headings that semantically match the query.** Citation rate rises 30.2% → 41.0% with heading↔query
   similarity. **Semantic match, not question syntax** — the Q&A *genre* measures −5.7%.

**Order: PDRN first, then copper peptide, then argireline, then matrixyl, then glutathione.**

---

## 5. Phase 3 — the spokes

**Blog handle: rename `news` → `learn` first.** Free while the blog has 0 articles, costly after.

**18 articles, not 100.** Every one carries a measured target term. 800–1,500 words — an 800-word page
gets >50% of Google's ~2,000-word grounding budget read; a 4,000-word page gets 13%.

### PDRN cluster — 6 articles

| Article | Target | Vol | KD |
|---|---|---|---|
| What salmon DNA actually is, and what PDRN is made from | `what is salmon pdrn` | 1,000 | 0 |
| How to use a PDRN serum: order, frequency, what to expect | `how to use pdrn serum` | ~520 | 0 |
| Layering PDRN with retinol and vitamin C | `can you use pdrn with retinol` | 350 | 0 |
| PDRN concentrations compared — what 1% means | `pdrn benefits` | 1,000 | 11 |
| **Best PDRN serums, compared on concentration and evidence** | `best pdrn serum` | 1,600 | 3 |
| PDRN vs polynucleotides — the same thing? | (from PAA) | — | — |

### Copper peptide cluster — 5 articles

| Article | Target | Vol | KD |
|---|---|---|---|
| What GHK-Cu is and what the trials actually measured | `what is copper peptide` | 1,300 | 22 |
| Copper peptide benefits, by evidence strength | `copper peptide benefits` | 1,300 | 14 |
| Copper peptides and vitamin C — can you layer them? | `copper peptide with vitamin c` | 390 | 0 |
| **Best copper peptide serums, compared on concentration** | `best copper peptide serum` | 1,600 | 5 |
| 1% vs 2% GHK-Cu — does concentration change the result? | long-tail | — | — |

### Remaining — 7 articles

Argireline (3): what it does to expression lines · argireline vs botox, honestly · argireline and
matrixyl together (`argireline matrixyl` 720).
Matrixyl (2): what Matrixyl 3000 is · **"matrixyl 3000 schädlich"** — a German safety query worth
answering directly.
Cross-family (1): peptide serum with vitamin C (480).

⚠️ **`best peptide serum` is cut from the plan.** It looked like the strongest cross-family article
(1,287 opportunity, KD 10) until the live SERP showed Forbes #2, Reddit #3, Ulta #5, Marie Claire #6 and
YouTube #8. Publishers own it, which matches the finding that commercial "best X" queries send **40.86%**
of citations to third-party listicles. **The play is to get into Forbes' and Marie Claire's lists — an
off-site job, not a content one.** `best pdrn serum` (KD 3) and `best copper peptide serum` (KD 5) stay,
because their SERPs are not publisher-locked.

### ⚠️ The constraint on comparison articles

Lily Ray's 220-site cohort — 54% lost 30%+ of peak traffic — lists *"Best X for Y"* and *"A vs B"*
among the eight highest-risk templates **at scale**. Four of the 18 above are that shape. The test is
hers: ***"Could a competitor publish a near-identical version of this page tomorrow using the same
prompt?"***

**Ours pass only if they are grounded in things only we have:** our stated concentrations (GHK-Cu 2%,
PDRN 1%, AH-8 10%, glutathione 2%), our PubMed-cited trials, and our own before/after photography. A
generic "Copper Peptides vs Retinol" explainer fails the test and must not be written.

---

## 6. Internal linking law

The whole defensible evidence base, in five rules:

1. Target **10–44 inbound internal links** per priority page. Below 5 is near-invisible; above ~45 the
   effect flattens or reverses.
2. **Maximum anchor-text variety** — the strongest single relationship in the Zyppy study.
3. **At least one exact-match anchor** to each commercial target — associated with >5× the traffic.
4. **Links in unique prose, never replicated boilerplate.** Boilerplate is detected and discounted as a
   block. A footer "Further Reading" list is worth little.
5. **Product pages are terminal** — they link to siblings and their collection, not back up to the blog.

---

## 7. Market and locale sequencing

**English first, measured, then translated — with one adjustment.**

Germany is **2–4× the Netherlands** on nearly every term and is the larger EU commercial market. But
German demand is almost entirely *commercial*, so the DE priority is **product and collection pages**,
not articles. The articles serve US/UK informational demand and, through translation, EU long-tail.

**Hard gate, unchanged:** 14 days minimum in English before translating.
⚠️ **Shipping English ahead of translation makes the five other locales worse, not neutral** — an
outdated translation is still served. Rebuilding one English section left `/de/` displaying the exact
unsupportable claim that had been removed that morning.

**Not yet pulled:** FR, ES, IT volumes. Do before translating into those three.

---

## 8. Two decisions before building

1. **Blog handle** — `learn`? `science`? `journal`? Free now, costly after the first article.
2. **Do the four thin concern collections earn their place?** With 9 products, one holds 2–3, and four
   collide with a page on the same handle. Either differentiate them by intent (§3 item 2) or retire
   them — but that is a call about the shop's navigation, not just SEO.

---

## 9. What this plan does not do

- **No cadence target.** No dataset on optimal e-commerce publishing frequency exists. 18 articles,
  published deliberately, then maintained — freshness in AI citations is manufactured by *updating*
  (72% of consistently-cited pages look fresh by update date vs 42% by publish date).
- **No llms.txt work, no schema-first push, no FAQ articles.** All measured null or negative.
- **No off-site programme.** 85% of AI brand mentions come from third parties and no unaffiliated indie
  ranked in the beauty top 25 — every one that did has Sephora/Ulta distribution. That is a separate
  decision, flagged in the strategy doc §8.
- **No ranking promise.** Only 1.74% of new pages reach the top 10 within a year, and hub architecture
  alone did not lift traffic at Hairgenetix inside its measurement window (impressions +5.2%, clicks
  −28%). The click gain there was expected from retitling — which is why Phase 1 comes first here.
