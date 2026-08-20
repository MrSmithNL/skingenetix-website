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

### PHOTO-002 — 2026 redesign: reference sets built, configs outstanding

**Priority:** 🔴 High
**Owner:** Claude (configs) + Malcolm (artwork corrections)
**Status:** Reference sets DONE — 9 products, 36 crops. Configs not started.

The whole range was redesigned. New artwork lives in Drive at
`Skingenetix/Images/Products/New designs` (25 pack shots + 3 product videos) with
per-product dielines under `Skingenetix/Packaging/`.

**Confirmed with Malcolm 2026-08-19:**

- **Serums are 30ml, creams are 50ml** — matching every bottle and jar label.
- The carton is **one box with two differently-coloured large faces**, not two variants.
  Coloured front, **matte-silk SILVER** back carrying the same layout. Only Acetyl
  Hexapeptide-8 pairs its colour with white. Serum carton 41×41×99mm.
- Lids are **brushed aluminium**, not chrome — the renders read glossier than the
  physical product does in the videos.

**Reference sets built** — `scripts/build-refs-2026-08-19.py`, output to
`assets/images/_refs-2026-08-19/` (gitignored, reproducible from Drive). Four crops per
product: `product_tight`, `box_coloured_face`, `box_silver_face`, `pack_full`. Verified
mechanically: nothing clipped, carton pairs scale-matched at 0.84 fill.

**`product_tight` comes from the dedicated single-product renders** in each product's own
folder under `Images/Products/<Product>/` — 2048px, already isolated, current artwork.
Those beat cropping the product out of a pack shot on every count. The one exception is
Acetyl Hexapeptide-8, whose render is the superseded ARGIRELINE design (see PHOTO-003);
it falls back to its pack-shot crop.

One reference is **generated, not photographed**: Matrixyl 3000 Pro Collagen Serum has no
silver pack shot, so its silver carton was generated from its own green face and stored in
Drive as `GENERATED-matrixyl-serum-silver-carton.png`. Replace it if a real shot appears.

**First production run happened 2026-08-19** — Glutathione Brightening Serum,
`configs/glutathione-brightening-serum.json`, 45 shots. See PHOTO-004 for what it found.

Glutathione first because its product render is the corrected artwork (PREMIUM FORMULA,
30ML), its carton correction is in place with the extra `box_artwork_flat.png` reference,
and its gold/silver carton is the most demanding finish in the range.

**Label wording is the highest-risk part of a config.** Quote every line verbatim with its
colour; write `packaging_desc` face by face. Preflight rejects unfilled `<placeholders>` and
a `product_desc` that quotes no label text, because an invented label is clean and legible
and therefore survives review.

### PHOTO-005 — First images LIVE; uploads continuing

**Priority:** 🔴 High
**Owner:** Claude (upload + generation) + Malcolm (selection, SEO study)
**Status:** PDRN cream **published**. Glutathione serum **published**.

**The 0.2% is broken.** 8 images went live on the PDRN cream on 2026-08-20 —
the first published from the rebuilt pipeline, replacing 5 that carried the retired
label. Live at <https://www.skingenetix.com/products/pdrn-collagen-night-cream>.

**Second product published the same day.** 8 images live on the Glutathione serum,
replacing all 6 that carried the retired label. Malcolm's gallery order: packaging hero
first, hands-dropper second. Live at
<https://www.skingenetix.com/products/glutathione-brightening-serum>.

| Product                  | Candidates | Prepared | Live  |
| ------------------------ | ---------- | -------- | ----- |
| Glutathione serum        | 557        | 82       | **8** |
| PDRN cream               | 274        | 72       | **8** |
| PDRN skin repair serum   | 293        | 0        | 0     |
| Copper Peptide serum     | 177        | 0        | 0     |
| Copper Peptide Day cream | 154        | 0        | 0     |
| Copper Peptide Night     | running    | 0        | 0     |

**Awaiting Malcolm's marks:** the two finished Copper Peptide runs are consolidated for
browsing at `assets/ai-generated/ALL-copper-peptide-{repair-serum,day-repair-cream}/`
(331 candidates). They are pre-top-up — the Gemini carton shots land after the next reset,
and the collector merges them in without disturbing marks already made.

