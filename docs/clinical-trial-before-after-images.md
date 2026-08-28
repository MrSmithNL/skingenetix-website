# Clinical-Trial Before/After Images — Acetyl Hexapeptide-8 Research Page

**Status as of 2026-08-27: fifteen waves generated, ~350 candidates on disk, NOTHING CHOSEN AND NOTHING PUBLISHED.**
All three blocks still carry unrelated placeholder photographs. This document exists so a fresh session
can continue from the current brief instead of re-deriving fifteen rounds of decisions.

---

## 1. Where it lands

| | |
|---|---|
| Page | `https://www.skingenetix.com/pages/acetyl-hexapeptide-8-research` |
| Template | `templates/page.research-argireline.json` — **not** `page.research-acetyl-*`; the template still carries the Argireline trade name |
| Section | `key_findings` (type `media-with-text`, `block_order: [f1, f2, f3]`) |
| Master size | square **2048×2048** — see §7 for why square |
| Class | **B** — no reference images, no product in frame |

**Currently live in those three blocks** (all placeholders, none related to the findings):

| block | live image |
|---|---|
| `f1` | `skingenetix-ingredients-acetyl-hexapeptide-8-serum.jpg` |
| `f2` | `skingenetix-philosophy-research.jpg` |
| `f3` | `skingenetix-philosophy-quality.jpg` |

---

## 2. What each block has to support

The picture illustrates a **measured change in the appearance of expression lines**. Each block's heading
is a number, and the image sits beside it — so the image is read as evidence for that number.

| block | study | heading on the page | design |
|---|---|---|---|
| `f1` | **Wang 2013** | 48.9% Overall Anti-Wrinkle Efficacy vs Placebo | RCT, placebo-controlled, 60 subjects (3:1), 4 weeks, twice daily, **periorbital / crow's feet** |
| `f2` | **Blanes-Mira 2002** | Up to ~30% Softer-Looking Wrinkle Depth in 30 Days | in-vitro + small in-use test, healthy female volunteers, 30 days, **around the eyes** |
| `f3` | **An 2019** | 14.6% Improvement in Just 5 Days | double-blind RCT, split-face, 52 Korean female subjects, microneedle patches, 29 days, **periorbital** |

### Why this page breaks from copper-peptide and matrixyl

Those two research pages carry **mechanism explainers**, because their findings *are* mechanism —
collagen synthesis, peptide signalling. All three Acetyl Hexapeptide-8 findings are the same kind of
thing: a measured change in how expression lines look. A diptych is therefore the honest form here,
and a mechanism diagram would be inventing a story the studies did not tell.

### ⚠️ Two unresolved honesty problems

1. **Site of measurement.** All three trials measured the **periorbital** region. Forehead and
   mouth/chin waves were generated (see §4) and both show a *different site* from the one the number
   came from. If a non-periorbital frame is ever chosen, the caption must not imply the number was
   measured there.
2. **f3's cohort.** An 2019 studied **52 Korean women**. Every casting wave since 2026-08-25 has been
   Caucasian or European/American. A Caucasian face beside a Korean-cohort finding is defensible as
   illustration, not as depiction of the trial — but it has never been put to Malcolm and should be.

---

## 3. The rules the picture may not break

These are the load-bearing constraints. They were each bought with a round.

- **No line may disappear.** The number, position and count of lines is identical in both panels.
  Only their *depth* changes. A line that vanishes turns an illustration into a false claim.
- **There must be a visible improvement.** Two panels that look the same are a complete failure —
  this is the entire purpose of the pair. The floor and the ceiling are both live and deliberately narrow.
- **Nothing else about her improves.** Not younger, slimmer, prettier, better groomed, better lit,
  or **lighter-skinned**. Skin-tone change between panels is the same class of dishonesty as making
  her younger, and is explicitly negated.
- **f3's magnitude is capped.** 14.6% on *fine* wrinkles cannot support a visibly smoother forehead.
  Two f3 candidates in the brunette wave overstated it. f3's after-text now states the two deeper
  creases are **completely unchanged**, the forehead must not read smoother overall, and a viewer
  should have to compare carefully to see the difference — and should then be able to.
