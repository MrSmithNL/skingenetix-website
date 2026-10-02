# Four new clinical-study articles: live, and what is left for you

**Date:** 2026-10-01 · **For:** Malcolm · **Prepared by:** Claude
**Status:** **live in six languages** since 16:05 on 2026-10-01, on your go-ahead ("All four, now", given in another Claude window).
**Decisions taken 2026-10-01 ("1 - 4 = agree", all four recommendations):**

| #   | Decision                              | What was done                                                                                                                                                                                                                                   |
| --- | ------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Robinson's label becomes "Matrixyl"   | Live: card badge and filter label "Matrixyl" (`build-clinical-studies-blog.py`, TAGS). A Matrixyl 3000 trial keeps "Matrixyl 3000".                                                                                                             |
| 2   | "Firming" and "Brightening" labels    | Live in six languages on Tadini and Watanabe. Each label page links to its Skin Solutions page, worded as that page ("Straffung & Volumen", "Éclat & Glow" …).                                                                                  |
| 3   | Stamp set decided separately          | No change. The Yogya article does not link to it.                                                                                                                                                                                               |
| 4   | Matrixyl card 2 carries the threshold | Done in six languages in the **unreleased** Matrixyl rebuild, where card 2 lives (not on the live page). Three other "significant" mentions on the live page are a new question for you (see `docs/claims/matrixyl-3000.md`, claim 6).          |
| 4b  | …and the three live mentions          | Agreed ("agree on both"). Live and verified in six languages: the overview paragraph, "Give it at least 8 weeks" and the Robinson evidence row now say the paper counted p ≤ 0.10 as significant. The rebuild's two repeats were fixed with it. |
| —   | German "heller wirkend"               | Kept ("agree on both"). It matches the live glutathione research page and translates "brighter-looking"; "strahlend" would claim radiance, which the trial did not measure.                                                                     |

Undo for 1 and 2: the previous tags of all eight articles are in `backups/clinical-studies-article-tags-20261001-161634.json`, and the
list template's previous version in `backups/hub-upgrade-templates__blog.clinical-studies.json-20261001-161715.json`
(`hub-upgrade.py configs/hub-upgrades/clinical-studies-blog.json --rollback`). Undo for 4b: the Matrixyl template's previous version is
`backups/hub-upgrade-templates__page.research-matrixyl.json-20261001-170516.json`.

You asked for the next four clinical-trial articles, chosen by keyword value (2026-09-30). They were written, designed, checked by
the design critic, scored by the central auditor, translated, and published in the Clinical studies blog. This page shows what
went live and lists what is still yours to decide.

---

## 1. How to look at them

