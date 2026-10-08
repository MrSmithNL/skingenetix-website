# Teardown: concern pages, The Science, Matrixyl, copper and glutathione, US/GB/DE (2026-10-08)

Tags: [SERP] `serp/serp.json` (desktop, today) · [PAGES] `serp/pages.json` · [AUTH] `serp/authority.json` (domain-level referring domains) · [VOL] `data/volumes.json` (clickstream = observed; Ads bucketed, unused) · [PT] `data/page-table.json` (Search Console, 28 days) · [GSC7]
`2026-10-07-visibility-forensics/data/gsc-weekly-and-query-page-28d.json` · [LH] `data/lighthouse-summary.json` · [LIVE] our pages fetched today · [WF] competitor pages fetched today. Verdicts: VERIFIED / PLAUSIBLE / NOT ESTABLISHED.

## 1. Findings

1. **Five of our pages have no H1**: the four concern pages and The Science serve zero `<h1>` [LIVE]. The concern pages also have only breadcrumb schema, no reviewer, no date, no study citations [PAGES, LIVE]. VERIFIED.
2. **Six of the 14 pairs are shop SERPs** (wrinkle serum, firming serum, skin firming cream, skin repair cream, brightening serum, glow serum): marketplaces, product pages, retailer categories [SERP]. A concern page is the wrong type; product pages should own them.
3. **The copper, glutathione and Matrixyl hubs are the most complete pages on their SERPs** (2,292 to 2,545 words, reviewer, dated 2026-10-07) [PAGES], yet none is in the top 10 for its head term. The gap is authority and time: our domain shows 701 referring domains, all junk per
   yesterday's audit; competitors 89 to 8,695 [AUTH]. PLAUSIBLE.
4. **Claims on the concern pages break the registers** (3.10). Mobile LCP is 12.2 s on a concern page [LH], one run.

## 2. Verdict table

| Keyword (market) | Observed demand [VOL] | Owner | Winnable? | Target |
|---|---|---|---|---|
| wrinkle serum (US) | 251 US / 79 GB | Argireline serum product | not by concern page | shopping/AIO; page one 12 mo, low confidence |
| fine lines and wrinkles (US) | 50 US / 79 GB | fine-lines page | yes | page one 6 mo |
| skin firming cream (US) | 201 | Matrixyl cream product | partly | page one 6-9 mo |
| firming serum (US) | 100 | Matrixyl serum product | unlikely | shopping/AIO |
| skin repair cream (US) | 50 US / 316 GB | none | no | drop |
| brightening serum (US/GB) | 1,057 / 871 | glutathione serum product | yes | page one 3-6 mo |
| glow serum (US) | 654 | none | no | drop |
| peptides for skin (US/GB) | 1,862 / 1,425 | The Science (rebuilt) | yes | page one 6-9 mo |
| peptides in skincare (US) | 352 / GB 395 | The Science | yes | with the above |
| what is matrixyl 3000 (US) | 50 / GB 79 | Matrixyl hub | yes, small | page one 3 mo |
| skingenetix (US) | 0 | home | held | stay #1 |
| copper peptide (GB) | 394 | copper hub | yes | top 5 3 mo, top 3 6 mo |
| glutathione for skin (GB) | 472 | glutathione hub | yes | top 3 3-6 mo |
| kupferpeptide (DE) | 208 | DE copper hub | yes | top 3 3-6 mo |

## 3. Keyword by keyword

### 3.1 "wrinkle serum" (US) → /pages/fine-lines-wrinkles

- **State:** 15 impressions, position 14.9, other queries [PT].
- **Page one:** Amazon twice, Walmart, Ralphs, one brand product page, one clean-beauty guide, a 2010 Consumer Reports piece. **AIO cites** Amazon, Ulta, Allure, La Roche-Posay, Vogue, YouTube [SERP].
- **Top 3 vs ours:** #2 dermaviduals product 127 words, 789 domains; #3 naturalorganicskincare guide 2,793 words, 12 h2, FAQ, author, 4 citations, 2026-06-01 [PAGES] [AUTH] [WF]. Ours 848 words, 3 h2, no author/date/citations.
- **Why they win:** the searcher wants to buy, so shops match; the guide wins on depth and a named author.
- **Changes:** none here. Add "wrinkle serum" as a secondary on /products/acetyl-hexapeptide-8-anti-wrinkle-serum, in its first sentence.

### 3.2 "fine lines and wrinkles" (US) → /pages/fine-lines-wrinkles

