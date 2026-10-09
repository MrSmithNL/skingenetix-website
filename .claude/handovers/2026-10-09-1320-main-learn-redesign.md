# Session Handover — 2026-10-09 13:20 — skingenetix-website — main (learn-redesign)

<!-- meta:
  rotation_reason: explicit user request (/session-handoff): "this session is run out of memory"
  approval_required: true   (several items wait on Malcolm, §10; none blocks §3)
  schema_version: 2.0
-->

## 1. Mission

Get every Skingenetix page and article to rank first on Google and in AI answers for its keyword (traffic plan
`docs/website-traffic-and-performance-plan-2026-10-08.md`, todo SEO-RANK-002), with pages that also look designed: this session's
last job is the **design run on the Learn article** ("full page design (content presentation, formatting and styling) improvement
run ... look at how the other pages are built ... before and after images for specific trial results ... use images where we can",
Malcolm, 2026-10-09).

## 2. Current cursor

- Plan: `docs/website-traffic-and-performance-plan-2026-10-08.md` → Part 6 → Phase 1 (1.5 speed done site-wide, 1.6 spoke 1
  published, 1.7 Learn blog template built as a preview, 1.10 monitor installed, 1.2 product drafts with Malcolm).
- Position: **Learn spoke 1 redesign** — hidden template built and verified structurally; the **design-critic review had been
  run; its cycle-1 report is saved in `docs/audits/2026-10-09-learn-argireline-matrixyl-design-critic-cycle-1.md`** (FIX).
- Spec gate: N/A (content/store). ADRs: `docs/decisions-log.md` ADR-2026-10-08-X and ADR-2026-10-09-Y (items 1–8).

## 3. Next concrete action

**Update 13:35:** the critic's cycle-1 report arrived after this handover was first written and is saved at
`docs/audits/2026-10-09-learn-argireline-matrixyl-design-critic-cycle-1.md` (FIX, not REBUILD; weighted 4.8). Apply its fixes to
`configs/hub-upgrades/learn-argireline-matrixyl-3000-design-2026-10-09.json` and re-apply with `python3 scripts/hub-upgrade.py <spec> --apply`
(allowed while no article uses the template): first the two blockers (the evidence table makes the phone page 740 px wide: add
`.sgx-evtable{min-width:0;max-width:100%}`; the step-1 photo `skingenetix-howto-step2-serum.jpg` has a watermark: swap it), then the
high items (alternate the backgrounds as listed, make "Do they work together?" a plain rich-text section, lower the key-figure
size a step, add a byline line under the banner, replace the Matrixyl beam render, a portrait mobile banner). Then run the
`design-critic` again (cycle 2, fresh context), audit the preview, switch the article
(`articleUpdate(id:"gid://shopify/Article/1002899276161", article:{templateSuffix:"learn-argireline-matrixyl-3000"})`), verify live,
audit live, show the renders on screen.

## 4. Verification recipe

```bash
# structure on the live URL after the switch (no ?view)
curl -s "https://www.skingenetix.com/blogs/learn/argireline-and-matrixyl-3000-together?v=$(date +%s)" -A "Mozilla/5.0" \
  | python3 -c "import sys,re;h=sys.stdin.read();m=h[h.find('<main'):h.find('</main>')];print(len(re.findall('<h1',m)),'h1;',m.count('<img'),'imgs;',h.count('Liquid error'),'errors')"
# expected: 1 h1; ~26 imgs; 0 errors
cd ~/"Claude Code/Projects/seo-toolkit" && .venv/bin/python scripts/audit_page.py \
  "https://www.skingenetix.com/blogs/learn/argireline-and-matrixyl-3000-together" --criteria v2 --page-type article \
  --keyword "matrixyl and argireline" --serp --market en-US --json "<repo>/docs/audits/page-audit-<date>-learn-...-live-2.json" --out ...
# expected: ≥ 9.0 (baseline today 9.9), zero confirmed failures (T4 sitemap lag clears once Shopify regenerates the sitemap)
```

Then a contact sheet of desktop 1440 + phone 390 on `~/Desktop/` and `open` it (Malcolm sees every render).

## 5. Stop conditions (ask before)

- New English copy going live or being translated (his rule 2026-09-29): the Learn list page's intro line; the product-page drafts;
  translations of spoke 1 (after its 14-day English measurement).
- Any image run or other spend beyond the standing audit budget; theme-wide settings; trial magnitudes on product pages (decision 15).
- Store writes while another Skingenetix window writes: run `ListAgents` first. Today windows **14** (competitor teardown,
  read-only) and **21** (keyword research + three wave-1 Learn drafts on the HIDDEN drafts blog, auditing them) were active; message
  them before audits (they pause Python fetches of skingenetix.com) and never stage their files.
