# Page quality gate — Collagen Skincare

**Page:** `/pages/collagen-skincare` (today `/pages/collagen-skin-plumping`; the address moves only after Malcolm has seen the page)
**Decision:** `docs/decisions-log.md` ADR-2026-09-29-D · **Keyword data:** `configs/keyword-data/collagen-2026-09-29/`
**Rule:** Rule 27, checks A–E. The page is not done until all five are answered here.
**Status (2026-09-29, evening):** English draft built on the hidden preview and taken through three design-critic cycles and three
central audits; checks A–E answered below. **Not translated yet, by design** (Malcolm: "only translate when the english version is fully
completed and correct and optimized"). Waiting on Malcolm: his review of the English, the Matrixyl card f1 photo, and the open items at
the end of this note.

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

## Build and preview (as built)

- Spec `configs/hub-upgrades/collagen-skincare-2026-09-29.json`, `"english_first": true` (the `hub-upgrade.py` mode made for this page,
  `f4127e7`): every text is `{"en": ...}`; the tool refuses the flag on any template a page uses. Preview
  `https://www.skingenetix.com/pages/collagen-skin-plumping?view=collagen-skincare` (the canonical stays on the page, so it is not
  indexed). Commits `d89eec4`, `0c25800`.
- Final order: hero → answer → shop → content (4 rows) → routine → proof → FAQ (7) → related → schema (Article JSON-LD, zero-height host).
- Section Custom CSS: hero 471, content 272, routine 139, answer 38, related 21, FAQ 61 characters, one statement per entry (Shopify
  scopes only the first statement of an entry; `hub-upgrade.py` now refuses a multi-statement entry, `0c25800`).

## A–E

| #     | Check                   | Answer                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | Evidence                                                                                                                                   |
| ----- | ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| **A** | Design and visual       | **FIX 5.7 → FIX 6.1 → FIX 6.4 (cycle 3, the cap).** Every cycle-2 finding verified fixed in cycle 3; its one regression (the phone routine rule left a 60 px text column at 200% zoom) was fixed after the cap and measured at 195/320/390: text column 155/160/230 px, nothing past the viewport, breaks only at hyphens. The critic's remaining ideas are art direction, listed under "Open for Malcolm". Page-level findings fixed: a watermarked, off-brand routine photo; hero contrast at 390 (worst H1 line 3.24 → 4.23:1); no hierarchy (display-to-body 4.0 → 6.14 at 1440); four competing buttons → one primary action in two places; answer at reading width; six identical card rows → varied widths, routine as a break, text off the cards; 200% zoom (CTA was 91×234 px in nine pieces → 168×71); routine a hidden swipe row → thumbnail rows on phones; no accent → Matrixyl teal `#016569` (template §3.6). | Critic reports cycles 1–3 (session scratchpad; summarised here); renders on Malcolm's Desktop `skingenetix-renders.png`                    |
| **B** | Content and voice       | Written from `docs/claims/collagen-skincare.md` (claims 1, 4, 5–7, §7 answer, §8 "collagen serum"), Matrixyl register §8.4–8.6, copper register §8.4. No invented numbers: every figure carries its source link and qualifier (Bos and Meinardi 2000, CIR 2022, Aguirre-Cruz 2020, Lee 2021, Sederma, Badenhorst 2016, Pickart 2015, Mortazavi 2024, CIR 2018). CIR collagen safety (claim 2) **not used**: its condition is confirming the collagen's source species. Product claims stay at "contains X, which has its own evidence" (register §6 gap 3). Safety FAQ added; no outcome promises. **Draft until Malcolm approves.**                                                                                                                                                                                                                                                                                          | Audit round 3: content 8.92, trust 10.0, health 10.0; C2 facts, C5 sourced evidence, V1 safety, V4 no promises all met                     |
| **C** | Search and strategy fit | Primary `collagen cream`; secondary `collagen face cream`, `collagen cream for face`, `collagen serum`, `collagen skincare`. One H1 ("Collagen Cream & Serum"), H2 per section. Links up to `/pages/skin-concerns`, across to the four sibling concern pages, down to the four products, out to the Matrixyl and copper science pages and the Badenhorst study article. All images have descriptive alt text (the two shared routine photos were fixed on the file, backup `backups/file-alt-howto-steps-20260929-174313.json`). **At go-live (Malcolm's OK):** SEO title "Collagen Cream & Serum: What Works on Skin" (42), meta "Do collagen creams work? How collagen helps skin by molecule size, why we make no collagen serum, and the creams and peptide serums with clinical results." (154), handle `collagen-skincare` + 301s in six locales, Firming page drops "collagen" as a target, fifth Skin Solutions tile. | Audit round 3: query fit 8.33 (the only failure is Q2, the title, which is page-level and set at go-live), P4 anchors met, T6 alt text met |
| **D** | Conversion              | One primary action, "Shop the Pro-Collagen Cream", in the hero and beside the collagen evidence; the other product mentions are inline links. Objections answered: does it work, does it penetrate, collagen serum or cream, which one for my face, morning or night, how soon, is it safe every day. The four-product grid stays near the top (ADR-2026-09-29-D: "products up front"); the audit's agency-standard X1 would move it after the evidence — **Malcolm to choose**. Tracking: the store's standard GA4 ecommerce events cover product views and add-to-cart; no page-specific CTA event is named yet (open).                                                                                                                                                                                                                                                                                                     | Critic cycle 2: "FIXED — only two button CTAs, both to the Pro-Collagen cream"                                                             |
| **E** | AI answer eligibility   | Indexable at go-live, no snippet restriction, main content in the server HTML, OAI-SearchBot / PerplexityBot / Claude-SearchBot allowed. Answers its question first ("Yes, as a moisturizer: …") in self-contained, quotable sentences. Article JSON-LD with headline, author (Person), dates, publisher, the four products as `mentions`, five `citation`s; the stock FAQ also emits FAQPage (not a goal since check E was revised).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | Audit round 3: AI eligibility 10.0 (A1–A4), structured data 10.0 (S1 markup matches the page, S3 Article)                                  |

**Central audit (v2, `--criteria v2 --page-type article --keyword "collagen cream"`), on the preview:** round 1 uncapped 6.1 → round 2
9.19 → round 3 **9.27**. Each run is capped at 2.0 by the `canonical_self_or_absent` gate, because the preview's canonical points at the
old page; that gate and Q2 clear only at go-live, so the **go-live re-audit on `/pages/collagen-skincare` is the one that counts**. Cost
3 × ~USD 1.16, within the standing budget.

## Open for Malcolm

1. **Review the English page** (preview link above). Nothing is translated until he says it is complete.
2. **Matrixyl card f1 photo:** pick from `~/Desktop/skingenetix-before-after-collagen-plumping-r2.png` (rows A–C). The card shows a grey
   placeholder until then.
3. **Hero photo:** it is the Firming collection's banner (a woman holding the Pro-Collagen jar); on phones the promise line runs over the
   jar's label. Keep, or a new banner (an image wave costs money).
4. **Safety FAQ, allergy line:** "Both creams contain ingredients of animal origin: collagen in the Pro-Collagen Firming Cream, and
   salmon-derived PDRN in the PDRN Collagen Night Cream. If you are allergic to fish or other animal proteins, contact us before you use
   them." The collagen's source species is still undisclosed (claims register §6 gap 1).
5. **Products before or after the evidence** (check D above).
6. **Design, beyond this page (critic cycle 3, 6.4):** no visual signature, because the whole Skin Concern family has no direction
   contract; more iterations on this page will not lift that. Its three concrete ideas, all within stock sections: (a) the four content
   rows repeat the shop grid's four product photos in the same order; swap two of them for owned science images (e.g.
   `skingenetix-matrixyl-3000-peptide-signalling-fibroblast-collagen-synthesis.jpg` for the Matrixyl row) and set "Collagen Cream or
   Collagen Serum?" as a text band; (b) one section padding everywhere; tighten shop into content and give the proof a larger band;
   (c) three 4-up square grids at 1440 (shop, routine, related); the routine could be 2×2 thumbnail rows on desktop.
7. Carried: the four product-fact contradictions in the claims register §0 (elastin, vegan, source species, the PDRN cream listing the
   Matrixyl peptides); the copper photo with eucalyptus and a jade roller (his pick, "S2"), which the brand direction's "not one leaf"
   rule questions.
