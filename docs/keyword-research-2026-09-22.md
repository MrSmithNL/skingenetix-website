# Keyword Research — Skingenetix, 2026-09-22

**Status:** ⚠️ **Superseded on volumes by `docs/keyword-strategy-2026.md` (same day).** This was the
first pass and used **Google Ads volume**. The full study added *observed clickstream* and found Ads
inflated by up to **178×** on this catalogue (`ghk copper peptide`: 135,000 Ads → 757 observed). The
method notes, SERP findings and GSC baseline here remain valid; **the volume figures do not.**
**Source:** DataForSEO Labs `keyword_suggestions` (terms *containing* the seed) + live SERP pulls, plus
Google Search Console. **7,280 keywords** captured across three markets.

**Raw data (committed):**
`configs/keyword-data/keywords-{us,nl,de}-2026-09-22.json` · `configs/keyword-data/gsc-baseline-2026-09-22.json`
**Tools (reusable):** `scripts/keyword-research.py` · `scripts/gsc-baseline.py`

---

## 0. Two method rules, and one I had to correct

**Never sum Google Ads volumes.** Ads buckets many phrasings onto one figure. Visible here:
`ghk copper peptide` and `copper peptide ghk` both return **135,000** — that is one bucket with the words
reversed, not 270,000 of demand. Same for `pdrn serum`/`pdrn serums` (22,200), `argireline
serum`/`argireline serums`/`serum with argireline` (3,600), and four Matrixyl variants at 880. **Every
figure below is a distinct bucket. Nothing is added up.**

**⚠️ Corrected mid-research — the Hairgenetix qualifier rule does not port.** That project's rule was
"every keyword must carry a hair qualifier", because there `ghk cu` leaked to *skin* audiences. Applied
literally on a skin brand it discards `copper peptide` — the head term itself. The real contamination
here is **non-topical intent**: injections, oral supplements, bodybuilding, lab reagents, hair-loss, and
dermatology conditions. `scripts/keyword-research.py` now filters on that instead, and prints what it
dropped.

**Also corrected:** the first pass used `keyword_ideas`, which expands *semantically* and returned
"skin tag removal" and "laser hair removal". `keyword_suggestions` returns terms *containing* the seed,
which is what a hero map needs.

---

## 1. Demand by family and market

Distinct buckets only. Difficulty is DataForSEO's 0–100 KD.

| Family | Term | 🇺🇸 US | 🇩🇪 DE | 🇳🇱 NL | KD (US) |
|---|---|---|---|---|---|
| **Copper peptide** | ghk copper peptide | **135,000** | 8,100 | 3,600 | 14 |
| | copper peptide | 33,100 | 1,300 | 720 | 9 |
| | copper peptide serum | 8,100 | 720 | 320 | 3 |
| | copper peptide for skin | 4,400 | — | — | 6 |
| **PDRN** | pdrn | **49,500** | 5,400 | 1,900 | 6 |
| | pdrn serum | 22,200 | 2,900 | 1,000 | 1 |
| | **what is pdrn** | **14,800** | — | — | **7** |
| | **pdrn skincare** | **12,100** | — | — | **0** |
| | pdrn cream / creme | 5,400 | 1,600 | 590 | 2 |
| | pdrn meaning | 5,400 | — | — | 15 |
| | what is pdrn in skincare | 4,400 | — | — | 10 |
| **Argireline / AH-8** | argireline | 9,900 | 1,600 | 390 | 3 |
| | argireline serum | 3,600 | 590 | 110 | 13 |
| | acetyl hexapeptide-8 | 2,900 | — | — | 7 |
| **Matrixyl 3000** | matrixyl 3000 | 6,600 | 1,000 | 210 | 0 |
| | matrixyl 3000 serum | 1,000 | — | — | 2 |
| **Glutathione** | glutathione serum | 1,600 | 260 | 140 | 0 |
| **Generic peptide** | peptide serum | 9,900 | 3,600 | 1,300 | 0 |
| | best peptide serum | 3,600 | — | — | 10 |

⚠️ `l argireline` shows 74,000 in the US. Almost certainly a bucket artefact or a misparse — **do not
build on it** until a live SERP confirms real intent.

### What this says

1. **PDRN is the strongest opportunity on the site**, and it is not close. Large volume in all three
   markets, *and* the informational head terms are wide open at near-zero difficulty — `pdrn skincare`
   KD 0, `what is pdrn` KD 7. That is a content hub's natural territory.
2. **Copper peptide carries the most raw volume** (135,000) at KD 14 — but this is where The Ordinary
   and NIOD sit.
