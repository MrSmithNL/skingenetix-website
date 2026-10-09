# Matrixyl 3000 Firming Serum: English product-page draft (2026-10-09)

Status: DRAFT for Malcolm's review. Nothing here has been sent to Shopify. Sources: `docs/claims/matrixyl-3000.md` (register),
`docs/website-traffic-and-performance-plan-2026-10-08.md` (Part 3.1, 3.2, step 1.2, Part 7),
`configs/page-targets.json`, `audits/2026-10-08-competitor-gap-per-page/serp/raw/` (People Also Ask lists), and the live content
in `_current-matrixyl-3000-firming-serum.json`.

## Target

| Item | Value |
| --- | --- |
| URL | `/products/matrixyl-3000-firming-serum` |
| Owner term | matrixyl 3000 (2,725 US / 1,339 GB monthly searches; today position 17.5 on 177 impressions) |
| Secondary terms | serum; "firming serum" (100 US) proposed in decision 3c |
| Page type | product |
| Job in the funnel | Buy page for "matrixyl 3000" and "matrixyl 3000 serum". The hub `/pages/matrixyl-3000-research` owns "what is matrixyl 3000" |
| Primary action | Add to basket; quiet second step: read the Matrixyl 3000 research |
| Concentration stated | None. What "10% MATRIXYL" on the pack means is unconfirmed (decision 8) |
| Trial magnitudes on the page | None (rule of 2026-09-26; decision 15 is open) |

Decision notes:

- **Decision 3c (open): "firming serum" moves to this page.** Alternative SEO title and first line are given below. They depend on 3c.
  The plan expects only a shopping block and an AI Overview slot for this term, not a page-one rank.
- **Decision 8 (open): what "10% MATRIXYL" means.** The register's trial facts for Matrixyl 3000 itself (claims 1, 3 and 7) can sit
  on the product only once the formula sheet confirms at least 3% Matrixyl 3000. Until then this draft uses the pentapeptide-4 trial
  (claim 2, serum only) and the lab finding with no figure.
- **Cannibalisation check.** The Matrixyl cream already ranks 5.6 for "matrixyl 3000" and carries "matrixyl 3000 cream" as a
  secondary. The audit of 2026-10-07 keeps the head term with the serum until a clean re-pull. See Open questions.

## SEO title and meta

| Field | Proposed text | Characters | Limit |
| --- | --- | --- | --- |
| SEO title | Matrixyl 3000 Serum with Vitamin C and Pentapeptide-4 | 53 | 60 |
| Meta description | Matrixyl 3000 serum with palmitoyl pentapeptide-4, a vitamin C derivative and hyaluronic acid for firmer-looking, smoother skin. Morning and evening. | 149 | 155 |
| Alternative SEO title (only if 3c is "yes") | Firming Serum with Matrixyl 3000 and Vitamin C &#124; Skingenetix | 60 | 60 |

The owner term "matrixyl 3000" appears once, at the front of the title. The live title "Matrixyl 3000 Serum for Firmer-Looking
Skin | Skingenetix" also fits; the proposal swaps the generic tail for the two named extras that a searcher can verify.

## Description

```html
<p><strong>Matrixyl 3000 serum with the two Matrixyl 3000 peptides (palmitoyl tripeptide-1 and palmitoyl tetrapeptide-7),
palmitoyl pentapeptide-4, a vitamin C derivative, niacinamide and hyaluronic acid, made for firmer-looking, smoother skin on
the face and neck.</strong></p>
<h3>What the research on these peptides shows</h3>
<ul>
<li>Palmitoyl pentapeptide-4, the original Matrixyl and also in this serum, was tested in a 12-week, double-blind,
placebo-controlled, split-face trial of 93 women aged 35 to 55. Image analysis and expert graders both rated the look of
wrinkles and fine lines ahead of placebo from week 8, by the paper's own significance bar (p of 0.10 or less, looser than
the usual 0.05). Procter &amp; Gamble scientists ran the trial
(<a href="/blogs/clinical-studies/matrixyl-wrinkle-trial-robinson-2005">read the trial appraisal</a>).</li>
<li>In lab tests on skin cells, the two Matrixyl 3000 peptides together raised collagen I by more than either peptide on its
own. The ingredient's maker ran those tests, and they do not show what happens in skin.</li>
</ul>
<p>These results describe the ingredients as studied, not this serum. The full figures are on the
<a href="/pages/matrixyl-3000-research">Matrixyl 3000 research page</a>.</p>
<h3>What to combine and how to layer</h3>
<p>Use it after cleansing, on slightly damp skin, after any lighter, watery serum and before your moisturiser. For a
two-step firming routine, seal it with the
<a href="/products/matrixyl-3000-pro-collagen-firming-cream">Matrixyl 3000 Pro-Collagen Firming Cream</a>, which carries the same
two Matrixyl 3000 peptides. If you also use the
<a href="/products/acetyl-hexapeptide-8-anti-wrinkle-serum">Argireline serum</a> for expression lines, apply that first.
Finish with SPF in the morning.</p>
<h3>Who it is for</h3>
<p>Adults who want a lightweight, twice-daily step for skin that looks less firm and for fine lines.</p>
<p>Matrixyl&reg; and Matrixyl&reg; 3000 are registered trademarks of Sederma (Croda).</p>
```

