# Acetyl Hexapeptide-8 Anti-Wrinkle Serum (Argireline serum): English product-page draft (2026-10-09)

Status: DRAFT for Malcolm's review. Nothing here has been sent to Shopify. Sources: `docs/claims/argireline-acetyl-hexapeptide-8.md`
(register), `docs/website-traffic-and-performance-plan-2026-10-08.md` (Part 3.1, 3.2, step 1.2, Part 7),
`configs/page-targets.json`, `audits/2026-10-08-competitor-gap-per-page/serp/raw/` (People Also Ask lists), and the live content in
`_current-acetyl-hexapeptide-8-anti-wrinkle-serum.json`.

## Target

| Item | Value |
| --- | --- |
| URL | `/products/acetyl-hexapeptide-8-anti-wrinkle-serum` |
| Owner term | argireline serum (605 US monthly searches; today position 9.3 on 154 impressions) |
| Secondary terms | acetyl hexapeptide-8 serum, 10% (from `page-targets.json`); "wrinkle serum" proposed in decision 3c |
| Page type | product |
| Job in the funnel | Buy page for "argireline serum". The hub `/pages/acetyl-hexapeptide-8-research` owns "argireline" and "does argireline work" |
| Primary action | Add to basket; quiet second step: read the Argireline research |
| Concentration stated | "10% Argireline peptide solution", as printed on the label. No peptide percentage and no grade (decision 8) |
| Trial magnitudes on the page | None (rule of 2026-09-26; decision 15 is open) |

Decision notes:

- **Decision 3a (open): may the visible product title carry "Argireline"?** The live title is "Acetyl Hexapeptide-8 Anti-Wrinkle
  Serum" and the word "Argireline" appears once on the page. This draft puts "Argireline" in the SEO title, the first line and the
  FAQ. If 3a is "no", use the fallback SEO title below and the fallback first line; the trademark sentence at the foot of the
  description still names Argireline once.
- **Decision 3c (open): "wrinkle serum" (251 US) moves to this page.** An alternative SEO title is given below. It depends on 3c.
  The description already says "wrinkle" in plain use only where the register allows ("lines"), so no body change is needed.
- **Decision 8 (open): the Argireline grade and peptide content.** The register says "10% Argireline" means 10% of the peptide
  solution (about 0.005% peptide). So this draft never writes "10% acetyl hexapeptide-8" and never says the serum matches the
  clinical dose. That line comes back once the supplier document confirms the grade (see Open questions).
- **Decision 12 (open): the "Botox in a bottle" item.** The People Also Ask box for "wrinkle serum" includes "What serum works like
  Botox?". The register lists every Botox comparison under claims to avoid, so no Botox item is drafted here.

## SEO title and meta

| Field | Proposed text | Characters | Limit |
| --- | --- | --- | --- |
| SEO title | Argireline Serum 10% for Expression Lines &#124; Skingenetix | 55 | 60 |
| Meta description | Argireline serum with 10% Argireline peptide solution, hyaluronic acid and niacinamide for softer-looking crow's feet and forehead lines. | 137 | 155 |
| Fallback SEO title (if 3a is "no") | Acetyl Hexapeptide-8 Serum for Expression Lines | 47 | 60 |
| Alternative SEO title (only if 3c is "yes") | Wrinkle Serum with Argireline 10% &#124; Skingenetix | 47 | 60 |

The owner term "argireline serum" appears once, at the front of the title. The live title "Acetyl Hexapeptide-8 10% Anti-Wrinkle
Serum" is replaced because "10% acetyl hexapeptide-8" reads as 10% pure peptide, which the register lists under claims to avoid.

## Description

