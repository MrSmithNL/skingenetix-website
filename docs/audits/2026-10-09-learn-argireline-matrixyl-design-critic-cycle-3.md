# Design critic, cycle 3 (final): Learn article redesign (2026-10-09)

**Page:** `/blogs/learn/argireline-and-matrixyl-3000-together?view=learn-argireline-matrixyl-3000` (hidden preview of
`templates/article.learn-argireline-matrixyl-3000.json`, spec `configs/hub-upgrades/learn-argireline-matrixyl-3000-design-2026-10-09.json`).
**Critic:** `design-critic` agent, fresh context. Captured live on 2026-10-09 at 390, 768, 1440 and 200% zoom (195 px), with Klaviyo and Shopify
Forms blocked and loads spaced about 30 s apart. I also ran an unblocked `capture.py` pass and `measure.py` at 1440 and 390, plus a DOM probe.
There is no direction contract for this site (no `website/design/`), so I judged the page against the reference family (Argireline hub,
Badenhorst study article, Collagen Skincare), the skill's craft rules and the store rules in memory.

**Disposition: FIX. There is no blocker, and the loop closes here (cycle 3 is the last).** Cycle 3 is the best-scoring cycle (5.9, up from 5.1
and 4.8), so it is the one to keep. **You can switch the article onto this template once High 1 and High 2 are applied and checked with a
capture.** Neither needs a fourth critic cycle: each is one CSS edit. The Medium items go to the Learn-template backlog for spokes 2 onwards.

| Axis (cycle-1 set) | Cycle 1 | Cycle 2 | Cycle 3 |
| ------------------ | ------- | ------- | ------- |
| Hierarchy          | 5.5     | 5.5     | 6.5     |
| Rhythm             | 4.0     | 6.0     | 6.0     |
| Imagery            | 4.5     | 5.5     | 5.8     |
| Typography         | 6.0     | 5.5     | 6.0     |
| Family fit         | 7.0     | 7.0     | 7.5     |
| Mobile             | 3.0     | 4.0     | 6.0     |

Rubric axes: Design 6.3 (weight 40%), Usability 6.0 (30%, for human check), Creativity 4.5 (20%), Content 7.2 (10%). Weighted total **5.9**
(cycle 2: 5.6 / 4.5 / 4.0 / 7.0 = 5.1).

## Cycle-2 items: status

| #    | Item                                               | Status                                  | Evidence (cycle 3)                                                                                                                                                                                                                                                                                                                                        |
| ---- | -------------------------------------------------- | --------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| B1   | Phone page scrolls sideways                        | **Fixed**                               | `scrollWidth` 390 at 390, 768 at 768, 1440 at 1440 (blocked and unblocked passes). The table now scrolls inside its own 350 px wrapper (its `scrollWidth` is 720). At 200% zoom the page is still 25 px too wide, but the cause is the theme footer: the Argireline hub measures the same 220 px at 195. See High 2 for the new problem inside the table. |
| H2   | Wrong-colour Matrixyl image (j2)                   | **Fixed**                               | `skingenetix-matrixyl-3000-firming-serum-clear-drop-on-cheek-macro.jpg` shows a clear drop (1440, slice 3). Its alt text names the "Full Matrixyl 3000 Ritual - Serum & Cream", which is not in the picture (Nit).                                                                                                                                        |
| H3   | Key-figure scale                                   | **Fixed**                               | Figure over label is 44/20 px at 1440 and 768 (2.2x), and 32.5/20 px at 390. Every figure sits below the H1 (60/48/40 px). The figures are now teal #016569.                                                                                                                                                                                              |
| H4   | Reading sections hug the left edge with long lines | **Mostly fixed**                        | Characters per line at 1440, counted from line boxes: together 65–75, caution 65–73, jobs 65–70, layering 63–69, answer 51–64 (cycle 2: 93–104). What remains is the left-edge problem in Medium 3.                                                                                                                                                       |
| M5   | No primary action                                  | **Fixed**                               | Teal "Shop the Peptide Duo Set" button, 263×58 at 1440 (y 1507) and 235×54 at 390 (y 2060). It is not in the first 390 screen (Nit).                                                                                                                                                                                                                      |
| M6   | No ingredient accent                               | **Fixed**                               | Teal on the figures, the button, and the links in the answer, together, caution and evidence sections (8 elements). The proof-card links and related links are still ink #1A1A1A (Nit).                                                                                                                                                                   |
| M7   | Image run at 390, equal pair at 1440               | **Not fixed**                           | 21 of 22 content images are still square. The jobs pair is still two 648 px squares side by side. At 390 there are still eight full-column 350 px squares between y 3,016 and y 8,579.                                                                                                                                                                    |
| M8   | Repetition                                         | **Partly fixed**                        | The jobs captions are cut (fixed). "22 of 45" still appears 6 times in the text, plus once on the image label, and the proof-card title still carries it. "Not tested together" is still said 6 ways.                                                                                                                                                     |
| M9   | H1 breaks mid-word at 200% zoom                    | **Fixed, but the same fault has moved** | The H1 is 28 px and no longer breaks. The answer card, proof cards and button now break mid-word instead (Medium 1).                                                                                                                                                                                                                                      |
| M10  | Mixed heading case                                 | **Fixed**                               | Every heading is in sentence case. Alignment is still mixed: centred for the figures, "What the trials measured" and "Before you start"; left everywhere else.                                                                                                                                                                                            |
| M11  | Related links 18 px tall                           | **Fixed in size, with a new fault**     | The links are now 48 px tall at 390 and 50 px at 1440, but the underline now runs through the letters (High 1).                                                                                                                                                                                                                                           |
| Nits | Byline middle dots                                 | **Fixed**                               | The byline now uses commas. Still open: step-2 alt is the filename ("skingenetix howto step3 moisturise"), the "Learn" label is not a link, the red sale badge, the spots on the Raikou model (human check), 10 radii (theme), header overlap at 200% zoom (theme).                                                                                       |