- **No baked-in text, ever.** No captions, percentages, labels or before/after words in the pixels.
  Langify translates page content and **cannot touch pixels**, so any burnt-in text is untranslatable
  and would strand eight locales.
- **Two sessions, not two frames.** See §4, round r3 — this is the single biggest quality jump.

---

## 4. The decision record — fifteen waves, and what each one changed

Configs are all in `configs/banners/`; assets in `assets/ai-generated/2026-08-22-multi-<wave>/`.
Nothing has been deleted; every round is still on disk.

| # | wave / config | what changed, and why |
|---|---|---|
| 1 | `block-acetyl-research-before-after` | The diptych established: two panels of exactly equal width meeting at one crisp central vertical edge, 1:1 frame. All 33 candidates found the split, so the form was never the problem. |
| 2 | `...-before-after-r2` | Malcolm: Caucasian middle-aged women only; skin must hold up in detail; the % must be **seen** but stay realistic. |
| 3 | `...-before-after-r3` | **The key round.** r1/r2 briefed identical camera, identical lighting, "nothing differs but the skin" — which is exactly why they read as *retouched pairs*. A real trial cannot pose someone identically weeks later, and a perfectly matched pair looks like one photograph edited twice. r3 asks for **two separate sessions**: different room, light direction, garment, hair fall, phone angle and gaze — everything a different day would change — while identity, moles and freckles stay fixed. |
| 4–5 | `...-forehead`, `...-forehead-r2` | Forehead site, so three blocks aren't three near-identical eye macros stacked down one page. Carries the site-of-measurement caveat (§2). |
| 6–7 | `...-mouth-chin`, `...-mouth-chin-r2` | Same reasoning, mouth corner and chin. Same caveat. |
| 8 | `...-fullface` | Different women, full face in both panels. Region split collapses — a full face shows all three sites at once, so three region waves would differ only by label. |
| 9 | `...-selfie` | **Cast ordinary women, light it like an amateur phone selfie.** The insight: a studio pair invites "who lit this and why", because nobody photographs themselves that way at home. A snapshot answers the question. Crooked framing and wrong white balance do the work that polish was fighting. |
| 10 | `...-selfie-r2` | More home-made, less attractive models. ⚠️ Ran without Gemini: both nbp models returned **429 — monthly billing cap exceeded**, not a rate limit. |
| 11 | `...-selfie-young` | Ages 30–40, and "clearly a selfie". **Undid one of my own rules**: earlier waves banned hands and arms to keep the phone out of shot, which is precisely why several read as portraits taken by someone else. The raised near arm is the strongest tell there is. |
| 12 | `...-selfie-40s` (+ r2–r5) | Age band moved up. r5 is the **structural fix** — see below. |
| 13 | `...-selfie-diverse` | Blondes, redheads, wider European/American backgrounds. **The four ethnicity bans were removed from the negative list** — a brief that negates what the casting asks for fights itself. |
| 14 | `...-selfie-neutral` | Plain interior walls, age band 45–55. Accepts honestly that at this crop only a few centimetres of wall show, so the nine "unique rooms" now live in **wall tone and light direction** rather than props. |
| 15 | `...-selfie-brunette` | Brunettes mixed in, faces closer, rooms rather than bare walls. **Causal fix:** the bare-wall wave put a phone back in frame on two slots after several clean rounds — an empty edge left nothing for the model to place there, so it supplied the object the scene implies. Giving each room **one** soft unidentifiable element fixed it. |
| 16 | `...-selfie-euro-us` | **Current best.** Casting narrowed back to Caucasian, split American/European, nine named women. f3's magnitude capped. |

### The structural fix (r5 onward) — the thing four rounds of prompt tuning could not solve

Malcolm: *"for each batch you use the same interior combination for all of the before and after images
of that run — each before and after pair should have unique background locations compared to the other
pairs in that run."*

`generate-multi.py` sends **one prompt per slot to every supplier**, so all candidates of a slot
necessarily share whatever location pair that prompt names. No wording could fix it.

