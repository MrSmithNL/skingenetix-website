#!/usr/bin/env python3
"""Tile a banner run into contact sheets and open them.

    python3 scripts/banner-contact-sheet.py assets/ai-generated/2026-08-21-banners-wave1

One sheet per slot, so each slot's candidates sit side by side at a size where the
type zone and the subject can actually be judged. Wide banners and square tiles are
never mixed on one sheet — a 2.25:1 banner shrunk to fit beside a 1:1 tile is too
small to review, which defeats the point.

Candidates keep their index in the filename so Malcolm can mark winners with his
underscore convention (`_` shortlist, `__` winner) on the source file and the mark
survives.

Author: Claude Code, 2026-08-21.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DESKTOP = Path.home() / "Desktop"
TILE_W = 900
FONT = "/System/Library/Fonts/Supplemental/Arial.ttf"


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


#: generate-banners.py writes .jpg and generate-multi.py writes .png. Globbing only
#: .jpg made this print "0 contact sheets" for a whole multi-supplier run on
#: 2026-08-24 with no error — the sheet was empty, not broken, so nothing said so.
def _shots(slot_dir: Path) -> list[Path]:
    return sorted(p for p in slot_dir.iterdir()
                  if p.suffix.lower() in (".jpg", ".jpeg", ".png"))


def build(slot_dir: Path, out: Path) -> bool:
    shots = _shots(slot_dir)
    if not shots:
        return False

    work = slot_dir / ".sheet"
    work.mkdir(exist_ok=True)
    scaled = []
    for i, s in enumerate(shots, 1):
        d = work / f"{i:02d}.png"
        # Stamp the candidate name on the tile. Six suppliers land in one folder and
        # a sheet without names cannot be turned back into a choice.
        cap = s.stem.replace(f"{slot_dir.name}-", "").replace("'", "")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(s),
                        # An explicit fontfile: drawtext falls back to fontconfig,
                        # which is not configured on this Mac and errors out.
                        "-vf", f"scale={TILE_W}:-2,"
                               f"drawtext=fontfile={FONT}:text='{cap}':x=16:y=12:fontsize=30:"
                               f"fontcolor=white:box=1:boxcolor=black@0.65:boxborderw=10",
                        str(d)], check=True)
        scaled.append(d)

    # Engines return different aspects for the same brief - gpt-image 2.246:1,
    # Nano Banana 2.357:1, Seedream 2.246:1 - so after scaling to a common width
    # the heights differ and hstack refuses the row. Pad every tile to the tallest
    # rather than cropping, so nothing is silently cut out of a candidate.
    tall = max(dims(s)[1] for s in scaled)
    for s in scaled:
        if dims(s)[1] != tall:
            tmp = s.with_name(s.stem + "_pad.png")
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(s),
                            "-vf", f"pad={TILE_W}:{tall}:0:(oh-ih)/2:color=black",
                            str(tmp)], check=True)
            tmp.replace(s)

    # Two columns keeps wide banners legible; squares tile 2-up just as well.
    cols = 2
    rows = [scaled[i:i + cols] for i in range(0, len(scaled), cols)]

    row_files = []
    for r, row in enumerate(rows):
        rf = work / f"row{r}.png"
        if len(row) == 1:
            w, h = dims(row[0])
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(row[0]),
                            "-vf", f"pad={TILE_W * cols}:{h}:0:0:color=white", str(rf)],
                           check=True)
        else:
            args = ["ffmpeg", "-loglevel", "error", "-y"]
            for x in row:
                args += ["-i", str(x)]
            args += ["-filter_complex", f"hstack=inputs={len(row)}", str(rf)]
            subprocess.run(args, check=True)
        row_files.append(rf)

    args = ["ffmpeg", "-loglevel", "error", "-y"]
    for rf in row_files:
        args += ["-i", str(rf)]
    if len(row_files) == 1:
        args += [str(out)]
    else:
        args += ["-filter_complex", f"vstack=inputs={len(row_files)}", str(out)]
    subprocess.run(args, check=True)
    return True


def main():
    run_dir = ROOT / sys.argv[1]
    if not run_dir.exists():
        sys.exit(f"not found: {run_dir}")

    made = []
    for slot_dir in sorted(p for p in run_dir.iterdir() if p.is_dir()):
        out = DESKTOP / f"skingenetix-{slot_dir.name}.png"
        if build(slot_dir, out):
            n = len(_shots(slot_dir))
            print(f"  {slot_dir.name:<30} {n} candidates -> {out.name}")
            made.append(out)

    print(f"\n{len(made)} contact sheets on the Desktop")
    # Tiles are ~900px wide from sources up to 6336px, a 7x downscale, and thin
    # letterforms do not survive it. On 2026-08-24 this sheet showed "PORN SKIN
    # REPAIR" on six candidates that all read "PDRN SKIN REPAIR" at native pixels.
    # The sheet is for composition and lighting only.
    print("NOTE: do not judge lettering from these sheets - the downscale breaks thin")
    print("      type and has faked a misspelling before. Crop the label at native")
    print("      pixels, and check again at the size the theme actually renders.")
    for m in made:
        subprocess.run(["open", str(m)])


if __name__ == "__main__":
    main()
