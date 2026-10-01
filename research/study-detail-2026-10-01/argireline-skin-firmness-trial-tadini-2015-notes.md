# Tadini 2015 (Argireline® / acetyl hexapeptide-3, skin mechanics): results and how-it-works, notes

**Config:** the brief named `configs/studies/drafts/argireline-skin-firmness-trial-tadini-2015.json`. Since commit bdeb789 the file is
`configs/studies/argireline-skin-firmness-trial-tadini-2015.json`, **live in six languages** (en, de, nl, fr, es, it). Its English text is
unchanged from the draft, so every flag below applies to the live page and needs the five translations redone. **Proposal:**
`argireline-skin-firmness-trial-tadini-2015.json` in this folder. 2 results (both plain photographs), 0 how-it-works blocks. **Written:**
2026-10-01. Register: `docs/claims/argireline-acetyl-hexapeptide-8.md`, "Supporting line" under §1, and evidence-table row Tadini 2015.

## 1. What I read

**Full text**: the SciELO HTML (open access) and the publisher PDF (_Braz J Pharm Sci_ 51(4):901–909). I read the Methods (pp. 902–903), the
Results and Discussion (pp. 904–907), the Conclusions and Acknowledgements (p. 907), and Figures 1–7. I rendered Figure 5 (p. 906) from the
PDF and read it as an image: face (B) Argireline ≈2.5 → ≈1.57*→ ≈1.67*●; vehicle ≈2.5 → ≈2.0 → ≈2.15, with no marks. Link checked: DOI
10.1590/S1984-82502015000400016 (Crossref: Tadini, 2015, title verbatim). The paper has no PubMed record.

## 2. Source table: every number in the proposal

| Number                                                                                                                                               | Source                                                                                                                   |
| ---------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| Reviscometer RV600: two needle-like sensors, one sends a pulse, the other receives it; timings in several directions                                 | Methods, Instrumentation, p. 903; Results and Discussion, p. 904                                                         |
| "Speed of shear wave propagation ... directly proportional to its stiffness"; authors read lower anisotropy as "increased firmness or tensor effect" | Results and Discussion, p. 904                                                                                           |
| Readings 10–15 hours after the last application                                                                                                      | Study protocol, p. 903                                                                                                   |
| Anisotropy ≈2.5 → ≈1.7 at week 4 (about a third lower), significantly below the start                                                                | Figure 5B, p. 906 (asterisk); values read from the plot, in line with the config's vector extraction (2.49 → 1.66, −33%) |
| Vehicle ≈2.5 → ≈2.2, not marked significant                                                                                                          | Figure 5B, p. 906                                                                                                        |
| Week 4: Argireline lower than the vehicle, p < 0.05                                                                                                  | Figure 5B caption ("● Significantly different from Vehicle after 4 weeks"); Statistical analysis, p. 903                 |
| Week 2: ≈1.6 (about 37% lower), significant against its start; vehicle ≈2.0, not marked                                                              | Figure 5B, p. 906 (config extraction 2.49 → 1.57)                                                                        |
| Kruskal–Wallis test for anisotropy                                                                                                                   | Statistical analysis, p. 903 ("Anisotropy calculated values were statistically analysed using the Kruskal-Wallis test")  |
| Authors' conclusion: acts on skin mechanical properties; effective ingredient for anti-ageing formulations                                           | Title; Results and Discussion, p. 907; Conclusions, p. 907                                                               |
| Earliest significant change of the three trials                                                                                                      | Tadini week 2 (Figure 5B); Raikou's first measurement day 20 (Raikou §2.7); Wang reports at week 4 (Wang Results 3.1)    |

## 3. Before/after reasoning, per result

