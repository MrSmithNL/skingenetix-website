# Keyword Strategy — Skingenetix, 2026

**Date:** 2026-09-22 · **Status:** Complete. Pairs with `content-plan-2026.md`.
**Scope:** 7 markets · 20,357 raw keywords · 17,279 de-bucketed · 2,450 enriched with observed
clickstream, search intent and difficulty · 12 live SERPs.
**Cost:** $4.13 of DataForSEO credit. **Tool:** `scripts/keyword-strategy.py` (`pull` / `analyse`).
**Data:** `configs/keyword-data/strategy/`

---

## 1. The correction that reorders everything

**Google Ads search volume is modelled and bucketed. It is not demand.** Comparing it against
DataForSEO clickstream — *observed* searches — on this catalogue:

| Term | Ads says | Actually observed | Inflation |
|---|---|---|---|
| **ghk copper peptide** | **135,000** | **757** | **178×** |
| copper peptide | 33,100 | 1,362 | 24× |
| pdrn skincare | 12,100 | 1,817 | 6.7× |
| pdrn serum | 22,200 | 3,936 | 5.6× |
| **pdrn** | 49,500 | **19,734** | 2.5× |

Ranked on Ads volume, **copper peptide looks like the flagship at 135,000**. That number is an artefact
— the same bucket returned for `ghk copper peptide`, `copper peptide ghk` and several other phrasings.
Real observed demand is **757**.

➡️ **Everything below is scored on observed clickstream.** Ads volume appears only as corroboration.
`docs/content-plan-2026.md` was written before this and named copper peptide "the volume hub" — that is
now corrected.

---

## 2. Scoring model

```
opportunity = observed_volume × relevance × winnability
```

| Component | Definition |
|---|---|
| **observed** | Clickstream volume. Falls back to Ads ÷ 3 when clickstream is absent (the measured median ratio here) |
| **relevance** | **1.0** names an ingredient we sell · **0.6** generic category we could win · **0.15** competitor-branded (real demand, wrong audience) · **0.0** off-intent |
| **winnability** | 1.0 at KD ≤ 10, tapering to 0.3 at KD ≥ 40 |

**Off-intent** strips injections, oral supplements, bodybuilding, lab reagents, hair, and skin
conditions. **Brand detection is vocabulary-based, not a list** — a named competitor list can never be
complete, and this catalogue surfaced Theramid, Rejuall, Dr Althea, Centellian, Geek & Gorgeous and
Lico, none of which were on one. Any token outside a seven-language cosmetic vocabulary is treated as a
brand, which fails safe.

---

## 3. Where the opportunity actually is

### By ingredient family — PDRN is 68% of everything

| Family | US | GB | DE | NL | FR | ES | IT | **Total** |
|---|---|---|---|---|---|---|---|---|
| **PDRN** | 43,324 | 16,303 | 7,596 | 1,728 | 4,849 | 263 | 2,654 | **76,717** |
| Generic peptide | 4,530 | 2,765 | 1,204 | 93 | 291 | 270 | 444 | 9,597 |
| Copper (GHK-Cu) | 5,430 | 1,889 | 844 | 613 | 217 | 225 | 140 | 9,358 |
| Argireline / AH-8 | 4,973 | 1,259 | 1,056 | 358 | 674 | 434 | 351 | 9,105 |
| Matrixyl 3000 | 3,427 | 1,574 | 211 | 102 | 217 | 395 | 210 | 6,136 |
| Glutathione | 1,537 | 814 | 422 | 110 | 72 | 39 | 0 | 2,994 |

**PDRN is 8× the next family.** Investment must follow that, not be split evenly across five hubs.

### By market — English is 77% of the opportunity

| Market | Opportunity | Share |
|---|---|---|
| **US** | 63,121 | 56% |
| **GB** | 24,495 | 22% |
| DE | 11,333 | 10% |
| FR | 6,320 | 6% |
| IT | 3,750 | 3% |
| NL | 3,004 | 3% |
| ES | 1,626 | 1% |

➡️ **English-first is the data's answer, not just a workflow convenience.** The store ships worldwide,
so US and GB demand is addressable. The Netherlands — the home market — is 3%.

---

## 4. The hero map — one owner per term

