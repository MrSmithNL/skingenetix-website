# Keyword ownership — which page should rank for which term

**Date:** 2026-09-30 · **For:** Malcolm's decision on question 4 ("which page is best for ranking as the key page per
keyword … maybe a second alternative similar keyword"), and the record of question 3 ("the keyword research and
keyword strategy should decide" the study articles' keywords).
**Data:** `configs/keyword-data/targeted-2026-09-30/targeted.json` (pulled by `scripts/keyword-research-targeted.py`),
the 2026-09-22 strategy data (`configs/keyword-data/strategy/`), live Google results for 20 terms (desktop, and mobile
where the two could differ). **DataForSEO cost: $1.26.**
**Volumes** are _observed_ monthly searches (clickstream), the strategy's traffic signal — not Google Ads buckets, which
inflate these terms up to 500× ("peptide skincare": Ads 49,500, observed 100).

---

## The short answer

| Clash                                                          | Recommendation                                                                                                                                                                        | Why, in one line                                                                                                                                                |
| -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Argireline** — product and hub both claim "argireline"       | **Hub keeps "argireline"; the product takes "argireline serum"**, with "acetyl hexapeptide-8 serum" as its second term                                                                | On phones Google shows explainers for "argireline" (study, The Ordinary, Vogue, Byrdie); the strategy already said this and `page-targets.json` drifted from it |
| **Matrixyl 3000** — product and hub both claim "matrixyl 3000" | **Product keeps "matrixyl 3000"** (+ "matrixyl", "matrixyl 3000 serum"); **the hub takes the science**: "what does matrixyl do", "palmitoyl tripeptide-1", "palmitoyl tetrapeptide-7" | Google ranks a _product page_ first for "matrixyl 3000" on desktop and mobile, and "matrixyl" alone is pure shopping                                            |
| **Peptide skincare** — homepage and The Science both claim it  | **A collection owns it**; the homepage owns the brand name; The Science owns "peptides in skincare" explainers                                                                        | Tiny real demand (≈ 250/month); Google shows shop categories (Space NK, Image Skincare)                                                                         |
| **Study articles** (question 3)                                | Each owns its **own trial's question**; the **hub** owns "does argireline work" (656/month) and "does copper peptide serum work"                                                      | Nobody searches the trial questions measurably; the one real efficacy query is answered best by the page that weighs _all_ the trials                           |

Two opportunities the data turned up, not in any plan yet:

- **"matrixyl and argireline" — 858 searches/month (US), and page one is only forum threads.** Nobody authoritative
  answers it. A spoke article ("Argireline and Matrixyl 3000 together: what the trials show") grounded in our two
  products and their trials is the clearest content win in this dataset.
- **"does argireline work" — 656/month (US), page one is a spa forum, a Dr Oz thread and a supplement review.** The
  Argireline hub should answer it in a section with that heading.

---

## 1. Argireline

**Pages in the cluster:** hub `/pages/acetyl-hexapeptide-8-research` · product `/products/acetyl-hexapeptide-8-anti-wrinkle-serum`
· collection `/collections/acetyl-hexapeptide-8` · study articles Wang 2013, Raikou 2017.

| Term                       | US    | GB      | What Google shows (2026-09-30)                                                                                                                                                            | Owner                                     |
| -------------------------- | ----- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------- |
| argireline                 | 3,734 | 1,103   | **Mobile:** PMC study, The Ordinary, Vogue, Reddit, Lubrizol, Byrdie, INCIDecoder, plus a shopping carousel. **Desktop:** eight Amazon listings. GB: The Ordinary's product, Amazon, eBay | **Hub**                                   |
| acetyl hexapeptide-8       | 1,009 | 236     | Ingredient explainers: Dr. Jart's ingredient page, Paula's Choice ingredient dictionary                                                                                                   | **Hub** (its own address already says it) |
| does argireline work       | 656   | —       | A spa forum, a Dr Oz thread, a supplement review — no brand page                                                                                                                          | **Hub**, as a section                     |
| argireline serum           | 605   | Ads 880 | Forum threads; no strong page                                                                                                                                                             | **Product**                               |
| argireline peptide         | 403   | 78      | (not pulled)                                                                                                                                                                              | Product (second term)                     |
| acetyl hexapeptide-8 serum | —     | 78      | we rank #38 (US, the collection)                                                                                                                                                          | Product (second term)                     |
| matrixyl and argireline    | 858   | 78      | Forum threads only                                                                                                                                                                        | **New spoke article**                     |
| argireline eye cream       | —     | 157     | (not pulled)                                                                                                                                                                              | No product matches — a range question     |

