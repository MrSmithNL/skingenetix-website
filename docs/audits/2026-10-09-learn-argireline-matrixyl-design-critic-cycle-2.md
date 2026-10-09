# Design critic, cycle 2: Learn article redesign (2026-10-09)

**Page:** `/blogs/learn/argireline-and-matrixyl-3000-together?view=learn-argireline-matrixyl-3000` (hidden preview of
`templates/article.learn-argireline-matrixyl-3000.json`, spec `configs/hub-upgrades/learn-argireline-matrixyl-3000-design-2026-10-09.json`).
**Critic:** `design-critic` agent, fresh context, captured live 2026-10-09 with Klaviyo and Shopify Forms blocked, loads spaced
about 30 s apart. Compared against the reference builds (Argireline hub, Badenhorst study article, Collagen Skincare) at 390 and 1440.
No direction contract exists for this site (no `website/design/`), so the page is judged against the reference family, the
skill's craft rules and the store rules in memory.

**Disposition: FIX** (weighted 5.1, up from 4.8, so cycle 2 is the best cycle so far; keep it). **Do not switch the article onto
this template yet: blocker 1 is still live.** One cycle is left (cycle 3 is the last under the loop rules).

| Axis (cycle-1 set) | Cycle 1 | Cycle 2 |
| ------------------ | ------- | ------- |
| Hierarchy          | 5.5     | 5.5     |
| Rhythm             | 4.0     | 6.0     |
| Imagery            | 4.5     | 5.5     |
| Typography         | 6.0     | 5.5     |
| Family fit         | 7.0     | 7.0     |
| Mobile             | 3.0     | 4.0     |

Rubric axes: Design 5.6 (40%), Usability 4.5 (30%, for human check), Creativity 4.0 (20%), Content 7.0 (10%) = **5.1**.

## Cycle-1 items: status

| #   | Item                                 | Status                                           | Evidence (cycle 2)                                                                                                                                                                                                                                                                                                    |
| --- | ------------------------------------ | ------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Phone page scrolls sideways          | **Not fixed**                                    | `scrollWidth` 740 at 390 (overflow 350 px), 545 px at 200% zoom. Full-page 390 capture is 740 px wide; caveat, reviewer line and date run off-screen. The CSS landed on the wrong element (see Blocker 1).                                                                                                            |
| 2   | Watermarked step-1 photo             | **Fixed**                                        | Step 1 is `skingenetix-matrixyl-3000-collagen-serum-pipette-drop-forming.jpg` with a descriptive alt.                                                                                                                                                                                                                 |
| 3   | Rhythm and backgrounds               | **Mostly fixed**                                 | Backgrounds now alternate white / #F0F0F0 down all 11 body sections; the "together" block is plain rich-text. New problem: see High 4.                                                                                                                                                                                |
| 4   | Key figure vs H1                     | **Fixed on phone, broken on tablet and desktop** | 390: figure 32.5 px under a 40 px H1 (good). 1440: figure 36 px over a 32 px label (1.13x, it no longer leads). 768: figure 19 px under a 26 px label (inverted).                                                                                                                                                     |
| 5   | Byline buried                        | **Fixed**                                        | Byline is the banner's last line at all widths.                                                                                                                                                                                                                                                                       |
| 6   | Matrixyl render implying penetration | **Fixed, but the replacement is wrong**          | Penetration render gone; the replacement is an amber gel drop (see High 2).                                                                                                                                                                                                                                           |
| 7   | Black mobile banner                  | **Fixed**                                        | Mobile banner mean rgb 62,64,67 (was 35,34,35), stddev 56, so the refraction image reads.                                                                                                                                                                                                                             |
| 8   | Related row                          | **Partly fixed**                                 | Square 300x300 images, titles align, links name their destination. At 390 the standalone "Read the ... appraisal" links are 18 px tall, and the row is still a swipe strip (second card cut off at x 325).                                                                                                            |
| 9   | Image monotony                       | **Not fixed**                                    | 21 of 22 content images are square (only the banner is not). At 390 the proof, jobs and layering sections show eight full-column 350x350 squares one after another, with only text between them. "Who should skip" is now plain text (fixed).                                                                         |
| 10  | Key-figure source links              | **Fixed**                                        | "Wang 2013" and "Matrixyl 3000 research" are linked under the figures.                                                                                                                                                                                                                                                |
| 11  | Repetition                           | **Partly fixed**                                 | "22 of 45" still appears 5 times (plus "22 of the 45" once). "Not tested together" is said 7 ways ("No study has tested" x3, "no published study", "None exists", "Not tested" x2). The jobs captions still repeat the paragraph above them word for word ("Deep wrinkles and the look of firmness.").                |
| 12  | Type                                 | **Not fixed, measure worse**                     | Body is still 15 px (1440) and 14 px (390), a theme-wide setting. Line length in together, caution, jobs, layering and products is 93 to 104 characters at 1440 (band 50 to 70; cycle 1 measured 81 to 90). Six headings are still Title Case and the rest sentence case; centred and left alignment are still mixed. |

## Blockers

- **1.** **The phone page still scrolls sideways** (interaction, for human check). The overflow is measured at 390 (scrollWidth 740) and at 200% zoom (545 px over).
  The fix targeted `.sgx-evtable` (it now has `min-width:0; max-width:100%`), but the element that stretches is its unclassed parent `<div>`, a grid
  item of `.prose` (display: grid) with `min-width:auto`. That div measures 720 px. **Spec fix (evidence `custom_css`):** replace the first rule with
  `.prose>*{min-width:0;max-width:100%}` (the CSS stays under 400 characters). Check that `document.documentElement.scrollWidth` is 390 at 390 and 195 at
  200% zoom before calling it fixed.

