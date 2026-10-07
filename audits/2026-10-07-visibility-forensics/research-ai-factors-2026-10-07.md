# AI-citation factors for ingredient-explainer queries — research note, 2026-10-07

Delegated research (brief: the `seo-visibility-forensics` skill's `research/ai-factors-prompt.md`), run for
skingenetix.com. Tiering: T1 = engine documentation or a controlled test; T2 = large correlational study; T3 =
practitioner or small-sample. Every figure carries its source; items the researcher could not verify are listed at the end.

## 1. What decides who gets cited, ranked by evidence strength

1. **Topical match of the title and opening to the question.** T2. Ahrefs, 1.4M ChatGPT prompts, 2026-04-15: cited
   URLs' titles scored 0.602 similarity to the prompt against 0.484 for uncited; natural-language slugs were cited
   89.8% vs 81.1%. https://ahrefs.com/blog/why-chatgpt-cites-pages/
2. **Citations, statistics and quotations in the body.** T1 (controlled, 2023 lab engine). Princeton GEO paper, 10K
   queries: adding sources, quotations and statistics lifted visibility 30–40%; keyword stuffing lowered it; a source
   ranked 5th gained +115% from citations. https://arxiv.org/abs/2311.09735
3. **Brand mentions on third-party sites, not backlinks.** T2. Ahrefs, 75K brands, 2025-05-26 (Spearman): branded web
   mentions 0.664, branded anchors 0.527, branded search volume 0.392, Domain Rating 0.326, backlinks 0.218; 26% of
   brands had zero AI Overview mentions. https://ahrefs.com/blog/ai-overview-brand-correlation/
4. **Organic rank: necessary, no longer sufficient.** T2. Ahrefs, 863K keywords, 2026-03-02: 37.9% of AI Overview
   citations rank top-10, 31.2% rank 11–100, 31.0% beyond 100; YouTube is the most-cited domain (5.6%).
   https://ahrefs.com/blog/ai-overview-citations-top-10/ Academic audit (Xu, Iqbal, Montgomery, 55,393 queries, rev.
   2026-10-01): about 30% of cited domains are absent from organic results and are more credible than page one.
   https://arxiv.org/abs/2605.14021
5. **Freshness.** T2. Ahrefs, 17M citations, 2025-07-28: AI-cited pages are 25.7% fresher than organic; ChatGPT median
   958 days. https://ahrefs.com/blog/do-ai-assistants-prefer-to-cite-fresh-content/ T3: Green Flag Digital, 2026-09-21:
   half of October 2025's most-cited pages had zero citations 11 months later; URLs with a year in the slug lost 80%.
6. **Structured data: no causal effect on citation.** T1. Google: "no special schema.org structured data that you need
   to add" (AI features doc, 2024-12-10). Ahrefs difference-in-differences, 2026-05-11: AI Mode +2.4%, ChatGPT +2.2%
   (not significant), AI Overviews −4.6%. https://ahrefs.com/blog/schema-ai-citations/
7. **Author and reviewer credentials.** T1 for Google ranking via the rater guidelines (§5); no study isolates them as
   an AI-citation cause.
8. **Reviews.** T1 for shopping surfaces only: ChatGPT shopping ranks merchants on availability, price, quality and
   being the maker, with review summaries from public sites; Shopify Catalog feeds it directly. No evidence reviews
   affect explainer citations. https://help.openai.com/en/articles/11128490-shopping-in-chatgpt

## 2. Small brands with no backlinks

