# Design critic, cycle 1: Learn article redesign, salmon sperm skin care (2026-10-09)

**Page:** `/blogs/learn/salmon-sperm-skincare-vs-the-salmon-sperm-facial?view=learn-salmon-sperm-skin-care` (hidden preview of
`templates/article.learn-salmon-sperm-skin-care.json`, spec `configs/hub-upgrades/learn-salmon-sperm-skin-care-design-2026-10-09.json`).
**Critic:** `design-critic` agent, fresh context. Captured live on 2026-10-09 with Klaviyo, Shopify Forms and the cookie dialog blocked,
and loads spaced about 30 s apart. Captures were taken at 390, 768, 1440 and 200% zoom, plus `measure.py` at 1440 and at 390. The page was set
beside the PDRN hub, the Ye 2026 study article and Collagen Skincare at 390 and 1440. No direction contract exists for this site (there is no
`website/design/`), so the page is judged against the reference family, the skill's craft rules, the PDRN claims register and the store rules
in memory.

**Disposition: FIX** (weighted 6.1). **Do not switch the article onto this template until Blocker 1 is decided.** Blocker 1 is a claims
question for Malcolm, not a build fault. Then fix High 2 to 4 and run cycle 2.

| Axis (sibling cycle-1 set) | This page, cycle 1 | Sibling (Argireline + Matrixyl) cycle 1 |
| -------------------------- | ------------------ | --------------------------------------- |
| Hierarchy                  | 6.0                | 5.5                                     |
| Rhythm                     | 5.5                | 4.0                                     |
| Imagery                    | 6.0                | 4.5                                     |
| Typography                 | 6.0                | 6.0                                     |
| Family fit                 | 7.0                | 7.0                                     |
| Mobile                     | 6.5                | 3.0                                     |

Rubric axes: Design 6.0 (40%), Usability 6.8 (30%, for human check), Creativity 4.5 (20%), Content 7.5 (10%) = **6.1**.

## Lessons from the sibling's cycle 1: status on this page

| #   | Sibling cycle-1 item              | Here          | Evidence                                                                                                                                                                         |
| --- | --------------------------------- | ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Phone page scrolls sideways       | **Pass**      | scrollWidth 390 at 390 and 320 at 320. Both tables stack as label/value rows under 700 px. At 200% zoom the content fits; only the site footer overflows (see the Nits).         |
| 2   | Watermarked photo                 | **Pass**      | None of the 15 content images carries a watermark or a filename alt.                                                                                                             |
| 3   | Bone runs, equal rhythm           | **Partly**    | The runs are shorter (1,976 px and 2,007 px at 1440, against 4,413 and 3,318), but there are still two, and every section still has 80 px top and bottom padding (High 2 and 3). |
| 4   | Key figure outsizes the H1        | **Pass**      | Figure 44 px under a 60 px H1 at 1440; 32.5 px under a 40 px H1 at 390.                                                                                                          |
| 5   | Byline buried                     | **Pass**      | It is the banner's last line at every width.                                                                                                                                     |
| 6   | Image implying penetration        | **Pass**      | No image shows anything passing into skin. The DNA banner, the gel strands, the pipette drop, the swatch, the spatula and the microscope make no depth claim.                    |
| 7   | Black banner on the phone         | **Pass**      | The hub's 1.048:1 mobile crop; the pink helices read.                                                                                                                            |
| 8   | Related row                       | **Partly**    | The images are square and the links name their destinations. The links are 18 px tall, and at 768 the row becomes a swipe strip (Medium 7).                                      |
| 9   | Image monotony, product by safety | **Partly**    | No product photo sits beside the safety copy. 12 of 15 content images are square at 1440 (13 of 15 at 390); the hub is also 17 of 20, so this is the family's habit.             |
| 10  | Key-figure source                 | **Pass**      | The Ye figure links "The 31-woman split-face trial".                                                                                                                             |
| 11  | Repetition                        | **Partly**    | Medium 9.                                                                                                                                                                        |
| 12  | Body size and line length         | **Not fixed** | Body is still 15 px (1440) and 14 px (390), a theme setting. Lines reach 104 characters in `names` and `work` (High 4).                                                          |

## Blockers

