#!/usr/bin/env python3
"""Switch one section block off (or on) in a live theme template, keeping its translations.

Author: Claude (Fable 5.1) for Malcolm Smith · 2026-10-08
Why: the Impact theme's `heading` block renders as <p class="h1">, so five pages served no <h1> (verified
2026-10-08). The title moved into the richtext block as a real <h1> through a set-only spec; the old heading
block must then stop rendering. Deleting it would drop its six translations (memory:
clearing-a-field-drops-its-translations), so it is disabled instead: Shopify's `"disabled": true` keeps the
block and its translations and simply does not render it. --enable reverses it.

    python3 scripts/disable-block.py templates/page.fine-lines-wrinkles.json hero heading            # dry run
    python3 scripts/disable-block.py templates/page.fine-lines-wrinkles.json hero heading --apply
    python3 scripts/disable-block.py templates/page.fine-lines-wrinkles.json hero heading --enable --apply

Backs up the template to backups/disable-block-<template>-<stamp>.json before writing (hub-upgrade.py's
read_file/upload helpers; theme 184835965313).
"""
import argparse, datetime as dt, importlib.util, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def _load(name, path):
    s = importlib.util.spec_from_file_location(name, ROOT / path)
    m = importlib.util.module_from_spec(s)
    argv, sys.argv = sys.argv, [sys.argv[0]]
    s.loader.exec_module(m)
    sys.argv = argv
    return m


hu = _load("hu", "scripts/hub-upgrade.py")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("template")
    ap.add_argument("section")
    ap.add_argument("block")
    ap.add_argument("--enable", action="store_true")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    raw = hu.read_file(a.template)
    head, body = raw[: raw.index("{")], raw[raw.index("{"):]
    d = json.loads(body)
    blk = d["sections"][a.section]["blocks"][a.block]
    state = "enabled" if a.enable else "disabled"
    print(f"  {a.template} {a.section}/{a.block} ({blk['type']}): currently {'disabled' if blk.get('disabled') else 'enabled'} -> {state}")
    if a.enable:
        blk.pop("disabled", None)
    else:
        blk["disabled"] = True
    if not a.apply:
        print("  dry run; add --apply")
        return 0
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    (ROOT / "backups" / f"disable-block-{a.template.split('/')[-1]}-{stamp}.json").write_text(raw)
    hu.upload(a.template, head, d)
    print(f"  ✓ written (backup disable-block-{a.template.split('/')[-1]}-{stamp}.json)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
