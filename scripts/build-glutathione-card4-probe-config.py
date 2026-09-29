#!/usr/bin/env python3
"""Build the single-image wave for glutathione findings card f4: a skin probe resting on a cheek.

    python3 scripts/build-glutathione-card4-probe-config.py
    → configs/banners/glutathione-card4-measurement-probe-r1.json

    python3 -u scripts/generate-multi.py configs/banners/glutathione-card4-measurement-probe-r1.json \
        --candidates 1 --only <slot-id>[,<slot-id>]
    python3 scripts/wave-contact-sheet.py glutathione-card4-measurement-probe-r1 \
        --stable-labels configs/banners/glutathione-card4-measurement-probe-r1.json --expect 5 --tile 400

⚠️ `--candidates 1` IS NOT OPTIONAL: generate-multi.py never reads `defaults.candidates` and its flag
defaults to 2, which silently doubles the spend.

WHAT THE CARD SAYS (docs/claims/glutathione.md §8.6, f4 "Smoother, Better-Moisturised Skin, Measured by
Instrument"): in the Watanabe 2014 trial, skin-surface image analysis at the crow's feet recorded smoother
texture on the glutathione side from week 6, and a Corneometer probe on the cheek recorded higher skin
moisture at weeks 8 and 9. These are INSTRUMENT results, so the picture is the instrument, not a before/after.
Malcolm, 2026-09-29, choosing between options for card 4: "Skin-measurement probe" (the approval for the
spend, all suppliers).

THE BRIEF'S RULES, AND WHERE EACH COMES FROM
  1. THE DEVICE IS DESCRIBED, NEVER NAMED (describe-the-thing-dont-name-it): no brand or model name is in
     anything an engine reads (asserted: Corneometer, Courage, Khazaka and friends). A named instrument drags
     in its brand's housing, its logo and its read-out.
  2. NO TEXT, NO LOGO, NO NUMBERS, NO SCREEN ON THE DEVICE. Said positively in the prompt (the object is one
     plain, unmarked colour all over - Luma receives no negatives at all), and by name only in the negatives.
     FLUX.2 is known to print graduation digits on lab glassware whatever the negatives say
     (website-imagery rule 4): check its candidates at full size.
  3. NO PRODUCT ON SCREEN. The card reports the trial's lotion, not our serum (template §6.3), so no bottle,
     dropper, jar or cosmetic. Stated positively as "nothing else is in the picture"; the objects are named
     only in the negatives (asserted: none of them in a positive).
  4. NO MOLES, WARTS, SKIN TAGS OR BEAUTY MARKS (Malcolm's standing rule, memory
     no-moles-and-varied-clothes-in-model-images). The positive text says what her skin DOES carry - pores,
     fine vellus hairs, faint lines - and the marks are named only in the negatives (asserted via the
     glutathione builder's MARK_WORDS).
  5. THE PROBE IS TOUCHING HER. "Resting on" can be drawn hovering; the brief gives a checkable physical cue
     instead: the flat end sits flush on the skin and the skin gives a fraction around its rim.
  6. REAL, HYDRATED SKIN, NOT AIRBRUSHED. Smooth and supple at a glance, pores and fine texture at 100%.
  7. NO CAPTION BAIT AND NO DIGITS in anything an engine reads (the round-3 skeleton's CAPTION_BAIT words
     became burnt-in captions on nbp_pro), and no window named (named windows get drawn).
  8. SQUARE 2048 MASTER. Engines pull a tight crop back to a portrait
     (engines-return-a-portrait-whatever-crop-you-ask-for): crop the winner in post.
  9. CLOTHES VARY PER SLOT, nothing printed on them; a garment is stated because the nbp engines pull back to
     head-and-shoulders and leave shoulders bare when none is.

THE THREE SLOTS vary the woman, the angle (three-quarter, side profile, slightly from below) and the hand
(pale-blue nitrile glove, bare hand, violet nitrile glove), and the probe's colour (white / light grey).

SMOKE LOG: SMOKE_LOG below (slot a on all six suppliers first; two brief faults found and fixed for b-c).

FULL WAVE, 2026-09-29: 18 of 18, no refusal or failure (slot a on the smoke brief, b-c on the revised one).
Run folder assets/ai-generated/2026-08-22-multi-glutathione-card4-measurement-probe-r1 (manifest-smoke-a.json,
manifest.json). Sheet: ~/Desktop/skingenetix-glutathione-card4-probe-r1.png, rows A-C = slots a-c (stable
labels), columns 1-6 = flux2, gpt_image, luma, nbp_flash, nbp_pro, seedream.
  HELD ON ALL 18: no text, logo, digits, screen or buttons on any device (checked at full resolution); no
  bottle, dropper, jar or cosmetic anywhere; one hand only, the technician otherwise out of frame.
  STILL OPEN AFTER THE FIXES: a flange head wider than the body on flux2 (A1, B1), nbp_pro (B5, C5) and seedream
  (B6) - fix 2 did not hold on those three engines; nbp_flash B4 drew the measuring face towards the camera, so
  it is not flush on the skin, and gpt_image B2 rests on its rim; flux2 C1 drew the probe oversized, over the
  side of the nose; seedream C6 put it on the temple (the crow's-feet site, not the cheekbone); pigment spots
  or patches on seedream (A6, B6, C6), luma (all three: orange and mottled, B3 and C3 also read fifty-plus) and
  flux2 A1 - fix 1 held on gpt_image, nbp_flash and nbp_pro only; luma bordered C3; flux2 B1 has her eyes open
  and one pale, polished-looking nail. Cleanest on every rule: gpt_image A2 and C2, nbp_flash A4 and C4,
  nbp_pro A5.
Author: Claude Code, 2026-09-29. Candidates only; nothing is uploaded or published by this file.
"""
import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


