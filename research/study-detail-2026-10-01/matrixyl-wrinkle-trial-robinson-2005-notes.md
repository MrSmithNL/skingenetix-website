# Robinson 2005: results and how-it-works blocks (notes)

**Study:** Robinson LR et al., 2005, _Int J Cosmet Sci_ 27(3):155–160, PMID 18492182. Palmitoyl pentapeptide-4 (pal-KTTKS, the original
Matrixyl®) at 3 ppm in a moisturiser, against the same moisturiser without it. Split-face, double-blind, 93 women, 12 weeks, Procter &
Gamble. **Config:** `configs/studies/matrixyl-wrinkle-trial-robinson-2005.json`. The brief named `configs/studies/drafts/…`; the worktree
merged `main` while I worked, and the file moved there when the article went live at 16:05. The content is identical; I diffed it.
**Register:** `docs/claims/matrixyl-3000.md` (§1 claims 2, 4 and 6; §4 avoid list; §8.4 wording rules; §8.5 card f2). **Output:**
`matrixyl-wrinkle-trial-robinson-2005.json` (same folder). **Date read:** 2026-10-01.

## 1. What I read, and how

| Source                                                                     | Access                                                                                                       | What it gave                                                                                                                                                                                                                                                                                                |
| -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Robinson 2005, the abstract (NCBI efetch)                                  | Abstract only. The full text is paywalled: Wiley, Unpaywall "closed" (per the config `_note`, 2026-09-30)    | Design, n, ages, 3 ppm, 12 weeks; "significant improvement vs. placebo control for reduction in wrinkles/fine lines by both quantitative technical and expert grader image analysis"; self-assessed fine lines significant; "directional effects for other facial improvement parameters"; "well tolerated" |
| Aldag et al. 2016, CCID 9:411, PMC5108505                                  | Full text (Europe PMC XML)                                                                                   | The −4 to +4 blinded expert scale and its five features. Significance was counted at p ≤ 0.10. Weeks per result, and which results also pass p ≤ 0.05. Merz-funded                                                                                                                                          |
| Abu Samah & Heard 2011, IJCS 33:483                                        | Full text, read in a browser at Wiley (curl gets a 403)                                                      | Two-week washout; REAL 1.0 photographs at weeks 0, 4, 8 and 12; P&G algorithms for the crow's-feet area and the cheek; a blind-coded "Visual Perception Study"; "small, but … significant at weeks 8 and 12"; Katayama's method in summary; no detectable permeation in their own laboratory (unpublished)  |
| Gorouhi & Maibach 2009, IJCS 31:327, PMID 19570099                         | Full text, read in a browser at Wiley                                                                        | Age spots: "significantly better scores than placebo for expert grader assessment and subject self-assessment" (text and the controlled-trials table)                                                                                                                                                       |
| CIR 2012 literature review, "Safety Assessment of Palmitoyl Oligopeptides" | Full PDF                                                                                                     | p. 7: ~0.4 g per side, no irritation, "small, but … significant at weeks 8 and 12"; self-assessed age spots, dark circles and firmness "significant at week 12"                                                                                                                                             |
| CIR 2024 final report, pentapeptide-4                                      | Full PDF                                                                                                     | p. 6: did not permeate full-thickness hairless-mouse skin. p. 5: highest leave-on use in face and neck products is 0.0012%                                                                                                                                                                                  |
| **Katayama et al. 1993**, J Biol Chem 268:9941, PMID 8486721               | **Full text (4-page PDF, open access at jbc.org, fetched in a browser).** The register had the abstract only | See §2                                                                                                                                                                                                                                                                                                      |
| **US 6,974,799 B2** (Lintner, Sederma)                                     | Full text, Google Patents                                                                                    | Table 1: the pal-KTTKS dose series, and the method below it                                                                                                                                                                                                                                                 |
| **de Mello et al. 2026**, J Pept Sci 32:e70111, PMC13280649                | Full text (Europe PMC XML)                                                                                   | Collagen per cell in adult human dermal fibroblasts; methods, statistics, funding                                                                                                                                                                                                                           |

