# Content Structure & Build Plan — Skingenetix, 2026

**Date:** 2026-09-22 · **Status:** Ready to build — one decision left in §8 (concern collections)
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
| 1 | **Retitle and re-meta the 5 research pages.** Drop *"X Research and Studies"* — a title that promises a bibliography and draws researchers. Lead with the buyer's question and the answer's substance, e.g. *"What Is PDRN? Salmon DNA Skincare and What the Studies Show"*. Handles stay | The science layer holds **56% of site impressions and 2 of 21 clicks** (0.16% CTR vs 1.93% elsewhere) |
| 1b | **Rename the blog `news` → `learn`**, title *Learn*. Zero articles, so no redirects | Decided 2026-09-22 — `docs/decision-learning-centre-2026-09-22.md` |
| 1c | **Make `/pages/the-science` the Learn front door** — index of the 5 hubs, latest articles, INCI reference; menu label *Learn*; keep the handle | It ranks for nothing today (13 impressions, p29.6) and has no citations |
| 2 | **Resolve the 4 concern-handle collisions.** `/pages/` and `/collections/` both 200, both self-canonical, near-identical titles | Live cannibalisation on `fine-lines-wrinkles`, `firming-skin-density`, `skin-repair-renewal`, `brightening-glow` |
| 3 | **Meta titles + descriptions everywhere.** ⚠️ *Corrected 2026-09-22:* they already existed on all pages and most collections; only product titles were unset (2 of 21). Rewritten to the hero map rather than created | ⚠️ `ProductInput.seo` replaces the whole object — always send title *and* description |
| 4 | **Cross-link research ↔ solution pages, in prose** | Currently zero cross-family links. Zyppy: 0–4 inbound → ~2 clicks, 40–44 → ~8. Anchor variety was the strongest effect in that study |
| 5 | **Even out hub depth** — glutathione has 1 key finding, copper peptide has 3 | |
| 6 | Fix logged defects: `/pages/skin-concerns` lists 4 of 5 concerns; `/pages/brightening-glow` has a dead CSS block; `/pages/the-science` JSON-LD has a hardcoded 2026-03-11 date | |

**Exit:** every page has a meta title and description; no duplicate-intent titles; every research page
carries ≥2 inbound in-prose links; the blog is at `/blogs/learn/`; the acetyl page CTR is measurably moving.

---

## 4. Phase 2 — turn the 5 research pages into real hubs

