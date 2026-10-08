# Session Handover — 2026-10-07 13:46 — skingenetix-website — study-outcome-sections

<!-- meta:
  rotation_reason: explicit user request (/session-handoff)
  approval_required: true   (the next gate is Malcolm approving the English of the new sections)
  schema_version: 2.0.0
-->

## 1. Mission

Malcolm's request of 2026-10-01: every clinical-study article gets **one section per proven trial result**, with a labelled before/after
picture where one honestly fits, plus **"how it works" blocks** for the effects that were tested, like the ingredient science pages. The
template is built and deployed. All eight articles have been measured against it and their content written. The English is on
previews. What remains: Malcolm approves the English, then five translations, then go-live.

## 2. Current cursor

- **Plan file:** `docs/todo.md` → entry **"STUDY-DETAIL"**.
- **Review:** `docs/review-2026-10-01-study-results-and-how-it-works.md`; §6 lists the open decisions.
- **Rules:** `docs/study-page-template.md` §3.1, including "First deploy" and "Deployed 2026-10-02".
- **Position:**
  - English previews of all **8** articles are built and verified (`<article>?view=clinical-study-draft`).
  - Design critique (Ye, Robinson): verdict FIX, partly applied. Done: the black-ground picture swapped, card headline at h3 size, pictures
    centred. Open: the structural proposal (a Malcolm decision).
  - Central audit: done on the **Ye preview only**. Uncapped **9.59**; the one confirmed failure, T8, is a preview artefact.
  - Still to audit: the other **7** previews. A background run stopped when the session ended.
- **Spec gate:** N/A (content work). **ADR:** ADR-2026-10-01-R in `docs/decisions-log.md`.

## 3. Next concrete action

Run the central audit (v2) on the seven remaining English previews, one at a time and 30 s apart: Badenhorst, Robinson, Watanabe, Wang,
Raikou, Tadini and Yogya. Fix only confirmed failures that are not preview artefacts. Then put the result to Malcolm for approval of the
English, as §6 of the review lists.

## 4. Verification recipe

```bash
cd ~/"Claude Code/Projects/seo-toolkit" && .venv/bin/python scripts/audit_page.py \
  "https://www.skingenetix.com/blogs/clinical-studies/<handle>?view=clinical-study-draft" \
  --criteria v2 --page-type evidence --keyword "<primary from configs/page-targets.json>" --serp --market en-US \
  --json "<wt>/docs/audits/page-audit-<date>-<handle>-preview-detail.json" --out "<wt>/docs/audits/page-audit-<date>-<handle>-preview-detail.txt"
```

**Expected:** "uncapped" is 9.0 or more, and the only CONFIRMED FAILURE is T8 or T4. Both are preview artefacts: the `?view=` address is not
in the hreflang set or the sitemap, and both clear at go-live.

Keywords:

| Article | Keyword |
| --- | --- |
| Wang | "argireline crow's feet" |
| Raikou | "argireline forehead lines" |
| Badenhorst | "copper peptide serum wrinkles" |
| Ye | "pdrn vs retinol" |
| Yogya | "pdrn after microneedling" |
| Tadini | "acetyl hexapeptide-3" |
| Robinson | "palmitoyl pentapeptide-4" |
| Watanabe | "glutathione brighten skin" |

## 5. Stop conditions (ask before)

- **Translating the new blocks or publishing them live.** Malcolm's rule: finish and approve the English first. A full
  `build-study-page.py --apply` refuses English-only blocks, by design.
- **Merging the content configs into main.** They stay on branch `study-outcome-sections` until translated: another window's `--apply` from
  main would refuse them.
- **Changes to the critic's structure** (a hero row plus a compact list). It is a new layout variant against the stock-sections-first rule;
  Malcolm decides.
- **Swapping the science-page pictures** that exceed their trials, and **retouching the reused Badenhorst pair**: both are §6 questions.
- **Any paid image generation.**
- **Store writes while another Skingenetix window is publishing.** Check `ListAgents` and message first.

## 6. Autonomy envelope (approved, proceed without asking)

- All `.md` edits and commits (standing approval, 2026-04-22).
- Shopify API content work as in the project CLAUDE.md. That covers preview builds (`--preview`), Files uploads, and theme uploads of our own
  section and the study article templates, if verified afterwards.
