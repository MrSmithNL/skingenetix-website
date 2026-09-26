# Decisions Log — Skingenetix (CLIENT-003)

Technical decisions recorded in ADR (Architecture Decision Record) format.

---

## ADR-001: Theme Selection — Impact or Prestige (REVISED)

**Date:** 2026-03-05
**Status:** REVISED — was "free theme (Sense/Refresh)", now recommending premium
**Context:** Hairgenetix uses a premium theme (Release - Satyam). Skingenetix needs its own visual identity while remaining manageable by Claude Code. After competitor analysis of QU:RE Skincare (qureskincare.com), a free theme would look noticeably less premium than the primary competitor.
**Decision:** Use **Impact** ($380) or **Prestige** ($400) premium Shopify theme.
**Rationale:**

- QU:RE Skincare uses a custom dark premium theme — we need to match that visual standard
- **Impact** (by Maestrooo): dark mode, bold imagery, DTC-focused, conversion tools (sticky cart, quick buy, cross-sell, promo banners), editorial sections
- **Prestige** (by Maestrooo): luxury feel, before/after slider, shop-the-look, premium positioning
- Both are standard Shopify 2.0 architecture (Claude-friendly, no custom Liquid needed)
- $380-400 one-time cost is small vs looking like a premium brand from day one
- Impact's "Sound" style specifically designed for wellness/skincare/luxury
  **Consequences:** One-time $380-400 cost. Both themes are well-documented and widely used, so Claude can manage them via JSON settings + custom CSS. Malcolm needs to purchase and install from Shopify Theme Store.
  **Competitor reference:** See `research/competitor-analysis-qure.md`

---

## ADR-002: Use Langify for Translations (Same as Hairgenetix)

**Date:** 2026-03-05
**Status:** ⚠️ **NOT IMPLEMENTED — superseded by ADR-002a (2026-08-27)**
**Context:** Multiple translation options exist — Shopify native Translate & Adapt (free), Langify ($17.50/mo), Transcy, LangShop.
**Decision:** Use Langify for consistency with Hairgenetix.
**Rationale:**

- Owner already knows the system
- Built-in image and video translation (unique to Langify)
- Can translate third-party app content
- Manual quality control for sensitive skincare claims
- Running two different translation systems across brands adds complexity
  **Consequences:** $17.50/month cost. Text translations can be registered via Shopify's native translation API and Langify will pick them up (they're compatible). Image/video translations require manual work in Langify UI.

---

## ADR-002a: Translate & Adapt is the translation system (correcting ADR-002)

**Date:** 2026-08-27
**Status:** Accepted — describes the live store
**Context:** ADR-002 proposed Langify in March and was never implemented, but the rest of the
documentation was written as though it had been. `CLAUDE.md`, `AGENTS.md`, `README.md`,
`docs/architecture.md` and `.claude/rules/shopify.md` all instructed future sessions to use Langify and to
**never** enable Translate & Adapt. That is backwards, and it was found only because a translation
requirement forced the question.

**Evidence (2026-08-27, `appInstallations`):** the installed apps include **Translate & Adapt**
(`translate-and-adapt`). There is **no Langify**. Only the `en` locale is published, so no translation
work has been done under either system and nothing is lost by the correction.

**Decision:** **Translate & Adapt** (Shopify native, free) is the translation system for this store.
Do not install Langify alongside it — the one-system rule stands, only the name changes.

**Rationale:** it is what is installed; it is free where Langify is $17.50/mo; and — the deciding
practical point — theme and template text is exposed natively as `ONLINE_STORE_THEME_JSON_TEMPLATE`
translatable resources, so section settings become translatable with **no app configuration at all**.
That property is what made the labelled before/after section possible without custom translation
plumbing.

**Consequences:**

- Any **text setting** added to a section in a page template is automatically translatable. Prefer that
  over baked-in image text, hardcoded strings or `custom-html` blocks whenever the words must translate.
