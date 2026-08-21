#!/usr/bin/env python3
"""Inventory every image slot in the live Skingenetix theme.

Reads the published theme's settings_data.json plus every template/*.json and
section/*.json, and reports which sections carry an image setting, whether it is
filled, and what the section is. This is the evidence base for deciding which
banners and key visuals the store actually needs — as opposed to which ones a
theme demo happens to ship with.

Writes docs/theme-image-audit.json and prints a readable summary.

Author: Claude Code, 2026-08-21.
"""
import json
import os
import re
import sys
import time
import urllib.request
from pathlib import Path

API = "2025-01"
ROOT = Path(__file__).resolve().parent.parent


def load_env():
    env = {}
    for line in (ROOT / ".env").read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    return env


def token(store, cid, sec):
    body = json.dumps({"client_id": cid, "client_secret": sec,
                       "grant_type": "client_credentials"}).encode()
    req = urllib.request.Request(f"https://{store}/admin/oauth/access_token", data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())["access_token"]


CACHE = Path("/private/tmp/claude-501/skingenetix-theme-cache")


def rest(store, tok, path, cache=False):
    """GET with a 429 backoff. The asset endpoint is 2 req/s and one file per
    call, so a full theme walk WILL trip the bucket without this."""
    if cache:
        CACHE.mkdir(parents=True, exist_ok=True)
        cf = CACHE / (re.sub(r"[^A-Za-z0-9]+", "_", path)[:180] + ".json")
        if cf.exists():
            return json.loads(cf.read_text())

    for attempt in range(8):
        req = urllib.request.Request(f"https://{store}/admin/api/{API}/{path}",
                                     headers={"X-Shopify-Access-Token": tok})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                data = json.loads(r.read())
            break
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
            wait = 2 ** attempt
            print(f"    429 — backing off {wait}s", file=sys.stderr)
            time.sleep(wait)
    else:
        raise RuntimeError(f"gave up on {path} after repeated 429s")

    time.sleep(0.6)  # stay under the 2 req/s leaky bucket
    if cache:
        cf.write_text(json.dumps(data))
    return data


def main():
    env = load_env()
    store = env["SHOPIFY_SKINGENETIX_STORE"]
    tok = token(store, env["SHOPIFY_SKINGENETIX_CLIENT_ID"],
                env["SHOPIFY_SKINGENETIX_CLIENT_SECRET"])

    themes = rest(store, tok, "themes.json")["themes"]
    live = next(t for t in themes if t["role"] == "main")
    print(f"Store        : {store}")
    print(f"Live theme   : {live['name']} (id {live['id']}, {live['theme_store_id']})")
    print()

    assets = rest(store, tok, f"themes/{live['id']}/assets.json")["assets"]
    keys = [a["key"] for a in assets]

    wanted = [k for k in keys
              if k.startswith("templates/") and k.endswith(".json")
              or k == "config/settings_data.json"
              or k.startswith("sections/") and k.endswith(".json")]

    out = {"store": store, "theme": live["name"], "theme_id": live["id"],
           "all_asset_keys": keys, "files": {}}

    for key in sorted(wanted):
        data = rest(store, tok, f"themes/{live['id']}/assets.json?asset[key]={key}", cache=True)
        body = data["asset"].get("value")
        if body is None:
            continue
        try:
            out["files"][key] = json.loads(body)
        except json.JSONDecodeError:
            out["files"][key] = {"_raw_unparsed": body[:2000]}

    (ROOT / "docs" / "theme-image-audit.json").write_text(json.dumps(out, indent=2))

    # ---- readable summary: every image-bearing setting in every section ----
    IMG_HINT = re.compile(r"image|banner|background|logo|favicon|video|media|photo",
                          re.I)

    print("=" * 78)
    print("IMAGE-BEARING SETTINGS, BY FILE AND SECTION")
    print("=" * 78)
    for key, doc in out["files"].items():
        if not isinstance(doc, dict):
            continue
        rows = []

        def walk(node, path):
            if isinstance(node, dict):
                for k, v in node.items():
                    if IMG_HINT.search(str(k)) and not isinstance(v, (dict, list)):
                        rows.append((path, k, v))
                    else:
                        walk(v, f"{path}.{k}" if path else k)
            elif isinstance(node, list):
                for i, v in enumerate(node):
                    walk(v, f"{path}[{i}]")

        walk(doc, "")
        if not rows:
            continue
        print(f"\n--- {key} ---")
        for path, k, v in rows:
            filled = "FILLED " if v not in ("", None, False) else "EMPTY  "
            sec = path.split(".sections.")[-1].split(".")[0] if ".sections." in path else path
            print(f"  {filled} {sec:<34} {k:<26} {str(v)[:60]}")

    # ---- what sections each template actually renders, in order ----
    print()
    print("=" * 78)
    print("SECTION ORDER PER TEMPLATE (what a visitor scrolls past)")
    print("=" * 78)
    for key, doc in out["files"].items():
        if not (isinstance(doc, dict) and "sections" in doc):
            continue
        order = doc.get("order") or list(doc["sections"].keys())
        print(f"\n--- {key} ---")
        for i, sid in enumerate(order, 1):
            s = doc["sections"].get(sid, {})
            print(f"  {i:>2}. {sid:<28} type={s.get('type','?')}")

    print(f"\nWrote docs/theme-image-audit.json")


if __name__ == "__main__":
    main()
