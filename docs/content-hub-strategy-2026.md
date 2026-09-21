# Content & AI-Findability Strategy — Skingenetix, 2026

**Date:** 2026-09-21 · **Status:** Proposed, awaiting Malcolm's decisions (§10) · **Supersedes:**
`docs/seo-strategy.md` and `docs/content-strategy.md` (both "Draft", both factually stale)

**Evidence base:** `docs/research-2026-ai-search-and-content-hubs.md` — body **and addendum**. Every claim
below traces there. Read this doc for *what to do*; read that one for *why*, and before overriding anything.

**Goal as stated:** rank Skingenetix as high as possible for the biggest-volume keyword(s) per product,
across Google and AI search, via a content structure of research and informative articles.

> **I am recommending something different from what was asked, and the reason is in §1.** The brief assumes
> the content hub is the lever. The 2026 evidence — including an academic study that used *skincare* as its
> test category — says the lever for a brand at this stage is the **product and feed layer**, and that the
> hub is a slower second act. I've planned both, in that order. If you want the hub first regardless, say
> so and I'll resequence — it's a legitimate call, just a more expensive one.

---

## 1. Four findings that reshape the brief

### 1.1 ⭐ The barrier is missing information, not brand size

**Chu & Hou, arXiv:2606.17443v2, 21 August 2026 — and skincare is their primary test category**, chosen
precisely because consumers cannot judge quality before purchase. Three models, 670 valid trials.

When a real brand and a fictional brand carried *identical* specifications, the real brand was recommended
**100% of the time**. Not once did a fictional brand win — all three models, both languages, all four
skincare subcategories. That is the incumbent advantage, at its theoretical maximum.

**But it breaks with a single concrete signal:**

| Unknown brand's differentiating signal | Breakthrough rate |
|---|---|
| None | **4.6%** |
| Star rating (+0.075–0.1 advantage) | 64.3% |
| Price | 66.8% |
| **Reviews** | **79.7%** |

**Variance decomposition: product parameters 82.4% · position 6.5% · brand 1.2%.**

Authors, quoted: *"the barrier for new brands is not brand equity itself, but the lack of any
distinguishing information. This overturns the common assumption that small brands cannot compete with
large ones."*

➡️ **This is more hopeful and more actionable than the "small brands can't win" narrative**, and it points
at the product page and the feed — reviews, ratings, price, specs — not at articles.

⚠️ Two things to hold alongside it. The same paper found **authority-style language including fabricated
clinical claims** is worth +0.17 rating points at zero cost — we will not do that, and since 15 May 2026 it
is formally against Google's spam policy ("attempting to manipulate generative AI responses"). And the
first-mover payoff (+0.802) **collapses to +0.007 under universal adoption** — but non-participating brands
received *zero* recommendations. Abstaining is not neutral.

### 1.2 Beauty's weak spot is exactly where we can win

**Adobe AI Citation Readability by retail sub-industry (May 2026):**

| Sub-industry | Overall | Blog/News | Category | **PDP** |
|---|---|---|---|---|
| **Cosmetics** | **63% (1st)** | **78% (1st)** | **71% (1st)** | **51% (5th of 6)** |
| Grocery | 48% | 62% | 58% | **70%** |

**Cosmetics leads every surface except the product page, where it sits 19 points behind groceries.** The
editorial advantage is category-wide — every skincare brand has an ingredient blog — so it is not a
differentiator. **The product page is where the category is collectively weak.**

And in beauty specifically, **54.7% of sources cited in ChatGPT beauty conversations are retail and
e-commerce domains** — the highest commerce share of any category. **In beauty, ChatGPT cites shops, not
magazines.**

### 1.3 Correction: commercial intent is no longer the safe harbour

An earlier draft of this strategy said commercial queries were barely touched by AI Overviews (4.3%). That
was Sept 2025 data and it has moved. **Semrush, 2 July 2026, 600,000+ keywords:** commercial-intent SERPs
carrying AI Overviews **grew 71% in six months**; transactional-intent **declined 5%**.

Current prevalence (Seer, 53 brands, 5.47M queries, GSC data): **informational 36% · commercial 8% ·
transactional 5%.**

