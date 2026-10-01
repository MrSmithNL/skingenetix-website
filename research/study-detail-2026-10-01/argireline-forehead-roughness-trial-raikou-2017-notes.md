# Raikou 2017 (Argireline®, forehead): results and how-it-works, notes

**Config:** `configs/studies/argireline-forehead-roughness-trial-raikou-2017.json` (live, English only). **Proposal:**
`argireline-forehead-roughness-trial-raikou-2017.json` in this folder. 2 results (both plain photographs), 0 how-it-works blocks.
**Written:** 2026-10-01. Register: `docs/claims/argireline-acetyl-hexapeptide-8.md`.

## 1. What I read

**Full text, all 8 pages** (_J Cosmet Dermatol_ 16:271–278): the author institution's repository PDF linked in register row 6
(relabaima.uniwa.gr), extracted and read in full. That covers Methods 2.1–2.7, Results 3.1–3.3, Tables 2 and 3, Figures 1–3, the Discussion
and the Acknowledgement. Links checked: [PubMed 28150423](https://pubmed.ncbi.nlm.nih.gov/28150423/) (esummary: Raikou V, 2017, _J Cosmet
Dermatol_) and DOI 10.1111/jocd.12314 (Crossref: Raikou, 2017, same title). The JSON cites the DOI, as the rest of the page does.

## 2. Source table: every number in the proposal

Group codes: G3 = acetyl hexapeptide-3 (Argireline®) alone; G4 = placebo.

| Number                                                                               | Source                                                                                         |
| ------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| Skin Visioscan VC98, built-in CCD camera                                             | §2.2, p. 272; §2.7.1, p. 274                                                                   |
| cR2 = cyclic maximum roughness, "indicative of fine lines"                           | §2.7.1, p. 274; Figure 1 caption, p. 275                                                       |
| Seated in an armchair, eyes closed "to relax"; 20-minute acclimatisation at 19–21 °C | §2.4, p. 272                                                                                   |
| cR2 G3: 83.8 → 77.6 (day 20) → 75.0 (day 40)                                         | Table 2, p. 275                                                                                |
| cR2 G4: 82.3 → 85.8 (day 20)                                                         | Table 2, p. 275                                                                                |
| −7.4% vs +4.3% at day 20                                                             | Table 3, p. 275 (G3 −7.4 marked b,c; G4 4.3 marked c, so the shared letter "c" marks G3 vs G4) |
| P = .022                                                                             | Results 3.1.1 and Figure 1 caption, p. 275                                                     |
| "Forehead measurement is common practice for products targeting moderate lines"      | §2.4, p. 272                                                                                   |
| Clearest results on the forehead                                                     | Results 3, p. 275 ("The significant results were obtained for the frontal region")             |
| Tewameter TM300; open-cylinder probe with two sensor pairs                           | §2.2, p. 272; §2.7.2, p. 274                                                                   |
| TEWL G3: 8.1 → 5.7 (day 20) → 5.4 (day 40)                                           | Table 2, p. 275                                                                                |
| TEWL G4: 7.0 → 10.0 (day 20) → 18.0 (day 40)                                         | Table 2, p. 275                                                                                |
| P = .025 (day 20), P = .01 (day 40)                                                  | Results 3.2, p. 276; Figure 3 caption                                                          |
| Only G3 fell; G1, G2 and G4 rose                                                     | Results 3.2, p. 276                                                                            |
| Dryness reported only by the placebo group                                           | §3.3, p. 277 ("Dryness (score 3) was reported by the subjects of G4")                          |

**Not printed in the paper:** the TEWL unit. Table 2 gives bare numbers, and g/m²/h is the Tewameter's standard unit. The proposal prints no
unit. The live key figure says "(g/m²/h)": that is an inference, not a reading (see D3).

**Not used:** cR3 (−5.3% vs +7.2%). Table 3's letters give G3 and G4 no shared mark at day 20, and the text lists no G3–G4 cR3 test, so it
is not a significant result against placebo. The day-60 figures are not used either: G3 vs G4 was not significant at day 60 (register row 6:
never use −11.7% as "vs placebo").

**Paper typo, as the register notes:** the prose of 3.1.1 prints placebo as "−4.6%"; Tables 2 and 3 give +4.3%. The proposal follows the
tables.

## 3. Before/after reasoning, per result

