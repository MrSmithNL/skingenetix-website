"""Upload Glutathione Radiant Glow Serum v2 reference crops to fal.ai CDN.
Writes ref_urls_v2.json so the orchestrator can ingest by URL.
"""

import json
import os
from pathlib import Path

import fal_client

REF_DIR = Path(__file__).parent.parent / "assets/images/glutathione-serum-source"
REF_FILES = [
    "v2_full_bottle.png",
    "v2_product_tight.png",
    "v2_label_closeup.png",
    "v2_pipette_detail.png",
    "v2_material_detail.png",
]

assert os.environ.get("FAL_KEY"), "FAL_KEY missing from environment"

urls: dict[str, str] = {}
for f in REF_FILES:
    path = REF_DIR / f
    print(f"Uploading {f} ...", end=" ", flush=True)
    url = fal_client.upload_file(str(path))
    urls[f.replace(".png", "").replace("v2_", "")] = url
    print(url)

out = REF_DIR / "ref_urls_v2.json"
out.write_text(json.dumps(urls, indent=2))
print(f"\nWrote {out}")
