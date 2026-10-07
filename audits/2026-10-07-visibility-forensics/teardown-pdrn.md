# PDRN keyword family: competitor teardown (2026-10-07)

Site: www.skingenetix.com (Shopify peptide-skincare store). Markets: US first, then GB, DE, NL.
Scope: 7 US terms, GB "pdrn" and "pdrn serum", DE "pdrn", NL "pdrn".
Written in plain English. Every number carries a source tag (key below). Where something could not be measured, it says so.

## Source tags

| Tag | What it is |
|---|---|
| [SERP] | Top-10 Google SERPs pulled 2026-10-07 (DataForSEO live, desktop, depth 10): `scratchpad/serps-2026-10-07.json`. Includes AI Overview (AIO) references and People-Also-Ask (PAA). |
| [FETCH] | My own fetches on 2026-10-07 with `curl`, one Chrome user agent and one Googlebot user agent per page, measured with trafilatura and BeautifulSoup (`scratchpad/comp/measure.py`, outputs in `scratchpad/comp/measures.json`, `own_measures.json`, `textflags.json`, `headingflags.json`, `studylinks.json`). |
| [GSC] | Google Search Console export, window 2026-07-07 to 2026-10-05 (`gsc-90d-2026-10-07.json`, `gsc-detail-2026-10-07.json`). |
| [INSPECT] | URL Inspection API results for our URLs, 2026-10-07 (`url-inspection-2026-10-07.json`). |
| [LH] | Lighthouse mobile lab runs of our pages, 2026-10-07 12:20 UTC (`lh-mobile-*.json`). |
| [BL] | DataForSEO backlink summary and the 100 most recent referring domains (`backlinks-skingenetix.json`, `refdomains-skingenetix.json`; 100 of 624 domains). |
| [KS] | `docs/keyword-strategy-2026.md` sections 3 to 5 (observed volumes). Ads figures from `configs/keyword-data/keywords-*-2026-09-22.json` are labelled "Ads, bucketed". |
| [TRANCO] | Tranco public site-popularity list, queried 2026-10-07 (tranco-list.eu API). Lower number = more visited. A popularity proxy, not a Google authority score. |
| [WEB] | WebSearch results from today, cited by URL where used. |

Pages I fetched from our own site: 5 (the serum was already saved). The cap was 5.

---

## 1. Three findings and the single biggest lever

1. **Our English PDRN hub is not in Google at all, and that decides everything else.** The URL Inspection API says "URL is unknown to Google" [INSPECT], although the page is in the sitemap, has a self-canonical, no noindex, and is linked from the homepage and five other pages
   [FETCH]. Our German and Dutch hubs were crawled on 2026-09-05 and 2026-09-10 [INSPECT]. The English hub has zero Search Console impressions in the 90-day window [GSC]. It is also the strongest page we have: 2,237 words, 79 percentage figures, 5 linked studies and a named
   medical reviewer, against at most 23 percentage figures on the best competitor page [FETCH].
2. **Content is not why we lose. Authority, page type and SERP features are.** None of the 33 readable competitor pages I fetched cites the Ye 2026 PLOS ONE trial (the head-to-head PDRN-vs-retinol split-face trial our hub reports as the only controlled trial of topical PDRN on
   intact skin) [FETCH]. Only 8 of 30 commercial and editorial pages link even one study
   [FETCH]. No page shows a "medically reviewed by" line [FETCH]. Yet small sites outside the Tranco top 1 million hold top-3 slots (ItGirlies, House of Communal, EG Skin Clinic, The K Beauty Edit, Maruderm, pdrn-skin.com) and top-5 slots (Beauty By Peptides, The Style List)
   [SERP] [TRANCO]. They are indexed and match what Google wants to show: a category page, a listicle or an expert explainer. We have 627 referring domains on paper but all 100 I could inspect are automated spam (spam score 45 to 75, rank 0) [BL].
3. **The US PDRN SERPs are crowded with features, not just pages.** An AI Overview appears on all 7 US terms. YouTube is cited in 6 of the 7. Reddit is cited in 5 (the same r/AsianBeauty thread is cited in 3). Instagram holds 3 of the 6 listed results for "pdrn"; Reddit, YouTube,
   LinkedIn and TikTok hold 5 of the 7 for "pdrn vs retinol" [SERP]. A hacked US town website holds #2 for "pdrn" [FETCH] [SERP].

**Single biggest lever:** get `/pages/pdrn-research` crawled and indexed (manual Request Indexing in the Search Console interface, then confirm with a fresh inspection), then earn the first genuine links to it by pitching the Ye 2026 head-to-head result. Nothing else on this list
matters until Google can see the page.

---

## 2. Method and limits

### 2.1 How pages were classified

Every page was fetched twice, with a Chrome user agent and with `Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)`, and the readable text was compared [FETCH]. Classes: BRAND, RETAILER/MARKETPLACE, EDITORIAL, UGC, MEDICAL, SPAM.

Result: 30 pages returned identical readable text to both agents. Two were unreadable to both (Instagram login wall; SkinCeuticals US Cloudflare challenge). Six differed, and in every case the site refused my fake Googlebot (Boots x2, Wikipedia, Little Wonderland NL, Amazon US,
Amazon UK). That is normal bot verification by IP address, the opposite of cloaking. **No cloaking was found.**

| Page | Class | Chrome UA | Googlebot UA | Note |
|---|---|---|---|---|
| stonevillenc.org/medicube-pdrn-pink-peptide-serum-stylevana-track/ | **SPAM** | no connection (4+ attempts) | no connection | Domain home page is the Town of Stoneville, NC: 656 words of town-hall content, zero mentions of PDRN, identical for both agents. The PDRN URL's SERP snippet (dated 8 Sep 2026) is Medicube serum copy. A US town site carrying Korean-skincare copy is unrelated content, consistent with an injected page on a hacked domain; I could not read the page itself. |
| instagram.com/p/DdVuiLmDmnb/ and two reels | UGC | 200, 0 readable words | 200, 0 readable words | Login wall. Cannot be measured. |
| ulta.com/p/pdrn-pink-peptide-eye-serum... | RETAILER | 200, 1.41 MB | 200, 1.41 MB | Same text |
| thestylelist.in/post/pdrn-is-taking-over-skincare | EDITORIAL | 200 | 200 | Same text (1,424 vs 1,425 words) |
| intl.skinceuticals.com/en_IN/pdrn.html | BRAND | 200 | 200 | Same text. The US page `www.skinceuticals.com/pdrn.html` returns a Cloudflare "Just a moment" challenge to both agents (403), so it was not measured; I used the international twin, which is the page that ranks #1 for "what is pdrn" [SERP]. |
| kiokii.com blog | BRAND (store blog) | 200 | 200 | Same text |
| navaaesthetics.com | MEDICAL (aesthetics clinic) | 200 | 200 | Same text |
| allure.com, cosmopolitan.com, the-independent.com | EDITORIAL | 200 | 200 | Same text |
| olivekollection.com/collections/pdrn | RETAILER | 200 | 200 | Same text |
| bronzeom.com (VT PDRN Cream 100) | RETAILER (Omani Shopify store, prices in OMR) | 200 | 200 | Same text |
| itgirlies.com, beautybypeptides.com | EDITORIAL (affiliate) | 200 | 200 | Same text |
| officialyuri.com, houseofcommunal.com, theinkeylist.com, getrael.com, sulskin.com | BRAND | 200 | 200 | Same text |
| egskinclinic.co.uk | MEDICAL (dermatology clinic) | 200 | 200 | Same text |
| skincupid.co.uk, thekbeautyedit.co.uk, beautyfashionshop.nl, cultbeauty.com/.co.uk | RETAILER | 200 | 200 | Same text |
| boots.com (blog and collection) | RETAILER | 200 but a 6 KB "Pardon Our Interruption" bot page | 403 | Not measured |
| littlewonderland.nl | RETAILER | 200 | 403 | Blocks spoofed Googlebot |
| loreal-paris.de, marudermcosmetics.com | BRAND | 200 | 200 | Same text |
| pdrn-skin.com/?lang=de | BRAND (small store, home page) | 200 | 200 | Same text |
| dr-jetskeultee-skincare.nl | BRAND (hosts a reprinted magazine interview) | 200 | 200 | Same text |
| amazon.com, amazon.co.uk (search results) | MARKETPLACE | 200 / 503 | 200 | Search-result pages, not content |
| pmc.ncbi.nlm.nih.gov/articles/PMC5405115, en.wikipedia.org | MEDICAL / reference | 200 | 200 / 403 | AIO sources |
| skinlaundry.com/blog/PDRN | BRAND | 200 | 200 | Article sits only in the Next.js data blob (client-rendered); 16 words in plain HTML |

### 2.2 What I could not measure (stated once, applies throughout)

- **Brand search demand, referring-domain counts and Domain Rating for competitors:** needs paid tools. I used [TRANCO] rank as a popularity proxy and WebSearch for news and Reddit signals. WebSearch ignores `site:`, so Reddit counts per brand are not available.
- **Competitor page speed:** the free PageSpeed API returned a daily quota error for all 3 attempts. Only our own Lighthouse data exists.
- **Boots, SkinCeuticals US, Instagram, Amazon UK:** blocked to my fetches; classified from the SERP only.
- **Our Dutch hub:** not fetched (5-fetch cap). The German hub was fetched; the Dutch hub is built from the same template (`configs/hub-i18n/pdrn-research.json`), so its structure is inferred, not measured.
- **Word counts** are main-content words from trafilatura. On collection and category pages the product grid is stripped, so those counts are low by design (product counts come from links in the HTML instead).
- **The "covers X" flags** (polynucleotides, injections, side effects, how to use) are text matches plus headings. They say "mentioned" or "has its own heading", not how well it is covered.
- **Volumes:** US/GB/DE observed figures are from [KS]. NL has no observed figure in the strategy; I quote the Ads bucketed figure and label it.

---

## 3. Where our PDRN pages stand today

### 3.1 Indexing [INSPECT]

| URL | Google status | Last crawl |
|---|---|---|
| /pages/pdrn-research (EN hub) | **URL is unknown to Google** | none |
| /de/pages/pdrn-research | Submitted and indexed | 2026-09-05 |
| /nl/pages/pdrn-research | Submitted and indexed | 2026-09-10 |
| /products/pdrn-renewal-serum | Submitted and indexed | 2026-10-05 |
| /products/pdrn-collagen-night-cream | Submitted and indexed | 2026-09-28 |
| /collections/pdrn | Submitted and indexed | 2026-10-06 |
| /blogs/clinical-studies/pdrn-vs-retinol-split-face-trial-ye-2026 | Submitted and indexed | 2026-10-04 |
| /blogs/clinical-studies/pdrn-microneedling-split-face-trial-yogya-2022 | **Unknown to Google** | none |