- Never `--no-verify`, never `rm -rf`, never re-apply an old owning hub spec.

## 6. Autonomy envelope (approved — proceed without asking)

- `.md` edits/commits (standing); central audits (standing, ~USD 0.5–1 each); DataForSEO pulls of cents.
- Malcolm 2026-10-09: "proceed with all next steps and improvements ... verify fully complete and working on the live site";
  "publish the Argireline and Matrixyl 3000 together article ... then do a full page design improvement run" — so the redesign may
  replace the live article layout once critic + audit pass (it carries only approved text).
- Decision 5 approved (spend: weekly monitor ~USD 1/week; AI-citation panel; OpenAI credits are his to buy).
- Skin Concerns safety answer approved and live. Hero no-fade rule rollout approved and done.
- Commits through the clean-worktree recipe (memory `commit-through-a-clean-worktree-when-lint-staged-cannot-restore`).

## 7. Decisions log (don't re-debate)

- **Collagen page:** grid below the explanation (Malcolm: "make the changes so the collagen page scores maximum"), hero no-fade,
  four accuracy fixes, Mokhtar 2026 cited → 9.73–9.9, zero confirmed failures (ADR-2026-10-08-X). Judge-noise splits (C9/C11) are
  not "fixed".
- **Speed:** `scripts/hero-reveal-off.py` on 24 templates incl. the home slideshow (slideshow needs the first slide held too, or
  theme.js blinks the image); best warm Lighthouse runs 3.0–4.7 s everywhere (were 11–15 s); single runs jump 4 ↔ 12 s (simulation).
- **Skin Concerns:** real H1, fifth card Collagen Skincare, safety FAQ replaced (approved), four concern pages link up to the hub;
  cluster declared (`hub_url` in seo-toolkit `configs/skingenetix.config.json` 1d1d5c7 + `configs/page-targets.json`).
- **Learn article** published as approved; redesign uses its own template from stock modules, no main-article section, approved
  text cut out programmatically, three before/after cards: Wang 2013 (mole-free image
  `skingenetix-argireline-acetyl-hexapeptide-8-crows-feet-softened-before-after-study.jpg`), Raikou 2017, Matrixyl 3000 half-face.
  No chart (the article itself says the trials cannot be compared).
- **Product pages:** nine drafts for approval only, magnitudes kept off (rule 2026-09-26), "free from" line removed (EU Annex III).
- **Decision 3** shown as a validated page; Malcolm has not answered yet.

## 8. Constraints learned this session

- `translationsRegister` can report success and hold nothing (2 of 4 templates): verify each locale live; re-register.
- After a template write the first full browser load rebuilds compiled CSS (~2.5 s blank): warm with Playwright before Lighthouse.
- The central auditor read Impact's `…__content-with-nav` as navigation until seo-toolkit 7cfb5b3.
- Shopify's Custom CSS scoper splits `:is()` lists on commas (still works).
- `hub-upgrade.py` now builds/guards page, article AND blog templates (`pages_using` reads articles/blogs).
- The theme emits Article JSON-LD from the layout; the stock main-article section always prints the title as H1.
- Product content lives in descriptionHtml + `custom.key_benefits/how_to_use/full_ingredients/clinical_research` (rich text) +
  `custom.faq_items`/`how_to_steps` (metaobjects); live exports in `docs/drafts/product-pages-2026-10-09/_current-*.json`.
- `test_hub_i18n` was red because the five `configs/hub-i18n/*.json` lacked the team-credit byline (fixed d330554; 206 tests pass).

## 9. Failed approaches (don't retry)

- Lighthouse on a local copy compared with live (localhost HTML is "instant"); single Lighthouse runs as evidence.
- Showing only the slideshow carousel (blinks the image); a `pages_using` call for an article template before the fix.
- Retouching nothing: the Argireline hub's live crow's-feet card (`…crows-feet-before-after-close-up.jpg`) has moles — swap it.

## 10. Open questions / awaiting Malcolm

1. **API key restriction:** add PageSpeed Insights API + Chrome UX Report API to key "Claude 2" (ends …8_hQ) in project
   gen-lang-client-0740290272 (62087691133) → Credentials → API restrictions → Save. He was doing this at 13:00; test with a PSI call.
2. **Request indexing** for `/blogs/learn/argireline-and-matrixyl-3000-together` (new) — and the earlier two
   (`/pages/pdrn-research`, Tadini) he says he did; re-inspect with the URL Inspection API in a few days.
