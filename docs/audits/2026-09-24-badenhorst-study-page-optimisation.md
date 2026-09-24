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

| Band | Standard | First build 1440 | **Rebuilt 1440** | First build 390 | **Rebuilt 390** | Hub (signed off) |
|---|---|---|---|---|---|---|
| displayToBody | 4.4–6.6 | 3.53 | **4.32** | 2.35 | **3.06** | 4.00 |
| body line-height | 1.40–1.60 | 1.60 | 1.60 | 1.60 | 1.60 | 1.60 |
| distinctSectionPaddings | ≥ 3 | 2 | **7** | 2 | **6** | 1 |
| measureCh (real content) | 50–70 | — | **61** | — | 40 | 54 |
| distinctRadii | ≤ 3 | 10 | 9 | 9 | 8 | 15 |
| tapTargets < 44px | 0 | 55 | 54 | 40 | 40 | 87 |

**What is ours and what is the house's:**

- **`distinctRadii`, tap targets and page weight** are the Impact theme's, and are the same or better
  here than on the signed-off hub. They belong to a sitewide pass, not to this page.
- **`displayToBody`** was the one genuinely ours. Fixing it properly meant raising the H1 rather than
  shrinking the body — the limits list is *meant* to be the largest body text on the page. The theme
  caps the H1 at 60px, so the page sets `clamp(52px, 6vw, 88px)` with `!important`.
- **`measureCh`: the 85 reported in the first build was not real.** See the correction below.

**Corrected during the check:** `.sty h2 {font-size: 32px}` never applied — the theme's own H2 rule
won, silently. Nor did a plain `main h1 {font-size: …}`. Both now use selectors specific enough to
win, verified against computed style on the live page. (Memory: *CSS on the page is not CSS applying*.)

**Reverted during the check:** making the bands full-bleed (`overflow-x: clip` + `margin-inline:
calc(50% - 50vw)`) shipped a **blank page** to the live site. The theme gives `.sty` no width, so it
shrink-to-fits; with every child pulled out by −50vw its width computed to 0 and the clip context cut
the body away. Computed styles read correctly — only the screenshot showed it. Reverted within
minutes and documented in the template's trap table.

**Critique:** the `design-critic` agent ran on the deployed URL in a fresh context and returned
**REBUILD (scoped)** at **5.48** (Design 4.6 · Usability 5.8 · Creativity 5.0 · Content 9.0), with the
instruction *"do not generate the other eleven configs against this CSS"*. Its blockers were verified
against the live DOM before acting, and all are fixed. See §A-critique.

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

## A-critique — what the critic found, and what was done

Every blocker was verified against the live DOM before acting, because a report is not evidence.

| Sev | Finding | Verified | Action |
|---|---|---|---|
| Blocker | **The primary CTA rendered as struck-through blue text, not a button.** The theme paints an animated underline on every `a` with `background-image` + `background-size`, which collapsed the fill to a 1px strip; the label stayed blue on transparent. | `background-size: 100% 1px`, `background-repeat: no-repeat`, `color: rgb(1,78,177)` on a 298×47 box | Every longhand overridden with `!important`. Now a solid blue pill, white label. |
| Blocker | The answer paragraph — the sentence an engine quotes — was the **smallest text on the page** (15px under a 60px H1). | confirmed, 15px | 20px desktop / 17px mobile; the byline stays quiet at 14px. |
| Blocker | **Three unrelated left edges**: H1 330, band 180, content 204. | confirmed | `study_head` widened to `large`; the H1 constrained and centred; the citation moved into the band system. |
| High | One padding value on every band. | `distinctSectionPaddings` 2 | Padding now carries rank: **7 distinct values** (56/72/72/88/104/80/40). |
| High | Two heading sizes, and the **H1 was lighter (w300) than the six H2s (w600)** under it. | confirmed | Four sizes (26/36/40/54), all weight 300, H1 raised to `clamp(52px, 6vw, 88px)`. |
| High | **Band 5 read as a footnote** — narrowest, least-padded, most boxed thing on the page. | 1032px inside 1080px bands, 32px padding against 64px | **On ink**, 104px padding, 54px heading, 20px list — the largest body text on the page. |
| High | No first screen at 390; the first figure sat at y=822. | confirmed | Short H1 at 52px + the answer paragraph now fill it. |
| High | H1 orphan — "al.)" alone on the last line, on **every** study page by convention. | confirmed | H1 shortened to the question; `text-wrap: balance`. |
| High | Chart comparator grey at **2.58:1** fails non-text contrast. | confirmed | **Open — sitewide.** It is `scripts/hub_charts.py`, shared with the signed-off hubs. Not changed unilaterally. |
| Med | 320px horizontal overflow, 11px. | confirmed, and ours — hubs and home are 0 | **Open.** The fix attempted (viewport breakout) shipped a blank page and was reverted. |
| Med | One image, full-size, no `srcset`. | 321 KB for a 302px slot | `srcset` at 400/600/800/1200 with `sizes`. |
| Med | White chart card on a white band. | confirmed | Card ground tinted to #FAFAFA. |
| Med | Prose measure too wide. | **artefact — see below** | Caption and reference capped anyway; real measure now 61ch. |
| Nit | Glance table numerals not tabular. | confirmed | `tabular-nums`. |

**Correction — the measure finding was not real.** Both the critic and my own first note reported
`measureCh` 85–87 as a sitewide fault. `measure.py` takes the first paragraph over 200 characters
*in document order*, which on every page of this store is the Shopify cookie-consent dialog. That is
why the page and its hub reported the same number. Measured on real content, the rebuilt page runs
**median 71ch, max 74ch before the caps and 61ch after**; the hub runs 54–94ch. The skill was patched
to prefer `main`.

## Status — all five checks answered

| Check | Verdict |
|---|---|
| A Design | Rebuilt against the critique. `displayToBody` **3.53 → 4.32** (1440) and **2.35 → 3.06** (390); `distinctSectionPaddings` **2 → 7**; `measureCh` **61**, in band. Two open items: the shared chart grey, and 11px of overflow at 320px. A second critique should run on the rebuilt page before the remaining eleven are generated. |
| B Content | Pass. Every figure read at source; the hub claim defect it uncovered is fixed in six languages. |
| C Search | **SEO 100/100.** Open: the page is English-only. |
| D Conversion | Pass — and the CTA now actually renders as a button. Open: tracking events unnamed. |
| E AI visibility | **GEO 79 → 100/100.** |

Final audit, 2026-09-24: **SEO 100 · GEO 100 · DESIGN 100 · MARKETING 100 — zero findings.**
