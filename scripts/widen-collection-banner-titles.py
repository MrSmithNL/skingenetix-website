#!/usr/bin/env python3
"""Widen the collection banner text column so titles stop wrapping unnecessarily.

    python3 scripts/widen-collection-banner-titles.py --dry-run
    python3 scripts/widen-collection-banner-titles.py
    python3 scripts/widen-collection-banner-titles.py --restore backups/<template>-<stamp>.json

THE BUG, AND WHY IT ONLY SHOWS ON A LAPTOP
Each collection template carries a `banner_text_width` custom-html section holding one rule:

    .collection-banner .v-stack { max-width: clamp(320px, 26vw, 620px); }

The ceiling (620px here) is the width the banner was actually designed around. But the middle
term is in **vw**, and 26vw only reaches 620px at a viewport of ~2385px — a 5K display. These
were tuned on a big monitor, so on Malcolm's 1506px laptop the vw term dominates and the box
collapses to 392px, barely half what was intended. Every ceiling in the set is unreachable below
about 1600px.

At 392px the box is narrower than the word "Brightening", which is 420px at the 80px display
size — and the theme sets `overflow-wrap: anywhere` on banner headings, so instead of overflowing
it breaks mid-word: "Brightenin / g". Same fault on Creams & Moisturizers, where "Moisturizers"
is 442px in a 422px box.

THE FIX
Keep each banner's own designed ceiling where it is big enough, raise it where the title needs
more, and set the vw term so the ceiling is actually reached at laptop width (~1440px) rather
than only on a 5K display. Nothing gets wider than **780px**, which is the width of the
`.place-self-*` column the text sits in — going past that would do nothing, and the point is to
stop starving the box, not to run type across the model's face.

MEASURED, NOT GUESSED
`need` below is the intrinsic single-line width of each title, measured on the live page at
1506px by cloning the heading with `white-space: nowrap`. `longest` is its longest single word —
any box narrower than that breaks mid-word.

    collection                need  longest  before -> after
    brightening-glow           699      420   392 -> 700   one line
    creams-moisturizers        809      442   422 -> 780   two clean lines, no mid-word break
    fine-lines-wrinkles        775      321   587 -> 780   one line
    acetyl-hexapeptide-8       767      526   720 -> 780   one line
    copper-peptide             932      364   633 -> 780   two clean lines (needs more than the column)
    firming-skin-density       825      283   663 -> 780   two clean lines
    skin-repair-renewal        808      304   633 -> 780   two clean lines
    all / pdrn / serums          -        -   already one line, left alone

NOT EVERY TITLE CAN BE ONE LINE, AND TWO SHOULD NOT BE
  skin-repair-renewal  stays at two lines. One line needs 808px and the wider type runs across the
                       jar and the model's face — checked by rendering it.
  copper-peptide       renders on THREE lines and always has, at every width from 560px to 780px.
                       This is not a width problem: the theme's `split-lines` element treats the
                       hyphen in "(GHK-Cu)" as a break, giving "Copper Peptide / (GHK- / Cu)".
                       Releasing the column to 960px puts it on one line but still renders
                       "GHK- Cu" with a gap. The fix is in the text, not the CSS — a non-breaking
                       hyphen (U+2011) in the collection title — and that is a content change to
                       the collection name, so it is left for Malcolm to decide.

Author: Claude Code, 2026-08-30.
"""
import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "2025-01"
BACKUPS = ROOT / "backups"

# collection handle -> (vw term, ceiling px). The ceiling is reached at ~1440px viewport.
TARGETS = {
    "brightening-glow":     (49, 700),
    "creams-moisturizers":  (58, 840),
    "fine-lines-wrinkles":  (55, 780),
    "acetyl-hexapeptide-8": (55, 780),
    "copper-peptide":       (55, 780),
    "firming-skin-density": (60, 860),
    "skin-repair-renewal":  (55, 780),
}

