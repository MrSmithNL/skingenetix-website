# Research: would a scientific-study layer raise the whole site's credibility for Google and AI search?

**Date:** 2026-09-22 · **Status:** Research complete. Recommendation awaits Malcolm's decision · **Owner:** Claude (research), Malcolm (decision)
**Question (Malcolm):** Would an in-depth study hub, plus one detailed plain-English page for each key study, make the
whole site more valuable and credible to Google (rankings, E-E-A-T, topical authority, site-level quality) and to
AI answer engines (ChatGPT, Perplexity, Google AI Overviews and AI Mode, Gemini, Claude)?
**The criterion:** credibility and depth across the whole site. Clicks and conversion per page are explicitly
**not** the test, and production cost is not a constraint.
**Revisits:** `decision-citations-study-pages-navigation-2026-09-22.md` §3, which said "not adopted".
**Builds on:** `research-2026-ai-search-and-content-hubs.md`. Its grading applies here and its §9/§A8 blacklist is
respected: none of those statistics appear below.

Grades: **[OFFICIAL]** platform documentation · **[CAUSAL]** controlled or quasi-experimental · **[CORR]**
correlational · **[LOCAL]** our own measured data (Hairgenetix or Skingenetix) · **[ANECDOTAL]** single snapshot,
single site or opinion.

---

## 1. Verdict: build a modified version

**Build an Evidence Library, plus one page for each qualifying *human* study.** Do not build one page for every
paper the site cites.

The earlier "no" was the right answer to the wrong question. It rested mainly on revenue per session and on
nine Hairgenetix articles judged after **16 days** live. Measured against credibility and AI visibility, and
rechecked against the full Hairgenetix record, the case changes:

| Question | Answer | Why |
|---|---|---|
| Does a well-made study page add credibility for Google? | **Yes, if it is analysis, not paraphrase** | Google's rater guidelines treat an expert putting research into plain language as valuable. They rate the same page *Lowest* when it is a low-effort restatement. The dividing line is the added appraisal (§2.1) |
| Does it add AI visibility? | **Modestly positive, and mostly through Google's AI features** | Hairgenetix's study articles rank on page one for evidence queries (median position 6.9, ~88,800 EN impressions in September). One is cited in the AI Overview for a head term it does not rank for. Our own GSC shows AI-style "randomized trial pubmed" queries already reaching the Argireline hub. ChatGPT, by contrast, cites institutions for health questions (§2.2) |
| Does it raise the whole site's standing? | **Plausibly, not provably** | Google confirms it uses site-wide signals and classifiers. No study isolates what a research layer does to them. The best proxy (Floyi) ties *ranked coverage of a topic map* to AI citation at 0.51, versus 0.09 for Domain Rating. That supports a tight, complete map, not volume |
| Is it scaled-content risk? | **No, if it is limited to human studies** | Topical human trials for our five ingredients are genuinely scarce: roughly 2–4 per ingredient, **~12–18 pages in total**. The "~180 URLs" figure behind the earlier "no" counted every lab paper in all six languages |
| Is it a differentiator? | **Yes, in this niche** | The INKEY List's PDRN page (ranks #5 for `pdrn serum`) cites **no** named study, only supplier data. SkinCeuticals lists studies on an index page that links out to journals. No competitor sampled publishes plain-English appraisals of *independent* trials, including the null results |

**What makes it "modified":**

1. **One page for each human clinical study or systematic review.** Lab and animal work gets a line in the library,
   not a page.
2. **Every page is an appraisal, not a summary.** It covers design quality, effect versus placebo, the concentration
   tested compared with ours, what the study does *not* show, and who paid for it.
3. **Negative and null results get pages too.** Miller 2006, for example, found blinded measurements showed no
   difference for copper peptide. Nothing signals trustworthiness more cheaply, and no competitor does it.
4. **The library page is the hub.** The ingredient hubs keep the head terms, and the study pages never target them.
5. **English first, then a gate, then human-quality translation.** Untranslated locale URLs are noindexed
   (§3.7).
6. **Measure on Hairgenetix first.** Its 19 existing EN study articles can be checked in Search Console's new
   Generative AI report today, for free. That is the fastest real evidence available (§3.8).

**What would change this verdict:** if Hairgenetix's Generative AI report shows its study articles have close to
zero AI Overview and AI Mode impressions, cut the layer back to the library page alone. If the first wave of
Skingenetix study pages starts taking head-term impressions from the hubs, merge them into the hubs.

