# Page quality gate — Collagen Skincare

**Page:** `/pages/collagen-skincare` (today `/pages/collagen-skin-plumping`; the address moves only after Malcolm has seen the page)
**Decision:** `docs/decisions-log.md` ADR-2026-09-29-D · **Keyword data:** `configs/keyword-data/collagen-2026-09-29/`
**Rule:** Rule 27, checks A–E. The page is not done until all five are answered here.
**Status:** plan row written 2026-09-29, before the build. Checks A–E are filled in after the preview is built.

---

## Plan row

| Field                         | Value                                                                                                                                                                                             |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Question the page answers** | "Do collagen creams and serums work, and which one should I buy?"                                                                                                                                 |
| **Job in the funnel**         | Middle: a shopper comparing collagen creams and serums. The page answers honestly, then sells the two collagen creams and the two peptide serums.                                                 |
| **Primary keyword**           | `collagen cream` (US 656 a month observed, GB 472; difficulty 0–2)                                                                                                                                |
| **Secondary set**             | `collagen face cream`, `collagen cream for face`, `collagen serum`, `collagen skincare`; DE `kollagen creme`, `kollagen serum`, `kollagen gesichtscreme`; NL `collageen serum`, `collageen creme` |
| **Not this page's terms**     | `firming` (Firming page), `peptide cream` (Pro-Collagen cream), `pdrn cream` (PDRN night cream), `matrixyl 3000` (serum), `collagen peptides` / supplements (off-intent)                          |
| **Primary action**            | Shop the Matrixyl 3000 Pro-Collagen Firming Cream (the collagen cream); quiet second step: the proof cards and the ingredient science pages                                                       |
| **Sources**                   | Claims register `docs/claims/collagen-skincare.md` (new), `docs/claims/matrixyl-3000.md` §8, `docs/claims/copper-peptide-ghk-cu.md` §8.4                                                          |

## Blocks (standard sections first)

| #   | Section id | Type                                                | Holds                                                                                                                                                                                                   |
| --- | ---------- | --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | `hero`     | `image-with-text-overlay` (stock)                   | H1 inside the richtext, one-line promise, no number                                                                                                                                                     |
| 2   | `answer`   | `rich-text` (stock)                                 | _Do Collagen Creams Work?_ as H2, a short answer whose first sentence is bold and quotable on its own, the byline with a date                                                                           |
| 3   | `shop`     | `featured-collection` (stock, hand-picked products) | the two collagen creams and the two peptide serums, near the top                                                                                                                                        |
| 4   | `content`  | `media-with-text` (stock)                           | what collagen does in a cream · cream or serum · Matrixyl 3000 · copper peptide                                                                                                                         |
| 5   | `proof`    | `research-before-after` (ours, in git)              | two before/after cards: Matrixyl 3000 deep-wrinkle area, copper peptide firmer and denser-looking skin                                                                                                  |
| 6   | `routine`  | `multi-column` (stock)                              | a morning and evening routine with cream and serum                                                                                                                                                      |
| 7   | `faq`      | `faq` (stock)                                       | five or six real questions from the secondary set. The section also emits FAQPage schema; since Rule 27 check E was revised (2026-09-29) that is no longer required, and the FAQ is here for the reader |
| 8   | `related`  | `multi-column` (stock)                              | the four other Skin Solutions pages                                                                                                                                                                     |
| 9   | `schema`   | `custom-html`                                       | WebPage JSON-LD only (no stock section can carry it)                                                                                                                                                    |

**Dropped from the old page:** _Why Does Collagen Decline?_ (it duplicated the Firming page's intent and carried unsourced figures) and _Topical
Peptides vs. Other Approaches_ (its "collagen cannot penetrate" line contradicted the Firming page and the product we sell). The old FAQ answers
("superior results", "no downtime or risk", "highly effective alone") are replaced.

## Build and preview

- One spec owns the whole new template: `configs/hub-upgrades/collagen-skincare-2026-09-29.json`, `"create": true`, built from an empty template
  so every text is registered in six languages (a copied template carries no translations).
- Preview: `/pages/collagen-skin-plumping?view=collagen-skincare`. The canonical stays on the page address, so the preview is not indexed.
- Page-level fields (SEO title, meta description, handle) cannot be previewed; they are listed below and change only at go-live.

## A–E

_To be filled in after the preview is built and measured._
