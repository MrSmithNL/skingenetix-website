# Yogya 2022 (RF microneedling + polynucleotides vs saline): results and how-it-works, notes

Config: `configs/studies/pdrn-microneedling-split-face-trial-yogya-2022.json`. It moved there from `configs/studies/drafts/` during this
task (merge 2f05222, "Live in six languages, 2026-10-01"); the content did not change. Output:
`pdrn-microneedling-split-face-trial-yogya-2022.json` (English only). Prepared 2026-10-01.

**Proposed:** 1 result (no before/after), 0 how-it-works blocks.

## 1. What I read, and how

- **Full text:** PMC9110589 as JATS XML through NCBI efetch. I read the abstract, Key Summary Points, Methods, Results (with Table 1),
  Discussion, Funding, Disclosures and Ethics.
- **Figures:** Figures 3, 4, 5 and 6 at full size from the publisher (`media.springernature.com/full/…/13555_2022_729_FigN_HTML.png`). I did
  not reuse Figure 7: the article is CC BY-NC 4.0.
- **Identity of the link:** Crossref `10.1007/s13555-022-00729-7` gives _Efficacy and Safety of Using Noninsulated Microneedle
  Radiofrequency Alone versus in Combination with Polynucleotides for Treatment of Periorbital Wrinkles_, by Yogya, Wanitphakdeedecha and
  Wongdama, 2022, in Dermatology and Therapy. NCBI esummary for PMID 35501660 returns the same title, Yogya Y as first author, and
  PMC9110589 with the same DOI. The block links the DOI.

## 2. Source table

**Wrinkle indentation, Antera 3D, from Figure 3:**

| Visit              | Serum side | Saline side | Between sides (Fig 3B)                                                         |
| ------------------ | ---------- | ----------- | ------------------------------------------------------------------------------ |
| Baseline           | 10.3       | 11.2        | n.s. (text: "no statistically significant differences in the baseline values") |
| 2 weeks after last | 9.3        | 10.3        | –                                                                              |
| 1 month            | 9.2        | 10.0        | –                                                                              |
| 2 months           | 8.9 \*     | 10.3        | \* (text: P = 0.006)                                                           |
| 3 months           | 8.9 \*     | 10.4        | \* (legend: "\*P < 0.05")                                                      |
| 6 months           | 8.8 \*     | 9.5 \*      | –                                                                              |

**Within-side significance** (`*` in Figure 3A): the serum side at 2, 3 and 6 months; the saline side at 6 months only. The text gives 6
months as serum P = 0.008 and saline P = 0.041.

**How I read "P < 0.05 and P = 0.006, respectively".** The full sentence is: "began to improve at the 2-month follow-up (Fig. 3A), and a
better improvement was observed on the treatment side than on the control side (P < 0.05 and P = 0.006, respectively; Fig. 3B)". The first p
is the within-side change at two months and the second is the between-side test, which is how the config reads it too.

| Number in the block                                   | Source                                                                                                  |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| 10.3 → 8.9, −14% (13.6%)                              | Fig 3; arithmetic (10.3 − 8.9) / 10.3                                                                   |
| 11.2 → 10.3, −8% (8.0%)                               | Fig 3; arithmetic                                                                                       |
| p = 0.006 at 2 months; p < 0.05 at 3                  | Results text; Fig 3B asterisks and legend                                                               |
| 8.9 at 3 months, 8.8 at 6; saline 10.4 at 3, 9.5 at 6 | Fig 3A/3B                                                                                               |
| visits: before, 2 weeks, 1, 2, 3, 6 months            | Methods: "baseline and at 2 weeks, 1 month, 2 months, 3 months, and 6 months after the final treatment" |
| Antera 3D, indentation                                | Methods, "Objective and subjective evaluations"                                                         |

**Read, but not placed in the block:**

- **Maximum depth (Figure 4):** 0.066 → 0.060 with the serum and 0.073 → 0.068 with saline, with no significance at any visit.
- **R2 (Figure 5):** the only between-side gap is at 2 months, 0.59 against 0.66, with the serum side lower. At 6 months the sides read 0.58
  and 0.57.
- **Self-ratings (Figure 6):** at 6 months the serum side scored 3 / 2 / 9 / 9 / 6 and the saline side 2 / 3 / 9 / 8 / 7 (0%, under 25%,
  26–50%, 51–75%, over 75%). On both sides 24 of 29 women (82%) rated themselves more than 25% improved, and 15 of 29 (51%) more than 50%.
  The two sides did not differ (P = 0.189).
- **Pain:** 2.1 ± 1.5 in Table 1, and 2.2 ± 1.9 in the safety text.

## 3. Which results qualify, and why there is one section

The only positive result that beats saline at p ≤ 0.05 is wrinkle indentation, at two months (p = 0.006) and three months (p < 0.05). That
makes one section.

| Candidate       | Between sides                                      | Section?      |
| --------------- | -------------------------------------------------- | ------------- |
| Indentation     | p = 0.006 (2 mo), p < 0.05 (3 mo), serum better    | **Yes**       |
| Maximum depth   | No difference at any visit                         | No            |
| Elasticity (R2) | One gap, at 2 months, favouring saline; level at 6 | No            |
| Self-ratings    | No difference (P = 0.189)                          | No; see below |
| Pain, safety    | Not a comparison between the sides                 | No            |

