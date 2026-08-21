#!/usr/bin/env python3
"""Generate Skingenetix website banners and key visuals from a wave config.

    source ~/.claude/config/image-credentials.env
    python3 scripts/generate-banners.py configs/banners/wave1.json --smoke
    python3 scripts/generate-banners.py configs/banners/wave1.json
    python3 scripts/generate-banners.py configs/banners/wave1.json --only D1,D2

This is deliberately NOT the product-photography runner. That skill fans a single
product across six backends with a reference lock, because the job is to reproduce a
real label. Banners are the opposite job: mostly reference-FREE material studies at
wide aspect ratios the shared `_fal_size` helper cannot express (it knows 1:1, 4:5 and
9:16 only). So this runner passes explicit pixel dimensions.

The class distinction from docs/visual-identity/03-art-direction-and-briefs.md is
enforced here rather than left to the prompt author: a class B slot is sent with no
references AND has the branding negatives appended, because a reference-free shot that
is asked for identity invents one. That failure is on record for this project
(2026-08-19, five t2i shots, thirty invented labels).

Author: Claude Code, 2026-08-21.
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
T2I = "fal-ai/bytedance/seedream/v5/lite/text-to-image"
EDIT = "fal-ai/bytedance/seedream/v5/lite/edit"
COST_PER_IMAGE = 0.035


def die(msg):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def build(slot, defaults):
    """Compose the final prompt and negative for one slot."""
    neg = [defaults["negative_global"]]
    if slot["class"] == "B":
        neg.append(defaults["negative_class_b"])
    if slot.get("negative_extra"):
        neg.append(slot["negative_extra"])
    return slot["prompt"], ", ".join(n for n in neg if n)


def generate(slot, defaults, out_root, n, dry=False):
    import fal_client

    prompt, negative = build(slot, defaults)
    refs = list(slot.get("refs") or [])

    # Class A slots name local finals; fal needs URLs, so upload them once.
    for rel in slot.get("ref_files") or []:
        path = ROOT / rel
        if not path.exists():
            die(f"{slot['id']}: reference not found — {rel}")
        print(f"    uploading reference {path.name}")
        refs.append(fal_client.upload_file(str(path)))

    if slot["class"] == "B" and refs:
        die(f"{slot['id']}: class B slot must not carry references")
    if slot["class"] == "A" and not refs:
        die(f"{slot['id']}: class A slot needs references or it will invent branding")

    model = EDIT if refs else T2I
    args = {
        "prompt": prompt,
        "image_size": {"width": slot["width"], "height": slot["height"]},
        "num_images": n,
    }
    if negative:
        args["negative_prompt"] = negative
    if refs:
        args["image_urls"] = refs

    out_dir = out_root / slot["id"]
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "brief.json").write_text(json.dumps(
        {**slot, "_resolved_prompt": prompt, "_resolved_negative": negative,
         "_model": model}, indent=2))

    print(f"\n[{slot['id']}] {slot['title']}")
    print(f"    class {slot['class']} · {slot['width']}x{slot['height']} · {n} candidates")
    print(f"    model {model}")
    if dry:
        print(f"    DRY RUN — prompt {len(prompt)} chars, negative {len(negative)} chars")
        return []

    t0 = time.time()
    try:
        res = fal_client.subscribe(model, arguments=args, with_logs=False)
    except Exception as e:                                   # noqa: BLE001
        print(f"    FAILED: {e}")
        return []

    saved = []
    import urllib.request
    for i, img in enumerate(res.get("images", []), 1):
        url = img.get("url")
        if not url:
            continue
        dest = out_dir / f"{slot['id']}_{i:02d}.jpg"
        urllib.request.urlretrieve(url, dest)
        saved.append(dest)
    print(f"    saved {len(saved)} in {time.time() - t0:.0f}s -> {out_dir.relative_to(ROOT)}")
    return saved


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    ap.add_argument("--smoke", action="store_true",
                    help="one slot, one candidate — proves the endpoint and ratio")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", help="comma-separated slot id prefixes")
    ap.add_argument("--candidates", type=int)
    args = ap.parse_args()

    if not os.environ.get("FAL_KEY"):
        die("FAL_KEY not set — run: source ~/.claude/config/image-credentials.env")

    cfg = json.loads((ROOT / args.config).read_text())
    defaults = cfg["defaults"]
    slots = cfg["slots"]

    if args.only:
        want = tuple(s.strip() for s in args.only.split(","))
        slots = [s for s in slots if s["id"].startswith(want)]
    if args.smoke:
        slots = slots[:1]

    n = 1 if args.smoke else (args.candidates or defaults["candidates"])
    out_root = ROOT / "assets" / "ai-generated" / f"2026-08-21-banners-{cfg['wave']}"

    print(f"Wave      : {cfg['wave']}")
    print(f"Slots     : {len(slots)}")
    print(f"Candidates: {n} each = {len(slots) * n} images")
    print(f"Est. cost : ${len(slots) * n * COST_PER_IMAGE:.2f}")
    print(f"Output    : {out_root.relative_to(ROOT)}")

    total = []
    for slot in slots:
        total += generate(slot, defaults, out_root, n, dry=args.dry_run)

    print(f"\n{'=' * 60}")
    print(f"Generated {len(total)} images · ~${len(total) * COST_PER_IMAGE:.2f}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