➡️ "Best peptide serum for wrinkles" is *commercial* — the fastest-growing AIO category, being absorbed.
"Buy Skingenetix PDRN serum 30ml" is *transactional* — receding. **The protected ground is branded and
transactional.** Informational content — the layer a hub adds — remains the most exposed of all at 36%.

### 1.4 Ranking is still the AI lever; the furniture is not

Citation rate by retrieval position: **rank 1 = 58.4%, rank 10 = 14.2%.** On-page structural tactics move
citation by 3–11 percentage points; rank moves it by 44. Google's May 2026 documentation:
*"optimizing for generative AI search is optimizing for the search experience, and thus still SEO."*

Every controlled 2026 study finds schema, structural rewriting, question-headings and llms.txt null or
negative. **We do not need a separate "AISO programme"** — we need to rank, and to be complete and current.

---

## 2. Where we're starting from

**Better than the docs suggest.** A 10-page, template-consistent, PubMed-cited proto-hub already exists:
5 ingredient research pages, 5 concern/solution pages, 2 hub pages (`/pages/the-science`,
`/pages/skin-concerns`), plus `/pages/ingredients`, 13 collections, 9 products + 2 stamp sets + 11 bundles,
and a working plan-file → `patch-template.py` → backup → publish pipeline.

**Five real gaps, all verified live on 2026-09-21:**

| Gap | Evidence |
|---|---|
| **Not in Google Search Console** | Service account sees only `hairgenetix.com` and `loveoverexile.com`. **Zero ranking data exists for this site** |
| **No keyword study** | None in the repo. Already a named blocker: *"Product renaming stays blocked until the SEO/GEO/AISO keyword study"* (`todo.md:1730`) |
| **4 live title collisions** | `/pages/` and `/collections/` both 200, both self-canonical, both leading with the identical phrase — *"Fine Lines and Wrinkles - Peptide Skincare Routine"* vs *"Fine Lines and Wrinkles - Products"* |
| **No meta titles/descriptions** | BUILD-005 genuinely not started. No pattern documented |
| **Zero cross-family linking** | A solution page never links to the relevant research page, or vice versa |

**⚠️ And the constraint that gates everything in §3: zero inventory, not yet selling.** Online availability
is extracted from PDPs in **79%** of cases and is a live AI-shopping gatekeeper. There are also no genuine
customer reviews — and reviews are the single strongest breakthrough signal in §1.1. **The highest-value
track cannot fully fire until there is stock to sell and customers to review it.** That is a business
sequencing question, not an SEO one, and it belongs in §10.

**Two things already fine — do not "fix" them:**

- **robots.txt blocks no AI crawlers.** Shopify default, permissive. Good as-is. (Blocking `Google-Extended`
  would be the mistake — 21 major publishers got zero Gemini citations that way. Note it controls Gemini
  training/grounding only; **Googlebot** is what feeds AI Overviews and AI Mode.)
- **`/llms.txt`, `/llms-full.txt`, `/agents.md` all return 200** — Shopify's May 2026 defaults. Frontier
  crawlers fetched llms.txt **0 times in 1,227 requests** over seven months. **Leave them. Zero investment.**

---

## 3. Track A — the product and feed layer (do this first)

This is the reordering. It is cheaper than the hub, it is where the measured effect sizes are largest, and
it is where the beauty category is collectively weakest.

### 3.1 Product page completeness

**88.29% of all ChatGPT product offers derive from crawled PDPs.** Measured levers, from 200,000 commercial
prompts across five engines:

| PDP feature | Lift in top offers | Our status |
|---|---|---|
| "Best Price" signal | **+777%** | n/a — we are not price-competing |
| **FAQs on the PDP** | **+188%** | ✅ 6 per product via `custom.faq_items` — already built |
| **Video** | **+106%** | ❌ none |
| **Customer Q&As** | **+60%** | ❌ none |

Plus what ChatGPT extracts: reviews and trust signals, delivery info, **availability (79%)**, and clear
descriptive product naming.

**What to do:** state concentrations explicitly (we have them — GHK-Cu 1–2%, Acetyl Hexapeptide-8 10%,
PDRN 1%, Glutathione 2%); full specs and volumes; visible maintained date; comparisons with alternatives;
confident rather than hedged language. **These are the gatekeepers the one properly controlled experiment
actually found** — and unusually, we can supply all of them honestly.