---

## 2. The evidence, weighed on credibility and AI value

### 2.1 What Google says: summaries fail, appraisal passes

| Source | What it says | Grade |
|---|---|---|
| Google, *Optimizing for generative AI features*, updated 2026-07-10 ([link](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)) | *"Don't just recycle what others on the internet have already said, or could easily be produced by a generative AI model."* It contrasts a first-hand take with *"a summary of existing content [that] simply restates information already available elsewhere."* | [OFFICIAL] |
| Google, *Creating helpful, people-first content*, updated 2025-12-10 ([link](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)) | Self-assessment questions: *"Does the content provide original information, reporting, research, or analysis?"*, *"substantial value when compared to other pages"*, and whether it is self-evident who wrote it | [OFFICIAL] |
| Google, *Ranking systems guide*, updated 2025-12-10 ([link](https://developers.google.com/search/docs/appearance/ranking-systems-guide)) | *"Site-wide signals and classifiers are also used and contribute to our understanding of pages."* Original-content systems show *"original reporting, ahead of those who merely cite it."* | [OFFICIAL] |
| Search Quality Rater Guidelines, version **11 Sept 2025**, §4.6.5–4.6.6 ([PDF](https://guidelines.raterhub.com/searchqualityevaluatorguidelines.pdf)) | *"Paraphrasing may be valuable, for example when an expert paraphrases the contents of a government policy in easy-to-understand language."* But *Lowest* is required when *"all or almost all of the MC… is copied, paraphrased… with little to no effort, little to no originality, and little to no added value."* Also: *"Trust is the most important member of the E-E-A-T family"*. For YMYL pages, content should be *"accurate and consistent with well-established expert consensus."* | [OFFICIAL] |
| Same, §3.2, on effort | *"The automatic creation of thousands of pages by running existing freely available content through existing translation software without any oversight, manual curation, etc., would not be considered to have effort."* | [OFFICIAL]. This governs the translation policy |
| Google spam policies, updated **2026-08-28** ([link](https://developers.google.com/search/docs/essentials/spam-policies)) | Scaled content abuse: *"many pages are generated for the primary purpose of manipulating search rankings and not helping users"*, *"no matter how it's created"*. It includes *"Stitching or combining content from different web pages without adding value."* | [OFFICIAL] |
| Google structured-data policies, updated 2026-07-10 ([link](https://developers.google.com/search/docs/appearance/structured-data/sd-policies)) | *"Your structured data must be a true representation of the page content."* Use the most specific *applicable* type | [OFFICIAL]. This rules out marking our summaries as `ScholarlyArticle` (§3.4) |

➡️ **Google's documents describe the page we must build, and the page we must not.** An abstract rewritten in
friendlier words is the example Google itself gives of low value. An expert-reviewed appraisal, stating what the
study shows, how strong it is and what it does not prove, is the paraphrase-with-added-value the rater guidelines
call valuable. The concept is not the risk. **Execution quality is the whole risk.** Because site-wide classifiers
exist, weak pages would count against the good ones.

### 2.2 What AI engines cite for health and ingredient questions

| Finding | Source | Grade |
|---|---|---|
| Google AI Overviews for **German** health queries: **65.55%** of citations went to "less reliable" (non-institutional) sources. Academic journals got **0.48%**, and government plus academic sources together about **1%**. YouTube was the top domain at 4.43%. Only **36%** of cited URLs were in the organic top 10; 74% were in the top 100 | SE Ranking, 14 Jan 2026, 50,807 queries, 465,823 citations, one Berlin snapshot ([link](https://seranking.com/blog/health-ai-overviews-youtube-vs-medical-sites/)) | [CORR], single snapshot |
| **ChatGPT** health answers: *"Over 75% of the sources cited… were from established institutional sources"* (Mayo, Cleveland Clinic, NHS, PubMed, Wikipedia) | Jacques et al., arXiv 2601.17109, 23 Jan 2026. 100 HealthSearchQA questions, 615 citations, ChatGPT 5.2 Pro ([link](https://arxiv.org/abs/2601.17109)) | [CORR], small n |
| Hairgenetix: *"ChatGPT reads medical sources, not shops"*. PubMed, AAD, Reddit and FDA dominate | Hairgenetix `traffic-and-ai-visibility-analysis-2026-09-22.md` §1 | [LOCAL] |
| AI Overviews and AI Mode *"may use a 'query fan-out' technique — issuing multiple related searches across subtopics"* | Google, *AI features*, updated 2025-12-10 ([link](https://developers.google.com/search/docs/appearance/ai-features)) | [OFFICIAL] |
| 40.2–71.9% of AI citations go to sites *not* in the top 20 for that query. 26.8–43.7% go to sites that rank elsewhere *in the same topic map*. Ranked coverage correlates with AIO citation at **0.51**, Domain Rating at **0.09** | Floyi, 2 Sep 2026 (existing research doc §6) | [CORR] |
| Cited pages were **not** more original than uncited ones (median Information Gain 52 vs 55.5, p = .07). The AIO cited the most original page 33% of the time, against 50% expected by chance. Legal content was the only exception | On-Page.ai (Lancheres), 15 Jul 2026. 50 keywords, 793 citations, one day, US only ([link](https://api.on-page.ai/research/ai-citation-study)) | [CORR], small |
| **Primary** research pages are reported as ~3.3× more citation-dense than other pages | Kevin Indig, Growth Memo, 2026 (paywalled; figure seen only in secondary summaries) ([link](https://www.growth-memo.com/p/why-most-original-data-never-gets)) | [CORR], unverified at source. **It applies to primary research. A study summary is secondary.** Do not use it to justify this layer |
| Evidence-backed claims, specifications and depth of coverage are strong secondary citation drivers (5 of 6 models). Formatting is null | Sprinklr, SIGIR '26 (existing doc §2.2) | [CAUSAL] |
| Numbers/statistics content gives **+61.6%** influence uplift. Q&A format **−5.7%** | Zhang, He & Yao, Apr 2026 (existing doc §2.3) | [CORR] |
| An 800-word page gets >50% grounding coverage; a 4,000-word page gets 13% | DEJAN, Dec 2025 (existing doc §3.2) | [CORR + mechanism] |
| In skincare, LLM recommendation variance is **82.4% product parameters**. Authority-style language *including fabricated clinical evidence* buys +0.17 rating points | Chu & Hou, arXiv 2606.17443v2 (existing doc §A2) | [CAUSAL], preprint. **Evidence signals matter to AI recommenders. Only the honest version is on the table** |

➡️ **Engines split.** ChatGPT answers health questions from institutions, and a brand page will rarely displace
PubMed or Mayo there. Google's AI features cite non-institutional explainers heavily (about 65% in the German data,
with journals under 0.5%), fan out into sub-queries, and cite pages that rank anywhere in the topic's map. **The
realistic AI gain is in Google's AI Overviews and AI Mode**, at the "does X work / what did the trial find" layer.
It is not "Skingenetix becomes ChatGPT's source for GHK-Cu".

### 2.3 The local evidence, re-read without the conversion lens

**Hairgenetix: 19 EN study articles, September 2026** (from `audits/2026-09-22-page-scorecard/pages.json`) **[LOCAL]**

| Measure | Value |
|---|---|
| Impressions, 28 days | **88,771** |
| Median average position | **6.9**: page one for evidence queries |
| Clicks, September / July | 452 / 856 |
| Sessions Jun–Sep / orders | 3,188 / 11 |
| Older, established study articles | 2025 copper-microneedling study: 192–366 clicks/month since April · AHK-Cu 2007: 86–362 · GHK 2016 trial: 44–99 |
| The nine judged "failures" | **16 days old** when judged. Only 1.74% of new pages reach the top 10 within a year (Ahrefs, existing doc §A6), so 16 days measures nothing |

**AI Overviews (Hairgenetix live SERP pull, 22 Sep 2026, 28 queries)** **[LOCAL, one snapshot]**
- `/blogs/articles/minoxidil-microneedling-meta-analysis-abdi-2023` is cited in the AI Overview for
  **"microneedling and minoxidil"**, a head term where Hairgenetix has **no top-10 organic rank**. This is exactly the
  Floyi pattern: cited because it ranks elsewhere in the map.
- `/pages/scientific-research-pdrn` (a research hub, not a study page) is cited in the AIO for "pdrn hair growth".
- `copper-peptide-ahk-cu-hair-follicle-growth-study-2007` ranks #13 on "ghk-cu vs ahk-cu", where the AIO cites the
  comparison article.
- The top queries on these pages look like machine fan-out, not typed searches: *"ghk-cu hair growth human clinical
  trial pubmed"*, *"dhurat 2013 microneedling minoxidil 24 hours after procedure protocol"*, *"microneedling
  androgenetic alopecia systematic review meta-analysis 2025"*.

**Skingenetix GSC baseline (22 Jun–20 Sep 2026)** **[LOCAL]**
- Six of the site's queries are trial-shaped, all of them on the Argireline hub: *"acetyl hexapeptide-8 topical
  randomized trial wrinkles pubmed"* and variants, plus *"systematic review of the efficacy and safety of topical
  glutathione"*.
- **Typed demand for study pages is close to zero:** `copper peptide research` 20/month (US), `ghk cu studies` 20
  (DE), `matrixyl 3000 study` 10 (DE), `argireline pubmed` 10 (DE, NL).
- **Demand for "does it work" is real:** `does pdrn really work` 390, `does pdrn work` 320, `does argireline work`
  140, `does pdrn work topically` 140, `pdrn results` 90 (US). **That intent belongs to the hubs** (see
  `decision-learning-centre-2026-09-22.md`). Study pages support the hubs' answer. They do not compete for it.

➡️ **Re-read by Malcolm's criterion, the Hairgenetix record is a qualified success.** ~89,000 monthly impressions at
page-one positions for evidence queries is exactly the "visible across the topic" footprint that Floyi's data links
to AI citation. One study article earned an AIO citation on a head term. The earlier decision counted those
impressions as a problem ("~70% of lost impressions were on study articles that never earned clicks"). As
visibility, they are an asset. What they did **not** do is earn clicks or revenue, and that stays true. It simply
is not the test here.

**Honest caveats on this local evidence:** one SERP snapshot. Impressions include ordinary blue-link impressions,
not only AI-feature ones. Hairgenetix's topics (microneedling) have far more human trials than Skingenetix's
ingredients. And the Hairgenetix articles used a scholarly template with abstract-level summaries. We cannot tell
from this data whether *appraisal-grade* pages would do better or worse.

### 2.4 What competitors do (observed live 2026-09-22) **[ANECDOTAL]**

| Brand | How studies are handled | Per-study pages? |
|---|---|---|
| **The INKEY List**, `/pages/pdrn` (#5 `pdrn serum`, #11 `what is pdrn`) | ~3,500–4,000 words. **No named study**, no PubMed links. Claims ("25–35% collagen synthesis") attributed only to *"clinical studies completed using 2% INJIN PDRN"* by the supplier. Byline: a "Digital Skincare Advisor" | No |
| **SkinCeuticals**, clinical-studies index ([link](https://www.lorealdermatologicalbeauty.us/skinceuticals/science/clinical-studies)) | One index page by category. Each entry has year, product, title, journal, a short blurb, and an outbound link to the journal or a PDF. These are **their own sponsored** studies | No, it links out |
| **Paula's Choice**, ingredient dictionary | Research-rated ingredient entries with references | No |
| Brand blogs ranking for "argireline clinical study results" (Depology, Curology) and "does PDRN work" (Chemist Confessions) | Multi-study explainers: "what the trials found", "hype vs reality" | No: one article per ingredient |
| Live results for **"argireline clinical study results"** | PubMed (Wang 2013), ResearchGate, **Lubrizol** (supplier), ClinicalTrials.gov, then two brand explainers | — |
| Live results for **"does PDRN work on skin"** | Dermatology Times, PMC reviews, PLOS One, a brand "hype vs reality" post. The strongest line in the results: the first *topical* human PDRN evidence is described as a **late-2025** study | — |

➡️ **Nobody in this niche publishes independent, appraised, per-study pages.** The ranking brand pages either cite
supplier data or blend several studies into one explainer. Per-study appraisal passes Lily Ray's test (*"could a
competitor publish a near-identical version tomorrow using the same prompt?"*) only if it contains our judgement.
An AI can reproduce an abstract. It cannot reproduce our concentration comparison, our grading, or our decision to
publish a null result.

Mainstream scrutiny is rising too. NPR, 7 Sep 2026, *"The copper peptide trend has gone from creams to injections —
ahead of the science"* ([link](https://www.npr.org/2026/09/07/nx-s1-5955552/copper-peptides-skin-aging-health-safe)).
A brand that shows exactly how strong its evidence is sits on the right side of that story.

### 2.5 Measurement is now possible, and it is free

Search Console's **Generative AI performance report** was announced 3 Jun 2026 and reached every property on
**31 Aug 2026**. It shows **AI Overview and AI Mode impressions per page**, by country, device and date. There are no
clicks and no position. It is UI-only; no API is documented. A site's links appearing several times in one AI
feature count as one impression. ([Help](https://support.google.com/webmasters/answer/16984139?hl=en),
[blog](https://developers.google.com/search/blog/2026/06/gen-ai-performance-reports)) **[OFFICIAL]**

➡️ For the first time we can measure directly whether study pages surface in Google's AI features, rather than
guessing from one SERP snapshot.

---

## 3. The architecture, if built

### 3.1 Placement check (architecture gate)

| Question | Answer |
|---|---|
| **Where?** | L5, vertical content inside the Skingenetix store. Shopify content (metaobjects, a page template, a hub page), not code in `saas-platform/` |
| **Why this level?** | The content is brand- and ingredient-specific. The reusable part is the *method*: the study template, the grading scale and the verify-citation step. That belongs in the central content capability (`smith-ai-agency/docs/capabilities/`), so Hairgenetix and later clients share one template |
| **What consumes it / what does it consume?** | Consumed by the ingredient hubs, product pages, the library page and the Merchant Center Q&A feed. Consumes PubMed/PMC, the claims register (`configs/claim-fixes/`) and `scripts/link-citations.py` |
| **Does it already exist?** | Partly. Hairgenetix has a study template (`hairgenetix/docs/content-briefs/draft-study-zhang-2022.html`) and a research-hub page. Reuse and improve both (§3.4). Do not create a third pattern |

### 3.2 Page type: metaobject web pages, piloted on two entries first

| Option | URL | For | Against |
|---|---|---|---|
| **A. Metaobject `study` (onlineStore + renderable)** ✅ recommended | `/pages/study/<handle>` | **One source of truth.** The same fields (PMID, design, n, duration, concentration, grade, verdict) feed the study page, the library table, hub callouts, product "evidence" blocks and the Merchant Center Q&A. Fix a number once, and every surface updates. Structured fields make the appraisal checklist enforceable. Translatable field by field. Sitemap-included | Zero adopters among the six beauty brands sampled. No native author, date or feed, so the template must render them. Needs a new theme template (a Liquid change, so Malcolm approves) |
| B. Dedicated blog `studies` | `/blogs/studies/<handle>` | Native Article schema, author, dates, RSS. Existing article tooling | Free text, so facts get duplicated across surfaces and drift. Tag archives need the noindex fix. Blog listing pages are thin |
| C. Plain `/pages/` | `/pages/<handle>` | Simplest | No structure, no listing. Each page is hand-built |

**Why A:** the biggest credibility risk here is **inconsistency**. The same trial could be described with different
numbers on the hub, the product page and the study page, and Hairgenetix has already shipped mis-attributed
citations. Structured fields prevent that. **Pilot:** build two entries, then confirm three things: Translate & Adapt
exposes the metaobject fields, the rendered HTML is server-side (not JavaScript), and the pages appear in
`sitemap.xml`. If any of the three fails, fall back to option B with the same template.

The **library page** is a normal page at `/pages/evidence-library`. It renders every `study` entry, plus every
cited lab or animal paper as a non-linked row.

### 3.3 Which studies qualify

**A study gets its own page only if all of these are true:**
1. **Human** participants: RCT, controlled or split-face trial, open-label clinical trial, or a systematic review
   or meta-analysis. Lab, cell, ex-vivo and animal studies get a library row, never a page.
2. **The route is relevant to what we sell.** Topical, or a delivery we can honestly relate to topical use. Injected
   PDRN trials may be *referenced* on the hub, with a clear "this was injected" label, but get no page implying
   topical relevance.
3. **Indexed** in PubMed or with a DOI, and **verified against the abstract or full text**, not just a link that
   resolves (Hairgenetix lesson: a dental-screening paper was cited for AHK-Cu).
4. **Cited by at least one of our pages or claims.** The study page exists because a claim depends on it.
5. **Null and negative results qualify on the same terms.**
6. **It passes the information-gain checklist** (§3.4). If there is not enough to say beyond the abstract, it stays
   a library row.

**Expected size (to confirm per ingredient before committing):** roughly 2–4 qualifying studies each for
Argireline, GHK-Cu, PDRN (topical human evidence is very recent and thin), Matrixyl 3000 (much of it is supplier
data, which is labelled as such) and glutathione (topical vs oral must be separated). **About 12–18 pages.** That
is a curated set, not a template run at scale.

### 3.4 The study-page template

Target **900–1,300 words**, inside the grounding sweet spot (DEJAN; AirOps peak 500–999). The substance goes in the
first 30% of the page (44.2% of ChatGPT citations come from there).

| # | Section | Content | Why |
|---|---|---|---|
| 1 | **H1** | The question the study answers, plus the study's identity. *"Does Argireline reduce eye wrinkles? The 2013 placebo-controlled trial (Wang et al.)"* | A semantic match to evidence queries. **Never the bare head term** (§3.6) |
| 2 | **Byline strip** | "Appraised by [name]. Reviewed by Dr Esther Bodde on [date]. How we grade evidence →" | Who / how / why. Name the reviewer **only after she has reviewed that page** |
| 3 | **Key facts box** | Design · n · who took part · what was applied, at what %, how often · duration · comparator · primary outcome · **result versus comparator, in numbers** · funding and conflicts · **our evidence grade** · PubMed/DOI link | Front-loaded, numeric, extractable. The Sprinklr and Zhang findings (numbers, evidence, specs) |
| 4 | **The verdict in two sentences** | What it shows and how strongly | Confident about what is known (Sprinklr: confident beats hedged). Limits are stated as facts, not hedges |
| 5 | **What they did** | Methods, in plain English | — |
| 6 | **What they found** | Numbers from the full text where available. Redraw any chart from the reported numbers; never copy journal figures unless they are CC-BY | Copyright |
| 7 | **How good is this evidence?** | Randomisation, blinding, size, drop-outs, industry funding, how valid the outcome measure is, effect size versus placebo | **This section is the information gain.** It is what separates us from the abstract, and from INKEY-style supplier citations |
| 8 | **What it does not show** | Lab vs skin · concentration · vehicle · population · duration · "this tested the ingredient, not our product" | Trust, and the EU cosmetic-claims rules (§4) |
| 9 | **How it compares with our formula** | Our concentration and vehicle against the study's, stated neutrally. One product link, only if the product contains the studied ingredient | Honest bridge. The earlier linking cap still applies |
| 10 | **Where it fits** | Links to the ingredient hub (head-term anchor) and to one or two sibling studies on the same question | Links, and tells readers whether this study is typical or an outlier |
| 11 | **Reference** | Full citation, PMID, DOI. Any erratum or retraction status, checked at publication and at each review | Accuracy |

**Leave out:** FAQ blocks (the Q&A genre measures −5.7%, and FAQ rich results were removed on 7 May 2026),
AI-generated before/after images (already excluded site-wide), and any "clinically proven" wording about our product.

**Schema (for correctness, not as a lever).** Ahrefs' controlled test found −4.6% / +2.4% / +2.2%.
- `WebPage` with `reviewedBy` (Person), `lastReviewed`, and `mainEntity` → `Article` (`author`, `datePublished`,
  `dateModified`, `about` → the ingredient).
- `Article.isBasedOn` → `ScholarlyArticle` {name, author, datePublished, `isPartOf` Periodical, `identifier` PMID
  and DOI, `sameAs` the PubMed URL}. This describes the relationship honestly: our page is *based on* a scholarly
  article, and is not one.
- **Never** type our own page as `ScholarlyArticle` or `MedicalScholarlyArticle`. That breaks Google's
  "true representation" rule, and Hairgenetix already reached the same conclusion in its 2026-09-02 audit.
  Everything in the JSON-LD must also be visible on the page.

### 3.5 Hub structure

```
/pages/the-science  (front door, menu "Science")
   ├── /pages/<ingredient>-research   ×5   ingredient hubs: own "what is X" and "does X work"
   │        └── in-prose links to that ingredient's study pages, where each claim is made
   ├── /pages/evidence-library        the study hub: every cited paper, graded; the method page
   │        └── /pages/study/<handle> ×12–18   one per qualifying human study
   └── /blogs/learn/<article>         practical how-to and comparison articles
```

**The library page is itself the most citable asset** in this plan. It is a single table: ingredient · study ·
type (lab / animal / human) · n · grade · one-line verdict · which of our pages rely on it · link. Put a short
**"How we grade evidence"** method at the top. This is the one *original* artefact the layer produces (our
grading of a whole evidence base), so it comes closest to "primary" content. It also carries out the
"Evidence Library" idea already floated in the 2026-09-22 decision.

### 3.6 Linking rules and cannibalisation guard

| Link | Rule |
|---|---|
| Hub → study page | In prose, at the sentence that makes the claim. Anchor describes the finding ("the 60-person placebo-controlled trial"). **This replaces that claim's direct PubMed link.** The study page's key-facts box carries PubMed in its first screen, so a reader is still one click from the source and gains the appraisal on the way |
| Study page → hub | **One** in-prose link in the upper half, using the ingredient's **head-term anchor** ("Argireline®", "what PDRN is"). 12–18 new exact or near-exact anchors address the audit finding that the Argireline hub has **zero** "argireline" anchors |
| Study page → product | At most one, only where the product contains the studied ingredient, framed by the concentration comparison |
| Study page → siblings | One or two, same question |
| Product → study page | The clinical-research block links the one or two most relevant study pages with **varied** anchors, replacing the single templated "View the full Clinical Research & Trials" |
| Library ↔ everything | Library links every study page. Every study page links back to the library once, in the byline strip |
| Body link cap | About 5 internal links in the main content. Hairgenetix's science spokes carried 21–26 and diluted every one |

**Cannibalisation guard** (Hairgenetix study articles outranked their own pillar: 5.1 and 8.6 vs 28.5):
- Study-page titles and H1s **never lead with the bare ingredient term** and always carry the study identity.
- The hubs keep "what is X", "does X work" and "X benefits". Study pages *support* the hub's evidence section
  and do not restate it.
- **Tripwire:** after 6–8 weeks, if any study page holds more than ~30% of a hub head term's impressions, or sits
  above the hub for it, de-optimise the study page's title and move the overlapping text into the hub.

### 3.7 Six locales: translation and noindex policy

⚠️ **Shopify serves the English original at `/de/…`, `/fr/…` and the other locale URLs when no translation exists.**
Those URLs are live, hreflang-linked and in the sitemap. Publishing in English first therefore creates **five
English-language duplicates under foreign-language URLs** straight away.

1. **Before the first study page ships:** a theme change (Malcolm approves) that emits
   `<meta name="robots" content="noindex,follow">` on a `study` entry or the library page **when the current locale
   is not listed** in a `translated_locales` field on the entry. The field is filled only after a translation has
   passed verification.
2. **English live for at least 14 days, then the gate** (§3.8).
3. **Translate with the existing verified pipeline** (Claude translation, read-back, live-HTML check). Never ship
   raw machine translation: the rater guidelines count unsupervised machine translation at scale as having no
   effort.
4. **Order: DE and FR first.** They have the highest locale value on Hairgenetix, and German health AIOs lean
   hardest on non-institutional sources. Then NL, ES and IT.
5. **Do not noindex translated pages to be safe.** Noindexed pages cannot be cited by Google's AI features, which
   need Googlebot to index them.
6. **Maintenance costs ×6.** Any change to a study's numbers must reach all locales in the same release, or the
   outdated translation keeps being served (a known Skingenetix failure).

### 3.8 How to measure it

| Step | What | When |
|---|---|---|
| **0. Hairgenetix read-out (free, before building)** | Search Console → Generative AI report → Pages. Export AI impressions for the 19 EN study articles and the research hubs, Sep–Oct 2026. Compare with the commercial articles | This week. **It decides the size of the build** |
| 1. Baselines | Skingenetix GSC: the 5 hubs' head-term positions and impressions; the Generative AI report per page (if the property has enough volume to show one); trial-shaped queries | Before wave 1 |
| 2. AI citation panel | 20–30 prompts ("does argireline work", "is there evidence for topical PDRN", "copper peptide clinical trials skin", in DE and EN), across ChatGPT, Perplexity and AI Mode, **≥7 runs per prompt per day for 10–24 days** (St. Gallen). Use DataForSEO `llm_responses` (costs money, so it needs Malcolm's OK). Track the skingenetix.com citation share and *which URL* is cited | Before wave 1, then at 8 and 16 weeks |
| 3. Classic search | Study pages: impressions and position on evidence queries. Hubs: the cannibalisation tripwire | 6–8 and 12 weeks |
| 4. Credibility outcomes | Referring domains and mentions that link to library or study pages · reviewer sign-off on 100% of pages · zero unsupported claims in a claims audit | Quarterly |

**Wave plan:** Wave 1 builds the library, plus **five** study pages, one per ingredient and including at least one
null result (Miller 2006), in English. Gate at 8 weeks. Wave 2 builds the remaining qualifying studies. Translation
follows each wave's gate. Change nothing else on the hubs during a wave's window. (Don't bundle changes: the
Hairgenetix August 2026 lesson.)

---

## 4. Risks and how to mitigate them

| Risk | Why it is real | Mitigation |
|---|---|---|
| **Pages read as paraphrase → *Lowest*, and drag on the site-wide classifier** | The rater guidelines and Google's AI guide name "a summary of existing content" as the low-value case. The classifier works site-wide | The appraisal sections (§3.4, rows 7–9) are mandatory. Work from the full text where accessible. Reviewer sign-off. A study that yields nothing beyond its abstract stays a library row |
| **Study pages cannibalise the hubs** | It happened at Hairgenetix | Title rule, intent split and the 30% tripwire (§3.6) |
| **Citation errors** | Hairgenetix cited a dental-screening paper for AHK-Cu and a prostate-surgery paper as Pickart | Check each page against its abstract or full text. Fetch the PMID by script, then read it as a human. Check for retractions at publish and at each review |
| **Reading the evidence as a product claim** | Under the EU cosmetic claims criteria (Regulation (EU) No 655/2013), claims must be supported by adequate evidence. An ingredient trial is not evidence for our finished product | Every page carries "this study tested X at Y%, not our product". No "clinically proven" for products. Watch disease language (e.g. wound healing, alopecia) in DE especially |
| **Honesty cuts both ways** | Pages will show that much of the evidence is thin (PDRN's topical human evidence dates from 2025) | That **is** the credibility. Product and hub copy must then match the grades. The claims-fix programme (`scripts/fix-claims.py`) already moves in this direction |
| **A reviewer byline shown before the review happens** | A fake review is a trust breach, and Trust outranks the rest of E-E-A-T | The byline renders only when a `reviewed_on` date field is set |
| **Locale duplication and stale translations** | Shopify's English fallback at locale URLs; outdated translations still served | The §3.7 noindex-until-translated rule; one-release updates across all locales |
| **Metaobject pages behave unexpectedly** | No adopters to learn from | Two-entry pilot with three explicit checks; the blog fallback uses the same template |
| **Expecting ChatGPT citations** | ChatGPT cites institutions for about 75% of health sources | Set expectations: the gain is mainly in Google's AI features and in site-level trust. Off-site work (listicles, reviews, retail) remains the ChatGPT lever |
| **Freshness decay** | AI freshness comes from maintained updates, not new publishing (Seer) | An annual review date on every entry, with a real re-check: new trials, retractions, errata. Never re-date a page without a substantive change |
| **Measurement noise** | Same-prompt citation overlap is only 0.32–0.43 (Jaccard) | ≥7 runs per prompt per day and rolling windows. No single-run before/after claims |
| **Spreading effort too thin** | Track A (product and feed) still has the largest measured effects | This layer is small (12–18 pages). Run it alongside Track A, not instead of it |

---

## 5. What this changes in existing documents (for Malcolm's decision)

- `decision-citations-study-pages-navigation-2026-09-22.md` §3: "not adopted" becomes **"adopted in modified form,
  pending the Hairgenetix Generative AI read-out"**, with a pointer here. Its "Evidence Library page later" becomes
  the hub of this layer.
- `content-plan-2026.md`: add the library and wave 1 as a Track B item after the hub retitles. They share a
  measurement window with nothing else.
- `todo.md`: (1) Hairgenetix Generative AI export; (2) `study` metaobject definition and two-entry pilot;
  (3) the locale-noindex theme change (needs approval); (4) a per-ingredient list of qualifying studies, verified
  against PubMed.
- Hairgenetix: its study template should adopt §3.4 rows 7–9 (appraisal) and drop the FAQ block. The four-question
  pattern was abstract-level.

**Not changed by this research:** the priority of Track A (product and feed), the off-site track, the hubs owning
the head terms, and the exclusion of before/after search terms.

## 6. Gaps

- **No study anywhere** isolates what adding a research layer does to site-level quality signals. The site-level
  case is Google's documentation plus correlational coverage data.
- **No controlled evidence** that reviewer bylines or PubMed links raise AI citations (Hairgenetix research, 2026-09-22).
- The Hairgenetix AI-feature exposure of its study articles is **unmeasured until the Generative AI report is
  exported**. That is the single most decision-relevant missing number.
- No live Google SERP or AIO pull was made for Skingenetix study-intent queries in this pass (DataForSEO costs money
  and needs approval). The competitor observations come from a general web search and page fetches.
- Perplexity launched "Premium Health Sources" in May 2026; its page could not be fetched (403). Its effect on
  which web pages Perplexity cites for health questions is unknown.
