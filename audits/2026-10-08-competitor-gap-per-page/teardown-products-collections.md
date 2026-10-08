# Products and collections: competitor teardown (2026-10-08)

Scope: 18 keyword/market pairs across 5 product pages, 6 collections and the Collagen rebuild. Labels: VERIFIED (read in primary data), PLAUSIBLE, NOT ESTABLISHED.

Tags: [SJ] serp/serp.json (desktop top 10, 2026-10-08) · [PG] serp/pages.json · [PT] data/page-table.json (Search Console 28 days, all locales) · [VOL] data/volumes.json (clickstream observed; Ads bucketed) · [AUTH] serp/authority.json · [RPT] serp/report.md · [OWN] our pages, curl today ·
[WF] competitor pages, WebFetch today · [GSC7] yesterday's query-by-page export · [REG] docs/claims · [KS] docs/keyword-strategy-2026.md.

## 1. Findings

1. **Seventeen of the 18 SERPs show a product carousel; only 6 show an AI Overview** [SJ]. For buying terms the shop feed outweighs Overview citations. Free-listing feed URLs already appear in Search Console (`utm_medium=product_sync`, `currency=USD/GBP`) [GSC7], so the feed exists. It
   lacks rating and attribute depth (plan B.5).
2. **Three of our collection assignments cannot be won by a collection.** "peptide moisturizer", "microneedling serum" and DE "peptide hautpflege" are guide-and-forum SERPs with no retailer collection in the top 8 [SJ] [PG]. "peptide cream" is Amazon search plus category pages plus listicles.
3. **Rating markup is a tie-breaker, not the gate.** Only 8 of 75 measured top pages carry `AggregateRating`; 19 carry `Product` [PG]. Face the Future ranks #3 for GB "pdrn skincare" without ratings [WF].
4. **Our Kaufland listing, "Skingenetix Glutathion-Serum 2%", is #7 for DE "glutathion serum"; our store page is absent** [SJ]. The docs record Kaufland orders, so it is ours (PLAUSIBLE; fetch blocked). Our store title says "Glutathione" [OWN].
5. **Live defects.** The creams collection says "Coming soon." above five live products; both stamp sets are "Sold out" with `OutOfStock` schema; collections carry `BreadcrumbList` only [OWN].
6. **Spam holds slots.** Hacked domains hold 4 of 8 on "copper peptide skincare" and 2 of 8 on "peptide moisturizer"; joybuy.de (suspected cloaking) holds 5 of 6 on DE "peptid serum" [SJ] [RPT].

## 2. Method and limits

One desktop snapshot; mobile can differ. Boots, Dermstore, Lancome, Next block fetches (used [PG]). Read directly: Watts, Neova, Face the Future, Cosibella, Nurse Jamie [WF]; Kaufland gave 403. Our authority count (701) is almost all link-generator spam [AUTH]. Clickstream undercounts; Ads
buckets are direction only. DE clicks cannot be isolated in [PT].

## 3. Where we stand

| Page | Words | Schema | Search Console 28d [PT] |
|---|---|---|---|
| Matrixyl cream | 336 | Product, FAQ | 130 imp, 2 clicks; "matrixyl 3000" pos 5.6 [GSC7] |
| Copper night cream | 366 | Product, FAQ | 126 imp, 1 click |
| Copper day gel-cream | not in [PG] | Product, FAQ | 31 imp, 2 clicks |
| PDRN cream | 417 | Product, FAQ | 102 imp, 1 click; "pdrn night cream" pos 7.7 [GSC7] |
| DE glutathione serum | 485 | Product, FAQ | EN page 235 imp, 6 clicks |
| Collections: copper / creams / microneedling / pdrn | 52 / 45 / 37 / 38 | Breadcrumb only | 149 imp (2 clicks) / 0 / 0 / 19 imp, pos 11.5 |
| DE serums / DE all | 45 / 72 | Breadcrumb only | EN serums 62 imp, pos 49 |

## 4. Term by term

Shared product-page changes (not repeated; schema today has EUR price and GTIN only [OWN]): rating markup from genuine reviews; Merchant Center ratings plus `product_detail` and `product_highlight`; shipping and returns markup; USD and GBP price check (my fetch showed EUR; US view NOT ESTABLISHED).

