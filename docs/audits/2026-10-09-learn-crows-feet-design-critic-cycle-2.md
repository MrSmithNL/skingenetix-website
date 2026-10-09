# Design critic, cycle 2: Learn article "Crow's feet" redesign (2026-10-09)

**Page:** `/blogs/learn/crows-feet-what-causes-them-and-what-helps?view=learn-crows-feet`, the hidden preview of
`templates/article.learn-crows-feet.json`. The spec is `configs/hub-upgrades/learn-crows-feet-design-2026-10-09.json`.

**Critic:** the `design-critic` agent, in a fresh context. Captured live on 2026-10-09 at 390, 768, 1440 and 200% zoom (195 px). Klaviyo,
Shopify Forms and analytics were blocked and the cookie dialog was hidden. Each capture scrolled the page in steps first, and page loads
were spaced about 30 s apart. `measure.py` ran at 1440 and 390. I opened the mobile menu, ran a hit test on its links and pressed Escape.
I tested each proposed CSS fix by injecting it into the live preview before writing it down.

**References:** the Argireline hub, the Wang 2013 study article (cycle-1 captures from the same day) and the live designed sibling,
"Argireline and Matrixyl 3000 together" (captured fresh at 1440 and 390).

**No direction contract** exists for this site (there is no `website/design/`). The page is judged against the family references, the
skill's craft rules (cited as "rule N"), the store rules in memory and the cycle-1 report.

## Disposition: FIX (weighted 6.0, up from 5.3)

| Axis       | Weight | Cycle 1        | Cycle 2               |
| ---------- | ------ | -------------- | --------------------- |
| Design     | 40%    | 5.5            | 6.2                   |
| Usability  | 30%    | 5.0            | 6.0 (for human check) |
| Creativity | 20%    | 4.0            | 4.5                   |
| Content    | 10%    | 7.5            | 7.8                   |
| **Total**  |        | **5.25 (5.3)** | **5.96 (6.0)**        |

**There is no blocker, and this cycle improves on cycle 1, so keep it.** The article can switch onto this template once High 1 is applied
and checked with one capture at 1440. That fix is two CSS edits, and both were tested in the browser. The Medium items can follow in a
third cycle, which is the last one allowed, or go to the Learn-template backlog.

Every fix from cycle 1 held up except the zoom headings and part of the alignment work. The page now alternates its grounds strictly. Its
proof run is half the length and titled by results, and its table shows the result on a phone. The new faults come from the new call to
action, which falls apart on desktop, and from things cycle 1 left alone: identical section padding, a safety heading that floats away
from its items, and a checklist that becomes a swipe strip on a tablet.

## Cycle-1 items: status

