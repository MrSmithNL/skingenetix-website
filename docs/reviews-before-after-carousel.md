# `reviews-before-after` — the customer before/after review carousel

Built 2026-08-27 for `/pages/reviews`. This document exists so a future session can use, extend
or translate this section without re-deriving why it was built rather than configured.

Sibling of `research-before-after` (see `docs/research-before-after-section.md`). They look
related and are deliberately separate: that one is a *clinical finding* beside a copy card, this
one is a *customer review* in a carousel card.

---

## 1. What it is

| | |
|---|---|
| Theme file (live) | `sections/reviews-before-after.liquid` on theme `184835965313` (Impact) |
| Source of truth | `theme/sections/reviews-before-after.liquid` **in this repo** — edit here, then deploy |
| In use on | `templates/page.reviews.json`, section id **`before_after`**, blocks `rv_1` `rv_2` `rv_3` |
| Replaced | the previous `before_after` section (type `multi-column`, 4 image tiles) |
| Deploy | `python3 scripts/reviews-add-before-after-carousel.py [--dry-run]` |
| Undo | the same script prints its own `--restore backups/page.reviews-<stamp>.json` line |

One card carries all six things a review slide needs: the before/after pair, the customer's
name, a verified badge, a star rating, a review title, the review body, and a link to the
product reviewed.

**No core theme file was modified.** This is a new file added alongside the theme's own
sections, so an Impact update cannot overwrite it — and equally, it will not receive Impact's
improvements.

---

## 2. Why a custom section, and not something built in

Malcolm's standing constraint is to use standard sections before writing our own, so every
plausible stock Impact section was read on the live theme first. None carries more than five of
the six fields:

| Section | Image | Name | Stars | Title | Body | Product link | Carousel |
|---|---|---|---|---|---|---|---|
| `testimonials` | avatar only — **`sizes: 40px, 56px`, srcset caps at 168w** | ✅ | ✅ native | ✅ | ✅ | ✗ | ✅ native |
| `multi-column` | ✅ one | ✗ | ✗ | ✅ | ✅ | ✅ | below `md` only |
| `media-with-text` | ✅ one | ✗ | ✗ | ✅ | ✅ | ✅ | ✗ |
| `before-after-image` | ✅ drag slider | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| `slideshow` | ✅ one | ✗ | ✗ | ✅ | ✅ | ✅ button | ✅ |
| `press` | ✗ | ✅ | ✅ | ✗ | ✅ quote | ✗ | ✅ |

`testimonials` is the closest and fails on the one thing that cannot be worked around: its image
is an **avatar by design**, capped in the Liquid at 168px wide. A before/after pair is impossible
there, not merely small.

---

## 3. What is reused rather than rebuilt

The carousel is **not custom**. It is the theme's own machinery, assembled:

- `<scroll-carousel>` with `class="scroll-area bleed md:unbleed"` — the same element and classes
  `sections/testimonials.liquid` uses.
- `{% render 'scrollbar', observes: …, show_buttons: true %}` — the theme's prev/next
  circle-buttons and progress bar. The snippet carries `peer-not-scrollable:hidden`, so the
  controls **hide themselves when the track does not overflow**. That is why no block-count test
  is written anywhere in this section: a count is a proxy for the target, and this store has
  already shipped two production bugs from scoping on one (see `docs/architecture.md`,
  2026-08-25).
- The star row is `{% render 'icon' with 'rating-star' %}`, the identical markup `testimonials`
  renders, so ratings match the rest of the store.
- Breakpoints are copied from `testimonials`: 1 card below 700px, 2 to 1150px, 3 above.

Hairgenetix's equivalent component loads **Swiper 11 from jsDelivr**. Nothing external is loaded
here.

---

## 4. The image contract — read this before supplying images

`image` is **one file holding both frames, split at exactly 50%, square overall (1:1)**, so each
half is a portrait rectangle half as wide as it is tall. Malcolm's brief, 2026-08-27.

The before label sits over the left half and the after label over the right half at fixed
percentages, so **a master that is not an even 50/50 split will misplace them.**

**Never supply an image with BEFORE or AFTER printed into the pixels.** The four images this
section replaced had them burnt in as a dark teal bar and a green bar across the top 40px, and
pixels cannot be translated — nine locales are planned. The labels are `text` settings for
exactly this reason.

### Current images are placeholders

`scripts/build-review-ba-squares.py` rebuilt three 1:1 masters from the old 2:1 files by cropping
the label bar off and centre-cropping each half. They are **560×560**, which is the ceiling the
sources impose — against a 432px card at 2× the CDN has nothing above 560w to serve, so they are
soft on a retina display. That is a reason to regenerate, not a reason to compress differently.

Two further faults in the source set, both requiring regeneration rather than cropping:

- **`skingenetix-ba-firmness-combined.jpg` has the AI image brief rendered into the photograph** —
  a white panel reading `image-container`, `body: display: flex…`, `alt "Close of skin with
  sagging"`. It is excluded from the build for that reason, which is why there are three cards
  and not four.
- **All four pairs are two different people.** The fine-lines "before" is a hazel-eyed European
  woman and the "after" is a brown-eyed East Asian woman. Regeneration must follow
  `docs/clinical-trial-before-after-images.md` — two photographic sessions, one subject.

---

## 5. Translation

Same mechanism as `research-before-after`. Every `text` setting on a section stored in a page
template is exposed by Shopify as a translatable resource of type
`ONLINE_STORE_THEME_JSON_TEMPLATE`, keyed:

```
section.page.reviews.json.before_after.<block-id>.<setting-id>:<hash>
```

So `before_label`, `after_label`, `author`, `verified_label`, `title`, `content`,
`product_prefix` and `product_text` all appear in **Translate & Adapt** with no app
configuration. `product_url` is a `url` setting and is not translated; Shopify resolves the
locale prefix on internal links itself.

⚠️ The `:hash` suffix is a digest **of the value**, so editing the English invalidates that key's
translation. Settle the wording before translating. Only `en` is published today.

---

## 6. The settings

Section: `full_width`, `subheading`, `title`, `content`, `link_text`, `link_url`, `background`,
`background_gradient`, `text_color`, `heading_color`, `card_background`, `card_text_color`,
`label_background`, `label_text_color`, `verified_color`.

Per block (type `review`, max 24 blocks):

| setting | type | translatable | notes |
|---|---|---|---|
| `image` | image_picker | — | **1:1 diptych, split at exactly 50%** |
| `image_mobile` | image_picker | — | optional |
| `before_label` / `after_label` | text | ✅ | chips on the picture; clear one to hide it |
| `author` | text | ✅ | customer name |
| `show_verified` / `verified_label` | checkbox / text | ✅ | default "Verified Customer" |
| `show_rating` / `rating` | checkbox / range 1–5 | — | theme star markup |
| `title` | text | ✅ | review headline |
| `content` | richtext | ✅ | review body |
| `product_prefix` | text | ✅ | default "Reviewing" |
| `product_text` / `product_url` | text / url | ✅ / — | the product or treatment, and its link |

---

## 7. Two things caught during the build, both worth remembering

**The whitespace-stripping Liquid tags ate the space** between the "Reviewing" prefix and the
product link, so the live page read `ReviewingAcetyl Hexapeptide-8…`. The gap is now a CSS
`margin-inline-end`, not a typed space. Note that `innerText` **cannot** verify this — it
concatenates inline elements with no separator whatever the margin is, and reported the fault as
still present after it was fixed. Measure `a.left - prefix.right` off the live DOM instead.

**A CSS comment containing Liquid's stripping tag delimiters 422s the upload.** Liquid parses the
whole file before the browser ever sees it, so a comment describing the tags is still a tag.
Shopify's message is explicit — `Liquid syntax error (line 200): Unknown tag` — and a successful
PUT doubles as the syntax check.

---

## 8. How to verify it yourself

```bash
# is the section live, and does it hold what it should
python3 - <<'PY'
# see scratchpad verify.py — reads the live DOM for: media aspect ratio (must be 1.000),
# labels inside the image rect, six fields per card, and scrollWidth vs clientWidth
PY
```

Measured live 2026-08-27 after deploy:

| | desktop 1440 | mobile 390 |
|---|---|---|
| media box | 432 × 432 (ratio 1.000) | 289 × 289 (ratio 1.000) |
| labels inside the picture | 3/3 | 3/3 |
| six fields present | 3/3 | 3/3 |
| track overflow | `scrollWidth == clientWidth` — controls correctly hidden | 946 vs 390, `is-scrollable`, controls shown |

---

## 9. Open, and not fixed by this build

- **The review copy is placeholder.** Every name, rating and body was already live on this page
  in the `testimonials` section and was re-attached to the matching photograph — nothing new was
  invented, and none of it is real. The store has no orders. See the fabricated-social-proof note
  in `docs/architecture.md`.
- **Those three reviews now appear twice on the page** — once in this carousel and once in the
  `testimonials` section below it.
- **The standard answer for the review *corpus* is Klaviyo Reviews**, which Hairgenetix already
  runs (4.8 / 1,613 reviews, verified-buyer pills, linked product chips). Klaviyo is already on
  the Skingenetix account; only the onsite/email script is installed, not the reviews block.
- The page's `trust` section still claims *"Verified Reviews — All reviews from confirmed
  customers"* on a store with no reviews app and no orders.

---

*Related: `docs/research-before-after-section.md`, `docs/clinical-trial-before-after-images.md`,
`.claude/rules/shopify.md`, `.claude/rules/website-imagery.md`.*
