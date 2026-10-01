# Ye 2026 (PDRN vs retinol): results and how-it-works, notes

Config: `configs/studies/pdrn-vs-retinol-split-face-trial-ye-2026.json` (live, six languages). Output:
`pdrn-vs-retinol-split-face-trial-ye-2026.json` (English only, as the brief asks). Prepared 2026-10-01.

**Proposed:** 4 results (none with a before/after: see §4), 3 how-it-works blocks (2 from skin samples, 1 from cells).

## 1. What I read, and how

- **Full text:** PMC13353946 as JATS XML through NCBI efetch. I read the Methods in full (materials, cell culture, Table 2 ex vivo groups,
  the UVA/UVB protocol, histology, the in vivo Raman, the clinical protocol and statistics), then the Results and Discussion, including the
  limitations.
- **Figures:** Figures 1, 5 and 6 at original resolution from PLOS
  (`journals.plos.org/plosone/article/figure/image?size=original&id=…g00N`), with every bar label and significance mark of Figure 6B read at
  2–4× zoom.
- **Identity of the link:** Crossref `10.1371/journal.pone.0350905` gives _Topical medium-length PDRN enhances dermal extracellular matrix
  repair in photodamaged skin via PI3K–Akt/TGF-β–regulated pathways_, by Ye, Wang and Du, published 2026 in PLOS One. NCBI esummary for PMID
  42430369 returns the same title, Ye R as first author, PMC13353946 and the same DOI. Every citation in the blocks links the DOI.

### How I read the significance marks in Figure 6B (open question 1)

The legend says only "Statistical significance is indicated in the figure", with no key. I read the marks as follows:

- **The black `\***` above each bar\*\* is that side's change from day 0.
- **The red `#`, `##` or `###`** sits over a bracket joining the two sides at one visit, so it is the between-side test.
- **"n.s."** marks two of the day-14 comparisons.

I took the thresholds from the paper's own legends to Figures 1 and 2: `#` p < 0.05, `##` p < 0.01, `###` p < 0.001. The Methods name the
test for the split-face comparisons: a paired t-test, or Wilcoxon for non-normal data, two-sided, with significance at p < 0.05. The blocks
print "p < 0.001" and so on on that basis.

## 2. Source table: every number in the blocks

### Figure 6B, clinical. Change from day 0 on each side, n = 31

| Measure (instrument)               | D14 retinol | D14 PDRN | between | D28 retinol | D28 PDRN | between | D28 ratio |
| ---------------------------------- | ----------- | -------- | ------- | ----------- | -------- | ------- | --------- |
| Dermal thickness (Ultrascan UC22)  | +2.94%      | +7.54%   | ###     | +5.53%      | +11.52%  | ###     | 2.08×     |
| Dermal density (Ultrascan UC22)    | +2.98%      | +4.75%   | #       | +4.79%      | +9.56%   | ###     | 2.00×     |
| R2 elasticity (Cutometer)          | +14.90%     | +21.31%  | ###     | +24.82%     | +44.03%  | ###     | 1.77×     |
| F4 firmness, lower = firmer        | −8.15%      | −12.80%  | ##      | −16.25%     | −29.61%  | ###     | 1.82×     |
| Crow's-feet number (VISIA 7)       | −3.53%      | −8.33%   | ###     | −6.43%      | −19.98%  | ###     | 3.11×     |
| Crow's-feet area (VISIA 7)         | −3.94%      | −12.44%  | ###     | −6.56%      | −22.99%  | ###     | 3.50×     |
| Under-eye wrinkle number (VISIA 7) | −4.55%      | −8.64%   | #       | −7.00%      | −23.37%  | ###     | 3.34×     |
| Under-eye wrinkle area (VISIA 7)   | −3.35%      | −9.43%   | ###     | −6.73%      | −19.95%  | ###     | 2.96×     |
| Tear-trough length (Antera 3D)     | −3.87%      | −4.98%   | n.s.    | −6.64%      | −10.42%  | ##      | 1.57×     |
| Tear-trough volume (Antera 3D)     | −4.99%      | −7.38%   | #       | −10.17%     | −13.67%  | ##      | 1.34×     |
| Eye-bag volume (Antera 3D)         | −5.23%      | −7.48%   | n.s.    | −10.24%     | −14.84%  | #       | 1.45×     |

