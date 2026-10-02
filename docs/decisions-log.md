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

## ADR-2026-09-29-C: A "Clinical studies" section under Science

**Date:** 2026-09-29
**Status:** Accepted. Malcolm asked where the research articles are in the navigation; the audit found none. He approved all four
elements of the design in `docs/decision-research-section-navigation-2026-09-29.md`.
**Decision:**

1. **Name:** "Clinical studies": page `/pages/clinical-studies`, menu line "All clinical studies". This replaces the planned
   `/pages/evidence-library`.
2. **Placement:** one line under the five tiles in the existing Science mega-menu (and the sixth line in the phone drawer), a
   footer link in Explore, and a band on `/pages/the-science`. No new top-level item and no split.
3. **Study pages:** the banner label "Clinical Study · YYYY" becomes a breadcrumb, _Science › Clinical studies › [ingredient]_,
   with a four-level BreadcrumbList.
4. **Timing:** the page is built now in English, unpublished, in parallel with the Raikou prototype work. **Nothing is linked**
   (menu, footer, the-science, breadcrumbs, hub and homepage links) until the index and the study pages are translated; then it
   all goes live together in six languages.

**Scope of the page:** the rows are the five hubs' Evidence & Sources tables (ADR-2026-09-24-P already applied), with "Read our
appraisal" where a study page exists. Individual study pages are not menu items.
**Not decided here:** product → study links (internal-link programme), the Discover duplicate, and hiding the empty Learn blog.

**Amended 2026-09-29 (same day): Clinical studies is a blog.** Malcolm clarified he meant a blog list of the study articles, like Hairgenetix,
and approved moving the study pages into it (`docs/decision-clinical-studies-blog-2026-09-29.md`):

- `/blogs/clinical-studies` (stock `main-blog` list under a stock image band). One article per appraised study. Each article is a shell
  (title, excerpt, card image, date, ingredient tag, SEO) whose `study.entry` metafield points at the unchanged `study` metaobject.
  `templates/article.clinical-study.json` renders the designed layout through that reference.
- `/pages/study/<handle>` → `/blogs/clinical-studies/<handle>` (301; Shopify applies it per locale). The `study` definition's web pages are
  switched off.
- The 32-row table page (`templates/page.clinical-studies.json`) was retired unpublished; its rows stay on the hubs.
- Menu: **Discover** (a stock item beside The Science) replaces the styled line under the Science tiles. It goes live with the footer
  link and the Science-page band once Badenhorst and Raikou are translated.

**Amended again 2026-09-29: the menu item is under Science.** Malcolm: "add this page https://www.skingenetix.com/blogs/clinical-studies
to the main menu under 'science'." Live the same day: `main-menu` › Science › **Clinical studies** (type BLOG, `/blogs/clinical-studies`),
translated (Klinische Studien, Klinische studies, Études cliniques, Estudios clínicos, Studi clinici). On desktop it renders as a full-width,
centred text line under the five ingredient tiles (`scripts/menu-image-tiles.py` ROWS, pushed with the new `--css-only` flag so the header
was not rewritten); in the phone drawer it is the sixth line. This replaces the Discover placement. Linked on his instruction ahead of the
Badenhorst and Raikou translations. The footer link and the Science-page band were not part of this instruction and are still open.

**Amended a third time 2026-09-29: the menu item is under Discover, with an image tile.** Malcolm: "sorry - add the blog overview for
Clinical studies page menu link under 'Discover' (not science)", then "and add an image for it". Live the same day: the same menu item
(`gid://shopify/MenuItem/809197994369`, ID kept) moved from Science to Discover, beside The Science, Ingredients and Our Philosophy. The
move dropped its five translations; they were re-registered on `gid://shopify/Link/809197994369`. On desktop it is the fourth image tile
(`skingenetix-menu-clinical-studies-research-lab.jpg`, a square crop of the existing evidence-bench candidate
`the-science--C-evidence-bench-gpt_image_02.png`, no new generation; plan
`configs/banners/menu-clinical-studies-tile-2026-09-29.json`). The text line under the Science tiles is gone (`ROWS = []` in
`scripts/menu-image-tiles.py`, pushed with `--css-only`). Verified live in English, German and the phone drawer. This supersedes the
Science placement. Backup of the menu before the move: `backups/main-menu-20260929-154059.json`.

