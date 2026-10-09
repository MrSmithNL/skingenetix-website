# Matrixyl 3000 Pro-Collagen Firming Cream: English product-page draft (2026-10-09)

Status: DRAFT for Malcolm's review. Nothing here has been sent to Shopify. Sources: `docs/claims/matrixyl-3000.md` (register),
`docs/claims/collagen-skincare.md` (second register), `docs/website-traffic-and-performance-plan-2026-10-08.md` (Part 3.1, 3.2,
step 1.2, Part 7), `audits/2026-10-08-competitor-gap-per-page/teardown-products-collections.md` (section 4.1),
`configs/page-targets.json`, `audits/2026-10-08-competitor-gap-per-page/serp/raw/` (People Also Ask lists), and the live content
in `_current-matrixyl-3000-pro-collagen-firming-cream.json`.

## Target

| Item | Value |
| --- | --- |
| URL | `/products/matrixyl-3000-pro-collagen-firming-cream` |
| Owner term | matrixyl cream (today position 14.8 on 130 impressions for "peptide cream"; 5.6 for "matrixyl 3000") |
| Secondary terms | collagen cream with matrixyl, matrixyl 3000 cream |
| Page type | product |
| Job in the funnel | Buy page for "matrixyl cream". The creams collection takes "peptide cream"; the Collagen page `/pages/collagen-skincare` owns "collagen cream" |
| Primary action | Add to basket; quiet second step: read the Matrixyl 3000 research |
| Concentration stated | None. The label gives no percentage |
| Trial magnitudes on the page | None (rule of 2026-09-26; decision 15 is open) |

Decision notes:

- **"Collagen cream" is never targeted.** The phrase appears only inside the assigned secondary "collagen cream with Matrixyl 3000", once,
  in the description. The title uses "with Collagen" after "Matrixyl Cream", as the audit proposed.
- **Decision 3b (open): does this page also take "skin firming cream" and "peptide cream"?** Part 3.1 sends "skin firming cream"
  (201 US) here. Part 3.2 and the audit (section 4.1) send "peptide cream" (453 US / 395 GB) to the creams collection, and judge it
  not winnable by this page. Alternative lines for both are given below, marked as depending on 3b.
- **Decision 8 (open) and the register.** The cream's Matrixyl 3000 level is unknown, so the Sederma 2-month figures stay off.
- **Never pentapeptide-4.** The cream does not contain it (register section 0). No sentence here mentions it.

## SEO title and meta

| Field | Proposed text | Characters | Limit |
| --- | --- | --- | --- |
| SEO title | Matrixyl Cream with Collagen: Matrixyl 3000, 50 ml | 50 | 60 |
| Meta description | Matrixyl cream with Matrixyl 3000 peptides, a Triple Collagen Complex, hyaluronic acid and squalane for firmer-looking, smoother skin. 50 ml. | 141 | 155 |
| Alternative SEO title (only if 3b is "yes": skin firming cream) | Skin Firming Cream with Matrixyl 3000, 50 ml &#124; Skingenetix | 58 | 60 |
| Alternative meta description (only if 3b is "yes") | Skin firming cream with Matrixyl 3000 peptides, a Triple Collagen Complex, hyaluronic acid and squalane for firmer-looking skin. 50 ml. | 135 | 155 |
| Alternative SEO title (only if 3b adds "peptide cream") | Peptide Cream with Matrixyl 3000 and Collagen, 50 ml | 52 | 60 |

The owner term "matrixyl cream" appears once, at the front of the title. "Matrixyl 3000 cream" appears in the first FAQ question and in FAQ 3.

## Description

```html
<p><strong>This Matrixyl cream pairs Matrixyl 3000 (palmitoyl tripeptide-1 and palmitoyl tetrapeptide-7) with a Triple
Collagen Complex, hyaluronic acid and squalane in a 50 ml cream for firmer-looking, smoother skin.</strong></p>
<p>It is a collagen cream with Matrixyl 3000, and the two parts do different jobs. The collagen proteins work on the surface
of the skin. The Matrixyl 3000 peptides are the part associated with the skin's own collagen activity.</p>
<h3>What the research shows</h3>
<ul>
<li>Collagen molecules are too large to cross intact skin, so they sit on the surface as a moisture-retaining film, and only
some of the smallest hydrolyzed fragments can reach the outer layer. Collagen in a cream does not replace the collagen your
skin makes (<a href="/pages/collagen-skincare">what topical collagen does and does not do</a>).</li>
<li>In lab tests on skin cells, the two Matrixyl 3000 peptides together raised collagen I by more than either peptide on its
own. The ingredient's maker ran those tests, and they do not show what happens in skin.</li>
</ul>
<p>These results describe the ingredients as studied, not this cream. The full figures are on the
<a href="/pages/matrixyl-3000-research">Matrixyl 3000 research page</a>.</p>
<h3>What to combine and how to layer</h3>
<p>Use it as the last leave-on step, after your serums, on slightly damp skin. For a two-step firming routine, apply the
<a href="/products/matrixyl-3000-firming-serum">Matrixyl 3000 Firming Serum</a> first and this cream over it; both carry the
same two Matrixyl 3000 peptides. In the morning, finish with SPF. The manufacturer's Matrixyl 3000 studies ran for 2 months, so
give it 2 months.</p>
<h3>Who it is for</h3>
<p>Normal-to-dry and mature-looking skin that wants a richer cream. The texture comes from squalane and hyaluronic acid.
The cream contains collagen of animal origin, so it is not vegan.</p>
<p><strong>Size:</strong> 50 ml</p>
<p>Matrixyl&reg; and Matrixyl&reg; 3000 are registered trademarks of Sederma (Croda).</p>
```