⚠️ **Google removed FAQ rich results entirely on 7 May 2026.** FAQ *content* still lifts PDP citation
(+188%); FAQ *rich snippets* are gone. Keep the content, expect no snippet.

### 3.2 Reviews infrastructure

**79.7% breakthrough with reviews vs 4.6% without** — the strongest single signal in the skincare study.
Reviews are also product-page *main content* by Google's own rater definition.

We already have a route: **Klaviyo Reviews is on this account** (the sister brand's app, currently
onsite-script only). This is an install, not a purchase.

⚠️ **Honesty constraint.** The existing review quotes are real customers under changed names — that was
closed as acceptable on 2026-09-10 and stays closed. But a *ratings* programme must be genuine. Given zero
inventory, there are no new customers to review. **This track is gated on selling.**

### 3.3 Merchant Center feed + conversational attributes — the neglected lever

**Google Merchant Center Conversational Attributes** (launched GML May 2026) let a brand submit **up to 30
Q&A pairs per product**, plus ingredient-sheet PDFs (`document_link`), related products, and variant axes.

**In lululemon's test, brand-submitted conversational attributes were incorporated 50% of the time in
relevant AI Mode product recommendations.** Merchants adopting core feed best practices saw **+5%
conversions the following month**.

Feed citations appear as the **first product offer ~99.9%** of the time, and feed retrieval grew from **4.3%
to ~20% in seven months**. Google's own guidance draws the line cleanly: schema gets you rich results;
**feeds get you product visibility**.

**Nobody in this category is doing this.** It is the single best-evidenced, least-contested, least-adopted
lever available — and we already have the ingredient data, the concentrations and the PubMed citations to
fill 30 Q&A pairs per SKU honestly.

⚠️ **AI performance insights in Merchant Center are AU/CA/IN/NZ/US only** — not UK, not EU. Google agentic
checkout is US-only; UK is 2027 at the earliest. We can *submit* the attributes; we cannot yet *measure*
them from a European account.

### 3.4 Schema — the minimum, correctly

Not a lever, possibly a small negative (**−4.6%** on AIO in the only controlled study). Do it for Google
rich results and correctness, once:

- **Organization** with `@id`, on one page only — not sitewide
- **Product** with **price, availability, specs** — these are AI gatekeepers *as facts*, and schema is where
  Google reads them for Shopping
- **BreadcrumbList**
- Keep the existing per-product `FAQPage`
- **Do not** build an FAQPage/HowTo push; do not add `MedicalScholarlyArticle` to self-authored summaries

⚠️ Whatever is in schema must also be **visible HTML** — Google's policy, and all five engines ignored
hidden JSON-LD.

---

## 4. Track B — the content hub

Still worth building. Slower, and secondary to Track A.

### 4.1 Hub on the ingredient, not the concern

**Five ingredient hubs.** Because: the products are ingredient-branded and those are the winnable technical
entities; concern terms are owned by publishers; **a small map is the only route to authority** (Floyi — the
Authority tier is 25–50% *ranked coverage of the map*, and below 5%, where 97.2% of sites sit, the citation
rate is 0.14%); and the proto-hub already exists on this axis.

Concern pages stay as **commercial-investigational satellites** routing to products. They are not hubs.

### 4.2 Who owns which term

The ingredient name *is* the product name, so collection, product and research page all orbit one phrase.
That is three-way cannibalisation built into the structure — and it is what destroyed pages at Hairgenetix,
where two pages answering one question collapsed a 1,504-clicks/month article to 212.

| Term shape | Owner | Why |
|---|---|---|
| `copper peptide serum` (commercial head) | **`/products/<handle>`** | Hairgenetix's product page went **17.9 → 1.1** on exactly this shape and delivered 109 orders, beating both blog articles. Price + specs are unanimous AI gatekeepers — only a PDP has them. Transactional intent is also the *receding* AIO category |
| `copper peptide serums` / browse | `/collections/<ingredient>` | Category pages take 15.96% of e-commerce AI citations — the most under-discussed winner |
| `what is GHK-Cu` (informational head) | **`/pages/<ingredient>-research`** | Exists already. Must **not** carry the commercial term in title or H1 |
| Long-tail questions, comparisons | **New blog spokes** | §4.3 |
| `peptides for fine lines` | `/pages/<concern>` | Commercial-investigational |