**The rule:** one page per keyword *and intent*. Differentiating two pages by format fails; only intent
works. Opportunity figures are summed across all seven markets; observed volumes shown US/GB/DE.

### Hub pages — informational head terms

| Page | Owns | Opp | Observed US/GB/DE | KD |
|---|---|---|---|---|
| **`/pages/pdrn-research`** | **`pdrn`** | **36,914** | 19,734 / 6,462 / 4,650 | 6 |
| | `what is pdrn` | 7,887 | 5,602 / 2,285 / — | 7 |
| | `pdrn meaning` | 2,116 | 1,665 / 551 / 105 | 15 |
| | `salmon dna pdrn` · `salmon pdrn` | 1,368 | 1,211 / 157 / — | 0 |
| | `pdrn benefits` · `what does pdrn do` | 1,177 | 1,110 / 78 / — | 9–11 |
| **`/pages/acetyl-hexapeptide-8-research`** | **`argireline`** | **7,149** | 3,734 / 1,103 / 845 | 3 |
| **`/pages/copper-peptide-research`** | `copper peptide` | 2,204 | 1,362 / 394 / 105 | 9 |
| **`/pages/glutathione-research`** | `glutathione for skin` | 1,631 | 1,211 / 472 / 422 | 29 |
| **`/pages/matrixyl-3000-research`** | matrixyl informational long-tail | low | — | — |

⚠️ **Do not also target `what is pdrn in skincare` (1,425) or `what does pdrn do for skin` (629) with
separate articles.** They are the same intent as the hub and would cannibalise it. Cover them as
**sections within the PDRN hub**, with matching H2s.

### Product pages — transactional terms

| Product | Owns | Opp | Observed US/GB/DE | KD |
|---|---|---|---|---|
| `pdrn-renewal-serum` | **`pdrn serum`** | **8,319** | 3,936 / 2,049 / 845 | 1 |
| `copper-peptide-ghk-cu-renewal-serum` | `copper peptide serum` | 5,496 | 2,977 / 1,339 / 634 | 3 |
| `matrixyl-3000-firming-serum` | `matrixyl 3000` | 5,127 | 2,725 / 1,339 / 211 | 0 |
| `pdrn-collagen-night-cream` | `pdrn cream` | 4,453 | 2,321 / 1,024 / 634 | 2 |
| `acetyl-hexapeptide-8-anti-wrinkle-serum` | `argireline serum` | 991 | 605 / — / 211 | 13 |
| `glutathione-brightening-serum` | `glutathione serum` | 953 | 555 / 236 / — | 0 |
| `matrixyl-3000-pro-collagen-firming-cream` | `peptide cream` | 627 | 504 / 472 / — | 4 |

### Collection pages — category and plural terms

| Collection | Owns | Opp | Observed US/GB/DE | KD |
|---|---|---|---|---|
| **`/collections/pdrn`** | **`pdrn skincare`** | **3,628** | 1,817 / 1,182 / — | 0 |
| `/collections/serums` | **`peptide serum`** | 4,016 | 3,129 / 1,418 / 1,056 | 0 |
| `/collections/all` or a peptide collection | `peptide skincare` | 312 | 100 / 157 / 211 | 9 |

**`/collections/pdrn` has a proven template.** In GB, **Boots ranks #1 for `pdrn serum` with a
collection page** titled *"PDRN Skincare | Serums, Creams & More"*, and Cult Beauty ranks #8 with the
same shape. That is exactly the page we should build.

⚠️ **`peptide serum` is assigned to the collection, not a product.** The classifier called it PRODUCT;
the live SERP is Forbes #1, Amazon, Timeless, The Ordinary — a category SERP. A single product page
cannot win it.

### Articles — commercial guides

| Article | Target | Opp | KD | Verdict |
|---|---|---|---|---|
| Best PDRN serums, compared on concentration | `best pdrn serum` | 1,042 | 3 | ✅ **Build** |
| Best copper peptide serums | `best copper peptide serum` | 532 | 5 | ✅ Build |
| ~~Best peptide serums~~ | `best peptide serum` | 1,287 | 10 | ❌ **Do not build** |

