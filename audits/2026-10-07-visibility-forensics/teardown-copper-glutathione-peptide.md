# Competitor teardown: copper peptide (GHK-Cu), glutathione and "peptide serum" keywords

**Site:** www.skingenetix.com (Shopify; US main market, then GB, DE, NL)
**Date:** 2026-10-07
**Method:** today's Google top-10 SERPs (DataForSEO pull, desktop, already paid for), plus my own fetches of the competitor pages with curl and a Chrome user agent (UA), plus WebFetch. No paid API was run. No Rube/Composio.
**Where the numbers come from:**

- SERPs, AI Overview (AIO) references and People-Also-Ask (PAA): `scratchpad/serps-2026-10-07.json`
- Page measurements: `scratchpad/t/analysis.jsonl` (copied next to this file as `teardown-measurements.jsonl`)
- Search demand: `docs/keyword-strategy-2026.md` §4-§5 (observed clickstream, not Ads volume)
- Search Console and backlink context: the brief, plus `scratchpad/backlinks-skingenetix.json`

**Reading rule:** "measured" means I fetched the page today and counted it. "Schema says" means I read the page's JSON-LD. "Not measured" means I could not get the data, and I say why.

---

## 1. The three most important findings

1. **For "copper peptide" and "ghk-cu" in the US, the SERP is currently a hijacked-site spam SERP, and nobody legitimate is in the visible top 7.** Seven of seven organic rows for "copper peptide" are stonevillenc.org. Three more spam or hacked URLs sit in "ghk-cu". That is a
   temporary opening, not a verdict on our content. When Google cleans it, the pages that fill the space are the ones the AI Overview already cites: NPR, Wikipedia, The Ordinary, NIOD, Reddit, YouTube. Our hub is not among them.
2. **Our hub pages are already the strongest *content* in the set on evidence (named trials, PubMed links, tables, reviewer, dates), but they miss the questions Google's own PAA boxes ask: side effects, what not to mix, how to layer.** Both hubs have zero "side effect" or
   "irritation" wording. The copper hub never says what not to mix with copper peptide. The glutathione hub never answers "retinol or glutathione?". Every AIO-cited glutathione page has a safety section.
3. **We lose on authority and on machine-readable commerce signals, not on article quality.**
   - Backlinks: DataForSEO shows 627 referring domains, but they are junk (spam score 52 of 100, rank 0, mostly .store/.online/.site/.ru). There is no genuine referring domain.
   - Reviews: our product pages have no AggregateRating or Review schema, while Cult Beauty, Timeless, Remedy, Alpha-H and medicube all have it.
   - Currency: the schema on both serums says EUR (see §8).
   - Roundups: Forbes and Innerbody own every "best X" SERP, and we are in neither.

**Single biggest lever:** get the copper serum onto the pages Google and the AIO already trust. That means earned inclusion in Innerbody's "best copper peptide serum" roundup (which has an own-brand #1, so the route is a review sample plus a transparent concentration sheet) and
Forbes-type lists. On our own pages, the biggest lever is to put real review markup on the two product pages and answer the PAA safety and layering questions on both hubs. See §6 for the ranked list.

---

## 2. Classification of every URL I treated as a competitor

Each URL was fetched with Chrome UA and with `Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)`. Where a site blocks bots (403 or captcha), I say so.

| Domain / URL | Class | Evidence |
|---|---|---|
| stonevillenc.org (every URL) | **SPAM** (hijacked town site) | See §3 |
| reuniontower.com (`/?w=532525374082400`) | **SPAM** (hijacked) | SERP snippet is an unrelated product listing ("Terracotta light, polaroid proofs, and olive wax seals", "USD25.62 USD67.62 payments of $6.41") under a GHK-Cu title. Today the site returns 403 to both UAs, including the homepage, so I could not read the page. |
| com.ui.edu.ng/ghk-cu-peptide-vitamin-bridge/ | **SPAM** (hijacked university subdomain) | Snippet dated "3 days ago" on a Nigerian university subdomain. Today the URL returns 404 for both UAs, so the page has already been removed. |
| curf.clemson.edu | **EDITORIAL (genuine, institutional)**. My working hypothesis of "hacked" is not supported. | This is the Clemson University Research Foundation. Both UAs return byte-identical HTML (md5 936bea1f..., 99,031 bytes). The Article schema shows published 2021-01-26 and modified 2025-03-19. No spam keywords in the HTML. It ranks for "skincare clinical studies" because it is a real university press item about a skincare line. Not a spam case. |
| amazon.com, amazon.co.uk, amazon.de, ebay, etsy, temu, walmart, target, instacart, doordash, noon, gosupps, boutiqaat, musinsa | RETAILER/MARKETPLACE | |
| theordinary.com, niod.com, medik8, alpha-h, photozyme, timelessha, clinicalskin, colorescience, remedyskin, peachandlily, dermaestheticsusa, medicube.us, drmarnie, hydropeptide, imageskincare, zoskinhealth, them-ethod.com, neova | BRAND | |
| boots, cultbeauty, sephora, spacenk, facethefuture, beautyoutlet, filler-direct, dermstore, superdrug, cosibella, lyko, iciparisxl, skinsider.co.uk, qandaskin | RETAILER | |
| forbes, innerbody, vogue, glamour, elle, cosmopolitan, byrdie, healthline, npr, cleveland clinic, adventhealth | EDITORIAL | |
| westlakedermatology.com, clnq.com, vibrantskin.com, drdavidjack.com, eastparkhealthcare.co.uk, realself, practo | MEDICAL (clinic or practitioner blogs) | |
| pmc.ncbi.nlm.nih.gov, pubmed, cosmoderma.org, jddonline.com, researchgate | MEDICAL (journal) | |
| reddit.com, youtube.com, instagram.com, facebook, linkedin posts, x.com, essentialdayspa.com forum | UGC | The essentialdayspa forum thread is a real old forum page (2,281 words, identical for both UAs). Not spam. |
| wikipedia.org | EDITORIAL (reference) | |

---

## 3. The stonevillenc.org cloaking evidence

**Plain-English verdict:** a US town website (Town of Stoneville, NC) has been taken over and is serving hundreds of machine-written "copper peptide" pages. It is **not** classic user-agent cloaking on the evidence I could gather. It does something related: it disguises itself on
every request. I could not test what real Googlebot sees, because Google verifies Googlebot by IP address and a spoofed UA does not pass that test.

**Observed today (2026-10-07), with the commands run via curl:**

