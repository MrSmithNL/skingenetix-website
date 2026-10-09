# Design critic, cycle 2: Learn article "Copper uglies" redesign (2026-10-09)

**Page:** `/blogs/learn/copper-uglies-what-they-are-and-how-long-they-last?view=learn-copper-uglies` (hidden preview of
`templates/article.learn-copper-uglies.json`, spec `configs/hub-upgrades/learn-copper-uglies-design-2026-10-09.json`).
**Critic:** `design-critic` agent, fresh context. Captured live on 2026-10-09 at 390, 768, 1440 and 200% zoom (195 px), with
Klaviyo and Shopify Forms blocked and the cookie banner hidden; `capture.py --zoom` was also run unblocked. `measure.py` was run at
1440 and 390. Reference diff against the copper hub and the Badenhorst study article (captures from today).

**No direction contract exists** (no `website/design/`, no `02-reference-rules.md`), so the page is judged, as in cycle 1, against
the reference family, the skill's craft rules and the store rules in memory.

**Disposition: FIX** (weighted **5.9**, up from 5.3). **This cycle improves on cycle 1 and is the one to keep.** Do not switch the
article onto this template until B1 and H1 below are fixed. Both are small. Then run cycle 3 as the last one.

| Axis                        | Weight | Cycle 1 | Cycle 2 |
| --------------------------- | ------ | ------- | ------- |
| Design                      | 40%    | 5.4     | 6.2     |
| Usability (for human check) | 30%    | 5.5     | 6.0     |
| Creativity                  | 20%    | 4.0     | 4.5     |
| Content                     | 10%    | 7.0     | 7.0     |
| **Weighted**                |        | **5.3** | **5.9** |

## Status of the cycle-1 items

| Cycle-1 item               | Status                      | Evidence today                                                                                                   |
| -------------------------- | --------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| B1 amber cream image       | **Partly fixed**            | The picture is right: a clear gel leaving a dropper, on palette. The alt text now names our serum (see B1 below) |
| B2 table overflow at 200%  | **Fixed, with a new fault** | Table scrollWidth 155 = clientWidth at 195. The stacked cells are half-width (see H1 below)                      |
| H1 figures outranked       | **Fixed at 1440 and 390**   | Figures 44 / H2 38 at 1440; 32.5 / 28 at 390. Two leftovers: the FAQ heading (M8) and 200% zoom (M4)             |
| H2 four left edges         | **Open**                    | Six x positions now (H2 below)                                                                                   |
| H3 lone product card       | **Partly fixed**            | Three products in the row; still no button anywhere in `main` (now M1)                                           |
| H4 grey bands on the tile  | **Fixed**                   | All three tile anchors 416×416 over 416×416 images                                                               |
| M1 line length             | Open                        | `measureCh` 76; probe 78 to 84 characters at 1440; banner subline 104                                            |
| M2 equal weight            | Open                        | 13 of 18 sections open at exactly 80 px                                                                          |
| M3 icon rows repeat        | Open                        | Unchanged; 1,958 px of 12,415 at 390                                                                             |
| M4 200% zoom breaks        | Open                        | Figures 19.5 px under 20 px labels; "guesswor / k"                                                               |
| M5 pipette behind the type | Open                        | Unchanged at 1440                                                                                                |
| M6 body 15 / 14 px         | Open                        | Theme-wide; Malcolm's decision                                                                                   |
| M7 repeated facts          | Open                        | Intro still repeats the "39 of 40" label directly under it                                                       |
| Nits                       | Mostly open                 | Eyebrow, ink-coloured figure links, tablet swipe strip and radii unchanged; filename alt replaced (B1)           |

## Blockers

**B1. The purging image's alt text names our serum, directly beside "What causes copper uglies".** Classes: copy, imagery.

- **Where:** the purging section, left image (648×727 at 1440; full-width 390×390 at 390). The section's two H2s are "Copper
  uglies vs purging" and "What causes copper uglies: what is known and what is guesswork".
- **Measured:** the alt reads "Skingenetix Copper Peptide (GHK-Cu) 2% Renewal Serum, 30ml - macro of the pipette tip with a drop
  of the blue serum". It is the file's product alt text, carried into the article.
