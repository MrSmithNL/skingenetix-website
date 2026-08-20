#!/usr/bin/env python3
"""Turn Malcolm's underscore-marked picks into upload-ready, SEO-named images.

He marks a winner by prefixing its filename with '_' in the ALL-<product>
folder. This finds those, gives each an SEO filename carrying the search terms
and the key actives, optimises it for web, and records which engine produced it
so cost-per-winner can finally be computed - the number the whole rebuild was
supposed to make answerable.

Naming follows the skill's documented convention,
    [product_with_key_ingredient]_[shot_type]_[n]_skingenetix.jpg
with the actives written into the product part, per Malcolm's brief.

Nothing is uploaded here. This only prepares files.
"""
import json
import os
import re
import sys

sys.path.insert(0, "/Users/malcolmsmith/Claude Code/Projects/smith-os/"
                   "packages/forge/skills/product-photography/scripts")
import optimise  # noqa: E402

BACKENDS = ("seedream", "luma", "nbp_pro", "nbp_flash", "flux2", "gpt_image")
# run-01__06_product_and_box_hero_nbp_pro_1.png
PAT = re.compile(r"^_?(?P<run>run-\d+)__(?P<n>\d{2})_(?P<shot>.+?)_(?P<be>" +
                 "|".join(BACKENDS) + r")_(?P<i>\d+)\.(?:png|jpe?g|webp)$")


def prep(src_dir, out_dir, product_seo, label):
    picks = sorted(f for f in os.listdir(src_dir)
                   if f.startswith("_") and f.lower().endswith((".png", ".jpg", ".jpeg", ".webp")))
    os.makedirs(out_dir, exist_ok=True)
    per_shot, records = {}, []

    for f in picks:
        m = PAT.match(f)
        if not m:
            print(f"  ! could not parse {f}")
            continue
        shot = m.group("shot")
        per_shot[shot] = per_shot.get(shot, 0) + 1
        stem = f"{product_seo}_{shot}_{per_shot[shot]}_skingenetix".lower()

        src = os.path.join(src_dir, f)
        tmp = os.path.join(out_dir, stem + os.path.splitext(f)[1])
        os.link(src, tmp) if not os.path.exists(tmp) else None
        rec = optimise.for_web(tmp, out_dir)
        os.remove(tmp)

        rec.update({"source": f, "run": m.group("run"), "backend": m.group("be"),
                    "shot_n": int(m.group("n")), "shot": shot})
        records.append(rec)

    manifest = os.path.join(out_dir, "_upload-manifest.json")
    json.dump({"product": label, "product_seo": product_seo,
               "count": len(records), "images": records},
              open(manifest, "w"), indent=2)

    bytes_in = sum(r["bytes_in"] for r in records)
    bytes_out = sum(r["bytes_out"] for r in records)
    print(f"{label}: {len(records)} images ready")
    print(f"   {bytes_in/1e6:.1f} MB -> {bytes_out/1e6:.1f} MB "
          f"({100 - 100*bytes_out/max(bytes_in,1):.0f}% smaller)")
    print(f"   covering {len(per_shot)} distinct shots")
    return records


if __name__ == "__main__":
    src, out, seo, label = sys.argv[1:5]
    prep(src, out, seo, label)
