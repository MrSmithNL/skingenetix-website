# Design critic, cycle 2: Learn article redesign, salmon sperm skin care (2026-10-09)

**Page:** `/blogs/learn/salmon-sperm-skincare-vs-the-salmon-sperm-facial?view=learn-salmon-sperm-skin-care` (hidden preview of
`templates/article.learn-salmon-sperm-skin-care.json`, spec `configs/hub-upgrades/learn-salmon-sperm-skin-care-design-2026-10-09.json`).
**Critic:** `design-critic` agent, fresh context. Captured live on 2026-10-09 at 390, 768, 1440 and 200% zoom (195 px), with Klaviyo, Shopify Forms
and the cookie dialog blocked, and loads spaced about 30 s apart. I also ran an unblocked `capture.py` pass, `measure.py` at 1440 and 390, DOM
probes at 1440/768/390/320/195 (characters per line counted from line boxes, section padding, scroll strips), and pixel samples of each section's
ground. A `curl` of the served HTML confirmed the cycle-2 labels are live. The references are the PDRN hub and the Ye 2026 study page (cycle-1
captures from today). There is still no direction contract for this site (there is no `website/design/`), so the page is judged against the
reference family, the skill's craft rules, the PDRN claims register and the store rules in memory.

**Disposition: FIX** (weighted **6.3**, up from 6.1). This revision improves on cycle 1, so keep it. **No blocker is left on this page.** Two of the
cycle-1 fixes did not take effect on the live page (High 1 and High 2), and the page should not switch until they are applied and confirmed by a
capture. Then run cycle 3, the last one.

| Axis (sibling cycle-1 set) | Cycle 1 | Cycle 2 |
| -------------------------- | ------- | ------- |
| Hierarchy                  | 6.0     | 6.3     |
| Rhythm                     | 5.5     | 6.0     |
| Imagery                    | 6.0     | 6.5     |
| Typography                 | 6.0     | 6.0     |
| Family fit                 | 7.0     | 7.0     |
| Mobile                     | 6.5     | 6.8     |

Rubric axes: Design 6.4 (40%), Usability 7.0 (30%, for human check), Creativity 4.5 (20%), Content 7.5 (10%) = **6.3**
(cycle 1: 6.0 / 6.8 / 4.5 / 7.5 = 6.1).

## Cycle-1 items: status

| Cycle-1 item                                   | Status                                     | Evidence (cycle 2)                                                                                                                                                                                                                                                                                                                                                                                                                            |
| ---------------------------------------------- | ------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| B1 Before/after reads as a Ye trial photograph | **Resolved on this page, with a residual** | The eyebrow "Eye bags, Ye 2026 eye-cream trial" and "After 28 days" are gone. Live labels: "What a 14.8% smaller eye bag looks like", "Before", "After", pill "Ye 2026, PDRN side: −14.8% (retinol side −10.2%)". The card now reads as a picture of the size of the change. Residual: Medium 1. The Ye study page still serves "After 28 days" (3 matches in its HTML), so the same picture keeps its trial label one click away (Medium 2). |
| H2 Bone runs, invisible evidence card          | **Half fixed**                             | `proof` is white (sampled 255,255,255) and its bone text card now has an edge. `serum` and `proof` read as one white block of 1,185 px. The second bone run is down from 2,007 to 1,120 px at 1440 (2,494 to 1,631 at 390). **`sperm` still renders bone** (sampled 240,240,240 edge to edge), so the first run is unchanged: `answers`, `sperm` and `names` run for 1,900 px at 1440 (2,302 at 390). See High 1.                             |
| H3 Equal weight, 16 px above the legal H2      | **Partly fixed**                           | The legal H2 now has 72 px above it (computed `margin-top` 72px). `prices` has 0 top padding and hangs off the routes row. `work` is still 80/80 (the 120 px was not applied). 12 of the 15 content sections are 80/80 at 1440 (40/40 at 390), and only two padding values exist (rule 23 asks for 3 or more). `measure.py` reports 1 because it reads the outer wrapper.                                                                     |
| H4 Three left edges, 104-character lines       | **Not fixed in `names` and `work`**        | Counted from line boxes at 1440: `names` 110 median (117 max), `work` 112 median (116 max). The `.prose>p` rule matches nothing (High 2). The left edge still changes 10 times down the page (11 in cycle 1).                                                                                                                                                                                                                                 |
| M5 No chart                                    | **Not done**                               | The page still has no chart.                                                                                                                                                                                                                                                                                                                                                                                                                  |
| M6 Accent lost on the phone; ink links         | **Mostly fixed**                           | Figures are rose at both widths (sampled 158,79,92 at 390). Links are rose in `answers` and `sperm`, but still ink #1A1A1A in `figures`, `work`, `products` and `related` (Nit).                                                                                                                                                                                                                                                              |
| M7 Swipe strips at 768                         | **Not done**                               | Measured scrollWidth inside a 768 px viewport: `facial` 1,035, `label` 1,375, `related` 1,375. The third card is cut at the edge (768 slices 1, 3, 4).                                                                                                                                                                                                                                                                                        |
| M8 Card titles, products, no primary action    | **Two of three fixed**                     | Card titles are 26 px. Product tiles are 318 px (cycle 1: 660). There is still no button in `main`: only Subscribe and the language switcher (Medium 3).                                                                                                                                                                                                                                                                                      |
| M9 Repetition                                  | **Not done**                               | The captions of figures `s1` and `s3` still repeat short answers 1 and 2 word for word. "No placebo" appears 5 times.                                                                                                                                                                                                                                                                                                                         |
| M10 Image run at 390                           | **Not done**                               | `facial` (1,786 px) and `related` (2,380 px) still stack seven full-width 350 px squares: 4,166 px, 29% of the 14,298 px page.                                                                                                                                                                                                                                                                                                                |
| Nits                                           | **One fixed**                              | The related links are now 48 px (390) and 50 px (1440) tall, and the underline sits clear of the letters. Still open: the "Learn" label is not a link; the H1 is in Title Case; the icon row is centred at 390; the `names` row rules stop about 32 px short of the text at 390; the footer is 25 px too wide at 200% zoom and the Menu control is 22×22 (both site-wide); the page is 2,264 KB, with 839 KB of script (rule 53).             |