| #    | Item                                     | Status              | Evidence (cycle 2)                                                                                               |
| ---- | ---------------------------------------- | ------------------- | ---------------------------------------------------------------------------------------------------------------- |
| B1   | Alts say "photographs"                   | **Fixed**           | No alt here says "photograph"; nor do the Badenhorst and Watanabe pages (curl, English).                         |
| H2   | GHK-Cu mole and magnitude                | **Fixed**           | Diptych removed. The Wang and Ye pairs show freckles, no mole (`img-wang.png`, `img-ye.png`).                    |
| H3   | Banner alt makes a claim                 | **Fixed**           | "Ripples spreading across a dark liquid surface".                                                                |
| H4   | Proof run: no heading                    | **Fixed**           | 48 px H2; cards titled by result. Run is 1,658 px, 15% of the page (was 2,872, 24%).                             |
| H5   | Bone ground unbroken for 6,196 px        | **Fixed**           | Strict alternation. Longest run of one ground is 1,658 px at 1440 and 1,685 px at 390.                           |
| H6   | Table hides Result on a phone            | **Fixed**           | At 390, Result is at x 159–304 in the 20–370 window. Wrapper has `tabindex`, `role`, label.                      |
| H7   | Related links struck through             | **Fixed, 390–1440** | `background-origin:content-box` works. Wrapped links at 200% zoom fail (Medium 1).                               |
| M8   | No primary action                        | **Partly**          | Button works at 390 (336×56) and 768 (354×58), breaks at 1440 (High 1). Figure links are ink.                    |
| M9   | Left edge zig-zags                       | **Mostly fixed**    | Eight reading sections start at x 464. Safety items are still centred at 390 and 768 (Medium 5).                 |
| M10  | H2s bind to the paragraph above          | **Fixed**           | 48 px above both second H2s, at 390 and 1440.                                                                    |
| M11  | Figure scale flat or inverted            | **Fixed**           | Figure over label: 44/20 (2.2x) at 1440, 33/16 (2.1x) at 390, 28/16 (1.75x) at zoom.                             |
| M12  | Headings break mid-word at zoom          | **Partly**          | Two breaks remain: "ingredient/s" and "smoothe/r" (Medium 1).                                                    |
| M13  | Lines too long                           | **Mostly fixed**    | 55–69 characters a line in reading sections. Evidence intro 74, products 76, standfirst 82.                      |
| M14  | Under-eye picture is off-question        | **Open**            | Accepted as interim in cycle 1. Now also a framing problem (Medium 6).                                           |
| M15  | Watanabe pair barely shows crow's feet   | **Fixed**           | Removed.                                                                                                         |
| M16  | Product block off-axis; PDRN unexplained | **Fixed**           | Paragraph at x 464. The PDRN sentence is accurate and careful.                                                   |
| M17  | Small standalone links                   | **Fixed**           | "Learn" is 37×48. The appraisal and related links are 48–50 px tall.                                             |
| Nits | Cycle-1 nits                             | **Mixed**           | Related H2 is now sentence case. Still open: headset icon, figure H2/H3 outline, 10.9 px pills, site-wide items. |

## Measurements

| Measure                             | 1440                                    | 390                        | Band / note                                                                           |
| ----------------------------------- | --------------------------------------- | -------------------------- | ------------------------------------------------------------------------------------- |
| Document `scrollWidth`              | 1440                                    | 390                        | 220 at 195 (200% zoom). The overflow is the site-wide footer form, not this template. |
| Page height                         | 11,209 (cycle 1: 11,940)                | 12,818 (13,689)            |                                                                                       |
| H1 / section H2                     | 60 / 48 px                              | 40 / 32 px                 | H1 is 28 px at 200% zoom                                                              |
| `displayToBody`                     | 4.0                                     | **2.86**                   | Rule 4 asks for at least 3 at 390. Rule 3 allows 1.5–2.4 inside an article.           |
| Body / line-height                  | 15 px / 1.6                             | 14 px / 1.6                | Rule 10 asks 17–20 px. Theme-wide and Malcolm's decision, so not scored here.         |
| Display line-height                 | 1.0 (figures), 1.1 (H1, H2)             | same                       | Band 0.80–1.05                                                                        |
| Fonts rendered                      | Muli, Fraunces                          | same                       | As intended                                                                           |
| Section padding                     | **80/80 on all 13 body sections**       | **40/40**                  | `distinctSectionPaddings` 1. Rule 23 asks for variation of 3x or more.                |
| Longest run of one ground           | 1,658 px (proof)                        | 1,685 px (evidence, proof) | Cycle 1: 6,196 and 6,983                                                              |
| Table                               | 1,344 px, no scroll                     | 350 px window over 960     | Result column is second                                                               |
| Primary button                      | **178×130 at x 1180, four lines**       | 336×56                     | 354×58 at 768                                                                         |
| Characters per line                 | 55–69 reading; 74, 76, 82               | 37–53                      | Band 50–70                                                                            |
| Left text edges at 1440             | 464 (8 sections); 612, 746, 128/812, 48 | 20; 52 in cards            |                                                                                       |
| Tap targets under 44 (`measure.py`) | 71 of 106                               | 56 of 72                   | Header, mega-menu, footer and cookie dialog. Template links are 48–50.                |
| Distinct radii                      | 10                                      | 10                         | Set by the theme                                                                      |
| Page weight                         | 2,111 KB (script 839)                   | 2,059 KB                   | Rule 53 allows 1,500. This is site-wide.                                              |