**Selection is Malcolm's, by leading underscore** — `_` keeps, `__` publishes. He wants
every candidate available and no shortlisting. See
`memory/malcolm-picks-winners-by-underscore.md`.

**Replace, never append** — every remaining live product image still shows the retired
DEEP REGENERATION FORMULA / PROFESSIONAL TREATMENT label.

**Blocked deliberately:** product _titles_ stay on the old naming until an SEO/GEO/AISO
keyword study per product is done — Malcolm's sequencing, optimised for the key ingredient
against the most-used and most-relevant search terms.

⚠️ Match images to products by **checking the image, not the title**. See
`memory/shopify-store-map-2026-08.md`.

**Queued for the next Gemini reset:** top-ups for Copper Peptide Day cream, Copper Peptide
serum and Copper Peptide Night cream — all three ran on the four non-Gemini engines only,
which leaves carton shots thin. The 2026-08-20 allowance was already at **244/250** by
15:50, so none of the three could start that day; each is
`--backends nbp_pro,nbp_flash` into the existing `run-01`, which merges on filename.
⚠️ Generation reads `GEMINI_API_KEY` **only** and this project's `.env` has no Gemini key —
see the Authentication note in `docs/architecture.md` before starting them.

**Colour is now per product, not per template (2026-08-20).** The substance inside the
container was described nowhere, so every drop, swatch and open-jar shot invented a colour —
white cream, water-clear serum. Each config now carries `formulation` (what the substance
looks like, and what it never looks like) and `palette` (scene colours built from the
product's own brand colour), and `fanout.py` refuses to run a product that declares
neither. Confirmed colours are in `memory/product-colours-2026-08.md`.
⚠️ **Copper Peptide DAY is the DARK cream and NIGHT is the LIGHT one** — it reads backwards
against the usual convention and was written inverted once already.

**No re-run for PDRN cream or Glutathione serum** — Malcolm, 2026-08-20: "i have enough
images for the PDRN cream and the Glutathione serum." Both have live images and full finals
folders. Their `formulation`/`palette` blocks are filled in and correct, so if either is
ever run again it inherits the fix; but the known-wrong substance shots (white Glutathione
drops) are simply not worth $2 to redo. Do not propose it again.

**QA run 2026-08-20 (verdicts are information, not a filter — Malcolm still picks):**

| Product              | Judged | PASS          | Shots with no passing candidate |
| -------------------- | ------ | ------------- | ------------------------------- |
| Copper Peptide serum | 177    | **135 (76%)** | 3 — 06, 07 and 27               |
| Copper Peptide Day   | 154    | **134 (87%)** | 0                               |

The serum's three empty shots are `product_and_box_hero`, `product_and_box_angled` and
`range_stacked_angled` — all carton work, failing on `label_wording` and `carton_faces`.
That is the concrete case for the Gemini top-up rather than a general preference for it.
Dominant failure reason overall is `label_wording` (36 of 62 failures across both).

**Upload plans are per-product data, not code.** Gallery order and alt text are Malcolm's
decisions and now live in `scripts/finals/upload-plans/<handle>.json`; the uploader reads
one and refuses any selected file it cannot map to a planned shot, rather than appending it
with generic alt text.

### PHOTO-004 — First production run: what it found

**Priority:** 🔴 High
**Owner:** Malcolm (winner selection) + Claude (regeneration)
**Status:** Run complete, QA complete, winners not yet picked

The first full run through the rebuilt pipeline. Config:
`configs/glutathione-brightening-serum.json`. Output:
`assets/ai-generated/2026-08-19-glutathione-radiant-glow-serum/run-01/`.

**Three pieces of the documented pipeline did not exist and were built during this run:**

1. `upload_refs.py` — nothing could produce the CDN urls Seedream and FLUX.2 need. Without
   them those two engines silently fall back to text-to-image, which is why the health
   check returned two blank unbranded bottles beside four correct ones. A missing url does
   not error; it removes the reference.
2. `contact_sheet.py` — no way to look at 293 candidates. This was the actual bottleneck
   behind 4,077 generated / 8 published.
3. `qa.py` — SKILL.md had listed a vision QA gate as pipeline step 11 since v1 with no
   implementation, the same gap the orchestrator had.

**The quoted-wording rule mostly beat reference-lock, which was not expected.** The
handover predicted the stale 50ML pack shots would show through. On most candidates the
face-by-face `packaging_desc` won and the carton reads 30ML. It did NOT win universally —
`06_product_and_box_hero_seedream_0` carries `STABLE VITAMIN C | 50ML` and `ALL SKIN
TIIRS`. Quoting the wording moves the odds; it does not remove the need for correct
references.

**Defects found, and where each was fixed.** Every one came from a real candidate:

| Defect                             | Cause                                            | Fixed in                     |
| ---------------------------------- | ------------------------------------------------ | ---------------------------- |
| Short, squat pipette bulb          | nothing described the bulb's size                | config + template + QA check |
| Purple / navy "brand gradient"     | shot 02 brief named no colour                    | template brief + config      |
| Amber-tinted frosted glass         | weak instruction                                 | config + template negatives  |
| Carton lines printed on the bottle | bottle lines never stated exhaustive             | config                       |
| Mirror-polished carton             | references shot glossy; dieline says matte satin | config                       |
| Invented carton wording            | nothing forbade additions                        | config + template            |
| Literal "BODY COPY" on a panel     | **our own prompt said "carry small body copy"**  | config                       |
| Lowercase "skingenetix", stray ®   | capitalisation never stated                      | config                       |

**Still open, not fixable from the prompt side:**

- The photographed carton references are glossy and still read 50ML. Re-rendered pack
  shots would retire the whole class (PHOTO-003).
- Luma regenerated the retired `PROFESSIONAL TREATMENT` sub-line even though that
  reference was excluded — the model reaching for a plausible alternative, not copying a
  reference. This is why the QA gate matters more than reference hygiene alone.
- QA spend is **not recorded in the cost ledger**. `qa.py` makes one vision call per
  candidate and records nothing, because Gemini 3.7 Flash's price has not been verified
  against a bill and inventing one would repeat the `nbp_flash $0.02` mistake. Unrecorded
  spend is how $122.37 went untracked in the first place.

### ⚠️ PHOTO-003 — Artwork corrections needed before print

**Priority:** 🔴 High
**Owner:** Malcolm
**Status:** Open

Reference-lock is faithful: generated images reproduce whatever the reference shows,
whatever the prompt says. These are therefore blockers, not things to prompt around.

1. **Three serum cartons state 50ML** — Glutathione, Acetyl Hexapeptide-8, Matrixyl
   serum. Serums are 30ml. PDRN and Copper Peptide serum cartons are already correct.
2. **Glutathione bottle read PROFESSIONAL TREATMENT** — ✅ resolved in the _dedicated
   render_, ❌ **still present in the pack shots.** The corrected render was in
   `Images/Products/Glutahione Brightening Serum/` all along, so `product_tight.png` reads
   PREMIUM FORMULA and 30ML. But `pack_full.png` is cropped from a pack shot that predates
   the fix: its bottle still reads **PROFESSIONAL TREATMENT** and its carton reads **50ML**,
   so it contradicts `product_tight` on two lines at once. Found 2026-08-19 while writing
   the first config; `pack_full.png` is excluded from that config's reference set for this
   reason. The same check has **not** been run on the other eight products' pack shots.

**Status (2026-08-19 18:30): ✅ RESOLVED in the references.** The updated serum `.ai` files
are genuine PDFs — magic bytes `%PDF-1.6` — so they render once copied to a `.pdf`
extension. `sips` had been refusing them on the extension alone. All three confirmed
corrected to **30ML**.

Each of the three now gets a fifth reference, `box_artwork_flat.png`, cropped from the
updated artwork. It is an **addition, not a replacement**: the flat artwork carries the
correct wording, the pack shot carries the perspective, edges and satin sheen, and
reference-lock takes both.

**Still worth doing:** re-rendered pack shots of the three cartons, so the photographic
reference agrees with the artwork rather than being corrected alongside it.

**Third correction — the Acetyl Hexapeptide-8 dedicated render is the SUPERSEDED design.**
`Images/Products/Argireline Age Control Serum /Argireline Age Control Serum.png` reads
"ARGIRELINE / ADVANCED AGE CONTROL"; its own carton says ACETYL HEXAPEPTIDE-8 /
ANTI-WRINKLE SERUM. That product falls back to its pack-shot crop. A current render would
be better.

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
