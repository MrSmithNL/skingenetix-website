# Claims register: Collagen skincare (topical collagen — creams and serums)

**Built:** 2026-09-29 · **Scope:** `/pages/collagen-skincare` (rebuild of `/pages/collagen-skin-plumping`, per ADR-2026-09-29-D), answering "do collagen
creams/serums work?" for `collagen cream`, `collagen face cream`, `collagen serum` (+ DE `kollagen creme/serum`, NL `collageen serum/creme`). Covers
**Matrixyl 3000 Pro-Collagen Firming Cream** and **PDRN Collagen Night Cream** (the two products that actually contain collagen), and the honest framing
for "collagen serum" traffic, which has no matching product.
**Standing rule:** use the strongest claim the best evidence supports. It has to be true, sourced, and within EU Regulation 655/2013 (the common criteria:
legal compliance, truthfulness, evidential support, honesty, fairness, informed decision-making). Every claim must read as cosmetic (how skin looks and
feels), never medicinal ("boosts collagen production", "regenerates", "restores" are avoided as product promises).
**Verification standard:** every number below was checked on 2026-09-29 against a primary text — a full paper, an abstract, a CIR final report, or our
own live product/ingredients pages (fetched with curl, a full Chrome user agent). Where only an abstract was available, the row says so and the grade is
lower.
**Out of scope:** oral collagen supplements. The evidence base for oral collagen (peptide drinks, tablets) is a different literature (mostly positive in
industry-funded RCTs, null in independently funded ones) and answers a different question. This register and the page it serves are about **topical**
creams and serums only. Say so explicitly on the page if a visitor's question is really about drinking collagen.

**Grades:** **A** = controlled human study with instrument measurement · **B** = uncontrolled or self-assessed human data, or manufacturer in-vivo data ·
**C** = ex vivo (excised human skin) or reconstructed skin model · **D** = in vitro (cells) or animal · **Review/Safety** = independent expert panel or
systematic review, no new primary data.

---

## 0. Read this first: what our products actually contain

Checked live on 2026-09-29 (`/pages/ingredients`, product pages, fetched with curl + a full Chrome user agent; no Shopify data changed).

|                                                                        | Matrixyl 3000 Pro-Collagen Firming Cream                                                                                                                                                                                                                                                                                                                                                                                                       | PDRN Collagen Night Cream ("PDRN + Collagen Night Cream")                                                                                                                                       | Matrixyl 3000 Firming Serum                                                                                                                                                         | PDRN Renewal Serum                                                                              | Copper Peptide GHK-Cu Renewal Serum                                                                                   |
| ---------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| **Contains collagen?**                                                 | ✅ **Yes** — "Triple Collagen Complex" listed as a key active: "**collagen proteins (Collagen, Hydrolyzed & Soluble Collagen)**"                                                                                                                                                                                                                                                                                                               | ✅ **Yes** — "**Hydrolyzed Collagen**" listed as a key active                                                                                                                                   | ❌ **No.** Key actives: Matrixyl 3000, Palmitoyl Pentapeptide-4, 3-O-Ethyl Ascorbic Acid, Niacinamide, Hyaluronic Acid. No collagen-named ingredient anywhere in the full INCI list | ❌ **No.** Key actives: PDRN, Oligopeptide-1, Copper Tripeptide-1, Niacinamide, Hyaluronic Acid | ❌ **No.** Key actives: GHK-Cu (2%), a "multi-peptide complex", 3-O-Ethyl Ascorbic Acid, Niacinamide, Hyaluronic Acid |
| **Elastin?**                                                           | ⚠️ Printed on the carton ("MATRIXYL 3000 \| TRIPLE COLLAGEN \| **ELASTIN** \| 50ML") and stated in the product FAQ ("contains collagen and **elastin** of animal origin"), but **no ingredient named Elastin or Hydrolyzed Elastin appears anywhere in the disclosed key actives or the full "Other ingredients" INCI list** on `/pages/ingredients`. Same gap the Matrixyl 3000 register flagged on 2026-09-22; **still open on 2026-09-29**. | Not claimed                                                                                                                                                                                     | —                                                                                                                                                                                   | —                                                                                               | —                                                                                                                     |
| **Collagen source species (bovine/marine/fish)?**                      | ❌ **Not disclosed anywhere on the site** (checked `/pages/ingredients` and the product page; no hit for "bovine", "marine" or "fish"). This matters: the independent CIR panel specifically advises fish-derived collagen/elastin be labelled, because fish is a major allergen and reactions have been reported in fish-allergic people (§5).                                                                                                | Same — not disclosed                                                                                                                                                                            | —                                                                                                                                                                                   | —                                                                                               | —                                                                                                                     |
| **"Every formula is vegan" (site-wide intro on `/pages/ingredients`)** | ❌ **Contradicted.** This cream's own FAQ says "No. The formula contains collagen and elastin of animal origin, so it is not suitable for a vegan routine." Both statements are still live on 2026-09-29. Same contradiction the Matrixyl register flagged on 2026-09-22 (§2 #19 there); **unresolved**.                                                                                                                                       | Hydrolyzed Collagen is conventionally animal- or marine-derived (CIR, §5); if ours is, the site-wide "every formula is vegan" claim is also wrong for this product and has never said otherwise | —                                                                                                                                                                                   | —                                                                                               | —                                                                                                                     |

**Four consequences drive most of this register:**

1. **Two products, and only two, may honestly carry a "contains real collagen" claim**: the Matrixyl 3000 Pro-Collagen Firming Cream and the PDRN Collagen
   Night Cream. **No serum contains collagen.** "Collagen serum" search traffic must be answered honestly (§8) — it cannot land on a product page and imply
   the serum contains collagen.