If 3b is "yes" (skin firming cream), the first line becomes: "This skin firming cream pairs Matrixyl 3000 (palmitoyl
tripeptide-1 and palmitoyl tetrapeptide-7) with a Triple Collagen Complex, hyaluronic acid and squalane in a 50 ml cream for
firmer-looking, smoother skin." The second sentence of the next paragraph then reads "It is a skin firming cream with Matrixyl 3000
and collagen, and the two parts do different jobs."

If 3b also adds "peptide cream", the first line becomes: "This peptide cream pairs Matrixyl 3000 (palmitoyl tripeptide-1 and
palmitoyl tetrapeptide-7) with a Triple Collagen Complex, hyaluronic acid and squalane in a 50 ml cream for firmer-looking, smoother
skin." Link "peptide cream" once to `/collections/creams-moisturizers`. The audit (section 4.1) advises against giving this page the term.

## Key benefits

Field `custom.key_benefits`, one bullet per line:

- Firmer-looking, plumper skin - the two Matrixyl 3000 peptides, whose maker's studies ran for 2 months
- Smoother, more supple-looking surface - collagen proteins that sit on the skin as a moisture-retaining film
- Triple Collagen Complex - collagen, hydrolyzed collagen and soluble collagen, with Matrixyl 3000 in the same cream
- Rich, comfortable feel - squalane, hyaluronic acid and allantoin
- What to expect: it feels rich and comfortable from the first use. The manufacturer's Matrixyl 3000 studies measured results at
  2 months, so give it 2 months.

## How to use

Field `custom.how_to_use`:

Use morning and/or evening as the last leave-on step, after your serums. Massage a pea-sized amount over slightly damp skin on the
face and neck. In the morning, follow with SPF. Give it 2 months before judging it.

Layering: apply the [Matrixyl 3000 Firming Serum](/products/matrixyl-3000-firming-serum) first, then this cream over it. No study
has found anything Matrixyl 3000 should not be used with, and none has tested combinations. Add one new active at a time
(retinol, exfoliating acids) and patch test first.

Three steps (field `custom.how_to_steps`, text only; the images stay):

1. Cleanse: wash with a gentle, pH-balanced cleanser and pat skin dry.
2. Apply your serum: use the Matrixyl 3000 Firming Serum or your usual serum, and let it absorb.
3. Matrixyl cream and SPF: smooth on the cream, then finish with SPF 30+ in the morning.

## Clinical research

Field `custom.clinical_research`:

In lab tests on skin cells, the two Matrixyl 3000 peptides together raised collagen I by more than either one alone.

- Lab work only: it does not show what happens in skin, and no study has measured collagen in living skin for Matrixyl 3000
- The manufacturer's Matrixyl 3000 studies ran for 2 months; their figures are on the research page
- No independent controlled trial of Matrixyl 3000 on its own has been published
- The independent Cosmetic Ingredient Review Expert Panel assessed both Matrixyl 3000 peptides as safe in cosmetics at current use
  levels (2018); this is a finding about the ingredient, not a test of this cream
- Collagen proteins are too large to cross intact skin; they act on the surface as a moisture-retaining film, and only some small
  hydrolyzed fragments reach the outer layer

Lab: Sederma patent US 6,974,799 (human skin cells, 3 days). Safety: Johnson et al., "Safety Assessment of Tripeptide-1,
Hexapeptide-12, Their Metal Salts and Fatty Acyl Derivatives, and Palmitoyl Tetrapeptide-7 as Used in Cosmetics", Int J Toxicol 2018
(DOI 10.1177/1091581818807863). Collagen size: Bos and Meinardi, Exp Dermatol 2000;9:165-169 (PubMed 10839713). Results describe
the ingredients as studied, not this product; the full figures are on the research page.
[See all the Matrixyl 3000 research](/pages/matrixyl-3000-research)