#: The glutathione before/after builder: its Prettier render, its MARK_WORDS guard and (as .r3) the
#: under-eye skeleton's caption-bait list, size and Luma cap. Importing it runs its own module asserts only.
glut = _load("glut", "scripts/build-glutathione-cards-before-after-config.py")
skel = glut.r3

WAVE = "glutathione-card4-measurement-probe-r1"
OUT = ROOT / "configs" / "banners" / f"{WAVE}.json"
PAGE = "/pages/glutathione-research"
TEMPLATE = "templates/page.glutathione-research.json"
HEADING = "Smoother, Better-Moisturised Skin, Measured by Instrument"
ID_PREFIX = "gluc4--"
SMOKE_SLOTS = {"a"}
SMOKE_BRIEF = "assets/ai-generated/2026-08-22-multi-glutathione-card4-measurement-probe-r1/smoke-brief-a.json"
SMOKE_LOG = """
SMOKE LOG, 2026-09-29 (slot a; 6 of 6 returned; gpt_image resolved to gpt-image-2.5-sunburst). Judged at render
size (500 px), at 1100 px whole-frame and at the centre half at full resolution. Slot a is NOT re-run; its brief
is at SMOKE_BRIEF (manifest-smoke-a.json beside it).
  HELD ON ALL SIX: a plain white cylinder with a darker grey head, NO text, logo, digits, screen or buttons on
  any device (flux2 included); no bottle, dropper, jar or cosmetic anywhere; the head resting on the skin, not
  hovering; one gloved hand from the right-hand edge, the rest of the technician out of frame; light-olive
  Mediterranean women, late thirties to mid-forties; the grey T-shirt; a plain pale background; no mole, wart
  or skin tag. Every engine pulled back to a head-and-neck portrait (the known trait: crop in post), and most
  put the head on the mid-cheek in front of the ear rather than just under the eye - which is where Watanabe's
  Corneometer measured, so it is left alone.
  TWO BRIEF FAULTS, FIXED FOR SLOTS b-c:
    1. FLECKS AND PIGMENT SPOTS on flux2 (freckles across nose and cheeks), seedream (brown patches on the
       cheek) and luma (an orange, mottled cheek). The skin paragraph said "clear and even" but never that the
       colour is unbroken; it now carries round 2's fix (glutathione builder SKIN_R2: each pore the same colour
       as the skin around it, nothing darker between them) and "her true, natural skin colour under neutral
       daylight" (Luma sees no negatives). Negatives add dark flecks, pigment patches, orange skin.
    2. THE HEAD WAS NOT A FLAT END: luma drew a rounded dome and flux2 a grey flange twice the body's width.
       "Flat, round and blunt, the same width as the body" was named, not measured; it is now "exactly as wide
       as the body and perfectly flat, its round face meeting the side of the cylinder in a crisp, square edge
       all round" (measure-geometry-dont-describe-it), with dome / flange in the negatives.
  NOT BRIEF FAULTS (recorded): seedream, gpt_image and luma drew the probe about two fingers thick (a real
  moisture probe is about that thick, so it reads true); flux2 gave her heavy lashes; luma's cast is its known
  warm drift.
"""

