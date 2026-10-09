# Design critic, cycle 1: Learn article "Crow's feet" redesign (2026-10-09)

**Page:** `/blogs/learn/crows-feet-what-causes-them-and-what-helps?view=learn-crows-feet`, the hidden preview of
`templates/article.learn-crows-feet.json`. The spec is `configs/hub-upgrades/learn-crows-feet-design-2026-10-09.json`.
**Critic:** the `design-critic` agent, in a fresh context. Captured live on 2026-10-09 at 390, 768, 1440 and 200% zoom (195 px), with
Klaviyo, Shopify Forms and analytics blocked and the cookie dialog hidden. Page loads were spaced about 30 s apart.
**References:** the Argireline hub, the Wang 2013 study article and Fine Lines & Wrinkles, captured at 1440 and 390.
**No direction contract** exists for this site (there is no `website/design/`). The page is judged against the family references, the
skill's craft rules (cited as "rule N"), the store rules in memory and the sibling page's cycle-1 and cycle-2 reports.

## Disposition: FIX (weighted 5.3)

| Axis       | Weight | Score                  |
| ---------- | ------ | ---------------------- |
| Design     | 40%    | 5.5                    |
| Usability  | 30%    | 5.0 (for human check)  |
| Creativity | 20%    | 4.0                    |
| Content    | 10%    | 7.5                    |
| **Total**  |        | **5.25, shown as 5.3** |

**Do not switch the article onto this template until Blocker 1 is fixed.** Most of the generic fixes from the sibling page's cycles landed
and hold up:

- The table now stays inside its box.
- The figures sit below the H1 at every width.
- The byline is in the banner.
- The accent appears on the figures and on the links in the rich-text sections.
- The Robinson row is in the table, so the "who paid" column is complete.

What still holds the page back is the middle third: the run of proof cards, an unbroken bone ground and the alignment.

## Measurements

| Measure                      | 1440                                                             | 390                            | Band / note                                                                                                                   |
| ---------------------------- | ---------------------------------------------------------------- | ------------------------------ | ----------------------------------------------------------------------------------------------------------------------------- |
| Document `scrollWidth`       | 1440                                                             | **390**                        | 200% zoom: 220 at 195 (25 px over). The overflow comes from the site-wide footer logo and newsletter form, not this template. |
| Table wrapper / table        | 1344 / 1344                                                      | **350 / 960**                  | The table scrolls inside its own wrapper. **The Result column starts at x 665 of 960.**                                       |
| H1                           | 60 px                                                            | 40 px                          | 28 px at 200% zoom                                                                                                            |
| Key figure / label           | 44 / 20 (2.2x)                                                   | **33 / 20 (1.65x)**            | **20 / 20 (1.0x) at 200% zoom**                                                                                               |
| Section H2                   | 48 px                                                            | 32 px                          | The figures (44) are now smaller than every H2 (48)                                                                           |
| Body                         | 15 px                                                            | 14 px                          | Rule 10 asks 17 to 20 px. This is a theme-wide setting.                                                                       |
| Characters per line          | answers, naturally, professional: ~80 to 86; evidence: ~88 to 89 | ~55 to 60                      | Band 50 to 70. "65ch" in Muli renders at about 80 characters.                                                                 |
| Left text edges at 1440      | x = 612, 428, 746, 48, 128/812, 1155                             |                                | Six different edges down one article                                                                                          |
| Unbroken bone ground         | **878 to 7074 px (6,196 px, 5 sections)**                        | **1018 to 8001 px (6,983 px)** | 52% of the page                                                                                                               |
| Proof section height         | **2,872 px**                                                     | 2,797 px                       | 24% of the page                                                                                                               |
| Standalone links under 44 px | 4 "Read our appraisal" links (18 px), "Learn" (37 x 18)          |                                | Inline links in prose are excused                                                                                             |
| `--sg-accent`                | empty                                                            |                                | The hub sets `#3E4A52`. The proof-card, product and related links render `#1A1A1A`.                                           |
| Primary button               | none                                                             | none                           | The hub, Wang and Fine Lines & Wrinkles pages each carry one or more                                                          |
| Page weight                  | 2,251 KB (script 841)                                            | 2,060 KB                       | Rule 53 allows 1,500. This is site-wide.                                                                                      |
| Distinct radii               | 10                                                               | 10                             | Set by the theme                                                                                                              |

## The five before/after illustrations: caption and label check