```html
<p><strong>Argireline serum with 10% Argireline peptide solution, hyaluronic acid, niacinamide and ectoin, made to soften
the look of crow's feet and forehead lines.</strong></p>
<p>Argireline is the trade name of the peptide acetyl hexapeptide-8. It is modelled on part of SNAP-25, a protein
involved in expression, and is designed to soften the look of expression lines.</p>
<h3>What the research on Argireline shows</h3>
<ul>
<li>In a double-blind, placebo-controlled trial of 60 adults, an emulsion with 10% Argireline was applied around the eyes
twice a day for 4 weeks. Clinicians graded the crow's feet as clearly improved in more people on Argireline than on
placebo, and skin roughness measured on silicone replicas fell while the placebo group showed no significant change
(<a href="/blogs/clinical-studies/argireline-crows-feet-trial-wang-2013">read the trial appraisal</a>).</li>
<li>In a randomised, placebo-controlled trial of 24 women, forehead roughness was lower than at the start by day 20 on
10% Argireline, while it rose on placebo
(<a href="/blogs/clinical-studies/argireline-forehead-roughness-trial-raikou-2017">read the trial appraisal</a>).</li>
</ul>
<p>These results describe the ingredient as studied, not this serum. The full figures are on the
<a href="/pages/acetyl-hexapeptide-8-research">Argireline research page</a>.</p>
<h3>What to combine and how to layer</h3>
<p>Use it after cleansing, on slightly damp skin, before your moisturiser and SPF. If you also use the
<a href="/products/matrixyl-3000-firming-serum">Matrixyl 3000 Firming Serum</a>, put this serum on first, then the Matrixyl
serum, then your moisturiser. They are two different peptides, one for the look of expression lines and one for the look of
firmness. No study has tested the pair together, so we promise no combined result.</p>
<p>Use it on intact skin only. Do not use it with microneedling devices or any needle.</p>
<h3>Who it is for</h3>
<p>Adults who want a lightweight, twice-daily serum for expression lines on the forehead and around the eyes.</p>
<p>Argireline&reg; is a registered trademark of Lubrizol. Acetyl hexapeptide-8 is the ingredient name on the label.</p>
```

The first line carries the owner term, the label concentration in the register's own wording ("10% Argireline peptide solution")
and the defining facts. Both cited facts are claims 1, 2 and 6 of the register with the percentages removed.

If 3a is "no", the first line becomes: "Acetyl hexapeptide-8 serum with 10% Argireline peptide solution, hyaluronic acid, niacinamide and ectoin,
made to soften the look of crow's feet and forehead lines." The trademark sentence stays.

## Key benefits

Field `custom.key_benefits`, one bullet per line:

- Softer-looking expression lines - Argireline, a peptide designed to soften the look of crow's feet and forehead lines
- Smoother-looking skin - studied on silicone replicas of the skin around the eyes, and on the forehead
- Light and layerable - absorbs quickly and sits under your moisturiser and SPF
- Comfortable, hydrated feel - hyaluronic acid and ectoin
- Supporting peptides and niacinamide - palmitoyl tripeptide-1 and palmitoyl tetrapeptide-7, as listed in the ingredients
- What to expect: in the studies of Argireline, forehead roughness was lower by day 20 and crow's feet were graded clearly
  smoother in more people than on placebo after 4 weeks of twice-daily use. The effect is not permanent.

## How to use

Field `custom.how_to_use`:

Use morning and evening. After cleansing, press 3-4 drops onto slightly damp skin and pat it in across the forehead and
around the eyes, keeping it out of the eyes. Wait about a minute, then follow with your moisturiser and, in the morning, SPF 30+.

Give it at least 4 weeks of twice-daily use before judging it. The studies measured results at day 20 and at 4 weeks.

Layering: apply it before the [Matrixyl 3000 Firming Serum](/products/matrixyl-3000-firming-serum) if you use both, and before
your moisturiser. No study has tested Argireline with other actives, so there is no tested do-not-mix list; add one new product at
a time. Do not use it with microneedling devices or any needle.

Three steps (field `custom.how_to_steps`, text only; the images stay):

1. Cleanse: wash with a gentle, pH-balanced cleanser and pat skin dry.
2. Apply the serum: press a few drops onto the forehead and around the eyes, keeping it out of the eyes. Wait 60 seconds.
3. Moisturise and SPF: follow with your moisturiser. Finish with SPF 30+ every morning.

## Clinical research

Field `custom.clinical_research`:

In a 4-week, double-blind trial, more people on 10% Argireline were graded clearly smoother around the eyes than on placebo.