### 4.1 "peptide cream" (US 453, GB 395 clickstream; Ads 2,400 / 1,000) [VOL] → Matrixyl cream

| | |
|---|---|
| Us | Not in top 10 either market; no query for it in Search Console |
| Page one US | Amazon search, Dermstore category, GWU listicle, No7 collection, Allure, Drunk Elephant product, CeraVe, Reddit. No Overview [SJ] |
| Page one GB | Amazon x3, Next, eBay, JD Williams, Reddit, forum, LinkedIn. No Overview |
| Top 3 vs ours | Amazon search; Dermstore 358 words, 8 H2, `CollectionPage`; GWU 80 words, 11 H2 [PG]. Ours: 336 words, product page |

**Why they win:** a category SERP. Two of the top four US results are category pages and one is a marketplace search; GB is retailer and marketplace listings. One product page cannot answer a generic query.
**Verdict: not winnable by the Matrixyl cream.** Move "peptide cream", "peptide creams", "peptide face cream" to `/collections/creams-moisturizers` (rebuilt, 4.6). The cream keeps "matrixyl cream" and "collagen cream with matrixyl" (positions 21 to 29 already [GSC7]). **Changes to the
cream:** (1) title "Matrixyl 3000 Cream with Collagen, 50 ml" (avoids bare "collagen cream", which the Collagen page owns); (2) first line names the two peptides, palmitoyl tripeptide-1 and tetrapeptide-7, never pentapeptide-4 [REG]; (3) Matrixyl 3000 concentration if the formulator will
give it; (4) link to the hub and the serum. **Target:** "matrixyl cream" page one in 3 months; collection on "peptide cream" US page 10 in 9 to 12 months, GB 12.

### 4.2 "ghk-cu cream" (US 805, GB 158) and "copper peptide cream" (US 201, GB 79; Ads 880) [VOL] → decision

| | |
|---|---|
| Us | Not in top 10; night cream 126 imp, day cream 31 imp |
| Page one | ghk-cu cream: The Ordinary glossary, Reddit, Watts product, eBay, Glimmer Goddess, FormulateRx, Skin Biology, Joi & Blokes. Copper peptide cream: eBay, Vitali, Byrdie, Amazon, Healthline, Glimmer Goddess, FormulateRx [SJ] |
| Overview | ghk-cu: Yahoo (AgelessRx launch), Google Shopping cards, PMC, Allure. Copper cream: Neova collection, Neuroganhealth product, Allure |
| Top 3 vs ours | Ordinary 131 words; Watts 407 words, 12 H2, `AggregateRating`, no concentration stated [WF]. Ours 366 words, "2%" in title |

**Why they win:** same SERP for both terms (Glimmer Goddess and FormulateRx appear in both), so one page should own both. Five small shops (137 to 646 words; 88 to 1,739 referring domains [AUTH]) hold ranks 3 to 8, so authority is not the wall.
**Decision: the night cream owns both terms; the day gel-cream owns neither.** The night cream has no vitamin C; the day cream contains 3-O-ethyl ascorbic acid [OWN], and "what not to mix copper peptides with" is a People Also Ask on this SERP [SJ raw]. Making the vitamin C cream the head
page invites that question first. No query data supports a day/night split (0 clickstream) [VOL]. **Night cream changes:** (1) title "Copper Peptide Cream 2% GHK-Cu, Night Cream" (today "Night" splits the phrase "copper peptide cream"); (2) first line "A rich 50 ml copper peptide cream
with 2% GHK-Cu"; add the INCI name (Copper Tripeptide-1, check `/pages/ingredients`); (3) section "Which copper peptide cream: night or day?" linking sideways, and "Can I use it with vitamin C?" answered by the formulation owner, not me; (4) 2% is the formula's strength, never "the studied
dose" [REG]. Day cream: anchor text "copper peptide day gel-cream" only. **Target:** "ghk-cu cream" page one in 4 to 6 months, top 5 in 12; "copper peptide cream" page one in 6 to 9.

### 4.3 "pdrn cream" (US 2,416 / GB 1,108 / DE "pdrn creme" 104 clickstream) [VOL] → PDRN night cream

