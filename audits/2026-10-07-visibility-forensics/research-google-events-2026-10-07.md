# Google-side events, 2026-08-01 to 2026-10-07 — research note

Delegated research (brief: the skill's `research/google-events-prompt.md`). Status: VERIFIED = a Google page was
opened; OBSERVED = volatility trackers via SERoundtable; CLAIMED = blog only.

## Ranking updates

| Date (PT) | Event | Status | Source |
|---|---|---|---|
| 18 Aug → 21 Aug | August 2026 spam update, global, all languages | VERIFIED | https://status.search.google.com/incidents/LEubPCm2octf2uMqCFKE |
| 24 Sep → still open on 7 Oct | September 2026 spam update, "rollout may take up to two weeks", no completion entry | VERIFIED | https://status.search.google.com/incidents/XhUDXP7A67iHCD2kmbVu |
| 1–13 Aug (several days) | Unconfirmed volatility | OBSERVED | SERoundtable |
| 3–4 Sep, reverted 13 Sep | Large sites dropped then surged back | OBSERVED | SERoundtable |
| 15–16 Sep | Volatility spike, UK and e-commerce mentioned | OBSERVED | SERoundtable |
| 25–27 Sep, 30 Sep–1 Oct, 4–6 Oct | Three spam-update waves; losers named: AI-generated sites, programmatic pages | OBSERVED | SERoundtable |

**No core update in the window.** The last core update on the dashboard is May 2026. No helpful-content or
product-reviews update exists as a named 2026 event. VERIFIED.

## Search Console reporting

- 24 Sep: Web split into "text-based" and "multimodal" as a filter in the Performance and Generative AI reports; Google
  describes a filter, not a re-count. VERIFIED https://developers.google.com/search/blog/2026/09/web-multimodal-in-sc
- Data anomalies: 13 Aug Discover logging error; 13–17 Aug Generative AI report impressions under-logged, restored
  21 Aug. Nothing logged for September or October. VERIFIED https://support.google.com/webmasters/answer/6211453
- 26 Aug: google.com/goto passthrough links; affects rank trackers, not Search Console. VERIFIED (spokesperson quote).

## AI Overviews, AI Mode and policies

- 28 Aug: AI Overviews may dynamically expand into AI-Mode-style answers "for topics where our systems determine it's
  most useful". No category list published. VERIFIED (Google statement).
- No health or YMYL AI Overview policy change in the window.
- 28 Aug: site-reputation policy; from 30 Aug manual actions do not apply for searchers in the EEA. Relevance: DE and NL
  results can keep showing third-party sections of big hosts that are demoted for US and GB searchers. VERIFIED
  https://developers.google.com/search/blog/2026/08/update-site-reputation-policy
- 1–5 Oct: gen-AI content guide and helpful-content page updated with rater-guideline material (effort, originality,
  accuracy). Scaled-content and hacked-content policy text unchanged. VERIFIED.
- The Search Quality Rater Guidelines PDF is still the 11 September 2025 edition. Blog claims of 2026 editions are false.

## Hacked-site spam on the peptide head terms

- **stonevillenc.org is hacked and cloaked.** A 13 Sep 2026 report describes Googlebot receiving an 85 KB peptide article
  while browsers get 1.4 KB of JavaScript redirecting to a WhatsApp group selling peptides; one query returned ten
  Stoneville URLs on page one; a second North Carolina town on the same host is set up the same way. Wayback captures:
  the injected URLs first appear 10 Sep 2026 (200); captures on 2 and 5 Oct return 403. Our own probe on 7 Oct: several
  URLs time out, the ones that answer serve the same "Understanding the Entity: GHK-Cu" page to both user agents.
  Source: https://dadstrengthdaily.substack.com/p/a-nc-town-governments-website-sent
- **curf.clemson.edu is not hacked.** It is a genuine university news item about an anti-ageing line, thin on relevance,
  ranking on domain authority.

## Verdict

The only confirmed ranking events are two spam updates. Neither can demote a clean site directly, but the September one
is reshuffling exactly the head terms (copper peptide, GHK-Cu, Matrixyl 3000) where a hacked site held several page-one
slots, so a zero-authority newcomer's positions there will swing as spam is removed and other sites fill the gaps. There
was no core update, no Search Console re-count, one restored logging error, and an EEA-only loosening of site-reputation
enforcement. A Google-side contribution to volatility: plausible. A single Google event explaining where the site ranks:
no. The site's head-term positions were never stable to begin with.

Could not verify: tracker readings by country; category-level winners and losers; a live fetch of every stonevillenc.org
URL (connections refused); the exact day the helpful-content page changed.