| Card            | Result label on image                                         | Article / register                                          | Visible caption implies a study photo? | Stored alt text                                                                                                                       |
| --------------- | ------------------------------------------------------------- | ----------------------------------------------------------- | -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| Wang 2013       | 22 of 45 graded clearly smoother vs 0 of 15 on placebo        | Matches the table; register claim 1                         | No                                     | OK                                                                                                                                    |
| Ye 2026         | Crow's-feet area −23.0% vs −6.6% with retinol                 | Matches the table; register Fig 6B                          | No                                     | OK (the gloss "about a quarter softer" is a nit)                                                                                      |
| Badenhorst 2016 | 55.8% more wrinkle-volume reduction than the plain serum base | Matches; register short form                                | No                                     | **"Two close-up photographs of the same woman's right eye corner, before and after 8 weeks", which asserts a photograph (Blocker 1)** |
| Watanabe 2014   | Rated moderately softer: 1 in 3 women vs none on placebo      | Matches (33.3% investigator, 30.0% women); register claim 4 | No                                     | **"…the same lines in both photographs" (Blocker 1)**                                                                                 |
| Ye eye bags     | Eye-bag volume −14.8% vs −10.2% with retinol                  | Matches the prose; register claim 5                         | No                                     | OK. The picture answers a different question from its heading (Medium 14).                                                            |

All five labels match the article and the claims registers.

## Blockers

- **1.** **Two stored alt texts call generated before/after images "photographs"** (copy/imagery). The GHK-Cu alt reads "Two close-up photographs of the
  same woman's right eye corner, before and after 8 weeks". The glutathione alt reads "the same lines in both photographs". Screen readers,
  image search and AI extractors read both. Each sits beside "(Badenhorst 2016)" or "(Watanabe 2014)" and the trial's length, so the text asserts a
  documentary trial photograph.

  This is not the disclosure question that Malcolm closed on 2026-09-22. That decision covers what we do not say. These alts make a positive false
  statement.

  **Spec fix (Files, no template change):** set the alt on `skingenetix-copper-peptide-ghk-cu-crows-feet-wrinkles-before-after.jpg` to "Before
  and after: the outer corner of the eye, crow's-feet lines softer after 8 weeks". Set the alt on `skingenetix-glutathione-crows-feet-softer-before-after-study.jpg`
  to "Before and after: crow's feet at the outer eye corner, a little softer after 10 weeks". Both files are also live on the copper and glutathione
  pages, so the fix corrects those pages too.

## High

- **2.** **The GHK-Cu diptych breaks the no-moles rule and shows more change than the trial measured** (imagery, for human check).
  - **The mole:** a brown mole sits at the temple in both panels (crop `img-ghk.png`, at x 92, y 236 and x 427, y 255). Malcolm's rule of
    2026-09-29 bans moles.
  - **The magnitude:** the after panel shows the crow's-feet fan almost gone. The register gives the absolute change as volume −24.1% at 8 weeks
    (copper register, lines 39 and 211). The 55.8% is relative to the base. The page's own copy says "softer lines, not no lines".

  **Spec fix:** retouch the mole by cloning skin, not inpainting. Replace the after panel, or the whole `proof.f3` image, with a pair that keeps every
  line about a quarter softer, as the Ye image does. The same file is live on the copper research page.

- **3.** **The banner's stored alt makes an efficacy claim** (copy). It reads "Ripples settling into a still, dark liquid surface, **representing expression
  lines smoothing out**". That is an unqualified result, stronger than the register's "soften the look of expression lines", on a page that opens
  with "cannot stop the movement". **Spec fix (Files):** change the alt on both banner files (desktop and mobile) to "Ripples spreading across a dark
  liquid surface". The same files serve the clinical-studies banners.
- **4.** **The proof run has no heading, demotes its own results and leaves the cards empty** (hierarchy).
  - **No heading:** after the table's footnote, four diptychs and four white cards follow with no section heading (`proof.settings.title` is "").
  - **Results demoted:** each card's 36 px title names the method ("Clinicians' grade of crow's feet, made blind"). The result itself appears only
    in a 10.9 px pill on the photo (390).
  - **Empty cards:** each white card is 660 px tall, and its text fills about a third of it (d1440 slices 2 and 3).
  - **Weight:** the run is 2,872 px, a quarter of the page, of one repeated treatment (rules 24 and 27).

  The hub's cards title the result instead ("22 of 45 Graded Clearly Improved — None on Placebo") and fill the card with design, results and citation.

  **Spec fix:** give `proof` a section title, for example "What did each trial find?". In each card:
  - **title:** the result, for example "22 of 45 graded clearly smoother, none of 15 on placebo";
  - **subheading:** "Argireline 10%, Wang 2013";
  - **content:** the measure and the design, for example "Clinicians' blind grade; 60 adults aged 25–60; 4 weeks; placebo cream", plus the link.