**Why the self-ratings stay out of the result's section.** The template puts results without a p-value inside the section they support.
These ratings do have a p-value, and it shows no difference between the sides, so they describe the microneedling rather than the serum.
Placing them inside the polynucleotide result would credit the serum with the procedure's effect. The config already reports them openly in
`media.body[1]` and `limits.items[4]`.

## 4. Before/after reasoning

**No before/after,** and no labels. The section gets a plain photograph of the measuring instrument. Four reasons:

1. **The gain is speed, not size.** By six months both sides had improved by much the same amount: 10.3 → 8.8 (−14.6%) on the serum side and
   11.2 → 9.5 (−15.2%) with saline. A single before/after pair cannot show "sooner", and any after panel would show the procedure's change,
   which both sides share.
2. **The result belongs to a clinic procedure.** A face picture next to a polynucleotide label invites a reader to credit a serum on intact
   skin.
3. **The paper's own photographs (Figure 7) cannot be reused** under CC BY-NC.
4. **The change is too small to picture honestly.** −14% on an indentation score is a difference a viewer would have to compare carefully to
   see.

## 5. How it works: zero blocks, and why

1. **The paper tested no mechanism.** It has no histology, no laboratory arm and no skin samples. Its Discussion offers hypotheses:
   polynucleotides acting on the dermal matrix, "wound healing", microchannels and electroporation as the delivery route. None was measured
   in this trial.
2. **The delivery route belongs to the procedure.** A block explaining that the needles let the serum in would describe the procedure. It
   would suggest exactly what the register forbids a reader to infer, that a serum alone does this. It also sits beside the register's avoid
   line "Topical PDRN reaches the dermis".
3. **The procedure's own effect is not the polynucleotides'.** The authors' earlier histology, in which heat and needles prompt new
   collagen, is told in wound-healing terms the brief bans ("heals/wound").
4. **The A2A receptor finding does not fit.** Fibroblasts with A2A receptors (Thellung 1999) are register grade D, read from the abstract
   only, and were not tested with this polynucleotide: 65–130 kDa, from an unstated source. The finding is already on the hub's f2 card.
5. **The Ye 2026 laboratory findings belong to the Ye article.** The skin samples and cells are its m1–m3, and repeating them here is barred
   ("the two PDRN articles must not repeat each other's blocks"). They also used a different material: salmon PDRN of up to 850 kDa, in an
   eye cream, on intact skin samples.

The `mechanisms` key is kept, with `"items": []` and a heading, so the builder clears every slot. The heading is not drawn when there are no
items.

## 6. Register check, for the one result section

| Sentence, or the point it makes                                             | Register line                                                                                                                        |
| --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| Title opens "With microneedling …"; ¶3 "in this clinic setting"             | §2 row 2: "A, but procedure-assisted, so **not transferable** to a leave-on on intact skin"                                          |
| ¶2 figures and p-values                                                     | §2 row 2: "Indentation improved faster on the PN side: 10.3 → 8.9 at 2 months (between sides P = 0.006; also different at 3 months)" |
| ¶3 "held its gain … the saline side's score rose back to 10.4 … 9.5 at six" | §2 row 2: "saline side significant only at 6 months, and both sides similar by then (8.8 vs 9.5)"                                    |
| No advice to apply a serum after microneedling                              | Config `_note`: "never advise a serum on microneedled skin"                                                                          |
| No "heal", "wound", "repair", "regenerate", "stimulate", "activate"         | Brief (PDRN line) and register §3 avoid list; automated scan: no hits                                                                |
| "polynucleotide" for the trial's material; no source claim                  | §2 row 2: "**The paper does not state the PN's source.**"                                                                            |

## 7. Flags (D) in the current live config

1. **LOW, already decided.** `figures[0]` "2 vs 6 months" is a time. Template §4 allows a time only where the paper reports no magnitude,
   and the magnitude (−14% vs −8%) sits in `figures[1]`. Commit b67cf69 chose it deliberately ("the trial's finding is speed"), so this is a
   note only.
2. **LOW, already decided.** `figures[2]` "2.2/10" pain is not a result against the comparator. The design critique of 2026-10-01 put it
   there. Note only.
3. **LOW.** `media.body[2]` says "the needles open short-lived channels that let large molecules such as polynucleotides reach deeper". It
   is attributed to the researchers ("Their reasoning:") and concerns microneedled skin, so it does not break the register's line on intact
   skin. It is, though, the sentence an avoid-list checker would stop at first. An optional rewording: "… that let large molecules such as
   polynucleotides past the skin's surface layer".

Nothing else conflicts. The figures, chart, limits, FAQ and glance rows match Figures 3–6, Table 1 and the Methods as I read them.

## 8. Open questions for the client

1. **One result section,** with no before/after and no how-it-works blocks: is that acceptable for this article? It is the honest maximum
   the paper supports.
2. **Translations.** The block is English only, and the article is live in six languages, so a full `--apply` needs de, nl, fr, es and it
   first. The image is TBD.