- **1.** **The before/after card reads as a photograph from the Ye trial, and the trial could not have produced it** (imagery/copy,
  for Malcolm's decision). The block is `proof` / `f1` and the image is `skingenetix-pdrn-eye-bag-volume-before-after-study.jpg` (d1440, y 5343 to 6163).
  Everything around the picture attributes it to the study:
  - the eyebrow reads "Eye bags, Ye 2026 eye-cream trial";
  - the labels say "After 28 days", the trial's own duration;
  - the result pill reads "Eye-bag volume −14.8% vs −10.2% with retinol";
  - the woman is cast to match the cohort (East Asian, 35 to 55), in candid phone-selfie realism.

  Ye was a **split-face** trial, with PDRN on one side and retinol on the other. The "after" panel shows both eyes changed by the same amount,
  yet the pill compares the two sides, so the picture shows a result the design cannot produce. This breaks the brief's rule that
  before/after illustrations must not imply study photographs. **The constraint:** Malcolm ruled out any AI or illustration disclosure on 2026-09-22,
  and the same image and labels are live on the Ye study page (slot `ye.o4`). So this is a question to put to him, not a fix to make unasked.
  **The spec fix to propose (labels only, no disclosure):**
  - `subheading` → "What a 15% smaller eye bag looks like";
  - `after_label` → "After";
  - `result_label` → "Ye 2026, PDRN side: −14.8% (retinol side −10.2%)".

  These labels describe the size of the change rather than the trial's photographs. The Ye page needs the same decision.

  The rest of the register check passes. No image shows PDRN reaching the dermis. The "Injection" route uses a consultation photograph
  (`skingenetix-dermatologist-skin-consultation-client-conversation.jpg`), with no needle and no equivalence drawn to the cream.

## High

- **2.** **Two sections have no background, so the bone runs return and the evidence card disappears** (layout/spacing). The body ground
  is `#F0F0F0`. `sperm` (media-with-text) and `proof` (research-before-after) set no section background, so both render on bone:
  - `answers`, `sperm` and `names` run as bone for 1,976 px at 1440 (2,315 px at 390);
  - `proof`, `safety`, `avoid` and `legal` run as bone for 2,007 px (2,494 px at 390).

  The `proof` card is `--rba-card-bg:#F0F0F0` on a `#F0F0F0` ground, so it has no edge at all. Its heading ("What can a salmon sperm serum or cream do…", in `serum`)
  sits alone on white, cut off from its own evidence. **Spec fix:**
  - `sperm` custom_css: `.section{background:#FFFFFF}`, and set block `m` `background` to `#F0F0F0`;
  - `proof` custom_css: add `.section{background:#FFFFFF}`.

  The result reads answers bone / sperm white / names bone, and serum and proof become one white block.

- **3.** **Equal weight: 15 of 16 sections use the same padding** (layout/spacing). Every `div.section` measures 80 px top and 80 px bottom. Only
  `avoid` differs (0 px top). `measure.py` reports `distinctSectionPaddings` 1 because it reads the outer wrapper; the real count is 2 (band ≥ 3,
  rule 23). The worst case: the `legal` H2 "Is salmon sperm skincare legal?" sits **16 px** below the patch-test paragraph, while every other H2
  gets 160 px. **Spec fix:**
  - `legal` custom_css: `.prose h2{margin-top:72px}`;
  - `prices` custom_css: `.section{padding-top:0}`, so the price note hangs off the routes row;
  - `work` custom_css: `.section{padding-block:120px}`, so the evidence section is the one that gets room.
- **4.** **The reading column jumps between three left edges, and two sections run 104-character lines** (layout/typography). At 1440 the H2s
  start at x 48 (`names`, `facial`, `work`, `label`, `related`), x 428 (`serum`, `safety`, `legal`) and x 812 (`sperm`). The edge changes 11 times
  down the page. `names` and `work` set 15 px text 104 characters wide with the right 40% of the screen empty (d1440 slices 1 and 2). The band is 50 to 70.
  **Spec fix:**
  - `names` custom_css: `.rich-text__wrapper{max-width:65ch;margin-inline:auto}` (the rule `serum` already uses);
  - `work` custom_css: `.rich-text__wrapper{margin-inline:auto}.prose>p{max-width:65ch}`, which keeps the five-column table at full width.

## Medium

- **5.** **The family's signature visual is missing** (imagery/family fit). The hub and the Ye study page both carry the rose-against-grey bar chart. Here the page's
  central number, 23.0% vs 6.6%, appears four times and only ever as text: the figure, the table cell, the short answer and the frame paragraph. **Spec fix:**
  reuse the Ye page's "How much each side improved in 28 days" chart, cut to two rows (crow's-feet area 23.0/6.6, eye-bag volume 14.8/10.2), as a
  liquid block in `work` after the table.
