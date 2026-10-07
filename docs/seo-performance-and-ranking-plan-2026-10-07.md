# Skingenetix: search performance, competitor analysis and the plan to rank first — 2026-10-07

**Written for:** Malcolm, as owner, and the next build sessions.
**Status:** report complete; the plan in Part C needs the decisions listed in §C.6 before building starts.
**Evidence record:** `audits/2026-10-07-visibility-forensics/README.md` (every number, source and verdict), with the raw
pulls in `data/`, the three competitor teardowns (`teardown-*.md`), the measured gap report (`serp/report.md`) and two
research notes (Google events; AI-citation factors).
**Method:** the agency's `seo-visibility-forensics` procedure (decompose, date, verify each cause, then compare each hero
page against the pages above it), with the central auditor (`seo-toolkit`, criteria v2) for page quality and the
`seo-content-strategy` skill for the plan. Spend today: about USD 5.80 in all (five central audits, USD 5.20; DataForSEO about
USD 0.60).

---

## The short version

1. **The site is five weeks old to Google.** Search Console has data from 31 August. In that time weekly clicks grew
   from 6 to 35 and impressions from 328 to about 1,550. That is a healthy start from zero, not a ranking position.
2. **We rank in the top 10 for none of the key terms in any market, and no AI Overview cites us.** Of 33 live SERPs
   checked today (US, GB, DE, NL), 22 carry an AI Overview; we are cited in 0 and appear on page one in 0.
3. **The flagship PDRN hub has never been crawled by Google.** The English `/pages/pdrn-research` is "unknown to Google"
   in the URL Inspection API, while all five translations are indexed. PDRN carries 68% of our search opportunity and
   its demand tripled in a year. This is the single largest fixable problem on the site, and the fix starts with a
   manual "Request indexing" in Search Console.
4. **We have no authority.** 627 referring domains sound like a lot; 622 of them are "free backlink generator" junk
   pages that appeared on 6 and 7 October, and the other five are worthless. Genuine referring domains: zero. The brands
   above us carry thousands of referring domains and 10,000 to 370,000 brand searches a month; "skingenetix" has none.
5. **The content is close to the bar but not at it.** The study articles score 9.5–9.9 on the central audit. The hubs,
   audited on the central criteria for the first time today, score lower than the retired script said: PDRN 8.99 with
   three confirmed failures, Argireline 7.83 uncapped and capped to 4.9 because the product page claims the same
   keyword. The fixes are specific and cheap.
6. **The US head-term SERPs are currently polluted by a hacked town website** (stonevillenc.org) holding several
   page-one slots for "copper peptide", "ghk-cu", "matrixyl 3000" and "pdrn". Google's September spam update is still
   rolling. Those slots will change hands; we should be ready to take them.
7. **What ranks and gets cited above us is not better science.** It is brands with distribution and mentions (The
   Ordinary, SkinCeuticals, INKEY, Medicube), publishers (Allure, Vogue, Cosmopolitan, Forbes), retailers (Ulta, Boots,
   Amazon, Cult Beauty), and user content (Reddit, YouTube, Instagram). Our differentiator, independent appraisal of named
   trials, is real and nobody else in the niche has it; it will only count once the pages are indexed, linked, and
   mentioned elsewhere.

The plan (Part C) therefore has three layers, in this order: **get indexed and fix the pages (weeks 1–2)**, **earn
mentions and reviews (months 1–6)**, and **publish the spokes that fill the unowned questions (months 1–4)**. Ranking
first for "pdrn" against SkinCeuticals and Medicube is a 12-month target at the earliest; ranking first for
"matrixyl and argireline", "does argireline work", "pdrn vs retinol" and the study questions is achievable within a
quarter.

---

## Part A — Where we are and why

### A.1 Traffic and rankings (Search Console, read today)

| Week starting | Clicks | Impressions | Sessions (GA4) | Orders |
|---|---|---|---|---|
| 31 Aug | 6 | 328 | 0 | 0 |
| 7 Sep | 4 | 996 | 33 | 0 |
| 14 Sep | 13 | 844 | 36 | 0 |
| 21 Sep | 20 | 1,582 | 54 | 2 |
| 28 Sep | 35 | 1,538 | 155 | 0 |

- 90-day totals: 78 clicks, 5,288 impressions, 32 days with data. Mobile converts impressions to clicks five times
  better than desktop (3.3% against 0.7%).
- Countries: the US gives most impressions (average position about 10), the Netherlands most clicks. There are no
  brand searches at all.
- DataForSEO's independent check (30 September): 14 US keywords ranked, all between #38 and #64; one GB keyword at #66.

**Where each hero page stands** (weekly impressions / clicks at average position; translations folded in):

| Page | 7 Sep | 14 Sep | 21 Sep | 28 Sep | Reading |
|---|---|---|---|---|---|
| Argireline hub | 466/0 @8 | 380/0 @8 | 197/0 @8 | 124/0 @12 | the only page with volume, and it is falling; its queries are "acetyl hexapeptide-8" variants and PubMed-shaped searches, never "argireline" |
| Glutathione hub | 30/0 @9 | 44/0 @8 | 482/0 @6 | 49/1 @10 | one-week spike after the rebuild, then back to baseline |
| Copper peptide hub | 28/0 @21 | 18/0 @17 | 264/0 @8 | 180/1 @9 | rising since its rebuild; queries are quoted study titles |
| Matrixyl hub | 8/0 @16 | 33/1 @6 | 34/0 @10 | 121/3 @8 | rising; earns the site's few hub clicks |
| **PDRN hub (English)** | 0 | 0 | 0 | 0 | **never shown: not in Google's index** |
| Copper serum (product) | 62/0 @21 | 29/2 @8 | 59/5 @7 | 166/3 @9 | best product page; "buy copper peptides" queries at 12–47, own name at 1 |
| Glutathione serum | 25/0 @16 | 45/0 @7 | 101/3 @9 | 67/3 @7 | |
| Matrixyl serum | 30/0 @34 | 42/0 @22 | 42/1 @15 | 77/0 @12 | "matrixyl 3000" at 23–40 |
| Argireline serum | 12/0 @14 | 58/0 @9 | 36/0 @7 | 50/2 @11 | "hexapeptide anti wrinkle serum" at 5 |
| PDRN serum | 13/0 @3 | 10/0 @5 | 19/1 @7 | 37/0 @7 | tiny; "pdrn serum" absent |
| Ye 2026 PDRN-vs-retinol study | – | – | 86/1 @5 | 175/5 @8 | **the best new page on the site, in four languages** |
| Home | 28/4 @9 | 24/2 @4 | 52/4 @6 | 36/3 @5 | |

