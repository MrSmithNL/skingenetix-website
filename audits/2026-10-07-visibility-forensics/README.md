# Visibility forensics — skingenetix.com — 2026-10-07

Evidence record for the SEO and AI-search performance review of 2026-10-07. Procedure: the `seo-visibility-forensics`
skill (Phases 0–6; Phase 4 storefront walk and Phase 7 monitor not run: no sales drop was reported). Every line names its
source and verdict: VERIFIED (primary data), PLAUSIBLE, RULED OUT, NOT ESTABLISHED. The plain-English report that reads
this record is `docs/seo-performance-and-ranking-plan-2026-10-07.md`.

Generators used: `scripts/gsc-baseline.py` (Search Console, service account, read-only); the Search Console URL
Inspection API (same key); the skill's `forensics.py timeline|queries|pages` and `serp_gap.py pull|pages|authority|report`
(config: `config.json` in this folder); DataForSEO `backlinks/summary`, `backlinks/referring_domains`,
`serp/google/organic/live/advanced`, `keywords_data/google_ads/search_volume`, `keywords_data/google_trends/explore`;
Lighthouse 13.5 (local, mobile); the central auditor `seo-toolkit/scripts/audit_page.py --criteria v2` (reports in
`docs/audits/page-audit-2026-10-07-*`). Spend for the data in this record: about USD 0.30 (DataForSEO) + USD 1.02 per
central audit.

## Phase 0 — Timeline and decomposition

Search Console has data from **2026-08-31** only: 32 days with data in the 90-day window 2026-07-07 → 2026-10-05. The
site is pre-traffic; there is no drop to decompose. The decomposition sentence is therefore: *of the organic clicks
the site has, 100% arrived in the last five weeks; traffic is growing from zero and conversion cannot yet be measured.*

| Week starting | Clicks | Impressions | GA4 sessions (non-Direct) | Orders |
|---|---|---|---|---|
| 2026-08-31 | 6 | 328 | 0 (0) | 0 |
| 2026-09-07 | 4 | 996 | 33 (8) | 0 |
| 2026-09-14 | 13 | 844 | 36 (16) | 0 |
| 2026-09-21 | 20 | 1,582 | 54 (15) | 2 |
| 2026-09-28 | 35 | 1,538 | 155 (101) | 0 |

Source: `forensics.py timeline`, `gsc-baseline.py --days 90` (78 clicks, 5,288 impressions in total). VERIFIED.
Device split, 90 days: mobile 53 clicks / 1,615 impressions (3.3% CTR), desktop 24 / 3,649 (0.7%). Country: US carries
most impressions at an average position of about 10; the Netherlands most clicks.

Query families (`forensics.py queries`, window 2026-09-07 → 2026-10-04): brand 0 clicks / 0 impressions; topic 3 / 957;
generic 1 / 98. **There is no brand demand**: "skingenetix" does not appear in Search Console and Google Ads returns no
volume for it. VERIFIED.

## Phase 1 — Where each hero page stands

Weekly impressions / clicks @ average position, locales folded into the English path (`dimensions: [page, date]`):

| Page | w/c 08-31 | 09-07 | 09-14 | 09-21 | 09-28 |
|---|---|---|---|---|---|
| /pages/acetyl-hexapeptide-8-research (Argireline hub) | 199/1@9 | 466/0@8 | 380/0@8 | 197/0@8 | 124/0@12 |
| /pages/glutathione-research | 4/0@8 | 30/0@9 | 44/0@8 | 482/0@6 | 49/1@10 |
| /pages/copper-peptide-research | 21/0@49 | 28/0@21 | 18/0@17 | 264/0@8 | 180/1@9 |
| /pages/matrixyl-3000-research | 6/0@14 | 8/0@16 | 33/1@6 | 34/0@10 | 121/3@8 |
| /pages/pdrn-research (all locales; English = 0) | 7/0@25 | 38/0@32 | 4/1@5 | 3/0@10 | 6/0@7 |
| /products/copper-peptide-ghk-cu-renewal-serum | 9/0@4 | 62/0@21 | 29/2@8 | 59/5@7 | 166/3@9 |
| /products/glutathione-brightening-serum | 9/1@9 | 25/0@16 | 45/0@7 | 101/3@9 | 67/3@7 |
| /products/matrixyl-3000-firming-serum | 3/0@5 | 30/0@34 | 42/0@22 | 42/1@15 | 77/0@12 |
| /products/acetyl-hexapeptide-8-anti-wrinkle-serum | 2/0@6 | 12/0@14 | 58/0@9 | 36/0@7 | 50/2@11 |
| /products/pdrn-renewal-serum | 7/0@3 | 13/0@3 | 10/0@5 | 19/1@7 | 37/0@7 |
| /blogs/clinical-studies/pdrn-vs-retinol… (Ye 2026, incl. old /pages/study URL) | – | – | – | 86/1@5 | 175/5@8 |
| / (home) | 9/2@13 | 28/4@9 | 24/2@4 | 52/4@6 | 36/3@5 |

