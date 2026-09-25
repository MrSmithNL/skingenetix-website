# Science pages: the open design-critique proposals, before and after (2026-09-25)

**Why this exists.** On 2026-09-24 the `design-critic` agent judged `/pages/pdrn-research` (FIX, 6.50). The page-level fixes were made the same day. Six
proposals would also change the approved Argireline template, so they were parked for Malcolm (`docs/todo.md`, CONTENT-001, the 🛑 line). Malcolm asked: _"show
me before and after on screen so I can decide."_

**What was made.** One contact sheet per proposal, plus an overview. Every "after" is a **browser-only mock**. A headless browser loaded the live page, injected
CSS or HTML into its own local copy, and took a screenshot. **Nothing on the store was changed.** The values in the captions were measured from the live pages
that day, not estimated.

| Sheet                                  | File on the Desktop                            |
| -------------------------------------- | ---------------------------------------------- |
| Overview (all six)                     | `~/Desktop/skingenetix-design-proposals.png`   |
| 1 Body text size                       | `~/Desktop/skingenetix-design-proposals-1.png` |
| 2 Phone title vs key figures           | `~/Desktop/skingenetix-design-proposals-2.png` |
| 3 New PDRN hero banner                 | `~/Desktop/skingenetix-design-proposals-3.png` |
| 4 Usage-image variety                  | `~/Desktop/skingenetix-design-proposals-4.png` |
| 5 One grading scale                    | `~/Desktop/skingenetix-design-proposals-5.png` |
| 6 Collapse the sources table on phones | `~/Desktop/skingenetix-design-proposals-6.png` |

**Already decided, not mocked: "one accent colour".** The critic wanted blue kept for links only, because copper's clinical blue clashed with PDRN rose. Malcolm
decided on 2026-09-24 that each page uses its own ingredient accent (template §3.6: PDRN rose, Argireline slate, copper blue, Matrixyl teal, glutathione
champagne). That is live, so the clash the critic saw is gone.

**The source critique** is the design-critic's report from the 2026-09-24 session (agent transcript `37e57ac1…/subagents/agent-af6cb6d8972c330d5`). It was never saved in the repo, so its words are quoted below.

---

## Decisions for Malcolm

1. **Body text:** raise it to 17 px on desktop and 16 px on phones? If yes, across the whole site (one theme setting) or on the science pages only?
2. **Phone title:** A (title up to 52 px), B (key figures down to 36 px), or leave it?
3. **PDRN hero:** pick one of the 27 banners already generated for this slot, approve a small new generation wave, or keep today's centred hero?
4. **Usage images:** vary the subjects and shapes? If yes, use existing files (as mocked) or brief one new "where it comes from" image per ingredient?
5. **Grading:** adopt one scale, A · B · C · D · Review, on all five pages?
6. **Collapsing the sources table on phones:** drop the proposal (it is mostly moot now), or collapse the table anyway?

---

## 1. Body text size

**What the critic said:** _"Body text is 15px at 1440 and 14px at 390 (cards, table, usage). The rule is 17–20px, and the trial population was 35–55."_ Fix: 16–17 px on phones.

**Measured today (PDRN, the same on all five pages):**

| Text                                                                     | 1440              | 390              |
| ------------------------------------------------------------------------ | ----------------- | ---------------- |
| Theme base (`--text-base`): finding cards, FAQ answers, key-figure notes | 15 px (0.9375rem) | 14 px (0.875rem) |
| Sources table body (`.est__ap`)                                          | 15 px             | 15 px            |
| How-to step text (`.uz__d`)                                              | 16 px             | 16 px            |
| Usage paragraphs (`.uz__p`)                                              | 17 px (already)   | 16 px (already)  |

**What the "after" changes:** base text **15 → 17 px on desktop and 14 → 16 px on phones**. The cards, step text and sources table follow at the same size, and the evidence-index qualifiers go to 16 px. Captions, bylines, the author line and study meta lines stay small on purpose.

```css
/* desktop */
:root {
  --text-base: 1.0625rem;
}
.uz__step .uz__d,
.est table,
.est__ap {
  font-size: 17px;
}
.evd__qual {
  font-size: 16px;
}
/* ≤699px  */
:root {
  --text-base: 1rem;
}
.uz__step .uz__d,
.est table,
.est__ap {
  font-size: 16px;
}
```

**The cost the mock exposed:** every finding card gets taller than its photo. The text column overruns the image by:

