# Design critic, cycle 3: Learn article redesign, salmon sperm skin care (2026-10-09)

**Page:** `/blogs/learn/salmon-sperm-skincare-vs-the-salmon-sperm-facial?view=learn-salmon-sperm-skin-care`, the hidden preview of
`templates/article.learn-salmon-sperm-skin-care.json`, built from spec `configs/hub-upgrades/learn-salmon-sperm-skin-care-design-2026-10-09.json`.

**Critic:** the `design-critic` agent, in a fresh context. This is cycle 3, the last one.

**Method:**

- **Captures:** taken live on 2026-10-09 at 1440, 768, 390 and 200% zoom (a 195 px viewport). Klaviyo and Shopify Forms were route-aborted,
  the cookie dialog was hidden, the page was scrolled in steps before each full-page capture, and loads were spaced about 30 s apart.
- **Measurements:**
  - `measure.py` at 1440 and 390;
  - DOM probes at all four widths: characters per line counted from line boxes, heading sizes and x positions, link colours, the CTA's box,
    table columns, and scroll widths;
  - pixel samples of each section's ground;
  - a menu test with pop-ups blocked: the menu was opened, its links hit-tested, and Escape pressed.
- **Unblocked pass:** I also ran `capture.py --menu --zoom`. It does not block Klaviyo, so its menu frames show the newsletter pop-up, not the
  menu.
- **References:** the PDRN hub, the Ye 2026 study page and the live Argireline + Matrixyl sibling, captured today at 1440 and 390.

**Known context, stated once:** this site has no direction contract and no `website/design/` folder, so the page has no signed signature to be
judged against. Malcolm decides whether the Learn family goes back to the art director. Below, the page is judged on its own merits, against the
reference family, the craft rules, the PDRN claims register and the store rules.

## Disposition

**FIX, weighted 6.5** (6.45 before rounding). Cycle 2 scored 6.3 and cycle 1 scored 6.1, so **this cycle is the best of the three: keep it.**
The cycle limit is reached, so this is the cycle that ships.

- **No blocker.**
- **The article can switch onto this template once High 1 is fixed** and a capture at 1440 confirms it. High 1 is a two-declaration Custom CSS
  edit to `products` and needs no further critic cycle.
- The Medium findings can follow on the live template.

| Axis (sibling set) | Cycle 1 | Cycle 2 | Cycle 3 |
| ------------------ | ------- | ------- | ------- |
| Hierarchy          | 6.0     | 6.3     | 6.4     |
| Rhythm             | 5.5     | 6.0     | 6.1     |
| Imagery            | 6.0     | 6.5     | 6.5     |
| Typography         | 6.0     | 6.0     | 6.6     |
| Family fit         | 7.0     | 7.0     | 7.0     |
| Mobile             | 6.5     | 6.8     | 7.0     |

| Rubric axis (weight) | Cycle 1 | Cycle 2 | Cycle 3 |
| -------------------- | ------- | ------- | ------- |
| Design (40%)         | 6.0     | 6.4     | 6.6     |
| Usability (30%)      | 6.8     | 7.0     | 7.2     |
| Creativity (20%)     | 4.5     | 4.5     | 4.5     |
| Content (10%)        | 7.5     | 7.5     | 7.5     |
| **Weighted**         | 6.1     | 6.3     | **6.5** |

Usability scores are for human check: vision judges are unreliable on that axis.

## What changed after cycle 2, checked on the live page

| Claimed change                   | Verdict                                       | Evidence                                                                                 |
| -------------------------------- | --------------------------------------------- | ---------------------------------------------------------------------------------------- |
| H1: `sperm` ground painted white | **Fixed**                                     | Ground 255,255,255 at x 20, x 720 and below the card; card 240,240,240, now with an edge |
| H2: `names`/`work` text on 32rem | **Fixed at 1440**                             | Paragraphs at x 464, 512 px wide; 68 and 67–71 characters a line (cycle 2: 110+)         |
| H2: `names`/`work` H2 size clamp | **Fixed at 1440, new fault at 768**           | 37.4 px at 1440; **28 px at 768**, other H2s 38 px (Medium 1)                            |
| H2: inline table rules           | **Half applied**                              | Rows stack at 390, but `td{border:0;padding:2px 0}` loses to the section CSS (Nit)       |
| M4: one 32rem axis               | **Mostly fixed**                              | Prose at 61–74 characters a line at 1440 (cycle 2: 78–87); `legal` peaks at 74           |
| M4: `avoid` icons on the axis    | **Done**                                      | Two columns at x 464 and x 740                                                           |
| M3: shop CTA in #9E4F5C          | **Works at 390 and 768, broken from 1150 px** | 1440: 142 × 154 px, five lines, at x 1180 (High 1)                                       |
| M3: centred two-up products      | **Done**                                      | Tiles span x 272–1168 at 1440 (cycle 2: 48–708)                                          |
| Figure labels scale              | **Done**                                      | Numbers 32.5 px at 390 and 28 px at 195; captions 16 px under 700 px                     |