Every within-side change carries `***`.

### Where each number in the blocks comes from

| Block | Figure on the page                                                                                                                                                              | Source                                                                                                                                                                                                                                                                                                                                 |
| ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| o1    | 20–23% vs 6–7% (all four wrinkle readings, D28)                                                                                                                                 | Fig 6B, the four VISIA bars                                                                                                                                                                                                                                                                                                            |
| o1    | crow's-feet area 23.0% vs 6.6%; under-eye number 23.4% vs 7.0%; p < 0.001 × 4                                                                                                   | Fig 6B                                                                                                                                                                                                                                                                                                                                 |
| o1    | D14 crow's-feet area 12.4% (vs D28 retinol 6.6%), p < 0.001 at D14                                                                                                              | Fig 6B; matches Results: "evident by Day 14 and exceeded retinol-induced changes measured at Day 28"                                                                                                                                                                                                                                   |
| o1    | VISIA 7, wrinkle number and area, Image-Pro Plus                                                                                                                                | Methods, "Clinical evaluation"                                                                                                                                                                                                                                                                                                         |
| o2    | R2 +44.0% vs +24.8%; F4 29.6% vs 16.3% (p < 0.001); D14 21.3 vs 14.9 (p < 0.001), 12.8 vs 8.2 (p < 0.01)                                                                        | Fig 6B                                                                                                                                                                                                                                                                                                                                 |
| o2    | "about 1.8 times"                                                                                                                                                               | Results: "approximately 1.8-fold higher"                                                                                                                                                                                                                                                                                               |
| o2    | Cutometer, suction probe                                                                                                                                                        | Methods: "Cutometer MPA580 (2-mm probe)"                                                                                                                                                                                                                                                                                               |
| o3    | thickness 11.5% vs 5.5%, density 9.6% vs 4.8% (p < 0.001); D14 7.5 vs 2.9 (p < 0.001), 4.8 vs 3.0 (p < 0.05)                                                                    | Fig 6B                                                                                                                                                                                                                                                                                                                                 |
| o3    | early signal, partly hydration or plumping; same base on both sides                                                                                                             | Discussion ¶5: "may partly reflect transient hydration or plumping effects"; "nonspecific moisturization alone is unlikely to explain the results because the split-face design controlled for the vehicle base and the same 0.1% PDRN-850K eye cream increased multiple ECM-related proteins in the UV-irradiated ex vivo skin model" |
| o4    | eye-bag 14.8% vs 10.2% (p < 0.05); hollow volume 13.7 vs 10.2, length 10.4 vs 6.6 (p < 0.01); D14 volume 7.4 vs 5.0 (p < 0.05)                                                  | Fig 6B                                                                                                                                                                                                                                                                                                                                 |
| o4    | "Every woman … had visible eye bags"                                                                                                                                            | Methods: "All participants presented … eye bags … eye bag grades > 1"                                                                                                                                                                                                                                                                  |
| m1    | full-thickness human skin in culture; UVA + UVB four times a day apart; the same cream after each, then daily for 3 more days; plain-medium comparison; stained slices measured | Methods, "UV-irradiated human ex vivo skin model", Table 2 (30 J/cm² UVA + 50 mJ/cm² UVB), "UVA/UVB irradiation and treatment protocol", "Histological and immunostaining analyses"                                                                                                                                                    |
| m1    | the same cream                                                                                                                                                                  | Methods: "0.1% PDRN-850K (same formulation as used in the ex vivo study)"                                                                                                                                                                                                                                                              |
| m1    | I +82%, III +69%, VI +232%, VII +191%, XV +21% (others: IV 59.2, V 108.2, XVII 42.1, XVIII 60.6)                                                                                | Fig 5B, "improvement rate" vs UV-damaged control                                                                                                                                                                                                                                                                                       |
| m1    | "significantly higher"; outer living layer thicker; three per group                                                                                                             | Results text ("all significantly elevated"; "significantly increased the thickness of the viable epidermal layer"); Fig 5 legend n = 3                                                                                                                                                                                                 |
| m2    | elastin +36% (35.6), fibrillin-1 +115% (115.2)                                                                                                                                  | Fig 5B                                                                                                                                                                                                                                                                                                                                 |
| m2    | R2 44% vs 25%                                                                                                                                                                   | Fig 6B                                                                                                                                                                                                                                                                                                                                 |
| m3    | 0.5 µg/mL; human dermal fibroblasts                                                                                                                                             | Fig 1 axis labels; Methods, "Cell culture"                                                                                                                                                                                                                                                                                             |
| m3    | collagen I and III genes about 2× (p < 0.01, p < 0.05), n = 3, after 48 h                                                                                                       | Fig 1G bar heights (≈2.15× and ≈2.3×; no printed values, hence "about twice"); legend `*`/`**` vs control; Methods: 48 h co-treatment                                                                                                                                                                                                  |
| m3    | signals stronger within 6 h; TGF-β about 5× (p < 0.001)                                                                                                                         | Methods: "treated with PDRN-850K for 6 h"; Fig 1B (TGF-β/β-actin ≈ 5.2, `***`); Fig 1D (p-PI3K ≈ 3.0×, p-AKT ≈ 2.7×); Fig 1F (LC3A/B-II ≈ 1.5×, SQSTM1 ≈ 0.8×)                                                                                                                                                                         |
| m3    | blocking any one of the three cancelled the rise                                                                                                                                | Fig 1G: SB-431542, LY294002 and chloroquine each bring COL1A1 and COL3A1 to or below control (`#` to `###`)                                                                                                                                                                                                                            |

