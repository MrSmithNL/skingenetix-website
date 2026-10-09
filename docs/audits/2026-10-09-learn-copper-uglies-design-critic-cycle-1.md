# Design critic, cycle 1: Learn article "Copper uglies" redesign (2026-10-09)

**Page:** `/blogs/learn/copper-uglies-what-they-are-and-how-long-they-last?view=learn-copper-uglies` (hidden preview of
`templates/article.learn-copper-uglies.json`, spec `configs/hub-upgrades/learn-copper-uglies-design-2026-10-09.json`).
**Critic:** `design-critic` agent, fresh context. Captured live on 2026-10-09 at 390, 768, 1440 and 200% zoom, with Klaviyo and
Shopify Forms blocked and the cookie banner hidden, loads spaced about 30 s apart. `measure.py` was run at 1440 and 390, and
`capture.py --zoom` was run as well. The page was compared with the copper hub (`/pages/copper-peptide-research`, captured
today), the Badenhorst study article and Collagen Skincare (cycle-2 captures from today).

**No direction contract exists** (there is no `website/design/` and no `02-reference-rules.md`). So the page is judged against
the reference family, the skill's craft rules and the store rules in memory, as the sibling cycles were.

**Disposition: FIX** (weighted **5.3**). **Do not switch the article onto this template until B1 and B2 are fixed**, then run cycle 2.

| Axis                        | Weight | Score   |
| --------------------------- | ------ | ------- |
| Design                      | 40%    | 5.4     |
| Usability (for human check) | 30%    | 5.5     |
| Creativity                  | 20%    | 4.0     |
| Content                     | 10%    | 7.0     |
| **Weighted**                |        | **5.3** |

The generic fixes from the sibling page's cycle 2 landed as follows. The table parent shrinks (scrollWidth 390 at 390, 768 at
768, 1440 at 1440). The figure leads its label (44/20 px). The byline uses no middle dots. Body links use #014EB1. Related links
are 46 to 48 px tall. Two of the generic fixes created new faults, though: see H4 and M1.

## Blockers

**B1. The purging image is a mustard-amber swirl on black marble, and it carries our copper night cream's name.** Classes: imagery, copy.

- **Where:** the purging section, left 45% (648×824 at 1440; a full-width 390 px square at 390).
- **What is wrong:** the file is `skingenetix-copper-peptide-night-cream-texture.jpg`. The night cream's substance is **light blue
  `#A6C4E0`** (product-colours register, confirmed by Malcolm 2026-08-20), and every other copper image on the page is blue.
- **Why it matters:** its alt text is the filename, "copper peptide night cream texture". So a screen reader or an AI extractor
  reads our named product directly beside the heading "What causes copper uglies". That is an image making a claim. On a page about
  skin looking worse, the shape also reads as the swirl emoji.
- **Smaller fault:** it is drawn 824 px tall from a 648 px source, a 1.27× upscale.
- **Fix:** set block `m` to `copper_peptide_ghk_cu_2_percent_advanced_repair_skin_serum_macro_dropper_tip_gel_1_skingenetix.jpg`
  (an unlabelled clear gel leaving a dropper on a pale ground; checked by eye). Give it the alt text "A clear gel drop leaving a
  glass dropper".
- **What not to use:** the labelled night-cream jar swatch. It would put our product beside "causes" in plain sight.
- **Alternative:** remove the image and make `purging` a plain rich-text section. One image band is enough on this page.

**B2. The page scrolls sideways at 200% zoom.** Classes: interaction, reflow. For human check.

- **Evidence:** at a 195 px viewport the scrollWidth is 250, and `capture.py` reports `overflowX` 55. The overflow is 0 at 390, 768 and 1440.
- **Where:** the evidence table. Its "What was measured" column is clipped (`full-390x200pct.png`, at about y 7,500 to 8,800).
- **Rules broken:** WCAG 1.4.10 and craft rule 54.
- **Cause:** two 50% columns with 14 px side padding and words like "construction”" need about 209 px, and only 155 px is available.
- **Why the fix goes in the liquid block:** the `online` Custom CSS is already about 414 characters, so the new rules cannot fit
  there. Put a `<style>` element inside the `t` liquid block instead:
  `.sgx-evtable{overflow-x:auto}@media(max-width:320px){.sgx-evtable thead{display:none}.sgx-evtable td{display:block;width:auto;padding:6px 0;border:0}.sgx-evtable td:first-child{font-weight:600;padding-top:14px}}`
- **Also:** drop the duplicate `.prose>div{…}` rule, because `.prose>*` already covers it.
- **Check before calling it fixed:** scrollWidth must be 195 at 195.