# --------------------------------------------------------------------------------------
# The three slots.
# --------------------------------------------------------------------------------------
SLOTS = [
    dict(key="a", label="three-quarter, gloved hand from the right",
         who=("a SPANISH woman of about thirty-eight, with dark brown hair pulled smoothly back off her face "
              "into a low knot, light-olive skin with a warm golden undertone, brown eyes and natural dark brows"),
         eyes="Her eyes are open, looking calmly ahead past the camera.",
         garment="a soft heather-grey crew-neck T-shirt",
         probe="smooth matte WHITE",
         hand=("A hand in a plain PALE-BLUE nitrile examination glove comes into the picture from the right-hand "
               "edge and holds the probe lightly between thumb and fingers."),
         view=("THE VIEW: a three-quarter view of the side of her face, at the level of her eyes. Her face is "
               "turned about forty degrees away from the camera, towards the left-hand edge of the picture, so "
               "her near cheek, cheekbone and the outer corner of her near eye face the camera.")),
    dict(key="b", label="side profile, bare hand from below",
         who=("a CROATIAN woman of about forty-four, with very dark brown hair with a few grey strands, tied "
              "back smoothly behind her ear, light-olive skin with a warm undertone, dark brown eyes and thick "
              "natural brows"),
         eyes="Her eyes are softly closed, her face completely relaxed.",
         garment="a dark-teal knitted jumper",
         probe="smooth matte LIGHT GREY",
         hand=("A bare hand with short, clean, unpolished nails comes into the picture from the lower edge and "
               "holds the probe lightly between thumb and fingers."),
         view=("THE VIEW: her face in side profile, seen square from the side at the level of her cheekbone. "
               "Her nose points to the right-hand edge of the picture, so her near cheek, her cheekbone, the "
               "outer corner of her near eye and the line of her jaw run across the picture, with her ear at "
               "the left.")),
    dict(key="c", label="slightly from below, gloved hand from above",
         who=("a PORTUGUESE woman of about thirty-four, with wavy dark-brown hair gathered back loosely at the "
              "nape of her neck, light-olive skin with a warm golden undertone, hazel eyes and soft natural "
              "brows"),
         eyes="Her eyes are open, her gaze lowered calmly, not towards the camera.",
         garment="a plain navy top with a round neck",
         probe="smooth matte WHITE",
         hand=("A hand in a plain VIOLET nitrile examination glove comes into the picture from the upper "
               "right and holds the probe lightly between thumb and fingers."),
         view=("THE VIEW: the camera is a little below her face, looking slightly up along her cheek towards "
               "the cheekbone, in a three-quarter view. Her face is turned towards the right-hand edge of the "
               "picture, and the line of her jaw is nearest the camera, with her cheekbone and the outer "
               "corner of her near eye above it.")),
]


def build_prompt(s: dict) -> str:
    """One brief for every supplier, Luma included: every constraint that matters is stated positively,
    because Luma receives no negatives. Kept under the Luma cap (asserted)."""
    return (
        "A close, calm, documentary photograph of a real dermatology research study in progress: a small "
        "handheld skin probe resting on a woman's cheekbone. It is one square photograph that fills the whole "
        "frame, right out to all four edges.\n\n"

        "THERE IS NO WRITING ANYWHERE IN THE PICTURE. No words, no letters, no numbers, no symbols, no "
        "captions and no labels, on anything in it or across it, and no strips, bars or boxes. It is just the "
        "photograph.\n\n"

        f"THE PROBE: a small, plain cylinder in {s['probe']} plastic, about as thick as a finger and about five "
        "times as long as it is thick. One end is its measuring head: EXACTLY AS WIDE AS THE BODY AND PERFECTLY "
        "FLAT, its round face of slightly darker grey meeting the side of the cylinder in a crisp, square edge "
        "all round. A thin, plain grey cable leaves the other end and "
        "runs out of the picture. THE WHOLE DEVICE IS PLAIN AND UNMARKED: one smooth, even colour all over, "
        "with nothing on its surface at all - no buttons, no lights, no markings of any kind. It is a simple, "
        "quiet piece of laboratory equipment, not a beauty gadget, and nothing sharp or pointed is anywhere on "
        "it.\n\n"

        f"THE MOMENT: {s['hand']} Its flat round head rests FLUSH AGAINST THE SKIN OF HER CHEEKBONE, just "
        "below and outside the corner of her near eye, square to the skin and pressing so gently that the "
        "skin gives only a fraction around its rim. It is touching her, flat on her cheek - not hovering above "
        "it and not tilted onto its edge. Only the hand and wrist come into the picture; the rest of whoever "
        "holds the probe is outside it.\n\n"

        + s["view"] + " THE PICTURE IS CLOSE: it runs from the outer corner of her eye and her temple at the "
        "top down to her cheek and the line of her jaw at the bottom. The probe's head and the skin around it "
        "are the sharpest part of the picture and sit near its centre.\n\n"

        f"THE WOMAN: {s['who']}. {s['eyes']} Her expression is calm and neutral: mouth closed and relaxed, "
        "not smiling. She is an ordinary study volunteer, not a model, and she wears no makeup at all. If any "
        f"of her clothing shows at the bottom edge, it is {s['garment']}, plain, with nothing on it.\n\n"

        "HER SKIN: it looks naturally smooth, supple and well hydrated, and it is REAL, UNRETOUCHED SKIN. At "
        "full size, fine pores are visible across her cheek, fine vellus hairs catch the light along the "
        "cheekbone, and the faint lines of her age sit at the corner of her eye. Her skin colour is clear and "
        "even, with nothing on it but pores, fine hairs and those faint lines. THE COLOUR IS UNBROKEN ACROSS "
        "HER CHEEKS, HER NOSE AND HER FOREHEAD: each pore is a tiny pit the same colour as the skin around it, "
        "and nothing darker sits on the skin between them. It is her true, natural skin colour under neutral "
        "daylight. A soft natural sheen, not glossy, not airbrushed, not waxy.\n\n"

        "THE LIGHT AND THE BACKGROUND: soft, bright, even daylight from the front and a little above, with "
        "gentle shadows only. Behind her, a plain, pale grey-white background, softly out of focus, with "
        "nothing on it. Clean, cool-neutral colour; calm, clinical and real, like a photograph taken for the "
        "study itself rather than for an advertisement.\n\n"

        "NOTHING ELSE IS IN THE PICTURE: only her face and hair, the probe and its cable, the one hand holding "
        "it, and the plain background."
    )


