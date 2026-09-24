# Study inventory, product mapping and build ranking

**Date:** 2026-09-24
**Asked by:** Malcolm — "make an inventory and index of all the research studies that we use or link to, then research which ones are best related to the products we sell, then choose the ones that will help our visibility and traffic the most."
**Status:** inventory complete; ranking complete; **no pages built yet**.
**Governed by:** `docs/research-2026-study-hubs-credibility.md` §3.3 (the six qualifying criteria) and its 12–18 page cap.

---

## 1. The inventory

Parsed from the evidence tables of all five claims registers, which are the authoritative record
because every row there was read at source.

| Ingredient | Studies cited | With PubMed ID / DOI / PMC |
|---|---:|---:|
| PDRN | 27 | 27 |
| Glutathione | 22 | 20 |
| Copper peptide | 20 | 13 |
| Matrixyl 3000 | 20 | 11 |
| Argireline | 19 | 17 |
| **Total** | **108** | **88** |

The 20 without an identifier are conference abstracts and manufacturer brochures. That absence is
itself a disqualifying signal under criterion 3, not a gap in the parsing.

**First consequence, worth stating plainly.** A page per cited study is **108 × 6 locales = 648
URLs**. The earlier estimate of ~180 was itself used to justify the original "no"; the real number
is three and a half times larger. This settles the "every study" question on arithmetic alone.

---

## 2. Classification against the six criteria

| Ingredient | Page candidate | Library row only | Excluded on route |
|---|---:|---:|---:|
| Matrixyl 3000 | 9 | 10 | 1 |
| Copper peptide | 7 | 11 | 2 |
| Glutathione | 5 | 8 | 9 |
| PDRN | 5 | 12 | 10 |
| Argireline | 3 | 13 | 3 |
| **Total** | **29** | **54** | **25** |

**Excluded on route (25)** are grade X and off-route work: injected PDRN, oral and IV glutathione,
plant and algal "PDRN". These cannot support a leave-on topical claim and get neither a page nor a
row that implies they do.

**Library row only (54)** are cell, animal, ex-vivo and formulation studies, plus every source the
registers themselves mark "do not use", "unreliable", "not transferable" or "believed fabricated".
The classifier reads those verdicts out of the register rather than re-deciding them — which is what
cut the candidate list from 40 to 29.

**One correction to the earlier research.** Criterion 2 is "route relevant to what we sell". We sell
**two microneedling stamp sets** (copper peptide and PDRN). Microneedle-delivery studies are
therefore route-relevant for those two ingredients and remain off-route for the other three. The
2026-09-22 research did not account for the stamp sets.

---

## 3. What study pages actually win — the finding that changes the plan

Hairgenetix runs this layer already, so its Search Console data is the best available predictor.
90 days, 3,327 page+query pairs on study URLs:

| Query shape | Impressions | Share | Clicks | Avg position |
|---|---:|---:|---:|---:|
| study / research / trial / clinical | 13,061 | 15.7% | **13** | 5.1 |
| what is / definition | 2,907 | 3.5% | 4 | 7.8 |
| does it work / effectiveness | 1,648 | 2.0% | 15 | 5.5 |
| before and after | 649 | 0.8% | 6 | 8.3 |
| vs / comparison | 474 | 0.6% | 3 | 9.1 |
| is it safe / side effects | 156 | 0.2% | 0 | 6.4 |

**The remaining ~75% of impressions come from bare ingredient names.** The twelve largest queries
reaching a study page are `ahk cu`, `ahk cu peptide`, `ahk-cu`, `ahkcu`, `ahk-cu peptide`,
`ahk peptide`, `ghk peptide` and close variants.

Two conclusions follow, and they pull in opposite directions:

1. **These pages are not read as study summaries. They rank as the ingredient's authority page.**
   That is where their 14.6% share of site impressions comes from.
2. **Which makes them a cannibalisation risk to the very hubs we just built.** The research doc
   already set a tripwire — de-optimise if a study page takes >30% of a hub head term's impressions.
   The Hairgenetix data shows that is not a hypothetical: on that site the study page effectively
   *is* the ingredient page.

And the explicitly evidence-shaped queries — the ones a study page is supposedly for — returned
**13 clicks in 90 days** across 13,061 impressions. As a traffic play this layer does not work. As a
visibility and citation play it does.

---

## 4. Skingenetix's own demand, measured