**The head terms are absent.** In the 90-day query list there is no row at all for "argireline", "pdrn", "pdrn serum",
"what is pdrn", "pdrn skincare", "pdrn cream", "argireline serum", "glutathione for skin" or "peptide serum". "matrixyl
3000" has 51 impressions at position 14.5; "copper peptide serum" 4 at 32.5; "copper peptide" 3 at 47. What we do rank for
is our own product names, INCI names ("acetyl hexapeptide-8", "ghk-cu"), and quoted study titles, which is exactly what
a new, unlinked site with precise content ranks for first.

### A.2 Indexing: the PDRN hub is not in Google

The Search Console URL Inspection API, run today on 36 URLs:

| URL | Google's verdict |
|---|---|
| `/pages/pdrn-research` (English), including the non-www, trailing-slash and `?view=` forms | **URL is unknown to Google** |
| `/de`, `/nl`, `/fr`, `/es`, `/it` `/pages/pdrn-research` | indexed, crawled 5–17 September |
| the other four hubs, all product pages checked, both collections, the clinical-studies list, home, the-science | indexed |
| Wang, Raikou, Badenhorst, Ye, Watanabe study articles | indexed |
| **Yogya, Tadini, Robinson** study articles (live since 1 October) | **unknown to Google** |

The PDRN page was published on 25 March, is linked from the homepage, the Science page, its product, its collection and
its study article, is in the sitemap, returns 200 with a correct canonical, and serves the identical page to Googlebot and
to a browser. Why Google has never fetched it is not established; what is established is that nothing on our side blocks
it. The fix is manual: Search Console → URL inspection → Request indexing, for the four URLs above. There is no API for
that button.

### A.3 Authority: zero

| Metric (DataForSEO, today) | Skingenetix |
|---|---|
| Domain rank | 0 |
| Referring domains | 627, of which **622 first seen on 6–7 October** on throwaway TLDs (.store, .online, .site, .shop, .website, .space): auto-generated "free backlink generator" and "DA checker" pages, spam score 45–75 |
| Referring domains with a low spam score | 2, both junk blogs |
| Genuine editorial, retailer, press or community links | **0** |

Google ignores link-generator pages, so no disavow is needed, but they must not be read as authority. Every brand above us
on every SERP has real links and real brand demand (US monthly brand searches: Medicube 368,000; The Ordinary 201,000;
Skin Laundry 27,100; Timeless 9,900; Skingenetix none).

### A.4 Demand: the category is growing, PDRN fastest

| Term (US, Google Ads monthly, bucketed) | Now | 12 months ago |
|---|---|---|
| pdrn | 74,000 | 22,200 |
| pdrn serum | 27,100 | 9,900 |
| copper peptide serum | 12,100 | 3,600 |
| argireline | 8,100 | 8,100 |
| matrixyl 3000 | 6,600 | 4,400 |
| peptide serum | 9,900 | 8,100 |

Google Trends puts PDRN's peak in May 2026 and a steady plateau since July at roughly half the peak. The observed
(clickstream) figures in the keyword strategy remain the sizing rule; the Ads figures confirm direction only.

### A.5 Page quality: the central audit, run on the hubs for the first time

| Page | Score (v2) | Confirmed failures |
|---|---|---|
| PDRN hub | 8.99 | the intro says PDRN beat retinol by "more than twice", the key figure says 3.5× and the FAQ "more than three times" (C10); "pdrn" 108 times on the page (Q5); no Article type in the structured data (S3) |
| Argireline hub | 7.83, capped to **4.9** | the product page also claims "argireline" (P1, the unresolved ownership decision, caps the score); no answer to "is Argireline better than retinol?" or "what to avoid with it?" (Q4); a duplicated image block in the FAQ (C10); no contraindications, pregnancy or interaction guidance (V1) |
| Copper peptide hub | 8.58 | duplicated FAQ image and a citation paragraph repeated three times (C10); no interactions, contraindications or when-to-see-a-professional (V1); "copper peptide" 69 times (Q5); no Article type (S3) |
| Matrixyl hub | 8.5, capped to **4.9** | the serum also claims "matrixyl 3000" (P1 cap); no side effects or contraindications (V1); "matrixyl 3000" 78 times (Q5); S3 |
| Glutathione hub | 7.78 | an unqualified "Yes" to "does topical glutathione work?" on one manufacturer trial and one small independent trial, and the serum (which also contains niacinamide) supported with studies of a different formula (C9); duplicated image, the Watanabe citation repeated four times, the serum named inconsistently (C10); only a patch-test tip for safety (V1); "keep using it to keep the result" and "it works where it is applied" read as outcome promises (V4); S3 |
| Study articles (1–2 October) | 9.50–9.88 | four lack a link back from their hub (P3); Yogya's intent (Q3) |
| Clinical-studies list | 9.37 | payment information (R6, flips between runs) |
| Payment page | 8.64 | no byline, no date |

The retired two-model script had scored the hubs 9.6–9.8. Those numbers are not comparable and should no longer be
quoted. **The bar is unchanged (Malcolm, ADR-2026-09-30-Q): 9.0 or more, all gates passing, no confirmed failures.**

### A.6 Technical

| Check | Result |
|---|---|
| robots.txt, sitemaps, canonicals, hreflang (six locales + x-default), 301s from the old study URLs | correct |
| AI crawlers (OAI-SearchBot, PerplexityBot, Claude-SearchBot, GPTBot) | allowed; nothing to change |
| Structured data | hubs are `WebPage` + FAQ + study citations; the auditor expects `Article`. Products carry no `aggregateRating` because the Klaviyo review stars are drawn by script and invisible to machines |
| Mobile speed (Lighthouse, lab) | Argireline hub: performance 60, largest content paint 11.1 s, 2.5 MB. PDRN hub: 72, 7.8 s. PDRN serum: 60, 4.9 s, 3.9 MB, interactive at 15.4 s |
| Field Core Web Vitals | none (too little traffic) |
| HTML weight | 430–650 KB per page (the Impact theme) |

