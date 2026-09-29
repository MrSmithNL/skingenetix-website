# Decision: where the research lives — a "Clinical studies" section under Science

**Date:** 2026-09-29 · **Asked by:** Malcolm — "where can you find the scientific/research articles on the website navigation?
there should be an articles or research section right? … design the best solution based on what the SEO, GEO and AISO strategy
and research says". **Status:** analysed and designed; **nothing changed on the live site**. Each numbered design element in §4
needs its own go-ahead (navigation changes are site-wide).
**Approved 2026-09-29 (ADR-2026-09-29-C):** the name "Clinical studies", the placement (Science menu line, footer, the-science), the
study-page breadcrumb, and building now in English, unpublished, with nothing linked until translated.

---

## 1. Short answer

**There is no research section today.** A visitor cannot find a study page from the menu, the footer, the Science front door or
a product page. Each study has one way in: a single in-sentence link on its ingredient hub. Raikou 2017 has none at all. The
index page the strategy planned (`/pages/evidence-library`) was never built and returns 404. The "Learn" blog exists but holds
zero articles.

**Recommended:** one research section: a **Clinical studies** page (`/pages/clinical-studies`), reached from **one new line
inside the existing Science menu**, the footer and the Science front door. The study pages sit beneath it, with a visible
breadcrumb. No new top-level menu item, and no split of the menu.

---

## 2. What we found (live audit, 2026-09-29; 32 pages fetched, menus read from the Admin API)

```
Header "Science" (every page) ──> 5 ingredient hubs (image tiles)
   pdrn-research ─────────────> Ye 2026 study          (1 in-sentence link)
   acetyl-hexapeptide-8 ──────> Wang 2013 study        (1 in-sentence link)
   copper-peptide-research ───> Badenhorst 2016 study  (1 in-sentence link)
   matrixyl-3000, glutathione > (no study pages exist)
/pages/the-science ──────────> the 5 hubs only
Raikou 2017 study ───────────> linked from nowhere (sitemap only)
/pages/evidence-library ─────> 404
/blogs/learn ────────────────> empty ("This blog is empty"), but listed in the sitemap
```

| Page                    | Clicks from the homepage (crawler) | Desktop visitor                                   | Phone visitor |
| ----------------------- | ---------------------------------- | ------------------------------------------------- | ------------- |
| The-science, the 5 hubs | 1                                  | 1                                                 | 3 taps        |
| Wang, Ye, Badenhorst    | 2                                  | 2, via one link a quarter of the way down its hub | 4 taps        |
| Raikou                  | unreachable                        | unreachable                                       | unreachable   |

- **Menus.** Main: Shop · Skin Solutions · **Science** · Discover · Support. Science holds the five hubs as image tiles. Discover
  also points at `/pages/the-science` (The Science, Ingredients, Our Philosophy), so the two overlap. Footer Explore: The
  Science, Our Ingredients, Our Philosophy. Nothing points at a study, the blog or a library.
- **No page lists the studies.** Each hub's "See all N studies" jumps down its own page, and those rows link to PubMed.
- **Product pages** link to their hub ("See all the PDRN research →"), never to a study.
- **The homepage cites "48.9% … (Wang 2013)"** in its numbers band without linking the Wang appraisal.
- **Breadcrumbs:** none visible anywhere. Study pages carry a BreadcrumbList with one item ("Home"); hubs skip The Science.
- **llms.txt** is Shopify's auto-generated shopping-agent file and lists no content pages.
- **Comparison, the sister store:** Hairgenetix has a top-level "Scientific research" menu with its hubs and a "Research articles"
  link to `/blogs/articles`.

Raw evidence: the audit's HTML and link maps (session scratchpad, 2026-09-29).

---

## 3. What the research and our strategy say

