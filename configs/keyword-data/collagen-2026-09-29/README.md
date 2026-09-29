# Collagen keyword pull — 2026-09-29

Why: Malcolm asked whether `/pages/collagen-skin-plumping` can own a collagen-skincare term without overlapping any other key page
("option 3 first - then 1": existing data first, then a small paid pull capped at $5).

- Tool: `scripts/keyword-strategy.py` functions (DataForSEO Labs `keyword_suggestions`, limit 300 per seed; clickstream
  `bulk_search_volume` for the top 400 filtered terms per market). Seeds: `seeds.md` (15 per market).
- Markets: US 2840/en, GB 2826/en, DE 2276/de, NL 2528/nl. Filter: supplements, food/drinks, injectables, devices, lips, hair,
  body-only and competitor brands removed before scoring.
- Spend: $1.42 for the pull, $1.43 including four SERP checks (`serps.json`).
- Per market: {"US": {"raw": 1803, "kept": 1441, "clickstreamed": 400}, "GB": {"raw": 1569, "kept": 1223, "clickstreamed": 400}, "DE": {"raw": 453, "kept": 385, "clickstreamed": 385}, "NL": {"raw": 197, "kept": 157, "clickstreamed": 157}}
- `pull-XX.json`: `all` = every suggestion, `kept_head` = the filtered top terms with `clickstream` (observed) volume.
- `keyword-ownership-map-2026-09-29.md`: every key URL's primary and secondary terms, and the terms two URLs chase.

Result and decision: `docs/decisions-log.md` ADR-2026-09-29-D.
