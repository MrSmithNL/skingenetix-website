# Study-page template

**Date:** 2026-09-24 · **Reference build:** `/pages/study/copper-peptide-wrinkle-trial-badenhorst-2016`
**Replaces:** the pilot structure of four centred rich-text blocks.
**Companion to:** `docs/science-page-template.md` (the hub template).

---

## 1. Why the pilot structure had to go

The pilot rendered four plain `rich-text` sections reading metaobject fields. Shopify richtext
strips class attributes, so nothing richer than paragraphs and lists could live there: no key-figures
band, no chart, no table, no image. The pages read as documents, not as designed pages.

**The lever was already in the template.** The `jsonld` field is a `multi_line_text_field` holding raw
HTML, emitted unescaped by a `liquid` block as `{{ metaobject.jsonld.value }}`. One more field of the
same type, rendered the same way, carries a fully designed body.

---

## 2. Structure

Three theme sections. Everything designed lives in the middle one.

| Section | Field | Carries |
|---|---|---|
| `study_head` | `intro` (rich text) | H1, byline, the answer paragraph, the verdict |
| `study_designed` | `sections_html` (raw HTML) + `jsonld` | the seven bands below, and the schema |

`study_reference` was removed on 2026-09-24. Empty of visible content it still rendered 80px of
dead band, and it painted a second white section straight after the last bone one; the citation is
band 7 now and the schema block moved into `study_designed`.

The seven bands inside `sections_html`, each painting its own background:

| # | Band | Ground | Padding |
|---|---|---|---|
| 1 | **Key figures** — three numbers, in Fraunces like the hubs' | white | 56 |
| 2 | **At a glance** — a real `<table>`, nine rows | bone | 72 |
| 3 | **What the measurements showed** — the chart + its `<table>` + a captioned source | white | 72 |
| 4 | **What the researchers did** — prose beside a responsive image | bone | 88 |
| 5 | **What this study does not show** — **on ink**, the largest body text on the page | **#1A1A1A** | 104 |
| 6 | **What it means for our products** — one solid CTA, one ghost | white | 80 |
| 7 | **Reference** — citation and the read-at-source note | bone | 40 |

Padding carries rank. Six bands at one value is a colour stripe, not pacing: the first build measured
`distinctSectionPaddings` 2 against a floor of 3, and now measures 7.

**Band 5 is the reason the page exists.** A summary of an abstract is rated *Lowest* by Google's raters
and is what any competitor can generate; an appraisal that states what the study cannot support is not.
It shipped as a tinted, rounded box *narrower and less padded* than its neighbours — the standard aside
component, i.e. the register of a footnote. The design critic's verdict was that if you hid the words
you could not tell which band mattered. It is now the one break in the rhythm.

---

## 3. Hard rules

- **One `<h1>`**, and it must not open with the bare ingredient term — `scripts/study-pages.py`
  rejects that, because it cannibalises the hub. Lead with the question.
- **Every figure read at source**, from the tables and methods, not the abstract. The reference band
  states the date and which parts were read.
- **The concentration line is mandatory**, even — especially — when the paper never gives one.
- **Nulls and non-significant results appear in band 5**, not omitted.
- **Sections and CSS are self-contained.** The band CSS ships inside `sections_html`, so a page cannot
  depend on theme styles that might change.
- **SEO title ≤ 60 characters, description ≤ 160.** Both are asserted before publishing.
- **Schema:** `WebPage` carrying `author`, `reviewedBy`, `lastReviewed`, with `mainEntity` → `Article`
  → `isBasedOn` → `ScholarlyArticle` (DOI or PMID). Our page is never typed `ScholarlyArticle`.

---

## 4. Build sequence

1. Read the paper at source. Record design, n, what was applied, comparators, duration, measurement,
   concentration, funding, and every figure with its p-value.
2. Update the ingredient's claims register if anything differs from what is recorded there.
3. Write the six bands. Chart config follows `scripts/hub_charts.py` — `title`, `subtitle`, `unit`,
   `decimals`, `domain`, `ticks`, `value_width`, `series`, `rows`, `table_head`, **`caption`**
   (`caption` is required; the renderer raises `KeyError` without it).
