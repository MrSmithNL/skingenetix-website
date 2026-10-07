# Teardown: why we do not rank for Argireline and Matrixyl 3000

**Date:** 2026-10-07 · **Scope:** the Argireline (acetyl hexapeptide-8) and Matrixyl 3000 keyword families, US first, then GB and DE · **Cost:** nothing paid (no DataForSEO, no Rube; only the SERP file already pulled today, curl, WebFetch, WebSearch and local files).

## How to read this document

Every figure carries a source tag.

| Tag | Source |
|---|---|
| **[SERP]** | `serps-2026-10-07.json`: DataForSEO top-10 pulled today, **desktop only**, with AI Overview (AIO) references, People-Also-Ask (PAA) and shopping blocks. Pulled before this task; I did not re-run it. |
| **[PROBE]** | My own curl fetches today, once with a Chrome user agent (UA) and once with the Googlebot UA, saved in `scratchpad/cmp/`. |
| **[GSC]** | Search Console exports in the scratchpad (window 2026-07-07 to 2026-10-05). |
| **[TRANCO]** | The public Tranco top-1M list (a ranking of how much traffic a domain gets across the web, downloaded today). It is **not a Google authority score**. Rank 1 is the busiest domain. "Not in 1M" means rank worse than 1,000,000. |
| **[D1]** / **[D2]** | `docs/keyword-ownership-analysis-2026-09-30.md` and `docs/keyword-strategy-2026.md` (this repo). **[D1] holds the only mobile SERP data we have.** |
| **[BL]** | `backlinks-skingenetix.json` and `refdomains-skingenetix.json` (our own backlink profile). |
| **[LH]** / **[INSPECT]** | Lighthouse mobile run and URL Inspection exports in the scratchpad. |

Demand figures (per month, observed clickstream, from [D2] §4 and [D1]): "argireline" 3,734 US / 1,103 GB / 845 DE, KD 3; "argireline serum" 605 US; "acetyl hexapeptide-8" 1,009 US; "does argireline work" 656 US; "matrixyl 3000" 2,725 US / 1,339 GB, KD 0, 211 DE; "matrixyl and argireline" 858 US.

**Limits you must know about (not measured, and why):**

- **No fresh mobile SERP.** The pull was desktop only and a mobile pull is a paid call, which this task forbids. Mobile evidence below is from 2026-09-30 [D1] plus the GSC device split. Re-pull mobile before acting on the ownership call.
- **No competitor backlink counts, branded-search volume or traffic estimates.** All need a paid tool. [TRANCO] is a rough substitute for "how big is this site".
- **No Reddit thread counts per brand.** WebSearch ignored the `site:reddit.com` operator and returned shops instead (four tries). Reddit itself serves bots a login shell (Chrome UA: 8 KB; Googlebot UA: HTTP 403), so Reddit page content could not be measured. Reddit's presence is
  counted only from the SERP file.
- **Competitor page speed not measured.** The PageSpeed API quota was exhausted (`psi-argireline-*.json` hold HTTP 429 errors). We have a Lighthouse run for our own hub only.
- **Pages I could not fetch:** schrammek.de (HTTP 403 to both UAs and to WebFetch), specialchem.com (403), justanswer.com (403), huffpost.com (HTTP 406), the stonevillenc.org spam pages (connection timeout for both UAs after 20-25 s). Their rows say "not measured".
- **Word counts** come from an automatic article extractor (trafilatura) and are rough. Where it clearly failed (shop pages full of menus, Typology, Amazon) I say so.
- A 403 to the Googlebot UA is **not** evidence of cloaking. Reddit, RealSelf and Wikipedia block faked Googlebot UAs because they check the real bot by IP address.
- We fetched our own site 3 times in this task (the two product pages and the German hub); the hub files were already saved. That is inside the limit of 5.

---

## 1. Classification of every page treated as a competitor

Each page was fetched with both UAs [PROBE]. "Same" means the two responses were the same size within about 0.5%.

