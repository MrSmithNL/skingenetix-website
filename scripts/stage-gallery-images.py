#!/usr/bin/env python3
"""Turn Malcolm's numbered picks into web-ready, SEO-named files a gallery plan can publish.

    python3 scripts/stage-gallery-images.py <gallery-plan.json> [--apply]

WHY A SCRIPT
`publish-product-gallery.py` uploads whatever it is handed and does NOT optimise - verified by
reading it, not assumed. So every bundle so far has had this step done by hand: resolve the
picks, re-encode, rename, drop them in `assets/publish-ready/`. Hand-running it is how a PNG
once reached the CDN and cost roughly 35x the bytes for every client that does not send
`Accept: image/webp`.

IT RESOLVES BY SHEET NUMBER. Malcolm picks off a numbered contact sheet ("5 main, then 2, 16,
9, 15"), so the plan carries `n` and this reads `_sheet-index.json` from the selection folder to
map it back to a filename. The number means nothing outside that one sheet - it shifts the
moment a file is added to the folder - which is why the resolved ref, supplier and source
filename are all written into the plan as it stages. After that the plan no longer depends on
the sheet existing.

OPTIMISATION IS `upload-theme-images.optimise`, NOT A SECOND IMPLEMENTATION. It caps the long
edge to 3000 (the theme's srcset tops out there), forces JPEG, strips metadata and keeps quality
high, deliberately not compressing hard because Shopify's CDN re-encodes anyway. Restating any
of that here would let the two drift.

Author: Claude Code, 2026-09-14.
"""
import argparse
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("uti", ROOT / "scripts" / "upload-theme-images.py")
uti = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(uti)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plan")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    plan_path = ROOT / a.plan
    plan = json.loads(plan_path.read_text())
    sel = ROOT / plan["selection_folder"]
    dest = ROOT / plan["source_dir"]
    index = json.loads((sel / "_sheet-index.json").read_text())["index"]

    items = plan["gallery"] + plan.get("files_only", [])
    print(f"{len(items)} images   {sel}  ->  {dest}\n")
    ok = True
    for it in items:
        n = str(it["n"])
        if n not in index:
            print(f"  !! sheet number {n} is not in _sheet-index.json"); ok = False; continue
        src = sel / index[n]
        if not src.exists():
            print(f"  !! missing source for {n}: {src}"); ok = False; continue
        it["source_file"] = index[n]
        warn = uti.check_seo_name(it["file"])
        flag = f"   SEO: {'; '.join(warn)}" if warn else ""
        print(f"  {n:>3}. {index[n]}\n       -> {it['file']}  ({len(Path(it['file']).stem)} chars){flag}")
        if warn:
            ok = False
        if a.apply:
            dest.mkdir(parents=True, exist_ok=True)
            out = dest / it["file"]
            got = uti.optimise(src, out)
            if Path(got) != out:          # optimise returned the source untouched
                out.write_bytes(Path(got).read_bytes())
    if not ok:
        print("\nfix the problems above before publishing")
        return 1
    if not a.apply:
        print("\nDRY RUN - pass --apply to write the files")
        return 0
    plan_path.write_text(json.dumps(plan, indent=2) + "\n")
    print(f"\nstaged, and source filenames recorded in {a.plan}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
