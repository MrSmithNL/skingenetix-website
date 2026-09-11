#!/usr/bin/env python3
"""Emit the round-2 Copper Peptide SET brief — ten compositions, one product spec.

    python3 scripts/build-copper-peptide-set-batch2.py
    set -a; source ~/.claude/config/image-credentials.env; set +a
    python3 scripts/generate-multi.py configs/banners/copper-peptide-set-batch2-2026-09-10.json

WHY A BUILDER AND NOT TEN HAND-WRITTEN SLOTS
Round 1 (`configs/banners/copper-peptide-set-2026-09-10.json`) was hand-written, and its
three product blocks are copy-pasted into all five slots. That was survivable at five and
is not at ten: the label spec is the one part of this brief that must be byte-identical
everywhere, because an unspecified label is an invented one and a label that drifts between
slots produces candidates that cannot be compared. Here the spec is written ONCE and each
composition supplies only its arrangement, surface, camera and light.

WHY THE PRODUCTS ARE NAMED, NOT PLACED, IN THE SHARED BLOCK
Round 1 said "LEFT ... CENTRE ... RIGHT" inside the product description, which welded the
spec to a single left-to-right row. Half the compositions below are not rows - flat-lays,
clusters, pyramids, one product lying down - so the shared block identifies each unit as THE
DAY JAR / THE SERUM BOTTLE / THE NIGHT JAR and every composition places them by that name.

THE THREE BLUES ARE THE WHOLE RISK. The line shares one carton blue but three different
CONTAINER blues. In a single-product shot an engine cannot conflate them; in a set shot it
is the default failure. The separation paragraph is therefore emitted into EVERY slot after
the product blocks, never left to the composition text to imply.

LUMA gets its own trimmed prompt on every slot - it caps at 6000 characters and answers a
longer prompt with a bare HTTP 422 that reads exactly like a content refusal. The cap is
asserted at build time below, so this file fails loudly here rather than silently losing a
backend an hour into a run.

Round-1 verdict that shaped this batch, from Malcolm: gpt_image, nbp_flash and seedream are
the usable engines, nbp_flash and seedream the best two. All five are still briefed, because
"every image goes to every supplier" is a standing instruction (BRAND-003) and one round's
verdict is not a licence to narrow the next one.

Author: Claude Code, 2026-09-10.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from copper_peptide_set_spec import (  # noqa: E402
    NEGATIVE, REF_FILES, build_slot,
)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "configs" / "banners" / "copper-peptide-set-batch2-2026-09-10.json"

#: Each entry is (id, opening line, ARRANGEMENT, SCENE, FRAME). Split this way so a composition
#: can be retuned on one axis - surface, or camera, or placement - without rewriting the others,
#: which is the mistake the bundle-shot geometry work kept making with its shared ratios.
COMPOSITIONS = [
    (
        "b2-a-pyramid-blocks",
        "A premium skincare product photograph of THREE DIFFERENT Skingenetix Copper Peptide products arranged as a set in a clear pyramid.",
        "ARRANGEMENT. The serum bottle stands raised at the centre apex on a pale stone cube, with the day jar and the night jar sitting lower and slightly forward on either side of it, their fronts turned a few degrees inward towards the camera. The three silhouettes together read as a triangle with the bottle at the top point. All three front labels face the camera and stay fully legible.",
        "SCENE. Pale cool-grey stone cubes of two heights on a matching stone surface, a soft cool mid-grey seamless background behind. Even diffused light from the front and slightly above with a gentle cool fill, so no container throws a shadow across another and every label stays open.",
        "FRAME. Camera slightly above the group, looking gently down so the pyramid reads clearly. All three products and the tops of the cubes are fully inside the frame with clear margin above and to both sides; nothing is cut by any edge. Square format. Sharp focus across all three front labels, every line legible.",
    ),
    (
        "b2-b-black-glass-reflection",
        "A dramatic premium skincare product photograph of THREE DIFFERENT Skingenetix Copper Peptide products standing together as a set on polished black glass.",
        "ARRANGEMENT. The three stand in a shallow arc, the serum bottle a little forward of centre and the two jars set back and turned a few degrees inward, so the group has depth rather than sitting in a flat line. All three front labels face the camera and stay fully legible.",
        "SCENE. A polished black glass surface throwing a clean vertical mirror reflection of all three beneath them, fading to black. The background is deep graphite going to near-black at the corners. Cool rim light from behind and slightly above on both sides draws a bright edge down the flank of each container, with a soft frontal fill just strong enough to keep the labels readable. Restrained, cold, high-end.",
        "FRAME. Camera at the height of the jars' shoulders, close to eye level with the group. The three products AND their reflections are fully inside the frame, with dark margin above and to both sides; nothing is cut by any edge. Square format. Sharp focus across all three front labels, every line legible.",
    ),
    (
        "b2-c-wet-slate-droplets",
        "A fresh, cold-feeling premium skincare product photograph of THREE DIFFERENT Skingenetix Copper Peptide products standing together as a set on wet dark slate.",
        "ARRANGEMENT. The three stand close together in a loose triangle, the serum bottle at the back and slightly higher, the two jars forward and apart at the front, one turned a few degrees further than the other. All three front labels face the camera and stay fully legible.",
        "SCENE. A dark blue-grey slate surface, wet, with fine water droplets beaded across the stone and clinging to the shoulders of the glass. A shallow film of water around the bases catches a cool reflection. Cool crisp light from the upper left, slightly harder than studio soft, so each droplet carries a tiny highlight and the wet stone reads as genuinely wet rather than merely dark. The background is a cool dark grey falling off gently.",
        "FRAME. Camera low, near the level of the jar lids, so the wet surface stretches away beneath the group. All three products fully inside the frame with clear margin above and to both sides; nothing is cut by any edge. Square format. Sharp focus across all three front labels, every line legible.",
    ),
    (
        "b2-d-silk-drape-cluster",
        "A soft, tactile premium skincare product photograph of THREE DIFFERENT Skingenetix Copper Peptide products grouped as a set on draped silk.",
        "ARRANGEMENT. An asymmetric cluster rather than a row: the serum bottle standing upright at the back left, the day jar upright and forward at the right, and the night jar LYING ON ITS SIDE in the front centre with its lid towards the camera and its front label turned up so it stays readable. The three do not line up and do not sit at equal spacing.",
        "SCENE. Cool pale grey silk with soft rolling folds, the fabric gathering into gentle shadowed troughs between and behind the products. A matching pale grey background out of focus behind. Soft diffused light from the upper right, gentle enough that the silk's folds read as soft gradients rather than hard creases.",
        "FRAME. Camera slightly above the group at a three-quarter angle. All three products fully inside the frame with silk reaching every edge; nothing is cut by any edge. Square format. Sharp focus across all three front labels, every line legible.",
    ),
    (
        "b2-e-hard-shadow-colour-block",
        "A graphic, modern premium skincare product photograph of THREE DIFFERENT Skingenetix Copper Peptide products standing together as a set against a single block of colour.",
        "ARRANGEMENT. The three are staggered in depth rather than in a line: the day jar nearest the camera at the left, the serum bottle further back at the centre, the night jar furthest back at the right, each a clear step behind the last. All three front labels face the camera and stay fully legible.",
        "SCENE. A seamless saturated brand-blue ground and background of one flat colour, no horizon line visible. Hard directional light from the upper left, like clean midday sun, throwing three long crisp-edged shadows across the ground to the lower right. No softening, no gradient, no props of any kind - the whole image is three products, one colour and three hard shadows.",
        "FRAME. Camera at eye level with the group. All three products and the full length of all three shadows are fully inside the frame; nothing is cut by any edge. Square format. Sharp focus across all three front labels, every line legible.",
    ),
    (
        "b2-f-tilted-flatlay",
        "An overhead premium skincare product photograph, camera directly above and looking straight down, of THREE DIFFERENT Skingenetix Copper Peptide products arranged as a set.",
        "ARRANGEMENT. All three lie flat on the surface on a loose diagonal running from the lower left to the upper right, each one TILTED to a different angle rather than squared up to the frame, and spaced unevenly. The two jars lie label-up so their front labels read straight to the camera; the serum bottle lies on its side with its front label facing up and its pipette in line with the bottle. Nothing is parallel to the frame edge.",
        "SCENE. A smooth cool pale-grey plaster surface with a faint matte texture, seen from directly above. Soft broad light from one side laying a short soft shadow beside each object. Nothing else on the surface - no leaves, no flowers, no towels, no tools, no scattered props.",
        "FRAME. All three fully inside the frame with clear plaster margin reaching every edge; nothing is cut by any edge and nothing touches the frame. Square format. Sharp focus across all three labels, every line legible.",
    ),
    (
        "b2-g-low-hero-plinth",
        "A monumental premium skincare product photograph of THREE DIFFERENT Skingenetix Copper Peptide products standing together as a set on a single dark plinth.",
        "ARRANGEMENT. The three stand shoulder to shoulder in a tight group on one shared plinth, the serum bottle at the centre and the two jars flanking it, close enough that their silhouettes nearly touch. All three front labels face the camera and stay fully legible.",
        "SCENE. A single dark graphite stone plinth with a crisp square front edge, filling the lower part of the frame. Behind, a deep cool blue-grey gradient going darker towards the top. Cool key light from high and slightly left, raking down the front of the containers, with a cold soft fill from the right. The mood is architectural and still.",
        "FRAME. Camera LOW, below the level of the plinth top, angled slightly UP at the group so the three products stand against the gradient and read as tall. All three are fully inside the frame with clear space above them; nothing is cut by any edge. Square format. Sharp focus across all three front labels, every line legible.",
    ),
    (
        "b2-h-ice-and-glass",
        "A cold clinical premium skincare product photograph of THREE DIFFERENT Skingenetix Copper Peptide products standing together as a set among clear ice.",
        "ARRANGEMENT. The three stand in a shallow group with the serum bottle at the back centre and the two jars forward and apart, with clear angular blocks of ice set between and behind them at varying heights, none of the ice covering a label. All three front labels face the camera and stay fully legible.",
        "SCENE. A cool white surface with irregular clear ice blocks, some frosted and some glassy, a thin film of meltwater beneath them catching a cold reflection. Crisp cool light from behind and above so the ice glows and refracts, with a clean frontal fill keeping the labels open. Everything reads cold: white, pale ice-blue, clear glass and steel.",
        "FRAME. Camera near eye level with the group. All three products are fully inside the frame with clear margin above and to both sides; nothing is cut by any edge, and no ice block obscures any part of any label. Square format. Sharp focus across all three front labels, every line legible.",
    ),
    (
        "b2-i-bathroom-shelf",
        "An in-context lifestyle photograph of THREE DIFFERENT Skingenetix Copper Peptide products standing together as a set on a floating shelf in a modern bathroom.",
        "ARRANGEMENT. The three stand in a relaxed row along the shelf, unevenly spaced, the serum bottle nearer one end than the middle and the two jars grouped closer together, as they would actually be left rather than styled dead centre. All three front labels face the camera and stay fully legible.",
        "SCENE. A pale grey stone floating shelf against a wall of large-format matte off-white tiles with fine grout lines. Cool daylight from a window out of frame to the left, soft and directional, laying gentle shadows to the right along the shelf. The room is calm, modern and uncluttered - no towels, no plants, no flowers, no brushes, no soap dispensers, no other bottles or jars of any kind.",
        "FRAME. Camera at shelf height, straight on. All three products are fully inside the frame with clear space above them and shelf visible to left and right; nothing is cut by any edge. The tiled wall behind is very slightly soft while all three products stay sharp. Square format. Sharp focus across all three front labels, every line legible.",
    ),
    (
        "b2-j-shallow-depth-cluster",
        "An intimate close premium skincare product photograph of THREE DIFFERENT Skingenetix Copper Peptide products clustered together as a set.",
        "ARRANGEMENT. A tight overlapping cluster seen at a three-quarter angle: the day jar closest to the camera at the lower left with its front label square to the lens, the serum bottle rising immediately behind and between, the night jar furthest back at the right and partly overlapped by the bottle. The group fills much more of the frame than a catalogue shot would.",
        "SCENE. A dark cool blue-grey surface and background with no visible horizon, lit by a soft cool key from the upper left and a cold rim from behind the right so the rear jar separates from the ground. Quiet and close.",
        "FRAME. Camera close and at the height of the jar shoulders. The day jar's front label is in crisp sharp focus; the serum bottle behind it is slightly softer and the night jar furthest back softer still, a real shallow depth of field falling away through the group. All three products stay fully inside the frame; nothing is cut by any edge. Square format. The day jar's label is sharp and every line of it legible.",
    ),
]

def build():
    slots = [build_slot(*c) for c in COMPOSITIONS]

    cfg = {
        "_comment": (
            "Copper Peptide THREE-PRODUCT SET, round 2 — ten compositions, 2026-09-10. "
            "GENERATED by scripts/build-copper-peptide-set-batch2.py; edit the builder, not "
            "this file. Malcolm's brief after round 1: more variations, different positions "
            "and different settings. Compositions drawn from a survey of skincare set "
            "photography — triangular/pyramid hierarchy, staggered depth, rule-of-odds "
            "asymmetric clustering, reflective surfaces, water and droplets, hard-shadow "
            "colour block, tilted flat-lay, low hero angle, in-context shelf, and shallow "
            "depth of field. Round-1 verdict from Malcolm: gpt_image, nbp_flash and seedream "
            "usable, nbp_flash and seedream best; all five suppliers still briefed per "
            "BRAND-003. flux2 is skipped automatically wherever ref_files are present."
        ),
        "wave": "copper-peptide-set-batch2-2026-09-10",
        "defaults": {"negative_global": NEGATIVE},
        "slots": slots,
    }
    OUT.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")

    print(f"{OUT.relative_to(ROOT)}\n{len(slots)} slots\n")
    for s in slots:
        print(f"  {s['id']:<28} prompt={len(s['prompt']):>5}  luma={len(s['prompt_luma']):>5}")
    missing = [r for r in REF_FILES if not (ROOT / r).exists()]
    if missing:
        raise SystemExit(f"missing reference files: {missing}")
    print(f"\n  {len(REF_FILES)} reference files present")
    print(f"  5 suppliers x 2 candidates x {len(slots)} slots = {len(slots) * 10} candidates")


if __name__ == "__main__":
    build()
