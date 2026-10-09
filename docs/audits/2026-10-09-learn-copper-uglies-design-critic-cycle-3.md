# Design critic, cycle 3: Learn article "Copper uglies" redesign (2026-10-09)

**Page:** `/blogs/learn/copper-uglies-what-they-are-and-how-long-they-last?view=learn-copper-uglies` (hidden preview of
`templates/article.learn-copper-uglies.json`, spec `configs/hub-upgrades/learn-copper-uglies-design-2026-10-09.json`).
**Critic:** `design-critic` agent, fresh context. Captured live on 2026-10-09 at 390, 768, 1440, 320 and 200% zoom (195 px).
Klaviyo and Shopify Forms were blocked, the cookie banner hidden, scrolling stepped and page loads spaced about 30 s apart.
`measure.py` was run at 1440 and 390. Extra probes:

- banner contrast with the type hidden;
- the button at six desktop widths;
- gaps around every H2;
- the mobile menu, open, with pop-ups blocked.

Reference diff against the live sibling (Argireline + Matrixyl 3000), the copper hub and the Badenhorst 2016 article, all captured
today.

**No direction contract exists, and the page has no signature** (stated in cycles 1 and 2). Whether the Learn family goes back to
the art director is Malcolm's decision, so this cycle judges the page on its own merits: against the reference family, the skill's
craft rules and the store rules in memory.

**Disposition: FIX** (weighted **6.1**, up from 5.9). **Cycle 3 is the best cycle and the one to keep.** This was the last
cycle. There is one new blocker (B1): the "Shop" button added in the cycle-2 fix renders as a five-line blob at every desktop
width from 1180 to 1920 px. The fix is two CSS rules in one section. Once B1 is fixed and the numbers given there are confirmed,
switch the article onto this template. No cycle 4 is needed. H1 and the Mediums do not block the switch.

| Axis                        | Weight | Cycle 1 | Cycle 2 | Cycle 3 |
| --------------------------- | ------ | ------- | ------- | ------- |
| Design                      | 40%    | 5.4     | 6.2     | 6.3     |
| Usability (for human check) | 30%    | 5.5     | 6.0     | 6.6     |
| Creativity                  | 20%    | 4.0     | 4.5     | 4.5     |
| Content                     | 10%    | 7.0     | 7.0     | 7.0     |
| **Weighted**                |        | **5.3** | **5.9** | **6.1** |

## Status of the cycle-2 items

| Cycle-2 item                | Status                  | Evidence today                                                                                     |
| --------------------------- | ----------------------- | -------------------------------------------------------------------------------------------------- |
| B1 alt names our serum      | **Fixed**               | A renamed copy of the file; the alt is now "A clear gel drop leaving a glass dropper"              |
| H1 half-width stacked cells | **Fixed**               | `td` full width (155 px at 195, 280 at 320); claim cell bold; table 956 px tall at 195 (was 1,604) |
| H2 six left edges           | **Mostly fixed**        | Nine H2s, the table and both icon rows at x 464; left: purging 728, routine 80, FAQ and related 48 |
| M1 no button                | **Replaced by B1**      | Button works at 390 (293×56), 768 and 1024 (308×58); broken from 1180 to 1920 (134×154)            |
| M2 equal weight             | Open                    | 13 of 18 sections open at exactly 80 px (40 at 390)                                                |
| M3 icon rows repeat         | Open                    | Unchanged; four of five icons in the second row are reused (M2 below)                              |
| M4 200% zoom hierarchy      | **Fixed, new flatness** | Figures 28 over 16 px labels; purging H2 22 px, unbroken; H1 = figures = H2 = 28 (M6)              |
| M5 pipette behind the type  | Open, **now High**      | Measured 1.4:1 at 1440 and 2.0:1 at 390 where it crosses the letters (H1 below)                    |
| M6 body 15 / 14 px          | Open                    | Theme-wide; Malcolm's decision; not scored                                                         |
| M7 intro repeats the figure | Open                    | Unchanged (M8 below)                                                                               |
| M8 FAQ heading 48 px        | **Fixed**               | 37.4 px at 1440, 28 at 390; 28 against 38 at 768 (Nits)                                            |
| M9 in-prose H2s bind upward | **Partly fixed**        | Purging 48 above / 32 below; basics still 16 / 32 (M4 below)                                       |
| M10 accent on furniture     | **Partly fixed**        | The button carries #014EB1, but about 40 other accent uses compete (M7 below)                      |
| Nits                        | Mostly open             | Figure links now #014EB1 (fixed); eyebrow, card, swipe strip and radii unchanged                   |

