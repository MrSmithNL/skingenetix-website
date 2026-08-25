# Ingredient tile picks — /pages/the-science — 2026-08-25

Malcolm's picks, recorded from a message that landed in the **copper-peptide-research
session** while the images belong to the **ingredient-tile waves**. Written down here so
they survive the session boundary, because two Claude Code sessions were working this repo
in parallel on 2026-08-25 and neither can see the other's transcript.

**Nothing here has been uploaded or published.** This is a record, not an action.

---

## Why the confusion happened — the naming is not unique

Five ingredients each got **two** waves — an A/B/C "material" set and a D/E/F "cell" set —
so there are **9 waves and ~334 candidates**, and **the slot letters A–F restart for every
ingredient**.

That makes a bare candidate name ambiguous. `D-cell-field-gpt_image_01` exists as **two
different photographs**, one in the acetyl wave and one in the glutathione wave. The only
thing that disambiguates is the `ingredient_N` prefix — which is precisely the part that
gets dropped when a name is read off a contact sheet and typed into chat.

This is the same failure already on record for this project as *"same shot id, three
places, all different pictures"* (see the `extend-banner-canvas.py` header comment on the
PDRN v1/v2/serum collision, which published the wrong photograph once).

### The fix, if these waves are ever re-run

Name candidates with the ingredient in them — `glut-D-cell-field-gpt_image_01`, not
`D-cell-field-gpt_image_01`. The slot id alone is only unique *within* a wave, and humans
quote it *across* waves.

---

## The map

| Ingredient | Block | Scene colour | Waves generated | Picks |
|---|---|---|---|---|
| Copper Peptide GHK-Cu | `ingredient_1` | Clinical `#014EB1` | A/B/C + D/E/F (fibroblast) | **none yet** |
| Acetyl Hexapeptide-8 | `ingredient_2` | Pearl grey `#D8D6D4` | A/B/C + D/E/F (cell) | 2 confirmed |
| Matrixyl 3000 | `ingredient_3` | Teal `#016569` | A/B/C only | **none yet** |
| PDRN | `ingredient_4` | Blush `#F3BFC2` | A/B/C + D/E/F (helix) | 1 confirmed |
| Glutathione | `ingredient_5` | Champagne `#DFC08F` | A/B/C + D/E/F (cell) | 4 confirmed |

---

## Confirmed picks — 7 of 9, unambiguous

Paths are relative to the repo root.

### PDRN — `ingredient_4`

- `assets/ai-generated/2026-08-22-multi-science-ingredient-pdrn-cell/ingredient_4--D-double-helix/ingredient_4--D-double-helix-gpt_image_01.png`

### Acetyl Hexapeptide-8 — `ingredient_2`

- `assets/ai-generated/2026-08-22-multi-science-ingredient-acetyl-hexapeptide-8-cell/ingredient_2--E-single-cell/ingredient_2--E-single-cell-flux2_01.png`
- `assets/ai-generated/2026-08-22-multi-science-ingredient-acetyl-hexapeptide-8-cell/ingredient_2--F-surface-electron/ingredient_2--F-surface-electron-gpt_image_01.png`

### Glutathione — `ingredient_5`

- `assets/ai-generated/2026-08-22-multi-science-ingredient-glutathione-cell/ingredient_5--E-single-cell-lit/ingredient_5--E-single-cell-lit-gpt_image_02.png`
- `assets/ai-generated/2026-08-22-multi-science-ingredient-glutathione-cell/ingredient_5--E-single-cell-lit/ingredient_5--E-single-cell-lit-seedream_01.png`
- `assets/ai-generated/2026-08-22-multi-science-ingredient-glutathione-cell/ingredient_5--F-radical-scatter/ingredient_5--F-radical-scatter-nbp_flash_01.png`
- `assets/ai-generated/2026-08-22-multi-science-ingredient-glutathione-cell/ingredient_5--F-radical-scatter/ingredient_5--F-radical-scatter-seedream_02.png`

Malcolm wrote these last two as `F-redical-scatter`; the slot is `F-radical-scatter`. Typo,
not a different slot — there is no `redical` slot in any wave.

---

## UNRESOLVED — 2 of 9

`D-cell-field-gpt_image_01` and `D-cell-field-gpt_image_02` were both named, and both exist
in **two** waves as different photographs:

| Candidate | Acetyl (`ingredient_2`, pearl grey) | Glutathione (`ingredient_5`, champagne) |
|---|---|---|
| `D-cell-field-gpt_image_01` | exists | exists |
| `D-cell-field-gpt_image_02` | exists | exists |

**Do not guess.** One plausible reading of the order Malcolm listed them in is that `_02`
groups with the acetyl picks and `_01` with the glutathione run — which would give each
ingredient one frame per D/E/F slot. That is an inference from list order, nothing more,
and it has not been acted on.

Both pairs are shown side by side on
`~/Desktop/skingenetix-your-picks-source-check.png`, built 2026-08-25.

---

## More than one pick per slot

Glutathione has **two** picks for `E-single-cell-lit` and **two** for `F-radical-scatter`.
Each tile takes one image, so either these are a shortlist rather than winners, or they are
intended for different blocks. Needs a decision before anything is uploaded.

---

## Not affected by any of this

The copper-peptide **page banner** (`/pages/copper-peptide-research` header) was chosen,
built and published earlier the same day from a different wave entirely —
`banner-copper-peptide-research`, slot B, nbp_pro_02. That is live and unrelated.

The copper-peptide **block f1** tile (`key_findings`) has a 55-candidate wave generated and
sheeted (`block-copper-peptide-collagen-pathways`) and is **still awaiting a pick**.
