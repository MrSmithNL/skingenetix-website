"""Build reference crop set for Matrixyl 3000 Pro Collagen Serum photo shoot.

Source: assets/images/matrixyl-3000-serum-source/source.png (2048x2048).
Output: 5 reference crops, all centre-cropped square then resized
(NEVER stretch-resize — see product-photography SKILL hard rule).
"""

from pathlib import Path
from PIL import Image

SRC = Path(__file__).parent.parent / "assets/images/matrixyl-3000-serum-source/source.png"
OUT = SRC.parent

img = Image.open(SRC)
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


# 1) Full bottle hero (whole image, already square) — used as the canonical reference
full = img.resize((1024, 1024), Image.LANCZOS)
full.save(OUT / "full_bottle.png")

# 2) Product tight — crop padding off but keep entire bottle visible. Looking at the image,
# the bottle occupies roughly the central 60% horizontally and 95% vertically. Crop just a bit
# of the white margin and centre-crop square.
tight_region = (250, 0, 1798, 2048)  # 1548 wide x 2048 tall → crop square = 1548
product_tight = centre_crop_square(img, tight_region, 1024)
product_tight.save(OUT / "product_tight.png")

# 3) Label closeup — the printed label region with Skingenetix logo + all text.
# Label spans roughly x:580-1480, y:900-1700 → 900x800. Centre-crop square = 800x800.
label_region = (580, 900, 1480, 1700)
label_closeup = centre_crop_square(img, label_region, 1024)
label_closeup.save(OUT / "label_closeup.png")

# 4) Pipette + cap detail — top portion with white rubber bulb + silver collar.
# Pipette region roughly x:780-1300, y:150-900 → 520x750. Centre-crop square = 520x520.
pipette_region = (700, 150, 1380, 900)
pipette_detail = centre_crop_square(img, pipette_region, 1024)
pipette_detail.save(OUT / "pipette_detail.png")

# 5) Material detail — frosted glass surface texture (lower portion of bottle, no label).
# Material region roughly x:600-1450, y:1700-2000 → 850x300. Take square 300x300 from centre.
material_region = (700, 1620, 1380, 2000)  # below the label
material_detail = centre_crop_square(img, material_region, 1024)
material_detail.save(OUT / "material_detail.png")

# Print verification
for f in ["full_bottle.png", "product_tight.png", "label_closeup.png", "pipette_detail.png", "material_detail.png"]:
    p = OUT / f
    im = Image.open(p)
    print(f"{f}: {im.size} {p.stat().st_size:,} bytes")
