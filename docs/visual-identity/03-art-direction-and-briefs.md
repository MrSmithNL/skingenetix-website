# Skingenetix Art Direction & Generator Briefs

**Date:** 2026-08-21 · Derived from [`01-benchmark-research.md`](01-benchmark-research.md) and
[`02-inventory-and-gaps.md`](02-inventory-and-gaps.md).

---

## 1. The direction — "Clinical Luminism"

One line: **a single subject, lit hard, on a colour the brand owns, with half the frame left
quiet for type — and not one leaf.**

It is the Bader/Sturm end of the panel rather than the La Mer/Tatcha end, because Skingenetix
sells named molecules and has no heritage story to tell. The brand's credibility is
*the molecule and the evidence*, so the imagery has to look like it came from somewhere
rigorous.

### 1.1 Palette

Taken from the live theme where one already exists, extended where it does not.

| Role | Name | Hex | Where it comes from |
|---|---|---|---|
| Primary ground | Graphite | `#1A1A1A` | Already the theme's primary button + hero background |
| Light ground | Bone | `#F0F0F0` | Already the theme page background |
| Accent | Copper | `#D9967E` → `#B87333` | Theme's existing secondary button, deepened. Ties to GHK-Cu, the flagship active |
| Clinical blue | Clinical | `#014EB1` | Existing Copper Peptide scene colour |
| Teal | Matrixyl | `#016569` | Existing Matrixyl scene colour |
| Champagne | Glutathione | `#DFC08F` | Existing Glutathione scene colour |
| Blush | PDRN | `#F3BFC2` | Existing PDRN scene colour |
| Pearl grey | Acetyl | `#D8D6D4` | Existing Acetyl scene colour |

Scene colours are the ones already agreed for product photography (see the
`product-colours-2026-08` memory and the per-product files in `configs/`). Reusing them means
the banners and the product shots belong to the same world instead of two parallel systems.

### 1.2 The concern-to-colour system

The four homepage concern tiles currently look interchangeable. Binding each to its lead
ingredient's existing scene colour makes the grid legible at a glance and links concern →
molecule → product:

| Concern tile | Lead ingredient | Ground colour |
|---|---|---|
| Fine Lines & Wrinkles | Acetyl Hexapeptide-8 | Pearl grey `#D8D6D4` |
| Firming & Skin Density | Matrixyl 3000 | Teal `#016569` |
| Skin Repair & Renewal | Copper Peptide GHK-Cu | Clinical blue `#014EB1` |
| Brightening & Glow | Glutathione | Champagne `#DFC08F` |

### 1.3 The five rules, as production constraints

1. **One subject per frame.** Never more than one bottle, one hand, one form.
2. **Reserved type zone.** 40% of the frame — left or right third, never centre — held at low
   detail and even tone so a headline sits on it unaided. Specified per brief as a measured
   fraction, not as "leave space for text".
3. **Committed ground.** Every frame names one ground colour from §1.1.
4. **Hard key light, single soft fill.** Clinical, directional, with a real shadow. Not the
   flat diffuse "spa" light currently on the site.
5. **No botanicals.** Named as an explicit negative on every brief. No leaves, sprigs, flowers,
   citrus, fruit, herbs, wood, stone, linen, or water droplets on foliage.

---

## 2. Two classes of brief — and why the distinction is load-bearing

This is the part that decides whether the run succeeds, and it comes from a failure already
recorded on this project.

### Class A — Reference-locked (the product is in frame)

The real bottle must appear. The brief ships with **reference images** from
`assets/publish-ready/<product>/`, and quotes the label text **verbatim, line by line, with its
colour**, per the `label-text-must-be-quoted` rule.

Route to **Seedream 5 Lite** (`fal-ai/bytedance/seedream/v5/lite/edit`) or **Luma uni-1**.
**FLUX.2 is barred** from every Class A brief — it substitutes invented brand identities that
look clean and are wrong.

### Class B — Reference-free (material, light, place — no product)

Texture, liquid, skin, laboratory, metal, abstract structure. These get **no references**, and
therefore must be given **no product description and no brand identity at all**.

> A shot that receives no references must not be asked for identity — only for material.