**Rule, non-negotiable: one hero page per keyword *and intent* pair.** Differentiating by format alone —
slug, H1, angle — **failed completely** at Hairgenetix. Intent is the only axis that works.

### 4.3 The spoke layer

**Free lever, expiring: rename the blog handle.** `news` → `learn`, giving `/blogs/learn/<article>`. The
blog is empty, so there is no migration cost. It becomes costly the moment the first article ships.

**Format priority by measured influence uplift:**

| Format | Evidence | Verdict |
|---|---|---|
| **Comparison** | +55.3% uplift; 2.4× more brand mentions; a gatekeeper in the Sprinklr experiment | **Build — with the caveat below** |
| **Numbers/statistics-led** (concentrations, trial results) | **+61.6%**, highest non-code genre | **Build** |
| Definition / explainer | +57.3%, but Aleyda Solis explicitly deprioritises *"standalone commodity definitions"* | **Put it at the top of the hub page. Not its own article** |
| **Q&A / FAQ-shaped articles** | **−5.7%**, the only negative genre; FAQ pages 4.8% citation share; FAQ+HowTo schema "roughly 10× worse" | **Do not build** |

⚠️ **The comparison caveat, and it matters.** Lily Ray's 220-site cohort — 54% lost 30%+ of peak traffic —
lists "comparison pages (A vs B)" among the eight highest-risk templates *at scale*. The reconciliation is
her own test: ***"Could a competitor publish a near-identical version of this page tomorrow using the same
prompt?"*** A comparison grounded in **our** stated concentrations, **our** cited trials and **our**
before/after photography passes. A generic "Copper Peptides vs Retinol" explainer does not — and that is
exactly what an AI-drafted comparison defaults to.

**Length: 800–1,500 words. Not 3,000.** Google allocates a fixed **~2,000-word grounding budget per query**
and takes a median of **377 words per source**. An **800-word page gets >50% coverage; a 4,000-word page
gets 13%.** Citation rate peaks at 500–999 words. A competitor outranks Hairgenetix's 4,466-word guide with
**1,014 words and no H2s**.

**Map size: 4–6 spokes per hub, 20–30 articles total.** Coverage of 26–50% of the query fan-out beats 100%
(38.2% vs 34.0%), and scaled content abuse is now formal spam policy.

### 4.4 Cadence — and the honest arithmetic

**Only 1.74% of newly published pages rank in the top 10 within a year**, down from 5.7% in 2017. **72.9%
of top-10 pages are 3+ years old.** The average #1 page is five years old. Publishing *n* posts multiplies
a 1.74% probability by *n*.

**And the finding that should govern the whole track: freshness in AI citations is manufactured by updates,
not by new publishing.** Seer, 7,683 pages / 47,097 citations: by publish date only **42%** of consistently
cited pages look fresh; by last-update date, **72%** do. **27% were originally published 2+ years ago** and
maintained. *"Newest gets you the spike, established plus maintained gets you the staying power."*

⚠️ Counterweight: Orbit Media's 13-year dataset finds *"publish monthly or less"* also correlates with weak
performance. **Too little is also bad.** The defensible position is a small number of genuinely
non-commodity pieces, maintained — not a treadmill, and not silence.

### 4.5 On-page pattern

Three things only:

1. **Front-load the substantive answer.** 44.2% of ChatGPT citations come from the first 30% of the page —
   the only structural finding that survives scrutiny. Our own AISO work measured the same on hairgenetix:
   trust signals at 80% of page HTML are stripped by Trafilatura; at 70% they survive.
2. **Match headings semantically to the query** (30.2% → 41.0%). **Semantic match, not question syntax** —
   the Q&A *genre* measures negative.
3. **Be complete and current.** Concentrations, real citations, comparisons, confident language, visible
   maintained date.

---

## 5. Implementation plan

Sequential. **Do not bundle phases** — Hairgenetix confounded three changes at once in August 2026 and
destroyed attribution for the quarter.