- 60 adults, double-blind and placebo-controlled: 10% Argireline twice daily around the eyes for 4 weeks; clinicians graded more
  people as clearly improved on Argireline than on placebo
- Skin roughness fell on silicone replicas of the skin around the eyes; the placebo group showed no significant change
- In a 24-woman placebo-controlled trial, forehead roughness was lower than at the start by day 20 on Argireline while it rose
  on placebo; the day-60 difference from placebo was not significant
- In the same trial, water loss through the skin fell on Argireline and rose on placebo at day 20, which fits a skin that holds on
  to its moisture
- In a 40-woman, vehicle-controlled study, 10% Argireline lowered a measure of how unevenly skin resists stretching (facial
  anisotropy, which rises with age); the authors read this as firmer, tauter skin, but elasticity itself did not change
- No adverse effects were reported in the peptide groups of the controlled studies
- The evidence is mixed: an independent split-face imaging study of a hyaluronic acid serum with and without Argireline (19 women,
  4 weeks) found no difference between the two sides

Wang et al. 2013, Am J Clin Dermatol 14:147-153 (PubMed 23417317); Raikou et al. 2017, J Cosmet Dermatol 16:271-278
(PubMed 28150423); Tadini et al. 2015, Braz J Pharm Sci 51(4); Henseler 2023 (PubMed 38024099). In the Wang and Raikou trials the
ingredient was supplied through its distributors. Results describe the ingredient as studied, not this product; the full figures are on
the research page. [Read the research](/pages/acetyl-hexapeptide-8-research)

Register checks: the first bullet is claim 1, the second claim 2, the third claim 6 (day 20; the day-60 caveat is in the register),
the fourth claim 7 (worded as feel only), the fifth the Tadini correction of 2026-10-01 (firmness attributed to the authors),
the sixth claim 8 (Wang, Raikou; Tadini is not used for tolerability) and the last the Henseler 2023 null.

## FAQ

Field `custom.faq_items`. Items 1 to 6 follow the People Also Ask questions for "argireline" and "wrinkle serum"; item 7 is the
safety item.

1. **Does an Argireline serum really work on wrinkles?**
   In placebo-controlled trials of 10% Argireline, clinicians graded crow's feet as clearly improved in more people than on
   placebo after 4 weeks, and forehead roughness was lower by day 20 while it rose on placebo. One independent imaging study of a
   hyaluronic acid serum with Argireline found no difference between the sides. These are studies of the ingredient, not of
   this finished serum. It softens the look of expression lines; it does not change how your skin works, and the effect is not
   permanent.

2. **How long does an Argireline serum take to show results?**
   The trials measured at day 20 for the forehead and at 4 weeks for crow's feet, with twice-daily use. Plan on at least 4 weeks
   of morning and evening use. The studies measured results during use, and the effect is not permanent.

3. **How do I layer it, and what should I not use it with?**
   Apply it after cleansing, on slightly damp skin, before your moisturiser and SPF. If you also use the Matrixyl 3000 Firming
   Serum, apply this one first. No study has tested Argireline with other actives, so there is no tested do-not-mix list; add
   one new product at a time. Use it on intact skin only, never with microneedling devices or needles.

4. **Is Argireline better than retinol?**
   No study compares them, so nobody can say which is better. They are different kinds of ingredient: retinol is a vitamin A
   derivative and Argireline is a peptide. Retinol is not among this serum's listed actives, and you can use the serum on its own.

5. **Can I use Argireline and Matrixyl 3000 together?**
   They are two different peptides, one for the look of expression lines and one for the look of firmness, and we sell them as a
   pair. No study has tested Argireline and Matrixyl 3000 together, so we make no combined-result claim. If you use both, apply
   this serum first, then the [Matrixyl 3000 Firming Serum](/products/matrixyl-3000-firming-serum), then your moisturiser.

6. **What is acetyl hexapeptide-8, and is it the same as Argireline?**
   Acetyl hexapeptide-8 is the ingredient name for the peptide sold under the trade name Argireline. It was earlier called
   acetyl hexapeptide-3. It is modelled on part of SNAP-25, a protein involved in expression, and is designed to soften the look of
   expression lines. Laboratory findings are on the [research page](/pages/acetyl-hexapeptide-8-research).

