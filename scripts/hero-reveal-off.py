#!/usr/bin/env python3
"""Show a template's hero banner at once instead of fading it in: one line in the hero section's own Custom CSS.

Author: Claude (Opus 5.5) for Malcolm Smith · 2026-10-09
Why: Impact sets `[reveal-on-scroll=true]{opacity:0}` and the hero's <image-banner> fades in only after theme.js has
loaded and the full image has downloaded, so Google times the largest paint from the fade. On /pages/collagen-skincare
the rule below took the live mobile LCP from about 14 s to 4.0-4.4 s; every other section keeps its animation and no
theme setting moves (ADR-2026-10-08-X). Malcolm, 2026-10-09: "proceed with all next steps and improvements" (the
per-page roll-out of that rule).

The rule is `image-banner{opacity:1!important}` in the hero section's `custom_css` (a sibling of `settings`); Shopify
scopes Custom CSS to its section, so nothing outside the hero changes. Custom CSS caps at 500 characters per section.

    python3 scripts/hero-reveal-off.py --all                    # dry run over every live hero template
    python3 scripts/hero-reveal-off.py --all --apply
    python3 scripts/hero-reveal-off.py templates/page.faq.json --apply
    python3 scripts/hero-reveal-off.py --all --undo --apply     # take the rule out again

Backs up each template to backups/hero-reveal-off-<template>-<stamp>.json before writing (hub-upgrade.py's
read_file/split/upload helpers; theme 184835965313).
"""
import argparse, datetime as dt, importlib.util, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
RULE = "image-banner{opacity:1!important}"
HERO_TYPES = ("image-with-text-overlay",)
# Every template whose page is live (or about to go live) with a fading hero, 2026-10-09. Not index.json: its hero is a
# slideshow, a different element, tested separately.
ALL = [
    "templates/page.brightening-glow.json", "templates/page.contact.json", "templates/page.faq.json",
    "templates/page.fine-lines-wrinkles.json", "templates/page.firming-skin-density.json",
    "templates/page.glutathione-research.json", "templates/page.ingredients.json", "templates/page.pdrn-research.json",
    "templates/page.philosophy.json", "templates/page.research-argireline.json",
    "templates/page.research-copper-peptide.json", "templates/page.research-matrixyl.json",
    "templates/page.science.json", "templates/page.shipping-returns.json", "templates/page.skin-concerns.json",
    "templates/page.skin-repair-renewal.json", "templates/page.collagen-skincare.json",
    "templates/page.matrixyl-preview.json", "templates/article.clinical-study.json",
    "templates/article.clinical-study-pilot.json", "templates/article.clinical-study-draft.json",
    "templates/blog.clinical-studies.json", "templates/blog.clinical-studies-preview.json",
    "templates/metaobject/study.json",
]


def _load(name, path):
    s = importlib.util.spec_from_file_location(name, ROOT / path)
    m = importlib.util.module_from_spec(s)
    argv, sys.argv = sys.argv, [sys.argv[0]]
    s.loader.exec_module(m)
    sys.argv = argv
    return m


hu = _load("hu", "scripts/hub-upgrade.py")


def hero_id(j):
    """The first enabled image-with-text-overlay among the first three rendered sections."""
    live = [k for k in j.get("order", []) if not j["sections"][k].get("disabled")]
    return next((k for k in live[:3] if j["sections"][k]["type"] in HERO_TYPES), None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("templates", nargs="*")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--undo", action="store_true")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    names = ALL if a.all else a.templates
    if not names:
        ap.error("name templates or pass --all")
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    changed = 0
    for name in names:
        raw = hu.read_file(name)
        hdr, j = hu.split(raw)
        hid = hero_id(j)
        if not hid:
            print(f"  - {name}: no image-with-text-overlay hero, skipped")
            continue
        css = list(j["sections"][hid].get("custom_css", []))
        has = RULE in css
        if has != a.undo:
            print(f"  = {name} [{hid}]: already {'without' if a.undo else 'with'} the rule")
            continue
        css = [c for c in css if c != RULE] if a.undo else css + [RULE]
        if sum(len(c) for c in css) > 500:
            print(f"  ✗ {name} [{hid}]: Custom CSS would pass 500 characters, skipped")
            continue
        print(f"  {'-' if a.undo else '+'} {name} [{hid}]: {len(css)} rule(s), {sum(len(c) for c in css)} chars")
        if a.apply:
            (ROOT / "backups" / f"hero-reveal-off-{name.split('/')[-1]}-{stamp}.json").write_text(raw)
            j["sections"][hid]["custom_css"] = css
            hu.upload(name, hdr, j)
        changed += 1
    print(f"  {changed} template(s) {'written' if a.apply else 'would change; dry run, add --apply'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