| Result                                | Decision                                                 | Why                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ------------------------------------- | -------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1. Forehead cR2 −7.4% vs +4.3%        | **Plain photograph** (I agree with the client's default) | It is an instrument reading of a roughness value, which §3.1 lists under "Picture, plain". A 7.4% change in a camera-derived roughness value is not a change a viewer can see. The hub's `forehead-lines-before-after.jpg` also fails §3 of the image rules: the woman's eyelids sit visibly lower in the before panel (the card-images config itself records "her eyelids sit lower in the before panel"), so the after looks more awake. Something besides the measured area improves. Contact sheet: `detail/argireline/argireline-before-after-check.png`, panel 3. |
| 2. Water loss 8.1 → 5.7 vs 7.0 → 10.0 | **Plain photograph**                                     | An instrument reading with nothing to see on a face. A photograph of droplets or "dewy" skin would picture a "hydrates" claim, which the register forbids.                                                                                                                                                                                                                                                                                                                                                                                                              |

**My honest view on the hub picture (card f5):** it should not carry "Forehead roughness −7.4% vs +4.3% on placebo (day 20)" either, for the
same two reasons. Flagged for the hub (D4).

## 4. How it works: zero blocks, and why

- **The trial tested no mechanism.** The Discussion (p. 277): "The possible mechanisms of the influence of acetyl hexapeptide-3 and/or
  tripeptide-10 citrulline on skin barrier have not been defined in our study." On water loss: "there is no evidence in the bibliography
  regarding the correlation of the tested peptides with TEWL" (p. 277). So the water-loss finding is written as **result 2**, never as a
  mechanism or as "barrier repair" (register row 7: "Do not say 'repairs the skin barrier'").
- **No second laboratory finding exists to tailor.** The only laboratory finding specific to Argireline (SNARE complex assembly, Blanes-Mira
  2002, abstract only) is used once, on the Wang 2013 page. A reworded copy here would be the same block on two pages. The independent cell
  test (Lim 2018) found Argireline's own effect not significant (Figure 5B), so it cannot be used. Kraeling 2015 (skin samples) is a
  penetration finding, not an effect. Wang 2013 JCLT (collagen in mice) is on the AVOID list ("Boosts collagen"). Full detail in the Wang
  notes, §4.
- The JSON keeps `mechanisms` with `items: []` and a `_why_none` note, so the section renders nothing.

## 5. Register check: result sentences that carry a claim

| Sentence                                                                                                                                            | Register line                                                                                                                                               |
| --------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "Forehead roughness fell 7.4% in 20 days while it rose 4.3% on placebo"                                                                             | Row 6 (A): "At day 20, roughness cR2 fell −7.4% with Argireline and rose +4.3% with placebo (P = .022)", and "Use the day-20 figure only"                   |
| "For a reader, this is forehead skin measurably smoother within three weeks ..."                                                                    | Row 6 hero: "Smooths forehead lines and texture from day 20"                                                                                                |
| "kept edging down afterwards, to 75.0 at day 40"                                                                                                    | A group mean, with no comparison to placebo claimed (row 6: "Do not use −11.7% as 'vs placebo'"; the same care applies to day 40)                           |
| "Water loss through the skin fell by days 20 and 40 while it rose on placebo"                                                                       | Row 7: "significant against placebo at day 20 (P = .025) and day 40 (P = .01), but not at day 60"                                                           |
| "The lower the reading, the more of its moisture the skin is holding on to" / "skin that held on to more of its moisture through the first 40 days" | Row 7: "Word it as appearance or feel only ('helps skin hold on to moisture'). Do not say 'repairs the skin barrier'." No "hydrates" (AVOID row "Hydrates") |
| "Argireline® was the only one of the trial's four creams under which water loss fell"                                                               | Results 3.2. It makes no combination or Matrixyl claim (AVOID: "Synergy with Matrixyl 3000")                                                                |

## 6. Flags on the current config (D)

| #   | Where                                     | Current text                                                                                                                                                                               | Problem                                                                                                                                                                                                                                                                                 | Suggested fix                                                                                                                                                                                                    |
| --- | ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| D1  | `limits.items[3]` "Where it was measured" | "The significant differences were on the forehead, **which the authors put down to the single main expression muscle between the brows, against the larger muscle group around the eye.**" | Read in our voice, it says the peptide's effect depends on how many muscles are involved, which is an implied muscle-action claim. The AVOID list covers "relaxes facial muscles", and template §3.1 says nothing about muscles for Argireline. "Reporting a study is still our prose." | "Skin was imaged on the forehead and around the eyes. The significant differences were on the forehead, the site where cosmetics aimed at moderate lines are usually measured, the authors note." (§2.4, p. 272) |
| D2  | `figures[2]`                              | "None — Skin reactions reported with the peptide creams"                                                                                                                                   | A word, not a result (§4 "Key figures are results"). The paper reports a further magnitude: day-40 water loss.                                                                                                                                                                          | **"5.4 vs 18.0"** — "Water loss through the skin at day 40", note "With Argireline® against the placebo cream (P = .01; Table 2)". Tolerability stays in the FAQ and the safety block.                           |
| D3  | `figures[1]` label                        | "Water loss through the skin fell, day 20 **(g/m²/h)**"                                                                                                                                    | The paper never prints a unit (Table 2). The value shows the active's before and after only; its comparator is in the note.                                                                                                                                                             | Drop the unit. Optionally make it "8.1 → 5.7 vs 7.0 → 10.0" if the figure style allows.                                                                                                                          |
| D4  | Hub card f5 (outside this config)         | `forehead-lines-before-after.jpg` labelled "Forehead roughness −7.4% vs +4.3% on placebo (day 20)"                                                                                         | Instrument-scale result; the eyelids differ between panels (see §3).                                                                                                                                                                                                                    | Replace with a plain photograph, or regenerate the pair with eyelids, expression and gaze locked and only a light softening of the forehead lines.                                                               |

Raikou is "done" (audit 9.82, ADR-2026-09-30-Q). D1 is the only flag I would act on before the new sections go up. D2 and D3 are optional
polish.

Checked and fine: the answer, verdict, chart and caption (only cR2 is called significant), glance rows (coded 50 g jars, mean age about 45,
Crallis supply), the media body, and the FAQ. **A useful extra source:** the paper's introduction (p. 271) says "The acetyl hexapeptide-3 or
acetyl hexapeptide-8, as it has been recently renamed". That is primary-literature support for the "another label name" line on the Tadini
page, which until now rested on tertiary sources (see the Tadini notes).

## 7. Open questions for the client

1. Should the hub's forehead card (f5) keep its before/after? My view is no (§3).
2. Accept D1's rewrite of the "Where it was measured" item?
3. The proposal has no how-it-works block on this article. Is that acceptable, or do you want one? Any block here would repeat the Wang
   page's laboratory finding.