## High

**H1. The key figures are outranked.** Class: hierarchy.

- **Evidence:** section H2s are 48 px against figures of 44 px at 1440, and 32 px against 32.5 px at 390. Twelve H2s are set at
  3.2× body inside an article; craft rule 3 puts the band at 1.5 to 2.4×.
- **The family does the opposite:** the hub measures figures of 50.4 px over H2s of 38 px at 1440, and 45.5 over 28 at 390.
- **Why it matters:** the "0", the page's only candidate signature, is smaller than "Frequently asked questions".
- **Fix:** add `h2{font-size:28px}@media(min-width:700px){h2{font-size:38px}}` to the Custom CSS of every rich-text,
  media-with-text, faq and multi-column section. This matches the hub, and it also cures the mid-word break in M4.

**H2. The H2s start from four different left edges at 1440:** x 48 (four times), 80, 428 (six times) and 728 (twice). Class: layout.

- **The table section hugs the left gutter:** its heading and its 780 px table leave the right 45% of the screen empty (slice
  y 3,776). This is cycle-2 High 4 again, because `online` never got the wrapper rule.
- **The two icon-row headings sit off their items:** the headings are in the centred column at x 428, while their items run from
  x 48 to 1392.
- **Fix:**
  - `online`: add `.rich-text__wrapper{max-width:720px;margin-inline:auto}`.
  - `react_h` and `safety_h`: delete the 65ch rule and set `content_width` to `large`, so that each H2 starts at x 48 with its items.

**H3. The page's only commercial step is a lone 318 px product card.** Classes: layout, interaction.

- **Evidence:** at 1440 the card sits at x 48 to 366 with 1,026 px of empty row beside it. At 768 it fills half a row.
- **No buttons:** the page has none. The only `<button>` elements are Subscribe and English.
- **The family:** the hub closes on "Shop Copper Peptide Serum". Badenhorst closes "What it means for our products" on two buttons.
- **Fix:** replace `products` with a rich-text section (content_width small, background white). It keeps the same sentence and
  adds a `button` block, "See the Copper Peptide Serum", linking to `/products/copper-peptide-ghk-cu-renewal-serum`. That gives the
  page one quiet action (craft rule 46).

**H4. The middle "Read the evidence" card shows grey bands, at every width.** Classes: imagery, interaction.

- **Evidence:** there are 13 px bands above and below the image. The anchor measures 416×442 against a 416×416 image, and only this
  image is dimmed.
- **Cause:** the cycle-2 tap-target rule `a{display:inline-block;padding-block:13px}` also pads the tile anchor `a.sgx-research-tile`.
  The site script `scripts/research-related-tiles.py` gives tiles linking to `*-research` pages a 22% ink overlay, and that overlay
  paints the padding.
- **Fix:** replace the rule with `.v-stack a{display:inline-block;padding-block:13px}`. The `.prose a.link` rule already covers the
  text links.
