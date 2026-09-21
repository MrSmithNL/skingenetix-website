# Research — AI search and content hubs, 2026

**Date:** 2026-09-21 · **Status:** Evidence base for `content-hub-strategy-2026.md` · **Owner:** Claude (research), Malcolm (decisions)

This is the evidence, separated from the strategy. Read it when you want to know *why* the strategy
says what it says, or when you're tempted to do something it advises against.

Everything is graded. **[CAUSAL]** = controlled or quasi-experimental. **[CORR]** = correlational.
**[OFFICIAL]** = platform documentation. **[WEAK]** = single vendor, no method, or unreplicated.
Dates matter more than usual here — a 2023 finding about GPT-3.5 is not evidence about 2026 systems.

---

## 0. The headline, stated plainly

**The 2026 evidence has turned against the GEO playbook that the industry sells.** Every properly
controlled study published this year finds that page *furniture* — schema, question headings,
structural rewriting, llms.txt — has null or negative effect once relevance is held constant. What
moves citation is *substance and rank*: topical relevance, completeness, verifiable numbers, current
dates, explicit prices and specs, and above all **where you rank in the retrieval set**.

Google now says this itself, in documentation. This is not a contrarian reading of the field; it is
the field's own best-designed studies agreeing with the platform's own guidance.

**A second, harder truth for a brand this size:** only ~2.9% of AI citations point at the brand's own
domain. The dominant citation target for commercial queries is somebody else's "best X" listicle. A
content hub is worth building, but it is not the lever that gets Skingenetix named in AI answers.

---

## 1. What the platforms actually say

**[OFFICIAL]** Google, *Optimizing for generative AI features on Google Search*
([link](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)), published
15 May 2026, last updated 10 July 2026. Verbatim:

- *"From Google Search's perspective, optimizing for generative AI search is optimizing for the search experience, and thus still SEO."*
- *"Structured data isn't required for generative AI search, and there's no special schema.org markup you need to add."*
- *"There's no requirement to break your content into tiny pieces for AI to better understand it."*
- *"You don't need to create new machine readable files, AI text files, markup, or Markdown to appear in Google Search (including its generative AI capabilities), as Google Search itself doesn't use them."*

**[OFFICIAL]** Danny Sullivan, *Search Off the Record*, 8 January 2026, on chunking content for LLMs:
*"I was talking to some engineers about that. We don't want you to do that. We really don't."* And
the line worth remembering: *"That's what's happening now. But tomorrow the systems may change."*

**One honest crack in Google's story.** Google's *AI Features* doc (updated 2025-12-10) says AI
Overviews and AI Mode *"may use different models and techniques."* US antitrust filings describe
**FastSearch**, built on **RankEmbed** signals, which *"retrieves fewer documents"* and whose
*"quality is lower than Search's fully ranked web results."* So "AI answers come from the same
systems as Search" is a simplification Google does not quite assert in writing.

**Microsoft contradicts Google.** Fabrice Canel said at SMX Munich (March 2025 — *older source*) that
schema markup helps Microsoft's LLMs, naming FAQPage, Article and HowTo. No 2026 retraction found.
Neither company has published an experiment. Treat the disagreement as unresolved.

---

## 2. The controlled evidence

### 2.1 Schema does not cause AI citations **[CAUSAL]**

