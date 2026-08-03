# Todo — Skingenetix (CLIENT-003)

## 🟢 Phase 6 follow-up — staging triage (P6-FU-4 / skingenetix)

**Source:** Phase 6 cluster 10 contamination cleanup (this repo
intentionally NOT modified by C10 — its single dirty entry looked
like genuine work, not contamination).

**Status:** 1 untracked entry: `?? assets/`

**Action:** check `ls assets/` — if these are real product assets to
ship, `git add assets/ && git commit`. If they're test/staging files
that shouldn't be tracked, add `assets/<pattern>/` to `.gitignore`.

This is the lowest-priority Phase 6 follow-up — single dir, isolated.

## How This Works

- Check at start of every session
- Update at end of every session
- Priority: 🔴 High / 🟡 Medium / 🟢 Low

---

## Actual State (verified 2026-08-03 via Shopify API)

The store is **much further along** than the item statuses below suggest (those were written at project setup). Live reality:

- **Live** on www.skingenetix.com (EUR), theme **Impact** installed (MAIN)
- **9 active products** (serums + creams), all EUR 49,95, but **0 inventory** (not selling yet)
- **18 content pages** + **13 collections** live
- Blog "News" exists but **0 articles**
- **Only English** locale published (no multilingual yet)
- All 9 products have **HS-code 3304.99.5000 + origin CN** (US import) and **Shopify taxonomy categories** (Face Serums / Face Moisturizers) as of 2026-08-03

Biggest open gaps for "further building": multilingual (9 languages), blog content, SEO audit, and inventory/launch readiness. See `handover-2026-05-06.md` for the full state-discovery notes.

---

## Open Items

### SETUP-001 — Create Shopify Store

**Priority:** 🔴 High
**Owner:** Malcolm (human)
**Status:** ✅ DONE
**Store URL:** skingenetix.myshopify.com
**Domain:** skingenetix.com (registered at OpenDomainRegistry.net)

### SETUP-002 — Domain Configuration

**Priority:** 🔴 High
**Owner:** Malcolm (human)
**Status:** ✅ DONE — live on www.skingenetix.com
**What needs doing:**

- Point DNS at OpenDomainRegistry to Shopify
- Set up A record and CNAME per Shopify instructions
- Configure MX records for email (GoDaddy)

### SETUP-003 — Email Hosting Setup

**Priority:** 🔴 High
**Owner:** Malcolm (human)
**Status:** Not started
**What needs doing:**

- Add domain to GoDaddy hosting account
- Create email addresses (info@, support@, etc.)
- Configure MX records at OpenDomainRegistry
- Test email delivery

### SETUP-004 — Shopify Payments (KYC)

**Priority:** 🔴 High
**Owner:** Malcolm (human)
**Status:** Not started
**What needs doing:**

- Set up Shopify Payments with bank details
- Complete KYC/identity verification
- Configure accepted payment methods

### SETUP-005 — Install & Configure Theme

**Priority:** 🔴 High
**Owner:** Malcolm (install) + Claude (configure)
**Status:** ✅ DONE (install) — Impact theme installed as MAIN. Finetuning tracked under BUILD-001.
**What needs doing:**

- Choose and install free theme (Sense or Refresh)
- Claude configures colors, typography, layout via JSON

### SETUP-006 — Create Custom App for API Access

**Priority:** 🔴 High
**Owner:** Malcolm (human)
**Status:** ✅ DONE — credentials received, pending Bitwarden save
**What was done:**

- Custom app created in Shopify
- Client ID and secret generated
- Pending: Save to Bitwarden (vault needs unlocking)

### SETUP-007 — Install Core Apps

**Priority:** 🔴 High
**Owner:** Malcolm (human)
**Status:** Not started
**What needs doing:**

- Install Langify (configure 9 languages)
- Install Klaviyo
- Install Kaching Bundles
- Install hCaptcha

### SETUP-008 — Tax & Shipping Configuration

**Priority:** 🟡 Medium
**Owner:** Malcolm (human)
**Status:** Not started
**What needs doing:**

- Configure EU VAT settings
- Set up shipping zones and rates (mirror Hairgenetix)
- Configure checkout branding

### BUILD-001 — Theme Customization

**Priority:** 🟡 Medium
**Owner:** Claude
**Status:** Not started
**Dependencies:** SETUP-005, SETUP-006
**What needs doing:**

- Configure theme JSON settings (brand colors, fonts, layout)
- Add custom CSS for Skingenetix identity
- Set up homepage sections and blocks

### BUILD-002 — Products & Collections

**Priority:** 🟡 Medium
**Owner:** Claude
**Status:** Not started
**Dependencies:** SETUP-006
**What needs doing:**

- Create all product listings via API
- Set up variants, pricing, images
- Create collections (by type, by concern)
- Add metafields for custom data

### BUILD-003 — Navigation & Pages

**Priority:** 🟡 Medium
**Owner:** Claude
**Status:** Not started
**Dependencies:** SETUP-006
**What needs doing:**

- Create navigation menus (main, footer)
- Create content pages (About, FAQ, Ingredients, Guarantee, Support)
- Set up blog structure

### BUILD-004 — Translations

**Priority:** 🟡 Medium
**Owner:** Claude (text) + Malcolm (media)
**Status:** Not started
**Dependencies:** BUILD-001, BUILD-002, BUILD-003
**What needs doing:**

- Generate translations for all text content (9 languages)
- Register via translationsRegister API
- Malcolm uploads translated images/videos in Langify

### BUILD-005 — SEO Setup

**Priority:** 🟡 Medium
**Owner:** Claude
**Status:** Not started
**Dependencies:** BUILD-002, BUILD-003
**What needs doing:**

- Meta titles and descriptions for all pages/products
- URL handle optimization
- Structured data (schema markup)
- Sitemap verification

### LAUNCH-001 — Analytics & Tracking

**Priority:** 🟢 Low (needed before launch)
**Owner:** Malcolm (human)
**Status:** Not started
**What needs doing:**

- Connect Google Analytics 4
- Set up Google Ads conversion tracking
- Configure Facebook Pixel

### LAUNCH-002 — Email Flows

**Priority:** 🟢 Low (needed before launch)
**Owner:** Malcolm (human)
**Status:** Not started
**What needs doing:**

- Configure Klaviyo welcome flow
- Set up abandoned cart emails
- Set up post-purchase follow-up
- Set up review request flow

### LAUNCH-003 — Pre-Launch Testing

**Priority:** 🟢 Low (needed before launch)
**Owner:** Malcolm + Claude
**Status:** Not started
**What needs doing:**

- Test purchase flow in each language
- Verify all translations display correctly
- Check mobile responsiveness
- Verify email delivery
- Final SEO audit

---

## Completed Items

| ID           | What                                                     | Completed  |
| ------------ | -------------------------------------------------------- | ---------- |
| RESEARCH-001 | Full technical research — Shopify + Claude Code approach | 2026-03-05 |

---

## Session Log

| Date       | What Was Worked On                                                                                                                                                                                                                 |
| ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2026-03-05 | Project created. Research completed. Initial architecture and standard files set up.                                                                                                                                               |
| 2026-05-06 | State-discovery: found store far ahead of docs. Handover written (handover-2026-05-06.md). No store changes.                                                                                                                       |
| 2026-08-03 | Set HS-code 3304.99.5000 + origin CN on all 9 products (US import). Set Shopify taxonomy categories (5x Face Serums, 4x Face Moisturizers). Fixed expired Skingenetix client secret in business dashboard. Doc-sync (this update). |
