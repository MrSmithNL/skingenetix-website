#!/usr/bin/env python3
"""Add an image Malcolm supplied by hand to a product's finals folder.

    add_supplied.py <src> <product-dir> <product_seo> <shot> <shot_n>

Same treatment as a generated candidate - SEO name, web optimise, manifest entry
- with three differences that matter:

  * the candidate number is taken from what is already in the folder, so a
    supplied image never collides with or overwrites a generated one;
  * the untouched original is kept in the ALL-<product> folder beside the
    generated candidates, so the optimise step stays reproducible;
  * it is tagged backend "external", which keeps it out of cost-per-winner -
    that number compares ENGINES, and a hand-supplied image has no engine.
"""
import json
import os
import re
import shutil
import sys

sys.path.insert(0, "/Users/malcolmsmith/Claude Code/Projects/smith-os/"
                   "packages/forge/skills/product-photography/scripts")
import optimise  # noqa: E402


def next_n(out_dir, product_seo, shot):
    pat = re.compile(rf"^_*{re.escape(product_seo)}_{re.escape(shot)}_(\d+)_skingenetix\.")
    used = [int(m.group(1)) for f in os.listdir(out_dir) if (m := pat.match(f))]
    return max(used, default=0) + 1


def add(src, out_dir, product_seo, shot, shot_n, all_dir):
    n = next_n(out_dir, product_seo, shot)
    stem = f"{product_seo}_{shot}_{n}_skingenetix"

    kept = os.path.join(all_dir, f"_supplied-by-malcolm__{shot_n:02d}_{shot}_external_{n}.png")
    if not os.path.exists(kept):
        shutil.copy2(src, kept)

    # Stage the copy under a name the optimiser cannot also produce. A .jpg
    # source staged as "<stem>.jpg" collides with for_web's own output path, so
    # the cleanup below deleted the finished image.
    tmp = os.path.join(out_dir, "_staging_" + stem + os.path.splitext(src)[1])
    shutil.copy2(src, tmp)
    rec = optimise.for_web(tmp, out_dir)
    if os.path.exists(tmp) and os.path.abspath(tmp) != os.path.abspath(rec["path"]):
        os.remove(tmp)
    # for_web names the output from the staged stem; restore the intended name.
    want = os.path.join(out_dir, stem + os.path.splitext(rec["path"])[1])
    if os.path.abspath(rec["path"]) != os.path.abspath(want):
        shutil.move(rec["path"], want)
        rec["path"] = want
        rec["filename"] = os.path.basename(want)
        rec["alt_text"] = optimise.alt_text_from_name(want)
    rec.update({"source": os.path.basename(src), "run": "supplied-by-malcolm",
                "backend": "external", "shot_n": shot_n, "shot": shot})

    man_path = os.path.join(out_dir, "_upload-manifest.json")
    man = json.load(open(man_path))
    man["images"] = [i for i in man["images"] if i["filename"] != rec["filename"]] + [rec]
    man["count"] = len(man["images"])
    json.dump(man, open(man_path, "w"), indent=2)

    print(f"in  : {rec['bytes_in']/1e6:.2f} MB")
    print(f"out : {rec['bytes_out']/1e6:.3f} MB  {rec['width']}x{rec['height']}  "
          f"q{rec['quality']}  upscaled={rec['upscaled']}  "
          f"({100 - 100*rec['bytes_out']/rec['bytes_in']:.0f}% smaller)")
    print(f"name: {rec['filename']}")
    print(f"alt : {rec['alt_text']}")
    print(f"folder now holds {man['count']} images")
    return rec


if __name__ == "__main__":
    src, out_dir, seo, shot, shot_n = sys.argv[1:6]
    all_dir = "assets/ai-generated/ALL-" + os.path.basename(out_dir.rstrip("/"))
    add(src, out_dir, seo, shot, int(shot_n), all_dir)