**The fix: nine slots instead of three** — `f1-a/b/c`, `f2-a/b/c`, `f3-a/b/c`, each with its own
prompt, its own model and its own unique room pair, `candidates: 1`. That is why every wave from r5
onward has nine slots.

---

## 5. The current brief

**`configs/banners/block-acetyl-research-selfie-euro-us.json`** — 9 slots, 1 candidate each, class B, 2048².

The nine women: Midwest American dishwater blonde · Irish-American faded auburn, densely freckled ·
Southern American mid-brown brunette with sun weathering · Italian-American near-black brunette ·
Danish pale ash-blonde · Irish coppery red · French chestnut brunette greying at the temples ·
Polish ash-blonde with broad cheekbones · Greek almost-black brunette. *(Four brunettes, three blondes,
two red — the hair range preserved inside the narrower casting.)*

### The prompt skeleton — thirteen blocks, in this order

Every one of the nine prompts is this skeleton with the per-slot details swapped. Reuse it verbatim.

1. **The frame** — two phone selfies of the same woman weeks apart, side by side filling one square,
   two panels of exactly equal width, one crisp vertical edge precisely at centre, left = earlier.
2. **Expression** — flat and unposed both days, mouth closed, not smiling.
3. **Two occasions, not two copies** — everything identifying stays the same; everything a different
   day would change is different.
4. **Identity lock** — same face shape, jawline, nose, eye colour, skin colour, brow shape, hair colour
   and cut, moles and freckles in the same places.
5. **Two different rooms** — per-slot wall colour + light direction + *one* soft out-of-focus element.
6. **Also different between the days** — phone angle, camera height, gaze, garment, hair fall.
7. **Obviously self-taken, but no phone and no hands** — this is the view *through* the front camera,
   so the hand holding it cannot appear in its own frame.
8. **The crop** — phone held right up close, face fills the panel, cuts across the forehead below the
   hairline and at the point of the chin, cheeks run to both edges. Forehead, both eyes and whole mouth
   still in view — *the eye corners and forehead lines are the point and must not be cropped away.*
   Close-lens distortion: nose and chin read large, forehead looms.
9. **Camera tells** — not eye level, gaze slightly off the lens, a few degrees crooked and off-centre,
   imperfect focus, noise in the shadows, indoor white balance a little wrong.
10. **The woman** — per-slot nationality, hair, skin, eyes, brows. No makeup, unstyled, *"an ordinary
    person, not a model, and neither picture makes any attempt to flatter her."*
11. **Age governs the skin** — 45–55: lines well established, hold a real shadow at rest, more than at
    forty; grey at the parting normal. But no deep folds, heavy jowls or slack neck of the sixties.
12. **The honesty clause** — same number and position of lines, not one has disappeared, moles and
    freckles unchanged; only *depth* changes; not younger, slimmer, prettier, lighter-skinned.
13. **The visible-improvement floor** — someone comparing must be able to *see* which lines are softer
    and point to them. **Two panels that look the same are a complete failure.**
14. **Directional light, both days** — bright and well exposed, but daylight from one side, because
    *"flat frontal light flatters skin and hides what the picture exists to show, while light coming
    across her face rakes over the surface so every line casts its own small shadow."* Direction and
    quality differ between the days; the sidelit quality does not.
15. **Skin realism** — pores visible and varying by zone, several larger than neighbours; pigmentation
    uneven and **asymmetric, never mirrored**; vellus hairs catching the sidelight; greasy at the nose
    and forehead, drier at the outer cheeks.
16. **Then the per-panel line inventory** — left: the exact lines and counts. Right: *every one still
    there, same places, same number, none disappeared* — but each about half as deep, lighter and
    shorter shadow.

### Deeper complexions need their own lighting note

An expression line on deep brown skin reads far less by shadow and much more by how a **specular
highlight breaks along it**, and engines left unguided render dark skin grey and ashy. Those slots
state the skin stays warm and luminous with its own undertones and the sidelight picks out a sheen
along the cheekbone. Negate `no ashy grey skin, no grey cast on dark skin, no desaturated skin`.

---

## 6. Failure modes and the negatives that answer them

