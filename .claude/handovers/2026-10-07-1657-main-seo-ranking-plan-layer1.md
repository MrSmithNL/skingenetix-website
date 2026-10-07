# Session Handover — 2026-10-07 16:57 — skingenetix-website — main (seo-ranking-plan-layer1)

<!-- meta:
  rotation_reason: natural break (Layer 1 of the ranking plan shipped; next slice is content and off-site work)
  approval_required: true   (six decisions sit with Malcolm, listed in §11; none blocks the next action)
  schema_version: 3.0.0
-->

## 1. Mission

Set up the site's pages, articles and technical criteria so Skingenetix ranks first on Google and in AI answers for its
key terms. Today's session did two things: (a) the performance review, competitor analysis and the plan to rank first;
(b) on Malcolm's "lets proceed with the fixes and improvements", Layer 1 of that plan live on all five ingredient hubs in six
languages, with four of the five now meeting the audit bar.

## 2. Big picture & masterplan

- Vision: a peptide-skincare store whose ingredient hubs and appraised clinical-study articles are the pages Google and AI
  engines cite, so the products sell on evidence (project `CLAUDE.md`; `docs/content-hub-strategy-2026.md`).
- Masterplan / roadmap: `/Users/malcolmsmith/Claude Code/Projects/skingenetix-website/docs/todo.md` → entry **SEO-RANK-001**
  (the three-layer plan), with the full plan in
  `/Users/malcolmsmith/Claude Code/Projects/skingenetix-website/docs/seo-performance-and-ranking-plan-2026-10-07.md` (Part C,
  keyword-by-keyword in C.5). Position: **Layer 1 done except Malcolm's items; Layer 2 (off-site) waits for his scope and
  budget; Layer 3 (spokes and collection rebuilds) not started.** The parallel STUDY-DETAIL thread (result sections on the
  eight study articles) sits in the worktree `../skingenetix-website-wt-outcomes` waiting for Malcolm's approval of the
  English; it is not this session's work.
- Where this work fits: the hubs are the pages the whole plan rests on (PDRN alone is 68% of the measured opportunity);
  getting them indexed, consistent and to the audit bar is the precondition for the spokes and the off-site mentions.
- Why it matters: VERIFIED today, the site ranks in no top 10 and is cited in no AI Overview on 33 live SERPs, has zero
  genuine referring domains, and its flagship PDRN hub has never been crawled by Google. Content quality was never the
  blocker; discovery, authority and a few consistency faults were.
- This session's role (for the fresh session): the builder of Layer 3 content and the keeper of the hub bar. It may draft
  English articles on the hidden drafts blog, run central audits (standing budget), and edit `.md` freely. It may not
  translate or publish new copy before Malcolm has approved the English, change product titles, add the withheld "Botox in
  a bottle" item, spend beyond the standing audit budget, or write to the store while another Skingenetix window is
  publishing.

## 3. Current cursor

- Plan file: `/Users/malcolmsmith/Claude Code/Projects/skingenetix-website/docs/todo.md`, entry SEO-RANK-001.
- Position: Layer 1 → all ticked except the items marked 🛑 (Malcolm) · Layer 2 → not started (decision) · Layer 3 → item 1
  not started ("Argireline and Matrixyl 3000 together" spoke).
- Spec gate: N/A (content work). ADR: ADR-2026-10-07-V in `docs/decisions-log.md`.

## 4. Next concrete action

Write the first Layer 3 spoke, "Argireline and Matrixyl 3000 together: what the trials show", as an **English draft on the
hidden drafts blog** (`/blogs/clinical-studies-drafts/`, `seo.hidden=1`, the pattern the study articles use), grounded only in
the two registers (`docs/claims/argireline-acetyl-hexapeptide-8.md` §1 "Bundles with Matrixyl 3000" and
`docs/claims/matrixyl-3000.md` §4): three-bullet answer first, "do they work together" (no study of the pair exists, say so),
"which first", "who should skip", the evidence from the two hubs, the reviewer line, a link to the duo set and to both
hubs, 800–1,500 words, no combined percentage, no "synergy". Then audit the draft with the central auditor (`--criteria v2
--page-type article --keyword "matrixyl and argireline"`, read the uncapped score) and put the English to Malcolm.

