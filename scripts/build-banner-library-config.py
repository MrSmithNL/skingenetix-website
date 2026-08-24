#!/usr/bin/env python3
"""Emit a skin-art banner wave for one product, from that product's own spec.

    python3 scripts/build-banner-library-config.py copper-peptide-repair-serum
    python3 scripts/build-banner-library-config.py --all

Malcolm wants a library of skin-art banners rather than one philosophy image:
one run per product, varied body pose, the product placed left / centre / right
so text can go wherever the frame leaves room, and some close-ups of the face
and eyes. Nine products x eight briefs is not something to hand-write.

Two things this encodes that were learned the hard way tonight:

* PRODUCT POSITION IS A MEASURED FRACTION, never a body part. The smoke test put
  the bottle "against the side of her jaw" and negated "bottle in the centre of
  the frame" - but the jaw IS near centre in a reclining crop, so the brief
  fought itself and four of five suppliers put the bottle over the headline.
  Each brief now names the third of the frame the product occupies, and the
  clear zone opposite it.

* CLASS A MEANS REFERENCES, ALWAYS. A product in frame means the reference-lock
  protocol applies. Label lines are quoted verbatim from the product's own
  config; everything below the headline lines is thrown out of the depth of
  field rather than asked to be small, which is the fix that worked on the
  carton stacks. FLUX.2 is barred outright, and Luma is flagged - on the smoke
  test it invented an 'XXX' mark before the wordmark, the same failure that got
  FLUX.2 barred in the first place.

Author: Claude Code, 2026-08-22.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIGS = ROOT / "configs"
PUBLISH = ROOT / "assets" / "publish-ready"

#: Folder name in assets/publish-ready differs from the config stem for some products.
FOLDERS = {
    "copper-peptide-repair-serum": "copper-peptide-repair-serum",
    "copper-peptide-day-repair-cream": "copper-peptide-day-repair-cream",
    "copper-peptide-night-repair-cream": "copper-peptide-night-repair-cream",
    "matrixyl-3000-pro-collagen-serum": "matrixyl-3000-pro-collagen-serum",
    "matrixyl-3000-pro-collagen-cream": "matrixyl-3000-pro-collagen-cream",
    "pdrn-skin-repair-serum": "pdrn-skin-repair-serum",
    "pdrn-collagen-repair-cream": "pdrn-collagen-repair-cream",
    "glutathione-brightening-serum": "glutathione-brightening-serum",
    "acetyl-hexapeptide-8-serum": "acetyl-hexapeptide-8-serum",
}

#: (id, pose, product third, clear zone, extra negatives)
#: Product position is varied across the set so the library covers banners whose
#: text sits left, right or centre. The clear zone is always opposite the product.
POSES = [
    ("A-face-full-prod-left",
     "lying with her head resting back and turned toward the camera, her WHOLE FACE fully in "
     "view and unobscured - brow, both eyes, nose, lips, cheekbones and jaw all inside the "
     "frame and sharp - her eyes closed and her expression calm, the line of her neck and "
     "décolleté running away to the right, skin filling the frame edge to edge",
     "left third of the frame, between 0 and 33 percent of frame width, held below her chin "
     "and clear of her face",
     "right half of the frame, which stays smooth and even in tone",
     "face cropped, chin only, partial face, top of head cut off, eyes open"),
    ("B-face-full-prod-right",
     "lying with her head resting back and turned toward the camera, her WHOLE FACE fully in "
     "view and unobscured - brow, both eyes, nose, lips, cheekbones and jaw all inside the "
     "frame and sharp - her eyes closed and her expression calm, the line of her neck and "
     "décolleté running away to the left, skin filling the frame edge to edge",
     "right third of the frame, between 67 and 100 percent of frame width, held below her chin "
     "and clear of her face",
     "left half of the frame, which stays smooth and even in tone",
     "face cropped, chin only, partial face, top of head cut off, eyes open"),
    ("C-face-full-eyes-open-left",
     "lying with her head resting on one side, looking directly into the lens with a level "
     "composed gaze, her WHOLE FACE fully in view and unobscured - brow, both eyes, nose, lips, "
     "cheekbones and jaw all inside the frame and sharp - the line of her neck and décolleté "
     "running away to the right, skin filling the frame edge to edge",
     "left third of the frame, between 0 and 33 percent of frame width, held clear of her face",
     "right half of the frame, which stays smooth and even in tone",
     "face cropped, partial face, top of head cut off, eyes closed, looking away"),
    ("D-face-full-eyes-open-right",
     "lying with her head resting on one side, looking directly into the lens with a level "
     "composed gaze, her WHOLE FACE fully in view and unobscured - brow, both eyes, nose, lips, "
     "cheekbones and jaw all inside the frame and sharp - the line of her neck and décolleté "
     "running away to the left, skin filling the frame edge to edge",
     "right third of the frame, between 67 and 100 percent of frame width, held clear of her face",
     "left half of the frame, which stays smooth and even in tone",
     "face cropped, partial face, top of head cut off, eyes closed, looking away"),
    ("E-face-full-gaze-away",
     "lying with her head resting back and tilted, her WHOLE FACE fully in view and unobscured "
     "- brow, both eyes, nose, lips, cheekbones and jaw all inside the frame and sharp - her "
     "eyes open and looking softly away from the lens, the line of her neck and décolleté "
     "running away to the right, skin filling the frame edge to edge",
     "left third of the frame, between 0 and 33 percent of frame width, held clear of her face",
     "right half of the frame, which stays smooth and even in tone",
     "face cropped, partial face, top of head cut off, eyes closed, direct eye contact"),
    ("F-face-full-above-centre",
     "lying down photographed from directly above, her WHOLE FACE fully in view and unobscured "
     "- brow, both eyes, nose, lips, cheekbones and jaw all inside the frame and sharp - her "
     "eyes closed, her hair spread away from her face, the neck and décolleté running down out "
     "of frame, skin filling the frame edge to edge",
     "centre of the frame but low, in the bottom third of the frame height, clear of her face",
     "upper third of the frame, which stays smooth and even in tone",
     "face cropped, partial face, top of head cut off, eyes open, horizontal banding, flat "
     "stripe across the frame"),
    ("G-face-full-over-shoulder",
     "lying on her front with her head turned back over her shoulder toward the camera, her "
     "WHOLE FACE fully in view and unobscured - brow, both eyes, nose, lips, cheekbones and jaw "
     "all inside the frame and sharp - eyes meeting the lens, the line of her shoulder running "
     "across the lower frame, skin filling the frame edge to edge",
     "right third of the frame, between 67 and 100 percent of frame width, standing close to "
     "camera and clear of her face",
     "centre and left of the frame, which stays smooth and even in tone",
     "face cropped, partial face, back of the head, top of head cut off, eyes closed"),
    # Malcolm: nbp_pro_01 was "the only one showing some of the body" and he wants
    # more like it. The earlier poses all crop at the neck, so these two name the
    # shoulder and upper body as being in frame rather than leaving it to chance.
    ("I-body-and-face-left",
     "lying back with her head and her upper body both in frame, her WHOLE FACE fully in view "
     "and unobscured - brow, both eyes, nose, lips, cheekbones and jaw all inside the frame and "
     "sharp - eyes closed, and the line of her shoulder, collar and décolleté clearly visible "
     "sweeping away below and to the right, so the picture holds the body as well as the face, "
     "skin filling the frame edge to edge",
     "left third of the frame, between 0 and 33 percent of frame width, held clear of her face",
     "right half of the frame above the shoulder line, which stays smooth and even in tone",
     "face cropped, partial face, top of head cut off, head only, tight head crop, eyes open"),
    ("J-body-and-face-right",
     "lying back with her head and her upper body both in frame, her WHOLE FACE fully in view "
     "and unobscured - brow, both eyes, nose, lips, cheekbones and jaw all inside the frame and "
     "sharp - eyes open and looking softly away, and the line of her shoulder, collar and "
     "décolleté clearly visible sweeping away below and to the left, so the picture holds the "
     "body as well as the face, skin filling the frame edge to edge",
     "right third of the frame, between 67 and 100 percent of frame width, held clear of her face",
     "left half of the frame above the shoulder line, which stays smooth and even in tone",
     "face cropped, partial face, top of head cut off, head only, tight head crop, eyes closed"),
    # And a much tighter face crop than any pose so far.
    ("K-face-macro-close",
     "in very tight macro on her face alone, the face filling almost the entire frame from edge "
     "to edge - the skin texture of the cheek, the lashes, the lips and the fine down on the "
     "jaw all rendered in extreme detail - her eyes closed and her expression calm, no neck or "
     "shoulder in frame at all",
     "far right edge of the frame, within the last 20 percent of frame width, only partly in "
     "frame and softly out of focus",
     "left portion of the cheek and jaw, which stays smooth and even in tone",
     "wide shot, neck in frame, shoulder in frame, whole head small in frame, eyes open"),
    ("H-eye-macro",
     "in extreme macro on one eye and brow, the lashes, the fine skin of the lid and the "
     "texture of the brow filling the right two thirds of the frame, the eye open and looking "
     "slightly away from the lens, everything beyond falling into soft shadow",
     "far left edge of the frame, within the first 20 percent of frame width, small and softly "
     "out of focus",
     "centre and right of the frame beyond the eye, which stays smooth and even in tone",
     "both eyes, full face, eye closed"),
]

#: Every serum is a CLEAR liquid in tinted or frosted glass. Not one of the five
#: product_desc files says so - they describe the glass colour and stop - so with
#: nothing stated about the contents each supplier fills the bottle with whatever it
#: assumes, and that assumption is milky white. It showed worst on Glutathione and
#: Matrixyl because their glass is pale; Copper Peptide and PDRN hid it behind a
#: strong tint. Stated here once for all serums rather than patched per product.
SERUM_NOTE = (
    "The glass colour described above is the colour of the GLASS ITSELF, not of the "
    "contents. Inside, the serum is a CLEAR, COLOURLESS, WATER-TRANSPARENT liquid - "
    "light passes straight through it, the pipette stem is visible through the bottle, "
    "and the fluid in the pipette is clear. The contents are never milky, creamy, "
    "opaque, white, pearlescent or yellow, and the bottle is never solid or painted."
)

SERUMS = {
    "copper-peptide-repair-serum",
    "pdrn-skin-repair-serum",
    "glutathione-brightening-serum",
    "matrixyl-3000-pro-collagen-serum",
    "acetyl-hexapeptide-8-serum",
}

#: The creams are genuinely opaque, so they get no such note - a jar of cream that
#: reads transparent would be just as wrong in the other direction.
SERUM_NEG = (
    ", milky liquid, creamy contents, white contents, opaque contents, pearlescent liquid, "
    "yellow liquid, solid white bottle, painted plastic bottle, lotion inside the bottle"
)

NEG_GLOBAL = (
    "invented brand name, different brand, altered label, extra text on the product, mangled "
    "lettering, gibberish text, two products, packaging box, watermark, signature, border, "
    "collage, multi-panel, botanicals, jewellery, glitter, plastic retouched skin, waxy skin, "
    "airbrushed, second person, tattoo, six fingers, extra fingers, fused fingers, malformed "
    "hand, upright seated pose, standing, vertical composition, bright background, "
    "white background"
)


def product_lines(desc: str) -> str:
    """Pull the quoted label lines out of a product_desc, verbatim."""
    quoted = re.findall(r"'([^']{2,60})'", desc)
    seen, out = set(), []
    for q in quoted:
        # The wordmark is named separately in the prompt, so excluding it here
        # stops the brief reading "the wordmark 'Skingenetix', then 'Skingenetix'".
        # Volume/ingredient lines carrying a pipe are the fine print, which is
        # deliberately thrown out of focus rather than set as legible type.
        if q.lower() == "skingenetix" or "|" in q:
            continue
        if q.isupper() and q not in seen:
            seen.add(q)
            out.append(q)
    return ", then ".join(f"'{q}'" for q in out[:3])


def first_ref(folder: str) -> list[str]:
    d = PUBLISH / folder
    if not d.exists():
        return []
    pref = sorted(p for p in d.glob("__*hero*.jpg"))
    pref += sorted(p for p in d.glob("__*macro_label*.jpg"))
    pref += sorted(p for p in d.glob("__*.jpg"))
    out, seen = [], set()
    for p in pref:
        if p.name not in seen:
            seen.add(p.name)
            out.append(str(p.relative_to(ROOT)))
        if len(out) == 2:
            break
    return out


def build(stem: str) -> dict:
    cfg = json.loads((CONFIGS / f"{stem}.json").read_text())
    desc = cfg["product_desc"]
    folder = FOLDERS[stem]
    refs = first_ref(folder)
    if not refs:
        sys.exit(f"{stem}: no reference packshots in assets/publish-ready/{folder}")
    # First sentence of the product spec carries the physical description.
    physical = desc.split(". ")[0].strip()
    if stem in SERUMS:
        # rstrip the period: the template continues ", exactly as in the reference images"
        physical = f"{physical}. {SERUM_NOTE}".rstrip(".")
    lines = product_lines(desc)

    slots = []
    for sid, pose, third, clear, neg in POSES:
        prompt = (
            f"Extreme close-up fine-art beauty photograph of one woman around thirty five years "
            f"old {pose}. One hand with five slender relaxed fingers holds the product, which sits "
            f"in the {third}, sharp and with its label turned square to camera. The product is "
            f"{physical}, exactly as in the reference images. Legible type on it reads only: the "
            f"Skingenetix DNA-helix mark with the wordmark 'Skingenetix', then {lines}. Every "
            f"remaining line falls outside the depth of field, visibly soft and blurred beyond any "
            f"possibility of being read. Print no word that is not quoted here. The background "
            f"beyond her is a deep graphite grey, colour #1A1A1A, dark and even. One directional "
            f"light from above models the form so the lit ridges glow and the hollows fall into "
            f"shadow. Skin real and finely textured with visible pores and fine down, unretouched. "
            f"The {clear}, carrying no hard edge, bright highlight or feature, so a headline can "
            f"sit there. Very shallow depth of field, fine film grain, cinematic wide format, "
            f"sculptural, quiet and premium. Her whole face stays inside the frame with clear space "
            f"above her head, and the product never overlaps or obscures her face."
        )
        slots.append({
            "id": f"{stem}--{sid}",
            "title": f"{stem} — {sid}",
            "class": "A",
            "width": 3072,
            "height": 1280,
            "target_slot": "banner library",
            "ref_files": refs,
            "prompt": prompt,
            "negative_extra": (f"{neg}, product in the clear zone, product over the headline area"
                               + (SERUM_NEG if stem in SERUMS else "")),
        })
    return {
        "wave": f"banner-library-{stem}",
        "created": "2026-08-22",
        "doc": ".claude/rules/website-imagery.md",
        "note": (
            f"Skin-art banner library for {stem}. Eight poses, the product placed left, centre or "
            f"right so the set covers banners whose text sits on any side, plus face and eye "
            f"close-ups. Class A throughout: references attached, label lines quoted verbatim from "
            f"configs/{stem}.json, everything below them thrown out of the depth of field. FLUX.2 "
            f"barred (invents brands); Luma invented an 'XXX' mark on the smoke test and should be "
            f"read with that in mind. Product position is stated as a measured fraction of frame "
            f"width because the smoke test proved a body-part anchor does not hold - 'against the "
            f"jaw' put the bottle over the headline in four of five suppliers."
        ),
        "defaults": {"candidates": 2, "negative_global": NEG_GLOBAL},
        "slots": slots,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("product", nargs="?")
    ap.add_argument("--all", action="store_true")
    args = ap.parse_args()
    stems = list(FOLDERS) if args.all else [args.product]
    for stem in stems:
        if stem not in FOLDERS:
            sys.exit(f"unknown product: {stem}\nknown: {', '.join(FOLDERS)}")
        cfg = build(stem)
        out = CONFIGS / "banners" / f"library-{stem}.json"
        out.write_text(json.dumps(cfg, indent=2))
        print(f"{out.relative_to(ROOT)}  ({len(cfg['slots'])} slots, refs: "
              f"{len(cfg['slots'][0]['ref_files'])})")


if __name__ == "__main__":
    main()