Speed is poor but is not why we rank nowhere; it becomes a factor once pages are competing on page one.

### A.7 What changed on Google's side (verified against Google's own pages)

No core update since May 2026. Two spam updates: 18–21 August and one that began 24 September and had not closed by
7 October. No Search Console re-count (the 24 September change adds a filter). The September update is reshuffling exactly
the head terms where the hacked town site holds page-one slots. None of this penalised us; it adds noise to positions
that were never stable.

### A.8 Why we rank where we rank, ranked by size

| Cause | Size | Fixable by us? |
|---|---|---|
| The PDRN hub and three new study articles are not in the index | largest, for the flagship | yes, this week |
| Zero genuine authority and zero brand demand, against brands with thousands of links and six-figure brand searches | largest, site-wide | yes, over months: mentions, reviews, retail listings, community |
| Five weeks of history; most pages crawled once | large, temporary | time plus internal links and freshness |
| Hubs below the audit bar: contradictions, missing follow-up answers, missing safety guidance, keyword repetition, product/hub keyword clash | medium | yes, days |
| AI Overviews on 22 of 33 SERPs cite YouTube, Google's own shopping, Instagram, Reddit, Allure, The Ordinary; brand-owned explainers are 6% of beauty citations | medium | partly: product data, reviews, mentions |
| Hacked-site spam on four US head terms | medium, temporary | no; be ready when it clears |
| Mobile speed | small today | yes, later |

---

## Part B — Who is above us, and why

Method: 33 live Google SERPs (desktop, top 10, US/GB/DE/NL) pulled today with their AI Overviews; every page above us
measured on words, headings, answer-first opening, named studies, tables, FAQ, author and reviewer, dates, schema, video,
reviews, prices; domain authority for 39 domains; three family teardowns by researchers who read the pages
(`audits/2026-10-07-visibility-forensics/teardown-*.md`); a two-user-agent probe of every suspect domain. Spend: under
USD 0.60.

### B.1 The picture across all 33 SERPs

| Measure | Result |
|---|---|
| SERPs where we are in the top 10 | 0 of 33 |
| SERPs with an AI Overview | 22 of 33 |
| AI Overviews that cite us | 0 of 22 |
| Most-cited sources in those Overviews | YouTube 15, Google's own shopping pages 14, Instagram 7, Reddit 7, Allure 5, The Ordinary 5, Wikipedia 4, Vogue 4, PubMed Central 3, INKEY List 3, Amazon 3, Ulta 3 |
| Most frequent page-one domains | Reddit 29 placements, a 2011 spa forum (essentialdayspa.com) 15, Amazon 12, the hacked town site (stonevillenc.org) 17, YouTube 8, The Ordinary 6, Byrdie 4 |
| Pages above us by kind | user content (Reddit, YouTube, Instagram, forums) and marketplaces first; then brand pages (The Ordinary, SkinCeuticals, INKEY, Medicube, Timeless, Remedy, NIOD); then publishers (Allure, Vogue, Cosmopolitan, Byrdie, Forbes, Glamour); then retailers (Ulta, Boots, Cult Beauty, Superdrug, Douglas, Zalando); medical pages (PubMed Central, Wiley) on the informational terms |

### B.2 Authority: the gap in numbers

DataForSEO domain rank and referring domains, today. Rank reflects link quality; the count alone does not (ours is junk).

| Domain | Referring domains | Domain rank | Role on our SERPs |
|---|---|---|---|
| forbes.com | 1,132,565 | 644 | owns "best peptide serum", "best copper peptide serum" |
| vogue.com · allure.com · cosmopolitan.com · byrdie.com | 206,058 · 97,086 · 107,151 · 68,136 | 561 · 482 · 519 · 461 | the editorial pages the Overviews cite |
| ulta.com · boots.com · cultbeauty.com | 42,856 · 37,346 · 6,024 | 483 · 479 · 341 | retailers; Boots #1 in GB for "pdrn serum" with a collection page |
| innerbody.com | 24,752 | 396 | the "best copper peptide serum" page and the Overview's source |
| paulaschoice.com | 8,918 | 421 | #1 for "acetyl hexapeptide-8" |
| theordinary.com | 8,629 | 403 | #2 "argireline" US, #1 GB; #4 "matrixyl 3000"; 5 Overview citations |
| skinceuticals.com | 6,536 | 375 | #1 "what is pdrn" |
| theinkeylist.com · medicube.us · timelessha.com · skinlaundry.com | 2,638 · 1,135 · 1,810 · 1,956 | 299 · 301 · 282 · 269 | PDRN and Matrixyl brand pages |
| remedyskin.com · neova.com · niod.com | 977 · 1,004 · 1,315 | 290 · 303 · 362 | copper peptide brand pages |
| joinmidi.com · depology.com · klow.co · asterwood.co · maelove.com | 3,531 · 1,320 · 167 · 106 · 1,120 | 323 · 255 · 185 · 160 · 232 | the small sites the Overviews cite for Argireline questions |
| **skingenetix.com** | **627 (622 link-generator junk, 0 genuine)** | **0** | |

Reading: even the smallest brands the Overviews cite (Asterwood, Klow) hold a real domain rank of 160–185 from a few
hundred genuine links; we hold none. The publishers and retailers are a different order of magnitude and are not
competitors to out-write; they are places to be listed.

### B.3 What the pages above us actually are

The measured factor table is in `serp/report.md`. The pattern, term by term:

| Term | #1–3 today (US desktop) | What wins | Our page's measured shape |
|---|---|---|---|
| argireline | Amazon listing (about 260 words, 23 ratings), The Ordinary product (about 150 words of own copy, FAQPage), Amazon | reviews, price, brand; on mobile and in the Overview, explainers (Vogue, Midi, Argentum) that frame "Botox in a bottle" and side effects | hub: 2,086 words, 13 H2s, 8 PubMed links, 3 tables, reviewer named; **no "does it work", no Botox framing, no downsides, no retinol, no "what to avoid"** |
| argireline serum | Reddit ×2, a Q&A site, the spa forum | nothing authoritative; products appear only in the shopping block and the Overview | product: 391 words; the word "Argireline" appears once |
| does argireline work | a 2022 brand blog (Depology), RealSelf, W magazine, Skin Deva, Reddit | small sites with a verdict-first answer | hub never asks the question |
| matrixyl and argireline | spa-forum threads from 2011, a Q&A page, one cloaked spam page | nothing | no page |
| matrixyl 3000 | today Reddit, forum and three hacked-site pages; on 30 September Timeless #1 (829 reviews at 4.9 in markup, 2,636 words, three resellers), The Ordinary #4, No7 #7 | reviews in markup, brand, resellers | serum: 351 words, no concentration, no study, no rating markup; Google currently prefers our cream (position 5.6) over the serum (32.9) |
| copper peptide | 7 of 7 organic rows are the hacked town site; Overview cites NIOD, NPR, Wikipedia, YouTube | nothing legitimate to beat yet | hub: 2,314 words, 6 PubMed links; **no "what not to mix", no layering, no side-effects section** |
| copper peptide serum | Remedy (844 words, author, FAQ, ratings in markup), The Ordinary, Neova, Amazon, Innerbody | ratings in markup, concentration disclosure, brand | product: 417 words, 9 visible reviews, **no rating markup**; our serum already ranks #1 for "copper peptides and vitamin C" |
| best copper peptide serum | Forbes, Reddit, YouTube, Innerbody (updated 2026-09-03, grades concentration disclosure) | publisher roundups | no page; the play is inclusion |
| glutathione for skin | a Wiley review, Derma Co, Cymbiotika, a clinic; Overview cites PubMed, Cosmoderma, Paula's Choice | medical and brand explainers, every one with a safety section and oral-vs-topical-vs-injection | hub: 2,204 words, 5 PubMed links; **no side-effects section, no oral/injection comparison** |
| glutathione serum | Musinsa, eBay, Medicube, Amazon, Noon | a product-feed SERP | product: 425 words; winnable with a clean feed and rating markup |
| peptide serum | The Ordinary, Photozyme, Forbes, Clinical Skin, Colorescience; Timeless #6 and Clinical Skin #4 with 90–93 words of copy and ItemList schema | title match and collection schema, brand | `/collections/serums`: 53 words, no ItemList |
| peptide skincare | Medik8, Dermstore, PubMed Central, Vogue, Image Skincare | retailer and brand category pages | no owner page |
| pdrn vs retinol | a thin acne blog, LinkedIn, YouTube, Reddit | nothing authoritative | the Ye 2026 article: 1,608 words, 12 H2s, reviewer, already at position 7–8 |
| skincare clinical studies | a brand's clinical-results page (FAQPage, 29 questions), a cosmeceutical blog, a university news item | title match | `/blogs/clinical-studies`: 421 words, no ItemList |
| GB pdrn serum | Boots collection page #1, Amazon, a K-beauty blog, Glamour, Cult Beauty | retailer collection pages | our product; `/collections/pdrn` is the page to build |
| DE pdrn | L'Oréal Paris, a brand blog, pdrn-skin.com, feelbe, YesStyle; Overview cites dm, Douglas, Koreanbeauty | brand explainers in German | our DE hub is indexed and has the most words on the SERP (2,180) but no German brand demand |
| NL pdrn | a dermatologist's shop, Little Wonderland, a clinic | clinics and K-beauty shops | our NL hub earned 36 impressions at position 36 |

(The PDRN family is detailed in B.5.)

### B.4 The spam on the US head terms

stonevillenc.org, the website of a North Carolina town, holds 17 page-one placements across our terms: all seven organic
rows for "copper peptide", four for "ghk-cu", three for "matrixyl 3000", one for "pdrn". A 13 September report documents
the hack: Googlebot is served peptide articles, browsers a redirect to a WhatsApp peptide seller. Wayback captures of the
injected URLs start 10 September; by 2 October some return 403. The pages we could fetch today served the same
"Understanding the Entity: GHK-Cu" text to both user agents, with randomised titles and fake old dates, and the site's
homepage is blank. Google's September spam update has been rolling since 24 September. Two more domains on our SERPs
(a 2011 spa forum and a scraper page) hold slots on "argireline serum" and "matrixyl and argireline" with content from
2011–2015.

What this means: on four US head terms there is currently no legitimate #1 to beat, and the slots will change hands
within weeks. The pages that fill them will be the ones the Overview already trusts (NIOD, The Ordinary, Wikipedia, NPR,
YouTube) unless an indexed, linked, question-shaped page of ours is ready. Reporting the hacked site to Google costs
nothing and shortens the wait.

### B.5 Why each family's leaders perform better, in one paragraph each

**Argireline and Matrixyl (teardown: `teardown-argireline-matrixyl.md`).** The content is not what blocks us: our two hubs
hold more cited evidence than any page ranking or cited for these terms (Amazon ranks #1 for "argireline" on about 260
words; The Ordinary on 150). The head terms are won by reviews, price, resellers and brand demand (Timeless: 829 reviews
at 4.9 in markup). The question terms are won by nobody: "does argireline work" shows a 2022 brand blog and a 2021
magazine test; "matrixyl and argireline" shows 15-year-old forum threads and a cloaked spam page; the Overviews cite
small brand blogs (Klow, Skin Deva, Asterwood, Maelove) that rank in no top-million list. Our hub never asks "does it
work", never addresses the "Botox in a bottle" framing (23 mentions on Midi's cited page), has no downsides, retinol or
mixing sections, and those are the People Also Ask themes on 7 of 11 SERPs. Ownership: the hub owns "argireline",
"acetyl hexapeptide-8" and "does argireline work"; the product owns "argireline serum" and "matrixyl 3000 serum" and
needs the word "Argireline" on the page (a trademark decision); "matrixyl and argireline" gets a spoke; the "matrixyl
3000" head term stays with the serum until a clean re-pull, but Google today prefers our cream for it, so the cream's
title should move to "collagen cream with matrixyl".

**Copper peptide, glutathione and the peptide category (teardown: `teardown-copper-glutathione-peptide.md`).** The US
"copper peptide" SERP is entirely spam today; when it clears, the Overview's sources (NPR, Wikipedia, The Ordinary, NIOD,
Reddit, YouTube) fill it. On "copper peptide serum" every brand at the top (Remedy, Cult Beauty, Timeless, Medicube)
exposes ratings in schema and we do not; Innerbody and Forbes own the Overview and the top four for the "best" terms, and
Innerbody grades concentration disclosure, which we state. Our hubs lead on trial evidence but never cover side effects,
what not to mix (our copper serum contains vitamin C, so a formulation owner must answer first) or oral-versus-topical
glutathione, which every cited glutathione page does. Our `/collections/serums` has 53 words and no ItemList schema
while Timeless (90 words) and Clinical Skin (93) rank #6 and #4 for "peptide serum" on title match and schema. The
product schema shows EUR from an EU fetch; the US view was not verified.