- **5.** **Bone ground runs unbroken for 6,196 px** (layout/spacing). It covers answers, why, evidence, proof and choose: y 878 to 7074 at 1440 and 1018 to
  8001 at 390, measured by pixel. The spec says "backgrounds alternate", but `why` and `proof` inherit the page bone. This is the same failure as the
  sibling page's cycle-1 High 3.

  **Spec fix:** figures `#F0F0F0` (as on the Wang page), answers `#FFFFFF`, evidence `#FFFFFF`, choose `#FFFFFF`, products `#F0F0F0`, naturally
  `#FFFFFF`. That gives strict alternation from the figures down to related.

- **6.** **On a phone the table hides its results** (interaction, for human check).
  - **At 390:** the 350 px window shows Ingredient, Trial and People. Result sits at x 665 to 810, behind 315 px of sideways scroll, with no visual
    hint that the table scrolls.
  - **For keyboard users:** the wrapper has no `tabindex`, role or label, so a keyboard user cannot scroll it (axe `scrollable-region-focusable`).
  - **At 200% zoom:** one column of eight is visible.

  **Spec fix (liquid block `evidence.t`):**
  - reorder the columns to Ingredient, Result, Trial, People, Length, Compared with, What was measured, Who paid;
  - give `.sgx-evtable` the attributes `tabindex="0" role="region" aria-label="Five crow's-feet trials compared"`;
  - optionally add one draft line to block `h`: "On a phone, swipe the table sideways for every column."

  The section CSS budget is 443 of 500 characters, so the fix has to be markup, not CSS.

- **7.** **The related-row links render struck through** at every width (interaction). Crops `crop-rel390.png` and `crop-rel1440.png` show it. The cause is
  the cycle-2 tap-target rule `a{display:inline-block;padding-block:13px}`. The theme draws its underline as a background at `min(100%, 26.87px)`
  from the top of the padding box, and the 13 px padding pushes that line about 14 px into an 18 px line of text. **Spec fix (related `custom_css`):**
  `a{display:inline-block;padding-block:13px;background-origin:content-box}`.

## Medium

- **8.** **No primary action, and the accent stops halfway** (interaction/colour). The only buttons are Subscribe and English. The references carry "Shop
  Acetyl Hexapeptide-8 Serum" (hub), "Read the full evidence" and "See the product" (Wang), and three Shop buttons (Fine Lines & Wrinkles).
  `--sg-accent` is empty, so the proof, product, under-eye and related links are graphite. **Spec fix:**
  - add one button, "Shop the Acetyl Hexapeptide-8 Serum", to the products section;
  - add `a:not(.button){color:#3E4A52}` to the `proof`, `products`, `undereye` and `related` CSS.
- **9.** **The left edge zig-zags** (layout). Text starts at x 428 in answers and naturally, 48 in evidence, choose and products, 746 or 812 in the media
  cards and 48 in the safety icons. At 390 the safety items switch to centred text while everything around them is left-aligned. **Spec fix:** centre
  the reading text on the answers axis.
  - **evidence:** change `p,h2{max-width:44rem}` to `p,h2{max-width:44rem;margin-inline:auto;width:100%}` (the table stays full width);
  - **choose and products:** apply the same to their heading and intro;
  - **safety:** at 699 px and below, set the safety items to `text-align:start` (selector to confirm).
- **10.** **Two H2s bind to the paragraph above them** (hierarchy). "Is it crow's feet…" and "Which skincare ingredients…" sit 12 px under the previous
  paragraph at 390 (about 20 px at 1440), with about 24 px below each. Each is a second block inside one `.prose` grid. **Spec fix:** in answers, add
  `.prose>div+div{margin-top:48px}`. In evidence, move block `a` (the age question) into answers, so the table section opens with its own H2. That
  also saves CSS budget.
- **11.** **The figure scale goes flat on phone and inverts at zoom** (hierarchy). The figure-to-label ratio is 33/20 px at 390 and 20/20 px at 200%, where
  the four-line label outweighs "22 of 45". The fixed `h3.h4{font-size:20px}` does not scale with the viewport. **Spec fix (figures):**
  - add `@media screen and (max-width:699px){h3.h4{font-size:16px}}`;
  - add `@media screen and (max-width:320px){.impact-text__text{font-size:28px!important}}`.

    That gives about 2.1x at 390 and 1.75x at zoom.

- **12.** **Five headings break mid-word at 200% zoom** (typography, rule 54). The breaks are "ingredient/s", "profession/al", "Korea/ns", "wrinkl/es" and
  "Clinicia/ns'" (`z-overview.png`). **Spec fix:**
  - **evidence, professional and undereye:** add `@media screen and (max-width:320px){h2{font-size:24px!important}}` to each;
  - **proof cards:** add the same rule for the card title, with the card padding reduced at 320 px and below.