3. **Product drafts:** per page yes/edits/no + five decisions (`docs/review-2026-10-09-product-pages.md`; previews on
   `~/Desktop/skingenetix-product-previews/`).
4. **Decision 3:** "approve all" or strikes (`~/Desktop/skingenetix-decision-3-keyword-plan.html`); then update page-targets,
   product titles, monitor heroes.
5. **Learn list intro line** (preview `/blogs/learn?view=learn`): approve → assign blog `templateSuffix: "learn"`, translate.
6. Remaining plan decisions (Part 7): 6 study previews' English, 7 which apps are used, 8 formula sheet, 15 trial figures, 17 The Science pillar.

## 11. Plan & sub-plan references (read fresh)

- Plan: `docs/website-traffic-and-performance-plan-2026-10-08.md`; todo `docs/todo.md` (SEO-RANK-002 block, 2026-10-09 entries).
- ADRs: `docs/decisions-log.md` (ADR-2026-10-08-X, ADR-2026-10-09-Y).
- Specs: `configs/hub-upgrades/learn-argireline-matrixyl-3000-design-2026-10-09.json`, `blog-learn-design-2026-10-09.json`,
  `skin-concerns-*.json`, `*-hub-uplink-2026-10-09.json`; monitor `audits/visibility-monitor/config.json`.
- Review packs: `docs/review-2026-10-09-product-pages.md`; design templates `docs/science-page-template.md`, `docs/study-page-template.md`.
- Memory index: `~/.claude/projects/-Users-malcolmsmith-Claude-Code-Projects-skingenetix-website/memory/MEMORY.md` (new today:
  hero no-fade per page, Lighthouse warm-first, registration-can-fail, Learn articles get their own template, read the page note).

## 12. File state

- Modified/created this session (all committed): `scripts/hero-reveal-off.py`, `scripts/hub-upgrade.py`, `scripts/study-template-build.py`,
  `scripts/build-clinical-studies-blog.py`, `scripts/learn-article-draft.py`, `scripts/menu-image-tiles.py`, tests in `tests/`,
  `configs/hub-upgrades/*2026-10-09*.json`, `configs/hub-i18n/*.json`, `configs/page-targets.json`, `configs/learn/drafts/argireline-and-matrixyl-3000-together.json`,
  `audits/visibility-monitor/`, `docs/` (todo, decisions-log, architecture, review pack, drafts, audits).
- Outside the repo: smith-os `packages/forge/skills/seo-visibility-forensics/` (apex_host, b878de5) mirrored to `~/.claude/skills/`;
  seo-toolkit `configs/skingenetix.config.json` (1d1d5c7); `~/Library/LaunchAgents/com.skingenetix.visibility-monitor.plist`.
- Not mine (leave alone): windows 14/21 files — `audits/2026-10-09-competitor-teardown-top4/`, `audits/2026-10-09-microneedling-number-one/`,
  `audits/2026-10-09-new-article-keywords/`, `docs/article-plan-2026-10-09.md`, `scripts/keyword-research-adjacent.py` (+ test),
  three `configs/learn/drafts/*` wave-1 drafts and their audits; the old 2026-10-02 audit files.

## 13. Git state

- Branch `main`; last commit **c9e6d78** — "learn: spoke 1 published; its redesign built on a hidden article template; Learn list page on
  a hidden blog template". Pushed: yes. Uncommitted diff of mine: none (this handover is committed after).

## 14. Session log (2026-10-08 evening → 2026-10-09 13:20)

- Collagen: X1/S2 fixed, proof cards alternate, menu tile = Malcolm's #29, grid moved on his "maximum" order, hero no-fade, accuracy
  fixes; audits 9.73 → 9.9.
- Site-wide speed: hero no-fade on 24 templates + home slideshow (filmed for blinks); live verification with warm Lighthouse.
- Skin Concerns + concern pages + cluster; auditor bug reported and fixed in seo-toolkit; hub-i18n configs repaired.
- Product drafts (3 agents) + browser previews; decision 3 validated page; monitor installed + baseline; skill domain check fixed.
- Learn: spoke 1 published (9.9), summary fix + guard, comments closed, featured image, redesign template + Learn list template
  previews built; critic launched (no report received).

## 15. Continuation prompt

> Read `/Users/malcolmsmith/Claude Code/Projects/skingenetix-website/.claude/handovers/2026-10-09-1320-main-learn-redesign.md` and
> continue from §3. Operate within §6; halt at any §5 stop condition and ask Malcolm. Re-read the files in §11 fresh. Run
> `ListAgents` before store writes or audits. Begin with a one-line confirmation of the cursor (§2), then execute §3.
