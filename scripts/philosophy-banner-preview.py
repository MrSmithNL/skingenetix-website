#!/usr/bin/env python3
"""Cut philosophy-hero candidates to the 4.42:1 master and preview them AS THE PAGE RENDERS THEM.

    python3 scripts/philosophy-banner-preview.py assets/ai-generated/2026-08-22-multi-page-philosophy-lab-scientist
    python3 scripts/philosophy-banner-preview.py <run-dir> --top 0.02 --only P2

Two products per candidate, because they answer different questions:

  <stem>-master.jpg   3750x848, the file that would be uploaded
  <stem>-render.jpg   1920x440, what a visitor at 1920 actually sees - the master
                      cover-cropped by the box, the section's dark overlay applied,
                      and the page's real centred headline drawn on top

The second one exists because .claude/rules/website-imagery.md rule 3 is that a contact
sheet cannot judge delivery, only generation. On this page the specific risk is contrast:
white type sits CENTRED over the frame, and the section overlay is currently 45 - enough
to turn a bright laboratory into a grey rectangle. Judging the crop without the type on it
has already cost this project a round elsewhere.

WHY THE CROP IS AIMED HIGH RATHER THAN CENTRED. The wave was briefed for a head about a
quarter of the way down so the master could be cut from the middle of the frame. Every one
of the six suppliers ignored that and put the head 5-14% down, so a centred cut decapitates
the subject. The band is therefore taken from `--top` (default 4% of source height), which
keeps whatever headroom the engine gave and cuts at the chest. That is a stated rule with a
visible result, not an auto-detected bounding box - measuring the head automatically was
wrong twice on this project, and a number checked only against itself gets believed.

Author: Claude Code, 2026-08-27.
"""
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

MASTER_W, MASTER_H = 3750, 848           # 4.42:1, the standing publishing recipe
BOX_W, BOX_H = 1920, 440                 # measured live 2026-08-27 at >=1400px
OVERLAY_HEX, OVERLAY_PCT = "#1A1A1A", 45  # the section's own settings, today
SERIF = "/System/Library/Fonts/Supplemental/Didot.ttc"
SANS = "/System/Library/Fonts/Supplemental/Futura.ttc"


def dims(p: Path) -> tuple[int, int]:
    out = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(p)],
                         capture_output=True, text=True).stdout
    w = h = 0
    for line in out.splitlines():
        if "pixelWidth" in line:
            w = int(line.split(":")[1])
        if "pixelHeight" in line:
            h = int(line.split(":")[1])
    return w, h


def ff(*args):
    r = subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *args],
                       capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"ffmpeg failed: {r.stderr[-400:]}")


#: Built from scripts/face-landmarks.swift, which wraps the macOS Vision framework.
#: Absent or unbuilt, --aim simply falls back to --top.
FACEPOS = ROOT / "scripts" / "bin" / "facepos"


def face_band(src: Path) -> "tuple[float, float] | None":
    """(top of the eyes, bottom of the lips) in source pixels, or None."""
    if not FACEPOS.exists():
        return None
    r = subprocess.run([str(FACEPOS), str(src)], capture_output=True, text=True)
    for line in r.stdout.splitlines():
        parts = line.split("\t")
        if len(parts) < 4 or "ERR" in line:
            continue
        # Faces are emitted largest-first, so f0 is the foreground subject and any
        # further face is the colleague at the microscope. Taking the largest is the
        # rule; it is worth knowing it was WRONG once, on a 6336px frame where the
        # detector found only the colleague until the input was downscaled first.
        first = parts[3].split("|")[0]
        vals = dict(kv.split("=") for kv in first.split() if "=" in kv)
        return float(vals["eyeY"]), float(vals["mouthY"])
    return None


def master(src: Path, dst: Path, top_frac: float, aim: bool = False) -> None:
    """Cut the widest 4.42:1 band the source allows.

    With --aim the band is centred on the eyes-to-mouth span, which is the only thing
    that works across a mixed wave: the six suppliers place the face at wildly different
    heights, so ONE global offset either cuts the smile off the bottom (0.10) or leaves
    nothing but forehead (0.00). Both were tried on the close-up wave and both failed on
    roughly half the candidates. Where the face is taller than the band - Luma frames
    closest and exceeds it - centring loses a little of each end rather than all of one.
    """
    w, h = dims(src)
    band_h = round(w / (MASTER_W / MASTER_H))
    if band_h > h:                        # source already wider than 4.42:1
        band_h, band_w = h, round(h * MASTER_W / MASTER_H)
        x = (w - band_w) // 2
        crop = f"crop={band_w}:{band_h}:{x}:0"
    else:
        y = None
        if aim:
            band = face_band(src)
            if band:
                eye, mouth = band
                y = int(round((eye + mouth) / 2 - band_h / 2))
                y = max(0, min(y, h - band_h))
        if y is None:
            y = min(round(h * top_frac), h - band_h)
        crop = f"crop={w}:{band_h}:0:{y}"
    ff("-i", str(src), "-vf", f"{crop},scale={MASTER_W}:{MASTER_H}:flags=lanczos",
       "-q:v", "2", str(dst))


