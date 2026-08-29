# Plan — a unique before/after review carousel on every product page

**Status: PLAN, nothing built.** Written 2026-08-29 from Malcolm's brief: put the
`reviews-before-after` carousel on each product page, unique per product, sourced from the
customer review photos in Drive, splitting reviews across products where a solution type has
several. It must be **easy to manage** and **fully translatable**.

Related: `docs/reviews-before-after-carousel.md` (the section as built for `/pages/reviews`),
`docs/clinical-trial-before-after-images.md` (where the photographs came from).

---

## 1. What exists right now

| | |
|---|---|
| Section | `theme/sections/reviews-before-after.liquid` — built 2026-08-27, live on `/pages/reviews` |
| Card carries | before/after pair, name, verified badge, star rating, title, body, product link |
| Carousel | the theme's own `<scroll-carousel>` + `scrollbar` snippet. Nothing external loaded |
| Image contract | **one file, both frames, split at exactly 50%, square (1:1)** |
| Products | **11** — 9 skincare + 2 microneedling stamp sets, all `active` |
| Product templates | **`templates/product.json` only** (+ `product.pre-order.json`). All 11 share one |
| Review photos | **76**, in Drive under `Images/Reviews /` (⚠️ trailing space in the folder name) |

### The photographs are already correct

All 76 are square — 65 at 2048², 11 at 4096² — and spot-checking confirms they are true
diptychs split at 50%, one woman, two occasions. **They already satisfy the section's image
contract exactly.** No cropping, no re-splitting. They are named by customer (`Heather-S.png`)
and filed by concern:

| folder | images |
|---|---|
| `Wrinkles` | 25 |
| `General` | 28 |
| `Firming` | 14 |
| `Brightening` | 9 |

---

## 2. ⚠️ The honesty problem, stated once