**PDRN (teardown: `teardown-pdrn.md`).** Our English hub is not in Google at all, and that decides everything else; it is
also the strongest page on any of the 13 PDRN SERPs (2,237 words, 79 percentage figures, 5 linked studies, a named
medical reviewer, against at most 23 percentage figures on the best competitor page). None of the 33 readable competitor
pages cites the Ye 2026 PDRN-versus-retinol trial; only 8 of 30 commercial and editorial pages link any study; no page
shows a reviewer line. What wins instead: SkinCeuticals (#1 "what is pdrn"), INKEY, Skin Laundry and Cult Beauty with
short brand explainers; Ulta and Boots with category pages; Allure, Vogue, Cosmopolitan and Glamour with listicles; and
on every US PDRN term an AI Overview that cites YouTube (6 of 7 terms; one video, "Does PDRN Really Do Anything?", is
cited on four), Reddit (5 of 7; one r/AsianBeauty thread on three), SkinCeuticals, INKEY and Ulta. A dozen small or
unranked sites hold top-3 slots (ItGirlies, House of Communal, EG Skin Clinic, The K Beauty Edit, Maruderm), so authority
is a handicap, not a wall. The recurring People Also Ask questions are "Is PDRN salmon sperm?" (5 of 13 SERPs), "Do PDRN
serums actually work?" (4), "What not to mix with PDRN cream?", "Can you use retinol and PDRN together?", "How to use
salmon PDRN serum?" and, in German, "Wann sollte man PDRN anwenden?". Our hub answers the origin and the trial; it does
not ask those questions in those words. The single biggest lever is to get the hub crawled, then earn the first genuine
links to it by pitching the head-to-head retinol result.

### B.6 What this means for "why are they performing better"

| Reason | Share of the gap | Evidence |
|---|---|---|
| They are indexed and we (the PDRN hub) are not | total, for PDRN | URL Inspection |
| Reviews and product facts in machine-readable form | large on every product term | Timeless 829 ratings in markup; Remedy, Cult Beauty, Medicube all expose ratings; ours are script-drawn |
| Brand demand and distribution | large on every head term | Medicube 368k, The Ordinary 201k brand searches; Amazon holds 7 of 8 "argireline" desktop slots; every indie in the beauty AI top 25 has Sephora or Ulta distribution |
| Third-party mentions and listicle inclusion | large on "best X" and in the Overviews | Allure, Vogue, Forbes, Innerbody cited; publisher pages are 42% of beauty AI citations, brand sites 6% |
| Question-shaped sections (does it work, Botox, side effects, what to mix, retinol) | medium, and the only gap we close alone | People Also Ask on 7 of 11 Argireline SERPs; every cited glutathione page has a safety section |
| Genuine links | medium, slow | 0 genuine referring domains against 106–8,629 for the brands cited |
| Spam and forum occupancy | temporary | 17 hacked-site placements; Reddit 29 |
| Content depth, evidence, structure | **not a reason**: we lead on all three | measured on every term |

---

## Part C — The plan to rank first, keyword by keyword

### C.1 What the evidence says works here, and what does not

The plan follows the project's own research (`docs/research-2026-ai-search-and-content-hubs.md`, `docs/content-hub-strategy-2026.md`
§9), confirmed today by the two research notes in the audit folder:

- **Rank and substance decide citation; page furniture does not.** Schema, question headings, llms.txt and "restructuring for
  AI" measured null or negative in every controlled study. Topical match of the title and opening to the question, named
  studies with numbers, freshness, and third-party mentions are what correlate with being cited.
- **Brand mentions on other sites correlate with AI citation three times more strongly than backlinks** (Ahrefs, 75,000
  brands). For a brand with zero of either, the first mentions matter more than the first links.
- **For a new brand, reviews and distinguishing product facts break the "incumbent monopoly"**: in the skincare study the
  project already relies on (Chu and Hou 2026), an unknown brand with reviews was recommended 79.7% of the time against
  4.6% without. That work happens on the product page and the feed, not the blog.
- **Shorter, focused pages beat long guides** for AI grounding; the agency skill's 4,000-word pillar rule does not apply
  here (the project ruled it out on evidence; the hubs stay at roughly 2,500 words with the answer first).
- **"Best X" terms owned by publishers are off-site work** (get listed), not pages to build.

### C.2 Layer 1 — Get indexed and get the pages to the bar (weeks 1–2)

| # | Action | Who | Gate |
|---|---|---|---|
| 1 | **Request indexing** in Search Console for `/pages/pdrn-research`, and the Yogya, Tadini and Robinson articles | Malcolm (manual, 5 minutes) | Inspection shows "indexed" within 14 days; re-check weekly |
| 2 | **Fix the hub template once, for all five hubs**: remove the duplicated image block in the FAQ section (C10 on every hub); add a short safety block (contraindications, pregnancy, what not to combine, when to see a professional) in the register's wording (V1); cut keyword repetition to under 1.5 per 100 words (Q5); emit `Article` alongside `WebPage` in the structured data (S3) | Claude | each hub re-audits at 9.0+, no confirmed failures |
| 3 | **PDRN hub: one number for the retinol comparison, and the questions people ask.** Add H2s in the words searchers use: "Is PDRN salmon sperm?" (asked on 5 of 13 SERPs), "Do PDRN serums actually work?", "PDRN vs polynucleotides", "What not to mix with PDRN", "Can you use PDRN with retinol?", "How to use a PDRN serum", a short salmon-versus-plant PDRN section; one definition sentence above the stat tiles; a visible published date beside "last reviewed". German title to carry "Was ist PDRN" and "Wirkung". On both PDRN product pages, link the head-to-head retinol claim to the Ye article (it is stated without a source today). The intro says "more than twice", the key figure 3.5×, the FAQ "more than three times". Settle on the register's figure ("more than three times", Ye 2026 Fig. 6B) in all six languages; the German "mehr als doppelt" goes with it | Claude, Malcolm confirms | C10 clears |
| 4 | **Argireline hub: answer the two unanswered follow-ups** ("Is Argireline better than retinol?" and "What should I avoid using with it?") as H2 sections, and add the "Does Argireline work?" section (656 searches a month, forum-only page one) | Claude | Q4 clears |
| 5 | **Decide keyword ownership and apply it** (open since 30 September): hub keeps "argireline", product takes "argireline serum"; product keeps "matrixyl 3000", hub takes the science terms; a collection owns "peptide skincare". Update `configs/page-targets.json`, the two product titles and the hub H1s | Malcolm decides, Claude applies | P1 cap on the Argireline hub lifts |
| 6 | **Link every study article from its hub** (P3 fails on four of eight) and from the related product page | Claude | P3 clears |
| 7 | **Finish STUDY-DETAIL**: Malcolm approves the English result sections on the eight previews, then translation, then go-live | Malcolm, Claude | the current handover's gate |
| 8 | **Housekeeping**: hide the empty `/blogs/learn` from the sitemap until it has articles (or publish the first spoke there first); give the tag pages distinct titles; mark the eight study articles' translations as reviewed | Claude (tag titles need a core-layout edit: ask first) | |
| 9 | **Remove the retired script's 9.6–9.8 hub scores from the tracker**; record today's v2 scores as the baseline | Claude | done in this session |