## Blockers

- None.

## High

- **H1. From 1150 px up, the page's only call to action renders as a five-line pill outside the reading column** (interaction/hierarchy).
  - **Measured at 1440:** the link is 142 × 154 px at x 1180, and "Shop / the / PDRN / Renewal / Serum" wraps one word per line. It sits right of
    the 512 px header box, which spans x 464–976, and the intro paragraph overflows that box to 700 px.
  - **Cause:** at `min-width:1150px` the theme sets `.section-header{grid-template-columns:700px}` and
    `.section-header>.text-with-icon{grid-column-start:2}`. Capping the header at 32rem leaves the second column almost no room. At 390 and 768
    the button is fine: 293 × 56 and 308 × 58 px.
  - **Why it matters:** this is the conversion moment on every laptop and desktop, and it is the first thing a director's eye snags on in that
    screen. See the "1440: CTA" crop on the contact sheet.
  - **Spec fix (`products.custom_css`):**
    - add `grid-template-columns:minmax(0,1fr)` to the existing `.section-header{…}` rule;
    - add `grid-column-start:1` to the existing `.section-header>a{…}` rule;
    - delete the two `.prose h2,p.h2` rules. `products` has no H2, so they are dead, and deleting them keeps the section near 380 of 500
      characters.
    - Confirm with a capture at 1440.

## Medium

- **M1. Between 700 and about 1,460 px, the evidence H2s are smaller than every other H2** (typography).
  - **Measured at 768:** the `names` and `work` H2s are 28 px; `serum`, `safety`, `legal`, `facial`, `label` and `related` are 38 px. The proof
    title is 32 px. `clamp(28px,2.6vw,38px)` reaches 38 px only at 1,462 px wide.
  - **Why it matters:** the section that carries the evidence is demoted on tablets and small laptops (see the "768" crop).
  - **Spec fix (`names` and `work`):** replace `h2{font-size:clamp(28px,2.6vw,38px)}` with the pair every other section uses:
    `.prose h2{font-size:28px}` and `@media screen and (min-width:700px){.prose h2{font-size:38px}}`. Both sections end near 373 characters.
- **M2. The three-column `names` table spans 1,344 px for cells of one to six words** (layout/spacing).
  - **Measured at 1440:** the columns start at x 48, 540 and 1,170, so a row reads across about 1,120 px of grey. The five-column `work` table
    earns that width; this one does not.
  - **Spec fix (`names` only):** change `.sgt{max-width:100%;overflow:auto}` to `.sgt{max-width:48rem;margin-inline:auto;overflow:auto}`.
- **M3. Safety, avoid and legal form the longest single-ground run on the page** (layout/spacing).
  - **Measured:** 461 + 638 + 476 = 1,575 px of #F0F0F0 at 1440, up from about 1,120 px in cycle 2, because the two-column icon list on the axis
    made `avoid` taller. It is 1,630 px at 390.
  - **Why it matters:** three sections share one ground and one padding and carry no image. The legal question sits inside the slab, held apart
    only by a 72 px margin hack. This breaks rule 23 ("no adjacent sections with the same padding token and background").
  - **Spec fix:**
    - keep `legal` on #F0F0F0 with only its `close` block (the patch-test line, which belongs to safety);
    - move the `law` block into a new rich-text section `law` after it, on #FFFFFF, with the same 32rem rules;
    - drop `.prose h2{margin-top:72px}`.
- **M4. H2s sit on three left edges, 416 px apart** (layout/spacing).
  - **Measured at 1440:** H2s start at x 48 (`facial`, `label`, `related`), x 464 (`names`, `work`, `serum`, `safety`, `legal`) and x 812 (the
    `sperm` and `proof` cards).
  - **Why it matters:** the multi-column section heads keep the container edge while every prose head moved to the axis, so the eye re-finds the
    start of each section.
  - **Spec fix (`facial`, `label`, `related`):** add
    `.section-header{max-width:32rem;margin-inline:auto;width:100%;grid-template-columns:minmax(0,1fr)}`. The last declaration avoids High 1's
    700 px column trap. Leave the card grids full width, which matches how the tables now break out under axis H2s.