**Identifiers checked** (NCBI esummary for PubMed and PMC; Crossref for DOIs). Each resolves to the paper named beside it: 18492182
(Robinson), 8486721 (Katayama), 19570099 (Gorouhi), PMC5108505 (Aldag), PMC13280649 (de Mello), 10.1111/j.1468-2494.2011.00657.x (Abu
Samah), and US6974799B2 (title "Compositions containing mixtures of tetrapeptides and tripeptides"; Lintner and Sederma SA; granted
2005-12-13).

I also ran the builder's own `check_detail()`. With "TBD" images it fails only on the image names, as expected, because "TBD" contains no
ingredient name. With the suggested filenames it passes, both with and without the pending item, and with the pending item's before/after
option.

## 2. Source table: every number to where I read it

| Number or fact used                                                                                                                                            | Where it appears | Source and location                                                                                                 |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------- | ------------------------------------------------------------------------------------------------------------------- |
| Five features (texture, fine lines and wrinkles, age spots, dark circles, firmness), scored −4 (much worse) to +4 (much better) by blinded experts             | o1, o2, pending  | Aldag 2016, the "Lysine–threonine–threonine–lysine–serine pentapeptide (KTTKS)" section                             |
| Photographs coded so graders could not tell the sides apart ("treatment blind-coded … Visual Perception Study")                                                | o1               | Abu Samah 2011, the clinical paragraph of the palmitoyl-KTTKS section                                               |
| Age spots better on the peptide side at **week 12, p ≤ 0.05**                                                                                                  | o1               | Aldag 2016, same section ("only skin texture at 4 weeks and age spots at 12 weeks were significantly better")       |
| Graders' and women's age-spot scores both significantly better                                                                                                 | o1               | Gorouhi & Maibach 2009, the Pal-KTTKS paragraph and the controlled-trials table row                                 |
| Texture better at **week 4, p ≤ 0.05**; still ahead at week 8 at p ≤ 0.10                                                                                      | o2               | Aldag 2016, same section                                                                                            |
| Texture was the only feature ahead at week 4                                                                                                                   | o2               | Aldag 2016. At either threshold, nothing else is listed at week 4                                                   |
| Photographs at weeks 4, 8 and 12 (and baseline)                                                                                                                | o2               | Abu Samah 2011                                                                                                      |
| Fine-line length (computer) and graded fine lines better at **weeks 8 and 12, p ≤ 0.10**                                                                       | pending          | Aldag 2016                                                                                                          |
| Computer measured the "total linear depression area around the eye (crow's feet area)"; total length of lines                                                  | pending          | Abu Samah 2011; Aldag 2016                                                                                          |
| Women's self-assessed fine lines significant                                                                                                                   | pending          | Robinson 2005 abstract                                                                                              |
| Effect "small"                                                                                                                                                 | pending          | CIR 2012 p. 7; Abu Samah 2011                                                                                       |
| Procollagen end pieces "cleaved off extracellularly by specific peptidases"                                                                                    | m1               | Katayama 1993 p. 9941, introduction                                                                                 |
| Fragments K1–K12 tested; KTTKS (K10, residues 212–216) the smallest active one, with 80% of the activity                                                       | m1               | Katayama 1993 p. 9942, Results; Fig. 1A                                                                             |
| Cells: human lung fibroblasts (HFL-1), subconfluent, in culture wells                                                                                          | m1               | Katayama 1993 p. 9941–9942, Experimental Procedures                                                                 |
| Collagen and fibronectin production raised                                                                                                                     | m1               | Katayama 1993 abstract; Fig. 1                                                                                      |
| Feedback idea ("implicated in feedback regulation of their own synthesis"; "We postulate…")                                                                    | m1               | Katayama 1993 abstract                                                                                              |
| pal-KTTKS in normal human skin fibroblasts, 3 days, against the solvent (0.08% DMSO), ELISA, n = 3                                                             | m2               | US 6,974,799, the paragraph under Table 1                                                                           |
| Collagen I +8% / +30% / +48% / **+93%** at 1 / 2 / 4 / **8 ppm** (8 ppm is the highest dose tested); fibronectin **+100%** at 8 ppm                            | m2               | US 6,974,799, Table 1, "Pal KTTKS" rows                                                                             |
| Adult human dermal fibroblasts (HDFa), 72 h; picrosirius red dye; collagen per cell significantly higher at 0.0031 and 0.0062 wt% than in medium-only controls | m2               | de Mello 2026, §2.7, §2.9, §3 and Fig. 7 (Kruskal–Wallis with Dunn's correction, n = 3, \* p ≤ 0.05, \*\* p ≤ 0.01) |
| Funded by EPSRC EP/V053396/1; no conflicts                                                                                                                     | m2               | de Mello 2026, Funding and Conflicts                                                                                |

**Deliberately not used:**

- **Collagen IV +22%** (patent). It adds nothing to the block.
- **de Mello's cytotoxicity at higher doses.** The block reports positive results only.
- **Katayama's "no response in confluent cells".** Same reason.
- **CIR 2024's "0.6% of the applied peptide reached the mouse dermis".** It is a penetration fact (register §4), and it must never appear.
- **Jones 2013** (Mol Pharm). Aldag cites it, but I did not read its full text, so it is not cited.

## 3. Results (outcomes): what is proposed, and why

| Slot                | Result                                                                          | Bar                                                                      | Before/after         |
| ------------------- | ------------------------------------------------------------------------------- | ------------------------------------------------------------------------ | -------------------- |
| o1                  | The look of age spots improved more than with the plain moisturiser, by week 12 | p ≤ 0.05, blinded experts; the women's own scores agreed                 | No                   |
| o2                  | Skin texture looked better than with the plain moisturiser at week 4            | p ≤ 0.05, blinded experts                                                | No                   |
| `_pending_items[0]` | Fine lines and wrinkles reduced more, from week 8                               | **p ≤ 0.10 only**, marked `"_pending": "p<=0.10 — Malcolm's decision 2"` | No (option recorded) |

**Why age spots come before texture.** Both clear p ≤ 0.05, and neither has a published size. Age spots win on corroboration:

- it was significant at the trial's end point (week 12);
- two kinds of assessor agree, the blinded graders and the women themselves (Gorouhi; CIR 2012).

Texture is the earlier result (week 4), but only the graders measured it, and it reached p ≤ 0.05 at one check-up.

**Where the pending item goes.** It sits in `outcomes._pending_items`, not in `items`. If underscore keys are stripped recursively, it
cannot go live by accident. If Malcolm approves p ≤ 0.10, insert it as `items[0]`. It is then the strongest result:

- it is the trial's own question;
- two independent methods agree at two check-ups;
- the women's self-assessment was significant.

The order becomes fine lines, age spots, texture (3 of the 4 slots).

**Not proposed: dark circles.** They pass only p ≤ 0.10, at one check-up (week 12). Even under a "yes" to p ≤ 0.10 they are weak; the chart
already shows them.

**Texture paragraph 2 mentions week 8 at p ≤ 0.10**, labelled with its bar, as time-course depth. If Malcolm rules against p ≤ 0.10 anywhere
on the page, delete that one sentence.

**Wording.**

- Every "significant" or "better" carries its threshold (claim 6).
- Pentapeptide-4 is named as the subject, there is no "independent", and there is no percentage (claim 2 conditions).
- No product is named in the result blocks: the serum-only condition is already handled by the FAQ and "What it means".
- "Age spots" is the cosmetic term already live on the page ("The look of age spots"). I avoided "lighter", "dark spots" and "even tone",
  even though those are glutathione's rules, not this register's.

### Before/after reasoning (the lead's "none": confirmed)

- **o1, age spots.** Visible on a face, yes, but no source gives the size, so no picture can be checked against §3.1's "does not exceed the
  result". No hub picture exists for this result either. The Matrixyl hub's card-f2 brief (register §8.5) explicitly forbids any change in
  age spots. A pigment pair would also invent a tone change, the same failure the before/after doc (§3) calls "lighter-skinned".
- **o2, texture.** Texture is a fine-grain feature. A pair would have to exaggerate it to be visible at web size (before/after doc §3:
  "there must be a visible improvement"). With no size known, any visible change exceeds what we can show. **No.**
- **Pending, fine lines.** The draft Matrixyl 3000 hub's card f2 is this trial. Malcolm ruled on 2026-09-26 that it is "shown as a modest
  change", and its pair still waits for his pick from wave r1 (`configs/banners/before-after-matrixyl-cards-r1.json`, slots d–f;
  `docs/todo.md`). Template §3.1 says to reuse the hub picture first. I still recommend **no**:
  - §3.1 also requires that the picture's change not exceed the result, and with no size published that check is impossible;
  - this article's own "How to read this result" says no size is known, so a labelled pair on the same page would contradict it.

  The option is recorded in `_before_after_option`: `after` "After 12 weeks", `result` "Fine lines reduced more than placebo (p ≤ 0.10)", 47
  characters. It passes the builder.

