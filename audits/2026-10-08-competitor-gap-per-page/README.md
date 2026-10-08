# Competitor gap per page — skingenetix.com — 2026-10-08

Evidence record for the per-page competitor analysis that extends the 2026-10-07 visibility forensics to every
keyword-owning page. Procedure: the `seo-visibility-forensics` skill, Phase 5 (`serp_gap.py pull | pages | authority |
report`) on a second config (`config.json` here), plus `serp_gap_deep.py mentions` on yesterday's set, local Lighthouse, and
a DataForSEO volume pull for the terms the strategy pull never covered. The plain-English plan that reads this record is
`docs/website-traffic-and-performance-plan-2026-10-08.md`; the three teardowns in this folder hold the per-keyword evidence.

## What was pulled, and what it cost

| Step | Generator | Output | Spend (USD) |
|---|---|---|---|
| Volumes for 80 English terms in US and GB and 16 German terms (clickstream observed volume and Google Ads volume) | DataForSEO `keywords_data/clickstream_data/bulk_search_volume` and `google_ads/search_volume`, called directly (the repo helper returns one Ads row only) | `data/volumes.json` | 0.33 |
| 39 live SERPs with AI Overviews, desktop, depth 10 (24 US, 8 GB, 6 DE, plus US "pdrn cream") | `serp_gap.py pull` | `serp/serp.json`, `serp/raw/` | 0.08 |
| Top 6 pages per keyword measured against ours (words, headings, tables, FAQ, video, answer-first, author line, schema, dates, citations) | `serp_gap.py pages --top 6` | `serp/pages.json` | 0 |
| Referring domains for every domain on the 39 SERPs | `serp_gap.py authority --top 10` | `serp/authority.json` | under 0.05 |
| The per-keyword gap table | `serp_gap.py report` | `serp/report.md` | 0 |
| Brand demand and Reddit and YouTube presence for the 12 brands most present on yesterday's 33 SERPs | `serp_gap_deep.py mentions` | `../2026-10-07-visibility-forensics/serp/mentions.json` | 0.35 |
| Mobile Lighthouse on 9 of our page types and 6 competitor pages | `npx lighthouse` 13.5, mobile, throttled, one run each | `data/lighthouse/*.json`, `data/lighthouse-summary.json` | 0 |
| Page experience via the PageSpeed Insights API | `serp_gap_deep.py vitals` | **failed**: HTTP 403 with the Google API key (the key's project has not enabled the PageSpeed Insights API), HTTP 429 without a key (rate limit). The 403 attempt is kept in the scratchpad; no vitals data exists | 0 |
| Per-page table: owner term, volumes, Search Console 28-day totals, SERP summary | this folder's scripts (inline Python, recorded in the session) | `data/page-table.json`, `data/serp-summary-both-days.json` | 0 |

Total today: about USD 0.81.

## Verdicts

| Finding | Verdict | Source |
|---|---|---|
| Nine pages with real impressions had no keyword owner in `configs/page-targets.json` (the glutathione serum 235 impressions in 28 days, the copper collection 149, the Matrixyl cream 130, the copper night cream 126, the PDRN cream 102, the copper day gel-cream 31, and the creams, microneedling and collagen pages) | VERIFIED | `data/page-table.json` |
| Four terms with no owning page carry more observed demand than most hub terms: "peptides for skin" 1,862 US, "brightening serum" 1,057 US and 871 GB, "ghk-cu cream" 805 US, "microneedling stamp" 805 US | VERIFIED (clickstream, 2026-10-08) | `data/volumes.json` |
| The Skin Solutions pages' owner terms ("fine lines", "firming", "skin repair", "brightening") have no measurable demand as written; the category forms ("wrinkle serum" 251, "skin firming cream" 201, "skin repair cream" 316 GB, "brightening serum" 1,057) do | VERIFIED | `data/volumes.json` |
| We rank in no top 10 on the 39 new pairs except the brand term, where we are first and cited by the AI Overview | VERIFIED | `serp/serp.json` |
| AI Overviews appear on 25 of 39 new SERPs (47 of 72 across both days); most-cited domains YouTube, The Ordinary, PMC, Allure, Vogue, Reddit, Wikipedia, Paula's Choice, Cleveland Clinic | VERIFIED | `serp/report.md` |
| Category terms ("wrinkle serum", "firming serum", "peptide cream", "glow serum", GB "brightening serum", GB "peptide cream") are owned by Amazon, eBay, Ulta, Dermstore on desktop | VERIFIED | `serp/serp.json` |
| Every page type of ours paints its largest element at 10.7 to 12.5 s on a throttled phone; the Matrixyl cream product page at 4.7 s; first paint 2.0 to 3.9 s; blocking time under 500 ms; HTML of a hub 462 KB | VERIFIED (lab, one run each) | `data/lighthouse-summary.json`; curl of the copper hub |
| The late paint is caused by the theme's section reveal animation or hero loading order rather than by scripts or the server | PLAUSIBLE, NOT ESTABLISHED: the hero image already carries `fetchpriority="high"`; the copper hub has three `reveal-on-scroll="true"` sections and 462 KB of HTML, the home page 23 reveal sections and 529 KB; Lighthouse's LCP-element audit returned no element. The two product pages are the control: both have three reveal sections and about 645 KB of HTML, yet the Matrixyl cream paints at 4.7 s and the copper serum at 11.4 s, so the cause is the specific element painted last on each page, not page weight. Test: duplicate theme, animations off, Lighthouse with the element audit read, per page type (plan step 1.5) | copper hub, home and two product pages, curl 2026-10-08 |
| App scripts not used on most pages: Shopify Forms 259 KB on every page, Profit Pumper bundles 467 KB and Appstle 72 KB on product pages, a 152 KB country-flag sprite on every page | VERIFIED | `data/lighthouse/*.json` network requests |
| Competitors' pages are not fast either (SkinCeuticals 4.9 s, The Ordinary 6.1 s, Paula's Choice 12.4 s, Remedy 53.6 s LCP), so speed is not what ranks them above us | VERIFIED (lab) | `data/lighthouse-summary.json` |
| Brand demand: The Ordinary 201,000 US searches a month, SkinCeuticals 135,000, Boots 550,000, Allure 90,500; Skingenetix 0. The Ordinary in 241,000 Reddit and 9.7 million YouTube results; Skingenetix in none | VERIFIED (Google Ads brand volume, DataForSEO SERP counts; "theinkeylist" returns 110 because the brand query is the domain stem, a data trap) | `../2026-10-07-visibility-forensics/serp/mentions.json` |
| Hacked-site spam (stonevillenc.org) holds page-one slots on "peptides in skincare", "copper peptide skincare", GB "copper peptide" | VERIFIED | `serp/serp.json` |
| The four Skin Solutions pages and The Science serve no `<h1>` element; the five hubs and the home page serve one | VERIFIED (curl of the six pages, 2026-10-08) | teardown-concern-science-hubs-markets.md §1; re-checked by the session |
| Register-breaking claims are live on the concern pages: "even reverse them" and "safe for sensitive skin?" (Fine Lines), "Overnight Structural Repair" and "stimulation of new collagen production" (Firming), "more than twice the wrinkle improvement" (Skin Repair) | VERIFIED (curl, exact phrases found) | the same |
| The German copper hub's H1 is the English "Copper Peptide (GHK-Cu)" | VERIFIED (curl of `/de/pages/copper-peptide-research`) | the same |
| The creams collection shows "Coming soon" above five live products; both stamp sets render "Sold out" with `OutOfStock` schema under a pre-order template; collections carry breadcrumb schema only | VERIFIED (curl of the creams collection and the PDRN stamp set, 2026-10-08) | teardown-products-collections.md §1; re-checked by the session |
| 17 of the 18 buying-term SERPs show a product carousel and only 6 an AI Overview; 8 of 75 measured top pages carry rating markup; our Kaufland listing is #7 for DE "glutathion serum" while the store page is absent | VERIFIED (serp.json, pages.json) | teardown-products-collections.md |
| Six of the fourteen concern, science and hub pairs are shop SERPs (wrinkle serum, firming serum, skin firming cream, skin repair cream, brightening serum, glow serum), where a concern page is the wrong page type | VERIFIED | `serp/serp.json`, the teardown |
| Our two referring domains (DataForSEO) are not genuine authority; genuine referring domains remain zero | VERIFIED (yesterday's filter) | `serp/authority.json`, yesterday's README |

## Limits

- Desktop SERPs only today; yesterday showed mobile SERPs differ in kind on head terms. Mobile pulls for the new category
  terms are a Phase 3 re-plan item.
- One Lighthouse run per page, lab only; no field data until the PageSpeed API is enabled.
- The teardown agents read the top pages themselves (their fetches are listed in each teardown's sources); figures they
  quote beyond `pages.json` are theirs.
- "fine lines and wrinkles" and "peptides in skincare" page-one rows include a spam page; positions there will move when the
  spam update settles.

## Files

- `config.json`: the 39 pairs with hero pages, the markets, the thresholds.
- `serp/`: `serp.json`, `raw/` (one file per pair), `pages.json`, `authority.json`, `report.md`.
- `data/`: `volumes.json`, `page-table.json`, `serp-summary-both-days.json`, `lighthouse-summary.json`. The 15 raw Lighthouse
  runs in `data/lighthouse/` stay local (gitignored there: 500 KB each, and the commit hook would reformat them); re-run
  `npx --no-install lighthouse <url> --form-factor=mobile --output=json` to regenerate one.
- `teardown-concern-science-hubs-markets.md`, `teardown-products-collections.md`, `teardown-study-articles.md`.