| failure seen | guard |
|---|---|
| Pair reads as one photo retouched twice | two-sessions structure (§4 r3); `no identical backgrounds between the panels, no same room in both panels` |
| Panels identical — no visible change | `no unchanged lines between the panels, no zero difference between the panels` |
| A line vanishes | `no line disappearing between the panels` |
| She gets younger / lighter / made-up in the after panel | `no younger woman in the right panel, no change of skin colour between the panels, no lighter skin in the right panel, no makeup appearing in the right panel` |
| Flat light hides the lines | `no flat frontal lighting, no shadowless face` |
| Reads as a portrait someone else took | camera tells in §5 step 9 |
| Phone or hand creeps in | `no hand, no fingers, no arm, no elbow, no phone, no mirror, no reflection` + give the room **one** legitimate edge element |
| Invented captions / percentages | `no text, no lettering of any kind, no numbers, no percentages, no captions, no labels` — and **exclude nbp_pro** |
| Beauty-filter skin | `no beauty-filter smoothing, no frequency separation, no airbrushed skin, no plastic skin, no uniform skin texture` |
| Wrong age | `no elderly woman, no heavy jowls, no sagging neck, no woman over fifty-five, no woman under forty` |

---

## 7. Supplier notes specific to this brief family

- **nbp_pro — EXCLUDED on evidence.** Seven waves of invented captions burnt into the image.
- **Luma — refuses this brief family with HTTP 422.** Do not count on it.
- **Gemini billing:** on 2026-08-26 both nbp models returned **429 "monthly spending cap exceeded"** —
  that is a *billing* failure, not the 250/day rate limit, and it reads identically in the logs.
  The key is the **sister brand's**, so Hairgenetix spends the same allowance.
- Working set in practice: **seedream, gpt_image, nbp_flash** (+ flux2, which returns 1 per call).
- **Square 2048²**, because `media-with-text` takes its row height from the master's own aspect and a
  non-square master makes this block taller than its siblings.

---

## 8. How to continue — exact commands

```bash
cd "/Users/malcolmsmith/Claude Code/Projects/skingenetix-website"
set -a; source ~/.claude/config/image-credentials.env; set +a          # `set -a` is mandatory
python3 -c "import os; print({k: bool(os.environ.get(k)) for k in ('FAL_KEY','OPENAI_API_KEY','GEMINI_API_KEY')})"

# re-run the current best brief
python3 scripts/generate-multi.py configs/banners/block-acetyl-research-selfie-euro-us.json

# or a new round: copy that config, bump the wave name and the slot-id prefix, edit, then run
python3 scripts/banner-contact-sheet.py assets/ai-generated/2026-08-22-multi-block-acetyl-research-selfie-euro-us
```

Then Malcolm marks winners in place with `_` (shortlist) / `__` (final), and:

```bash
python3 scripts/finals/prepare-marked-run-output.py <run-dir> assets/publish-ready/acetyl-research-findings --apply
python3 scripts/upload-theme-images.py configs/banners/<plan>.json
python3 scripts/patch-template.py configs/banners/<plan>.json --template templates/page.research-argireline.json --dry-run
```

**Slot letters restart every wave** — `f1-a` names a different photograph in each wave. Always glob
before acting on a filename.

---

## 9. Outstanding

1. **Malcolm has not picked anything from any of the fifteen waves.** The `euro-us` wave (9 candidates)
   and the `brunette`, `neutral`, `diverse` and `r5` waves all have contact sheets built and shown.
2. **Put the f3 cohort question to him** (§2) — Caucasian face beside a Korean-cohort finding.
3. **Decide the site question** (§2) — if any forehead or mouth/chin frame is chosen, the caption must
   not imply the number was measured there.
4. A publish plan (`configs/banners/*-publish.json`) has never been written for these three blocks.

---

---

## 10. Reusing this on a page that measures TONE, not line depth — the glutathione build

`/pages/glutathione-research` needed the same form for blocks **f1** (Watanabe 2014, 2% GSSG,
10 weeks) and **f3** (Khanna 2025 systematic review). Built 2026-08-27 from this document. Config
builder: `scripts/build-glutathione-before-after-config.py`; briefs
`configs/banners/block-glutathione-research-before-after-{r1,r2}.json`.