| Test | Result |
|---|---|
| Homepage `https://www.stonevillenc.org/` with Chrome UA and with Googlebot UA | Both return HTTP 200 with a **2-byte body (`\r\n`)**. The real homepage of the town site is blank. Content is only served on the injected deep URLs. |
| Same deep URL, three clients (Chrome UA, Googlebot UA, plain curl) | For three of four test URLs the three responses are **byte-identical** (same md5). So there is no UA-based difference on those. |
| Fourth URL (`/what-is-copper-peptide-serum-team/`) | The three responses **differ** (54,792 / 54,507 / 54,908 bytes). The diff shows the difference is **random per request**, not per UA. |
| What differs between requests | The CSS class names change on every request (for example `dsfcrmt` becomes `bbdlpic`). The `<meta name="description">` and `og:title` change too. One request says "Dec 31, 2025 · What are copper peptides?", the next says "Jan 15, 2026 · Find the best copper peptide serum..." and "Aug 19, 2016 · Learn about using copper peptides...". **The date prefixes in the descriptions are invented.** They are there to make Google show an old-looking date. |
| Visible "Published" stamp | Each page says "Published October Oct 7, 2026 8:35 AM" (today, and with a doubled "October Oct"). Google's snippets for the same URLs carry dates of Sep 8-23, 2026. So the page re-stamps itself with the current time. |
| Title and snippet vs live page | Google indexed "copper peptides dermatology \| Understanding the Entity". The live title now is "...Understanding the Science: How Do Copper Peptides Work?". The title is regenerated, not fixed. |
| Page content | 688 to 752 words each (measured on 5 URLs). Template AI prose ("A Personal Journey into Ingredient Science", "As a longtime enthusiast..."). H1 is the keyword plus a variant ("copper piptide copper peptides for skin"). Slugs are keyword-stuffed ("copper-piptide-studio", "peptido-ghk-info", "copper-peptit-list"). No JSON-LD at all. No canonical tag. `robots: index, follow`. |
| Page furniture | Generic "Log In / Sign Up" nav, a related-keyword link block ("peptide for snoring", "collagen peptides for joint...", "3ml peptide vial"), and bare github/twitter/instagram/youtube links. It has no relation to a town government. |
| Connectivity | My first attempts to the deep URLs hung with no reply, for both UAs, from this IP (TLS completed, no HTTP response). A later retry succeeded. Treat that as intermittent rate-limiting, not a finding. |
| Host | IP 162.241.217.99 (Unified Layer / Bluehost-type shared hosting). WordPress endpoints (`/wp-login.php`, `/wp-json/`) answer 200. This is consistent with a compromised WordPress install. |
| Reach | 7 of 7 US "copper peptide" results; 4 of 8 for "ghk-cu"; 1 of 8 in the GB "copper peptide serum" SERP (#5). Source: serps json. |

**What I could not establish:** whether Google's own crawler receives a different page than I do. To prove that, use Search Console's URL Inspection "Live test" on one stonevillenc URL (not possible, as it is not our property) or a Googlebot-IP fetch. Neither is available to us.

**What to do about it (not our site to fix):** report it with Google's spam report form ("Report webspam", category "hacked content" and "scaled content abuse") and send the town's webmaster a note. Do not copy any of its tactics. Expect the SERP to change without warning.

**Also noticed in our own data:** `refdomains-skingenetix.json` shows 624 referring main domains and 660 backlinks, but spam score 52, rank 0, and a domain named `dofollowbacklinksgenerator.site` first seen **today**. That is link-spam aimed at us (a negative-SEO or link-farm
pattern), not earned authority. Do not report 627 referring domains as a strength.

---

## 4. Per-term teardown

Legend for the tables: **Ours** = our best page for that term, measured today. "n/m" = not measured (reason given).

### 4.1 "copper peptide" (US, 1,362/mo observed, KD 9)

**SERP today:** positions 1-7 are all stonevillenc.org (SPAM). There are **no legitimate organic results in the rows returned** (the pull returned 7 organic rows for this query, not 10). Features: AI Overview, images, PAA, perspectives, popular products (Google Shopping units:
The Ordinary, Good Molecules/Target, Rowe Casa, Peach & Lily, NIOD, Remedy Skin).

**AI Overview cites:** NIOD copper-peptides category, NPR (2026-09-07), Wikipedia (GHK-Cu), The Ordinary copper-peptides category, two Google Shopping product units, two YouTube videos, one Reddit thread (r/SkincareAddictionLux "is using copper peptides even worth it").

**PAA:** What should you not mix with copper peptides? / Does copper peptide stimulate collagen? / How to use GHK-Cu peptide? / How to layer copper peptides?

Because there are no legitimate organic pages, the comparison set is the four web pages the AIO cites.

| Factor | NPR | Wikipedia | The Ordinary category | NIOD category | **Ours: /pages/copper-peptide-research** |
|---|---|---|---|---|---|
| Page type | News article | Reference article | Ingredient collection | Ingredient collection | Research hub |
| Title | "People are injecting copper peptides ahead of the science" | "Copper peptide GHK-Cu" | "Copper Peptides \| Shop by Ingredient" | "Copper Peptides Skincare Selection" | "Copper Peptides (GHK-Cu) for Skin: Benefits and Research" |
| H1 | "The copper peptide trend has gone from creams to injections, ahead of the science" | Copper peptide GHK-Cu | (promo banner text captured; real H1 n/m) | (promo banner text captured) | "Copper Peptide (GHK-Cu)" |
| Main-content words | 1,170 | 2,515 | 36 | 131 | **2,314** |
| H2s | 1 | 7 | 8 (mostly education links) | 2 | 13 |
| Opens with direct answer | No: news lead | Yes: definition | No | No | **Yes** ("Copper peptide (GHK-Cu) is a peptide of three amino acids bound to copper...") |
| Named studies with PubMed/DOI links | 3 links | 61 | 0 | 0 | **6** (Badenhorst 2016, Abdulghani 1998, etc.) |
| Tables | 0 | 2 | 1 | 1 | **3** |
| FAQ | No | No | Yes (education links) | Yes | **Yes**, 6 Q&A with FAQPage schema |
| Visible author / reviewer | Will Stone (NPR), 2026-09-07 | Anonymous | None | None | **Malcolm Smith; reviewed by Dr Esther Bodde, last reviewed 25 Sep 2026** |
| JSON-LD | NewsArticle | Article | none readable (bot shell) | none | WebPage, ScholarlyArticle x6, FAQPage, Person x2 |
| Images / video | 18 / 1 | 16 / 0 | 45 / 0 | 40 / 0 | 32 / 0 |
| Products and prices | none | none | 1 product, $32 | 2 products, $62 and $93 | 4 products listed, EUR 15.05-126.95 |
| Reviews/ratings | none | none | n/m | n/m | none in schema |
| Concentration stated | n/m | n/m | 1% (Multi-Peptide + Copper Peptides 1%) | n/m | **2%, with a section explaining what 2% means** |
| Side effects | Mentioned briefly | None | none | none | **None** |
| How to use | No | No | "Layering Guide" link | No | Yes (3 steps) |
| What to combine with | Vitamin C mentioned | Vitamin C mentioned once | link only | none | "sits well alongside other peptides"; **nothing on what NOT to mix** |
| Results timeline | No | No | No | No | **Yes**: 4 and 8 weeks, from the trial |

**Why they outrank us, in order of weight:**

- **(a) Authority and brand.** NPR and Wikipedia are domains Google trusts for health and are cited in an AIO regardless of page length. The Ordinary and NIOD are one company (DECIEM) with real brand search demand and retail distribution. Reddit and YouTube hold the "does it
  work" intent. We have no genuine backlinks, so a better page cannot beat these on authority alone.
- **(b) Content.** Our content is not weaker. It is the only page of the five with a reviewer, six PubMed-linked trials, tables and a timeline. What it lacks is the safety and mixing material the PAA asks for, and an angle on injections and supplements. NPR's whole article is
  about injections, and GHK-Cu queries carry that intent (the PAA for "ghk-cu" has "Is it safe to inject GHK-Cu everyday?" and "negative side effects of GHK-Cu").
- **(c) SERP features.** The AIO takes the top of the page, then Shopping units and videos. A research hub is not the page type Google puts in a Shopping unit.
- **(d) Technical.** Nothing blocks us that I could see: the hub renders server-side, has canonical and hreflang, and my crawl returned 2,314 words of content. I did not run the Search Console URL Inspection live; the existing `url-inspection-2026-10-07.json` should be consulted for indexing state.

**What must change to beat the best legitimate page:** (there is no legitimate #1 today; the target is "be the first legitimate organic result under the AIO")

1. Add a section "Side effects and who should avoid it" (patch test, skin sensitivity, pregnancy and what is not known) with source links. Answer **"What should you not mix with copper peptides?"** and **"How to layer copper peptides?"** as H2s with a two-sentence answer first.
   Do not invent chemistry; cite the source for each claim, and mark anything with weak evidence as such.
2. Add an "Injections and supplements: what the evidence does and does not show" section. NPR is the AIO's anchor for exactly this. This is a topic where overstating is dangerous, so it is a reviewer-signed section (Dr Bodde) and it does not recommend any route other than topical use.
3. Add a "Copper peptide vs retinol / vitamin C" comparison row. We already have the trial evidence for it in the FAQ; give it its own H2 so Google can lift it.
4. Get one genuine third-party link to the hub (see §6).

### 4.2 "copper peptide serum" (US 2,977/mo, GB 1,339/mo, KD 3)

**SERP today (US):**

| # | URL | Class |
|---|---|---|
| 1 | amazon.com/clp/B00I3OW1M0 (Platinum Skin Care "Super CP Serum") | RETAILER |
| 2 | YouTube: "Are Copper Peptides Worth the Hype? \| Doctorly Reviews" | UGC |
| 3 | amazon.com/dp/B0D1LLWZBG (PeptideLabz hair serum) | RETAILER |
| 4 | healthline.com/health/copper-peptides | EDITORIAL |
| 5 | Reddit r/SkincareAddictionLux | UGC |
| 6 | dermaestheticsusa.com/products/copper-serum | BRAND |
| 7 | peachandlily.com/products/copper-peptide-pro-firming-serum | BRAND |
| 8 | YouTube: "These COPPER PEPTIDE Serums are Ridiculously GOOD" | UGC |

**Top 3 legitimate organic:** the two Amazon pages and the Doctorly video (all legitimate, none of them a content page). **AI Overview cites:** Remedy Skin product page, Innerbody "best copper peptide serum", Forbes "best peptide serums", three YouTube videos, one Instagram reel,
two Shopping units. **PAA:** Which copper peptide serum is best? / What should you not mix with copper peptides? / Is copper good for your face? / Why use copper peptide serum? **Features:** AIO, PAA, popular products, product considerations, video.

| Factor | Amazon #1 (Super CP) | Amazon #3 (hair serum) | Healthline #4 | Remedy Skin (AIO) | Dermaesthetics #6 | Peach & Lily #7 | **Ours: product page** |
|---|---|---|---|---|---|---|---|
| Page type | Marketplace listing | Marketplace listing | Editorial, medical-reviewed | Brand product | Brand product | Brand product | Brand product |
| Title | "Copper Peptide Serum Super CP Serum 1 oz" | "Copper Peptide Hair Serum with Copper Tripeptide-1 & AHK-Cu" | "Copper Peptides: Benefits for Skin and Hair Care, and How to Use Them" | "Copper Peptide Complex Advanced Firming Serum" | "Copper Firming Serum: Elasticity & Anti-Aging" | "Blue Copper Peptide Pro Firming Face Serum" | "Copper Peptide Serum 2% (GHK-Cu) \| Skingenetix" |
| H1 | (cart widget captured) | (cart widget captured) | "How Copper Peptides Assist the Health of Your Skin and Hair" | same as title + "The most studied, multi-functional firming peptide in skincare." | "Copper Serum" | "Copper Peptide Pro Firming Serum" | "Copper Peptide (GHK-Cu) 2% Renewal Serum" |
| Main-content words | 928 | 2,552 | 1,113 | 844 | 464 | 158 | **417** |
| Opens with direct answer | n/a | n/a | Partly ("Copper peptides are among the most talked about beauty trends right now...") | Product pitch | Product pitch | Ingredient list | Product pitch plus one-line explanation |
| Named studies with links | 0 | 0 | 5 PubMed/DOI links | 5 links | 0 | 0 | **0 on the page; the hub has 6** |
| Tables | specs tables | specs tables | 0 | 0 | 0 | 0 | 0 |
| FAQ | No | No | No | Yes | Yes | Yes | **Yes, 6 Q&A with FAQPage schema** |
| Author/reviewer | n/a | n/a | Written by Kristeen Cherney; **reviewed by Sara Perkins, MD** (schema) | "Dermatologist-created", Dr Muneeb Shah | none | none | none on the product page |
| Visible dates | Reviews dated | Reviews dated 2025-2026 | schema dates 2020-10-26 | none | none | none | none |
| JSON-LD | none found | none found | MedicalWebPage, Person | Product x2, Offer, **AggregateRating**, Organization | Product, Offer | ProductGroup, Product, Offer | Product, Brand, Offer, FAQPage, BreadcrumbList. **No AggregateRating/Review** |
| Images/video | 44 / 11 | 121 / 12 | 17 / 1 | 172 / 1 | 23 / 0 | 469 / 7 | 33 / 0 |
| Price | not captured | not captured | none | 4 price points | $125, $150, $185 | $50 | EUR 49.00 (schema currency EUR) |
| Reviews/ratings | Amazon star rating plus reviews | Amazon reviews | none | **AggregateRating in schema** | star icons on the page | yes | Customer before/after photos, **no rating markup** |
| Concentration stated | no | 9% appears in text (unverified meaning) | none | n/m ("20%" is another ingredient) | **1.2%** | none | **2% (20,000 ppm)** |
| Side effects | no | no | **Yes**, section "Are there any risks or side effects?" | no | no | no | **no** |
| How to use | no | 8 mentions | **Yes** | Yes | Yes | no | **Yes** ("3 simple steps") |
| Combine with vitamin C/retinol | no | no | mentioned | 4 and 2 mentions | mix mentions | no | 1 mention each; no guidance |
| Results timeline | no | 1 mention | no | 2 | 1 | no | 1 mention |

**Why these outrank us:**

- **(a) Authority/brand.** Amazon, Healthline and Reddit are among the highest-authority domains for any shopping query. Amazon also has years of reviews and the "buy" convenience.
- **(b) Content.** For this query Google is not rewarding long content: the #1 and #7 pages have 928 and 158 words. The signal is the product plus reviews. Our product page is mid-pack on words (417) and the only one in the set that states a double-digit concentration (2%, which
  is higher than The Ordinary at 1% and Dermaesthetics at 1.2%).
- **(c) SERP features.** The AIO, Shopping units, YouTube and "product considerations" fill the page. The "Which copper peptide serum is best?" PAA is answered by roundups (Innerbody, Forbes), not by a brand page.
- **(d) Technical.** The visible product-page gap is **machine-readable social proof**. Remedy, Cult Beauty (AggregateRating plus 10 Review items), Timeless (AggregateRating on 16 products), medicube and Alpha-H ("4.7 out of 5, 92 reviews" on the page) all expose ratings. We have
  review photos but they are invisible to search engines (see the existing note `klaviyo-reviews-are-invisible-to-machines`). Also: **GSC shows the product page at position 6-9 mostly on "buy copper peptides" queries at positions 12-47 with 3 clicks from 166 impressions**, which
  fits a page that is a candidate but has no rating stars or price in the result.

**What the product page must change:**

1. Add AggregateRating and Review markup from the real reviews (only genuine ones; the store already has a memory rule that review honesty matters). This is the one change competitors show a direct link to.
2. Add a short "Side effects, patch test and who should avoid it" block and a "How to layer" block ("use with: ..., avoid with: ...", sourced). **Check the formulation first:** our serum contains stable vitamin C alongside 2% GHK-Cu (product page: "stable vitamin C, niacinamide
   and hyaluronic acid"), while the common advice in the PAA is not to mix copper peptides with vitamin C. A product page that says nothing about this invites the question; it needs an answer from the formulation owner, written with care, not a guess from me.
3. Link the 2% claim to the hub's "What 2% GHK-Cu means" section and quote the Badenhorst figure with the "funded by the maker" caveat the hub already carries.
4. Confirm the US price and currency (see §8).

### 4.3 "ghk-cu" (US, 757/mo observed for "ghk copper peptide"; Ads showed 135,000)

**SERP today:** 6 of 8 organic rows are spam (stonevillenc.org x4 at #1, #3, #4, #8; reuniontower.com #6; com.ui.edu.ng #7). The two legitimate rows are Amazon supplement listings: #2 "GHK-Cu Peptide with Liposomal Delivery for Hair & Skin" and #5 "GHK-Cu Copper Peptide
Supplement, 6-in-1 Collagen". **No AIO.** Features: AIO flag is in the features list but no references returned, knowledge graph, PAA, perspectives.

**PAA:** What is GHK-Cu peptide used for? / What are the negative side effects of GHK-Cu? / What shouldn't you mix with copper peptides? / Is it safe to inject GHK-Cu everyday?

I did not fetch the Amazon listings for this query (they are marketplace supplement pages and not comparable to a skincare hub). **This is mostly off-intent for us:** the shopping intent is oral supplements and injections, which our strategy marks as off-intent. The only part we
can reasonably serve is the PAA "What is GHK-Cu used for / side effects / what to mix", as a labelled section of the hub. Do not chase this term with a product page.

### 4.4 "best copper peptide serum" (US 532/mo, KD 5)

**SERP today:** #1 Forbes "The Best Peptide Serums That Smooth And Firm Skin"; #2 Reddit r/Ulta; #3 YouTube; #4 Innerbody "Best Copper Peptide Serum \| The top 7 options of 2026"; #5 Amazon search page; #6 **them-ethod.com "Best Copper Peptide Serum: What to Look For"**; #7
YouTube dermatologist review; #8 neova.com collection; #9 Target search page; #10 Walmart "best copper peptide serum" page. No AIO shown for this query, PAA present.

**Top 3 legitimate:** Forbes, Reddit, YouTube. **Forbes could not be measured**: it returns 403 to Chrome UA, 403 to Googlebot UA and 403 to WebFetch (bot wall). Its title and date come from the SERP only (article URL dated 2026-08-06).

| Factor | Innerbody #4 | them-ethod #6 (brand blog) | **Ours** (no page targets this) |
|---|---|---|---|
| Type | Editorial roundup | Brand blog post (Shopify) | Hub is informational, product is a product page |
| Title / H1 | "Best Copper Peptide Serum \| The top 7 options of 2026" | "Best Copper Peptide Serum: What to Look For" | n/a |
| Words | **8,834** | 1,360 | hub 2,314 |
| Direct answer up top | Summary block: "Best for most people: Copper Peptide by Innerbody Labs", "Best upmarket alternative: Allies of Skin..." | No; a framing paragraph | No |
| Named studies with links | **26 PubMed/DOI links** | 0 | 6 (hub) |
| Tables | 4 | 0 | 3 (hub) |
| FAQ | FAQPage schema, 4 Q&A | Yes | hub FAQ |
| Author/reviewer | Dan Min (schema); 8 Person entities in the schema | "Admin" | Malcolm Smith plus Dr Bodde |
| Dates | Last updated Sep 3rd, 2026 | published 2026-07-28 | hub reviewed 25 Sep 2026 |
| JSON-LD | Article, **Product x7, Review x7**, ItemList, FAQPage | Article | |
| Products and prices | 7 products with prices | 1 price ("£100") | |
| Concentration | **Compares them** (e.g. "1% ... more or less standard", "Good Molecules ... 5ppm") | no | 2% stated |
| Side effects | **31 mentions**, a section "Are copper peptides safe?" | 4 mentions | 0 |
| How to use / mix | mix 13 mentions | how to use 14, "How to use a copper peptide serum without overloading skin" | |
| Results timeline | yes | "What results should you realistically expect?" | yes (hub) |

**Can a brand page win this?** Partly, and on the evidence in front of me:

- A **brand blog does rank**: them-ethod.com is #6 with a 1,360-word guide, an author of "Admin" and zero study links. So the threshold for a brand guide is low.
- The top of the SERP is **Forbes, Reddit and YouTube**, which brand content does not displace. Innerbody's #1 recommendation is its own brand ("Copper Peptide by Innerbody Labs"), so its list is partly self-interested, but it still funnels the AIO citation for "copper peptide serum".
- Innerbody scores brands on **disclosed concentration**. It marks down INNBEAUTY for not specifying it. We are the only brand in the set that states 2% (20,000 ppm) on the pack. That is a genuine hook for the outreach in §6.

**Verdict:** write one "best copper peptide serum" guide on our own site as a *supporting* page (an honest comparison that includes competitors, with our 2% and funded-by-maker caveats), aimed at the #6-#8 band where them-ethod and Neova sit. The realistic route to the #1-#4 band
is to be **listed** in Innerbody, Forbes-type and Glamour/Vogue-type roundups. It is not a content problem.

### 4.5 "glutathione for skin" (US 1,211/mo, GB 472/mo, KD 29)

**SERP today (US):** #1 Reddit r/SkinSolutionsindia; #2 LinkedIn post; #3 Amazon search page; #4 RealSelf (injections, Saudi Arabia); #5 Practo (injections); #6 Instacart (NOW oral supplement); #7 essentialdayspa forum; #8 eBay. **No brand, editorial or medical page in the
organic rows.** The intent is skin whitening, injections and pills. **Top 3 legitimate:** Reddit, LinkedIn, Amazon.

**AI Overview cites (US):** PMC11862975 (narrative review, glutathione supplementation for skin lightening), Cosmoderma review, Paula's Choice, Westlake Dermatology, Ovid/Pigment International, Skinn Suite, Vibrant Skin. **PAA:** Does glutathione good for skin? / Which is better,
retinol or glutathione? / What foods are high in glutathione? / What are the side effects of glutathione on skin?

**SERP (GB):** #1 PMC11862975; #2 Skinsider (retailer ingredient page); #3 Cosmoderma; #4 Amazon UK; #5 CLNQ clinic blog; #6 Dr David Jack; #7 Paula's Choice; #8 East Park Healthcare. AIO cites PMC, PubMed 40013212, Cosmoderma, PubMed 39444151, Skinsider, Skintique, Vibrant.

| Factor | PMC11862975 (AIO #1, GB #1) | Cosmoderma | Paula's Choice | Westlake Derm | Vibrant Skin | Skinsider (GB #2) | **Ours: /pages/glutathione-research** |
|---|---|---|---|---|---|---|---|
| Type | Peer-reviewed review | Journal review | Brand education | Clinic blog | Clinic blog | Retailer ingredient page | Research hub |
| Title | "Exploring the Safety and Efficacy of Glutathione Supplementation for Skin Lightening: A Narrative Review" | "Glutathione in dermatology: A bright future or fading hype?" | "Glutathione for Skin: Skin Benefits & Uses" | "Glutathione Skin Brightening: Does It Really Work?" | "Glutathione for the Skin: Things You Need to Know" | "Glutathione Korean Skincare Products" | "Glutathione for Skin: Benefits, Studies and How to Use It" |
| Words | 5,319 | 1,542 | **not measured**: body is not in the HTML I received (10 visible words; likely a bot-protection shell). Schema read instead. | 1,345 | 1,644 | 474 | **2,204** |
| H2 questions | Review headings | Mechanisms, Clinical evidence, Safety and adverse effects, Controversies | n/m | "Potential Side Effects and Safety Concerns"; "Topical vs. Oral vs. Injectable"; "Is Glutathione Better Than Other Brightening Ingredients?" | "How Long Does Glutathione Take to Work", "Glutathione for Skin Side Effects" | "What is glutathione?", "Is glutathione good for skin?" | "What Is Glutathione?", "At a glance", "What Does Glutathione Do for Skin?", "How to Use" |
| Direct answer at the top | Abstract | Abstract | n/m | Yes | Yes | Yes | **Yes** |
| Named studies with links | 81 links | 11 | 0 | 1 | 4 | 0 | **5** (Watanabe 2014; Wahab 2021 etc.) |
| Tables | 0 | 1 | n/m | 0 | 0 | 0 | **3** |
| FAQ | no | no | **FAQPage schema, 9 Q&A** | yes | no | yes | **FAQPage, 6 Q&A** |
| Author/reviewer | Journal authors | Gupta S., doi 10.25259/CSDM_49_2025, 2025-04-29 | Mercedes Santaella-Lam; **reviewed by Corey L. Hartman MD** (schema); published 2023-01-23, modified 2026-06-16 | Eden Warrick, PA-C (board-certified PA) | "Vibrant Team", 2026-05-19 | none | **Malcolm Smith; reviewed by Dr Esther Bodde; last reviewed 26 Sep 2026** |
| Side effects | 16 mentions | covered | 2 | **6 mentions, own section** | **10 mentions, own section** | 1 | **0** |
| What to combine with | 1 | 3 vitamin C | 0 | 1 retinol | vitamin C 2, retinol 4, mix 10 | 0 | vitamin C 8 mentions, retinol **0** |
| Timeline | 11 | 5 | n/m | 0 | 5 | 0 | **22** |
| Concentration | 0.1%-3% in review | 0.5% | n/m | 2% | 2% | 20% | **2%, stated, with an explanation** |

**Why the AIO-cited pages outrank us:**

- **(a) Authority.** PMC, Cosmoderma (a journal), Paula's Choice (a top skincare brand) and clinic sites are all trusted health sources with real backlink profiles. We have none.
- **(b) Content.** Every AIO-cited page has a **safety and side-effects section** and a comparison with the other routes (oral, injection, other brighteners). Our hub has the strongest trial evidence (the Watanabe double-blind trial and an independent trial) but **never mentions
  side effects**, never answers "retinol or glutathione?", and does not address oral vs topical vs injection, which is what the searcher is actually after. Google's PAA shows what they ask.
- **(c) SERP features.** Organics are Reddit, forums, Amazon. The AIO is the prize and it prefers medical sources. We are not cited.
- **(d) Technical.** Nothing blocking. **A note on our own spike:** the hub went to 482 impressions in one week and fell to 49. I cannot say why from this data. The common pattern is a short-lived test position that Google withdrew after a quality check; I have no evidence for
  that here, so treat it as a hypothesis to check in Search Console (queries and position by day for that week).

**What the hub must change to beat the best legitimate page** (Skinsider in GB, PMC and Cosmoderma as AIO anchors):

1. Add "Side effects and safety" (topical use, patch test, what is known and not known) and "Oral, injection or topical?" as H2s. Say plainly that the IV/injection route is not what this page covers, and that safety concerns exist (the PMC review has a safety section; quote and
   link it). Only quote what the source states.
2. Add "Glutathione vs retinol" and "Glutathione vs vitamin C" as short H2s with a two-sentence answer first.
3. Keep the brightening claims as they are (the register rules about wording stay in force).

### 4.6 "glutathione serum" (US 555/mo, GB 236/mo, KD 0)

**SERP today (US):** #1 global.musinsa.com (VT Cosmetics Tone-On Serum); #2 eBay (Glutathione Comprime Super Fort Whitening Serum); #3 medicube.us "AGE-R Glutathione Glow Serum"; #4 Amazon Live video; #5 Noon (Saudi); #6 Reddit r/IndianBeautyTalks; #7 gosupps. **No AIO.**
Features: forums, images, PAA, popular products, short videos. **Top 3 legitimate:** Musinsa, eBay, medicube.

| Factor | Musinsa #1 | medicube #3 | **Ours: /products/glutathione-brightening-serum** |
|---|---|---|---|
| Type | Marketplace listing | Brand product | Brand product |
| Title | "VT COSMETICS VT Glutathione Tone-On Serum 30ml" | "[Subscr.] AGE-R Glutathione Glow Serum" | "Glutathione Serum 2% with Vitamin C \| Skingenetix" |
| Main-content words | 2 (listing is JavaScript-rendered) | 94 | **425** |
| JSON-LD | Product, **AggregateRating**, Offer | Product x2, Offer, **AggregateRating** | Product, Offer, FAQPage. **No AggregateRating** |
| Concentration | no | no | **2% GSSG** |
| FAQ | no | no | 6 Q&A |
| Price | n/m | $300 shown in schema/page text (likely a bundle; not verified) | EUR 39.00 |
| Side effects / how to use | none | none | how to use 10 mentions; side effects 1 |

**Why they outrank us:** (b) it is **not** content. Musinsa has 2 words in the HTML and medicube has 94, and both rank above a 425-word page. KD is 0, so this is a **product-feed and review-signal game**: Product schema with AggregateRating, price, availability. (a) medicube is a
recognised K-beauty brand with retail distribution; Musinsa is a large Korean marketplace. (c) A Shopping/"popular products" layer sits above the organics.
**What to change:** rating markup (as above), a US-geolocated price and currency check, and a one-line answer on the page to "What does glutathione serum do?" (PAA #1). A product-page edit is cheaper here than any content project, and it is the one term in this report where a
plain brand product page can realistically reach the top 3 within weeks. I cannot put a number on that; the SERP only says the bar is low.

### 4.7 "peptide serum" (US 3,129/mo, GB 1,418/mo, NL, KD 0)

**SERP today (US):**

| # | URL | Class |
|---|---|---|
| 1 | theordinary.com/en-us/multi-peptide-ha-serum-100613.html | BRAND (product) |
| 2 | photozyme.com/collections/best-peptide-serum | BRAND (collection with guide text) |
| 3 | forbes.com "The Best Peptide Serums That Smooth And Firm Skin" (2026-08-06) | EDITORIAL |
| 4 | clinicalskin.com/products/hyaluronic-acid-peptide-serum | BRAND (product) |
| 5 | colorescience.com/blogs/blog/what-is-peptide-serum | BRAND (blog) |
| 6 | timelessha.com/collections/peptides | BRAND (collection) |
| 7 | YouTube "Dermatologist: Do Peptide Serums Actually Work?" | UGC |
| 8 | dermstore.com/c/skin-care/treatments-serums/peptide/ | RETAILER (category) |

No AIO. Features: forums, images, PAA, popular products, product considerations.

| Factor | The Ordinary #1 | Photozyme #2 | Forbes #3 | Clinical Skin #4 | Colorescience #5 | Timeless #6 | **Ours: /collections/serums** |
|---|---|---|---|---|---|---|---|
| Type | Product | Collection plus guide | Listicle | Product | Blog | Collection | Collection |
| Title | "Multi-Peptide + HA Anti-Aging Serum" | "Best Peptide Serum: How To Choose And Use One" | "The Best Peptide Serums That Smooth And Firm Skin" | "Hyaluronic Acid + Peptide Serum" | "What is Peptide Serum & Why Should You Use It?" | "Peptide Serums & Sprays" | "Peptide Serums: Copper Peptide, PDRN, Matrixyl and More" |
| Words | 572 | 359 | **not measured** (403 to Chrome UA, Googlebot UA and WebFetch) | 93 | **1,799** | 90 | **53** |
| H2s | 6 question-style | 4 question-style | n/m | 8 | 6 question-style | 4 | 4 (stat labels, not questions) |
| Direct answer | n/a | Mid-page | n/m | no | yes | "Discover the building blocks of youthful skin" | **no intro text** |
| Studies linked | 0 | 2 | n/m | 0 | 1 | 0 | 0 |
| Tables | 1 | 0 | n/m | 0 | 0 | 0 | 0 |
| FAQ | **FAQPage 5 Q&A** | yes | n/m | yes | no | yes | no |
| Reviewer | none | none | n/m | none | Person (author) | none | none |
| JSON-LD | Product, Offer, FAQPage | Organization, **AggregateRating**, Brand | n/m | Product, Offer | Article, Person | **CollectionPage, Product x16, AggregateRating x16**, ItemList | BreadcrumbList only. **No CollectionPage, ItemList or Product** |
| Products and prices | $19.90 | $25-$50 | n/m | $90-$250 | $99-$179 | $20.95-$27.95+ | 6 products, EUR 39-69 |
| Concentration | 1% | n/m | n/m | none | none | none | 1% and 2% in product names |

**Why they outrank us:**

- **(a) Authority/brand.** The Ordinary's Multi-Peptide + HA is a best-seller with massive brand search. Forbes is Forbes.
- **(b) Content.** Not what decides it. Timeless ranks #6 with **90 words** and Clinical Skin #4 with **93**. What they have that we do not is **Product/ItemList/AggregateRating schema** on the collection and a title that is exactly the query ("Peptide Serums & Sprays"). Our
  collection title is longer and lists three ingredients before the term "peptide serum" stops being the lead; our page has 53 words and no machine-readable list of products.
- **(c) SERP features.** Popular-products and forums layers. No AIO.
- **(d) Technical.** The collection lacks CollectionPage and ItemList schema (measured: BreadcrumbList only).

**Can a brand page realistically win "peptide serum"?** Yes for the lower top-10 and conceivably top 5: **five of the top 8 US results (The Ordinary, Photozyme, Clinical Skin, Colorescience, Timeless) are brand-owned pages**, and several have fewer than 400 words. KD is 0. I
would not promise #1: The Ordinary's product page is the entrenched winner. **But a collection page like Timeless's is the right shape and we have the right inventory (6 serums).** The Forbes slot is a separate, off-page job (see §6).

**GB and NL are easier.** GB top 9: Boots (The Ordinary), Alpha-H product, Forbes, The Ordinary, Glamour UK, Superdrug, Hydropeptide blog, Elle UK, Cosmopolitan UK. NL top 8: Alpha-H NL (x2), ICI Paris XL (x2), koreanskincare.nl, Vogue NL, Lyko, Qandaskin. In NL the brand pages
are product pages with 321,000-byte HTML and almost no unique copy (Alpha-H NL: 749 words). Dutch editorial is Vogue NL (485 words, 2024) and Lyko (822 words). The Dutch SERP is thin, and the Netherlands is our home market, but the demand is small (3% of opportunity per the
strategy), so the effort should follow demand.

**What our collection must change:** (1) retitle to lead with the query ("Peptide Serums" first), (2) add a 150-250-word intro that answers "What does a peptide serum do?" and "Which is better, peptide or retinol?" in two sentences each (those are the PAA questions), (3) add
CollectionPage and ItemList schema with Product entries for each serum, (4) show ratings on the cards once the review markup exists, (5) add an FAQ block. Medik8's peptides collection is the model: 172 words, CollectionPage plus ItemList plus Product x9 plus FAQPage, and it is
**#1 for "peptide skincare"** and an AIO citation.

### 4.8 "peptide skincare" (US 100/mo, KD 9)

**SERP today (US):** #1 Medik8 US collection; #2 Dermstore ingredient page; #3 PMC11762834 (review "Peptides: Emerging Candidates for the Prevention and Treatment of Skin Senescence", 16,753 words, 346 links); #4 Vogue "How the Best Peptides Skin Care Can Deliver Botox-Like
Results" (3,141 words, Iman Balagam, modified 2026-05-27); #5 IMAGE Skincare collection; #6 The Ordinary guide "What are Peptides and What do They do for Skin?"; #7 ZO Skin Health. **Top 3 legitimate:** Medik8, Dermstore, PMC. **AIO cites:** Medik8 collection, Cleveland Clinic,
AdventHealth, CeraVe, two YouTube videos. **PAA:** What do peptides do in skincare? / What are the top 5 peptides? / Is there a downside to using peptides? / Do dermatologists recommend peptides?

| Factor | Medik8 #1 | Dermstore #2 | PMC review #3 | Cleveland Clinic (AIO) | **Ours: /collections/serums** |
|---|---|---|---|---|---|
| Type | Collection | Category | Journal review | Health system article | Collection |
| Words | 172 | 358 | 16,753 | 1,120 | 53 |
| JSON-LD | CollectionPage, ItemList, Product x9, FAQPage x7 | CollectionPage | none | Article, MedicalOrganization, Person | none useful |
| Studies linked | 0 | 0 | 346 | 1 | 0 |
| Author | none | none | academic | "Cleveland Clinic" | none |
| Side effects / downsides | n/m | 0 | 16 | 1 | 0 |

**Why they outrank us:** the volume is small (100/mo), so this is a supporting term, not a growth term. The same fix as §4.7 applies, and the same page can serve both ("peptide serum" and "peptide skincare" are different phrases but have the same intent in practice). **Do not
make a second page for this term** (the strategy's own rule: one page per keyword and intent).

### 4.9 "collagen cream" (US; not in the strategy's hero list)

**SERP today (US):** #1 Reddit r/koreanskincare; #2 Sweetcare (Medicube Collagen Lifting cream; **could not be measured**, Cloudflare returns 403); #3 a Facebook post; #4 Reddit r/BeautyDE; #5 DoorDash; #6 a Cancer Research UK forum thread; #7 Boutiqaat; #8 Temu. **No brand-owned
editorial, no AIO.** PAA: What is the most effective collagen cream? / Do collagen creams actually work? / Is it okay to use collagen cream every day? / Which is better for older skin, collagen or retinol?

This is the weakest SERP in the set (forums, marketplaces, a food-delivery app) and the easiest to enter on paper. But the strategy assigns our collagen product to "pdrn cream" (the PDRN Collagen Night Cream), and "collagen cream" is a different intent ("do collagen creams work":
a topical collagen molecule is too large to absorb, a point a reviewed explainer could make honestly). I have no page of ours measured for this term. **Not recommended as a priority;** add it as a PAA-answer section on the PDRN or Matrixyl pages if wanted.

### 4.10 "skincare clinical studies" (US)

**SERP today (US):** #1 drmarnie.com/pages/clinical-results; #2 halecosmeceuticals.com blog "Essential Guide to Medical Grade Skincare Evaluation"; #3 curf.clemson.edu (genuine, see §2); #4 jddonline.com review "Over-the-Counter Topical Skincare Products: A Review of the
Literature"; #5 ResearchGate; #6 an Instagram reel; #7 freshaestheticsspa.com; #8 Medscape on X. **AIO cites:** skincareresearch.org/study-participants, citruslabs.com/skincare, centerwatch.com, denovaresearch.com, essextesting.com, discc.com, unionderm.com. **All seven AIO
references are clinical-trial *recruitment* or contract-testing sites.** The intent is, in large part, "I want to take part in a skincare clinical study", not "show me the studies behind products". PAA: What is the 4 2 4 rule in skincare? / What is the #1 skincare in the world? /
What is the #1 cause of skin aging? / Which skincare brands are clinically tested and proven?

| Factor | Dr. Marnie #1 | Hale #2 | Clemson #3 | **Ours: /blogs/clinical-studies** |
|---|---|---|---|---|
| Type | Brand "clinical results" page | Brand blog | University news | Study index (Shopify blog) |
| Title | "Clinical Results - DR. MARNIE Skincare Studies & Outcomes" | "Essential Guide to Medical Grade Skincare Evaluation" | "Clemson, Experts Create Breakthrough Anti-Aging Skincare Line - CURF" | "Skincare Clinical Studies, Read in Full \| Skingenetix" |
| Words | 98 | 799 | 637 | 421 |
| H2s | 7 | 9 | 3 | 2 ("Before you try it", "Studies by ingredient") |
| JSON-LD | OnlineStore, **FAQPage with 29 Q&A** | none | Article, Person, ImageObject | BreadcrumbList only |
| Studies linked | 0 | 0 | 0 | 0 on the index (they are on each study page) |
| Percentages | 100%, 97% | none | none | 0.1% to 23% (study results) |

**Why they outrank us:** (a) Dr. Marnie is a recognised brand with press and third-party sales data behind its claims, and the page carries 29 FAQ entries in schema. (b) Hale and Clemson answer a different question ("what is medical-grade", "who is doing the research"). (d) Our
page is a Shopify blog index with no ItemList or CollectionPage markup.
**What to change:** add `ItemList` schema for the studies; add a plain-English "How we read a skincare study" explainer (grades A to D already exist in our hub tables: re-use them); answer "Which skincare brands are clinically tested and proven?" in a single quotable paragraph at
the top; link out to the PubMed record for each study from the index. The title already matches the query. **Be aware that intent is split;** the trial-recruitment intent is not ours to serve.

### 4.11 "copper peptide serum" (GB, 1,339/mo, KD 3)

**SERP today (GB):** #1 Amazon UK search page; #2 Cult Beauty (The Ordinary Multi-Peptide + Copper Peptides 1%); #3 Filler Direct (a professional microneedling-supplies shop); #4 Face the Future (The Ordinary); **#5 stonevillenc.org (SPAM, in GB too)**; #6 Beauty Outlet
(Revolution Skincare copper peptide serum); #7 Space NK (The Ordinary); #8 eBay UK. **AIO cites:** Niche Beauty Lab, Boots (The Ordinary), Innerbody, YouTube, Byrdie, Sephora UK, Instagram.

The GB SERP is a **retail-of-The-Ordinary** SERP. Cult Beauty (measured): 376 words, Product + Offer + **AggregateRating + 10 Review items**, price £13.50 (from £28.90 shown as list), FAQ. Filler Direct (measured): 66 words, Product + Offer, £23.99 ex VAT. Neither has an author, studies or tables.

**Why they outrank us:** retail distribution plus review schema. We have the evidence advantage and a 2% concentration; we lack ratings markup and GB retail presence. A page targeting this term in GB needs: GBP price visible, UK shipping and returns, rating markup, and a clear
comparison of 2% against The Ordinary's 1%. I did not fetch the live Space NK/Beauty Outlet pages (retailer listings, not comparable on content).

### 4.12 "peptide serum" (GB) and "glutathione for skin" (GB)

- **"peptide serum" GB:** covered in §4.7 (Boots, Alpha-H, Forbes, Glamour UK 3,147 words and modified 2026-05-15, Superdrug, Hydropeptide, Elle UK, Cosmopolitan UK). Boots could not be fetched (bot-protection page "Pardon Our Interruption"). Alpha-H product page (measured): 379
  words, Product + Offer, "Rated 4.7 out of 5 stars, 92 Reviews", FAQ section, 6-week trial of 26 participants quoted on the page.
- **"glutathione for skin" GB:** covered in §4.5. The most useful structural finding: **Skinsider's retailer ingredient page is #2** with 474 words, question H2s, FAQ and a product list. It has no studies and no author. A brand ingredient hub with real trials should beat it; it
  is cited in the AIO, which is the page type that gets the AIO slot.

### 4.13 "kupferpeptid serum" (DE)

**SERP today:** only 5 organic rows: #1 Amazon.de "Copper Peptide Gesichtsserum, GHK-Cu Peptide Serum"; #2 Etsy listing "Kupferpeptid-Gesichtsserum 2 %, GHK-Cu (600 mg)"; #3 Temu; #4 Reddit r/SkincareAddiction (German-language thread); #5 Cosibella DE (Nacomi Copper Peptide
0.5%). No AIO. PAA (German): Was bringt Kupferpeptid? / Was ist besser, Retinol oder Kupferpeptide? / Welches ist das beste Peptid für die Haut? / Ist GHK-Cu ein wirksames Mittel gegen Haarausfall? Cosibella (measured): 516 words, Product + Offer + Brand schema, 0.5%
concentration, no studies, no author. **This is the thinnest SERP in the set.** An editorial or brand page in German with a stated 2% and PubMed links would stand out. The existing `de` locale is live. German demand is 634/mo for the term (from the strategy). **I did not measure
our German product page;** the brief said the `de` locale is published, so verify it is fully translated before building on it (the repo memory records an English rewrite that went live untranslated on five locales).

---

## 5. Why-they-outrank-us summary across the 15 terms

| Cause | Where it decides | Evidence |
|---|---|---|
| **Domain authority and brand demand** | copper peptide (AIO), best copper peptide serum, glutathione for skin, peptide serum, peptide skincare | NPR, Wikipedia, Forbes, Healthline, Innerbody, PMC, Paula's Choice, The Ordinary, Medik8 hold the AIO and the top 4 slots. We have 627 referring domains with spam score 52, rank 0, and no genuine one. |
| **Machine-readable commerce signals (ratings, price, collection lists)** | copper peptide serum, glutathione serum, peptide serum, peptide skincare | AggregateRating on Remedy, Cult Beauty, Timeless x16, medicube, Musinsa; ItemList/Product on Medik8, Timeless. Ours: none on products or collections. |
| **Answering the PAA safety/layering questions** | copper peptide, glutathione for skin, copper peptide serum | Every AIO-cited glutathione page has a side-effects section; Healthline and Innerbody have one for copper; both of our hubs have none. |
| **Roundup inclusion (Forbes, Innerbody, Glamour, Vogue)** | best copper peptide serum, peptide serum, copper peptide serum (AIO) | Innerbody and Forbes are both in the AIO and in the top 4. We are in neither. |
| **Forums and video** | copper peptide serum, glutathione for skin, glutathione serum, collagen cream | Reddit holds #1 or #2 in four of these SERPs; YouTube is in the top 8 of four. |
| **Indexing/technical on our side** | none found | Both hubs and both product pages return 200 with canonical and 7 hreflang tags. I did not find a blocker. |

---

## 6. What we must change, ranked by impact against effort

### On-page (our site)

| # | Action | Page | Why | Effort |
|---|---|---|---|---|
| 1 | **Add Review/AggregateRating schema from genuine reviews** | both product pages | Competitors at the top of the product SERPs all expose ratings. Ours are invisible to machines. | Medium: needs the reviews as server-side data |
| 2 | **Add "Side effects, patch test, who should avoid it" and "Oral vs topical vs injection"** with sources | glutathione hub; copper hub | Every AIO-cited glutathione page has it; NPR frames the copper AIO around injections | Low: copy, reviewed by Dr Bodde |
| 3 | **Answer "what not to mix with copper peptides" and "how to layer" as H2s with a 2-sentence answer first** | copper hub and copper product page | It is PAA #1 and #4 for "copper peptide" and #2 for "copper peptide serum". **Check the formulation first:** our serum contains vitamin C. | Low, but needs a formulation owner's answer |
| 4 | **Rebuild /collections/serums:** retitle, 150-250 words of intro, FAQ, CollectionPage + ItemList + Product schema | /collections/serums | Timeless and Clinical Skin rank #6 and #4 for "peptide serum" with 90 and 93 words, because of schema and title match | Medium |
| 5 | Add `ItemList` schema and an explainer to the clinical-studies index | /blogs/clinical-studies | Dr Marnie #1 carries FAQPage with 29 questions | Low |
| 6 | Write one honest "best copper peptide serum" guide with a comparison table of disclosed concentrations | new article | them-ethod ranks #6 with 1,360 words and no studies; Innerbody grades concentration disclosure | Medium |
| 7 | Confirm US currency and price on product schema | both product pages | See §8 | Low |
| 8 | German product page check | /de/products/... | Thinnest SERP in the set | Low |

### Off-page (this is where the biggest gap is)

1. **Roundup outreach, in this order:** Innerbody (the "best copper peptide serum" page was updated 2026-09-03 and is the AIO's source for "copper peptide serum"; send a sample and a one-page concentration sheet, since the page grades disclosure), then the Forbes Personal Shopper
   author who wrote the 2026-08-06 "Best Peptide Serums" piece, then Glamour UK (modified 2026-05-15) and Vogue (modified 2026-05-27). A listing in these pages is worth more than anything we can write on our own site. I cannot estimate the traffic; the data I have does not
   support a number.
2. **Earned links to the two hubs:** a dermatology or clinical-trial site that cites the Badenhorst (copper) or Watanabe (glutathione) trial is the natural source. One genuine referring domain would be the first the site has. Do not buy links; the existing 627 are already a signal of link spam.
3. **Reddit and YouTube presence:** Reddit holds a top-2 slot in four of these SERPs and is cited in the AIO. A disclosed brand account answering copper-peptide and layering questions on r/SkincareAddictionLux is allowed by Reddit's rules only if disclosed. I did not check subreddit-specific rules.
4. **Clean the link profile:** the spam backlinks (`dofollowbacklinksgenerator.site` appeared today) are a candidate for a Search Console disavow file. This is a judgement call; Google says it generally ignores such links, so do not spend a lot of time on it.
5. **Report the hijacked sites** (stonevillenc.org, reuniontower.com) to Google. It costs nothing and the SERP clears faster.

### Which terms to prioritise

1. **"glutathione serum" (US 555, KD 0):** a product-feed game that a clean product page can win; do items 1 and 7 first.
2. **"copper peptide serum" (US 2,977, GB 1,339, KD 3):** items 1, 3, then roundup outreach.
3. **"peptide serum" (US 3,129, GB 1,418, KD 0):** item 4 (collection rebuild); realistic for the top 8, not #1.
4. **"glutathione for skin" (US 1,211, GB 472, KD 29):** item 2 and one external link.
5. **"copper peptide" (US 1,362, KD 9):** item 2 and item 3. A spam clean-up will reshuffle the SERP.
6. **"ghk-cu", "collagen cream":** do not chase.

---

## 7. What I could not measure, and why

| Item | Reason |
|---|---|
| Forbes "Best Peptide Serums" page | 403 to Chrome UA, Googlebot UA and WebFetch (bot wall). Only the SERP title and URL date are known. |
| Paula's Choice glutathione page body | The HTML returned had 10 visible words (likely a bot-protection shell). I read its JSON-LD (author, reviewer, dates, 9 FAQ questions) but not the article text. |
| Boots (The Ordinary peptide serum) | Bot-protection page ("Pardon Our Interruption"). |
| Sweetcare (collagen cream #2) | Cloudflare challenge. |
| The Ordinary and NIOD category pages | Their H1 is a promo banner, and the JSON-LD is not in the HTML I received. Word counts (36 and 131) are real but small because the product grids load by script. |
| Musinsa listing | The page is JavaScript-rendered: 2 words in the server HTML. |
| Amazon listings | Fetched, but the star rating and review count are not in the HTML I parsed; I report only what the schema and text showed. |
| Domain authority, backlinks, brand search volume of competitors | Not available without a paid backlink API, which I was told not to run. All "authority" statements are qualitative and based on who the domains are, plus our own DataForSEO backlink file. |
| Where our pages rank today | The SERP pull is top-10 only. Our hub and product pages did not appear in any of the 15 top-10s I read. I did not re-run Search Console. |
| What real Googlebot sees on stonevillenc.org | Googlebot is IP-verified; a spoofed UA does not reproduce it. |
| US view of our product pages | My fetches came from an EU location and show EUR prices. |
| Traffic estimates for any recommendation | Not given. No click-through-rate or share-of-voice data was available, and I have not invented any. |

## 8. Caveats on our own data

- **Currency.** Both product pages' schema says `priceCurrency: EUR`, price 49.00 and 39.00. This was fetched from an EU location. For a US shopper Shopify may serve USD, but I did not verify it. If the US schema also says EUR, the Google Shopping and rich-result signals for the
  US market are weakened; check this with a US-geolocated fetch before relying on it.
- **Review honesty.** The product pages show "Verified Customer" before/after photos. They are not marked up. Only mark up reviews that are real and attributable.
- **Evidence dating.** The hub pages carry "last reviewed 25 and 26 September 2026". Competitor dates come from their own schema and may be stale (Healthline's schema says 2020-10-26, but the page may display a later date).

## Sources

- SERP data: `scratchpad/serps-2026-10-07.json` (DataForSEO `serp/google/organic/live/advanced`, desktop, pulled 2026-10-07)
- Demand: `docs/keyword-strategy-2026.md`
- Backlinks: `scratchpad/backlinks-skingenetix.json`, `scratchpad/refdomains-skingenetix.json` (DataForSEO, pulled 2026-10-07)
- Page fetches (all 2026-10-07): npr.org/2026/09/07/nx-s1-5955552/copper-peptides-skin-aging-health-safe; en.wikipedia.org/wiki/Copper_peptide_GHK-Cu; theordinary.com/en-us/category/skincare/shop-by-ingredients/copper-peptides;
  niod.com/en-us/categories/skincare/shop-by-ingredients/copper-peptides; healthline.com/health/copper-peptides; remedyskin.com/products/copper-peptide-firming-serum-ghkcu; dermaestheticsusa.com/products/copper-serum; peachandlily.com/products/copper-peptide-pro-firming-serum;
  innerbody.com/best-copper-peptide-serum; them-ethod.com/blogs/journal/best-copper-peptide-serum; paulaschoice.com/expert-advice/skincare-advice/ingredient-spotlight/glutathione-for-skin.html; westlakedermatology.com/blog/glutathione-skincare-ingredient-focus/;
  pmc.ncbi.nlm.nih.gov/articles/PMC11862975/; pmc.ncbi.nlm.nih.gov/articles/PMC11762834/; vibrantskin.com/blogs/skincare/glutathione-for-skin; cosmoderma.org/glutathione-in-dermatology-a-bright-future-or-fading-hype/; skinsider.co.uk/skin-care/ingredients/glutathione/;
  medicube.us/en-de/products/subscr-age-r-glutathione-glow-serum; global.musinsa.com/us/products/5833052; theordinary.com/en-us/multi-peptide-ha-serum-100613.html; photozyme.com/collections/best-peptide-serum; timelessha.com/collections/peptides;
  us.medik8.com/collections/peptides; dermstore.com/c/ingredient/peptides/; health.clevelandclinic.org/peptides-for-skin; vogue.com/article/best-peptide-skincare; drmarnie.com/pages/clinical-results; halecosmeceuticals.com/blog/medical-grade-skincare-evaluation;
  curf.clemson.edu/clemson-university-researchers-and-skincare-experts-partner-to-create-breakthrough-anti-aging-skincare-line/; cultbeauty.co.uk/p/the-ordinary-multi-peptide-copper-peptides-1-serum-30ml/14853143/; filler-direct.co.uk/product/copper-peptide-serum-1-x-5ml/;
  uk.alpha-h.com/products/multi-peptide-revitalise-serum; glamourmagazine.co.uk/gallery/best-peptide-serums; clnq.com/blog/glutathione-the-secret-of-skin-health/; cosibella.com.de/de/products/nacomi-25565; alpha-h.nl/products/multi-peptide-revitalise-serum-30ml;
  vogue.nl/beauty/skincare/beste-peptide-serums-huid/; lyko.com/nl/magazine/reviews/beste-peptideserums-huidverzorging; colorescience.com/blogs/blog/what-is-peptide-serum; clinicalskin.com/products/hyaluronic-acid-peptide-serum;
  hydropeptide.co.uk/blogs/skincare-routines/what-are-peptide-serums; amazon.com/clp/B00I3OW1M0; amazon.com/dp/B0D1LLWZBG
- Our pages: `scratchpad/own_pages_copper-peptide-research.html`, `own_products_copper-peptide-ghk-cu-renewal-serum.html`, `own_pages_glutathione-research.html`, plus one fetch each of `/products/glutathione-brightening-serum`, `/collections/serums`, `/blogs/clinical-studies` (3
  fetches of our site in total)
- Spam probes: stonevillenc.org, reuniontower.com, com.ui.edu.ng, essentialdayspa.com (Chrome UA and Googlebot UA, curl)