- **13.** **Lines are too long** (typography, rule 10). "65ch" in 15 px Muli renders at about 80 to 86 characters, and the evidence paragraphs reach 88 to 89. **Spec fix:** replace 65ch and 44rem with about 32rem, which gives about 66 characters.
- **14.** **The under-eye picture answers a different question from its heading** (imagery/copy). The heading asks about under-eye **wrinkles**, but the image
  and its pill show eye-bag volume. The matching line figure (−23.4% vs −7.0%) appears only in the prose. **Spec fix:** use an under-eye-lines
  diptych labelled "Under-eye lines −23.4% vs −7.0% with retinol". Until one exists, the current pair stays (it is accurate, only off-question).
- **15.** **The Watanabe diptych barely shows crow's feet** (imagery, for human check). At 330 px per panel the outer eye corner is close to the hairline,
  and the head angle and framing change between panels, so what differs is pose and light. **Spec fix:** crop tighter on the eye corner, as the
  Wang and Ye pairs do, or re-render with a matched pose.
- **16.** **The product block is off-axis, and the PDRN card has no explanation** (layout/copy). The paragraph sits at x 48 while the cards are centred at
  x 272 to 1168. The copy names only the Argireline serum, and the table's footnote says Ye did not test our product, so a reader cannot tell why
  the PDRN serum is shown. **Spec fix:** centre the paragraph on the 56rem axis, and add one sentence about the PDRN serum. Mark it draft for
  Malcolm: for example, it contains PDRN, the Ye ingredient, at another strength and not as an eye cream.
- **17.** **Standalone links are small on a phone** (interaction, for human check). The four "Read our appraisal of …" links are 18 px tall at 390, and the
  "Learn" crumb is 37 x 18 px. **Spec fix:** apply the High 7 rule, including `background-origin:content-box`, to the `proof`, `undereye` and
  `banner` CSS.

## Nits

- The safety item "Pregnant or breastfeeding?" uses a headset icon (`picto-customer-support`).
- The three figures are `<h2>` and their labels `<h3>`, ahead of the first real H2 (heading outline).
- "Read the Trials and the Research" is the only Title Case H2.
- The pills are 10.9 px at 390, and two of them wrap to two lines.
- The eye-bag pair's after panel is framed tighter and lit brighter than the before panel.
- The mobile banner reads as a dark band: mean rgb 52 at 390, including the white type; the desktop ripple side is 39 with std 13. This is
  consistent with the family.
- Site-wide: the 25 px footer overflow at zoom, header icons overlapping the logo at zoom, the 15/14 px body, ten radii and 2.1 MB of weight.

## Open question for Malcolm (not a finding)

Each diptych sits beside its trial's name, its measure and "Before / After N weeks". A reader may take it as a trial photograph. No visible caption
says so, and no disclosure is recommended (decision of 2026-09-22). It is raised only because the brief asked for this check.

## Reference diff

- **Argireline hub:** the hub's proof cards lead with the result and fill the card, and the hub adds a chart and a Shop button. Ours lead with the
  method, leave each card two-thirds empty, and have neither.
- **Wang 2013 article:** Wang has a full breadcrumb, figures on bone, a 19 px standfirst and one centred reading column. Ours drops from the figures into
  15 px bullets and then jumps to the left gutter.
- **Fine Lines & Wrinkles:** that page varies its image subjects and sizes and carries three Shop buttons. Ours repeats five identical diptych squares
  and has no button.

## Signature, tells and cluster

**Signature: none.** The honest "Who paid" column is the most distinctive idea on the page. It is the eighth column, though, and sits 810 px to the
right on a phone.

**Tells of assembly:**

- four identical 660 px diptych squares alternating with mostly empty white cards for 2,872 px;
- links struck through by a fix that nobody looked at;
- six left edges, because each module keeps its own container;
- alt text calling generated images "photographs".

**Cluster:** closest to 4, the theme card kit: rounded 10 px white cards in a checkerboard, with ten radii.

## Single change that most improves the page

Rewrite the proof run to the hub pattern (High 4): a section title, the result as each card's title, and the design and measure in the body. It is a
spec text edit of about 20 minutes, with no new assets, and it turns a quarter of the page from repetition into evidence. Blocker 1 comes first and
takes minutes.

Captures, measurements and references (scratchpad, not committed): `/private/tmp/claude-501/-Users-malcolmsmith-Claude-Code-Projects-skingenetix-website/4237e530-0fcc-4ba5-85dd-7427c7f586ff/scratchpad/cf1/`
(`measure-1440.json`, `measure-390.json`, `dom.json`, `probe.json`, `full-*.png`, `ref-*.png`). Contact sheet: `~/Desktop/learn-crowsfeet-cycle1-renders.png`.
No `scores.csv` exists for this project; the scores are recorded in the table above, as in the sibling page's reports.