**Reading.** "Argireline" is a mixed query: people want to know _and_ to buy. On a phone — where most skincare searching
happens — Google ranks explainers, which is what the hub is. The product still reaches desktop shoppers through the
shopping carousel (Merchant Center), not through organic ranking. The 2026-09-22 strategy reached the same split; only
`configs/page-targets.json` drifted (it gave the product "argireline").

**Alternative keyword for the product (your question):** "argireline serum" as primary, with "argireline peptide serum"
and "acetyl hexapeptide-8 serum" as the second terms. Together ≈ 1,000/month of buying intent the hub never competes for.

**One more overlap to settle:** the single-product collection `/collections/acetyl-hexapeptide-8` is what currently
ranks (#38 US, #66 GB) for "acetyl hexapeptide-8 (serum)", competing with the product. Recommendation: the collection
keeps a browse title ("Argireline® skincare") and no head term, so Google's signal consolidates on the product.

## 2. Matrixyl 3000

**Pages:** hub `/pages/matrixyl-3000-research` · products `/products/matrixyl-3000-firming-serum` and
`/products/matrixyl-3000-pro-collagen-firming-cream`.

| Term                                              | US        | GB      | What Google shows                                                                                                                                                                | Owner                                                                 |
| ------------------------------------------------- | --------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| matrixyl                                          | 3,734     | 866     | **Shopping on both devices**: eBay, Walmart, Amazon, The Ordinary's product                                                                                                      | **Serum product**                                                     |
| matrixyl 3000                                     | 2,725     | 1,339   | **#1 a product page (Timeless "Matrixyl 3000 Serum") on desktop and mobile**; #2 No7's ingredient shop page; then The Ordinary glossary, INKEY blog, INCIDecoder, Women's Health | **Serum product**                                                     |
| matrixyl 3000 serum · matrixyl serum              | 100 · 151 | 236 · — | Product pages: The Ordinary, Timeless, Depology                                                                                                                                  | Serum product (second terms)                                          |
| what does matrixyl do                             | 252       | —       | (not pulled)                                                                                                                                                                     | **Hub**                                                               |
| palmitoyl tetrapeptide-7 · palmitoyl tripeptide-1 | 504 · 353 | 78 · 78 | ingredient-name searches                                                                                                                                                         | **Hub** (the INCI names, as "acetyl hexapeptide-8" is for Argireline) |

**Reading.** The opposite of Argireline. For "matrixyl 3000" Google puts a _product named for the ingredient_ first on
both devices, and bare "matrixyl" is pure shopping. Our serum is literally called Matrixyl 3000 Firming Serum. The
product is the page best placed to rank; the hub owns the science questions and the ingredient names.

**The alternative I considered and do not recommend:** hub owns "matrixyl 3000", product owns "matrixyl 3000 serum". It
would mirror Argireline, but "matrixyl 3000 serum" is only 100 + 236 searches, against 2,725 + 1,339 for the head term
where a product page already wins. The decision should follow each SERP, not symmetry.

## 3. Peptide skincare

| Term             | US  | GB  | What Google shows                                                                                                                                     | Owner            |
| ---------------- | --- | --- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------- |
| peptide skincare | 100 | 157 | US: low-quality pages; **GB: shop categories** (Space NK, Image Skincare "peptides" collection, M&S, Lookfantastic) and guides (Boots, Vogue, Medik8) | **A collection** |

`page-targets.json` gives it to both the homepage and The Science; the strategy gave it to a collection. Recommendation:
**a collection** (all products, or a "Peptide skincare" collection) owns it; the **homepage** owns the brand name;
**The Science** owns the explainer family ("peptides in skincare", "what are peptides"). Low stakes either way: ≈ 250
real searches a month.

## 4. The study articles (question 3 — decided by the research)

Measured demand for each trial's own question is close to zero. That is a finding, not a gap: the 2026-09-22 pull never
covered these phrases, so this pull searched for them directly (every keyword containing the ingredient _and_ the study's
words, US and GB).

| Article         | Its question                                 | What people search (observed/month)                                         | Primary keyword                   | Role                                         |
| --------------- | -------------------------------------------- | --------------------------------------------------------------------------- | --------------------------------- | -------------------------------------------- |
| Wang 2013       | Does Argireline soften crow's feet?          | "argireline crow's feet": none measurable; "does argireline work" 656 → hub | **argireline crow's feet**        | Evidence page for the hub                    |
| Raikou 2017     | Does 10% Argireline smooth forehead lines?   | "forehead lines" searches are "best cream" shopping (≈ 130) → concern page  | **argireline forehead lines**     | Evidence page for the hub                    |
| Badenhorst 2016 | Does a copper peptide serum reduce wrinkles? | "does copper peptide serum work" 50 → hub                                   | **copper peptide serum wrinkles** | Evidence page for the copper hub             |
| Ye 2026         | Can PDRN beat retinol on crow's feet?        | "pdrn vs retinol": none measurable yet; "pdrn vs collagen" 151              | **pdrn vs retinol**               | Evidence + comparison spoke for the PDRN hub |

**The rule this sets (now in the keyword and content strategies):** _"Does X work?" belongs to the ingredient hub — the
only page that weighs every trial. Each study article owns its own trial's question, links up to the hub with the head
term, and is judged as an evidence page, not a traffic page._

**Applied now:** Badenhorst's SEO title asked the hub's question ("Does a Copper Peptide Serum Work?") while its H1 asks
the trial's. It becomes **"Badenhorst 2016: Can a Copper Peptide Serum Reduce Wrinkles?"** (60 characters).

## 5. What changes, and where

| File                                               | Change                                                                                                                           | Status                             |
| -------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------- |
| `docs/keyword-strategy-2026.md` §4                 | New "Clinical-study articles" table; the efficacy rule; the dated SERP evidence                                                  | Done with this analysis            |
| `docs/content-hub-strategy-2026.md` §4.3           | Study articles named as the spoke layer's evidence pages, linked to the keyword table                                            | Done                               |
| `configs/page-targets.json`                        | Study articles added (primary + hub)                                                                                             | Done                               |
| `configs/page-targets.json`                        | Argireline product → "argireline serum"; Matrixyl hub → "what does matrixyl do"; homepage and The Science off "peptide skincare" | **Waits for your decision**        |
| Page titles/H1s that follow from the decision      | e.g. the Argireline product title leads with "Argireline Serum"; the Matrixyl hub title leads with the question                  | After your decision, six languages |
| New spoke: "Argireline and Matrixyl 3000 together" | 858/month, forum-only page one                                                                                                   | Proposal                           |
| Argireline hub: a "Does Argireline work?" section  | 656/month                                                                                                                        | Proposal                           |

## 6. Honest limits

- **One day of SERPs, two devices.** Google's results moved between 2026-09-22 and today for "argireline" (the desktop
  view became all Amazon). The recommendation leans on the mobile view and on the matching 2026-09-22 snapshot; re-check
  in 30 days.
- **Clickstream is a panel estimate** and reads zero for rare phrasings; "none measurable" means below the panel's floor,
  not no one.
- **US and GB only.** They are 77 % of the opportunity (strategy §3); DE/FR follow the same page types.
- **The site ranks for almost nothing yet** (14 keywords, all below #38), so there are no positions to protect — and no
  proof yet of which page Google would prefer for _us_. Measure 14 days after any change (strategy §7 gate).