**Most of the skeleton transfers unchanged** — two sessions not two frames, one prompt per slot,
the identity lock, the visible-improvement floor, no hand or phone, no baked-in text. **Three
things must be inverted, and they are not optional:**

| §5 step | On a wrinkle page | On a tone page |
|---|---|---|
| 14 — lighting | **Raking sidelight**, so every line casts its own shadow | **Soft, broad, frontal daylight.** A shadow gradient across a cheek is indistinguishable from a patch of pigment — raking light manufactures the fault in the left panel |
| 9 — camera tells | "Indoor white balance a little wrong" | **Dropped.** A warm half and a cool half is a tone difference the product did not cause. Buy amateur-ness with framing, focus and noise instead — and brief colour as a **match between the halves**, not a property of each |
| 12 — honesty clause | `no lighter skin in the right panel` | Contradicts a trial whose endpoint *is* melanin index. Re-cut: the **patches converge toward her own surrounding tone**; the skin between them, under the jaw and on the neck is identical. Negate only whitening, bleaching, chalky/grey and changed ethnicity |

**Position beat wording.** r1 carried the freckle rule explicitly, in paragraph 17, and gpt_image,
nbp_flash and seedream all cleared the discrete marks anyway — the engine's own prior (brightening
= removing spots) got there first. Moving the identical rule to **paragraph 3** fixed it on every
engine in r2. Split the marks: **diffuse mottling is the subject and evens out; discrete moles,
freckles and sun spots are identity anchors and may not disappear.**

**Yield, 8 slots × 5 suppliers:** gpt_image **8/8**, nbp_flash **7/8**, seedream 4/8, luma 4/8,
**flux2 0/8**. Roughly 22 of 40 clean.

### Failure modes this page adds to §6

| failure seen | guard |
|---|---|
| "A dull greyish cast" painted as a discrete slate patch that reads as a **bruise** (luma, seedream, 3 slots) | Never give a colour word for the whole cast. Say *warmer, muddier, less clear than the skin beside it* |
| Before panel reads as **clinical disease** — confluent lentigines, raised yellow lesions (seedream) | Cap the left panel explicitly: everyday uneven tone, nothing a dermatologist would treat |
| A **cheek macro** pulled back to a half-face portrait by all five engines, on both slots that asked | An extreme crop cannot be briefed on a face. Ask for half-face, crop tighter in post |
| Phone and hand in frame (nbp_flash, 1 slot) | Unchanged from §6 — the room element helps but does not eliminate it |
| flux2: different, older woman; desaturation; zero difference; **a fabricated stock-photo watermark** | Exclude flux2 from this brief family, as nbp_pro already is |

### Two honesty questions for Malcolm, not yet put to him

1. **Watanabe 2014 was split-face** — one face, treated side against placebo side. These diptychs
   read as week 0 against week 10, which is how the paper reports each side against its own
   baseline and is the form the section labels support. It illustrates the trial; it does not
   depict it.
2. **f3 illustrates a systematic review, not a trial.** A before/after is a weaker fit for a pooled
   conclusion than for a single study. Its magnitude is capped accordingly, but the alternative is a
   non-photographic block there.

---

---

## 11. Reusing this for the copper-peptide round — 3 shot types x 4 concerns x 8 women

Malcolm, 2026-08-27: a new batch for the copper-peptide clinical research, in three shot
types across four concerns, eight amateur women each — **96 diptychs**. Builder:
`scripts/build-copper-peptide-before-after-configs.py`, which emits twelve configs
`configs/banners/block-copper-peptide-ba-<concern>-<shot>.json`, eight slots each.

Age band moves to **40–60** (was 45–55) and the negative list is corrected to match. Every
earlier config in this family carried `no woman over fifty-five`; left alone it would have
fought the casting on more than a third of the slots.

### The structural change, and the cause it fixes

> *"the position, pose, distance from camera and head position were too similar — so it
> looked like the image was a duplicate."*