- **Why it matters:** a screen reader and an AI extractor read our product's name as the picture for "what causes copper uglies".
  The article's own key line is "the result belongs to that serum, not to ours". This is the same image-makes-a-claim fault cycle 1
  blocked on, moved from the night cream to the serum. The alt also says "blue serum" over a clear drop.
- **Fix:** a neutral alt such as "A clear gel drop leaving a glass dropper". If the file is also product media, change a renamed copy,
  not the product's own image.

## High

**H1. Under 330 px the stacked table keeps half-width cells, so the 200%-zoom reader gets one word per line and no column labels.**
Classes: interaction, layout. For human check.

- **Measured at 195 (390 at 200%):** each `td` is 77.5 px wide, about 50 px of text after padding. The table is 1,604 px tall, nearly
  four screens. At 320 the cells are 140 px of a 280 px column and the table is 1,076 px tall.
- **Where:** `zoom-sheet.png`, third column: "Seen / in / laboratory / cells / only;" and "1 of / 40 / women / in the / one".
- **Cause:** the section's Custom CSS is scoped `#shopify-section-…__online .sgx-evtable td{width:50%}` (specificity 1-1-1). It
  beats the liquid block's `.sgx-evtable td{width:100%}` (0-1-1), so `display:block` applies but the width does not.
- **Why it matters:** `thead` is hidden when stacked, so nothing labels which cell is the online claim and which is the measurement.
  At 320 the stacked form is strictly worse than the two-column table it replaces: the same 140 px cells, minus the headers.
- **B2 itself is fixed:** nothing in `main` passes the right edge at 195. The document still measures 220 at 195, but the cause is
  the site footer's 200 px newsletter form, which is sitewide (see Nits).

**H2. The headings start from six different left edges at 1440.** Class: layout. (Cycle-1 H2, open.)

- **Measured x positions:** 428 (six reading-column H2s), 728 (two purging H2s), 48 (the table, FAQ, related row and the product
  sentence), 80 (routine), and 481 for "What to do if your skin reacts". That last heading is centred (478 px wide) over items that
  start at x 48.
- **Where:** `s1440-3.png`. The table section still hugs the left gutter at 780 px with the right 45% of the screen empty, and the
  "What to do" heading floats centred above a left-aligned four-up row.
- **On the phone:** at 390 both icon-row headings are left-aligned at x 20 above centred items.

## Medium

- **M1. The commercial step is an unnamed grid** (cycle-1 H3, downgraded). Classes: layout, interaction. Three products fill three
  of four slots: x 48 to 1050 at 1440, with an empty 342 px slot on the right. At 390 they sit 2 + 1, with an orphan. `main` holds
  no `.button` or `<button>`. The lead-in sentence sits at x 48, off the reading column at x 428. The hub's 390 capture puts "Shop
  Copper Peptide" on a button about 1,800 px down. Whether a named button is still needed is now a conversion choice, not a blocker:
  the row does work as a step.
- **M2. Equal weight** (open). Class: layout/spacing. 13 of 18 sections open at exactly 80 px (DOM offset). `measure.py` reports
  `distinctSectionPaddings` 1. The two evidence moments (figures and table) get the same space as the injections paragraph.
- **M3. The two icon rows repeat each other** (open). Classes: copy, components. "If a reaction persists" repeats "Ask a pharmacist
  or dermatologist". The headset icon is used twice. At 390 the two rows stack nine centred items over 1,958 px of 12,415 (15.8%).
- **M4. The 200% zoom hierarchy inverts** (open). Class: typography. At 195 the figures are 19.5 px, under their 20 px labels and the
  28 px H2s. The purging H2 (28 px in a 131 px column, `overflow-wrap:anywhere`) still breaks as "guesswor / k".
- **M5. The banner pipette runs behind the title at 1440** (open). Class: imagery. The pipette (x about 680 to 760) crosses "Copper"
  and "and" in the H1, and runs on behind the subline and byline (`s1440-0.png`). The hub and Badenhorst banners keep the subject
  clear of the type.
