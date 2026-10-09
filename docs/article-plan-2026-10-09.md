# New articles plan: the keywords nobody on the site owns, and how each article beats today's top 3 (2026-10-09)

**For:** Malcolm. **Status:** plan for decision; nothing written or published. **Fits inside:** the traffic and performance
plan of 2026-10-08 (`docs/website-traffic-and-performance-plan-2026-10-08.md`), Track C ("content that fills unowned
questions"). It replaces that plan's spoke list where the two differ, and changes nothing else in it.
**Evidence:** `audits/2026-10-09-new-article-keywords/` (README is the evidence record). **Spend today:** DataForSEO
about USD 9.60; Search Console free.

---

## The short version

1. **Our keyword research had a blind spot.** It only counted searches that contain one of our ingredient names, so it
   never measured the problems our products address. Today's research pulled 19,238 US and 17,212 GB keywords on related
   topics, each with its observed monthly searches.
2. **Most of the 15 planned blog articles have almost no searches.** For example, "copper peptide with vitamin C" and
   "how to use a PDRN serum" have zero observed searches a month, and both repeat questions the hub pages already answer.
   Of the 15, three survive as written, two merge into stronger new articles, one is retargeted, three are blocked by the
   claims rules or an open decision, one waits for German data, and five are dropped or folded into existing pages (Part 3).
3. **The real unowned demand is in problem-led questions**, at ten times the volume of the ingredient questions:
   "crows feet" (9,714 US / 2,613 GB searches a month), "salmon sperm" (1,759 / 1,029), "forehead wrinkles" (1,610 /
   554), "at home microneedling" (1,510 / 475) and "copper uglies" (1,157 US).
4. **We hold an edge nobody on page one has: published trials.** Across the top 3 for every planned article, almost no
   page cites a single study. We already host appraisals of five trials that measured crow's feet, of the only controlled
   facial tolerance figure for copper peptides, and of the only two controlled trials of PDRN on skin.
5. **The first wave is four articles** (Part 4): spoke 1 on Argireline and Matrixyl (already drafted, 9.68), then crow's
   feet, copper uglies, and salmon sperm skincare vs the salmon sperm facial. A second wave adds forehead wrinkles, a
   "how to choose a PDRN serum by the label" guide and Matrixyl Synthe'6. Microneedling, under-eye wrinkles and the copper
   guides wait for their gates.
6. **None of them competes with existing content** (Part 5). No page of ours has a top-10 position for any new primary
   term in 90 days of Search Console data (the few hits are 1 to 3 impressions on other terms). Each article's Google
   results share at most one of their top 10 with the results for the nearest page's own keyword.
7. **Honest targets:** page one in 3 to 6 months for copper uglies and GB crow's feet; 6 to 12 months for US crow's feet,
   salmon sperm skincare and forehead wrinkles. The top 3 on the bigger terms needs the off-site work in the traffic plan:
   the small clinic sites above us still have 40 to 1,500 referring domains against our 0 genuine ones.
8. **Rough value:** if wave 1 reaches those targets, about 600 to 1,200 extra organic clicks a month, against about 150
   today.
9. **Researched, and recommended not to build** (Part 4.4). Smile lines and neck wrinkles: a cream cannot honestly serve them,
   and no trial of ours measured them. GB "polynucleotides" (4,750 a month): all clinics. The derma-stamp hair terms:
   Hairgenetix already plans pages for them.
10. **Ten decisions are yours** (Part 7). The ones that unblock the most are approving the list, the rule on naming
    competitors in "best X" guides, and the microneedling register conflict.

---

## Part 1 — Where the visibility work stands today

| Area                       | State on 2026-10-09                                                                                                                                                                                                                                                                                    | Source                                          |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------- |
| Traffic                    | 35 organic clicks a week (w/c 2026-09-28), five weeks old in Google's eyes; no brand demand; no top-10 position on any target term; the AI Overview cites us only on our own brand name                                                                                                                | traffic plan Part 2.1                           |
| The plan                   | Five tracks: A indexing and on-page to the bar, B authority and reviews, C new content, D speed and conversion, E markets. 37 pages have a keyword owner in `configs/page-targets.json`                                                                                                                | traffic plan Part 4                             |
| Speed (Track D)            | the hero no-fade rule is live on 23 templates; live LCP on the collagen page fell from about 14 s to 4.0 to 4.4 s                                                                                                                                                                                      | commits `544e11b`, `f5ed1a8` (ADR-2026-10-09-Y) |
| Pages to the bar (Track A) | nine product-page drafts for your approval (`docs/drafts/product-pages-2026-10-09/`); the Skin Solutions pages now link to `/pages/skin-concerns` and back; another window is tearing down the top 4 for every existing page's term                                                                    | `f5ed1a8`; window 14                            |
| Content (Track C)          | 5 ingredient hubs and 8 clinical-study articles live; the Learn blog (`/blogs/learn`) is empty and hidden from Google until its first article; spoke 1 ("Argireline and Matrixyl 3000 together", 1,147 words, audit 9.68) waits for your approval; 15 spokes planned in `docs/content-plan-2026.md` §5 | site inventory today                            |
| Decisions open             | 17 in the traffic plan Part 7 (indexing requests, keyword ownership, off-site budget, formula sheet, stamp sets, and more)                                                                                                                                                                             | traffic plan Part 7                             |

What was missing, and what this document adds: the keyword research only ever measured phrases that contain one of our
ingredient names, so no one had measured the questions people ask about the problems our products address. The 15
planned spokes had never been checked against observed searches. And no planned article had a teardown of its own top 3.

---

## Part 2 — What the new research found

### 2.1 The blind spot in the September research

The September pull asked DataForSEO for "every keyword containing _pdrn_", "every keyword containing _copper peptide_",
and so on, stopping at 700 per ingredient. That method cannot find a search that does not name the ingredient. Today's
pull used three methods on 78 seeds per market (phrase match, questions only, and Google's own "related searches" graph,
which finds neighbours that share no words with the seed), in the US and GB: 19,238 and 17,212 keywords, cut to 11,680 and
7,392 after removing duplicates and off-topic terms, each with its observed monthly searches (clickstream, the traffic
signal the strategy trusts, not Google Ads' rounded buckets).

Most of the generic "peptide" demand turned out to be the wrong audience: "what are peptides" (38,211 US) and "are
peptides safe" (6,787) are dominated by injectable and bodybuilding peptides and oral collagen. Those were removed.

### 2.2 Where the unowned demand is

Observed searches a month, summed across the unowned topical terms in each cluster (US / GB):

| Cluster                                  | Demand US / GB                                          | Biggest single terms                                                                   | Fits our products and evidence?                                                |
| ---------------------------------------- | ------------------------------------------------------- | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| At-home microneedling and derma stamps   | 50,919 / 17,313                                         | derma stamp 8,154 / 3,088 (a shop term); at home microneedling 1,510 / 475             | yes: two stamp sets; but see decision 4                                        |
| Smile lines                              | 20,505 / 6,725                                          | smile lines 9,613 / 3,404; how to get rid of smile lines 2,768 / 1,425                 | partly: no trial measured smile lines                                          |
| Polynucleotides, salmon, skin boosters   | 18,703 / 20,321                                         | polynucleotides 703 / 4,750; salmon sperm 1,759 / 1,029; salmon sperm facial 553 / 237 | yes: PDRN serum and cream; injections only as context                          |
| Crow's feet and eye lines                | 15,234 / 3,719                                          | crows feet 9,714 / 2,613; crows feet eyes 1,157 US                                     | **yes, strongly: two of our trials measured crow's feet (Wang 2013, Ye 2026)** |
| Copper peptides (beyond the hub's terms) | 11,383 / 2,291                                          | copper uglies 1,157 US                                                                 | yes: copper serum and creams                                                   |
| Forehead lines                           | 6,427 / 2,213                                           | forehead wrinkles 1,610 / 554; how to get rid of forehead wrinkles 1,258 / 237         | yes: one trial (Raikou 2017)                                                   |
| Neck and crepey skin                     | 16,461 / 3,477                                          | crepey skin 3,221 / 633 (mostly arms and legs); neck wrinkles 1,006 / 316              | weakly: no trial on the neck                                                   |
| Our own ingredients' question long tail  | PDRN 2,354 US over 174 terms; Argireline 1,201 over 134 | none above 300                                                                         | already answered by the hubs                                                   |

Two conclusions. First, the problem-led questions (crow's feet, forehead lines, smile lines) carry ten times the demand of
the ingredient questions we planned to answer. Second, our own ingredient long tail is small and mostly already answered
by the hubs, which is why most planned spokes measure at zero (Part 3).

### 2.3 What Google shows for these terms

From 36 live SERPs (23 US, 13 GB, desktop, 2026-10-09):

- **An AI Overview appears on 35 of 36, and cites us on none.** The most-cited sources: YouTube 27, Instagram 16, Google
  11, Cleveland Clinic 9, Healthline 8, Reddit 7, Facebook 6.
- **Page one is mostly clinics and brand explainers, not medical publishers.** Cleveland Clinic and Healthline lead only
  on "smile lines" and appear on the forehead and crow's-feet SERPs; elsewhere the top 3 are aesthetic clinics, small
  brands (3lab, Germaine de Capuccini, Kiehl's, Nivea, Caudalie), Reddit and YouTube.
- **The top 3 almost never cite research.** Of the measured top-3 pages, nearly all link to no study at all. Our study
  articles cite 6 to 12 sources each, and we hold the only appraisals of the trials that measured crow's feet, forehead
  roughness and copper peptide tolerability.
- **The pages at #1 have few links of their own** (0 to 22 referring domains on the page, except Cleveland Clinic and
  Healthline at 87 to 258), **but their sites have more than ours** (small clinics 40 to 1,500 referring domains; ours 2,
  of which 0 genuine). So a better page can reach page one on the thin SERPs, while the top 3 on the publisher-led SERPs
  still needs the off-site track.
- **Hacked-site spam** (stonevillenc.org) holds five of the top seven slots for "can you use copper peptides with retinol"
  and one for "matrixyl synthe 6 benefits".

### 2.4 What people ask that the tools miss

PDRN is the fastest-rising ingredient of 2026 (Spate: 37.2 million monthly interactions across Google, TikTok and
Instagram, up 610% a year). The open doubt everyone raises and no brand answers is whether PDRN does anything on the skin,
or only as an injection (Dermatology Times; Marie Claire UK). "Copper uglies" is a Reddit term repeated by retailers with no
trial behind it. People Also Ask on the eye and smile-line SERPs asks "What do Koreans do for smile lines?" and "What do
Koreans use for under eye wrinkles?", a K-beauty angle PDRN fits. Sources: `audits/2026-10-09-new-article-keywords/community-and-trends.md`.

---

## Part 3 — The 15 planned spokes, re-checked against observed searches

The plan's spokes were sized on Google Ads buckets and never measured. Observed searches a month (US / GB), and what each
collides with on the site today:

| #   | Planned spoke                                          | Target term: observed US / GB                                                         | Collides with                                                                     | Verdict                                                                                             |
| --- | ------------------------------------------------------ | ------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| 1   | How to use a PDRN serum                                | how to use pdrn serum 0 / 0 (how to use pdrn 50; when to use pdrn serum 50)           | the PDRN hub's how-to section                                                     | **fold into the hub**; do not write                                                                 |
| 2   | PDRN vs retinol, and using both                        | pdrn vs retinol 352 / 79                                                              | the Ye 2026 article owns it                                                       | **already decided**: the comparison and "can you use both" go on the Ye article                     |
| 3   | Best PDRN serums, compared                             | best pdrn serum 654 / –                                                               | nothing, but a "best X" page names competitors, which the claims registers forbid | **blocked**: decision 3                                                                             |
| 4   | PDRN vs polynucleotides                                | no measured volume (GB "polynucleotides" 4,750 is clinic intent)                      | –                                                                                 | **merge into new article A3** (the salmon sperm facial and polynucleotides)                         |
| 5   | Salmon vs vegan PDRN                                   | vegan pdrn 252 / –                                                                    | nothing                                                                           | **keep, gated** on the sourcing facts (decision 5)                                                  |
| 6   | Copper peptides with vitamin C and retinol             | copper peptide with vitamin c 0 / 0; can you use copper peptides with retinol 151 / 0 | the copper hub's "what not to mix" FAQ                                            | **retarget to retinol** (see Part 4)                                                                |
| 7   | Best copper peptide serums, compared                   | best copper peptide serum 503 / 79                                                    | as 3; the traffic plan also said "only after a roundup lists us"                  | **blocked**: decision 3                                                                             |
| 8   | Copper peptide side effects                            | copper peptide side effects 0 / 0                                                     | the copper hub's safety block                                                     | **replace with new article A4** ("copper uglies", 1,157 US)                                         |
| 9   | 1% vs 2% GHK-Cu                                        | no measurable demand                                                                  | the copper hub FAQ; concentration facts unconfirmed                               | **drop** (hub FAQ)                                                                                  |
| 10  | Argireline vs Botox                                    | unmeasured                                                                            | the register forbids Botox comparisons; your decision 12 is open                  | **blocked**                                                                                         |
| 11  | Argireline and Matrixyl together (spoke 1)             | matrixyl and argireline 858 US                                                        | a Matrixyl hub FAQ line (minor)                                                   | **keep**: drafted, audited 9.68, waiting for your approval                                          |
| 12  | Matrixyl 3000 vs Synthe'6                              | matrixyl synthe 6 benefits 251; matrixyl synthe 6 100 / 79; vs 100                    | nothing                                                                           | **keep** (Part 4)                                                                                   |
| 13  | Ist Matrixyl 3000 schädlich? (DE)                      | German demand not yet measured                                                        | the Matrixyl hub's "Is Matrixyl 3000 safe?" FAQ                                   | **hold** until the German pull                                                                      |
| 14  | Glutathione side effects on skin                       | glutathione side effects skin 0 / 0 (the head term, 1,157, is oral supplements)       | the glutathione hub FAQ                                                           | **drop**                                                                                            |
| 15  | Peptide serum with vitamin C                           | 0 / 0                                                                                 | the FAQ page                                                                      | **drop**                                                                                            |
| +   | How to choose a peptide moisturizer (traffic plan 3.2) | peptide moisturizer 553 US (pulled 2026-10-08)                                        | the creams collection lists it as a secondary                                     | **keep as the traffic plan says**, after the creams collection rebuild; window 14 owns its teardown |

So of the 15: three survive as written (11, 12, and 5 once unblocked); two merge into stronger new articles (4, 8); one is
retargeted (6); three are blocked by the claims rules or an open decision (3, 7, 10); one waits for German data (13); and
five are dropped or folded into the pages that already answer them (1, 2, 9, 14, 15).

---

## Part 4 — The articles to write

### 4.1 The list, in the order to write them

Demand is observed searches a month, US / GB, for the primary term and, after "+", the whole cluster the article answers.
"Top 3 today" is the desktop SERP of 2026-10-09; mobile was pulled for every primary term and differs where noted. Every
target assumes the article is indexed in its first week and the off-site track starts (traffic plan Part 5).

| #                             | Article (SEO title)                                         | Primary term                             | Demand US / GB                                                            | Top 3 today                                                                                             | Why we can win                                                                                                                                 | Target                                               |
| ----------------------------- | ----------------------------------------------------------- | ---------------------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| **Wave 1: weeks 1 to 4**      |                                                             |                                          |                                                                           |                                                                                                         |                                                                                                                                                |                                                      |
| S1                            | Matrixyl and Argireline: What the Trials Show (drafted)     | matrixyl and argireline                  | 858 US                                                                    | thin blogs and forums (2026-10-07)                                                                      | drafted, audited 9.68; we sell both and appraise both trial sets                                                                               | first in 3 months                                    |
| A1                            | Crow's Feet: What Causes Them and What Really Helps         | crows feet                               | 9,714 / 2,613; cluster about 12,500 / 3,100                               | US: a 2014 London clinic page, a surgeon's 478-word list, a brand blog; GB: two clinics, Today.com      | five trials we host measured crow's feet; none of the six top-3 pages names a single study                                                     | GB page one in 3 to 6 months; US page one in 6 to 12 |
| A2                            | Copper Uglies: What They Are and How Long They Last         | copper uglies                            | 1,157 US; cluster about 1,650                                             | Reddit, Dermalogica (never uses the term), YouTube                                                      | the only controlled facial tolerance figure (39 of 40); the AI Overview's main claim cites a review PubMed does not contain                    | page one in 3 months, top 3 in 6                     |
| A3                            | Salmon Sperm Skincare vs the Salmon Sperm Facial, Explained | salmon sperm skin care                   | 703 US; plus salmon sperm 1,759 / 1,029 and salmon sperm facial 553 / 237 | a 549-word clinic blog calling DNA "a protein", CNN Underscored, a Facebook video                       | none of 27 top-3 results across nine salmon SERPs names a controlled trial; we appraise both                                                   | page one in 6 months, top 3 in 12                    |
| **Wave 2: weeks 4 to 10**     |                                                             |                                          |                                                                           |                                                                                                         |                                                                                                                                                |                                                      |
| A4                            | Forehead Wrinkles: Causes and What Helps                    | forehead wrinkles                        | 1,610 / 554; cluster about 5,300 / 1,900                                  | a clinic with no author or date, Cleveland Clinic (general), Kiehl's                                    | answer-first and dated where #1 is neither; one forehead trial (Raikou 2017), a thin edge                                                      | US page one in 6 to 12 months; GB is a shop SERP     |
| A5                            | Best PDRN Serum: How to Choose by What the Label Says       | best pdrn serum                          | 654 US (+ about 700 related); GB 315                                      | small affiliate and brand lists (desktop); Yahoo Shopping, Harper's Bazaar and INKEY on mobile          | label reading is the winning angle and our label states 1% (10,000 ppm); names no competitor (decision 3)                                      | page one in 6 months                                 |
| A6                            | Matrixyl Synthe'6 Benefits, and How It Differs From 3000    | matrixyl synthe 6 benefits               | 251 US (uncertain) + about 350                                            | Reddit, a 1,371-word brand page, the hacked spam site                                                   | the honest answer that no study compares the two                                                                                               | top 3 in 6 months                                    |
| **Wave 3: when a gate opens** |                                                             |                                          |                                                                           |                                                                                                         |                                                                                                                                                |                                                      |
| A7                            | At-Home Microneedling: Needle Length, How Often, Aftercare  | at home microneedling                    | 1,510 / 475 (+ 401 / 237)                                                 | Reddit, the FDA, Vogue (US); Dr Pen, Vogue, Trinny (GB)                                                 | sourced honesty on needle length and frequency; a real tool. Gate: decision 4                                                                  | GB page one in 6 to 12 months; US page one in 12     |
| A8                            | What Serum to Use With Microneedling: What Was Tested       | microneedling serum                      | 402 / 237 (+ 151 / 237)                                                   | Reddit threads and 47 to 231-word pages                                                                 | an evidence table (Yogya, Li); the AI Overview names PDRN. Gate: decision 4                                                                    | page one 6 months after publishing                   |
| A9                            | Under-Eye Wrinkles (title when built)                       | under eye wrinkles                       | 302 / 158; cluster about 1,400 / 870                                      | Estée Lauder, two clinics                                                                               | Ye 2026 measured under-eye lines. Gate: A1 draws under-eye impressions                                                                         | page one in 6 months once built                      |
| A10                           | Best Copper Peptide Serum: What the Label Must Show         | best copper peptide serum                | 503 / 78 (+ about 400)                                                    | unstable: Forbes and Innerbody in one pull, spam in another; Good Housekeeping and Healthline on mobile | the 2% we state; a roundup listing would decide it. Gate: a roundup lists us, or 6 months                                                      | page one in 9 to 12 months                           |
| A11                           | Can You Use Copper Peptides With Retinol? How to Layer      | can you use copper peptides with retinol | 151 US; about 950 across the mixing terms                                 | a clinic page, Reddit, five slots of hacked spam (desktop and mobile alike)                             | an open field, but no combination has been tested, so the edge is thin. Gate: the copper hub section (Part 8, row 11) fails to rank in 8 weeks | page one in 3 months if built                        |
| P5                            | Salmon vs vegan PDRN (planned spoke 5)                      | vegan pdrn                               | 252 US                                                                    | Instagram, two vegan-PDRN sellers                                                                       | page one plausible, but the readers want vegan products we do not sell. Gate: decision 5                                                       | build only if decision 5 says so                     |

**Rough value, stated with its assumption:** if wave 1 reaches the targets above at a typical 2 to 5% click rate for
positions 4 to 10 (about 8% in the top 3 for A2, about 10% at #1 for S1), it adds roughly 600 to 1,200 organic clicks a
month, against about 150 a month today (35 a week). That alone covers a large part of the traffic plan's month-6 goal of 500 clicks a week. It is an estimate,
not a forecast; Part 5 of the traffic plan's caveat applies (only 1.74% of new pages reach the top 10 within a year
without links).

**What the AI answers need, on every article:** the answer in the first two sentences (44% of ChatGPT citations come from
the first 30% of a page); the table no competitor has; named trials with their numbers and who paid; a visible date and
the reviewer. The AI Overviews on these SERPs already cite brand explainers (Bioderma, Eucerin and Elemis on crow's feet;
small brand blogs on copper uglies), so a brand page with named trials is eligible.

### 4.2 Wave 1, article by article

The full teardown, factor tables and wording rules for each are in the teardown files; this is what the writer's brief
carries.

#### S1 — Matrixyl and Argireline: What the Trials Show (drafted)

Already drafted (`configs/learn/drafts/argireline-and-matrixyl-3000-together.json`, 1,147 words, audited 9.68 uncapped)
and waiting for your approval of the English and Dr Bodde's review. Publish it first: it is ready, and its publish step
unhides the Learn blog for everything after it. Teardown: `audits/2026-10-07-visibility-forensics/teardown-argireline-matrixyl.md`.

#### A1 — Crow's Feet: What Causes Them and What Really Helps

- **Terms:** crows feet (9,714 / 2,613); how to get rid of crows feet; crows feet eyes (1,157 US); crows feet when smiling;
  fine lines under eyes (251 / 79). Under-eye wrinkles get one section now and their own article later (A9), because
  Google treats them as a separate intent (no shared results).
- **Top 3 torn down** (`teardowns/expression-lines.md`): US #1 facecliniclondon.com, a Botox clinic page from 2014 (2,174
  words, no studies, no author, a factual error about Botox); #2 drhalaas.com, a surgeon's 478-word procedure list; #3
  3lab.com, a brand blog from 2022 (935 words, says laser makes crow's feet "disappear"). GB: perfectskinstudio.co.uk (a
  clinic blog, 115 referring domains to its whole site), thamesdentalandskin.co.uk (305 words), Today.com (a shopping
  article). **Not one cites a study.** On mobile, Cleveland Clinic and Healthline lead in GB.
- **The gap:** nobody separates the line you see when you smile from the line that stays at rest, or says what a cream
  can do about each; nobody answers "crow's or crows' feet?"; the creams mentioned are either sold by the page or brushed
  aside to sell injections.
- **Our edge:** five controlled trials that measured crow's feet, each already appraised on our site: Wang 2013
  (Argireline: 22 of 45 clearly smoother-looking vs 0 of 15 on placebo, 4 weeks), Ye 2026 (0.1% PDRN eye cream vs 0.1%
  retinol: area −23.0% vs −6.6% in 28 days), Badenhorst 2016 (GHK-Cu: 55.8% more wrinkle-volume reduction than the plain
  base, maker-funded), Robinson 2005 (palmitoyl pentapeptide-4, the original Matrixyl, p ≤ 0.10), Watanabe 2014
  (glutathione: visibly softer in 1 in 3 vs none).
- **Outline:** what crow's feet are (and the spelling) · why they show when you smile and why they stay · at what age
  they appear · which skincare ingredients have been tested on crow's feet (the table) · how to choose a cream for crow's
  feet (label, concentration, an ingredient with a crow's-feet trial, SPF; no product list) · can you get rid of them
  naturally · crow's feet and under-eye lines: what the PDRN eye-cream trial measured (answers "What do Koreans use for
  under-eye wrinkles?" honestly: Ye was a Chinese trial, so never call it Korean evidence) · what a professional can offer
  (named as options; different, does not transfer) · using actives near the eyes safely.
- **The table nobody has:** "Five ingredients, one place measured": ingredient and strength · trial · people · length ·
  compared with · what was measured · result · who paid; footnote that the designs differ, the rows cannot be ranked and
  the results describe the ingredient as studied, not our products.
- **Links:** first 150 words up to `/pages/fine-lines-wrinkles` and `/pages/acetyl-hexapeptide-8-research`; sideways to
  the Wang and Ye articles (the others from the table); down to the Argireline serum. **Length:** 1,200 to 1,500 words.
- **Must not:** "48.9% reduction" (Wang is a count); "relaxes muscles", "Botox-like", "needle-free alternative";
  "stimulates collagen" as our claim; any ranking across the rows; "retinol" in the title (the Ye article owns that
  comparison); an image showing lines erased.

#### A2 — Copper Uglies: What They Are and How Long They Last

- **Terms:** copper uglies (1,157 US); copper peptides uglies (150); how long do copper uglies last (100); what are copper
  uglies; side effects of copper peptides. Replaces planned spoke 8, whose terms have no searches.
- **Top 3 torn down** (`teardowns/copper-matrixyl-bestx.md`): #1 a Reddit thread; #2 Dermalogica's copper peptide
  explainer (1,068 words, July 2026), which never uses the word "uglies"; #3 a YouTube review. Below them, a 2011 spa forum
  page and The Ordinary's glossary. Four of the six organic results never use the term. Mobile is the same field.
- **The gap:** none defines the term, says how long it lasts, or answers "are they reversible?". The AI Overview's
  explanation comes from a clinic page that cites "a 2023 safety review of 12 studies, 512 participants"; **PubMed holds no
  such review** (checked). Its "use 0.5 to 1%" has no source.
- **Our edge:** Badenhorst 2016, the one controlled facial trial: 39 of 40 women used a GHK-Cu serum for 8 weeks without a
  problem, and the authors saw none of the peeling, dryness or redness they watched for. Its appraisal is live.
- **Outline:** what copper uglies are · is it a real side effect (what the one trial recorded) · copper uglies vs purging ·
  what causes it: known vs guesswork · how long they last, and are they reversible · what to do if your skin reacts ·
  could the rest of your routine be the cause · are GHK-Cu injections the same thing (context only) · FAQ.
- **The table nobody has:** "What you'll read online vs what was measured" ("demolition before construction": lab cells
  only; "lasts 4 to 6 weeks": no study; "use 0.5 to 1%": no study; "a 2023 review of 512 people": not in PubMed; "most
  people react": 1 of 40 in the trial).
- **Links:** up to `/pages/copper-peptide-research` and `/pages/skin-concerns`; sideways to the Badenhorst article; down to
  the copper serum with "patch-test first". No stamp-set link. **Length:** 1,100 to 1,400 words.
- **Must not:** state a mechanism as fact; apply "39 of 40" to our 2% products (the trial's concentration is unstated);
  give durations; touch acne; name brands or creators.

#### A3 — Salmon Sperm Skincare vs the Salmon Sperm Facial, Explained

- **Terms:** salmon sperm skin care (703 US); salmon sperm (1,759 / 1,029); salmon sperm facial (553 / 237); salmon sperm
  for skin (201 / 79); salmon dna facial (301 / 79). Absorbs planned spoke 4 ("PDRN vs polynucleotides") as a section.
  "salmon sperm serum" and "salmon sperm cream" are shop terms and go to the PDRN product pages instead.
- **Top 3 torn down** (`teardowns/pdrn-salmon-polynucleotides.md`): for "salmon sperm skin care", #1 a 549-word South Dakota
  clinic blog that calls PDRN "a protein" (DNA is not a protein), #2 CNN Underscored (a 2,015-word product roundup with
  dermatologists quoted, no studies), #3 a clinic's Facebook video. For "salmon sperm": metroderm.org, BBC (the one page with
  20 links), a med spa. A brand explainer (Dr David Jack's blog) already ranks #7 US and #8 GB, so this kind of page reaches
  page one. Healthline is cited in all five salmon AI Overviews.
- **The gap:** none of the 27 top-3 results names a controlled trial of salmon DNA on skin, and none separates the three
  things sold as a "salmon sperm facial" (injection, microneedling with a serum, a leave-on facial).
- **Our edge:** the live appraisals of the two controlled trials (Ye 2026 on intact skin; Yogya 2022 after clinic
  microneedling) and the label fact "1% PDRN (10,000 ppm), salmon-derived sodium DNA".
- **Outline:** is it made from actual sperm · salmon DNA, PDRN, polynucleotides, sodium DNA: the same thing? · what a
  salmon sperm facial is (three versions; dated, attributed prices) · does it work (three sentences and the route table,
  then a link up to the hub, which owns "does PDRN work") · what a serum or cream can and cannot do, including under the
  eyes · is it safe, and who should avoid it · is it legal (re-verify the FDA position before publishing) · how to read a
  salmon DNA label.
- **The tables nobody has:** "Three routes, three bodies of evidence" (injection; clinic microneedling plus serum; a
  leave-on cream at home), each with who does it, the best human evidence, what it measured and what it does not show;
  and a naming panel showing the name on the label tells you neither molecule size nor route (Yogya's "polynucleotide"
  was smaller than Ye's "PDRN").
- **Links:** up to `/pages/pdrn-research` and `/pages/fine-lines-wrinkles`; sideways to the Ye and Yogya articles; down to the
  PDRN serum. Never the PDRN stamp set. **Length:** 1,200 to 1,400 words.
- **Must not:** "Rejuran in a bottle", "same as" or "alternative to injections", "a facial in a bottle"; DNA repair,
  regeneration, "reaches the dermis"; any Ye number without its footnote; celebrity names (Jennifer Aniston appears in
  People Also Ask; naming her implies an endorsement); suggesting home microneedling with the serum.

### 4.3 Waves 2 and 3, in brief

- **A4 Forehead wrinkles** (after A1 is indexed, so the template is proven): what causes them · is it normal at 20 or 25 ·
  are they genetic · how to prevent them · what skincare can do (Raikou 2017: forehead roughness −7.4% vs +4.3% on
  placebo at day 20, about six women per arm, so the edge is thin) · massage and silicone patches (no evidence reviewed;
  say so) · frown lines between the brows · when to see someone. Never "without Botox" in the title or H1.
- **A5 Best PDRN serum, by the label** (after the PDRN collection rebuild, traffic plan step 1.3): a label checklist any
  reader can apply (declared % and ppm, INCI name, source, what the evidence tested, price per ml), our serum as the worked
  example with its weaknesses, a %-to-ppm converter, a disclosure that we sell one. Never "best" about our own product.
- **A6 Matrixyl Synthe'6** (after its register section is written from Sederma's own data): what Synthe'6 is (palmitoyl
  tripeptide-38, same maker as Matrixyl 3000), what the maker's study found, lab vs faces, the two compared, and the honest
  line that no study has compared them head to head.
- **A7 and A8 microneedling:** one face article (needle length, frequency, technique, aftercare, who should not) and later
  a serum article, both written to `teardowns/microneedling.md`. Neither may tell readers to put our serums on freshly
  needled skin until decision 4 is made. The hair-growth side of derma stamps is left to Hairgenetix.
- **A9 Under-eye wrinkles:** when A1's Search Console data shows under-eye impressions.
- **A10 Best copper peptide serum, by the label:** after a roundup lists us, or in 6 months.
- **A11 Copper with retinol:** the copper hub gets the visible section first (Part 8, row 11); the article only if that
  section has not ranked after 8 weeks.

### 4.4 Researched and not built

| Term                                                                   | Demand US / GB                      | Why not                                                                                                                             | Where it goes instead                                                         |
| ---------------------------------------------------------------------- | ----------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| smile lines; how to get rid of smile lines                             | 9,613 / 3,404; 2,768 / 1,425        | mostly a volume fold a cream cannot fill; no trial of ours measured it; an honest page would be about fillers (an excluded subject) | one honest FAQ on the Fine Lines page; your call on a standalone (decision 6) |
| neck wrinkles                                                          | 1,006 / 316                         | the vertical bands are muscle; no neck trial; INKEY already holds the honest angle                                                  | one FAQ line on the Fine Lines page                                           |
| dehydration lines vs wrinkles                                          | 151 / 79                            | INKEY's 2,632-word page dominates; we add nothing beyond a section                                                                  | a section on the Fine Lines page                                              |
| polynucleotides; what do polynucleotides do; polynucleotides under eye | GB 4,750; 237; 712                  | every organic slot is a clinic selling injections                                                                                   | a section of A3                                                               |
| pdrn vs exosomes                                                       | 100 + 50                            | clinic microneedling intent; no exosome register                                                                                    | none                                                                          |
| derma stamp; how to use a derma stamp; derma stamp vs derma roller     | 8,154 / 3,088; 201 / 316; 251 / 158 | shop and hair-growth SERPs; Hairgenetix plans a page for each                                                                       | "facial derma stamp" on the stamp-set product pages; face headings inside A7  |
| best products to use after microneedling; best at home microneedling   | 50 / 237; 553 / 158                 | need competitor brand names; publisher roundups                                                                                     | answered with criteria inside A7                                              |
| best peptide serum                                                     | 1,110 US                            | publisher-owned (unchanged)                                                                                                         | off-site inclusion                                                            |

---

## Part 5 — No new article competes with existing content

Three tests per article, all measured: (1) does any page of ours already earn impressions for the term (Search Console,
90 days, 664 query-page rows); (2) how many of the top-10 results does the article's SERP share with the SERP of the
nearest page's owner term (two pages compete when Google answers both queries with the same results); (3) does the
article's intent belong to a page by rule (a hub owns "what is X" and "does X work?", ADR-2026-09-30-K; a product owns the
shop term).

| Article                       | Primary term               | Our impressions on it (90 days)                                                       | Nearest existing page and its term                                                                                        | Shared top-10 results           | Resolution                                                                                                                                                                                         |
| ----------------------------- | -------------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- | ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A1 Crow's feet                | crows feet                 | 0 (3 for "copper peptides for crows feet", copper hub, position 18)                   | Wang 2013 article ("argireline crow's feet"); Fine Lines page ("fine lines and wrinkles"); Ye article ("pdrn vs retinol") | 0; 0; –                         | no conflict; "retinol" stays out of the title; the Wang and Ye articles link up to A1                                                                                                              |
| A2 Copper uglies              | copper uglies              | 0                                                                                     | copper hub ("copper peptide"; tolerance FAQ q8)                                                                           | 0                               | the hub keeps its term; q8 links to A2 with the anchor "copper uglies"; planned spoke 8 retired                                                                                                    |
| A3 Salmon sperm skincare      | salmon sperm skin care     | 0                                                                                     | PDRN hub ("pdrn", "what is pdrn", "salmon dna", section "is PDRN salmon sperm")                                           | 0 with any of the 18 PDRN SERPs | A3 asks "what is it and how does it differ from the facial"; its evidence answer is three sentences and a link up to the hub, which keeps "does PDRN work"; the shop terms go to the product pages |
| S1 Matrixyl and Argireline    | matrixyl and argireline    | –                                                                                     | Matrixyl hub FAQ line                                                                                                     | –                               | assessed on 2026-10-07; unchanged                                                                                                                                                                  |
| A4 Forehead wrinkles          | forehead wrinkles          | 0 (2 for "forehead argireline before and after", Raikou article, positions 19 and 34) | Fine Lines page; Raikou 2017 article ("argireline forehead lines", no demand)                                             | 0                               | the Fine Lines page gets a paragraph, not the term; Raikou stays the citation                                                                                                                      |
| A5 Best PDRN serum            | best pdrn serum            | 0                                                                                     | PDRN serum ("pdrn serum"); PDRN collection ("pdrn skincare"); PDRN hub ("pdrn")                                           | 0; 0; 0                         | stays informational and links down                                                                                                                                                                 |
| A6 Matrixyl Synthe'6          | matrixyl synthe 6 benefits | 1 impression (the serum, position 32)                                                 | Matrixyl serum ("matrixyl 3000")                                                                                          | 0                               | no conflict                                                                                                                                                                                        |
| A7 At-home microneedling      | at home microneedling      | 0                                                                                     | copper stamp set ("microneedling stamp"); Yogya article ("pdrn microneedling")                                            | 1                               | anchors "copper peptide microneedling stamp set"; no "derma stamp" headings (Hairgenetix)                                                                                                          |
| A8 Microneedling serum        | microneedling serum        | 0 (2 for "ghk cu microneedling serum", German copper serum, position 8)               | microneedling collection (lists "microneedling serum" as a secondary)                                                     | –                               | remove it from the collection's secondaries when A8 is built                                                                                                                                       |
| A10 Best copper peptide serum | best copper peptide serum  | 2 (the copper serum, positions 14 and 25)                                             | copper serum ("copper peptide serum"); copper hub                                                                         | 0; 1                            | stays informational and links down                                                                                                                                                                 |

**Between the new articles themselves:** crow's feet vs under-eye wrinkles share no results, which is why A9 is a separate
article, not a section that would try to rank for both; the forehead head term and its "how to" share 7 results counting
the AI Overview, so one article (A4) takes both; the US salmon "facial" and "skin care" SERPs share 3 and the GB salmon head
and facial SERPs share 4, so one article (A3) takes them.

**After publishing:** the traffic plan's 8-week gate applies to each article (Part 6, step 9).

---

## Part 6 — How each article is written, checked and published

The same steps for every article, in this order. "Audit" is the central auditor (`seo-toolkit/scripts/audit_page.py
--criteria v2 --page-type article --keyword "<term>"`, about USD 3 a run; the bar is 9.0 or more with no confirmed
failures, ADR-2026-09-30-Q). Nothing is published while another Skingenetix window is publishing (`ListAgents` first).

| Step | What                            | How                                                                                                                                                                                                                                                                                                                                                                                            | Check                                                                                                          | Undo                            |
| ---- | ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- | ------------------------------- |
| 1    | Writer's brief                  | The article's section in Part 4 plus its teardown file, with the claims register's wording rules **pasted in** (a brief that says "lightening" gets "lightening" back) and the study facts copied from the study article, never re-derived                                                                                                                                                     | the brief names the one primary term, the outline, the table no competitor has, the links and the safety block | none needed                     |
| 2    | English draft                   | `configs/learn/drafts/<handle>.json` (title, SEO title ≤ 60, description ≤ 155, summary, tags, body); `python3 scripts/learn-article-draft.py <config>` checks length (800 to 1,500 words), allowed tags and the forbidden words, then `--apply` puts it on the hidden drafts blog                                                                                                             | the dry run passes; the draft renders at its hidden URL                                                        | delete the draft article        |
| 3    | Images                          | at least two, from existing files first (the research-page standard), each with descriptive alt text; no before-and-after framing                                                                                                                                                                                                                                                              | images load; alt text present                                                                                  | remove the image                |
| 4    | Audit, fix, re-audit            | the central auditor on the hidden draft, read uncapped (a hidden draft fails the indexing gates by design); fix confirmed failures only                                                                                                                                                                                                                                                        | 9.0 or more uncapped, no confirmed failures                                                                    | revert the config               |
| 5    | Review                          | Dr Bodde reviews the claims (her credit appears only after she has reviewed); you approve the English                                                                                                                                                                                                                                                                                          | written yes from both                                                                                          | none                            |
| 6    | Publish                         | `learn-article-draft.py <config> --apply --blog learn --public`; **for the first article only**, set the Learn blog's `seo.hidden` back to 0 (window b2 hid the empty blog today, `gid://shopify/Blog/118556918145`); add the article's owner row to `configs/page-targets.json`; add one exact-match link from the parent page or hub in prose, and the sideways links from the study article | the live URL returns 200, is in the sitemap, and is linked from its parent                                     | unpublish; remove the owner row |
| 7    | Index and track                 | Search Console "Request indexing" for the URL (manual, you); add the term to the weekly monitor config                                                                                                                                                                                                                                                                                         | the URL is indexed within 7 days; the term appears in the weekly report                                        | remove from the monitor         |
| 8    | Measure 14 days, then translate | English only for 14 days (your rule); pull the German, French, Italian, Dutch and Spanish volumes for the term first; then the six-language translation package, German first                                                                                                                                                                                                                  | six-language verify                                                                                            | the translation register        |
| 9    | Cannibalisation gate at 8 weeks | if the article takes more than 30% of its parent's or hub's head-term impressions, de-optimise its title and move the text into the parent                                                                                                                                                                                                                                                     | Search Console per page                                                                                        | revert the title                |

**Cost per article:** about USD 6 for two audit rounds, plus the translation pass. **Time per article:** one working
session to draft and audit, then your and Dr Bodde's review.

---

## Part 7 — Decisions that are yours

Numbered for this plan; where one overlaps a traffic-plan decision (Part 7 there), it says so.

1. **Approve the article list and its order** (Part 4.1): wave 1 is S1, A1, A2 and A3; wave 2 is A4, A5 and A6; wave 3
   waits for its gates. Approve as a block, or strike lines.
2. **Approve the re-check of the 15 planned spokes** (Part 3): retire or fold 1, 2, 9, 14 and 15; merge 4 into A3 and 8 into
   A2; retarget 6; hold 13 for German data. This replaces the spoke list in `docs/content-plan-2026.md` §5.
3. **"Best X" guides and the rule against naming competitors** (A5, A10): (a) keep the rule and write unnamed "how to choose
   by the label" guides (recommended); or (b) a narrow exception: names only in a label-data table, every cell sourced and
   dated to the brand's own label, no ranking words about rivals, a disclosure, a quarterly re-check, and a legal read
   under the EU comparative-advertising rules first.
4. **Microneedling, before A7 and A8 can be written:**
   1. **The register conflict.** The Argireline register forbids our serum with home microneedling, the copper register
      sells the stamp with GHK-Cu, and the PDRN register says "not on broken skin" while a PDRN stamp set is on sale. Your
      choice: (a) only the set's own vials go on needled skin, if point 2 below confirms they are suitable; or (b) needle
      bare skin and apply serums only to settled, intact skin later.
   2. **The vials.** Ask the formulator whether they are sterile, fragrance-free and free of ascorbic acid, and made for
      needled skin.
   3. **Needle length.** Keep 0.5 mm, which is the top of every source's home range, or add a 0.25 to 0.3 mm head for
      beginners.
   4. **The pack.** Four vials sold as "a one-month ritual" implies weekly sessions, where two sources say every 2 to 4
      weeks at 0.5 mm.
   5. **The live wording and the schema.** "Absorb deeper" and "micro-channels" are on the live pages, and the sets carry
      `InStock` where `PreOrder` with a date is right (overlaps traffic-plan decision 13).
   6. **Hairgenetix.** One link from A7 to Hairgenetix's stamp guide for scalp readers: yes or no.
5. **Vegan PDRN** (P5): first fix the contradiction ("every formula is vegan" on the ingredients page against the PDRN cream's
   FAQ), disclose the cream's collagen source, and get the supplier's certificate of analysis. Then decide whether P5 is
   worth building at all, since its readers want vegan products we do not sell.
6. **Smile lines:** an honest FAQ on the Fine Lines page only (recommended), or also a standalone "Smile Lines: What
   Skincare Can and Cannot Do" (GB page one is plausible; it would make no product claim and sell little).
7. **Medical review:** Dr Bodde reviews every article before it goes live, and A3's line on FDA status is re-verified at
   source the week it publishes.
8. **The AI-answer check:** DataForSEO's AI-answer panel (about USD 0.70 a run) to record whether ChatGPT and Perplexity
   cite us on the wave-1 questions before and after publishing. The Google AI Overviews are already tracked free in the
   SERP pulls (overlaps traffic-plan decision 5).
9. **Indexing:** "Request indexing" in Search Console for each article on the day it publishes (manual, a few minutes;
   overlaps traffic-plan decision 1).
10. **Spoke 1's English** (overlaps traffic-plan decision 6): approving it publishes the first Learn article and unhides the
    blog for everything after it.

---

## Part 8 — Found on the way (for the other work tracks)

These are not articles; they belong to the existing pages and are handed to the windows that own them.

| #   | Finding                                                                                                                                                                                                                                                     | Evidence                                           | Belongs to                                                                                                                                                                                               |
| --- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **"matrixyl" on its own has no owner**: 3,573 US / 791 GB observed searches a month; the serum owns "matrixyl 3000"                                                                                                                                         | `classified.json`                                  | decision 3 of the traffic plan; natural secondary for the Matrixyl 3000 serum                                                                                                                            |
| 2   | **"derma stamp" (8,154 / 3,088) and "dermastamp" (3,322 / 1,662) are shop terms** (Dr Pen, Amazon, Target hold page one)                                                                                                                                    | `serp/serp.json`                                   | the two stamp-set product pages, worded for the face; window b2 told today                                                                                                                               |
| 3   | **The hair side of derma stamps belongs to Hairgenetix**: the "how to use a derma stamp" SERPs are mostly hair-growth pages, and hairgenetix.com already ranks #5 for "derma stamp vs derma roller"                                                         | `serp/serp.json`                                   | Hairgenetix; Skingenetix writes only the face intent                                                                                                                                                     |
| 4   | **"Does PDRN work on the skin, or only as an injection?"** is the doubt every 2026 article raises and no brand answers honestly ("does pdrn work topically" 251 US; Dermatology Times, Marie Claire UK). The rule is that "does X work?" belongs to the hub | `community-and-trends.md`; ADR-2026-09-30-K        | a PDRN hub section, within the register (no "reaches the dermis")                                                                                                                                        |
| 5   | **"Peptides vs retinol" is the most repeated People Also Ask question** on every peptide SERP, yet has almost no observed demand of its own (0 to 158)                                                                                                      | `serp/paa-related.json`, 10-07 and 10-08 raw SERPs | a section of The Science "Peptides for skin" pillar (traffic plan 1.4c), with no superiority claim                                                                                                       |
| 6   | **The Learn blog is hidden** (noindex, out of the sitemap) since window b2 hid it today, because it was empty                                                                                                                                               | b2 message, 2026-10-09                             | the first article's publish step unhides it (Part 6, step 6)                                                                                                                                             |
| 7   | **"microneedling serum" is still a secondary of the microneedling collection** although the traffic plan dropped it as an advice SERP                                                                                                                       | `configs/page-targets.json`                        | remove it from the collection when article A7 takes it                                                                                                                                                   |
| 8   | **The hacked-site spam holds five of the top seven slots** for "can you use copper peptides with retinol" and one for "matrixyl synthe 6 benefits"                                                                                                          | `serp/serp.json`                                   | add both SERPs to the spam report (traffic plan step 0.6)                                                                                                                                                |
| 9   | **Not yet measured**: the German, French, Italian, Dutch and Spanish volumes for the new topics (mobile was pulled for every primary term)                                                                                                                  | –                                                  | pull before translating any new article                                                                                                                                                                  |
| 10  | **The Fine Lines page overclaims**: its Argireline card lists "frown lines and smile lines" (no trial covers either) and says "visibly relax the look" (the register says "soften the look")                                                                | `teardowns/expression-lines.md` §4                 | the Fine Lines re-aim (traffic plan 1.4a/b); add the dehydration-lines section, a short "by area" block linking A1, the Raikou article and A9, and the smile-line and neck FAQ lines                     |
| 11  | **The copper hub's mixing answer is hidden in FAQ q7**; "can you use copper peptides with retinol" has about 950 searches across the mixing terms and its SERP is held by spam                                                                              | `teardowns/copper-matrixyl-bestx.md` §2            | promote q7 to a visible section, "Using copper peptides with retinol, tretinoin, vitamin C and acids", with a five-row table whose "tested together?" column says No throughout (A11 only if this fails) |
| 12  | **"salmon sperm serum" (201 / 79) and "salmon sperm cream" (50 / 79) are shop terms**                                                                                                                                                                       | `teardowns/pdrn-salmon-polynucleotides.md`         | an FAQ line on the PDRN serum and PDRN night cream ("Is PDRN the 'salmon sperm' ingredient?"); window b2 told today                                                                                      |
| 13  | **The Yogya article is listed as owner of "polynucleotide"** (1,106 / 871 searches), which its trial-specific title cannot serve                                                                                                                            | `configs/page-targets.json`                        | drop it from Yogya's secondaries; A3 covers the definition                                                                                                                                               |
| 14  | **The stamp pages and collection say "absorb deeper" and "through fine, sterile micro-channels"**, which the copper register's conditions forbid; the sets show "Pre-order" with `InStock` schema, not `PreOrder`                                           | `teardowns/microneedling.md`                       | decision 4 and the traffic plan's decision 13                                                                                                                                                            |
| 15  | **The ingredients page says "every formula is vegan"; the PDRN cream's FAQ says it is not** (open since 2026-09-22)                                                                                                                                         | `teardowns/pdrn-salmon-polynucleotides.md`         | decision 5; fix before any vegan-PDRN content                                                                                                                                                            |

---

## Part 9 — Evidence and sources

- Evidence record: `audits/2026-10-09-new-article-keywords/README.md` (every step, generator and cost).
- Keyword data: `raw-*.json.gz`, `candidates-*.json.gz`, `classified.json.gz`, `seeds.json`; generator
  `scripts/keyword-research-adjacent.py`.
- SERPs and measurements: `serp/serp.json`, `serp/raw/`, `serp/paa-related.json`, `serp/pages.json`, `serp/authority.json`,
  `serp/report.md`, `teardowns/measurements.jsonl`.
- Teardowns: `teardowns/expression-lines.md`, `teardowns/pdrn-salmon-polynucleotides.md`, `teardowns/microneedling.md`,
  `teardowns/copper-matrixyl-bestx.md` (brief: `teardowns/BRIEF.md`).
- Search Console, 90 days: `data-gsc-new-topics-90d.json`. Community and trends: `community-and-trends.md`.
- Rules this plan follows: `docs/content-plan-2026.md` §5 to §6 (spokes, linking law), `docs/keyword-strategy-2026.md`
  (scoring), `docs/claims/*.md` (wording), the traffic plan Parts 4, 6 and 9.
