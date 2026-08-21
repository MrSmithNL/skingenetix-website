#!/usr/bin/env python3
"""Prepare images Malcolm marked directly in a fan-out run's output folder.

    python3 scripts/finals/prepare-marked-run-output.py <run-dir> <finals-dir> [--apply]

`prepare-selected-for-upload.py` reads the ALL-<product> browse folder, where
every file is named `run-01__NN_shot_engine_N.png`. Malcolm has also started
marking winners in the fan-out's own output folder, where the files already
carry their final SEO name. Same intent, different naming, so this reads that
form instead.

It takes the engine from the run's `manifest.json` rather than from the
filename, so cost-per-winner keeps working - that number compares ENGINES and is
the question the whole pipeline rebuild exists to answer. Marking in the output
folder throws the engine away from the name; the manifest still has it.

Marks are preserved: `_` keeps, `__` publishes, exactly as they were.

Author: Claude Code, 2026-08-21.
"""
import json
import os
import re
import sys

sys.path.insert(0, "/Users/malcolmsmith/Claude Code/Projects/smith-os/"
                   "packages/forge/skills/product-photography/scripts")
import optimise  # noqa: E402

IMG = (".png", ".jpg", ".jpeg", ".webp")


def marks(name):
    """The leading underscores Malcolm used to mark this file."""
    return re.match(r"^(_*)", name).group(1)


def match_record(marked_name, index):
    """Find the manifest record for a marked file.

    Renaming in Finder to prepend an underscore can EAT leading characters -
    the 2026-08-21 Matrixyl run has `_atrixyl_...`, which is `matrixyl` with the
    m consumed. So an exact match is tried first, then a unique suffix match.
    An ambiguous suffix raises rather than guessing: attributing a winner to the
    wrong engine is worse than refusing to place it.
    """
    bare = marked_name.lstrip("_")
    if bare in index:
        return index[bare], bare
    hits = [k for k in index if k.endswith(bare)]
    if len(hits) == 1:
        return index[hits[0]], hits[0]
    raise KeyError(f"{marked_name!r} matched {len(hits)} manifest records"
                   + (f": {hits}" if hits else " - not from this run?"))


def next_free(out_dir, stem_base):
    """A candidate number in `out_dir` that nothing already uses."""
    m = re.match(r"^(?P<head>.+)_(?P<n>\d+)_skingenetix$", stem_base)
    if not m:
        return stem_base
    head, n = m.group("head"), int(m.group("n"))
    while True:
        cand = f"{head}_{n}_skingenetix"
        if not any(f.lstrip("_").startswith(cand + ".") for f in os.listdir(out_dir)):
            return cand
        n += 1


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    apply = "--apply" in sys.argv
    if len(args) != 2:
        print(__doc__)
        return 2
    run_dir, out_dir = args

    man = json.load(open(os.path.join(run_dir, "manifest.json")))
    index = {}
    for c in man["candidates"]:
        rp = c.get("renamed_path") or ""
        if rp:
            index[os.path.basename(rp)] = c

    marked = sorted(f for f in os.listdir(run_dir)
                    if f.startswith("_") and f.lower().endswith(IMG))
    if not marked:
        print("nothing marked in", run_dir)
        return 0

    os.makedirs(out_dir, exist_ok=True)
    man_path = os.path.join(out_dir, "_upload-manifest.json")
    fin = json.load(open(man_path))
    by_name = {i["filename"]: i for i in fin["images"]}

    print(f"{len(marked)} marked file(s) in {os.path.basename(run_dir)}\n")
    done = failed = 0
    for f in marked:
        try:
            rec, real = match_record(f, index)
        except KeyError as e:
            print(f"  !! {e}")
            failed += 1
            continue
        mk = marks(f)
        stem = next_free(out_dir, os.path.splitext(real)[0])
        if not apply:
            print(f"  {mk or '  '}{stem}.jpg   [{rec['backend']}]")
            done += 1
            continue

        tmp = os.path.join(out_dir, "_staging_" + stem + os.path.splitext(f)[1])
        with open(os.path.join(run_dir, f), "rb") as src, open(tmp, "wb") as dst:
            dst.write(src.read())
        out = optimise.for_web(tmp, out_dir)
        if os.path.exists(tmp) and os.path.abspath(tmp) != os.path.abspath(out["path"]):
            os.remove(tmp)
        want = os.path.join(out_dir, stem + os.path.splitext(out["path"])[1])
        if os.path.abspath(out["path"]) != os.path.abspath(want):
            os.rename(out["path"], want)
            out["path"] = want
            out["filename"] = os.path.basename(want)
            out["alt_text"] = optimise.alt_text_from_name(want)
        if mk:
            marked_path = os.path.join(out_dir, mk + out["filename"])
            os.rename(out["path"], marked_path)
            out["path"] = marked_path
        out.update({"source": f, "run": os.path.basename(os.path.dirname(run_dir + "/")),
                    "backend": rec["backend"], "shot": rec.get("shot_name"),
                    "shot_n": int(rec.get("shot_n") or 0)})
        by_name[out["filename"]] = out
        print(f"  {mk or '  '}{out['filename']}   [{rec['backend']}]  "
              f"{out['bytes_in']/1e6:.2f} -> {out['bytes_out']/1e6:.3f} MB")
        done += 1

    if apply:
        fin["images"] = list(by_name.values())
        fin["count"] = len(fin["images"])
        json.dump(fin, open(man_path, "w"), indent=2)
        print(f"\n{done} prepared, {failed} unmatched. folder now holds {fin['count']}")
    else:
        print(f"\n{done} would be prepared, {failed} unmatched.  DRY RUN - pass --apply")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