## ADR-2026-09-29-D: "Collagen & Skin Plumping" is kept and becomes the collagen-skincare page

**Date:** 2026-09-29
**Status:** Accepted. Malcolm: "Yes, and rename address".
**Context:** `/pages/collagen-skin-plumping` predates the keyword strategy. It sat in no menu, its only inbound links were
Related tiles, and it duplicated `/pages/firming-skin-density` by intent (same Matrixyl 3000 + copper peptide, same routine,
near-identical FAQs; it also contradicted the Firming page on topical collagen). It earned 1 impression in 90 days. Malcolm
asked to keep it and add it to the menu only if it can own a collagen or other high-volume term with no overlap or
cannibalisation with any other key page.
**Evidence:** the existing keyword data had no qualifying term; its collagen head terms had never been seeded. A paid pull
(US, GB, DE, NL; $1.43; `configs/keyword-data/collagen-2026-09-29/`) measured an unowned collagen cream / serum cluster of
about 3,700 observed searches a month: US collagen cream 656, collagen serum 605, collagen face cream 201, collagen cream for
face 201; GB collagen cream for face 472, collagen face cream 394, collagen cream 394; DE kollagen serum 317, kollagen creme
211, kollagen booster 105, kollagen gesichtscreme 105; NL collageen serum 102, collageen booster 102, collageen creme 51.
Keyword difficulty 0–2. The US results mix shops and brands with editorial guides (Allure, Byrdie, NYT Wirecutter); the GB
results are mostly forums. "Collagen peptides" demand is supplements and is excluded.
**Decision:**

- The page becomes **Collagen Skincare**: a shoppable guide answering which collagen creams and serums work. Primary
  term `collagen cream` (with `collagen face cream`, `collagen cream for face`), secondary `collagen serum`; DE `kollagen creme`,
  `kollagen serum`, `kollagen gesichtscreme`; NL `collageen serum`, `collageen creme`.
- New address `/pages/collagen-skincare`, with a 301 from `/pages/collagen-skin-plumping` in every language.
- `/pages/firming-skin-density` keeps firming, sagging and elasticity terms and stops targeting "collagen" (meta description; its
  topical-collagen FAQ moves to the collagen page). Products keep their own terms (e.g. the Pro-Collagen cream keeps
  `peptide cream`).
- Menu: a fifth Skin Solutions tile, "Collagen Skincare", in six languages, once the rebuilt page is approved.
  **Conditions:** products shown up front (the searches are commercial); the answer on topical collagen is honest and sourced (a
  new claims register); no product promise to boost collagen; the rebuilt page is shown to Malcolm before it goes live.

## ADR-2026-09-30-P: The two pilot studies get their own article template until they are rebuilt