### Phase 0 — Instrumentation · **BLOCKING, needs Malcolm**

1. **Verify `skingenetix.com` in Google Search Console**, grant the existing service account
   (`~/.config/ga4/service-account.json`) read access. It already works for hairgenetix.com — this is an
   access grant, not a build.
2. Confirm the cross-brand rule holds: separate GSC properties, no keyword competition with Hairgenetix.
3. Port `gsc-inspect.py` and `rescue-baseline.py` from hairgenetix, retargeted.
4. Pre-change baseline snapshot.

**Exit:** GSC returns data for skingenetix.com.

### Phase 1 — Fix what is already live · *cheap, parallel to Phase 0*

Every item is a defect on a live page.

1. **Resolve the four title collisions** — differentiate by intent, **not canonical, not 301**. Collection
   gets browse framing; page gets guidance framing. Stop both leading with the identical phrase.
2. **Meta titles and descriptions** across all pages and products. ⚠️ `ProductInput.seo` **replaces the
   whole SEO object** — sending `title` alone nulls the description. Always send both.
3. **Cross-link the two families**, in prose. Zyppy: 0–4 inbound internal links → ~2 clicks, 40–44 → ~8
   (4×), flattening past ~45; **anchor variety was the strongest relationship in the study**; at least one
   exact-match anchor → 5× traffic. Not a footer block — boilerplate is discounted as a block.
4. **Even out research-page depth** — glutathione has 1 key finding against copper peptide's 3.
5. **Organization + Product schema** per §3.4. Once, then stop.
6. **Fix logged live defects:** `/pages/skin-concerns` lists 4 concerns but 5 exist; `/pages/brightening-glow`
   has a dead CSS block targeting a removed section ID; `/pages/the-science` JSON-LD has a hardcoded
   `datePublished`/`dateModified` of 2026-03-11.

**Exit:** no duplicate-intent titles, every page has meta, every research page has ≥2 inbound in-prose links.

### Phase 2 — Product and feed layer · *Track A, the highest-value work*

1. **Merchant Center conversational attributes** — up to 30 Q&A pairs per SKU, ingredient-sheet
   `document_link`, related products. Built from data we already hold honestly.
2. **PDP completeness** — concentrations, full specs, comparisons, confident language, maintained date.
3. **Video on PDPs** (+106%) — we have a large generated-imagery pipeline; video is the gap.
4. **Customer Q&As** (+60%).
5. **Reviews programme** — ⚠️ gated on having customers. See §10.

**Exit:** every SKU carries concentration, specs, FAQ, and feed conversational attributes.

### Phase 3 — Keyword study · **BLOCKED on a data source**

⚠️ **We have no keyword volume tool.** No DataForSEO credentials, no Semrush/Ahrefs API in either repo.
Hairgenetix used DataForSEO Ads volume **plus clickstream**. Malcolm must pick a source — §10.

Deliverable: a **hero map** — keyword family → intent → hero page → second slot → action. Rules carried over:

- **Every keyword must carry a skin/face qualifier.** Hairgenetix lost 57–65% of impressions to generic
  `ghk cu` terms that converted nothing. `copper peptide` alone pulls dermatology and chemistry traffic.
- **Never sum Google Ads volumes** — nine variants returning one figure is bucket-smearing. A "113,300/mo
  opportunity" at Hairgenetix was bucket repetition and wrong.
- **Gate: before creating any article, check GSC for the intended primary keyword. If an existing page
  already ranks top 10, improve that page instead.** Hairgenetix implemented this as a hard `sys.exit`;
  port it.

**Exit:** one hero page per keyword+intent, zero unassigned head terms, zero double-assignments.

### Phase 4 — Build the hub layer · *Track B*

1. **Rename the blog handle** (`news` → `learn`). Free now, costly later.
2. **Noindex blog tag archives** — `{% if current_tags %}` → `<meta name="robots" content="noindex,follow">`.
   Shopify gives no admin control and `seo.hidden` cannot reach them.
3. **Upgrade the 5 research pages into hubs** — front-loaded definition block, links down to every spoke,
   across to sibling hubs, to products below the fold.
4. **Write spokes, comparison-first**, 4–6 per hub, 800–1,500 words, English only, each passing Ray's
   near-identical-prompt test.