90 days, whole property: **541 impressions, 3 clicks, 173 queries.** The site is effectively
pre-traffic, so these are weights, not forecasts.

| Ingredient | Impressions | Share | Avg position |
|---|---:|---:|---:|
| Copper peptide | 191 | 35.3% | 38.6 |
| Matrixyl 3000 | 126 | 23.3% | 25.3 |
| Argireline | 84 | 15.5% | 14.5 |
| PDRN | 36 | 6.7% | 34.7 |
| Glutathione | 25 | 4.6% | 16.2 |

⚠️ **Do not read this as the opportunity split.** `keyword-strategy-2026.md` puts PDRN at 68% of
qualified *search opportunity*; the table above is what we currently *capture*, at positions 14–39.
Both are true and they measure different things. Opportunity should drive the content plan;
current capture tells us where we already have a foothold.

**The one genuinely encouraging signal.** Ten evidence-shaped queries already reach us, and they are
strikingly specific:

| Query | Impressions | Position |
|---|---:|---:|
| `pubmed acetyl hexapeptide-8 topical wrinkles randomized trial` | 7 | **7.7** |
| `pubmed acetyl hexapeptide-8 topical randomized clinical trial` | 4 | 8.2 |
| `pubmed acetyl hexapeptide-8 topical randomized trial wrinkles` | 3 | 7.3 |

Tiny volume, but this is exactly the audience a study page serves, and we are already at position 6–10
for it **without having built one**. It is also the query shape an AI system issues when fact-checking
a claim.

---

## 5. The ranked build list

Ranking = study strength × product linkage × demand foothold × cannibalisation risk.

### Tier 1 — build first (4 pages)

| Study | Ingredient | Grade | Why it ranks first |
|---|---|---|---|
| **Badenhorst 2016** | Copper peptide | A− | The only controlled split-face trial we have for copper; 40 women, 8 weeks, 3D imaging. Copper is our largest current foothold (35% of impressions) and has four products behind it. |
| **Raikou 2017** | Argireline | A | Second controlled trial for the ingredient where we already rank 6–10 on PubMed-style queries. Wang 2013 is already built, so this completes the pair. |
| **Henseler 2023** | Argireline | A (null) | The only independent imaging test, and it found nothing. Publishing the null is the single strongest differentiator against every competitor selling this peptide. |
| **Robinson 2005** | Matrixyl 3000 | A | The controlled human trial behind palmitoyl pentapeptide; Matrixyl is our second foothold (23%) with two products and currently rests mostly on manufacturer data. |

### Tier 2 — build if tier 1 holds at the 8-week gate (4 pages)

Mokhtar 2026 (copper, independent systematic review) · Ye 2026 (PDRN — already built as the pilot) ·
Watson 2009 (Matrixyl, the mechanism paper) · Grandi 2019 (glutathione, null, but a different
formulation — needs the parked formula facts first).

### Deliberately not in tier 1

- **Abdulghani 1998** (copper) — the 7-of-10 biopsy result is our most quoted copper figure, but it
  is a 20-person pilot with no between-group test. It belongs in the library with that caveat visible,
  not on a page that lends it authority.
- **Every Matrixyl manufacturer brochure panel** — no identifier, sponsor-run. Library rows.
- **All four Matrixyl reviews** — a page each would be four near-identical secondary summaries, which
  is precisely the "could a competitor publish this tomorrow" failure.

---

## 6. Recommendation

Build **four tier-1 pages plus the Evidence Library**, not 12–18 and certainly not 108.

The cap should come down from the research doc's 12–18 because of §3: the layer earns visibility, not
clicks, and at Hairgenetix it does so by competing for ingredient names. On a site whose five hubs are
two days old and sitting at positions 14–39, adding pages that compete for the same terms is the one
way this could actively hurt.

**Gate before tier 2:** at 8 weeks, check that no tier-1 study page holds more than 30% of its hub's
head-term impressions, and that the hub still outranks it. Those are the research doc's own numbers.

**Still outstanding and not blocking:** the Search Console Generative AI report is UI-only — it is not
exposed by the API, and every AI search type was rejected on probing. Reading it takes 30 seconds in
the interface and would tell us whether AI engines cite us at all, which is the one input that would
justify going beyond four.

---

Related: `docs/research-2026-study-hubs-credibility.md`, `docs/decision-citations-study-pages-navigation-2026-09-22.md`, `docs/keyword-strategy-2026.md`, `docs/claims/*.md`, `configs/studies/`.