**This was never a wording fault.** §5 step 8 of the acetyl skeleton pins the framing
identically in both panels — "the phone is held right up close and her face completely fills
the panel, the frame cuts across her forehead just below the hairline and at the point of
her chin" — and that paragraph is applied to the earlier day *and* the later day. Room, wall
colour, light direction, garment and hair were all briefed to vary; head size and head
position in frame, which are what most say *same photograph*, were held constant. The
glutathione r2 builder added a head-and-gaze paragraph but hedged it — "the difference is
small, she is recognisably in the same kind of pose both times" — which is the hedge that
had to go.

Camera height, camera tilt, degree of head turn, distance and position-in-frame are now
stated **separately per panel** (paragraph 6 of every prompt). Verified on three engines:
all three produced two genuinely different photographs.

### ⚠️ But the side of the face must be locked, or the pair proves nothing

The first version of the viewpoint table turned her head *opposite* ways on eight of twelve
pairs. Malcolm caught it:

> *"it should always be showing the same part of the face — if showing the front then the
> front, if showing the left side then the left side in the before and after. Not before:
> left side and After: right side."*

Left cheek and right cheek are **different areas of skin**, with different lines, different
moles and different pigmentation. There is nothing to compare, and it is the same class of
fault as the panels being two different women. The table now carries a `side` per pair — four
front, four her-left-cheek, four her-right-cheek — the *direction* of turn is constant within
a pair and only its *degree* changes, and paragraph 6b states the rule outright.

**The camera moves; the side it looks at does not.**

### The distance guard (paragraph 7)

If the later panel is further away or softer, the lines look shallower *because of the
camera* and the pair stops being evidence. Do **not** fix this by always putting the after
closer — across ~100 images "the after is the close one" becomes its own tell. Distance
varies in both directions, bounded so the region of interest stays equally resolved in both
panels, and the prompt says outright that the change may not be explainable by distance,
softness or blur.

### Gaze

Subtly different on all, **noticeably different on 30%** (30 of 96, indexed globally so the
proportion holds across the round rather than rounding inside each batch of eight). Gaze is
the free axis: it can move anywhere while the head stays locked to one side.

### The four concerns, and the one that inverts

`fine-lines`, `firming` and `repair` take **raking sidelight**. `brightening` takes **soft
broad frontal light** and matched colour between the halves, per §10 — which partially
overrides Malcolm's "different lighting for each before and after": on that batch the light
*direction* still differs between days, colour temperature and exposure may not. Flagged to
him 2026-08-27.

`firming` also **substitutes its macro shot**: firmness is contour, a cheek macro has no
contour in it, so that cell uses a very close **jaw-and-neck** crop instead. Named in the
config note rather than quietly swapped.

### Shot types cannot be briefed — see §10, now confirmed on three more engines

seedream, gpt_image and nbp_flash **all three** returned head-and-shoulders portraits for the
skin-only macro, and again for the "part of the face" vertical slice, which came back framed
almost like the whole-face wave. With the five engines of §10 that is eight engine-runs
across two brief families. **Generate at the framing the engines give, and crop the winners
to their shot type in post.** Note that once the two panels sit at different distances and
angles, one uniform crop box will not land on the same region in both — each panel needs its
own. `scripts/face-landmarks.swift` is in the repo for that.

### The bad-photograph style — waves 13–18, added 2026-08-28

Malcolm: *"a batch that is noticeably bad quality photo (not the detail — but clearly a home
made selfie photo with bad lighting) ... Quality of the realism should stay as real as
possible."* Then: *"do all of them for wrinkle reduction and for skin firming"* — so all
three shot types on `fine-lines` and `firming`, six waves, 48 diptychs.

Built as a `style` axis on the same builder (`style="amateur"`), not a second script.

**The central distinction, and it needs its own paragraph in every prompt: THE PHOTOGRAPH IS
BAD, THE IMAGE IS NOT.** An engine told to make a bad photo degrades the *render* — soft
mush, smeared features, obvious artefacts — which destroys the only thing these pictures
exist to show. The brief separates them explicitly: the light was wrong, the framing was
careless and the phone struggled, but the image is sharp, high-resolution and faithful, with
real pores and real vellus hair. Verified on the smoke test: both gpt_image and nbp_flash
produced convincingly awful snapshots with the skin detail fully intact.