NEGATIVE_GLOBAL = (
    # Text on or around the device, and the read-out an instrument implies.
    "no text, no lettering of any kind, no words, no letters, no numbers, no digits, no percentages, no "
    "captions, no labels, no caption bar, no title, no watermark, no stock photo watermark, no logo, no brand "
    "name, no brand mark, no engraving, no sticker on the device, no printing on the device, no screen, no "
    "display, no digital read-out, no monitor, no computer, no laptop, no tablet, no phone, no buttons on the "
    "device, no indicator light, no LED, no glowing tip, no blue light, no measurement scale, no ruler, no "
    "grid overlay, no arrows, no callout lines, "
    # Product and cosmetics (the card is about the trial's lotion, not our serum).
    "no bottle, no jar, no dropper, no pipette, no serum, no cream, no lotion, no tube, no cosmetic product, "
    "no packaging, no cotton pad, no makeup, no foundation, no mascara, no eyeliner, no lipstick, "
    # What a handheld cylinder at the face gets mistaken for.
    "no pen, no marker, no pencil, no lipstick tube, no thermometer, no microphone, no microneedling pen, no "
    "needle, no needle tip, no syringe, no injection, no derma roller, no jade roller, no gua sha, no massage "
    "tool, no beauty device, no LED mask, no laser, no electrodes, no wires stuck to the face, no pointed tip, "
    "no domed tip, no rounded end, no flange, no rim wider than the probe, "
    # Skin marks (Malcolm's rule) and filtered skin.
    "no mole, no moles, no wart, no warts, no skin tag, no beauty mark, no beauty spot, no raised spot, no "
    "freckles, no dark flecks, no dark spots, no pigment patches, no orange skin, no blemishes, no acne, "
    "no redness, no rash, no wound, no bruise, no airbrushed "
    "skin, no plastic skin, no waxy skin, no porcelain skin, no poreless skin, no beauty-filter smoothing, no "
    "glossy skin, no oily shine, no dewy glass skin, "
    # People and hands.
    "no second face, no technician's face, no person in the background, no full body, no extra fingers, no "
    "malformed hand, no two hands on the probe, no hand touching her face other than with the probe, no "
    "jewellery, no earrings, no rings, no spectacles, no headband, no hair clip, no smile, no grimace, "
    "no pain, no teenager, no elderly woman, no very pale skin, no pink-toned fair skin, "
    # Setting and style.
    "no clinic room, no hospital bed, no desk, no shelves, no window, no door, no plant, no clutter, no busy "
    "background, no patterned background, no studio glamour, no beauty advertisement, no fashion photograph, "
    "no dramatic lighting, no hard shadows, no coloured light, no neon, no vignette, no border, no picture "
    "frame, no split screen, no collage, no multiple panels, no printed graphic on "
    "clothing, no bare shoulders"
)