## The three before/after illustrations: label and framing check

| Card        | Label on image                                         | Article / register      | Stored alt                         | Mole | Framing                              |
| ----------- | ------------------------------------------------------ | ----------------------- | ---------------------------------- | ---- | ------------------------------------ |
| Wang 2013   | 22 of 45 graded clearly smoother vs 0 of 15 on placebo | Table; register claim 1 | OK                                 | None | Wall beige to sage                   |
| Ye 2026     | Crow's-feet area −23.0% vs −6.6% with retinol          | Table                   | OK ("a quarter softer" is a gloss) | None | Wall to blue-grey; cooler            |
| Ye eye bags | Eye-bag volume −14.8% vs −10.2% with retinol           | Prose                   | OK                                 | None | Wall changes; after face ~15% larger |

All three labels match the article and the claims registers. No visible caption or alt implies a study photograph.

## Blockers

None.

## High

- **High 1. On desktop the page's only call to action collapses into a four-line blob beside the paragraph** (interaction/hierarchy).
  At 1440, "Shop the Acetyl Hexapeptide-8 Serum" renders 178×130 px at x 1180, outside the 32rem reading column, as an underlined
  graphite pill that wraps onto four lines and breaks "Hexapeptide-/8" (`crop-cta1440.png`; 1440 slice 3). It reads as a broken
  component, and it is the one action the page asks for. The theme's `section-header` is a grid whose columns compute to
  `700px 177.9px`. The paragraph takes 700 px and the link gets what is left. The underline, on every width, comes from the section's own
  `a:not(.button){…text-decoration:underline}`, which also matches the button. The sibling uses a real theme `.button`, and it holds.

  **Spec fix (products `custom_css`, 441 of 500 characters):**
  - change `a:not(.button){color:#3E4A52;text-decoration:underline}` to `.prose a{color:#3E4A52;text-decoration:underline}`.
    The product-card titles then fall back to the theme ink, which also trims the accent count (rule 16);
  - add to the header rule: `.section-header{max-width:32rem;margin-inline:auto;width:100%;display:flex;flex-direction:column;`
    `align-items:flex-start;gap:24px}`;
  - add `text-decoration:none` to the `.section-header>a{…}` rule.

  Injected into the live preview, the layout part gives a 354×58 button at x 464, under the paragraph, with the paragraph back at 512 px
  (`fix-cta-after.png`). Check the underline removal with a capture.

## Medium

- **Medium 1. At 200% zoom two headings still break mid-word, and the wrapped links look struck through** (typography, rule 54).
  - "Which skincare ingredient/s have been tested" (evidence H2, 32 px). The evidence CSS never got the 320 px rule, because it was at
    478 characters.
  - "22 of 45 graded clearly smoothe/r" (Wang card title). The 22 px rule applies, but the card keeps the section's own
    `.rba__text{padding:40px 32px}`, which leaves 91 px, and the theme sets `overflow-wrap:anywhere` on `.h2`.
  - "What do Koreans use for under-eye wrinkles" ends with "?" alone on a line (same cause, under-eye card).
  - "Why do crow's feet show…" sets one word per line, 13 lines (no 320 px rule in `why`).
  - Wrapped links ("Read our / appraisal of / Wang 2013", and the related links) draw the theme's underline under line 1, so it cuts
    across the top of line 2 (`z-crops.png`).

  **Spec fix:**
  - **evidence (484):** drop `background:#fff;` from the table rule, `font-weight:600;` from the `th` rule (headers are bold anyway) and
    `;max-width:100%` from `.sgx-evtable`. Then add `@media(max-width:320px){h2{font-size:24px!important}}`. Tested: "ingredients" stays
    whole (`fix-zoom.png`).
  - **proof (390):** add `@media screen and (max-width:320px){.rba__row .rba__text{padding:24px 16px!important}.rba__text .h2`
    `{overflow-wrap:normal}a:not(.button){display:inline;padding-block:0}}`. Use `!important` and the extra class, because the section
    prints its own padding rule after head styles. Check with a capture.
  - **undereye (269):** add the same padding and `h2{overflow-wrap:normal}` inside a 320 px query.
  - **related (191):** add `@media screen and (max-width:320px){a{display:inline;padding-block:0}}`.
  - **why (127):** add `@media screen and (max-width:320px){h2{font-size:24px!important}}`.

