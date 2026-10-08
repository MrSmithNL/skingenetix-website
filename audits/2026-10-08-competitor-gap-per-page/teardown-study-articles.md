# Teardown: the eight clinical-study articles and the list page (2026-10-08)

Source tags: `S` = serp/ (serp.json, pages.json, authority.json) · `D` = data/ (volumes.json, page-table.json, lighthouse-summary.json) · `GSC` = visibility-forensics `data/gsc-weekly-and-query-page-28d.json` (qp28) · `UI` = its url-inspection.json · `V7` = its serp/ (yesterday) · `T` =
`configs/keyword-data/targeted-2026-09-30/targeted.json`. Volumes are US monthly clickstream panel estimates (50 is the floor) unless stated. Targets are my judgment, not forecasts.

## Bottom line

1. **Content shape is not what loses.** On every SERP pulled, our article is as long or longer than the top three, with an author, FAQ and 6 to 12 sources; most top pages cite none [S pages]. What differs is authority (we have zero genuine referring domains; competitors 494 to 1,533 [S
   authority; V7 README]) and intent: page one rewards dictionaries, shops, clinics and forums.
2. **Three articles are not in Google yet.** Yogya, Tadini and Robinson are "unknown to Google" [UI]. I checked live: all three are in `sitemap_articles_1.xml` and linked from the list page and their hub. Watanabe went live the same day and was crawled 3 Oct, so this is crawl lag. The
   Request-indexing button is manual.
3. **Search Console flatters Ye.** Position 7.4 on 261 impressions [D page-table], but only 19 impressions carry a visible query, and they are the paper's title and DOI. The head query "pdrn vs retinol" has 1 impression [GSC]. People are finding it as a citation.
4. **Key-figure tiles render as H2s** on the two live pages I fetched ("2 vs 6 months", "-14%", "2.2/10" on Yogya; "Week 8/12/4" on Robinson). Headings should be questions.
5. **AI Overviews cite none of us** on the five queries pulled [S serp]. PubMed/PMC is cited only on "topical glutathione". On "acetyl hexapeptide-3" Tadini's own paper (ResearchGate) ranks #4 and is cited. No PMC page sits above us in any organic list. Where the paper is open, we are the
   plain-English companion, not a rival.

STUDY-DETAIL (result sections, how-it-works blocks) is assumed live below.

---

## 1. Wang 2013 (`argireline-crows-feet-trial-wang-2013`)

- **Question and demand:** "Does Argireline soften crow's feet?" "argireline crows feet": 50 US [D volumes].
- **Rank and index:** not top 10 [S]; indexed, crawled 5 Oct [UI]; 85 impressions, pos 13.8 [D page-table]. Visible queries are non-English: "argireline vorher nachher" pos 10 [GSC].
- **Page one:** brand and blog sites (skindeva #1, scrubalildeepa #2, YouTube #3, Typology, Glam, Era Organics). No medical or PMC page. AIO cites Typology, YouTube, Glam, skindeva; not us [S].
- **Shape:** skindeva 1,067 words, 7 H2, FAQ, video, dated Nov 2025; scrubalildeepa 951 words, 21 H2; ours 1,466 words, 12 H2, FAQ, author, 12 citations, answer-first [S pages].
- **Why they win:** "myths and facts" and "Botox in a bottle" framing on domains with 714 to 881 referring domains [S authority]. We lose on authority only.
- **Changes:** (1) first sentence carries "Argireline", "crow's feet" and the number: 22 of 45 graded clearly smoother in 4 weeks, 0 of 15 on placebo; (2) a sibling sentence naming Raikou and Tadini, both linked, and a hub up-link with the anchor "Argireline"; (3) a visible "Reviewed" date;
- **Job:** credibility and citation, plus the multilingual long tail. **Watch:** hub position for "argireline", non-English impressions, AIO citation. **Target:** US top 20 by 5 Jan 2027.

## 2. Raikou 2017 (`argireline-forehead-roughness-trial-raikou-2017`)

- **Question and demand:** "argireline forehead lines": 0 [D]. Forehead demand is shopping: "cream for forehead lines" 720 (ads volume), difficulty 17; clickstream 0 [T]. That belongs to /pages/fine-lines-wrinkles.
- **Rank and index:** no SERP pulled; indexed, crawled 4 Oct [UI]; 20 impressions, pos 29.2 [D].
- **Who answers today (one WebSearch):** retailer pages (Adore Beauty, Sephora, The Ordinary stockists) and a generic "may soften, unlikely to freeze" blurb with the supplier's "up to 30%". No one cites a trial.
- **Proposed question:** nobody searches the phrase. The article can own the paper's identity: it is titled for "tripeptide-10-citrulline and acetyl hexapeptide-3". Volumes for "tripeptide-10 citrulline", "argireline 10% study" and "argireline forehead wrinkles" are unmeasured (about USD
  0.05 to check).
