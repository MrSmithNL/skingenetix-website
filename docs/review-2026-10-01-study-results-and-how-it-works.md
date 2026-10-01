# Study articles: one section per result, and how it works

**For:** Malcolm · **Date:** 2026-10-01 · **Decision record:** ADR-2026-10-01-R · **Rules:** `docs/study-page-template.md` §3.1

You asked for two things on every clinical-study article, both as the science pages have them:

- a separate section for each proven trial result, with a before/after picture where one can be used;
- separate blocks that explain how the active works on skin, for the effects that were tested.

**The template is built.** It is tested, and it is merged into `main` (`204c6f4`). It is not on the store yet: it goes up once the other
window's live audits finish. Until a study gets its own content, every live article renders exactly as it does today.

I then measured all eight articles against the new rules. Five researchers read each trial in full, plus the laboratory studies behind
it, and checked every sentence against the ingredient's claims register. Their proposals and source tables are in
`research/study-detail-2026-10-01/`.

## 1. Every article against the new criteria

None of the eight has a section per result or a how-it-works block today. Each result now sits only in a key figure, a chart row or a
sentence. Proposed:

| Article                     | Result sections                                                                     | Before/after         | How it works                                                                |
| --------------------------- | ----------------------------------------------------------------------------------- | -------------------- | --------------------------------------------------------------------------- |
| Badenhorst 2016 (copper)    | 3: wrinkle volume 55.8% more than the plain serum; 31.6% more than Matrixyl 3000; depth 32.8% more | 1 (volume)           | 2, from the paper's own lab arm: collagen up to +18%, elastin about +30% in skin cells |
| Ye 2026 (PDRN)              | 4: crow's feet and under-eye lines; elasticity and firmness; deeper-layer thickness; eye bags | 0 (see §2)           | 3: nine collagens, elastin and fibrillin in skin samples; collagen genes in cells |
| Watanabe 2014 (glutathione) | 4: skin pigment −10.7% vs −3.1%; crow's feet; texture; moisture                       | 1 (brightness)       | 0: the paper calls its mechanism speculation, and the one independent cell test found no effect |
| Robinson 2005 (Matrixyl)    | 2: age spots (week 12); texture (week 4). Fine lines held for decision 3            | 0: no size is known  | 2: collagen in lab-grown cells (Katayama 1993; Sederma's dose series)         |
| Wang 2013 (Argireline)      | 2: 22 of 45 graded clearly improved vs 0 of 15; smoother skin replicas              | 0 (see §2)           | 1: modelled on SNAP-25, in the developers' laboratory tests                   |
| Raikou 2017 (Argireline)    | 2: forehead roughness −7.4% vs +4.3%; water loss fell while placebo's rose          | 0: instrument results | 0: the authors say the mechanism is "not defined"                            |
| Tadini 2015 (Argireline)    | 2: firmness reading down a third, below the plain cream; already lower at week 2    | 0: instrument result | 0: nothing was tested                                                       |
| Yogya 2022 (PDRN)           | 1: eye wrinkles −14% vs −8% with saline at two months                               | 0: a procedure, speed only | 0: only the procedure itself, which the register keeps off the page       |

**Totals:** 20 result sections, 2 with a before/after, and 8 how-it-works blocks. Four articles get no how-it-works block. In each of
those four, nothing was tested that the register allows us to say, and an untested mechanism would be a supplier's claim, not evidence.

## 2. The before/after pictures

The sheet is on your Desktop (`skingenetix-before-after-check.png`), and a copy is in `research/study-detail-2026-10-01/`. It shows
each science-page picture beside what its trial measured. The written rule (`docs/clinical-trial-before-after-images.md` §3) is that
the picture's change must not exceed the trial's result. On a study article the picture sits next to the exact number, so the rule
bites harder there than on a hub.

| Picture (hub card)              | Trial measured                             | Picture shows                                 | Verdict           |
| ------------------------------- | ------------------------------------------ | --------------------------------------------- | ----------------- |
| Badenhorst crow's feet (copper f1) | one wrinkle's volume −24.1% vs −15.0%   | crow's feet −21% (measured); the forehead and under-eye soften too | **Fits, with a flag** |
| Watanabe brightness (glutathione f1) | pigment −10.7% vs −3.1%               | a modest, even brightening                    | **Fits**          |
| Wang crow's feet (Argireline f1) | lines softened, still there (the paper's photos) | the deep fold and most fine lines gone | Exceeds           |
| Raikou forehead (Argireline f5) | roughness −7.4%, by instrument             | lines visibly smoothed; eyelids differ        | Exceeds           |
| Ye crow's feet (PDRN f1)        | wrinkle area −23.0% vs −6.6%               | most lines gone; different light and background | Exceeds         |
| Ye eye bags (PDRN f4)           | eye-bag volume −14.8% vs −10.2%            | the bag has nearly gone                       | Exceeds           |
| Watanabe crow's feet (glutathione f2) | "visibly softer" in 1 in 3 women     | most crow's-feet and smile lines gone         | Exceeds           |