2. **The Elastin gap and the vegan contradiction are pre-existing, still open, and directly relevant to this page** (a "does it work / is it honest" guide
   is exactly where a sharp reader checks the ingredient list against the marketing). **Do not repeat "elastin" as a disclosed active on the new page**
   until the INCI list is corrected or elastin is confirmed present. **Do not repeat "every formula is vegan" anywhere the collagen products are discussed.**
3. **The collagen source (bovine vs marine/fish) needs disclosure**, both for the vegan claim and because the independent CIR safety panel specifically
   flags fish-derived collagen/elastin as needing allergen labelling (§5). This is a genuine open item for Malcolm/the formulator, not something this
   register can resolve from public data.
4. **The PDRN cream's "Other ingredients" list ends "…Palmitoyl Tripeptide-1, Palmitoyl Tetrapeptide-7"** — the two Matrixyl 3000 peptides — without
   naming them as key actives. The Matrixyl 3000 register (§6 gap 2, 2026-09-22) already flagged this as a possible base-formula overlap between the two
   creams; it is unchanged on 2026-09-29. Not a topical-collagen issue, but worth a line in the gaps (§6) since this page touches both creams.

---

## 1. Headline claims, ready to use (ranked)

### Claim 1 (hero, mechanism). Size decides the job: film on the surface, or a trace in the outer layer

**Claim:** _"Collagen works on skin in two different ways depending on its size. Native and soluble collagen molecules are far too large to cross intact
skin, so they sit on the surface as a moisture-retaining film. Hydrolyzed collagen — collagen broken down into smaller peptides — is small enough that a
fraction can reach the skin's outermost layer and act as a natural moisturising factor."_

- **Fact:** the general size rule for skin penetration is documented by Bos & Meinardi (2000): compounds need to be **under about 500 Da** to cross the
  stratum corneum in meaningful amounts; this is the basis of "the 500 Dalton rule" used across dermatology and transdermal drug design.
  **Source:** Bos JD, Meinardi MMHM. "The 500 Dalton rule for the skin penetration of chemical compounds and drugs." _Exp Dermatol._ 2000;9(3):165-9.
  PMID 10839713. **Read: abstract.**
- **Collagen's own sizes, from the independent CIR safety panel (Table 2 of the report):** **native Collagen 130,000 to >1,000,000 Da**; **Soluble
  Collagen 30,000–40,000 Da, up to an average of 300,000 Da**; **Hydrolyzed Collagen 400–25,000 Da** (most cosmetic hydrolysates cluster 400–2,000 Da,
  per the same report's manufacturing data). Every one of these is far above the 500 Da line except the smallest hydrolyzed-collagen peptides, which sit
  right at or just above it.
  **Source:** CIR Expert Panel (Burnett CL et al). "Safety Assessment of Skin and Connective Tissue-Derived Proteins and Peptides as Used in Cosmetics."
  Final report released 2017-10-05; published _Int J Toxicol._ 2022. DOI 10.1177/10915818221104783. **Read: full CIR final-report PDF.**
- **Direct penetration test (ex vivo, animal skin):** radiolabelled **native collagen and its individual alpha chains did not penetrate intact
  stratum corneum at all** over 48 hours; native collagen only crossed when the skin's barrier had first been tape-stripped away. **Grade D**
  (ex vivo, hairless mouse skin, 1988; classic, still cited by current collagen-cosmetics papers).
  **Source:** Coapman SD, Lichtin JL, Sakr A, Schiltz JR. "Studies of the Penetration of Native Collagen, Collagen Alpha Chains, and Collagen Cyanogen
  Bromide Peptides Through Hairless Mouse Skin in Vitro." _J Soc Cosmet Chem._ 1988;39:275-281. **Read: abstract + secondary summary.**
- **Hydrolyzed collagen's partial penetration, and its main job as a humectant:** a 2020 review reports that in one study, **about 8% of hydrolyzed
  collagen in the 5–13 kDa range penetrated the skin**, and states plainly that hydrolyzed collagen "has been identified as a cosmetic ingredient with
  good moisturizing properties **at the stratum corneum layer** of the skin" — i.e. mainly a surface/outer-layer humectant, not a deep-penetrating active.
  A cited 30-day human trial of a 10%-concentration fish-scale collagen-peptide facial mask found "the higher increments in skin moisture content and
  relatively elasticity" at that concentration. **Grade: review**, citing mixed-quality underlying studies not independently re-verified here.
  **Source:** Aguirre-Cruz G, León-López A, Cruz-Gómez V, Jiménez-Alvarado R, Aguirre-Álvarez G. "Collagen Hydrolysates for Skin Protection: Oral
  Administration and Topical Formulation." _Antioxidants._ 2020;9(2):181. DOI 10.3390/antiox9020181. **Read: full text.**
- **Attach to:** the answer-first paragraph (§7), the Matrixyl 3000 Pro-Collagen Firming Cream and PDRN Collagen Night Cream (both contain hydrolyzed
  and/or native/soluble collagen per §0), and the hub mechanism section. **Conditions:** (a) never say hydrolyzed collagen "penetrates the dermis" or
  "replaces lost collagen" — nothing in this evidence base shows that; (b) keep "a fraction" / "some" in front of any hydrolyzed-collagen penetration
  claim, never "penetrates"; (c) this is a mechanism claim, not an efficacy claim — pair it with claim 2 or 3 for outcomes.

### Claim 2. Independent, expert-panel safety clearance for every collagen ingredient we use

**Claim:** _"Collagen, Hydrolyzed Collagen and Soluble Collagen — the three ingredients in our Triple Collagen Complex — are each assessed as safe for
cosmetic use by the independent U.S. Cosmetic Ingredient Review (CIR) Expert Panel, at concentrations up to 96% in face and neck skincare."_

- **Fact:** the CIR Expert Panel's final report concluded that **Collagen, Hydrolyzed Collagen, Soluble Collagen, Elastin and Hydrolyzed Elastin** (among
  19 skin- and connective-tissue-derived ingredients reviewed) **"are safe in the present practices of use and concentration"**. Industry survey data in
  the same report show **Collagen has the highest reported maximum use concentration of the 19 ingredients: up to 96% in face and neck skincare
  products**; Hydrolyzed Collagen is used in 543 formulations (up to 16.5% in leave-on products); Soluble Collagen in 425 formulations. Human and animal
  irritation, sensitisation, phototoxicity and ocular-irritation data reviewed were consistently negative or minimal at the concentrations tested
  (Hydrolyzed Collagen non-irritating in human dermal tests up to 50%; nonsensitising in a guinea-pig maximisation test and a 50-subject HRIPT).