**Plain images** (`_image_brief` in the JSON). None of them show people, branding, text, diagrams or anything travelling into skin. Each
suggested filename carries "palmitoyl", as the builder requires.

| Slot    | Picture                                                                                                      |
| ------- | ------------------------------------------------------------------------------------------------------------ |
| o1      | An empty facial-imaging station                                                                              |
| o2      | Two identical unlabelled moisturiser bottles (the split-face pair), different from the story's cream-on-teal |
| Pending | A camera lens on an imaging mount                                                                            |
| m1      | Glass cell-culture flasks                                                                                    |
| m2      | A 24-well culture plate (the plate the patent used)                                                          |

These five images fit the review pack's "photographs of the instruments" item, which still waits for Malcolm's approval and a budget.

## 4. How it works (mechanisms): two blocks, each line checked against the register

Robinson had no laboratory arm, so both blocks come from cited laboratory studies that I read in full. Both carry `"evidence": "laboratory"`
and say "In the laboratory" in their text. Neither links a cell result to the women's skin or to our serum. Neither says stimulate, boost,
rebuild or repair, and neither says anything about penetration.

### m1: "A five-amino-acid piece of procollagen raised collagen in lab-grown cells" (Katayama 1993)

| Sentence                                                                                                                                                                                             | Register line that allows it                                                                                                                                                                                                                                               |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Title                                                                                                                                                                                                | §4: "Allowed: 'in lab tests on skin cells, … raised collagen I'". It says "lab-grown cells", **not "skin cells"**, because Katayama's KTTKS work used human lung fibroblasts (see flag F8)                                                                                 |
| "Collagen starts as a longer molecule, procollagen, and as it is made, enzymes trim pieces off both ends."                                                                                           | §8.4: "Write 'a piece cut from procollagen as collagen is made' … not 'released as collagen is broken down'"                                                                                                                                                               |
| "In the laboratory, researchers at the University of Tennessee cut one end piece into ever shorter fragments and tested each on fibroblasts, the cells that make collagen, grown in culture dishes." | §8.4: "Katayama: 'fibroblasts, the cells that make collagen, grown in the lab'"                                                                                                                                                                                            |
| "The shortest fragment that still worked was five amino acids long (KTTKS)."                                                                                                                         | §3 row 14: KTTKS is the "minimum sequence necessary…"                                                                                                                                                                                                                      |
| "It raised the cells' production of collagen and of fibronectin, a protein that helps cells anchor to the collagen network."                                                                         | §4 allowed form ("in lab tests … raised collagen"), with the laboratory framing set in sentence 2 of the same paragraph; claim 4 condition (c) "collagen language reports the lab study"                                                                                   |
| "The authors proposed that these trimmed-off pieces act as a signal telling cells to make more collagen."                                                                                            | §8.4: "the authors proposed that such pieces tell cells to make more"                                                                                                                                                                                                      |
| "Palmitoyl pentapeptide-4 is that same five-amino-acid sequence with palmitic acid, a fatty acid, attached, and it was designed around this laboratory finding."                                     | The live definition says "five amino acids from type I procollagen joined to palmitic acid". The Robinson abstract says it "was designed as a topical agent to stimulate collagen production"; that is the designers' intent, and our sentence does not repeat "stimulate" |

