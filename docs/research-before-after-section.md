# `research-before-after` — the labelled before/after section

Built 2026-08-27 for `/pages/acetyl-hexapeptide-8-research`. This document exists so a future session can
use, extend or translate this section without re-deriving why it was built rather than configured.

---

## 1. What it is

A **custom, additive theme section** — `sections/research-before-after.liquid` — that renders a
side-by-side before/after image with up to **four text labels overlaid on it**, beside a copy card.

| | |
|---|---|
| Theme file (live) | `sections/research-before-after.liquid` on theme `184835965313` (Impact) |
| Source of truth | `theme/sections/research-before-after.liquid` **in this repo** — edit here, then deploy |
| In use on | `templates/page.research-argireline.json`, section id **`key_findings_ba`**, blocks `f1` `f2` `f3` |
| Replaced | the previous `key_findings` section (type `media-with-text`), now removed |

**No core theme file was modified.** This is a new file added alongside the theme's own sections, so an
Impact update cannot overwrite it — and equally, it will not receive Impact's improvements.

---

## 2. Why a custom section, and not something built in

Both native options were examined first and both fail a hard requirement:

- **`media-with-text`** (what the page used before) has **no caption, overlay, label or badge setting at
  all**. Every setting on both of its block types was checked. Labels cannot be put on the image.
- **`before-after-image`** (the theme *does* ship one) has `before_text` and `after_text` — but it takes
  **two separate image files**, renders a **drag-to-compare slider**, and offers **only two labels**. Our
  masters are single-file diptychs, and the page needs a third label (the result) plus a fourth (the
  illustration note).

Baking the labels into the image pixels was rejected outright: **pixels cannot be translated.**

---

## 3. How translation works — read this before touching the labels

**The labels are translatable because they are `text` settings on a section stored in a page template.
Nothing in the Liquid does it. Do not add label text any other way.**

Shopify exposes every text setting of such a section as a translatable resource of type
**`ONLINE_STORE_THEME_JSON_TEMPLATE`**, keyed:

```
section.page.<template>.json.<section-id>.<block-id>.<setting-id>:<hash>
```

Verified live on 2026-08-27 — 12 label keys, e.g.:

```
section.page.research-argireline.json.key_findings_ba.f1.before_label:5dsmnbx9rfl9   = 'Before'
section.page.research-argireline.json.key_findings_ba.f1.after_label:37u26hm1ltu7k    = 'After 4 weeks'
section.page.research-argireline.json.key_findings_ba.f1.result_label:1akx2zzfj0lzx   = '48.9% overall anti-wrinkle efficacy vs placebo'
section.page.research-argireline.json.key_findings_ba.f1.note_label:26d0h0r6vnbtw     = 'Illustration'
```

### ⚠️ The translation app is **Translate & Adapt**, not Langify

**Langify is NOT installed on this store.** The installed app is Shopify's own **Translate & Adapt**.
`CLAUDE.md`, `AGENTS.md`, `README.md`, `docs/architecture.md`, `.claude/rules/shopify.md` and ADR-002 all
said the opposite until 2026-08-27; they have been corrected but older handovers still carry the wrong
claim. Verified via `appInstallations` — see §7.

Because the resource type is a **Shopify-native** one, these labels appear in Translate & Adapt with **no
app configuration**. There is nothing to wire up.

### How to actually translate them

1. Publish the target locale (only `en` is published today — see §6).
2. Shopify admin → **Translate & Adapt** → the locale → *Theme* → *Templates* → `page.research-argireline`.
3. The label strings appear there as ordinary entries.
4. Or programmatically, via the `translationsRegister` mutation against the resource id
   `gid://shopify/OnlineStoreThemeJsonTemplate/page.research-argireline?theme_id=184835965313`, using the
   `key` **and** the `digest` from `translatableContent`.

### ⚠️ The trap that will cost someone a day

**The `:hash` suffix on each key changes when the setting's value changes.** Editing the English text
invalidates the existing translation for that key. So:

- Settle the English wording **before** paying for or generating translations.
- Moving a block to a different section id (as this build did, `key_findings` → `key_findings_ba`)
  creates **entirely new keys** and orphans the old ones. That was free this time because no
  translations existed; after nine locales are populated it would mean redoing them.

---

## 4. The settings

Per block (type `finding`, max 6 blocks):

| setting | type | translatable | notes |
|---|---|---|---|
| `image` | image_picker | — | the side-by-side diptych, **split at exactly 50%** |
| `image_mobile` | image_picker | — | optional |
| `media_position` | select | — | `start` = image left, `end` = image right |
| `before_label` | text | ✅ | default "Before" |
| `after_label` | text | ✅ | e.g. "After 4 weeks" |
| `result_label` | text | ✅ | e.g. "48.9% overall anti-wrinkle efficacy vs placebo" |
| `note_label` | text | ✅ | e.g. "Illustration". **Clear it to hide it** |
| `label_background` / `label_text_color` | color | — | per block |
| `subheading` / `title` | text | ✅ | |
| `content` | richtext | ✅ | |

Label placement relies on the master being a diptych split at **exactly 50%** — `before` sits over the
left half, `after` over the right. A master that is not an even split will misplace them.

---

## 5. Layout, and the two bugs worth remembering

Geometry is **matched to the theme's own `media-with-text`**, measured live on
`/pages/copper-peptide-research` (which still uses it): white card `#fff`, `border-radius: 10px`,
`padding: 80px` desktop / `40px 32px` mobile, column gap **24px** desktop / 20px mobile.

> The 24px gap was derived, not read: the original renders a **660px** image and a first attempt with a
> 48px gap rendered **648px**. If you change the gap, re-check the image width against 660.

**Bug 1 — the result label wrapped onto two lines however wide the image was.**
An absolutely-positioned box at `left: 50%` shrink-to-fits inside only the **remaining 50%** of its
container. Fixed with `width: max-content`. Wrapping is deliberately still allowed under 700px, where a
45-character label cannot fit on one line at a readable size.

**Bug 2 — label contrast.** Each label has its own **local pill scrim**, never a wash over the whole
image. A flatter overlay dulls the photograph instead of fixing legibility — a lesson this store already
paid for on its collection banners.

CSS is scoped to `#shopify-section-{{ section.id }}`, the pattern the theme's own sections use. Because
this is a real Liquid section, the `custom-html` restriction on `{{ }}` does **not** apply here.

**Known cosmetic residue:** on `f1` and `f2` the copy card renders taller than the 660px image (703px and
727px) because those study descriptions are longer than the ones the original section held. Tops align;
bottoms do not. Fixing it means either clipping copy or cropping faces, so it was left — the honest fix is
to trim a line of copy.

---

## 6. Current state

- Only **`en`** is published. Nine locales are planned but none exist yet, so **no translation work has
  been done and none is pending**.
- The section is live with three blocks and all four labels populated.
- The three masters render **uncropped at 660×660** — the old `media-with-text` was cropping 3.6–5.1% off
  each side.

---

## 7. How to verify any of this yourself

```bash
# which translation app is really installed
{appInstallations(first:30){nodes{app{title handle}}}}

# are the labels translatable, and what are their keys
{translatableResources(first:40,resourceType:ONLINE_STORE_THEME_JSON_TEMPLATE){
   nodes{resourceId translatableContent{key value digest}}}}

# deploy an edited section (source of truth is theme/sections/ in this repo)
PUT /admin/api/2025-01/themes/184835965313/assets.json
    {"asset":{"key":"sections/research-before-after.liquid","value":"<file contents>"}}
```

Shopify **rejects invalid Liquid on upload**, so a successful PUT is also the syntax check.

Rollback for the template: `python3 scripts/patch-template.py --restore backups/page.research-argireline-<stamp>.json --template templates/page.research-argireline.json`

---

*Related: `docs/clinical-trial-before-after-images.md` (where the images came from),
`.claude/rules/shopify.md`, `docs/decisions-log.md` ADR-002 correction note.*