## FAQ

Field `custom.faq_items`. Items 1 to 6 follow the People Also Ask questions for "matrixyl 3000" and "skin firming cream"; item 7
is the safety item.

1. **What does Matrixyl 3000 do for your face, and what does the cream add?**
   Matrixyl 3000 is a pair of signal peptides, palmitoyl tripeptide-1 and palmitoyl tetrapeptide-7, developed by Sederma. They are
   matrikines: short peptides modelled on pieces of the skin's own matrix proteins and associated with the skin's own collagen
   activity. In cosmetics they are used for the look of firmer, smoother skin. This cream adds a Triple Collagen Complex,
   hyaluronic acid, squalane and allantoin.

2. **Does a skin firming cream like this really work, and how long does it take?**
   A cream changes how skin looks and feels; it does not lift or tighten tissue. The manufacturer's Matrixyl 3000 studies ran for
   2 months, so plan on 2 months of daily use. No independent controlled trial of Matrixyl 3000 on its own has been published, and
   no study has tested this finished cream. Its richer texture comes from squalane and hyaluronic acid.

3. **Can I use the Matrixyl 3000 cream every day, and where does it go in my routine?**
   Use it morning and/or evening as the last leave-on step, after your serums. Apply the Matrixyl 3000 Firming Serum first if you
   use it, then this cream, and finish with SPF 30+ in the morning.

4. **What can I not mix with Matrixyl 3000?**
   No study has found anything Matrixyl 3000 should not be used with, and none has tested combinations. Add one new active at a
   time, such as retinol or an exfoliating acid, and patch test first.

5. **Is Matrixyl 3000 better than retinol?**
   No study compares them, so nobody can say which is better. Peptides like these are not acids or vitamin A derivatives, so they
   are a different kind of ingredient from retinol.

6. **Does the cream contain real collagen, and is it vegan?**
   Yes to the first: the Triple Collagen Complex lists collagen, hydrolyzed collagen and soluble collagen. It is of animal origin,
   so the cream is not vegan. Collagen proteins sit on the surface as a moisture-retaining film and do not replace the collagen
   your skin makes; the Matrixyl 3000 peptides are the part associated with the skin's own collagen activity.

7. **Are there side effects, and should I patch test?**
   The independent Cosmetic Ingredient Review Expert Panel assessed both Matrixyl 3000 peptides as safe in cosmetics at current use
   levels. That is a finding about the ingredient, not a tolerance test of this cream. Patch test first: put a small amount on the
   inner forearm for 24 hours before the first full use. Stop using it if stinging or redness does not settle. The cream contains
   collagen of animal origin, so ask us or your doctor first if you have a known allergy to animal proteins. The peptides have not
   been tested in pregnancy, so ask your doctor if you are pregnant or breastfeeding.

## Alt text

Main product image: "Skingenetix Matrixyl 3000 Pro-Collagen Firming Cream, 50 ml pack" (64 characters).

Check the wording against the image before use (jar or carton).

## Internal links used

| Link | Where | Direction |
| --- | --- | --- |
| `/pages/matrixyl-3000-research` | description, clinical research | up to the ingredient hub |
| `/products/matrixyl-3000-firming-serum` | description, how to use, FAQ 3 | sideways to one sibling product (the duo) |
| `/pages/collagen-skincare` | description | sideways to the Collagen page, which owns "collagen cream" |
| `/collections/creams-moisturizers` | only if 3b adds "peptide cream" | up to the creams collection |

There is no study article for this cream: the pentapeptide-4 trial (`/blogs/clinical-studies/matrixyl-wrinkle-trial-robinson-2005`)
is not linked here because the cream does not contain pentapeptide-4.

## What changed and why