### m2: "With its fatty-acid tail, it raised collagen in lab tests on human skin cells" (Sederma patent; de Mello 2026)

| Sentence                                                                                                                                                                                                                                                                                                                   | Register line that allows it                                                                                                                                                                                                             |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Title                                                                                                                                                                                                                                                                                                                      | Claim 4 condition (a): "'in lab tests on skin cells' must stay in the sentence". The patent and de Mello both used human **skin** fibroblasts                                                                                            |
| "In the laboratory, Sederma, the company that sells palmitoyl pentapeptide-4 as Matrixyl®, gave it to human skin fibroblasts for three days."                                                                                                                                                                              | Claim 4 fact: "normal human skin fibroblasts, 3-day contact"; the manufacturer is named, as on the hub's card f4                                                                                                                         |
| "Collagen I rose with the dose, to 93% above cells given only the solvent at 8 ppm, the highest dose tested, and fibronectin rose 100% at that dose."                                                                                                                                                                      | Claim 4: "pal-KTTKS (Matrixyl) at 8 ppm: collagen I +93%". §8.4: "always … 'against cells given only the solvent'. Say 'at the highest dose tested'". Fibronectin +100% I read at source (patent Table 1); the register does not list it |
| "A University of Reading laboratory, funded by a public research council, found the same direction in 2026: in skin fibroblasts from adult donors, palmitoyl pentapeptide-4 raised the collagen each cell made, significantly more than in cells given the culture medium alone, measured with a dye that binds collagen." | §8.1 new-evidence table: de Mello 2026, "C16-KTTKS (pentapeptide-4) stimulated collagen production in adult human dermal fibroblasts … Positive, lab, independent (pentapeptide-4)"; §4 allowed form                                     |
| "Laboratory findings that explain how palmitoyl pentapeptide-4 may work."                                                                                                                                                                                                                                                  | Science template §4 rule 3: a required qualifier "said positively ('laboratory findings that explain how X may work')"; the same line as the hub's card f4                                                                               |