- **Source:** CIR Expert Panel (Burnett CL et al). "Safety Assessment of Skin and Connective Tissue-Derived Proteins and Peptides as Used in Cosmetics."
  Final report released 2017-10-05; published _Int J Toxicol._ 2022. DOI 10.1177/10915818221104783. **Read: full text (CIR PDF).**
- **Grade: Review/Safety** — this is an independent expert-panel safety finding, not an efficacy grade.
- **Attach to:** both collagen-containing creams, and the hub safety section. **Conditions:** (a) this is an **ingredient**-level safety finding, not a
  test of our finished formula (see §5); (b) the panel's report also raises a fish-allergy labelling point for fish-sourced collagen/elastin — **do not
  use this claim without first confirming our collagen's source species** (§0, §6 gap 1); (c) never round "assessed as safe" up to "clinically proven
  gentle" or "hypoallergenic" — those need product-level testing we do not have (§5).

### Claim 3. A proprietary, penetration-engineered collagen cream showed measurable 4-week changes in an uncontrolled human trial

**Claim (for the mechanism/background section, never attributed to our product):** _"When collagen is specially engineered to reach the skin — as
120-nanometre micronized fibrillar particles inserted into a cream, rather than left as ordinary large collagen fibres — a small clinical study measured
real changes after four weeks: wrinkles reduced 19%, skin firmness up nearly 40%, and hydration markedly improved."_

- **Fact, read at source (full paper):** 55 healthy women aged 35–50 used a cream containing **0.2% micronized collagen (m-collagen, ~120 nm particles)**
  twice daily for 4 weeks, in a **single-arm, open-label study with no placebo or vehicle-control arm** (all comparisons are against the same subjects'
  own baseline; the paper reports the design as "within-treatment analysis", t-test, p<0.05). Results at week 4 vs baseline: profilometry (Rz, fine
  lines/wrinkles) **−19.24%**; Cutometer firmness (R0) **+~38%**; elasticity (R2/R5/R7) **+37% / +25% / +39%**; Corneometer hydration **+197%** (this last
  figure is measured against a **washed-out, unmoisturised baseline** — see "Claims to avoid" §4, it is not a comparison with any other cream). Author's
  own paper states the rationale plainly: _"collagen fibers are too large to penetrate the stratum corneum (SC)… a topically applied collagen cream has
  little to no effect on the skin"_ without this kind of engineering. A separate, related paper by the same authors used ex vivo human skin to show the
  micronized particles reach the stratum corneum and epidermis in 3 hours (Grade C).
- **Source:** Lubart R, Lipovsky A. "Immediate and Long Term Clinical Benefits of a Novel Topical Micronized Collagen Face Cream." _J Cosmet Dermatol Sci
  Appl._ 2022;12:153-163. DOI 10.4236/jcdsa.2022.124013. **Read: full text (PDF).** Companion ex vivo paper: Lubart R, Yariv I, Fixler D, Lipovsky A. "A
  Novel Facial Cream Based on Skin-penetrable Fibrillar Collagen Microparticles." _J Clin Aesthet Dermatol._ 2022;15(5):59-64.
- **Grade: B** (human, instrument-measured, but **uncontrolled/single-arm**, manufacturer-funded — Hava Zingboim Ltd. funded the study and one author is
  employed there — and published in a lower-tier, non-mainstream journal, _Journal of Cosmetics, Dermatological Sciences and Applications_ [SCIRP]).
- **Attach to:** the "does the evidence exist at all?" part of the answer, and nowhere else. **Conditions:** (a) **this is not our product** — it is a
  different manufacturer's proprietary 120 nm micronized-collagen technology at 0.2%, and our creams use standard hydrolyzed/soluble/native collagen, not
  this delivery system; never let a reader infer it describes our cream; (b) never quote the 197% hydration figure without "against an unmoisturised
  baseline, not against another cream" — see §4; (c) no placebo arm means "significant" here means "different from before treatment", not "different
  from a comparable moisturiser"; (d) use only as evidence that _engineered_ topical collagen has been measured to do something in a real trial, in
  contrast with plain collagen fibres, which the same authors say do not.

### Claim 4. A hydrolyzed-collagen combination cream measurably improved hydration and barrier function in a small pilot

**Claim:** _"In a pilot study, a cream combining hydrolyzed collagen with hyaluronic acid and proteoglycan roughly doubled skin hydration and cut water
loss by about a third after four weeks, in people with dry, eczema-prone skin."_

- **Fact, read at source (full text):** 23 participants (mean age 40.7, mostly Asian women) with mild atopic dermatitis or dry/xerotic skin applied a
  cream containing 0.01% of a proprietary liposome combining soluble proteoglycan, hyaluronic acid and **hydrolyzed collagen**, twice daily for 4 weeks,
  in a **prospective, single-arm pilot study with no placebo/vehicle-control arm**. Transepidermal water loss (TEWL) fell from 26.47±7.36 to 17.43±6.35
  (p<0.005); Corneometer hydration rose from 30.78±8.24 to 56.34±11.57 (p<0.005); itching (VRS) fell from 1.78±0.42 to 0.23±0.42 (p<0.005).