- **M6. Body text is 15 px on desktop and 14 px on the phone** (open; theme-wide; Malcolm's decision). Class: typography. Craft rule 10.
- **M7. The intro repeats the figure** (open). Class: copy. "39 of 40 women tolerated a GHK-Cu serum for 8 weeks" is the figure
  label, and the very next sentence repeats it.
- **M8. The FAQ heading outranks the key figures** (new). Class: hierarchy. "Frequently asked questions" is 48 px against figures of
  44 at 1440, and 32 against 32.5 at 390. The `faq` section was left out of the 28/38 rule. It is a 48 px heading over two
  questions.
- **M9. In-prose H2s sit closer to the paragraph above than to their own text** (new). Class: typography. "What causes copper
  uglies" sits 24 px below the previous paragraph and 32 px above its own text. "Is it a real side effect?" is about 30 above and
  37 below (`s1440-1.png`). The headings bind upward.
- **M10. The accent is spent on furniture, not on an action** (new). Class: colour. #014EB1 appears about 22 times: 3 figures,
  3 body links, 6 list markers, 9 icons and the callout rule. No action carries it (craft rule 16).

## Nits

- **Eyebrow:** "Learn" still sits above the H1, unlinked. Badenhorst uses a breadcrumb (craft rule 44).
- **Link colour:** the three "Badenhorst 2016" links in the figures and the product-sentence link are ink (#1A1A1A), not #014EB1.
- **Short-answers card:** a 12 px rounded white box; Badenhorst's "At a glance" does the same job with hairline rows (craft rules 28, 42).
- **Tablet swipe strip:** at 768 the related row is a swipe strip, and the third card is cut at the edge with no scroll cue.
- **Radii:** six values in `main` (12, 9999, 10, 8, 6, 5 px), set by the theme.
- **Upscaling:** the purging image is drawn 648×727 from a 648×648 source (1.12×). The product images at 390 are drawn at 171 px
  from 155 px sources.
- **Skin-concerns tile:** a hand pressed to the cheek, under "Read the evidence" on a reactions page (human check).
- **Sitewide, not this template:** at 195 the footer newsletter form (200 px) pushes the document to 220. The header icons overlap
  the logo at 200%.

## Reference diff

- **Copper hub:** its banner is a dark lab scene with the subject clear of the type, and at 390 it reaches a shop button within about
  two screens. Ours has the pipette behind the H1 and has no button.
- **Badenhorst study:** a breadcrumb places the reader. "At a glance" uses hairlines, not a card. The verdict paragraph carries the
  page. Ours has an eyebrow, a rounded card, and puts its strongest idea (the online-vs-measured table) in a default grey table
  hugging the left gutter.

## Answers

- **Signature:** none. The online-vs-measured table is the candidate, but it is set at default weight, off the reading column.
  (Creativity 4.5.)
- **Three tells of assembly:**
  - one 80 px rhythm on 13 of 18 sections;
  - two icon-in-circle rows with a repeated item and a reused headset icon;
  - a product-name alt text on a mood image, plus a four-up product grid holding three.
- **Cluster:** 4, the theme kit: icon-in-circle rows, rounded white cards and one rhythm throughout.
- **Weighted 5.9, FIX.** It improves on cycle 1 (5.3), so cycle 2 is the cycle to keep.

**Loop note:** under the rubric, no contract and no signature is grounds to go back to the art director rather than iterate. That
applies to the whole Learn template family, not to this page. One more cycle (B1 and H1) will make this page shippable as the
ceiling of the stock-section template. Raising Creativity above about 5 needs a family-level direction from Malcolm, not cycle 4.

**Single change that most improves the page:** B1, the neutral alt text on the purging image. It is one field (or one renamed copy
of the file) and takes minutes. Next comes H1: the stacked cells need to win the specificity contest with the section's 50% rule,
which is about one selector.

No `scores.csv` was written, because no `website/design/` structure exists (as in cycle 1).
Captures and measurements (scratchpad, not committed):
`/private/tmp/claude-501/-Users-malcolmsmith-Claude-Code-Projects-skingenetix-website/4237e530-0fcc-4ba5-85dd-7427c7f586ff/scratchpad/cu2/`
(`page/` for the blocked captures, `probe.json` and `zoom-sheet.png`; `measure-1440.json`, `measure-390.json`, `refdiff-390.png`).
Contact sheet: `~/Desktop/learn-copper-cycle2-renders.png`.
