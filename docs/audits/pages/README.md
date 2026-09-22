# Page audits — SEO · GEO/AISO · Design

**Standard (Malcolm, 2026-09-22):** every page is validated in a live browser, checked against the design
system, and audited for SEO, GEO and AISO — URL, technical and on-page factors, HTML tagging — to the highest
quality standard. Image needs become to-dos.

**Tool:** `scripts/page-audit.py <path> [<path> …]` → one `<slug>-<date>.md` + `.json` per page here, plus
desktop (1440) and mobile (390) full-page screenshots in `/tmp/audit-<slug>/`.

**What it scores**

| Area | Basis |
|---|---|
| **SEO** | Google Search Central: HTTP 200, clean URL, title 30–60 with head term, description 70–160, indexable, self-canonical, hreflang ×6 + x-default, Open Graph, exactly one `<h1>` with head term, ≥3 real `<h2>`, no skipped levels, image alt + dimensions, ≥5 internal links, valid non-duplicated JSON-LD, FAQ schema matching visible questions, sitemap |
| **GEO / AISO** | The agency 36-factor AISO model (page-level factors), re-weighted by `docs/research-2026-ai-search-and-content-hubs.md`: head term in first 30% (A10, weight 3), extractable text without JS ≥ 600 words (D7, 3), definition sentence early (A1), secondary intents covered (A8), fact + citation density (A3), page entity schema with `dateModified`, visible updated date (E1), headings survive extraction, AI crawlers allowed (D1). **Not scored** where 2026 evidence is null or negative: llms.txt, FAQ-schema weighting, Q&A genre, publishing cadence |
| **Design** | Live Chromium at 1440 and 390 px: no band under the header, no empty-but-tall sections, backgrounds alternate on the palette (Bone `#F0F0F0` / White / Graphite `#1A1A1A`, `docs/visual-identity`), no horizontal overflow, no broken images, no heading broken mid-word |

---

## Scores — 2026-09-22

| Page | Before | After |
|---|---|---|
| `/pages/pdrn-research` | *(upgraded before the tool existed)* | **SEO 100 · GEO 100 · Design 100** |
| `/pages/acetyl-hexapeptide-8-research` | SEO 81 · GEO 65 · Design 84 | **SEO 98 · GEO 100 · Design 100** |
| `/` | SEO 84 · GEO 61 · Design 84 | — |
| `/pages/the-science` | SEO 79 · GEO 53 · Design 94 | — |
| `/pages/copper-peptide-research` | SEO 90 · GEO 77 · Design 84 | **SEO 100 · GEO 100 · Design 100** |
| `/pages/matrixyl-3000-research` | SEO 90 · GEO 86 · Design 84 | — |
| `/pages/glutathione-research` | SEO 90 · GEO 86 · Design 84 | — |
| `/pages/fine-lines-wrinkles` | SEO 90 · GEO 81 · Design 90 | — |
| `/pages/firming-skin-density` | SEO 88 · GEO 81 · Design 90 | — |
| `/pages/skin-repair-renewal` | SEO 88 · GEO 74 · Design 81 | — |
| `/pages/brightening-glow` | SEO 88 · GEO 81 · Design 90 | — |
| `/collections/pdrn` | SEO 93 · **GEO 28** · Design 90 | — |
| `/collections/serums` | SEO 92 · **GEO 39** · Design 90 | — |
| `/products/pdrn-renewal-serum` | SEO 94 · **GEO 47** · Design 84 | — |
| `/products/copper-peptide-ghk-cu-renewal-serum` | SEO 90 · **GEO 40** · Design 84 | — |
| `/products/matrixyl-3000-firming-serum` | SEO 98 · **GEO 51** · Design 84 | — |
| `/products/acetyl-hexapeptide-8-anti-wrinkle-serum` | SEO 82 · GEO 58 · Design 84 | title now carries Argireline® 10% |

Remaining on the Argireline page: the URL does not carry "argireline". **Deliberately not changed** — URL
structure is "a very, very lightweight ranking factor" (Google) and this page holds 1,014 of the site's 2,065
impressions; a redirect would risk that for almost nothing.

---

## Site-wide patterns — fix once, not page by page

| # | Pattern | Pages | Fix (standard sections, no Liquid) |
|---|---|---|---|
| 1 | **No real `<h1>`.** Impact renders every heading block as `<p class="h1">` | 8 designed pages | Move the hero title into the hero richtext as `<h1>` (proven on PDRN + Argireline) |
| 2 | **Backgrounds don't alternate** — theme default is Bone everywhere | 14 | Set section backgrounds Bone/White around the fixed-Bone findings sections |
| 3 | **No page-entity schema, no visible "last updated"** | 14 | WebPage JSON-LD inside an existing content section (never its own section) + an italic updated line |
| 4 | **Thin for AI on product and collection pages** — < 600 extractable words, no early definition | 7 | Product-page completeness (strategy §3.1): answer-first description, ingredient explainer, how-to, FAQ — a separate workstream |
| 5 | Topic headings are visual-only `<p class="h2">` | most | `<h2>` inside richtext |
| 6 | Off-palette backgrounds (`#F7F7F7` references blocks) | 9 | Set to Bone |
| 7 | `/pages/the-science`: FAQ schema does not match the visible questions; duplicate schema types on `/` and `/pages/the-science` | 2 | Rebuild the-science as the Learn front door (waits for first articles) |
| 8 | Mid-word heading break on mobile | skin-repair-renewal | Shorter heading words |