The failure this prevents is on record: on 2026-08-19 five text-to-image shots were handed the
product description without references and all thirty candidates invented a branded bottle with
a mangled helix and stray ® marks — on briefs that never mentioned a bottle. Every Class B brief
below therefore carries the explicit negative **"no bottle, no jar, no label, no logo, no
lettering, no packaging, no text of any kind"**.

Class B may route to FLUX.2, since there is no branding in frame to invent.

### Practical consequence for this set

Of the 9 Wave-1 items, **1 is Class A** (hero slide 1) and **8 are Class B**. Keeping the
product out of most banners is not a compromise — it is what the panel does. Bader's founder
band, Tatcha's institute photograph and Bader's black quote band contain no product at all.

---

## 3. Global negatives (applied to every brief)

```
no botanicals, no leaves, no sprigs, no flowers, no citrus, no fruit, no herbs,
no wood, no rough stone, no linen or textile props, no scattered pebbles,
no water splashes, no bokeh sparkle overlays, no lens flare,
no text, no watermark, no signature, no border, no collage, no multi-panel layout,
not a flat-lay, no clutter, no more than one subject
```

Class B briefs add:

```
no bottle, no jar, no dropper bottle, no tube, no packaging,
no label, no logo, no brand mark, no lettering of any kind
```

Kept deliberately short. Long negative lists trip Luma's content policy because it has no
negative-prompt field and the list has to be folded into the prompt body (`luma-constraints`
memory, 6000-char cap).

---

## 4. Output specifications

Measured from the live DOM at 1440px, then doubled for retina.

| Slot type | Rendered | Ratio | Generate at |
|---|---|---|---|
| Homepage hero slide | 1440 × 640 | **2.25 : 1** | 3072 × 1365 |
| Concern / find-a-serum tile | 250 × 250 | **1 : 1** | 2048 × 2048 |
| Science split media | 389 × 407 | **0.95 : 1** | 2048 × 2160 |
| Page-break band (new) | full-bleed | **2.4 : 1** | 3072 × 1280 |
| Mega-menu tile | 220 × 220 | **1 : 1** | 2048 × 2048 |

Seedream reaches 3072 natively and 4096 at the same price; every other backend caps at 2048 or
1024. Wide banners therefore route to Seedream by default.

---

## 5. Wave 1 briefs — the nine that change the brand most

### A1 · Homepage hero, slide 1 — "The Molecule" · **Class A** · 3072 × 1365

- **Subject:** one Copper Peptide Advanced Repair Serum bottle, standing, right third of frame.
- **Reference:** `assets/publish-ready/copper-peptide-repair-serum/` hero white-bg frame.
- **Ground:** Graphite `#1A1A1A`, seamless, falling off to near-black at the left edge.
- **Light:** single hard key from upper right at roughly 40°, throwing a long defined shadow
  left across the ground; one soft fill at 20% from the left to keep the blue glass readable.
- **Type zone:** left 40% of frame held at even near-black, no detail, no shadow crossing it.
- **Accent:** a narrow copper `#B87333` specular running down the right edge of the bottle only.
- **Label:** quote verbatim from the reference — do not paraphrase, do not invent a strapline.

### A2 · Homepage hero, slide 2 — "Peptide Chain" · **Class B** · 3072 × 1365

- **Subject:** macro of a single viscous, water-clear serum thread lifting from a pool, caught
  mid-draw so it forms one continuous strand across the right two-thirds.
- **Ground:** Graphite `#1A1A1A` wet-look surface with a mirror reflection.
- **Light:** hard raking light from the right; the strand refracts a thin clinical-blue
  `#014EB1` core with a copper `#B87333` rim highlight.
- **Type zone:** left 40%, unbroken black, the strand must not enter it.
- **Negatives:** global + Class B set.

### A3 · Homepage hero, slide 3 — "Skin, Close" · **Class B** · 3072 × 1365

- **Subject:** one macro passage of adult skin across a cheekbone, filling the right two-thirds
  — real texture, visible pores, fine down, no retouching to plastic.
- **Ground:** the skin itself; background falls to graphite at the frame edge.
- **Light:** hard low key from the right at a shallow angle so the texture reads as relief.
- **Type zone:** left 40% falls into shadow, even and near-black.
- **Care:** one adult, 35–55, no full face — the frame stops below the eye. No model release
  issues, no identifiable person.