- Langify's image/video translation is not available. Nothing currently depends on it.
- ⚠️ Translation keys carry a `:hash` of the value — **editing English text invalidates that key's
  translation**, and moving a block to a new section id orphans its keys entirely. Settle wording before
  translating. Full detail: `docs/research-before-after-section.md` §3.
- Older handovers still assert the Langify rule; treat this ADR as the authority.

---

## ADR-003: Hybrid Claude/Human Management Model

**Date:** 2026-03-05
**Status:** Accepted
**Context:** Need to balance Claude Code automation with human operability for key functions.
**Decision:** 80/20 split — Claude handles product/content/translation/SEO via API; humans handle one-time setup, media translations, visual approval, and strategic decisions.
**Rationale:** See full research report at `research/skingenetix-shopify-research.md`
**Consequences:** Requires custom app API token setup. Most app configurations (Langify, Klaviyo, Kaching) still need their admin UIs for initial setup and media management.

---

## ADR-004: Email Hosting on GoDaddy (Separate from Shopify)

**Date:** 2026-03-05
**Status:** Proposed
**Context:** Shopify does not provide email hosting. Need email for the Skingenetix domain. Malcolm has an existing GoDaddy hosting account that supports multiple domains.
**Decision:** Use GoDaddy hosting for email, with MX records configured at OpenDomainRegistry.
**Rationale:**

- No additional cost (existing hosting account)
- Already set up and familiar
- Keeps email independent from Shopify
- Domain registrar (OpenDomainRegistry) just needs MX records pointed to GoDaddy
  **Consequences:** Email management happens in GoDaddy control panel, not Shopify.

---

## ADR-005: Dedicated Templates for Collection Banners

**Date:** 2026-08-24
**Status:** Accepted
**Context:** The shop landing page needed a branded header banner. All thirteen collections shared `templates/collection.json`, so tuning the banner
there would have changed `/collections/serums`, `/collections/pdrn` and ten others. The `collection-banner` section also had settings that actively
damaged a designed product line-up: parallax renders the image at 130% and only ever reveals 77% of its height (it cut the bottle bases off), and a
50% overlay greyed the products out.
**Decision:** Copy the shared template to `templates/collection.<handle>.json`, edit only its banner, and point the collection at it with
`templateSuffix`. Publish with `scripts/publish-collection-banner-template.py <handle>` (has `--dry-run` and `--restore`). Applied to `all` on
2026-08-24 and generalised to `pdrn` the same day; each page carries its own overlay, text placement and measured text width.
**Rationale:**

- The banner box is a **fixed pixel height** (375/400/440) across a full-bleed width, so its aspect ratio runs from ~1.0 on a phone to ~5.8 on a 2560 monitor. No single crop survives that, which is why the section ships with a separate mobile image slot.
- Every other collection keeps the shared template untouched.
  **Consequences:** Gotchas worth remembering, each of which cost a round to find:
- Section ids in a JSON template render as `shopify-section-template--<theme id>__<key>`, so an id selector built from the section key silently matches nothing. Target the section's class instead.
- Shopify rejects the `html` setting with a 422 if it contains `{{` or `}}` — which minified CSS produces the moment a rule closes inside a media query (`;}}`). Keep the braces apart.

**Amendment 1, 2026-08-24 — the 700–1099px band was misreading product names.**
Squeezing a 3:1 banner into that width shrank the jar labels to ~3px per character, and at that size **`PDRN` resolved as `PORN`** on both banners — the exact failure `.claude/rules/website-imagery.md` rule 3 was written about, reproduced live. Two findings worth keeping:

- **Serving a bigger source does not fix it.** The limit is the _display_ size, not the delivery: a forced 1600w source rendered the identical misread at 768px. Only enlarging the subject on screen works.
- **Shopify will not upscale, and fails silently when asked to.** Requesting `width=1600&height=988&crop=right` against an 848px-tall master returned `1600x533` — the _full frame resized, crop ignored_. Size a crop request from the master's own height, never from the viewport.