---

## Image to-dos (from the visual reviews)

| Page | Need | Why | Priority |
|---|---|---|---|
| `/pages/acetyl-hexapeptide-8-research` | **Mechanism illustration** for "What Does Argireline Do for Expression Lines?" — nerve ending → SNARE complex → muscle, in the clinical-luminism style, Pearl grey `#D8D6D4` | The section is text-only and explains a mechanism; the copper and Matrixyl pages already carry mechanism explainers. AISO A9 (multi-modal) | Medium |
| `/pages/pdrn-research` | Optional image for "Salmon DNA: Where PDRN Comes From" — abstract DNA strand / purification, Blush `#F3BFC2`. **No literal fish** (clinical luminism: one subject, no botanicals or food) | Long text-only section; A9 | Low |
| All remaining hubs | Assess during each upgrade | — | — |

⛔ **Not a to-do:** the before/after diptychs. Malcolm, 2026-09-22 — no illustration/AI disclosure; see memory
`no-ai-disclosure-on-before-after-images`.

---

## Claims verified at source during the audits

| Claim on the site | Source | Verdict |
|---|---|---|
| PDRN: ~20% softer-looking crow's feet in 28 days (split-face, 31 women) | Ye et al. 2026, PLOS ONE — full text | ✅ Accurate. **Study used 0.1% PDRN-850K, not 1%** — now stated on the page |
| AH-8: 48.9% vs 0% placebo (60 subjects, 4 weeks) | Wang et al. 2013, PMID 23417317 | ✅ Accurate. **An efficacy *rate* from subjective assessment, not a 48.9% reduction** — now worded that way |
| AH-8: up to ~30% wrinkle depth in 30 days | Blanes-Mira et al. 2002, PMID 18498523 | ✅ Accurate — developers' study, **10% hexapeptide emulsion** |
| AH-8: 14.6% improvement in 5 days | An et al. 2019, PMC7992733 — full text | ✅ Accurate — day 5, fine wrinkles, **microneedle patch** (card already says so) |
| AH-8: delivery limits results | Zdrada-Nowak et al. 2025, PMID 40565185 | ✅ Accurate, and stronger: reaching the nerve–muscle junction topically "remains uncertain" — now on the page |
| Copper: first isolated from human plasma in 1973 | Pickart PhD thesis, UCSF 1973 — cited in Pickart 2015 (PMC4508379) and 2018 (PMC6073405) | ✅ Accurate |
| Copper: plasma GHK ~200 ng/mL at 20 → 80 ng/mL by 60 | Pickart 2015 and 2018 — full text | ✅ Accurate. **Both reviews are by Skin Biology, a GHK-Cu product company** — now stated on findings card 1 |
| Copper: findings card 3 — "controlled trial, 12 weeks, greater satisfaction vs control" | Miller et al. 2006, PMID 16847171 | ❌ **Misleading.** 13 patients **after CO2 laser resurfacing**; blinded measurements found **no difference** in redness, wrinkles or skin quality; only the questionnaire differed (p = .04). Card rewritten to say all of that |
| Copper: FAQ "2% is at the upper end of the clinically studied range (0.5–2%)" | Searched Pickart 2015, 2018, Mortazavi 2024 full texts | ❌ **No source.** Removed; the answer now says most studies do not state a concentration |
| Copper: FAQ "well-tolerated, including by sensitive skin" | No source found | ❌ Removed; replaced with an honest patch-test answer |
| Copper: "one of the most-studied peptides in skin science" (card 1, FAQ 1) | Mortazavi et al. 2024, PMID 39963574 | ❌ Contradicted — the review finds "a surprising absence of clinical studies". Removed; the page now grades evidence by strength |
| Copper: collagen in 70% vs 50% vitamin C vs 40% retinoic acid | Abdulghani 1998, via Mortazavi 2024 and Pickart 2015 | ✅ Accurate — **thigh biopsies, 10 people per group, one month** (Pickart 2018 says 12 weeks; two of three sources say one month) |
| Copper: 12-week face (71 women) and eye (41 women) studies | Leyden et al. 2002, via Pickart 2015 | ✅ Reported — but **AAD 2002 meeting proceedings, never published as full papers**; stated on the page |
| Copper: collagen IV doubled with hyaluronic acid | Jiang et al. 2023, PMID 37062921 | ✅ Accurate — ×2.03 **ex vivo** (×25.4 in cells); authors from ingredient makers |
| Copper: keratinocyte growth, integrin, p63 | Kang et al. 2009, PMID 19319546 | ✅ Accurate — lab skin models only |
