# Plan — a unique before/after review carousel on every product page

**Status: BUILT AND LIVE, 2026-08-29, with placeholder copy.** Malcolm: *"use placeholder
texts for now, I will give you the texts next."* All 11 product pages now carry their own
carousel. §10 records what shipped and what is still open.

Originally written as a plan; kept as written so the reasoning survives. Written 2026-08-29 from Malcolm's brief: put the
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

## 2. ✅ RESOLVED 2026-08-30 — the cards carry real customers

**Malcolm, 2026-08-30, asked directly: _"the before and after reviews are from real verified
customers"_.** That closes this section. The photographs came from his Drive folders and the
91 filled texts were transcribed from his source document (`scripts/review-texts.py`, 86
transcribed by hand because the `.docx` leaks raw OOXML). They are not written by us, and the
name, rating and "Verified Customer" badge on those cards are therefore accurate.

⚠️ **The original text of this section was wrong and is preserved below only so the reasoning
is not lost.** It was written on 2026-08-29 from the observation that Drive held images but no
matching text, and it inferred from there that the copy would have to be invented. That
inference was mistaken — the text existed, in a separate document. Any doc still repeating the
"fabricated testimony at scale" framing about these cards is stale.

**What the correction does NOT cover — this part still stands, and is a separate cleanup:**

Twelve testimonial quotes written at project setup (March 2026, before Malcolm supplied
anything) are still live and are **not** his customers. Verified 2026-08-30 against all 99
real cards: **zero full-name matches** (a few first names coincide — there is a Sarah E and an
Emma H — but no Sarah M. or Emma R.).

| Where | Section | Names |
|---|---|---|
| Every product page, directly below the real carousel | `customer_reviews`, "What Our Customers Say" | Sarah M., Emma R., Lisa K., Anna D. — each suffixed **"- Verified Customer"**, 5 stars |
| `/pages/reviews` | `testimonials`, "Customer Testimonials" | Caroline B., Sophie L., Hannah V., Nicole P., Rebecca S., Isabelle M., Elena G., Katharina H. |

Their voice gives them away — *"What convinced me was the transparency - actual PubMed links,
real concentrations, no marketing fluff."* On the product page the effect is that real
testimony and setup copy now sit on one page both claiming "Verified Customer". The store is
EUR/EU-facing, where the Omnibus Directive prohibits presenting fabricated reviews as genuine.
**Awaiting Malcolm's instruction; nothing has been removed.**

<details>
<summary>Original §2 as written 2026-08-29 (superseded — kept for the reasoning)</summary>

> **There is no review text anywhere in Drive — only images named after a person.** So every
> name, star rating, title and body would be written by us, for a store that has **zero orders**
> and has never sold anything. […] Presenting them as named verified customers is fabricated
> testimony at scale.
>
> Three workable positions were offered: (1) illustrative, labelled as such — drop the name,
> rating and badge; (2) hold the carousel until Klaviyo Reviews carries real ones; (3) ship as
> written testimony.

The build was designed to be identical under all three, so no code changed when this resolved.
§6 still notes the two fields that would have changed under option 1.

</details>

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

## 3a. What Hairgenetix actually does — and why it argues against copying it

Inspected live 2026-08-29 (`a24be5-c5.myshopify.com`, theme `165687230796`), because Malcolm
asked what could be learned from the sister brand's per-product setup.

**The decisive finding: there is no per-product setup.** `sections/sw--before_after.liquid` is
section-block driven, and the same section id `sw_before_after_dcCkxq` with the **same 14
customers** — Stuart US, Karen UK, Diego US, Aven US, Miguel US, Denise Belgium… — is
copy-pasted into all four product templates (`product.json`,
`product.copper-peptide-product.json`, `product.supplements-and-serum.json`,
`product.cartridges.json`). 17 products, 4 templates, **one dataset duplicated four times**.

That is worth stating plainly: **the architecture Hairgenetix uses is what produced the
duplication Malcolm is asking us to avoid.** Blocks-in-template-JSON makes copy-paste the path
of least resistance, and the sister store is the evidence of where that ends up. It is the
strongest argument for §3's metaobject model, not against it.

### Worth taking

- **Labels as `text` settings** (`before_img_text`, `after_img_text`) rather than baked into
  the pixels — the same conclusion this project reached independently, and it validates it.
- **Country appended to the customer name** ("Karen, UK", "Andres, Denmark"). Good signal on an
  international store; worth adopting in `author`.
- Two separate images per card is a viable alternative to one diptych — but **not for us**: our
  76 source files are already single-file diptychs, and one file guarantees the 50% split that
  the labels are positioned against.

### Worth avoiding, all of it observed live

