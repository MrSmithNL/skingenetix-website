# Page quality gate — Badenhorst 2016 study page

**Page:** `/pages/study/copper-peptide-wrinkle-trial-badenhorst-2016`
**Built:** 2026-09-24 · **Template:** `docs/study-page-template.md` (this page IS the template)
**Rule:** Rule 27, the five checks A–E. A page is not done until all five are answered in writing.

Because this page is the template for eleven more, a fault here is a fault eleven times. Findings
below are marked **[template]** where they belong to the structure rather than to this page.

---

## A — Design and visual

**Measured** with `~/.claude/skills/web-design-direction/measure.py` at 1440 and 390, and compared
with the signed-off science-page template (`/pages/acetyl-hexapeptide-8-research`) so that a
house-wide characteristic is not mistaken for a new defect.

| Band | Standard | Study 1440 | Study 390 | Hub 1440 (signed off) |
|---|---|---|---|---|
| displayToBody | 4.4–6.6 | **3.53** | **2.35** | 4.00 |
| body line-height | 1.40–1.60 | 1.60 | 1.60 | 1.60 |
| distinctSectionPaddings | ≥ 3 | **2** | **2** | **1** |
| measureCh | 50–70 | **85** | 40 | **85** |
| distinctRadii | ≤ 3 | 10 | 9 | 15 |
| tapTargets < 44px | 0 | 55 | 40 | 87 |
| page weight | — | 2,252 KB | 2,088 KB | 2,233 KB |

**What is ours and what is the house's:**

- **`measureCh` 85, `distinctRadii`, tap targets, page weight** are identical or better on this page
  than on the signed-off hub. They come from the Impact theme and the site-wide type scale. Flagging
  them here would be flagging the whole site; they belong to a separate sitewide pass, not to this
  page. **Open decision — sitewide, not page.**
- **`displayToBody` 3.53 is worse than the hub's 4.00**, and that part is ours: the body is 17px here
  against the hub's 15px, while the theme caps the H1 at 60px on both. Reaching 4.4 at a 60px H1 needs
  a ≤ 13.6px body, which would be worse to read on a long-form page. **Open decision [template]:**
  either the theme's display cap rises for this page type, or the band is accepted as not applying to
  a reading page. Not silently "fixed" by shrinking the body.
- **`distinctSectionPaddings` 2** — six bands at 64px desktop / 44px mobile. Out of band, and ours.
  The page is still better than the signed-off hub (1). **[template]**

**Corrected during the check:** the `.sty h2 {font-size: 32px}` rule in `study_sections.py` never
applied — the theme's own H2 rule wins, and the bands render at the theme's 48px/32px, which is the
scale the hubs use. The dead rules were removed rather than left in the source claiming otherwise.
(Memory: *CSS on the page is not CSS applying*.)

**Critique:** the `design-critic` agent ran on the deployed URL in a fresh context. See §A-critique.

---

## B — Content and voice

- Every figure was read from the **full PDF** on 2026-09-24 — Tables 2 and 3 and the Methods, not
  the abstract. The reference band says so on the page.
- The read uncovered a **live claim defect on the copper hub**: the comparator was described as "the
  same serum without GHK-Cu" in six settings and six languages. The paper's control carried neither
  the peptide nor the lipid nano-carrier. Fixed the same day
  (`configs/claim-fixes/copper-vehicle-2026-09-24.json`) and recorded in
  `docs/claims/copper-peptide-ghk-cu.md`.
- No invented numbers. Nulls and non-significant results are stated, not omitted: depth vs Matrixyl
  3000 at **p = 0.0577 (not significant)** is limitation 5.
- Marketing audit: **100/100** — no medicinal wording, no hedging, no unsupported claim, every result
  figure beside its source.
- The byline names Dr Esther Bodde as reviewer. Per `reviewer-credit-live-before-review`, that credit
  is live on Malcolm's say-so ahead of her review and is removable with one command.

---

## C — Search (SEO) and strategy fit

`scripts/page-audit.py`, 2026-09-24: **SEO 100/100**.

- One H1, and it does not open with the bare ingredient term — `build-study-page.py` refuses that,
  because it would cannibalise the hub.
- Title 50 chars, description 142. Self-canonical, hreflang for all six locales + x-default,
  indexable, in the sitemap, BreadcrumbList present.
- Sits below its hub: links up to `/pages/copper-peptide-research`, down to the serum. 17 unique
  internal links.
- **Open:** the page is English-only. Five locales serve English until the config carries
  translations. **[template]**

---

## D — Conversion

- One primary action — "Read the copper peptide evidence" — with a ghost second step to the serum,
  both at the foot, after the appraisal. This is deliberately not a sales page; the ask comes only
  once the reader has been given the caveats.
- Audit: path to purchase present, 2 products linked, proof beside the ask.
- **Open [template]:** no tracking events are named for this page type yet. Per
  `verify-tracking-in-a-live-browser`, "GA4 is set up" is not evidence — this needs a live-browser
  check before any study page is judged on conversion.

---

## E — AI visibility (GEO)

`scripts/page-audit.py`: **GEO 79/100** at first build. Five findings, all template-level:

| Sev | Finding | Action |
|---|---|---|
| high | No answer-first definition sentence | Added a 50-word answer paragraph under the byline **[template]** |
| med | `WebPage` had no `dateModified` | Added `datePublished` + `dateModified` **[template]** |
| med | The `Reference` H2 did not survive extraction | Citation moved into `sections_html` as band 7 **[template]** |
| med | `study_designed` + `study_reference` both white | Same fix — the theme section stops rendering **[template]** |
| low | Schema had no `citation[]` | Added, pointing at the DOI **[template]** |

Already passing: 647 words extract without JavaScript, 34 measured figures, 3 citation markers,
atomic paragraphs (0 over 120 words), 5 snippet-sized answer blocks, a real `<table>`, a visible
last-reviewed date, no links inside tables, all major AI crawlers allowed.

**Open:** only 647 of 1,011 words survive extraction — roughly a third of the page, most likely the
tables and the chart, is invisible to a text extractor. Worth measuring properly before deciding
whether it matters. **[template]**

---

## Status

Checks B, C, D and E are answered. Check A is answered on measurements and awaits the critique.
The GEO fixes are built and verified locally but **not yet deployed** — they were held so the
critic could judge the version it was given.