3. **Germany is 2–4× the Netherlands** on nearly every term. For a store selling EUR into the EU, DE is
   the bigger commercial market, not the home market.
4. **Glutathione is small everywhere** — 1,600 / 260 / 140. Hub effort must not be split evenly.
5. **Generic `peptide serum` is real in the EU** (DE 3,600, NL 1,300) — a viable collection-page target.

---

## 2. Who actually ranks — live SERPs

### `what is pdrn` (US, informational)

**AI Overview present.** Also People Also Ask, video, perspectives.

| # | Domain | Type |
|---|---|---|
| 2 | **skinceuticals.com** | **brand ingredient explainer** |
| 4 | pmc.ncbi.nlm.nih.gov | primary research |
| 6 | cosmopolitan.com | magazine |
| 8 | **cultbeauty.com** | retailer guide |
| 9 | **skinlaundry.com** | brand |
| 10 | dermatologytimes.com | trade |
| 11 | **theinkeylist.com** | **brand ingredient explainer** |

➡️ **Brand-owned educational pages rank here.** SkinCeuticals at #2 and INKEY List at #11 are doing
exactly what our five research pages already do. This is the single most encouraging finding for the hub
model — it is not a publisher-only SERP.

### `pdrn serum` (DE, commercial)

**No AI Overview** — consistent with commercial intent sitting at 4–8% AIO prevalence.

| # | Domain | Type |
|---|---|---|
| 1 | korean-skincare.de | small retailer |
| 3 | amazon.de | marketplace |
| 4 | koreanbeauty.de | small retailer |
| 5 | littlewonderland.de | small blog guide |
| 6 | dybeauty.de | small blog, *"Was ist PDRN in der Kosmetik?"* |
| 7 | idealo.de | price comparison |
| 8 | instagram.com | social |
| 9 | douglas.de | large retailer guide |

➡️ **Thin competition.** Small affiliate blogs and marketplaces, no dominant brand. **Genuinely winnable.**

---

## 3. Competitive ownership

Competitors own the *branded* product terms, not the category:

| Family | Who owns the branded head term | Volume |
|---|---|---|
| Generic peptide | **The Ordinary** multi-peptide serum | 40,500 (US) |
| PDRN | **Medicube** PDRN Pink Peptide Serum | 33,100 (US) |
| Copper peptide | The Ordinary / NIOD | 4,400 / 1,600 |
| Argireline | The Ordinary Argireline Solution 10% | 6,600 |
| Matrixyl 3000 | Timeless Skin Care | 1,300 |

➡️ **The category-education terms are unowned in every family.** That is the gap the hub occupies.

---

## 4. What Search Console already shows

90-day window, but only **17 days carry data** — 21 clicks, 2,065 impressions. The property is new.

| Finding | Detail |
|---|---|
| **One page carries half the site's impressions** | `/pages/acetyl-hexapeptide-8-research` — **1,014 of 2,065 impressions**, position 8.4, **1 click** |
| **The demand we're already visible for is ingredient-term demand** | Dozens of `acetyl hexapeptide-8` variants, matching the ingredient-hub hypothesis |
| **Over half of impressions come from the US** | 1,110 of 2,065, position 10.1 — while the store sells EUR into the EU |
| **Research-intent queries are pulling us in** | "acetyl hexapeptide-8 topical randomized controlled trial wrinkles pubmed", "systematic review … topical glutathione" |
| Bot/scraper noise present | `"fedex" -site:reddit.com…`, `/ugcadd`, `how about this?` |

➡️ **The impression-rich, click-poor pattern from Hairgenetix is already happening here**, on the very
first page to gain traction. 1,014 impressions → 1 click is a 0.10% CTR. The research pages attract
researchers, not buyers. That is the single most important thing to design around.

---

## 5. Open questions

- **`l argireline` at 74,000** — unverified, likely an artefact. Needs a SERP check before use.
- **No clickstream pulled yet.** DataForSEO's clickstream endpoints give *observed* rather than modelled
  volume, and settled the product-naming question on Hairgenetix. Worth running before any renaming.
- **FR / ES / IT not yet pulled.** Only US, DE, NL. The store has six live locales.
- **KD scores are uniformly low (0–28)** across every family. Encouraging, but low KD plus a thin SERP
  is a better signal than low KD alone — verified for PDRN, not for the others.
- **No AI-visibility baseline yet.** DataForSEO's `ai_optimization` family (`llm_responses`,
  `llm_mentions`) can measure whether we are named in AI answers — at ≥7 runs per prompt, per the
  St. Gallen finding.