| | |
|---|---|
| Us | Not in top 10; "pdrn night cream" pos 7.7, "pdrn kollagen" pos 1 [GSC7] |
| Page one US | Reddit x2, Bronze (VT cream, 167 words), Skinsort, Juliette Armand (273 words), QVC thread [SJ] [PG] |
| Page one GB | Glamtouch product (398 words), Skin2Seoul, ASOS guide, Superdrug, koreanpdrn guide, INKEY guide |
| Page one DE | kbeautyhouse (1,053 words), koreanbeauty.de (2,638), Amazon, Little Wonderland, Medicube product at #6 |
| Overview (US) | Clinique PDRN cream product page, Reddit, YouTube, Soko Glam (VT cream), Anua cream, Instagram |

**Why they win:** named PDRN cream product pages win and get cited (Clinique, Soko Glam, Anua), and 167 to 398-word pages on domains with 99 to 773 referring domains hold slots [AUTH]. Reddit holds two US slots.
**Winnable: yes, the best product-page odds here.** Our title already matches ("PDRN Cream 1% with Salmon DNA"; DE "PDRN Creme 1% mit Lachs-DNA") [OWN]. **Changes:** (1) first line "PDRN cream with 1% PDRN (sodium DNA) and hydrolyzed collagen, 50 ml"; (2) FAQ rewritten around the PAA:
"What not to mix with PDRN cream?" (answer: no data, patch test), "Is PDRN salmon sperm?" (plain origin answer from the PDRN register), "When to put PDRN cream on?", plus the fish-allergy line [SJ raw] [REG]; (3) link from the PDRN hub and `/collections/pdrn`; (4) the page's "up to 23%"
result is from a 0.1% eye cream in Ye 2026 [OWN]; see Q3. **Target:** page one US in 6 to 9 months, GB 6 to 9, DE 3 to 6.

### 4.4 "glutathion serum" (DE 208; Ads 260) [VOL] → `/de/products/glutathione-brightening-serum`

| | |
|---|---|
| Us | Store page not in top 10; Kaufland listing #7 [SJ] |
| Page one | Shop Apotheke and Amazon.de (each twice, same URL), koreanbeauty.de #5 (`AggregateRating`), Medicube DE, Kaufland, Ankorstore, iHerb |
| Top 3 vs ours | Two marketplace listings, no pages to measure. koreanbeauty.de 364 words; ours 485, FAQ and `Product` schema [PG] |

