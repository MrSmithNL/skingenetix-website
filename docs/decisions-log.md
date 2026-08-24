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
**Status:** Proposed
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
**Context:** The shop landing page needed a branded header banner. All thirteen collections shared `templates/collection.json`, so tuning the banner there would have changed `/collections/serums`, `/collections/pdrn` and ten others. The `collection-banner` section also had settings that actively damaged a designed product line-up: parallax renders the image at 130% and only ever reveals 77% of its height (it cut the bottle bases off), and a 50% overlay greyed the products out.
**Decision:** Copy the shared template to `templates/collection.<handle>.json`, edit only its banner, and point the collection at it with `templateSuffix`. Publish with `scripts/publish-collection-banner-template.py <handle>` (has `--dry-run` and `--restore`). Applied to `all` on 2026-08-24 and generalised to `pdrn` the same day; each page carries its own overlay, text placement and measured text width.
**Rationale:**

- The banner box is a **fixed pixel height** (375/400/440) across a full-bleed width, so its aspect ratio runs from ~1.0 on a phone to ~5.8 on a 2560 monitor. No single crop survives that, which is why the section ships with a separate mobile image slot.
- Every other collection keeps the shared template untouched.
  **Consequences:** Gotchas worth remembering, each of which cost a round to find:
- Section ids in a JSON template render as `shopify-section-template--<theme id>__<key>`, so an id selector built from the section key silently matches nothing. Target the section's class instead.
- Shopify rejects the `html` setting with a 422 if it contains `{{` or `}}` — which minified CSS produces the moment a rule closes inside a media query (`;}}`). Keep the braces apart.

**Amendment 1, 2026-08-24 — the 700–1099px band was misreading product names.**
Squeezing a 3:1 banner into that width shrank the jar labels to ~3px per character, and at that size **`PDRN` resolved as `PORN`** on both banners — the exact failure `.claude/rules/website-imagery.md` rule 3 was written about, reproduced live. Two findings worth keeping:

- **Serving a bigger source does not fix it.** The limit is the *display* size, not the delivery: a forced 1600w source rendered the identical misread at 768px. Only enlarging the subject on screen works.
- **Shopify will not upscale, and fails silently when asked to.** Requesting `width=1600&height=988&crop=right` against an 848px-tall master returned `1600x533` — the *full frame resized, crop ignored*. Size a crop request from the master's own height, never from the viewport.

**Amendment 2, 2026-08-24 — `image_size: "auto"` was the wrong lever; widen the master instead.**
`auto` avoided cropping but made both headers **taller than every other collection page**, which is a visible inconsistency and was rejected on review. The banner now keeps the theme's standard `sm` height (375/400/440) everywhere, and the fit is solved in the image rather than the box:

- **Widen the master to 3000px** (the long-edge cap in `upload-theme-images.py`). At a *fixed* box height, `object-fit: cover` scales purely by height, so surplus width is not wasted — it is croppable margin, and the subject renders at exactly `box_height / master_height` regardless of viewport.
- **Aim that margin with `object-position: right center`.** The theme centres it, which would eat the model and the extension equally; anchoring to the subject side means horizontal cropping only ever removes extended backdrop.
- This also **retired the tablet crop from Amendment 1**: at the standard height the 700–1099px band crops horizontally instead of squeezing, so the products fill more of the frame and every label reads without special-casing.
- Vertical crop at very wide viewports is the residual trade-off: 5% at 1920 on the 4.14:1 master, versus 31% before it was widened.