- **Medium 2. Every section has the same padding, so nothing dominates** (layout/spacing, rule 23). All 13 body sections are 80/80 at
  1440 and 40/40 at 390 (`distinctSectionPaddings` 1). With the grounds now alternating, this even beat is the strongest template signal
  left. The proof section, the one place the page shows results, gets the same weight as the closing review lines.
  **Spec fix:** give `proof` `@media screen and (min-width:1000px){.section{padding-block:128px}}` (454 characters with Medium 1), and
  let `closing` and `related` run tighter at about 48 px.
- **Medium 3. The safety heading floats away from its own items** (hierarchy). "Using actives near the eyes safely, and when to see
  someone" sits 160 px below the professional text and 184 px above its first icon at 1440. At 390 the gaps are 80 above and 136 below.
  The heading reads as the end of the previous section, because it lives in its own `safety_intro` section with full bottom padding.
  **Spec fix:** in `safety_intro` add `.section{padding-bottom:0}` (147 characters). That leaves about 104 px at 1440 and 96 at 390.
  To close it further, move the H2 into the `safety` section's own `title` setting.
- **Medium 4. On a tablet the checklist turns into a swipe strip that hides half of it** (interaction, for human check). At 768 the four
  "How do you choose" items sit at x 32, 372, 712 and 1051. Item 3 is cut at the edge ("Ask w…") and item 4 is off-screen, with no
  control. The related row does the same. **Spec fix (choose, 243 characters):**
  `@media screen and (min-width:700px) and (max-width:999px){.multi-column{grid:auto/1fr 1fr;overflow:visible;margin-inline:0}`
  `.multi-column__item{grid-column:auto}}`. Tested: a 2×2 grid at x 64 and 408 (`fix-choose768.png`). Add the same to `related`.
- **Medium 5. The safety list is centred on phone and tablet while everything around it is left-aligned** (layout). At 390, five items
  with ragged centred paragraphs of three or four lines run for 1,147 px. At 768 they are two centred columns. This is the part of cycle-1
  Medium 9 that was not applied. **Spec fix (safety, 117 characters):**
  `@media screen and (max-width:999px){.text-with-icons__item{text-align:start;justify-items:start}}`. The icon may need
  `margin-inline:0` as well. Check with a capture.
- **Medium 6. Every before/after pair changes the room and the light between panels** (imagery, for human check).
  - **Wang:** the wall behind turns from beige to sage.
  - **Ye:** the wall turns from beige to blue-grey, and the after light is cooler and brighter.
  - **Eye bags:** the wall changes, the after face is about 15% larger and sits lower in the frame, and the top 40% of the square is hair
    and wall.

  A reader comparing skin sees a different room first. That makes the change look staged and larger than the measured 23% or 15%, on a
  page whose message is "softer lines, not no lines". The eye-bag pair still answers a question about eye bags under a heading about
  under-eye wrinkles (cycle-1 Medium 14). **Spec fix:** re-render or retouch the after panels to the before panel's wall, light and scale,
  with new file stems. For the eye-bag pair, crop to the eyes or swap in an under-eye-lines pair labelled "Under-eye lines −23.4% vs −7.0%
  with retinol".

## Nits