4. Publish the metaobject. English first.
5. Verify live: one H1, bands present, real `<table>` count, chart rendered, JSON-LD parsed.
6. Capture desktop and mobile, tile to `~/Desktop/skingenetix-renders.png`, `open` it.
7. Translate with `scripts/hub-i18n.py` once the English is signed off.

---

## 5. Traps met building the first one

| Trap | What happens |
|---|---|
| Shopify prepends **several** `/* */` comments to metaobject templates | `hub-upgrade.split()` strips one and the JSON parse fails. Strip them all. |
| Empty rich-text sections still render their padding | The legacy `study_facts`/`study_body` sections left ~600px of dead band on a page that did not use them. `rich-text` has no `remove_vertical_spacing`, so the sections had to be removed — which meant porting the two pilot pages onto `sections_html` first. |
| `hub_charts.render_chart` requires `caption` | `KeyError: 'caption'` with no guidance. |
| `pageByHandle` does not exist in the Admin API | Use `study-pages.py`'s `hub_id()`, which queries `pages(query:"handle:…")`. |
| `study-pages.py` requires all six locales for every field | It cannot publish an English-first page. `build-study-page.py` publishes English first and adds locales as the config carries them. |
| **The theme's own rules beat CSS shipped in `sections_html`** | `.sty h2{font-size:32px}` and `main h1{font-size:…}` both silently did nothing. Use a selector specific enough to win (`.sty .sty__band h2`) or `!important`, and **verify on the live page** — computed style, not intent. |
| **A viewport breakout renders the page blank** | `.sty{overflow-x:clip}` + `.sty__band{margin-inline:calc(50% - 50vw);width:100vw}` shipped a blank page. The theme gives `.sty` no width, so it shrink-to-fits; with every child pulled out by −50vw its width computed to **0** and the clip context cut the body away. The computed styles read correctly (`margin-left:-720px`, `width:1440px`) — **only the screenshot showed it**. Bands are therefore not full-bleed. |
| **Clearing a field drops its translations** | Emptying English `reference` removed all five translations of it in the same call, so the two pilot pages lost their translated citations. Read and re-register the translations *before* clearing the source, or rebuild them from the config. |
| `measure.py` measured the cookie dialog | `measureCh` takes the first paragraph over 200 characters **in document order**, which was the Shopify consent dialog — the same 85ch on every page of the site. Patched in the skill 2026-09-24 to prefer `main`. Real measure on this page: **61ch**. |

---

## 6. Status

- **Built:** Badenhorst 2016 (copper peptide), English.
- **Ported to the new field:** both pilots, English and all five translations, content unchanged.
- **Legacy sections removed** from `templates/metaobject/study.json`.
- **Not yet done:** the pilots still show their old *content* in the new wrapper; they have no key
  figures, chart or limitations band until they are rewritten to this template. Translations of the
  Badenhorst page are pending.

Related: `docs/study-inventory-2026-09-24.md` (which twelve studies and why),
`docs/research-2026-study-hubs-credibility.md` (the qualifying criteria),
`docs/science-page-template.md` (the hub template this borrows its rhythm from).

---

## 7. The files

| File | Role |
|---|---|
| `scripts/study_sections.py` | The renderer: CSS, the six band builders, `render(cfg, loc)`. Refuses to emit a Liquid delimiter. |
| `scripts/build-study-page.py` | Checks, publishes and verifies a page from its config. English first; translations when the config carries them. |
| `configs/studies/<handle>.json` | One study: figures, glance rows, chart, media, limitations, meaning, and the `checks` probes that must survive into the rendered HTML. |
| `scripts/study-template-upgrade.py` | The idempotent migration that added the `sections_html` field and the `study_designed` section to the live template. |
| `scripts/study-pages.py` | The pilot tool. Still owns `intro`, `key_facts`, `body`, `reference`; it cannot build a designed page. |

```
python3 scripts/build-study-page.py configs/studies/<handle>.json                # dry run
python3 scripts/build-study-page.py configs/studies/<handle>.json --apply        # publish
python3 scripts/build-study-page.py configs/studies/<handle>.json --verify-live  # check live
```