**Not the same text as the hub.** The hub's card f4 is about Matrixyl 3000 (the +256% pair). Nothing here repeats it. m2 is the
pentapeptide-4 row of the same patent table plus de Mello, which the hub does not use.

**Heading:** "How does palmitoyl pentapeptide-4 work? What lab tests show". The second clause keeps the cell framing in the heading itself.
The plain alternative is "How does palmitoyl pentapeptide-4 work?"

## 5. Flags (D): the current config against the register and the template

**F1. Key figure 3, "3 ppm", is not a result.** Template §4 says key figures are results; a concentration is not one.

- Suggest: **"Week 4", "Skin texture ahead of placebo (p ≤ 0.05; size not reported)"**, the earliest result at the usual bar.
- 3 ppm stays in At a glance and in FAQ 2.

**F2. Key figure 1, "93", is a count.** The template allows a count only when the paper reports no further magnitude, and then "say so in
the figure's note". Its note does not say so. Minor.

**F3. The whole page, not just a section, rests on the pending p ≤ 0.10 ruling.**

- These lead with the fine-line result: the H1, answer, verdict, SEO description, FAQ 1, "What it means" ¶1 and key figure 2.
- The article went **live at 16:05 today**.
- The answer and the SEO description state that result without its threshold. They avoid the word "significant", so claim 6 is met to the
  letter. But the answer is the paragraph AI engines quote. Consider adding "by the paper's p ≤ 0.10 test" (the answer would grow from 60 to
  about 67 words, within 35–75).
- **If Malcolm rules against p ≤ 0.10**, the H1 and answer need re-pointing to texture and age spots. That is a rebuild, not a section edit.

**F4. Limits, item 3.** "The authors call it small, and significant at weeks 8 and 12" has no threshold in that sentence (claim 6). Item 4
gives it, but each item can be read alone. Fix: "…significant at weeks 8 and 12 by the paper's own test (p ≤ 0.10)".

**F5. At a glance, concentration row: "within the 2–8 ppm range recommended for cosmetics" is unsourced.**

- It is not in the abstract, CIR 2012, CIR 2024, Abu Samah, Aldag, Gorouhi or the register.
- Citable replacement: "well below the highest level reported in face products, 0.0012% (CIR, 2024, p. 5)".
- This row is live in six languages.

**F6. Context ¶1: "designed from a piece of type I procollagen to prompt collagen production".** This states a collagen action without
laboratory framing (register §4 avoid row; claim 4 condition (a); the EC in-vitro rule).

- Fix: "…designed from a piece of type I procollagen that raised collagen production in lab tests on cells".
- Or point to the new how-it-works section.