- **Page one:** Reddit #1, small clinic and med-spa blogs, one news piece. **AIO cites** Cleveland Clinic, Kiehl's, Health.com, two clinics [SERP]. Informational: right page type.
- **Top 3:** ipawc 769 domains, fadeout 1,079 words, 10 h2, FAQ, 950 domains, 2025-11-26; #4 illumia 633 words, author [PAGES] [AUTH]. Ours 848 words, none of author/date/citations.
- **Why they win:** plain-language causes and options, a named human behind them. The bar is low.
- **Changes, in order:** (1) real H1 "Fine Lines and Wrinkles: Causes and What Helps"; title the same (47 characters). (2) Two-sentence answer first: what fine lines are, what helps (sun protection, retinoids, peptides), and what peptides can and cannot do. (3) Sections: "Fine lines vs
  wrinkles", "What helps, ranked by evidence", "When to see a professional"; advice beyond our products passes the Lily Ray test. (4) Reviewer line (Dr Bodde) and a date. (5) Link Wang 2013 and Badenhorst 2016. (6) Show the Argireline serum, Matrixyl serum, day gel-cream. (7) Link up to
  both hubs, sideways to Firming. (8) Article schema with reviewer. 1,200 to 1,500 words.
- **Target:** page one in 6 months; top 3 needs genuine links.

### 3.3 "skin firming cream" and "firming serum" (US)

- **Demand:** 201 and 100. **Page one:** Amazon, Target, Dermstore, Vitacost; abbio.io article #3; Facebook, Pinterest; spam. No AIO on the cream; the serum AIO cites ZO Skin Health, Crème de la Mer, a compounding pharmacy [SERP].
- **Top 3:** abbio.io 1,318 words, video, author, 2026-04-22, 86 domains; Dermstore serum 322 words [PAGES] [AUTH]. Ours 731 words, 3 h2.
- **Why they win:** product intent; one small brand with a video article and an author reaches #3 on 86 domains.
- **Changes:** the **cream term goes to /products/matrixyl-3000-pro-collagen-firming-cream** (page-table shows 130 impressions at position 5.6 for "matrixyl 3000" [PT]): H1/first line "skin firming cream", GBP/USD price, reviews markup. **"Firming serum" goes to
  /products/matrixyl-3000-firming-serum.** The concern page keeps the informational job "why skin loses firmness" (sourced) and links down to both products.
- **Target:** cream page one in 6-9 months; serum shopping/AIO only.

### 3.4 "skin repair cream" (US; GB 316)

- **Page one:** Sente and Allskin product pages (1,123 and 709 domains), Sephora, a Glamour barrier-repair list, CVS. **AIO cites** DermaRite, YouTube, Amazon, Glamour [SERP] [AUTH].
- **Why they win:** the intent is barrier repair for dry skin; our page is PDRN and copper renewal, and "repairs the barrier" is on the copper avoid list.
- **Verdict:** not winnable by this page; "repair" invites claims we cannot make. **Drop.** GB 316 could be tested later with the PDRN collagen night cream.

### 3.5 "brightening serum" (US/GB) and "glow serum" (US)

- **Brightening, US:** Le Mieux product (194 words, 1,760 domains), Skin Authority (642), Facile (46 words), Amazon, Byrdie list, Rose Inc. No AIO. **GB:** Amazon UK, Simply Be, a suspected cloaked retailer, Reddit, eBay; AIO cites Amazon UK and Google [SERP] [PAGES].
- **Why they win:** short product pages with price and reviews, some very thin (46 and 194 words). Our serum already sits near positions 7-9 (235 impressions, 6 clicks) [PT]. Our concern page is 840 words, no H1.
- **Changes:** owner is **/products/glutathione-brightening-serum**: lead with "brightening serum", the 2% GSSG and Watanabe result in plain words, price, reviews markup, GB shipping line. The concern page re-aims at "dull skin and uneven tone: what helps" and links down.
- **Target:** page one US and GB in 3-6 months.
- **Glow serum:** Amazon, Olive Young (Beauty of Joseon), Target, Pinterest; AIO cites Glow Recipe, Jouer, Byrdie. A brand-product query. **Drop.**

### 3.6 "peptides for skin" / "peptides in skincare" (US/GB) → /pages/the-science

- **Demand:** 1,862 US, 1,425 GB; "in skincare" 352 and 395 [VOL]. Ours: 25 impressions, position 18.6 [PT].
- **Page one US:** a dermatology group, YouTube twice, SkinBetter, Naturopathica, spam. **AIO cites** Cleveland Clinic, UChicago Medicine, The Ordinary, YouTube. **GB:** Dr Rogers, Nourish, Facebook, Glamour UK, M&S; AIO cites Boots, Paula's Choice UK, PMC [SERP].
- **Top 3:** Palm Beach Derm 1,201 words, 9 h2, FAQ, 848 domains. WebFetch shows a 2024 date, no author and one outside link, so it is a weak article [WF] (the measured table says author and 2026-05-14; the two disagree). GB: Dr Rogers 2,672 words, 16 h2, 2 tables, video, 30 citations,
  FAQ, medical-article schema; Nourish 2,531 words, 1,092 domains [PAGES] [AUTH]. Ours: 407 words, 4 h2, FAQ schema, no H1; the title says "peptide skincare".
