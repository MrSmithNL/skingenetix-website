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

### ✅ BRAND-007 — /pages/skin-repair-renewal: two medical explainer diagrams

**Closed 2026-08-25.** Malcolm: professional medical-beauty explainer diagrams for the
*What Slows Skin Repair?* and *The Renewal Approach* blocks, in the style of the Matrixyl
explainer set. Both blocks wore borrowed stock — a cream-texture swirl and a turquoise
laboratory scene — neither of which explained anything.

**Style inherited unchanged** from the live Matrixyl set on `/pages/matrixyl-3000-research`:
layered skin cross-section, three legible strata, actives as translucent spheres above the
surface, delivery as shafts of light rather than arrows, starburst glints at arrival,
high-key hazy ground, peach-cream tissue. Colour is Clinical blue `#014EB1` — this concern's
ground colour in the concern-to-colour map — with teal and turquoise negated so it never
blurs into the Matrixyl page, the mirror of that brief negating copper.

**The two pictures are deliberately not interchangeable**, which is the r3 lesson:

- **causes is the deficit state** and carries *no* spheres, *no* shafts and *no* glints — the
  whole delivery vocabulary is absent on purpose. Its four faults are the four the copy
  names, each in the stratum it belongs to: piled dull surface plates (slower renewal), grey
  motes settling on them (environmental stress), sparse slack fibre below (loss of firmness),
  and the surface sagging into the gap (reduced resilience).
- **approach is the supported state**, and it had to carry the copy's *negative* argument —
  renewal skincare supports the skin's own processes rather than forcing turnover through
  exfoliation, "which can thin the skin". So the outer layer is explicitly whole, and
  peeling, flaking, dissolving and scrub particles are all negated by name. A picture that
  stripped the surface would illustrate the thing the paragraph argues against.

**Two actives, two devices, two destinations**, because this page is not a single-ingredient
page: PDRN as a flat untwisted ladder of paired beads reaching the renewal cell layer, GHK-Cu
as a three-bead chain with a copper centre reaching the fibre zone.

**The molecule check overturned the best-looking candidate.** `nbp_pro_01` won the approach
block on the contact sheet *and* on the render-size pairing. At 100% its copper chains carry
**five** beads and its ladders visibly **spiral** — the wrong molecule for a tripeptide, and
the DNA cliché the set has negated throughout. Neither fault is visible below ~40% zoom. All
eleven candidates were then cropped to the sphere band at full resolution and the beads
counted: gpt-image, nbp_flash, nbp_pro_02, seedream and luma_01 render it correctly;
nbp_pro_01 and luma_02 do not; FLUX.2 adds gold beads, negated by name. `nbp_flash_02` won on
the count *and* the picture.

**Re-run twice more, and both rounds were my brief's fault, not the engines'.**