**Ahrefs, 11 May 2026** ([link](https://ahrefs.com/blog/schema-ai-citations/)). Difference-in-differences:
**1,885 pages that added JSON-LD**, matched against ~4,000 controls, 30-day windows, Aug 2025–Mar 2026.

| Platform | Effect |
|---|---|
| Google AI Overviews | **−4.6%** (small but significant) |
| Google AI Mode | +2.4% (indistinguishable from zero) |
| ChatGPT | +2.2% (indistinguishable from zero) |

The same team ran the naive correlational version first on 6M URLs and found cited pages were **~3×
more likely to carry JSON-LD**. Same data, same team: strong positive correlation, null causal effect.
Their explanation — AI favours well-maintained authoritative sites, and those sites happen to run
structured data.

This is the cleanest demonstration in the field that the correlational GEO literature is confounded.
It is also credible *because it runs against the publisher's commercial interest*.

**Caveat they state:** every page already had 100+ AIO citations pre-treatment. It proves schema
doesn't *add* citations to already-visible pages; it can't speak to an invisible page.

They also tested whether engines read hidden JSON-LD: ChatGPT, Claude, Perplexity, Gemini and AI Mode
**all ignored it** and read visible HTML. (Our own AISO skill recorded this independently in March.)

### 2.2 Structural formatting is null **[CAUSAL]**

**Vishwakarma, Kumar & Jamidar (Sprinklr), SIGIR '26 — peer-reviewed.** 252,000 trials, 6 LLMs,
two-document head-to-head RAG, one factor varied per trial, **brand names anonymised**, counterbalanced
ordering, logistic mixed-effects models.

**Gatekeepers** (significant in all 6 models): topical relevance · **explicit price** · **recent
timestamp** · list position.

**Strong secondary** (5 of 6): specifications present (OR 8.63–243) · confident vs hedged language ·
evidence-backed claims · query terms present · depth of coverage · **comparisons with alternatives**.

**The null:**

| Factor | Significant in | Odds ratios across 6 models |
|---|---|---|
| Structured vs dense content | **1 of 6** | 1.68, 1.03, **0.79**, **0.90**, **0.78**, 1.25 |
| Organised vs scattered | **1 of 6** | 2.21, 3.87, 2.49, 1.19, 1.13, 1.57 |

Three of six structure coefficients are *below 1.0* — the less-structured version won. Authors:
*"formatting choices had no impact… formatting changes showed minimal return and can be deprioritized."*

**Note how commercial that gatekeeper list is.** Price, specs, dates, comparisons — these are product-page
fields, not blog-post furniture.

### 2.3 Question-phrased headings are *not* the finding **[CORR]**

**AirOps × Kevin Indig, 13 April 2026.** 16,851 queries × 3 runs, 353,799 pages, ChatGPT only. Headings
embedded (BGE-base), cosine similarity vs query:

| Heading↔query cosine similarity | Citation rate |
|---|---|
| < 0.50 | 30.2% |
| 0.80–0.89 | 34.5% |
| 0.90+ | **41.0%** |

A ~10.8pp spread. **But this is semantic match to the query, not interrogative syntax.** No 2026 study
isolates question phrasing. The "write your H2s as questions" advice is an extrapolation.

Worse — **Zhang, He & Yao (28 April 2026)**, 602 prompts / 21,143 citations, measured influence uplift
by content genre: Code +76.9% · **Numbers/statistics +61.6%** · **Definition markers +57.3%** ·
**Comparison content +55.3%** · How-to +41.2% · **Q&A format −5.7%**. Q&A formatting was the only genre
with a *negative* effect.

### 2.4 Measurement is mostly noise **[CAUSAL-adjacent, academic]**

**Schulte, Bleeker & Kaufmann, University of St. Gallen**, arXiv:2604.07585, 10 April 2026. Four engines,
four verticals, 45 days, 4,044 consecutive-day pairs, plus 3,409 same-day re-run pairs.

Day-to-day source citation overlap (Jaccard): **0.336–0.423**. Same prompt re-run within 24 hours:
**0.321–0.434** — *the same range*. So the instability is not index drift; it is the model's own sampling.

Their operational recommendation: **at least 7 runs per prompt per day** for brand visibility, **8** for
source coverage; rolling windows of 10–24 days. Verbatim: *"single observations of AI visibility are
misleading."*

**Why this matters more than any tactic in this document:** almost every GEO case study — including any
we might run — is a single-run before/after. At Jaccard ≈ 0.33, an effect must be enormous to be
distinguishable from re-running the same prompt twice.

---

## 3. What actually predicts citation

### 3.1 Retrieval rank dominates everything **[CORR, large]**

AirOps, ChatGPT citation rate by retrieval position: **rank 1 = 58.4%**, rank 2 = 54.4%, rank 3 = 35.5%,
**rank 10 = 14.2%**. A 4× spread.

On-page structural factors move citation rate by **3–11 percentage points**. Rank moves it by **44**.

**Zyppy Signal meta-analysis (Cyrus Shepard, 7 May 2026)** synthesised 54 studies/experiments/patents,
scoring 23 factors 0–10: URL accessibility **9.5**, search rank **9.4**, fan-out rank **9.3**, preview
control **9.2** … llms.txt **2.0** (lowest). The top-scoring factors are all *retrievability and rank*.

**The strategic consequence: classic SEO ranking is the primary AI-visibility lever.** There is no
separate door.

### 3.2 Shorter and focused beats comprehensive **[CORR + mechanism]**

**DEJAN (Dan Petrovic), 20 December 2025** — 7,060 queries, 883,262 snippets from Gemini's grounding API.
This is the best *mechanistic* evidence anywhere in the field:

- Google allocates a **fixed ~2,000-word grounding budget per query** (median 1,929).
- Median grounding taken per source: **377 words**.
- **An 800-word page gets >50% coverage. A 4,000-word page gets 13%.**

A February 2026 follow-up found extraction is **extractive at the individual-sentence level**, not
passage level, with non-contiguous sentences stitched by ellipsis.

AirOps corroborates from the other direction — citation rate by word count: <500 = 30.5%,
**500–999 = 34.3%**, 1,000–2,000 = 32–33%, **5,000+ = 28.6%**. And by fan-out coverage: 0% = 35.5%,
**26–50% = 38.2% (peak)**, 100% = 34.0%.

➡️ **The "ultimate guide" playbook actively hurts.** Indig's own headline: *"Shorter, Focused Content
Wins in ChatGPT."*

Readability cuts the same way: Flesch-Kincaid grade **16–17 (college) = 35.9%**, the optimum;
FK < 8 = 29.6%. Simplifying language does not help.

### 3.3 Front-loading is the one structural finding that survives **[CORR]**

Kevin Indig / Gauge, Feb 2026 — 1.2M ChatGPT responses, 30M citations: **44.2% of citations come from
the first 30% of the page.**

Caveat: no baseline published, so this is close to what mild front-loading would produce anyway. But it
is consistent with the Sprinklr finding that *position in context* dominates, and with DEJAN's
sentence-level extraction. It is the best-supported structural move available.

Our own AISO skill independently measured the same thing on hairgenetix.com: trust signals at 80% of
page HTML are stripped by Trafilatura; the same text at 70% survives intact.

### 3.4 Freshness **[CORR]**

Ahrefs, Feb–Mar 2026, **16,975,000 cited URLs** across 7 platforms: AI-cited content averages **1,064
days old** vs **1,432 days** for organic top-10 — a **25.7% freshness advantage**. (Vendor sites inflate
this to "4.3×"; 25.7% is the real number.)

But AirOps found the relationship **non-monotonic**: <30 days = 25.3%, **30–89 days = 32.8% (peak)**,
2–5 years = 27.5%, 5+ years = 27.6%. **Very new content underperforms.** Naive "publish fresh" is wrong.

⚠️ The claim that artificially refreshing publication dates lifts AI position "by as much as 95 places"
is **[WEAK]** — one practitioner, primary source unreachable, and it contradicts Google's stated red
flag on fake freshness. Do not act on it.

### 3.5 Brand mentions vs backlinks — contested, and the confound is fatal **[CORR]**

The famous Ahrefs figures (26 May 2025 — *2025 source*, 75,000 brands, Spearman): branded web mentions
**0.664** · branded anchors 0.527 · branded search volume 0.392 · Domain Rating 0.326 · referring
domains 0.295 · **backlinks 0.218**.

**But the 2026 replication does not replicate.** Semrush, 20 July 2026 — 50,000+ brands, 1,094 categories,
600,000+ citations, Jan–Jun 2026: mentions and citations showed a **slight negative correlation, −0.229**;
only 21% of most-cited domains were also the most-mentioned brand; branded search volume predicted topical
ownership in 55.7% of pairs, organic traffic **48.4% — worse than a coin flip**.

Part of this is a construct difference (Semrush measures *citation*, Ahrefs measures *mention*) — but that
difference is the story, because the slogan assumes they're the same thing.

**The confound, quantified.** Ranqo (arXiv 2606.20065, Mar–May 2026, vendor-affiliated): unbranded
visibility by brand stature — **Tier 1 global 72.9% · Tier 2 mid-market 43.6% · Tier 3 niche 11.4%**.
~30 points per rung. If stature alone moves visibility ~60 points and also drives web mentions, ρ=0.664
is exactly what you'd expect *even if mentions did nothing*.

And the one controlled study (Sprinklr) **anonymised brand names specifically to remove familiarity
effects** and still found content properties driving citation.

➡️ Treat brand-building as good business, not a proven AI-visibility lever.

### 3.6 llms.txt is inert **[CAUSAL-adjacent, multiple independent nulls]**

| Study | Scale | Finding |
|---|---|---|
| Server-log study, ~900 domains, Sep 2025–Apr 2026 | 1,227 requests | **Frontier crawlers (GPTBot, ClaudeBot, PerplexityBot, OAI-SearchBot, Google-Extended) = 0 requests, 0.0%** |
| Ahrefs, 15 June 2026 | 137,000 domains | 97% of llms.txt files got zero requests; **Slackbot fetched it more than PerplexityBot** |
| SE Ranking, Nov 2025 | ~300,000 domains | **Removing llms.txt as a model feature *improved* citation-prediction accuracy** — it was noise |
| ALLMO.ai | 94,000+ citations | present in **<0.002%** |
| Zyppy Signal, May 2026 | 54 sources | scored **2.0/10**, lowest of 23 factors |

Plus Google's flat statement in §1. **Settled. Do not invest.**

---

## 4. Where AI search actually bites — and where it doesn't

**This is the most decision-relevant section for an e-commerce store.**

**AI Overview prevalence by intent** (Ahrefs, 146,122,391 desktop SERPs, Sept 2025 data):

| Intent | AIO prevalence |
|---|---|
| **Informational** | **21.4%** |
| Commercial | **4.3%** |
| Transactional | **2.1%** |
| Navigational | 0.9% |
| Shopping category overall | 3.2% |

Corroborated from three directions: Grossman et al. (SIGIR '26) found **Amazon Retail product keywords
trigger an AIO only 17.4%** of the time — the *lowest* of nine query classes, vs 94.6% for explanatory
questions. Similarweb (June 2026): commercial/transactional queries run **0–30% zero-click** vs
**70–100% for informational**.

➡️ **The zero-click crisis is an informational-content crisis. Product and collection pages are barely
touched.** The exposed layer is precisely the blog/pillar tier a content hub adds.

**Causal confirmation of the damage, where it lands:** Wang et al., arXiv 2608.18352, 18 Aug 2026 —
**preregistered field experiment, N=1,100**. Forcing AI Mode cut external click-through **−18.8pp**;
removing AI features *raised* clicks **+8.8pp**. AI Mode also reduced trust (−0.337), usefulness,
satisfaction and sense of agency, all p<0.001.

**Beauty is the fastest-growing AI referral category.** Similarweb, 3 Sep 2026: beauty **+312.5% YoY**
(1.0M → 4.0M monthly visits); **54.7% of ChatGPT beauty answers cite retail/e-commerce sources** — the
highest commerce share of any category. Adobe: AI-sourced retail traffic converted **54% better** by
May 2026. But AI referrals remain a low single-digit share of total traffic.

---

## 5. The ceiling on a brand this size

Three convergent findings that any plan must price in:

1. **Only ~2.9% of AI citations point at the brand's own domain** (Ranqo, 149,912 citations). 75.2%
   reference competitor or peer-brand pages. **The listicle is the single most-cited format at 35.7%.**
2. **Tier-3 niche brands: 11.4% unbranded visibility** vs 72.9% for household names. 63.2% of
   brand-prompt-engine combinations **never surface at all** — "near-binary" rather than gradual.
3. **Sharma 2026:** ChatGPT recognises 99.4% of products when named but surfaces them in only **3.32%**
   of organic discovery queries. A ~30× gap between "the model knows you" and "the model volunteers you."
   No structural tactic in the reviewed literature closes it.

➡️ **The highest-leverage AI-visibility work is off-site** — third-party "best of" roundups, review
platforms, genuine community presence. That is a different programme from a content hub, and it should
not be silently folded into one.

---

## 6. Content hub architecture — what survives 2026

**Is pillar-and-cluster still right? Yes, but the payoff mechanism inverted.**

No credible 2026 source refutes it with data. The loudest "it's dead" pieces are a practitioner post
that states outright *"I can't prove this is why rankings improved"*, and an article whose key statistic
I traced to a **fabricated citation** (it attributed "86% of AI citations came from sites with 5+
interconnected pages" to a Yext study that says nothing of the kind).

HubSpot, who invented the model, updated their canonical page **17 June 2026 and kept it**.

**What changed — Floyi, *The Topical Authority Report 2026*, 2 Sept 2026** (42 topical maps, 29,319
topics, 535,239 top-20 positions, 354,955 AI citations):

| Tier | Ranked coverage of map | Cited in this % of citing AIOs |
|---|---|---|
| Tourist | <5% (**97.2% of all sites**) | 0.14% |
| Specialist | 5–25% | 4.4% |
| Authority | 25–50% | **16.5%** |
| Giant | 50%+ | 30.8% |

Verbatim: *"40.2% to 71.9% of AI citations for a query went to websites that did not rank in the top 20
for the query"*; *"26.8% to 43.7% … did not rank for that query, but did rank elsewhere in the same map."*

Ranked coverage correlates with AI citations at **0.51** (AIO). Domain Rating: **0.09**.

But **position beats coverage on queries you already own** — ranking 1–3 gives a 60.7% citation rate,
nearly 4× the Authority tier's overall 16.5%.

➡️ **Coverage's value is on *adjacent* queries you don't rank for.** That argues for a **tightly scoped**
map with high coverage, not an ever-expanding one.

**Internal linking — the only defensible evidence base is Zyppy** (23M internal links, 1,800 sites;
page restamped Feb 2026 but the dataset is 2022, and Zyppy themselves say "directionally useful", not
scientific):

- Inbound internal links: 0–4 → ~2 clicks; **40–44 → ~8 clicks (4×)**. Flattens or reverses past ~45–50.
- **53% of all URLs studied had ≤3 internal links pointing at them.**
- **Anchor variety was the strongest relationship in the whole study.**
- At least one **exact-match anchor → over 5× the traffic**.
- Empty anchor text made no measurable difference.

Zyppy does **not** cover link position, first-link priority, or orphan pages. Any article attributing
those to Zyppy is wrong. On placement, Mueller reversed Google's own earlier line in 2022 — *"I don't
think there is anything quantifiably different about internal links in different parts of the page"* —
with the real mechanism being that **boilerplate is detected and discounted as a block**. Anyone quoting
a weighting ratio is inventing it.

**Cannibalisation — Mueller, 22 Sept 2025:** *"If you have 3 different pages appearing in the same search
result, that doesn't seem problematic to me just because it's 'more than 1'… pages aren't duplicates just
because they happen to appear in the same search results page."*

The real failure signal is: *the page you want to rank has been displaced by one you don't, and
conversions follow the wrong URL.* For the /pages/ vs /collections/ case, the correct resolution is
**differentiate by intent — not canonical, not 301** — plus a decisive internal-link hierarchy.

⚠️ No 2026 study tests that specific resolution. It is reasoned practice from Mueller's position +
Ahrefs' resolution matrix + Zyppy's anchor data.

**Content velocity:** Google's helpful-content self-assessment names both failure modes explicitly,
including *"Are you adding a lot of new content … primarily because you believe it will help your search
rankings overall by somehow making your site seem 'fresh'?"* and the spam policies (updated 2026-08-28)
define **scaled content abuse** and **doorway abuse** — the latter being the direct trap for a
programmatic ingredient- or concern-page build.

**There is no dataset on optimal publishing cadence for e-commerce. Anyone quoting one is inventing it.**

**AI content is not penalised but underperforms.** Ahrefs, 27 July 2026, 1,000,000 pages: 5.3% of top-3
results are 100% AI-generated; every position 1–10 contains 8.4–11.7% pages that are ≥80% AI. Graphite
(Oct 2025, 31,493 keywords): only **7% of top-ranking articles are AI-generated**, and ChatGPT and
Perplexity each cite **82% human-written** content.

---

## 7. Shopify constraints (verified live, 21 Sept 2026)

| Constraint | Detail |
|---|---|
| URL roots | `/pages/`, `/blogs/`, `/collections/`, `/products/` immutable on Liquid |
| Article depth | Exactly two segments: `/blogs/<blog>/<article>` |
| Collections | Flat — no parent/child URLs |
| `/collections/<c>/products/<p>` | Still auto-canonicalises to `/products/<p>` |
| sitemap.xml | Uneditable |
| `seo.hidden` metafield | Products, pages and blog posts **only** — not collections, not tag archives |
| Blog handle | **Renameable — free lever.** `/blogs/learn/<article>` is achievable |
| Multiple blogs | Allowed, no documented cap = multiple hub roots |
| **Blog tag archives** | **Crawlable, indexable, self-canonical, NO noindex, and no admin control.** Only fix is conditional `<meta name="robots" content="noindex,follow">` under `{% if current_tags %}` |
| Metaobjects (`onlineStore` + `renderable`) | → `/pages/<handle>/<entry>`, sitemap-included. **The only native two-level semantic path.** Zero of six leading beauty brands sampled use it — opportunity or operational pain, no published case study either way |

**Multi-locale multiplies everything.** Six locales × N articles = **6N indexable URLs**, all in the
sitemap, all hreflang-linked. Shopify handles the technical side correctly. Thin or machine-translated
articles become 5N low-quality URLs. And Shopify Markets gives *translations of the same articles*, not
different articles per market — you cannot target locale-specific keywords with locale-specific editorial
inside one store.

---

## 8. The local evidence: what Hairgenetix learned the hard way

Read `~/Claude Code/Projects/hairgenetix/docs/content-architecture-strategy-2026-09-01.md` for the full
account. The transferable lessons:

1. **The product page beat both blog articles.** `/products/copper-peptide-hair-growth-serum` went from
   position 17.9 to **1.1** on "best copper peptides for hair growth" — 800 clicks, 109 orders, 5.73% CR
   — while two blog listicles cannibalised each other over the same term.
2. **Two listicles answering the same question are the same page to Google, however differently they are
   written.** Differentiating by format (slug, H1, angle, product count) failed completely. All six of the
   new guide's briefed target keywords never ranked; it simply colonised the control's terms, which
   collapsed from 1,504 clicks/month to 212.
3. **An orphaned page dies.** The value destruction happened when a link retrofit gave one page 4 inbound
   links and left the other with 1.
4. **Science articles are impression-rich and click-poor.** The microneedling cluster: 620,000 impressions
   at **0.59% CTR** over four months. One study article: 137,282 impressions, 82 clicks, **0.06%**. One
   commercial, human-titled article out-converted them by **~90×**.
5. **Positions 4–10 are the whole opportunity.** 2,280 queries / 141,872 impressions / **1.92% CTR** vs
   20.99% at positions 1–3. Normal is 3–8%. Getting that band to 4% is ~+2,900 clicks with **no new
   content and no new links**. The retitling programme, not the hubs, was where the click gain was expected.
6. **Depth is not the constraint.** A competitor ranks #1 for "derma stamp for hair growth" with 1,014
   words, no H2s, no H3s, no schema. Hairgenetix's 4,466-word guide ranked 11th. *"Write longer articles"*
   was explicitly deleted from the plan.
7. **Links are the binding constraint** — 62 referring domains, last of 14 competitors, field median ~600.
8. **Don't bundle changes.** August 2026 confounded three changes at once and destroyed attribution.
   Sequential, with a measure gate between.
9. **Don't localise ahead of the measurement gate.** One spoke went live in 11 locales before its English
   performance was measured; every fix now costs 11×.
10. **Verify citations by abstract content, not by the link resolving.** A school dental-screening study
    was found cited for AHK-Cu, and a laser prostate-surgery paper cited as Pickart.

**And the most honest data point:** at the last baseline, impressions were up 5.2% but clicks were **down
28%**. *Hub architecture alone did not lift traffic inside the measurement window.*

---

## 9. Claims I could not verify — do not cite these

- **"Tables increase citation probability by over 400%"** — untraceable.
- **"Numbered lists cited 2.7× more"** — untraceable.
- **"March 2026 University of Tokyo / Tsukuba study, 17.3% lift from structural formatting"** — no such
  paper exists on arXiv or either university's publication list. **Believed fabricated**, and now being
  cited as fact across multiple sites.
- **"ChatGPT and Google AI show <1% consistency on identical brand queries"** — attributed to Brand24;
  I fetched that report and the claim is not in it. Use the St. Gallen Jaccard figures instead.
- **"4.3× more cited for fresh content"** — traces to no primary study. The real figure is 25.7%.
- **"Domain Authority correlation fell to r=0.18 from r=0.43"** — single vendor, unverified.
- **"78% of commercial keywords are owned by category pages"** — unfindable, probably fabricated.
- **The +40% GEO figure** (Aggarwal et al., KDD 2024) — real, but it is a **2023 preprint on GPT-3.5**,
  measured on a bespoke "Position-Adjusted Word Count" metric for a document *already placed* in a
  five-document context, where the winning tactics were permitted to invent statistics. **No replication
  exists.** Every 2026 "+41% for statistics" claim recycles it without saying so.

**A general warning:** a large share of what ranks for these queries in 2026 is AI-generated SEO spam
carrying invented statistics with fabricated attributions. Two were caught during this research by
fetching the cited primary source and finding it said something else entirely.

---

## 10. Open gaps

- **No skincare-vertical competitor teardown.** The session's web-search budget (200 calls) was exhausted.
  Who ranks for "copper peptide serum", "matrixyl 3000", "PDRN skincare" — and what shape their content
  takes — is unresearched.
- **No keyword volume data.** See the strategy doc, §Phase 1. This is the binding blocker.
- **Perplexity has published no official source-selection statement.**
- **Whether brand-owned ingredient pages build entity associations is untested.** No study exists.
- **Whether metaobject-backed content hubs work in practice** — zero published case studies, zero adopters
  in a sample of six leading beauty brands.

---

# Addendum — three further research streams, 2026-09-21

Three deeper investigations reported after the body above was written. **They change the recommended
priority order**, so read this section before acting on §1–10.

## A1. Correction: commercial intent is no longer the safe harbour

§4 above cites AIO prevalence of 4.3% commercial / 2.1% transactional. **That is Sept 2025 data and it has
moved.**

**Semrush, 2 July 2026** — 600,000+ keywords, US desktop, Nov 2025 – Apr 2026, 10 industries, segmented by
intent and CPC tier:

- **Commercial-intent SERPs carrying AI Overviews grew 71%** in six months.
- **Transactional-intent SERPs saw a 5% *decline*.**
- Google Ads and AI Overviews now co-appear roughly **2× more often** than a year ago.

Seer's 2026 update (53 brands, **5.47M queries**, 2.43bn impressions, GSC data) puts current prevalence at
**informational 36% · commercial 8% · transactional 5%**.

➡️ **Revised read:** "best peptide serum for wrinkles" — *commercial* — is the fastest-growing AIO category
and is being absorbed. "Buy Skingenetix PDRN serum 30ml" — *transactional* — is receding. **The protected
ground is branded and transactional, not helpful comparison content.**

Seer also found that on transactional queries, not-cited organic CTR fell **4.17% → 2.15% (−48%)** across
1.73M impressions **despite only 5% AIO exposure** — so something other than AI Overviews is compressing
commercial CTR. Do not attribute commercial CTR decline to AIO; the exposure isn't there to explain it.

## A2. ⭐ The most important finding for this project

**Chu & Hou, "Incumbent Advantage: Brand Bias and Cognitive Manipulation Dynamics in LLM Recommendation
Systems," arXiv:2606.17443v2, 21 August 2026.** Academic. **Skincare is the primary test category**, chosen
precisely because consumers cannot judge quality pre-purchase. GPT-4o-mini, Claude Sonnet, Gemini 3 Flash.

1. **Conditional Monopoly.** Across **670 valid trials**, when a real brand and a fictional brand had
   *identical* specifications, the real brand was recommended **100% of the time** (Incumbent Advantage
   Index = 10.0, the theoretical maximum). Not one fictional brand was ever recommended — all three models,
   both languages, all four skincare subcategories.

2. **But the monopoly is fragile, and this is the actionable half:**

   | Unknown brand's differentiating signal | Breakthrough rate |
   |---|---|
   | None | **4.6%** |
   | Star rating (+0.075–0.1 advantage) | **64.3%** |
   | Price | **66.8%** |
   | **Reviews** | **79.7%** |

3. **Variance decomposition: product parameters 82.4% · position 6.5% · brand 1.2%.**

4. Authors, quoted: *"the barrier for new brands is not brand equity itself, but the lack of any
   distinguishing information. This overturns the common assumption that small brands cannot compete with
   large ones."*

5. ⚠️ **Ethical hazard they document explicitly:** authority-style language **including fabricated
   clinical-evidence claims** is worth +0.17 rating points — equivalent to a 15.3% price discount or 1.9×
   more reviews, at zero cost. **Naming this so it is consciously avoided.** It is also now formally
   against Google's spam policy, updated **15 May 2026** to cover *"attempting to manipulate generative AI
   responses in Google Search."*

6. **Social dilemma:** first-mover payoff **+0.802**, collapsing to **+0.007** under universal adoption
   (half-life ≈ 1.4 brands). **Non-participating brands received zero recommendations.** The advantage is
   temporary; abstaining is not neutral, it is exclusion.

➡️ **This supersedes the "hard ceiling" framing in §5.** The Ranqo 11.4%-for-Tier-3 figure measures brands
*with no distinguishing information*. The gap is information, not size — and it is closable on the product
page, not the blog.

## A3. Product pages are the dominant AI commerce surface

**Profound, 24 June 2026** — ~1M shopping product offers (30-day snapshot), ~548M offers (8-month
unsampled lookback), ~6,000 cited product URLs scraped with significance testing:

- **88.29% of all ChatGPT product offer instances derive from crawled web PDPs.** Even among merchants
  *with* feed integration, ~76% still come from crawled pages.
- **But feeds win placement:** product-feed citations appear as the **first product offer ~99.9%** of the
  time. Feed retrieval grew **4.3% (Nov 2025) → ~20% (Jun 2026)** — roughly 15× in seven months.
- Shopify storefronts dominate feed retrievals (OpenAI partnership).

**Measured PDP levers** (Profound, 200,000 commercial prompts, Dec 2025, 5 engines):

| PDP feature | Lift in top offers |
|---|---|
| "Best Price" tag | **+777%** |
| **FAQs on the PDP** | **+188%** |
| Video | **+106%** |
| Customer Q&As | **+60%** |

What ChatGPT extracts from PDPs: customer reviews and trust signals, delivery info, **online availability
status (79%)**, product-naming clarity. Decision drivers in shopper prompts: **quality/performance 24.4%**,
price only 13.2%.

**Citation share by intent** (Wix Studio AI Search Lab, 23 Mar 2026 — 75,000 AI answers, **1,056,727
citations**, ChatGPT + AI Mode + Perplexity):

| Intent | Winner | Share |
|---|---|---|
| **Commercial** ("best retinol serum") | **Listicles** | **40.86%** |
| | Category pages | 12.42% |
| | Discussions/forums | 11.44% |
| **Transactional** ("buy X") | **Product pages** | **24.88%** |
| | Category pages | 14.97% |

eCommerce industry overall: listicles 19.94%, articles 19.49%, **category pages 15.96%**. Category pages
are the most under-discussed winner in this data.

⚠️ **Note the apparent conflict with §3.5's "2.9% of citations go to brand domains."** Profound's
11.84bn-citation study finds **57% of citations are brand sites** — but that bucket **includes competitor
and peer brand sites**. In 24 of 29 industries the median customer gets more citations from *other* brands'
sites than from any other bucket. Both are true: AI cites commercial websites heavily, just not
necessarily yours.

## A4. The feed layer — the genuinely neglected 2026 lever

**Google Merchant Center Conversational Attributes**, launched GML May 2026
([docs](https://support.google.com/merchants/answer/17085370)). Six optional attributes via a supplemental
data source; they do not affect Shopping approval:

| Attribute | Content |
|---|---|
| `question_and_answer` | **Up to 30 Q&A pairs per product** |
| `document_link` | PDFs — ingredient sheets, manuals |
| `related_product` | Accessories, bundles |
| `item_group_title` | Variant family label |
| `variant_option` | Size/shade/volume axis |
| `popularity_rank` | Percentile within your own inventory |

**The hard number (Google, 16 Sep 2026): in lululemon's test, conversational attributes submitted by the
brand were incorporated 50% of the time in relevant AI Mode product recommendations.** Same post: merchants
adopting core Merchant Center feed best practices saw **+5% conversions the following month**.

Google's own AI optimisation guide draws the distinction cleanly — schema gets you rich results; **feeds get
you product visibility**: *"Using products like Merchant Center… can help your products and services to be
visible in both AI responses and other Google Search results."*

Also note: **Google removed FAQ rich results entirely on 7 May 2026.** FAQ *content* still helps on PDPs
(+188% above); FAQ *rich snippets* are gone. And **`Google-Extended` controls Gemini training/grounding
only** — Google states it *"does not impact a site's inclusion in Google Search nor is it used as a ranking
signal."* Blocking or allowing it does nothing for AI Mode visibility; **Googlebot** is what feeds AIO and
AI Mode.

⚠️ **AI performance insights in Merchant Center went broadly available 16 Sep 2026 — but only in AU, CA,
IN, NZ, US. Not the UK, not the EU.** Google agentic checkout is **US only**; UK is 2027 at the earliest
and unconfirmed.

## A5. Beauty — the category's specific shape

- **Beauty is the fastest-growing AI referral category, +312.5% YoY** — but from the smallest base,
  **2.0M average monthly visits worldwide** (Similarweb, 3 Sep 2026).
- **54.7% of sources cited in ChatGPT beauty conversations were retail and ecommerce domains** — far above
  any other category's commerce share. **In beauty, ChatGPT cites shops, not magazines.**
- **Adobe "AI Citation Readability" by retail sub-industry (May 2026):**

  | Sub-industry | Overall | Blog/News | Category | **PDP** |
  |---|---|---|---|---|
  | **Cosmetics** | **63% (1st)** | **78% (1st)** | **71% (1st)** | **51% (5th of 6)** |
  | Grocery | 48% | 62% | 58% | **70%** |

  ➡️ **Cosmetics leads on everything except product pages, where it sits 19 points behind Grocery.** The
  editorial advantage is category-wide and therefore not a differentiator; **the product page is where the
  category is collectively weak and an individual brand can still win.**

- **5WPR Beauty AI Visibility Index 2026:** Sephora-house brands = 38% of AI citations; ingredient-led
  independents = 31%; legacy mass brands = 4%. **No unaffiliated indie ranked in the top 25** — every indie
  that appeared (Glossier, Drunk Elephant, Glow Recipe, Augustinus Bader) has Sephora/Ulta distribution.
  Dual-retailer placement earns a ~1.2× citation premium. Verbatim: *"AI engines do not weight DTC-only
  signals heavily compared to retailer-distributed signals."*
  ⚠️ 5WPR's own separate report contradicts this, claiming indies outperform legacy. Flagged, not resolved.
  Their Q3 2026 index appears **modelled rather than measured** (62 prompts → "310 modeled responses") —
  do not cite its percentages; the qualitative source hierarchy is usable directionally.

## A6. Content velocity — the arithmetic

**Ahrefs, 15 May 2025** (1M random URLs; 2M URLs created Oct 2023; 1.3M US keywords):

- **Only 1.74% of newly published pages rank in the top 10 within a year** — down from 5.7% in 2017.
- **72.9% of pages in Google's top 10 are more than 3 years old** (59% in 2017).
- **The average #1 ranking page is 5 years old** (2 years in 2017).

**Lily Ray, 13 May 2026** — 220+ sites drawn from AI content platforms' own published customer-stories pages:
**54% lost 30%+ of peak organic traffic · 39% lost 50%+ · 22% lost 75%+.** Trajectory: 6–12 months of page
growth, traffic peak 3–6 months after the content peak, then steep decline. Budget roughly **a year from
launch to collapse.** Her own disclaimer: correlation, third-party estimates, selection bias (these
volunteered as vendor case studies).

**Her eight highest-risk templates at scale:** comparison pages (A vs B) · "What is X" glossary pages ·
"Best X for Y" listicles · self-promotional listicles · competitor-vs-alternatives pages · programmatic
location/language scaling · FAQ farms · off-topic content.

⚠️ **This qualifies the "comparison-first" recommendation in the strategy doc.** Comparisons measure well
(+55.3% influence, 2.4× brand mentions) *and* appear on Ray's risk list. The reconciliation is her own test:
***"Could a competitor publish a near-identical version of this page tomorrow using the same prompt?"***
A comparison grounded in our own stated concentrations, our own cited trials and our own photography
passes that test. A generic "Copper Peptides vs Retinol" explainer does not.

**Graphite (55,400 URLs from Common Crawl, three detectors, <2% false-positive validation):** ~50% of new
articles are AI-generated, but only **~14% of indexed Google results** and **~7% of top-ranking results**
are. A **7× filtering gradient** from production to top-of-SERP.

**Seer, 24 July 2026** — 7,683 pages, 47,097 citations, ChatGPT/Gemini/Perplexity, Mar–Jun 2026:
**by publish date only 42% of consistently-cited pages look fresh; by last-update date, 72% do.**
**27% of "fresh" cited pages were originally published 2+ years ago** and maintained through updates.
Verbatim: ***"The freshness LLMs reward is being manufactured by updates, not by new publishing."***
And: *"Newest gets you the spike, established plus maintained gets you the staying power."*

**Counterweight — Orbit Media, 13th annual, n=1,042, Sep 2026:** *"publish monthly or less"* is **also**
among the strategies correlating with weak performance. The top predictors are **influencer/expert
collaboration (2.6× the benchmark, practised by only 7%)**, human editors (~2×), and original research
(+50%). Only 14% of marketers report strong results — six points below a twelve-year low. Skews B2B.

➡️ **Cadence is far from the main variable, but too little is also bad.** The defensible position: a small
number of genuinely non-commodity pieces, maintained.

## A7. Google on pruning — the popular framing is wrong

Google's core-updates doc (updated 10 Dec 2025), verbatim: *"Deleting content is a last resort… **In fact,
if you're considering deleting entire sections of your site, that's likely a sign those sections were
created for search engines first, and not people. If that's the case for your site, then deleting the
unhelpful content can help the good content on your site perform better.**"*

**The operative distinction, which most pruning advice gets backwards:**
- Delete because of **why a page exists** (built to game search) — **Google endorses this.**
- Delete because of **how a page performs** (old, low-traffic, thin) — **Google has explicitly debunked
  every one of these criteria.** Sullivan, 2023: *"Are you deleting content from your site because you
  somehow believe Google doesn't like 'old' content? That's not a thing!"*

**Martin Splitt, Nov 2024, on duplicate content:** *"Some people think it influences the perceived quality
of a site but it doesn't."* One of pruning's two load-bearing justifications, denied on camera.

**Genuine consolidate-and-301 is the only pruning variant with explicit first-party Google approval**
("Move a site with URL changes", updated 20 Aug 2026). Lazy redirect-to-homepage is treated as a soft 404.

**SearchPilot has ~150 published split tests and not one is on pruning, deindexing or consolidating.**
No large-N observational study exists either.

## A8. More fabricated statistics found — blacklist

Added to §9 above. All verified by re-fetching the alleged primary source:

| Claim | Attributed to | Status |
|---|---|---|
| "76.4% of ChatGPT's most-cited pages updated within 30 days" | Ahrefs July 2025 | **CONFIRMED FABRICATION** — figure and concept absent from the study |
| "16+ posts/month = 3.5× traffic" | HubSpot | ~2015, confounded by company size, **HubSpot deleted it from their own page in 2025**; they now recommend 2–8/month |
| "Content velocity: 15%/67%/189%/340% growth by tier" | VeloSEO, Jan 2026 | Unverifiable vendor marketing — no methodology, no controls, sells a velocity tool |
| "50–80% traffic drops from scaled content abuse" | Digital Applied, Mar 2026 | **All six ranges unattributed** |
| "Pages not updated quarterly are 3× more likely to lose visibility" | mis-cited to Semrush | Actually AirOps, **no sample size**, and explicitly disputed by Gianluca Fiorelli |
| "86.5% of top-ranking pages contain AI content" | unattributed | Irreconcilable with Graphite's 7%; conflates "contains any AI text" with "is AI-generated" |
| "Bloggers who update old posts are 2.5× more likely to report strong results" | Orbit Media | **Contradicted** — not in either the 2025 or 2026 edition |
| "January 2026 core update" / "June 2026 core update" | various | **Neither exists** on Google's status dashboard |
| "13-week rule" for AI citation decay | Profound / Ray / Amsive | **Three claimed parents**, no sample size from any, and cited four months *before* Profound published it |

**A search engine's own AI summary fabricated Orbit Media statistics during this research.** Two further
claims were caught by fetching the cited primary source and finding it said something else entirely.