## High

- **2.** **The Matrixyl image in "Why are they different jobs?" shows the wrong product colour** (imagery). `skingenetix-matrixyl-serum-texture-closeup.jpg`
  is an amber, bubbled gel drop. Malcolm confirmed on 2026-08-20 that the Matrixyl serum is transparent with no tint, in a deep emerald-teal scene
  (`#016569`), so this picture misdescribes the product. Its alt text is the filename ("matrixyl serum texture closeup"). **Spec fix:** set block `j2`
  to a Matrixyl image in the emerald scene. The Collagen page uses one beside "Matrixyl 3000: Signal Peptides" (likely
  `skingenetix-matrixyl-3000-pro-collagen-full-firming-treatment.jpg`; confirm by eye), and the block needs a descriptive alt.
- **3.** **The key-figure scale has flattened on desktop and inverted on tablet** (hierarchy). Measured figure vs label: 36/32 px at 1440 and 19/26 px at 768. The
  change to `impact_text_size_ratio` 0.5 fixed the phone and broke the other two widths. The "0", the page's only candidate signature, is the same size and
  the same slate grey as the other two figures. **Spec fix (figures `custom_css`):** `h3.h4{font-size:20px}@media(min-width:700px){.impact-text__text{font-size:44px!important}}`.
  That gives about 2.2x figure-to-label on every width, keeps the figure under the H1 (40 px on phone, 60 px on desktop), and leaves the ratio setting alone.
- **4.** **Five reading sections hug the left edge with long lines and an empty right half** (layout/spacing). At 1440, together, jobs, layering, caution and
  products set 15 px text 93 to 104 characters wide, starting at the 48 px gutter. The right 40 to 45% of each screen is empty (d1440 slices 1, 3 and 4).
  The Badenhorst reference centres a reading column instead. **Spec fix:** in the together and caution `custom_css`, `.rich-text__wrapper{max-width:65ch;margin-inline:auto}`.
  In the jobs, layering and products `custom_css`, `p,ul{max-width:65ch}`.

## Medium

- **5.** **No primary action on the page** (interaction / conversion). The only `<button>` elements in the page are Subscribe and English. Both family references
  carry one ("Shop Argireline" plus a closing band; "Shop the Pro-Collagen Cream" in the banner). **Spec fix:** add a button block "Shop the Peptide Duo Set"
  to the `answer` media-with-text text block, linked to the duo product.
- **6.** **No ingredient accent** (colour). `--sg-accent` is empty and every link is `#1A1A1A`. The family uses its accent on figures and links (Badenhorst blue
  figures, Collagen teal links). **Spec fix:** in the figures and evidence `custom_css`, `a,.impact-text__text{color:#016569}` (the Matrixyl teal measures
  about 5.9:1 on #F0F0F0).
- **7.** **Image run at 390 and the equal pair at 1440** (imagery). See item 9 above. The jobs pair is two identical 648 px squares side by side (rule 27). **Spec fix:**
  re-crop the jobs pair to 4:5 and the three step images to 3:2. Name the new files without the old stem as a prefix (for example `skingenetix-layering-spf-forehead-3x2.jpg`,
  not `skingenetix-howto-step4-spf-3x2.jpg`), because the upload binds a neighbour file when one stem prefixes another.
- **8.** **Repetition** (copy). See item 11 above. **Spec fix:** delete the first paragraph of `jobs` (the captions already carry it). Drop "22 of 45" from the
  proof card title, so it reads "Crow's feet graded clearly smoother in 4 weeks".
- **9.** **The H1 breaks mid-word at 200% zoom** (typography). "Argirelin / e" (`first-390x200pct.png`). **Spec fix (banner `custom_css`):**
  `@media(max-width:320px){h1{font-size:28px!important}}`.
- **10.** **Mixed heading case and alignment** (typography). Title Case: "What the Trials Measured", "Before You Start", "Read the Trials and the Research" and the
  three proof card titles. Everything else is sentence case. **Spec fix:** sentence case for all six, to match the article's own question headings.
- **11.** **Related links are 18 px tall at 390** (interaction, for human check). **Spec fix (related `custom_css`):** `a{display:inline-block;padding-block:13px}`.

## Nits

- The key-figure numbers render as `<h2>` ("22 of 45", "−39%", "0") with their labels as `<h3>`. The proof card titles are `<h3>` at 36 px, the same size as the `<h2>` "Before You Start".
- Step-2 alt text is still the filename. Step 2 is still a frequency, not a step.
- The "Learn" eyebrow is still not a link.
- The red sale badge on the duo is still a fourth colour.
- The Raikou forehead model still has brown spots on both cheeks (no-moles rule).
- The byline is a middle-dot meta string.
- The theme's header icons overlap the logo at 200% zoom. This happens on every page, not only this one.
- Nine distinct radii, set by the theme.

**Signature:** none yet. The honest "0 trials of the two together" could carry the page, but it still sits as the third of three equal grey numbers.

**Single change that most improves the page:** the one-rule grid-item fix in Blocker 1 (minutes). It is the only thing stopping the switch. After that, High 3
(about 80 characters of CSS) restores the hierarchy that the scale change broke.

Captures and measurements (scratchpad, not committed): `/private/tmp/claude-501/-Users-malcolmsmith-Claude-Code-Projects-skingenetix-website/4237e530-0fcc-4ba5-85dd-7427c7f586ff/scratchpad/c2/`.
Contact sheet: `~/Desktop/learn-spoke1-cycle2-renders.png`.