- **Changes:** (1) keep the H1; (2) open with the instrument result: roughness -7.4% vs +4.3% on placebo, P = .022, 24 women, skin imaging; (3) the paper's full title in the first FAQ answer; (4) a down-link to /pages/fine-lines-wrinkles for shoppers. Do not retitle toward "best cream".
- **Job:** citation only. **Watch:** impressions on paper-title queries. **Target:** none for rank.

## 3. Badenhorst 2016 (`copper-peptide-wrinkle-trial-badenhorst-2016`)

- **Question and demand:** "copper peptide serum wrinkles": 0 [D]. The nearest measured question the trial answers is "matrixyl vs copper peptides": 50 (floor), competition 0.03 [T].
- **Rank and index:** no SERP pulled; indexed, crawled 30 Sept [UI]; 83 impressions, pos 11.6, 2 clicks [D]; "ghk-cu badenhorst" pos 5.4 [GSC].
- **Who answers today:** product pages quoting brand percentages, a Dermatology Times Q&A, and a 2015 NZ Herald/Viva story that is the same trial as Snowberry's marketing ("31.6% above Strivectin") [WebFetch nzherald.co.nz, 25 Mar 2015].
- **Why it matters:** the trial's best-known number was published by its sponsor. An independent appraisal ("maker-funded, concentration never stated") fills a real gap, and the page already says it.
- **Changes:** (1) keep the 60-character title; (2) decision: test "Copper Peptide vs Matrixyl 3000: The Badenhorst 2016 Trial" (58 characters), since the 31.6% result is the only one tied to a measured question; it is the trial's own comparison, so it fits ADR-2026-09-30-K; (3) both
  results in one opening paragraph; (4) funding line in the first screen; (5) sideways link to Robinson.
- **Job:** credibility. **Watch:** paper-name queries, copper hub position. **Target:** hold position 11 or better.

## 4. Ye 2026 (`pdrn-vs-retinol-split-face-trial-ye-2026`)

