#!/usr/bin/env python3
"""Clear the `note_label` on every `research-before-after` finding block.

    python3 scripts/clear-before-after-note-label.py --dry-run
    python3 scripts/clear-before-after-note-label.py

Malcolm, 2026-08-27: remove the 'Illustration' label from the PDRN page and from
/pages/acetyl-hexapeptide-8-research.

The section's Liquid guards the element with `{%- if block.settings.note_label != blank -%}`,
so setting the value to an empty string removes the `<p class="rba__label rba__label--note">`
outright rather than leaving an empty pill. Verified against sections/research-before-after.liquid
before writing this.

⚠️ THE DISCLOSURE IS NOW MISSING FROM THESE PAGES AND HAS TO COME BACK IN THE COPY.

`note_label: "Illustration"` was the device marking these before/after diptychs as illustrations
of a published finding rather than photographs of trial subjects. Every one is AI-generated and
sits beside a real number from a real paper, so the disclosure has to exist somewhere.

Malcolm, 2026-08-27, in two messages: *"we can address this in other ways - like in the text"*
and *"lets fix it in the text later though. fix the images first"*. So this script does the
label removal ONLY, and the text disclosure is an OUTSTANDING TASK, not a decision against it.
Until it is done, four AI-generated before/after images carry no disclosure at all — one on
/pages/pdrn-research and three on /pages/acetyl-hexapeptide-8-research.

When it is picked up: append a line to each finding block's `content`, below the citation, where
the theme already renders italic footnote text and where Translate & Adapt can reach it. Do it
idempotently so a re-run cannot stack duplicates.

Only section JSON is touched, never Liquid — .claude/rules/shopify.md rule 2.

Author: Claude Code, 2026-08-27.
"""
import argparse
import json
import urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "2025-01"
TEMPLATES = ["templates/page.pdrn-research.json", "templates/page.research-argireline.json"]


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
    print(f"Live theme : {theme['name']} (id {theme['id']})\n")
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    for key in TEMPLATES:
        asset = call(store, tok, f"themes/{theme['id']}/assets.json?asset[key]={key}")["asset"]
        tpl = json.loads(asset["value"])

        cleared = []
        for sname, section in tpl.get("sections", {}).items():
            if section.get("type") != "research-before-after":
                continue
            for bname, block in (section.get("blocks") or {}).items():
                st = block.get("settings", {})
                if st.get("note_label"):
                    cleared.append(f"{sname}.{bname} — was '{st['note_label']}'")
                    st["note_label"] = ""

        short = key.split("/")[-1]
        if not cleared:
            print(f"{short}: nothing to clear")
            continue

        backup = ROOT / "backups" / f"{short.replace('.json','')}-{stamp}.json"
        backup.write_text(json.dumps(json.loads(asset["value"]), indent=2))
        print(f"{short}: clearing {len(cleared)}")
        for c in cleared:
            print(f"    {c}")
        print(f"    backup {backup.relative_to(ROOT)}")
        print(f"    undo   python3 scripts/patch-template.py --restore "
              f"{backup.relative_to(ROOT)} --template {key}")

        if args.dry_run:
            print("    DRY RUN — not pushed\n")
            continue
        call(store, tok, f"themes/{theme['id']}/assets.json", "PUT",
             {"asset": {"key": key, "value": json.dumps(tpl, indent=2)}})
        print("    PUSHED\n")


if __name__ == "__main__":
    main()