## High

1. **Related links look struck through, on every width** (typography / interaction). This is a new fault, caused by the cycle-2 tap-target fix. The theme draws the
   underline as a background image at `background-position: 0 min(100%, 26.87px)` from the padding box. With the new 13 px top padding, the line now lands
   about 1.5 px above the baseline at 390 (0.7 px at 1440), so it cuts through the letters. All four "Read the …" links read as deleted text (crop
   `z-rel390.png`; 1440 slice 5). **Spec fix (related `custom_css`):** `a{display:inline-block;padding-block:13px;background-origin:content-box}`. That keeps
   the 48 px target and puts the line under the descenders. Check it with a capture.
2. **On the phone, the evidence table hides its Result column** (interaction, for human check). At 390 the 720 px table scrolls inside a 350 px box. The Length,
   What was measured and Result columns sit at x 386–740, off-screen. The only hint that the table scrolls is a 16 px clipped sliver of "People". So the pair
   row reads "None exists / –", and its answer, "Not tested", is out of view. At 200% zoom, 2 of the 6 columns show. **Spec fix (evidence `custom_css`):** add
   `@media(max-width:699px){.sgx-evtable table{min-width:0}.sgx-evtable :is(th,td):nth-child(n+3):not(:last-child){display:none}}`. That shows Ingredient,
   Trial and Result; the proof cards already give people, length and measure. To stay under the 500-character limit, delete
   `.sgx-evtable th{font-weight:600;background:#F0F0F0}`: the background matches the section's and headers are bold by default.

## Medium

1. **At 200% zoom, the short-answer card, the proof cards and the CTA break mid-word** (typography). "The short answe/rs", "Forehea/d roughne/ss", and the button
   splits into "Sho/p/the/Pep/tide/Du/o/Set" (91×211 px, `zoom-sheet0.png`). There are two causes. First, 32 px of card padding leaves 91 px for text.
   Second, the theme's `break-all` class sits on the answer prose. **Spec fix:** in answer, add
   `@media(max-width:320px){.media-with-text__content{padding:24px 16px}.prose{overflow-wrap:normal;word-break:normal}}`; in proof, add
   `@media(max-width:320px){.rba__text{padding:24px 16px}}`.
2. **The images are still almost all square** (imagery). This is cycle-2 M7, unchanged. The Collagen reference mixes its crops. **Spec fix:** as in cycle 2,
   re-crop the jobs pair to 4:5 and the steps to 3:2, with new file stems.
3. **The reading column's left edge wanders at 1440** (layout/spacing). Text blocks start at x 48 (jobs, layering, products, evidence, related), x 428 (together,
   caution), x 812 or x 128 (cards), or centred (two headings). Beside "Why are they different jobs?", "Which goes first" and "What do our products contain?",
   the right 55% of the screen is empty (slices 2–4). The Badenhorst reference holds one centred column. **Spec fix:** in jobs, layering and products,
   replace `p,ul{max-width:65ch}` with `.section-header .prose{max-width:65ch;margin-inline:auto}`.
4. **Every section has the same padding** (layout/spacing). 80/80 px on all 11 body sections at 1440 and 40/40 at 390; `measure.py`
   `distinctSectionPaddings` reports 1 (rule 23). Nothing dominates, and the "0" gets no moment of its own. **Spec fix:** give the figures section 128 px
   and the tips section 48 px, through each section's `custom_css` `.section{padding-block:…}`.
5. **Repetition** (copy). This is cycle-2 M8, still partly open. **Spec fix:** proof-card title "Crow's feet graded clearly smoother in 4 weeks".

## Nits

At 768 the layering row is a swipe strip that cuts off step 3, and "Before you start" leaves its third item alone on a row. At 200% zoom the
product-card titles are clipped ("Hexapept", "€44,0C"), which is theme-wide. The CTA is not in the first screen at 390 (rule 47). Body text is 15/14 px,
theme-wide (rule 10). The page weighs 2.1–2.4 MB, with 839 KB of script, theme-wide (rule 53). The display-to-body ratio is 2.86 at 390 (rule 4).
The table caveat runs about 150 characters on one line at 1440.

## Reference diff (390 and 1440)

- **Argireline hub:** the modules and teal accent now match, but the hub ends on a full-width CTA band, and ours ends on a related strip with
  struck-through links.
- **Badenhorst study:** it keeps one centred column and one chart as its dominant visual; ours moves its left edge three times and has no
  dominant moment.
- **Collagen hub:** it mixes the crops of its product, texture and before/after images; ours sets 21 of 22 images square.

**Signature:** none yet. The honest "0 trials of the two together" is now teal, but it is the same size as the other two figures and comes third.
**Generated tells:** square-everything imagery, one section padding, a left edge that wanders. **Cluster:** none. The page is in the store's own
family, which is correct for this site.

**Single change that most improves the page:** High 1 plus High 2, two CSS edits (about 10 minutes plus one capture). After them the template
can replace the stock article.

Captures and measurements (scratchpad, not committed): `/private/tmp/claude-501/-Users-malcolmsmith-Claude-Code-Projects-skingenetix-website/4237e530-0fcc-4ba5-85dd-7427c7f586ff/scratchpad/c3/`
(`shots/`, `cap/`, `measure-1440.json`, `measure-390.json`, `probe2.json`). Contact sheet: `~/Desktop/learn-spoke1-cycle3-renders.png`.
No `scores.csv` was written: this site has no `website/design/` directory, which follows cycles 1 and 2.