- Central audits: about USD 3 per audit and USD 12 per loop (standing, 2026-09-29).
- **Picture choice is delegated** (Malcolm, 2026-10-01: "find which ones work best per section… select from all available already created
  images"). Show the sheets on screen.
- Malcolm on 2026-10-02: "proceed" and "finish the work in this session".

## 7. Decisions log (don't re-debate)

- **Storage:** a companion `study_detail` metaobject (35 fields) per study, linked from the article as `study.detail` (`study.draft_detail`
  for previews). The `study` definition is full at 40 of 40 fields.
- **Sections:** both reuse the science pages' `research-before-after`. Order: glance → **outcomes** → chart → story → **mechanism** → limits.
- **A result counts as "proven"** when it is positive and significant against the comparison at p ≤ 0.05. Robinson's fine lines at
  p ≤ 0.10 are in, labelled with the bar (Malcolm).
- **Before/after only** where the face shows the measured area and the change does not exceed the result.
  - The six in use: Wang, Ye ×2, Watanabe ×2 and Badenhorst. Wang, Ye and Watanabe's crow's feet are new and retouched; Badenhorst and
    Watanabe's brightness are reused hub pairs.
  - Plain photos: Robinson (no size published), Yogya (no honest subtle pair), and every instrument-only result.
- **Wang's SNAP-25 lab block is allowed** (Malcolm). Raikou, Tadini, Yogya and Watanabe have no how-it-works block: nothing tested is
  allowed by the registers.
- **Ye's figures:** they come from Figure 6B, and the text says "significant" without p-values (the figure's legend does not define its
  marks). Eye bags are about 1.5×, not 2×; crow's feet are "more than three times".
- **Claim fixes, all live and verified in six languages** (Malcolm: "fix all").
  - Seven study configs.
  - The PDRN hub: card f4, stats s2, card f1, evidence row 02, FAQ q1 and the chart.
  - The Argireline register (Tadini line) and the PDRN register (claims 2/4/5).

## 8. Constraints learned this session

- **An empty section between same-background sections opens a gap.** Impact closes it with `--section-background-hash`. Hence
  `empty_previous_hash: "0"` on the mechanism slot. Never remove it.
- **A template uploaded seconds after a section schema change silently drops the new setting.** Re-upload and read it back.
- **The worktree** `../skingenetix-website-wt-outcomes` has no `.env`, `backups/` or `assets/` (all gitignored). `.env` and `backups` are
  symlinked; run image uploads from the main tree.
- **The Bash hook blocks Italian "su"** (it reads it as the `su` command). Write foreign text to a file with the Write tool.
- **`study-i18n.py merge` needs complete locale files.** Helper scripts are in the scratchpad (`i18n_update.py`); generate the files from
  the config. Live translations use a no-break space before `%` (de, fr, es) and before `; : ? !` (fr).
- **`study-template-build.py` builds the article templates from the branch's code.** It is cherry-picked to main; keep them in step.

## 9. Failed approaches (don't retry)

- **`cv2.inpaint` for moles** leaves a smooth, textureless blob. Clone ring-matched skin instead (memory
  `retouch-a-mole-by-cloning-skin-not-inpainting`).
- **Clone sources** taken across a diptych's 50% split, or from `BORDER_REFLECT` padding, copied the seam or the mole back.
- **Full-face selfie pairs** (the copper `eyes-m30`, the acetyl selfie folders): crow's feet are unreadable at 660px.
- **The Matrixyl card pool:** nearly every pair has moles, and Malcolm rejected that pool on 2026-09-29.
- **Opus subagents** hit the weekly limit on 2026-10-01 (reset on 10-04). The design critic ran on `model: sonnet`.

## 10. Open questions / awaiting Malcolm

1. **Approve the English** of the new sections, article by article, on the previews. Then translate and go live.
2. **The reused Badenhorst before/after** still shows a small mole near the eye: retouch it?
3. **Four science-page cards** still use pictures that exceed their trials: Argireline f1 and f5, PDRN f1, glutathione f2. Swap them for the
   new honest pairs?
4. **The German PDRN overview** says "mehr als doppelt so stark": true, but weaker than the English "more than three times". Upgrade it?
5. **The critic's structure** (FIX on both previews): about 10 same-weight picture-and-card rows in a row on PDRN. Should result 1 become a
   hero row with results 2–4 as a compact list? Robinson's plain pictures were called decorative. On phones the result pill is small
   (about 10.9px).

## 11. Plan & sub-plan references (read fresh)