**Two details I read and deliberately did not use:**

- **The elastin gene.** The Results text says ELN mRNA was "significantly upregulated", but Figure 1G shows no mark on ELN against control.
  m3 therefore names collagen I and III only.
- **Significance in Figure 5B.** The chart has no error bars and no significance marks. The significance of the skin-sample rises rests on
  the text ("all significantly elevated"), with n = 3.

## 3. Why these four results, and in this order

The abstract groups the clinical results into four families: periocular wrinkles, dermal thickness and density, eye-bag parameters, and
elasticity with firmness. Every family has a between-side difference at p ≤ 0.05 at day 28.

Split by site, that would be five sections, one more than the template's four slots. I put the two VISIA sites, crow's feet and the lines
under the eye, into one section. They use the same instrument and the same two readings, the paper treats them together as "periocular
wrinkles", and the page's chart already has the same four rows. That way every significant result keeps a section.

Strongest first:

1. **Wrinkles:** all four readings at p < 0.001, about 3× the retinol change.
2. **Elasticity and firmness:** p < 0.001 at day 28, and ahead at day 14 as well.
3. **Dermal thickness and density:** p < 0.001.
4. **Eye bags and tear troughs:** p < 0.05 to 0.01, about 1.3–1.6× the retinol change.

**If Malcolm wants crow's feet on its own:** crow's feet / under-eye lines / elasticity and firmness / dermal. Eye bags would then drop out
as the weakest result. I do not recommend it, because the hub's second card is the eye-bag result.

**Not proposed as a section:** tolerability ("no reported adverse reactions" on either side). It is not a comparison between the sides, and
the hub's f3 card and the safety note already carry it. Ye reports no self-assessment.

## 4. Before/after reasoning, per result

| Result                 | Visible on a face? | Picture shows the measured area? | Does the existing picture's change stay within the result? | Decision |
| ---------------------- | ------------------ | -------------------------------- | ---------------------------------------------------------- | -------- |
| o1 wrinkles            | Yes                | Yes (crow's feet, one side)      | **No, in my judgement** (below)                            | false    |
| o2 elasticity/firmness | No (instrument)    | –                                | –                                                          | false    |
| o3 dermal ultrasound   | No (instrument)    | –                                | –                                                          | false    |
| o4 eye bags            | Yes                | Yes (under-eye, one side)        | **No** (below)                                             | false    |

**o1, the crow's-feet pair** (`skingenetix-pdrn-crows-feet-periorbital-wrinkles-before-after.jpg`, 3000 px, local copy in
`assets/publish-ready/page-pdrn-research-crows-feet/`).

- **The August pass.** The selection note of 2026-08-27 (`configs/banners/page-pdrn-research-crows-feet-publish.json`) passed this pair:
  "every crow's-foot line is still present, only shallower".