| Article                                          | Live page                                                                                                   | Desktop sheet                                     |
| ------------------------------------------------ | ----------------------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| **Yogya 2022:** PDRN with microneedling          | [live](https://www.skingenetix.com/blogs/clinical-studies/pdrn-microneedling-split-face-trial-yogya-2022)   | `~/Desktop/skingenetix-study-review-yogya.png`    |
| **Tadini 2015:** Argireline® and firmness        | [live](https://www.skingenetix.com/blogs/clinical-studies/argireline-skin-firmness-trial-tadini-2015)       | `~/Desktop/skingenetix-study-review-tadini.png`   |
| **Robinson 2005:** the original Matrixyl®        | [live](https://www.skingenetix.com/blogs/clinical-studies/matrixyl-wrinkle-trial-robinson-2005)             | `~/Desktop/skingenetix-study-review-robinson.png` |
| **Watanabe 2014:** glutathione and brighter skin | [live](https://www.skingenetix.com/blogs/clinical-studies/glutathione-skin-brightening-trial-watanabe-2014) | `~/Desktop/skingenetix-study-review-watanabe.png` |

Each sheet shows the whole English page on a computer screen (left) and on a phone (right, cut into strips; read them left to
right). The overview `~/Desktop/skingenetix-study-review-overview.png` shows the first screen of all four, with the four list-card
pictures along the bottom. The sheets were captured from the hidden previews at 15:55, just before go-live. The live English pages
carry the same content.

## 2. What each article says

**Yogya 2022.** 29 women in a hospital trial. Each had radiofrequency microneedling on the whole face, then a 0.3%
polynucleotide (PDRN-type) serum on one side and salt water on the other. Wrinkles around the eyes improved significantly on the
serum side by **2 months**, and on the salt-water side only by **6 months**. By 6 months both sides had drawn level. Keyword:
_pdrn microneedling_. The page says plainly that this backs PDRN after a clinic procedure, not as a leave-on serum.

**Tadini 2015.** 40 women, publicly funded (FAPESP, Brazil), 10% Argireline® cream against the same cream without it. The trial
measured **firmness, not wrinkles**: a firmness signal on the face fell by about a third within two weeks and stayed down. The plain
cream made no significant change. Keyword: _acetyl hexapeptide-3_ (the name the paper uses).

**Robinson 2005.** 93 women, 12 weeks, run by Procter & Gamble. One side of the face got a moisturiser with palmitoyl
pentapeptide-4, the peptide in the **original** Matrixyl® (our serum has it alongside Matrixyl® 3000). The other side got the same
moisturiser without it. Fine lines and wrinkles improved more on the peptide side from week 8. Scientists usually accept a result
when there is less than a 1-in-20 chance it is a fluke. The wrinkle results pass only the looser 1-in-10 bar the authors chose
(p ≤ 0.10), and the page says so in its key figure. Smoother texture (week 4) and fewer age spots (week 12) pass the usual bar. The
full paper is behind a paywall, so the page is built from the abstract and four published reports of it, and it says so. Keyword:
_palmitoyl pentapeptide-4_.

**Watanabe 2014.** 30 women, 10 weeks, a 2% glutathione lotion on one side and a placebo on the other. Skin pigment fell **10.7%**
against **3.1%** with placebo, a difference measurable from week 1. By week 10, 77% of the women rated the treated side
moderately brighter (23% the placebo side). It was run by the company that makes the ingredient, and the page says so. Keyword:
_glutathione brighten skin_. The wording follows the glutathione rules: "brighter-looking", never "lighten" or "whiten".

**Scores** (central auditor, run on the previews; the bar is 9.0 or more with no confirmed failures):

| Article  | Before the design fixes | After the design fixes |
| -------- | ----------------------- | ---------------------- |
| Yogya    | 9.65                    | 9.50                   |
| Tadini   | 9.65                    | 9.50                   |
| Robinson | 9.59                    | 9.55                   |
| Watanabe | 9.69                    | 9.84                   |

All four cleared the bar. The only failures were the ones a hidden preview causes itself ("not in the sitemap", "hidden from
Google"), and going live removes them. The small drops after the fixes come from the judges disagreeing about one question, which
the rules say not to chase. **The live pages are being re-audited now** in the other window.

---

## 3. Decisions still open

### Decision 1: Robinson's label on the list page (live now as "Matrixyl 3000")

Every article carries an ingredient label on its card and in the filter row. The builder labels anything Matrixyl as
**"Matrixyl 3000"**, so that is what Robinson's card shows live. But Robinson tested the original Matrixyl®, and the Matrixyl
claims register says never to mix the two up. (The page itself explains the difference in its first lines.)

- **A. Change it to "Matrixyl" (recommended).** This is accurate. A Matrixyl 3000 trial would get its own label later.
- **B. Keep "Matrixyl 3000"** as the family name, matching the research page it links to.

### Decision 2: Two new skin-concern labels

The list page has a second filter row for skin concerns (fine lines, crow's feet, forehead lines, compared with retinol). Yogya
and Robinson went live with the fine-lines and crow's-feet labels. Tadini and Watanabe fit none of the existing ones, so they went
live with their ingredient label only.

- **A. Add "Firming" (Tadini) and "Brightening" (Watanabe) (recommended).** Each label's page would link to the matching Skin
  Solutions page (Firming & skin density, Brightening & glow), as the wrinkle label already does. Both labels need translating.
- **B. No new labels.** The two articles stay under their ingredient only.

### Decision 3: The PDRN microneedling stamp set

The **PDRN Microneedling Facial Stamp Set, 1 Month** (EUR 89) is set up in Shopify but not on the shop, and has no stock. The copper
version (EUR 69) is the same. The Yogya article could become its evidence page.

**One caution first.** Yogya tested **radiofrequency microneedling done in a hospital**, not a home stamp. The PDRN claims register
marks the result as **"not transferable"** beyond skin opened by that kind of procedure. So if the set launches, its page can cite
Yogya as background on the ingredient, never as proof that the stamp works.

- **A. Keep the stamp set a separate decision (recommended).** The Yogya article does not depend on it. It links to the PDRN
  research page and the PDRN serum and night cream, not to the stamp set.
- **B. Launch the stamp set now.** This needs stock, its page checked against the register, and its usage claims checked. A to-do
  item already lists "stamp-set usage frequency" as unsupported wording.

### Decision 4: One card on the Matrixyl research page

Card 2 on the Matrixyl® 3000 research page describes the Robinson result as "significant" without saying it passed only the
looser 1-in-10 bar. The new article states that bar openly, so the two pages now describe the same result differently.

**Correction (2026-10-01, after your answer):** card 2 is in the unreleased rebuild of the Matrixyl page, not on the live page. This
note first said "live", repeating the register without checking the page. The fix went into the rebuild. The live page says
"significant" without the threshold in three other places. You agreed to fix them too, and they are live (row 4b above).

- **A. Add the bar to the card's wording (recommended)**, in all six languages, so the hub and the article agree.
- **B. Leave the card as it is.**

### Already live: the card pictures

As last time, Claude made the first choice of the four list-card pictures from the no-models science pool, in the ingredient
colours and each different from its page's banner and story picture. They went live with the articles and are along the bottom of
the overview sheet:

| Article  | Pool number | Picture                                           |
| -------- | ----------- | ------------------------------------------------- |
| Yogya    | PDRN-038    | fine rose-coloured strands on dark graphite       |
| Tadini   | ARG-112     | a wave of light losing height across a dark field |
| Robinson | GEN-159     | a close-up network of fine teal fibres            |
| Watanabe | GEN-221     | a shallow pool of clear liquid on champagne gold  |

**Name a pool number to swap any of them.** One picture was passed over on purpose: PDRN-012, a cell nucleus, suggests "repairs
DNA", which the PDRN claims register rules out.

### Later, no rush

The design critic raised things that reach beyond these four pages:

- **The chart design is shared with all five research pages.** It suggests the values at the bar ends, the data table folded away,
  and captions on the left. Changing it changes the approved hubs too, so it waits for your word.
- **Photographs of the instruments the trials used** (the microneedling device, the skin meters). This would be a paid image run
  across every supplier, so it needs your approval and a budget.
- **Two pictures repeat on every study page.** The microscope beside "How to read this result" and the scientist beside "Where
  this trial sits in the evidence" are the same on all eight study pages. This is already on your list of template items (T7).
  The instrument photographs above would be one way to replace them.

---

## 4. What is still to happen

The other Claude window that published the articles is finishing go-live:

1. Check every article in all six languages.
2. Remove the four hidden preview drafts.
3. Audit each live page against the 9.0 bar.

**For you:** press "Request indexing" in Google Search Console for the four new addresses above. There is no way to do that from
code.

**Undo:** each article can be unpublished from the blog in one step. The study content stays stored in Shopify, so it can be put
back without rebuilding.

## 5. Sources

- Page rules: `docs/study-page-template.md` (§3 go-live, §4 hard rules)
- Design critique: `docs/audits/2026-10-01-new-study-drafts-design-critique.md`
- Audits: `docs/audits/page-audit-2026-09-30-*-draft-preview*.txt`
- Claims registers: `docs/claims/pdrn.md`, `argireline-acetyl-hexapeptide-8.md`, `matrixyl-3000.md` (Robinson threshold and card
  f2, line 149), `glutathione.md`
- Configs: `configs/studies/<handle>.json`
- Go-live commits: `aafd247` (translations), `b35ed71` (live)