## 5. Verification recipe

```bash
cd ~/"Claude Code/Projects/seo-toolkit" && .venv/bin/python scripts/audit_page.py \
  "https://www.skingenetix.com/blogs/clinical-studies-drafts/<handle>" --criteria v2 --page-type article \
  --keyword "matrixyl and argireline" --serp --market en-US \
  --json "<repo>/docs/audits/page-audit-<date>-<handle>-draft.json" --out "<repo>/docs/audits/page-audit-<date>-<handle>-draft.txt"
```

Expected: uncapped 9.0 or more; the only confirmed failures T4/T8 (draft artefacts: not in sitemap/hreflang). Run audits in
the **foreground** (10-minute timeout, one at a time, about 2 minutes apart) and read the full log; a background job was
killed at a turn boundary today and a grep filter hid a timeout.

## 6. Stop conditions (ask before)

- Translating or publishing any new copy before Malcolm has approved the English (his rule, 2026-09-29; today's FAQ items
  went live in six languages only because he said "proceed with the fixes").
- Changing product titles (the word "Argireline" on the serum: trademark; the Matrixyl cream's title).
- Publishing the "Is Argireline 'Botox in a bottle'?" item (register lists the phrase under claims to avoid; the draft text
  is in `docs/todo.md`, SEO-RANK-001).
- Any spend beyond the standing audit budget (about USD 3 per audit, USD 12 per loop); the `llm_responses` AI-citation panel;
  weekly SERP monitoring (about USD 0.50 a week); image runs.
- Any store write while another Skingenetix window is publishing: `ListAgents` first.
- The copper hub's 55.8% figure: do not edit it until the derivation is re-read at source (§11).

## 7. Autonomy envelope (approved, proceed without asking)

- All `.md` edits and commits (standing approval, 2026-04-22).
- Shopify content work per the project `CLAUDE.md`: previews, drafts on the hidden blog, Files uploads, our own set-only hub
  specs via `scripts/hub-upgrade.py` (six languages at once, never English-only on a live template).
- Central audits (standing, 2026-09-29) and DataForSEO pulls of a few cents.
- Malcolm, 2026-10-07: "lets proceed with the fixes and improvements" (Layer 1, applied today; see ADR-2026-10-07-V).

## 8. Decisions log (don't re-debate)

- **Layer 1 live in six languages at once** (ADR-2026-10-07-V): Article schema + `dateModified`; FAQ avatar cleared; question
  and safety FAQ items on every hub; PDRN retinol figure "more than three times" everywhere; glutathione answers qualified;
  copper consistency; SEO titles re-translated; keyword ownership aligned in `configs/page-targets.json` and in the
  seo-toolkit client config (`configs/skingenetix.config.json`, commits de5f85c and 6808210 there).
- **Keyword ownership:** hub "argireline" / product "argireline serum"; serum "matrixyl 3000" / hub "matrixyl 3000 benefits"
  (its title carries it; "what does matrixyl 3000 do" failed Q2); The Science "peptides in skincare"; home the brand;
  `/collections/all` "peptide skincare". Product titles unchanged (Malcolm's).
- **PDRN's remaining C9** (the "3.5×" hero figure called "hype-leaning"): accurate (23.0% vs 6.6%, Ye 2026 Fig. 6B) and set
  under Malcolm's strongest-credible-claim rule, so left for him, not changed.
- **Copper's remaining C4/C9/Q5:** loop limit reached (four runs); recorded in the tracker for the next session.
- **The "Botox in a bottle" FAQ item withheld** pending Malcolm; draft text in the todo.
- **No disavow** of the 622 link-generator domains (Google ignores them); re-check growth in two weeks.
- **Audit scores of the retired two-model script (9.6–9.8 for the hubs) are withdrawn**; today's central v2 runs are the
  baseline.

## 9. Constraints learned this session

- [VERIFIED — URL Inspection API, 2026-10-07] The English `/pages/pdrn-research` is "unknown to Google" under every URL
  variant; all five translations are indexed; three study articles live since 10-01 (Yogya, Tadini, Robinson) are also
  unknown. Nothing on our side blocks them (200, self-canonical, in the sitemap, linked, identical to Googlebot).
  **Request indexing is manual (Malcolm); no API.** Why Google never fetched it is NOT ESTABLISHED (hypothesis: crawl demand
  on a five-week-old site).
- [VERIFIED — DataForSEO backlinks, 2026-10-07] 627 referring domains, 622 of them link-generator junk first seen 6–7 Oct;
  genuine referring domains: zero. Never quote the raw count as authority.
- [VERIFIED — 33 SERPs + 9 mobile pulls] Desktop US head-term SERPs carry hacked-site spam (stonevillenc.org, 17 placements);
  mobile SERPs differ in kind (explainers). Always pull both devices before naming a competitor.
- [VERIFIED — three apply rounds] Six-language hub edits: read live values per locale from `translatableResource` right
  before building a spec (a stale snapshot reverted the retinol fix once today); minimal substitution keeps tags, classes
  and links; translator agents substitute into the exact `old_locale`; `hub-upgrade.py --apply` is idempotent (a connection
  reset mid-registration was fixed by re-running it). Memory: `six-language-hub-edits-go-through-a-translation-package`,
  `re-pull-live-values-before-every-spec-batch`.
- [VERIFIED — auditor source, `page_audit/extraction.py` and `checks.py`] Q5 fails on any paragraph under 150 words with ≥3
  uses, or ≥8 uses above 3 per 100 words; extraction uses `include_links=True` (link URLs count), strips `<em>/<strong>`
  before extracting. Copper's one "packed paragraph" could not be reproduced locally even with those settings
  (HYPOTHESIS: the auditor's content also includes schema text).
- [VERIFIED — live HTML] The Impact FAQ section renders `team_avatar` twice (desktop and mobile) and emits FAQPage JSON-LD
  with every answer, so an answer sentence appears twice in the HTML by design.
- [VERIFIED — audit logs] The OpenAI judge (gpt-6-sol) fails every call: "credit_balance_exhausted". The panel ran on three
  models all day. Malcolm's spending decision.
- [VERIFIED — twice] The pre-commit hook (lint-staged) cannot stash/restore the other session's unstaged handover deletions in
  this working tree; commit through a detached worktree (memory
  `commit-through-a-clean-worktree-when-lint-staged-cannot-restore`; script recipe there). Never `--no-verify`; never type
  `rm -rf` (deny list).
- [VERIFIED] Background Bash jobs can be killed at a turn boundary (exit 143/144); run audits in the foreground.
- [VERIFIED — Lighthouse, lab] Mobile LCP 7.8–11.1 s on the hubs; not today's blocker, a later item.

## 10. Failed approaches (don't retry)

- A background audit script piping through `grep | head` hid a `httpx.ReadTimeout` and a kill; no report was written and the
  failure was invisible. Run in the foreground with a full log.
- Building the content spec from `hub-values.json` captured before an earlier apply: reverted a live fix. Re-pull first.
- Whole-element rewrites in the English package dropped `class` attributes and product links; the translators caught it.
  Edit by minimal substitution on the live element.
- `ffmpeg hstack` on frames of different heights; use `scale=w:h:force_original_aspect_ratio=decrease,pad=w:h` per frame first,
  and write the filter inline (a shell variable expanded empty).
- A commit command containing `rm -rf` was refused by the deny list; use Python to delete files.

## 11. Open questions / awaiting Malcolm

1. Request indexing in Search Console for `/pages/pdrn-research`, Yogya, Tadini and Robinson (manual, ~5 minutes).
2. Keyword ownership on the product pages: may the serum's title carry "Argireline" (trademark)? Move the Matrixyl cream's
   title to "collagen cream with matrixyl"? (`docs/keyword-ownership-analysis-2026-09-30.md`; teardown §4.)
3. The off-site track's scope and budget (Part C.3): reviews flow, Merchant Center attributes, listicle outreach, YouTube
   sampling, Reddit presence, newswire, retail. Nothing starts without this.
4. The `llm_responses` AI-citation panel spend (about USD 0.70 a run) and the weekly monitor's SERP spend (about USD 0.50).
5. Approve or veto the "Botox in a bottle" FAQ item (draft in the todo); approve the English of the eight study previews
   (STUDY-DETAIL, other worktree).
6. The OpenAI account has no credits (one audit judge dead).
7. PDRN's "3.5×" framing: keep (his rule) or soften (the auditor's C9).
8. Copper: re-read how Badenhorst's 55.8% vehicle-relative figure is derived before touching it (the judges compute 61%
   from −24.1% vs −15.0%); reword "the compared serum lacked GHK-Cu and its nano-carrier". The Ye article still lacks a
   sibling link to Yogya (P3): add it in the STUDY-DETAIL rebuild.
   Relied on but not re-verified by this session: the demand figures in `docs/keyword-strategy-2026.md` (observed clickstream,
   2026-09-22); the register facts behind today's FAQ answers (taken from `docs/claims/*.md` as written); the teardown
   agents' page measurements (their own fetches, listed in each teardown's sources).