5. **Publish deliberately, not in a burst.**

⚠️ **Publishing a hub without simultaneously retrofitting links into its spokes wastes the hub.**
Hairgenetix's Hub B pillar shipped with **1 inbound link** and sat at position 10.6 for a month.

**Exit:** 5 hubs live with ≥8 inbound in-content links each; zero orphaned articles.

### Phase 5 — Measure, then translate · **hard gate**

**Do not localise ahead of measurement.** Hairgenetix put a spoke live in 11 locales before measuring
English; every fix since costs 11×. Here it costs 6×, with a worse trap: **an outdated translation is still
served.** Rebuilding an English section left `/de/` showing the old German heading — the exact unsupportable
claim removed that morning — flagged `outdated:true` but rendering live. **Shipping English first makes five
locales worse, not neutral.**

- **14 days minimum** in English before translation.
- Keep prose in `richtext`/`text` settings, never `custom-html` — CSS leaks to translators and `custom-html`
  sections are exposed as translatable strings.
- Key translations by **stable prefix without the `:hash` suffix** — the hash derives from the current
  English value and invalidates the moment English changes.

### Phase 6 — Off-site · *parallel track*

See §8.

---

## 6. Measurement

**Classic search:** GSC via ported Hairgenetix tooling. Track by **hub role**, not URL soup.

**The lever nobody expects to be biggest:** Hairgenetix's positions 4–10 band ran **1.92% CTR** against a
3–8% norm across 141,872 impressions. Lifting it to 4% was worth ~+2,900 clicks **with no new content and no
new links**. Check for the same pattern the moment GSC has data — it may outrank the entire hub build on ROI.

**AI visibility — this requirement is unusual, don't skip it.** The St. Gallen study found identical prompts
re-run *minutes apart* share only **32–43% of cited sources**. Standard error drops below 0.10 only at
**n = 7 runs per prompt per day**; source coverage needs **n = 8**.

➡️ **Any AI visibility measurement must run ≥7 times per prompt, or it is measuring noise.** Every GEO
vendor case study is a single-run before/after and cannot detect anything short of an enormous effect.

⚠️ **Attribution is badly broken and this will distort any read.** Only **8.8%** of AI-influenced visits
arrive through a channel analytics labels "AI"; **71% of ChatGPT visits land in GA4 as "Direct"**; Google AI
Mode and AI Overviews are **not separately attributed in GA4 at all**. Visits typically arrive **four to
seven days** after the recommendation. Consensus undercount: ~3× on referrer, ~11× on whole journey.

---

## 7. Expectations — set honestly

- **Beauty AI referral traffic is growing fastest of any category (+312.5% YoY) from the smallest base** —
  2.0M monthly visits *worldwide, across the whole category*. AI referrals remain a low single-digit
  percentage of most sites' total traffic. A well-run DTC brand's public figure: **Omnilux, 3.2% of total
  revenue from AI channels** in March 2026. That is the realistic shape of the prize.
- **Hub architecture alone did not lift traffic at Hairgenetix inside the measurement window** —
  impressions +5.2%, clicks **−28%**. The click gain was expected from retitling, not hubs.
- **Science articles are impression-rich and click-poor.** Hairgenetix's microneedling cluster: 620,000
  impressions at **0.59% CTR**. One commercial article out-converted the whole cluster by **~90×**.
- **Content takes 6–12 months.** Only 1.74% of new pages reach the top 10 within a year.

---

## 8. The off-site track

Included because the evidence demands it, not because it was asked for.

**85% of AI brand mentions come from third-party sources.** The listicle is the most-cited format for
commercial queries at **40.86%**. Reddit takes **20.4% of AIO first-citation slots** versus 1.94% for
fourteen major publishers combined. And the hardest finding for a DTC brand: **5WPR found no unaffiliated
indie in the beauty top 25** — every indie that appeared (Glossier, Drunk Elephant, Glow Recipe, Augustinus
Bader) has Sephora/Ulta distribution, and dual-retailer placement earns a ~1.2× citation premium.

The work: third-party "best peptide serum" roundup inclusion; review-platform presence; genuine community
presence; retailer distribution.