## Blockers

**B1. The new "Shop the Copper Peptide Serum" button renders as a 134×154 px blob, one word per line, outside the reading
axis, at every desktop width from 1180 to 1920 px.** Classes: interaction, layout.

- **Where:** the products section header (contact sheet B1; `s1440-5.png`). At 1440 the pill sits at x 1180 to 1314 with
  "Shop / the / Copper / Peptide / Serum" stacked. The lead-in beside it runs from x 464 to 1164.
- **Measured:** the 32rem rule works: the header is 512 px wide at x 464. But the theme lays the header out as a two-column grid
  (`grid-template-columns: 700px 134px`, `justify-content: space-between`). The prose keeps its 700 px track, the link gets what
  is left, and both spill 338 px past the header's right edge. The result is identical at 1180, 1280, 1366, 1440 and 1920 (button
  134×154 each time). At 1024, 768 and 390 the header stacks and the button is right (308×58, 308×58, 293×56).
- **Line length:** the lead-in runs 700 px, 93 characters a line, against a band of 50 to 70 (craft rule 10).
- **Why it matters:** this is the page's only primary action and its only filled accent, and it is the element the cycle-2 fix
  (M1, M10) added. A malformed button reads as a broken page. The live sibling's button renders at 263×58.
- **Fix (spec, `products` custom_css):** the section has no H2, so delete its two H2 size rules. Then add
  `.section-header{grid-template-columns:minmax(0,1fr);justify-items:start}` and `.section-header .prose{width:auto}`. That
  comes to about 430 of the 500 characters. Verify at 1180, 1440 and 1920:
  - the button is no more than 60 px tall;
  - at 1440, the button and the lead-in sit inside x 464 to 976;
  - the lead-in is no more than 70 characters a line.

## High

**H1. The banner's pipette runs behind the H1 at every width. Where it crosses the letters, contrast falls to 1.4:1 at 1440
and 2.0:1 at 390.** Classes: imagery, colour/contrast. This was M5 in cycles 1 and 2; it is raised now that it is measured.
For human check.

- **Where:** the first screen (contact sheet A1, A3).
  - **At 1440:** the type block starts at x 612, and the pipette runs through it at about x 680 to 760, crossing "Copper", "and",
    the subline and the byline. The left 612 px of the banner is empty blue.
  - **At 390:** the centred H1 sits directly over the centred pipette ("Uglies", "They", "Last").
- **Measured:** the type was hidden and the background sampled under each text box. Median contrast is 9.4:1 at 1440 and 10.8:1
  at 390. At the lightest pixels under the text it falls to:
  - 1.38:1 under the H1 and 1.39:1 under the subline at 1440;
  - 1.97:1 under the H1 and 1.95:1 under "Learn" at 390.

  Large text needs 3:1. Craft rule 33 asks for the scrim to be measured at the image's extremes.

- **Reference:** the sibling, the hub and Badenhorst all keep the subject clear of the type at both widths. This is the only page
  in the family with its subject behind the headline.
