# Microneedling for skin, rank-first research: evidence record (2026-10-09)

**For:** `docs/microneedling-number-one-plan-2026-10-09.md`. **Asked by Malcolm, 2026-10-09:** rank first for the top
microneedling-for-skin keywords; research whatever is needed to know what that takes. **Spend:** DataForSEO about USD
7.40 (keyword pull 4.58, clickstream 1.30, 38 SERPs 0.08, authority under 0.05, brand mentions 0.39, AI-answer panel
0.86 plus three failed Gemini probes at no cost), inside the USD 20 research limit Malcolm set the same day.

## What was done

| Step                                                                                                                                                                                                                                                   | Generator                                                                           | Output                                                                             | Verdict                                                                                                           |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| 1. Keyword universe, US, GB, DE, NL: phrase match, question filter (English, German and Dutch words) and the related-searches graph on 21 seeds (microneedling, derma stamp, derma roller, pens, microchanneling, micro-infusion, microneedle patches) | `scripts/keyword-research-adjacent.py pull --markets US GB DE NL` with `seeds.json` | `raw-*.json.gz` (7,954 US, 6,188 GB, 4,476 DE, 4,455 NL)                           | VERIFIED                                                                                                          |
| 2. De-bucketed, off-intent removed, observed searches added                                                                                                                                                                                            | `... enrich --markets US GB DE NL`                                                  | `candidates-*.json.gz` (4,242 / 2,472 / 1,678 / 850 buckets), `clickstream-*.json` | VERIFIED                                                                                                          |
| 3. Demand by keyword family                                                                                                                                                                                                                            | inline                                                                              | `family-demand.json`                                                               | VERIFIED (family edges are regex-drawn; a few aftercare and before-and-after terms sit in the serum family)       |
| 4. Live SERPs with AI Overviews, 38 pairs (17 US, 9 GB, 9 DE, 3 NL), desktop                                                                                                                                                                           | skill `seo-visibility-forensics` `serp_gap.py pull` with `config.json`              | `serp/serp.json`, `serp/raw/`                                                      | VERIFIED                                                                                                          |
| 5. Top-4 pages measured, authority, gap report                                                                                                                                                                                                         | `serp_gap.py pages`, `authority`, `report`                                          | `serp/pages.json`, `serp/authority.json`, `serp/report.md`                         | VERIFIED                                                                                                          |
| 6. Brand demand, Reddit and YouTube presence for the 14 most frequent competitor domains                                                                                                                                                               | `serp_gap_deep.py mentions --top-brands 14`                                         | `serp/mentions.json`                                                               | VERIFIED (subdomain brands such as us.drpen.co return no brand volume; "dr pen" is 12,835 US in the keyword pull) |
| 7. AI answers: ChatGPT (gpt-6.1-sol), Perplexity (sonar-pro), Claude (sonnet-5-5), web search on, 10 buyer questions each; Gemini returned 40501 for every model tried, so Google's own AI is read from the AI Overviews in step 4                     | `generators/ai_answers.py`                                                          | `ai-answers/answers.json`                                                          | VERIFIED as a one-run snapshot (stable shares need 7+ runs)                                                       |
| 8. Search Console, 90 days, our microneedling pages and queries                                                                                                                                                                                        | `forensics.gsc_query`                                                               | `data-gsc-microneedling-90d.json`                                                  | VERIFIED: the collection 6 impressions, the PDRN stamp set 5, nothing on any head term                            |
| 9. Regulation and safety (FDA, EU MDR and GPSR, cosmetics law, MHRA, ASA, dermatology bodies, case reports)                                                                                                                                            | research subagent                                                                   | `research-regulation-and-safety.md`                                                | VERIFIED / REPORTED per line; not legal advice                                                                    |
| 10. Clinical evidence for at-home microneedling and microneedling with actives (PubMed E-utilities, Europe PMC)                                                                                                                                        | research subagent                                                                   | `research-clinical-evidence.md`                                                    | VERIFIED titles; about 20 papers appraised from the abstract only (marked)                                        |
| 11. Product and category page teardown of the winners against our stamp pages and collection                                                                                                                                                           | teardown subagent                                                                   | `teardown-product-and-category-pages.md`                                           | see the file                                                                                                      |

The article-level teardown of "at home microneedling", "derma stamp" (US, GB), "how to use a derma stamp", "derma stamp vs
derma roller", "after microneedling care" and the serum terms is in `../2026-10-09-new-article-keywords/teardowns/microneedling.md`
and was reused, not repeated.

## Key measurements

- **Dr. Pen holds the commercial results in all four markets** (us.drpen.co, uk.drpen.co, eu.drpen.co: pens, rollers,
  stamps, serums, guides) on sites with about 40 to 110 referring domains: catalogue breadth, exact-match category names,
  country sites and brand demand, not links.
- **The US head term is a medical wall** (Cleveland Clinic, PMC, ASDS, FDA, AAD, Yale); **the GB head term is led by a brand
  guide** (Trinny London); **the DE at-home term by a drugstore guide** (Rossmann).
- **Google's product block appears on almost every commercial microneedling SERP**; we have no product feed.
- **AI answers:** ChatGPT advised against at-home microneedling on every question, citing the AAD and FDA; Perplexity
  recommended single-use, shallow (0.25 mm) stamps with single-use serum ampoules; Claude said stay at or below 0.5 mm.
  Most-cited domains: fda.gov 25, aad.org 17, banish.com 13, evenskyn.com 13, mdpen.co 7; hairgenetix.com was cited 4 times.
- **No controlled trial of an at-home facial stamp exists**; a 2026 review rates home microneedling evidence Level D.
- **US regulation:** a 0.5 mm stamp sold with serum and "apply after stamping" instructions matches FDA's description of a
  possible combination product; collagen, scar, wrinkle-treatment and penetration claims make a stamp a device.

## Generators

- `scripts/keyword-research-adjacent.py` (repo; `--markets` added today, tests in `tests/test_keyword_research_adjacent.py`).
- `generators/ai_answers.py` (this folder).
- `~/.claude/skills/seo-visibility-forensics/scripts/serp_gap.py` and `serp_gap_deep.py`.

## Open items

- Mobile SERPs not pulled for the microneedling terms; FR, IT and ES not pulled.
- The regulatory reading is research, not legal advice; a regulatory specialist should confirm the 0.5 mm device question
  and the serum-on-needled-skin position before the pairing instruction is used anywhere.
