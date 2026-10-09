# Design critic, cycle 1: Learn article redesign (2026-10-09)

**Page:** `/blogs/learn/argireline-and-matrixyl-3000-together?view=learn-argireline-matrixyl-3000` (hidden preview of
`templates/article.learn-argireline-matrixyl-3000.json`, spec `configs/hub-upgrades/learn-argireline-matrixyl-3000-design-2026-10-09.json`).
**Critic:** `design-critic` agent, fresh context, against the reference builds (Argireline hub, Badenhorst study article,
Collagen Skincare). **Disposition: FIX, not REBUILD** (weighted 4.8). Do not switch the article onto this template until blockers 1
and 2 are fixed; then run the critic again (cycle 2). Scores: hierarchy 5.5, rhythm 4.0, imagery 4.5, typography 6.0,
family fit 7.0, mobile 3.0.

## Blockers

1. **Phone page scrolls sideways (evidence table).** At 390 px the page is 740 px wide (545 px over at 200% zoom). The rich-text
   container is a CSS grid, so the table wrapper stretches to the table's 720 px minimum and its own `overflow-x:auto` never acts;
   the caveat, the Dr Bodde reviewer line and the date run off-screen. Fix: give `.sgx-evtable` `min-width:0;max-width:100%`
   (section Custom CSS), or stack the rows as label/value pairs under 700 px.
2. **Step 1 photo carries a watermark.** `skingenetix-howto-step2-serum.jpg` reads "WatativePrext" across the pipette, shows an
   amber oil bottle (not ours), and its alt text is the filename. Not used on any live page (checked 2026-10-09). Fix: a
   frosted-bottle pipette shot already in Files (e.g. `skingenetix-matrixyl-3000-collagen-serum-pipette-drop-forming.jpg`).

## High

- **3.** **Rhythm:** six white 50/50 cards in a row (y 1021 to 5273 at 1440); bone runs unbroken twice (4,413 px, then 3,318 px). Fix the
  backgrounds: together white, tips white, products white, evidence bone, related white (also removes the bone-to-footer seam).
  Turn "Do Argireline and Matrixyl 3000 work together?" into a plain rich-text section (no image) so the before/after cards are
  the first image run. This is the single biggest improvement.
- **4.** **Hierarchy:** on the phone the key figure (46 px) outsizes the H1 (40 px); desktop 50 vs 60; ten H2s at 48 px. Fix: lower the
  impact-text size one step.
- **5.** **Byline buried** at 88% of the page. Fix: one line under the banner subline ("By the Skingenetix Research Team · medically
  reviewed by Dr Esther Bodde · 8 October 2026"); key figures stay directly under the banner.
- **6.** **Both Matrixyl 3D renders may make a claim** (beads beamed through the skin to deep cells: the picture rejected on 2026-09-30
  against the register's "penetrates deep into the dermis" avoid line; both are also live on the Matrixyl research page). Fix:
  use `skingenetix-matrixyl-3000-collagen-matrix-structure-laboratory.jpg` in "Why are they different jobs?"; review the
  together-block render too (human check).
- **7.** **Banner is a black band on the phone** (mean rgb 35,34,35; the silk sits in the left 40% and is cropped out). Fix: a portrait
  mobile image with the silk fold in frame. Text contrast is fine (≥ 9.5:1).

## Medium

- **8.** Related row: two 300×200 and two 300×300 images misalign titles; "Read" links are 34×18 px; at 390 it is an uncontrolled swipe
  strip. Fix: square images, name each link's destination.
- **9.** Image monotony: 14 of 17 images square; the Acetyl bottle appears 6 times; a product beauty shot sits beside the safety copy.
  Fix: "Who should skip" as rich-text with no image.
- **10.** Key figures carry no source links (the study and ingredient pages link "(Wang et al., 2013)").
- **11.** Repetition: "No study has tested the pair" five times before the table; "22 of 45" five times; the "jobs" captions repeat the
  paragraph above. Fix: cut the captions or that paragraph's lead.
- **12.** Type: body 15/14 px (site-wide theme setting; the rule for a 40+ audience is 17–20); lines 81–90 characters (table caveat about
  141; band 50–70); headings mix Title Case and sentence case, centred and left.

## Nits

"Learn" eyebrow is not a link (the study page has a breadcrumb); step 2 is a frequency, not a step; two step images use the
filename as alt text; the red sale badge adds a fourth colour; the forehead before/after model has brown spots on both cheeks
(check against the no-moles rule).

**Signature:** none yet. The honest "0 trials of the two together" could carry it, but it is set as the third of three equal stats.
Tells of assembly: six identical card rows, filename alt text, nearly every image square.