- **Source:** Lee YI, Lee SG, Kim J, Choi S, Jung I, Lee JH. "Proteoglycan Combined with Hyaluronic Acid and Hydrolyzed Collagen Restores the Skin Barrier
  in Mild Atopic Dermatitis and Dry, Eczema-Prone Skin: A Pilot Study." _Int J Mol Sci._ 2021;22(19):10450. **Read: full text.**
- **Grade: B** (human, instrument-measured, but uncontrolled/single-arm; a combination product, so hydrolyzed collagen's individual share of the effect
  cannot be isolated). Independently funded (Korean government/university grants); no stated ingredient-maker conflict, but the proprietary "H.ECM"
  liposome carrier is a trademarked ingredient.
- **Attach to:** the barrier/hydration section of the mechanism discussion. **Conditions:** (a) this is a **combination product**, so never attribute the
  full effect to hydrolyzed collagen alone; (b) the population was dry/eczema-prone skin, not general anti-ageing users — frame as "skin-barrier support",
  not "wrinkle reduction"; (c) no placebo arm.

### Claim 5. Where "does topical collagen firm skin?" already has an answer on the store — keep it, and now source it

**Claim (matches the live Firming-page FAQ, now with sources attached):** _"Hydrolyzed collagen peptides are small, low-molecular-weight fragments;
larger collagen molecules form a moisture-retaining film on the surface. Combined with signal peptides (Matrixyl 3000, GHK-Cu), topical collagen
supports a visibly firmer, smoother finish."_

- **Fact:** this exact sentence is live today (2026-09-29) on `/pages/firming-skin-density`, FAQ "Can topical collagen really firm skin?" — and per
  ADR-2026-09-29-D, this FAQ is planned to move to the new collagen page. **It is accurate and consistent with claim 1 above**, but currently carries
  **no citation** on the live page.