- **What the native pixels show today.** The lines are indeed all there. But in the after panel they read far fainter than a 20–23% fall in
  wrinkle area and number would make them. That panel is also lit flatter, brighter and cooler, with less raking light. The crêpey skin
  under the eye smooths out too. That fails §3 of `docs/clinical-trial-before-after-images.md` twice: "nothing else about her improves …
  better lit", and a change that exceeds the result.
- **Decision:** false.
- **If Malcolm upholds the August pass,** switch the result to `before_after: true` with `after` = "After 28 days" and `result` = "Crow's
  feet −20 to −23% vs −6 to −7% with retinol" (50 characters, the hub's own label).
- **The better route is a calibrated pair:** every line present at about four-fifths of its depth and contrast, with the same light
  direction and colour in both panels.

**o4, the under-eye pair** (`skingenetix-pdrn-under-eye-bags-before-after.jpg`, r3 F4 `nbp_flash 01`).

- **What the picture shows.** In the after panel most of the bulge has gone, and the lighting is more even.
- **Even the brief overshoots.** The r2/r3 brief aimed for "four-fifths of the bulge" to remain, a change of about 20%. That is already more
  than the measured 14.8%.
- **The label overshoots too.** It says "about 2×", but Figure 6B shows 1.45× (flag 1).
- **Decision:** false.
- **A calibrated pair is possible:** about a seventh less volume, a change a viewer "should have to compare carefully" to see (the An 2019
  rule in §3). Its labels would be "After 28 days" and "Eye-bag volume −14.8% vs −10.2% with retinol" (45 characters).

## 5. Register check: every how-it-works sentence

Register lines (`docs/claims/pdrn.md`):

- **R-a**, "The one fact": "2. **Lab/ex vivo mechanism claims**, labelled as laboratory research."
- **R-b**, claim 7: "Boosts 9 types of collagen, plus elastin, in UV-damaged human skin (laboratory study)" … "the words 'laboratory study
  on human skin samples' must appear in the claim. Never 'boosts collagen in your skin'."
- **R-c**, log 2026-09-24: "The explants were treated with the same 0.1% PDRN-850K eye cream as the clinical arm (Table 2), so 'the same
  cream' is accurate."
- **R-d**, avoid row: "'Regenerates skin' / 'stimulates stem cells' / 'rebuilds collagen in your skin' … State 'in laboratory studies on
  human skin samples'."
- **R-e**, claim 8 condition: "with 'laboratory research' … Avoid 'activates', 'regenerates' and 'stimulates cell growth'."
- **R-f**, §2 row 1: "A (clinical); C (ex vivo); D (cells)"; "Ex vivo: collagens I, III, IV, V, VI, VII, XV, XVII, XVIII, elastin,
  fibrillin-1 and YAP all ↑."
- **R-g**, legal frame: "Cosmetic, not medicinal … 'Repairs DNA', 'heals', 'treats' and 'anti-inflammatory' are medicinal wording."
- **R-h**, avoid row: "Topical PDRN reaches the dermis".

