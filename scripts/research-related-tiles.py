#!/usr/bin/env python3
"""Make the 'Explore More Research' card images clickable, with the main menu's
hover treatment.

    python3 scripts/research-related-tiles.py --dry-run
    python3 scripts/research-related-tiles.py
    python3 scripts/research-related-tiles.py --remove

The stock multi-column section renders its image as a DIRECT CHILD of
`.multi-column__item` — only the "Read Research" text is a link — so CSS alone
cannot make the picture clickable. A small script in the sitewide
`brand_layout_css` block wraps each image in an anchor pointing at that card's own
link, and the CSS then gives the wrapper the menu-tile behaviour: the brand
overlay at rest, lifting to nothing on hover while the picture zooms 6%.

SCOPE — this is the part that matters. `brand_layout_css` renders on every page,
and this store has 18 multi-column sections. Scoping by a block count has broken
five pages here before, and scoping by the heading text would break the day a
second locale publishes. So the test is structural and content-based, and neither:

  a section whose id ends `__related`   (the section key, stable across themes;
                                         the numeric middle of a Shopify section
                                         id is what goes stale, not the suffix)
  AND whose card links point at a *-research page

Checked against all 48 templates. That matches exactly the 5 research pages'
`related` sections and nothing else:

  - `Related Skin Solutions` on the 5 solution pages also uses the key `related`,
    but its cards link to /pages/<concern>, so it is excluded.
  - `Clinically Studied Actives` on /pages/the-science does link to research
    pages, but its key is `ingredients_overview`, so it is excluded. It is the
    same kind of card and could be included later by adding its key here.

Author: Claude Code, 2026-08-30.
"""
import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "2025-01"
BACKUPS = ROOT / "backups"
FOOTER_KEY = "sections/footer-group.json"
MARK_START = "/* === SGX RESEARCH RELATED TILES START === */"
MARK_END = "/* === SGX RESEARCH RELATED TILES END === */"

BLOCK = MARK_START + """
<style>
/* 'Explore More Research' cards — Claude Code, 2026-08-30.
   Same resting/hover behaviour as the main-menu image tiles: the brand overlay
   (#1a1a1a at 22%, the value the collection banners and the science hero use)
   sits over the picture at rest and lifts to nothing on hover, while the picture
   zooms 6% over 1.5s on the theme's own .zoom-image easing.

   Unlike the menu tiles there is no bottom scrim: the card's title and text sit
   BELOW the picture rather than over it, so nothing needs local contrast. */
a.sgx-research-tile {
  display: block;
  position: relative;
  isolation: isolate;
  overflow: hidden;
  border-radius: 6px;
  line-height: 0;
}
a.sgx-research-tile::after {
  content: "";
  position: absolute;
  inset: 0;
  z-index: 1;
  pointer-events: none;
  background: rgba(26, 26, 26, .22);
  transition: background .35s ease-in-out;
}
a.sgx-research-tile:hover::after,
a.sgx-research-tile:focus-visible::after {
  background: rgba(26, 26, 26, 0);
}
a.sgx-research-tile > img {
  display: block;
  width: 100%;
  transition: transform 1.5s cubic-bezier(.22, 1, .36, 1);
}
a.sgx-research-tile:hover > img,
a.sgx-research-tile:focus-visible > img {
  transform: scale(1.06);
}
/* Keyboard users get a visible ring; the anchor is otherwise silent. */
a.sgx-research-tile:focus-visible {
  outline: 2px solid rgb(var(--text-color, 26 26 26));
  outline-offset: 3px;
}
</style>
<script>
(function () {
  // See the scope note in scripts/research-related-tiles.py. Two conditions,
  // both structural: the section key is `related`, and the card links at a
  // research page. Never a block count, never the heading text.
  function wrap(root) {
    (root || document).querySelectorAll(
      '[id$="__related"].shopify-section--multi-column .multi-column__item'
    ).forEach(function (item) {
      if (item.querySelector('a.sgx-research-tile')) return;      // already done
      var img = item.querySelector(':scope > img');
      if (!img) return;
      var link = item.querySelector('a[href*="-research"]');
      if (!link) return;                                          // not a research card
      var a = document.createElement('a');
      a.className = 'sgx-research-tile';
      a.setAttribute('href', link.getAttribute('href'));
      // The heading already names the destination, so the picture is decorative
      // to a screen reader — announcing the same link twice is noise.
      a.setAttribute('tabindex', '-1');
      a.setAttribute('aria-hidden', 'true');
      img.parentNode.insertBefore(a, img);
      a.appendChild(img);
    });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { wrap(); });
  } else {
    wrap();
  }
  // Theme editor re-renders a section without reloading the page.
  document.addEventListener('shopify:section:load', function (e) { wrap(e.target); });
})();
</script>
""" + MARK_END


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
    r = urllib.request.Request(f"https://{store}/admin/api/{API}/{path}", data=data,
                               method=method,
                               headers={"X-Shopify-Access-Token": tok,
                                        "Content-Type": "application/json"})
    for a in range(6):
        try:
            with urllib.request.urlopen(r, timeout=90) as res:
                out = json.loads(res.read())
            time.sleep(0.5)
            return out
        except urllib.error.HTTPError as ex:
            if ex.code != 429:
                sys.stderr.write(ex.read().decode(errors="replace")[:1500] + "\n")
                raise
            time.sleep(2 ** a)
    raise RuntimeError(path)


def upsert(html, block):
    if MARK_START in html and MARK_END in html:
        head = html.split(MARK_START)[0]
        tail = html.split(MARK_END, 1)[1]
        return head + block + tail if block else (head.rstrip() + "\n" + tail.lstrip())
    if not block:
        return html
    return html.rstrip() + "\n" + block + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--remove", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    e = env()
    store = e["SHOPIFY_SKINGENETIX_STORE"]
    tok = token(e)
    theme = next(t for t in call(store, tok, "themes.json")["themes"] if t["role"] == "main")
    tid = theme["id"]
    print(f"Store      : {store}")
    print(f"Live theme : {theme['name']} (id {tid})\n")

    raw = call(store, tok, f"themes/{tid}/assets.json?asset[key]={FOOTER_KEY}")["asset"]["value"]
    BACKUPS.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = BACKUPS / f"footer-group-{stamp}.json"
    backup.write_text(raw)
    print(f"Backup     : {backup.relative_to(ROOT)}")
    print(f"Undo with  : python3 scripts/menu-image-tiles.py --restore "
          f"{backup.relative_to(ROOT)} --key {FOOTER_KEY}\n")

    doc = json.loads(raw)
    sec = doc["sections"].get("brand_layout_css")
    if not sec:
        sys.exit("footer-group.json has no brand_layout_css section")
    before = sec["settings"]["html"]
    sec["settings"]["html"] = upsert(before, "" if args.remove else BLOCK)
    print(("Removing" if args.remove else "Installing")
          + f" the research-tile block ({len(sec['settings']['html']) - len(before):+d} chars)")

    if "{{" in sec["settings"]["html"]:
        sys.exit("refusing to push: custom-html rejects '{{' in its html setting")

    new = json.dumps(doc, indent=2)
    if args.dry_run:
        out = BACKUPS / f"footer-group-PROPOSED-{stamp}.json"
        out.write_text(new)
        print(f"\nDRY RUN — proposal at {out.relative_to(ROOT)}, nothing pushed")
        return

    call(store, tok, f"themes/{tid}/assets.json", "PUT",
         {"asset": {"key": FOOTER_KEY, "value": new}})
    print(f"\nPUSHED {FOOTER_KEY}")


if __name__ == "__main__":
    main()
