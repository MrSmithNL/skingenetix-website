# Decision: Clinical studies becomes a blog — one article per study, listed like Hairgenetix

**Date:** 2026-09-29 · **Asked by:** Malcolm: "what i meant with the hub page … is more a article blog page where we show all the articles in
a blog list style. Like Hairgenetix set up … Analyse this — also from SEO and content strategy perspective — and decide on the best solution.
also this Clinical studies overview/hub page should be in the main website navigation right? under the 'Discover' main menu section?"
**Amends:** ADR-2026-09-29-C (name kept; page type, URL and menu placement change). **Status:** decided, approved (Malcolm: "Yes, build the blog and
move them") and **built 2026-09-29**: blog live with four articles, old addresses 301 to the articles (locale-aware), table page
retired. Still gated on translation: the Discover menu item, footer link and Science-page band.

---

## 1. The decision

1. **"Clinical studies" is a Shopify blog, `/blogs/clinical-studies`, shown as a list of article cards.** One article per study we have
   appraised: its picture, the question it answers, the study and year, one line of what it found, and the date.
2. **The four study pages move into it as articles.** The designed study layout moves with them onto the article template, fed by the same
   fields. Each old address `/pages/study/<name>` gets a permanent redirect.
3. **The 32-row graded table page is retired before it is published.** Every row already lives in the Evidence & Sources table of its
   ingredient page; the blog's intro links to those five tables.
4. **Menu:** ~~under Discover~~ **under Science** (Malcolm's instruction later the same day; live, see decisions log). Originally: "Clinical studies" goes under Discover, beside The Science, as a plain menu item. This replaces the line under the Science tiles
   approved this morning. The footer link and the band on the Science page stay.

## 2. Why a blog list is the right overview

| Question                                       | Blog list (decided)                                                                                                                                    | The graded table page (retired)                                     |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------- |
| What a visitor expects from "Clinical studies" | A list of readable articles, each a study explained, the pattern Hairgenetix, SkinCeuticals and every editorial site use                               | A dense 32-row table: useful to a researcher, heavy as a front door |
| Unique content                                 | Each article is original analysis, the unit that earns citations                                                                                       | Every row duplicates a table already on an ingredient page          |
| Built with                                     | The theme's own blog list: banner, featured first article, excerpts, dates, authors, optional ingredient tags. **Stock sections**, Malcolm's firm rule | Custom code for five tables                                         |
| Grows without rework                           | Publish an article and it appears in the list, in every language                                                                                       | A generator must be re-run                                          |
| Signals search and AI engines read             | Every article carries a published and updated date (freshness is a measured AI-citation factor); the list is a clean crawl path; an RSS feed           | One large page                                                      |
| Reuse elsewhere                                | The stock "blog posts" section can show the latest studies on the Science page, the hubs and the homepage, which is internal linking at no cost        | None                                                                |

## 3. The SEO and content-strategy checks

- **The folder does not move rankings** (Google Starter Guide; our 2026-09-22 SERP tally). So the move is judged on the visitor, the build and
  what the page type provides, and all three favour the blog.
- **Cannibalisation, the risk Hairgenetix showed.** Its study articles ranked for bare ingredient names and outranked their own pillar. The
  guards are unchanged:
  - article titles lead with the question, never the bare ingredient name (the builder enforces it);
  - each article links up to its hub with the head-term anchor;
  - the list page's H1 is "Clinical studies", not an ingredient;
  - the tripwire stands: a study page holding more than 30% of its hub's head-term impressions is de-optimised.
- **Two blogs, not one.** Hairgenetix mixes study write-ups and buyer's guides in one blog. Our 2026-09-22 decision keeps practical how-to
  articles in `/blogs/learn`, so study appraisals get their own blog and a menu label that says exactly what is inside.
- **Tag archives.** With about six articles, ingredient filter pages would be thin near-duplicates, and the theme cannot mark them noindex
  without a core edit. Tags stay off until there are about twelve articles.
- **Moving the four live pages costs almost nothing.** The site is pre-traffic (541 impressions in 90 days, sitewide), two of the four pages
  are old pilots due for a rebuild anyway, and a 301 carries whatever they have.
- **Six languages.** Article titles, bodies, excerpts, SEO fields and custom fields are all translatable in Translate & Adapt, as the study
  pages are today.

## 4. Menu: under Discover, and why that is the better home

|              | Under Discover (decided)                                              | A line under the Science tiles (approved this morning)                                        |
| ------------ | --------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| Build        | A normal menu item: stock, translatable, no code                      | A styled bar under the image tiles: custom CSS in the sitewide stylesheet                     |
| Fit          | Beside "The Science", the page that explains how we read the research | Next to the five ingredient tiles, where it reads like a sixth ingredient unless styled apart |
| Search value | The same: a sitewide menu link                                        | The same                                                                                      |

"Discover" is still one of NN/g's vague labels, and it still duplicates "Science" (both open `/pages/the-science`). That is a separate
decision, not made here.

## 5. What happens next

1. Create the blog `clinical-studies` and its list template: an intro that answers what the page is, the article cards, the grading key,
   and links to the five ingredient evidence tables.
2. Move the study template onto `templates/article.clinical-study.json` with article custom fields, and rebuild each study as an article in
   six languages (Badenhorst, Raikou, then Wang and Ye on the new layout).
3. Redirect the four `/pages/study/*` addresses.
4. Card images: the ingredient's dark model banner, a different candidate for each article, from the product banner libraries (no new
   generation).
5. Go live together in six languages: the Discover menu item, the footer link, the Science page band and the study breadcrumbs.
6. Retire `templates/page.clinical-studies.json` and its generator; they were never published or linked.

Related: `docs/decision-research-section-navigation-2026-09-29.md`, `docs/decision-learning-centre-2026-09-22.md`,
`docs/study-inventory-2026-09-24.md` §3 (the Hairgenetix data).