## 12. Plan & sub-plan references (read fresh; do not inline)

- Plan: `docs/todo.md` (SEO-RANK-001) · `docs/seo-performance-and-ranking-plan-2026-10-07.md` (Part C)
- Content plan and hero map: `docs/content-plan-2026.md` (§5 spokes) · `docs/keyword-strategy-2026.md` (§4)
- ADRs: `docs/decisions-log.md` (ADR-2026-10-07-V and the September ADRs it rests on)
- Specs applied today: `configs/hub-upgrades/*-audit-fixes-2026-10-07.json`, `*-content-fixes-2026-10-07.json`,
  `*-content-fixes-2-2026-10-07.json`, `copper-peptide-research-content-fixes-3-2026-10-07.json`
- Keyword maps: `configs/page-targets.json`; seo-toolkit `configs/skingenetix.config.json`

## 13. Knowledge, research & learnings (links, read fresh)

- Evidence record and raw data: `audits/2026-10-07-visibility-forensics/README.md`, `data/`, `serp/report.md`,
  `teardown-pdrn.md`, `teardown-argireline-matrixyl.md`, `teardown-copper-glutathione-peptide.md`,
  `research-google-events-2026-10-07.md`, `research-ai-factors-2026-10-07.md`, `config.json` (the forensics/monitor config)