**Amendment 2, 2026-08-24 — `image_size: "auto"` was the wrong lever; widen the master instead.**
`auto` avoided cropping but made both headers **taller than every other collection page**, which is a visible inconsistency and was rejected on review. The banner now keeps the theme's standard `sm` height (375/400/440) everywhere, and the fit is solved in the image rather than the box:

- **Widen the master to 3000px** (the long-edge cap in `upload-theme-images.py`). At a _fixed_ box height, `object-fit: cover` scales purely by height, so surplus width is not wasted — it is croppable margin, and the subject renders at exactly `box_height / master_height` regardless of viewport.
- **Aim that margin with `object-position: right center`.** The theme centres it, which would eat the model and the extension equally; anchoring to the subject side means horizontal cropping only ever removes extended backdrop.
- This also **retired the tablet crop from Amendment 1**: at the standard height the 700–1099px band crops horizontally instead of squeezing, so the products fill more of the frame and every label reads without special-casing.
- Vertical crop at very wide viewports is the residual trade-off: 5% at 1920 on the 4.14:1 master, versus 31% before it was widened.

**Amendment 3, 2026-08-27 — the right-pin applies to page heroes too, and it needs a partner fix in the tablet band.**
`/pages/acetyl-hexapeptide-8-research` shipped its 3000×688 (4.36:1) hero without the pin, so the theme's default `object-position: center` split the
crop evenly and cut the droplet in half on a laptop. Measured on the live page: 0px cropped at 1920 (the design case), 407px at 1512, 479px at 1440,
465px at 1280 — with half of each falling on the right edge, where the subject sits (bright content runs x=1826..3000 of the master). Pinning right
moved every crop onto the deliberately empty left extension. Verified by DOM computed style at seven viewports and a full-page pixel diff; the
banner's right-edge luminance now reads 106.7 at 1280/1440/1512, identical to the uncropped 1920 case.

Two things this page added to the recipe:

- **`object-fit: contain` is not the alternative, even when the ask sounds like "show all of it".** The box is a _height_, not an aspect ratio, so
  contain letterboxes: 110px of dead band at 1440, and at 768 a 176px-tall image floating in a 400px box. It only works if the master's top and bottom
  edges are flat, and this one's are not — sd 31 and 23, peaks 138 and 147, because the slide and caustic run to the edge. Cover plus a right pin is
  the only fit that keeps the subject at full scale.
- **Pinning right can push the subject under the type in the 700–1199px band, and it did.** At those widths the 400px box zooms the master ~1.7×, so
  the caustic moved in behind the copy: peak luminance under the text went from 54 to 183 at 1024. The text runs to 81% of the frame there (96% at
  768), leaving no column to scrim without dimming the droplet. Fixed the way `/pages/the-science` does it — cap the text column (`max-width:
min(58vw, 620px)`) and put a left-to-right scrim on `.content-over-media::before` — which brought the peak back to 138 at 768/1024 and 42 at 1152
  without crushing the mean (25–34). Desktop is untouched: at 1280+ the column stays 780px and there is no scrim.

Delivered as a `liquid` block inside the section (`configs/banners/page-acetyl-research-pin-right.json`, pushed with `scripts/patch-template.py`), so
`{{ section.id }}` resolves at render time. A `custom-html` section would 422 on the Liquid, and a hardcoded template id goes stale silently —
`/pages/brightening-glow` still carries one that matches nothing.

## ADR-006: A `custom-html` Style Section Is Never Placed Mid-Order

**Date:** 2026-08-27
**Status:** Accepted
**Context:** On `/pages/the-science`, "Our Evidence Standard" sat flush against the bottom of the hero banner with no gap, while the equivalent
section on every other page had a normal 80px above it. The section's own settings were not the fault: `research_standard` computed `padding-top: 0px`
against a normal `padding-bottom: 80px`, and its siblings — `/pages/acetyl-hexapeptide-8-research` `overview`, `/pages/skin-repair-renewal` `content`,
and the same page's `ingredients_overview` — all read 80/80.