| Principle                                                                                                         | Evidence                                                                                                                                                                                                                                              | Strength                           |
| ----------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------- |
| **One consolidated evidence hub, reachable from the main navigation**                                             | SkinCeuticals (Clinical Studies, in the global nav; its agency case study says deep-link-only content was not being found), Augustinus Bader (`/evidence/…`), Examine.com (one evidence view per topic)                                               | Observed + agency case study       |
| **Don't promote individual study pages in the menu**                                                              | At Hairgenetix, study pages ranked as the ingredient's authority page (~75% of their impressions from bare ingredient names) and outranked their own pillar (5.1 and 8.6 against 28.5). Sitewide menu links are discounted as boilerplate and dilute. | Our own GSC data + Google guidance |
| **Hubs stay the authority** for the head terms (`pdrn`, `argireline`…); studies link up with the head-term anchor | `research-2026-study-hubs-credibility.md` linking rules; cannibalisation tripwire >30% of a hub head term                                                                                                                                             | Our strategy                       |
| **Shallow, well-linked structure** helps crawling; orphans die                                                    | Google (Illyes, 2025, crawl efficiency); our research note that an orphaned page dies; a pillar with 1 inbound link sat at position 10.6                                                                                                              | Primary + observed                 |
| **Descriptive labels beat vague ones**                                                                            | NN/g: "Learn", "Explore", "Discover" are ineffective category names                                                                                                                                                                                   | Primary research                   |
| **"Clinical studies" matches how people search**                                                                  | Evidence-shaped queries reaching study pages use "study / clinical / trial"; `pubmed acetyl hexapeptide-8 … randomized trial` already reaches us at position 7–8                                                                                      | Our GSC data                       |
| **The index is the most citable asset** for AI engines: one page, every study, graded, dated                      | `research-2026-study-hubs-credibility.md` §3; Google's AI-features guidance names findability through internal links                                                                                                                                  | Our strategy + primary             |
| **Listing-page schema:** CollectionPage + ItemList; BreadcrumbList for hierarchy                                  | schema.org; Google's structured-data guidance                                                                                                                                                                                                         | Primary                            |
| **llms.txt is not a lever**                                                                                       | Server-log studies of ~900 domains: 0 AI-crawler fetches in 1,227 requests; Ahrefs: 97% of files never requested                                                                                                                                      | Measured, third party              |

The folder a page sits in does not move rankings (Google Starter Guide; our 2026-09-22 SERP tally found no structure winning), so
the study pages stay where they are.

---

## 4. The design

### 4.1 The Clinical studies page — `/pages/clinical-studies`

The planned "Evidence Library", named for what visitors look for.

- **H1** "Clinical studies". **Answer-first paragraph** (quotable, 40–60 words): what the page is, the count, how studies are
  graded and that the key trials are written up in full.
- **How we grade**, in one line: A controlled human trial measured by instrument · B smaller, uncontrolled or manufacturer
  data · C tests on skin samples · D cell studies · Review a summary of other work. This is the grading the hubs already use;
  the 25 Sep proposal to add a site-wide scale is still open.
- **A plain-text jump line** to the five ingredients, not pills.
- **One section per ingredient**, reusing the hubs' own Evidence & Sources table (the same component, look and vetted rows).
  - Each row: study title as published, authors and year, journal, grade and what it found.
  - **"Read our appraisal →"** where a study page exists, then **"View on PubMed →"**.
  - Each section opens with one line linking to its hub with the head-term anchor.
- **Scope follows ADR-2026-09-24-P:** the rows are the hubs' tables, which already exclude null and non-transferable studies:
  PDRN 4, Argireline 8, copper 6, Matrixyl 9, glutathione 5, **32 in all**. Matrixyl's table appears when its hub is live on the
  template.
- **Schema:** CollectionPage → ItemList of the study pages; BreadcrumbList Home › Science › Clinical studies; `dateModified`
  and `reviewedBy` as on the hubs.
- **Build rung:** a stock page template with the tables as custom-html, the same forced rung as the hubs' evidence tables
  (stock sections cannot render a three-column table). The rows are generated from the five hub specs by a script, so a change
  to a hub's table reaches the index.