| Card | Today  | At 17 px |
| ---- | ------ | -------- |
| 1    | 129 px | 292 px   |
| 2    | 15 px  | 108 px   |
| 3    | 72 px  | 227 px   |
| 4    | 52 px  | 144 px   |

The critic separately flagged the overrun as a fault (finding 7: _"trim cards 1, 2 and 4 so the text fits in 660px"_). Bigger text therefore needs shorter card copy, or it makes that fault worse.

**Pages:** all five. The theme base drives the stock sections everywhere. The custom sections exist only on the two template pages (PDRN, Argireline) until the other three move onto the template.

**Two ways to do it:**

- **Site-wide:** the theme's typography setting (the one behind `--text-base`) changes body text on every page, including products and collections. It is one setting and quick to change, but every page type then needs a visual check.
- **Science pages only:** put the CSS in each section's `custom_css`. That field sits beside `settings` in the template JSON, not inside it (memory `custom-css-is-a-sibling-of-settings-not-a-member`). About 30 minutes for the two template pages.

**Risk:** translations are unaffected either way, because this is CSS only and not custom-html copy. Do **not** edit the `<style>` inside the four custom-html sections for this: any change to their English HTML makes all five translations stale until `scripts/hub-i18n.py` is re-run.

**Decide:** raise body text to 17 px desktop / 16 px phone? Site-wide or science pages only?

---

## 2. Page title larger than the key figures on phones

**What the critic said:** _"At 390 the H1 is 40px but the key figures are 45.5px, so the figures outrank the H1."_ The H1-to-body ratio is 2.86×, against a rule of at least 3×. Fix: _"make the H1 larger than the key figures."_

**Measured today at 390:** H1 40 px, key figures 45.5 px, on PDRN and Argireline alike.

| Option | Change (phones only, ≤699 px)                | Result                                                                                                                                  |
| ------ | -------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| **A**  | hero `h1{font-size:52px;line-height:1.02}`   | Title still 2 lines. H1-to-body 3.7× (3.25× with proposal 1). Hero contrast stays above 4.5:1: eyebrow 4.71, H1 6.3 (today 4.81 / 6.6). |
| **B**  | stats section `--impact-text-font-size:36px` | The key figures lose some punch. The band gets 34 px shorter (738 → 704 px).                                                            |

**Pages:** all five use the same stock hero and key-figures sections. The change goes in each page's hero (A) or stats (B) section `custom_css`. **Check
first:** longer H1s such as "Argireline® (Acetyl Hexapeptide-8)" and "Glutathione for Skin (GSH and GSSG)" may run to 3 lines at 52 px. Option A may need 48 px
on those pages.

**Effort:** 15–20 minutes. **Risk:** low. It is CSS in stock sections, so translations are unaffected.

**Decide:** A, B, or leave as is?

---

## 3. A new PDRN hero banner

**What the critic said:** _"The text is centred over the busiest part of the helix image … The art direction says the text zone sits in the left or right third,
never the centre. The reference hero is left-aligned on a quiet two-thirds."_ It named this _"the single change that would help most: recompose the hero: text
left-aligned on a banner with the helices in the right third and a quiet 40% on the left, as on Argireline."_

**Where it stands:** the contrast failure the critic measured (2.85:1) is already fixed. The overlay went up to 50% on 2026-09-24, and today's hero measures
**H1 5.63:1, subtitle 5.08:1** at 1440 and **eyebrow 4.81, H1 6.6** at 390. What remains is the composition: the hero breaks the art-direction rule and differs
from the template.

**No images were generated.** Suitable banners already exist. The 2026-08-25 wave `configs/banners/page-pdrn-research-banner.json` was briefed for exactly this:
_"the LEFT 40% OF THE FRAME IS EMPTY GRAPHITE"_, with the helix or strands on the right, at 4.39:1. It holds **27 unused candidates**: 3 concepts (PDR-1
helix-right, PDR-2 strand drift, PDR-3 membrane knit) × 9 engine outputs, all in `assets/ai-generated/2026-08-22-multi-page-pdrn-research-banner/`. The live
banner came from the sister wave on the same day: Malcolm picked PDG-1 (helices at both edges), whose quiet zone is the centre.