BRAND_WORDS = re.compile(r"corneometer|courage|khazaka|visioscan|visiometer|tewameter|cutometer|"
                         r"skin-?visiometer|\bbrand\b|\blogo\b", re.I)
PRODUCT_WORDS = re.compile(r"\bbottle|\bdropper|\bserum\b|\bjar\b|\bcream\b|\blotion\b|\bpipette|"
                           r"\bpackag", re.I)


def config() -> dict:
    slots = []
    for s in SLOTS:
        prompt = build_prompt(s)
        k = s["key"]
        assert len(prompt) < skel.LUMA_CAP, f"{k}: prompt {len(prompt)} chars is over the Luma cap"
        assert not any(ch.isdigit() for ch in prompt), f"{k}: digit in prompt"
        # (negatives too: gpt_image and the Gemini engines read them as an "Avoid:" line)
        bait = skel.caption_bait(prompt + NEGATIVE_GLOBAL)
        assert not bait, f"{k}: caption bait {bait}"
        assert "window" not in prompt.lower(), f"{k}: 'window' in prompt"
        m = BRAND_WORDS.search(prompt)
        assert not m, f"{k}: a brand or logo word in a positive: {m.group(0)!r}"
        m = PRODUCT_WORDS.search(prompt)
        assert not m, f"{k}: a product word in a positive: {m.group(0)!r}"
        m = glut.MARK_WORDS.search(prompt)
        assert not m, f"{k}: a mark is named in a positive: {m.group(0)!r}"
        assert "light-olive" in s["who"] and "FLUSH AGAINST THE SKIN" in prompt, k
        # smoke fixes (SMOKE_LOG)
        assert "COLOUR IS UNBROKEN" in prompt and "crisp, square edge" in prompt, k
        slots.append({
            "id": f"{ID_PREFIX}probe-{k}",
            "title": (f"f4 skin probe · watanabe-2014 · {s['label']} — "
                      f"{re.sub(r'^an? ', '', s['who'].split(',')[0])}"),
            "class": "B", "width": skel.SIZE, "height": skel.SIZE,
            "target_slot": f"{PAGE} key_findings f4 ({HEADING})",
            "generated_from": (f"smoke brief - {SMOKE_BRIEF} (not re-run)" if k in SMOKE_SLOTS else "r1"),
            "garment": s["garment"],
            "ref_files": [], "prompt": prompt,
            "negative_extra": "",
        })
    for neg in ("no text", "no logo", "no numbers", "no screen", "no bottle", "no dropper", "no mole", "no wart",
                "no skin tag", "no beauty mark"):
        assert neg in NEGATIVE_GLOBAL, neg
    ids = [s["id"] for s in slots]
    assert not any(a != c and c.startswith(a) for a in ids for c in ids), "a slot id prefixes another"
    return {
        "wave": WAVE, "created": "2026-09-29", "round": "r1",
        "doc": ("docs/claims/glutathione.md §8.1 (Watanabe 2014, Figure 3) and §8.6 (card f4), "
                ".claude/rules/website-imagery.md; built by scripts/build-glutathione-card4-probe-config.py"),
        "note": ("GLUTATHIONE SCIENCE PAGE, FINDINGS CARD f4 (Watanabe 2014 instrument results: skin-surface "
                 "image analysis at the crow's feet, smoother from week 6; a Corneometer probe on the cheek, "
                 "higher moisture at weeks 8 and 9). ONE photograph, not a before/after: a small, plain, "
                 "unmarked handheld skin probe resting flush on a woman's cheekbone, held by a technician's "
                 "hand. MALCOLM, 2026-09-29: 'Skin-measurement probe'. No text, logo, brand, screen or numbers "
                 "on the device; no product, bottle, dropper or cosmetic; no moles, warts, skin tags or beauty "
                 "marks; real, hydrated, unretouched skin. Caucasian, light-olive skin, early thirties to "
                 "mid-forties. Square 2048 master. CANDIDATES ONLY; Malcolm picks. Smoke test: slot a on all "
                 "six suppliers first."),
        "target_templates": [TEMPLATE],
        "defaults": {"candidates": 1, "negative_global": NEGATIVE_GLOBAL, "negative_class_b": ""},
        "slots": slots,
    }


def main() -> None:
    cfg = config()
    text, _ = glut.render(cfg, OUT)
    OUT.write_text(text)
    print(f"wrote {OUT.relative_to(ROOT)} — {len(cfg['slots'])} slots")
    for s in cfg["slots"]:
        print(f"  {s['id']:<16} prompt {len(s['prompt']):>5}   {s['title']}")


if __name__ == "__main__":
    main()
