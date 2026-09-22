# Page audit — `/pages/the-science`

**Date:** 2026-09-22 · **Tool:** `scripts/page-audit.py` · **Live:** https://www.skingenetix.com/pages/the-science

| Area | Score |
|---|---|
| SEO | **79/100** |
| GEO | **53/100** |
| DESIGN | **94/100** |

## SEO

| | Check | Detail |
|---|---|---|
| ✅ | HTTP 200, no redirect | 200 → https://www.skingenetix.com/pages/the-science |
| ✅ | Clean URL (lowercase, hyphens, no params, ≤ 60 chars) | /pages/the-science |
| 🟡 | URL carries the head term | head term 'peptide skincare' |
| ✅ | Title present, 30–60 chars | 59c: Learn About Peptide Skincare and the Research / Skingenetix |
| ✅ | Title contains head term | 'peptide skincare' |
| ✅ | Meta description 70–160 chars | 147c |
| 🟡 | Meta description contains head term |  |
| ✅ | Indexable (no noindex) | no robots meta |
| ✅ | Self-referencing absolute canonical | https://www.skingenetix.com/pages/the-science |
| ✅ | hreflang for all 6 locales + x-default | 7 alternates |
| ✅ | Open Graph title/description/image/url | complete |
| ✅ | og:title matches the page title | Learn About Peptide Skincare and the Research / Skingenetix |
| 🔴 | Exactly one <h1> | none |
| 🟠 | <h1> contains head term |  |
| ✅ | Topic headings are real <h2> (≥ 3) | 4 <h2>: ['Our Evidence Standard', 'Clinically Studied Active Ingredients', 'Frequently Asked Questions', 'Experience the Research'] |
| ℹ️ | Visual-only headings (styled <p>/<span>) | 7 that look like headings but are not: ['The Research Behind Our Formulas', 'Copper Peptide GHK-Cu', 'Acetyl Hexapeptide-8', 'Matrixyl 3000', 'PDRN', 'Glutathione', 'Our Transparency Commitment'] |
| ✅ | No skipped heading levels | clean |
| ✅ | Content images have alt text | 26/26 |
| ✅ | Images declare width/height (CLS) | 0 without |
| ✅ | Internal links in content ≥ 5 | 29 unique |
| ✅ | All JSON-LD parses | 0 invalid block(s) |
| 🟠 | No duplicate schema types | duplicates ['BreadcrumbList'] |
| ✅ | BreadcrumbList present |  |
| 🔴 | FAQ schema matches visible questions | 3 Qs; not visible: ['Are peptides clinically studied to improve skin?', 'What concentrations does Skingenetix use?'] |
| ✅ | Page listed in XML sitemap |  |

## GEO

| | Check | Detail |
|---|---|---|
| ✅ | No links inside tables (AI extraction drops the table) | 0 found |
| ✅ | Page entity schema (WebPage/Article) with dateModified | WebPage modified 2026-09-05 |
| 🟡 | Schema cites sources (citation[]) | 0 citations |
| ℹ️ | Reviewer/author in schema (reviewedBy/author) | pending Dr Bodde's review |
| 🔴 | A10 · head term in first 30% of text | 'peptide skincare' |
| 🔴 | A1 · definition sentence early ('X is a …') |  |
| ✅ | A8 · secondary intents covered on the page | ['research'] / ['research'] |
| ✅ | A2 · atomic paragraphs (none > 120 words) | 16 paragraphs, 0 too long |
| ✅ | F2 · snippet-sized answer blocks (35–70 words) ≥ 3 | 4 |
| ✅ | A3 · fact density (measured figures ≥ 5) | 10 figures |
| ✅ | A3 · cited sources ≥ 3 | 5 citation markers |
| ✅ | E3 · cites recent research (2024+) | latest 2026 |
| ✅ | E1 · visible last-reviewed/updated date | Reviewed On |
| ✅ | A6 · structured list or table present |  |
| 🟡 | A4 · headings mirror search questions | 0 question-form H2 |
| 🔴 | D7 · extractable text without JavaScript ≥ 600 words | 413 words extracted (main text 776) |
| 🔴 | Head term survives extraction |  |
| 🟠 | H2 sections survive extraction | lost: ['Our Evidence Standard'] |
| ✅ | D1 · robots.txt allows the major AI crawlers | all allowed |
| ✅ | llms.txt present (evidence: fetched 0× by frontier crawlers — not scored) |  |

## DESIGN

| | Check | Detail |
|---|---|---|
| ✅ | No blank band between header and first section | 0px |
| ✅ | No empty-but-tall sections | none |
| ✅ | Section backgrounds alternate | Bone → rgb(247, 247, 247) → Bone → White |
| 🟡 | Backgrounds on the brand palette | off-palette ['rgb(247, 247, 247)'] |
| ✅ | No horizontal overflow (desktop) | 0px |
| ✅ | No broken images (desktop) | none |
| ✅ | Headings never break mid-word (desktop) | none |
| ✅ | No horizontal overflow (mobile) | 0px |
| ✅ | No broken images (mobile) | none |
| ✅ | Headings never break mid-word (mobile) | none |

## Outline as served

- **H1:** []
- **H2:** ['Our Evidence Standard', 'Clinically Studied Active Ingredients', 'Frequently Asked Questions', 'Experience the Research']
- **Visual-only headings:** ['The Research Behind Our Formulas', 'Copper Peptide GHK-Cu', 'Acetyl Hexapeptide-8', 'Matrixyl 3000', 'PDRN', 'Glutathione', 'Our Transparency Commitment']
- **Schema types:** ['BreadcrumbList', 'WebPage', 'Organization', 'BreadcrumbList', 'FAQPage']
- **Extracted words (no JS):** 413 of 776

## Section map (desktop)

| Top | Height | Section | Type | Background |
|---|---|---|---|---|
| 126 | 0 | schema_markup | custom-html | Bone |
| 126 | 440 | hero | image-with-text-overlay | Bone |
| 566 | 477 | research_standard | text-with-icons | Bone |
| 1042 | 1656 | ingredients_overview | multi-column | rgb(247, 247, 247) |
| 2698 | 500 | transparency | image-with-text-overlay | Bone |
| 3198 | 625 | faq | accordion-content | Bone |
| 3823 | 909 | products_link | featured-collection | White |
| 4733 | 516 | footer | footer | Bone |
| 5249 | 0 | brand_layout_css | custom-html | Bone |