- **6.** **The key figures lose the accent on the phone** (colour). They render `#9E4F5C` at 1440 (sampled 158,79,92) but `#3E4A52` at 390 (sampled 62,74,82).
  The hub and Ye are rose at both widths. Links are rose in `answers` but `#1A1A1A` in `figures`, `work`, `products` and `related`. **Spec fix:**
  - `figures` `heading_text_color` → `#9E4F5C`;
  - add `a:not(.button){color:#9E4F5C}` to the `figures`, `work` and `related` custom_css.
- **7.** **Three rows become swipe strips at 768, with the last card cut off and no controls** (interaction, for human check). Measured scrollWidth
  against a 768 px viewport: `facial` 1,035, `label` 1,375, `related` 1,375. "The claims" and "A leave-on facial or cream" are cut at the edge. **Spec fix
  (each of the three custom_css):** `@media (min-width:700px) and (max-width:999px){.scroll-area{grid-template-columns:1fr 1fr!important;grid-auto-flow:row;overflow:visible}}`.
- **8.** **The card titles shout and the products outweigh the evidence** (hierarchy):
  - **Card titles.** The H3s are 36 px against 48 px H2s (0.75). "Yogya 2022: microneedling plus polynucleotide serum" wraps to 5 lines in a 300 px
    column, and the label checks ("The name") are 2.4× their 15 px text. **Spec fix:** `facial`, `label` and `related` custom_css `h3{font-size:26px}`.
  - **Products.** The two product tiles are 660×660 (the section is 1,021 px tall), as large as the before/after and twice the hub's shop
    tiles. **Spec fix:** `products_per_row_desktop` → 4.
  - **No primary action.** The only buttons in `main` are Subscribe and English. **Spec fix:** a `button` block in `label`, "See the label on our PDRN
    serum" → `/products/pdrn-renewal-serum`.
- **9.** **Repetition** (copy). The captions of figures `s1` and `s3` repeat short answers 1 and 2 word for word. "No placebo" appears 5 times. **Spec fix:** empty the
  `content` of `s1` and `s3` (the subheading carries them).
- **10.** **Image run at 390** (imagery). `facial` and `related` stack seven full-width 350×350 squares, 4,055 px in all, which is 28% of the 14,237 px page. The three
  routes are one sentence each under a mood picture. **Spec fix:** `related` custom_css `@media (max-width:699px){.multi-column{grid-template-columns:1fr 1fr}}`, so the four cards sit 2 by 2.

## Nits

- The "Learn" eyebrow is not a link; the Ye page has a breadcrumb. This is a repeat of the sibling's nit.
- The H1 is in Title Case, and every H2 is in sentence case.
- At 768, "23.0% vs 6.6%" breaks onto two lines.
- At 390 the `names` table's 2 px row rules stop about 32 px short of the text column.
- At 390 the icon row switches to centred alignment, and everything around it is left-aligned.
- "polynucleo/tides" breaks mid-word in the H2 at 200% zoom.
- These are site-wide, not this page's fault:
  - the footer logo and newsletter overflow 25 px at 200% zoom;
  - the Menu control measures 22×22 (for human check);
  - the page weighs 2,333 KB, including 839 KB of JS (rule 53: ≤ 1,500 KB);
  - body text is 15/14 px.

**Signature:** none yet. The candidate is the "0 sperm cells in the bottle" figure, which answers the search question in one glyph. It currently sits as
the first of three equal numbers, under the hub's own banner image. The first screen is therefore the hub's and the Ye page's first screen with
a different title.

**Three tells of assembly:** one padding value on 15 sections; a symmetric three-up grid of square mood images for the three routes; and the
reading column changing edge 11 times.

**Convergence cluster:** none cleanly. The page leans toward cluster 4 (rounded white cards on grey, nearly every image square).

**Single change that most improves the page:** High 2, two CSS rules and one block setting (minutes). It removes both bone runs and gives the
before/after its card back. Blocker 1 is a one-message question to Malcolm.

Captures and measurements (scratchpad, not committed):
`/private/tmp/claude-501/-Users-malcolmsmith-Claude-Code-Projects-skingenetix-website/4237e530-0fcc-4ba5-85dd-7427c7f586ff/scratchpad/critic/`
(`shots/` with the reference captures, `cap/`, `measure-1440.json`, `measure-390.json`). Contact sheet: `~/Desktop/learn-salmon-cycle1-renders.png`.