- **Source:** claim 1's sources (Bos & Meinardi 2000; CIR MW table; Coapman 1988; Aguirre-Cruz 2020).
- **Grade:** inherits claim 1's mix (mechanism review + D + Review).
- **Attach to:** the new collagen page, verbatim or near-verbatim, now with the citations claim 1 provides. **Conditions:** this sentence must **not be
  contradicted** by the new page (the brief's hard requirement) — the new page's answer-first paragraph (§7) is written to agree with it, not compete
  with it.

### Claim 6 (ingredient, not collagen itself). Matrixyl 3000's peptides are associated with the skin's own collagen activity — summarised from the Matrixyl 3000 register

**Claim:** _"Matrixyl® 3000, in the serum and both creams, is a pair of signal peptides shown in lab tests on skin cells to raise collagen I by up to
256%, and in the manufacturer's 2-month clinical study to reduce the area of deep wrinkles by 39%."_

- **Fact and full sourcing:** see `docs/claims/matrixyl-3000.md` §1 claims 1 and 4 (Sederma brochure v.131030, 2013, Grade B; US Patent 6,974,799 B2,
  Grade D). **Do not re-derive these numbers here** — the Matrixyl register is the source of truth and carries its own wording conditions (e.g. "in lab
  tests on skin cells", never "boosts collagen in your skin").
- **Grade:** B (in-vivo, manufacturer) / D (in-vitro, manufacturer) — see the Matrixyl register for the full breakdown.
- **Attach to:** all Matrixyl 3000 products (serum, both creams). **Conditions:** exactly as the Matrixyl 3000 register's §1 and §4 specify — this is an
  **ingredient** claim about collagen _activity_, never a claim that the product "contains collagen" (the serum does not; the two creams that do contain
  collagen separately list it as "Triple Collagen Complex", not as part of Matrixyl 3000).

### Claim 7 (ingredient, not collagen itself). Copper peptide GHK-Cu's own trial evidence — summarised from the copper-peptide register

**Claim:** _"Copper peptide GHK-Cu, in the PDRN Collagen Night Cream and the copper-peptide products, reduced wrinkle volume 55.8% more than a plain
serum base and 31.6% more than a Matrixyl 3000 product, in a double-blind trial."_

- **Fact and full sourcing:** see `docs/claims/copper-peptide-ghk-cu.md` §1 claims 1–2 (Badenhorst et al. 2016, _J Aging Sci_, Grade A−).
- **Attach to:** PDRN Collagen Night Cream (contains Copper Tripeptide-1) and copper-peptide products. **Conditions:** exactly as that register's §1
  specifies — ingredient claim only, "a plain serum base" (never "the same serum without GHK-Cu"), never name the competitor brand tested.

---

## 2. What must not be contradicted (Firming page and old collagen-skin-plumping page)

| Live text                                                                                                                                                                                                                                                                                                            | Where                                                                     | Verdict for the new collagen page                                                                                                                                                                                                                                                |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "A visibly firmer look benefits from two things: supporting the skin's own collagen activity and supplying collagen proteins directly. Signal peptides are associated with the skin's natural collagen activity, while topical collagen proteins provide immediate support for a smoother, plumper-looking surface." | `/pages/firming-skin-density`, "The Collagen-Peptide Approach to Firming" | ✅ **Keep this framing exactly.** It distinguishes "supports collagen activity" (peptides, claim 6) from "supplies collagen protein" (claim 1/5) — the same distinction this register makes. The new page must use the same two-track structure, not a third, conflicting story. |
| "A triple collagen complex (hydrolyzed, soluble and native collagen) helps support a smoother, plumper-looking surface… Hydrolyzed collagen peptides penetrate the skin surface, while larger collagen molecules form a protective film that improves moisture retention."                                           | `/pages/firming-skin-density`, Pro-Collagen cream block                   | ✅ **Consistent with claim 1** (now sourced). Confirms the cream's "Triple Collagen Complex" matches its ingredients-page description of "Collagen, Hydrolyzed & Soluble Collagen" (§0).                                                                                         |
| "Can topical collagen really firm skin?" FAQ (claim 5 above)                                                                                                                                                                                                                                                         | `/pages/firming-skin-density`                                             | ✅ **Reuse, add citations.** Per ADR-2026-09-29-D this FAQ moves here.                                                                                                                                                                                                           |
| Old `/pages/collagen-skin-plumping` page                                                                                                                                                                                                                                                                             | retired, 301 to the new page                                              | Not re-verified line by line here (the ADR already flags it duplicated the Firming page and "contradicted the Firming page on topical collagen"); **do not carry any of its wording forward without checking it against §1 and §4 of this register first.**                      |

---

## 3. Evidence table (every source reviewed)

| #   | Source                                                                                                         | Design                                                                                          | n                                             | Concentration                                               | Duration           | Measure                                                                               | Result (as read)                                                                                                                                                                                                                                                            | Control/stats                                | Sponsor/conflict                                                                                                                        | Grade                                        | Read                                                                                                     |
| --- | -------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- | --------------------------------------------- | ----------------------------------------------------------- | ------------------ | ------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| 1   | **Bos & Meinardi 2000**, _Exp Dermatol_ 9(3):165-9, PMID 10839713                                              | Position paper                                                                                  | —                                             | —                                                           | —                  | —                                                                                     | Proposes the 500 Da rule for skin penetration                                                                                                                                                                                                                               | —                                            | Academic                                                                                                                                | Mechanism/review                             | Abstract                                                                                                 |
| 2   | **Coapman et al. 1988**, _J Soc Cosmet Chem_ 39:275-281                                                        | Ex vivo, hairless mouse skin, radiolabelled tracer                                              | —                                             | —                                                           | 48 h               | Penetration through intact vs tape-stripped skin                                      | Native collagen/alpha chains: ~0% through intact skin; 60-70% through tape-stripped (barrier-removed) skin                                                                                                                                                                  | Intact vs stripped skin                      | Academic                                                                                                                                | D                                            | Abstract + secondary summary                                                                             |
| 3   | **CIR Expert Panel (Burnett et al.)**, final report 2017 / _Int J Toxicol_ 2022, DOI 10.1177/10915818221104783 | Independent safety review, 19 ingredients                                                       | —                                             | Up to 96% (Collagen); 400-16.5% range (Hydrolyzed Collagen) | —                  | Irritation, sensitisation, phototoxicity, MW ranges                                   | "Safe in the present practices of use and concentration" for Collagen, Hydrolyzed Collagen, Soluble Collagen, Elastin, Hydrolyzed Elastin. MW: native Collagen 130,000->1,000,000 Da; Soluble Collagen 30,000-40,000 (up to 300,000 avg); Hydrolyzed Collagen 400-25,000 Da | —                                            | Independent panel                                                                                                                       | Review/Safety                                | Full text                                                                                                |
| 4   | **Aguirre-Cruz et al. 2020**, _Antioxidants_ 9(2):181, DOI 10.3390/antiox9020181                               | Narrative review                                                                                | —                                             | Topical HC typically 1-10 kDa                               | —                  | Penetration, humectant mechanism                                                      | ~8% of 5-13 kDa HC penetrated skin in one cited study; HC "good moisturizing properties at the SC layer"; a cited 30-day, 10%-conc. fish-collagen facial-mask trial improved moisture and elasticity                                                                        | Varies by cited study                        | Academic                                                                                                                                | Review                                       | Full text                                                                                                |
| 5   | **Lee et al. 2021**, _Int J Mol Sci_ 22(19):10450                                                              | Prospective, single-arm pilot                                                                   | 23 (25 enrolled), mostly women, mean age 40.7 | 0.01% proteoglycan+HA+hydrolyzed collagen liposome          | 4 wk, 2x/day       | TEWL, Corneometer, itching (VRS)                                                      | TEWL 26.47→17.43 (p<0.005); hydration 30.78→56.34 (p<0.005); itch 1.78→0.23 (p<0.005)                                                                                                                                                                                       | vs own baseline; no control arm              | Korean govt/university grants; no ingredient-maker conflict declared                                                                    | B (combination)                              | Full text                                                                                                |
| 6   | **Lubart & Lipovsky 2022**, _J Cosmet Dermatol Sci Appl_ 12:153-163, DOI 10.4236/jcdsa.2022.124013             | Single-arm, open-label clinical study                                                           | 55 women, 35-50                               | 0.2% micronized (~120 nm) fibrillar collagen                | 4 wk, 2x/day       | Profilometry, Cutometer (R0/R2/R5/R7), Corneometer                                    | Wrinkles -19.24% (p<0.05); firmness +38%; elasticity +25-39%; hydration +197% (vs unmoisturised baseline)                                                                                                                                                                   | vs own baseline; no control/placebo arm      | Hava Zingboim Ltd. (manufacturer); 1 author employed there                                                                              | B                                            | Full text                                                                                                |
| 7   | **Lubart et al. 2022**, _J Clin Aesthet Dermatol_ 15(5):59-64                                                  | Ex vivo human skin, 3 h application                                                             | —                                             | 0.2% in cream, ~120 nm particles                            | 3 h                | IMOPE penetration imaging, EPR spectroscopy                                           | Collagen microparticles detected in stratum corneum/epidermis; 77% reduction in OH-radical intensity                                                                                                                                                                        | —                                            | Hava Zingboim Ltd.; 2 authors consultants to manufacturer                                                                               | C                                            | Full text (ex vivo section); recaptcha blocked the companion clinical-arm claims, corroborated via row 6 |
| 8   | **Dondero et al. 2025**, _Sci Rep_ 15:29391, DOI 10.1038/s41598-025-11372-5                                    | 2D cell culture + 3D reconstructed skin models (EpiDerm, EpiDerm-FT); **not living human skin** | —                                             | Hydrolyzed fish collagen (HFC), ~2 kDa                      | Single application | Cell viability, wound-healing scratch assay, COL3A1 gene expression, dermal thickness | Increased viability/wound-healing at 47 µgHyp/mL; COL3A1 induction 11.37-fold (formulated) vs 1.59-fold (solution alone); dermal thickness increased at higher concentrations                                                                                               | vs untreated/solution controls in lab models | Horizon 2020 + Italian grants; collagen and cream "kindly supplied by Ardes s.r.l." (ingredient maker); no competing interests declared | D/C (lab tissue models, not real human skin) | Full text                                                                                                |
| 9   | **Matrixyl 3000 register**, `docs/claims/matrixyl-3000.md` §1 claims 1, 4                                      | See that register                                                                               | See that register                             | See that register                                           | See that register  | See that register                                                                     | -39% deep-wrinkle area (2 mo, manufacturer); +256% collagen I (lab, highest dose)                                                                                                                                                                                           | See that register                            | Manufacturer (Sederma)                                                                                                                  | B / D                                        | Already verified there                                                                                   |
| 10  | **Copper-peptide register**, `docs/claims/copper-peptide-ghk-cu.md` §1 claims 1-2                              | See that register                                                                               | See that register                             | See that register                                           | See that register  | See that register                                                                     | +55.8% wrinkle-volume reduction vs plain serum base; +31.6% vs Matrixyl 3000 product                                                                                                                                                                                        | See that register                            | Snowberry NZ (manufacturer)                                                                                                             | A−                                           | Already verified there                                                                                   |

---

## 4. Claims to AVOID

| Claim                                                                                                                                    | Why                                                                                                                                                                                                                                                                                                                                            |
| ---------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "Collagen creams penetrate deep into the dermis" / "reach the deeper layers of your skin"                                                | Native and soluble collagen (30,000 Da to >1,000,000 Da) do not cross intact skin at all (Coapman 1988); hydrolyzed collagen's own literature caps meaningful penetration at the stratum corneum, not the dermis (Aguirre-Cruz 2020).                                                                                                          |
| "Replaces your own collagen" / "restores lost collagen" / "boosts collagen production" as a product promise for a plain-collagen product | No study in this register shows topical collagen protein triggers new collagen synthesis in living human skin; that is a different mechanism (matrikine peptide signalling — claim 6/Matrixyl) from supplying collagen protein directly (claim 1/5). Also risks a medicinal reading under Regulation 1223/2009.                                |
| "Clinically proven to reduce wrinkles" for our Pro-Collagen cream or PDRN cream, unqualified                                             | We have **no product-level human trial** of either cream. The only human collagen-cream trials in this register (rows 5-6) test different manufacturers' different, more concentrated or specially engineered formulas, not ours.                                                                                                              |
| Quoting the Lubart 2022 "197% more hydrated" figure without "against an unmoisturised baseline"                                          | The comparison is the treated cream vs the same subjects' skin during a product-free washout period, not vs an untreated area during use, and not vs a competing moisturiser. Any occlusive/humectant cream would show a large percentage rise from that baseline; it is not evidence our (or any) collagen cream beats ordinary moisturisers. |
| "Our micronized collagen technology" / any reference implying our cream uses the Lubart/Hava Zingboim 120 nm delivery system             | We do not. Our creams use standard hydrolyzed/soluble/native collagen (§0).                                                                                                                                                                                                                                                                    |
| "Every formula is vegan" anywhere near the two collagen creams                                                                           | Directly contradicted by the Matrixyl cream's own FAQ ("contains collagen and elastin of animal origin"). See §0 and §6 gap 2.                                                                                                                                                                                                                 |
| "Marine collagen" / "sustainably sourced collagen" / "bovine-free"                                                                       | Source species is not disclosed anywhere on the site (§0). Do not invent a sourcing story.                                                                                                                                                                                                                                                     |
| "Hypoallergenic" / "gentle for sensitive skin" / "dermatologically tested" for our collagen products                                     | No product-level HRIPT or in-use tolerance test on record for either cream (see §5). The CIR conclusion is an ingredient-level safety finding, not a test of our finished formula.                                                                                                                                                             |
| Any percentage from row 8 (Dondero 2025) presented as skin evidence                                                                      | That study used 2D cell cultures and 3D reconstructed-skin lab models, not living human skin or human volunteers — say "in lab-grown skin models", never "in skin" unqualified.                                                                                                                                                                |
| Naming Strivectin, or any competitor brand tested in the copper-peptide trial                                                            | Comparative-advertising risk; already flagged in the copper-peptide register.                                                                                                                                                                                                                                                                  |
| "Collagen serum" as a product name or implying any of our serums contain collagen                                                        | No serum we sell contains a collagen-named ingredient (§0). See §8 for the honest framing.                                                                                                                                                                                                                                                     |

---

## 5. Safety and tolerability, as reported

- **CIR Expert Panel (independent, final report 2017 / published 2022):** Collagen, Hydrolyzed Collagen, Soluble Collagen, Elastin and Hydrolyzed
  Elastin are each **"safe in the present practices of use and concentration in cosmetics"**. Supporting data include: Hydrolyzed Collagen non-irritating
  in human dermal tests up to 50% solution; nonsensitising in a guinea-pig maximisation test and in a 50-subject HRIPT (20% solution); not phototoxic or
  photosensitising to humans at up to 0.5%; **UV-induced erythema was decreased** after a 10% solution of Hydrolyzed Collagen (MW 1,500 Da) applied
  post-irradiation (a positive, usable finding, ingredient-level only). Hydrolyzed Elastin (25% w/v) produced no dermal irritation or sensitisation in a
  52-subject HRIPT.
- **Allergy flag the Panel raises, directly relevant here:** fish is a major food allergen, and the Panel reviewed **case reports of allergic reactions
  (urticaria, anaphylaxis) in fish-allergic individuals** after using cosmetics containing fish-derived Elastin, Atelocollagen or Hydrolyzed Collagen. The
  Panel **"advised manufacturers to label products containing these fish-derived ingredients"**. **Our collagen's source species is not disclosed
  anywhere on the site (§0) — this must be confirmed before any "safe for all skin types" or unqualified safety claim is made about the two collagen
  creams.**
- **One relevant reaction in the general protein-hydrolysate literature:** in a study of hairdressers with hand dermatitis, 3 of 12 sensitised patients
  reacted to a trademarked 1% Hydrolyzed Collagen solution on a scratch/prick test — a pre-sensitised population, not general users, but a reminder that
  "hypoallergenic" needs product-level testing, not an ingredient-level CIR finding.
- **Our products:** **no product-level tolerance study (HRIPT or in-use test) on record** for the Matrixyl 3000 Pro-Collagen Firming Cream or the PDRN
  Collagen Night Cream. Use the ingredient-level CIR finding (claim 2) plus a plain usage fact ("suitable for daily use"), not a tolerance claim, until
  one exists.

---

## 6. Gaps

1. **Collagen source species (bovine, porcine, marine/fish) is not disclosed anywhere on the site** for either collagen-containing cream. This blocks
   (a) resolving the "every formula is vegan" contradiction, (b) any fish-allergen labelling the CIR panel recommends, (c) any sourcing claim. **Ask the
   formulator/supplier before the new page ships.**
2. **Elastin is named on the pack and in the FAQ but is not in the disclosed "Key Active Ingredients" or full "Other ingredients" INCI list** for the
   Matrixyl 3000 Pro-Collagen Firming Cream on `/pages/ingredients`. Carried over, unresolved, from the Matrixyl 3000 register (§6 gap 2, 2026-09-22).
   Confirm against the formula sheet/carton artwork before the new collagen page repeats "elastin" as a disclosed active.
3. **No product-level human trial (efficacy or tolerance) exists for either of our two collagen creams.** Everything in §1 claims 3-4 is either a
   different manufacturer's more concentrated/engineered formula, or a combination product that cannot isolate collagen's share. The honest ceiling for
   product-specific claims is "contains a triple collagen complex (assessed safe by the independent CIR panel), alongside Matrixyl 3000 / GHK-Cu, which
   do have their own trial evidence" (claims 6-7).
4. **PDRN Collagen Night Cream's "Other ingredients" list ends with the two Matrixyl 3000 peptides**, undeclared as key actives, mirroring squalane/
   allantoin appearing in the Matrixyl cream's key actives but the PDRN cream's "other ingredients". Same base-formula-overlap question the Matrixyl
   register raised on 2026-09-22 (§6 gap 2 there); not resolved by anything read for this register. Not itself a collagen-claims problem, but worth
   flagging since this page discusses both creams.
5. **Oral collagen literature was deliberately not reviewed for grading here** (out of scope, per the brief). If the new page's FAQ fields "does
   drinking collagen work better?", that needs its own, separate research pass — do not answer it from this register.
6. **Dondero et al. 2025 and the Lubart/Lipovsky papers are the newest topical-collagen primary literature found (2025/2022)**; a repeat PubMed sweep
   should happen before this register is 6 months old (2027-03), per the standing "no competitor/technical research older than 6 months without
   re-validation" rule.
7. **The Coapman 1988 and Bos & Meinardi 2000 sources were read at abstract/secondary-summary level only**, not full text (both are old, paywalled
   papers). The mechanism conclusion they support (native collagen too large to penetrate) is corroborated independently by the CIR MW table and by the
   Lubart 2022 paper's own stated rationale, so the claim stands on three independent sources even without the two oldest full texts.
8. **Aguirre-Cruz 2020's 30-day fish-collagen facial-mask trial was read only as summarised by the review**, not at its own primary source (the review
   did not give a full citation for it in what was extracted). Do not cite that specific 30-day trial's numbers as a standalone claim without finding and
   reading its primary paper first.

---

## 7. Answer-first paragraph — "Do collagen creams work?" (for the page's overview/definition block)

> **Collagen works on skin in two different ways, depending on molecule size. Native and soluble collagen molecules are too large to cross intact skin,
> so they sit on the surface as a moisture-retaining film. Hydrolyzed collagen peptides are small enough that some reach the skin's outer layer and act
> as a humectant.** Neither replaces the collagen your skin makes itself — for that, look to signal peptides like Matrixyl® 3000 and copper peptide
> GHK-Cu, which have their own trial evidence.

(51 words for the bold, self-contained sentence pair; one trailing sentence links to the peptide products, matching the page's job of leading to
Skingenetix products without overclaiming.)

---

## 8. "Collagen serum" — the honest framing (we sell none)

**The fact:** none of our five serums contains a collagen-named ingredient (§0). Two creams do. "Collagen serum" carries real, unowned search volume
(GB 605/mo, US collagen serum terms, DE `kollagen serum` 317/mo, NL `collageen serum` 102/mo — per the keyword pull behind ADR-2026-09-29-D) that this
page must answer honestly rather than ignore or mislabel.

**The honest answer, in three moves:**

1. **Say plainly that we don't sell a collagen serum**, and why that's not a gap: collagen protein molecules are generally too large for a lightweight
   serum format to do much with (claim 1) — the format collagen actually works in is a cream, where it can sit on the surface as an occlusive,
   moisture-retaining layer (which is also why both our collagen products are creams, not serums).
2. **Distinguish "collagen serum" from "peptide serum" for the reader**, then point to the Matrixyl 3000 Firming Serum as the honest peptide-serum
   answer: it contains Matrixyl® 3000 and palmitoyl pentapeptide-4, matrikine peptides **associated with the skin's own collagen activity** (claim 6),
   **not collagen protein itself**. The product page's own copy already uses safe wording here ("matrikine peptides associated with the skin's collagen
   activity" — Matrixyl register §2 #17). Reuse that register's approved wording; never say the serum "contains collagen" or "boosts your collagen".
3. **Route the reader who specifically wants collagen protein to the two creams** (Matrixyl 3000 Pro-Collagen Firming Cream, PDRN Collagen Night Cream),
   with claim 1/5's honest mechanism claim attached, and claim 2's independent safety finding.

**Wording to use:** _"Looking for a collagen serum? We don't make one — collagen molecules are generally too large for a lightweight serum to carry
usefully. Our Matrixyl® 3000 Firming Serum instead uses signal peptides associated with the skin's own collagen activity. If you want collagen protein
itself, our Pro-Collagen Firming Cream and PDRN Collagen Night Cream both contain a triple collagen complex / hydrolyzed collagen."_

**Wording to avoid:** "our serum works like a collagen serum", "collagen-boosting serum" (the Matrixyl register already flags "collagen boosting" as
risking a physiological-action/medicinal reading — §4 there), any sentence that lets "peptide serum" and "collagen serum" blur into the same claim.

---

## 9. Verification log — 2026-09-29

| What                                                                                                                             | Where read                                                                  | Result                                                                                                                                                                                                                      |
| -------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Matrixyl 3000 Pro-Collagen Firming Cream: key actives + full INCI                                                                | `/pages/ingredients#pro-collagen-cream`, curl fetch 2026-09-29              | "Triple Collagen Complex - collagen proteins (Collagen, Hydrolyzed & Soluble Collagen)"; full list ends "...Glucose, Acetyl Hexapeptide-8." No Elastin anywhere in the list.                                                |
| Matrixyl 3000 Pro-Collagen Firming Cream: product-page accordion + FAQ                                                           | `/products/matrixyl-3000-pro-collagen-firming-cream`, curl fetch 2026-09-29 | Accordion repeats the same 5 key actives. FAQ "Is it vegan?" → "No. The formula contains collagen and elastin of animal origin..." — still live.                                                                            |
| PDRN Collagen Night Cream: key actives + full INCI                                                                               | `/pages/ingredients#pdrn-collagen-cream`, curl fetch 2026-09-29             | "Hydrolyzed Collagen - collagen proteins for a smoother, plumper-looking surface" is a key active. Full list ends "...Polysorbate 20, Palmitoyl Tripeptide-1, Palmitoyl Tetrapeptide-7."                                    |
| Matrixyl 3000 Firming Serum, PDRN Renewal Serum, Copper Peptide GHK-Cu Renewal Serum, Glutathione Brightening Serum: key actives | `/pages/ingredients`, curl fetch 2026-09-29                                 | None lists a collagen-named ingredient.                                                                                                                                                                                     |
| Site-wide vegan claim                                                                                                            | `/pages/ingredients` intro, curl fetch 2026-09-29                           | "Every formula is vegan, cruelty-free and free from parabens, sulfates, fragrance, mineral oil and artificial colors." Still live, still contradicted by the Matrixyl cream FAQ.                                            |
| Firming page's existing topical-collagen mechanism claim and FAQ                                                                 | `/pages/firming-skin-density`, curl fetch 2026-09-29                        | "The Collagen-Peptide Approach to Firming" section and "Can topical collagen really firm skin?" FAQ, quoted verbatim in §1 claim 5 and §2.                                                                                  |
| Bos & Meinardi 2000                                                                                                              | PubMed/Semantic Scholar summaries                                           | 500 Da rule confirmed as stated.                                                                                                                                                                                            |
| Coapman et al. 1988                                                                                                              | Secondary summary (full text paywalled, not accessed)                       | Native collagen/alpha chains: ~0% penetration through intact skin, 60-70% through tape-stripped skin.                                                                                                                       |
| CIR final report (skin/connective-tissue proteins and peptides)                                                                  | Full CIR PDF, `tsupep092017final.pdf`, fetched 2026-09-29                   | All figures in §1 claim 2, §3 row 3 and §5 read directly from the report's Abstract, Table 2 (MW), Table 5/6 (use concentrations), Dermal Irritation and Sensitization Studies, and Clinical Studies/Case Reports sections. |
| Aguirre-Cruz et al. 2020                                                                                                         | Full text (PMC7070905)                                                      | MW ranges, ~8% penetration figure, humectant-mechanism quote, and the 30-day fish-collagen mask trial summary all as extracted and quoted in §1 claim 1 and §3 row 4.                                                       |
| Lee et al. 2021                                                                                                                  | Full text (PMC8508667)                                                      | All figures in §1 claim 4 and §3 row 5 read directly from the paper's Results (TEWL, Corneometer, VRS tables) and Methods (composition, funding).                                                                           |
| Lubart & Lipovsky 2022 (JCDSA)                                                                                                   | Full text (PDF, read via document tool)                                     | Every figure in §1 claim 3 and §3 row 6 read directly from the paper's Results §3.1-3.5, Table 3 and the Summary/Discussion section, including the funding statement.                                                       |
| Lubart et al. 2022 (JCAD)                                                                                                        | Extracted summary (PMC blocked by reCAPTCHA; read via a mirrored summary)   | Ex vivo penetration and particle-size figures in §3 row 7; flagged as not independently re-verified against the primary PDF.                                                                                                |
| Dondero et al. 2025                                                                                                              | Extracted summary (PMC blocked by reCAPTCHA; read via a mirrored summary)   | Lab-model design, MW (~2 kDa), and gene-expression figures in §3 row 8; flagged as lab-model-only, not living human skin.                                                                                                   |
| Matrixyl 3000 and copper-peptide claims (claims 6-7)                                                                             | `docs/claims/matrixyl-3000.md`, `docs/claims/copper-peptide-ghk-cu.md`      | Summarised, not re-derived; both registers' own conditions carry forward unchanged.                                                                                                                                         |

**No figure in §1-§5 of this register was contradicted by anything else read.** Everything above was checked at source except the two items flagged in
the log as "mirrored summary" (both non-blocking for the page's planned claims, since neither is used as a standalone number in §1).