- **Why they win:** the title is the query and the page is a full explainer. Ours is an index of links.
- **Changes, in order:** (1) H1 and title "Peptides for Skin: What the Research Shows". (2) Opening answer: what peptides are, what has been tested on skin, and that most data is manufacturer-funded. (3) A table of our five actives with evidence grade, study size and concentration: no
  competitor has one, so it passes the Lily Ray test. (4) "How to choose": disclosed concentrations. (5) FAQ: do they work, vs retinol, mixing. (6) Reviewer line, date, 1,200 to 1,500 words. (7) Link down to the five hubs and the serums collection ("peptide skincare" stays with the
  collection). (8) Article schema with reviewer.
- **Target:** page one in 6-9 months; AIO citation PLAUSIBLE with medical review; top 3 NOT ESTABLISHED.

### 3.7 "what is matrixyl 3000" (US) → /pages/matrixyl-3000-research

- **Demand:** 50 US, 79 GB. **Page one:** The Ordinary glossary, No7, Timeless product, Amazon, Reddit, INKEY List, Clarins, INCIDecoder. **AIO cites** The Ordinary, YouTube, No7, INKEY List, Nira [SERP].
- **Top 3:** Ordinary 131 words, 8,695 domains; No7 556 words, 543; Timeless 2,636 words, product [PAGES] [AUTH] [WF]. Ours 2,292 words, 13 h2, FAQ, author, 2026-10-07: the best page on the SERP and not in the top 10.
- **Why they win:** brand authority; a 131-word page beats a 2,292-word one.
- **Changes:** put the one-sentence definition before the stat tiles; otherwise leave it. Switch the owned term (section 5).
- **Target:** page one in 3 months; worth it for the AIO citation, not traffic.

### 3.8 "skingenetix" (US) → /

Rank 1; the AIO cites us and Ankorstore. Look-alikes fill #2-#7 [SERP]; brand demand is 0 [VOL]. Home: 12 clicks, 123 impressions, position 4.9 in 90 days [GSC7]. No `sameAs` in the Organization schema [LIVE]. **Change:** add `sameAs` (Ankorstore, social profiles); nothing else.

### 3.9 "copper peptide" (GB), "glutathione for skin" (GB), "kupferpeptide" (DE)

**Copper, GB** (394). #1 stonevillenc.org (the cloaked spam site flagged yesterday), #2 skintique glossary (269 words, 5 h2, named updater, 18 Aug 2026, 89 domains, no sources) [WF], #3 Paula's Choice NL (156 words), then a university page, WLRN, Amazon. AIO cites PMC, The Ordinary,
Healthline, Wikipedia, YouTube [SERP] [PAGES] [AUTH]. Ours: 2,545 words, 13 h2, reviewer, dated 2026-10-07; 419 impressions at 9.4 in 90 days, mostly quoted-study queries [GSC7]. *Why they win:* a short exact glossary in a large link tree. *Changes:* (1) add "Side effects and who should be
careful" as an H2 (competitors in DE have it; ours has none) from register facts only (tolerated by 39 of 40 women; no sensitive-skin data). (2) GBP price and UK shipping beside the product links. (3) Re-pull in 3 weeks; the rebuild is one day old and recrawl is NOT ESTABLISHED. Top 5 in 3
months, top 3 in 6; first place only if the spam #1 is removed (PLAUSIBLE).

**Glutathione, GB** (472). Today's page one is Reddit, LinkedIn, eBay, Practo (suspected cloaked), RealSelf, JustAnswer: no brand, editorial or medical page. AIO cites PMC, PubMed, MDPI, Cosmoderma, Paula's Choice UK [SERP]. Yesterday's teardown listed a different GB page one (PMC,
Skinsider), so the SERP is unstable. Ours: 2,401 words, reviewer, 13 h2, no side-effects section [PAGES, LIVE]; 599 impressions at 6.6 in 28 days, the most of any page, 1 click [PT]. *Why they win:* no authoritative page holds the organic slots. *Changes:* (1) H2 "Does topical glutathione
whiten skin?" answering honestly: one 30-woman trial, pigment −10.7%, limited evidence, and we do not use the word "whitening". (2) "Side effects and safety" and "Oral, injection or topical?". (3) Short "vs vitamin C" and "vs retinol". Top 3 in 3-6 months; unusually winnable.

