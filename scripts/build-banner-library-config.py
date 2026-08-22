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
    ("A-recline-prod-left",
     "lying with her head tipped back, seen in profile from the side and slightly above, "
     "eyes closed, skin filling the frame edge to edge from the décolleté at the lower right "
     "up the long sweep of the throat to the jaw and lips at the upper left",
     "left third of the frame, between 0 and 33 percent of frame width",
     "right half of the frame, which stays smooth and even in tone",
     "eyes open"),
    ("B-recline-prod-right",
     "lying with her head tipped back, seen in profile from the side and slightly above, "
     "eyes closed, skin filling the frame edge to edge from the décolleté at the lower left "
     "up the long sweep of the throat to the jaw and lips at the upper right",
     "right third of the frame, between 67 and 100 percent of frame width",
     "left half of the frame, which stays smooth and even in tone",
     "eyes open"),
    ("C-recline-prod-centre",
     "lying with her head tipped fully back and turned away, eyes closed, photographed from "
     "almost directly above so the throat and décolleté read as an abstract landscape filling "
     "the whole frame, the chin at the upper right",
     "centre of the frame but low, in the bottom third of the frame height",
     "upper third of the frame, which stays smooth and even in tone",
     "eyes open, product high in the frame"),
    ("D-face-eyes-to-camera",
     "in close-up with her head resting on one side, looking directly into the lens with a "
     "level composed gaze, her face filling the right half of the frame - brow, eyes, "
     "cheekbone and lips all sharp - and the line of her neck running away to the left",
     "right third of the frame, between 67 and 100 percent of frame width",
     "left half of the frame, which stays smooth and even in tone",
     "eyes closed, looking away"),
    ("E-face-eyes-closed",
     "in close-up with her head resting on one side and her eyes closed, lashes catching the "
     "light, her face filling the left half of the frame and the line of her neck running away "
     "to the right",
     "left third of the frame, between 0 and 33 percent of frame width",
     "right half of the frame, which stays smooth and even in tone",
     "eyes open"),
    ("F-eye-macro",
     "in extreme macro on one eye and brow, the lashes, the fine skin of the lid and the "
     "texture of the brow filling the right two thirds of the frame, the eye open and looking "
     "slightly away from the lens, everything beyond falling into soft shadow",
     "far left edge of the frame, within the first 20 percent of frame width, small and softly "
     "out of focus",
     "centre and right of the frame beyond the eye, which stays smooth and even in tone",
     "both eyes, full face, eye closed"),
    ("G-decollete-above",
     "lying down photographed from directly above so her décolleté and the base of her throat "
     "read as an abstract landscape running horizontally across the whole frame, her chin "
     "entering at the top right, eyes outside the frame",
     "left third of the frame, between 0 and 33 percent of frame width",
     "centre and right of the frame, which stays smooth and even in tone",
     "face in frame, eyes in frame"),
    ("H-over-shoulder",
     "lying on her front with her head turned back over her shoulder toward the camera, eyes "
     "meeting the lens, the line of her shoulder running across the lower frame and her face "
     "at the upper left",
     "right third of the frame, between 67 and 100 percent of frame width, standing large and "
     "close to camera and slightly soft",
     "centre and left of the frame, which stays smooth and even in tone",
     "eyes closed, looking away"),
]

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
            f"sculptural, quiet and premium."
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
            "negative_extra": f"{neg}, product in the clear zone, product over the headline area",
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
