# Todo — Skingenetix (CLIENT-003)

## ✅ Phase 6 follow-up — staging triage (P6-FU-4 / skingenetix) — CLOSED 2026-08-13

**Source:** Phase 6 cluster 10 contamination cleanup (this repo
intentionally NOT modified by C10 — its single dirty entry looked
like genuine work, not contamination).

**Outcome:** the C10 read was right — `assets/` is genuine work, not
contamination. It holds 9.7 GB / 4,374 files of AI product-photography
fan-out output. That is far past GitHub's file and repo size limits, so
it is **gitignored, not committed**. `scripts/` (6 small Python
ref-builder/uploader files, no secrets) **is** now committed.

**⚠️ Consequence:** `assets/` is not backed up by this repo. It exists
only on this machine and in Drive. If that matters, a separate backup
target is needed — this is an open risk, not a solved problem.

**Also fixed in the same pass:** a cloud-sync artifact had left 47 asset
directories where the real content sat in a `" (1)"` twin and the
bare-named directory (the one every doc referenced) was empty. All 47
were repaired to their documented names; 2 byte-identical duplicates
(`.claude/settings (1).local.json`, `docs/architecture/generated/c4 (1)/`)
were removed.

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

### PHOTO-000 — Product photography: real status (audited 2026-08-19)

**Priority:** 🔴 High
**Owner:** Malcolm (winner selection) + Claude (regeneration)
**Status:** Open

Full visual audit of every run to date. The headline number is the last row.

|                                  |             |
| -------------------------------- | ----------- |
| Runs generated (Apr 14 – May 18) | **25**      |
| Images generated                 | **4,077**   |
| SEO-renamed                      | 3,078       |
| Recorded spend                   | **$122.37** |
| **Published to the live store**  | **8**       |

Eleven products live (9 active + 2 draft stamp sets), 47 product images total,
of which 8 match the AI naming pattern — so **~0.2% of what was generated has
reached the store**. Three products carry no AI imagery at all and Copper Peptide
Day Gel-Cream has a single image.

**Six of the nine 2026-05-18 runs were recorded nowhere** — Argireline, PDRN Skin
Repair, Matrixyl 3000 Serum, Copper Peptide Day Repair, Copper Peptide Advanced
Night Repair, PDRN Collagen Repair. Roughly 1,400 images and ~$34 of spend. They
are listed in the table below so they stop being invisible.

**The orchestrator that produced all of this does not exist.** No script on this
machine contains `fanout_tier` or `shots_total`; only the small ref-builder
helpers in `scripts/` survive. None of the 25 runs is reproducible — the pipeline
would have to be rebuilt from the skill's prose.

| Run (2026-05-18)                     | Candidates | Cost   | In docs before today |
| ------------------------------------ | ---------- | ------ | -------------------- |
| glutathione-radiant-glow-serum       | 146        | $5.69  | yes                  |
| copper-peptide-advanced-repair-serum | 128        | $6.18  | yes                  |
| matrixyl-3000-pro-collagen           | 157        | $9.80  | yes                  |
| matrixyl-3000-pro-collagen-serum     | 182        | $10.68 | **no**               |
| argireline-serum                     | 165        | $9.39  | **no**               |
| pdrn-skin-repair                     | 142        | $6.10  | **no**               |
| copper-peptide-day-repair            | 136        | $7.46  | **no**               |
| copper-peptide-advanced-night-repair | 178        | —      | **no**               |
| pdrn-collagen-repair                 | 130        | —      | **no**               |

**Action:** pick winners and publish. That is the only step between $122 of
finished work and the store.

### PHOTO-SKILL-001 — product-photography skill rebuilt to v3.0

**Priority:** 🟡 Medium
**Owner:** Claude
**Status:** ✅ DONE 2026-08-19 (smith-os `66bdb17`)

