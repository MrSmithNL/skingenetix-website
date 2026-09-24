# Decision + build plan — merging the evidence sections on the science hubs

**Date:** 2026-09-23
**Raised by:** Malcolm — "the 'evidence at a glance' and 'published references' section on all the science pages are very similar. Can they be combined?" and "the 'What the evidence shows' section is also very similar to the content sections with images underneath."
**Decision taken:** pilot the new pattern on the Argireline hub first; roll to the other four only if it holds its audit scores.
**Status:** **built and live** on Argireline (2026-09-23), then adopted as the science-page template. See `docs/science-page-template.md` and ADR-2026-09-24-S. The rollout gate in §4 was missed on two small counts (external 9.68 against 9.70; `page-audit` GEO 100 → 96), and Malcolm adopted the page anyway. See template doc §8.
**Superseded detail:** the built page went further than this plan: an evidence **index** of numbered rows rather than bullets, and the usage section as custom-html with a 3-step timeline rather than `media-with-text`.

---

## 1. What was measured (not assumed)

All figures below were read off the live theme templates and the live rendered DOM on 2026-09-23, not from documentation.

### 1.1 The two evidence lists overlap almost completely

Copper hub, the reference build:

| List | Studies |
|---|---|
| `evidence_table` (Evidence at a Glance) | 11 — Badenhorst, Mokhtar, Abdulghani, Leyden, Miller, Li, Jiang, Kang, Pickart 2015 + 2018, Mortazavi |
| `references` (Published References) | 11 — the same, minus Leyden, plus Wang J 2026 |
| **Shared** | **10 of 11** |

The two divergences are explicable rather than accidental: Leyden 2002 was never published in full, so there is nothing to link; Wang 2026 is cited but never appraised.

Unique content in each:

- **References only:** the verbatim published title and the journal/volume.
- **Evidence table only:** our appraisal — grade, n, design, result, conflicts of interest.

Both carry a link to the same paper. These are two layers of one job.

### 1.2 Correction — the evidence table is not a table

Initially assumed, then disproved against the live DOM:

| Section | `<table>` elements | `<div>` | Exempt `sgref__ti` titles |
|---|---|---|---|
| `evidence_table` (`specification-table`) | **0** | 36 | 0 |
| `references` (`custom-html`) | **0** | 25 | 12 |
| `charts` (`custom-html`) | **2** | 34 | 0 |

`specification-table` renders `<div class="feature-chart__table-row">` despite the class name. The only two real tables on a hub are the chart data tables.

**Consequence:** merging into a `specification-table` would move divs into divs. The AI-extraction benefit that would justify the merge does not exist in that shape. It only exists if the merged section emits a real `<table>`.

### 1.3 The verbatim-title exemption is bound to a CSS class

`scripts/page-audit.py:114–116`:

```
# Only the References list's title element is exempt; a quoted title in prose still counts.
for t in main.xpath('.//*[contains(concat(" ",@class," ")," sgref__ti ")]'):
```

The exemption travels with the class `sgref__ti`, not with the section. Any section that can emit that class keeps the exemption with no tool change.

`specification-table` **cannot** emit it. Its schema is `heading: text` (HTML escaped) and `value: richtext` (Shopify richtext strips class attributes). So a merged section built on the stock table would push verbatim published titles into a scanned element — the exact failure mode recorded in the memory entry `citation-titles-are-quoted-verbatim` ("fix the audit, never the citation").

### 1.4 "What the evidence shows" really is unstructured

Copper `evidence` section, live DOM: **one `<h2>`, zero `<ul>`, zero `<li>`.** The "three strengths of evidence" is running prose. Argireline is the same shape.

Findings cards then restate individual studies with images below.

### 1.5 Anchor links are possible with no theme edit

Block-level DOM ids already exist and are stable per template:

```
block-template--26327026532737__key_findings-f1
```

So a bullet can anchor straight to the image block that expands it. Two caveats:

- The id embeds the **template** numeric id, which differs per hub. Hrefs must be derived at build time from the live template, never hardcoded across pages.
- `hub-upgrade.py --verify-live` only checks `href="/…"`. A broken `#fragment` would fail **silently**.

### 1.6 Findings-card titles are invisible to the document outline

Copper `key_findings` blocks carry their title in the section's `title` setting, which Impact renders as a paragraph. The section contributes **no `<h2>`** to the outline. Free SEO/GEO value is being left on the floor.

---

## 2. Two live claim defects found on the Argireline hub

Found while reading the Argireline findings cards for this plan. Both are forbidden by `docs/claims/argireline-acetyl-hexapeptide-8.md` §3 "Claims to AVOID". Both are live now, in six languages.

### Defect 1 — the 48.9% misread, on our own page

- **Live card f1 title:** "48.9% Overall Anti-Wrinkle Efficacy vs Placebo"
- **Live `result_label`:** "48.9% overall anti-wrinkle efficacy vs placebo"
- **Register §3 forbids:** *"Reduces wrinkles by 48.9%", "49% deeper-wrinkle reduction", "48.9% efficacy" with no explanation* — because 48.9% is **22 of 45 people graded as improved**, not a reduction in anything.
- The register names two published reviews that made exactly this misread and says never to cite them for it.
- The page's own `evidence` prose already states it correctly ("22 of 45 were graded clearly improved… against 0 of 15 on placebo"). **The prose is right and the card is wrong**, on the same page.

### Defect 2 — a microneedle-patch result presented as a serum result