No verified case of a zero-backlink skincare brand being cited was found. Nearest evidence: low-authority sites earning
citations through narrow topical depth (Green Flag, 2026-09, T3); 31% of AI Overview citations from outside Google's
top 100 (Ahrefs 2026-03, T2); low-ranked sources gain most from adding citations and statistics (Princeton, T1).
Reading: relevance-matched, evidence-dense pages can be cited without links; brand-level recommendation ("best X
serum") tracks third-party mentions, which take months.

## 3. Reddit, YouTube and listicles in skincare answers

- Reddit is heavily read but selectively cited: 12.6% of ChatGPT Search answers, 9% of AI Mode, 3.5% of Perplexity;
  cited posts are modest Q&A threads about 900 days old (Semrush, 217K prompts, 2025-11-10). Reddit's ChatGPT share fell
  from about 60% to 10% in September 2025 while LinkedIn, YouTube, Forbes and PRNewswire rose.
  https://www.semrush.com/blog/reddit-ai-search-visibility-study/ https://www.semrush.com/blog/most-cited-domains-ai/
- YouTube is the top-cited domain in AI Overviews overall and for health: 4.43% of citations on 50,807 German health
  queries, journals 0.48% (SE Ranking, 2026-01).
- Beauty-specific, T3: editorial titles 42% of citations, SEO blogs 31%, brand-owned sites 6%; Reddit then Allure and
  Vogue most cited; half of citations under 11 months old; Claude cited no social sources (Foundation Agency, 683
  citations, 2026-07-15). 5WPR Beauty AI Visibility Index 2026: The Ordinary 7.0%, CeraVe 6.0%; ingredient-led
  independents 31% of citations; Claude favours clinically credentialed brands.
- How brands get in: Allure Best of Beauty is a paid-entry submission with sample testing; press releases are now
  cited. Caution: Google's spam policies (2026-08-28) define spam to include "attempting to manipulate generative AI
  responses", and site-reputation abuse covers paid third-party placements.
  https://developers.google.com/search/docs/essentials/spam-policies

## 4. Clinical-evidence content

Indirect but consistent: citations, statistics and quotations are the top three controlled GEO methods; cited domains
are more credible than page one; engines rarely cite PubMed itself for consumer queries (0.48%), so the citable layer
is the plain-language page that digests and appraises the named trial, which is the study-page format this site has
built. No head-to-head study of trial-appraisal pages versus generic explainers exists.

## 5. Google's E-E-A-T position (checked against the hosted PDF on 2026-10-07)

- Current Search Quality Rater Guidelines: dated 2025-09-11, 182 pages. Claims of 2026 revisions on marketing blogs
  are not in Google's hosted document.
- Cosmetics are not a named YMYL category, but "YMYL Health or Safety" covers anything that could harm health. Rater
  examples that apply directly: a pimple-popping article rated Lowest because "the author does not have skin care
  expertise"; a flu article rated Low for no evidence of medical expertise. YMYL content must be "consistent with
  well-established expert consensus".
- Helpful-content guidance (2026-10-05): bylines and author pages; fabricated creator profiles damage trust. Gen-AI
  guidance (2026-10-01): fact-check before publishing; AI-generated e-commerce images need IPTC `DigitalSourceType`.
- There is no Google "medical reviewer requirement"; a credited reviewer is rater evidence of expertise, not a rule.

## 6. Five actions for skingenetix.com, each with its evidence

1. Open every hub with a two-sentence quotable answer whose title and H1 mirror the query, then the named trials with
   numbers (Ahrefs 2026-04; Princeton).
2. Earn third-party mentions in Allure, Byrdie, Refinery29, dermatologist YouTube and newswire-distributed trial
   summaries, measured as mentions, not links (Ahrefs 2025-05; Semrush 2025-11; 5WPR). No paid placements.
3. Answer PDRN, GHK-Cu and Argireline questions in r/SkincareAddiction Q&A threads under a disclosed brand account;
   expect a 1–2-year lag (Semrush).
4. Keep evidence pages visibly current: a dated "last reviewed", real updates when trials publish, no years in URLs.
5. Treat schema as rich-result hygiene only; put effort into Shopify Catalog and Merchant Center completeness and public
   review volume for shopping surfaces (Ahrefs 2026-05; Google; OpenAI).

Keep the reviewer credit (a real person with real credentials): it is exactly what raters look for on skincare pages.

## Could not verify

The "YouTube 0.737" coefficient; a vendor's "2–6 weeks to citation"; "300+ reviews = 3× citations"; the OpenAI help page
(quoted via search excerpt); the newswire release behind the 5WPR index (403).