### C.3 Layer 2 — Authority, mentions and reviews (months 1–6)

This is the lever that moves the head terms, and it is the one the site has done nothing on. It needs a scope and budget
decision from Malcolm (the hub strategy flagged it on 21 September; the AISOGEN outreach function is not built yet).

| # | Action | Evidence | Cost and owner |
|---|---|---|---|
| 1 | **Reviews that machines can read.** Klaviyo review-request flow after delivery; once there are verified reviews, add `aggregateRating` to the product schema and keep the Shopify Catalog (used by ChatGPT shopping) complete | Chu and Hou: reviews lift recommendation from 4.6% to 79.7% | free; Claude builds the flow, Malcolm approves the email |
| 2 | **Merchant Center feed completeness and conversational attributes**: up to 30 Q&A pairs per product from the claims registers, ingredient sheets as `document_link`, concentrations, variants. The Google & YouTube channel is installed; no product carries any Google Shopping attributes today | lululemon test: brand attributes used in 50% of AI Mode recommendations | free; Claude |
| 3 | **Get into the listicles that own the commercial terms**: Forbes and Innerbody ("best copper peptide serum"), Allure, Byrdie, Cosmopolitan, Glamour UK, Vogue ("best pdrn serum", "pdrn serum"). Pitch the appraised-trial angle and send product; no paid placements | 40.9% of commercial-query citations go to listicles; Allure and Vogue are the most-cited beauty editorial sources | sampling budget; Malcolm decides who pitches |
| 4 | **Dermatologist and creator YouTube reviews.** YouTube is the single most-cited domain in AI Overviews (15 of the 22 Overviews today cite it) | Ahrefs 2026-03; today's pull | sampling budget |
| 5 | **Reddit presence under a disclosed brand account**, answering PDRN, GHK-Cu and Argireline questions in r/SkincareAddiction and r/30PlusSkinCare with links to the study appraisals. Slow (cited threads average 900 days old) but Reddit is on 7 of the 22 Overviews | Semrush 2025-11 | time; Malcolm decides |
| 6 | **Press-release the study appraisals** through a newswire when a new trial is appraised (PRNewswire is among the most-cited sources since September 2025) | Semrush | ~USD 300–500 per release; Malcolm decides |
| 7 | **Retail distribution** beyond Kaufland and Bol: Amazon, Cult Beauty, Boots marketplace. Every indie in the beauty AI top 25 has retailer distribution | 5WPR 2026 | commercial decision |
| 8 | **Dr Bodde's review**: she is credited; she has not yet confirmed. A confirmed review with a profile page is the exact rater evidence for skincare pages | rater guidelines, 2025-09-11 edition | Malcolm |

Measure mentions, not links: a monthly DataForSEO brand-mention count and the AI-citation check (needs Malcolm's OK on the
`llm_responses` spend, about USD 0.70 per run).

### C.4 Layer 3 — Content that fills unowned questions (months 1–4)

The 15 spokes in `docs/content-plan-2026.md` §5 stand. Today's SERPs change their order. Build first where page one is
forums, thin blogs or nothing:

| Order | Piece | Target (observed US/month) | Page one today | Why we can win |
|---|---|---|---|---|
| 1 | "Argireline and Matrixyl 3000 together: what the trials show" (spoke) | matrixyl and argireline, 858 | a spa forum, a Q&A site, a scraper | nobody authoritative; we have both products and both trial sets |
| 2 | "Does Argireline work?" section on the hub | 656 | a brand blog, RealSelf, W magazine, Reddit | hub already weighs all four trials |
| 3 | PDRN vs retinol: add a plain comparison and a "can you use both" section to the Ye article | pdrn vs retinol (growing) | a thin acne blog, LinkedIn, YouTube, Reddit | we hold the only appraisal of the trial that compared them; the article already ranks 7–8 |
| 4 | "Best PDRN serums, compared on concentration and evidence" | best pdrn serum, 1,042 (KD 3) | an affiliate listicle, YouTube, Reddit | thin incumbents; must name competitors honestly and be grounded in concentrations and trials |
| 5 | `/collections/pdrn` rebuilt on the Boots model (collection page with an explainer, every PDRN product, the hub linked) | pdrn skincare 1,817; pdrn serum (GB) | Boots #1 in GB with exactly this page | proven template |
| 6 | "How to use a PDRN serum" and "PDRN vs polynucleotides" spokes | 520 + People Also Ask | brand blogs | hub questions the hub does not answer |
| 7 | "Copper peptides with vitamin C and retinol" spoke | 390 + 170; our serum already ranks #1 for "copper peptides and vitamin c" | brand blogs, Reddit | we already own the long tail |
| 8 | "Best copper peptide serums" | 532 (KD 5) | Forbes, Innerbody, Reddit | harder; pair with listicle outreach |
| 9 | The remaining spokes (glutathione side effects, PDRN how-to, 1% vs 2% GHK-Cu, Matrixyl Synthe'6, German Matrixyl) | per the content plan | | |

Rules that stay: 800–1,500 words, the answer in the first paragraph, a link up to the hub in the first 150 words, named
trials with numbers, the Lily Ray test for every comparison, no "before and after" pages, no translation before the
English has measured for 14 days, one page per keyword and intent.

### C.5 The keyword-by-keyword plan

"Today" is from Search Console (position where we have impressions) or "none" (no impressions in 90 days). "#1 today" is
the US desktop result unless marked; the mobile result is given where it differs in kind. Targets are honest estimates,
not forecasts: "page one" means top 10; "first" means #1 organic. Opportunity figures are observed monthly searches
(US / GB / DE) from the keyword strategy.

| Keyword (market) | Owner page | Today | #1 today, and what wins | Our moves, in order | Realistic target |
|---|---|---|---|---|---|
| **pdrn** (US 19,734 · GB 6,462 · DE 4,650) | PDRN hub | none (not indexed) | desktop: Instagram, hacked site, Ulta; mobile: Reddit, WhoWhatWear, Vogue Arabia, INKEY, YouTube; Overview cites PMC, Allure, SkinCeuticals, Wikipedia | 1 request indexing · 2 fix the three audit failures (one retinol figure, repetition, Article type) · 3 one-sentence definition above the stat tiles; H2s for "what is PDRN in skincare", "PDRN vs polynucleotides", "injections vs topical", "side effects", "how to use" · 4 earn the first mentions (listicles, YouTube, newswire) · 5 DE and NL: the hub is already indexed and the longest page on both SERPs; add brand demand there through retail listings | page one US in 6 months; first in NL/DE within 6 months if mentions arrive; first in US is a 12-month-plus goal against SkinCeuticals and the publishers |
| what is pdrn (US 5,602 · GB 2,285) | PDRN hub | none | SkinCeuticals #1 (brand explainer), PMC, Cosmopolitan, Cult Beauty, Skin Laundry; Overview cites Cult Beauty, YouTube, INKEY, Skin Laundry | same page as above; the H1 question form ("What is PDRN?") and the definition sentence first | page one in 6 months |
| pdrn serum (US 3,936 · GB 2,049 · DE 845) | PDRN serum product | none | desktop: Reddit ×3, hacked site, a small shop; mobile: Allure, a K-beauty shop, The Independent, Cult Beauty; GB: Boots collection #1 | 1 reviews flow → `aggregateRating` · 2 "Argireline"-style fix: say "PDRN serum" and "1%" in the title and first line · 3 Merchant Center attributes · 4 link from the hub and the Ye article · 5 listicle outreach (Allure, Glamour, Vogue, The Independent) | shopping block and Overview citation in 3 months; page one organic in 9–12 months |
| pdrn skincare (US 1,817 · GB 1,182) | `/collections/pdrn` | none (8 impressions in 90 days) | Ulta, Cosmopolitan, SkinCeuticals, Cult Beauty, Nordstrom (retailer and brand category pages, 1,134 words at #1); ours is 38 words and 3 products, the wrong shape for this SERP | rebuild the collection on the Boots model: 200–300-word explainer, every PDRN product, FAQ, CollectionPage + ItemList schema, link to the hub | page one in 6 months |
| pdrn cream (US 2,321 · GB 1,024 · DE 634) | PDRN night cream | none | Reddit, a small shop, YouTube | product-page fixes as for the serum; link from the hub | page one in 6–9 months |
| best pdrn serum (US 1,042, KD 3) | new spoke | none | an affiliate listicle (1,643 words), YouTube, Reddit; Overview cites Glamour, Vogue, Ulta | write the honest comparison on concentration and evidence (naming competitors) after the collection page; pitch Glamour and Vogue in parallel | page one in 3–6 months; first is plausible, the incumbents are thin |
| pdrn vs retinol (US small, growing) | Ye 2026 study article | position 7–8, 175 impressions a week | a thin acne blog, LinkedIn, YouTube, Reddit; no Overview | add a plain comparison section and "can you use both"; link from the PDRN hub and the serum; request indexing not needed (indexed) | **first within 3 months** |
| pdrn after microneedling (small) | Yogya 2022 article | not indexed | — | request indexing; add the aftercare how-to the audit flagged (Q3) | page one in 3 months |
| **argireline** (US 3,734 · GB 1,103 · DE 845) | Argireline hub | none for the term; the page ranks 8–30 for "acetyl hexapeptide-8" | desktop: Amazon ×7 and The Ordinary; mobile: INCIDecoder, Reddit, Depology, WhoWhatWear, a derm blog; Overview cites Vogue, Wikipedia, The Ordinary, Midi | 1 lift the P1 cap (ownership decision) · 2 add the question sections: does it work, Botox in a bottle (what it is and is not), side effects, vs retinol, what not to mix, vs Matrixyl · 3 definition sentence first; `dateModified` in schema · 4 German title with "Argireline" · 5 earn mentions | page one on mobile in 3–6 months; Overview citation plausible once the question sections exist; desktop head slots (Amazon) not a target |
| does argireline work (US 656) | Argireline hub, section | none | a 2022 brand blog, RealSelf, W magazine, Skin Deva, Reddit | the section with that exact heading and a one-sentence verdict first | **first within 3 months** |
| argireline serum (US 605) | Argireline serum product | position 5 for "hexapeptide anti wrinkle serum" | Reddit ×3, a Q&A site, the spa forum; products only in the shopping block and the Overview | the word "Argireline" on the page (trademark decision); rating markup; Merchant Center | shopping block and Overview in 3 months; organic page one in 6 |
| acetyl hexapeptide-8 (US 1,009) | Argireline hub | position 8–30 | Paula's Choice (definition first), Amazon; Overview cites PMC, JDD, Wikipedia | same hub work; keep the INCI name in the H1 | page one within 3 months (already close) |
| matrixyl and argireline (US 858) | new spoke | none | 2011 forum threads, a Q&A page, a cloaked spam page; Overview cites Klow, Skin Deva, Asterwood | write the spoke: three-bullet answer first, "do they work together", "which first", "who should skip", evidence from both hubs, reviewer, link to the duo set | **first within 3 months** |
| **matrixyl 3000** (US 2,725 · GB 1,339 · DE 211) | Matrixyl serum (head term); hub for the science terms | serum 23–40; cream 5.6; hub earns the clicks | desktop today: Reddit, forum, three hacked pages; mobile: Depology, INCIDecoder, Women's Health, Timeless (829 reviews in markup), Paula's Choice; 30 Sept: Timeless #1 | 1 lift the P1 cap: serum keeps "matrixyl 3000", hub takes "what does matrixyl do", the peptide names and all of DE; move the cream's title to "collagen cream with matrixyl" so one page carries the head term · 2 serum: state the concentration if the formula allows, two cited facts, rating markup, fix the pentapeptide/vitamin C mismatch · 3 re-pull after the spam clears | page one in 6 months; first needs reviews and resellers, 12 months |
| **copper peptide** (US 1,362 · GB 394) | Copper hub | position 47 | desktop: the hacked site ×7; mobile: The Ordinary, Neova, NPR, Wikipedia; Overview cites NIOD, NPR, Wikipedia, YouTube | 1 safety block and "what not to mix / how to layer" H2s (formulation owner answers the vitamin C question first) · 2 "oral vs topical vs injection" paragraph (NPR frames the Overview around injections) · 3 template fixes · 4 report the hacked site to Google | page one when the spam clears, within 3 months; first in 9–12 months |
| copper peptide serum (US 2,977 · GB 1,339) | Copper serum product | position 32; the page ranks 6–9 for "buy copper peptides" variants and #1 for "copper peptides and vitamin C" | Remedy (844 words, author, ratings in markup), The Ordinary, Neova, Amazon, Innerbody | 1 rating markup from genuine reviews · 2 "what to combine with" and layering answers on the page · 3 Innerbody and Forbes outreach with a concentration sheet · 4 confirm USD pricing in the US schema | page one in 6 months; first in 12 with reviews and a roundup listing |
| best copper peptide serum (US 532, KD 5) | roundup inclusion, then a spoke | none | Forbes, Reddit, YouTube, Innerbody (updated 2026-09-03) | get listed (Innerbody grades concentration disclosure, which we have); write the comparison only after | inclusion in one roundup within 6 months; our own page page one in 9 |
| **glutathione for skin** (US 1,211 · GB 472 · DE 422) | Glutathione hub | 1 click a week; impressions 30–480 | a Wiley review, Derma Co, Cymbiotika, a clinic; Overview cites PMC, PubMed, Cosmoderma, Paula's Choice; GB: PMC, Skinsider, Cosmoderma | side effects and "who should avoid it"; "oral vs topical vs injection"; one external link from a dermatology or trial-citing site | page one in 6 months |
| glutathione serum (US 555 · GB 236, KD 0) | Glutathione serum product | position 10–24 ("glutathione whitening/brightening serum") | Musinsa, eBay, Medicube, Amazon, Noon: a product-feed SERP | rating markup, feed completeness, "brightening" wording kept, USD schema check | **page one in 3 months**; first in 6 |
| **peptide serum** (US 3,129 · GB 1,418 · DE 1,056) | `/collections/serums` | none | The Ordinary, Photozyme, Forbes, Clinical Skin (93 words, ItemList), Colorescience; GB: Boots, Alpha-H, Forbes | rebuild the collection: title match, 150–250-word intro, FAQ, CollectionPage + ItemList + Product schema | top 8 in 6 months; first unrealistic against The Ordinary and Forbes |
| peptide skincare (US 100 · GB 157 · DE 211) | a peptide collection | none | Medik8, Dermstore, PMC, Vogue, Image Skincare | assign to `/collections/all` (retitled) or a new "peptides" collection; low priority | page one in 6 months |
| collagen cream (US, new cluster about 3,700) | Collagen Skincare page (preview) | 1 impression | Reddit, Sweetcare, Facebook; Overview cites Reddit, Allure, GM Collin, Byrdie | finish the Collagen Skincare rebuild (Malcolm's review pending), then measure | page one in 6–9 months |
| skincare clinical studies (small) | `/blogs/clinical-studies` | none | a brand's clinical-results page (FAQPage, 29 questions), a cosmeceutical blog, a university news item | an explainer paragraph and ItemList schema on the list; the eight articles carry the rest | page one in 3 months |
| study-trial questions (8 articles; no measurable demand) | each article | 9.5–9.9 audits; 3 not indexed | thin or no competition | request indexing; hub links (P3); finish STUDY-DETAIL | first for their own trial questions within 3 months; their job is credibility and citations, not traffic |

**Sequencing:** everything in the "1" positions above is Layer 1 and takes two weeks. The three "first within 3 months"
targets (pdrn vs retinol, does argireline work, matrixyl and argireline) are the proof points to measure the method on.
The head terms move only with Layer 2.

### C.6 Decisions for Malcolm

1. Request indexing for the four URLs (A.2).
2. Keyword ownership (C.2 #5).
3. Scope and budget for the off-site track (C.3): which of reviews flow, Merchant Center attributes, listicle outreach,
   YouTube sampling, Reddit presence, newswire, retail are in; who does outreach.
4. The `llm_responses` AI-citation panel spend (about USD 0.70 a run, monthly).
5. Approve the English on the eight study previews (the open STUDY-DETAIL gate).
6. The tag-page titles need a core-layout edit (asked before, still open).

### C.7 Measurement

- Weekly: the skill's monitor (`monitor.py` with `audits/2026-10-07-visibility-forensics/config.json`): Search Console
  clicks by page and query family, SERP positions on the 33 tracked keywords, Overview citations, authority, alerts on a
  3-position fall or a lost citation. Install the launchd job once Malcolm agrees to the weekly SERP spend (about USD 0.50).
- After every page change: the central audit, 9.0+ with no confirmed failures, once before acting on noise.
- Eight weeks after a study article goes live: the cannibalisation gate (if it takes more than 30% of its hub's head-term
  impressions, de-optimise it), per the content plan.
- Monthly: genuine referring domains, brand mentions, verified review count, AI citations on the 10 tracked prompts.

### C.8 What not to do

Build llms.txt; push schema beyond the minimum; write 3,000-word guides; publish FAQ-format articles; scale "what is X"
or "A vs B" templates; re-date pages without real changes; buy links or placements; use authority-style clinical
language the registers do not support; translate before measuring; bundle changes; chase the link-generator spam with a
disavow (Google ignores it).