| fault | why it matters |
|---|---|
| `img_url: 'master'` on every slide | serves the **full-size original** with no `srcset` — a 2048px master into a small card, on 14 slides, on every product page. Ours uses the theme's responsive pipeline |
| `review_star` is an **`html` setting** | raw HTML per block: untranslatable, and Shopify **422s** any `html` setting containing `{{`, `}}`, `{%` or `%}` (ADR-005, learned here the hard way). Ours is a numeric range rendered through the theme's own `rating-star` icon |
| **Swiper 11 loaded from jsDelivr** | an external library on every product page. Ours reuses the theme's `<scroll-carousel>` and `scrollbar` snippet — nothing external, and the prev/next controls hide themselves when the track does not overflow |
| **Invalid JSON in the live schema** | `"label": "Add Customer Name",` — a trailing comma, live right now. It parses in no JSON parser |
| `customer_headline1` / `2` / `3` | three fixed slots instead of one repeatable structure |
| Parallel index-aligned metafield lists | `custom.ingredients_titles` / `_sub_titles` / `_descriptions` / `_images` / `_popup_des` assemble item N from index N of five separate lists. Delete one entry and **everything after it silently misaligns** |

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


---

## 10. What actually shipped, 2026-08-29

| | |
|---|---|
| Metaobject | `customer_review`, 9 fields, `translatable` capability on, storefront-readable |
| Product metafield | `custom.customer_reviews` (`list.metaobject_reference`, validated to the definition) |
| Images | **76 uploaded** as SEO-named JPEGs via `scripts/upload-theme-images.py` |
| Entries | **76**, upserted by stable handle `review-<concern>-<person>` |
| Section | `sections/product-reviews-before-after.liquid` — new file, no core Liquid touched |
| Template | `templates/product.json` section `before_after` **swapped in place** |
| Scripts | `product-reviews-setup.py`, `-build-plan.py`, `-publish.py`, `-add-section.py` |

**The template already had a `before_after` section** — a `multi-column` of three static tiles
headed "Verified Customer Results", the same three on all eleven products. It was **replaced in
place, keeping the section id**, not appended: two before/after sections on one product page is
worse than the generic one alone. Keeping the id also held its position in `order` without
touching the array. Same approach `reviews-add-before-after-carousel.py` took on the reviews page.

Undo the section swap: `python3 scripts/product-reviews-add-section.py --restore backups/product.json-20260829-114101.json`

**Moved up 2026-08-29** on Malcolm's instruction — "directly beneath the product info, above
'How to Use — 3 Simple Steps'". Order is now `main → before_after → featured_in → how_to_use →
…`. Only the `order` array changed; no section id, setting or block was touched, so no
translation key moved and nothing was deleted and recreated.

Taken literally, "directly beneath the product info" puts it above `featured_in` (the press
bar) as well. That turns out to be moot: **`featured_in` renders nothing on product pages** —
the `logo-list` section is in the template order but produces no DOM at all. Worth knowing
separately from this change.
Undo the move: `--restore backups/product.json-20260829-122332.json`

### Verified live, measured off the DOM (not `innerText`, which lies on this theme)

| | desktop 1440 | mobile 390 |
|---|---|---|
| card counts match allocation on all 11 products | ✅ 76 total | — |
| media aspect ratio | 1.000 on every card | 1.000 |
| labels inside their own picture | ✅ | ✅ |
| card heights | one value, 595px | one value, 520px |
| track overflows (carousel active) | ✅ 3648 vs 1200 | ✅ |
| edge prev/next buttons | shown | correctly hidden below 700px |
| horizontal page overflow | — | none |
| console errors | 0 | 0 |

### ⚠️ Open — state as measured live on 2026-08-30

1. ~~**The copy is placeholder.**~~ **91 of 99 cards now carry real transcribed copy.** The
   remaining **8 are all on `copper-peptide-ghk-cu-microneedling-facial-stamp-set-1-month`**
   and are live and publicly visible, reading "PLACEHOLDER: review headline" under a name,
   five stars and a Verified Customer badge.

   **The text pool is exhausted, not merely unrun** — `product-reviews-fill-copy.py --report`:
   98 texts transcribed, 12 held back because they state an age, 2 surplus. Both surplus texts
   are `pdrn_serum` ones that name a serum, so the `FORMAT_WORDS` filter correctly bars them
   from a microneedling device. No honest text remains that can sit on that product.

   **Malcolm, 2026-08-30: leave them for now — the microneedling products are the next piece
   of work.** Not a defect to fix in isolation; it resolves with that product's own round.

2. ~~**§2 is still unanswered.**~~ **Resolved — see §2.** The cards are real customers, so the
   name, rating and badge are accurate and stay.
3. **"Fiona C" appears on two products** — `glutathione-brightening-serum` and one wrinkle
   product. Two *different* photographs (she is in both the Wrinkles and Brightening Drive
   folders) but the same name, which reads as one customer reviewing two products.
4. **The setup-written testimonial quotes are still live** — four on every product page
   (`customer_reviews`) and eight on `/pages/reviews` (`testimonials`), none matching a real
   customer by full name. See §2 for the table and the verification. **Awaiting instruction.**
5. **Klaviyo Reviews' product-reviews block is ALREADY INSTALLED** on `templates/product.json`.
   Earlier notes had this as outstanding; it is not. Real reviews have somewhere to land.
6. **4 orphan `customer_review` metaobjects** are unattached to any product —
   `review-wrinkles-heather-s` and `review-wrinkles-megan-a` (the two duplicate-photograph
   drops of 2026-08-29, deliberately detached rather than deleted so their translations
   survive), plus `review-firming-marie-r` and `review-brightening-fiona-c`. 103 entries exist,
   99 are attached. Harmless — nothing renders them — but worth knowing before a count is
   trusted.