- **Live card f3 title:** "14.6% Improvement in Just 5 Days"
- Source is An 2019, which the register marks: *"**A microneedle device, not a serum. Not transferable.**"*
- It sits as a headline finding card on a leave-on serum page with no statement that it was a dissolving microneedle patch.

Both must be fixed regardless of whether the merge goes ahead. They are inside the §7 autonomy envelope (removing claims found unsupported at source, in all six languages).

---

## 3. The decision

### 3.1 Part A — merge, but into the references section, not the stock table

**Build "Evidence & Sources" by extending the existing `references` custom-html section to emit a real `<table>`, one row per study.** Do not create a `specification-table` for Argireline, and retire it on the other four when they follow.

Each row carries:

| Column | Content |
|---|---|
| Study | Verbatim published title in `<span class="sgref__ti">` + author, year, journal, volume |
| Appraisal | Grade + design + n + result + conflicts (today's evidence-table `value` content) |
| Link | PubMed / DOI, as now |

Why this shape and not the stock table:

- **Keeps the verbatim-title exemption** by class, with no change to `page-audit.py` and no pressure to paraphrase a citation.
- **Is the only shape that actually gains extraction**, because it is the only one that emits `<table>`.
- **Keeps the JSON-LD where it is.** `jsonld_host` stays `"references"` — no relocation, and no risk of the empty-custom-html 160px blank band.
- **Does not add custom code on balance.** `references` is already custom-html; we enrich it and skip creating the stock section. This satisfies the "stock sections before custom code" rule via its stated carve-out: no stock section can do this job.

### 3.2 Part B — bullet summary anchoring to the image blocks

Malcolm's proposal, adopted, with two additions:

1. Open `evidence` with a short bulleted summary — one bullet per finding — each anchoring to the image block below that expands it.
2. Move the findings-card titles into the block richtext as real `<h2>`s so they enter the document outline and become checkable by `--verify-live`.
3. Add a fragment-link check, because a broken `#anchor` is currently silent.

---

## 4. Build plan — Argireline pilot

Order matters: claims before layout, so we never translate wording we are about to withdraw.

| # | Step | Detail | Verify |
|---|---|---|---|
| 1 | Fix the two claim defects | Rewrite f1 away from "48.9% efficacy" to the responder framing ("22 of 45 graded clearly improved; 0 of 15 on placebo"). Either withdraw f3 or re-label it explicitly as a dissolving microneedle patch, not the serum. Six languages. | `page-audit.py` MARKETING ≥ 85 |
| 2 | Re-verify every figure at source | Register §2 rows are dated 2026-09-22. Handover §11 lists Raikou forehead values as inherited, not re-read. Re-open Wang 2013, Raikou 2017, Henseler 2023 before publishing any of their numbers. | Source read logged in the register |
| 3 | Confirm the render contract | Check whether `research-before-after` block titles emit `<h2>`; capture the Argireline template numeric id for the anchor hrefs. | Live DOM |
| 4 | Build "Evidence & Sources" | Ten rows chosen from register §2. Verbatim titles in `sgref__ti`. Merge in the 8 existing reference entries so nothing currently cited is dropped. Real `<table>`. | Row count = studies cited on the page |
| 5 | Bullet summary + anchors | Bullets at the top of `evidence`, anchored to `key_findings_ba` f1–f3. Card titles to real `<h2>`. | Every fragment resolves to a live id |
| 6 | Usage image rows | Split the live translated `usage` rich-text at its two `<h2>`s ("What 10% Argireline® Means", "How to Use Argireline") into a two-image `media-with-text`, from the five existing Argireline images. | Six locales |
| 7 | Backgrounds | Re-alternate from the merged section down. | Visual |
| 8 | Ship and check | Dry run → `link-citations.py --write` → `--apply` **once** → `set-reviewer.py --apply` → `--verify-live` ✓ ×6 → `page-audit.py` → `aiso-audit-page.py --round 3`. | External ≥ 9.0, and **not below today's 9.70** |
| 9 | Show it | Desktop + mobile, tiled to `~/Desktop/skingenetix-renders.png`, `open`ed. | On screen |

### Rollout gate

Roll to PDRN, copper, Matrixyl and glutathione **only if** Argireline holds ≥ 9.0 externally and does not fall below its current 9.70, and `page-audit.py` does not drop on any area. If either slips, the merge stops at one page and the other four keep both sections.

---

## 5. Risks

| Risk | Handling |
|---|---|
| The merge costs audit score on pages already at 9.60–9.82 | That is what the one-page pilot is for. Rollout is gated on the pilot's numbers. |
| A broken `#anchor` fails silently | Add a fragment check; do not rely on `--verify-live`, which only tests `href="/…"`. |
| Verbatim titles lose their exemption | Prevented by keeping `sgref__ti`; this is why the stock table was rejected. |
| Custom code grows | Net neutral — one custom section enriched, one stock section not created. |
| Opportunity cost | Phase 3 (15 spokes) is the growth work and has not started. The pilot is one page, not five. |

---

## 6. What this does not do

- Does not touch the menu (§6 stop condition).
- Does not add any formula-level claim — the parked facts stay parked, ingredient-level only.
- Does not add AI disclosure to before/after images (Malcolm, 2026-09-22 — settled).
- Does not change product titles, prices or inventory.

---

Related: `docs/content-plan-2026.md` §4 (research-page standard), `docs/decisions-log.md` (ADR-2026-09-23-G verbatim citation titles, ADR-2026-09-23-T key figures at the top), `docs/claims/argireline-acetyl-hexapeptide-8.md`.
