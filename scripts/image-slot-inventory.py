#!/usr/bin/env python3
"""Turn the raw theme dump into the banner/key-visual inventory.

audit-theme-images.py answers "what does the theme contain". This answers the
question that actually drives a photography brief: for every slot on every page
that renders a BANNER or KEY VISUAL — as opposed to a product packshot or a
colour swatch — is there an image in it, and which file is it?

Colour settings (background, button_background, …) are excluded: they matched
the crude keyword filter in the audit script but are not images.

Reads docs/theme-image-audit.json, writes docs/image-slot-inventory.json and
prints the gap table.

Author: Claude Code, 2026-08-21.
"""
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AUDIT = json.loads((ROOT / "docs" / "theme-image-audit.json").read_text())

# A setting holds an image only if its value is a shopify:// handle or it is an
# image-typed key that is currently empty. Colours are hex, sizes are ints.
IMAGE_KEY = re.compile(r"^(image|image_\d+|background_image|video|media|logo|"
                       r"transparent_logo|favicon|slide_image|mobile_image)$")
COLOUR_VAL = re.compile(r"^#[0-9a-fA-F]{3,8}$")

# Which section types put a large, art-directed image on the page. These are the
# ones a photography brief has to fill; a product-card grid fills itself from
# the catalogue.
BANNER_TYPES = {
    "slideshow":                 "Homepage hero slide",
    "image-with-text-overlay":   "Page hero banner",
    "collection-banner":         "Collection hero banner",
    "media-with-text":           "Section key visual (split layout)",
    "image-link-blocks":         "Navigation / concern tile",
    "multiple-images-with-text": "Concern block imagery",
    "multi-column":              "Column card image",
    "press":                     "Press / featured logo strip",
    "logo-list":                 "Logo strip",
    "testimonials":              "Testimonial portrait",
}


def walk(node, path, out):
    if isinstance(node, dict):
        for k, v in node.items():
            p = f"{path}.{k}" if path else k
            if isinstance(v, (dict, list)):
                walk(v, p, out)
            elif IMAGE_KEY.match(k) and not COLOUR_VAL.match(str(v)):
                out.append((p, k, v))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk(v, f"{path}[{i}]", out)


rows = []
for fkey, doc in AUDIT["files"].items():
    if not isinstance(doc, dict):
        continue
    sections = doc.get("sections", {})
    order = doc.get("order") or list(sections.keys())

    for sid in order:
        sec = sections.get(sid, {})
        stype = sec.get("type", "?")
        found = []
        walk(sec, "", found)
        for path, k, v in found:
            rows.append({
                "template": fkey,
                "section": sid,
                "section_type": stype,
                "role": BANNER_TYPES.get(stype, "—"),
                "is_banner": stype in BANNER_TYPES,
                "setting": k,
                "path": path,
                "value": v,
                "filled": bool(v) and v not in ("", None, False),
            })

    if not sections:  # settings_data.json etc.
        found = []
        walk(doc, "", found)
        for path, k, v in found:
            rows.append({
                "template": fkey, "section": "(theme settings)",
                "section_type": "settings", "role": "Brand asset",
                "is_banner": True, "setting": k, "path": path,
                "value": v, "filled": bool(v) and v not in ("", None, False),
            })

(ROOT / "docs" / "image-slot-inventory.json").write_text(json.dumps(rows, indent=2))

banner_rows = [r for r in rows if r["is_banner"]]
filled = [r for r in banner_rows if r["filled"]]
empty = [r for r in banner_rows if not r["filled"]]


def short(v):
    if not v:
        return "—"
    return str(v).replace("shopify://shop_images/", "")


print("=" * 100)
print(f"BANNER / KEY-VISUAL SLOTS: {len(banner_rows)} total — "
      f"{len(filled)} filled, {len(empty)} EMPTY")
print("=" * 100)

print("\n\n### EMPTY SLOTS — these render with no image today\n")
by_tpl = defaultdict(list)
for r in empty:
    by_tpl[r["template"]].append(r)
for tpl in sorted(by_tpl):
    print(f"\n{tpl}")
    for r in by_tpl[tpl]:
        print(f"   {r['section']:<26} {r['section_type']:<26} {r['setting']}")

print("\n\n### FILLED SLOTS — grouped by the image file they use\n")
usage = defaultdict(list)
for r in filled:
    usage[short(r["value"])].append(f"{r['template'].replace('templates/','').replace('.json','')}:{r['section']}")
for img in sorted(usage, key=lambda i: -len(usage[i])):
    print(f"\n  {img}")
    print(f"      used {len(usage[img])}x: {', '.join(usage[img][:8])}"
          + (" …" if len(usage[img]) > 8 else ""))

print("\n\n### RE-USE PRESSURE — one file doing many jobs is a branding smell\n")
for img, uses in sorted(usage.items(), key=lambda kv: -len(kv[1]))[:15]:
    print(f"  {len(uses):>3}x  {img}")

print(f"\n\nDistinct image files in use : {len(usage)}")
print(f"Wrote docs/image-slot-inventory.json")