**The mock:** four of the 27 in the live hero, text left-aligned, overlay 50 → 25% (Argireline's level). These four illustrate the idea; they are **not a
shortlist**. All 27 are on the sheet. Contrast was measured as the critic did: hide the text, take the 98th-percentile background pixel under each line, compare
with white.

| Candidate                         | H1     | Subtitle                             |
| --------------------------------- | ------ | ------------------------------------ |
| PDRN today (centred, 50% overlay) | 5.63:1 | 5.08:1                               |
| Argireline reference (left, 25%)  | 16.3:1 | 15.1:1                               |
| PDR-1-helix-right-seedream_01     | 16.3:1 | 16.3:1                               |
| PDR-1-helix-right-nbp_pro_01      | 16.9:1 | 17.0:1                               |
| PDR-2-strand-drift-nbp_pro_01     | 16.2:1 | 16.2:1                               |
| PDR-3-membrane-knit-seedream_01   | 7.0:1  | 6.3:1 (strands reach under the text) |

**What changes if one is picked:**

- the hero `image` and `mobile_image`, via a publish config like `configs/banners/page-pdrn-research-publish.json`;
- `overlay_opacity` 50 → 25;
- the text-position setting set to the one Argireline's hero uses.

The phone needs its own crop from the chosen file, as the current banner has (a 4.4:1 frame shows only empty graphite at 1:1). The crop is made in post, and nothing is generated. The Seedream files are already 4.39:1. The Nano Banana ones (2.36:1) are cropped, as the live banner was.

**Also update:** template doc §6.1, which says _"PDRN's [banner] is quiet in the centre, so its text stays centred"_.

**Effort:** about 1 hour: crop, export, upload through the Files API, change the settings, verify in six languages. **Cost:** nothing if an existing file is
picked. A new wave (Seedream is the only engine that honours wider than 3:1) needs a cost quote and Malcolm's approval before it runs. **Risk:** low. It is a
stock section, so the translated hero text is untouched; only image and layout settings change.

**Decide:** pick one of the 27 existing banners, approve a small new wave, or keep today's centred hero?

---

## 4. Usage-image variety

**What the critic said:** _"Row 1, 'Salmon DNA', is a second pink helix render, the same idea as the hero; the one row about salmon shows no salmon and no
sourcing. The serum bottle appears three times within about 1,700px. 9 of the 11 content images are 1:1 squares (rule 31 asks for at least 4 aspect ratios)."_

**Measured today:**

- PDRN has **7 of 8** content images square; the product cut-out is the one exception.
- Across the five pages' usage sections, **9 of 10** images are square; glutathione's micrograph is 0.87.
- The PDRN usage rows today:
  - row 1: the pink helix `skingenetix-pdrn-polynucleotide-dna-helix-skin-research.jpg`, which is also the PDRN ingredient tile;
  - row 2: serum and night cream on rippled water, **Malcolm's pick on 2026-09-24**;
  - row 3: a model applying the serum from the bottle.
- If proposal 3 puts a helix in the hero, row 1 repeats it even more directly.

**The mock (existing files only):**

- row 1 becomes the lab photo from the philosophy page (`skingenetix-cosmetic-chemistry-scientist-phone.jpg`), shown at 4:5;
- row 3 is cropped to 4:3;
- row 2 is left alone.

**Caveats:**

- No image of sourcing or salmon exists; the banner briefs kept "salmon" out on purpose, to avoid fish imagery on a clinical page.
- The lab photo is AI-generated and could be read as "our scientist in our lab". Malcolm should judge whether that implies more than we can say.
- Per his naming rule, it would be uploaded as a copy under a `skingenetix-pdrn-…` name.

**What changes:**

- **Image shape:** `aspect-ratio` on `.uz__media img` per row. This is CSS, so it goes in `custom_css` and has no translation impact.
- **Image swap:** the `<img>` sits inside the usage custom-html, so the English HTML changes. Re-run `scripts/hub-i18n.py` for the five locales.

**Pages:** all five. Do it now on PDRN and Argireline; do the other three as part of their move onto the template.

**Effort:** about 1 hour on PDRN with an existing file. **Cost:** a "where it comes from" image per ingredient would need a small generation wave, quoted first.

**Decide:** vary the usage images and shapes? If yes, use existing files like this, or brief one new "sourcing" image per ingredient?

---

## 5. One grading scale, site-wide

**What the critic said:** _"PDRN: A · D · X · Not PDRN · Review. Argireline: A · B · C · Review. With no B or C, the PDRN legend jumps from A to D and looks like grades are missing … define one site-wide scale in the template doc and use the same letters on every page."_

**Measured today (five pages, five ways):**

| Page                     | How it grades                                                                                         |
| ------------------------ | ----------------------------------------------------------------------------------------------------- |
| PDRN (template)          | pills **A · D · Review**. The legend defines only those three, so it still jumps from A to D          |
| Argireline (template)    | pills **A · B · C · Review**, with no D                                                               |
| Copper (old layout)      | text: "Grade A−", "Grade B", "Grade B, secondary", "Grade A, null result", C, D, "Independent review" |
| Matrixyl (old layout)    | text: A, B, D                                                                                         |
| Glutathione (old layout) | text: A, B, X, "Grade A, different molecule", "Grade A for the combination only"                      |

**The mock (on PDRN):** one five-step legend replaces the partial one:

> **A** controlled human trial, measured by instrument · **B** smaller, uncontrolled or manufacturer human data · **C** human skin samples in the lab · **D** cells or animals · **Review** a summary of other studies

It is shown in full on every page, with the letters a page does not use faded, so no gap looks like a missing grade. The pill styles already exist (`.est__pill--a/b/c/d/r`).

The claims registers already grade with the same A–D letters (e.g. `docs/claims/pdrn.md` line 51). Their X and ≠ grades are no longer needed on the pages, because ADR-2026-09-24-P dropped those rows.

**What changes:**

- template doc §3.5 gains the scale;
- on PDRN and Argireline, the `evidence_sources` lead paragraph plus the legend strip. This is a custom-html edit, so the five definitions go into each page's phrase table and `scripts/hub-i18n.py` rebuilds the locales. Verbatim titles are not touched.
- The other three pages take the scale when they move onto the template. There:
  - copper's "A−" becomes "A", and the caveat that the minus carried (maker-funded, weaker journal) stays in the row text;
  - glutathione's X rows and copper's null-result row are removed under ADR-2026-09-24-P anyway.

**Effort:** 1–2 hours for the two template pages, translations included. **Risk:** grade letters sit next to claims. Every grade must match the page's claims register, and must not be re-judged while rewording.

**Decide:** adopt this one A · B · C · D · Review scale for all five pages?

---

## 6. Collapse the sources table on phones (`<details>`)

**What the critic said:** _"The table is 6,145px tall, 25% of a 24,200px page and about 7 screens. Five of the 14 rows (3 × X, 2 × Not PDRN) exist only to say they do not apply."_ Fix: group those five in a native `<details>`.

**Why it is mostly moot:** those rows are gone. Since 2026-09-24 (positive results only, ADR-2026-09-24-P) the tables keep only the studies the claims rest on, so there is nothing left to group. Measured at 390, where one phone screen is about 844 px:

| Page       | Rows       | Table                              | Whole section | Collapsed (mock) |
| ---------- | ---------- | ---------------------------------- | ------------- | ---------------- |
| PDRN       | 4 (was 14) | 1,555 px (~1.8 screens; was 6,145) | 1,974 px      | 504 px           |
| Argireline | 8          | 3,223 px (~3.8 screens)            | 3,696 px      | 558 px           |

The mock collapses the **whole** table behind "Show all N studies and their grades", because the rows the critic meant no longer exist.

**Against doing it:**

- The table is the page's signature: _"every claim is one click from its study."_
- The evidence index's "See all N studies" button jumps to `#evidence-sources`, and on a phone it would land on a closed box unless a small script opens it.
- Opening it on desktop and closing it on phones cannot be done in CSS alone.
- The summary text needs translating (custom-html, so `hub-i18n.py`).

**Decide:** drop the proposal (recommended for PDRN), or collapse the table on phones anyway (only worth weighing for Argireline's 8 rows)?

---

## How the mocks were made

- **Browser:** Python Playwright, headless Chromium, 1440 × 900 desktop and 390 × 844 phone (2× pixel density).
- **Pop-ups and header:** requests to Klaviyo and Shopify Forms were blocked, and the sticky header was set to static so it does not repeat over the crops.
- **Page order:** PDRN first, then copper, Matrixyl and glutathione. Argireline was captured last, because another session was changing its card-5 image.
- **Mocks:** each "after" was CSS or HTML injected into the local page copy only.
- **Measurements:** font sizes are computed styles; heights are CSS pixels. The card overrun is the text column's height minus the image's. Contrast uses the critic's method: text hidden, 98th-percentile background luminance under each text line, WCAG contrast against white.
- **Where the files are:** capture scripts, raw captures and `measure-*.json` are in the session scratchpad. They are not in the repo, because none of it is needed to act on a decision.