Readings (VERIFIED unless marked):

- **The English PDRN hub has never earned a Search Console impression.** Every impression on that path is a locale
  version (NL 36, ES 12, FR 5, DE 3, IT 2 in 90 days).
- **The Argireline hub is the only page with sustained volume, and it is falling**: 466 → 124 weekly impressions
  over four weeks, position 8 → 12, with zero clicks for a month. Its impressions come from "acetyl hexapeptide-8"
  variants and PubMed-shaped queries ("acetyl hexapeptide-8 topical wrinkles randomized trial pubmed"), not from
  "argireline" (3,734 observed US searches a month), which does not appear in its queries at all. PLAUSIBLE cause of the
  fall: Google's removal of non-human impressions (the skill's data trap, September 2026) plus the loss of the
  pre-rebuild page's query set; NOT ESTABLISHED which share is which. Clicks were ~0 before and after, so nothing of
  value was lost.
- **The head terms are absent.** In the top-200 queries of the last 90 days (678 of 5,288 impressions; the rest are
  anonymised) there is no row for "argireline", "pdrn", "pdrn serum", "what is pdrn", "pdrn skincare", "pdrn cream",
  "argireline serum", "glutathione for skin" or "peptide serum". "matrixyl 3000" has 51 impressions at position 14.5,
  "copper peptide serum" 4 at 32.5, "copper peptide" 3 at 47.
- **What does rank is long-tail and INCI-name queries**: "hexapeptide anti wrinkle serum" p5 (product), "copper
  peptide (ghk-cu) 2% renewal serum" p1 (our own product name), "glutathione whitening serum" p10, "best matrixyl
  serum" p6, "pdrn night cream" p8, quoted study titles at p4–5 on the hubs.
- **The Ye 2026 PDRN-vs-retinol study article is the best new page**: 175 impressions and 5 clicks in its second
  week at position 7–8, in English, German, French and Italian. Not cannibalising its hub: the hub has nothing to lose.
- **DataForSEO ranked keywords (2026-09-30):** 14 US keywords, all at #38–#64; GB one keyword at #66. No top-10 position
  on any target term in any market. VERIFIED (`configs/keyword-data/targeted-2026-09-30/targeted.json`).

### Index status (Search Console URL Inspection API, 2026-10-07)

| URL | Verdict | Last crawl |
|---|---|---|
| /pages/pdrn-research (EN) | **URL is unknown to Google** — never crawled; same for the non-www, trailing-slash and `?view=` variants | – |
| /de, /nl, /fr, /es, /it /pages/pdrn-research | Indexed | 09-05 to 09-17 |
| /pages/acetyl-hexapeptide-8-research | Indexed (referrer recorded: homepage) | 10-05 |
| /pages/copper-peptide-research · glutathione · matrixyl | Indexed | 10-02 · 10-03 · 09-19 |
| all 6 single-product pages checked, /collections/pdrn, /collections/serums, /blogs/clinical-studies, home, the-science, /blogs/learn (empty) | Indexed | 09-26 to 10-07 |
| Wang · Raikou · Badenhorst · Ye · Watanabe study articles | Indexed | 09-30 to 10-05 |
| **Yogya · Tadini · Robinson study articles (live since 10-01)** | **URL is unknown to Google** | – |

