#!/usr/bin/env python3
"""Enable or disable a named section across every theme template that holds it.

    python3 scripts/toggle-section.py featured_in --disable --dry-run
    python3 scripts/toggle-section.py featured_in --disable
    python3 scripts/toggle-section.py featured_in --enable

Sets `"disabled": true` on the section, which is exactly what the theme editor's
"hide section" control writes. Nothing is deleted: every block, image and setting
stays in the template, so --enable puts the section back untouched. That is the
whole reason this exists rather than a `remove_sections` plan.

`disabled` is a TOP-LEVEL key of a section, a sibling of `settings` — NOT a member
of it. patch-template.py's `setting_updates` writes into `settings`, so routing a
`disabled` flag through it succeeds, prints as applied, and does nothing. Same trap
as `custom_css`; see memory/custom-css-is-a-sibling-of-settings-not-a-member.md.

Backs up every template it touches before writing and prints one restore command per
file, matching patch-template.py's convention.

Author: Claude Code, 2026-08-27.
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


def call(store, tok, path, method="GET", payload=None):
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
            if ex.code == 429:
                time.sleep(2 ** attempt)
                continue
            # patch-template.py swallows this body and the real reason with it.
            sys.exit(f"HTTP {ex.code} on {path}\n{ex.read().decode()}")
    raise RuntimeError(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("section_id", help="section key, e.g. featured_in")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--disable", action="store_true")
    g.add_argument("--enable", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    want_disabled = bool(args.disable)

    e = env()
    store = e["SHOPIFY_SKINGENETIX_STORE"]
    tok = token(e)
    theme = next(t for t in call(store, tok, "themes.json")["themes"] if t["role"] == "main")
    tid = theme["id"]
    print(f"Store      : {store}")
    print(f"Live theme : {theme['name']} (id {tid})")
    print(f"Section    : {args.section_id} -> disabled={want_disabled}\n")

    assets = call(store, tok, f"themes/{tid}/assets.json")["assets"]
    keys = sorted(a["key"] for a in assets
                  if a["key"].startswith(("templates/", "sections/")) and a["key"].endswith(".json"))

    BACKUPS.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    touched, skipped = [], []

    for key in keys:
        raw = call(store, tok, f"themes/{tid}/assets.json?asset[key]={key}")["asset"]["value"]
        try:
            doc = json.loads(raw)
        except json.JSONDecodeError:
            continue
        sec = (doc.get("sections") or {}).get(args.section_id)
        if sec is None:
            continue
        if bool(sec.get("disabled")) == want_disabled:
            skipped.append(key)
            print(f"  {key}  already disabled={want_disabled} — untouched")
            continue

        if want_disabled:
            sec["disabled"] = True
        else:
            sec.pop("disabled", None)

        backup = BACKUPS / f"{Path(key).stem}-{stamp}.json"
        backup.write_text(raw)
        body = json.dumps(doc, indent=2)
        if args.dry_run:
            print(f"  {key}  WOULD SET disabled={want_disabled}   (backup {backup.name})")
        else:
            call(store, tok, f"themes/{tid}/assets.json", "PUT",
                 {"asset": {"key": key, "value": body}})
            print(f"  {key}  disabled={want_disabled}")
            print(f"       undo: python3 scripts/toggle-section.py {args.section_id} "
                  f"{'--enable' if want_disabled else '--disable'}")
            print(f"       or  : python3 scripts/patch-template.py --restore "
                  f"backups/{backup.name} --template {key}")
        touched.append(key)

    verb = "would change" if args.dry_run else "changed"
    print(f"\n{verb} {len(touched)} template(s); {len(skipped)} already in the wanted state")
    if not touched and not skipped:
        sys.exit(f"section {args.section_id!r} not found in any template — nothing done")


if __name__ == "__main__":
    main()