The cause was a `custom-html` section named `hero_banner_css` holding the hero's injected `<style>`, sitting in the section order **between** the hero and `research_standard`. The theme's `section-spacing-collapsing` snippet emits

```
#shopify-section-<id> + * { --previous-section-background-hash: <hash> }
```

so whatever section physically precedes another becomes its "previous section" for the collapse test. A `custom-html` section has no background, so
its hash is `0`; `research_standard` has no background either, so its hash is `0`; the two matched and the theme collapsed the top padding — behaving
exactly as designed, on a section the designer never intended to be there. On every other page nothing sits in that gap, so
`--previous-section-background-hash` is never set, the test fails, and the padding survives. Note the hero itself never emits the rule:
`image-with-text-overlay` renders the snippet only `{%- unless section.settings.full_width -%}`, and these heroes are all full width.

**Decision:** Injected CSS goes in a **`liquid` block inside the section it styles**. Where a standalone `custom-html` section is genuinely needed, it
is appended at the **end of the section order**, never inserted mid-page. `hero_banner_css` was deleted and its CSS moved into a `hero_css` block
(`configs/banners/page-science-hero-css-into-block.json`).

**Rationale:**

- A zero-height section is not a zero-effect section. It is still a sibling, and the theme's spacing model is built on sibling adjacency.
- The block form also fixes scoping. The old CSS was scoped by **class** (`.shopify-section--image-with-text-overlay`), and this page carries two
  sections of that type, so the hero's rules were also landing on the `transparency` band — which was only keeping its own look because its
  `transparency_css` block scores (1,1,1) on ID against the class rule's (0,2,1).

**Consequences:**

- **Audited all 32 JSON templates for the same pattern.** `/pages/the-science` was the only instance. Every other injected style section
  (`banner_text_width` on ten collection templates, `concern_tile_scrim` on the homepage, `hero_image_position`, `faq_image_layout`,
  `banner_crop_anchor`, `intro_image_position`, `concern_overlay_css`) is **last in its section order** or followed only by another `custom-html`, so
  none of them collapses anything visible. `page.research-copper-peptide.json` has `hero_banner_css` mid-order but the section after it carries a
  background, so its hash differs and it never collapsed.
- **A `liquid` block brings its own 8px cost, which must be paid back.** The theme renders the block as `<div {{ block.shopify_attributes }}>…</div>`
  inside `.prose`, and that empty div takes a gap in the text stack — enough to push a vertically-centred hero heading up by 8px (301 → 293 on
  the-science; 334 → 326 on the acetyl page). Add `#shopify-section-{{ section.id }} .prose > div:has(> style) { display: none; }` to the block's own
  CSS. The `<style>` inside still applies: `display` does not affect the CSSOM.
- Verified by full-page pixel diff at 390 and 1440. Above the gap the only changed rows are the rotating announcement bar; below it, once shifted by the 80px (40px on mobile) that was added, the page is identical to the pixel.

---

## ADR-2026-09-22-R: Medical reviewer credited before her review

**Date:** 2026-09-22
**Status:** Accepted (Malcolm), pending Dr Bodde's confirmation
**Context:** The science pages had no named expert reviewer, and both external AI auditors (ChatGPT, Gemini) marked the Matrixyl hub down only on author and expert review (7–8/10). The standing rule was to add Dr Esther Bodde's byline only after she had read the pages.
**Decision:** Malcolm: "Lets already add Esther Bodde as verified. I will check with her." The credit went live on 2026-09-22 on the four rebuilt hubs
and both study pages, in six languages, in two places: the visible byline and `reviewedBy` in the JSON-LD. The glutathione hub is excluded until it
has been rebuilt against its claims register.
**Wording:** "Medically reviewed by Dr Esther Bodde, Cosmetic & Medical Physician". This is Malcolm's decided credential. Hairgenetix's "Cosmetic &
Plastic Surgeon" is flagged as possibly inaccurate and is not used. The credential stays in English in every locale, because a translation can read as
a protected professional title.
**Consequences:** The pages state a review that has not happened yet. If she declines or asks for changes, run `python3 scripts/set-reviewer.py
configs/reviewers/esther-bodde.json --remove --apply`. It removes the credit everywhere in one step and keeps the author line and our own
`lastReviewed` date.