- At 1440 the proof cards are 660 px squares holding 297–313 px of text, so they are still about half empty.
- At 390 the table rows are 130–217 px tall, set by the off-screen "Who paid" text, which leaves 50–90 px of air under each visible row.
- Labels are small at 390: the before/after pills are 10.9 px, and the figures' source links are ink, not accent.
- The figures are `<h2>` and their labels `<h3>`, ahead of the first real H2. The H1 is in Title Case while every H2 is sentence case.
- The safety item "Pregnant or breastfeeding?" still uses a headset icon (`picto-customer-support`).
- The copy says "PDRN Renewal Serum" and the card says "PDRN 1% Renewal Serum".
- At 1440 the fourth related tile ("Argireline research") shows a grey band above and below its picture, and the other three do not
  (1440 slice 6, pixel 205 vs 255; human check).
- At 390 the first screen holds no action (rule 47). That is normal for an article, and the button sits at y 7,203.
- Site-wide: the 25 px footer overflow at zoom, header icons overlapping the logo at zoom, product-card titles clipped at zoom, the
  15/14 px body, ten radii and 2.1 MB of page weight.

## Rule 27 check A: tells

- Pill labels above headings: none. "In short:" is a bold run-in, not a pill.
- One coloured word per heading: none.
- Arrows on every link: none. The button's chevron is hidden.
- Middle-dot meta lines: none. The byline uses commas.
- Identical card grids: one, the related row of four identical tiles. The sibling uses the same pattern, so this is family fit, not a
  new tell.
- Store rules: no moles on the remaining images, no black backgrounds (the banner is a dark photograph with a 28% overlay, as on the
  family), accent `#3E4A52` on the figures, links and button.

## Reference diff

- **Argireline hub:** the hub turns its trials into a bar chart and closes with a full-width Shop band. Ours has no chart, and on desktop
  its only Shop action is the broken blob in High 1.
- **Wang 2013 article:** Wang holds one centred column and carries "Read the full evidence" and "See the product" as real theme buttons.
  Ours now holds the same column for its text, but the module cards (why, proof, under-eye) and the full-width rows still step out to
  x 48, 128, 746 and 812.
- **Sibling Learn article:** the sibling puts a real `.button` in its answer card near the top (y 1,507 at 1440), varies its pictures
  (product shots, a three-step row) and runs three proof pairs. Ours puts the action 6,300 px down and has fewer kinds of picture. It does
  have a better table, with the result second and "Who paid" on every row.

## Signature, tells and cluster

**Signature: none yet.** The candidate is still the honest evidence table. It puts the result second and names who paid for every trial,
and the page closes on "softer lines, not no lines". On a phone, though, "Who paid" sits at x 830–980, behind the sideways scroll, and
nothing visual marks the table as the page's centre. A designer would remember the honesty, not the page.

**Tells of assembly:**

- a header link restyled as a button, which the theme's grid crushes to 178 px on desktop;
- 80/80 padding on every section;
- a safety heading in its own section, 184 px above its items;
- square white text cards sized to their pictures and half empty.

**Cluster:** still closest to 4, the theme card kit (10 px white cards on bone, ten radii), though the alternating grounds and the
shorter proof run soften it.

## Single change that most improves the page

Apply High 1: two CSS edits in the products section, already tested in the browser. That turns the page's only action from a broken
blob into a proper button on the reading axis, and it is the one condition for switching the template. It takes about five minutes,
plus one capture at 1440 to confirm the underline is gone. The zoom fixes in Medium 1 come next and take about 15 minutes.

Captures, measurements and fix tests (scratchpad, not committed):
`/private/tmp/claude-501/-Users-malcolmsmith-Claude-Code-Projects-skingenetix-website/4237e530-0fcc-4ba5-85dd-7427c7f586ff/scratchpad/cf2/`
(`measure-1440.json`, `measure-390.json`, `dom.json`, `probe2.json` to `probe5.json`, `full-*.png`, `d1440-*.png`, `m390-*.png`,
`crop-cta*.png`, `fix-*.png`, `cmp-1440.png`, `ref-sib-*.png`). Contact sheet: `~/Desktop/learn-crowsfeet-cycle2-renders.png`.
No `scores.csv` exists for this project, because there is no `website/design/`. The scores are recorded in the table above, as in cycle 1.
