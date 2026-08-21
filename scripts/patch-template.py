#!/usr/bin/env python3
"""Apply a plan of image assignments and new sections to a live theme template.

    python3 scripts/patch-template.py configs/banners/homepage-publish-2.json --dry-run
    python3 scripts/patch-template.py configs/banners/homepage-publish-2.json
    python3 scripts/patch-template.py --restore backups/index-<stamp>.json

The generic successor to patch-homepage.py, which hard-coded the hero. A plan here
declares `image_assignments` (section, block, slot) and optional `new_sections` with
an `insert_after`, so the same script serves the remaining pages.

Backs up the template before every push and prints its own restore command. Only
section JSON is touched, never Liquid — .claude/rules/shopify.md rule 2.

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
            if ex.code != 429:
                raise
            time.sleep(2 ** attempt)
    raise RuntimeError(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plan", nargs="?")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--restore")
    ap.add_argument("--template", default="templates/index.json")
    args = ap.parse_args()

    e = env()
    store = e["SHOPIFY_SKINGENETIX_STORE"]
    tok = token(e)
    theme = next(t for t in call(store, tok, "themes.json")["themes"] if t["role"] == "main")
    print(f"Store      : {store}")
    print(f"Live theme : {theme['name']} (id {theme['id']})\n")

    tid = theme["id"]

    if args.restore:
        body = (ROOT / args.restore).read_text()
        key = json.loads(body) and args.template
        call(store, tok, f"themes/{tid}/assets.json", "PUT",
             {"asset": {"key": key, "value": body}})
        print(f"RESTORED {key} from {args.restore}")
        return

    plan = json.loads((ROOT / args.plan).read_text())
    by_slot = {i["slot"]: i for i in plan["images"]}
    missing = [s for s, i in by_slot.items() if not i.get("uploaded_handle")]
    if missing:
        sys.exit(f"no uploaded handle yet for: {missing} — run upload-theme-images.py first")

    tpl = args.template
    current = call(store, tok, f"themes/{tid}/assets.json?asset[key]={tpl}")["asset"]["value"]
    doc = json.loads(current)

    BACKUPS.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = BACKUPS / f"{Path(tpl).stem}-{stamp}.json"
    backup.write_text(current)
    print(f"Backup     : {backup.relative_to(ROOT)}")
    print(f"Undo with  : python3 scripts/patch-template.py --restore {backup.relative_to(ROOT)} "
          f"--template {tpl}\n")

    if plan.get("setting_updates"):
        print("\nSetting updates:")
    for u in plan.get("setting_updates", []):
        sec = doc["sections"].get(u["section"])
        if not sec:
            sys.exit(f"section not found: {u['section']}")
        # A slide's own settings live on its block, not the section.
        target = sec
        label = u["section"]
        if u.get("block"):
            target = sec.get("blocks", {}).get(u["block"])
            if not target:
                sys.exit(f"block not found: {u['section']}.{u['block']}")
            label = f"{u['section']}.{u['block']}"
        target.setdefault("settings", {}).update(u["settings"])
        for k, v in u["settings"].items():
            shown = v if not isinstance(v, list) else f"[{len(v)} rule(s)]"
            print(f"  {label}.{k} = {str(shown)[:90]}")

    order = doc.get("order") or list(doc["sections"].keys())

    for sid in plan.get("remove_sections", []):
        if sid in doc["sections"]:
            del doc["sections"][sid]
            if sid in order:
                order.remove(sid)
            print(f"\nRemoved section: {sid}")
        else:
            print(f"\n  section {sid} not present — nothing to remove")

    for ns in plan.get("new_sections", []):
        sid = ns["id"]
        if sid in doc["sections"]:
            print(f"\n  section {sid} already exists — updating in place")
        section = json.loads(json.dumps(ns["section"]))
        # Not every inserted section carries an image — a custom-html style block
        # does not — so image_slot is optional.
        if ns.get("image_slot"):
            section["settings"]["image"] = by_slot[ns["image_slot"]]["uploaded_handle"]
        doc["sections"][sid] = section
        if sid in order:
            order.remove(sid)
        anchor = ns.get("insert_after")
        idx = order.index(anchor) + 1 if anchor in order else len(order)
        order.insert(idx, sid)
        print(f"\nNew section:")
        print(f"  {sid}  ({section['type']}) inserted after {anchor}")
        if ns.get("image_slot"):
            print(f"    image   : {by_slot[ns['image_slot']]['filename']}")
        for bid in section.get("block_order", []):
            bs = section["blocks"][bid]["settings"]
            txt = bs.get("text") or bs.get("content") or ""
            print(f"    {bid:<14}: {str(txt)[:80]}")

    for nb in plan.get("new_blocks", []):
        sec = doc["sections"].get(nb["section"])
        if not sec:
            sys.exit(f"section not found: {nb['section']}")
        bid = nb["id"]
        block = json.loads(json.dumps(nb["block"]))
        # Inherit any key the sibling block sets that this one does not, so a new
        # slide cannot silently miss a default the existing slides depend on.
        if nb.get("inherit_from"):
            src = sec["blocks"].get(nb["inherit_from"], {}).get("settings", {})
            for k, v in src.items():
                block.setdefault("settings", {}).setdefault(k, v)
        if nb.get("image_slot"):
            block["settings"]["image"] = by_slot[nb["image_slot"]]["uploaded_handle"]
        sec.setdefault("blocks", {})[bid] = block
        order_key = "block_order"
        border = sec.get(order_key) or list(sec["blocks"].keys())
        if bid in border:
            border.remove(bid)
        after = nb.get("insert_after")
        idx = border.index(after) + 1 if after in border else len(border)
        border.insert(idx, bid)
        sec[order_key] = border
        print(f"\nNew block: {nb['section']}.{bid} ({block.get('type')}) after {after}")
        for k in ("title", "subheading", "button_text"):
            if block["settings"].get(k):
                print(f"    {k:<12}: {str(block['settings'][k])[:70]}")
        print(f"    block_order : {' -> '.join(border)}")

    print("Image assignments:")
    for a in plan.get("image_assignments", []):
        sec = doc["sections"].get(a["section"])
        if not sec:
            sys.exit(f"section not found: {a['section']}")
        handle = by_slot[a["slot"]]["uploaded_handle"]
        # Mega-menu blocks hold several images per block under image_1, image_2 ...
        # so the target key is not always "image".
        key = a.get("setting", "image")
        if a.get("block"):
            blk = sec.get("blocks", {}).get(a["block"])
            if not blk:
                sys.exit(f"block not found: {a['section']}.{a['block']}")
            blk["settings"][key] = handle
            print(f"  {a['section']}.{a['block']}.{key} -> {by_slot[a['slot']]['filename']}")
        else:
            sec["settings"][key] = handle
            print(f"  {a['section']}.{key:<20} -> {by_slot[a['slot']]['filename']}")

    doc["order"] = order
    new = json.dumps(doc, indent=2)

    print(f"\nSection order now: {' -> '.join(order)}")

    if args.dry_run:
        out = BACKUPS / f"{Path(tpl).stem}-PROPOSED-{stamp}.json"
        out.write_text(new)
        print(f"\nDRY RUN — proposed template at {out.relative_to(ROOT)}, nothing pushed")
        return

    call(store, tok, f"themes/{tid}/assets.json", "PUT",
         {"asset": {"key": tpl, "value": new}})
    print("\nPUSHED to the live theme.")


if __name__ == "__main__":
    main()