The PDRN hub was created and published in Shopify on 2026-03-25, is linked from the homepage, the Science page, its
product, its collection and its study article, sits in `sitemap_pages_1.xml` with lastmod 2026-09-22, returns 200 with a
self-canonical, and serves the identical 439 KB document to a Googlebot user agent and to Chrome (no cloaking, no
challenge page). VERIFIED. Why Google has not fetched it in six months is NOT ESTABLISHED; the only remaining lever is
a manual "Request indexing" in Search Console (no API exists) and more internal links with the exact URL.

Google's `site:` index shows 298 results; the first 20 are mostly locale pages and old `/pages/study/` URLs that now
301 to `/blogs/clinical-studies/`. VERIFIED (DataForSEO SERP).

## Phase 1b — Demand (DataForSEO, US, 2026-10-07; about USD 0.10)

| Term | Google Ads now | 12 months ago | Trend |
|---|---|---|---|
| pdrn | 74,000 (bucketed; observed clickstream 19,734 in Sept) | 22,200 | ×3.3; Google Trends peaked May 2026 at 76, steady at 36–43 since July |
| pdrn serum | 27,100 | 9,900 | ×2.7 |
| copper peptide serum | 12,100 | 3,600 | ×3.4 |
| argireline | 8,100 | 8,100 | flat |
| matrixyl 3000 | 6,600 | 4,400 | +50% |
| peptide serum | 9,900 | 8,100 | flat |
| glutathione serum | 1,600 | 1,300 | flat |
| medicube (brand) | 368,000 | 201,000 | the PDRN category leader by brand demand |
| the ordinary (brand) | 201,000 | 165,000 | |
| skin laundry (brand) | 27,100 | 40,500 | |
| timeless skincare (brand) | 9,900 | 5,400 | |
| skingenetix (brand) | none | none | |

