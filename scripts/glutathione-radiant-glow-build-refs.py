"""Build reference crop set for Skingenetix Glutathione Radiant Glow Serum photo shoot.

Source: assets/images/glutathione-serum-source/source_v2_corrected.png (2048x2048 RGBA).
Output: 5 reference crops, all centre-cropped square then resized
(NEVER stretch-resize — see product-photography SKILL hard rule).

Adapted from pdrn-skin-repair-build-refs.py.
"""

from pathlib import Path
from PIL import Image

SRC = Path(__file__).parent.parent / "assets/images/glutathione-serum-source/source_v2_corrected.png"
OUT = SRC.parent

img = Image.open(SRC).convert("RGB")
w, h = img.size
assert w == h == 2048, f"Expected 2048x2048 source, got {img.size}"


def centre_crop_square(im: Image.Image, region: tuple[int, int, int, int], target: int = 1024) -> Image.Image:
    crop = im.crop(region)
    cw, ch = crop.size
    side = min(cw, ch)
    left = (cw - side) // 2
    top = (ch - side) // 2
    sq = crop.crop((left, top, left + side, top + side))
    return sq.resize((target, target), Image.LANCZOS)


full = img.resize((1024, 1024), Image.LANCZOS)
full.save(OUT / "v2_full_bottle.png")

tight_region = (380, 180, 1668, 1620)
product_tight = centre_crop_square(img, tight_region, 1024)
product_tight.save(OUT / "v2_product_tight.png")

label_region = (480, 800, 1540, 1580)
label_closeup = centre_crop_square(img, label_region, 1024)
label_closeup.save(OUT / "v2_label_closeup.png")

pipette_region = (720, 170, 1320, 770)
pipette_detail = centre_crop_square(img, pipette_region, 1024)
pipette_detail.save(OUT / "v2_pipette_detail.png")

material_region = (700, 1450, 1340, 1620)
material_detail = centre_crop_square(img, material_region, 1024)
material_detail.save(OUT / "v2_material_detail.png")

for f in ["v2_full_bottle.png", "v2_product_tight.png", "v2_label_closeup.png", "v2_pipette_detail.png", "v2_material_detail.png"]:
    p = OUT / f
    im = Image.open(p)
    print(f"{f}: {im.size} {p.stat().st_size:,} bytes")