- Malcolm: *"the underside of the skin isn't good enough … it now looks like a half empty
  area"*. Round 1 had told every engine the deep zone held bundles that were *"thin, sparse
  and slack … with wide empty gaps between them"* — my own way of signalling lost firmness.
  Six engines obliged and made an arch-shaped void. Research settled it: ageing skin does
  **not** empty — collagen fragments and disorganises, elastic fibres clump, fibroblasts
  fall, and the **dermal-epidermal junction flattens**, which round 1 lacked entirely
  ([Baumann 2007](https://pathsocjournals.onlinelibrary.wiley.com/doi/full/10.1002/path.2098),
  [Am J Pathol 2020](https://ajp.amjpathol.org/article/S0002-9440(20)30142-5/fulltext),
  [StatPearls: Dermis](https://www.ncbi.nlm.nih.gov/books/NBK535346/)).
- Round 2 then **overshot**: "packed edge to edge" cured the void and produced a dense
  fibrous mat, in a different visual world from its own partner. **Filled and uncrowded are
  both achievable** — round 1 and round 2 are two ends of one knob.
- Malcolm: *"get the style to fit … they need to fit together as a pair"* and *"show a clear
  wrinkle so you can see the damage underneath"*. Round 3 states the style as a
  **description of the published frame** rather than a genre, and re-runs **both** blocks —
  no work on one image makes it pair with the other while the colours disagree.

**Reddish pink is also the anatomically right answer**, not only a preference: dermis is
eosinophilic and densely vascular, pink in every H&E section and every professional plate.

**Published 2026-08-26: both frames from `nbp_pro_01`.** One engine for both was the
deciding criterion — the blocks sit directly above and below each other, so a split pick
wins each picture and loses the pair. Molecules counted at 100% first: two flat PDRN
ladders and two three-bead copper tripeptides, balanced. Five of eleven pass; `luma_02`
renders five beads and FLUX.2 omits the tripeptide.

Configs: `block-skin-repair-renewal-medical.json` (round 1),
`block-srr-causes-dermis-detail.json` (round 2),
`block-srr-matched-pair.json` (round 3 briefs),
`block-srr-pair-publish.json` (the published pair, handles and delivered CDN bytes).

### ✅ BRAND-006 — /pages/faq category blocks: titles to the top, real photography in all five

**Closed 2026-08-25.** Malcolm: align the block titles to the top of the image area, then
fill the five pictures — two from images we already had, three newly made.

**The alignment.** The title was absolutely positioned at the *foot* of the picture, which
put it roughly 400px below the first accordion row in the right-hand column. It is now at
the top, so the two columns start on the same line. The scrim went with it: a bottom scrim
under a top title would darken the empty half of the frame and leave the type sitting on
whatever happened to be up there.

**What went in each block, and why.**

| Block | Picture | Source |
|---|---|---|
| Products & Usage | Woman applying pale-blue cream to her cheekbone | library — cream-application-faces, NBP Flash |
| Ingredients & Safety | Open Copper Peptide Night Repair jar, lid resting beside it | library — ALL-copper-peptide-night-repair-cream, Seedream |
| Orders & Shipping | White shipping box, brand mark on the lid | **new** — NBP Pro |
| Returns & Refunds | Smiling woman reading her phone | **new** — Seedream |
| Skincare & Routine | Macro cheek, clear serum falling from a glass pipette | **new** — NBP Flash |

**NBP Pro won the box on the HELIX, not on the spelling.** gpt-image spelled `Skingenetix`
correctly on both its candidates and drew the mark as bare vertical dashes with no
continuous strand — right word, wrong logo. Only NBP Pro reproduced the reference mark:
S-curve strand crossing the dashes, scattered dots, capital S, bold italic lowercase, and
no other lettering anywhere on the box. **A brand check is not a spellcheck** — same
lesson as `count-label-elements`, one level up: the mark itself is an element to verify.

**The two library images were cropped to 4:3 before upload, not left square.** `object-fit:
cover` discards 25% of a square's height at every viewport; cropping here chose what went
instead of letting the browser choose. `scripts/make-faq-category-crops.py` makes both
reproducible, since `assets/` is gitignored. It also trims the ~50px ragged black film
border NBP Flash baked into the cream-application frame — measured at 51/50/42/42px on a
4096 square, trimmed at 70. Left in, it renders as a dark bar down both sides of the block.

**One block needed its own scrim, and measuring is what found it.** With the standard ramp
the five blocks read 10.6 / **4.0** / 19.4 / 20.5 / 19.4 to one, measured off the live page.
The open-jar shot is a bright product frame on a pale ground and was five times weaker than
its neighbours. It now carries `.sg-faq-bright` — a steeper ramp on that block alone — and
reads 11.2:1. Which blocks are pale is **data in the IMAGES map**, not a hardcoded section
id, because template-scoped ids go stale.

**Left deliberately undone:** the five `skingenetix-faq-placeholder-*.jpg` files are still in
Shopify Files. Deleting data from an external service needs Malcolm's explicit go-ahead
(CLAUDE.md hard boundary). Nothing references them — search Files for `faq-placeholder`.

**Two corrections, same day.** Malcolm: *"redo the Returns & Refunds image with a caucasian
middle aged woman"* and *"redo the Skincare & Routine image removing the black section at the
top covering the models face."*

- **Returns** needed no new generation. The original run already held **seven** Caucasian
  candidates across four engines — the East Asian model had been a choice made for range
  across the page, not the only thing the batch produced. gpt-image 01 wins it at render
  size, and the swap cost nothing. The all-suppliers rule paid twice: once for the first
  choice, again for making a change free.
- **Skincare did need re-shooting, and my brief caused the fault.** It asked for a backdrop
  *"falling to near-black at the top of the frame so the upper third is quiet and almost
  empty"* — written to give the white title a dark ground. At a 4:3 crop of a face that
  close, a quiet empty upper third **is** a black bar across the forehead. Every engine did
  exactly what was asked. The rewrite states the frame as an **edge condition** — skin
  reaches all four edges, no backdrop anywhere — because the way to stop an engine putting
  something behind her is to leave nothing behind her to describe. All nine candidates came
  back clean, so it was the brief, not the engines.
- Without a dark ground the new frame reads 6.4:1 under the title. Flagged `bright`, it
  reads 15.0:1. **That flag is why a photograph never has to be composed around the type.**
  All five now measure 10.6 / 11.2 / 19.4 / 20.7 / 15.0.

Configs: `page-faq-image-layout.json` (layout + CSS), `faq-category-images.json` (the three
new briefs), `faq-category-images-publish.json` (the first five, with handles and reasoning),
`faq-skincare-no-black-band.json` (the re-shoot brief), `faq-revisions-publish.json` (the two
replacements).

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
Those beat cropping the product out of a pack shot on every count.

⚠️ **Corrected 2026-08-21:** this section previously claimed Acetyl Hexapeptide-8's render
was the superseded ARGIRELINE design, and that claim kept the product out of the rollout
for two days. It is wrong. Its built reference reads
`ACETYL HEXAPEPTIDE-8 / ANTI-WRINKLE SERUM / 10% ACETYL HEXAPEPTIDE-8 | 30ML` — current
2026 artwork. It ran cleanly on 2026-08-21 (177/177, $4.90) and is published. **Open the
reference before believing a note about it.**

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

### ✅ BRAND-001 — Homepage rebuilt against a five-brand premium benchmark

**Priority:** 🟢 Done (2026-08-21) — follow-ups below
**Owner:** Claude (research, generation, publishing) + Malcolm (all image selection)
**Docs:** `docs/visual-identity/01-benchmark-research.md`, `02-inventory-and-gaps.md`,
`03-art-direction-and-briefs.md`

**What prompted it.** Malcolm: every image on the site is a placeholder. A live capture of
Augustinus Bader, Dr. Barbara Sturm, La Mer, La Prairie and Tatcha, compared against a full
audit of the theme's 239 image slots, found the store was *not* missing images — 236 of 239
slots were filled and every file returned HTTP 200. The faults were art direction and
architecture:

1. The hero and all four concern tiles were botanical flat-lays — leaves, flowers, citrus —
   on a brand selling synthesised peptides. The pictures argued against the proposition.
2. **Zero full-width bands.** The page ran white → grey → white to the footer. Bader runs
   five as chapter breaks. This was the largest single gap.
3. 76 files covered 236 slots; three `philosophy-*` images carried 18 slots between them.

**Direction adopted — "clinical luminism":** one subject, hard light, a ground the brand
owns, 40% of frame reserved for type, no botanicals. Palette and per-concern colours reuse
the agreed product-photography scene colours so banners and packshots are one system. The
**peptide chain** is now the brand's signature device, after Malcolm set the positioning as
"the leading peptide skincare brand".

**Live on the homepage:**

| Section | State |
| ------- | ----- |
| Hero | 3-slide slideshow — model → laboratory glass → Matrixyl bottle, left-aligned type |
| Targeted Solutions ×4 | Human register, each on its ingredient's colour |
| The Science of Peptides | Peptide-chain macro (replaced a cyan stock lab shot) |
| **The Peptide Standard** | **NEW** full-bleed band, peptide helix render |
| Customer reviews | **NEW** 6-slide slider, Tatcha layout, prev/next arrows, per-slide product link |
| Find Your Product ×4 | Material register, matched colours |
| **Brand band** | **NEW** full-width closer above the footer |

Also fixed site-wide: four- and five-item link-block rows now fill the full row (the theme
sizes by items-per-row, so a 4-block row at `large` left a 274px dead column). Applied via a
`custom-html` section in `footer-group`, so it also corrected `page.ingredients` untouched.

⚠️ **That same footer-group section put dead carousel arrows on six other pages for four
days** — fixed 2026-08-25, `configs/banners/fix-stray-slider-arrows.json`. The reviews
slider is built in two halves that have to agree on one number, and they did not: the CSS
turns a `media-with-text` into a horizontal scroller only at
`:has(> .media-with-text__item:nth-child(6))`, while the arrow-injection JS guarded on
`items.length < 2`. **JS said 2, CSS said 6.** So every `media-with-text` with two or more
blocks got arrows — and because those sections were never converted to scrollers,
`scrollBy({left: …})` had nothing to scroll. The always-visible rule then pinned them on
permanently, advertising an interaction that could not happen. Six pages carried them, found
by scanning all 57 templates: `key_findings` on **copper-peptide, matrixyl, argireline,
pdrn and glutathione research**, plus `science_story` on **philosophy** — every one a
3-block section. Malcolm spotted it on copper-peptide-research. The JS threshold is now 6,
with a comment tying it to the CSS rule. Verified live on five pages: 0 arrows on the
3-block sections, 2 on the genuine 6-block sliders, and the homepage reviews slider still
advances a full panel (scrollLeft 0 → 1392).

⚠️⚠️ **Reconciling the two halves at six was still wrong, and the same day it hid five
whole pages** — fixed 2026-08-25 16:45,
`configs/banners/solution-pages-remove-content-carousel.json`. Malcolm: "for all of the
solution pages: remove the carousel function from the content blocks, so that the content
blocks are all shown on the page." A block count is a *proxy* for the reviews slider, not a
description of it, and six sections on this store have six or more `media-with-text` blocks.
One is the reviews slider. The other five are the `content` sections of the **Skin
Solutions** pages — brightening-glow, collagen-skin-plumping, fine-lines-wrinkles,
firming-skin-density, skin-repair-renewal — each carrying six editorial blocks (intro,
causes, approach, three products). All five were long-form reading collapsed to **one
visible block with the other five behind a horizontal scroll**: measured on
fine-lines-wrinkles, `scrollWidth` 8184 against `clientWidth` 1344.

Both halves now ask the same question, and it is not a count: **does this section contain
the "See All Customer Reviews" link**, `a[href$="/pages/reviews"]` — the one thing actually
unique to the reviews slider. `$=` rather than `=` so a Langify locale prefix
(`/de/pages/reviews`) still matches. Checked against all 57 live templates: 22
`media-with-text` sections exist and that link is in exactly one. Section ids were not an
option — they render as `shopify-section-template--<theme id>__<key>` and go stale — and
`custom-html` rejects Liquid, so section content is the only stable discriminator available
from a sitewide style block. Verified live on all five pages: `grid-auto-flow: row`,
`overflow-x: hidden`, no horizontal scroll, 0 arrows, all six blocks stacked and alternating
(page heights 4308–4732px). Homepage reviews slider unchanged: 6 items, column flow,
scrollWidth 8304, 2 arrows. Research and philosophy pages unaffected.

**Lesson: a homepage that looks right hides a site-wide fault.** The reviews section has
exactly six items, so the drifted threshold was invisible exactly where the feature was
built and tested. Anything injected from `footer-group` runs on **every page** — check what
else its selector matches before shipping.

**Lesson: scope by what the thing IS, not by a number that happens to match it.** Two bugs
in two days came out of one count. The first fix made the count consistent; only the second
replaced it with a selector that describes the target. When a sitewide rule needs to hit one
section, find the markup unique to that section — a count will always eventually collide.

🩹 **Capture artefact, not a bug — do not report it as one.** In a full-section Playwright
screenshot the third Key Findings block renders as a blank white card. It is fine: the theme
uses `reveal-on-scroll`, and an *element* screenshot captures content that is still below the
viewport at `opacity: 0`. Scrolled into view it reads `opacity: 1` with all its text. It
looked like a broken block twice.

**Follow-ups**

1. 🔴 **Review copy is invented.** Six names/quotes, five stars, on a store with no orders —
   now the most prominent section on the page. Malcolm to supply real reviews before launch.
2. 🟡 **P3 microscopy image** chosen by Malcolm and not yet placed — intended for the five
   research-page banners, two of which still borrow another page's image.
3. 🟡 **Before/after images** — two files carry the results claim across ~30 slots,
   provenance unconfirmed.
4. 🟡 **Press logos** — Vogue/Forbes/Elle/Bazaar/Cosmopolitan under "featured in".
5. 🟢 Remaining pages unstyled: collections, products, concern pages, research pages.

**Removed this session:** a section headed "Hear From Our Customers" on the fallback product
template, holding three invented video testimonials that all pointed at a **Hairgenetix
hair-growth advert**. See `memory/fabricated-social-proof-on-the-store.md`.

**Tooling added:** `scripts/audit-theme-images.py`, `image-slot-inventory.py`,
`generate-banners.py`, `upload-theme-images.py`, `patch-template.py`,
`banner-contact-sheet.py`. Every theme push backs up the template first and prints its own
`--restore` command.

### 🔄 BRAND-004 — Skin-art banner library + collection banners

**Priority:** 🟡 Library generated (2026-08-24); selection and placement ongoing
**Owner:** Claude (briefs, generation, placement) + Malcolm (every image choice)
**Tooling:** `scripts/build-banner-library-config.py`, `scripts/generate-multi.py`

**What it is.** A reusable library of skin-art banner frames — one wave per product, eleven
poses, four suppliers — so a banner's text can sit wherever a given frame leaves room.
**402 images across nine products, ~$25.**

Poses vary body position, gaze direction and product placement (left / centre / right
thirds), and include body-and-face, face-macro and eye-macro registers. Product position is
stated as a **measured fraction of frame width**, after a body-part anchor ("against her
jaw") put the bottle over the headline in four of five suppliers.

**Per-product state**

| Product | Images | State |
| ------- | ------ | ----- |
| Copper Peptide Serum | 57 | ⚠️ pre-fix — milky liquid behind blue glass |
| PDRN Serum | 44 | ⚠️ pre-fix — milky behind pink glass |
| Glutathione Serum | 44 | ✅ regenerated, clear liquid |
| Matrixyl Serum | 44 | ✅ regenerated, clear liquid |
| Acetyl Serum | 38 | ✅ (Seedream refused 6) |
| Day Cream | 44 | ✅ |
| Night Cream | 44 | ✅ + helix fix |
| Matrixyl Cream | 44 | ✅ + helix + spell-out |
| PDRN Cream | 43 | ❌ **`PORN` on most frames** — two regenerations failed |

Superseded batches kept in `assets/ai-generated/_superseded/`, not deleted.

**Four brief faults found and fixed, all one root cause** — the brief *named* a thing
without *describing* it, so each supplier filled the gap:

| Fault | Brief said | Fix |
| ----- | ---------- | --- |
| Garbled small print | "too small to read" | outside the depth of field |
| Milky serum | glass colour only | the colour is the glass, not the contents |
| Ribbon helix | "DNA-helix mark" | dots and dashes, never a solid ribbon |
| `PORN` label | "PDRN" | spelled P, D, R, N |

The last one **still fails on the PDRN cream**, whose jar sets the label large enough to be
drawn as a word rather than blurred. It was tolerated earlier on the cartons because it was
sub-legible there — a tolerance that did not survive a change of product format.

**Banners live** — audited against the live store 2026-08-25 08:40 by reading every
collection's and page's `templateSuffix` and then the banner image inside each template.
Read from the store, not from any earlier note in this file.

**Collections — 7 of 14 carry a banner**

| Collection | Image |
| ---------- | ----- |
| `/collections/all` | four-product range shot, extended left |
| `/collections/pdrn` | PDRN cream `B` pose, extended left |
| `/collections/copper-peptide` | day cream frame, extended left, arm sheared |
| `/collections/serums` | peptide face serums, extended right |
| `/collections/creams-moisturizers` | copper peptide night cream |
| `/collections/acetyl-hexapeptide-8` | acetyl serum, round-2 frame |
| `/collections/fine-lines-wrinkles` | acetyl serum `J-body-and-face-right` nbp_flash, **extended right** |

Still bare: `frontpage`, `glutathione`, `matrixyl-3000`, `firming-skin-density`,
`skin-repair-renewal`, `brightening-glow`, `microneedling`.

**Pages — 15 of 18 carry a banner**, including `skin-concerns`, `fine-lines-wrinkles`,
`firming-skin-density`, `skin-repair-renewal`, `brightening-glow`, `the-science`,
`ingredients`, `our-philosophy`, `reviews` and the three research pages. Bare: `contact`,
`faq`, `shipping-returns`.

**Note the split:** `firming-skin-density`, `skin-repair-renewal` and `brightening-glow`
have a banner on the **page** but not on the **collection** of the same handle. Both URLs
exist and both are reachable from the menus.

**Changed after that audit, 2026-08-25 (this session):**

| Page | Change |
| ---- | ------ |
| `/pages/the-science` | header replaced with the blue-glassware microscope frame; **the "Our Transparency Commitment" section converted from a grey `rich-text` panel into a full-bleed `image-with-text-overlay` band** on the evidence+microscope frame. Copy moved across byte-for-byte |
| `/pages/ingredients` | header replaced twice — first with the three-serum range shot, then with the laboratory-glassware frame Malcolm picked. Both files remain on the CDN; reverting is a repoint of `banner.image` + `banner.mobile_image` |

All four carry `object-position: right center` and a measured text max-width via a **`liquid`
block inside the section** (`{{ section.id }}` resolved at render time) rather than a
`custom-html` style block — see the brightening-glow fault below.

⚠️ **`/pages/brightening-glow` has a dead style block.** Its `hero_image_position`
`custom-html` targets `#shopify-section-template--26438110871937__hero`; the live section is
`template--26327016702337__hero`. **Zero matches**, so its image sits centre-cropped instead
of pinned left, and nothing errors. Fix with the same `liquid`-block pattern.

**An earlier revision of this table claimed Matrixyl and Glutathione were live. They are
not,** and still are not. Both sat on the *shared* `templates/collection.json` before the
per-collection templates of ADR-005 existed, and that shared template now carries banner
*settings* (parallax off, `sm`, overlay 25) with **no image**. The Glutathione assets are
built and waiting in `assets/publish-ready/collection-glutathione-banner/`.

**Two pages are still wearing borrowed images:** `/pages/pdrn-research` shows
`skingenetix-philosophy-research.jpg` and `/pages/glutathione-research` shows
`skingenetix-philosophy-ingredients.jpg` — both lifted from the philosophy page.

**`/pages/skin-concerns` is the first banner that is not a product shot,** and the first
where canvas extension does not apply. Measured on the frame, the body's edge *rises* as it
travels left (skin starts y=259 at x=0 but y=295 at x=100), so extending would march the
shoulder into the top-left the heading needs; the right edge is the head. The crop is
anchored with `object-position: center top` instead, so the 28%–46% of height a fixed 440px
band discards always comes off the lower chest. Overlay went 60 → 22. Full reasoning in
`configs/banners/page-skin-concerns-banner.json`.

**The four concern sections on `/pages/skin-concerns` now share the homepage's tiles**
(2026-08-25 13:45). They were the worst placeholders found on the store so far: Fine Lines
carried an **oil-painting landscape of a cottage and a country lane**, and Firming carried a
**screenshot of a text prompt** with the words "Minimalist still life… No text.
Photorealistic." visibly set in type. Repair had a stock DNA helix, Brightening a stock
bubble macro. All four were 800×600 or 1024×1024.

Malcolm chose the **model/skin set** — the same four files the homepage `skin_concerns`
section (`image-link-blocks`, "Targeted Solutions for Every Skin") already uses, rather than
the abstract texture set from the homepage's `find_serum` section. The blocks map 1:1
(`c1`–`c4`, same four `link_url`s), so the plan is four `image_assignments` and nothing
else. Files are **referenced by `shopify://shop_images/` handle, never re-uploaded** —
shopify.md rule 7 — which also carries their existing descriptive alt text across
unchanged. Plan: `configs/banners/page-skin-concerns-tiles.json`.

One cosmetic consequence: the fine-lines photograph has a near-white backdrop and
`concern_1`'s section background is `#ffffff`, so that one tile's left edge dissolves into
the page where the other three sit on a visible block of colour. On the homepage the same
file is fine because it wears a 40% dark overlay.

**The four tiles now carry a 20% wash that lifts to 0 on hover** (live 14:0x,
`configs/banners/page-skin-concerns-tile-overlay.json`). It is CSS, not a setting: the
homepage tiles are `image-link-blocks`, whose overlay exists because link text sits ON the
picture; these are `multiple-images-with-text`, whose schema has no overlay at all. Drawn
through the additive `custom-html` pattern this template already uses for
`banner_crop_anchor`. Remove with `remove_sections: ["concern_overlay_css"]`.

**Why 20% and not the homepage's 40%.** At 40% the photographs go grey and "Brightening &
Glow" reads muddiest of the four — the one tile whose whole promise is radiance. Judged on
a ladder at 0/12/20/28/40% composited locally against the real captured page, which is
faithful because the browser's own 40% was measured landing on `0.6*src + 0.4*26` to within
1/255. 12% barely marks the photograph though it does grey the near-white fine-lines
backdrop; 28% starts going grey. The homepage keeps 40% because white link text must stay
legible on its tiles; nothing sits on these.

**The hover reveal is what earns the overlay its place** — it turns a wash into an
affordance. These images are *not* links (the anchor is the button beside the picture), so
the reveal is invitation rather than navigation, and touch devices lose nothing: they keep
the tint. `:has(> img:hover)` rather than a bare `:hover` because **the list element is
524px against the image's 500px** (measured live), so a bare `:hover` would fire from the
empty margin beside the picture. Guarded by `@media (hover: hover)`, with an
`@supports not selector(:has(*))` fallback and a `prefers-reduced-motion` cut to 1ms.
**Verified in a real browser on all four tiles: 0.2 at rest → 0 on hover → 0.2 on exit.**

⚠️ **The first push of that overlay changed nothing at all, and looked completely correct
while doing so.** Two independent faults, either of which alone is silent — the theme
places the picture in grid column 2 (`grid-area: 1 / 2 / -1`) with a selector that outscores
an added one, and gives it `will-change: transform`, which paints it above any
non-positioned `::after`. The served HTML carried the CSS verbatim the whole time, so
reading it back "confirmed" a fix that did not exist. **A full-page pixel diff before and
after is the only check that catches this**; it showed zero changed rows outside the
announcement bar.

**The homepage concern tiles went 40% → 20% to match** (live 2026-08-25,
`configs/banners/homepage-concern-tile-overlay-20.json`). Unlike the concern page this is a
real block setting — `image-link-blocks` has `overlay_opacity` in its schema. The *second*
`image-link-blocks` section on the homepage, `find_serum` ("Find Your Perfect Product",
four tiles at 50%), is deliberately untouched, which is why the CSS below is keyed to the
`skin_concerns` section id rather than the section class.

**These tiles carry their white label ON the photograph, so 20% alone was not shippable.**
At 20% flat, `Skin Repair & Renewal` and `Firming & Skin Density` sat at 4.12 and 4.14
against the 4.5:1 that 15px bold text requires, and `Fine Lines & Wrinkles` had **no dark
ground left at all** — 100% of its label box was too pale, white on near-white, because
that photograph's backdrop is pale grey exactly where the label sits. Fixed with a **bottom
scrim** layered onto the theme's own `.content-over-media::before` (never an `::after` —
the content div is also `z-index: 1` and later in tree order, so an `::after` paints over
the label). All four now pass: **worst 4.74:1**, top half of every picture still at the
bare 20% wash.

⚠️ **Do not locate a text label by counting bright pixels per row.** The first contrast pass
did, and on photographs of skin the specular highlights clear any threshold — the "label
band" came back as 292 rows, essentially the whole tile, so every number was white text
against the *entire photograph* (it called 40% marginal at 3.89–4.17 and 20% a failure at
2.51–2.72; the true figures are 7.12–7.80 and 4.12–6.44). Worse, it could not detect its own
error: after the scrim the median moved but the 95th percentile did not, because the
brightest 5% lived in the untouched top of the picture. **Take the box from the DOM** — a
`Range` over the text node gives 19px at y=453. Same family as
`a-number-checked-only-against-itself-gets-believed`.

**Three lessons from the 2026-08-25 acetyl banners** (details in
`configs/banners/collection-fine-lines-wrinkles-banner.json`):

- **`scatter()`'s grain can be wildly over-amplitude, and it is not obvious.** It
  high-passes its sample patch with a hardcoded `sigma=25`; on a small or corner patch what
  survives is the backdrop's own vignette falloff rather than grain. On the acetyl `J` frame
  it measured **9.30 against the 0.565 the real backdrop has** — 16x — and shipped as a
  visibly mottled panel butted against smooth dark. **Measure the extension's
  high-frequency std against the source backdrop's before publishing any extension.**
- **`scatter()` builds each output ROW from a single source row,** so a patch narrower than
  a few hundred columns gives row means too noisy to settle and streaks the full width of
  the extension. The patch does not have to come from the edge being grown — only high
  frequencies are carried, so any clean region of the same backdrop will do.
- **Measure the h1 in the browser, do not estimate it.** The collection banner's h1 needs
  681px for one line; a 552px figure taken from a *page* banner was wrong enough to make the
  heading wrap at every width.

**The banner section was the real blocker, not the images.** `templates/collection.json`
had `enable_parallax: true` — the theme's schema says *"Parallax crops images"* — so no
aspect ratio survived, and `overlay_opacity: 50` flattened every picture. Both changed
(parallax off, overlay 25); this improved **all five collection pages** at once. Three
attempts and ~$0.50 were spent reworking the image before the settings were read.

**Open**

1. 🔴 **Glutathione banner is built but not published.** The overlap is fixed — the master
   was rebuilt to 3750px wide with the text anchored right — but the collection still has no
   `templateSuffix`, and `publish-collection-banner-template.py` has no `glutathione` entry
   in `PAGES`. Note the publish plan predates the rebuild and reuses the same filename;
   Shopify Files suffixes rather than replaces, so it needs a fresh name.
2. 🔴 **Five bare collections**, two of which already have a banner on their same-named
   *page*: `firming-skin-density`, `skin-repair-renewal`, plus `matrixyl-3000`,
   `microneedling` and `frontpage`.
   ⚠️ `brightening-glow` was in this list and is **now done** (2026-08-25 09:15) — the
   COLLECTION carries the glutathione `A-face-full-prod-left` nbp_flash frame, extended
   LEFT, distinct from the gpt_image take on the same-named *page*. Its concentration line
   was repaired from `25i` to `2%` first.
3. 🟡 **Two research pages wear philosophy-page images** — `/pages/pdrn-research` and
   `/pages/glutathione-research`. Both products have a full banner library already.
   ⚠️ `/pages/copper-peptide-research` had the same fault in its **body**, not its banner,
   and **block 1 is now fixed** (2026-08-25, `configs/banners/page-copper-peptide-research-key-finding.json`).
   `key_findings.f1` — "Supports the skin's own collagen & renewal pathways" — showed a
   generic unbranded dropper bottle borrowed from the ingredients page. It now carries
   Malcolm's pick `cp-collagen--C-copper-node-network-nbp_flash_02`: a copper node radiating
   through a blue fibre mesh, which actually states the claim in the heading. Uploaded under
   a **new** name (`skingenetix-copper-peptide-ghk-cu-collagen-network-research.jpg`) and the
   slot repointed — `skingenetix-ingredients-copper-peptide-serum.jpg` is untouched and still
   live on `/pages/ingredients` and `/pages/skin-concerns`. Delivered at 800w into a 660px
   box, so no downscale trap.
   **`key_findings.f2` followed the same afternoon** — "Supports skin-renewal cell activity
   (independent lab study)" now carries Malcolm's pick
   `cp-collagen--E-lattice-sparse-to-dense-nbp_pro_01`, uploaded as
   `skingenetix-copper-peptide-collagen-lattice-density-research.jpg`. It replaces
   `skingenetix-philosophy-research.jpg`, which was checked across the live site first and is
   **also on `/pages/our-philosophy`** — its home — so the file was left alone and only this
   page's reference moved. The section alternates `media_position` per block, so f2 renders
   image-right and the lattice's dense end lands nearest the text.
   **`key_findings.f3` is now done too** (2026-08-25, verified live: the page references
   `skingenetix-copper-peptide-ghk-cu-radiant-skin-appearance.jpg` and no longer
   `skingenetix-philosophy-quality.jpg`). Malcolm's pick
   `cpr-sat--C-direct-gaze-clinical-blue-gpt_image_02` — a photograph, deliberately, because
   f3's finding (Miller 2006) is **self-reported satisfaction**, so a woman appraising her own
   skin depicts the actual endpoint where a third mechanism illustration would depict
   something the study never measured. Alt text does not present her as a trial participant.
   **All three blocks on `/pages/copper-peptide-research` are therefore done.**

   ✅ **`/pages/matrixyl-3000-research` — all three Key Findings blocks done, 2026-08-25 16:20**,
   `configs/banners/page-matrixyl-research-key-findings.json`. It had the same borrowing on all
   three: a product shot of the serum on f1, and the two philosophy-page frames on f2 and f3.
   Malcolm chose the **`nbp_flash_01` set** — one engine, one candidate index, all three blocks —
   over a per-block mix, because the three sit stacked on one page and the object language has
   to be identical. The wave (`block-matrixyl-research-medical`, commit `a79f93f`) generated 31
   candidates across 6 suppliers; the alternative offered was `gpt_image_02`, stronger on f1's
   sparse-to-dense mechanism but a softer, painterly render that sits differently against
   nbp_flash's crisp CGI. Set coherence won.
   Uploaded under three new names, none a prefix of another (the uploader binds on
   `filename:<stem>*`): `…-collagen-network-supports-skin-surface`,
   `…-fibroblasts-building-collagen-matrix`, `…-signalling-fibroblast-collagen-synthesis`.
   All three replaced files are untouched and still live at their own homes.
   ⚠️ **Correction to the box geometry recorded on the copper-peptide job:** the media box is
   **not** 1:1 at every width. Measured live here, `key_findings.f1` is **660×764** at 1440 —
   the taller text column stretches the row, so a square master **is** cropped ~7% off each
   side on that block. f2 and f3 are 660×660, and all three are 350×350 at 390. Nothing
   important is lost on f1 (centred subject, pale surround) but the "no square has ever been
   cropped in this section" claim is wrong and should not be inherited again.
   ⚠️ The claim above that `/pages/pdrn-research` shows `skingenetix-philosophy-research.jpg`
   is **stale** — the page returns 200 and no longer references that file. Re-check before
   acting on it.
4. 🟡 **Fold the runtime-injected banner configs into the scripts.** The three banners of
   2026-08-24/25 were built by injecting config into `extend-banner-canvas.py` and
   `publish-collection-banner-template.py` at import time, because a second session was
   committing to both files at the same moment. Every setting is recorded in the three plan
   files; `scatter()`'s `sigma` needs to become configurable before the grain rescale can
   move in cleanly.
5. 🟡 **PDRN cream** — retire, use only small-label poses, or repair chosen frames individually.
6. 🟡 **Copper Peptide + PDRN serums** — re-run with the clear-liquid brief (~$5) so all five match.
7. 🟡 **`image_size: sm` → `md`** would make the band 2.57:1 against the library's native
   2.36:1, removing most of the need to extend images at all. Raised, undecided — and now
   also relevant to the skin-art register, where `md` would cut the discarded height on
   `/pages/skin-concerns` from 28% to roughly 8% at 1440.
8. 🟢 Five frames marked by Malcolm: PDRN serum `B`; the repaired G-pose pair awaiting a
   pick; `SKIN8-reclining-sweep-nbp_pro_02` → `/pages/skin-concerns`;
   `acetyl-hexapeptide-8 I-body-and-face-left-nbp_flash_01` → `/pages/fine-lines-wrinkles`;
   `acetyl-hexapeptide-8 J-body-and-face-right-nbp_flash_01` →
   `/collections/fine-lines-wrinkles`.

### 🔄 BRAND-005 — Ingredients page: real products, two registers, one size

**Priority:** 🟡 Live (2026-08-25); banner still a placeholder
**Owner:** Claude (build) + Malcolm (every image choice)
**Plans:** `configs/banners/page-ingredients-*.json` · **Tool:** `scripts/normalise-tile-scale.py`

`/pages/ingredients` carried nine placeholder products across **18 slots** — each product
appears twice, once as a small selector tile and once in its own detail section. All 18 are
now the real products.

**Two of the placeholders should not have been on a live Skingenetix page at all:** the
Glutathione tile showed a bottle branded **QUINER** — a competitor — and the Copper Peptide
Day Gel-Cream tile read **`SKINGENETIX®`**, a registered mark the brand does not use.

**Two registers, deliberately different** (Malcolm: the rows were "flat" when both used the
same shot):

| Row | Register |
| --- | --- |
| Small selector tiles | product hero on **white**, uniform |
| Large detail sections | product **in use** — pipette lifted with a drop forming, or jar open |

**No new uploads for the already-live heroes.** They are referenced in place as
`shopify://shop_images/<filename>`; copying them would break shopify.md rule 7 (Langify keys
translations off the URL) and create duplicates. The SEO naming rule governs what we
*upload*, not what we *reference*. It also means these tiles now **track the product pages**.

**Product scale is normalised, and the measurement was the hard part.**
`scripts/normalise-tile-scale.py` re-frames each tile so every serum fills 71.0% of frame
(the PDRN bottle) and every jar 47.4% (the Copper Peptide night cream) — both references
chosen by Malcolm. **Nothing is resampled**: only the canvas moves, so the pixels are the
originals. Canvas is grown by **replicating the border**, not filling flat — a median-colour
fill left a visible rectangle on five of nine tiles, because these sweeps are gradients.

⚠️ **The auto-measured boxes were wrong twice and shipped.** Edge energy cannot tell a
bottle from its reflection nor find a white bulb on a white sweep: copper measured 1215→1669
(rendered at 56% of frame) and matrixyl 1825→1539 (rendered at 91%). The *reference itself*
was 4% out. All five serums now carry a `y_override` read off a labelled pixel grid. Full
account in `memory/a-number-checked-only-against-itself-gets-believed.md`.

**Three frames Malcolm has never personally marked** are live on this page — the Copper Day
Gel-Cream white hero, and the two Matrixyl white heroes (serum #3, cream #7) taken from
`2026-08-21/run-01`. None carries his `_` or `__`. Worth his eye.

**Open**

1. 🟡 **The page banner is still a placeholder** — three unbranded generic dropper bottles,
   no Skingenetix product. A banner cannot sensibly be one product hero; the `/collections/all`
   range shot would fit. Malcolm's call.
2. 🟢 Four of eight Matrixyl white-hero candidates in each set were unusable — blocky helix
   marks, a teal lid the cream does not have, and two misspellings (`MATRIXEL`, `MATRIYEL`).
   Recorded so nobody picks off a filename without checking at 100%.

### 🔄 BRAND-003 — Every website image now goes to every supplier

**Priority:** 🟡 Rule and tooling live (2026-08-22); banner library generating
**Owner:** Claude (rule, tooling, briefs) + Malcolm (every image choice)
**Rule:** `.claude/rules/website-imagery.md` · **Runner:** `scripts/generate-multi.py`

**Malcolm's standing instruction, 2026-08-22.** Every image created for the website goes to
**every supplier on its latest and most capable model**, so he compares real alternatives and
chooses. One candidate per supplier is the floor.

**What bought this rule.** The whole homepage banner run went through **Seedream alone** —
`generate-banners.py` hardcodes two Seedream endpoints and has no routing. The product name
MATRIXYL failed in roughly **thirty of fifty candidates** across five rewritten briefs, spelled
letter by letter, every misspelling negated by name. It was treated as a prompting problem for
hours. The same brief sent to **gpt-image rendered it correctly on the first attempt, both
candidates** — then broke PDRN, which Seedream had always rendered correctly.

The final FAQ image needed **three engines**: Seedream for the composition and the only stack
with all jars the same size, gpt-image to fix MATRIXYL, NBP Flash to fix PDRN without breaking
MATRIXYL again. The failure modes do not overlap. The product-photography skill had said so for
months — "running the same brief across 3 backends raises per-variant pass rate from ~50% to
~85%" — and the banner runner ignored it.

**The roster had also drifted.** Checked 2026-08-22: `chatgpt-image-latest` and `gpt-image-1.5`
existed at OpenAI and were wired into nothing; `gemini-3.1-flash-lite-image` was new at Google.
Rule 2 is now to re-list before every production run, because a stale model id **404s silently**
and just returns fewer candidates.

**Judge twice, at different sizes.** A contact sheet cannot judge lettering — `NEAT2_04` looked
flawless tiled and reads `MATPIXYL` at full size. And a correctly-generated `PDRN` arrived on the
live page reading `PORN`, purely because the theme emitted `sizes="350px"` against a srcset
topping out at 700w and the downscale thinned the D. The pixels were right; the delivery was
wrong. Fixed at runtime by dropping srcset/sizes and requesting an explicit CDN width.

**Live on the homepage**

| Section | State |
| ------- | ----- |
| FAQ | Title centred above, questions 46% left, image right, support line full-width below, no card |
| FAQ image | Four-jar stack — **every quoted line correct** at full size and at render size |
| Philosophy band | Skin-art reclining profile, face in view, 720px tall |

**In progress**

- 🟡 **Banner library** — 9 products × 11 poses × 4 suppliers = 396 images, ~$22.
  Poses vary body position, gaze direction and product placement (left / centre / right thirds)
  so a banner's text can sit wherever the frame leaves room. Includes body-and-face and
  face-macro registers, plus an eye macro. **`H-eye-macro` produces collages** in two of three
  suppliers — a visible vertical seam splitting product and eye into panels — despite `collage`
  and `multi-panel` being negated.
- 🟢 Band copy is still a Claude draft; Malcolm to write it.

**Supplier facts measured across this session**

| Supplier | Finding |
| -------- | ------- |
| Seedream | Best label fidelity. **Refuses bare-skin subjects every time.** |
| gpt-image | Solved MATRIXYL first attempt. Refuses most bare-skin briefs. |
| NBP Flash | Cheapest at $0.02 and produced the clean FAQ stack and the chosen band |
| NBP Pro | 6× Flash, weaker labels, tilts the product |
| Luma | Best colour, but **invented an `XXX` mark on class A** — barred alongside FLUX.2 |
| FLUX.2 | Barred from class A: substitutes fictional brands |

Content filters refuse bare-skin briefs on Seedream, gpt-image and FLUX.2. Establishing clothing
in the opening sentence cut refusals from 13/36 to 1/48 — but naming a garment also changes the
picture, so it is not a free fix.

### 🔄 BRAND-002 — Homepage FAQ and brand band restructured on stock sections

**Priority:** 🟡 Layout live (2026-08-21); two images outstanding
**Owner:** Claude (audit, layout, briefs, publishing) + Malcolm (both image choices)

**What prompted it.** Malcolm: the FAQ takes up a lot of space — is there a setup with the
questions on the left and an image on the right? And make the bottom brand band work the way
tatcha.com's does. He then set the constraint explicitly: **use standard Shopify theme
sections and content modules wherever possible before writing our own.**

**What the theme already had.** The stock **FAQ** section has a `text_position` setting
(Left / Centre / Right). It was on **Centre**, the one value that stacks everything full width
down the middle — which is why the section ran ~1000px tall with empty margins either side.
Left or Right switches the same section to the theme's own `section-stack--horizontal`
two-column layout at ≥1150px. No new section, no custom code.

The heading, though, always renders **inside** one of those two columns. Malcolm wanted it
centred above both. Two routes were built and compared:

| Route | Result | Cost |
| ----- | ------ | ---- |
| Stock **Rich text** section above the FAQ | Works, but leaves a visible seam — `section-spacing-collapsing` **deliberately disables** collapsing for boxed sections above 700px, so two adjacent white cards cannot merge | zero code |
| Re-flow the FAQ's own `section-stack` as a 2-col grid, heading spanning row 1 | One card, title centred above, questions left, image right | 8 lines CSS |

Malcolm chose the second. Section height ~1000px → ~530px.

**Tatcha's band, established from their live markup** — not inferred. It is the same theme
family: a full-bleed image with the text in a **translucent white card, `max-width: 520px`,
`padding: 1rem`, `background: rgb(255 255 255 / 0.8)`**, holding one short serif sentence and
a solid filled button. No eyebrow, no body paragraph.

Our `image-with-text-overlay` reproduces all of that from **native settings** — content
position, heading size, button style, overlay opacity — **except the white card**. Our Impact
build exposes no content-background setting; the `slideshow` block's `background` setting is
the loading backdrop behind the image, not a panel behind the text (its own help text says so).
Tatcha runs a newer theme version that exposes it. Malcolm chose the **all-stock** version:
centred, X-Small heading, filled button, no panel — and made the band taller via the native
Image size setting (`md` 560px → `lg` 720px).

**Live on the homepage:**

| Section | State |
| ------- | ----- |
| FAQ | Title centred above, 9 questions left, image right, one card |
| Brand band | 720px tall, centred, X-Small heading, filled white button, eyebrow and body copy blanked |

**Outstanding**

1. 🟡 **New FAQ image** — the slot currently holds `skingenetix-peptide-chain-science-2026.jpg`
   as an explicit placeholder; it is already in use in "The Science of Peptides" higher up the
   same page. Four registers generated for Malcolm to choose from.
2. 🟡 **New brand band image** — the current one puts the model on the right with its clear
   space on the left, which is now the wrong side: the text is centred. Three briefs generated,
   all holding the **central 45%** of the frame quiet.
3. 🟢 Band copy is a first draft (`"Skingenetix began with a simple refusal: no proprietary
   blends."`) — Malcolm to improve.

**Notes for the next session.** The FAQ CSS is scoped by `:has(.faq-availability img)` rather
than by section id — ids are template-scoped and change, and the FAQ *page* has no avatar image
so it is untouched. The `!important` on the image width is required: the section's own
`team_avatar_width` range writes an inline `max-width` capped at 350px.

### ✅ PHOTO-005 — 2026 imagery live on every product that has artwork

**Priority:** 🟢 Done (2026-08-21) — follow-ups below
**Owner:** Claude (generation + upload) + Malcolm (selection, SEO study)
**Status:** **9 of 11 store products carry 2026 imagery — 86 images live.** Two days
earlier it was 8. Roughly $95 of generation across 2026-08-20/21.

| Product                       | Live   | Store page                                     |
| ----------------------------- | ------ | ---------------------------------------------- |
| PDRN + Collagen Night Cream   | **8**  | `pdrn-collagen-night-cream`                    |
| Glutathione Brightening Serum | **8**  | `glutathione-brightening-serum`                |
| Copper Peptide Night Cream    | **8**  | `copper-peptide-ghk-cu-night-cream`            |
| Copper Peptide Day Gel-Cream  | **9**  | `copper-peptide-ghk-cu-day-gel-cream`          |
| Copper Peptide Renewal Serum  | **13** | `copper-peptide-ghk-cu-renewal-serum`          |
| Matrixyl 3000 Serum           | **10** | `matrixyl-3000-hyaluronic-acid-collagen-serum` |
| Matrixyl 3000 Firming Cream   | **9**  | `matrixyl-3000-pro-collagen-firming-cream`     |
| Acetyl Hexapeptide-8 Serum    | **12** | `acetyl-hexapeptide-8-anti-wrinkle-serum`      |
| PDRN Renewal Serum            | **10** | `pdrn-renewal-serum`                           |

**Not done — the two microneedling stamp sets.** No 2026 photography artwork exists for
them, and both currently show **Hairgenetix** packaging with a registered ® mark on a
Skingenetix page. That needs artwork, not generation. It is the last wrong imagery on the
store.

**Selection is Malcolm's, by leading underscore** — `_` keeps, `__` publishes. He now marks
in two places: the `ALL-<product>` browse folders and the fan-out's own run output folder.
Both are handled; `prepare-marked-run-output.py` reads the second and recovers each image's
engine from the run manifest.

**Colour is per-product data now.** Each config carries `formulation` (what the substance
looks like, and what it never looks like) and `palette` (scene colours from the product's
own brand colour). `fanout.py` **refuses to run** a product that declares neither. Values in
`memory/product-colours-2026-08.md`.
⚠️ **Copper Peptide DAY is the DARK cream, NIGHT is the LIGHT one** — reads backwards
against the usual convention and was written inverted once.

**Follow-ups, none blocking:**

1. **Four Gemini top-ups** waiting on a daily-cap reset — Acetyl (ran on four engines only)
   plus the three Copper Peptide products. Each is `--backends nbp_pro,nbp_flash` into the
   existing `run-01`; filenames carry the engine so they merge cleanly.
   ⚠️ Generation reads `GEMINI_API_KEY` only and this project's `.env` has no Gemini key —
   see the Authentication note in `docs/architecture.md`.
2. **Two theme-level SEO items**, both needing approval because they touch Liquid:
   `decoding="async"` is absent on all 40 images, and JSON-LD `Product.image` carries only
   the featured image rather than the gallery.
3. **Two dieline faults before print** — the Matrixyl and Acetyl serum cartons both read
   `50ML` where their bottles read `30ML`. See `memory/artwork-faults-found-2026-08.md`.
4. **Product renaming** stays blocked until the SEO/GEO/AISO keyword study.

**Alt text: done for all 66 live images** (at the time of the pass), house format
`Skingenetix <Product>, <active>, <size> - <what is in frame>`, capped at 125 chars and
written from looking at each image. Re-runnable and idempotent via
`scripts/finals/set-product-alt-text.py`, which reports any undescribed image.

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

### 🔄 BRAND-006 — /pages/faq category blocks carry a picture (PLACEHOLDERS LIVE)

**Priority:** 🟡 Layout done and live 2026-08-25; real photography not chosen
**Owner:** Claude (layout) + Malcolm (every image choice)
**Plans:** `configs/banners/page-faq-image-layout.json`, `configs/banners/page-faq-placeholders.json`

Malcolm, 2026-08-25: *"where the faq block title is — lets make this block an image with
the title on top. So image and title left and faq right. use placeholder images for now."*

**The two-column layout needed nothing.** `accordion-content` already defaults to
`text_position: start`, which gives `.section-stack--horizontal` with a 50%
`.section-stack__intro` left and `.section-stack__main` right. Measured at 1440: intro
x=48 w=636, main x=756 w=636. The left column was a title floating in 636px of empty
space. This fills it.

**The picture had to be injected.** `accordion-content` has **no image setting anywhere in
its schema**, and its `content` field is a richtext whose Shopify sanitiser strips `<img>`.
So a page-scoped `custom-html` section injects a real `<img>` at runtime — chosen over a
three-line CSS `background-image` because these are content images on a live store and a
background throws away alt text, native lazy-loading and the srcset. Keyed on the section
id **suffix** (`faq_products`), never the full id, which carries a template-scoped prefix
that changes whenever the template is rebuilt.

**A bottom scrim is already in place** for when real photographs replace the flat
placeholders — same reasoning as the homepage tiles earlier the same day: a flat overlay
strong enough for the type greys the whole picture, a bottom gradient buys contrast only
where the type sits.

**Two variants, one class apart.** Shipped with the title **over** the picture. Adding
`.sg-faq-title-above` to a section switches it to title **above**. Both rule sets ship, so
the two can be compared on the live page without another publish.

⚠️ **The five images are PLACEHOLDERS and are live on the store.** Named `-placeholder-`
*and* carrying the word PLACEHOLDER rendered into the picture, so neither can quietly
become permanent. Regenerate with `scripts/make-faq-placeholders.py` (`assets/` is
gitignored, so the script is the reproducible artefact, not the JPEGs).

**Open**

1. 🔴 **Choose real photography for the five categories** — Products & Usage, Ingredients &
   Safety, Orders & Shipping, Returns & Refunds, Skincare & Routine. Then swap the five
   entries in `page-faq-image-layout.json`, re-run, and **delete the placeholders** from
   Shopify Files (search `faq-placeholder`, five files).
2. 🟡 **Decide title-over vs title-above** — currently over.

**Verified live at 1440 and 390:** five images injected, 636×477 desktop serving the 800w
candidate, 350×263 mobile serving 400w, title inside the image bounds at both, no
horizontal page overflow.

⚠️ **A `custom-html` `html` setting cannot contain `{{`, `}}`, `{%` or `%}`** — Shopify
reads them as Liquid and 422s. **JSON is what trips it, not Liquid**: an inlined
`json.dumps(mapping)` ends in two abutting closing braces. `patch-template.py` prints only
`HTTP Error 422: Unprocessable Entity`; the actual message is in the response body it
discards. Emit the map indented and assert on all four tokens before pushing.