The other four English hubs (argireline, copper peptide, matrixyl, glutathione) are all indexed [INSPECT]. So the PDRN hub is not blocked by a site-wide fault. What I verified about the English hub [FETCH]: no robots meta tag, self-canonical, hreflang for en/de/nl/fr/es/it
present, listed in `sitemap_pages_1.xml`, linked from the homepage (2 links), the PDRN collection (3), both product pages (3 each), the study article (8) and /pages/the-science (3). Lighthouse also reports it crawlable [LH]. Why Google has not discovered it is **not
established**. Hypotheses to test, none verified: (1) the Search Console Pages report may show "Discovered, currently not indexed"; (2) a crawl-demand problem on a site that earned 5,288 impressions and 78 clicks in 90 days [GSC]; (3) the API inspected a URL variant. First action
is a manual Request Indexing and a look at the Pages report.

### 3.2 What Google already shows for our PDRN pages [GSC] (window 2026-07-07 to 2026-10-05, all countries)

| Page | Impressions | Clicks | Avg position |
|---|---|---|---|
| /pages/study/pdrn-vs-retinol... (old URL) | 92 | 1 | 5.8 |
| /products/pdrn-collagen-night-cream | 88 | 2 | 8.9 |
| /products/pdrn-renewal-serum | 70 | 1 | 4.5 |
| /blogs/clinical-studies/pdrn-vs-retinol... (current URL) | 53 | 2 | 7.0 |
| /nl/pages/pdrn-research | 36 | 1 | 36.1 |
| /collections/pdrn | 8 | 0 | 4.8 |
| /de/pages/pdrn-research | 3 | 0 | 6.3 |
| /pages/pdrn-research (EN hub) | none | none | none |

Query level (last 28 days) [GSC]: "pdrn" appears only for the Dutch hub (18 impressions, position 52). "pdrn serum" appears only for the German product page (3 impressions, position 7). "pdrn night cream" gives the cream page 10 impressions at position 7.7. Our domain appears in
none of the 13 SERPs I pulled [SERP]. All of these are tiny numbers; they show Google can place us, not that we compete.

Technical flag: Google still shows more impressions on the **old** `/pages/study/...` URL than on the current `/blogs/clinical-studies/...` URL [GSC]. I could not fetch the old URL (fetch cap). Confirm it 301-redirects to the current URL.

### 3.3 Speed [LH] (mobile lab, one run each, no field data available)

| Page | Performance score | LCP | TBT | Page weight | Requests |
|---|---|---|---|---|---|
| EN hub | 72 | **7.8 s** (score 3) | 10 ms | 2,654 KiB | 319 |
| PDRN serum product page | 60 | 4.9 s | 540 ms | 3,902 KiB | 336 |

Competitor speed: not measured (see 2.2).

### 3.4 Links [BL]

DataForSEO shows 660 backlinks from 627 referring domains, rank 0, backlink spam score 52, first seen 2023-10-14. Link TLDs: .store 97, .online 94, .site 93, .shop 92, .website 90, .space 85, .com 31, .ru 22. Of the 100 most recent referring domains, all have spam score 45 to 75
(84 at 55, 14 at 45, 1 at 60, 1 at 75) and rank 0; they are automated "SEO checker" and "free backlinks" domains. Only 2 referring links are from the US. **Genuine referring domains: none found.**

### 3.5 Popularity of the domains that outrank us [TRANCO]

| Domain | Rank | Domain | Rank |
|---|---|---|---|
| instagram.com | 11 | reddit.com | 106 |
| cosmopolitan.com | 3,306 | vogue.com | 3,209 |
| ulta.com | 4,759 | boots.com | 10,165 |
| glamour.com | 9,540 | allure.com | 11,443 |
| the-independent.com | 13,608 | cultbeauty.com | 48,365 |
| skinceuticals.com | 87,031 | dermatologytimes.com | 119,256 |
| medicube.us | 147,458 | theinkeylist.com | 250,654 |
| loreal-paris.de | 267,094 | kiokii.com | 406,019 |
| littlewonderland.nl | 457,115 | officialyuri.com | 472,701 |
| skinlaundry.com | 581,405 | skincupid.co.uk | 600,460 |
| getrael.com | 743,849 | olivekollection.com | 949,880 |
| dr-jetskeultee-skincare.nl | 997,626 | beautyfashionshop.nl | 2,046,499 |
| bronzeom.com | 4,062,358 | sulskin.com | 4,275,589 |
| Not in list: navaaesthetics.com, thestylelist.in, itgirlies.com, beautybypeptides.com, houseofcommunal.com, egskinclinic.co.uk, thekbeautyedit.co.uk, marudermcosmetics.com, pdrn-skin.com, skingenetix.com | | | |

Read this as: big brands and publishers win the head terms, but a dozen small or unranked sites hold top-3 slots, so authority is a handicap, not a wall.

---

## 4. The SERPs side by side [SERP]

AIO = AI Overview. "UGC in top 3" counts Reddit, YouTube, Instagram, LinkedIn, TikTok. Volumes are observed monthly searches from [KS] unless marked.