**Why they win:** pharmacy and marketplace listings with the German word in the name; about 8 unique results; no Overview.
**Winnable: yes, page one in 3 months.** **Changes:** (1) title "Glutathion Serum 2% mit Vitamin C & Niacinamid" (was "Glutathione Serum 2% mit Vitamin C") [OWN]; (2) first line uses "Glutathion" once, "Glutathione" as the product name (PAA uses both spellings: "Was macht Glutathione mit
der Haut?"); (3) keep "heller wirkende", never "whitening" [REG]; (4) answer the PAA "Welche Nebenwirkungen hat Glutathion?" with the register's limits; (5) mirror the Kaufland listing's wording and link the two. **Target:** two slots (store plus Kaufland) on page one in 3 months; top 3 in
6.

### 4.5 "copper peptide skincare" (US Ads 720, no observed volume) → `/collections/copper-peptide`

| | |
|---|---|
| Us | Not in top 10; "buy copper peptides" pos 44 on this page [GSC7] |
| Page one | Stoneville spam x3, skincarecompany guide (1,048 words), Amazon (Biossance), Reddit x2 [SJ] |
| Overview | Neova collection, Reddit, Vogue, Art of Skincare |
| Neova's shape | 52-word intro, 16 products, star ratings on cards, 4-question FAQ, an "about" block [WF] |

**Why they win:** half the slots are hacked-domain spam that should fall away; the Overview cites a collection with ratings and an FAQ. Ours is 52 words with a meta description led by "55.8%" [OWN].
**Winnable: yes, once the spam clears.** **Changes:** (1) 200-word explainer in the collection description field (what GHK-Cu is, 2% in each product, which cream or serum for which skin, link to the hub); (2) FAQ from the PAA (downsides, what not to mix, how often); (3) card ratings; (4)
`CollectionPage` + `ItemList`; (5) meta description without the in-vivo figure (Q3). **Target:** page one 4 to 6 months; "buy copper peptides" variants move with it.

### 4.6 "peptide moisturizer" (US 553, GB 475; Ads 3,600) → creams collection: **no**

Page one: Editorialist listicle, Reddit, Stoneville spam, Stylecaster, QVC thread, a store blog (2,726 words), Sephora forum [SJ] [PG]. No Overview, no retailer: a collection is the wrong page type. **Verdict:** write one spoke, "How to choose a peptide moisturizer" (what to look for, dry
versus oily, how to layer, our creams as examples), as owner; page one in 6 to 9 months. The collection takes "peptide cream(s)" (4.1). **Collection changes now:** delete "Coming soon." and replace with a 200-word explainer naming the five products; title "Peptide Cream: Copper Peptide,
PDRN & Matrixyl Creams"; FAQ from PAA ("What does peptide cream do?", "downsides of topical peptides?") [SJ raw]; schema as 4.5.

### 4.7 "microneedling stamp" (US 805, GB 158) and "microneedling serum" (US 402, GB 237; Ads 5,400) → `/collections/microneedling`

Stamp page one: Nurse Jamie product (270 words, 23 reviews, safety list) [WF], Skinmedix product (334), DrPen how-to (943), Amazon x2, YouTube [SJ] [PG]. Serum page one: Reddit x2, clinics, a Q&A site, a 2,396-word blog. No collection in either.
**Stamp: product-led, not yet winnable.** Both sets are sold out [OWN], so no Shopping. If pre-order, set `PreOrder` plus a date in schema and feed. A two-product collection is the wrong page type: let the copper set's product page carry "microneedling stamp", adding usage, frequency, who
should not use it and an FAQ. Its "absorb deeper" echoes a penetration claim the copper register warns about (Q4). **Serum: drop it.** It is advice-seeking; write nothing until stock exists and a formulator confirms the vials suit needled skin. **Target:** stamp page one 6 to 9 months
after restock; serum none.

### 4.8 GB "pdrn skincare" (1,182) [PT] → `/collections/pdrn`

Today's page one has no Boots or Cult Beauty collection: Tira and Get The Gloss editorial, **Face the Future collection #3**, Allure, Amazon, Stylist, Notino ingredient page, two blogs [SJ]. Boots appears only in the Overview, through its "what is PDRN" explainer, with YouTube and a blog.
(Boots ranked #1 for "pdrn serum" yesterday; this term differs.) Face the Future: 60-word intro, 34 products, no ratings, no FAQ [WF]; domain 1,532 referring domains [AUTH]. Ours: 3 products, 38 words, GSC pos 11.5 [PT].
**Winnable: yes at #3 to #8.** Changes: 200-word explainer (what PDRN is, serum or cream, 1%, link to hub), ratings on cards, FAQ from the GB PAA ("Where can I buy PDRN serums in the UK?", "How to use retinol and PDRN?"), schema, GBP pricing. Meta description claims "over twice as much as
retinol"; see Q3. **Target:** top 10 in 4 to 6 months.

### 4.9 DE "peptid serum" (104; Ads 3,600) → `/de/collections/serums`; "peptide hautpflege" (312) → `/de/collections/all`: **second one no**

Peptid serum: Joybuy x5 (suspected cloaked), Cosibella #3 (117 products, 54-word intro, no ratings) [SJ] [RPT] [WF]. Ours: title "Peptidseren - ...", 6 products, 45 words, English product names [OWN]. **Winnable: only one real rival; page one in 3 to 6 months.** Changes: title
"Peptid-Serum: Copper Peptide, PDRN, Matrixyl"; 200-word German explainer (via the translation package); FAQ from PAA ("Was ist besser, Retinol oder Peptide?"); German product names. Peptide hautpflege: Ricaud, Nivea.at, Colibri, Diadermine and Harper's Bazaar explainers; an information
SERP. **Reassign to `/de/pages/the-science`** (title already "Peptid-Hautpflege und die Forschung dahinter") [OWN]; page one in 6 to 9 months. `/de/collections/all` takes no peptide term.

### 4.10 Collagen: US "collagen serum" (553), GB "collagen cream" (554), DE "kollagen creme" (208) → Collagen Skincare page

| | Page one | Shape |
|---|---|---|
| US serum | Lumene product (740 words, ratings), Advanced Clinicals product, Clearstem explainer (1,332) | products plus one explainer; no Overview |
| GB cream | eBay, Notino, Laneche (144 words), Ninispa, Roman (99), Mumsnet, Clarins collection | thin product pages, median 144 words |
| DE | Lancome, Dr Spiller (453), Judith Williams (71), Fuersie test, Vichy explainer | brands plus one test; no Overview |

**Why they win:** thin commercial pages on mid authority; our 1,764-word, answer-first page [OWN] out-writes all of GB. **Winnable: US and GB in 6 to 9 months; DE after translation.** The preview still carries the old title ("Collagen Support and Skin Plumping"); the go-live title
"Collagen Cream & Serum: What Works on Skin" and the 301s make it eligible. Keep the "we make no collagen serum" line [REG]; it answers the US PAA "How does collagen face serum work?". DE title: "Kollagen Creme und Serum: Was wirkt".

## 5. Ranked actions (impact against effort)

| # | Action | Impact | Effort |
|---|---|---|---|
| 1 | Delete "Coming soon." on creams collection; write its explainer | High (every cream term) | 30 min |
| 2 | DE glutathione title and first line to "Glutathion"; link Kaufland | High (3-month page one) | 30 min |
| 3 | Rebuild 5 collections (copper, creams, pdrn, DE serums, microneedling) on the description field plus FAQ | High | 1 day each, plus translation |
| 4 | Night-cream title/first line/FAQ; Matrixyl-cream title; PDRN-cream FAQ | Medium-high | 2 hours |
| 5 | Merchant Center attributes, availability (`PreOrder`), USD/GBP price check | High (17 of 18 SERPs have a carousel) | 1 day |
| 6 | Reviews into server-side rating markup | Medium | 2 to 3 days |
| 7 | Ownership changes (section 6) | Medium | 1 hour |
| 8 | Spoke: "How to choose a peptide moisturizer" | Medium | 1 day |
| 9 | Collagen page go-live, then DE and NL | Medium | Malcolm's review |

## 6. Proposed additions to `configs/page-targets.json`

| Path | primary | secondary | type |
|---|---|---|---|
| /products/copper-peptide-ghk-cu-night-cream | ghk-cu cream | copper peptide cream, copper peptide face cream | product |
| /products/copper-peptide-ghk-cu-day-gel-cream | copper peptide day cream | ghk-cu gel cream (never "copper peptide cream") | product |
| /products/matrixyl-3000-pro-collagen-firming-cream | matrixyl cream | collagen cream with matrixyl (drops "peptide cream") | product |
| /products/pdrn-collagen-night-cream | pdrn cream | pdrn night cream, pdrn creme, pdrn kollagen | product |
| /products/glutathione-brightening-serum | glutathione serum | glutathion serum, serum de glutation | product |
| /collections/copper-peptide | copper peptide skincare | copper peptide products, buy copper peptides | collection |
| /collections/creams-moisturizers | peptide cream | peptide creams, peptide face cream | collection |
| /collections/microneedling | microneedling stamp | derma stamp (not "microneedling serum") | collection |
| /pages/collagen-skincare | collagen cream | collagen serum, collagen face cream, kollagen creme | article |
| new spoke | peptide moisturizer | peptide moisturizer for dry skin | article |

The file has no per-locale field; DE needs one (`/de/collections/serums` = "peptid serum"; `/de/pages/the-science` = "peptide hautpflege"). Existing collection rows stay.

## 7. Open questions for Malcolm

1. Approve moving "peptide cream" from the Matrixyl cream to the creams collection, and "peptide moisturizer" to a new spoke? This contradicts [KS] section 4 and the Collagen page's "not this page's terms" row.
2. Night cream as owner of both copper cream terms, day cream unassigned. Agree?
3. Collection and product meta text carries magnitudes: copper (55.8%, "7 in 10"), PDRN ("up to 23%", "over twice as much as retinol"), Matrixyl (+256% in lab tests) [OWN]. The rule keeps in-vivo magnitudes off product pages until the formula is confirmed. Strip them?
4. Both stamp sets show "Sold out". Are they pre-order? May "absorb deeper" stay?
5. `CollectionPage`/`ItemList` JSON-LD needs custom Liquid. Allowed under "standard sections before custom code"?
6. Can the formulator give the Matrixyl 3000 concentration and the INCI name for GHK-Cu?
7. Confirm the Kaufland glutathione listing is ours, and who edits its title.