| Block | Sentence (abridged)                                                                                                       | Allowed by                                             | Avoid-list check                                                        |
| ----- | ------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------ | ----------------------------------------------------------------------- |
| m1    | "In the laboratory, the team kept pieces of full-thickness human skin alive in culture and exposed them to UVA and UVB …" | R-a, R-b                                               | method only                                                             |
| m1    | "After each exposure they applied the same 0.1% PDRN eye cream the women used …"                                          | R-c                                                    | –                                                                       |
| m1    | "Comparison samples had the same light and plain culture medium." / "Thin slices were then stained …"                     | R-a (method)                                           | –                                                                       |
| m1    | "Against the untreated UV-damaged samples, every one of the nine collagens was significantly higher."                     | R-b, R-f                                               | says "samples", never "your skin" (R-d)                                 |
| m1    | "types I and III rose 82% and 69%; … VI and VII (232% and 191%) … XV (21%)."                                              | R-b, R-f (Fig 5B)                                      | no "boost/rebuild"                                                      |
| m1    | "The living part of the outer layer was thicker too."                                                                     | R-f (viable epidermal thickness, abstract and results) | no "regenerates"                                                        |
| m1    | "These are laboratory findings in skin samples, three per group."                                                         | R-b, R-d                                               | carries the required label                                              |
| m2    | "Skin springs back because of its elastic fibres, built from elastin laid along a framework of fibrillin-1."              | general biology, no claim                              | –                                                                       |
| m2    | "In the same UV-damaged human skin samples, in the laboratory, the cream raised elastin by 36% and fibrillin-1 by 115% …" | R-b ("plus elastin"), R-f                              | "skin samples" + "laboratory" (R-b)                                     |
| m2    | "This is the laboratory side of the elasticity result on the women's faces, where the Cutometer reading rose 44% …"       | R-a; clinical figure from Fig 6B                       | no causal claim from lab to face                                        |
| m2    | "The skin samples show which fibres changed; the faces show elasticity changing in people. Both point the same way."      | R-a                                                    | –                                                                       |
| m3    | "In the laboratory, the team added … PDRN-850K (0.5 µg/mL) to human fibroblasts …"                                        | R-a, R-e                                               | –                                                                       |
| m3    | "the genes for collagen types I and III were about twice as active as in untreated cells"                                 | R-a, R-f (D, cells)                                    | no "activates", no "stimulates" (R-e)                                   |
| m3    | "three of the cells' internal signals were stronger: TGF-β … PI3K–Akt … autophagy"                                        | R-a                                                    | "stronger", not "activated"; "alive and productive", not "growth" (R-e) |
| m3    | "Blocking any one of the three cancelled the rise in the collagen genes."                                                 | R-a                                                    | –                                                                       |
| m3    | "In plain terms, in the laboratory PDRN worked through the cells' own collagen-making controls."                          | R-a, R-e                                               | lab-framed; no "in your skin"                                           |

**Automated scan** of every title and body (results and mechanisms) for repair, regenerat, heal, wound, activat, stimulat, penetrat, boost,
rebuild, restor, treat(s), lighten, whiten, scar, anti-inflamm, proven, safe, "cell growth" and "reaches the dermis": no hits except
"untreated".

**No disease names.** "UV-damaged" is the paper's laboratory model, not a condition of the reader's skin.

**The results against the register:**

- **Every comparison names retinol**, which meets claim 2: "Do not generalise to 'better than retinol' without the study frame".
- **No wrinkle ratio is given**, only percentages, because claim 2 says "not '3×'" (flag 7).
- **The R2/F4 percentages are read from Figure 6B, not invented.** Claim 4 says "Never invent a '+X% firmness' figure", and its premise
  ("absolute % changes appear only in a figure") is now met by reading that figure (flag 7).
- **o4 uses claim 5's cosmetic wording:** "the look of puffiness", "under-eye hollow".

**How-it-works candidates considered and NOT proposed:**

- **Penetration:**
  - **What was tested:** Raman in a lab epidermis model; FITC-labelled PDRN in pig skin "reaching the dermis at 8–12 h"; one volunteer by
    Raman.
  - **It is not an effect on skin.** It is delivery.
  - **The register bans it.** Its avoid list carries "Topical PDRN reaches the dermis".
  - **The evidence in people is thin:** one volunteer, and the authors say Raman "cannot unequivocally distinguish exogenous PDRN from
    endogenous nucleic acids".
  - **Its picture would break §4.** It would show something travelling into skin ("Images make claims").
- **A2A receptor** (Thellung 1999). It rests on the abstract only, it is grade D, and this paper did not test it. It is already on the hub's
  f2 card.
- **YAP** (+39.5% in skin samples). The finding is real, but explaining it needs jargon. I left it out of m2 to keep the block plain; it can
  be added.

## 6. Flags (D): the current live config, and the hub

