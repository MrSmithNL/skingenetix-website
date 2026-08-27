#!/usr/bin/env python3
"""Close the gap I opened between finding 1 and finding 2 on /pages/pdrn-research.

    python3 scripts/pdrn-research-fix-findings-spacing.py --dry-run
    python3 scripts/pdrn-research-fix-findings-spacing.py

THE FAULT, MEASURED. Moving the crow's-feet finding into its own
`research-before-after` section turned an intra-grid ROW GAP into a SECTION BOUNDARY:

    block 1 -> block 2   160px   (1440)   128px (1024)
    block 2 -> block 3    24px   (1440)    24px (1024)

The three findings used to be three rows of one `media-with-text` grid with
`row-gap: 24px`. Now the first is a separate section, so the space between them is the
sum of two `.section` wrappers' vertical padding — 80px bottom + 80px top — and the
findings no longer read as one evenly spaced list. That is a regression I introduced.

THE FIX, AND WHY IT IS CSS RATHER THAN A SETTING. `research-before-after` has no spacing
setting (its only section-level setting is `title`), and the theme's own
`remove_vertical_spacing` control zeroes BOTH edges, which would then collapse the gap to
whatever sits above. Only the two facing edges should shrink. So a template-local
`custom-html` section carries scoped CSS overriding `padding-block-end` on the first and
`padding-block-start` on the second, to 12px each — 24px total, matching the grid's own
row gap exactly, and 10px each under 1000px where the grid gap is 20px.

SCOPED BY STRUCTURE, NOT BY ID OR BY CLASS ALONE. Section ids are template-scoped and go
stale whenever the template is rebuilt, and a bare
`.shopify-section--research-before-after` rule would also shrink the acetyl page, where
the same section is followed by `references` and its 80px is correct. The selector is
therefore an adjacency pair — a research-before-after section that is IMMEDIATELY
FOLLOWED BY a media-with-text one — which is true here and nowhere else on the store.

Placed LAST in the section order and with `remove_vertical_spacing` on, so the carrier
section itself contributes no height. No Liquid is edited — .claude/rules/shopify.md
rule 2 — and no `{{ }}` appears in the html, which `custom-html` rejects.

Verify by reading COMPUTED padding back off the live page, never by finding the rule in
the source: on this project a verbatim-served style block once changed nothing.

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
SECTION = "findings_spacing_fix"

# `custom-html` rejects a value containing '{{', '}}', '{%' or '%}' with a 422 whose real
# message is only in the response body. Plain CSS trips it by accident: a rule closing
# immediately before a media query's own closing brace produces '}}'. Hence the space
# before the final brace below, and the assertion under it that scans for all four.
CSS = (
    "<style>"
    "/* Added by Claude Code 2026-08-27. The crow's-feet finding lives in its own "
    "research-before-after section, so the space to the next finding is two section "
    "paddings (80+80=160px) instead of the grid row gap (24px). Trim only the two facing "
    "edges. Scoped to a research-before-after section immediately followed by a "
    "media-with-text one, which is true on /pages/pdrn-research and nowhere else - the "
    "acetyl page's equivalent section is followed by references and keeps its 80px. */"
    ".shopify-section--research-before-after:has(+ .shopify-section--media-with-text) "
    "> .section { padding-block-end: 12px; }"
    ".shopify-section--research-before-after + .shopify-section--media-with-text "
    "> .section { padding-block-start: 12px; }"
    "@media (max-width: 999px) {"
    ".shopify-section--research-before-after:has(+ .shopify-section--media-with-text) "
    "> .section { padding-block-end: 10px; }"
    ".shopify-section--research-before-after + .shopify-section--media-with-text "
    "> .section { padding-block-start: 10px; } "   # trailing space: avoids '}}'
    "}"
    "</style>"
)

for _bad in ("{{", "}}", "{%", "%}"):
    assert _bad not in CSS, f"custom-html will 422 on {_bad!r}"


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
    backup.write_text(asset["value"])
    print(f"Backup     : {backup.relative_to(ROOT)}")
    print(f"Undo with  : python3 scripts/patch-template.py --restore "
          f"{backup.relative_to(ROOT)} --template {TEMPLATE}\n")

    tpl["sections"][SECTION] = {
        "type": "custom-html",
        "settings": {
            "full_width": True,
            "remove_vertical_spacing": True,   # the carrier must add no height of its own
            "remove_horizontal_spacing": True,
            "html": CSS,
            "background": "",
        },
    }
    if SECTION not in tpl["order"]:
        tpl["order"].append(SECTION)

    print("Section order now: " + " -> ".join(tpl["order"]))
    print("Trimming the two facing edges to 12px each (24px total, = the grid row gap);"
          " 10px each under 1000px (= 20px).")

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