| Result                                                | Decision                                                                               | Why                                                                                                                                                                                 |
| ----------------------------------------------------- | -------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1. Anisotropy ≈−33% at week 4, lower than the vehicle | **Plain photograph** of the probe type the trial used                                  | Anisotropy is a ratio of sound-pulse timings. Nothing about it is visible on a face, and §3.1 lists firmness readings under "Picture, plain". No hub picture exists for this trial. |
| 2. Anisotropy ≈−37% within two weeks                  | **Plain photograph** of two identical plain cream jars (the vehicle-controlled design) | The same measure. A picture of a face would claim a visible change the trial never measured (it measured no wrinkles).                                                              |

## 4. How it works: zero blocks, and why

- **The trial tested no mechanism.** The authors write that there are "few basic studies about its effects on skin, as well as, about its
  mechanism of action" (p. 904). The physics of the Reviscometer (pulse speed rises with stiffness) explains the _measurement_, so it sits
  inside result 1, not in a how-it-works block.
- **The Argireline laboratory finding does not fit this trial.** Blanes-Mira 2002 (SNARE complex) concerns expression lines, which this
  trial did not measure. Linking it to anisotropy or firmness would be our inference, and it is already used once, on the Wang 2013 page.
- **The only study tying Argireline to skin structure is an animal study.** Wang et al. 2013, _J Cosmet Laser Ther_,
  [PubMed 23464592](https://pubmed.ncbi.nlm.nih.gov/23464592/): type I collagen up in aged mice. The register lists "Boosts collagen" under
  AVOID ("The only evidence is in mice"). Not used.
- The JSON keeps `mechanisms` with `items: []` and a `_why_none` note.

## 5. Register check: result sentences that carry a claim

| Sentence                                                                                                                                     | Register line                                                                                                         | Comment                                                                                                     |
| -------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| "Facial anisotropy fell about a third and ended lower than with the plain cream"                                                             | Supporting line: "reduced facial skin anisotropy after 4 weeks against the vehicle (p < 0.05)"                        | Within the register                                                                                         |
| "The pulse travels faster through stiffer skin, which is why **the authors read** a lower anisotropy as a sign of firmer skin"               | Supporting line: "Usable as 'helps skin look more supple and even' only with care, because it is a technical measure" | Firmness is **attributed to the authors** (p. 904), never claimed in our voice. This depends on Q1 below    |
| "The authors conclude that acetyl hexapeptide-3 acts on the skin's mechanical properties ... an effective ingredient for anti-ageing creams" | Attributed; it is the paper's title and conclusion                                                                    | No efficacy claim for our product                                                                           |
| "Within two weeks anisotropy was significantly lower; the plain cream's was not"                                                             | Within-group only, and the body says so ("At this visit the paper compares each cream with its own starting value")   | Brief rule A, "significant within the active group only ... say so"                                         |
| Hydration                                                                                                                                    | Not mentioned in the results                                                                                          | Register AVOID "Hydrates": the face's moisture rose with both creams (Figure 1, p < 0.01 against the start) |

## 6. Flags on the current (live) config (D)

**The main one, which the lead asked about: "firm and tighten".** The register's only allowed wording for this trial is "helps skin look
more supple and even", "only with care". The paper's own reading (p. 904) is "increased firmness or tensor effect"; "tensor effect" is the
cosmetic-science term for a tightening effect. So "firmer, tauter" is a **fair translation of the authors' words**, but it exceeds the
register. My honest view:

1. The register's "more supple" points the wrong way. The authors argue the skin got _stiffer_ (faster pulse), which is the opposite of
   supple. The register line should be corrected, for example: "lowered facial anisotropy, which the authors read as increased firmness
   ('tensor effect'); the suction-based elasticity readings did not change. Say 'firmness-related measure' and attribute the firmness
   reading to the authors."
2. With that correction, the **H1 as a question** ("Does Argireline® firm and tighten facial skin?") is defensible, provided the page never
   answers "yes" in our own voice. The four places below currently do, and need rewording.

| #   | Where                                               | Current text                                                                                                             | Problem                                                                                                                                                                                                                  | Suggested fix                                                                                                                                                               |
| --- | --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| D1  | `h1`, `seo_title`                                   | "Does Argireline® firm and tighten facial skin?" / "Does Acetyl Hexapeptide-3 Firm Skin?"                                | Above the register's wording; needs the register change above                                                                                                                                                            | Keep the question once the register is updated. If the client prefers the strict register: "Does Argireline® change how facial skin behaves?" (weaker for search)           |
| D2  | `seo_description`                                   | "... **cut a firmness measure of facial skin** by about a third in 2 weeks."                                             | Firmness in our voice. It can also be **misread as firmness falling by a third**, the opposite of the finding                                                                                                            | "In a vehicle-controlled trial of 40 women, 10% Argireline (acetyl hexapeptide-3) lowered facial anisotropy, which rises with age, by a third in 2 weeks." (152 characters) |
| D3  | `figures[0]`                                        | Label "**Firmness signal** on the face by week 4"; note "Facial anisotropy, **which rises as skin loses firmness**, ..." | The paper says anisotropy rises **with age** (p. 906, citing Ruvolo 2007 and Hermanns-Lê 2001), not "as skin loses firmness". The label states firmness in our voice                                                     | Label: "Facial anisotropy by week 4". Note: "Facial anisotropy, which rises with age, fell from about 2.5 to 1.7 ..."                                                       |
| D4  | `limits.items[2]`                                   | "... **the firmness change** was the peptide's own."                                                                     | Firmness in our voice                                                                                                                                                                                                    | "... the anisotropy change was the peptide's own."                                                                                                                          |
| D5  | `context.body[1]`                                   | "... the one measure that changed **moved towards firmer skin**."                                                        | Firmness in our voice                                                                                                                                                                                                    | "... the one measure that changed moved the way the authors read as firmer skin."                                                                                           |
| D6  | `verdict`, `limits.items[0]`, `meaning.body[0]`     | "which the authors read as firmer, tauter skin" / "as firmer skin"                                                       | **Fine.** Attributed, and it matches the paper's "increased firmness or tensor effect"                                                                                                                                   | Keep once the register line is updated                                                                                                                                      |
| D7  | `definition`                                        | "another label name for acetyl hexapeptide-8" (the config note says it rests on tertiary sources)                        | Not a breach, and now verifiable                                                                                                                                                                                         | Primary support: Raikou 2017, p. 271, "acetyl hexapeptide-3 or acetyl hexapeptide-8, as it has been recently renamed". Add it to the config's `_note`; optionally cite it   |
| D8  | `deck`, `answer`, glance, `figures[2]` ("40 women") | 40                                                                                                                       | The paper says "Forty healthy female subjects" (p. 902) and later "the experiment was conducted with **twenty volunteers** who were divided in two groups" (p. 903). On the face, the groups may be 20 vs 20 or 10 vs 10 | Keep 40 (abstract and protocol). Do not print a per-group number for the face                                                                                               |

Checked and fine: the answer ("a firmness-related measure that rises with age"), the chart and its caption, the "−37% Already by week 2"
figure (within-group, said so), the glance rows (FAPESP, Galena, 1 mL, Fitzpatrick II–IV), the media body and the FAQ.

## 7. Open questions for the client

1. **Firmness wording (main question).** Update the register's Tadini line to allow "a firmness-related measure, which the authors read as
   firmer, tauter skin ('tensor effect')", and then keep the H1? Or keep the stricter "more supple and even", and then change the H1, SEO
   title and description (D1–D5)? My recommendation is the first, with D2–D5 applied either way.
2. Two result sections on one measure (week 4 against the vehicle, and week 2 within-group). The brief's rule allows the week-2 section
   because the paper compares groups only at week 4. If they read as repetitive on the page, merge result 2's time-course paragraph into
   result 1 and keep one section.
3. No how-it-works block on this article (§4). Accept?