1. **HIGH. "About 2×" for eye bags overstates Figure 6B.**
   - **Where:** `figures[1].note` ("about twice retinol's improvement in … eye bags"), `measurements.chart.rows[2]` ("Eye bags and tear
     troughs", value 2) and `measurements.chart.caption`.
   - **What Figure 6B shows:** eye-bag volume 1.45× (−14.84% vs −10.24%, p < 0.05), tear-trough volume 1.34×, length 1.57×.
   - **Why it got through:** the authors' text says "approximately two-fold greater", but their own figure does not bear it out.
   - **The same overstatement sits elsewhere:** on the PDRN hub card f4 (title "About 2× the Retinol Change", result label "Eye bags about
     2× the retinol change", and the body) and in register claim 5.
   - **Fix:** use the figure's numbers.
2. **HIGH. The chart is built on the authors' rounded ratios, while Figure 6B gives exact percentages for both sides.**
   - **The wrinkle row understates:** "Wrinkles around the eyes" = 2 against an actual 2.96–3.50×.
   - **The eye-bag row overstates** (flag 1).
   - **Suggestion:** rebuild the chart as the day-28 change on each side, PDRN against retinol:

     | Measure               | PDRN   | Retinol |
     | --------------------- | ------ | ------- |
     | Crow's-feet area      | −23.0% | −6.6%   |
     | Under-eye line number | −23.4% | −7.0%   |
     | Elasticity (R2)       | +44.0% | +24.8%  |
     | Firmness (F4)         | −29.6% | −16.3%  |
     | Dermal thickness      | +11.5% | +5.5%   |
     | Dermal density        | +9.6%  | +4.8%   |
     | Eye-bag volume        | −14.8% | −10.2%  |

3. **MEDIUM. The chart's comparator colour fails contrast.** `measurements.chart.series[1].color` is `#9AA3A4`. Template §4: "The comparator
   is grey `#8A9394` … `#9AA3A4` fails at 2.58:1."
4. **MEDIUM. `figures[2]` "Day 14" is a time.** Template §4 says "Key figures are results … Use a time … only when the paper reports no
   further magnitude", and Figure 6B reports one.
   - **Suggested figure:** "−12.4% by day 14".
   - **Label:** "Crow's-feet wrinkle area at day 14".
   - **Note:** "against −3.9% with retinol (p < 0.001); already more than the retinol side reached by day 28 (−6.6%)".
5. **LOW. The page still says the exact statistics are out of reach.** `limits.items[2]` ("The ratios are the authors' own approximations;
   the exact statistics appear in the paper's Figure 6") and the chart subtitle say so, but they have now been read, so the page can state
   them. The `_note` ("exact statistics in Fig 6B only") is out of date in the same way.
6. **LOW. `media.body[0]` claims more blinding than the paper describes.** "Neither they nor the assessors knew which side had which" goes
   beyond the paper, which says only "randomized, double-blind" and never says who was blinded. Suggest: "The study was double-blind: the
   two creams looked the same and were assigned at random." The first half is the paper's word; the identical base is in the Methods.
7. **Register (not config).** Claims 2 ("not '3×'"), 4 ("absolute % changes appear only in a figure") and 5 ("twice as much") predate a
   reading of Figure 6B. They need a verification-log entry and a decision on the wrinkle ratio, which reads 3.0–3.5× by the figure.
8. **Hub before/after pictures** f1 and f4: see §4. These are for Malcolm, because they are live on `/pages/pdrn-research`.

No other conflicts found. I checked the answer, verdict, definition, glance rows, limits 1, 2, 4, 5 and 6, context, FAQ and meaning against
the register and template §4.

## 7. Open questions for the client

1. **Significance marks.** May the page print p-values as the thresholds read from the paper's own key (`#` < 0.05, `##` < 0.01, `###` <
   0.001), given that Figure 6's legend does not repeat that key? The alternative is to say "significant" without a number.
2. **The crow's-feet pair.** Uphold the 2026-08-27 pass (the labels are ready, see §4), or generate a calibrated pair?
3. **The eye-bag pair.** Commission a calibrated pair at about 15% (subtle), or keep a plain photograph?
4. **Grouping.** Crow's feet and under-eye lines in one section (recommended), or split into two, which drops the eye-bag section?
5. **Three how-it-works blocks, or two?** Two of the three come from the same skin-sample experiment. If Malcolm prefers fewer, merge m1 and
   m2.
6. **"About 2×" everywhere.** Correct it on this article (figures, chart, caption), the hub card f4 and register claim 5 to the Figure 6B
   numbers?
7. **Translations.** These blocks are English only. Ye is live in six languages, so a full `build-study-page.py --apply` refuses them until
   de, nl, fr, es and it are added (template §5). Image files are TBD; the builder also refuses "TBD" (no ingredient name), as expected.
