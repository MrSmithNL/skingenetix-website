# Science-page template — the Argireline build

**Status:** adopted 2026-09-23 (Malcolm: _"now lets save this as the template to follow for the other science pages. We will improve them accordingly one by one later."_). Written up 2026-09-24. ADR-2026-09-24-S.
**Reference page:** [/pages/acetyl-hexapeptide-8-research](https://www.skingenetix.com/pages/acetyl-hexapeptide-8-research), live in six languages.
**Replaces:** Matrixyl 3000 as the reference build. Amends items 2 and 6 of the research-page standard (`docs/content-plan-2026.md` §4).
**Rollout:** one page at a time, on Malcolm's go-ahead for each. **PDRN done 2026-09-24** (external 9.82, page audit 100/96/100/93). Next: copper peptide, Matrixyl 3000, glutathione.

---

## 1. What the template is, in one paragraph

A science page that answers the ingredient question in its first screen, shows the three strongest numbers straight away, then lets the reader go from a short, numbered list of what the evidence shows to the study behind each line, and ends with every source in one real table. **Its signature:** _every claim is one click from the study that supports it._ Since 2026-09-24 every card is a positive, sourced result (ADR-2026-09-24-P): the page does not publish negative findings as cards or index rows.

---

## 2. Section order

Twelve sections. The first column is the section id used in the template JSON; keep the same ids on every hub so the tools and anchors work unchanged.

| #   | Section id         | Type                                  | Background      | What it holds                                                                                                                           | Built with                      |
| --- | ------------------ | ------------------------------------- | --------------- | --------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------- |
| 1   | `hero`             | `image-with-text-overlay`             | image           | H1 inside the richtext (Impact renders heading blocks as `<p>`), one-line promise                                                       | stock                           |
| 2   | `stats`            | `impact-text`                         | White `#ffffff` | the three key figures, each with its qualifier and source link                                                                          | stock                           |
| 3   | `overview`         | `custom-html`                         | Bone `#F0F0F0`  | centred definition, author line, dated byline; then _At a glance_ beside the product cut-out, with _Back to Science_ and _Shop_ buttons | custom (§5)                     |
| 4   | `evidence`         | `custom-html`                         | White           | mechanism lead, then a numbered index of the findings, strongest first, each row linking to its card; button to the table               | custom (§5)                     |
| 5   | `key_findings_ba`  | `research-before-after` (our section) | card            | one card per index row, image side alternating, labels burned onto the image                                                            | our own section, already in git |
| 6   | `charts`           | `custom-html`                         | White           | `scripts/hub_charts.py` bars with a real `<table>` under each                                                                           | custom (no stock chart)         |
| 7   | `usage`            | `custom-html`                         | Bone            | row 1 _What N% X Means_ (image left); row 2 _How to Use X_ as a 3-step timeline (image right), layering note                            | custom (§5)                     |
| 8   | `evidence_sources` | `custom-html`                         | White           | **Evidence & Sources**: one real `<table>`, one row per study; the page's WebPage JSON-LD lives here                                    | custom (§5)                     |
| 9   | `faq`              | `faq`                                 | Bone            | 5–6 questions, answers carry the same qualifiers as the body                                                                            | stock                           |
| 10  | `shop_ingredient`  | `featured-collection`                 | White           | the products with this ingredient                                                                                                       | stock                           |
| 11  | `related`          | `multi-column`                        | Bone            | the other four science pages                                                                                                            | stock                           |
| 12  | `cta`              | `rich-text`                           | Ink `#1A1A1A`   | one button to the serum                                                                                                                 | stock                           |

The old pages carried separate `evidence_table` (`specification-table`) and `references` sections. **Both are replaced by `evidence_sources`**, which is why the template has one section fewer and the backgrounds from FAQ down are flipped compared with the other four pages today.

---

## 3. Section by section

### 3.1 `overview` — answer first, then the credentials

- **Intro, centred, full width, at the top of the Bone band.** `<h2 class="ovw__ih">What Is X?</h2>`, then a definition of 40–60 words whose first sentence is bold and self-contained (the sentence an AI engine quotes), then one sentence on how results were measured.
- **Author line:** `<p class="ovw__auth">Written by <strong>Malcolm Smith</strong>, founder of Skingenetix, who compiles the claims registers behind these pages.</p>`
- **Byline paragraph — a contract, not copy.** Exactly `<p><em>By Skingenetix. Medically reviewed by Dr Esther Bodde, Cosmetic &amp; Medical Physician. Every figure checked against the published paper or its PubMed record. Last reviewed <date>.</em></p>`
  - `<p><em>` with **no class**: `scripts/set-reviewer.py` finds the byline by that literal shape.
  - The reviewer sentence is taken verbatim from `configs/reviewers/esther-bodde.json`: `--remove` deletes it as an exact substring, so any rewording strands Dr Bodde's credit.
  - "Last reviewed [date]" is scored by `page-audit.py` (GEO E1) and matched by set-reviewer's `date_marker`.
  - ⚠️ **Both paragraphs stay direct children of `.ovw__intro`, in the prose flow.** Wrapped in their own `<div>` behind a hairline, the AI crawlers' extractor (Trafilatura) dropped all five trust signals, and the external audit fell from 9.70 to 8.65 on _author_, _medical review_ and _recency_. Unwrapped: 9.68 (commit `df440a2`). Style them with CSS; CSS does not affect extraction.
- **Two-column row:** _At a glance_ list on the left, transparent product cut-out on the right. The list has six fixed labels, in this order: **What it is · Best evidence · Independent evidence · Not shown · Safety · How to use.** "Independent evidence" and "Not shown" are what separate this page from a brand page.
- **Buttons:** ghost _Back to Science_ under the list, solid _Shop X_ under the image. A note line links to the matching concern page.

### 3.2 `evidence` — the index

- Centred `<h2 class="evd__h">` phrased as the query: _What Does X Do for Y?_
- A lead paragraph on the mechanism, with its citation linked.
- Caption: _"Here is what the evidence shows, strongest first. Each line opens the study behind it."_
- **Numbered rows `01`–`05`**, each an `<a class="evd__row" href="#rba-fN">`: a claim line and a one-line qualifier (who, how many, what design, and what it does not show). Order: strongest controlled result first, then the next-strongest human result, then lab or mechanism, then safety. Every row is a positive result; no row reports a null finding (ADR-2026-09-24-P).
- A foot line stating the concentration the trials used against ours, and a link to the study page if one exists.
- Button to `#evidence-sources`: _See all N studies and how we graded them._

### 3.3 `key_findings_ba` — one card per index row

- Our section `theme/sections/research-before-after.liquid`. Each card renders `id="rba-{{ block.id }}"`, so block ids **must** be `f1`…`fN` to match the index anchors.
- `media_position` alternates start / end.
- **The `result_label` is burned onto the image, so the number never travels without its qualifier** (e.g. _"14.6% vs 5.9% — dissolving microneedle patch"_). A result from a different delivery method or concentration says so in the label _and_ in the first bold line of the card.
- **The second card is a second positive USP shown as a before/after** (Malcolm, 2026-09-24): "we do not publish negative info about the ingredient… we use that space to show a USP that we can show a before and after for." Choose the strongest sourced result that a photograph can show and that differs from card 1. On PDRN that is the under-eye result (eye bags and tear troughs about 2× the retinol change; register claim 5). The pair is generated on the before/after pipeline and chosen by Malcolm, with its result label burned in like card 1's.

### 3.4 `usage` — two rows, and the how-to as a routine

- Row 1, _What N% X Means_: our own product hero, chosen so the percentage on the label is legible.
- Row 2, _How to Use X_: a connected vertical timeline, three numbered steps (_Start clean → Apply where it matters → Seal it in_), then a layering note linking a sibling science page. Every step is taken from copy that has already been checked against the claims register, so the timeline adds no new claim.
- It is deliberately not the flat numbered rows of the evidence index: the design rules forbid repeating a treatment on one page.

### 3.5 `evidence_sources` — Evidence & Sources

- `<div class="est" id="evidence-sources">`. The stable id is what the button in §3.2 targets. Never link to the template-generated section id, which changes if the template is recreated.
- A real `<table>` with three columns: **Study** (verbatim published title in `<p class="sgref__ti est__ti">`, then author, year, journal, volume, then the PubMed/DOI link) · **Grade** (pill: A controlled human trial measured by instrument · B smaller, uncontrolled or manufacturer data · C skin samples · Review) · **What it found, and what it does not show**.
- The class `sgref__ti` keeps the verbatim-title exemption in `page-audit.py` (ADR-2026-09-23-G). Titles are never paraphrased and never enter a translation table.
- Every study the page cites is a row, including the ones we cannot claim (injection, microneedle, other concentration): "listed and labelled rather than left out".
- The WebPage JSON-LD sits at the end of this section's HTML: `author` (Person: Malcolm Smith), `publisher`, `reviewedBy`, `lastReviewed`, `citation[]`, `inLanguage`. Set `jsonld_host: "evidence_sources"` in the spec and in the reviewer config's hub entry.

---

## 4. Claims rules the template enforces

These come from the claims registers and ADRs; the template simply gives each one a fixed place.

1. **A number always travels with its qualifier.** "48.9%" is _22 of 45 people graded improved_, never a reduction in anything (Argireline register §3). The same fix had to be made in the FAQ answer after it was made on the card, so search the whole page, FAQ included, for every figure you change.
2. **Different delivery or concentration → labelled, never implied.** Microneedle, injection and other concentrations are listed and labelled.
3. **No negative findings as cards or index rows** (ADR-2026-09-24-P). That slot shows a positive USP with a before/after. Whether studies that found nothing, or that do not transfer, stay in the Evidence & Sources table is an open question for Malcolm (2026-09-24).
4. **Our prose paraphrases disease names and mechanism phrases,** even when reporting a study (memory `reporting-a-study-is-still-our-prose`). Only the verbatim title is exempt.
5. **Ingredient-level only on products** until the formula facts are confirmed; the trial magnitudes live on the science page.
6. **Brightening is cosmetic** (glutathione): never "whitening", "even tone" or "dark spots" in our prose.

---

## 5. Why four sections are custom code (amending standard item 2)

Malcolm's rule is _standard sections before custom code_ (memory `standard-sections-before-custom-code`). Standard item 2 said custom code only for charts. The template needs four more, and each one was forced:

| Section            | Stock option tried or considered            | Why it cannot do the job                                                                                                                                                                                                                                         |
| ------------------ | ------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `overview`         | `rich-text` / `media-with-text`             | Shopify richtext strips `class` attributes, so neither the centred intro above a two-column row nor the styled buttons can be built. `media-with-text` also cropped the cut-out (`object-fit: cover`).                                                           |
| `evidence`         | `rich-text`                                 | A numbered index whose rows are links needs classed markup; richtext strips it.                                                                                                                                                                                  |
| `usage`            | `media-with-text` (what the other four use) | A visualised step timeline needs classes on `<ol>`/`<li>`; richtext strips them.                                                                                                                                                                                 |
| `evidence_sources` | `specification-table` + `references`        | `specification-table` renders `<div>` rows, not a `<table>`, so there is no extraction gain; and its value field strips classes, so the verbatim titles would lose their `sgref__ti` exemption (`docs/decision-evidence-sections-merge-2026-09-23.md` §1.2–1.3). |

**What this costs, and how the cost is handled:**

| Cost                                                                                                                                                                                 | Handling                                                                                                                                                                                                                                             |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Shopify translates a custom-html section as **one block of HTML per language**. Any edit to its English leaves all five translations stale, and a stale translation is still served. | `scripts/hub-i18n.py` rebuilds the five from the page's phrase table (`configs/hub-i18n/<page>.json`) and refuses on any structure, link, leak or look-alike-letter defect. **Never edit the English of these four sections without re-running it.** |
| Malcolm cannot comfortably edit these sections in the theme editor.                                                                                                                  | Edits go through the spec in `configs/hub-upgrades/`. Stock sections (hero, key figures, FAQ, shop, related, CTA) stay editable.                                                                                                                     |
| `page-audit.py` GEO drops 100 → 96: links inside a table. That rule is not among the documented audit factors.                                                                       | Accepted. Each row's link is the source link the external audit rewards.                                                                                                                                                                             |

---

## 6. Rolling the template onto another science page

One page per go-ahead. Claims before layout, so nothing is translated that is about to be withdrawn.

| #   | Step                                                                                                                                                                                                                                          | Tool                                                                                    | Done when                                         |
| --- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- | ------------------------------------------------- |
| 1   | **Claims first.** Re-read at source every figure the page will state; fix any card or FAQ that the register forbids.                                                                                                                          | `docs/claims/<ingredient>.md`                                                           | Figures logged in the register's verification log |
| 2   | **Harvest the live translations** of the sections being replaced (overview, evidence, findings cards, usage, evidence table, references) into a phrase table, so approved translations are reused rather than rewritten.                      | Translate & Adapt via the Admin API                                                     | Phrase table seeded                               |
| 3   | **Build the English** as two specs, one section, one owning spec: `<page>-layout-<date>.json` (overview, evidence) and `<page>-evidence-merge-<date>.json` (findings cards, usage, evidence_sources; removes `evidence_table`, `references`). | `scripts/hub-upgrade.py` dry run                                                        | Order-after matches §2                            |
| 4   | Link the in-text citations.                                                                                                                                                                                                                   | `scripts/link-citations.py --write`                                                     | —                                                 |
| 5   | **Translate.** Complete the phrase table, then build the five locales.                                                                                                                                                                        | `scripts/hub-i18n.py <config>` then `--write`                                           | "all checks passed"                               |
| 6   | **Apply once per spec.**                                                                                                                                                                                                                      | `hub-upgrade.py <spec> --apply`                                                         | Backups written                                   |
| 7   | Retire every spec the new ones supersede (`"_retired": "why"`); `--apply` then refuses. Point the reviewer config's hub entry at the layout spec with `byline: "overview.html"`, `jsonld_host: "evidence_sources"`.                           | edit JSON                                                                               | —                                                 |
| 8   | Re-stamp the reviewer and date.                                                                                                                                                                                                               | `scripts/set-reviewer.py configs/reviewers/esther-bodde.json --apply`                   | All hubs resolve                                  |
| 9   | **Verify live, six languages,** one storefront job at a time. Since 2026-09-24 this also checks classed headings and that every `#anchor` lands.                                                                                              | `hub-upgrade.py <spec> --verify-live` per spec                                          | ✓ ×6, anchors N/N                                 |
| 10  | Audit.                                                                                                                                                                                                                                        | `scripts/page-audit.py /pages/<page>` then `scripts/aiso-audit-page.py <url> --round N` | External ≥ 9.0; GEO 96 is the accepted table cost |
| 11  | **Design check (Rule 27 check A).** Measure at 1440 and 390, then the `design-critic` agent on the live URL in a fresh context.                                                                                                               | `~/.claude/skills/web-design-direction/measure.py`                                      | No blocking finding                               |
| 12  | Show it: desktop and mobile tiled to `~/Desktop/skingenetix-renders.png`, `open`.                                                                                                                                                             | capture recipe                                                                          | On screen                                         |
| 13  | Record: todo, register log, audits README, decisions log if anything was decided.                                                                                                                                                             | —                                                                                       | Committed and pushed                              |

### 6.1 Learned on the PDRN rollout (2026-09-24)

- **Harvest by element where a paragraph holds links or short connectors.** Pair the live English with each translation by position. Use the whole `<p>`/`<li>` when it contains a link or a short joining phrase ("and the"), because a short phrase would be substituted everywhere it appears. Use text nodes (12+ characters) elsewhere. Then check that the numbers in each pair agree. On PDRN every mismatch was word order or `1,500` vs `1500`, but that is the check that would catch a wrong figure. Of the PDRN build's 92 phrases, 46 are the page's own approved translations, 11 are generic template phrases from Argireline and 35 are new.
- **The FAQ's accordion colour flips with its background.** The old pages put Bone accordions on a White FAQ. The template's FAQ is Bone, so set `accordion_background: "#ffffff"` in the same `section_settings`, or the questions vanish into the band.
- **The WebPage JSON-LD is localised per language** by `hub-i18n.py`: `inLanguage`, the `/de/` URL and `@id`, and the name and description from the config's `jsonld_i18n`. Copy those from the page's superseded spec. The Argireline build had shipped English JSON-LD on all six languages.
- **A product cut-out from the white "selector" shot.** Background = near-white pixels (min channel ≥ 243) connected to the edge. Also clear the floor shadow: pale, colourless pixels beside or below the glass. Keep the largest component, feather the edge by 1.2 px, and judge the result on dark and at render size on Bone. Save as **WebP with alpha** (PDRN: 69 KB, against 668 KB as PNG). `upload-theme-images.py` forces JPEG, which would flatten the transparency, so upload the WebP through the Files API directly.
- **Usage can carry a third row** when the page absorbs a definitional query. PDRN keeps *Salmon DNA: Where PDRN Comes From* (content plan §4 item 4) above *What 1% PDRN Means* and the how-to.
- **Drop a citation nobody has read.** Khan 2022 and its card went, per the PDRN register §2 row 27. A table of "every study this page relies on" cannot include one we have not read.
- **`set-reviewer.py --apply` is not needed after a rebuild.** The builder writes the credit and date into the byline and JSON-LD. A dry run proves `--remove` still resolves the page, whereas `--apply` rewrites all five hubs and republishes the study pages.
- **`--verify-live` falls back to curl** when Cloudflare throttles Python (memory `cloudflare-throttles-python-not-curl`).
- **Nested CSS braces must be written `} }`.** A `@media{...{...}}` rule puts `}}` in the html, Shopify reads it as Liquid, and the whole template upload is refused. `hub-i18n.py` checks for this since 2026-09-24.
- **The hero's text follows the banner's quiet zone.** Argireline's banner is quiet on the left, so its text is left-aligned. PDRN's is quiet in the centre, so its text stays centred. Either way the subtitle is the template's **one-line promise with no number**, because the key figures sit directly below it. A long subtitle ran onto the busy helix at 2.85:1 contrast.
- **Card images must not claim what the text does not.** A render of PDRN travelling into the dermis illustrated a lab result, and register §3 lists "reaches the dermis" as a claim to avoid. A null-result card showed our own serum. (Superseded the same day: there is no null-result card any more; see ADR-2026-09-24-P.)
- **Every image in the page's own content carries the ingredient's name in its filename** (Malcolm, 2026-09-24: "all images used on this page must have names optimized for PDRN"). To use an image that lives under another name (another ingredient, the philosophy page), upload a copy under the ingredient's name. Never rename the original: translations and other pages key off its URL. The exception is the *Explore More Research* tiles, which show and link to the other ingredients and keep those names. PDRN audited clean on 2026-09-24: 11 content images, all `skingenetix-pdrn-…`.
- **Run the design critic before calling a page done.** PDRN cycle 1 scored FIX 6.50 and caught all of the above. Its template-level proposals are with Malcolm (`docs/todo.md` CONTENT-001).

---

## 7. What each of the other four pages has today (read live, 2026-09-24)

| Page           | Template file                  | Sections | Differs from the template                                                                                                                                                                                                                                             |
| -------------- | ------------------------------ | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| PDRN ✅ on the template 2026-09-24 | `page.pdrn-research`           | 15       | rich-text `overview` and `evidence`; findings split across `key_findings_ba` (1 card) and `key_findings` (`media-with-text`, 2); `media-with-text` usage; `specification-table` (10 rows) + `references`; a `findings_spacing_fix` style section at the end (ADR-006) |
| Copper peptide | `page.research-copper-peptide` | 14       | a `hero_banner_css` style section after the hero; rich-text overview and evidence; `key_findings` as `media-with-text` (3); `media-with-text` usage; `specification-table` (10) + `references`                                                                        |
| Matrixyl 3000  | `page.research-matrixyl`       | 13       | rich-text overview and evidence; `key_findings` as `media-with-text` (3); `media-with-text` usage; `specification-table` (7) + `references`                                                                                                                           |
| Glutathione    | `page.glutathione-research`    | 16       | findings split across `key_findings_ba1`, `key_findings` and `key_findings_ba3`; `media-with-text` usage; `specification-table` (10) + `references`; `findings_spacing_fix`                                                                                           |

All four still credit the author as "By Skingenetix" only; the named author line arrives with the template. Each keeps its own chart palette (PDRN `#9E4F5C`, copper `#014EB1`, Argireline `#3E4A52`).

---

## 8. The pilot's gate, and what was decided

The merge plan (`docs/decision-evidence-sections-merge-2026-09-23.md` §4) set a rollout gate: the external audit stays ≥ 9.0 and does not fall below 9.70, and `page-audit.py` does not drop in any area. Measured result:

| Measure                                        | Before the pilot    | After (round 5)                       | Gate                                                                            |
| ---------------------------------------------- | ------------------- | ------------------------------------- | ------------------------------------------------------------------------------- |
| External, combined                             | 9.70                | **9.68** (ChatGPT 9.65 · Gemini 9.70) | ≥ 9.0 met; "not below 9.70" missed by 0.02                                      |
| Author · medical review · recency              | 9.5 · 10 · 10       | 10 · 10 · 10                          | improved                                                                        |
| Heading hierarchy                              | 9.0                 | 8.5                                   | the key-figures band renders as standalone `<h2>`s (ADR-2026-09-23-T, accepted) |
| `page-audit.py` SEO · GEO · DESIGN · MARKETING | 98 · 100 · 100 · 93 | 98 · **96** · 100 · 93                | GEO −4: links inside the table                                                  |

So the gate as written was **not met on two counts, both small**. Malcolm then adopted the page as the template on its merits (above). Recorded so the next rollout knows the trade it is making.

---

## 9. Known loose ends on the reference page

- ~~Dead CSS for the old media-with-text overview in `evidence_sources`.~~ Removed 2026-09-24.
- ~~JSON-LD `citation[]` 8 works against 10 table rows.~~ 2026-09-24: Hoppel 2015 added (9). The Lipotec trade-press study stays out of `citation[]` because it is not a scholarly article.
- ~~JSON-LD `inLanguage: "en"` and the English URL on all five translated pages.~~ Fixed live 2026-09-24 (verified on /de/ and /it/ with curl).
- FAQ q3 calls the peptide "gentle … generally well tolerated", and q5 claims "measurable improvements from day 15 … additional cumulative benefits beyond 28 days". Both belong to the open "gentle / well tolerated" sweep (`docs/todo.md` CONTENT-001) and need checking at source.
- The three key figures render as standalone `<h2>`s, a theme behaviour accepted in ADR-2026-09-23-T.

Any edit to the English of `evidence_sources`, `overview`, `evidence` or `usage` must go through `scripts/hub-i18n.py` (§5).

---

## 10. Page quality gate (Rule 27), mapped

| Check            | How the template carries it                                                                                                                                                                                                                                                                                                                                |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **A** Design     | Fixed section rhythm with Bone/White alternation; no repeated treatment (numbered index ≠ step timeline ≠ table); buttons about 49px tall by construction (16px padding top and bottom, 15px text, 1px border; not yet measured live); every custom section has its own mobile layout. Still needs the measure + design-critic step per page (§6 step 11). |
| **B** Content    | Every sentence from the claims register; positive results only on cards and index rows; verbatim titles; paraphrased disease and mechanism wording.                                                                                                                                                                                                                                    |
| **C** SEO        | One H1 in the hero; query-shaped H2s (_What Is X?_, _What Does X Do for Y?_, _How to Use X_); links up to Science, across to the four siblings, down to the product.                                                                                                                                                                                       |
| **D** Conversion | Proof first (key figures), one primary action (_Shop X_) beside the proof, repeated in the CTA; the quiet second step is the evidence table.                                                                                                                                                                                                               |
| **E** GEO        | Answer-first bold definition; _At a glance_; a real `<table>`; author, reviewer and date in the extractable prose flow; WebPage JSON-LD with `citation[]`.                                                                                                                                                                                                 |

Related: `docs/content-plan-2026.md` §4 · `docs/decision-evidence-sections-merge-2026-09-23.md` · `docs/decisions-log.md` (ADR-2026-09-23-G, -T, -2026-09-24-S) · `docs/claims/` · `configs/hub-upgrades/acetyl-hexapeptide-8-{layout,evidence-merge}-2026-09-23.json` · `configs/hub-i18n/acetyl-hexapeptide-8-research.json`.