| Term | Volume | Organic results listed | UGC in top 3 | AIO | Other features |
|---|---|---|---|---|---|
| pdrn (US) | 19,734 | 6 | 1 (plus spam at #2) | yes | PAA, perspectives, product considerations, short videos, video |
| what is pdrn (US) | 5,602 | 7 | 0 | yes | PAA, perspectives, video |
| pdrn serum (US) | 3,936 | 6 | 0 | yes | images, popular products, product considerations, PAA, video |
| pdrn skincare (US) | 1,817 | 8 | 1 | yes | popular products, PAA, video |
| pdrn cream (US) | 2,321 | 8 | 2 | yes | shopping, popular products, images, PAA |
| best pdrn serum (US) | 1,042 | 7 | 2 | yes | discussions and forums, images, PAA |
| pdrn vs retinol (US) | none measurable yet | 7 | 2 | yes | images, video, PAA |
| pdrn (GB) | 6,462 | 8 | 0 | yes | PAA, video |
| pdrn serum (GB) | 2,049 | 9 | 0 | **no** | popular products, PAA, video |
| pdrn (DE) | 4,650 | 8 | 0 | yes | PAA, video |
| pdrn serum (DE) | 845 | 9 | 0 | no | PAA, people also search, video |
| pdrn (NL) | 1,900 (Ads, bucketed) | 8 | 0 | yes | PAA, video |
| pdrn serum (NL) | 1,000 (Ads, bucketed) | 10 | 0 | no | popular products, PAA |

### 4.1 What the AI Overviews cite (7 US terms) [SERP]

| Source | Terms citing it (of 7) |
|---|---|
| YouTube (4 videos; "Does PDRN Really Do Anything?" alone is cited on 4 terms) | 6 |
| Reddit (r/AsianBeauty "Thoughts on PDRN as a topical skincare ingredient" alone is cited on 3) | 5 |
| skinceuticals.com/pdrn.html | 3 |
| theinkeylist.com (/pages/pdrn on 2; /blogs/news/pdrn-vs-retinol in 4 locale versions on the retinol term) | 3 |
| ulta.com/discover/skin/best-pdrn-serums | 3 |
| Instagram reel DXfJsmDERtm | 3 |
| pmc.ncbi.nlm.nih.gov/articles/PMC5405115 (the Squadrito 2017 review) | 2 |
| cultbeauty.com/blog/what-is-pdrn | 2 |
| skinlaundry.com/blog/PDRN | 2 |
| vogue.com/article/best-pdrn-serum | 2 |
| allure.com (what-is-pdrn on 1, best-pdrn-serums on 1) | 2 |
| Wikipedia, a USC student magazine, a med-spa blog, a K-beauty store blog | 1 each |

GB and DE AIOs cite Boots (3 pages), Cult Beauty UK, Marie Claire UK, Skin Cupid, dm, Douglas, Lancôme DE, Maruderm and retailer collections [SERP]. NL AIO cites NL clinics and K-beauty retailers.

### 4.2 People-Also-Ask questions that recur [SERP]

| Question | SERPs (of 13) |
|---|---|
| Is PDRN salmon sperm? | 5 |
| Do PDRN serums actually work? | 4 |
| Is PDRN good for your skin? | 2 |
| How much does a PDRN shot cost? | 2 |
| What not to mix with PDRN cream? | 2 |
| Wann sollte man PDRN anwenden? (DE) | 2 |

Single-SERP questions worth answering: Is PDRN the same as retinol? Can you use retinol and PDRN together? What do dermatologists say about PDRN? Which PDRN serum is best for microneedling? How to use salmon PDRN serum? When to put on PDRN cream? Does PDRN stimulate hair growth?
(GB) How long do the effects last? (GB) Was macht PDRN? Für was ist PDRN gut? Ist PDRN Anti-Aging? Wat is PDRN? Wat zijn de nadelen van de PDRN-behandeling? Wat is een PDRN-behandeling? Wat is het beste PDRN-serum?

"What works 11 times faster than retinol?" in the retinol SERP refers to INKEY's retinal serum, not PDRN (INKEY page text) [FETCH].

---

## 5. What the pages Google rewards have in common (measured, 30 pages)

| Pattern | Pages that do it [FETCH] | Our EN hub |
|---|---|---|
| Definition in the opening lines | SkinCeuticals ("PDRN, or Polydeoxyribonucleotide, is a biopolymer derived from the DNA of salmon"), Kiokii, Cult Beauty, INKEY, Allure, L'Oréal DE (TL;DR bullets) | Definition is the first paragraph under "What Is PDRN?", but 117 words of result tiles come first |
| Question-style headings that mirror People-Also-Ask | Kiokii (8 question lines), House of Communal (13), L'Oréal DE (10), Beautyfashionshop NL (10), Maruderm DE (61) | FAQ block only; no question H2 for "Is PDRN salmon sperm?" or "Do PDRN serums work?" |
| Concentration stated | INKEY (2% = 20,000 ppm; "Concentration Matters" and "What is PPM in PDRN?" headings), Kiokii (ppm explainer: 10,000 ppm = 1%), Beauty By Peptides (Medicube "10,000 ppm, which is 1% salmon PDRN", called "the only product here that discloses a concentration") | Yes: "What 1% PDRN Means" (1% = 10,000 ppm) |
| Salmon vs plant-derived PDRN addressed | INKEY (vegan, from Artemisia capillaris, "No salmon"), Kiokii, L'Oréal DE (vegan PDRN+ from magnolia flowers), Beauty By Peptides | Two sentences; no own heading |
| Fresh visible dates | INKEY (12 May 2026), Cult Beauty (updated 2026-09-14), L'Oréal DE (2026-09-29, modified 09-30), Beautyfashionshop NL (6 Oct 2026), Beauty By Peptides (modified 2026-10-02), Maruderm (modified 2026-10-07, today) | "Last reviewed 24 September 2026"; no "published" date |
| Product next to the explanation | INKEY (14 product links, PDRN serum $18 for 30 ml), Kiokii (4 picks with prices), Official YURI (8 products, 10 prices) | 3 product cards at the foot |
| Linked studies | Only 8 of 30 pages link any study. Most: Allure 4, L'Oréal DE 3. | 5 external study links, 4 studies in a graded table. Best on the measured set. |
| Named medical reviewer | **None of the 30** | Yes (Dr Esther Bodde, Cosmetic & Medical Physician) |
| Cites the Ye 2026 PLOS ONE trial | **None of 33 readable competitor files, and not Wikipedia** | Yes, it is the centrepiece |

Weak spots we can copy-fix: no page of ours has a question heading for the top PAA question, no standalone side-effects section, no heading for "PDRN vs polynucleotides" (Cult Beauty, Maruderm and Beautyfashionshop all have one), no published date, and no vegan-PDRN section.

---

## 6. Term-by-term teardown

Reading guide for each comparison table: "Opens with definition" judges the first paragraph under the H1. "Studies" means unique links to PubMed, PMC, DOI or journal sites on the page. JSON-LD lists the types found. "Covers" means mentioned (M) or has its own heading (H). All
figures [FETCH] unless tagged.

### 6.1 "pdrn" (US), 19,734 observed searches per month [KS]

**Top results [SERP]**

| Rank | Page | Class | Note |
|---|---|---|---|
| 1 | instagram.com/p/DdVuiLmDmnb | UGC | "PDRN skincare is EVERYWHERE right now... but is it" |
| 2 | stonevillenc.org/medicube-pdrn-pink-peptide-serum-stylevana-track | **SPAM** (skipped) | Hacked town site, see 2.1 |
| 3 | ulta.com/p/pdrn-pink-peptide-eye-serum-pimprod2053535 | RETAILER | Medicube eye serum, "Online only $22.90" |
| 4 | instagram.com/reel/DT5Bdz5jg3x | UGC | |
| 5 | thestylelist.in/post/pdrn-is-taking-over-skincare | EDITORIAL | First measurable editorial result |
| 6 | instagram.com/reel/DNQkzunzB3J | UGC | |

Only 6 organic results exist. Features: AIO, PAA, perspectives, product considerations, short videos, video [SERP]. PAA: Is PDRn salmon sperm? / Is PDRN good for your skin? / How much does a PDRn shot cost? / Is PDRN the same as retinol? [SERP].
**AIO cites (10):** PMC5405115, Allure (what-is-pdrn), skinceuticals.com/pdrn.html, Wikipedia, YouTube (2 videos), Skin Laundry blog, Cult Beauty UK blog, INKEY /pages/pdrn, an Instagram reel [SERP].
Our page: the English hub, not indexed.

| Factor | Ulta eye serum (#3) | The Style List (#5) | Ours: EN hub |
|---|---|---|---|
| Page type | Retailer product page | Editorial article | Research hub |
| Title / H1 | "medicube - PDRN Pink Peptide Eye Serum \| Ulta Beauty" / "medicube PDRN Pink Peptide Eye Serum" | "PDRN Is the Regenerative Skincare Ingredient Taking Over This Season, Here's Why Dermatologists Want You to Know About It" (title = H1) | "What Is PDRN? Salmon DNA Skincare Benefits and Research" (55 chars) / "PDRN: Salmon DNA Skincare" |
| Main-content words | about 430 | 1,424 | 2,237 |
| Opens with definition | No (product summary) | No (trend intro; definition in first section) | Partly (tiles first, definition after 117 words) |
| Studies linked | 0 (brand-run "clinical trial tested" note, no link) | 0 | 5 links; 4 studies in table |
| Tables | 0 | 0 | 2 |
| FAQ | No | No | Yes, 6 Q&As, FAQPage schema |
| Author / reviewer | None / none | Alvira Dsouza (JSON-LD); two named dermatologists quoted; no reviewer line | Malcolm Smith byline; "Medically reviewed by Dr Esther Bodde, Cosmetic & Medical Physician" |
| Visible date | None | "Updated: May 29" (JSON-LD 2026-05-27, modified 05-29) | "Last reviewed 24 September 2026" |
| JSON-LD | Product, Offer, AggregateRating, Review, BreadcrumbList | BlogPosting, Person, Organization, ImageObject | WebPage, FAQPage, ScholarlyArticle, Person, Organization, BreadcrumbList |
| Images / video | 10 / 0 | 9 / 0 | 22 / 0 |
| Products and prices | 1 product, $22.90 [SERP] | 1 product link, no prices | 3 product cards, prices shown |
| Reviews shown | 4.2 average, 18 reviews (JSON-LD) | None | None |
| Concentration and salmon | No %; "PDRN (Salmon DNA)" | One "10,000ppm" mention; salmon yes | 0.1% in the trial, 1% in our products, 1% = 10,000 ppm; chum salmon (Oncorhynchus keta) |
| Covers | Polynucleotides no; injections no; side effects M ("hypoallergenic"); how to use H | Polynucleotides no; injections M; side effects M; how to use M | Polynucleotides M; injections M (FAQ); side effects M (evidence card, Safety bullet); how to use H |

**Why they outrank us**

- (a) Authority and brand: Instagram (Tranco 11) takes 3 of 6 listed slots; Ulta is a national retailer (4,759) selling the brand people actually search for. "medicube pdrn pink peptide serum" carries 33,100 US searches (Ads, bucketed) against 49,500 for "pdrn"; across the US
  PDRN Ads rows, brand-name queries (Anua, Medicube, Rejuran, VT and similar, my heuristic list) are about 41% of volume [keywords-us-2026-09-22.json]. So "pdrn" is partly a brand-intent query. Press: Allure, Cosmopolitan and The Independent all published PDRN explainers in 2025
  to 2026 [FETCH].
- (b) Content: not the reason. The #5 editorial result has no linked study and is outside the Tranco top 1 million. Our hub beats it on every measured content factor.
- (c) SERP features: an AI Overview, perspectives, short videos and a video block sit above or around 6 organic results; Instagram video takes half of them.
- (d) Technical: the hub is unknown to Google [INSPECT]; mobile LCP 7.8 s [LH].

**What the hub must change to compete here.** Target the #5 to #8 informational slots and the AI Overview, not Ulta or Instagram.

1. Get it indexed (section 7, action 1).
2. Put a 40 to 60 word definition directly under the H1, before the three tiles: what PDRN is, where it comes from, the label name (Sodium DNA), and the one-line evidence status. Keep the tiles below it.
3. Change the H1 to "What Is PDRN? Salmon DNA skincare, explained" so the H1 matches the title and the head term (Cult Beauty and INKEY use "What is PDRN?" as H1).
4. Add an H2 "Is PDRN really salmon sperm?" with a two-sentence answer using wording the hub already supports ("extracted from the sperm cells of chum salmon and purified to remove proteins, leaving DNA fragments"). It is the PAA question on 5 of 13 SERPs.
5. Add a visible "Published" date next to "Last reviewed", and an `Article` node with `datePublished`, `dateModified`, `author`, `reviewedBy`.
6. Link the PMC full text of the Squadrito 2017 review (PMC5405115) next to the existing PubMed link. That PMC page is cited by the AI Overview on 2 of the 7 US terms [SERP].
7. Fix the 7.8 s mobile LCP [LH].

**Off-page for this term:** the AI Overview leans on YouTube (6 of 7 US terms), Reddit (5) and Instagram (3). See section 7, actions 3 to 5.

### 6.2 "what is pdrn" (US), 5,602 [KS]

**Top results [SERP]:** #1 intl.skinceuticals.com/en_IN/pdrn.html (BRAND, the India-locale page ranking on the US SERP), #2 kiokii.com blog (BRAND), #3 navaaesthetics.com (MEDICAL), #4 unni.app, #5 justmylook.com blog (Medicube range), #6 banyanandbamboo.com (med-spa blog), #7 a Facebook post.
Features: AIO, PAA, perspectives, related searches, video. PAA: Is PDRn salmon sperm? / What do dermatologists say about PDRn? / Is retinol better than PDRn? / How much does a PDRn shot cost? [SERP].
**AIO cites (13 unique pages):** PMC5405115, Reddit r/AsianBeauty ("Thoughts on PDRN as a topical skincare ingredient"), skinceuticals.com, YouTube (3 videos), Cult Beauty, INKEY /pages/pdrn, Skin Laundry, Artisan Skin and Laser blog, a USC Dornsife student-magazine
article (24 Apr 2026), an Instagram reel [SERP].
Our page: the English hub (same page as 6.1).

| Factor | SkinCeuticals intl (#1) | Kiokii (#2) | Nava Aesthetics (#3) | Ours: EN hub |
|---|---|---|---|---|
| Page type | Brand ingredient page with FAQ accordion | Brand store blog post | Aesthetics-clinic blog post | Research hub |
| Title / H1 | "What is PDRN and Benefits of PDRN Skincare \| SkinCeuticals" / "PDRN" | "What Is PDRN? Salmon DNA Skincare, Honestly Explained - Kiokii and..." / "What Is PDRN? Salmon DNA Skincare, Honestly Explained" | "PDRN Explained: The Future of Skin Regeneration" / "What Is PDRN & Why It's the Next Big Thing in Skin Regeneration" | "What Is PDRN? Salmon DNA Skincare Benefits and Research" / "PDRN: Salmon DNA Skincare" |
| Main words | about 205 plus the FAQ | 1,351 | 1,042 | 2,237 |
| Opens with definition | Yes | Yes ("a purified fragment of DNA, usually taken from salmon or trout") | No ("If your skin looks dull even after consistent skincare...") | Partly |
| Studies | 0 | 2 (PMC5405115, PMC6027320) | 0 | 5 |
| Tables | 0 | 1 | 0 | 2 |
| FAQ | Yes, 3 questions, no schema | Yes (H2) | No | Yes, schema |
| Author / reviewer | None / none | Brand name only; none | JSON-LD author is "SEO LoginUser" (a CMS login); none | Named author; named medical reviewer |
| Visible date | None | Published 13 Aug 2026, updated 17 Aug 2026 | In JSON-LD only (24 Feb / 29 Aug 2026) | Reviewed 24 Sep 2026 |
| JSON-LD | BreadcrumbList, SiteNavigationElement | Article, BreadcrumbList, Organization, Person, WebPage | BlogPosting, Organization, Place, PostalAddress, WebSite | WebPage, FAQPage, ScholarlyArticle, Person, Organization |
| Images / video | 1 / 0 | 3 / 0 | 2 / 0 | 22 / 0 |
| Products and prices | None in the HTML | 4 picks with prices | None | 3 cards |
| Reviews shown | None | None | None | None |
| Concentration and salmon | No %; salmon yes | ppm explainer (10,000 ppm = 1%); salmon or trout, fish milt | No %; salmon yes | Yes / yes |
| Covers | Injections M (also "PDRN vs filler" FAQ) | Injectable vs skincare H; plant PDRN M; routine H; "salmon sperm" H | Injections M | See 6.1 |

**Why they outrank us**

- (a) Authority and brand: SkinCeuticals (Tranco 87,031, L'Oréal-owned) sells an actual PDRN product, the Phyto Corrective PDRN Visible-Redness-Reducing Serum 30 ml, stocked at Cult Beauty and LookFantastic [WEB:
  cultbeauty.com/p/skinceuticals-phyto-corrective-pdrn-visible-redness-reducing-serum-30ml/17886927/]. Its 205-word page is thin; it ranks on brand and entity strength. Kiokii (406,019) is a mid-size K-beauty store; Nava (not listed) is a clinic.
- (b) Content: Kiokii is better than us on one thing, a direct opening definition plus a concentration explainer in plain words. We beat all three on evidence.
- (c) SERP features: AIO cites SkinCeuticals on 3 of 7 US terms. Google also surfaces expert-credentialed sources here (a med-spa, a university student magazine), so our named medical reviewer is an asset once indexed.
- (d) Technical: ours is not indexed; all three of theirs are.

**What the hub must change:** items 2 to 6 from 6.1, plus these H2s (each answers a measured question): "Is PDRN the same as polynucleotides?" (Cult Beauty has it as an H3, Maruderm and Beautyfashionshop NL as H2), "PDRN injections vs creams" (Kiokii, EG Skin, Maruderm all have a
heading), "Salmon PDRN vs plant-derived (vegan) PDRN" (INKEY's whole proposition), and "PDRN side effects and who should avoid it" (INKEY and Cosmopolitan have one). For "What do dermatologists say about PDRN?" add one attributed sentence from Dr Bodde only with her agreement.

### 6.3 "pdrn serum" (US), 3,936 [KS]

**Top results [SERP]:** #1 allure.com/story/what-is-pdrn-skin-care-salmon-sperm (EDITORIAL), #2 olivekollection.com/collections/pdrn (RETAILER), #3 the-independent.com best-pdrn-serum (EDITORIAL), #4 Cult Beauty blog, #5 getthegloss.com, #6 Nordstrom ingredient-filtered browse page.
Features: AIO, images, popular products, product considerations, perspectives, PAA, video. PAA: Which PDRN serum is best for microneedling? / What are some good Korean skin serums? / How to use salmon pdrn serum? / Does medicube pdrn serum really work? [SERP].
**AIO cites (9):** an Amazon search page, Ulta "best-pdrn-serums", Allure "best-pdrn-serums", Reddit r/AsianBeauty, a brand product page (seshaskin.com/products/pdrn-regenerative-serum), YouTube, 3 Google Shopping product cards [SERP].
Our page: /products/pdrn-renewal-serum (indexed).

| Factor | Allure (#1) | Olive Kollection (#2) | The Independent (#3) | Ours: serum page |
|---|---|---|---|---|
| Page type | Magazine explainer | Retailer collection (48 product links) | Affiliate "best of" list | Product page |
| Title / H1 | "PDRN Has Quickly Taken Over Skin Care \| Allure" / same | "PDRN Korean Skincare - Shop Salmon DNA Toners, Serums, Creams & Masks \| Olive Kollection" / H1 is just "Olive Kollection" | "Best PDRN Serums for 2026, According to Dermatologists \| The Independent" / "Best PDRN serums according to dermatologists" | "PDRN Serum 1% with Salmon DNA \| Skingenetix" (43 chars) / "PDRN 1% Renewal Serum" |
| Main words | 2,545 | about 66 | about 955 | 363 |
| Opens with definition | Yes | No | No (affiliate notice first) | No (product pitch) |
| Studies | 4 (PMC11994882, PMC5098534, PMC5405115, NCBI NBK195888) | 0 | 0 | 0 (page says a clinical study beat retinol, with no citation) |
| Tables | 0 | 0 | 0 | 0 |
| FAQ | No (6 of 7 H2s are questions) | No | No | Yes, 6 Q&As, schema |
| Author / reviewer | Elizabeth Siegel (JSON-LD); cosmetic chemist Perry Romanowski quoted; no reviewer | None | Sophie Wirt (JSON-LD); "according to dermatologists"; no reviewer | None |
| Visible date | Yes (2026-04-30) | None | JSON-LD only (2026-04-08) | None |
| JSON-LD | NewsArticle, BreadcrumbList, Person, Organization | Organization only | NewsArticle, ItemList, Product, Offer, Person | Product, Offer, Brand, FAQPage, BreadcrumbList |
| Images / video | 5 / 0 | 97 / 0 | 1 / 0 | 24 / 0 |
| Products and prices | "Shop our PDRN product picks" section | 48 product cards with prices | 9 prices visible | 1 product; Offer EUR 69.00 in my fetch (market-dependent) |
| Reviews shown | None | None | None | None (no rating markup) |
| Concentration and salmon | No %; salmon 18 mentions | No; salmon in product names | No %; salmon yes | 1%; salmon yes (5 mentions) |
| Covers | Injections M; "Does PDRN skin care work?" H | None | Injections M; side effects M | How to use H ("3 Simple Steps") |

**Why they outrank us**

- (a) Authority: Allure (11,443) and The Independent (13,608) are national publishers. Olive Kollection (949,880) is not, and still takes #2.
- (b) Content and page type: Olive's page is 66 words with 48 products and 97 images. For this commercial-research term Google is rewarding category depth and product schema, not copy. The Independent's page carries ItemList plus Product schema and 9 visible prices. A single
  363-word product page is not the shape of any of the top three.
- (c) SERP features: "popular products" and "product considerations" are Google's shopping surfaces, and the AI Overview cites a brand's product page (Sesha Skin) and Shopping cards. Product pages can be cited, but they need a product feed, price and ratings.
- (d) Technical: indexed (crawled 2026-10-05) [INSPECT], but mobile performance score 60, LCP 4.9 s, total blocking time 540 ms, 3.9 MB [LH], and no rating markup.

**What the serum page must change**

1. State the strength at the top in plain words: "1% PDRN (10,000 ppm)". The hub already does.
2. Add an evidence block with links: the Ye 2026 DOI and the hub. Right now the page makes a head-to-head claim with no source on the page. The trial used a 0.1% eye cream; say so (the hub does).
3. Add genuine reviews into server-rendered markup (`aggregateRating` and `review`) only if the reviews are real and verifiable; the Klaviyo widget is client-side and invisible to machines (store memory note).
4. Answer three PAA questions on the page: "How to use salmon PDRN serum?", "Which PDRN serum is best for microneedling?" (we sell a microneedling stamp set and the Yogya microneedling appraisal exists), "What not to mix with PDRN?".
5. Cut page weight and blocking script: target LCP under 2.5 s on mobile.
6. Be in the lists, off-page: Allure "best-pdrn-serums", Ulta, Vogue, Glamour, The Independent are what the AI Overview cites (section 7, action 3).

Context only: the serum is EUR 69.00 in my fetch against INKEY's $18 for 30 ml [FETCH]. The page needs value proof (strength, evidence, what is different), not just keywords.

### 6.4 "pdrn skincare" (US), 1,817 [KS]

**Top results [SERP]:** #1 Reddit r/AsianBeauty "Thoughts on PDRN as a topical skincare ingredient" (UGC), #2 skinceuticals.com/pdrn.html (BRAND), #3 cosmopolitan.com (EDITORIAL), #4 INKEY /pages/pdrn (BRAND), #5 Nordstrom filtered browse page, #6 an Amazon search page, #7
Dermatology Times "Social media mythbusters: PDRN serums" (MEDICAL trade press), #8 prevention.com.
Features: AIO, PAA, popular products, related searches, video. PAA: Is PDRN good for your skin? / Is PDRn salmon sperm? / Do PDRN serums actually work? / Does salmon pdrn actually work? [SERP].
**AIO cites (11):** Reddit, SkinCeuticals, Ulta list, YouTube (3 videos), Cult Beauty, an Instagram reel, 3 Google Shopping cards [SERP].
Our page: /collections/pdrn (indexed).

| Factor | SkinCeuticals (#2; intl twin measured) | Cosmopolitan (#3) | INKEY /pages/pdrn (#4) | Ours: /collections/pdrn |
|---|---|---|---|---|
| Page type | Brand ingredient page | Magazine explainer with a dermatologist | Brand ingredient hub with product | Collection (3 products) |
| Title / H1 | See 6.2 | "What is PDRN Skincare? A Dermatologist Breaks Down the Trend" / "What Is PDRN Skincare, and Does It Actually Have Real Salmon Sperm in It?" | "PDRN: Benefits, How to Use & Best Products \| The INKEY List" / "What is PDRN?" | "PDRN Skincare: Salmon DNA Serum and Night Cream" (47 chars) / "PDRN" |
| Main words | about 205 | 1,131 | 3,403 | 38 |
| Opens with definition | Yes | No (hook; definition under first H2) | Yes, plus a "Quick Facts" box | No (one line, link to hub) |
| Studies | 0 | 0 | 0 (footnote: "studies completed using 2% INJIN PDRN, ran by the ingredient supplier") | 0 |
| Tables | 0 | 0 | 6 | 0 |
| FAQ | Yes, no schema | No (question H2s) | Yes, FAQPage | None |
| Author / reviewer | None | Beth Gillette (JSON-LD); Dr Melda Isaac, MD named in "Meet the expert"; no reviewer | "David, askINKEY Digital Skincare Advisor" (not a credentialed expert); no reviewer | None |
| Visible date | None | 2025-09-02, never modified (about 13 months old) | Published 12 May 2026, updated 12 May 2026 | None |
| JSON-LD | Breadcrumb, nav | NewsArticle, Person | FAQPage, Question, Answer | BreadcrumbList only (no CollectionPage or ItemList) |
| Images / video | 1 / 0 | 22 / 1 | 41 / 1 | 12 / 0 |
| Products and prices | None in HTML | 1 product link | 14 product links; PDRN serum $18 for 30 ml | 3 products |
| Reviews shown | None | None | Customer-review block, no markup | None |
| Concentration and salmon | No / yes | No / yes (13 mentions) | 2% = 20,000 ppm; vegan, "No salmon" | 1% in product names; salmon 2 mentions |
| Covers | Injections M | Facials vs at-home H; "Is PDRN safe for sensitive skin?" H | Side effects H; how to use H; vs retinol, hyaluronic acid and exosomes H; concentration H | Nothing |

**Why they outrank us**

- (a) Authority: SkinCeuticals, Cosmopolitan (3,306), INKEY (250,654), plus Reddit as #1. INKEY's PDRN serum was the first product of its INKEYLab line (reviewed by January 2026), with trade coverage (CEW UK, TheIndustry.beauty) and a TikTok Shop launch [WEB:
  missljbeauty.com/2026/01/the-inkey-list-pdrn-serum-review.html, theindustry.beauty/inside-inkeylab-the-inkey-lists-new-fast-track-innovation-hub-for-next-gen-products-and-consumer-co-creation/].
- (b) Content and page type: **this SERP is an ingredient-guide SERP, not a collection SERP.** Collection-style pages appear only at #5 (Nordstrom) and #6 (Amazon). Our collection is the wrong page type for #1 to #4, and with 38 words and 3 products it cannot beat Nordstrom's or
  Amazon's either. [KS] section 4 assigns this term to the collection; today's US SERP does not support that.
- (c) SERP features: AIO cites SkinCeuticals, INKEY's hub and Cult Beauty's guide (all ingredient guides).
- (d) Technical: ours is indexed; it has no collection or item markup and no copy.

**What to change.** Decision for Malcolm: either (A) turn /collections/pdrn into an INKEY-pattern page, or (B) assign "pdrn skincare" to the hub and keep the collection as the transactional end point.
Recommended A-lite: 300 to 500 words of copy under the grid ("which PDRN product, serum or night cream", strength, how to use, side effects), 4 to 6 FAQ answers taken from the PAA above, `CollectionPage` plus `ItemList` markup, product prices and ratings on the cards, and a
visible link up to the hub for "what is PDRN". Check whether the bundles that already exist in the catalogue (PDRN serum and cream set, PDRN plus copper-peptide duo, complete routine, microneedling stamp set; all visible in GSC) belong in this collection. Our fetch shows 3
products [FETCH] [GSC].

### 6.5 "pdrn cream" (US), 2,321 [KS]

**Top results [SERP]:** #1 Reddit r/SkinbarrierLovers "What do you think about this PDRN cream" (UGC), #2 bronzeom.com VT PDRN Cream 100 (RETAILER), #3 YouTube short (UGC), #4 Reddit r/KoreanBeauty "Why a Korean doctor says PDRN does absolutely..." (UGC), #5 juliettearmand.com.au
PDRN Rejuvenation Cream (BRAND product page), #6 QVC community thread, #7 gopicky.com discussion, #8 LinkedIn post.
Features: AIO, shopping, popular products, images, PAA. PAA: What is the best PDRN product? / What not to mix with pdrn cream? / Is PDRn salmon sperm? / When to put pdrn cream? [SERP].
**AIO cites (8):** Reddit r/AsianBeauty, YouTube, skincupid.us Dr.Rejuall cream product page, thekoreanstyle.com guide, Vogue "best-pdrn-serum", 3 Google Shopping cards [SERP].
Our page: /products/pdrn-collagen-night-cream (indexed).

Six of the 8 listed results are forum, video or social posts (Reddit x2, YouTube, LinkedIn, QVC community, gopicky). Only Bronzeom among the top 3 is measurable.

| Factor | Bronzeom (#2) | Ours: night cream page |
|---|---|---|
| Page type | Retail product page, Omani Shopify store, price in OMR | Product page |
| Title / H1 | "VT - PDRN Cream 100 @ [Arabic text]" / same | "PDRN Cream 1% with Salmon DNA: Collagen Night Cream" (51) / "PDRN 1% Collagen Night Cream" |
| Main words | 167 | 422 |
| Opens with definition | No | No (product pitch) |
| Studies | 0 | 0 |
| Tables / FAQ | 0 / no | 0 / yes, 6 Q&As |
| Author / reviewer / date | None | None |
| JSON-LD | Product, Offer, Brand, Organization | Product, Offer (EUR 79.00 in my fetch), Brand, FAQPage, BreadcrumbList |
| Images / video | 21 / 0 | 23 / 0 |
| Reviews shown | None | None |
| Concentration and salmon | No %; **no salmon**: says PDRN "extracted from ginseng" | 1%; salmon yes (3 mentions) |
| Covers | How to use M (one line) | How to use H ("3 Simple Steps") |

**Why they outrank us**

- (a) Authority: Bronzeom is at Tranco 4,062,358. It is not authority.
- (b) Content: the commercial bar is very low. A 167-word page with no PDRN origin information ranks #2. What it has that we do not: an exact-match title ("PDRN Cream"), a known brand (VT) and Google Shopping eligibility (the `srsltid` tag on its URL shows it came through Merchant free listings).
- (c) SERP features: discussion intent dominates (6 of 8), plus a Shopping block and an AI Overview that cites a product page.
- (d) Technical: ours is indexed (position 7.7 for "pdrn night cream", 10 impressions [GSC]), and our Shopify product feed is live (GSC shows our URLs with `utm_source=google&utm_medium=product_sync&utm_campaign=sag_organic`, one at position 1 for "pdrn kollagen"). Missing:
  ratings, evidence on the page, speed.

**What to change:** add genuine review markup; answer "What not to mix with PDRN cream?" and "When to put on PDRN cream?" on the page; add "serum or cream?" guidance linking to the serum; link the evidence; use the exact phrase "PDRN cream" in a visible subhead; confirm brand and
GTIN in the feed. Participation on r/SkinbarrierLovers, r/KoreanBeauty and r/AsianBeauty has to be disclosed and useful, never promotional (section 7, action 4).

### 6.6 "best pdrn serum" (US), 1,042 [KS]

**Top results [SERP]:** #1 itgirlies.com (EDITORIAL, affiliate), #2 YouTube short, #3 Reddit r/30PlusSkinCare "Best PDRN serum", #4 officialyuri.com blog (BRAND), #5 beautybypeptides.com (EDITORIAL, affiliate), #6 theglowranking.com, #7 Reddit r/koreanskincare.
Features: AIO, discussions and forums, images, PAA. PAA: Do PDRN serums actually work? / What is the no. 1 serum in Korea? / Which is better, Anua PDRN serum or Medicube PDRN serum? / Which salmon PDRN is best? [SERP].
**AIO cites (7):** Reddit r/AsianBeauty, Glamour, Vogue, Ulta list, YouTube, 2 Google Shopping cards [SERP].
Our page: **none exists.** The strategy plans "Best PDRN serums, compared on concentration" [KS]; it is not built.

| Factor | ItGirlies (#1) | Official YURI (#4) | Beauty By Peptides (#5) | Ours |
|---|---|---|---|---|
| Page type | Affiliate list (byline "Scale Selling Corporation") | Brand store blog list | Independent affiliate comparison | No page |
| Title / H1 | "10 Best PDRN Skincare Products in 2026 \| Top PDRN Serums, Creams & Ampoules \| ItGirlies" / "10 Best PDRN Skincare Products in 2026" | "8 Best Pdrn Serum and Treatment Products for Skin Repair - Official YURI" / same | "Best PDRN Serums Compared: Medicube, COSRX, Anua & Mixsoon - Beauty By Peptides" / "...Medicube vs. COSRX vs. Anua vs. Mixsoon" | |
| Main words | 1,115 | 3,027 | 1,317 | |
| Opens with | A promise: compared by skin goal | Definition-style intro | A warning: "PDRN on the front of a bottle does not guarantee PDRN is inside it" | |
| Studies | 0 | 2 | 1 (Frontiers in Pharmacology 2017 DOI) | |
| Tables | 1 (quick comparison) | 1 | 1 (price, size, PDRN source, concentration disclosed, fragrance) | |
| FAQ | Yes, schema | Yes, schema | Yes | |
| Author / date | "The It Girl Editorial Team"; no date | "The YURI Skincare Team" plus About the Author; published 2026-07-29, modified 08-01 | No named author; published 2026-09-13, modified 2026-10-02 | |
| JSON-LD | Product, Review, FAQPage, Brand | Article, BlogPosting, FAQPage, Person | Article, Person, WebSite | |
| Products and prices | 10, no prices | 8, 10 prices | 4, with prices | |
| Concentration | None | None | Yes (Medicube 10,000 ppm = 1%) | |

**Why they outrank us**

- (a) Authority: the winners are small. ItGirlies and Beauty By Peptides are not in the Tranco list; Official YURI is 472,701. Authority is not what decides this SERP.
- (b) Content: they compare named products in a table. Beauty By Peptides wins on a distinctive angle, label reading, and says "a brand that discloses is usually a brand with something to disclose". **That is our angle**: Medicube discloses 1% (10,000 ppm); INKEY discloses 2%
  (20,000 ppm, vegan, supplier-run studies); we state 1%.
- (c) SERP: a forum block plus an AI Overview built on Reddit, Glamour, Vogue and Ulta's own list.
- (d) Technical: nothing to inspect; we have no page.

**What to build.** The article from [KS], but as "PDRN serums compared on what the label says", not a ranking with ourselves on top (we sell one of the products; disclose it at the top). Contents:

- Comparison table: product, PDRN source (salmon, plant, ginseng), declared strength, size, price, fragrance, evidence. Fill each cell only from the product's own label or INCI list; today I only have secondary sources (Beauty By Peptides, INKEY's page), so each cell must be
  verified before publishing.
- H2 "How to read a PDRN label" (INCI names: Sodium DNA, Milt Extract; ppm to % conversion).
- H2s answering the four PAA questions above, including a neutral "Anua vs Medicube" paragraph taken from labels only.
- Visible published and updated dates, named author, Dr Bodde review, linked sources.
This is a PDRN-specific exception to the strategy's "best X is publisher-owned" rule: three of the top 5 are small independents.

### 6.7 "pdrn vs retinol" (US), no measurable volume yet [KS]

**Top results [SERP]:** #1 houseofcommunal.com "Is PDRN Good for Acne-Prone Skin?" (BRAND blog), #2 LinkedIn post, #3 YouTube short, #4 Reddit r/45PlusSkincare, #5 YouTube short, #6 skinsort.com compare page (Rejuran products), #7 TikTok discover page.
Features: AIO, images, PAA, related searches, video. PAA: Can you use retinol and PDRN together? / Do PDRN serums actually work? / What works 11 times faster than retinol? / What not to mix with pdrn cream? [SERP].
**AIO cites (5):** INKEY "pdrn-vs-retinol" in four locale versions (www, uk, eu, ca) and Rael "pdrn-vs-retinol-for-wrinkles" [SERP].
Our page: /blogs/clinical-studies/pdrn-vs-retinol-split-face-trial-ye-2026 (indexed). It is not in the 7 listed results.

| Factor | House of Communal (#1) | INKEY vs-retinol (AIO) | Rael (AIO) | Ours: study article |
|---|---|---|---|---|
| Page type | Brand blog, about acne-prone skin | Brand blog | Brand blog | Clinical-study appraisal |
| Title / H1 | "Is PDRN Good for Acne-Prone Skin? Here's What the Science Says - Communal" / "...Everything You Need to Know" | "PDRN vs Retinol: Which Is Right for Your Skin? \| INKEY" / "PDRN vs Retinol: Two Approaches to Skin Regeneration" | "PDRN vs Retinol for Wrinkles - Rael" / same | "PDRN vs Retinol: The Ye 2026 Crow's-Feet Trial" (46) / "Can PDRN outperform retinol on crow's feet?" |
| Main words | 1,350 | 1,101 | 1,239 | 1,615 |
| Opens with | Acne worry, then definition in first H2 | One-line verdict ("PDRN gives you glow and barrier repair in days, retinol delivers deep anti-aging over months... or use both") | A reader scenario ("staring at two serums") | Result tile first (up to -23% vs about -6%) |
| Studies | 0 ("Research has shown..." unlinked) | 1 (PubMed 37959659, mechanism only; brand-run footnotes) | 0 | 2 (DOI and PubMed of the trial itself) |
| Tables / FAQ | 0 / yes (13 question lines) | 0 / yes, FAQPage | 1 / yes | 1 / yes, 6 Q&As |
| Author / reviewer | "Communal Team"; none | "askINKEY skincare advisor"; none | Jessica Cho (JSON-LD); none | "by Dr Esther Bodde, Cosmetic & Medical Physician"; medically reviewed |
| Dates | Published 2026-08-12 | Published 16 Jan 2026, modified 2026-09-10 | 2026-06-15, modified 08-03 | Published 2026-09-22, modified 2026-09-30 |
| Products | 1 link | 13 links (a $15 and a $22 retinoid serum listed with prices) | 1 link | 2 links |
| Head-to-head trial cited | No | No | No | **Yes (the only page of these four that does)** |

**Why they outrank us**

- (a) Authority: INKEY (250,654) fills 4 of the 5 AI Overview slots through its locale sites. Communal is not in the Tranco list and still holds #1, with a page that mentions retinol 8 times and has a sibling "pdrn-vs-retinol-indian-skin" post.
- (b) Content: ours is the better evidence, but the SERP rewards "which one do I use, can I use both" answers. Our article answers a narrower question (one trial, crow's feet), opens on a result tile, and has no "use together" section.
- (c) SERP features: UGC is 5 of 7; an AI Overview built on two brand blogs.
- (d) Technical: the old `/pages/study/...` URL still gets more impressions than the current URL [GSC] (check the redirect). The hub, which should pass topical context, is not indexed. GSC shows the article at an average position of 4 for "pdrn vs retinol", from 1 impression:
  Google can place it; nobody is searching it yet [GSC].

**What to change:** open with a two-sentence plain answer ("In the one controlled trial, the PDRN side improved crow's-feet area about 3.5 times as much as the retinol side over 28 days; here are the limits"); add an H2 "Can you use PDRN and retinol together?" that says no trial
tested the combination (unless a source is found; INKEY's "yes, AM and PM" is a brand claim) ; keep the limits section (company-employed authors, 0.1% eye cream, 28 days, no placebo side). Add "PDRN vs retinol" as an H2 on the hub (exists) and link both ways. Confirm the redirect
from `/pages/study/...`.
**Off-page, specific to this term:** the trial is cited by none of the 33 readable pages. An independent plain-language summary is genuinely new information for the editors of the AI Overview's sources.

### 6.8 "pdrn" (GB), 6,462 [KS]

**Top results [SERP]:** #1 egskinclinic.co.uk/pdrn-in-skincare (MEDICAL), #2 sulskin.com blog (BRAND), #3 skincupid.co.uk/collections/pdrn?page=3 (RETAILER, a paginated page 3), #4 uk.style.yahoo.com, #5 belantti.co.uk blog, #6 paulaschoice.co.uk PDRN ingredient page, #7
pdrn-skin.com blog, #8 superbhb.co.uk blog.
Features: AIO, PAA, related searches, video. PAA: Does PDRN stimulate hair growth? / What are the best anti-aging serums in the UK? / How long do the effects of PDRn last? / What does salmon DNA PDRn do for your skin? [SERP].
**AIO cites (11):** Cult Beauty UK, Boots (three pages: what-is-pdrn guide, ingredient collection, routines guide), PMC5405115, K Beauty Edit collection, YouTube, an Instagram reel, Marie Claire UK "best-pdrn-skincare", Skin Cupid collection, Reddit r/SkincareAddiction [SERP].
Our page: the English hub (not indexed).

| Factor | EG Skin Clinic (#1) | Sulskin (#2) | Skin Cupid (#3) | Ours: EN hub |
|---|---|---|---|---|
| Page type | Dermatology-clinic blog | Brand/store blog | Retailer collection, page 3 of the series | Research hub |
| Title / H1 | "PDRN in Skincare - egskinclinic" / "PDRN in Skincare: An Edinburgh Dermatologist's Honest Take" | "What is PDRN? Discover the Latest Skincare Trend for Youthful Skin" / no H1 found | "PDRN Skincare: Anti-Aging Serums, Toners & Creams - Skin Cupid" / "PDRN" | See 6.1 |
| Main words | 465 | 549 | 73 | 2,237 |
| Opens with definition | No (anecdote; definition under first H2) | No (Kardashian "vampire facial" hook) | Yes | Partly |
| Studies | 0 | 0 | 0 | 5 |
| Tables / FAQ | 0 / no | 0 / not seen | 0 / none | 2 / yes |
| Author / reviewer | Unnamed first-person dermatologist; none | Tiff Y (JSON-LD); none | None | Named; medical reviewer |
| Date | JSON-LD 2026-06-21, not visible | JSON-LD 2025-02-17 | None | Reviewed 24 Sep 2026 |
| JSON-LD | BlogPosting, Person, Organization | Article, Person | CollectionPage, ItemList, Product, AggregateRating (5.0 from 2), Offer, MerchantReturnPolicy, OfferShippingDetails, HealthAndBeautyBusiness | See 6.1 |
| Images / products | 1 / none | 0 / 4 links | 16 / 16 on this page | 22 / 3 |
| Concentration and salmon | No / yes | No / "salmon sperm" | No / yes | Yes / yes |
| Covers | "Injectable vs Topical: What the Evidence Actually Says" H | Injections M; side effects M | Nothing | See 6.1 |

**Why they outrank us**

- (a) Authority: not decisive. EG Skin (not listed) and Sulskin (4,275,589) hold #1 and #2. The AI Overview leans on Boots (10,165), Cult Beauty (48,365) and Marie Claire.
- (b) Content: EG Skin is a 465-word clinician voice that says what the evidence is and is not; ours is deeper and more cautious. Skin Cupid's UK retail signals (shipping and returns in structured data, a UK store) are what we lack.
- (c) SERP features: the AI Overview cites retailer collection pages and "best of" lists.
- (d) Technical: ours is unindexed. hreflang offers `en` only (no `en-gb`) [FETCH]. UK price and delivery presentation: not measured.

**What to change:** items from 6.1 and 6.2; give the UK shopper GBP price, UK delivery and returns on the product pages (Skin Cupid's pattern); add an FAQ answer to "How long do the effects of PDRN last?" only if a source supports it (the trial measured 28 days and says nothing
about duration, so say that); the hair-growth question belongs to the sister brand, not this page.

### 6.9 "pdrn serum" (GB), 2,049 [KS]

**Top results [SERP]:** #1 boots.com/beauty/skincare/shop-skincare-ingredients/pdrn (RETAILER collection; blocked to my fetch), #2 amazon.co.uk search page (MARKETPLACE; 503 to Chrome, search page only), #3 thekbeautyedit.co.uk/collections/pdrn (RETAILER), #4
glamourmagazine.co.uk gallery, #5 Cult Beauty UK collection, #6 Dermatology Times, #7 Boots routines guide, #8 dr-pen.co.uk collection, #9 an Instagram reel.
**No AI Overview.** Features: popular products, PAA, related searches, video. PAA: Do PDRN serums actually work? / Is PDRn salmon sperm? / What is the best PDRN serum in the UK? / What is the best PDRN serum in Korean skincare? [SERP].
[KS] records that Boots ranks #1 with a collection titled "PDRN Skincare | Serums, Creams & More".
Our page: /products/pdrn-renewal-serum.

| Factor | The K Beauty Edit (#3) | Ours: serum page |
|---|---|---|
| Page type | Retailer collection, "74 products" | Product page |
| Title / H1 | "PDRN Korean Skincare UK \| Salmon DNA Skincare \| The K Beauty Edit" / "Collection: PDRN" | See 6.3 |
| Main words | about 540 (intro plus product text) | 363 |
| Opens with definition | Yes (also says "used in Korean dermatology clinics for years as an injectable") | No |
| Studies / tables / FAQ | 0 / 0 / none | 0 / 0 / yes |
| Author / date | None / none | None / none |
| JSON-LD | Organization only | Product, Offer, Brand, FAQPage |
| Images | 40 | 24 |
| Products and prices | 74, GBP prices, review counts per card ("8 reviews"), free delivery over GBP 22 | 1 |
| Reviews shown | Yes, counts per product | None |
| Concentration and salmon | No / yes | 1% / yes |

Boots and Amazon: not measurable (2.2).

**Why they outrank us**

- (a) Authority: Boots (10,165) is a major retailer; The K Beauty Edit is not in the Tranco list and takes #3 anyway.
- (b) Page type: four of the top five are category pages (Boots, Amazon, K Beauty Edit, Cult Beauty), and a fifth is a gallery list. A single product page cannot take those slots; the SERP shows a product carousel too.
- (c) SERP features: no AI Overview, so organic results get more of the click; this is the one English commercial SERP where that is true.
- (d) Technical: product page indexed; speed (LCP 4.9 s) and no ratings.

**What to change:** this term belongs to a deep PDRN collection, which we do not have (3 products). Options: widen /collections/pdrn with the existing bundles (see 6.4) and treat the product page as the target for "pdrn serum 1%" long-tail. Add review counts and UK price and delivery to the cards.

### 6.10 "pdrn" (DE), 4,650 [KS]

**Top results [SERP]:** #1 loreal-paris.de/tipps-und-trends/hautpflege/pdrn-wirkung (BRAND), #2 marudermcosmetics.com/de/blog (BRAND), #3 pdrn-skin.com/?lang=de (BRAND, small store home page), #4 feelbe.one blog, #5 yesstyle.com/de collection, #6 kbeautyworld.com product, #7
douglas.de product page, #8 ksisters.at blog.
Features: AIO, PAA, video. PAA: Für was ist PDRn gut? / Ist PDRn Lachs Sperma? / Wann sollte man PDRN anwenden? / Wie oft trägt man eine PDRn-Maske? [SERP].
**AIO cites (10):** dm.at article, douglas.de category page, koreanbeauty.at collection, cosmeterie.at magazine, littlewonderland.de blog, Lancome DE guide, Maruderm, YouTube, 2 Instagram reels [SERP].
Our page: /de/pages/pdrn-research (indexed, crawled 2026-09-05).

| Factor | L'Oréal Paris DE (#1) | Maruderm (#2) | pdrn-skin.com (#3) | Ours: DE hub |
|---|---|---|---|---|
| Page type | Brand magazine article | Brand blog (translated) | Small store home page with a dozen language blocks stacked on one page | Research hub |
| Title / H1 | "PDRN Wirkung: Anti-Aging ohne Injektionen \| L'Oréal Paris" / "PDRN Wirkung & Anti-Aging: Was der Wirkstoff für Deine Haut leisten kann" | "Was ist PDRN in der Hautpflege? Vorteile, Anwendungen und wichtige Informationen..." / similar | "PDRN SKIN" / English H1 "PDRN Skincare - Korean Salmon DNA Serum, Masks & Cream for Glass Skin" | "PDRN (Sodium DNA) Forschung und Studien" (39 chars) / "PDRN: Hautpflege mit Lachs-DNA" |
| Main words | about 1,065 plus sources | 8,727 (69 H2s) | 743 | 2,282 |
| Opens with definition | Yes: TL;DR bullets "Das Wichtigste zur Wirkung von PDRN im Überblick" | No (trend hook) | No (shop pitch) | Partly (3 tiles first) |
| Studies | 3 DOI links | 0 | 0 | 5 |
| Tables / FAQ | Tables detected (4, not verified) / yes, FAQPage | 0 / yes | 0 / yes | 2 / yes |
| Author / reviewer | "L'Oréal Group" (organisation); none | "Maruderm Cosmetics"; none | None | Named; medical reviewer |
| Date | Published 2026-09-29, modified 09-30 | Published 2026-05-27, modified 2026-10-07 | None | Reviewed 24 Sep 2026 |
| JSON-LD | Article, FAQPage, BreadcrumbList, Organization | BlogPosting, Organization, WebSite | Organization, WebSite | Same as EN hub |
| Products and prices | Section on its own PDRN+ products, no prices | None | 4 products with prices | 3 cards |
| Concentration and salmon | No / yes; vegan PDRN+ from magnolia flowers | No / yes | "+100%" hydration claims / yes | Yes / yes |
| Covers | Injections H ("PDRN-Kosmetik vs PDRN-Behandlung"); how to use H; limits H | Polynucleotides H; topical vs injectable H; side effects H | Side effects (FAQ) | Same as EN |

**Why they outrank us**

- (a) Authority: L'Oréal Paris DE (267,094) is a brand with its own PDRN product. #2 and #3 are not in the Tranco list.
- (b) Content and language match: **our DE title and H1 omit the words Germans search.** "Wirkung" (effect) leads L'Oréal's title; "Was ist PDRN?" leads Maruderm's. Ours says "Forschung und Studien" and "Hautpflege mit Lachs-DNA". Neither of the DE PAA questions ("Für was ist
  PDRN gut?", "Wann sollte man PDRN anwenden?") has a matching heading on our page, and L'Oréal's page opens with TL;DR bullets and has 10 question headings and a FAQPage block. Freshness: L'Oréal published eight days ago and Maruderm updated today.
- (c) SERP features: AIO cites retailers' category and guide pages (dm, Douglas, koreanbeauty.at) and Lancome.
- (d) Technical: ours is indexed but gets 3 impressions in 90 days (position 6.3) [GSC]. Indexing is not the problem here; query match is.

**What to change (after the English is final; the store's rule is English first, and an outdated translation is still served):** retitle to something like "PDRN Wirkung: Was Lachs-DNA in der Hautpflege kann" (50 characters); H1 "Was ist PDRN? Wirkung und Studienlage"; add a "Das
Wichtigste im Überblick" bullet block at the top; add question headings "Ist PDRN Lachssperma?", "Für was ist PDRN gut?", "Wann und wie oft wendet man PDRN an?"; add visible dates.

### 6.11 "pdrn" (NL), 1,900 (Ads, bucketed; no observed figure in [KS])

**Top results [SERP]:** #1 dr-jetskeultee-skincare.nl (BRAND site reprinting a Women's Health interview), #2 littlewonderland.nl/nl/specifieke-huidverzorging/ingredienten/pdrn/ (RETAILER ingredient page), #3 beautyfashionshop.nl/blog (RETAILER blog), #4 huidlaserutrecht.nl
(clinic: polynucleotiden PDRN), #5 loreal-paris.nl, #6 faberhuidkliniek.nl (clinic: PDRN microneedling), #7 skin360.nl (clinic), #8 kliniekvoorjou.nl (clinic).
Features: AIO, PAA, related searches, video. PAA: Wat is PDRn? / Wat is het beste PDRN-serum? / Wat zijn de nadelen van de PDRN-behandeling? / Wat is een PDRN-behandeling? [SERP].
**AIO cites (8):** Jetske Ultee, Little Wonderland, koreanskincare.nl product page, Faber clinic, koreanbeauty.nl collection, celestetic.nl, kliniekvoorjou.nl, iciparisxl.nl blog [SERP].
Our page: /nl/pages/pdrn-research (indexed, crawled 2026-09-10; **not fetched**, structure inferred from the German twin and `configs/hub-i18n/pdrn-research.json`).

| Factor | Dr. Jetske Ultee (#1) | Little Wonderland NL (#2) | Beautyfashionshop (#3) | Ours: NL hub |
|---|---|---|---|---|
| Page type | Brand site, reprinted magazine interview | Retailer ingredient category | Retailer blog | Research hub (translated) |
| Title / H1 | "Zalmsperma voor je huid PDRN skincare uitgelegd - Dr. Jetske Ultee" / none found | "PDRN Skincare \| Shop Online - Little Wonderland" / "PDRN" | "Werkt PDRN-skincare écht? Wat je wél en niet mag verwachten \| Beautyfashionshop" / same | Not measured |
| Main words | 450 | 51 (plus blog link; 144 images) | 1,104 | Not measured (EN is 2,237) |
| Opens with definition | No (magazine standfirst) | Yes (one sentence) | Yes, within the first section | Not measured |
| Studies | 0 | 0 | 0 | Same 5 as EN (inferred) |
| Tables / FAQ | 0 / no | 0 / none | 0 / yes, FAQPage | Inferred as EN |
| Author / reviewer | Demi Schoenmakers and Sanne Roes (Women's Health); dermatologist Dr Jetske Ultee quoted; no reviewer | None | "Sanne" visible; none | Named; medical reviewer (inferred) |
| Date | Visible, 10 Dec 2025 | None | Visible, 6 Oct 2026 | Reviewed 24 Sep 2026 (inferred) |
| JSON-LD | None | BreadcrumbList, Organization | BlogPosting, FAQPage, AggregateRating (4.7 from 40, shop-level), Person | Inferred as EN |
| Covers | Polynucleotides H-ish ("Wat is PDRN eigenlijk?"), injections H ("Van kliniek naar badkamerkast"), a clinic price "vanaf 400 euro per behandeling" | None | Polynucleotides H, topical limits H ("Het penetratieprobleem"), how to use H | |

GSC for our NL hub: 36 impressions, 1 click, average position 36.1 over 90 days; for the query "pdrn", 18 impressions at position 52 (last 28 days) [GSC].

**Why they outrank us**

- (a) Authority: weak across the board: Little Wonderland 457,115, Jetske Ultee 997,626, Beautyfashionshop 2,046,499. This is the most beatable of the SERPs: no spam, no UGC, small sites.
- (b) Content: the NL "pdrn" SERP is partly a treatment query: 4 of the 8 results are skin clinics selling PDRN injections, and the PAA is about the treatment. Our hub is a skincare page; it matches only the cream half of the intent. Our hub's Dutch title is not verified (the
  German one lacks the query words, so the Dutch one likely does too).
- (c) SERP features: AIO cites three clinics, three K-beauty retailers, a perfumery blog and the #1 brand site.
- (d) Technical: indexed; position 52 is a relevance problem, not a crawl problem.

**What to change (after the English is final):** Dutch title with "Wat is PDRN?" and "werking"; H2s mirroring the PAA ("Wat is PDRN?", "Wat zijn de nadelen van PDRN?", "PDRN-behandeling of crème: wat is het verschil?"); a short "Wat is het beste PDRN-serum?" section pointing to
the label-based comparison (6.6). For the injection-price question use a sourced figure (the Women's Health interview gives "vanaf 400 euro per behandeling"; confirm before quoting). Off-page: Dutch beauty press that already ran PDRN pieces (Women's Health NL) and Dutch
dermatologist or physician sites that can link the trial summary.

---

## 7. Action plan, ranked by impact against effort

"Demand pool" is the observed monthly search volume [KS] for the terms the action serves. It is not a traffic forecast; click share is unknown until the pages are indexed and ranked.

| # | Action | Effort | Impact | Demand pool (searches per month) |
|---|---|---|---|---|
| 1 | **Get the EN hub crawled and indexed.** In the Search Console interface: Request Indexing on `/pages/pdrn-research`; open the Pages report and note whether it says "Discovered, currently not indexed"; re-inspect after a few days. Do the same for the Yogya microneedling appraisal and the other two study pages listed as unknown. Confirm `/pages/study/pdrn-vs-retinol...` 301-redirects to the `/blogs/clinical-studies/` URL. | Small | Highest. Nothing in sections 6.1, 6.2 and 6.8 can happen first. | pdrn 19,734 US + 6,462 GB; what is pdrn 5,602 US |
| 2 | **Hub v2 on-page** (details below). | Medium | High | Same pool |
| 3 | **First genuine links and press** (details below). | Large, slow | High | All terms |
| 4 | **Honest Reddit presence** on the threads the AI Overviews cite. | Small, steady | Medium | AIO citation on 5 of 7 US terms |
| 5 | **A 60 to 90 second explainer video** with Dr Bodde. | Medium | Medium | YouTube cited on 6 of 7 US AIOs |
| 6 | **Serum and cream page upgrades**: evidence block with links, strength line, genuine review markup, PAA answers, speed (LCP 4.9 s, TBT 540 ms). | Medium | Medium to high (commercial terms) | pdrn serum 3,936 US + 2,049 GB + 845 DE; pdrn cream 2,321 US |
| 7 | **Decide who owns "pdrn skincare"** and rebuild `/collections/pdrn` accordingly (copy, FAQ, `CollectionPage` and `ItemList`, check bundles). | Small to medium | Medium | pdrn skincare 1,817 US + 1,182 GB |
| 8 | **Build "PDRN serums compared on what the label says"**, every cell verified from labels. | Medium | Medium | best pdrn serum 1,042 |
| 9 | **DE and NL hubs: retitle and add question headings**, after the English is final. | Small | Medium (DE), medium (NL, weakest competition) | DE 4,650; NL 1,900 (Ads, bucketed) |
| 10 | **Hub speed:** mobile LCP 7.8 s, 319 requests, 2.6 MB. | Medium | Medium | All |
| 11 | **Study article:** opening plain answer, "use together" section, redirect check. | Small | Low to medium | pdrn vs retinol: no measurable demand yet |

### Hub v2 (action 2): headings to add or change, in page order

1. H1: "What Is PDRN? Salmon DNA skincare, explained". Directly under it, a 40 to 60 word definition and one-line evidence status. Then the three result tiles.
2. Keep "What Is PDRN?" and "At a glance".
3. **New H2 "Is PDRN really salmon sperm?"** (PAA on 5 of 13 SERPs).
4. **Rename "What Does PDRN Do for Skin?" to "Does PDRN work in skincare? What the evidence shows"** (PAA: "Do PDRN serums actually work?" on 4 SERPs; "Is PDRN good for your skin?" on 2). This follows the strategy rule that "does X work" belongs to the hub.
5. Keep "PDRN vs Retinol: What the Measurements Show"; add one H3 "Can you use PDRN and retinol together?" that states no trial has tested it, unless a source is found.
6. **New H2 "Is PDRN the same as polynucleotides?"**
7. **New H2 "PDRN injections vs creams, and what a PDRN shot costs"** (PAA on 2 SERPs). Needs a sourced price; none is in the files I have for the US or UK.
8. **New H2 "Salmon PDRN vs plant-derived (vegan) PDRN"** (INKEY, Kiokii, L'Oréal DE all address it).
9. Keep "What 1% PDRN Means". Add a sourced line: Medicube declares 10,000 ppm (1%), INKEY 2% (20,000 ppm, vegan, supplier-run studies). Verify both from the products' own labels before publishing; today the sources are Beauty By Peptides and INKEY's own page.
10. **New H2 "PDRN side effects and who should avoid it"** (fish allergy, patch test, no adverse events in the 31-woman trial). Moves content that now sits in a bullet and an evidence card under a heading people search for.
11. Keep "How to Use PDRN"; add "When to apply it and what not to mix it with" (PAA: "What not to mix with PDRN cream?", "Wann sollte man PDRN anwenden?").
12. Keep "PDRN Evidence & Sources"; add the PMC link for Squadrito 2017.
13. FAQ: add the PAA questions above, with answers identical to the section answers.
14. Structured data: one `Article` (or `MedicalWebPage`) node carrying `datePublished`, `dateModified`, `author`, `reviewedBy` with the reviewer's credential and a profile link. FAQPage is optional; FAQ rich results ended 2026-05-07 (page quality gate, check E), so do not add schema purely for that.
15. Visible "Published" date beside "Last reviewed".

### Links and press (action 3): targets with a reason

The angle is the same everywhere: the only controlled trial of a PDRN cream against retinol (Ye et al., PLOS ONE 2026): 31 women, 28 days, crow's-feet area 23.0% vs 6.6%, with the limits stated up front (0.1% eye cream, authors include employees of two skincare companies, no
placebo side). None of the 33 readable competitor pages mentions it.

| Target | Why this one | Evidence |
|---|---|---|
| Allure (Elizabeth Siegel, "PDRN Has Quickly Taken Over Skin Care") | Cited by AIOs on 2 US terms; her article already links 4 PMC/NCBI papers, so she links to science | [SERP] [FETCH] |
| Cosmopolitan (Beth Gillette), The Independent IndyBest (Sophie Wirt), The Style List (Alvira Dsouza) | Each published a PDRN piece in 2025 to 2026 with dermatologist quotes | [FETCH] |
| Dermatology Times "Social media mythbusters: PDRN serums" | Physician-facing; appears in 3 SERPs (US skincare #7, GB serum #6, NL serum #5) | [SERP] |
| Marie Claire UK "best-pdrn-skincare", Glamour, Vogue, Ulta's "best-pdrn-serums" | Cited by the GB or US AI Overviews for list queries | [SERP] |
| Women's Health NL (Demi Schoenmakers, Sanne Roes) | Wrote the PDRN interview that is reprinted on the #1 Dutch result | [FETCH] |
| Dr Bodde's own professional pages | A credentialed person linking to the hub is the cleanest first link | n/a |
| Wikipedia "Polydeoxyribonucleotide" | It has about 50 journal links and does not cite the Ye 2026 paper (0 matches) [FETCH]. Because Skingenetix has a commercial interest, propose the citation on the article's Talk page; do not edit it directly. | [FETCH] |

Do not buy links, and do not try to "clean up" the 627 spam referring domains as a priority: they are automated checker domains and carry no authority either way [BL].

### Reddit (action 4)

Threads the AI Overviews or SERPs already use [SERP]: r/AsianBeauty "Thoughts on PDRN as a topical skincare ingredient" (cited by AIOs on 3 US terms; #1 for "pdrn skincare"), r/AsianBeauty "PDRN products are rapidly evolving..." (cited on 2), r/SkinbarrierLovers (#1 "pdrn
cream"), r/KoreanBeauty (#4 "pdrn cream"), r/30PlusSkinCare (#3 "best pdrn serum"), r/koreanskincare (#7), r/45PlusSkincare (#4 "pdrn vs retinol"), r/SkincareAddiction (GB AIO). Rules: a named account that discloses who it works for, answers the actual question with the PLOS ONE
link and the limits first, no shop link in the first reply, no coordinated voting.

---

## 8. Things I noticed on our own pages while measuring

These are outside the SEO brief but affect trust and should be decided by whoever owns the claims register.

1. **The "how many times better than retinol" wording differs.** The serum and collection meta descriptions say "more than twice as much as retinol"; the hub FAQ and study meta say "more than three times". The trial's own numbers are 23.0% vs 6.6% (about 3.5 times) on one measure
   and "up to -23% vs -6 to -7%" overall [FETCH]. Pick one phrasing the paper supports and use it everywhere.
2. **The product pages carry a claim the hub is careful about.** The serum page says the 1% PDRN "outperformed retinol head to head in a clinical study" and links no study [FETCH]. The trial used a 0.1% eye cream for 28 days and the hub says so ("No study has tested whether more
   PDRN does more"). INKEY handles the same issue with a footnote naming the supplier and the 2% test. The product pages should match the hub.
3. **Our price anchor.** The Offer markup shows EUR 69.00 (serum) and EUR 79.00 (cream) in my fetch (market-dependent), against INKEY's PDRN serum at $18 for 30 ml and Ulta's Medicube eye serum at $22.90 [FETCH] [SERP]. Not an SEO problem, but it is why the page needs to prove value.
4. **Redirect check.** Google still reports more impressions on the old `/pages/study/` URL than the new one [GSC].

---

## 9. What I could not establish, and what to re-measure

- **Why the English hub is unknown to Google.** Verified: in sitemap, linked internally, no noindex, self-canonical, 200 status. Not verified: the Search Console Pages-report status. Next step is a person with Search Console access opening that report.
- **Competitor authority** beyond the Tranco proxy: needs paid backlink data (referring domains per top-3 domain). Not run, by instruction.
- **Brand search demand** per competitor: not available without paid data.
- **Boots, SkinCeuticals US, Instagram, Amazon UK:** not measurable by fetch.
- **Our NL hub's title, H1 and word count:** not fetched.
- **Competitor Core Web Vitals:** PageSpeed quota exhausted.
- **Re-pull the same 13 SERPs 14 days after the hub is indexed**, and re-run URL Inspection. That gives a before and after.

## Sources used by URL ([WEB] items and cited pages)

- INKEY Lab PDRN serum review and launch coverage: https://www.missljbeauty.com/2026/01/the-inkey-list-pdrn-serum-review.html ; https://theindustry.beauty/inside-inkeylab-the-inkey-lists-new-fast-track-innovation-hub-for-next-gen-products-and-consumer-co-creation/ ;
  https://cewuk.co.uk/inkey-introduces-inkeylab-a-new-community-led-innovation-stream/
- SkinCeuticals Phyto Corrective PDRN serum (stockist page): https://www.cultbeauty.com/p/skinceuticals-phyto-corrective-pdrn-visible-redness-reducing-serum-30ml/17886927/
- Medicube PDRN Pink Peptide Serum review roundup (10,000+ reviews, 4.5 average): https://kimola.com/reports/unlock-insights-medicube-serum-customer-feedback-analysis-amazon-en-us-155192 (as summarised by WebSearch; not opened)
- Reddit r/AsianBeauty PDRN thread (mirror): https://redlib.groet-infra.nl/r/AsianBeauty/comments/1l86p6e/research_on_if_you_should_use_pdrn_creams_serums/
- Tranco: https://tranco-list.eu/
- Pages measured: the competitor URLs listed in section 6 and in `scratchpad/comp/targets.txt`.