---

## ADR-2026-09-23-G: Published citation titles are quoted verbatim, and the audit knows the difference

**Date:** 2026-09-23
**Status:** Accepted
**Context:** The glutathione hub cited five papers and had rewritten four of their titles, replacing "skin-whitening" with "even-tone" or "more even
complexion". A citation title is a bibliographic fact: changing it misrepresents the source and breaks the title match AI crawlers use to connect the
page to the paper (docs/claims/glutathione.md, fact 4). Restoring the published titles put "whitening" and "melasma" back on the page, and
`scripts/page-audit.py`'s EU-wording scan flagged them as our claims, dropping MARKETING from 93 to 71.
**Decision:** Titles are always quoted as published. The audit exempts only the References list's title element (`.sgref__ti`) from the
medicinal-wording scan; a quoted title in prose still counts, and so does every other word on the page. The chart caption that had quoted the paper's
"skin whitening" label was reworded rather than exempted.
**Also decided the same day:**

- `set-reviewer.py` takes a per-hub `reviewed` date (`hub_cfg`). Schema.org `lastReviewed` is the date the page's content was last checked, so a hub
  rebuilt on a later day carries its own date; one config-wide date had left the glutathione byline (23 September) and its JSON-LD (22 September)
  disagreeing.
- The audit's alternation check exempts a findings run of `research-before-after` and `media-with-text` in either order. Neither section has a background setting, so a run of them always sits on the page's Bone; the rule already exempted one order.
- The stock `impact-text` big figures render as `<h2>` and cost the glutathione hub a 6/10 on Gemini's heading-hierarchy criterion (7.5 average, the
  page's only failing criterion besides the open named-author question). Kept, as on Matrixyl: the research-page standard names `impact-text` for
  headline figures, and the alternative is custom code.
  **Consequences:** Four new tests in `tests/test_page_audit.py`, one in `tests/test_set_reviewer.py`. The glutathione hub audits 100/100/100/100 and 9.65 on the external dual-model audit with the published titles on the page.

---

## ADR-2026-09-23-T: The three key figures sit at the top of every science page

