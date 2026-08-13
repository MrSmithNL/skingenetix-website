"""Build reference crop set for Skingenetix PDRN Skin Repair Serum photo shoot.

Source: assets/images/pdrn-skin-repair-source/source.png (2048x2048).
Output: 5 reference crops, all centre-cropped square then resized
(NEVER stretch-resize — see product-photography SKILL hard rule).
"""

from pathlib import Path
from PIL import Image

SRC = Path(__file__).parent.parent / "assets/images/pdrn-skin-repair-source/source.png"
OUT = SRC.parent

img = Image.open(SRC).convert("RGB")
w, h = img.size
assert w == h == 2048, f"Expected 2048x2048 source, got {img.size}"


def centre_crop_square(im: Image.Image, region: tuple[int, int, int, int], target: int = 1024) -> Image.Image:
    """Crop `region` (l,t,r,b), centre-crop to square (min dimension), then resize to target square."""
    crop = im.crop(region)
    cw, ch = crop.size
    side = min(cw, ch)
    left = (cw - side) // 2
    top = (ch - side) // 2
    sq = crop.crop((left, top, left + side, top + side))
    return sq.resize((target, target), Image.LANCZOS)


# 1) Full bottle hero (whole image, already square)
full = img.resize((1024, 1024), Image.LANCZOS)
full.save(OUT / "full_bottle.png")

# 2) Product tight — crop white margins.
tight_region = (250, 0, 1798, 2048)
product_tight = centre_crop_square(img, tight_region, 1024)
product_tight.save(OUT / "product_tight.png")

# 3) Label closeup — PDRN label area with DNA helix, Skingenetix wordmark, all text.
label_region = (580, 950, 1480, 1750)
label_closeup = centre_crop_square(img, label_region, 1024)
label_closeup.save(OUT / "label_closeup.png")

# 4) Pipette + cap detail — white rubber bulb + silver collar at top of bottle.
pipette_region = (700, 150, 1380, 900)
pipette_detail = centre_crop_square(img, pipette_region, 1024)
pipette_detail.save(OUT / "pipette_detail.png")

# 5) Material detail — frosted pink glass surface texture (lower portion of bottle, below label).
material_region = (700, 1700, 1380, 2000)
material_detail = centre_crop_square(img, material_region, 1024)
material_detail.save(OUT / "material_detail.png")

for f in ["full_bottle.png", "product_tight.png", "label_closeup.png", "pipette_detail.png", "material_detail.png"]:
    p = OUT / f
    im = Image.open(p)
    print(f"{f}: {im.size} {p.stat().st_size:,} bytes")