- **Negatives:** global + Class B set + *no full face, no eyes, no makeup, no glitter.*

### E1 · Page-break band — "The Peptide Standard" · **Class B** · 3072 × 1280

The band that does Bader's job: the brand speaking once at full width.

- **Subject:** a single upright cylinder of solid copper, machined and lightly brushed,
  standing centre-right on a graphite ground — read as a laboratory reference standard, not
  as a product.
- **Ground:** Graphite `#1A1A1A`, seamless, deep falloff.
- **Light:** one hard key from the upper left; the copper carries a long specular and casts a
  single hard shadow to the right.
- **Type zone:** left 45%, unbroken.
- **Why copper:** GHK-Cu is the flagship. A copper object on black states the proposition
  without a bottle in frame.

### E2 · Page-break band — "Evidence" · **Class B** · 3072 × 1280

Tatcha's institute photograph, done honestly.

- **Subject:** one pair of gloved hands at a laboratory bench, mid-task with a pipette over a
  microplate. Hands and forearms only — the frame stops at the elbow, no face, no person
  identifiable, no name badge.
- **Ground:** a real bench — brushed stainless, matte black instrument housings behind, thrown
  well out of focus.
- **Light:** cool practical light from above and slightly behind, hard enough to edge the glove.
- **Type zone:** right 40%, the defocused background carrying it.
- **Honesty constraint:** this must not imply a facility Skingenetix owns. Caption it in the
  theme as a stock/illustrative image, or as the contract laboratory if that is accurate.
  **Do not caption it "our laboratory" unless that is true.**
- **Negatives:** global + Class B set + *no faces, no logos on equipment, no readable screens,
  no branded consumables.*

### D1–D4 · Concern tiles ×4 · **Class B** · 2048 × 2048

One shared construction, four grounds. Each is a **single form** — no props, no arrangements.

| Tile | Ground | Subject |
|---|---|---|
| **D1 Fine Lines & Wrinkles** | Pearl grey `#D8D6D4` | One smooth ribbon of water-clear gel folding over itself, centre frame, hard key from the left |
| **D2 Firming & Skin Density** | Teal `#016569` | One dense white cream peak drawn up to a single stiff point, hard key from the right |
| **D3 Skin Repair & Renewal** | Clinical blue `#014EB1` | One perfect blue serum droplet resting on a polished surface with its own reflection |
| **D4 Brightening & Glow** | Champagne `#DFC08F` | One shallow pool of clear liquid catching a single hard highlight, gold refraction beneath |

- **Common:** subject fills the central 60%; ground reads clean at 250 px; no gradient
  vignettes; the substance colours follow the agreed product-colour table, not invention.
- **Negatives:** global + Class B set.

---

## 6. Waves 2–4 (briefed, queued behind Malcolm's marks on Wave 1)

| Wave | Items | Class | Approach |
|---|---|---|---|
| **2 — Missing & borrowed** | C1 contact, C2 FAQ, C3 shipping-returns, B5 skin-concerns, B9 PDRN research, B10 glutathione research | B | Narrow 3:1 bands. Utility pages get quiet graphite material studies; the two research pages get their molecule's scene colour |
| **3 — Navigation** | A3–A8 mega-menu ×6, D5–D8 find-a-serum ×4 | B + A | Menu tiles are 1:1 crops on scene colour; find-a-serum mirrors the D1–D4 system |
| **4 — Page hero refresh** | B1–B4, B6–B8, B11–B15 | B | One material study per page on its ingredient's ground, replacing the three overworked `philosophy-*` files |

Wave 1 runs first because its nine images sit on the homepage, where they set the brand for
every visitor, and because approving its look approves the system for the other 28.

---

## 7. Cost estimate

Seedream 5 Lite at $0.035, four candidates per slot:

| Wave | Slots | Candidates | Cost |
|---|---|---|---|
| 1 | 9 | 36 | ~$1.30 |
| 2 | 6 | 24 | ~$0.85 |
| 3 | 10 | 40 | ~$1.40 |
| 4 | 12 | 48 | ~$1.70 |
| **Total** | **37** | **148** | **~$5.25** |

Two orders of magnitude below the ~$95 product-photography run, because banners need no
reference-lock fan-out across six engines — only Wave 1's single Class A slot does.