- `docs/todo.md` (the STUDY-DETAIL entry)
- `docs/review-2026-10-01-study-results-and-how-it-works.md` (§1–§6)
- `docs/study-page-template.md` §3.1, §5 and §6
- `docs/decisions-log.md` (ADR-2026-10-01-R)
- `research/study-detail-2026-10-01/` (the researchers' proposals, source tables, register checks, `before-after-check.jpg`)
- `configs/banners/study-detail-images-2026-10-02.json` (every picture, its pool ref and the reason)

## 12. File state

- **Worktree:** `/Users/malcolmsmith/Claude Code/Projects/skingenetix-website-wt-outcomes`, branch `study-outcome-sections`, clean.
- **Modified this effort (all committed):**
  - `scripts/build-study-page.py`
  - `scripts/study-template-build.py`
  - `scripts/build-clinical-studies-blog.py`
  - `scripts/study-i18n.py`
  - `theme/sections/research-before-after.liquid`
  - `tests/test_build_study_page.py`, `tests/test_study_template_build.py`, `tests/test_study_i18n.py`
  - `tests/test_build_clinical_studies_blog.py`
  - `configs/studies/*.json` (8) and `configs/studies/i18n/*`
  - `configs/hub-upgrades/pdrn-research-card-f4-figure-6b-2026-10-01.json`, `configs/hub-upgrades/pdrn-research-figure-6b-2026-10-02.json`
  - `configs/banners/study-detail-images-2026-10-02.json`
  - `docs/claims/argireline-acetyl-hexapeptide-8.md`, `docs/claims/pdrn.md`
  - `docs/study-page-template.md`, `docs/decisions-log.md`, `docs/todo.md`
  - `docs/review-2026-10-01-study-results-and-how-it-works.md`
  - `research/study-detail-2026-10-01/*`
  - `docs/audits/page-audit-2026-10-02-pdrn-vs-retinol-split-face-trial-ye-2026-preview-detail.*`
- **Store state:**
  - The `study_detail` definition, and the article metafields `study.detail` / `study.draft_detail`.
  - `<handle>-draft` study and study_detail entries for all 8, linked as `study.draft` / `study.draft_detail`.
  - Live articles read `study.entry` and are unchanged.
- **Desktop sheets:**
  - `skingenetix-study-before-afters.png`
  - `skingenetix-study-plain-pictures.png`
  - `skingenetix-study-previews-new-sections.png`
  - `skingenetix-study-preview-ye-phone.png`

## 13. Git state

- **Branch** `study-outcome-sections`: last commit `de48fa7`, pushed, nothing uncommitted. Nine commits are not in main; that is
  deliberate (English-only content).
- **Main:** `848b2e6`, pushed. It has all the code: template, publisher, section guard, gap fix, heading and card CSS, tests (196 pass).
- **The main tree** shows another session's deleted and moved handover files, not mine. Leave them.

## 14. Session log

- **2026-10-01:**
  - Template built test-first (27 tests); `study_detail` design.
  - Five researchers read all eight trials and their lab studies, checked against the registers.
  - Review written; Malcolm decided (see §7).
- **2026-10-01/02, claim fixes** (seven studies ×6, the PDRN hub in 6 places, two registers): published after the other window's "hubs
  done" and verified live in six languages.
- **2026-10-02, pictures:**
  - The picture reviewers died on the usage limit, so the selection was done in-session.
  - Four new pairs retouched (clone method) and 23 plain pictures; 28 files uploaded in total, Ye's replacement included.
- **2026-10-02, template deployed:**
  - The empty-section 80px band was found by before/after measurement and fixed in 5 minutes (the other window re-audited Wang).
  - The section heading was centred.
  - Eight English previews were built and verified.
- **2026-10-02, critic (sonnet):** FIX on both. Black-ground image swapped, h3 size and picture centring done; structure to Malcolm.
- **2026-10-02, audits:** the Ye preview scored 9.59 uncapped (T8 artefact). The rest of the background run stopped at session end.

## 15. Continuation prompt

> Read `/Users/malcolmsmith/Claude Code/Projects/skingenetix-website/.claude/handovers/2026-10-07-1346-study-outcome-sections.md` and
> continue from §3 "Next concrete action". Work in the worktree `/Users/malcolmsmith/Claude Code/Projects/skingenetix-website-wt-outcomes`
> (branch `study-outcome-sections`); run image uploads from the main tree. Check `ListAgents` for other Skingenetix windows before any store
> write. Operate within §6; halt at any §5 stop condition and ask Malcolm. Re-read the files in §11 fresh. Begin with a one-line
> confirmation of the cursor (§2), then execute.