The first line carries the owner term and the defining facts. No concentration is stated.

Alternative first line, only if 3c is "yes": "Firming serum with Matrixyl 3000: the two Matrixyl 3000 peptides (palmitoyl tripeptide-1 and
palmitoyl tetrapeptide-7), palmitoyl pentapeptide-4, a vitamin C derivative, niacinamide and hyaluronic acid, for firmer-looking,
smoother skin on the face and neck."

## Key benefits

Field `custom.key_benefits`, one bullet per line:

- Firmer-looking, smoother skin - the two Matrixyl 3000 peptides, whose maker's studies ran for 2 months
- Softer-looking fine lines and wrinkles - with palmitoyl pentapeptide-4, tested for 12 weeks against placebo in 93 women
- Hydrated feel - hyaluronic acid for a plump, dewy feel
- Vitamin C derivative and niacinamide - 3-O-ethyl ascorbic acid and niacinamide in the same serum
- What to expect: it feels light and hydrated on application. Most studies of these peptides measured results at 8 weeks and
  they kept building to 12, so give it at least 8 weeks.

## How to use

Field `custom.how_to_use`:

Use morning and evening. After cleansing, press 3-4 drops onto slightly damp skin across the face and neck. Apply after any
lighter, watery serum and before your moisturiser. Let it absorb for about a minute; finish with SPF in the morning. Give it at
least 8 weeks before judging it.

Layering: for a two-step firming routine, follow with the
[Matrixyl 3000 Pro-Collagen Firming Cream](/products/matrixyl-3000-pro-collagen-firming-cream). If you also use the
[Argireline serum](/products/acetyl-hexapeptide-8-anti-wrinkle-serum), apply that one first. No study has found anything Matrixyl 3000
should not be used with, and none has tested combinations either. Add one new active at a time (retinol, exfoliating acids) and patch
test first.

Three steps (field `custom.how_to_steps`, text only; the images stay):

1. Cleanse: wash with a gentle, pH-balanced cleanser and pat skin dry.
2. Apply the serum: press 3-4 drops onto the face and neck. It works best on slightly damp skin.
3. Moisturise and SPF: follow with your moisturiser. Finish with SPF 30+ every morning.

## Clinical research

Field `custom.clinical_research`:

Palmitoyl pentapeptide-4, also in this serum, put the look of wrinkles and fine lines ahead of placebo from week 8 in a 12-week trial.

- 93 women aged 35 to 55, double-blind, placebo-controlled, split-face, 12 weeks: image analysis and expert graders both rated
  wrinkles and fine lines ahead of placebo from week 8
- The effect was described as small, and the paper counted a p-value of 0.10 or less as significant (the usual bar is 0.05)
- In lab tests on skin cells, the two Matrixyl 3000 peptides together raised collagen I by more than either alone; this is lab
  work and does not show what happens in skin
- The manufacturer's Matrixyl 3000 studies ran for 2 months; their figures are on the research page
- The independent Cosmetic Ingredient Review Expert Panel assessed both Matrixyl 3000 peptides (2018) and palmitoyl pentapeptide-4
  (2024) as safe in cosmetics at current use levels; this is a finding about the ingredients, not a test of this serum
- No independent controlled trial of Matrixyl 3000 on its own has been published, and the pentapeptide-4 trial was run by Procter &
  Gamble scientists

Lab: Sederma patent US 6,974,799 (human skin cells, 3 days). Trial: Robinson et al. 2005, Int J Cosmet Sci 27:155-160 (PubMed
18492182). Safety: Johnson et al., "Safety Assessment of Tripeptide-1, Hexapeptide-12, Their Metal Salts and Fatty Acyl Derivatives,
and Palmitoyl Tetrapeptide-7 as Used in Cosmetics", Int J Toxicol 2018 (DOI 10.1177/1091581818807863); Cosmetic Ingredient Review final
report on pentapeptides, released 18 November 2024. Results describe the ingredients as studied, not this product; the full figures
are on the research page. [See all the Matrixyl 3000 research](/pages/matrixyl-3000-research)

