# Decision — menu label, study citations, study pages and internal linking

**Date:** 2026-09-22 · **Asked by:** Malcolm · **Status:** citations linked and claims fixed (done). **Menu: Malcolm chose the label only — "Science" — with no structural change** (a split was applied and reverted, 2026-09-22). Internal-link programme approved 2026-09-22.

Malcolm raised four questions:

1. Would "Peptides" be a better main-menu label than "Learn"?
2. The hubs mention many studies but hardly link them. Is that by design, and is internal linking optimal?
3. Hairgenetix built one human-readable article per scientific study, plus a study hub. Should Skingenetix?
4. Fix the unsupported copper claims on the product pages.

---

## 1. Menu label: replace "Learn", but not with "Peptides"

**Malcolm is right that "Learn" is weak.** NN/g (Apr 2023) says it directly: *"Vague verbs (such as
Explore, Discover, Learn, Partner, etc.) are not effective category names — they offer too little
differentiation."* Our header has **two** of them side by side. "Learn" and "Discover" both point to
`/pages/the-science`, and they overlap.

**"Peptides" would be inaccurate, though.** The evidence:

| Fact | Consequence for a "Peptides" label |
|---|---|
| **PDRN is not a peptide.** It is a polynucleotide (DNA fragments). It is also the flagship: 68% of qualified search opportunity and 4 of 21 products | The biggest thing in the menu would be mislabelled, on a brand whose asset is scientific accuracy |
| Glutathione is technically a tripeptide but is sold as an antioxidant and brightener | It reads as off-topic under "Peptides" |
| Phase 3 adds how-to and layering articles to `/blogs/learn/` | These are not "peptides" either |
| In competitor navs "Peptides" is a **shop filter** (Medik8: Shop → By Ingredient → Peptides) | Users expect products behind it, while our reading content sits there. Our own Shop → By Ingredient already does that job |
| Observed demand for generic "peptide skincare" is ~100 searches/month in the US and 211 in DE (Ads claims 49,500), and it is commercial intent | There is no search upside. Nav links are sitewide boilerplate, which Google discounts as a block |

**Recommendation:**
- **Replace both "Learn" and "Discover" with one descriptive noun: "Science".** It fits the destination (`/pages/the-science`), the brand line and every item in the menu, PDRN included.
- **Carry the peptide identity inside the mega-menu instead:** group **Peptides** (Copper Peptide, Argireline®, Matrixyl 3000) and **Beyond peptides** (PDRN, Glutathione). That is accurate and makes the specialism visible.
- **Rehome "Our Philosophy".** It already sits in the footer; an About link can go there too.
- The header becomes Shop · Skin Solutions · Science · Support.

⚠️ **Not changed yet: this is Malcolm's call.** When it is made, the Impact mega-menu matches blocks by the
*translated label*, so the menu label and the header `menu_item` setting must change together in all six
languages (memory `impact-mega-menu-matches-by-translated-label`).

---

## 2. Study citations were not linked. It was an omission, not a design choice. Fixed

The hub template wrote in-text citations as plain "(Kang et al., 2009)". The only links sat in the References
list at the foot of the page and on the findings cards.

**Measured on the live site before the fix:**
- 14 in-text citations on the upgraded hubs, **0 linked**.
- A reader checking a claim had to scroll past the rest of the page to reach its reference.

**Done 2026-09-22:**
- New tool `scripts/link-citations.py` links the **first mention of each study per section** straight to its
  PubMed record, in a new tab.
- The URL comes from the page's own citation list, so a link can only point at a study the page already
  lists.
- **12 citations linked across PDRN, Argireline® and copper, in all six languages (72 links), verified in live
  HTML.**
- Abdulghani 1998 stays as text because it has no PubMed record; it is cited via Pickart 2015.

**Why direct to PubMed, not to the in-page reference list:**
- It takes one click from the claim to the evidence.
- A jump link on mobile loses the reader's place.
- Google says outbound links are not a ranking factor, so the case is trust and usability, not rank.

---

## 3. One article per study — ⚠️ SUPERSEDED the same day: build a modified version

> **Reversed 2026-09-22 after Malcolm's challenge** (the criterion is the whole site's credibility for Google and AI,
> not per-page conversion). Re-researched in `docs/research-2026-study-hubs-credibility.md`. Verdict: build an
> **Evidence Library + one appraisal page per qualifying human study (~12–18)**. The reasoning below is kept as
> the record of why the first answer was wrong: it judged study pages on clicks.

### Original (superseded) reasoning

The current Skingenetix strategy does **not** include per-study pages, and the evidence supports leaving it
out:

| Evidence | Source |
|---|---|
| 9 study articles, 16 days live: **0.6 clicks/day combined**, 5 of 9 at zero | Hairgenetix `docs/performance-audit-2026-09-21.md` |
| Study/informational articles earned **€0.40 per session vs €3.12** for commercial articles | same |
| One study article: 137,282 impressions, 82 clicks (**0.06% CTR**); the microneedling study cluster: 0.59% | `research-2026-ai-search-and-content-hubs.md` §8 |
| Study articles **outranked their own pillar** (positions 5.1 and 8.6 vs the pillar's 28.5) | Hairgenetix `content-architecture-strategy-2026-09-01.md` |
| ~70% of Hairgenetix's lost impressions were on study articles that never earned clicks | Hairgenetix traffic analysis 2026-09-22 |
| **Hairgenetix's own decision:** *"Stop producing study/science articles… fold study evidence into commercial pages."* Keep the existing ones: two are cited in AI Overviews | Hairgenetix performance audit §P1 |
| Google spam policy (updated 2026-08-28) names **scaled content abuse**. Our hubs cite ~30 papers, so one page each would be ~30 summaries × 6 locales ≈ **180 URLs**, most of them summarising lab studies | research doc §6–7 |

**What we do instead:**
- **Keep the summary where the reader already is.** Each hub grades the evidence by strength, in plain English.
- **Link the claim to its source** (§2).
- **Consider one Evidence Library page later.** It would be a single index of every study the site cites, each with a one-line plain-English verdict and the page that uses it. One URL instead of 180, a natural internal-link hub, and a credibility signal.
- **The bigger credibility lever is the reviewer byline.** Dr Esther Bodde can be named once she has read the pages.

**Exception:** a standalone article for one study only if that study is itself a search target. Nothing in
the keyword data shows one today.

---

## 4. Internal linking: enough links in quantity, weak in quality

Crawl of all 54 English URLs, main content only (header and footer excluded), 2026-09-22:

| Hub | Inbound links | Source pages | Distinct anchors | Head-term (exact-match) anchors |
|---|---|---|---|---|
| PDRN (flagship, 68% of opportunity) | 15 | 13 | 8 | "PDRN" ×1 (added today) |
| Argireline® | 11 | 11 | 7 | **"argireline" ×0** |
| Copper peptide | 22 | 20 | 10 | ~1 |
| Matrixyl 3000 | 19 | 16 | 10 | "Matrixyl 3000" ×2 |
| Glutathione | 10 | 10 | 7 | "glutathione for skin" ×0 |

The target from the Zyppy study is 10–44 inbound links, maximum anchor variety, and at least one
exact-match anchor. Every hub meets the count. **The quality is the problem:**
- 4 of each hub's inbound links are the identical "Read Research" tile row.
- Product pages use one templated anchor ("View the full Clinical Research & Trials").
- `/pages/ingredients` repeats "See clinical studies →" up to 3× to one hub.
- The flagship has fewer prose links than copper.

**Proposed programme (not started; needs Malcolm's go-ahead because it touches ~20 product pages in six
languages):**
1. **Product pages:** replace the templated anchor with a varied, specific one per product, including one exact-match anchor per hub ("what PDRN is", "Argireline®").
2. **`/pages/the-science`, the five ingredient collections and `/pages/ingredients`:** in-prose links with head-term anchors. Remove the repeated "See clinical studies →".
3. **Phase 3 articles:** each links to its hub with a different anchor. This is where most of the new links should come from.
4. **Targets:** PDRN ≥ 20 inbound from ≥ 15 pages with ≥ 12 distinct anchors, and every hub with ≥ 1 exact-match anchor.

---

## 5. Unsupported claims: product pages fixed, and the same claims found elsewhere

**Fixed 2026-09-22, in all six languages, with the read-back and the live HTML both clean:**
- "at a high published strength" (3 copper products)
- "our most-studied hero active" (copper bundle)
- "GHK-Cu is one of the most-studied peptides in skin science", which was in:
  - the clinical-research block on **10** products
  - 1 product FAQ
  - `/pages/firming-skin-density`, `/pages/skin-repair-renewal` and `/pages/collagen-skin-plumping`
  - `/pages/the-science`, twice, including its structured data
- "over 50 published studies" (the-science). PubMed shows 174 GHK-Cu papers, 54 mentioning skin, and 1 indexed clinical trial. It now reads "more than 50 published papers on skin, most of them laboratory studies".

These went through the new tool `scripts/fix-claims.py`. It covers product descriptions, product metafields,
FAQ metaobjects and page templates. It fails its dry run if any language would keep the old claim, and it
supports `--rollback`. The specs are in `configs/claim-fixes/`.

**Still open. These are safety or efficacy claims that are unverified, not refuted, so they get checked at
source per ingredient rather than removed blind:**
- **"Gentle / well-tolerated":** 7 FAQ answers, `/pages/skin-repair-renewal`, `/pages/pdrn-research`, the Argireline page, the Matrixyl page, the homepage and one Matrixyl product description.
- **Matrixyl product copy:** "+117% collagen I / +327% collagen IV" (in vitro).
- **`/pages/our-philosophy`:** "hero actives at meaningful, published strengths".

These belong in the Matrixyl and glutathione hub passes.