- **Question and demand:** "Can PDRN outperform retinol on crow's feet?" "pdrn vs retinol": 352 US, 79 GB, CPC 2.20 [D].
- **Rank and index:** not in US desktop top 10 on 7 or 8 Oct [V7; S]; indexed, crawled 4 Oct [UI]; 261 impressions, 6 clicks [D].
- **Page one:** a houseofcommunal blog on acne-prone skin (#1, off-intent), a LinkedIn post, a YouTube short, Reddit, Skinsort, TikTok. No medical page; no AI Overview [V7].
- **Shape:** #1 1,350 words, 13 H2, no author, no sources; #2 459 words; #3 video. Ours 1,608 words, 12 H2, answer-first, author, 6 citations [V7 pages].
- **Why they win:** on merit they do not. It is the thinnest SERP in the set; we are three weeks old with no links.
- **Changes:** (1) title with the searcher's words first: "PDRN vs Retinol: What a 31-Woman Split-Face Trial Found" (54 characters); (2) first 40 words hold PDRN, retinol, 0.1% each, and up to 23% vs about 6 to 7%; (3) a plain head-to-head table of the four instruments above the chart; (4)
  the PDRN hub gets a "PDRN vs retinol" paragraph linking here with that anchor; Yogya is the sideways link; (5) "Reviewed" date.
- **Job:** the one study page with a real rank job. **Watch:** query-level position for "pdrn vs retinol", US and GB. **Target:** top 5 US by 8 Jan 2027; top 3 by April if one genuine link lands.

## 5. Yogya 2022 (`pdrn-microneedling-split-face-trial-yogya-2022`)

- **Question and demand:** owner term "pdrn after microneedling" has 0 clickstream. "pdrn microneedling": 403 US, 78 GB, CPC 6.06 [D].
- **Rank and index:** not top 10; **unknown to Google**; 0 impressions [UI; D].
- **Page one:** clinics and aesthetics sites (Yoo Direct Health, Renuyou, Aura PDX, MDPen, Parlour Miami), Reddit #2, Facebook #4. No medical page. AIO cites seven clinic or blog pages and Instagram; no PMC [S].
- **Shape:** #1 Yoo 1,974 words, 18 H2, answer-first, FAQPage schema, **0 citations**; #3 Renuyou 1,161 words; ours 1,992 words, 12 H2, 8 citations, **not answer-first**, referring domains 0 vs 4 [S pages; report.md].
- **Why they win:** clinics hold the "book this treatment" intent with local authority. None cites a trial. We match them on length and beat them on evidence, but are invisible.
- **Changes:** (1) get indexed; (2) primary becomes "pdrn microneedling", H1 stays trial-specific; (3) title "PDRN Microneedling: What the Yogya 2022 Trial Found" (50 characters); (4) answer-first opening: 29 women, wrinkles around the eyes eased significantly in 2 months on the
  polynucleotide side vs 6 on saline, level by 6; (5) a block "Is this evidence for PDRN at home?" answering no, because it was a clinic radiofrequency procedure; (6) sideways to Ye, up to the hub.
- **Target:** indexed within 14 days of the request; top 20 by 8 Jan 2027. Highest value once indexed (CPC 6.06).

## 6. Watanabe 2014 (`glutathione-skin-brightening-trial-watanabe-2014`)

- **Question and demand:** owner term "glutathione brighten skin": 0 clickstream. "topical glutathione": 302 US, CPC 4.12; GB 0 [D].
- **Rank and index:** not top 10; indexed, crawled 3 Oct [UI]; 5 impressions, pos 28.2 [D].
- **Page one:** Reddit x3, Quora, RealSelf x3, a LinkedIn post, a 91-word 2023 trade item. The weakest page one in the set. AIO cites PMC12710870, JCAD, PubMed 41416233, Dermatology Times and clinics; not us [S].
- **Shape:** #2 91 words, #3 487 words; ours 1,756 words, 12 H2, answer-first, 11 citations [S pages].
- **Why they win:** forums win an empty field; the Overview prefers clinical literature, which is where we belong.
- **Changes:** (1) primary "topical glutathione"; title "Topical Glutathione: The Watanabe 2014 Skin Trial" (49 characters); (2) first sentence defines the form tested: 2% oxidised glutathione lotion, split-face, 30 women, melanin index -10.7% vs -3.1% (p < 0.001), 10 weeks; (3) maker
  funding (Kyowa Hakko Bio) in the first screen; (4) check the hub answers "can glutathione absorb through skin" (the Overview's own source titles ask it); add it to the hub, not here; (5) "brighter-looking", never "lightening".
- **Target:** top 10 by 8 Jan 2027 (the field is forums). An Overview citation is possible but unlikely against PMC.

## 7. Tadini 2015 (`argireline-skin-firmness-trial-tadini-2015`)

- **Question and demand:** "acetyl hexapeptide-3": 151 US, CPC 7.99; GB 0 [D]. It is a naming query, not a firmness question.
- **Rank and index:** not top 10; **unknown to Google** [UI].
- **Page one:** cellbone supplier #1 (117 words), Wikipedia "Acetyl hexapeptide-8" #2, PubChem #3, **ResearchGate: Tadini's own paper #4**, Cosmetics & Toiletries, SpecialChem, a research-peptide seller. AIO cites Wikipedia, PubChem, the Tadini page, SpecialChem; not us [S].
- **Shape:** ours 1,757 words, 12 H2, 6 citations, **not answer-first** [S pages].
- **Why they win:** dictionaries and suppliers answer "what does this name mean". Google already ties the query to Tadini's paper.
- **Changes:** (1) request indexing; (2) definition-first opening: "Acetyl hexapeptide-3 is the older name for acetyl hexapeptide-8, sold as Argireline. In Tadini 2015, a 10% cream lowered facial anisotropy by about a third in two weeks" (confirm the naming against the register); (3)
  up-link to the hub with "acetyl hexapeptide-8" so the hub keeps that term; (4) paper and public-university funding in the first screen.
- **Target:** indexed in 14 days; rank 6 to 10 by 8 Jan 2027 (slots 5 to 9 are thin). An Overview citation is plausible since it already cites this paper.

## 8. Robinson 2005 (`matrixyl-wrinkle-trial-robinson-2005`)

- **Question and demand:** "palmitoyl pentapeptide-4": 251 US, **316 GB**, CPC 2.95 [D].
- **Rank and index:** not top 10; **unknown to Google** [UI].
- **Page one:** EWG #1 (blocked to bots), a forum, a formulator shop (203 words), Creative Peptides (1,092 words, no author), two Skinsort lists, Skincarisma. AIO cites INKEY decoder, Wikipedia, suppliers, Paula's Choice EU; not us [S].
- **Shape:** ours 1,764 words, 11 citations, not answer-first; the best-sourced page in the set [S pages].
- **Changes:** (1) request indexing; (2) definition-first: the original Matrixyl, 3 ppm, 93 women, split-face, 12 weeks, ahead of placebo from week 8, with the P&G authorship and small effect in the same screen; (3) one sentence separating it from Matrixyl 3000, linked to the hub; (4) pull
  a GB SERP (GB volume is higher).
- **Target:** indexed in 14 days; top 15 by 8 Jan 2027, otherwise a citation page.

## 9. The list page (`/blogs/clinical-studies`)

- **Demand:** "skincare clinical studies": 0 in every market [D]. Indexed; 11 impressions, pos 26 [UI; D].
- **Page one:** dermatology clinics recruiting trial volunteers (SkinDC, CTR4Dermatology, Pure Dermatology), clinicaltrials.gov. AIO cites skincareresearch.org, Citrus Labs, CenterWatch, De Nova [V7].
- **Shape:** ours 421 words, 2 H2, Breadcrumb schema only, performance 66, LCP 12.2 s lab mobile, 2,724 KiB [V7 pages; D lighthouse].
- **Honest read:** searchers on this phrase want to enrol in a trial. Ours publishes appraisals, so the term brings the wrong visitor and will not rank. It works as a hub: all eight articles are linked. The 10 `/blogs/clinical-studies/tagged/*` archives it links to are self-canonical thin
  pages (not audited).
- **Changes:** (1) `CollectionPage` + `ItemList` schema; (2) a quotable evidence table (ingredient, trial, size, result, year); (3) lazy-load and right-size card images; (4) measure "argireline clinical trial" and "peptide clinical trials" before any retarget.
- **Job:** navigation and entity page. **Watch:** articles indexed (8 of 8 by 22 Oct), list-to-article clicks in GA4. **Target:** no rank goal.

---

## End

### (1) Ranked actions, impact against effort

| # | Action | Impact | Effort |
|---|---|---|---|
| 1 | Request indexing for Yogya, Tadini, Robinson | High: 3 of 8 pages invisible | 5 minutes, manual |
| 2 | Yogya: "pdrn microneedling", answer-first, "at home?" block | High (403 US, CPC 6.06) | Low |
| 3 | Ye: searcher-words title, number up front, head-to-head table, hub anchor | High (352 US; best live signal) | Low |
| 4 | Watanabe: "topical glutathione", definition-first | Medium (302 US, weakest SERP) | Low |
| 5 | Tadini and Robinson: definition-first openings | Medium (151 US; 251 US + 316 GB) | Low |
| 6 | One genuine link to Ye or the PDRN hub | Highest: it is what separates us from every page above | High, outside the repo |
| 7 | Key-figure tiles out of H2s, in the STUDY-DETAIL go-live so translations are done once | Medium | Medium (8 x 6) |
| 8 | List page: schema, evidence table, image weight | Medium | Medium |
| 9 | Wang, Raikou, Badenhorst: openings, sibling links, dates | Low | Low |
| 10 | About USD 0.30 of checks: volumes for Raikou and list candidates, GB SERPs for Robinson and Yogya | Enables 2, 5, 8 | Low |

### (2) Proposed `configs/page-targets.json` changes

| Page | Now | Proposed | Basis |
|---|---|---|---|
| Yogya | pdrn after microneedling | **pdrn microneedling**; secondary keeps the old term | 403 US vs 0 [D] |
| Watanabe | glutathione brighten skin | **topical glutathione**; old term becomes secondary | 302 US vs 0 [D] |
| Badenhorst | copper peptide serum wrinkles | keep; option B "copper peptide vs matrixyl 3000" if approved | 50 floor [T] |
| Wang | argireline crow's feet | keep; add "argireline before and after" (unmeasured) | GSC long tail |
| Ye, Tadini, Robinson | unchanged | unchanged | measured already |
| Raikou, list | as now | keep until the volume check; list gets a `_note` on trial-recruitment intent | 0 measured |

Add a `_job` field, `rank` (Ye, Yogya, Watanabe, Tadini) or `citation` (the rest and the list), so audits stop scoring citation pages on position.

### (3) Open questions for Malcolm

1. Retarget Yogya and Watanabe to the measured terms? It amends the ADR-2026-09-30-K table.
2. Badenhorst: test the "Copper Peptide vs Matrixyl 3000" framing, given that its sponsor already markets that number?
3. Tadini: may the first sentence say acetyl hexapeptide-3 is the older name of -8? (Needs a register check.)
4. May the key-figure tiles stop being headings, in the same go-live as the STUDY-DETAIL English?
5. "Skincare clinical studies" was your term (30 Sept), but the SERP shows people looking to enrol in trials. Keep it, or test a replacement?
6. Who presses Request indexing on three URLs this week?
7. Do we want one outreach push for a single genuine link, and to whom?