**Date:** 2026-09-23
**Status:** Accepted (Malcolm: "shouldn't the 3 main USPs/claims bar be at the top of each of the science main pages? This is better for marketing right?")
**Context:** The Matrixyl and glutathione builds placed the stock `impact-text` band with the three key figures after the definition and the evidence
prose, a third of the way down the page. Proof points high on the page lift conversion, and `page-audit.py`'s own marketing rule rewards a proof point
in the first 30% of the text.
**Decision:** On all five hubs the band sits directly under the hero: hero → key figures (White) → definition and at-a-glance (Bone) → evidence prose
(White) → findings cards → charts → usage rows → evidence table → references → FAQ → shop → related → CTA. The charts moved below the findings cards
and the evidence table below the usage rows so the Bone/White alternation holds; the four sections from References down flipped colour. Argireline,
which had no band, got one from its register (48.9% vs 0%; −7.4% vs +4.3% at day 20; 4 weeks).
**Also this day:** the PDRN and copper hubs were brought level with the two reference builds (at-a-glance list, key figures, ten-row evidence table,
image rows with a how-to, two FAQs each, references and JSON-LD extended, PDRN's findings card rewritten to the verified figures), and the copper hub
now names the trial funder and the journal's weaker peer review beside the 55.8% figure.
**Trade-offs:** The definition paragraph now starts about 60 words later, still inside the answer-first window that both external auditors score. The
`impact-text` figures still render as `<h2>` (ADR-2026-09-22 and -G); that cost is unchanged by the move. The Argireline evidence table and image rows
remain a follow-up.

---

## ADR-2026-09-24-S: The Argireline page is the science-page template

**Date:** 2026-09-24 (the build 2026-09-23; Malcolm adopted it that afternoon)
**Status:** Accepted. Malcolm: "now lets save this as the template to follow for the other science pages. We will improve them accordingly one by one later."
**Context:** The evidence-sections merge (`docs/decision-evidence-sections-merge-2026-09-23.md`) was piloted on Argireline. Malcolm then redesigned
the page section by section on the live site. The changes: a centred intro above the at-a-glance row, a numbered evidence index linking to each
finding card, two new cards (the safety record and the null result), a 3-step how-to, a 10-row Evidence & Sources table replacing both the evidence
table and the references, and himself named as author.
**Decision:** The page is the template for all five science pages (`docs/science-page-template.md`). The sections run, in order: hero, key figures,
overview, evidence index, findings cards, charts, usage, Evidence & Sources, FAQ, shop, related, CTA. It replaces Matrixyl 3000 as the reference build
and amends standard items 2 and 6 in `docs/content-plan-2026.md` §4. The other four pages move to it one at a time, on Malcolm's go-ahead for each.
**Trade-offs:**

- **Four custom-html sections:** the overview, evidence index, usage and Evidence & Sources, on top of the charts. Each was forced, because Shopify
  richtext strips classes and `specification-table` emits `<div>` rows. The cost is translation: Shopify treats each section as one block of HTML per
  language. `scripts/hub-i18n.py` and a per-page phrase table (`configs/hub-i18n/`) carry that cost.
- **The pilot's own rollout gate was missed on two small counts:**
  - external audit 9.68 against a "not below 9.70" bar;
  - `page-audit.py` GEO 100 → 96, for links inside the table.
    Malcolm adopted the template on its merits after seeing the page. Both numbers are in the template doc §8 so each rollout knows the trade.
    **Also decided in the build:**

- Malcolm is named as the author, as founder, not as a clinician: "you can use me as an author".
- The byline stays in the prose flow, because wrapped in a `<div>` it was dropped by the crawlers' extractor (commit `df440a2`).
- One section, one owning spec. Superseded specs carry `_retired`, and `hub-upgrade.py --apply` refuses them.

---

## ADR-2026-09-24-P: Science pages show positive results, and the null-result slot becomes a before/after USP

**Date:** 2026-09-24
**Status:** Accepted. Malcolm: "lets replace this section with something positive. lets use this content block to show a usp where we can show a
before and after image showing the positive effects. lets also update the science page template here - so that we do not publish negative info about
the ingredient - but that we use that space to show a USP that we can show a before and after for."
**Context:** The template (ADR-2026-09-24-S) gave a finding card and an index row to the study that found nothing. On PDRN that was the controlled
pigment trial after microneedling (Gulfan 2022); on Argireline it is the independent imaging test (Henseler 2023). The design critique and both
external auditors had counted this transparency as a trust signal.
**Decision:** No negative findings as finding cards or index rows. The slot shows a second positive, sourced USP illustrated with a before/after pair.
On PDRN it is the under-eye result (Ye 2026: eye-bag volume and tear-trough depth about 2× the retinol change, Antera 3D; register headline claim 5),
placed second so the cards run strongest first. Its before/after is to be generated and chosen by Malcolm; until then the card carries the A6 cream
macro.
**Trade-offs:** The page gives up the "reports the study that found nothing" signal that both auditors praised; the external score is re-measured
after the before/after lands. Every claim that remains is still sourced and qualified (the register's rules on wording, comparators and
"ingredient-level only" are unchanged).
**Resolved the same day (Malcolm's answers):**

- **Argireline follows the rule.** Card 5 (the null imaging test) is now the Raikou forehead result (roughness −7.4% at day 20 against +4.3% on
  placebo), second in order, with its before/after to come. Card 3 (the An 2019 microneedle patch, non-transferable) is removed. This also fixed a
  live defect: index row 03 had linked the Raikou claim to the microneedle card.
- **The table drops null and non-transferable studies on both pages.** On PDRN that leaves Ye 2026, Thellung, Squadrito 2017 and Kim TH. On Argireline, Henseler 2023 and An 2019 go.
- **The At-a-glance lines stay.**
- **Before/after waves approved** for the PDRN under-eye and Argireline forehead cards; Malcolm picks the winners.
- **Accent colour per page** (§3.6 of the template).

**Amended 2026-09-26: caveat sentences.** Malcolm answered the 24-item caveat sheet (`docs/caveat-decisions-2026-09-25.md`): "all recommended. But make
choices and use wording based on what is more effective for marketing - and the promotion of our products." The rule now reaches the sentences inside
kept cards, rows, key figures, charts and FAQ answers:

- A limitation or null clause that no claims-register rule requires is removed ("small group", "day 60 not significant", "does not support a hydration
  claim", "not read by us").
- A required qualifier stays, said positively ("Tested side by side against a 0.1% retinol cream", not "No placebo side").
- A disclosure is stated once, in _At a glance_. A table row keeps only the disclosures its register makes a condition.
- Where two honest wordings exist, the more promotional one is used.
- The Evidence & Sources column heading is now "What it found".

Applied live on PDRN and Argireline in six languages on 2026-09-26. The Argireline FAQ's unsupported "benefits beyond 28 days" was replaced by the sourced
day-20 and 4-week results. Template §3.2, §3.5 and §4 rule 3 are updated. Copper and Matrixyl still carry the old column heading.

## ADR-2026-09-26-L: Study pages keep their appraisal, reframed; no page for a null study; Robinson 2005 from the abstract

**Date:** 2026-09-26
**Status:** Accepted. Malcolm answered three questions when study-page work resumed ("start work on the next scientific study articles").
**Context:** ADR-2026-09-24-P ("do not publish negative info about the ingredient") was written for the hubs. It never mentioned the study pages
(`/pages/study/<handle>`), whose "What this study does not show" section is the appraisal the credibility research says the page exists for
(`docs/research-2026-study-hubs-credibility.md`), and whose tier-1 list (`docs/study-inventory-2026-09-24.md` §5) included a page for a null study.
**Decision:**

1. **The limits section stays on every study page, reframed.** Its heading becomes "How to read this result", and each point is a plain fact (what
   was compared, what the paper does not report, who funded it) with no "failed" or "does not show" framing. Where a point has a positive side, it
   leads with it. Applies to the live Badenhorst page too.
2. **No page for Henseler 2023** (the null Argireline imaging study). Its tier-1 slot goes to rebuilding the Wang 2013 pilot on the stock template,
   and the Henseler sentence comes off the Wang page in that rebuild.
3. **Robinson 2005 (Matrixyl) is built from the abstract**, PubMed record and the CIR 2012 summary: the full text is paywalled and the register holds
   no percentage. Its key figures are design facts (93 women, 12 weeks, 3 ppm) and it has no chart. This is a stated exception to the template rule
   "every figure read at source, from the tables", and the page's source note says what was read.

**Trade-offs:** Decision 1 keeps the one element that separates an appraisal from an abstract summary, at the cost of stating limits on a page that
sells the ingredient; the reframe makes them read as how-to-read facts. Decision 3 gives Matrixyl a study page without a measured magnitude, so the
page states the result as "small but significant from week 8" and nothing stronger.
**Supersedes:** `docs/study-page-template.md` §3 "Nulls and non-significant results appear in band 5" and the research doc's "null results qualify
on the same terms" (§3.3 criterion 5).
