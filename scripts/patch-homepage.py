#!/usr/bin/env python3
"""Patch the live homepage template with the approved hero slides and concern tiles.

    python3 scripts/patch-homepage.py configs/banners/homepage-publish.json --dry-run
    python3 scripts/patch-homepage.py configs/banners/homepage-publish.json
    python3 scripts/patch-homepage.py --restore backups/index-<stamp>.json

This edits the PUBLISHED theme, so it always writes a timestamped copy of the current
templates/index.json to backups/ first and prints the exact restore command. Nothing
here touches Liquid — only the section JSON, which is what .claude/rules/shopify.md
rule 2 permits.

Setting keys and their allowed values were read from the theme's own slideshow schema
rather than assumed; `desktop_text_position` in particular only accepts the eight
`sm:place-self-*` strings the schema lists, and an invalid value silently breaks the
section in the editor.

Author: Claude Code, 2026-08-21.
"""
import argparse
import json
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "2025-01"
BACKUPS = ROOT / "backups"


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


def req(store, tok, path, method="GET", payload=None):
    data = json.dumps(payload).encode() if payload else None
    r = urllib.request.Request(f"https://{store}/admin/api/{API}/{path}", data=data, method=method,
                               headers={"X-Shopify-Access-Token": tok,
                                        "Content-Type": "application/json"})
    for attempt in range(6):
        try:
            with urllib.request.urlopen(r, timeout=90) as res:
                out = json.loads(res.read())
            time.sleep(0.6)
            return out
        except urllib.error.HTTPError as ex:
            if ex.code != 429:
                raise
            time.sleep(2 ** attempt)
    raise RuntimeError(f"gave up on {path}")


def live_theme(store, tok):
    return next(t for t in req(store, tok, "themes.json")["themes"] if t["role"] == "main")


def get_index(store, tok, tid):
    a = req(store, tok, f"themes/{tid}/assets.json?asset[key]=templates/index.json")
    return a["asset"]["value"]


def put_index(store, tok, tid, value):
    return req(store, tok, f"themes/{tid}/assets.json", "PUT",
               {"asset": {"key": "templates/index.json", "value": value}})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plan", nargs="?")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--restore", help="path to a backup file to push back")
    args = ap.parse_args()

    e = env()
    store = e["SHOPIFY_SKINGENETIX_STORE"]
    tok = token(e)
    theme = live_theme(store, tok)
    print(f"Store      : {store}")
    print(f"Live theme : {theme['name']} (id {theme['id']})\n")

    if args.restore:
        body = (ROOT / args.restore).read_text()
        put_index(store, tok, theme["id"], body)
        print(f"RESTORED templates/index.json from {args.restore}")
        return

    plan = json.loads((ROOT / args.plan).read_text())
    by_slot = {i["slot"]: i for i in plan["images"]}
    missing = [s for s, i in by_slot.items() if not i.get("uploaded_handle")]
    if missing:
        sys.exit(f"these slots have no uploaded handle yet: {missing}")

    current = get_index(store, tok, theme["id"])
    doc = json.loads(current)

    BACKUPS.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = BACKUPS / f"index-{stamp}.json"
    backup.write_text(current)
    print(f"Backup     : {backup.relative_to(ROOT)}")
    print(f"Undo with  : python3 scripts/patch-homepage.py --restore {backup.relative_to(ROOT)}\n")

    hero = doc["sections"]["hero"]
    copy = plan["hero_copy"]
    shared = copy["shared"]

    # --- hero: two slides -------------------------------------------------
    slide1 = hero["blocks"]["hero_slide_1"]
    slide1["settings"].update({
        "image": by_slot["hero_slide_1"]["uploaded_handle"],
        **copy["slide_1"], **shared,
    })

    slide2 = {"type": "image", "settings": {
        "image": by_slot["hero_slide_2"]["uploaded_handle"],
        **copy["slide_2"], **shared,
    }}
    # carry across any keys the theme wrote onto slide 1 that we did not set,
    # so slide 2 is not missing a default slide 1 relies on.
    for k, v in slide1["settings"].items():
        slide2["settings"].setdefault(k, v)
    slide2["settings"].update({"image": by_slot["hero_slide_2"]["uploaded_handle"],
                               **copy["slide_2"]})
    hero["blocks"]["hero_slide_2"] = slide2
    hero["block_order"] = ["hero_slide_1", "hero_slide_2"]
    hero["settings"].update(copy["section"])

    # --- concern tiles ----------------------------------------------------
    for bid, slot in (("c1", "concern_c1"), ("c2", "concern_c2"),
                      ("c3", "concern_c3"), ("c4", "concern_c4")):
        doc["sections"]["skin_concerns"]["blocks"][bid]["settings"]["image"] = \
            by_slot[slot]["uploaded_handle"]

    new = json.dumps(doc, indent=2)

    print("Changes:")
    print(f"  hero            : 1 slide -> 2 slides, autoplay {copy['section']['autoplay']}, "
          f"text {shared['desktop_text_position'].split()[-1]}")
    print(f"    slide 1       : \"{copy['slide_1']['title']}\"")
    print(f"    slide 2       : \"{copy['slide_2']['title']}\"")
    for bid, slot in (("c1", "concern_c1"), ("c2", "concern_c2"),
                      ("c3", "concern_c3"), ("c4", "concern_c4")):
        print(f"  skin_concerns {bid}: {by_slot[slot]['filename']}")

    if args.dry_run:
        out = ROOT / "backups" / f"index-PROPOSED-{stamp}.json"
        out.write_text(new)
        print(f"\nDRY RUN — proposed template written to {out.relative_to(ROOT)}, nothing pushed")
        return

    put_index(store, tok, theme["id"], new)
    print("\nPUSHED to the live theme.")


if __name__ == "__main__":
    main()