## FAQ

Field `custom.faq_items`. Items 1 to 6 follow the People Also Ask questions for "matrixyl 3000" and "firming serum"; item 7 is the
safety item.

1. **What does Matrixyl 3000 do for your face?**
   Matrixyl 3000 is a pair of signal peptides, palmitoyl tripeptide-1 and palmitoyl tetrapeptide-7, developed by Sederma. They are
   matrikines: short peptides modelled on pieces of the skin's own matrix proteins and associated with the skin's own collagen
   activity. In cosmetics they are used for the look of firmer, smoother skin. This serum adds palmitoyl pentapeptide-4, a vitamin C
   derivative, niacinamide and hyaluronic acid.

2. **Does a Matrixyl 3000 serum work, and how soon will I see it?**
   The manufacturer's Matrixyl 3000 studies ran for 2 months, and in the 93-woman pentapeptide-4 trial wrinkles and fine lines
   were ahead of placebo from week 8. A firmer, smoother look builds over 4 to 8 weeks, with best results around 12 weeks. No
   independent controlled trial of Matrixyl 3000 on its own has been published, and no study has tested this finished serum.

3. **Can I use Matrixyl 3000 every day?**
   This serum is made for use morning and evening: 3-4 drops on slightly damp skin, face and neck, then moisturiser and, in the
   morning, SPF 30+. Check the safety answer below before the first use.

4. **What can I not mix with Matrixyl 3000, and how do I layer it?**
   No study has found anything Matrixyl 3000 should not be used with, and none has tested combinations. Apply this serum after
   lighter, watery serums and before your moisturiser. For expression lines, apply the Argireline serum first. Add one new active
   at a time, such as retinol or an exfoliating acid, and patch test first.

5. **Is Matrixyl 3000 better than retinol?**
   No study compares them, so nobody can say which is better. Peptides like these are not acids or vitamin A derivatives, so they
   are a different kind of ingredient from retinol. This serum contains no retinol among its listed actives.

6. **Is Matrixyl 3000 the same as Matrixyl?**
   No. Matrixyl is the original peptide, palmitoyl pentapeptide-4. Matrixyl 3000 is a different pair, palmitoyl tripeptide-1 and
   palmitoyl tetrapeptide-7. This serum contains both. The [Matrixyl 3000 research page](/pages/matrixyl-3000-research) sets out
   what each one has been tested for.

7. **Are there side effects, and should I patch test?**
   The independent Cosmetic Ingredient Review Expert Panel assessed both Matrixyl 3000 peptides, and palmitoyl pentapeptide-4, as
   safe in cosmetics at current use levels, and the 93-woman trial reported pentapeptide-4 as well tolerated by the skin. Those are
   findings about the ingredients, not a tolerance test of this serum. Patch test first: put a small amount on the inner forearm for
   24 hours before the first full use. Stop using it if stinging or redness does not settle. The peptides have not been tested in
   pregnancy, so ask your doctor if you are pregnant or breastfeeding.

## Alt text

Main product image: "Skingenetix Matrixyl 3000 Firming Serum pack with palmitoyl pentapeptide-4 and vitamin C" (88 characters).

Check the wording against the image before use.

## Internal links used

| Link | Where | Direction |
| --- | --- | --- |
| `/pages/matrixyl-3000-research` | description, clinical research, FAQ 6 | up to the ingredient hub |
| `/blogs/clinical-studies/matrixyl-wrinkle-trial-robinson-2005` | description | sideways to the study |
| `/products/matrixyl-3000-pro-collagen-firming-cream` | description, how to use | sideways to the sibling cream (the duo) |
| `/products/acetyl-hexapeptide-8-anti-wrinkle-serum` | description, how to use, FAQ 4 | sideways to the Argireline serum |

## What changed and why