**Date:** 2026-09-30
**Status:** Accepted and live. Malcolm: "yes" (to the audit's fix list).
**Context:** The central SEO/GEO/AISO audit (2026-09-29, `docs/audits/tracker-skingenetix.com.md`) found Wang 2013 and Ye 2026
rendering twice: the stock article template printed seven empty section headings under their pilot body and their reference a
second time. Their content lives in `sections_html`; every stock field is empty.
**Decision:** `templates/article.clinical-study-pilot.json` — banner, body, safety note, JSON-LD — assigned to both (template
suffix `clinical-study-pilot`); `build-clinical-studies-blog.py` assigns it to any pilot config. The stock template is unchanged.
**Undo:** set the two articles' template suffix back to `clinical-study`. **Ends when** the pilots are rebuilt on the stock template.

## ADR-2026-09-30-S: A "Before you try it" safety note on every study article

**Date:** 2026-09-30
**Status:** Accepted and live in six languages. Malcolm: "yes — if this is best practice for premium skincare brands".
**Evidence:** `docs/research-2026-09-30-safety-notes-on-study-articles.md`. Not a Google rule (the rater guidelines have no such line)
and not an EU duty for articles, but the practice of Medik8, INKEY, Timeless and Murad, and justified here because each article sits
one click from a product and reports trial side effects without use guidance; PDRN is salmon-derived (fish allergy).
**Decision:** one block right before the product buttons, use guidance only; six-language words in `configs/study-safety-note.json`
(theme locale files, `skingenetix.study_safety`); PDRN line only on PDRN studies. Never "safe", "proven safe", "hypoallergenic" or
"dermatologically tested" (EU Reg 655/2013: a safety statement is a claim). **Open:** native review of the five translations; the product
pages carry no precautions at all (checked on the PDRN serum) — a separate decision.

## ADR-2026-09-30-K: Study articles own their trial's question; "does X work?" belongs to the hub

**Date:** 2026-09-30
**Status:** Accepted (Malcolm: "the keyword research and keyword strategy should decide this").
**Evidence:** `docs/keyword-ownership-analysis-2026-09-30.md` §4 ($1.26 of DataForSEO). No study's own question has measurable
demand; the efficacy questions do — "does argireline work" 656/month (US), page one forums only.
**Decision:** each study article owns its own trial question (`keyword-strategy-2026.md` §4 table; `page-targets.json` type
`study`), links up to its hub, and is judged as an evidence page, not a traffic page. "Does X work?" is a hub section. A study title
never asks the ingredient-wide question — Badenhorst retitled on this rule.
**Pending, same analysis §1–3:** the product-vs-hub overlaps (argireline, matrixyl 3000) and the "peptide skincare" owner — a
recommendation awaiting Malcolm.

## ADR-2026-09-30-Q: A page is done at a score of 9 or more, with no confirmed failures

**Date:** 2026-09-30
**Status:** Accepted. Malcolm: "lets keep improving until it scores a 9 or more."
**Context:** Commits `e89d845` and `fe94d19` retired the external ≥ 9.0 bar in both page templates. They followed the
`seo-aiso-validator` skill's rule that a score is never a gate, and they did not record a decision from Malcolm. He had set the bar
on 2026-09-24 ("improve it until it scores above a 9"), and he restated it when asked.
**Decision:** a page built or rebuilt on this store is done when three things hold on the central auditor (v2, `report.score`
quoted with its gates and coverage):

1. every gate passes;
2. there are no confirmed failures;
3. the score is **9.0 or more**.

The fix rules do not change:

- fix only confirmed failures the page can honestly meet;
- never fix contested verdicts;
- never add a citation, number, credential or person that is not true;
- never pad the page or add hidden text;
- safety wording, claims and brand decisions go to Malcolm.

When the confirmed failures are cleared but the score is still under 9, the loop continues:

- improve the page for its readers where the weakest dimension points;
- re-audit;
- report to Malcolm, and ask him when nothing honest is left to do.

**Consequences:**

- `docs/study-page-template.md` step 9 and `docs/science-page-template.md` step 10 now read "no confirmed failures and a score of
  9.0 or more".
- This project's bar is stricter than the skill's default, which stops at no confirmed failures.
- A score difference under about 0.9 is judge noise, so a page just under 9 is re-audited once before any content is changed for
  the score.

**First application:** Badenhorst 2016 on 2026-09-30 scored 9.78, with 0 confirmed failures, all five gates passing and 39 of
51 criteria assessed (`docs/audits/page-audit-2026-09-30-copper-peptide-wrinkle-trial-badenhorst-2016.md`). Done with no fix round.

## ADR-2026-10-01-R: Study articles get one section per proven result, and how-it-works blocks

**Date:** 2026-10-01
**Status:** Accepted (Malcolm's instruction). Template built and tested on branch `study-outcome-sections`; not yet deployed.
**Instruction:** "every study blog article should have seperate content sections for each of the proven trial outcomes with before and
after images where this can be used (similar to the ingredient science pages). And these should also be separate content blocks for the
proven working active effects of what was tested … lets add this to the scientific study article template - and lets run the existing study
articles against this criteria".
**Decision:** two sections on the article template, both the science pages' own `research-before-after` section: **results** (up to four,
after "At a glance") and **how it works** (up to three, after "What the researchers did"). The rules are in `docs/study-page-template.md`
§3.1:

- a result qualifies when it is positive and significant against the comparison (p ≤ 0.05);
- a before/after appears only where the result is visible and the picture does not exceed it;
- a how-it-works block covers an effect that was tested, framed as laboratory work, in the register's words.

The `study` entry is full (40 of 40 fields), so the content lives in a companion `study_detail` entry linked from the article as
`study.detail`. The section was amended to skip empty slots, so the science pages are unchanged.
**Defaults applied, open to Malcolm:**

- an instrument-only result (Raikou's roughness, Tadini's firmness reading) gets a plain photograph, not a before/after. The Argireline hub
  already shows a forehead before/after for Raikou;
- Robinson 2005's p ≤ 0.10 results follow his ruling on that study (review pack decision 2).

---

## ADR-2026-10-01-T: Review-pack decisions on the four new study articles

**Date:** 2026-10-01
**Status:** Accepted (Malcolm: "1 - 4 = agree", then "agree on both"). Live, verified in six languages.
**Context:** the review pack `docs/review-2026-10-01-four-new-study-drafts.md` listed what was still open after the four articles
(Yogya 2022, Tadini 2015, Robinson 2005, Watanabe 2014) went live. Malcolm took each recommendation.
**Decisions:**

1. **Robinson 2005 is labelled "Matrixyl", not "Matrixyl 3000"**, on its list card and in the filter row. It tested palmitoyl
   pentapeptide-4, the original Matrixyl®, and the register says never to conflate the two. A Matrixyl 3000 trial (handle
   `matrixyl-3000-…`) keeps its own label (`TAGS` in `scripts/build-clinical-studies-blog.py`, `cf0a4de`).
2. **Two new skin-concern labels: "Firming" (Tadini) and "Brightening" (Watanabe).** Each label page links to its Skin Solutions page
   (`/pages/firming-skin-density`, `/pages/brightening-glow`) and reuses that page's own translated title ("Straffung & Volumen", "Éclat
   & Glow" …) (`cf0a4de`).
3. **The PDRN microneedling stamp set stays a separate decision.** Yogya tested radiofrequency microneedling in a hospital, which the
   register marks "not transferable" to a home stamp, so the article does not link the set. If the set launches, its page may cite
   Yogya as background on the ingredient only.
4. **Robinson's "significant" always carries the paper's threshold** (p ≤ 0.10; the usual bar is p ≤ 0.05): on the rebuild's card
   f2 (`92bde04`) and in the three live places on the Matrixyl hub (`09aad33`, set-only spec
   `configs/hub-upgrades/matrixyl-3000-research-robinson-threshold-2026-10-01.json`).
5. **German glutathione wording stays "heller wirkend"**, matching the live hub and the register's "brighter-looking". "Strahlend"
   would claim radiance, which the trial did not measure. Any future change applies to the hub and the articles together.

**Robinson's p ≤ 0.10 footing** (the first draft of the review pack called this "decision 2", which ADR-2026-10-01-R refers to): settled
when Malcolm published all four articles ("All four, now"). Robinson went live stating the bar openly in its key figure and limits.
**Undo:** article tags `backups/clinical-studies-article-tags-20261001-161634.json`; list template
`backups/hub-upgrade-templates__blog.clinical-studies.json-20261001-161715.json`; Matrixyl hub template
`backups/hub-upgrade-templates__page.research-matrixyl.json-20261001-170516.json` (each `hub-upgrade.py <spec> --rollback`).