**⚠️ Bad light can fabricate the entire result, and it is a worse risk than the distance
confound.** If the earlier panel gets harsh light and the later panel gets kind light, the
improvement is the lamp — and it would be nearly invisible as a fault, because bad lighting
is *supposed* to differ between the two days. Both panels are therefore badly lit **to the
same degree**, the later is never the more flattering, and the skin must stay readable in
both in spite of it. `no flattering light in the right panel, no soft kind light in the right
panel, no better lit right panel` are negated. **Check this specifically when judging** — on
the gpt_image smoke test the later panel came back warmer and lower in contrast, which is
borderline.

**The negative list had to be rebuilt.** The standard `NEGATIVE_GLOBAL` bans `no dark room,
no dim room, no murky lighting, no underexposed picture, no camera flash, no orange tungsten
glow, no heavy shadow across the face, no bathroom, no fluorescent strip light` — every one
of which forbids exactly what this batch is for. `NEGATIVE_GLOBAL_AMATEUR` bans the
*degradation* words instead (`no low resolution, no smeared face, no illustration, no cgi,
no melted features`). Left unchanged those nine stale negatives would have fought the brief
on all 48 slots.

**Hands and arms come back.** Acetyl wave 11 found that banning arms is why several waves
read as portraits taken by someone else — "the raised near arm is the strongest tell there
is". It is required here on the `close` and `half` shots. **But not on `macro`:** at that
crop skin fills the panel, so demanding a raised shoulder in the corner asks for two
incompatible things at once, and a self-contradicting brief is how the cheek macro became a
portrait on eight engine-runs. The phone and mirrors stay banned everywhere — a mirror puts
the phone back in shot.

**Not run on `brightening`, and that is deliberate**, not an omission: a tone pair needs the
two halves matched for colour and brightness (§10), and this style's whole point is wrong
light differing between the days. The two briefs contradict each other.

Gaze is **noticeably different on all eight** slots here rather than the round's 30%, and the
per-day variation is pushed further — different room *type*, different time of day, hair up
one day and loose the other, a different *kind* of garment rather than a different colour.
`AMATEUR_SCENES` carries sixteen bad-light setups (overhead ceiling light, warm bedside lamp,
backlit window, strip light, uplighting desk lamp, screen light, and so on).

### Suppliers and cost

seedream, gpt_image, nbp_flash — 96 slots x 3 = 288 images, **≈$8.60**. nbp_pro excluded
(seven waves of invented captions), flux2 excluded (0/8 on the glutathione before/after
family, fabricates a stock-photo watermark), luma answers this family with HTTP 422.

⚠️ **Run with `--candidates 1`.** `generate-multi.py` reads `args.candidates` and **never**
reads `defaults.candidates` from the config, so the config's own `"candidates": 1` is
decorative. The flag defaults to 2 and would silently double the round to ≈$17.20.

⚠️ **nbp_flash returns 4096² unasked** where 2048 was requested. Harmless, and useful if a
macro crop is the target.

### Observed on the smoke tests

| engine | side-lock | moles preserved | makeup | age |
|---|---|---|---|---|
| gpt_image | ✅ | ✅ | none added | held |
| nbp_flash | ✅ | ✅ one-for-one, cheek/jaw/neck | none added | held |
| seedream | ✅ | ❌ several cheek moles gone | ❌ mascara appeared in the after panel | ❌ read younger |

Seedream broke four guards at once on the first sample. Kept in the round on Malcolm's call
(2026-08-27) — rule 1 is that every image goes to every supplier and he chooses, and one
sample is not evidence enough to drop an engine. **Check its candidates against the honesty
table before shortlisting any of them.**

---

*Related: `.claude/rules/website-imagery.md` (every image to every supplier; judge at 100% and at render
size), `docs/visual-identity/03-art-direction-and-briefs.md`, and the project memory entries
`before-after-pairs-need-two-sessions-not-two-frames`, `slot-letters-restart-per-wave`,
`label-text-must-be-quoted`, `a-tone-pair-inverts-the-lighting-rule-of-a-wrinkle-pair`.*