⚠️ Reddit is real but violently unstable — **up 73% then down 86% on ChatGPT inside ten months**. Not a
strategy on its own.
⚠️ **Do not pursue inauthentic brand mentions** — Google's mythbusting names this explicitly.

I am flagging this, not planning it. It needs a scope decision.

---

## 9. What not to do — explicitly

| Don't | Because |
|---|---|
| Build or optimise `llms.txt` | Frontier crawlers fetched it **0 times in 1,227 requests**; Google says it doesn't use them; scored 2.0/10, lowest of 23 factors. Shopify already serves one |
| Run a schema-first AISO push | Only controlled study: **−4.6% / +2.4% / +2.2%** |
| Write 3,000-word ultimate guides | Fixed ~2,000-word grounding budget; 800 words gets >50% coverage, 4,000 gets 13% |
| Build FAQ-format *articles* | Q&A genre **−5.7%**; FAQ pages 4.8% citation share. (FAQ content on *product pages* is different — that's +188%) |
| Scale formulaic comparison or "what is X" pages | Ray's 220-site cohort: 54% lost 30%+ of peak traffic. Eight highest-risk templates include exactly these |
| Chase publishing cadence | 1.74% of new pages rank top-10 in a year. **No dataset on optimal e-commerce cadence exists** |
| Restructure pages "for AI" | Structure significant in **1 of 6 models**, three coefficients *below 1.0*. Sullivan: *"We don't want you to do that. We really don't"* |
| Re-date pages without substantive change | Google: *"(No, it won't)"*. Raters are trained to check the Wayback Machine |
| Differentiate two pages by format | Failed completely at Hairgenetix. Intent is the only axis |
| Translate before measuring | An outdated translation is still served — English-first makes five locales *worse* |
| Rename or re-upload a live image | Translations key off the URL; Shopify suffixes on collision and serves the old file |
| Use authority-style or unsupported clinical language | Worth +0.17 rating points and explicitly against Google's spam policy since 15 May 2026. **The one tactic in the evidence base we will not use** |
| Bundle changes | August 2026 at Hairgenetix: three changes at once, attribution destroyed |
| Quote "+40% from GEO tactics" | 2023 preprint, GPT-3.5, bespoke metric, tactics allowed to invent statistics, **never replicated** |

---

## 10. Decisions needed from Malcolm

1. **GSC access** — verify `skingenetix.com`, grant the service account. *Blocking for all measurement.*
2. **Keyword data source** — we have none. DataForSEO? Google Ads Keyword Planner? Something already paid
   for? *Blocking for Phase 3.*
3. **⭐ Inventory and selling timeline.** The highest-value track (reviews, ratings, availability) is gated
   on having stock and customers. **When does the store go live?** This changes the whole sequence.
4. **Track order** — I am recommending product/feed before hub, against the brief. Confirm or override.
5. **Is the off-site track in scope?** It is where the AI-visibility evidence points, and retailer
   distribution may matter more than anything on-site.
6. **Do the thin concern collections earn their place?** With 9 products, one holds 2–3. Four collide with
   a page on the same handle.
7. **Scope check:** 5 hubs × 4–6 spokes ≈ 20–30 articles, English first, then 6 locales. Right size?
8. **Blog handle** — `learn`? `science`? Free to change now, costly after the first article.

---

## 11. Honest uncertainties

- **No competitor teardown exists.** The web-search budget was exhausted. Who ranks for "copper peptide
  serum" or "PDRN skincare" is unresearched — and it could change the hub map.
- **No volume data.** Every candidate head term is a guess until Phase 3.
- **Merchant Center AI insights are not available in the UK/EU** — we can submit conversational attributes
  but cannot yet measure their effect from a European account.
- **The /pages/ vs /collections/ resolution is reasoned practice, not measured fact.** No 2026 study tests it.
- **Chu & Hou is a single preprint**, three models, not yet peer-reviewed. It is the most directly relevant
  study in the evidence base and it should be treated as strong but unreplicated.
- **Beauty's two indie findings contradict each other** within one publisher's own work (5WPR). Unresolved.
- **Much of the 2026 literature is contaminated.** Several widely-quoted statistics were traced to
  fabricated attributions during this research — see the research doc §9 and §A8.