- **Fix it at the source too:** make the same change in scratchpad `learn_design_fixes.py`, line 53. The bare rule is in all four
  Learn specs (Argireline, salmon, crow's feet, copper).

## Medium

**M1. Line length is still out of band.** Class: typography.

- **What the cap gives:** "65ch" gives 78 to 82 characters per line, because `ch` is the width of a "0" in Muli (about 9 px).
  The 585 px column fits 82 characters on "The question behind…".
- **Uncapped text:** media-with-text text runs 84ch (632 px), and the banner subline runs 104 characters at 1440.
- **The band:** 50 to 70 characters, and 65 or fewer for a sans face (craft rule 10).
- **Fix (in the spec and in `learn_design_fixes.py` line 48):**
  - Replace `65ch` with `480px`.
  - Media-with-text sections: `.prose{max-width:480px}`.
  - Banner: `.prose p{max-width:560px}`.

**M2. Every section has the same weight.** Class: layout/spacing.

- **Evidence:** 15 of 18 sections open and close at exactly 80 px, measured as the offset of the first content in the DOM.
  (`measure.py` reports 0 because the theme pads `.section`, not the section element.)
- **Fix:** give the two evidence moments 120 px: `.section{padding-block:120px}` in the `figures` and `online` Custom CSS.

**M3. The two icon rows repeat each other.** Classes: copy, components.

- **Repeated items:**
  - "If a reaction persists" says "See a pharmacist or dermatologist if a reaction persists". That repeats its own title, and react
    item t3 as well.
  - "Patch-test" appears three times.
  - "Strong actives at another time" repeats the routine paragraph.
- **Icons:** four of the five safety icons reuse the react row's icons. A headset for "Ask a pharmacist" reads as a call centre.
- **On the phone:** at 390 the two rows stack nine centred items over 1,958 px, which is 16% of the page.
- **Fix:** keep `react` as the page's one icon row. Turn `safety` into a bulleted rich-text list in the reading column, and drop
  items s4 and s5.

**M4. Two things break at 200% zoom.** Class: typography.

- **Mid-word break:** the purging H2 splits as "guesswo / rk". H1 cures this.
- **Inverted figure:** the key figure is 19.5 px under a 20 px label.
- **Fix:** in `figures`, add `@media(max-width:320px){h3.h4{font-size:16px}}`.

**M5. The banner's pipette runs behind the type.** Class: imagery.

- **Where:** at 1440 the pipette sits at x 680 to 760, behind the H1, the subline and the byline. At 390 it is centred under the
  centred type.
- **Family fit:** the image is the Matrixyl comparison file, and its saturated flat blue reads as a different family from the dark
  lab banners on the hub and Badenhorst pages.
- **Fix (desktop):** `@media(min-width:1000px){.prose{max-width:600px}}` keeps the text block clear of the pipette.
- **Phone:** for human check.

**M6. Body text is 15 px on desktop and 14 px on the phone** for an audience aged 40 and over. Craft rule 10 asks for 17 to 20 px.
Class: typography.

- **Scope:** this is a theme-wide setting, carried over from cycles 1 and 2, so it is a decision for Malcolm.

**M7. The page repeats its few facts.** Class: copy.

- **"39 of 40":** appears four times. The intro sentence repeats the figure label word for word, directly under it.
- **The one woman's reaction:** the single case is told five times.
- **"Pharmacist or dermatologist":** appears four times, plus three variants.
- **Fix:** cut the intro's first sentence and the body text of figure 3.

## Nits

- **Eyebrow:** "Learn" sits above the H1 (craft rule 44) and is not a link. The Badenhorst page uses a breadcrumb here.
- **Link colour:** the key-figure links and the product-copy link are ink, not #014EB1.
- **Alt text:** the purging image's alt text is its filename.
- **Tablet swipe strip:** at 768 the related row is a swipe strip, and the third card is cut off at x 712 with nothing to show it scrolls.
- **Radii:** nine radii, set by the theme (the 12 px card, 10 px images and 6 px tile disagree).
- **Header at 200% zoom:** the header icons overlap the logo. This happens on every page.
- **Skin-concerns tile:** it shows a hand pressed to a freckled cheek. On a reactions page it can read as someone hiding a reaction
  (human check; it does not break the register). It is also not evidence, but it sits under "Read the evidence".

## Imagery without before/after

There are enough images for the page: the banner, two image bands, the product card and three tiles. The problem is that none of
them carries evidence. The family draws Badenhorst as a bar chart; this page draws nothing. No image pictures a mechanism or a
result. The only image that makes a claim is B1.

## Reference diff

- **Copper hub:** its figures dominate its headings (50.4/38 px), its evidence is drawn as a chart, and it closes on a shop button.
  Ours inverts the scale (44/48 px), hugs a table to the left and has no button.
- **Badenhorst study:** a breadcrumb and a dark lab banner with the subject clear of the type place the reader in the science
  section. Ours has an unlinked eyebrow and puts the pipette under the H1.
- **Collagen Skincare:** every texture shot matches the product's real colour. Our only texture shot is amber, against a light-blue cream.

## Answers

1. **Signature:** none. The "0 studies" figure or the online-versus-measured table could carry the page, but both are set at default
   weight. (Creativity 4.0.)
2. **Tells of assembly:**
   - one 80 px spacing on 15 of 18 sections;
   - two icon-in-circle rows with repeated items;
   - filename alt text on the only texture image, plus a single product card stranded in a four-across row.
3. **Cluster:** closest to cluster 4, the theme kit: icon-in-circle feature rows, a rounded white card and one rhythm throughout.
4. **Weighted 5.3, FIX.**

**Single change that most improves the page:** B1, the swap of the purging image. It is one setting and takes minutes, and it
removes the one thing a director would reject on sight. H1 comes next: about 56 characters of CSS per section restores the hierarchy.

No `scores.csv` was written, because no `website/design/` structure exists and the sibling cycles did not create one.
Captures and measurements (scratchpad, not committed):
`/private/tmp/claude-501/-Users-malcolmsmith-Claude-Code-Projects-skingenetix-website/4237e530-0fcc-4ba5-85dd-7427c7f586ff/scratchpad/cu1/`.
Contact sheet: `~/Desktop/learn-copper-cycle1-renders.png`.
