#!/usr/bin/env python3
"""Re-optimise anything in a finals folder that has drifted from the manifest.

Malcolm edits these folders directly - replacing an image in place, or dropping
in a variant the browser named "...-2.jpg". Both leave the folder inconsistent:
a replaced file is a full-weight original sitting among optimised ones, and an
off-convention name would become an ugly store URL.

This sweeps the folder rather than fixing one file at a time:

  * a file whose byte count no longer matches the manifest has been replaced -
    re-optimise it, keeping the original in the ALL-<product> folder first
  * a file the manifest has never seen gets adopted: renamed onto the SEO
    convention with the next free candidate number, then optimised
  * his leading-underscore selection marks are preserved exactly - they are how
    he picks winners and must survive any rename

Idempotent: run it as often as you like, it only touches what has drifted.
"""
import json
import os
import re
import shutil
import sys
import tempfile

sys.path.insert(0, "/Users/malcolmsmith/Claude Code/Projects/smith-os/"
                   "packages/forge/skills/product-photography/scripts")
import optimise  # noqa: E402

IMG = (".jpg", ".jpeg", ".png", ".webp")


def marks(name):
    """Leading underscores Malcolm uses to mark a pick. Preserve them."""
    m = re.match(r"^(_*)", name)
    return m.group(1)


#: What the two places Malcolm drops files from append to a colliding name.
#: A browser adds "-2" before the extension; Finder adds " copy", then
#: " copy 2". Missing either loses the shot name and files the image under a
#: shot called "supplied", which reaches the manifest, the alt text and the
#: store URL.
_STRAY_SUFFIX = re.compile(r"(?:-\d+)?(?: copy(?: \d+)?)?$", re.I)


def shot_from(stem, product_seo):
    """The shot name inside a stray file's stem, or 'supplied' if there is none.

    `stem` has no extension and no leading marks.
    """
    cleaned = _STRAY_SUFFIX.sub("", stem).strip()
    m = re.match(rf"^{re.escape(product_seo)}_(?P<shot>.+?)_(\d+)_skingenetix$", cleaned)
    return m.group("shot") if m else "supplied"


def next_n(files, product_seo, shot):
    pat = re.compile(rf"^_*{re.escape(product_seo)}_{re.escape(shot)}_(\d+)_skingenetix\.")
    used = [int(m.group(1)) for f in files if (m := pat.match(f))]
    return max(used, default=0) + 1


def sweep(out_dir, product_seo, all_dir, apply=True):
    man_path = os.path.join(out_dir, "_upload-manifest.json")
    man = json.load(open(man_path))
    by_name = {i["filename"]: i for i in man["images"]}

    disk = [f for f in sorted(os.listdir(out_dir)) if f.lower().endswith(IMG)]
    replaced, adopted, gone = [], [], []

    for f in disk:
        bare = f.lstrip("_")
        rec = by_name.get(bare)
        path = os.path.join(out_dir, f)
        size = os.path.getsize(path)

        if rec and size == rec.get("bytes_out"):
            continue                                    # unchanged

        if rec:
            replaced.append((f, size, rec["bytes_out"]))
            target_stem = os.path.splitext(bare)[0]
            shot, n = rec.get("shot"), None
        else:
            # Adopt: recover the shot name through whatever suffix the browser
            # or Finder added, then give it the next free number.
            stem = os.path.splitext(bare)[0]
            shot = shot_from(stem, product_seo)
            n = next_n(disk, product_seo, shot)
            target_stem = f"{product_seo}_{shot}_{n}_skingenetix"
            adopted.append((f, target_stem))

        if not apply:
            continue

        keep = os.path.join(all_dir, f"_supplied-by-malcolm__{target_stem}.orig{os.path.splitext(f)[1]}")
        if not os.path.exists(keep):
            shutil.copy2(path, keep)

        with tempfile.TemporaryDirectory() as td:
            staged = os.path.join(td, target_stem + os.path.splitext(f)[1])
            shutil.copy2(path, staged)
            os.remove(path)
            new = optimise.for_web(staged, out_dir)

        # Restore his selection marks onto the optimised file.
        mk = marks(f)
        if mk:
            marked = os.path.join(out_dir, mk + os.path.basename(new["path"]))
            shutil.move(new["path"], marked)
            new["path"] = marked
        new.update({"source": f, "run": "supplied-by-malcolm", "backend": "external",
                    "shot": shot, "shot_n": (by_name.get(bare) or {}).get("shot_n", 0)})
        by_name[new["filename"]] = new

    live = {f.lstrip("_") for f in os.listdir(out_dir) if f.lower().endswith(IMG)}
    gone = [n for n in list(by_name) if n not in live]
    for n in gone:
        by_name.pop(n)

    man["images"] = list(by_name.values())
    man["count"] = len(man["images"])
    if apply:
        json.dump(man, open(man_path, "w"), indent=2)

    print(f"replaced (re-optimised): {len(replaced)}")
    for f, now, was in replaced:
        print(f"   {now/1e6:>6.3f} MB -> was {was/1e6:.3f} MB   {f}")
    print(f"adopted (renamed onto convention): {len(adopted)}")
    for f, stem in adopted:
        print(f"   {f}\n      -> {stem}.jpg")
    print(f"dropped from manifest (deleted on disk): {len(gone)}")
    print(f"manifest now: {man['count']}   files on disk: {len(live)}")


if __name__ == "__main__":
    out_dir, seo = sys.argv[1], sys.argv[2]
    all_dir = "assets/ai-generated/ALL-" + os.path.basename(out_dir.rstrip("/"))
    sweep(out_dir, seo, all_dir)