7. **Are there side effects or downsides to Argireline?**
   In the controlled studies of Argireline, no adverse effects were reported in the peptide groups (45 users around the eyes for
   4 weeks in one trial; no warmth, stinging, redness, peeling or itching in another). Those studies are of the ingredient, not a
   tolerance test of this serum, and the main limit is the evidence: the studies are small and short. Patch test first: put a small
   amount on the inner forearm for 24 hours before the first full use. Stop using it if stinging or redness does not settle. Keep
   it out of the eyes. Argireline has not been tested in pregnancy, so ask your doctor if you are pregnant or breastfeeding.
   Never inject it.

## Alt text

Main product image: "Skingenetix Argireline serum: Acetyl Hexapeptide-8 Anti-Wrinkle Serum pack" (74 characters).

Check the wording against the image before use (bottle or carton).

## Internal links used

| Link | Where | Direction |
| --- | --- | --- |
| `/pages/acetyl-hexapeptide-8-research` | description, clinical research, FAQ 6 | up to the ingredient hub |
| `/blogs/clinical-studies/argireline-crows-feet-trial-wang-2013` | description | sideways to the study |
| `/blogs/clinical-studies/argireline-forehead-roughness-trial-raikou-2017` | description | sideways to the study |
| `/products/matrixyl-3000-firming-serum` | description, how to use, FAQ 3 and 5 | sideways to one sibling product |

The Tadini study (`/blogs/clinical-studies/argireline-skin-firmness-trial-tadini-2015`) is cited in the research text. Its link
can be added where the metafield allows links.

## What changed and why

| Field | Live text | Proposed text | Reason |
| --- | --- | --- | --- |
| SEO title | Acetyl Hexapeptide-8 10% Anti-Wrinkle Serum | Argireline Serum 10% for Expression Lines &#124; Skingenetix | Owner term at the front; "10% acetyl hexapeptide-8" reads as 10% pure peptide (register claims to avoid) |
| Meta description | "Nearly 1 in 2 saw clearly smoother crow's feet in 4 weeks ... On placebo: no one." | Page-specific description, no trial figure | Trial magnitude off the product (rule of 2026-09-26) |
| First line | "A targeted peptide serum that helps visibly relax the look of expression lines around the eyes and forehead." | Argireline serum with 10% Argireline peptide solution ... soften the look of crow's feet and forehead lines | Owner term and defining facts first; "relax" sounds like a muscle effect (register avoids "relaxes") |
| Bullet | "Acetyl Hexapeptide-8 - 10%, the concentration used in the clinical studies" | Removed | The match to the trial dose is conditional on the supplier grade (register claim 3; decision 8) |
| Bullet | "No parabens · no mineral oil · no synthetic fragrance" | Removed | Free-from claims removed on every product; "free from parabens" is not accepted (EC Technical Document, Annex III) |
| Bullet | "Helps soften the look of forehead lines, crow's feet and frown lines" | "... crow's feet and forehead lines" | No trial in the register covers frown lines |
| Best for | "...and anyone wanting a gentle, preventative anti-aging step" | "Adults who want a lightweight, twice-daily serum for expression lines" | "Gentle" is a tolerance claim with no product test; "preventative" is an unsupported outcome |
| Key benefit | "Relaxes the look of lines" | "Softer-looking expression lines" | As above |
| Key benefit | "Hydration - hyaluronic acid for a smoother, hydrated feel" | "Comfortable, hydrated feel - hyaluronic acid and ectoin" | Hydration is credited to the ingredient that provides it, not to the peptide (Tadini found no gain beyond the vehicle) |
| What to expect | "nearly 1 in 2 people were graded clearly smoother around the eyes after 4 weeks" | Direction and timing only | Magnitude removed |
| How to use | "...around the mouth" (step 2) | Removed | No trial covers the mouth area |
| How to use | "Best results build with consistent daily use over several weeks." | "Give it at least 4 weeks" | Matches the trial timing (day 20, 4 weeks) |
| Clinical research | "Nearly 1 in 2 saw clearly smoother-looking crow's feet in 4 weeks. On placebo: no one." | "...more people on 10% Argireline were graded clearly smoother ... than on placebo" | Magnitude removed; direction kept |
| Clinical research | "22 of 45 people graded clearly improved ... vs 0 of 15 on placebo" | "more people ... than on placebo" | Magnitude removed |
| Clinical research | "Forehead roughness down 7.4% by day 20, while it rose on placebo" | "lower than at the start by day 20 ... while it rose on placebo" | Magnitude removed |
| Clinical research | "48.9% is the share of people graded improved, not a wrinkle reduction." | Removed | The figure is gone, so the caveat is no longer needed |
| Clinical research | "Our serum contains 10% Acetyl Hexapeptide-8, the level used in the clinical trials" | Removed | Match to the trial dose awaits the supplier grade; "10% acetyl hexapeptide-8" is a claim to avoid |
| Clinical research | "Well tolerated: no side effects reported in the controlled studies" | "No adverse effects were reported in the peptide groups of the controlled studies" | Attributed to the studies; product has no tolerance test (register claim 8) |
| Clinical research | (not present) | Henseler 2023 null result, Tadini correction | Nuance belongs in the research text; the register lists Henseler as the only independent imaging test |
| FAQ | "Is it suitable for sensitive skin? Formulated without parabens, mineral oil or added synthetic fragrance, and it includes ectoin, a soothing hydration ingredient." | FAQ 7, the safety item | "Suitable for sensitive skin", "soothing" and the free-from list have no product-level support |
| FAQ | "helps relax the look of expression lines"; "typically builds over about 4 weeks" | FAQ 1, 2 | "Relax" removed; timing tied to the trials |
| FAQ | "It pairs well with the Copper Peptide or Matrixyl 3000 serums" | FAQ 5, Matrixyl only, no combined claim | No study of any pair; "pairs well" reads as a tested result |