| Field | Live text | Proposed text | Reason |
| --- | --- | --- | --- |
| SEO title | Matrixyl 3000 Serum for Firmer-Looking Skin &#124; Skingenetix | Matrixyl 3000 Serum with Vitamin C and Pentapeptide-4 | Owner term first; two named extras instead of a generic tail |
| Meta description | "...with pentapeptide-4, hyaluronic acid and vitamin C for firmer, smoother-looking skin and softer lines." | Similar, with "palmitoyl pentapeptide-4" and "firmer-looking" | "Firmer, smoother-looking" read as a promise; "softer lines" dropped from the meta |
| First line | "A collagen-support serum pairing Matrixyl 3000 peptides with hyaluronic acid ..." | Owner term and the named actives | "Collagen-support serum" states a physiological action (register avoid list) |
| Bullet | "No parabens · no mineral oil · no synthetic fragrance" | Removed | Free-from claims removed; "free from parabens" is not accepted (register section 2, number 18) |
| Best for | "fine lines and skin losing firmness, for anyone wanting a lightweight, twice-daily firming step" | "skin that looks less firm and for fine lines" | "Losing firmness" reads as a change in skin function |
| Key benefit | "Deep hydration - hyaluronic acid for a plump, dewy feel" | "Hydrated feel" | No data for "deep" hydration (register section 2, number 7) |
| Key benefit | "Antioxidant support - stable Vitamin C helps brighten the look of the skin" | "Vitamin C derivative and niacinamide ... in the same serum" | No claims register covers vitamin C; it is named as an ingredient, with no function claim |
| What to expect | "skin feels smoother and softer from the first use" | "feels light and hydrated on application" | Sensory only; "smoother and softer from the first use" has no data (register section 2, number 7) |
| Clinical research | "Matrixyl 3000's two peptides raised collagen I by 256% in lab tests on skin cells." | "...raised collagen I by more than either alone" | Magnitude removed; the lab qualifier stays |
| Clinical research | "Collagen I +256% in lab tests, nearly 4x the stronger peptide alone" | Direction only | Magnitude removed |
| Clinical research | "...reduced the look of wrinkles and fine lines more than placebo in a 12-week double-blind trial of 93 women" | Same facts, plus the paper's p of 0.10 bar and "small" | Any "significant" wording must carry the threshold (register claim 6) |
| Clinical research | "Significant from week 8 in that trial, and still at week 12" | "ahead of placebo from week 8" with the threshold | As above |
| Clinical research | "Both Matrixyl 3000 peptides assessed safe in cosmetics by an independent expert panel" | Kept, with pentapeptide-4 (2024) added and the "not a test of this serum" clause | Register claim 5; conditions kept |
| FAQ | "Is it suitable for sensitive skin? Formulated without parabens, mineral oil or added synthetic fragrance." | FAQ 7, the safety item | "Suitable for sensitive skin" and the free-from list have no product-level support |
| FAQ | "Hydration and smoothness look improved quickly" | "from week 8 ... 4 to 8 weeks, best around 12 weeks" | Register section 2, number 8 ("quickly" had no data) |
| FAQ | "What is Matrixyl 3000? ... valued in cosmetics for supporting a firmer, smoother appearance" | FAQ 1 with "associated with the skin's own collagen activity" | Register section 2, number 17 wording |
| Layering | "Apply after any lighter, watery serums" | Kept, and the Argireline serum named as the one to apply first | Matches the Argireline draft; not a tested finding |

Figures removed from the product (for decision 15): "256%" (collagen I in lab tests), "nearly 4x the stronger peptide alone", and the
"+147%" fibronectin and "+92%" hyaluronic acid figures that sit on the cream, not this page. The serum's live text carried only the
first two. The Sederma 2-month figures (-39% deep-wrinkle area and the others) were never on the product and stay off.

## Open questions for Malcolm

1. **Decision 8: "10% MATRIXYL" on the pack.** Until the formula sheet says whether it is 10% Matrixyl 3000 solution, Matrixyl, or
   both, the manufacturer's 2-month figures (claims 1 and 3) stay on the hub only. If it is at least 3% Matrixyl 3000, they can
   come onto this page, and claim 7 ("over three times the tested level") becomes available.
2. **Pentapeptide-4 level.** Claim 2's condition (d): the trial used 3 ppm, so the serum should hold at least that. Please confirm
   with the formula sheet. The wording does not say it matches.
3. **Decision 3c: "firming serum".** Alternative title and first line are given. The plan expects a shopping-block slot only.
4. **Cannibalisation with the cream.** The cream page is down for "matrixyl 3000 cream" and already ranks 5.6 for "matrixyl 3000".
   Keep the head term with the serum (this draft), or let the cream carry it. I kept the serum as the plan says.
5. **Tension between the brief and register claim 5.** The brief says never to write "safe". Register claim 5 (and the live copy)
   uses the Cosmetic Ingredient Review panel's own conclusion about the ingredients. I kept it in the research text and FAQ 7 only,
   attributed, with "not a test of this serum". Strike it if you prefer; the research text works without it.
6. **Vitamin C.** No register covers 3-O-ethyl ascorbic acid, so the draft names it with no function claim. A short register for
   vitamin C would let the bullet say more.
7. **Trademark line.** The register (gap 8) asks for the supplier's confirmation that the registered-trademark marks are permitted.
   Remove the sentence if it is not confirmed.
8. **Order of layering.** The Argireline serum first follows the live pages' own rule; it is not a tested finding.
9. **Alt text.** I have not seen the image. Confirm "pack" matches it.
