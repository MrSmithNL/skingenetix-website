# Session Handover — 2026-10-08 16:34 — skingenetix-website — main (plan-and-collagen-live)

<!-- meta:
  rotation_reason: explicit user request (/session-handoff) after a long, multi-part session
  approval_required: true   (several decisions sit with Malcolm, §11; none blocks the next action)
  supersedes: .claude/handovers/2026-10-08-112118-main-13f2.md (this session's unfilled auto-rotation snapshot, moved to archive/)
  schema_version: 3.0.0
-->

## 1. Mission

Set up the site's pages, articles and technical criteria so Skingenetix ranks first on Google and in AI answers for each page's
keyword. Today's session: (a) the full website traffic and performance plan, page by page, with competitor analysis for all 37
owner pages and a step-by-step implementation plan; (b) on Malcolm's "fix the issues the research found" and "remove my name as the
writer", the verified live faults fixed in six languages and the writer credit made generic; (c) on "Publish the page", the Collagen
Skincare page live with its menu tile, explainer image and three before/after result cards; (d) "proceed": the first Learn spoke
drafted and audited, and the speed cause proven without a store change.

## 2. Big picture & masterplan

- Vision: a peptide-skincare store whose ingredient hubs, appraised study articles and Learn spokes are the pages Google and AI
  engines cite, so the products sell on evidence (`CLAUDE.md`; `docs/content-hub-strategy-2026.md`).
- Masterplan: `docs/todo.md` → **SEO-RANK-002** (today's entry, above SEO-RANK-001), whose plan is
  `docs/website-traffic-and-performance-plan-2026-10-08.md` (Parts 1–10; Part 6 is the three-phase implementation plan with the
  mechanics, check, undo and cost of every step; Part 7 the 17 decisions that are Malcolm's).
- Position: **Phase 0 (Malcolm's decisions) open. Phase 1 partly done:** 1.1 the eleven unowned pages mapped with uncontested terms
  (the contested moves wait for decision 3); 1.4a claim and H1 fixes done; 1.5 the speed test done (cause found, the setting is
  decision 7); 1.6 spoke 1 drafted and audited; the Collagen Skincare go-live (Phase 2 step 2.5) pulled forward on Malcolm's word.
  Not started: 1.2 product pages, 1.3 collections, 1.4b concern pages re-aimed, 1.4c The Science pillar, 1.7 Learn blog template,
  1.8 STUDY-DETAIL go-live, 1.9 hub leftovers, 1.10 the monitor.
- Parallel thread: STUDY-DETAIL (result sections on the eight study articles) sits in `../skingenetix-website-wt-outcomes`
  (branch `study-outcome-sections`), waiting for Malcolm's approval of the English; not this session's work, but the Matrixyl hub
  preview's two before/after pairs were set today (§8).
- Why it matters: the site ranks in no top 10 on 72 pulled SERPs, has zero genuine referring domains, and its PDRN hub is not
  indexed; content quality is not the blocker, discovery, authority and a handful of consistency faults are (plan Part 2).
- This session's role for the fresh session: builder of Phase 1, keeper of the audit bar (9.0+, no confirmed failures), and the
  one who shows every render on screen (contact sheet + `open`). It may draft English on the hidden blogs, run central audits
  (standing budget), make set-only six-language edits of existing copy, and edit `.md` freely. It may not translate or publish new
  copy before Malcolm approves the English (except where he has ordered it), change theme-wide settings, add trial figures to
  products, spend on image runs or panels beyond what he approved, or write to the store while another Skingenetix window publishes.

## 3. Current cursor

- Plan file: `/Users/malcolmsmith/Claude Code/Projects/skingenetix-website/docs/website-traffic-and-performance-plan-2026-10-08.md`
  → Part 6 → Phase 1 → step 1.6 (spoke 1) at "hidden draft audited 9.68 uncapped; awaiting Malcolm's English approval", and the
  go-live follow-ups of the Collagen Skincare page (audit items X1 and S2 open; menu tile image pending Malcolm's pick).
- Spec gate: N/A (content and store work). ADR: ADR-2026-10-08-W in `docs/decisions-log.md`.

## 4. Next concrete action

Fix the two confirmed audit items on the live Collagen Skincare page without new copy: X1 (one primary action with its proof beside
it: the hero button and the "Shop the Pro-Collagen Cream" action must sit next to the evidence that supports them, 1 of 3 checks met
today) and S2 (the Article JSON-LD's `mentions` carry Product objects with no `offers`: add `offers` with price and currency from the
live products, or drop the Product mentions), applied by a direct patch of `templates/page.collagen-skincare.json` with a backup and
mirrored in `configs/hub-upgrades/collagen-skincare-2026-09-29.json`; then re-audit and show the render. If Malcolm has meanwhile sent
the menu-tile number, do that first (§11 item 1, two commands).

## 5. Verification recipe

```bash
cd ~/"Claude Code/Projects/seo-toolkit" && .venv/bin/python scripts/audit_page.py \
  "https://www.skingenetix.com/pages/collagen-skincare" --criteria v2 --page-type article --keyword "collagen cream" \
  --serp --market en-US --json "<repo>/docs/audits/page-audit-<date>-pages-collagen-skincare-live-2.json" \
  --out "<repo>/docs/audits/page-audit-<date>-pages-collagen-skincare-live-2.txt"
```

Expected: score 9.0 or more (today 9.74), **confirmed failures 0** (today X1; S2 as a code-check FAIL), cost about USD 0.80. Run in
the foreground, one audit at a time, and read the full log. Then `curl -s <page> | grep -c '<h1'` = 1 and the render on screen
(contact sheet, `open`).

## 6. Stop conditions (ask before)

- Translating or publishing new copy before Malcolm approves the English (his rule, 2026-09-29): the spoke to `/blogs/learn` with
  `--public`, the STUDY-DETAIL go-live, the Matrixyl hub rebuild go-live, the Collagen page's five translations (after its 14 days).
- The Impact theme's reveal-on-scroll animation setting (decision 7): proven cause of the slow paint, but it changes every page's feel.
- Trial figures ("55.8%", "up to 23%", "+256%") on product and collection pages (decision 15); "Botox in a bottle" item (12);
  PDRN "3.5×" framing (11); the contested keyword-ownership moves (3); Badenhorst's framing (16); The Science as a pillar (17).
- Any spend beyond the standing audit budget (about USD 1 per audit now that the OpenAI judge is dead, USD 12 per loop): image
  runs (today's two explainer waves cost the suppliers' usual fees; gpt-image is out of credits), the AI-citation panel, the weekly
  monitor's SERP spend.
- Any store write while another Skingenetix window is publishing: `ListAgents` first (none was open after 11:00 today).
- Never `--no-verify`; never type `rm -rf` (deny list); never re-apply an old owning hub spec (use set-only specs).

## 7. Autonomy envelope (approved, proceed without asking)

- All `.md` edits and commits (standing, 2026-04-22). Commits go through the clean-worktree recipe (§9) because lint-staged cannot
  restore another window's unstaged deletions in this tree.
- Central audits (standing, 2026-09-29) and DataForSEO pulls of cents.
- English drafts on the hidden drafts blog (`scripts/learn-article-draft.py`, `scripts/build-study-page.py --preview`).
- Set-only six-language edits of existing live copy through `scripts/hub-upgrade.py` specs built from live values re-read first.
- On the Collagen Skincare page (live in English only by Malcolm's decision, 14-day gate): direct template patches with a backup
  (`hu.read_file` → edit → `hu.upload`), because `hub-upgrade.py` refuses an `english_first` spec on a template a live page uses;
  keep the spec file as the source of truth.
- Malcolm, 2026-10-08: "Fix the issues the research found" (done for the verified set), "Remove my name from all pages as the writer"
  (done), "Publish the page and add it to the menu with a tile" (done bar the tile image), "Stam sets = pre order" (done),
  "proceed" with the plan items that do not need him (spoke 1 and the speed test done; the rest in §11 item 6).

## 8. Decisions log (don't re-debate)

- **Writer credit = "Skingenetix Research Team"**, visible and in schema (`author` = Organization Skingenetix); reviewer and research
  credits untouched; code comments naming the requester stay (ADR-2026-10-08-W).
- **H1 on the Skin Solutions pages and The Science:** the title lives in the hero richtext block as `<h1>` (same 60/40 px as the
  heading block); the heading block is `disabled: true`, never deleted (keeps its translations).
- **Claims replaced** with register wording in six languages (`configs/claim-fixes/concern-pages-2026-10-08.*.json`); the Skin Repair
  retinol multiple and the PDRN collection meta say "more than three times" (consistency with the hub, Ye 2026 Fig. 6B); whether the
  multiples stay at all is decision 15.
- **Collagen Skincare live in English only**: the content plan's 14-day English measurement precedes translation; meta title and
  description are translated already (five locales registered on the page's `meta_title`/`meta_description`).
- **Collagen hero** styled like the Skin Solutions banners (custom CSS removed, overlay 22) with one CSS rule keeping the image
  right-aligned so the woman is fully in view; the shop button stays.
- **Explainer** = r2 slot A nbp_pro 02 (Malcolm's "A7 nbp_pro 02"; r2 is the batch with the blue water), in a media-with-text
  section with the `<h2>` inside the content.
- **Before/after pairs** (Malcolm: "use any from the resolved selection, you choose"): collagen card f1 = collagen-plumping r1 C2
  gpt_image 01; new card f3 (palmitoyl pentapeptide-4 fine lines, Robinson 2005, p ≤ 0.10 stated per ADR-T) = Matrixyl cards r1 D2
  gpt_image 01; copper card f2 unchanged; order f1, f3, f2. Moles clone-retouched from same-panel skin (no-moles rule).
  The hidden Matrixyl preview took Matrixyl r1 C2 (card 1) and the same D2 (card 2) with the register labels.
- **Stamp sets sell at zero stock** (`inventoryPolicy CONTINUE`) as pre-orders; the template shows "Pre-order".
- **Keyword owners:** eleven previously unowned pages added with uncontested terms; the auditor's client map synced (seo-toolkit
  `configs/skingenetix.config.json`, commits 4bc45b2 and cfcde96 there). The contested moves (brightening serum, peptide cream,
  peptides for skin, the hub and article retargets) wait for decision 3.
- **Spoke build path:** a plain article on the stock article template through `scripts/learn-article-draft.py` (the study template's
  fixed rows and FAQ fit one trial only); hidden draft first, `--blog learn --public` on approval.
- **Speed:** the reveal-on-scroll animation is the LCP cause (13.8 s → 6.2 s locally); the fix is a theme setting, decision 7; the
  app-script trim is the second half.
- **No disavow**, no `llms.txt`, no schema beyond the minimum, no "best peptide serum" page (plan Part 9).
- Audit scores from the retired two-model script stay withdrawn; today's central v2 runs are the baseline.

## 9. Constraints learned this session

- [VERIFIED] `hub-upgrade.py --apply` refuses `english_first` once a page uses the template ("give the spec a view"); removing
  `english_first` fails because every value then needs six locales. Patch the single section directly with a backup.
- [VERIFIED] The Impact `heading` block renders `<p class="h1">` whatever its "heading tag" setting; only `<h1>` inside a richtext block
  is a real H1. Five pages served no H1 until today.
- [VERIFIED] Theme translation keys look like `section.page.<handle>.json.<section>.<block>.<setting>:<hash>`; menu titles are
  translated per `gid://shopify/Link/<id>`; page SEO lives in `global.title_tag`/`description_tag` metafields with translatable keys
  `meta_title`/`meta_description`; the 2025-07 API has no `pageByHandle` and no `seo` field on Page (use `pages(query:"handle:…")`).
- [VERIFIED] A collection description change needs `collectionUpdate` plus `translationsRegister` against the new digest
  (`scripts/collection-description-apply.py`); an outdated translation is otherwise served.
- [VERIFIED] The PageSpeed Insights API answers 403 with the Google key (API not enabled on its project) and 429 without; local
  `npx --no-install lighthouse` (13.5) is the fallback; Boots and Timeless block the lab.
- [VERIFIED] OpenAI has no credits: gpt-image returns nothing in image runs and the fourth audit judge is dead; audits now cost about
  USD 0.5 to 0.8. Seedream refused one explainer brief on a content check.
- [VERIFIED] Both six-row before/after sheets (Matrixyl cards r1, collagen-plumping r1) share the A–F grid and supplier columns, so a
  grid reference alone cannot be placed; show the resolved tiles and ask, or open one sheet per decision.
- [VERIFIED] The dark-spot detector over-fires on freckles, brows, eye corners and nostril shadows; confirm each hit with a crop
  before cloning. The clone must stay in the same panel (never across the split).
- [VERIFIED] Menu tiles: `scripts/menu-image-tiles.py` builds every tiled menu from its `TILES` href→file map (17 tiles across 4
  menus now); a new child needs a TILES entry and a re-run. The mega-menu's own promo slots cap at three and are unused.
- [VERIFIED] `wave-contact-sheet.py` drops a short row unless `--partial`; rebuild with `--partial` after a run with a failed supplier.
- [VERIFIED] Agents' markdown fails the commit hook on lines over 300 chars and on `[TAG][TAG]` reference syntax; `scratchpad/mdfix.py`
  (rebuild it: insert a space between bracket tags, wrap non-table lines) then `markdownlint --fix`.
- [VERIFIED] The Collagen page's `answer` media-with-text block keeps the `<h2>` in its content; the hero's phone capture shows the
  text over the lower part of the image by design (mobile text position end-center).
- [VERIFIED] Image runs: `set -a; source ~/.claude/config/image-credentials.env; set +a` before `generate-multi.py`; FLUX.2 prints
  digits on glassware; a square 2048 master; Malcolm picks by underscore or by grid reference in chat.

## 10. Failed approaches (don't retry)

- `hub-upgrade.py --apply` on the live collagen spec (refused; see §9). Direct patch instead.
- Retouching every detector hit automatically: it smeared a hair strand and a nostril edge; the redo used crops to pick real moles.
- The first author swap walked the JSON without unwrapping the `<script type="application/ld+json">` wrapper of the study `jsonld`
  field (0 swaps); the fixed script unwraps and re-wraps.
- `git status --cached` (no such flag); `setsid` (not on macOS; use `nohup … &` in a subshell); unquoted `?view=` in a zsh loop (glob
  error aborted the loop); foreign text in a Bash heredoc (the hook blocks it; use the Write tool).
- A single `grep -A` with a complex pattern on live HTML ("ugrep exceeds complexity"): use Python for context extraction.
- The PageSpeed vitals pull, with and without the key (403/429): do not launch until decision 2 (enable the API) is done.

## 11. Open questions / awaiting Malcolm

1. **Menu tile image:** Malcolm chose a model-face tile from `~/Desktop/skingenetix-menu-tile-model-faces.png` (38 numbered
   candidates; manifest in the scratchpad `tile-faces-manifest.json`, which does not persist: rebuild the sheet with the same script
   if needed) but his pasted label was unreadable. Ask for the tile number. Then: add
   `"/pages/collagen-skincare": "<file>"` to `TILES` in `scripts/menu-image-tiles.py` (replace the phone-hero entry), upload the file
   through `scripts/upload-theme-images.py` if it is not in Files yet, run `python3 scripts/menu-image-tiles.py --dry-run` then without
   the flag, capture the open menu (Playwright hover on "Skin Solutions") and show it.
2. **Spoke 1 English approval** (and Dr Bodde's sign-off): `/blogs/clinical-studies-drafts/argireline-and-matrixyl-3000-together`,
   config `configs/learn/drafts/argireline-and-matrixyl-3000-together.json`; the writer's open points are in its summary (Henseler
   2023 left out; the Matrixyl serum's concentration unconfirmed). On his yes: `scripts/learn-article-draft.py <cfg> --apply --blog
   learn --public`, hide the draft, 14 days, translate.
3. **Decision 7:** turn the reveal-on-scroll animation off (proven 13.8 s → 6.2 s locally).
4. **The Matrixyl hub rebuild go-live** (its two before/after pairs are now set on the preview).
5. **The other 17 decisions** in the plan's Part 7, chiefly: request indexing (1), enable the PageSpeed API (2), keyword ownership (3),
   the off-site scope and budget (4), spend (5), approve the English of the eight study previews (6), the formula sheet (8),
   Klaviyo flows (9), trial figures on product and collection pages (15).
6. **What the next session can do without him** (from the plan): fix the collagen audit items (§4); spokes 2–5 as hidden drafts
   ("Does Argireline work?" hub section; PDRN-vs-retinol and "can you use both" on the Ye article; "Best PDRN serums"; "How to use a
   PDRN serum"); the Learn blog template and the sitemap housekeeping; English drafts of the nine product pages and five collections
   for approval; the outreach materials; the copper 55.8% derivation re-read at source; the key-figure-tiles-as-H2 fix on the study
   template (structure only).

## 12. Plan & sub-plan references (read fresh; do not inline)

- Plan: `docs/website-traffic-and-performance-plan-2026-10-08.md` (Parts 6 and 7) · `docs/todo.md` entries SEO-RANK-002 and
  SEO-RANK-001 · the 2026-10-07 ranking plan `docs/seo-performance-and-ranking-plan-2026-10-07.md` (Part C.5 keyword table).
- Review pack: `docs/review-2026-10-08-concept-pages.md`. ADRs: `docs/decisions-log.md` (ADR-2026-10-08-W and the September ones).
- Evidence: `audits/2026-10-08-competitor-gap-per-page/` (README, three teardowns, serp/, data/) and `audits/2026-10-07-visibility-forensics/`.
- Specs applied today: `configs/hub-upgrades/*-team-credit-2026-10-08.json`, `*-h1-fix-2026-10-08.json`, `*-claim-fixes-2026-10-08.json`,
  `skin-repair-renewal-retinol-multiple-2026-10-08.json`, `copper-peptide-research-german-h1-2026-10-08.json`,
  `collagen-skincare-2026-09-29.json` (now the live page); `configs/claim-fixes/`; `configs/copy/creams-moisturizers-description-2026-10-08.json`;
  `configs/seo-changes/collagen-skincare-meta-2026-10-08.translations.json`; `configs/menus/main-menu-skin-solutions-collagen-2026-10-08.json`;
  `configs/banners/block-collagen-skincare-explainer-r{1,2}.json`, `collagen-skincare-explainer-publish-2026-10-08.json`,
  `collagen-before-after-publish-2026-10-08.json`; `configs/page-targets.json` (39 pages).
- New tools: `scripts/collection-description-apply.py`, `scripts/author-credit-replace.py`, `scripts/disable-block.py`,
  `scripts/learn-article-draft.py`; changed: `scripts/build-study-page.py`, `scripts/build-clinical-studies-blog.py`, `scripts/menu-image-tiles.py`.
- Keyword maps: `configs/page-targets.json`; seo-toolkit `configs/skingenetix.config.json`.
- Memory dir: `~/.claude/projects/-Users-malcolmsmith-Claude-Code-Projects-skingenetix-website/memory/` (index `MEMORY.md`).

## 13. Knowledge, research & learnings (links, read fresh)

- Research written today: the three teardowns in `audits/2026-10-08-competitor-gap-per-page/` and its README (verdict table).
- Audits: `docs/audits/page-audit-2026-10-08-pages-collagen-skincare-live.*` (9.74; X1, S2 open),
  `docs/audits/page-audit-2026-10-08-learn-argireline-and-matrixyl-3000-together-draft.*` (9.68 uncapped).
- Registers: `docs/claims/*.md`; template docs updated to the team credit: `docs/science-page-template.md`, `docs/study-page-template.md`.
- Memories saved today: `nine-pages-had-no-keyword-owner-and-the-category-terms-were-never-pulled`, `concern-pages-and-the-science-serve-no-h1`,
  `pagespeed-api-is-blocked-until-the-key-enables-it`, `malcolm-wants-the-full-plan-with-step-detail-before-execution`,
  `hub-upgrade-refuses-english-first-on-a-live-template`, `name-the-sheet-when-several-share-a-grid`,
  `reveal-on-scroll-animation-is-the-lcp-cause`.
- Skills used: `seo-visibility-forensics` (Phase 5 on a second config; `serp_gap_deep.py mentions` and the failed `vitals`),
  `seo-aiso-validator` (the central auditor), the image pipeline scripts (`generate-multi.py`, `wave-contact-sheet.py`,
  `upload-theme-images.py`), `menu-apply.py`, `menu-image-tiles.py`.

## 14. File state

- Modified or created this session, all committed (see §15): the docs, audits, configs, scripts and specs listed in §12; `mkdocs.yml`
  (nav: the plan, the review pack, the ranking plan); `docs/architecture.md` (two change-log rows), `docs/decisions-log.md`,
  `docs/todo.md`; the memory files (outside the repo).
- Local only (not tracked by design): `assets/ai-generated/2026-08-22-multi-block-collagen-skincare-explainer-r{1,2}/` (25 + 27
  candidates), `assets/publish-ready/collagen-skincare/` (the uploaded masters, incl. the retouched pairs),
  `audits/2026-10-08-competitor-gap-per-page/data/lighthouse/` (15 raw runs, gitignored there), `backups/*20261008*` (every store
  write's backup).
- Not mine, left alone: the other window's untracked `docs/audits/page-audit-2026-10-02-*-live.*`, `configs/banners/study-detail-images-2026-10-02.json`,
  `audits/2026-10-07-visibility-forensics/serp/vitals.json` (the failed 403 attempt), the deleted/moved handover files in the index,
  and a lint-staged backup stash from this morning (safe to drop).
- Desktop (for Malcolm): `skingenetix-renders.png` (latest: the three result cards), `skingenetix-menu-tile-model-faces.png`,
  `skingenetix-menu-skin-solutions.png`, `skingenetix-your-picks-resolved.png`, `skingenetix-block-collagen-skincare-explainer-r{1,2}.png`,
  the three before/after sheets, `skingenetix-traffic-and-performance-plan-2026-10-08.html`.
- Store state (live): Collagen Skincare at `/pages/collagen-skincare` with redirect, tile, explainer and three cards; the five hubs,
  five concern/science templates, three concern templates' claims, the creams collection, the PDRN collection meta, 8 articles,
  16 study entries, both stamp sets, the hidden spoke draft, the hidden Matrixyl preview's two cards.

## 15. Git state

- Branch: `main`. Last commit: `b6ba6cc` — collagen: before/after pairs on three result cards; spoke 1 drafted and audited 9.68;
  speed cause found. Earlier today: `92386f2`, `8324fe9`, `f125fb0`, `9174949`. Pushed: yes, all. This handover is committed after it.
- seo-toolkit: `cfcde96` (keyword map synced, home URL slash), pushed.
- Uncommitted diff of mine: none.

## 16. Session log

- 10:31–11:20 Prime; the plan question. Research: 39 SERPs + volumes + mentions + Lighthouse; three teardowns; the plan, the
  review pack, the evidence README; commit `9174949`.
- 11:20–13:50 Malcolm's five jobs: collagen reorder/hero/byline; Matrixyl pairs found waiting since 2026-09-26; author inventory and
  claims inventory (agents); explainer r1; team credit everywhere (hubs ×6 languages, articles, study entries, generators, specs
  scrubbed); H1 fix on five pages; claim fixes ×6 languages; German copper H1; "Coming soon" off; retinol multiple consistent;
  ADR-W; commit `f125fb0`.
- 13:50–14:40 Collagen go-live (handle, SEO, redirect, links), menu entry + tile, stamp sets pre-order, hero right-aligned,
  explainer r2, meta translations, audit 9.74; commits `8324fe9`, `92386f2`.
- 14:40–16:30 Three result cards with Malcolm's picks (retouched); spoke 1 drafted (agent), published hidden, audited 9.68; local
  speed A/B (reveal animation = cause); model-face tile sheet; commit `b6ba6cc`. Malcolm's tile label unreadable; asked for the number.
- Didn't work: see §10.

## 17. Continuation prompt

> Read `/Users/malcolmsmith/Claude Code/Projects/skingenetix-website/.claude/handovers/2026-10-08-1634-main-plan-and-collagen-live.md`
> and continue from §4 "Next concrete action". FIRST read §2 (big picture & masterplan) to understand your role and position, then
> the plan in §12 and the knowledge in §13 **fresh**; do not rely on summaries here. Operate within §7 autonomy envelope. Halt at any
> §6 stop condition and ask Malcolm. Check `ListAgents` for other Skingenetix windows before any store write. Begin with a one-line
> confirmation of the cursor (§3) and your role (§2), then execute §4, unless Malcolm has answered §11 item 1, in which case do the
> tile first.
