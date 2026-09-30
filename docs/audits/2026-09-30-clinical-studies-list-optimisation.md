# Page note: the Clinical studies list, `/blogs/clinical-studies` (Rule 27, checks A–E)

**Date:** 2026-09-30.
**Built by:** `scripts/build-clinical-studies-blog.py`, which writes `configs/hub-upgrades/clinical-studies-blog.json` for `hub-upgrade.py`.
**Live in:** six languages.

**Status:** the audit shows gates 6/6 and a score of 9.18. One confirmed failure is left (C3, below), and its fix is with Malcolm.
Under ADR-2026-09-30-Q the page is **not done** until that failure is gone.

## The page's plan row

| Question           | Answer                                                                                                                                                                                                                                                                                                       |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Job**            | The index of our clinical-study appraisals. It is the credibility layer behind every claim, and it lets a reader find a study by ingredient, by skin concern or by search.                                                                                                                                   |
| **Keyword**        | "skincare clinical studies" (Malcolm, 2026-09-30). It has no measured demand in any of the six markets, so this is an evidence page, not a traffic page (ADR-2026-09-30-K). Data: `configs/keyword-data/list-page-2026-09-30/`. "science backed skincare" (151 US + 157 GB) is left to `/pages/the-science`. |
| **Blocks**         | 1. Photo band: title, intro, a search box that searches the studies only. 2. Label rows: ingredient; skin concern plus a topic. 3. The list (stock main-blog). 4. "Before you try it". 5. "Studies by ingredient", with links to each hub's evidence table and to the shop.                                  |
| **Primary action** | Open a study. The quiet second step is the shop link in the closing band.                                                                                                                                                                                                                                    |

## A · Design and visual

- **Critic cycle 1** (preview, 2026-09-29): FIX 5.71. Every page-level finding was fixed.
- **Critic cycle 2** (live, 2026-09-30): FIX 6.55, in `2026-09-30-clinical-studies-blog-list-critique-cycle2.md`. Page-level
  findings fixed, then applied live on Malcolm's go (commit `135d891` and after):
  - **First screen on phones.** Each label row is one line that scrolls sideways, the phone band is 320px, and the lead photo is 2:1.
    The first study's title now sits at y = 790 (EN) and 826 (DE) of 844; it was at 991.
  - **Consistency and type.** One badge style; the intro is 17px (16px on phones); the closing band lines up with the list.
  - **Accessibility.** Titles hyphenate at 200% zoom, the cards have a focus ring, and there is no card zoom under reduced motion.
  - **Labels.** The "Skin concern" heading is set as a caption, not as a link.
- **Contrast**, measured at 390, 768, 1024 and 1440 in EN and DE: the lowest is 4.58:1.
- **Tried and reverted:** the tablet crop (N8). It put the flasks under the text, and the intro dropped from 7.90 to 2.31:1.
- **Open:**
  - the four card images are in four different styles (N1, image work);
  - the tablet photo shows no subject (N8). This waits on the blog's own banner, which is Malcolm's pick from the science sheets;
  - card titles are `<p>`, and the H1 comes late in reading order (F16, a core theme edit);
  - the search results page is thin (N5, theme template).
- **One cycle is left** under the three-cycle cap.

## B · Content and voice

- **Every word is approved copy.**
  - The intro and interface words come from `configs/hub-i18n/clinical-studies.json`.
  - The safety note is the approved study note (`configs/study-safety-note.json`); only its opening changes for a list.
  - The payment answers use facts read from Shopify (Malcolm approved the English).
- **No invented facts.** The card excerpts are the articles' approved SEO descriptions.
- **Safety.** The "Before you try it" note is on the page (Malcolm: "Add the note, aim for 9+"). It gives use guidance only, never
  "safe" (EU Reg 655/2013).

## C · Search (SEO) and strategy fit

- **Title.** "Skincare Clinical Studies, Read in Full | Skingenetix", 46–59 characters in six languages, with the keyword once.
- **Meta description.** A new one in six languages (127–153 characters); the page had none.
- **One H1.** It is the blog's translated title, hidden visually in main-blog's banner; the visible title on the photo is aria-hidden.
- **Hub links.** The closing band links to all five hub evidence tables.
- **Label pages.** `/tagged/*` stay indexed (Malcolm, 2026-09-30). They share the list's title (open: a core layout edit).
- **Search.** The article bodies carry each study's approved text for site search; it is never rendered.

## D · Conversion

- **Primary action.** One: open a study. The shop link sits in the closing band.
- **Customer service.** Payment help is now reachable site-wide: four payment Q&As on `/pages/faq`
  (`configs/hub-upgrades/faq-payment-2026-09-30.json`) and a "Payment" link in the footer's Support menu
  (`scripts/footer-support-payment-link.py`). All six languages.
- **Agency row X2** ("next steps, costs, timing"): not applicable to an evidence index. Skipped under the loop's rules.

## E · AI answer eligibility (GEO)

- A1–A3 pass: the page is snippet-eligible, the AI search crawlers are allowed, and the main content is in the server HTML.
- T8 passes: five language alternates, reciprocal.
- No FAQPage markup and no `llms.txt`; neither is required (Rule 27 E, revised 2026-09-29).

## Central audit (seo-toolkit v2, `--page-type collection`)

| Run           | Keyword                   | Gates                                | Score    | Coverage | Confirmed failures                                               |
| ------------- | ------------------------- | ------------------------------------ | -------- | -------- | ---------------------------------------------------------------- |
| 1, 2026-09-30 | none                      | 5 pass                               | 6.65     | 24/44    | Q7 no meta description · R6 no payment help · V1 no safety note  |
| 2, 2026-09-30 | skincare clinical studies | **6 pass** (T8 hreflang now checked) | **9.18** | 32/46    | **C3**: the cards give headline results without the trial's size |

**The fix proposed for C3** is to add each trial's size and design to its card summary. The card summary is also the article's
search-result description.

| Card       | Summary                                                                       | Owner                   |
| ---------- | ----------------------------------------------------------------------------- | ----------------------- |
| Badenhorst | Already has "40 women"                                                        | done                    |
| Raikou     | "In a randomised trial of 24 women, forehead roughness fell 7.4% in 20 days…" | this window             |
| Wang       | "…double-blind trial of 60 adults…"                                           | the d1 window's rebuild |
| Ye         | "…split-face trial of 31 women…"                                              | the d1 window's rebuild |

Each change alters live, translated text, so it needs Malcolm's go.

**Update, 2026-09-30 (Malcolm: yes).** Raikou's summary is live with "24 women" (meta description, JSON-LD, card). Wang and
Ye get their sizes in the d1 rebuild. Re-audit the list once those are live.
