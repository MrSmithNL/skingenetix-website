#!/usr/bin/env python3
"""Emit the round-3 Copper Peptide SET brief — ten CLOSE modern-minimalist bathroom scenes.

    python3 scripts/build-copper-peptide-bathroom-batch3.py
    set -a; source ~/.claude/config/image-credentials.env; set +a
    python3 scripts/generate-multi.py configs/banners/copper-peptide-bathroom-batch3-2026-09-11.json

Malcolm, 2026-09-11, after picking sixteen from round 2: "lets research much better modern,
minimalistic close up bathroom scene shots - and make a new batch of bathroom scene images."

Round 2 had exactly one bathroom slot (`b2-i-bathroom-shelf`) and it was a WIDE shelf shot. All
ten below are CLOSE - the group fills the frame and the room is a few surfaces and a quality of
light, not a room tour.

THE RESEARCH HAS A DIRECT CONFLICT WITH THE BRAND, AND THAT SHAPED EVERY SCENE HERE.
Current minimalist-bathroom styling is overwhelmingly WARM: travertine, taupe, cream, sand
tones, warm paneling, natural wood vanities, clay alcoves and warm metallic accents in gold and
brass. The Skingenetix palette bars every one of those by name. So what is taken from the
research is the STRUCTURE the sources agree on - seamless microcement, recessed niches, floating
vanities, frameless glass, backlit mirrors, matte black fixtures, honed stone, surfaces meeting
without trim - and every one of them is specified in the COOL register instead. The nearest
real-world reference is Bynacht: moody light, soft shadow, matte texture, deep blue-grey.

EVERY SURFACE IS A POSITIVE REQUIREMENT, NOT A NEGATIVE. Measured on 2026-09-10: the round-1
vanity slot returned a sage-green bowl and a warm beige granite counter while "green" and "warm
colour cast" were both barred by name in `negative_global`. The bar holds on the PRODUCTS and
leaks on the SET DRESSING. So each scene below states what the surface IS - "cool mid-grey
honed limestone with no beige or yellow in it" - rather than trusting the negative to keep
warmth out, and each names the props that ARE present so there is no gap for an engine to fill
with a plant or a bowl.

NOTHING IS CROPPED, DELIBERATELY. "Close up" here means the group fills the frame, not that a
container is cut. `negative_global` bars a cropped product, and a slot asking for a macro crop
while the negative forbids one is a contradiction that produces mush. A true macro crop is a
separate wave with its own negative.

The product spec is imported from `copper_peptide_set_spec`, not restated - see that module's
docstring for why.

Author: Claude Code, 2026-09-11.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from copper_peptide_set_spec import (  # noqa: E402
    NEGATIVE, REF_FILES, build_slot,
)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "configs" / "banners" / "copper-peptide-bathroom-batch3-2026-09-11.json"

OPENING = ("A close, modern, minimalist bathroom photograph of THREE DIFFERENT Skingenetix "
           "Copper Peptide products standing together as a set.")

#: (id, ARRANGEMENT, SCENE, FRAME). Three separate strings so one axis can be retuned without
#: disturbing the other two.
COMPOSITIONS = [
    (
        "b3-a-microcement-niche",
        "ARRANGEMENT. The three stand together inside a shallow rectangular niche recessed into the wall, the serum bottle at the centre and the two jars either side of it, spaced evenly with a little air between them and a little air above their tops. All three front labels face the camera and stay fully legible.",
        "SCENE. A seamless hand-troweled microcement wall in a COOL MID-GREY with a faint cloudy mottling and no beige, sand or yellow in it at all. The niche is cut straight into that same microcement with soft rounded internal corners and no tile, no trim and no frame of any kind around it. A concealed strip light in the top lip of the niche washes cool light down the back wall and across the labels. The only objects anywhere in the picture are the three products.",
        "FRAME. Camera square on to the niche at the height of the products, close enough that the niche opening fills most of the frame with a margin of plain microcement wall all around it. All three products are fully inside the frame; nothing is cut by any edge. Square format. Sharp focus across all three front labels, every line legible.",
    ),
    (
        "b3-b-floating-vanity-edge",
        "ARRANGEMENT. The three stand in a close group near the front edge of the vanity top, the serum bottle slightly behind the two jars so the group has depth, all three turned a few degrees towards the camera. All three front labels face the camera and stay fully legible.",
        "SCENE. A floating vanity top of COOL PALE GREY honed limestone with a crisp square front edge and a fine even grain, no warm or cream tone in the stone. Behind it a plain wall of the same cool grey in a matte finish. A slim matte-black wall-mounted spout is visible behind the group, softly out of focus. Cool even daylight from the left. The only objects anywhere in the picture are the three products and that spout.",
        "FRAME. Camera low and close, almost level with the vanity top, so the stone edge runs across the bottom of the frame as a sharp horizontal line. All three products are fully inside the frame with clear space above them; nothing is cut by any edge. Square format. Sharp focus across all three front labels, every line legible.",
    ),
    (
        "b3-c-fluted-glass-backlit",
        "ARRANGEMENT. The three stand in a close row directly in front of a fluted glass panel, the serum bottle at the centre and slightly forward, the jars just behind at either side. All three front labels face the camera and stay fully legible.",
        "SCENE. A floor-to-ceiling panel of COOL CLEAR reeded glass in fine vertical flutes, lit from behind by soft cool daylight so the whole panel glows a pale blue-white and breaks the light into vertical bands. The products stand on a narrow shelf of cool pale grey honed stone. No warm light, no yellow glow, no amber - the light coming through the glass is cold and blue-white. The only objects anywhere in the picture are the three products.",
        "FRAME. Camera square on, close, the fluted panel filling the whole background behind the group. All three products are fully inside the frame and stand clear of the frame edges; nothing is cut. The glass behind is softly out of focus while all three products stay sharp. Square format. Sharp focus across all three front labels, every line legible.",
    ),
    (
        "b3-d-basin-rim-droplets",
        "ARRANGEMENT. The three stand in a tight group on the stone surround immediately beside the rim of a basin, the two jars forward and the serum bottle just behind between them. All three front labels face the camera and stay fully legible.",
        "SCENE. A matte white stone basin with a thin square rim, set into a surround of COOL MID-GREY honed stone with no beige or cream in it. Fine water droplets are scattered across the stone surround and a few cling to the shoulders of the glass. A matte-black spout sits above and behind, well out of focus. Cool crisp daylight from the upper left so each droplet carries a small hard highlight. The only objects anywhere in the picture are the three products, the basin and that spout.",
        "FRAME. Camera close and just above the level of the jar lids, looking slightly down across the wet stone. All three products are fully inside the frame; nothing is cut by any edge. Square format. Sharp focus across all three front labels, every line legible.",
    ),
    (
        "b3-e-backlit-mirror-halo",
        "ARRANGEMENT. The three stand in a close group on a narrow ledge directly beneath a round backlit mirror, the serum bottle at the centre, the jars either side and a little forward. All three front labels face the camera and stay fully legible.",
        "SCENE. A round frameless mirror mounted flush to a wall of COOL DARK GREY matte plaster, with a concealed cool-white LED halo behind the mirror throwing a soft ring of cold light onto the wall around it. That halo is the main light in the picture and it is white-blue, never warm, never yellow. The ledge is a slim slab of cool pale grey stone. The room falls away into deep cool shadow at the edges. The only objects anywhere in the picture are the three products and the mirror.",
        "FRAME. Camera square on and close, the lower arc of the glowing mirror filling the upper part of the frame behind the group. All three products are fully inside the frame; nothing is cut by any edge. Square format. Sharp focus across all three front labels, every line legible.",
    ),
    (
        "b3-f-shower-ledge-steam",
        "ARRANGEMENT. The three stand in a close row along a built-in shower ledge, evenly spaced with a little air between them, the serum bottle at the centre. All three front labels face the camera and stay fully legible.",
        "SCENE. A built-in ledge of COOL GREY honed stone running along a wall of large-format matte pale-grey porcelain tiles with very fine grout lines. A faint cool haze of steam drifts across the upper part of the scene and the vertical edge of a frameless glass screen catches a thin cold highlight at one side. Everything is cool and damp: grey stone, pale grey tile, clear glass, white-blue light. The only objects anywhere in the picture are the three products.",
        "FRAME. Camera square on and close, the ledge running across the frame and the tiled wall filling the background. All three products are fully inside the frame; nothing is cut by any edge. Square format. Sharp focus across all three front labels, every line legible.",
    ),
    (
        "b3-g-low-key-dark-stone",
        "ARRANGEMENT. The three stand in a tight overlapping group, the serum bottle at the centre and slightly forward, the jars close either side and a little behind so their shoulders just overlap its flanks. All three front labels face the camera and stay fully legible.",
        "SCENE. A near-black honed stone surface and a near-black wall behind, both COOL and blue-black rather than brown-black. A single narrow shaft of cold white light falls from high on one side, crossing the three front labels and leaving the rest of the frame in deep shadow, with a faint cool bounce lifting the shadowed flanks just enough to separate them from the background. Moody, matte, restrained. The only objects anywhere in the picture are the three products.",
        "FRAME. Camera close and level with the labels. All three products are fully inside the frame with dark space above them; nothing is cut by any edge. Square format. The shaft of light falls squarely across all three front labels so every line stays legible and sharp.",
    ),
    (
        "b3-h-window-sill-daylight",
        "ARRANGEMENT. The three stand in a relaxed close group on a deep window sill, unevenly spaced, the two jars a little closer together and the serum bottle set slightly apart. All three front labels face the camera and stay fully legible.",
        "SCENE. A deep sill of COOL PALE GREY honed stone in a reveal of the same cool grey plaster, with soft north daylight coming from the window so the light is flat, cold and blue-white with no sun patch and no warm cast. A folded edge of pale cool-grey linen lies flat on the sill behind the group. The view beyond the window is blown out to plain soft white and shows nothing. The only objects anywhere in the picture are the three products and that folded linen.",
        "FRAME. Camera close and square on, the sill running across the lower frame and the pale window light filling the background. All three products are fully inside the frame; nothing is cut by any edge. Square format. Sharp focus across all three front labels, every line legible.",
    ),
    (
        "b3-i-mirror-doubled",
        "ARRANGEMENT. The three stand in a close row directly against a mirror, so each one is doubled by its own reflection immediately behind it and the group reads as six forms - three real and three reflected. The serum bottle is at the centre. All three REAL front labels face the camera and stay fully legible.",
        "SCENE. A frameless mirror running the full width behind the group, meeting a vanity top of COOL PALE GREY honed stone with no visible trim or joint line. Cool even light from the front and slightly above, soft enough that the mirror shows no glare across the labels. Everything in shot is grey, silver, clear glass and the products' own blues. The only objects anywhere in the picture are the three products and their reflections.",
        "FRAME. Camera square on and close, at the height of the labels, positioned so the camera itself does not appear in the mirror. All three products and their reflections are fully inside the frame; nothing is cut by any edge. Square format. Sharp focus across all three real front labels, every line legible.",
    ),
    (
        "b3-j-stone-shelf-shadow-play",
        "ARRANGEMENT. The three stand well apart in a single row on a long narrow shelf, with clear space between each one so the shelf reads as sparse rather than stocked, the serum bottle at the centre. All three front labels face the camera and stay fully legible.",
        "SCENE. A single slim shelf of COOL MID-GREY honed stone cantilevered from a wall of the same cool grey microcement, no brackets visible. Hard cold light rakes in from one side through a window out of frame, throwing three long crisp-edged shadows along the wall behind and a band of bright light across the shelf. No warm tone anywhere - the light is white-blue and the shadows are cool grey. The only objects anywhere in the picture are the three products.",
        "FRAME. Camera square on and close, the shelf running across the frame and the shadowed wall filling the background. All three products and all three of their wall shadows are fully inside the frame; nothing is cut by any edge. Square format. Sharp focus across all three front labels, every line legible.",
    ),
]

#: Appended to the shared negative for this wave only. The shared list already bars warm tones
#: generically; these name the specific warm MATERIALS the bathroom research is saturated with,
#: because "warm colour cast" did not stop a beige granite counter from arriving on 2026-09-10.
BATHROOM_NEGATIVE_EXTRA = (
    "travertine, beige stone, cream stone, sand-coloured stone, taupe, warm marble, wooden "
    "vanity, wood panelling, rattan, woven basket, brass fixtures, gold fixtures, warm metallic "
    "accents, clay walls, terracotta tile, houseplant, potted plant, folded towels on a rail, "
    "soap dispenser, toothbrush, candle, tray of cosmetics, other skincare bottles, clutter"
)


def build():
    slots = [
        build_slot(slot_id, OPENING, arrangement, scene, frame)
        for slot_id, arrangement, scene, frame in COMPOSITIONS
    ]
    for s in slots:
        s["negative_extra"] = BATHROOM_NEGATIVE_EXTRA

    cfg = {
        "_comment": (
            "Copper Peptide SET in modern minimalist bathroom scenes, round 3, 2026-09-11. "
            "GENERATED by scripts/build-copper-peptide-bathroom-batch3.py; edit the builder, "
            "not this file. Malcolm's brief: much better modern, minimalistic CLOSE UP bathroom "
            "scenes. Round 2 had one bathroom slot and it was a wide shelf shot; all ten here "
            "are close. Researched first: current minimalist-bathroom styling is overwhelmingly "
            "warm (travertine, taupe, cream, wood, brass) and this brand bars all of it, so the "
            "STRUCTURE is taken from the research - microcement, recessed niches, floating "
            "vanities, frameless glass, backlit mirrors, matte black fixtures, honed stone - and "
            "every surface is respecified in the cool register. Each scene states what its "
            "surface IS and names the props that ARE present, because the negative list is known "
            "to leak on set dressing. Nothing is cropped: negative_global bars a cropped "
            "product, so 'close up' means the group fills the frame."
        ),
        "wave": "copper-peptide-bathroom-batch3-2026-09-11",
        "defaults": {"negative_global": NEGATIVE},
        "slots": slots,
    }
    OUT.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")

    print(f"{OUT.relative_to(ROOT)}\n{len(slots)} slots\n")
    for s in slots:
        print(f"  {s['id']:<30} prompt={len(s['prompt']):>5}  luma={len(s['prompt_luma']):>5}")
    missing = [r for r in REF_FILES if not (ROOT / r).exists()]
    if missing:
        raise SystemExit(f"missing reference files: {missing}")
    print(f"\n  {len(REF_FILES)} reference files present")
    print(f"  5 suppliers x 2 candidates x {len(slots)} slots = {len(slots) * 10} candidates")


if __name__ == "__main__":
    build()
