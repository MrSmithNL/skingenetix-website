"""Upload PDRN reference crops to fal.ai CDN so Seedream and FLUX.2 can ingest by URL.
Writes ref_urls.json next to the source images for orchestrator pickup.
"""

import json
import os
from pathlib import Path

import fal_client

REF_DIR = Path(__file__).parent.parent / "assets/images/pdrn-skin-repair-source"
REF_FILES = ["full_bottle.png", "product_tight.png", "label_closeup.png", "pipette_detail.png", "material_detail.png"]

assert os.environ.get("FAL_KEY"), "FAL_KEY missing from environment"

urls: dict[str, str] = {}
for f in REF_FILES:
    path = REF_DIR / f
    print(f"Uploading {f} ...", end=" ", flush=True)
    url = fal_client.upload_file(str(path))
    urls[f.replace(".png", "")] = url
    print(url)

out = REF_DIR / "ref_urls.json"
out.write_text(json.dumps(urls, indent=2))
print(f"\nWrote {out}")
