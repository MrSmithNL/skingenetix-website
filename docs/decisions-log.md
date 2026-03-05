# Decisions Log — Skingenetix (CLIENT-003)

Technical decisions recorded in ADR (Architecture Decision Record) format.

---

## ADR-001: Use Free Shopify Theme (Sense or Refresh)

**Date:** 2026-03-05
**Status:** Proposed
**Context:** Hairgenetix uses a premium theme (Release - Satyam). Skingenetix needs its own visual identity while remaining manageable by Claude Code.
**Decision:** Use a free Shopify 2.0 theme (Sense or Refresh) rather than purchasing a premium theme.
**Rationale:**
- Gives Skingenetix distinct brand identity from Hairgenetix
- Free themes follow standard Shopify 2.0 architecture (most Claude-friendly)
- No license cost — budget goes to apps instead
- Sense is designed specifically for beauty/wellness brands
- Refresh is strong for storytelling and ingredient-focused content
**Consequences:** May have fewer out-of-box features than premium themes. Mitigated by Claude's ability to configure sections/blocks and add custom CSS.

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