**There is no review text anywhere in Drive — only images named after a person.** So every
name, star rating, title and body would be written by us, for a store that has **zero orders**
and has never sold anything. The photographs are AI-generated (they are the output of this
project's own generation runs). Presenting them as named verified customers is fabricated
testimony at scale.

This is not a new problem, it is an existing one getting larger: `docs/todo.md` REVIEW-001
already records *"the review copy is invented… still needs resolving before the store takes
orders"*, six invented quotes are live on the homepage, and the reviews page `trust` section
claims *"All reviews from confirmed customers"*. The store is EUR/EU-facing, where the Omnibus
Directive requires a trader to state how it verifies reviews and prohibits presenting fake
ones as genuine.

**This is Malcolm's call and the plan below proceeds either way** — the build is identical.
What changes is the wording on the card. Three workable positions:

1. **Illustrative, labelled as such.** Drop the name, the star rating and the "Verified
   Customer" badge; label the section something like "Illustrative results" with a line saying
   the photographs are illustrations, not customer submissions. Legally clean, ships today.
2. **Hold the carousel until there are real reviews.** Build it, populate it from Klaviyo
   Reviews once orders exist. Klaviyo is already on the account — see
   `docs/todo.md` REVIEW-001, it needs the `klaviyo_reviews` block installing, not buying.
3. **Ship as written testimony.** What the brief literally asks for, and what carries the
   exposure above.

Nothing below depends on which is chosen; §6 notes the two fields that change.

---

## 3. The architecture decision — metaobjects, not per-product templates

The obvious route is a template per product (`templates/product.<handle>.json` via
`template_suffix`, the ADR-005 pattern used for collection banners), each carrying its own
blocks. **It is the wrong choice here, on both of Malcolm's stated criteria.**

| | per-product templates | **metaobjects (recommended)** |
|---|---|---|
| Templates to maintain | **11** | **1** — the existing `product.json` |
| Where a review lives | a block inside one template | one entry in Content → Metaobjects |
| Managing it | open the theme customiser, find the product's template, find the block | edit the entry; it is a searchable list |
| Reusing a review | copy it into a second template by hand | reference it from a second product |
| Translation unit | ~460 hash-keyed template settings | **76 metaobject entries, translated once each** |
| Editing English | invalidates that key's translation (`:hash`) | same, but on 1 field not 11 copies |
| Adding a 12th product | write a 12th template | set one metafield |

**The store already does this.** There are three metaobject definitions live —
`how_to_step`, `faq_item` and a minimal `before_after` — and products already carry
`custom.faq_items` and `custom.how_to_steps` as `list.metaobject_reference`. Product content
resolved through a metaobject list is **the established pattern on this store**, not a new
idea. Following it is Rule 12: extend what exists.

It also means **one section instance on the shared template**, resolving its content from the
product it is rendering. That is what makes each carousel unique without 11 of anything.

### Translation

Metaobject entries are a first-class translatable resource in **Translate & Adapt** (ADR-002a
— Translate & Adapt, *not* Langify, whatever older docs say). Each entry's `title`, `body`,
`author`, `before_label` and `after_label` translate once and apply everywhere the entry is
referenced. Nine locales are planned; only `en` is published.

⚠️ Settle the English wording **before** translating: the translation key carries a hash of the
value, so editing the English silently orphans that string's translations.

---

## 4. The data model

**New metaobject definition `customer_review`** — the existing `before_after` definition
(`image`, `label`, `caption`) is too thin and is used elsewhere; leave it alone.

| field | type | translatable | notes |
|---|---|---|---|
| `image` | `file_reference` | — | the 1:1 diptych, split at 50% |
| `author` | `single_line_text_field` | ✅ | omit under §2 option 1 |
| `rating` | `number_integer` | — | 1–5; omit under option 1 |
| `title` | `single_line_text_field` | ✅ | review headline |
| `body` | `multi_line_text_field` | ✅ | review text |
| `before_label` | `single_line_text_field` | ✅ | default "Before" |
| `after_label` | `single_line_text_field` | ✅ | e.g. "After 8 weeks" |
| `verified` | `boolean` | — | omit under option 1 |
| `concern` | `single_line_text_field` | — | wrinkles / firming / brightening / general — for filtering and audit |

**New product metafield** `custom.customer_reviews`, type `list.metaobject_reference`
(→ `customer_review`). Exactly mirrors `custom.faq_items`.

---

## 5. Allocation — 76 photographs across 11 products, none reused

⚠️ **Products sit in more than one solution collection**, so "split the reviews by solution
type" is not a clean partition and cannot be automated blindly:

- `copper-peptide-ghk-cu-renewal-serum` is in **fine-lines-wrinkles, firming-skin-density and
  skin-repair-renewal**
- `matrixyl-3000-firming-serum` is in fine-lines-wrinkles **and** firming-skin-density
- `copper-peptide-ghk-cu-day-gel-cream` is in fine-lines-wrinkles **and** brightening-glow

Each product is therefore assigned **one primary pool**, and every photograph is used **once
and only once** — a review shown against two products is the same customer reviewing two
things, which reads as invented the moment anyone notices.

| product | pool | count |
|---|---|---|
| `acetyl-hexapeptide-8-anti-wrinkle-serum` | Wrinkles | 9 |
| `matrixyl-3000-firming-serum` | Wrinkles | 8 |
| `copper-peptide-ghk-cu-renewal-serum` | Wrinkles | 8 |
| `matrixyl-3000-pro-collagen-firming-cream` | Firming | 7 |
| `copper-peptide-ghk-cu-night-cream` | Firming | 7 |
| `glutathione-brightening-serum` | Brightening | 5 |
| `copper-peptide-ghk-cu-day-gel-cream` | Brightening | 4 |
| `pdrn-renewal-serum` | General | 7 |
| `pdrn-collagen-night-cream` | General | 7 |
| `pdrn-microneedling-facial-stamp-set-1-month` | General | 7 |
| `copper-peptide-ghk-cu-microneedling-facial-stamp-set-1-month` | General | 7 |
| | **total** | **76** |

Pools balance exactly: Wrinkles 9+8+8=25, Firming 7+7=14, Brightening 5+4=9, General 7×4=28.

---

## 6. The section

New file `theme/sections/product-reviews-before-after.liquid`, added alongside the theme's own
sections so an Impact update cannot overwrite it. **No core Liquid modified.**

It is the existing `reviews-before-after.liquid` with one change: instead of iterating
`section.blocks`, it iterates `product.metafields.custom.customer_reviews.value`. Everything
else is reused verbatim — the card, the `<scroll-carousel>`, the `scrollbar` snippet with its
`peer-not-scrollable:hidden` controls, the theme's `rating-star` icon, the breakpoints, the
edge prev/next buttons, and the `margin-inline-end` fix for the product-link prefix.

Carried over from the existing build, each bought with a round:

- **No text baked into the pixels, ever.** Labels are fields so Translate & Adapt can reach
  them. The reference images this project works from have "Before / After 3 treatments" burnt
  in; ours must not.
- **No block-count tests.** Two production bugs on this store came from scoping on a count.
  The scrollbar hides itself when the track does not overflow.
- **`align-items: stretch`** so card heights equalise, the opposite of what
  `research-before-after` needs.

Under §2 option 1 the section simply renders no author, no stars and no badge — the same
honest-empty-card behaviour the reviews page already has for its twelve unfilled slots.

**Placement:** appended to `templates/product.json` after the product information section and
before `related-products`. One section, all 11 products.

---

## 7. Images → Shopify

76 files through `scripts/upload-theme-images.py`, which enforces the two standing rules.

- **SEO filenames**, brand first: `skingenetix-review-before-after-<concern>-<name>.jpg`.
- **Web-ready means the format too.** The uploader shipped a PNG once and handed back a handle
  pointing at it — 35× the bytes for non-WebP clients. These are PNGs; they must land as JPEG.
- **Do not pre-compress.** Measured on this store: a 41% smaller upload delivered *more* bytes,
  because Shopify's CDN transcodes to WebP and JPEG artefacts cost bits to reproduce. Cap the
  long edge at 3000, strip EXIF, quality 95.
- ⚠️ **Uploads are suffixed, not replaced.** Re-uploading a name keeps serving the old image —
  this has bitten the project three times. A rename is a new file.

---

## 8. Build order

1. Create the `customer_review` metaobject definition and the `custom.customer_reviews` product
   metafield (GraphQL Admin API).
2. Upload the 76 images; record handle ↔ filename.
3. **Malcolm decides §2**, and supplies or approves the review copy.
4. Create 76 metaobject entries; attach each product's list in the §5 allocation.
5. Write and deploy `product-reviews-before-after.liquid`.
6. Add the section to `templates/product.json` (backup + `--restore` line, as every publisher
   here does).
7. Verify live at 1440 and 390 on **every** product: card count, media ratio 1.000, labels
   inside the image rect, thumbnails and links, `scrollWidth > clientWidth`. Measure the DOM —
   `innerText` lies on this theme and has produced three false readings.
8. Update `docs/architecture.md` + `docs/todo.md`, commit, push.

**Steps 1, 2, 5, 6 are unblocked now. Steps 3 and 4 need Malcolm.**

---

## 9. Open questions

1. **§2 — what do the cards claim?** The only real blocker.
2. **Review copy.** 76 titles and bodies. Malcolm writes them, or approves generated ones —
   which, given the store has no orders, is the same decision as question 1.
3. **`after_label` durations.** "After 8 weeks" is a claim about a timeframe. The research on
   these pages runs 4–12 weeks; a label should not outrun it.
4. **Do the two microneedling stamp sets get face reviews at all?** They are a device, not a
   cream, and the `General` photographs illustrate skin change rather than device use.