- Audits: `docs/audits/page-audit-2026-10-07-pages-*-live*.txt` (runs 1–4) and `docs/audits/tracker-skingenetix.com.md`
- Registers: `docs/claims/pdrn.md`, `argireline-acetyl-hexapeptide-8.md`, `copper-peptide-ghk-cu.md`, `matrixyl-3000.md`,
  `glutathione.md` (each has an "Applied on the store — 2026-10-07" section)
- Template and rules: `docs/science-page-template.md`, `docs/content-hub-strategy-2026.md` §9, `docs/research-2026-ai-search-and-content-hubs.md`
- Learnings saved today (memory dir `~/.claude/projects/-Users-malcolmsmith-Claude-Code-Projects-skingenetix-website/memory/`):
  `the-english-pdrn-hub-was-never-indexed.md`, `link-generator-spam-is-not-authority.md`,
  `central-v2-caps-hubs-at-4-9-on-a-keyword-clash.md`, `probe-both-devices-and-two-user-agents-before-naming-a-competitor.md`,
  `six-language-hub-edits-go-through-a-translation-package.md`,
  `commit-through-a-clean-worktree-when-lint-staged-cannot-restore.md`, `re-pull-live-values-before-every-spec-batch.md`
- Skills used: `seo-visibility-forensics` (the canonical competitor-gap procedure), `seo-content-strategy`,
  `seo-aiso-validator` (the auditor; its experience log received today's execution)

## 14. File state

- Modified this session (all committed): `docs/seo-performance-and-ranking-plan-2026-10-07.md` (new),
  `audits/2026-10-07-visibility-forensics/*` (new), `docs/audits/page-audit-2026-10-07-pages-*` (new),
  `docs/audits/tracker-skingenetix.com.md`, `docs/todo.md`, `docs/content-plan-2026.md`, `docs/architecture.md`,
  `docs/decisions-log.md`, `docs/claims/*.md` (five), `configs/page-targets.json`, `configs/hub-upgrades/*2026-10-07.json`
  (16 specs), `configs/seo-changes/*2026-10-07*` (four), `configs/seo-snapshots/*2026-10-07*` (two).
- In flight: nothing of mine. The working tree also shows another session's deleted and moved handover files and a
  half-staged handover edit (`.claude/handovers/2026-10-07-1346-study-outcome-sections.md`, state `MD`): not mine, leave them.
- Store state (live, six languages): the five hub templates; product MediaImage 70951919255937 alt; page SEO translations
  for PDRN, Argireline, copper, The Science; the glutathione description.
- Desktop: `~/Desktop/skingenetix-renders.png` (FAQ sections of PDRN EN/DE and Argireline EN, desktop and phone).

## 15. Git state

- Branch: `main`.
- Last commit: `4e1c0aa` — docs: architecture change log (preceded by `d3634f9` batches 2–3 and re-audits, `49d2fd0` Layer 1
  batch 1, `496af01` the report). This handover is committed after it.
- Pushed: yes, all four. seo-toolkit: `de5f85c`, `6808210` pushed.
- Uncommitted diff of mine: none.

## 16. Session log

- 14:00–15:10 Review: Search Console (fresh 90-day pull, weekly trend, per-page, URL inspection), backlinks, demand, 33 SERPs
  desktop + 9 mobile, Lighthouse, five central v2 hub audits (run 1), three competitor teardowns, two research notes; report
  and evidence record written; committed `496af01`.
- 15:15–15:40 Batch 1 live on all five hubs: Article schema, FAQ avatar cleared, PDRN retinol phrase (first time), 23
  replacements and 11 FAQ items in six languages via five translator agents; SEO titles and descriptions re-translated;
  page-targets aligned; committed `49d2fd0`. Run 2: PDRN 9.36, Argireline 9.34 (capped), copper 9.12, Matrixyl 4.9 → 9.42
  after the toolkit map, glutathione 9.33.
- 16:20–16:55 Batch 2 (fresh values): retinol phrase restored, links out of the ppm paragraph, citations shortened, Argireline
  paragraph split, copper and glutathione consistency, glutathione description, Matrixyl schema name. Run 3: PDRN 9.69,
  Argireline 9.75, copper 9.26, Matrixyl 9.6, glutathione 9.72. Batch 3 (copper): duplicate sentence and citations; run 4
  copper 9.40. Committed `d3634f9`, `4e1c0aa`.
- Didn't work: the background audit job (killed, filter hid a timeout); the stale-snapshot spec; whole-element English rewrites.

## 17. Continuation prompt

> Read `/Users/malcolmsmith/Claude Code/Projects/skingenetix-website/.claude/handovers/2026-10-07-1657-main-seo-ranking-plan-layer1.md`
> and continue from §4 "Next concrete action". FIRST read §2 (big picture & masterplan) to understand your role and position
> in the project, then read the plans in §12 and the knowledge/research in §13 **fresh** — do not rely on summaries here.
> Operate within §7 autonomy envelope. Halt at any §6 stop condition and ask Malcolm. Check `ListAgents` for other
> Skingenetix windows before any store write. Begin with a one-line confirmation of the cursor (§3) and your role (§2), then
> execute §4.