Figures removed from the product (for decision 15): "Nearly 1 in 2" and "48.9%" (the share graded improved), "22 of 45" against
"0 of 15", and "7.4%" (forehead roughness, day 20). The placebo figure "+4.3%" was not on the live page. All four stay on the research
page and the study articles.

## Open questions for Malcolm

1. **Decision 3a: "Argireline" in the visible product title.** This draft assumes yes in the SEO title and first line. A fallback is given.
2. **Decision 8: the Argireline grade and peptide content.** Until the supplier sheet confirms the grade (NP, C or Amplified), the
   draft states "10% Argireline peptide solution" as on the label and drops the line "the level used in the clinical studies".
   If the grade is confirmed, claim 3 comes back as one sentence in the first cited fact.
3. **Decision 15: trial figures on the product.** Four figures were removed (list above). Restoring any of them reverses the
   rule of 2026-09-26.
4. **Possible INCI mix-up between products.** The live ingredient list for this serum includes palmitoyl tripeptide-1 and
   tetrapeptide-7, the Matrixyl 3000 pair. The Matrixyl register (gap 2) found the cream's list ending in acetyl hexapeptide-8 and
   suspects swapped lists between products. Check this serum's carton before the supporting-peptides bullet goes live.
5. **Decision 12: "Botox in a bottle".** No Botox item is drafted. The "What serum works like Botox?" question is in the
   People Also Ask box for "wrinkle serum"; the register lists every Botox comparison under claims to avoid.
6. **Microneedling sets.** The draft says never to use this serum with needles (register section 4, Chen 2021). The store also
   sells microneedling stamp sets; make sure no page suggests using this serum with them.
7. **Layering order.** "Argireline first, then Matrixyl, then moisturiser" follows the live pages' own rule (lighter serum first). It
   is not a tested finding.
8. **Study-article links.** All three study articles return a live page today. The Tadini link sits in the research text only.
9. **Trademark.** The register lists the owner as Lubrizol/Lipotec; the live page says Lubrizol. Confirm the owner name with the
   supplier before the sentence is kept.
10. **Alt text.** I have not seen the image. Confirm "pack" matches it.