> **Decided 2026-09-22: the research pages stay where they are and *are* the hubs.** The blog is a
> separate layer at `/blogs/learn/`, linked to them in both directions — the structure The INKEY List
> runs on Shopify. Moving them would gain nothing measurable (URL folder is *"a very, very lightweight
> ranking factor"*) and would mean rebuilding seven custom-templated pages in six locales. Full reasoning:
> `docs/decision-learning-centre-2026-09-22.md`.

They already exist, already carry PubMed citations, and already rank. They need five things:

1. **A front-loaded definition block at the very top.** 44.2% of AI citations come from the first 30% of
   a page, and this is the one structural finding that survives controlled scrutiny. Answer
   *"what is PDRN"* in the first 40–60 words, before anything else.
2. **Links down to every spoke, across to sibling hubs, down to products below the fold.**
   ⚠️ A hub published without links retrofitted into its spokes is wasted — Hairgenetix's pillar shipped
   with 1 inbound link and sat at position 10.6 for a month.
3. **Headings that semantically match the query.** Citation rate rises 30.2% → 41.0% with heading↔query
   similarity. **Semantic match, not question syntax** — the Q&A *genre* measures −5.7%.
4. **Absorb the definitional questions as H2 sections** rather than separate articles — `what is salmon
   pdrn`, `pdrn benefits`, `what is copper peptide`, `copper peptide benefits`, what argireline does,
   what Matrixyl 3000 is. Separate articles would have split each hub's own intent.
5. **The signals pages lack.** Shopify emits Article schema for blog articles and **none for pages**;
   pages also have no author or feed. Each hub gets a visible *"Last reviewed [date] by [name]"* and
   hand-written JSON-LD (`dateModified`, `author`, `citation`) from page metafields. AI-cited content is
   on average 25.7% fresher than organic results (Ahrefs).
6. **An automatic "More on PDRN" list** driven by the article's ingredient tag — for navigation. The
   linking that counts is still in prose.

**Order: PDRN first, then copper peptide, then argireline, then matrixyl, then glutathione.**

---

## 5. Phase 3 — the spokes

**Blog: `/blogs/learn/`** — decided 2026-09-22. Every article tagged with its ingredient and linking **up
to its hub in the first 150 words** (the Hairgenetix lesson: its pillar sat at position 10.6 with one
inbound link until the spokes were retrofitted).

**15 articles, not 18.** Six topics in the earlier list asked the same question as their hub and are now
H2 sections inside it (§4 item 4). Three practical replacements come from the keyword data. Every
article answers something its hub does not: **how to use it, what to combine it with, whether it is
safe, and how it compares.** 800–1,500 words — an 800-word page gets >50% of Google's ~2,000-word
grounding budget read; a 4,000-word page gets 13%.

Volumes below are Google Ads (bucketed — direction only; see `keyword-strategy-2026.md` §1).

### PDRN — 5 articles

| Article | Target | Vol | KD |
|---|---|---|---|
| How to use a PDRN serum: order, frequency, what to expect | `how to use pdrn serum` | ~520 | 0 |
| PDRN vs retinol — and whether to use both | `pdrn vs retinol` · `can you use pdrn with retinol` | 390 · 210 | 0 |
| **Best PDRN serums, compared on concentration and evidence** | `best pdrn serum` | 1,600 | 3 |
| PDRN vs polynucleotides — the same thing? | (People Also Ask) | — | — |
| Salmon vs vegan PDRN — ⚠️ *only once our own source is confirmed* | `vegan pdrn` | 590 | — |

### Copper peptide — 4 articles

| Article | Target | Vol | KD |
|---|---|---|---|
| Copper peptides with vitamin C and retinol — what to layer, what to separate | `copper peptide with vitamin c` · `copper peptide and retinol` | 390 · 170 | 0 |
| **Best copper peptide serums, compared on concentration** | `best copper peptide serum` | 1,600 | 5 |
| Copper peptide side effects — who should be careful | `copper peptide side effects` · `is copper peptide safe` | 320 · 110 | — |
| 1% vs 2% GHK-Cu — does concentration change the result? | long-tail | — | — |

### Argireline and Matrixyl — 4 articles

| Article | Target | Vol |
|---|---|---|
| Argireline vs Botox, honestly | (People Also Ask — volume unverified) | — |
| Argireline and Matrixyl — the difference, and using them together | `argireline matrixyl` · `matrixyl vs argireline` | 720 · 110 |
| Matrixyl 3000 vs Matrixyl Synthe'6 | `matrixyl 3000 vs synthe 6` | 140 |
| **Ist Matrixyl 3000 schädlich?** — written for the German market first | `matrixyl 3000 schädlich` (DE) | 170 |

### Glutathione and cross-family — 2 articles

| Article | Target | Vol |
|---|---|---|
| Glutathione on skin — side effects and what the evidence supports | `glutathione side effects skin` | 390 |
| Peptide serum with vitamin C | `peptide serum with vitamin c` | 480 |

⚠️ **Glutathione framing: brightening, never "whitening".** The data holds `glutathione skin whitening
before and after` variants; they are excluded on both claim and framing grounds.

### Excluded on purpose

- **`best peptide serum`** — Forbes #2, Reddit #3, Ulta #5, Marie Claire #6 and YouTube #8 own it,
  matching the finding that commercial "best X" queries send **40.86%** of citations to third-party
  listicles. Getting into their lists is off-site work. `best pdrn serum` (KD 3) and
  `best copper peptide serum` (KD 5) stay, because their SERPs are not publisher-locked.
- **Every "before and after" search** — `copper peptide before and after` (880), `argireline before and
  after` (590), `matrixyl 3000 before and after` (110). Real demand, but the store's before/after images
  are **AI-generated illustrations** of published trial findings. An article ranking for "before and
  after" would present them as results — the same problem as the synthetic reviews unpublished on
  2026-09-21. Reopen only with genuine customer or clinical photography.
- **PDRN eye patches / eye cream** (1,300 / 720) — real demand, but for a format we do not sell. Recorded
  as a range signal in `keyword-strategy-2026.md` §6, not as content.

### ⚠️ The constraint on comparison articles

Lily Ray's 220-site cohort — 54% lost 30%+ of peak traffic — lists *"Best X for Y"* and *"A vs B"*
among the eight highest-risk templates **at scale**. Four of the 18 above are that shape. The test is
hers: ***"Could a competitor publish a near-identical version of this page tomorrow using the same
prompt?"***

**Ours pass only if they are grounded in things only we have:** our stated concentrations (GHK-Cu 2%,
PDRN 1%, glutathione 2% — ⚠️ *no concentration is stated for the Acetyl Hexapeptide-8 serum; the earlier "AH-8 10%" was unverified and is removed*), our full INCI lists, and the PubMed-cited trials already assembled on
the hubs. A generic "Copper Peptides vs Retinol" explainer fails the test and must not be written.

⚠️ **Corrected 2026-09-22:** this list previously included *"our own before/after photography"*. The
store's before/after images are AI-generated illustrations, not photography of results, so they are not a
differentiator and must not be presented as evidence in any article.

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

## 8. Decisions before building

1. ✅ **Blog handle — `learn`** (Malcolm, 2026-09-22). The science pages stay separate as the hubs; the
   two layers are linked as one learning centre. `docs/decision-learning-centre-2026-09-22.md`.
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
