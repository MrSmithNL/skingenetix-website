#!/usr/bin/env python3
"""Convert the FAQ block on every research page to the homepage's FAQ section.

    python3 scripts/research-faq-to-homepage-layout.py --dry-run
    python3 scripts/research-faq-to-homepage-layout.py

Malcolm, 2026-08-27: use the same FAQ content block set-up as the homepage, with the
title centred above.

ORIENTATION — CHECKED AGAINST THE LIVE HOMEPAGE, NOT AGAINST THE REQUEST. He described it
as "image left, faq's right", but the homepage renders the OPPOSITE: measured live, the
accordion sits at x=109 w=618 and the image at x=767 w=564, so the FAQs are on the LEFT
and the image on the RIGHT, under `text_position: "end"`. Asked, and he chose to match the
homepage exactly. So `text_position` is "end" here — if a later session reads his original
wording and "fixes" it to "start", that would be the regression, not the fix.

THE BLOCKS ARE ALREADY COMPATIBLE. Both `accordion-content` and `faq` take `item` blocks
with exactly `title` and `content`, so every question carries over verbatim and untouched.
Only the section type and its settings change; no question text is rewritten, retyped or
re-ordered.

⚠️ THE IMAGE IS A PLACEHOLDER. Malcolm: "use an existing image as placeholder for now. i
will select the images and tell you what ones to use per page." Every page therefore gets
the homepage's own FAQ photograph, which is deliberately the same on all five so it is
obvious at a glance that it has not been chosen yet. Each page has its own on-brand
candidates already uploaded — see the per-page notes in PAGES below — but the choice is
his to make.

One thing added that was not asked for, flagged rather than smuggled: a one-line
`content` under the heading, because the homepage set-up has one and the block looks
unfinished without it. Say the word and it comes out.

Author: Claude Code, 2026-08-27.
"""
import argparse
import json
import urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "2025-01"

#: Deliberately identical across all five, so an unchosen image is obvious.
PLACEHOLDER = "shopify://shop_images/skingenetix-faq-cream-jar-stack-2026-v3.jpg"

PAGES = {
    "templates/page.pdrn-research.json": {
        "content": "<p>Everything you need to know about PDRN and polynucleotides.</p>",
        # candidate when Malcolm chooses: skingenetix-pdrn-skin-renewal-cream-applying-to-cheekbone.jpg
    },
    "templates/page.research-argireline.json": {
        "content": "<p>Everything you need to know about Acetyl Hexapeptide-8.</p>",
        # candidate: skingenetix-acetyl-hexapeptide-8-peptide-refraction-research-banner.jpg
    },
    "templates/page.research-copper-peptide.json": {
        "content": "<p>Everything you need to know about Copper Peptide GHK-Cu.</p>",
        # candidate: skingenetix-copper-peptide-ghk-cu-radiant-skin-appearance.jpg
    },
    "templates/page.research-matrixyl.json": {
        "content": "<p>Everything you need to know about Matrixyl 3000.</p>",
        # candidate: skingenetix-matrixyl-3000-peptide-collagen-network-supports-skin-surface.jpg
    },
    "templates/page.glutathione-research.json": {
        "content": "<p>Everything you need to know about topical glutathione.</p>",
        # candidate: page carries no ingredient imagery of its own yet
    },
}

#: Copied from the live homepage `faq_section` so the two read as one system.
HOMEPAGE_DEFAULTS = {
    "full_width": False,
    "subheading": "",
    "team_avatar_width": 350,
    "support_hours": "Our customer support is available Monday to Friday: 8am-8:30pm.",
    "answer_time": "Average answer time: 24h",
    "button_text": "",
    "button_url": "",
    "text_position": "end",          # FAQs left, image right — see the note above
    "background": "",
    "background_gradient": "",
    "text_color": "",
    "heading_color": "",
    "heading_gradient": "",
    "button_background": "",
    "button_text_color": "",
    "accordion_background": "",
    "accordion_text_color": "",
}


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

    for key, cfg in PAGES.items():
        short = key.split("/")[-1]
        asset = call(store, tok, f"themes/{theme['id']}/assets.json?asset[key]={key}")["asset"]
        tpl = json.loads(asset["value"])
        sec = tpl.get("sections", {}).get("faq")
        if not sec:
            print(f"{short}: no `faq` section — skipped")
            continue
        if sec.get("type") == "faq":
            print(f"{short}: already converted — skipped")
            continue

        blocks = sec.get("blocks") or {}
        kinds = {b.get("type") for b in blocks.values()}
        if kinds != {"item"}:
            print(f"{short}: block types {kinds} are not all `item` — SKIPPED, "
                  f"converting would drop content")
            continue

        old_type = sec.get("type")
        old_title = sec.get("settings", {}).get("title") or "Frequently Asked Questions"

        settings = dict(HOMEPAGE_DEFAULTS)
        settings["title"] = old_title          # keep each page's own heading verbatim
        settings["content"] = cfg["content"]
        settings["team_avatar"] = PLACEHOLDER
        sec["type"] = "faq"
        sec["settings"] = settings
        # blocks and block_order are left exactly as they are

        backup = ROOT / "backups" / f"{short.replace('.json','')}-faq-{stamp}.json"
        backup.write_text(asset["value"])
        print(f"{short}: {old_type} -> faq, {len(blocks)} questions kept, title '{old_title}'")
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