### 4.2 Navigation — one line, three places

1. **Science mega-menu:** one new link, **"All clinical studies"**, rendered as a full-width line under the five image tiles on
   desktop and as the sixth line in the phone drawer. There is **no new top-level item and no split**; the tiles are unchanged.
2. **Footer, Explore:** add "Clinical studies".
3. **`/pages/the-science`:** a "Clinical studies" band linking the index and the written-up trials.

Individual study pages are **not** menu items (see §3). The blog is **not** in the menu until it holds at least three articles.
An empty section costs trust.

### 4.3 Study pages — a visible path

- The banner's "Clinical Study · 2017" label becomes a **breadcrumb**: _Science › Clinical studies › Argireline®_. This also
  removes the middle-dot eyebrow the 2026-09-26 critique flagged (T11).
- **BreadcrumbList** with four levels; `isPartOf` points at the index page; one "More clinical studies" link back to the index.

### 4.4 Links into the studies

| From          | Change                                                                                                                                                                                                                                                               |
| ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Each hub      | Study rows link to their appraisal; the first in-prose mention of an appraised trial links to the appraisal instead of PubMed (Raikou is cited 8 times on the Argireline hub, and none links to our page); an "All clinical studies" link beside "See all N studies" |
| Homepage      | The "48.9% (Wang 2013)" figure links to the Wang appraisal                                                                                                                                                                                                           |
| Product pages | The Clinical Research block links the product's lead study appraisal. This touches about 20 products in six languages, which is part of the internal-link programme awaiting a go-ahead since 2026-09-22                                                             |

### 4.5 Clean-ups found on the way

- **The empty Learn blog** is in the sitemap and says "This blog is empty". Hide it until articles exist, or publish the first
  articles.
- **Discover duplicates Science**: both point at the-science, and "Discover" is one of NN/g's vague labels. This is a separate
  decision (the 2026-09-22 menu ruling: change only what is named).
- **An empty duplicate footer menu** (`footer-explore`).

---

## 5. Sequence

1. Build the Clinical studies page in English, unpublished, and review it with the design critic.
2. Translate the index and the four study pages (Badenhorst and Raikou are still English-only).
3. Take the menu line, footer link, breadcrumbs and hub/homepage links live **together in six languages**. A menu link is
   site-wide, and the standing rule is all six languages before anything is linked.
4. Product links follow as part of the internal-link programme.

**Measure** (baseline at go-live, check at 8 weeks): impressions and clicks for the index and each study page; the hubs' head-term
share (tripwire: a study page above 30% of its hub's head-term impressions → de-optimise it).

---

## 6. Architecture placement

- **Where:** a Shopify page and template in this client's store (CLIENT-003 content). The generator script lives in this repo's
  `scripts/`, beside the hub and study builders.
- **Why here:** the content is specific to Skingenetix's ingredients and studies; nothing is reusable by another product.
- **Consumes:** the five hub evidence specs (`configs/hub-upgrades/*evidence-merge*.json`) and the `study` metaobjects.
  **Consumed by:** the Science menu, the footer, `/pages/the-science`, the hubs and every study page's breadcrumb.
- **Already exists?** Planned as `/pages/evidence-library` since 2026-09-22; never built (404). This is that page, renamed.

---

## 7. Mock-ups

Rendered 2026-09-29 by editing the live pages in a local browser only; nothing was written to Shopify:

- the menu before and after, desktop, plus the phone drawer;
- the study-page breadcrumb, desktop and phone;
- the Clinical studies page, desktop and phone.

They are shown on Malcolm's screen as a contact sheet.

Related: `docs/decision-learning-centre-2026-09-22.md` (the science layer and the blog), `docs/decision-citations-study-pages-navigation-2026-09-22.md`
(the Science label), `docs/research-2026-study-hubs-credibility.md` (the Evidence Library plan), `docs/study-inventory-2026-09-24.md`.