- **M5. Equal weight, unchanged** (layout/spacing).
  - **Measured:** 12 of the 16 content sections are 80/80 at 1440 and 40/40 at 390. `prices`, `avoid` and `legal` have 0 top padding. That is two
    values; rule 23 asks for three or more. `measure.py` reports 1 because it reads the outer wrappers.
  - The evidence section gets the same room as the label checklist.
  - **Spec fix (`work`):** add `@media screen and (min-width:1000px){.section{padding-block:120px}}`. The section stays under 500 characters
    with M1 applied.
- **M6. Swipe strips at 768, unchanged** (interaction, for human check).
  - **Measured scroll widths inside a 768 px viewport:** `facial` 1,035, `label` 1,375 and `related` 1,375. The third card is cut at the edge,
    with no control.
  - **Spec fix:**
    - `facial`: add `@media screen and (min-width:700px) and (max-width:999px){.multi-column{grid:auto/repeat(3,minmax(0,1fr))}}`;
    - `label` and `related`: the same rule with `repeat(2,…)`.
- **M7. At 200% zoom the two cards set 9 to 14 characters a line, and H2s break mid-word** (typography, for human check).
  - **Measured at 195 px:** the `sperm` and `proof` card text is 91 px wide, at 9–14 characters a line.
  - H2s split mid-word: "skincar|e" in the `sperm` card, "polynucleoti|des" in `names`, "microneedlin|g" in `facial` (see the "zoom" crop).
  - This breaks rule 54.
  - **Spec fix:**
    - `sperm`: add `@media screen and (max-width:320px){.media-with-text{--media-with-text-content-padding:16px}.prose h2{font-size:22px}}`;
    - `proof`: add `@media screen and (max-width:320px){.rba__text{padding:20px 16px!important}}`;
    - `names`, `work`, `facial` and `label`: add a 22 px H2 at 320 px or narrower, as the banner already does for its H1.
- **M8. The second screen is weaker than the sibling's** (hierarchy).
  - **Our page:** "The short answers:" is a bold paragraph on grey, not a heading. There is no product and no action until y 8,147 of 10,374 at
    1440 (79% down) and y 10,876 of 14,761 at 390 (74%).
  - **The Argireline sibling:** its second screen carries an H2 "The short answers", the product photograph and "Shop the Peptide Duo Set".
  - **Spec fix (`answers.short`):** open with `<h2>The short answers</h2>` instead of `<p><strong>The short answers:</strong></p>`. This is an
    English-first copy change, so the locales follow later.
- **M9. No chart: the central number exists only as text, unchanged** (imagery).
  - "23.0% vs 6.6%" appears as a figure, a table cell and "up to 23%". The hub and the Ye page both carry rose-against-grey bars.
  - **Spec fix:** copy the Ye study template's chart section ("How much each side improved in 28 days") into this template after `work`, cut to
    two rows: crow's-feet area 23.0 / 6.6 and eye-bag volume 14.8 / 10.2. This is the only signature candidate the page has.
- **M10. Repetition and the phone image run, unchanged** (copy/imagery).
  - **Repetition:**
    - the captions of figures `s1` and `s3` repeat short answers 1 and 2 word for word;
    - the `s2` caption repeats the `work` table's evidence cell, "The 31-woman split-face trial (Ye 2026): 0.1% PDRN eye cream vs 0.1%
      retinol, 28 days, no placebo";
    - "no placebo" appears 5 times.
  - **Image run at 390:** `facial` (1,786 px) and `related` (2,380 px) are 4,166 px, 28% of the 14,761 px page.
  - **Spec fix:**
    - give `s1` and `s3` captions a new fact each, and drop "no placebo" from `s2` and the `work` intro;
    - set `related.stack_on_mobile` to false, which makes one swipe row at 390 and saves about 1,800 px.
- **M11. The before/after picture reads as a bigger change than its heading's number** (copy/imagery, for Malcolm).
  - The card heading says "What a 14.8% smaller eye bag looks like". In the pair, the bags look close to gone, under different light, a different
    wall and a different expression.
  - Register row 5 limits this claim to "the look of puffiness", at ingredient level.
  - This is not the decided pill and not a disclosure point. It is whether the picture is sized to the number.
  - **Options for Malcolm:** retitle the card so the picture is not pegged to 14.8%, or use a subtler pair.

## Nits

- **The middle figure wraps at 768** (typography). "23.0% vs 6.6%" splits onto two lines: 88 px tall in a 213 px column, because the theme sets
  `break-all` on it. Fix: in `figures`, add `@media screen and (min-width:700px) and (max-width:999px){.impact-text__text{font-size:32px!important}}`.
- **The heading outline opens with three numbers** (interaction, for human check). The theme hard-codes `<h2 class="impact-text__text">`, so the
  outline after the H1 reads "0", "23.0% vs 6.6%", "3". This cannot be fixed in the spec: accept it, or ask Malcolm about an additive theme copy.