## Blockers

- None on this page.

## High

- **H1. `sperm` still sits on bone, so the first bone run is unchanged** (layout/spacing). The section's white setting does not render: the section
  carries `--section-background-hash: 0` and paints `rgb(240,240,240)`. The block background `#F0F0F0` therefore sits on a bone ground, and the text
  half has no edge. As a result:
  - `answers`, `sperm` and `names` read as one 1,900 px grey slab at 1440 (y 900 to 2800), and 2,302 px at 390;
  - at 390 the `sperm` text steps in to x 52 while every section around it starts at x 20, which reads as an indent with no container (390 slice 1).

  This is the same fault cycle 1 named. The spec change was made, but the live page does not show it.

- **H2. `names` and `work` still set 110–112 characters a line, under H2s at a fourth size** (typography/layout). Each richtext block renders as
  `.prose > div > p`, so the `.prose>p, .prose>h2` rule in both sections matches nothing. The computed `max-width` is `none` and the paragraphs are
  780 px wide at 1440. The band is 50–70 (rule 10). The same miss leaves both H2s at the theme size:
  - H2 sizes on the page at 1440: 48 px (`names`, `work`), 38 px (the rest) and 36 px (the proof title); at 390: 32, 28 and 24 px;
  - `work` is the evidence section, yet it is the hardest text on the page to read, and the right 40% of the screen beside it is empty (1440 slice 2).

## Medium

- **M1. The trial name is still printed on the photograph** (imagery/copy, for Malcolm). The pill "Ye 2026, PDRN side: −14.8% (retinol side −10.2%)"
  sits on the picture, which shows both eyes changed. The split-face contradiction cycle 1 described is weaker, because the card heading now frames
  the image as a size of change, but it is still written on the image. The pill is 10.9 px at 390, below the 12 px label floor (rule 41).
- **M2. The same picture keeps its trial label on the Ye study page** (copy, outside this page, for Malcolm). The Ye page's slot `ye.o4` still reads
  "After 28 days". It is the first link in this page's related row. Cycle 1 noted that page needs the same decision.
- **M3. The page still asks for nothing, and the shop row is lopsided** (hierarchy/conversion). There is no button in `main` (the PDRN hub has
  "Shop PDRN" and a dark CTA band). At 1440 the two product tiles fill x 48–708, and the right 684 px of the row is empty (1440 slice 4).
- **M4. Even the 65ch columns run long** (typography). At 1440, measured characters per line are 81 in `answers`, 82 in `prices`, 78 in `serum`,
  87 in `safety` and 83 in `legal`. Muli's zero is wider than its average letter, so `65ch` gives about 80 characters. Cycle 1 counted these as in band
  using a width estimate. At 390 everything is 48–57 (in band).
- **M5. Equal weight** (layout/spacing). 12 of 15 sections are 80/80, and only two padding values exist. The evidence section (`work`) gets the same
  room as the label checklist.
- **M6. Swipe strips at 768** (interaction, for human check). The three strips are unchanged (see the status table). This still matters because
  "The claims", "A leave-on facial or cream" and the third related card are cut off with no control.
- **M7. No chart; the central number exists only as text** (imagery/family fit). Both references carry the rose-against-grey bars. Here "23.0% vs 6.6%"
  appears as a figure, a table cell and "up to 23%" in the short answer.
- **M8. Repetition and the 390 image run** (copy/imagery). These are unchanged. They cost less than High 1 and High 2.

## Nits

- Links are in two colours: rose in `answers` and `sperm`; ink in `figures`, `work`, `products` and `related`.
- The other cycle-1 nits listed in the status table remain.

## Reference diff

- **PDRN hub:** ours is weaker at the ask and at the evidence. The hub has a primary button, a rose evidence list and a chart. Ours has a grey
  five-column table and no button.
- **Ye 2026 study page:** ours is weaker in its signature. The Ye page's bar chart is the thing a reader remembers. Ours states the same numbers in
  prose three times, and it opens on the Ye page's banner and figure strip with a different title.

**Signature:** none yet. The "0 sperm cells in the bottle" figure is still the candidate, and it is still the first of three equal numbers.

**Three tells of assembly:** one 80 px padding on 12 sections; a symmetric three-up grid of square mood images for the routes; the reading
column changes edge 10 times.

**Convergence cluster:** none cleanly. The page leans toward cluster 4: rounded cards on grey, and 10 of 12 content images square.

**Single change that most improves the page:** fix the `names`/`work` selector so it reaches `.prose > div > p` and the H2, then confirm with a
capture. It takes minutes, and it fixes the two longest lines and the two outsized H2s, in the evidence section. High 1 is the next smallest edit.

Captures and measurements (scratchpad, not committed):
`/private/tmp/claude-501/-Users-malcolmsmith-Claude-Code-Projects-skingenetix-website/4237e530-0fcc-4ba5-85dd-7427c7f586ff/scratchpad/critic2/`
(`shots/` with the blocked captures and slices, `cap/`, `measure-1440.json`, `measure-390.json`, `probe-1440-390.json`, `probe2.json`). Contact
sheet (unblocked pass): `~/Desktop/learn-salmon-cycle2-renders.png`.