- **Fix (spec, `banner`):** a master with the pipette in the left fifth (the store's widened-master recipe, about 4.4:1), plus a
  phone crop in which the drop ends above or beside the H1.
  - **Interim, desktop:** add `@media (min-width:1000px)` and cap the banner's text wrapper at `calc(50vw - 120px)`. Every line
    then starts at 50vw + 72 px, right of the pipette's edge at about 50vw + 40 px.
  - **Phone:** this needs the new crop. A scrim dark enough to pass would turn the banner near-black.

## Medium

- **M1. Equal weight** (open). Class: layout/spacing.
  - **Measured:** 13 of 18 sections open at exactly 80 px at 1440 (40 at 390). `measure.py` reports `distinctSectionPaddings` 1,
    because it reads the Shopify wrappers at 0.
  - **Why:** the figures and the online-vs-measured table get the same room as the 128 px acne note.
  - **Fix (spec):** set the section spacing per section in custom CSS. For example, from 700 px up, give `figures` and `online`
    128 px top and bottom and give `duration` and `injections` 56 px, so the page has three values. Confirm which wrapper carries
    the padding before applying it.
- **M2. The two icon rows repeat each other** (open). Classes: copy, components.
  - **Repeated icons:** four of the five icons in "Before you try" are reused from "What to do", with different meanings:
    - the stop sign is "Stop the product" and also "Broken skin and eyes";
    - the tick is "Keep the rest of your routine plain" and also "Patch-test first";
    - the timer and the headset are reused too.
  - **Repeated copy:** "If a reaction persists" repeats "Ask a pharmacist or dermatologist".
  - **Size:** at 390 the two rows take 1,958 px of 12,412 (15.8%).
  - **Fix (spec):** delete `safety.s5` and set `icon: none` on the `safety` items, or make that row a rich-text list with
    hairline rows (craft rules 28, 42). This also removes five accent SVGs.
- **M3. The products leave an orphan below 1000 px.** Class: layout. For human check.
  - **At 768 and 390:** the three products sit 2 + 1, with an empty slot to the right of the third.
  - **At 200% zoom:** the cards are 74 px wide and the titles wrap to seven lines ("Copper / Peptide / (GHK- / Cu) 2% / Day /
    Gel- / Cream").
  - **Fix (spec):** `stack_products: false` with `show_progress_bar: true`. The phone then gets a scroller with a visible cue
    and the desktop keeps the three-up grid.
- **M4. One in-prose H2 still binds upward.** Class: typography.
  - **Measured:** "Is it a real side effect? What the one trial recorded" sits 16 px below the paragraph above and 32 px above its
    own text. The purging section is fixed (48 / 32).
  - **Fix (spec, `basics` custom_css):** `.prose>div+div h2:first-child{margin-top:32px}`. That gives 16 + 32 = 48, matching
    the purging section.
- **M5. The related card titles almost equal the section heading** (not raised in cycle 2). Class: hierarchy.
  - **Measured:** "The Badenhorst 2016 trial", "Copper peptide research" and "Skin concerns" render as `<p class="h3">` at 36 px,
    under "Read the evidence" at 38. At 768 it is 32 under 38; at 390, 24 under 28.
  - **Semantics:** the `heading_tag: h3` setting does not make them headings.
  - **Fix (spec, `related` custom_css):** `p.h3{font-size:24px}`, and 20 px below 700.
- **M6. The type ladder flattens at 320 px and at 200% zoom.** Class: typography.
  - **Measured:** the H1, the three figures and every reading-column H2 are all 28 px; the purging H2s are 22. The cycle-2
    inversion is gone (figures 28 over 16 px labels), but now nothing outranks anything.
  - **Also:** display-to-body at 390 is 2.86 (`measure.py`), under craft rule 4's 3×.
  - **Fix (spec):** raise the two existing 320 px rules: the H1 to 36 px (`banner`) and the figures to 32 px (`figures`).
- **M7. The accent is still spent before the action.** Class: colour.
  - **Measured:** the button now carries #014EB1, but the probe counts about 40 accent uses:
    - 13 text runs (3 figures, 7 links, 3 product titles);
    - 6 list markers;
    - the callout rule and the button fill;
    - 18 accent SVGs, the nine row icons among them.

    Craft rule 16 budgets three or four.

  - **Fix (spec):** set `icon_color: #1A1A1A` on the nine icon-row items and delete the two `li::marker` accent rules (`answers`,
    `basics`). That leaves the figures, the links, the callout rule and the button.

- **M8. The intro repeats the figures** (open). Class: copy.
  - **Repeated facts:** "The best evidence we have is one controlled facial trial" appears in figure 1 and again as the intro's
    opening words. "39 of 40 women tolerated a GHK-Cu serum for 8 weeks" is figure 2's label and the intro's next clause, about
    300 px below.
  - **Fix (spec, `answers.intro`, needs copy approval):** keep only the research-page link sentence and the skin-concerns
    sentence.
- **M9. Body text is 15 px on desktop and 14 px on the phone** (open). Class: typography.
  - **Status:** theme-wide and Malcolm's decision, so it is not scored. Craft rule 10.

## Nits

- **Eyebrow:** "Learn" still sits above the H1 (craft rule 44). Badenhorst uses a breadcrumb.
- **Short-answers card:** a 12 px rounded white box where hairline rows would do (craft rules 28, 42).
- **Tablet swipe strip:** at 768 the related row is a swipe strip, and the third card is cut at the edge ("Skir") with no scroll
  cue.
- **Radii:** seven values in `main` (12, 9999, 60, 10, 8, 6, 5 px). The new 60 px button adds one (craft rule 29).
- **FAQ heading at 768:** 28 px against 38 for every other H2, because its `clamp(28px,2.6vw,38px)` hits the floor there. Use the
  page's 28 / 38 pair.
- **Axis at the end of the page:** the FAQ and "Read the evidence" leave the 464 axis for x 48 (theme layouts).
- **Upscaling:** the purging image is drawn 648×841 from a 648×648 source (1.30×, up from 1.12×, because the text column grew).
  At 390 the related tiles are drawn at 350 px from 244 px sources at DPR 1.
- **Banner file name:** `skingenetix-copper-peptide-ghk-cu-pipette-droplet-matrixyl-comparison-study.jpg` names a Matrixyl
  comparison on a copper uglies page (Rule 27 check C, descriptive filenames).
- **Stacked table:** under 330 px the table drops its column labels. The bold claim in quote marks carries the meaning, so this is
  acceptable.
- **Skin-concerns tile:** its alt text ends in brand wording ("Skingenetix skin repair and renewal ..."). It sits on a tile, not
  beside a claim, but it is the same class of fault as cycle-2 B1.
- **Page weight:** 2,170 KB at 1440 (841 KB of script), against the 1,500 KB budget (craft rule 53). Theme-wide.
- **Sitewide, not this template:**
  - the menu toggle is 22×22 px;
  - at 200% zoom the newsletter pop-up (in the unblocked skill capture) overflows the viewport, with no visible close button;
  - at 195 the footer newsletter form pushes the document to 220 px;
  - the header icons overlap the logo at 200%.

  With pop-ups blocked, the mobile menu opens cleanly.

## Reference diff

- **Live sibling (Argireline + Matrixyl 3000):**
  - **The sibling:** its banner keeps the subject left of the type. Its first scroll pairs a product photograph with the short
    answers and a working 263×58 button. Before/after pairs and a three-image how-to row then vary the density down the page.
  - **Ours is weaker:** its only commercial moment is 75% of the way down, behind a broken button. Between the banner and the
    products it is one text column with two images and two icon rows. The brief rules out before/after images here, so some of
    that gap is by design.
- **Copper hub:** subject on the right, type on the left, clear of each other; it reaches "Shop" early on the phone. Ours keeps the
  pipette behind the H1.
- **Badenhorst study:**
  - **The study page:** a breadcrumb places the reader, "At a glance" uses hairline rows, and the verdict carries the page.
  - **Ours:** it keeps the eyebrow and the rounded card. But the online-vs-measured table now sits on the reading axis in hairline
    rows, which closes most of the gap the cycle-2 diff named.

## Answers

- **Signature:** none. The online-vs-measured table is better set (on the axis, in hairline rows) but still at default weight.
  (Creativity 4.5.)
- **Three tells of assembly:**
  - one 80 px rhythm on 13 of 18 sections;
  - two icon-in-circle rows that reuse four of five icons;
  - a theme section-header link forced into a 134 px pill.
- **Cluster:** 4, the theme kit.
- **Weighted 6.1, FIX.** It beats cycle 2 (5.9) and cycle 1 (5.3), so cycle 3 is the one to keep.

**Loop note:** this was the third and last cycle.

- **What to ship:** cycle 3, the best-scoring cycle, once B1 is fixed and confirmed against the numbers in B1. Do not open
  cycle 4.
- **What can follow:** H1 needs a new banner image. The Mediums are one or two spec edits each and can follow on the live
  template.
- **The ceiling:** the page now sits at the limit of the stock-section template. Creativity above about 5 needs a family-level
  direction, which is Malcolm's art-director question, not another cycle.

**Single change that most improves the page:** B1. Two CSS rules in the products section stack the header so the button renders
as a button. It takes minutes, plus one probe at 1180, 1440 and 1920 to confirm. Next comes H1, which costs one new banner image
and a phone crop.

No `scores.csv` was written, because no `website/design/` structure exists (as in cycles 1 and 2).

**Captures and measurements** (scratchpad, not committed):
`/private/tmp/claude-501/-Users-malcolmsmith-Claude-Code-Projects-skingenetix-website/4237e530-0fcc-4ba5-85dd-7427c7f586ff/scratchpad/cu3/`

- `page/`: the blocked captures, `probe.json` and `probe2.json` (banner contrast, H2 gaps, button at six widths) and
  `menu-open-390.png`;
- `measure-1440.json` and `measure-390.json`;
- `refs/`: `refdiff-390.png`, `refdiff-1440.png` and `ours-vs-sibling-*.png`;
- `skillcap/`: the unblocked `capture.py --menu --zoom` run.

**Contact sheet:** `~/Desktop/learn-copper-cycle3-renders.png`.