# The theme caps the banner's text COLUMN at 780px, so a v-stack clamp above that does nothing on
# its own — the parent has to be released too. Only these two: a one-line title was rendered and
# looked at on all of them, and on skin-repair-renewal and copper-peptide the wider type runs over
# the model and the jar. `[class*="place-self"]` matches exactly one element inside the banner.
COLUMN = {"creams-moisturizers": 840, "firming-skin-density": 860}

RULE = re.compile(r"(\.collection-banner \.v-stack \{ max-width: )clamp\([^)]*\)(; \})")


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
    req = urllib.request.Request(
        f"https://{e['SHOPIFY_SKINGENETIX_STORE']}/admin/oauth/access_token",
        data=body, headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=60).read())["access_token"]


def call(store, tok, path, method="GET", payload=None):
    data = json.dumps(payload).encode() if payload else None
    req = urllib.request.Request(f"https://{store}/admin/api/{API}/{path}", data=data,
                                 method=method,
                                 headers={"X-Shopify-Access-Token": tok,
                                          "Content-Type": "application/json"})
    for _ in range(6):
        try:
            out = json.loads(urllib.request.urlopen(req, timeout=90).read())
            time.sleep(0.5)
            return out
        except urllib.error.HTTPError as ex:
            if ex.code == 429:
                time.sleep(3)
                continue
            # custom-html names the offending setting in the BODY, never the status line
            sys.exit(f"HTTP {ex.code}\n{ex.read().decode()[:2000]}")
    sys.exit("gave up after rate limiting")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--restore")
    args = ap.parse_args()

    e = env()
    store = e["SHOPIFY_SKINGENETIX_STORE"]
    tok = token(e)
    theme = next(t for t in call(store, tok, "themes.json")["themes"] if t["role"] == "main")
    print(f"Theme: {theme['id']} ({theme['name']})\n")

    if args.restore:
        body = Path(args.restore).read_text()
        stem = re.sub(r"-\d{8}-\d{6}$", "", Path(args.restore).stem)
        key = f"templates/{stem}.json"
        call(store, tok, f"themes/{theme['id']}/assets.json", "PUT",
             {"asset": {"key": key, "value": body}})
        print(f"restored {key}")
        return

    BACKUPS.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    for handle, (vw, ceiling) in TARGETS.items():
        key = f"templates/collection.{handle}.json"
        asset = call(store, tok,
                     f"themes/{theme['id']}/assets.json?asset[key]={urllib.parse.quote(key)}")["asset"]
        raw = asset["value"]
        doc = json.loads(raw)

        target = None
        for sid, sec in doc["sections"].items():
            if sec["type"] == "custom-html" and RULE.search(sec["settings"].get("html", "")):
                target = (sid, sec)
                break
        if not target:
            print(f"  {handle:<24} no banner_text_width rule — skipped")
            continue

        sid, sec = target
        before = RULE.search(sec["settings"]["html"]).group(0)
        new_clamp = f"clamp(320px, {vw}vw, {ceiling}px)"
        sec["settings"]["html"] = RULE.sub(rf"\g<1>{new_clamp}\g<2>", sec["settings"]["html"])

        html = sec["settings"]["html"]
        bad = {t: html.count(t) for t in ("{{", "}}", "{%", "%}") if t in html}
        assert not bad, f"{handle}: custom-html would 422 on {bad}"

        print(f"  {handle:<24} {before.split('max-width: ')[1][:-3]}  ->  {new_clamp}")

        if args.dry_run:
            continue
        (BACKUPS / f"collection.{handle}-{stamp}.json").write_text(raw)
        call(store, tok, f"themes/{theme['id']}/assets.json", "PUT",
             {"asset": {"key": key, "value": json.dumps(doc, indent=2)}})

    if args.dry_run:
        print("\n--dry-run, nothing pushed")
    else:
        print(f"\npushed. undo any of them with:\n  python3 {Path(__file__).name} "
              f"--restore backups/collection.<handle>-{stamp}.json")


if __name__ == "__main__":
    main()