- **Stacked tables at 390 rule every cell** (layout/spacing). The section-scoped `.sgt :is(th,td){border-bottom…;padding:10px}` outranks the
  inline `td{border:0;padding:2px 0}`, so `work` shows 15 cell hairlines plus 3 heavy row rules, with a 10 px inset. Fix: in both inline
  `<style>` blocks, write `.sgt td{border:0!important;padding:2px 0!important}`. The liquid block has no 500-character limit.
- **Links are still in two colours** (colour). They are rose in `answers` and ink #1A1A1A in `figures`, `work`, `products` and `related`. Fix: add
  `.prose a{color:#9E4F5C}` to those sections.
- **The "Learn" kicker** (copy). It sits above the H1 as a plain `<p>`, not a link (rule 44). This is a family pattern.
- **The H1 is in Title Case** (copy). The sibling uses sentence case (rule 45).
- **The icon grid is off the axis at 768** (layout/spacing). `avoid` starts at x 120 while the text axis is at x 128.
- **Two heads for one block** (hierarchy). The `serum` intro ends about 166 px above the proof card it introduces, and that card carries its own
  subheading and H3.
- **Radius count** (layout/spacing). Six radius values in `main` (5, 6, 10, 20 and 60 px, and pill), against rule 29's three or fewer. Most come
  from the theme.
- **Site-wide, not scored:**
  - the footer is 25 px too wide at 200% zoom;
  - the Menu control is 22 × 22 px, and the drawer links are 29 px tall (the menu opens, hit-tests and closes on Escape);
  - the Klaviyo pop-up at 200% zoom is 107 px too wide, with its close control off screen (unblocked pass, for human check);
  - the page weighs 2,334 KB at 1440 and 2,728 KB at 390, with 839 and 1,270 KB of script (rule 53);
  - body text is 15 px (14 px at 390), which is Malcolm's setting, so displayToBody of 4.0 and 2.86 is noted, not scored.

**Decided, noted only:**

- The pill on the eye-bag picture is 10.9 px at 390, and so are the Before and After labels. At 200% zoom the pill wraps to three lines, 48 px
  tall, over the chin.
- The Ye study page's own label is Malcolm's call.

## Reference diff

- **PDRN hub:** ours is weaker in the ask and the evidence.
  - The hub pairs "Shop PDRN Renewal Serum" with a product image and shows a chart; ours has neither near its evidence.
  - The hub uses three padding values (0, 64 and 80 px); ours uses two.
- **Ye 2026 study page:** ours is weaker in signature. The Ye page's bar chart is the thing a reader remembers; ours states the same numbers in
  prose three times.
- **Argireline sibling:** ours is weaker at the second screen and in imagery.
  - The sibling opens on a headed short-answer card with the product and the button. Ours opens on a bold label in grey.
  - The sibling shows three before/after pairs; ours shows one.
- **Reference rules:** this project has no `02-reference-rules.md`, so there are no "ten rules for this site" to check against.

## Answers

- **Signature:** none. The "0 sperm cells in the bottle" figure is still the candidate, and it is still the first of three equal numbers.
- **Three tells of assembly:**
  - one 80 px padding on 12 sections;
  - a symmetric three-up grid of square images (`facial`) and a four-up grid (`related`) as primary sections;
  - a CTA forced into a header slot the theme never designed for it, which is why it breaks at 1150 px.
- **Convergence cluster:** none cleanly. The page leans toward cluster 4: 11 surfaces at a 10 px radius on a grey ground, with square images.
- **Weighted total and disposition:** 6.5, FIX. The cycle limit is reached, so this cycle (the best of three) ships.
- **Single change that most improves the page:** High 1, the `products` header grid. It takes two declarations and minutes, and it repairs the
  only call to action on every screen 1150 px or wider. After that, M9 (the chart) adds the most, at a medium cost: one copied section and a
  capture.

## Files

Captures, probes and measurements are in the session scratchpad (not committed):
`/private/tmp/claude-501/-Users-malcolmsmith-Claude-Code-Projects-skingenetix-website/4237e530-0fcc-4ba5-85dd-7427c7f586ff/scratchpad/critic3/`.

- `shots/`: blocked captures at four widths, slices, menu frames and the proof crop.
- `ref/`: the three references at 1440 and 390.
- `measure-1440.json` and `measure-390.json`.
- `probe.json`: line lengths, headings, links and CTA geometry at four widths.
- `cap/` and `cap2/`: the unblocked `capture.py` runs.

The contact sheet is `~/Desktop/learn-salmon-cycle3-renders.png`. This project has no `09-critique/scores.csv`; the score table above records the
cycle.
