# Design critique, cycle 1: four new clinical-study drafts (2026-09-30 / 10-01)

**Pages:** the English drafts on the hidden preview blog `/blogs/clinical-studies-drafts/`: Yogya 2022 (PDRN), Tadini 2015
(Argireline), Robinson 2005 (Matrixyl), Watanabe 2014 (glutathione).

**Who judged:** the `design-critic` agent, in a fresh context. It captured every page at 1440, 390 and 195 (200% zoom), and
measured hero contrast under each line of text. Evidence sheet: `~/Desktop/skingenetix-study-drafts-critique-renders.png`.

**Reference:** the live Badenhorst 2016 article.

## Verdict

FIX on all four, none REBUILD.

| Page          | Total | Disposition   | Lead findings                                                                                                                                                                        |
| ------------- | ----- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Yogya 2022    | 5.89  | FIX           | Phone hero: breadcrumb 4.37:1 and deck 4.15:1 (need 4.5). No effect size in the key figures. Saline grey 2.58:1                                                                      |
| Tadini 2015   | 6.22  | FIX (minor)   | "Public" and "Week 2" as key figures. Chart values far from their bars                                                                                                               |
| Robinson 2005 | 5.59  | FIX (blocker) | Story image showed droplets passing into the dermis, a claim the Matrixyl register says to avoid. Grey meant "stricter test", not placebo. Value labels ran 4px from the card border |
| Watanabe 2014 | 6.16  | FIX (minor)   | Placebo grey 2.58:1. The 511px phone banner was upscaled 1.6×. The chart plotted the unscored ratings, not the measured result                                                       |

## Fixed in each page's config (no shared template or renderer change)

| Finding                                                    | Fix                                                                                                                                                  |
| ---------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| **R1** Robinson image draws dermal penetration             | Replaced by GEN-192: a peak of white moisturiser on deep teal. The trial tested a moisturiser, and teal is Matrixyl's colour                         |
| **Y1** Yogya phone hero below AA                           | New phone banner with a stronger scrim (0.78), measured 5.7:1 over the text zone                                                                     |
| **W2** Watanabe phone banner soft                          | New 716×688 crop from the hub banner's lossless original (GLR-4-GOLDEN-FLUID), scrim 0.45, 5.61:1                                                    |
| **Y3, W1** comparator grey 2.58:1                          | `#9AA3A4` changed to `#8A9394` (3.14:1)                                                                                                              |
| **R2** grey meant "stricter test"                          | The stricter-test series is now a teal tint, `#4A9396` (3.56:1). Grey stays the comparator on every chart                                            |
| **R3** value labels overflowed                             | Labels shortened to "2 of 3"; the weeks stay in the caption                                                                                          |
| **Y2, T-a, R5** key figures were times, p-values and words | Yogya: −14% indentation (saline −8%) and 2.2/10 pain. Tadini: −33% by week 4, −37% by week 2, 40 women. Robinson's label carries p ≤ 0.10            |
| **W3** chart plotted the unscored ratings                  | Now plots melanin index at the start and at week 10, both sides, with bars from 0                                                                    |
| **W4** old glutathione accent                              | `#8A6914` changed to the hub's `#836310` in the chart                                                                                                |
| **Owner note** "How to read" points                        | Yogya elasticity now leads with "the same on both sides at six months". Tadini moisture now reads "rose with both creams", with no "did not" framing |

## Left open, for Malcolm (shared parts)

- **S2, the chart component.** The critic wants values at the bar ends, a fixed comparator-grey token, the table in a
  `<details>`, and left-aligned captions. It is shared with the five hubs, so changing it changes approved pages.
- **S1, story images.** Three of the four are a single droplet in the ingredient's colour. The pool has no images of the
  instruments the trials used (a microneedling device, a Mexameter, a Reviscometer). New ones would mean a paid generation run.
- **Already on the owner's list** (template-wide): T2/T3 heading scale, T6 card look, T7 shared microscope and scientist
  images, and 77-character lines in the answer section.

Re-audit after these fixes: see `page-audit-2026-09-30-<handle>-draft-preview-after-critique.*`.