**F7. Katayama against Malcolm's hub decision 4.** On 2026-09-26 he took Katayama off the **Matrixyl 3000** hub as "the parent sequence, not
our ingredient". On **this** page the ingredient is pal-KTTKS, which is KTTKS plus palmitic acid, so Katayama is the origin of the very
sequence tested. I propose m1 on that basis. If he applies decision 4 here too, drop m1 and keep m2 alone.

**F8. Register corrections found at source.** These go into `docs/claims/matrixyl-3000.md`.

- **(a) Katayama's cells.**
  - KTTKS itself was tested on **human lung fibroblasts (HFL-1)**.
  - The six-cell-line figure, which includes human foreskin dermal fibroblasts, used the longer 15-residue peptide K3, not KTTKS.
  - KTTKS in other lines is "data not shown".
  - So "skin cells" must never be used for Katayama. §3 row 14's "Read: Abstract" can become "Full text (open access at jbc.org)".
- **(b) Age spots.** §8.5 says age spots and dark circles were "self-assessed and 'directional'". In fact:
  - Aldag reports age spots as a **blinded-expert** result at p ≤ 0.05 (week 12);
  - Gorouhi says both the expert and the self-assessed scores were significant;
  - the abstract's "directional" refers to the self-assessment of "other" parameters, and CIR 2012 calls the self-assessed age spots, dark
    circles and firmness "significant at week 12".

  The secondary sources disagree about the self-assessment. The JSON says only "the women's own ratings agreed", which is true under either
  reading. §8.5's rule against picturing age spots on the f2 pair still holds, because no size is known.

- **(c) Claim 4's pal-KTTKS row.** Add fibronectin +100% (8 ppm) and the dose series: collagen I +8/+30/+48/+93% at 1/2/4/8 ppm.
- **(d) Penetration.** Abu Samah's own laboratory found "no detectable permeation across excised skin" (unpublished), which supports the §4
  penetration avoid line. CIR 2024 measured 0.6% of the applied peptide in mouse dermis; never use that.

**F9. Texture: one ambiguity in Aldag.** Aldag ends: "No differences were found in skin texture or barrier function as measured by
transepidermal water loss." Most likely this means the **computer-measured** cheek texture did not differ, while the graders' texture score
did.

- The At-a-glance row ("texture on the cheeks" under computer analysis) is accurate as a description of method.
- o2 credits the result to the graders only.
- Low risk; no change proposed.

**F10. "Decision 2" numbering.** The committed review pack (`docs/review-2026-10-01-four-new-study-drafts.md`, commit `bdeb789`) numbers
**Decision 2 as the concern labels**. The p ≤ 0.10 ruling is not in it. `docs/decisions-log.md` line 536 still says "review pack decision
2". The p ≤ 0.10 question should be put to Malcolm explicitly. I used the `_pending` marker exactly as instructed.

**F11. Hub card f2 (review pack decision 4).** It states the same Robinson result without the threshold. This is consistent with the pending
item; option A there ("add the bar") matches this page.

## 6. Open questions for the client (Malcolm)

1. **p ≤ 0.10:** may the fine-line and wrinkle result have its own section? It already heads the live page (F3). Yes means the pending item
   becomes o1. No means the page's lead and key figure 2 need rework.
2. **Katayama on this page** despite hub decision 4 (F7): keep m1, or keep m2 only?
3. **A before/after for fine lines:** reuse the hub's card-f2 pair once he picks one, or no picture? I recommend no, because no size is
   known and the page says so.
4. **Image run:** five plain method photographs (two or three results and two how-it-works blocks), part of the review pack's "photographs
   of the instruments" item, which needs his approval and a budget.
5. **Key figure 3:** swap "3 ppm" for "Week 4, texture (p ≤ 0.05)" (F1)?

## 7. What I could not verify

- **The Robinson full text** (paywalled). Not known:
  - any effect size or exact p-value;
  - the exact wording of the grading scale (the −4 to +4 scale comes from Aldag alone);
  - which results the self-assessment reached significance on beyond fine lines (the sources conflict, F8b);
  - whether the image-analysis cheek texture differed (F9).

  Aldag reports n = 94; the abstract says 93, and 93 is used.

- **The source of "2–8 ppm recommended"** (F5).
- **Jones et al. 2013** (Mol Pharm): not read and not cited.