⚠️ **`best peptide serum` is owned by publishers** — Forbes #2, Reddit #3, Ulta #5, Marie Claire #6,
YouTube #8. This matches the research finding that commercial "best X" queries send **40.86%** of
citations to third-party listicles. **The play is to get *into* Forbes and Marie Claire's lists, not to
publish a competing one.** That belongs to the off-site track, not the content plan.

---

## 5. What the SERPs prove

12 live SERP pulls. Three findings that change decisions:

**1. Brand-owned ingredient explainers rank reliably.** Not a publisher-only space:

| Term | Brand pages in the top 10 |
|---|---|
| `what is pdrn` (US) | **SkinCeuticals #2**, Cult Beauty #8, Skin Laundry #9, INKEY List #11 |
| `pdrn` (US) | Skin Laundry #6, SkinCeuticals #8 |
| `pdrn serum` (US) | **INKEY List #5**, Medicube #7 |
| `pdrn` (FR) | **Lancôme #2** |
| `argireline` (US) | The Ordinary #4 |
| `matrixyl 3000` (US) | **Timeless #2**, The Ordinary #4, No7 #7 |

➡️ The hub model is validated for this category, in three languages.

**2. AI Overviews are on nearly every PDRN term**, including commercial ones — `pdrn`, `what is pdrn`,
`pdrn serum`, `pdrn skincare`, `argireline`, `copper peptide serum`, `matrixyl 3000` all carry one.
⚠️ **This contradicts the "commercial intent is safe" assumption** in the strategy doc for this
category specifically. PDRN is a trend term and Google is treating it as explanatory.
`peptide serum` and GB `pdrn serum` carry **no** AIO.

**3. Reddit is everywhere** — #7 on `pdrn`, #2 on `pdrn skincare`, #7 on `argireline`, #5 on
`matrixyl 3000`, #3 on `best peptide serum`. Consistent with Reddit taking 20.4% of AI Overview
first-citation slots.

---

## 6. A product gap the keyword data found

Real, qualified PDRN demand exists for formats we do not sell:

| Term | Opportunity | Observed US/GB/DE |
|---|---|---|
| `pdrn toner` | 1,157 | 454 / 315 / 211 |
| `pdrn mask` | 811 | 706 / — / 211 |
| `pdrn essence` + `pdrn 100 essence` | 1,168 | 151 / 709 / 105 |

**~3,100 of qualified opportunity sits on PDRN formats with no matching product.** That is a range
decision for Malcolm, not a content one — but it is the clearest product-development signal in the data.

---

## 7. Locale sequencing

| Priority | Markets | Why |
|---|---|---|
| **1** | **US + GB (English)** | 77% of total opportunity. Ships worldwide, so addressable |
| **2** | DE | 10%, and the largest EU locale by a wide margin |
| **3** | FR | 6%. Note Lancôme already ranks #2 for `pdrn` — competitive |
| **4** | IT, NL | 3% each |
| **5** | ES | 1%. Lowest return on translation effort |

**Hard gate unchanged:** 14 days in English, measured, before translating. Shipping English ahead of
translation makes the other five locales *worse*, not neutral — an outdated translation is still served.

---

## 8. Known limits

- **Clickstream is a panel estimate**, not a census. It is *observed* rather than modelled, which is why
  it is trusted over Ads here — but it is not ground truth either.
- **Enrichment covers the top 350 buckets per market**, not all 17,279. The long tail below that is
  scored on the Ads ÷ 3 fallback.
- **Brand detection is a heuristic.** It correctly caught Theramid and Rejuall; it missed
  *"the 6 peptide skin booster serum"* (Cosrx) because every token is ordinary vocabulary. Skim before
  committing a term to a page.
- **Zero-opportunity rows** in the data are terms where clickstream observed no searches at all. Treat
  them as unproven, not as zero demand.
- **KD scores cluster 0–15 across every family.** Verified against real SERPs for PDRN, argireline,
  matrixyl, copper peptide and peptide serum — but a low KD beside a Forbes-and-Reddit SERP
  (`best peptide serum`) still means "hard".
- **No AI-visibility baseline yet.** DataForSEO's `ai_optimization` family can measure whether we are
  named in AI answers, at ≥7 runs per prompt.
