#!/usr/bin/env python3
"""Move the crow's-feet finding into a `research-before-after` section on the PDRN page.

    python3 scripts/pdrn-research-add-before-after.py --dry-run
    python3 scripts/pdrn-research-add-before-after.py

Malcolm, 2026-08-27: use the before/after labels content function, like on
/pages/acetyl-hexapeptide-8-research. That page's `key_findings_ba` is a
`research-before-after` section whose `finding` blocks render Before / After / a result
line / "Illustration" as DOM TEXT over the image — not baked into the pixels. Two reasons
that matters and both are on this project's record: no engine ever renders the
percentage, so it cannot be garbled into a false efficacy claim; and the labels stay
translatable, because Translate & Adapt reaches theme JSON but cannot touch pixels.

This is a one-off structural edit, which is why it is its own script rather than a
patch-template.py plan — that runner assigns images and appends sections, but does not
move a block between sections or rewrite the alternation.

WHY THE ALTERNATION IS TOUCHED. `media-with-text` derives left/right from BLOCK INDEX
when `alternate_media_position` is true. Lifting f1 out would shift f2 and f3 up one and
flip both, putting two image-left rows adjacent. So alternation is switched off and the
two survivors carry explicit positions — f2 `end`, f3 `start` — reproducing the current
left / right / left rhythm exactly.

Only section JSON is touched, never Liquid — .claude/rules/shopify.md rule 2. The
`research-before-after` section already exists in the theme; this adds an instance.

Author: Claude Code, 2026-08-27.
"""
import argparse
import json
import urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "2025-01"
TEMPLATE = "templates/page.pdrn-research.json"
NEW_SECTION = "key_findings_ba"
IMAGE = "shopify://shop_images/skingenetix-pdrn-crows-feet-periorbital-wrinkles-before-after.jpg"


def env():
    out = {}
    for line in (ROOT / ".env").read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            out[k.strip()] = v.strip()
    return out


def token(e):
    body = json.dumps({"client_id": e["SHOPIFY_SKINGENETIX_CLIENT_ID"],
                       "client_secret": e["SHOPIFY_SKINGENETIX_CLIENT_SECRET"],
                       "grant_type": "client_credentials"}).encode()
    req = urllib.request.Request(f"https://{e['SHOPIFY_SKINGENETIX_STORE']}/admin/oauth/access_token",
                                 data=body, headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=60).read())["access_token"]


def call(store, tok, path, method="GET", payload=None):
    data = json.dumps(payload).encode() if payload else None
    r = urllib.request.Request(f"https://{store}/admin/api/{API}/{path}", data=data, method=method,
                               headers={"X-Shopify-Access-Token": tok,
                                        "Content-Type": "application/json"})
    with urllib.request.urlopen(r, timeout=120) as res:
        return json.loads(res.read())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    e = env()
    store = e["SHOPIFY_SKINGENETIX_STORE"]
    tok = token(e)
    theme = [t for t in call(store, tok, "themes.json")["themes"] if t["role"] == "main"][0]
    print(f"Live theme : {theme['name']} (id {theme['id']})")

    asset = call(store, tok, f"themes/{theme['id']}/assets.json?asset[key]={TEMPLATE}")["asset"]
    tpl = json.loads(asset["value"])

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = ROOT / "backups" / f"page.pdrn-research-{stamp}.json"
    backup.write_text(json.dumps(tpl, indent=2))
    print(f"Backup     : {backup.relative_to(ROOT)}")
    print(f"Undo with  : python3 scripts/patch-template.py --restore "
          f"{backup.relative_to(ROOT)} --template {TEMPLATE}\n")

    kf = tpl["sections"]["key_findings"]
    if NEW_SECTION in tpl["sections"]:
        print(f"{NEW_SECTION} already exists — nothing to do.")
        return
    f1 = kf["blocks"]["f1"]["settings"]

    # 1. the new section, carrying f1's own title and copy verbatim
    tpl["sections"][NEW_SECTION] = {
        "type": "research-before-after",
        "blocks": {
            "f1": {
                "type": "finding",
                "settings": {
                    "image": IMAGE,
                    "media_position": "start",       # keeps this row image-LEFT, as it is today
                    "before_label": "Before",
                    "after_label": "After 28 days",  # the trial ran 28 days / 4 weeks
                    "result_label": "~20% softer-looking crow's feet",
                    # The honesty device, carried over from the acetyl page unchanged: this is
                    # an illustration of the finding, not a photograph of a trial subject.
                    "note_label": "Illustration",
                    "label_background": "#1a1a1a",
                    "label_text_color": "#ffffff",
                    "title": f1["title"],
                    "content": f1["content"],
                },
            }
        },
        "block_order": ["f1"],
        "settings": {},
    }

    # 2. f1 leaves key_findings; f2 and f3 get explicit positions so the page still reads
    #    left / right / left once the new section sits above them.
    del kf["blocks"]["f1"]
    kf["block_order"] = [b for b in kf["block_order"] if b != "f1"]
    kf["settings"]["alternate_media_position"] = False
    kf["blocks"]["f2"]["settings"]["media_position"] = "end"
    kf["blocks"]["f3"]["settings"]["media_position"] = "start"

    # 3. the new section takes key_findings' place in the order, with key_findings after it
    order = [s for s in tpl["order"]]
    i = order.index("key_findings")
    order.insert(i, NEW_SECTION)
    tpl["order"] = order

    print("Section order now: " + " -> ".join(tpl["order"]))
    print(f"{NEW_SECTION}: 1 finding block, labels "
          f"Before / After 28 days / '~20% softer-looking crow's feet' / Illustration")
    print(f"key_findings: block_order now {kf['block_order']}, "
          f"alternate_media_position False, f2=end f3=start")

    if args.dry_run:
        out = ROOT / "backups" / f"page.pdrn-research-PROPOSED-{stamp}.json"
        out.write_text(json.dumps(tpl, indent=2))
        print(f"\nDRY RUN — proposed template at {out.relative_to(ROOT)}, nothing pushed")
        return

    call(store, tok, f"themes/{theme['id']}/assets.json", "PUT",
         {"asset": {"key": TEMPLATE, "value": json.dumps(tpl, indent=2)}})
    print("\nPUSHED to the live theme.")


if __name__ == "__main__":
    main()