| Field | Live text | Proposed text | Reason |
| --- | --- | --- | --- |
| SEO title | Matrixyl 3000 Pro-Collagen Firming Cream &#124; Skingenetix | Matrixyl Cream with Collagen: Matrixyl 3000, 50 ml | Owner term "matrixyl cream" first; "with Collagen" avoids the bare "collagen cream" the Collagen page owns |
| Meta description | "Firming cream with collagen, elastin and Matrixyl 3000 for firmer, plumper-looking skin and rich hydration. Ideal for mature or drier skin." | Matrixyl cream with the named actives | "Elastin" is not in the ingredient list (collagen register section 0); "ideal for" read as a promise |
| First line | "A firming cream with a triple collagen complex and Matrixyl 3000 peptides ..." | Owner term and named actives | Owner term first; two peptides named |
| Bullet | "No parabens · no mineral oil · no synthetic fragrance" | Removed | Free-from claims removed; "free from parabens" is not accepted (register section 2, number 18) |
| Bullet | "Triple Collagen Complex + Matrixyl 3000 - collagen proteins and matrikine peptides" | Split into two bullets | Keeps the two jobs apart (surface film vs peptides) |
| Best for | "mature or drier skin that wants firmer, plumper-looking skin and rich, comforting hydration" | "Normal-to-dry and mature-looking skin that wants a richer cream" | Hydration credited to texture, not promised as an outcome |
| Key benefit | "Collagen support - triple collagen complex with Matrixyl 3000 peptides" | "Triple Collagen Complex - collagen, hydrolyzed collagen and soluble collagen" | "Collagen support" reads as a physiological action |
| Key benefit | "Rich hydration - for a nourished, comfortable feel" | "Rich, comfortable feel - squalane, hyaluronic acid and allantoin" | "Nourished" is not measurable |
| What to expect | "skin feels smoother and softer from the first use" | "feels rich and comfortable from the first use" | Sensory only (register section 2, number 7) |
| Clinical research | "Matrixyl 3000's two peptides raised collagen I by 256% in lab tests on skin cells." | "...raised collagen I by more than either one alone" | Magnitude removed; the lab qualifier stays |
| Clinical research | "Collagen I +256% in lab tests, nearly 4x the stronger peptide alone" | Direction only | Magnitude removed |
| Clinical research | "Fibronectin +147% and hyaluronic acid +92% in the same tests" | Removed | Magnitudes removed (decision 15) |
| Clinical research | "This cream is built around Matrixyl 3000, a pair of signal peptides from Sederma" | Kept in FAQ 1 | Correct (register section 2, number 16) |
| Clinical research | "Both peptides assessed safe in cosmetics by an independent expert panel" | Kept, with the "not a test of this cream" clause | Register claim 5; conditions kept |
| Clinical research | (not present) | Collagen size and surface-film bullet | Collagen register claim 1; it agrees with the Collagen page |
| FAQ | "Formulated without parabens, mineral oil or added synthetic fragrance. We recommend a patch test first." | FAQ 7, the safety item | The free-from list has no support |
| FAQ | "Is it vegan? ... collagen and elastin of animal origin ... free from parabens and mineral oil" | FAQ 6, "collagen of animal origin" only | Elastin is not in the disclosed ingredients (collagen register section 0); free-from removed |
| FAQ | "Is it suitable for dry or mature skin? Yes. Its richer texture ... well suited ..." | Moved into "Who it is for" | Replaced by People Also Ask-based items |
| FAQ | "Apply the serum first, then this cream to seal" | Kept in FAQ 3 and how to use | "Seal" dropped (occlusion not covered) |
| Layering | "the same Matrixyl 3000 peptide family" | "the same two Matrixyl 3000 peptides" | Precise; avoids "family" implying pentapeptide-4 |

Figures removed from the product (for decision 15): "256%" (collagen I in lab tests), "nearly 4x the stronger peptide alone",
"+147%" (fibronectin) and "+92%" (hyaluronic acid).

## Open questions for Malcolm

1. **Decision 3b: skin firming cream and peptide cream.** Alternative lines are given for both. The audit's own verdict (section 4.1)
   is that this page cannot win "peptide cream"; I recommend "skin firming cream" only.
2. **Elastin.** The pack reads "Triple Collagen, Elastin" and the live FAQ says the cream contains elastin, but no elastin appears in
   the disclosed or full ingredient list. I left elastin out. Please confirm against the carton.
3. **Collagen source species.** Not disclosed anywhere. The Cosmetic Ingredient Review panel advises labelling fish-derived collagen,
   because fish is a major allergen. FAQ 7 carries an allergy line; I kept the collagen safety claim out of the description for this reason.
   Please ask the formulator which animal the collagen comes from.
4. **Vegan contradiction.** `/pages/ingredients` says every formula is vegan; this cream's FAQ says it is not. This draft only repeats the
   cream's own statement. The ingredients page needs a separate fix.
5. **Possible swapped ingredient lists.** The register (gap 2) found this cream's full list ending in acetyl hexapeptide-8 and the PDRN cream's
   list ending in the Matrixyl 3000 pair. If this cream does hold Argireline, no copy here mentions it. Check the carton.
6. **Tension between the brief and register claim 5.** The brief says never to write "safe". Register claim 5 and the live copy use the
   panel's conclusion about the ingredients. I kept it in the research text and FAQ 7 only, with "not a test of this cream".
7. **Cannibalisation.** This page also carries "matrixyl 3000 cream" and already ranks 5.6 for "matrixyl 3000", the serum's owner term.
   The first line uses "Matrixyl 3000 cream" once; the serum keeps the head term.
8. **Trademark line.** The register (gap 8) asks for the supplier's confirmation. Remove the sentence if it is not confirmed.
9. **Alt text.** I have not seen the image. Confirm "pack" matches it.