## 3. Live claims to correct (found while reading at source)

These are on live pages now, most of them in six languages:

| Priority | Page                         | What is wrong                                                                                  | Fix                                             |
| -------- | ---------------------------- | ---------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| High     | Ye article, PDRN hub card f4, PDRN register | "about 2×" retinol for eye bags; the paper's Figure 6B shows −14.8% vs −10.2% (about 1.5×) | say "about 1.5×", or give the two figures       |
| High     | Ye article chart              | "about 2×" for wrinkles **understates** them: −23.0% vs −6.6% is about 3.5×                   | rebuild the chart from Figure 6B (stronger, and exact) |
| High     | Badenhorst FAQ (and its FAQ schema) | the plain-serum comparison was in 20 women, not "39"; the answer opens with "not statistically significant" in bold | correct the count; lead with the result |
| Medium   | Badenhorst at a glance        | names Strivectin, which the register forbids                                                  | "a Matrixyl 3000 product"                       |
| Medium   | Badenhorst (three places)     | calls Dermatest "independent"; a Dermatest employee is a co-author                            | "a cosmetic research institute"                 |
| Medium   | Wang context                  | "quietening the signal that tightens expression muscles" paraphrases two avoid items          | the register's wording ("soften the look of expression lines") |
| Medium   | Raikou limits                 | a sentence about the muscle between the brows                                                 | the paper's own reason for measuring the forehead |
| Medium   | Watanabe limits item 4        | "the same on both sides" breaks positive-results-only                                         | delete                                          |
| Medium   | Tadini (four places)          | "firm and tighten", "firmer, tauter" go past the register's "more supple and even"            | update the register to the paper's "tensor effect" wording, or reword the page |
| Medium   | Key figures, five articles    | not results (template rule): Wang "3 of 3" and "0", Raikou "None", Badenhorst "39 of 40", Robinson "3 ppm", Ye "Day 14" | swap for magnitudes the researchers found (in their notes) |
| Low      | Ye chart                      | retinol in grey `#9AA3A4`, which fails contrast; the template requires `#8A9394`              | recolour with the rebuild                       |

The researchers' notes give replacement text for every row.

## 4. Decisions for you

**Decision 1: which before/after pictures go on the study articles?**

- **A (recommended).** Use the two that fit (Badenhorst, Watanabe brightness) now, and a plain photograph for the rest. Then run one
  image job for honest pairs of the four results a face can show: Wang crow's feet, Ye crow's feet, Ye eye bags and Watanabe crow's
  feet, each held to the trial's measured change. That job is a paid run, and I will price it before it starts.
- **B.** Reuse every hub picture as it is. This matches the hubs, but it breaks the written rule right beside the exact number.

Separately: four hub cards show the same over-large change. Should they be replaced as well?

**Decision 2: correct the live claims in §3?** I recommend all of them. The two Ye figures matter most: one overstates and one
understates. The six-language articles and the PDRN hub then need re-translating, which the study-i18n tool handles.

**Decision 3: Robinson's fine lines.** Should the result you approved as the page's lead, at the paper's looser p ≤ 0.10 bar, also
get its own section, labelled with that bar? I recommend yes.

**Decision 4: Wang's how-it-works block.** The Argireline register says to keep the SNAP-25 detail "on the learning hub". The block is
framed as the developers' laboratory work and uses no muscle or nerve words. I recommend allowing it on the study article.

**Decision 5: the pictures for about 26 plain blocks.** I propose picking first from the unused science pictures already in Shopify
Files (no cost), uploading copies under each ingredient's name and showing you a sheet. Anything missing would come from a priced
generation run.

## 5. What happens next

1. The template goes up in its documented order once the audits finish (`docs/study-page-template.md` §3.1, "First deploy").
2. On your decisions: the pictures, then the content goes into the eight configs.
3. Each article is previewed English first, through `?view=clinical-study-draft`.
4. Then the design critic and the central audit (done means 9 or more, with no confirmed failures).
5. You review it.
6. It is translated into five languages and goes live.