Templates rebuilt from the audit plus 94 client-curated luxury-brand references:
**serum_bottle 22 → 43 shots**, **cream_jar 22 → 37**. Luma `uni-1` added as a
sixth backend. Two mechanical defects that ran through all 25 runs are now
documented with enforcement rules: output resolution varies 9× (FLUX.2 and
gpt-image-2 return 1024px against Shopify's 2048 minimum), and aspect ratio was
never asserted on returned images.

The skill was also **never symlinked into `~/.claude/skills`**, so it has never
been invocable — every run was done by reading the markdown by hand. Fixed.

**Next run should use the new templates.** Cap at **three products per day**: the
Gemini daily quota is shared across NBP Pro and Flash, and on 2026-05-18 the
fourth product of the day lost all 44 NBP attempts to 429s.

### CI-001 — C4 README fix will be clobbered on regeneration

**Priority:** 🟢 Low
**Owner:** Claude
**Status:** Open

`docs/architecture/generated/c4/README.md` linked `../dependency-graph.md`, a file that is
never generated for this repo. That broken link aborted `mkdocs build --strict`, which is why
CI was red from June to 2026-08-13. It is fixed here by de-linking the reference.

**The catch:** that file is auto-generated by `render_c4.py` in `smith-os`
(`packages/forge/tools/architecture-artefacts/`). Re-running the generator will overwrite the
fix and turn CI red again. The durable fix belongs in the generator — it should only emit the
dependency-graph link for repos where that artefact is actually produced.

### PHOTO-GLUTATHIONE-2026-05-18 — Glutathione Brightening Radiant Glow Serum — winner selection

**Priority:** 🟡 Medium
**Owner:** Malcolm (human review)
**Status:** Awaiting selection

Updated product label (GLUTATHIONE BRIGHTENING / RADIANT GLOW SERUM (gold) / PREMIUM FORMULA /
2% GLUTATHIONE | 30ML / frosted clear glass dropper bottle with white pipette + silver collar)
uploaded to Drive 2026-05-18T14:28 UTC. The new design replaces the April-20 label which read
`GLUTATHIONE / RADIENT GLOW FORMULA / PROFESSIONAL TREATMENT` — it is Meta-compliant (no
`PROFESSIONAL TREATMENT` language) and corrects the `RADIENT → RADIANT` typo. Full 22-shot
Max-tier 5-backend fan-out completed the same day via the `serum_bottle` template.

**Output:** `assets/ai-generated/2026-05-18-glutathione-radiant-glow-serum/run-01/` — 146 SEO-renamed PNGs at the folder root (originals under `run-01/raw/`) from 190 attempts, 100% shot coverage. Cost: $5.69. Wall clock: 9.6 min. Naming pattern: `glutathione_brightening_radiant_glow_skin_serum_<shot>_<seq>_skingenetix.png`.

**Per-shot candidates:** 2 each for hero_white_bg, three_quarter_brand_gradient, brand_glow_hero, pedestal_edge_hero, dramatic_close_up_dark_bg; 8 each for the remaining 17 shots.

**Failure notes:** Nano Banana Pro hit Gemini 429 RESOURCE_EXHAUSTED on **all 44 attempts**
(32 edit + 12 t2i) — the daily Gemini quota (250 req/day on `gemini-3-pro-image`) was already
spent by that day's earlier runs (Matrixyl, PDRN, Copper Peptide Repair). Net effect: the five
sharp-routed label shots (01-04, 09) have only 2 Seedream candidates each instead of 4. The
other four backends (Seedream, FLUX.2 Pro, gpt-image-2, NBP 2 Flash) ran at 100% pass rate.
Hero shots spot-checked label-perfect — all six label elements correct, RADIANT spelled correctly.

**Action:** Review the 146 renamed PNGs and pick a winner per shot. Manifest at
`run-01/manifest.json`. The sharp-label hero shots are thin (2 candidates) — if neither is a
winner, rerun shots 01-04 + 09 via NBP Pro once the Gemini quota resets, or generate a fresh
Seedream/gpt-image-2 batch for those five only. Once winners are picked, publish to Shopify via
the Admin GraphQL API; C2PA-sign any destined for Meta ads.

### PHOTO-COPPERPEPTIDE-REPAIR-2026-05-18 — Copper Peptide Advanced Repair Serum — winner selection

**Priority:** 🟡 Medium
**Owner:** Malcolm (human review)
**Status:** Awaiting selection

New product label (COPPER PEPTIDE / ADVANCED REPAIR SERUM / PREMIUM FORMULA / 2% GHK-CU | 30ML /
frosted blue glass dropper bottle with white pipette + silver collar) uploaded to Drive 2026-05-18.
Full 22-shot Max-tier 5-backend fan-out (Seedream + FLUX.2 + gpt-image-2 + NBP Pro + NBP 2 Flash)
completed the same day via the `serum_bottle` template.

**Output:** `assets/ai-generated/2026-05-18-copper-peptide-advanced-repair-serum/run-01/renamed/` — 128 SEO-renamed PNGs (originals under `run-01/raw/`) from 190 attempts, 100% shot coverage. Cost: $6.18. Wall clock: 17.5 min. Naming pattern: `copper_peptide_ghk-cu_advanced_repair_skin_serum_<shot>_<seq>_skingenetix.png`.

**Failure notes:** FLUX.2 Pro edit blocked all 22 attempts (9MP total-area limit on 2K refs — downscale to 1024 next run). NBP Pro hit the Gemini 429 quota on 30/44 attempts. gpt-image-2 hit the OpenAI 5/min rate limit on 10/56 attempts. Hero shots and texture macros came through cleanly regardless.

**Action:** Review the 128 renamed PNGs and pick a winner per shot. Manifest at
`run-01/manifest.json`. `dramatic_close_up_dark_bg` is thin (2 candidates, both NBP slots
throttled) and candidate 1 has a label typo ("GHB-CU" for "GHK-CU") — favour the alternate.
Once winners are picked, publish to Shopify; C2PA-sign any destined for Meta ads.

### PHOTO-MATRIXYL-2026-05-18 — Matrixyl 3000 Pro Collagen — winner selection

**Priority:** 🟡 Medium
**Owner:** Malcolm (human review)
**Status:** Awaiting selection

Updated product label (MATRIXYL 3000 PRO COLLAGEN / FULL & FIRMING TREATMENT / PREMIUM FORMULA / frosted glass jar) uploaded to Drive 2026-05-18. Fresh 22-shot Max-tier fan-out completed the same day.

**Output:** `assets/ai-generated/2026-05-18-matrixyl-3000-pro-collagen/run-01-full-22shot/` — 157 SEO-renamed candidates across 9 backend/mode combinations (Seedream 5 Lite, FLUX.2 Pro, gpt-image-2, NBP Pro, NBP 2 Flash — each in edit and t2i mode). Cost: $9.80. Wall clock: 36.5 min.

**Action:** Review the 157 renamed PNGs and pick a winner per shot. Manifest at
`run-01-full-22shot/manifest.json` lists per-candidate costs, backends, and the recovery-run note
(gpt-image-2 edit `input_fidelity` bug — fixed, rerun captured 22 candidates). Once winners are
picked, publish to Shopify via the Admin GraphQL API; C2PA-sign any destined for Meta ads.

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
