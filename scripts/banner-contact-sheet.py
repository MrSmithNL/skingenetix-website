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
import re
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
        # Stamp the FULL candidate name on the tile. Six suppliers land in one folder
        # and a sheet without names cannot be turned back into a choice. The slot
        # prefix used to be stripped to save width, which made every sheet in a run
        # carry a tile called `luma_01` - the same string names a different
        # photograph in every slot, so a name copied off a sheet was ambiguous.
        cap = s.stem.replace("'", "")
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



# --------------------------------------------------------------------------------------
# Wave-level sheet. Added 2026-08-27 for the copper-peptide before/after round, which is
# 96 slots x 3 suppliers: one sheet per slot would be 96 sheets, which is not a review, it
# is a filing job. This lays a whole wave out as one grid instead — a row per woman, a
# column per supplier — so the engines can be compared against each other on the same
# casting at a glance, which is the actual decision being made.
#
# Still true, and still the reason the per-slot mode exists: a tile this size CANNOT judge
# fine detail. Use this to shortlist on composition, pose difference and obvious honesty
# failures, then open the shortlisted files at native pixels before choosing.
# --------------------------------------------------------------------------------------
WAVE_TILE_W = 640


def build_wave_sheet(run_dir: Path, out: Path) -> bool:
    slot_dirs = sorted(d for d in run_dir.iterdir() if d.is_dir() and not d.name.startswith("."))
    rows_src = [(d.name, _shots(d)) for d in slot_dirs]
    rows_src = [(n, sh) for n, sh in rows_src if sh]
    if not rows_src:
        return False

    work = run_dir / ".wavesheet"
    work.mkdir(exist_ok=True)
    cols = max(len(sh) for _, sh in rows_src)

    row_files = []
    for r, (slot_name, shots) in enumerate(rows_src):
        tiles = []
        for c, sfile in enumerate(shots):
            d = work / f"r{r:02d}c{c}.png"
            # Supplier is the only part of the name that varies inside a row, but stamp
            # the whole stem anyway: slot letters restart every wave, so a bare supplier
            # name copied off a sheet names a different photograph in every other wave.
            cap = sfile.stem.replace("'", "")
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(sfile),
                            "-vf", f"scale={WAVE_TILE_W}:{WAVE_TILE_W},"
                                   f"drawtext=fontfile={FONT}:text='{cap}':x=12:y=10:"
                                   f"fontsize=22:fontcolor=white:box=1:boxcolor=black@0.7:"
                                   f"boxborderw=8",
                            str(d)], check=True)
            tiles.append(d)
        while len(tiles) < cols:
            pad = work / f"r{r:02d}c{len(tiles)}.png"
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "lavfi",
                            "-i", f"color=c=black:s={WAVE_TILE_W}x{WAVE_TILE_W}",
                            "-frames:v", "1", str(pad)], check=True)
            tiles.append(pad)

        rf = work / f"row{r:02d}.png"
        args = ["ffmpeg", "-loglevel", "error", "-y"]
        for t in tiles:
            args += ["-i", str(t)]
        args += ["-filter_complex", f"hstack=inputs={len(tiles)}", str(rf)]
        subprocess.run(args, check=True)
        row_files.append(rf)

    args = ["ffmpeg", "-loglevel", "error", "-y"]
    for rf in row_files:
        args += ["-i", str(rf)]
    args += ["-filter_complex", f"vstack=inputs={len(row_files)}", str(out)]
    subprocess.run(args, check=True)
    return True


def main():
    argv = [a for a in sys.argv[1:] if a != "--per-wave"]
    per_wave = "--per-wave" in sys.argv
    run_dir = ROOT / argv[0]
    if not run_dir.exists():
        sys.exit(f"not found: {run_dir}")

    # The wave has to be in the Desktop filename. Two waves of the same brief at
    # different sizes (a 4.4:1 set and a 3:1 gpt-image set) carry IDENTICAL slot
    # names, so naming sheets by slot alone made the second run silently overwrite
    # the first — nine candidates replaced by two, with no error and no clue.
    wave = re.sub(r"^\d{4}-\d{2}-\d{2}-(multi-)?", "", run_dir.name)

    if per_wave:
        out = DESKTOP / f"skingenetix-wave--{wave}.png"
        if build_wave_sheet(run_dir, out):
            print(f"  {wave} -> {out.name}")
            subprocess.run(["open", str(out)])
        else:
            print(f"  {wave}: nothing to tile")
        return

    made = []
    for slot_dir in sorted(p for p in run_dir.iterdir() if p.is_dir()):
        out = DESKTOP / f"skingenetix-{slot_dir.name}--{wave}.png"
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