#: The headline as the live page wraps it, per text position. Centred, the page sets it
#: on two lines about 830px wide - which at 1920 runs x545-x1375, and a head at 0.7 across
#: lands at x1350. That collision is not a crop fault and no crop fixes it; the type and
#: the face are both asking for the middle. Left-aligned into a capped column is the
#: arrangement already shipped on /pages/fine-lines-wrinkles.
WRAP = {
    "centre": ["Real Research. Published", "Concentrations. Full Transparency."],
    "left": ["Real Research.", "Published Concentrations.", "Full Transparency."],
}
BODY = ("Every formula is built on peer-reviewed research and manufactured "
        "to the highest international standards.")
BODY_LEFT = ["Every formula is built on peer-reviewed research",
             "and manufactured to the highest international standards."]
LEFT_INSET = 160          # Impact's container gutter at 1920


def render(src: Path, dst: Path, pos: str, overlay: int) -> None:
    """What 1920px of browser shows: cover-crop, section overlay, then the real type."""
    # object-fit: cover with object-position 50% 50% - scale by height, centre-crop width.
    scale = BOX_H / MASTER_H
    inter_w = round(MASTER_W * scale)
    x = (inter_w - BOX_W) // 2
    ov = f"{OVERLAY_HEX}@{overlay / 100:.2f}"
    draw = [f"drawbox=x=0:y=0:w={BOX_W}:h={BOX_H}:color={ov}:t=fill"]

    if pos == "centre":
        px = "(w-tw)/2"
        lines, body, y0 = WRAP["centre"], [BODY], 126
        draw.append(f"drawtext=fontfile={SANS}:text='Our Philosophy':fontsize=17:"
                    f"fontcolor=white:x={px}:y=76")
    else:
        px = str(LEFT_INSET)
        lines, body, y0 = WRAP["left"], BODY_LEFT, 96
        draw.append(f"drawtext=fontfile={SANS}:text='Our Philosophy':fontsize=17:"
                    f"fontcolor=white:x={px}:y=52")
    for i, ln in enumerate(lines):
        draw.append(f"drawtext=fontfile={SERIF}:text='{ln}':fontsize=62:fontcolor=white:"
                    f"x={px}:y={y0 + i * 74}")
    for i, ln in enumerate(body):
        draw.append(f"drawtext=fontfile={SANS}:text='{ln}':fontsize=17:fontcolor=white:"
                    f"x={px}:y={y0 + len(lines) * 74 + 26 + i * 26}")

    ff("-i", str(src), "-vf",
       f"scale={inter_w}:{BOX_H}:flags=lanczos,crop={BOX_W}:{BOX_H}:{x}:0,{','.join(draw)}",
       "-q:v", "2", str(dst))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir")
    ap.add_argument("--top", type=float, default=0.04,
                    help="where the band starts, as a fraction of source height")
    ap.add_argument("--only", help="slot id prefix")
    ap.add_argument("--text", default="left", choices=["left", "centre", "both"],
                    help="where the overlaid type sits; 'left' is the recommendation")
    ap.add_argument("--aim", action="store_true",
                    help="centre the band on the measured eyes-to-mouth span")
    ap.add_argument("--overlay", type=int, default=22,
                    help=f"section overlay percent; the page currently ships {OVERLAY_PCT}")
    args = ap.parse_args()

    run = Path(args.run_dir)
    if not run.is_absolute():
        run = ROOT / run
    out = run / "preview"
    out.mkdir(parents=True, exist_ok=True)

    srcs = sorted(p for p in run.glob("*/*.png") if p.parent.name != "preview")
    if args.only:
        srcs = [p for p in srcs if p.parent.name.startswith(args.only)]
    if not srcs:
        sys.exit(f"no candidates under {run}")

    positions = ["left", "centre"] if args.text == "both" else [args.text]
    for p in srcs:
        m = out / f"{p.stem}-master.jpg"
        master(p, m, args.top, args.aim)
        for pos in positions:
            suffix = "-render.jpg" if len(positions) == 1 else f"-render-{pos}.jpg"
            render(m, out / f"{p.stem}{suffix}", pos, args.overlay)
        print(f"  {p.stem}")
    print(f"\n{len(srcs)} candidates -> {out.relative_to(ROOT)}")
    print(f"Masters are {MASTER_W}x{MASTER_H}. Renders are {BOX_W}x{BOX_H} with the type "
          f"{'/'.join(positions)}-aligned over an overlay of {args.overlay} "
          f"(the page ships {OVERLAY_PCT} today) - judge contrast on those, not on the "
          "masters.")


if __name__ == "__main__":
    main()