**Kupferpeptide, DE** (208). #1 nichebeautylab product (601 words, 1,721 domains), #2 Elle (368 words, 2024), #3 Lesielle (2,634 words, 10 h2, FAQ), #4 mooci (2,085 words, 12 h2, 7-question FAQ, dermatologist review, 2026-09-11) [PAGES] [WF]. AIO cites mooci, nichebeautylab, The Ordinary,
Lesielle. Ours: 2,544 words, German reviewer line (the measured flag missed it) [LIVE]; 29 impressions, position 10.5 [GSC7]. The H1 reads "Copper Peptide (GHK-Cu)" and the body mixes "Copper Peptide" (18) with "Kupferpeptid" (23) [LIVE]. *Why they win:* the German word in the headline
plus "Nebenwirkungen" and "Wo kaufen" sections. *Changes:* (1) H1 "Kupferpeptide (GHK-Cu)". (2) "Nebenwirkungen und Vorsicht" and "Wo kaufen in Deutschland, Österreich, Schweiz" (shipping, price in EUR). (3) Replace "Copper Peptide" by "Kupferpeptid" in prose. Page one is realistic now;
top 3 in 3-6 months: the best-odds term here.

### 3.10 Claims to fix before any of this ships

Live concern pages [LIVE] against the registers: "even reverse them" (fine lines); "safe for sensitive skin? Yes" (Argireline avoid list); "stimulation of new collagen production" (Matrixyl avoid list); "Overnight Structural Repair" (copper: repairs); "more than twice the wrinkle
improvement of retinol" (check against the PDRN register).

## 4. Ranked action list (impact against effort)

| # | Action | Impact | Effort |
|---|---|---|---|
| 1 | Add H1, reviewer, date, cited studies to the four concern pages and The Science | high, unlocks all | small |
| 2 | Fix the 3.10 claims first | removes risk | small |
| 3 | Rebuild The Science as the "Peptides for Skin" pillar | high: 3,287 observed US+GB searches | medium |
| 4 | DE copper: German H1, Nebenwirkungen, Wo kaufen | high: best odds | small |
| 5 | Glutathione hub: whitening answer, side effects, oral/injection/topical | high: weakest SERP | small |
| 6 | Move the shop terms to products: brightening, wrinkle, firming serum, firming cream | medium-high | small to medium |
| 7 | Copper hub (GB): side effects, GBP/UK cues | medium | small |
| 8 | Fine-lines page rewrite (3.2) | medium | medium |
| 9 | Matrixyl hub opener and owned-term switch; home `sameAs` | low | tiny |
| 10 | Drop skin repair cream and glow serum | saves effort | zero |
| 11 | Genuine links: pitch the Ye 2026 and Watanabe results | the real ceiling | large |

## 5. Changes proposed for configs/page-targets.json

| Page | Now | Proposed |
|---|---|---|
| /pages/fine-lines-wrinkles | "fine lines"; secondaries incl. "acetyl hexapeptide-8", "matrixyl 3000" | primary "fine lines and wrinkles"; secondary "fine lines", "wrinkles"; drop the ingredient terms (hubs own them) |
| /pages/firming-skin-density | "firming"; secondaries "matrixyl 3000", "copper peptide" | "skin firmness" (volume not measured); drop both ingredient terms |
| /pages/skin-repair-renewal | "skin repair"; secondaries "pdrn", "copper peptide" | "skin renewal" (volume not measured); drop both ingredient terms |
| /pages/brightening-glow | "brightening"; secondary "glutathione" | "dull skin"; secondary "uneven skin tone"; drop "glutathione" (volumes not measured) |
| /products/glutathione-brightening-serum | not listed | primary "brightening serum"; secondary "glutathione serum" |
| /products/matrixyl-3000-pro-collagen-firming-cream | none | primary "skin firming cream"; secondary "collagen cream with matrixyl" |
| /products/matrixyl-3000-firming-serum | "matrixyl 3000" | add secondary "firming serum" |
| /products/acetyl-hexapeptide-8-anti-wrinkle-serum | "argireline serum" | add secondary "wrinkle serum" |
| /pages/the-science | "peptides in skincare" | primary "peptides for skin"; secondary "peptides in skincare" |
| /pages/matrixyl-3000-research | "matrixyl 3000 benefits" | primary "what is matrixyl 3000" (50 US / 79 GB vs 0) |
| /pages/glutathione-research | "glutathione" | primary "glutathione for skin" |
| /de/pages/copper-peptide-research | no locale entry | add "kupferpeptide" (needs a per-locale mechanism) |
| "glow serum", "skin repair cream" | none | explicitly unowned |

## 6. Open questions for Malcolm

1. Is turning The Science into the "Peptides for Skin" pillar acceptable? The strategy puts explainers inside hubs, but this page is the parent of five hubs.
2. May Dr Bodde review the concern pages and the pillar, in German too?
3. Approve removing the 3.10 claims and the word "repair"?
4. Do we sell in GBP and EUR with local shipping? GB and DE cues depend on it.
5. Appetite for genuine link-building? Content alone cannot close the gap.
6. Agree to drop "skin repair cream" and "glow serum"?