| Domain / page | Class | UA probe result | Notes |
|---|---|---|---|
| amazon.com `/clp/` listings | RETAILER/MARKETPLACE | Chrome UA is redirected to the `/dp/` product page (1.0-2.1 MB); Googlebot UA gets the 58-62 KB `/clp/` page | Normal Amazon behaviour, not spam |
| theordinary.com | BRAND (also sells direct) | Same (408 KB) | |
| reddit.com threads | UGC | Chrome UA 8 KB login shell; Googlebot UA 403 | Content not measurable |
| gopicky.com | UGC (forum) | Same (103 KB) | Thread about using The Ordinary products |
| essentialdayspa.com `/forum/` | UGC (old skincare forum, "EDS Skin Care Forums") | Same (80 KB; 58 KB) | Posts are dated 2009-2011. A real forum on a day-spa domain, not a hack |
| justanswer.com | UGC (paid Q&A) | 403 to both | Not measured |
| realself.com | MEDICAL (Q&A with physician answer) | Chrome 200, Googlebot 403 | Has `QAPage` and `Physician` markup |
| paulaschoice.se, specialchem.com | BRAND ingredient dictionary / supplier dictionary | Paula's same; SpecialChem 403 | |
| vogue.com, wmagazine.com, womenshealthmag.com, byrdie, people.com, marieclaire.co.uk | EDITORIAL | Same | |
| joinmidi.com, klow-peptide.com, argentum.com, depology.com, asterwood.co, maelove.com, skindeva.com, theinkeylist.com, myfacedr.com, clinikally.com, typology.com, schrammek.de, clarins.de | BRAND or brand-run editorial (a seller writing the article) | Same (schrammek 403) | Midi appears to be a telehealth company; Klow lists a PharmD/PhD reviewer |
| incipedia.de, beauty.camp, wikipedia, pmc.ncbi.nlm.nih.gov, jddonline.com | EDITORIAL / MEDICAL reference | Same (Wikipedia 403 to fake bot only) | PMC and JDD are peer-reviewed |
| cultbeauty, fenwick, no7beauty, lookfantastic.de, target, thisisbeauty.us, timelessha.com, idealo | RETAILER or BRAND shop | Same | |
| **proniksedge.com** (matrixyl and argireline #3) | **SPAM, confirmed cloaking** | **Chrome UA: a "Project Management training Institute Nagpur" page (381 KB). Googlebot UA: a page titled "The Ordinary Matrixyl And Argireline I Tried The Ordinary MATRIXYL 10% HA For TWO WEEKS!" with 58 Matrixyl mentions and fake Product/AggregateRating/VideoObject markup (147 KB)** | A hacked institute site showing Google a different page than people see |
| **stonevillenc.org** (matrixyl 3000 #2, #4, #7; matrixyl serum etc.) | **SPAM (probable, not verified)** | Deep pages time out for both UAs; home page answers HTTP 200 | Domain is a North Carolina town site. Slugs such as `/peptides-matrixyl-3000-desk/` and `/matrixyl-3000-peptides-prime/` are the doorway pattern. Not in Tranco 1M. Content could not be fetched, so this is a judgement, not a measurement |

**Spam share:** 3 of 7 classic organic results for "matrixyl 3000" (US) and 1 of 7 for "matrixyl and argireline" (US) [SERP + PROBE].

---

## 2. What each SERP looks like today (desktop, [SERP])

| Term | Organic results returned | What they are | AI Overview | Other features |
|---|---|---|---|---|
| argireline (US) | 8 | **7 Amazon listings** + The Ordinary product page (#2) | Yes | PAA, images, shopping block |
| argireline serum (US) | 8 | **8 of 8 forum threads** (4 Reddit, 2 essentialdayspa, gopicky, skincaretalk) | Yes | PAA, shopping, "product considerations" |
| acetyl hexapeptide-8 (US) | **2** | Paula's Choice ingredient page, one Amazon listing | Yes | PAA, "perspectives", shopping |
| does argireline work (US) | 7 | Depology blog, RealSelf, W Magazine, Skin Deva, Reddit, Women's Health, ChemicalBook | Yes | Forums box, video, PAA |
| matrixyl 3000 (US) | 7 | Reddit x2, essentialdayspa forum, JustAnswer + **3 spam** | Yes | PAA, "perspectives", shopping |
| matrixyl 3000 serum (US) | 8 | Amazon, Timeless via thisisbeauty.us, Target search page, The Ordinary, Stylevana (Timeless), Amazon search, eBay, Sweetcare (Timeless) | Yes | Forums box, shopping (**Skingenetix is in the block**, "Full Matrixyl 3000 Ritual - Serum & Cream") |
| matrixyl and argireline (US) | 7 | essentialdayspa forum x5, JustAnswer, **1 cloaked spam** | Yes | PAA, "perspectives", shopping |
| argireline (GB) | 8 | The Ordinary collection, Cult Beauty, Fenwick, eBay, HuffPost, Amazon.co.uk, Etsy, The Ordinary | Yes | PAA, shopping |
| matrixyl 3000 (GB) | 10 | No7 collection, The Ordinary glossary, Amazon search, Reddit, INKEY, INKEE Decoder, Croda, Marie Claire, Timeless UK, Dermatica | **No** | PAA, shopping |
| argireline (DE) | 10 | Typology magazine, LOOKFANTASTIC x2, beauty.camp glossary, two pharmacies ("Argireline BTX"), Geizhals, Amazon.de, eBay | **No** | PAA, shopping |
| matrixyl 3000 (DE) | 10 | Schrammek, Clarins x3 (de and ch), incipedia, idealo (Timeless) x2, Reddit, Croda, dermida | **No** | PAA, shopping |

**Skingenetix does not appear in any organic top 10 for any of the 11 terms** [SERP].

**Two facts that change the reading:**

1. **The US SERPs moved in a week.** On 2026-09-30 "matrixyl 3000" US had a Timeless product page at #1 on desktop and mobile, then No7, The Ordinary glossary, INKEY and Women's Health [D1]. Today none of those is in the desktop top 7: Reddit, a spa forum and three spam pages
   hold it [SERP]. I did not re-pull to learn whether that is a hacked-site wave (the brief says so), personalisation, or a Google test. Treat today's Matrixyl head-term desktop SERP as abnormal.
2. **The People-Also-Ask boxes repeat the same questions across terms.** Counting by keyword match over the 11 PAA lists [SERP]: "downsides / side effects" appears in 7 of 11; "versus retinol" in 7 of 11; "what not to mix / combine / use first" in 7 of 11; "Matrixyl versus
   Argireline" in 4; "Botox" in 3 (acetyl hexapeptide-8 US, does argireline work, argireline DE). Our Argireline hub's FAQ answers none of the retinol, downsides or mixing questions (its five FAQ questions: what is it, how effective, how does it work, what concentration, how
   long). The Matrixyl hub answers retinol, other actives and safety.

---

## 3. Term-by-term teardown

### 3.1 "argireline" (US 3,734 per month, GB 1,103, DE 845)

**Top legitimate organic results (US, desktop):** #1 Amazon `/clp/B01M73TNMO`; #2 The Ordinary `argireline-solution-10-serum-100403.html` (the `en-vi` Virgin Islands version of the page; the AIO cites the `en-us` version); #3 Amazon `/clp/B01ND352PB`. Spam: none in this SERP.
**AIO cites:** Vogue, Wikipedia, The Ordinary (US product), Midi, Argentum, a YouTube video (`Y0Rgq902tgo`), Google Shopping tiles [SERP].
**PAA:** What does Argireline do for your face? / What are the downsides? / Is it better than retinol? / What can it not be mixed with? [SERP]

**Measured comparison.** Our hub is the page we want to rank for this term; our product page is shown for reference.

| Factor | Amazon #1 | The Ordinary #2 | Amazon #3 | Vogue (AIO) | Midi (AIO) | Argentum (AIO) | **Our hub** | **Our product** |
|---|---|---|---|---|---|---|---|---|
| Page type | marketplace listing | brand product page | marketplace listing | editorial article | telehealth article (MedicalWebPage) | brand journal article | ingredient research hub | product page |
| Title | "Beauty Enriched Matrixyl 3000 Argireline Hyaluronic Acid Serum Cream...(2 oz)" | "Fight Deep-Set Lines with Argireline Solution 10% Serum" | "For Dry Skin Pure Argireline Peptides Winkle Reduce Cream..." | "All About Argireline, a Peptide Called Botox in a Bottle" | "Argireline: What to Know Before You Buy" | "What is Argireline and what can it do for your skin?" | "Argireline® (Acetyl Hexapeptide-8): What It Does for Lines" | "Acetyl Hexapeptide-8 10% Anti-Wrinkle Serum" |
| H1 | listing title | "Argireline Solution 10%" | listing title | same as title | (not captured) | (not captured) | "Argireline® (Acetyl Hexapeptide-8)" | "Acetyl Hexapeptide-8 Anti-Wrinkle Serum" |
| Main-content words | about 260 (24 bullet + 234 description) | about 150 of own copy (hand-read; extractor was fooled by promo terms) | about 185 | 724 | 2,555 | 1,648 | 2,086 | 391 (page total 1,743 incl. reviews) |
| Opens with a direct answer | no (ad copy) | no (a patch-test notice comes first in the extract; product line "A serum for fine lines and wrinkles") | no | partly: frames the "Botox-like" claim, then explains | partly: frames the "Botox" claim | **yes** ("Argireline, affectionately dubbed 'botox in a bottle'... is...") | **partly**: four stat tiles first, then a "What Is Argireline?" paragraph | partly (benefit sentence) |
| Named studies with PubMed/DOI links | none | none | none | 1 outbound PubMed/DOI link, no named study | 7 links | 2 links, 2 citations | **8 links; 7 ScholarlyArticle schema blocks; Wang 2013, Raikou 2017, Henseler named** | none |
| Tables | 0 | 1 (product facts) | 0 | 0 | 0 | 0 | 3 | 0 |
| FAQ | no | 3 questions, FAQPage schema | no | no | yes (FAQ section) | yes (FAQ section) | 5 questions, FAQPage schema | 6 questions, FAQPage schema |
| Visible author / reviewer with credentials | seller only | none | seller only | Audrey Noble (no credentials shown) | **Ava Mainieri PhD and Kathleen Jordan MD as reviewers** | brand only | Malcolm Smith (founder) as writer; **Dr Esther Bodde, Cosmetic & Medical Physician, as reviewer** | none |
| Visible dates | none | none | none | published 2026-04-08 (schema) | 2026-07-02 | 2024-06-05 | "Last reviewed 23 September 2026" in text; **no `dateModified` in schema** (the Matrixyl hub has one) | none |
| JSON-LD types | none | Product, Offer, FAQPage | none | NewsArticle, Person, Organization, Breadcrumb | MedicalWebPage, Person, Organization | Article, Person, Organization | Breadcrumb, WebPage, Person, Organization, ScholarlyArticle x7, FAQPage | Product, Offer, Breadcrumb, FAQPage |
| Images / video | video present (5 video elements) | 61 images (mostly interface), no video | none | 21 images | 10 images | 81 images | 23 images, no video | 30 images, no video |
| Products and prices on page | the product, EUR 31.08 as shown to a Dutch visitor | the product, US$9.70 (schema) | EUR 88.83 | recommends products ($10 to $150) | none | brand's own products (EUR 116, 249) | shop block, EUR 44 | EUR 44 |
| Reviews / ratings | 4.1 stars from 23 ratings | review widget loads in the browser, no rating in the page code (not measured) | 3.0 stars from 1 rating | none | none | none | none | **9 "Verified Customer" reviews on the page, but no `aggregateRating` in the code** |
| Concentration stated | no | "10%" in the name | no | no | 1 mention | 2 mentions | **10% throughout (53 percentage mentions)** | 10% |
| "Botox" comparison | no | no | "no needle alternative" | **yes, in the title** | **yes, 23 mentions, a section titled "Why Botox in a Bottle Is the Wrong Expectation"** | yes (7) | **none (0 mentions)** | none |
| Side effects | irritation line only | "if irritation occurs" | no | "The Downsides" section | "Side Effects, Sensitivity..." section | 8 mentions | 3 mentions, no section; says "No side effects were reported in the controlled trials" | 1 mention |
| How to use | no | yes (a few drops, AM and PM) | no | yes | yes | yes (15 mentions) | yes | yes (3 simple steps) |
| Results timeline | no | no | no | no | no | 6 mentions | **16 mentions (4 weeks, day 20, 30 days)** | 3 |
| Before / after | listing says "before and after pictures" | no | yes (text) | no | 1 mention | no | **none on the hub** | **yes, a before/after block** |

**What the table says.** On proof we are ahead of everything that ranks or is cited: no top-3 page and no AIO source names a trial with a figure, while our hub states 22 of 45 versus 0 of 15 with the paper cited. What we lack is the question-shaped content (Botox, side effects,
retinol, mixing) that the PAA box and the AIO sources all carry, and a definition sentence ahead of the stat tiles.

**Why #1-#3 outrank us:**

- **(a) Authority.** Amazon is Tranco rank 26 and The Ordinary 40,451; the AIO's Vogue is 3,209, Midi 49,083 [TRANCO]. **Skingenetix is not in the top 1M**, and its backlink profile is 627 referring domains with zero real ones: every domain in the 100-row sample has rank 0, the
  profile spam score is 52, the top link TLDs are `.store` (97), `.online` (94), `.site` (93), `.shop` (92), `.website` (90), and only 2 of the links come from the US [BL]. The Ordinary has a dedicated Reddit community (the #1 and #2 results for "argireline serum" sit in
  r/TheOrdinarySkincare and r/SkincareAddiction) and sells through Sephora, Cult Beauty, Lookfantastic, Fenwick and Boots (all of them appear in the SERP file); its product or glossary page is cited in the AIO for four of the 11 terms [SERP]. I could not measure branded search
  volume.
- **(b) Content.** Content does not explain the Amazon wins: the #1 listing has about 260 words, a 4.1-star rating from 23 ratings and "Matrixyl 3000 Argireline" in its title. The Ordinary's page has about 150 words. They win because Google reads "argireline" on desktop as a
  buying query. Our hub's weakness is the missing question-shaped sections, not a lack of evidence.
- **(c) SERP features.** 7 of 8 desktop organic slots are Amazon. A shopping block and an AIO sit on top. The hub competes for the AIO and the mobile explainer slots, not for the Amazon slots.
- **(d) Technical.** Not the cause. Hub and products are indexed (URL Inspection: "Submitted and indexed", canonical correct, hub last crawled 2026-10-05) [INSPECT]. Our hub's own mobile lab test scores 60 out of 100, with Largest Contentful Paint 11.1 s, First Contentful Paint
  4.9 s, 2,534 KiB transferred, layout shift 0.001 [LH]. That is slow in a simulated slow-phone test, but I have no competitor numbers to prove it is worse than theirs.

**Our search position:** exact "argireline" has **no row in the 90-day GSC export**; the hub shows 1,350 impressions at average position 8.6 with 1 click, and the top matching queries are "acetyl hexapeptide-8" (22 impressions, position 15.7), "hexapeptide 8" (13, 18.5),
"argireline vorher nachher" (10, 8.4) and PubMed-shaped sentences [GSC]. Weekly hub impressions: 199, 466, 380, 197, 124 for the weeks starting 8-31 to 9-28 [GSC]. This is consistent with the long-tail queries fading, not with a ranking for the head term.

---

### 3.2 "argireline serum" (US 605)

**Top organic:** #1 Reddit r/TheOrdinarySkincare "Argeriline"; #2 Reddit r/SkincareAddiction "Can we talk Argireline?"; #3 gopicky.com discussion. All 8 organic results are forums (UGC) [SERP + PROBE]. No spam.
**AIO cites:** The Ordinary product, e-majestic.com (Vacation Argireline Serum), Vogue, Asterwood product page, Sephora, People ("The 10 Best Argireline Serums"), Google Shopping tiles. **Shopping block:** The Ordinary, Skin Deva (Walmart) x2, Derm, Maelove, Feel The Heal,
Beautefulskin, mattebeauty.co.

| Factor | Reddit #1 / #2 | gopicky #3 | essentialdayspa #4 | **Our product** |
|---|---|---|---|---|
| Page type | UGC thread | UGC thread | UGC thread (2011 posts) | product page |
| Words | not measurable | 53 (one question) | about 975 (old posts) | 391 |
| Studies / tables / FAQ / author / dates | not measurable | none | none (layout tables only) | none / none / 6 FAQs / none / none |
| Schema | not measurable | Organization, Breadcrumb | none | Product, Offer, FAQPage |
| Concentration | thread talk | none | "15%" in posts | 10% |

**Why they outrank us:**

- **(a)** Reddit is Tranco rank 106. Google gives forums a reserved slot on conversational "X serum" queries, and all 8 slots here went to forums.
- **(b)** Nothing a product page can out-write: the intent is "which serum / when do I use it". The Ordinary does not rank here with its own product page either; it is in the AIO and the shopping block.
- **(c)** Forums fill the whole organic list, AIO and shopping sit above them.
- **(d)** Our product page does not use the search word. "Argireline" appears **once** on the page; the title, H1 and meta description all say "Acetyl Hexapeptide-8" [PROBE]. For a term where The Ordinary, Skin Deva, Asterwood, Depology and Maelove all put "Argireline" in the
  product name, we are not a candidate. (A trademark question for Malcolm: Argireline® is Lipotec's mark; The Ordinary prints "ARGIRELINE is a trademark of Lipotec" under its product, and our hub already uses it.)

---

### 3.3 "acetyl hexapeptide-8" (US 1,009)

**Top organic (only two classic results returned):** #1 paulaschoice.se (English-language Swedish store) "What is Acetyl Hexapeptide-8?"; #2 Amazon `/clp/B0CZXTMJLS` (BACHERI serum). Spam: none.
**AIO cites:** PMC review (PMC12193160), Amazon (Forest Borgess serum), Wikipedia, JDD review (2025), Paula's Choice (FR site), SpecialChem, SkinCeuticals, two Instagram reels [SERP].
**PAA:** What does it do? / Does it really work? / Which peptide acts like Botox? / Is it the same as Argireline?

| Factor | Paula's Choice #1 | Amazon #2 | PMC review (AIO) | JDD review (AIO) | Wikipedia (AIO) | **Our hub** |
|---|---|---|---|---|---|---|
| Type | brand ingredient dictionary | listing | peer-reviewed review | journal review | encyclopedia | ingredient hub |
| Words | about 212 | about 157 (bullets only) | about 6,450 | about 760 (abstract and start) | about 950 | 2,086 |
| Opens with direct answer | **yes**: "Acetyl hexapeptide-8 is a synthetically derived peptide used in skin care to treat wrinkles and signs of ageing" | no | abstract | abstract | yes | partly (stat tiles first) |
| Named studies with links | none | none | **97 PubMed/DOI links** | review | 14 links | 8 |
| FAQ / tables | no / no | no / no | no / 2 | no | no / 1 | yes / 3 |
| Author | brand | seller | academic authors | **Lum, Hirpara, Pham MD** and others | none | founder + physician reviewer |
| Dates | none | none | not captured | 2025-03-12 | modified 2026-08-15 | "last reviewed" text only |
| JSON-LD | Organization, WebSite only | none | none | WebPage, Breadcrumb | Article | rich (see 3.1) |
| Botox mention | 1 | 4 | 14 | 0 in extract (title says "Botulinum Toxin") | 1 | **0** |

**Where we stand:** GSC shows "acetyl hexapeptide-8" at position 15.7 (22 impressions) and "acetyl hexapeptide 8" at 19.8, so page two [GSC].
**Why we are behind:** (a) Paula's Choice is Tranco 61,726 for .com and its definition format matches the PAA exactly; the AIO draws on PMC, JDD, Wikipedia and brand dictionaries, i.e. the medical-reference tier we are not in. (b) Content is not the gap: we are 10 times longer
than Paula's Choice and carry more cited trials than any brand page. The gap is the opening: our hub opens with numbers, not the one-sentence definition Paula's Choice uses. (c) With only two classic results plus AIO, PAA and shopping, there is very little room on the page. (d)
No technical blocker found.

---

### 3.4 "does argireline work" (US 656): unowned question

**Top legitimate organic:** #1 depology.com blog "Argireline™ Benefits For Your Skin?"; #2 RealSelf Q&A; #3 W Magazine "Is The Ordinary's Argireline Solution 10% Really 'Botox in a Bottle'?". Also: #4 Skin Deva "before and after", #5 Reddit, #6 Women's Health, #7 ChemicalBook. No
spam [SERP + PROBE].
**AIO cites:** Reddit r/30PlusSkinCare, Vogue, **Asterwood blog**, Midi, **Clinikally**, **Maelove**. Forums box: two Reddit threads and Quora [SERP].

| Factor | Depology #1 | RealSelf #2 | W Magazine #3 | Asterwood blog (AIO) | Clinikally (AIO) | Maelove (AIO) | **Our hub** |
|---|---|---|---|---|---|---|---|
| Type | brand blog | doctor Q&A | editorial test | brand blog | e-pharmacy blog | brand blog | ingredient hub |
| Title | "Argireline™ Benefits For Your Skin?" | "Is it true Argireline works like Botox..." | "Is The Ordinary's Argireline Solution 10% Really 'Botox in a Bottle'?" | "Argireline: The Botox Alternative That Actually Works" | "How to Use Argireline for Younger & More Lifted Facial Skin" | "How Argireline is (and is not) like Botox" | "Argireline® (Acetyl Hexapeptide-8): What It Does for Lines" |
| Words | 831 | 142 | 1,476 | 2,476 | 4,178 | 545 | 2,086 |
| Direct answer up top | no (chatty intro) | yes (physician answer) | no (anecdote) | **yes: "The short answer is yes, within specific limits."** | no | partly | **no ("does it work" is never asked or answered in those words)** |
| Studies named | none | none | none | **yes (34 mentions of study/trial, 2 links, reference list)** | none | "The NIH Study That Changed Our View", 6 citations | **Wang 2013, Raikou 2017, Henseler, 8 links** |
| Author with credentials | "Robin C" | physician (Physician schema) | 3 W editors, no credentials | Jon Kopecky, none shown | Arjun Soin, "Doctor's Desk" | "Team Maelove" | founder + physician reviewer |
| Dates | 2022-09-15, updated 2025-10-23 | none | **2021-09-06** | 2026-04-21, updated 2026-07-23 | 2026-04-01 | 2024-07-17, updated 2026-04-09 | last reviewed 2026-09-23 |
| FAQ | no | no | no | yes | yes | no | yes (5) |
| Botox / side effects / how to use / timeline | Botox 9 / no / no / no | Botox 4 | Botox 5 / no / how-to 11 / timeline 7 | Botox 21 / 5 / 17 / 9 | not counted ("Botox in a bottle" in the intro) | Botox 11 | **Botox 0** / 3 / 7 / 16 |
| Before/after | no | no | no | no | no | no | none |

**Why they outrank us:** (a) None of these pages is from a strong domain: Depology and Asterwood and Maelove are not in Tranco 1M, Clinikally is 62,865, W Magazine 22,957, RealSelf 36,809. **Small domains rank and are cited here.** (b) The cited pages **answer the question in the
headline words** and state the verdict early; the weakest page one result is a 2022 brand blog and a 2021 magazine test. Our hub holds the best evidence but never says "does it work?" or "Botox". (c) AIO, a forums box and a video row crowd the page. (d) Nothing technical.
**What to do:** see §5.

---

### 3.5 "matrixyl 3000" (US 2,725 per month, GB 1,339, DE 211), including why The Ordinary and Timeless win with product pages

**Top legitimate organic, US today (desktop):** #1 Reddit r/skincaredevices "Does Asterwood Matrixyl 3000 Serum Really Boost..."; #3 essentialdayspa forum "Matrixyl 3000 from Isomers"; #5 Reddit r/SkincareAddiction "Are peptides effective or not?". Also #6 JustAnswer
(wholesale-ingredient Q&A). **Spam, listed separately:** stonevillenc.org at #2, #4 and #7.
**AIO cites:** The Ordinary glossary (`matrixyl-3000-ingredient-glossary`), INKEY List article, naturalorganicskincare.com (raw Matrixyl booster product), Face Dr article, a YouTube video (`M2dmw9erSo4`), Google Shopping tiles.
**On 2026-09-30 [D1]** (desktop and mobile): #1 Timeless product page, #2 No7 ingredient shop page, then The Ordinary glossary, INKEY, INCIDecoder, Women's Health.

**"matrixyl 3000 serum" (US, today):** #1 Amazon (Asterwood Matrixyl 3000 with Argireline + mist), #2 thisisbeauty.us (Timeless retailer), #3 Target search page, #4 The Ordinary (the `en-lk` Sri Lanka collection URL), #5 Stylevana (Timeless), #8 Sweetcare (Timeless). AIO cites
Timeless's own page, two Depology product pages and Dermapproved (Asterwood).

| Factor | The Ordinary glossary (AIO, #2 GB) | The Ordinary collection (#4 serum) | Timeless product page (AIO, #2 on 9/30) | thisisbeauty.us (Timeless reseller, #2 serum) | INKEY article (AIO) | No7 collection (#1 GB) | **Our hub** | **Our serum** |
|---|---|---|---|---|---|---|---|---|
| Type | brand ingredient glossary | brand category page | brand product page | retailer product page | brand editorial | brand category page | ingredient hub | product page |
| Title | "Matrixyl 3000 \| Ingredients Glossary \| The Ordinary" | "Matrixyl 3000" | "Matrixyl 3000 Peptide Complex Serum \| Timeless Skin Care" | "Timeless Skin Care Matrixyl 3000 Serum 1 fl oz" | "What is Matrixyl 3000? The Science Behind the Peptide" | "Matrixyl 3000 Plus Skincare" | "Matrixyl 3000: Benefits, Studies and How to Use It" | "Matrixyl 3000 Serum for Firmer-Looking Skin \| Skingenetix" |
| H1 | "What Matrixyl 3000 Does For The Skin" | (category) | product name | product name | same as title | (category) | "Matrixyl 3000 (Palmitoyl Tripeptide-1 and Tetrapeptide-7)" | "Matrixyl 3000 Firming Serum" |
| Words | about 131 | about 38 | about 2,636 incl. FAQ | about 111 | about 4,448 | about 45 | 2,103 | 351 |
| Direct answer opening | yes (short) | no | claim-led ("clinically proven...") | no | yes (definition) | no | yes (definition after stat tiles) | benefit line |
| Named studies | none | none | brand trial percentages ("In a 14-day clinical trial, 96% of users reported improved firmness", "collagen synthesis is boosted by up to 258%"), no links | none | 27 study mentions, **0 links** | none | **6 PubMed/DOI links, 6 ScholarlyArticle blocks, graded A to D per its meta description** | none |
| FAQ | no | no | 4 questions + FAQPage | no | FAQPage | no | 6 questions + FAQPage | 6 questions + FAQPage |
| Author / reviewer | none | none | none | none | "askINKEY skincare advisor" | none | "By Skingenetix. Medically reviewed by Dr Esther Bodde" | none |
| Dates | none | none | 2026-06-01 / 2025-09-19 | none | published 2026-07-13, updated 2026-07-24 | none | 2026-03-10, **modified 2026-09-22** | none |
| JSON-LD | none | ItemList | ProductGroup, Product, Offer, FAQPage | Product, Brand, Offer | BlogPosting, Product, FAQPage | CollectionPage, ItemList | rich, plus dates | Product, Offer, FAQPage |
| Price | US$10.90 (Matrixyl 10% + HA) | US$13.10 to $23.90 | **US$27.95** | US$30 | n/a | £10 to £17.95 | EUR 44 etc. in shop block | **EUR 44** (shown to an EU visitor) |
| Reviews | not measured | not measured | **4.9 stars, 829 reviews in schema** | none | none | not measured | none | **none in schema (9 on-page review texts)** |
| Concentration stated | no | no | "1% hyaluronic acid"; Matrixyl % not stated | 3 mentions | 14 mentions | no | **44 percentage mentions (e.g. "-39% deep-wrinkle area")** | **none** |
| Side effects / timeline / before-after | none / none / none | none | 1 / 6 / none | none | 5 / 10 / none | none | 0 / 5 / "before and after" section | 0 / 3 / before-after block |

**Why The Ordinary and Timeless win with product pages (not content):**

- **The Ordinary:** The page that ranks is about 38 to 131 words long. It wins on (a) brand: Tranco 40,451, its own Reddit community, and retail distribution; (b) the ingredient name sits in the product name ("Matrixyl 10% + HA"), glossary and category URL; (c) one product shown
  in the shopping block; (d) the same glossary exists in more than 100 country versions (WebSearch returned `en-ca`, `en-fi`, `en-kr`, `en-ae`, `en-pr`, `en-sn`, `en-ws`, `en-sa` copies of the Argireline glossary alone), and country versions show up in the US results (`en-lk`,
  `en-vi`), so every locale builds the same brand signal. This is brand and distribution, not writing.
- **Timeless:** the product **is** the ingredient ("Matrixyl® 3000 Serum"), priced at $27.95 against our EUR 44 (not a like-for-like currency comparison; our US price was not measured), with **829 reviews at 4.9 stars in structured data**, a 2,636-word page with a "Clinical Trial
  Results" block (their own percentages) and FAQs, and a **reseller network**: thisisbeauty.us (#2), Stylevana (#5), Sweetcare (#8) rank for the serum term and idealo.at ranks twice in Germany, so one product occupies 3 of the 8 organic slots, plus the AIO [SERP]. Timeless's own
  domain is Tranco 464,361, which is still bigger than ours (we are outside the top 1M), and its product has real reviews, real reseller links and real price-comparison listings.
- **No7 (GB #1):** a 45-word collection page for its "Matrixyl 3000 Plus" range, on a Tranco 512,990 domain. Again brand plus exact ingredient-in-range-name, not words.

**Where we stand on the head term [GSC, 90 days]:** "matrixyl 3000": 51 impressions at average position 14.45, 1 click. Compare roughly 12,200 searches over the same three months in US+GB alone (2,725 + 1,339, times 3): **about 0.4%** (two different measurements, so indicative
only). Impressions are **spread across four of our URLs** [GSC, 28-day query-page rows]: the Pro-Collagen Cream (28 impressions, position 5.6), the Matrixyl serum (10, position 32.9; and 27 for "where can i buy matrixyl 3000" at 39.6), the home page (5, 8.6), and the hub (2, 47).
Google is picking the cream, not the serum we named the owner. Weekly impressions are rising for both: hub 6, 8, 33, 34, 121 (3 clicks in the last week) and serum 3, 30, 38, 39, 72 [GSC].
**Why we are behind:** (a) zero real authority, zero reviews that machines can see, no Reddit or YouTube footprint; (b) our serum page has no concentration, no study, no rating markup, no author or reviewer, and 351 words against Timeless's 2,636; (c) on today's head-term SERP
the commercial slots were removed and replaced by forums and spam, so even a perfect product page would be competing for a Reddit slot; (d) nothing technical (serum last crawled 2026-10-07, hub 2026-09-19, both indexed) [INSPECT]. One flag: the serum's **meta description**
mentions "pentapeptide-4... and vitamin C", while the page text speaks only of Matrixyl 3000; check that the formula and the description agree [PROBE].

**GB "matrixyl 3000" (no AIO):** #1 No7 collection, #2 The Ordinary glossary, #3 Amazon.co.uk search page; #4 Reddit, #5 INKEY UK, #8 Marie Claire (755 words, 2025-02-17), #9 Timeless UK, #10 Dermatica SkinLab (1,079 words, 2026-08-21). Top 3 are brand and retail category pages.
A hub-style article (INKEY, Marie Claire, Dermatica) can sit at #5 to #10 without top-tier authority. No spam.
**DE "matrixyl 3000" (no AIO):** #1 Schrammek "Wirkstoffporträt Matrixyl3000" (not measured, 403), #2 Clarins ingredient page (herbarium; 39-word extract, 8 sections), #3 incipedia (948 words, 2015/2017 dates, WebPage schema), #4 and #5 clarins.ch, #6 and #8 idealo.at (Timeless),
No. 7 Reddit, #9 ULProspector (Croda), #10 dermida.de. **Brand-run ingredient explainers (Schrammek, Clarins) hold the top two**, which matches [D2] §5: "brand-owned ingredient explainers rank reliably". PAA: "Was ist besser, Matrixyl oder Argireline?" [SERP]. Our hub translation
exists (`/de/pages/matrixyl-3000-research`: 4 impressions, position 2.75, 1 click [GSC]).

---

### 3.6 "matrixyl and argireline" (US 858): unowned question

**Top organic:** #1, #4, #5, #6, #7 essentialdayspa.com forum threads (2009-2011 era, e.g. "are there products with BOTH matrixyl AND argireline"); #2 JustAnswer (wholesale ingredients, 403, not measured); **#3 proniksedge.com = cloaked spam**. So there is **no legitimate page
one answer** [SERP + PROBE].
**AIO cites:** Asterwood product page (`/products/matrixyl-3000-argireline`), **Klow** "Matrixyl vs Argireline: Anti-Wrinkle Peptide Winner [2026]", **Skin Deva x2** ("Matrixyl and Argireline: Ultimate Anti-Aging Duo"; "How to Use Matrixyl and Argireline Together"), People "Best Argireline Serums".
**PAA:** Can Argireline and Matrixyl be used together? / Do I apply Matrixyl or Argireline first? / downsides / what not to pair.

| Factor | Klow (AIO) | Skin Deva duo (AIO) | Skin Deva how-to (AIO) | Asterwood product (AIO) | essentialdayspa #1 | **Ours** |
|---|---|---|---|---|---|---|
| Type | brand article, MedicalWebPage | brand blog | brand blog | product page | forum | **no page exists** (hubs mention the other peptide 1 to 2 times; our "Peptide Duo Set" product exists) |
| Title | "Matrixyl vs Argireline: Anti-Wrinkle Peptide Winner [2026]" | "Matrixyl and Argireline: Ultimate Anti-Aging Duo" | "Combining: How to Use Matrixyl and Argireline Together" | "Matrixyl 3000 + Argireline Peptide Serum - Dual Anti-Aging" | "are there products with BOTH matrixyl AND argireline" | n/a |
| Words | 2,154 | 1,250 | 654 | 474 | about 975 | n/a |
| Direct answer up top | **yes: three bullet takeaways (Matrixyl for static wrinkles, Argireline for dynamic)** | yes (question framed) | yes (definitions) | n/a | n/a | n/a |
| Named studies | **8 PubMed/DOI links, Sources section** | none | none | 2 mentions | none | n/a |
| Author / reviewer | **Dr Emilie Renaud, PharmD PhD, Clinical Pharmacologist** | none | none | none | forum members | n/a |
| Dates | **updated 2026-09-11** | 2025-11-10 | 2024-09-04 | none | 2011 | n/a |
| FAQ | yes | no | no | yes + reviews (4.73, 208) | no | n/a |

**Why nobody legitimate holds this SERP and who gets the AIO:** (a) forums with 15-year-old posts hold classic results; the AIO bypasses them and cites **small brand sites**, none of which is in Tranco 1M (Klow, Skin Deva), so domain size is not the entry ticket. (b) The cited
pages **answer "can I use them together" in the first screen**; Klow adds a credentialed reviewer and sources. (c) Spam and forums fill organic; shopping shows duo serums from Maelove, ANAiRUi, Eva Naturals, Skin Deva, Asterwood. (d) None.
**Our edge:** we sell both actives and have a duo-set product, and our two hubs carry the trials. What we do not have is a page that says "yes, and here is what is and is not known about using both."

---

### 3.7 "argireline" GB and DE (for completeness)

**GB (1,103 per month):** #1 The Ordinary collection "Argireline" (about 38 words, ItemList), #2 Cult Beauty product (359 words, **4.33 stars from 1,003 reviews**, Product/AggregateRating schema), #3 Fenwick (156 words); HuffPost #5 not measurable. AIO cites Wikipedia, Argentum,
Byrdie, Vogue, The Ordinary GB product, Boots, a PMC paper (PMC10665711), YouTube. Retail SERP; our hub has no GB visibility in the data.
**DE (845 per month, no AIO):** #1 **Typology magazine** "Welche Möglichkeiten gibt es, die Argireline zu nutzen?" (brand journal, five sections, sources list, dated 2025-11-21/2026-03-27; my word count of 47 is an extractor failure), #2 LOOKFANTASTIC (The Ordinary product,
**4.44 stars from 1,238 reviews**), #3 beauty.camp Lexikon (319 words, sections "Was ist Argireline?" and "Gibt es Nebenwirkungen?"), #4 and #7 Guyot Apotheken "Argireline BTX", #5 Apoluh "Argireline BTX 10%". PAA: "Ist Argireline ein Ersatz für Botox?", "Was ist besser, Matrixyl
oder Argireline?", "Welche Nachteile hat Argireline?".
**Our DE hub:** the title tag is "Acetyl Hexapeptide-8 Forschung und Studien" and **does not contain the word Argireline** (the H1 does) [PROBE]. It does not appear in the exported 90-day page list [GSC]. The German market names the product "BTX" and asks about Botox; our German
copy shows no "Botox" or "BTX" either (not checked in the translated text beyond the title).

---

## 4. Ownership: which page should target which term

**Evidence base.** Desktop: today's SERPs [SERP]. Mobile: 2026-09-30 only [D1] and the GSC device split (mobile 1,615 impressions at position 10.3, 3.3% click-through; desktop 3,649 at 11.4, 0.66%) [GSC]. **No fresh mobile pull exists.**

| Term | What Google ranks | Verdict | Confidence | What would change it |
|---|---|---|---|---|
| **argireline** (US) | Desktop today: 7 of 8 Amazon listings plus The Ordinary. Mobile (9/30): PMC, The Ordinary, Vogue, Reddit, Lubrizol, Byrdie, INCIDecoder, shopping row. AIO: Vogue, Wikipedia, The Ordinary, Midi, Argentum. GB: retail. DE: magazine, retailer, glossary | **Hub owns "argireline"**, aimed at mobile explainers, the AIO and PAA. **Do not expect the product page to enter the desktop Amazon list.** It reaches shoppers through the shopping block (Merchant Center) | Medium-high | A mobile re-pull showing product pages at the top |
| **argireline serum** (US) | 8 of 8 forum threads; products only in AIO and shopping | **Product** page, but its realistic win is the shopping block and an AIO citation, not an organic rank. First change: the page must contain the word "Argireline" (it appears once today) | Medium | Reddit slots giving way to product pages |
| **acetyl hexapeptide-8** | Two organic results (ingredient dictionary, Amazon) + AIO of PMC/JDD/Wikipedia/dictionaries | **Hub** (matches its URL; we are already at position 15.7) | High | none |
| **matrixyl 3000** (US) | 9/30: Timeless product page #1 on desktop **and** mobile. Today: no commercial page in the top 7. AIO: explainers (The Ordinary glossary, INKEY, Face Dr) plus a raw-ingredient product. GB: category pages and explainers. DE: brand explainers | **Keep the serum as owner of the head term "matrixyl 3000", but split the job**: the serum owns "matrixyl 3000 serum", "buy" and shopping; the hub owns "what is / benefits / does it work / vs retinol" and **all of DE** (where the top two are ingredient explainers). Today's SERP is too disturbed to flip the earlier decision | **Low-medium** | A clean re-pull of desktop and mobile after the spam clears |
| **does argireline work** | Page one is a 2022 brand blog, a Q&A and a 2021 magazine test; the AIO cites small brand blogs | **Argireline hub, as a section with that exact heading and a one-sentence verdict first** (agrees with [D1]) | High | none |
| **matrixyl and argireline** | Forums and one cloaked spam page; AIO cites Klow, Skin Deva, Asterwood | **A new spoke article** that links to both hubs and to the duo-set product (agrees with [D1]), not a section inside a hub, because Google is citing standalone pages | High | none |

**One thing the data contradicts.** [D1] and the keyword strategy expect the serum to take "matrixyl 3000". The only evidence that the product page should win is Timeless at #1 on 9/30. That page has 829 reviews, a stated clinical block and a reseller network. Our serum has none
of the three, and Google today prefers our **cream** for that head term (position 5.6 against 32.9). Decide whether to keep splitting signal across the cream, the serum and the hub, or to point the collection and cream's title toward "collagen cream with matrixyl" so the serum
alone carries "matrixyl 3000" (the strategy file already lists "collagen cream with matrixyl" as the cream's second term).

---

## 5. What our pages must change to beat the #1 legitimate page

Ordered by expected return divided by effort. "Expected" means an estimate, not a forecast; I cannot quote a traffic number I did not measure.

### A. Argireline hub (`/pages/acetyl-hexapeptide-8-research`)

1. **Add the missing question sections, with the verdict in the first sentence of each:** "Does Argireline work?" (state the two-trial picture and the Henseler null result in two sentences; note the standing rule that science pages publish positive results only and keep nulls to
   a reframed limits section, so decide how much of Henseler goes in this section), "Is Argireline 'Botox in a bottle'?" (the honest answer is no, with the mechanism difference; Midi, Asterwood and Maelove all use this framing), "Side effects and downsides", "Argireline vs
   retinol", "What not to mix with Argireline", "Argireline vs Matrixyl 3000". These are the PAA questions that appear in 7 of 11 SERPs. **Check each sentence against the claims register before it goes in:** the hub says "No side effects were reported in the controlled trials",
   and a downsides section needs wording that matches what the trials report.
2. **Put one definition sentence above the stat tiles** (Paula's Choice's page, the #1 result for the acetyl hexapeptide-8 term, opens exactly that way).
3. **Add `dateModified` to the page schema** (the Matrixyl hub has it; this hub only shows "Last reviewed 23 September 2026" as text). Keep the reviewer line; Midi and Klow are cited with named credentialed reviewers.
4. **German title tag:** put "Argireline" in it (e.g. "Argireline (Acetyl Hexapeptide-8): Wirkung und Studien"). 845 searches per month name the product that way.
5. Do not chase the Amazon listing slots; they are not winnable by a hub.

### B. Argireline serum (`/products/acetyl-hexapeptide-8-anti-wrinkle-serum`)

1. **Put "Argireline" in the title, H1 or first paragraph**, if Malcolm is content with the trademark position (decision needed; see 3.2).
2. **Mark up the 9 on-page reviews** (`aggregateRating`). Cult Beauty (1,003 reviews) and Lookfantastic (1,238) win their regional SERPs partly on visible star ratings. Our reviews are visible text but not in the code [PROBE]; see the memory note that Klaviyo reviews are invisible to machines.
3. Link up to the hub's "does it work" section and sideways to the duo-set. Keep Merchant Center feeding the shopping block, since our product is already in that block for the matrixyl serum term.

### C. Matrixyl hub (`/pages/matrixyl-3000-research`)

It already answers retinol, other actives and safety. Add (1) a "Matrixyl 3000 vs Argireline" section that points to the new spoke, (2) the DE title check, (3) a direct definition above the tiles. Its weekly impressions already rise (6 to 121) and it has the first clicks, so **do
not restructure it**; extend it.

### D. Matrixyl serum (`/products/matrixyl-3000-firming-serum`)

Gaps against Timeless: no concentration, no study, no rating markup, no reviewer, 351 words. Add the stated percentage if the formula allows, two or three cited facts from the hub with links, rating markup from the reviews, and resolve the "pentapeptide-4 / vitamin C" description
mismatch. Resolve the cannibalisation with the Pro-Collagen Cream (3.5).

### E. Two new spokes

1. **"Argireline and Matrixyl 3000 together"** (858 per month; page one has no legitimate answer). Structure copied from what is being cited: three-bullet answer first, then "do they work together", "which first", "who should skip", then the evidence from our two hubs, reviewer
   named, `dateModified` set, link to the duo set. No claim of a combined trial unless one exists in the register; I did not find one in this research.
2. The "does Argireline work" section on the hub (A1) rather than a separate page, because the hub is the only page weighing every trial [D1].

### F. Off-site (the part content cannot fix)

Every top result has a footprint we lack: The Ordinary and Timeless have Reddit threads and many resellers; Midi, Klow and Asterwood have pages the AIO trusts. Our link profile is 627 spam domains, 0 genuine [BL]. Start with the sources the AIO already cites for these terms:
YouTube (cited for both "argireline" and "matrixyl 3000") and Reddit (4 of 8 "argireline serum" results). A disavow file for the spam links is worth a separate decision; I have not tested whether they cause harm.

---

## 6. The single biggest lever

**Make the Argireline hub the page that answers the question cluster Google keeps asking, in the words it asks them, and publish the "Argireline and Matrixyl 3000" spoke.** On these question terms (does it work 656, together 858 per month) page one is forums and old blogs, spam,
and the AI Overview cites small sites that rank in no top-1M list, so authority is not what is blocking us. We already hold stronger evidence than every cited page; what is missing is the question-and-answer shape. It needs no backlinks and no new store pages, it can be built
from the existing register, and it can be re-measured within a week.

**What I would not expect it to fix:** the "argireline" and "matrixyl 3000" head terms on desktop, where Amazon, The Ordinary, Timeless and, today, Reddit and spam hold the slots. Those need reviews, price position, resellers and outside links, and they are months of work.

---

## 7. Open questions for Malcolm

1. May the product page carry the word "Argireline" in its title (Lipotec trademark)?
2. Should the Pro-Collagen Cream stay targeted at "matrixyl 3000" signals, or should the serum alone carry them?
3. Is a "Botox in a bottle" section acceptable to the claims register, framed as "what it is and is not"?
4. Authorise a mobile re-pull of the 11 SERPs (about 11 paid calls at roughly $0.002 each, based on the cost in `serp_pull.py`) so the ownership decision is based on both devices on the same day?
5. Re-pull "matrixyl 3000" US desktop in 5-7 days to see whether the three spam pages and the missing commercial results were a transient.

*Raw probe files and the metric extractor are in `/private/tmp/claude-501/-Users-malcolmsmith-Claude-Code-Projects-skingenetix-website/f78cea59-644d-45cd-8fa1-6176afb40dbd/scratchpad/cmp/` (`probe.log`, `metrics.json`, `m.py`, `d.py`). They are session scratch and will not persist.*