Reading: the category is growing, PDRN fastest; the brands above us carry 10,000–370,000 brand searches a month and we
carry none. VERIFIED (Ads volumes are bucketed; direction only, per the keyword strategy's rule).

## Phase 2 — What we changed (from git, the decisions log and the tracker)

| Date | Change | Site-wide? |
|---|---|---|
| 09-22 | 39 SEO titles rewritten; blog `news` → `learn`; 15 cross-links; 95 title translations; Dr Bodde `reviewedBy` | yes |
| 09-23 | All five hubs to the "research-page standard"; key-figure bar at the top; byline unwrapped | hubs |
| 09-24 → 09-29 | Argireline page becomes the hub template; PDRN (09-24), copper (09-26), glutathione (09-29) rebuilt on it | 4 hubs |
| 09-26 | 24 caveat decisions live on PDRN and Argireline; Raikou live (EN only) | 2 hubs + 1 article |
| 09-29 | `/blogs/clinical-studies` created; 301s from `/pages/study/*`; menu tile under Discover | new section |
| 09-30 | Study articles retitled to their trial question; safety note on every study; payment FAQ + footer link | articles, FAQ |
| 10-01 | Yogya, Tadini, Robinson, Watanabe live ×6; hubs link to them | 4 articles |
| 10-02 | Study authors as Person on ScholarlyArticle; PDRN hub figures realigned to Ye Fig. 6B; result-section layout | articles, PDRN hub |

No change in the window removed a page, changed a URL without a 301, or added a noindex. The theme's Shopify
auto-rewrite of 2026-10-02 (see the skill's data traps) was not audited here: NOT ESTABLISHED whether it touched the
page templates; the buy path was not walked (no sales drop reported).

## Phase 3 — Google events (research note: `research-google-events-2026-10-07.md`)

No core update in the window (last: May 2026). Two spam updates: 18–21 August and one begun 24 September, still open on
7 October, rolling in three observed waves. No Search Console re-count (the 24 September change adds a text/multimodal
filter); one restored logging error (13–17 August, Generative AI report). Site-reputation enforcement loosened for EEA
searchers from 30 August. The town website stonevillenc.org is confirmed hacked and cloaked (13 September report; Wayback
first capture 10 September); curf.clemson.edu is genuine. VERIFIED against Google's pages. Verdict: Google-side events add
noise to head-term positions that were never stable; none penalised the site. The AI-citation factors note is
`research-ai-factors-2026-10-07.md`.

## Authority (DataForSEO backlinks, 2026-10-07; USD 0.08)

| Metric | Value |
|---|---|
| Domain rank | 0 |
| Referring domains | 627 (624 main domains) |
| Referring domains with spam score < 30 | **2** (huldra.pages.dev 2023, antiaginglorraine.blogspot.com 2025) |
| Backlinks | 660, 650 of them text anchors; 34 nofollow |
| TLDs of referring domains | .store 97, .online 94, .site 93, .shop 92, .website 90, .space 85, .com 31, .ru 22 |
| First seen | 2023-10-14 (the domain's first link); **622 of the 627 domains first seen on 2026-10-06 or 10-07** |

The 622 new domains are auto-generated "free backlink generator", "DA checker" and "SEO checker" pages
(dofollowbacklinksgenerator.site, highdachecker.space, buycheapbacklinks.space …), spam score 45–75. They are the
output of someone submitting the domain to link-generator tools in the last two days; Google ignores such links and no
disavow is needed, but they must not be mistaken for authority. VERIFIED. **Genuine referring domains: zero.** The
brands above us on every SERP have thousands.

## Technical (2026-10-07)

| Check | Result | Verdict |
|---|---|---|
| robots.txt | Shopify default; no AI-crawler rules, so OAI-SearchBot, PerplexityBot, Claude-SearchBot, GPTBot are allowed; agents.md and UCP endpoints present | fine |
| Sitemaps | index + per-type per-locale; pages sitemap lists all 19 pages incl. pdrn-research; blogs sitemap lists all 8 studies and the empty /blogs/learn | fine (remove or fill /blogs/learn) |
| Canonical / hreflang | self-canonical; en + 5 locales + x-default on every page checked | fine |
| Old study URLs | /pages/study/*→ 301 to /blogs/clinical-studies/* | fine |
| Structured data, hubs | WebPage + BreadcrumbList + FAQPage + ScholarlyArticle citations + Person/Organization; **no Article type** (central audit S3 fails on it) | fix |
| Structured data, products | Product + Offer + Brand + FAQPage; **no aggregateRating** (reviews are client-side Klaviyo widgets) | fix (gated on verified reviews) |
| HTML weight | 429–647 KB per page | heavy; Impact theme |
| Lighthouse mobile, Argireline hub | performance 60, LCP 11.1 s, FCP 4.9 s, 2.5 MB; SEO 100; accessibility 87 | **poor LCP** |
| Lighthouse mobile, PDRN hub | performance 72, LCP 7.8 s, FCP 2.4 s, 2.7 MB | poor LCP |
| Lighthouse mobile, PDRN serum | performance 60, LCP 4.9 s, TBT 540 ms, 3.9 MB, TTI 15.4 s | poor |
| Field Core Web Vitals | none (too little traffic; CrUX/PageSpeed API keys return 403) | not assessable |
| Title/H1/description | present and keyword-led on every hero page checked | fine |

Lighthouse lab figures are single local runs on a throttled mobile profile; direction is reliable, the decimals are not.

## Central audit v2 (seo-toolkit, 2026-10-07, first run on the hubs)

| Page | Score | Confirmed failures | Report |
|---|---|---|---|
| /pages/pdrn-research | 8.99 | C10 (intro says "more than twice" retinol, key figure says 3.5×, FAQ says "more than three times"; a jar image repeated three times), Q5 ("pdrn" 108 times, 3.5 per 100 words), S3 (no Article type) | `docs/audits/page-audit-2026-10-07-pages-pdrn-research-live.*` |
| /pages/acetyl-hexapeptide-8-research | 7.83 uncapped, **capped 4.9** | P1 cap: "argireline" is also the product page's primary keyword in `page-targets.json`; Q4 (no retinol comparison, nothing on what to avoid combining); C10 (duplicated image block in the FAQ); V1 (no contraindications, pregnancy or interaction guidance); also Q5 ("argireline" 46×), S3 | `…-pages-acetyl-hexapeptide-8-research-live.*` |
| /pages/copper-peptide-research | 8.58 | C10 (duplicated FAQ image; citation paragraph repeated three times; alt text names "Advanced Day Repair cream" against "Day Gel-Cream" on the page); V1 (no interactions, contraindications, when to see a professional); Q5 (69×), S3 | `…-pages-copper-peptide-research-live.*` |
| /pages/matrixyl-3000-research | 8.5 uncapped, **capped 4.9** | P1 cap: "matrixyl 3000" shared with the serum; V1 (no side effects, contraindications); Q5 (78×), S3 | `…-pages-matrixyl-3000-research-live.*` |
| /pages/glutathione-research | 7.78 | C9 (unqualified "Yes" on two trials; the serum, which also contains niacinamide, supported with studies of a different formula); C10 (duplicated image; Watanabe citation repeated four times; serum named two ways); V1 (patch-test tip only); V4 ("keep using it to keep the result", "it works where it is applied" read as promises); S3 | `…-pages-glutathione-research-live.*` |

**Pattern:** C10 (a duplicated image block in the FAQ section), V1 (no safety block beyond patch-testing), Q5 (keyword
repetition above 1.5 per 100 words) and S3 (no Article type) recur on every hub because they come from the shared hub
template. One template fix clears them on all five. The two P1 caps are the keyword-ownership decision that has been
open since 2026-09-30. The retired two-model script's 9.6–9.8 hub scores are not comparable and are withdrawn.

## Phase 5 — Who is above us and why

Generators: `serp_gap.py pull` (33 SERPs, desktop, depth 10, with async AI Overviews; `serp/serp.json`, USD 0.07),
`pages` (top 6 pages per keyword measured; `serp/pages.json`), `authority` (`serp/authority.json`), `report`
(`serp/report.md`); a US mobile pull of nine head terms (`data/serps-us-mobile.json`, USD 0.02); domain authority for 39
domains (`data/competitor-domain-authority.json`, USD 0.05); the three teardowns `teardown-pdrn.md`,
`teardown-argireline-matrixyl.md`, `teardown-copper-glutathione-peptide.md` with `teardown-measurements.jsonl` and the
probe files under `data/`.

| Measure | Result | Verdict |
|---|---|---|
| Our top-10 presence | 0 of 33 SERPs | VERIFIED |
| AI Overviews present / citing us | 22 of 33 / 0 | VERIFIED |
| Most-cited Overview sources | YouTube 15, Google shopping 14, Instagram 7, Reddit 7, Allure 5, The Ordinary 5, Wikipedia 4, Vogue 4, PMC 3, INKEY 3 | VERIFIED |
| Most frequent page-one domains | Reddit 29, essentialdayspa.com (a 2011 forum) 15, Amazon 12, stonevillenc.org 17, YouTube 8, The Ordinary 6 | VERIFIED |
| Hacked-site spam | stonevillenc.org: all 7 organic rows for "copper peptide" (desktop), 4 for "ghk-cu", 3 for "matrixyl 3000", 1 for "pdrn"; also on mobile "copper peptide serum" (3 rows) and a second town site (tobaccovillenc.org). Mobile "copper peptide" is clean (The Ordinary, Neova, NPR, Wikipedia) | VERIFIED |
| Domain authority | skingenetix.com rank 0; The Ordinary 403 (8,629 referring domains), SkinCeuticals 375 (6,536), INKEY 299 (2,638), Timeless 282 (1,810), Medicube 301 (1,135), Remedy 290 (977); the small sites the Overviews cite: Asterwood 160 (106), Klow 185 (167); publishers 461–644 (68,000–1.1M) | VERIFIED |
| Content shape, ours vs #1 | our hubs: 2,086–2,314 words, 13–14 H2s, 5–8 PubMed links, FAQ, reviewer, dated. #1 pages: Amazon about 260 words; The Ordinary about 150; SkinCeuticals explainer; Remedy 844 words with ratings in markup; Timeless 2,636 words with 829 reviews in markup | VERIFIED |
| What our hubs lack that cited pages have | question-shaped sections: "does it work", "Botox in a bottle", side effects / who should avoid, what not to mix / layering, vs retinol, oral vs topical vs injection (glutathione, copper); a definition sentence before the stat tiles; `dateModified` on the Argireline hub | VERIFIED (teardowns) |
| What our product pages lack | `aggregateRating` from genuine reviews (every brand at the top of the product SERPs exposes it); the word "Argireline" (once on the page); concentration and cited facts on the Matrixyl serum; USD in the US schema (unverified) | VERIFIED |
| Collections | `/collections/serums` 53 words, no ItemList; Timeless and Clinical Skin rank #6 and #4 for "peptide serum" with 90–93 words and ItemList; Boots #1 in GB for "pdrn serum" with a collection page | VERIFIED |
| Suspected cloaking among competitors (different page for Googlebot and a browser) | parade.com, caretobeauty.com, proniksedge.com, sweetcare.com, ulta.com (bot walls or cloaking; not probed further) | PLAUSIBLE |
| Prior-work rule | earlier docs compared structure and demand (keyword strategy §5, ownership analysis); never measured: domain authority, brand demand, YouTube/Reddit presence, review markup, mobile SERPs, cloaking. All measured today | VERIFIED |

## Verdicts so far

| Candidate cause of "we rank nowhere" | Verdict | Evidence |
|---|---|---|
| The flagship PDRN hub is not in Google's index | **VERIFIED** | URL Inspection: unknown to Google; 0 EN impressions in 90 days |
| Zero genuine authority; competitors have thousands of referring domains and 10k–370k brand searches a month | **VERIFIED** | backlinks summary; Ads brand volumes |
| Site is 5 weeks old in Google's eyes; most pages crawled once | **VERIFIED** | first GSC data 08-31; crawl dates |
| Three of the four newest study articles are undiscovered | **VERIFIED** | URL Inspection |
| Hacked-site spam occupies the US desktop head-term SERPs (copper peptide, ghk-cu, matrixyl 3000, pdrn) | **VERIFIED** (temporary) | 17 placements; the 13 Sept hack report; Wayback; our probes |
| The pages above us win on reviews in markup, brand demand, distribution and third-party mentions, not on content | **VERIFIED** | Phase 5 table; teardowns |
| Our hubs miss the question-shaped sections the Overviews cite (does it work, side effects, what to mix, vs retinol) | **VERIFIED** | teardowns; central audit Q4/V1 on three hubs |
| Two hubs are capped at 4.9 by the unresolved product/hub keyword ownership | **VERIFIED** | P1 on Argireline and Matrixyl |
| Hub content quality is the blocker | RULED OUT as the primary cause | PDRN hub 8.99 on the central audit with three fixable failures; study pages 9.5–9.9 |
| A Google update penalised the site | RULED OUT | Phase 3: no core update; spam updates target violators; our changes added no spam |
| Mobile page speed (LCP 5–11 s) | PLAUSIBLE contributor, not the cause | Lighthouse; no field data |
| Translations outrank the English (NL/ES PDRN hub indexed, EN not) | VERIFIED as symptom | GSC per-locale rows |

## Open items

1. Request indexing for `/pages/pdrn-research` and the Yogya, Tadini and Robinson articles (manual; Malcolm).
2. Phase 3 (Google events) and Phase 5 (competitor gap) results: see appendices when the subagents return.
3. The 622-domain link-generator blast: check in two weeks whether it keeps growing; no action otherwise.

## Addendum, 15:00 — all five hub audits complete

PDRN 8.99 · copper 8.58 · glutathione 7.78 · Argireline 7.83 → capped 4.9 · Matrixyl 8.5 → capped 4.9. Total cost USD 5.20. None of the five meets the bar (9.0+, no confirmed failures). Template faults C10, V1, Q5 (four of five) and S3 (five of five) recur; P1 caps two; C9 and V4
on glutathione are wording. Reports: `docs/audits/page-audit-2026-10-07-pages-*-live.{txt,json}`.
