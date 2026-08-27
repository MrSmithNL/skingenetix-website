#!/usr/bin/env python3
"""Rebuild the 'Published References' block on every research page.

    python3 scripts/references-block-rebuild.py --parse-only     # show what was extracted
    python3 scripts/references-block-rebuild.py --dry-run
    python3 scripts/references-block-rebuild.py

Malcolm, 2026-08-27, having reviewed three designed options: use option C, with an ICON
instead of the numbers.

WHAT WAS WRONG WITH THE BLOCK, measured on the live pages rather than assumed:
  - it is an <ol>, but the theme strips the list marker, so an ORDERED LIST ARRIVES
    UNORDERED — the numbering it is attempting simply does not render
  - authors, title, journal and identifier are all 15px regular, so nothing leads
  - the raw DOI/PMID string is the boldest element in each entry and the least useful
    part to a reader; it also wraps badly on a phone
  - titles come out of <cite> italic, and a whole italic sentence reads slower upright
  - the heading is centred over left-aligned text, so the block has no single edge

Option C draws its own marker rather than relying on the stripped list style. Numbering
would only have earned its place if the page copy cited by number, which it does not —
an icon carries the same structural rhythm without implying a cross-reference that
isn't there. The glyph is a document, inline SVG, monochrome: it says 'published paper',
which is exactly what each row is.

CITATION DATA IS PARSED OUT OF THE LIVE MARKUP, NEVER RETYPED. Five pages and thirty-odd
references is more than enough for a transcription error, and a wrong DOI on a research
page is worse than an ugly one. Anything the parser cannot read is reported and the page
is skipped rather than half-rebuilt — run --parse-only first and read it.

No Liquid is touched — .claude/rules/shopify.md rule 2 — and the html carries no '{{',
'}}', '{%' or '%}', which `custom-html` rejects with a 422 whose real message is only in
the response body. Asserted before any request is made.

Author: Claude Code, 2026-08-27.
"""
import argparse
import html as html_mod
import json
import re
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "2025-01"

PAGES = [
    "templates/page.pdrn-research.json",
    "templates/page.research-argireline.json",
    "templates/page.research-copper-peptide.json",
    "templates/page.research-matrixyl.json",
    "templates/page.glutathione-research.json",
]

#: A document glyph — "this row is a published paper". Inline, monochrome, no braces.
ICON = (
    '<svg class="sgref__ico" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
    '<path d="M6 2.75h7.5L18.5 7.75V21.25H6z" fill="none" stroke="currentColor" '
    'stroke-width="1.6" stroke-linejoin="round"/>'
    '<path d="M13.25 2.75V8h5.25" fill="none" stroke="currentColor" stroke-width="1.6" '
    'stroke-linejoin="round"/>'
    '<path d="M8.75 12.5h6.5M8.75 15.75h6.5M8.75 19h4" stroke="currentColor" '
    'stroke-width="1.6" stroke-linecap="round"/>'
    "</svg>"
)

CSS = (
    "<style>"
    "/* Published References — rebuilt by Claude Code 2026-08-27. Scoped to .sgref so it "
    "cannot reach the rest of the page. The theme strips list markers, which is why the "
    "old <ol> rendered unnumbered; this draws its own marker instead. */"
    ".sgref{max-width:780px;margin:0 auto;padding:40px 20px;}"
    ".sgref__h{font-size:30px;font-weight:700;color:#1A1A1A;margin:0 0 26px;"
    "letter-spacing:-.01em;line-height:1.2;}"
    ".sgref__list{display:flex;flex-direction:column;}"
    ".sgref__r{display:grid;grid-template-columns:34px 1fr auto;gap:0 16px;"
    "align-items:start;padding:16px 0;border-bottom:1px solid #E4E4E4;}"
    ".sgref__r:first-child{border-top:1px solid #E4E4E4;}"
    ".sgref__ico{width:22px;height:22px;color:#1A1A1A;display:block;margin-top:1px;"
    "flex:none;}"
    ".sgref__ti{font-size:15px;font-weight:700;color:#1A1A1A;margin:0 0 3px;"
    "line-height:1.4;}"
    ".sgref__me{font-size:13px;color:#6E6E6E;margin:0;line-height:1.5;}"
    ".sgref__me em{font-style:italic;}"
    ".sgref__lk{font-size:12px;font-weight:700;color:#1A1A1A;text-decoration:none;"
    "white-space:nowrap;border-bottom:1px solid #E4E4E4;padding-bottom:2px;"
    "transition:border-color .15s ease;}"
    ".sgref__lk:hover,.sgref__lk:focus-visible{border-color:#1A1A1A;}"
    ".sgref__lk:focus-visible{outline:2px solid #1A1A1A;outline-offset:3px;}"
    "@media (max-width:600px){"
    ".sgref__r{grid-template-columns:26px 1fr;gap:0 12px;}"
    ".sgref__ico{width:18px;height:18px;}"
    ".sgref__lk{grid-column:2;margin-top:8px;}"
    ".sgref__h{font-size:24px;} "   # the space belongs BETWEEN the two braces, not after
    "}"
    "</style>"
)

# Ye R et al. (2026). <cite>Title</cite>. <em>Journal</em>. 8:224. DOI: <a href=...>id</a>
LI = re.compile(r"<li[^>]*>(.*?)</li>", re.S | re.I)
AUTH = re.compile(r"^\s*(.*?)\s*\((\d{4})\)\s*\.", re.S)
CITE = re.compile(r"<cite[^>]*>(.*?)</cite>", re.S | re.I)
JOUR = re.compile(r"<em[^>]*>(.*?)</em>", re.S | re.I)
LINK = re.compile(r"<a[^>]*href=[\"'](.*?)[\"'][^>]*>(.*?)</a>", re.S | re.I)
KIND = re.compile(r"(DOI|PMID|PMCID)\s*:\s*<a", re.I)
VOL = re.compile(r"</em>\s*\.\s*([^<.]*?\d[^<.]*?)\s*\.", re.S)


def strip_tags(s):
    return html_mod.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def parse(block_html):
    """Return (entries, problems)."""
    out, bad = [], []
    for raw in LI.findall(block_html):
        e = {}
        m = AUTH.search(strip_tags(re.sub(r"<cite.*", "", raw, flags=re.S | re.I)) or "")
        plain = strip_tags(raw)
        m = AUTH.search(plain)
        if m:
            e["authors"], e["year"] = m.group(1).strip(), m.group(2)
        c = CITE.search(raw)
        j = JOUR.search(raw)
        a = LINK.search(raw)
        e["title"] = strip_tags(c.group(1)) if c else ""
        e["journal"] = strip_tags(j.group(1)) if j else ""
        e["url"] = a.group(1) if a else ""
        e["id"] = strip_tags(a.group(2)) if a else ""
        k = KIND.search(raw)
        e["kind"] = k.group(1).upper() if k else ""
        v = VOL.search(raw)
        e["vol"] = v.group(1).strip() if v else ""
        missing = [f for f in ("authors", "year", "title", "journal", "url") if not e.get(f)]
        if missing:
            bad.append((plain[:90], missing))
        else:
            out.append(e)
    return out, bad


def link_text(e):
    """Name the destination, never the raw identifier.

    Only PubMed and PMC get named, because they ARE the destination. A doi.org link
    resolves to whichever publisher holds the paper, so naming the journal produced
    'View on Cosmetics' — a real journal name that reads as a category. 'View study'
    is honest for every one of them.
    """
    u = e["url"].lower()
    if "pubmed" in u:
        return "View on PubMed"
    if "pmc.ncbi" in u or "/pmc/" in u:
        return "View on PMC"
    return "View study"


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def build(entries, heading="Published References"):
    rows = []
    for e in entries:
        meta = f"{esc(e['authors'])}, {e['year']} &middot; <em>{esc(e['journal'])}</em>"
        if e["vol"]:
            meta += f" &middot; {esc(e['vol'])}"
        rows.append(
            '<div class="sgref__r">'
            f"{ICON}"
            "<div>"
            f'<p class="sgref__ti">{esc(e["title"])}</p>'
            f'<p class="sgref__me">{meta}</p>'
            "</div>"
            f'<a class="sgref__lk" href="{esc(e["url"])}" target="_blank" '
            f'rel="noopener">{link_text(e)} &rarr;</a>'
            "</div>"
        )
    return (CSS + '<div class="sgref">'
            f'<h2 class="sgref__h">{esc(heading)}</h2>'
            '<div class="sgref__list">' + "".join(rows) + "</div></div>")


for _bad in ("{{", "}}", "{%", "%}"):
    assert _bad not in CSS and _bad not in ICON, f"custom-html will 422 on {_bad!r}"


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
    ap.add_argument("--parse-only", action="store_true")
    args = ap.parse_args()

    e = env()
    store = e["SHOPIFY_SKINGENETIX_STORE"]
    tok = token(e)
    theme = [t for t in call(store, tok, "themes.json")["themes"] if t["role"] == "main"][0]
    print(f"Live theme : {theme['name']} (id {theme['id']})\n")
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    failed = False

    for key in PAGES:
        short = key.split("/")[-1]
        asset = call(store, tok, f"themes/{theme['id']}/assets.json?asset[key]={key}")["asset"]
        tpl = json.loads(asset["value"])
        sec = tpl.get("sections", {}).get("references")
        if not sec or sec.get("type") != "custom-html":
            print(f"{short}: no custom-html `references` section — skipped")
            continue
        old = sec["settings"].get("html", "")
        if "sgref" in old:
            print(f"{short}: already rebuilt — skipped")
            continue

        entries, bad = parse(old)
        hm = re.search(r"<h2[^>]*>(.*?)</h2>", old, re.S | re.I)
        heading = strip_tags(hm.group(1)) if hm else "Published References"
        print(f"{short}: {len(entries)} references parsed, heading '{heading}'")
        for x in entries:
            print(f"    {x['year']}  {x['title'][:64]}")
            print(f"           {x['authors']} | {x['journal']} | {x['kind'] or '?'} -> "
                  f"{link_text(x)}")
        for txt, miss in bad:
            failed = True
            print(f"    !! COULD NOT PARSE ({', '.join(miss)}): {txt}")
        if bad:
            print(f"{short}: SKIPPED — fix the parser rather than shipping a partial block\n")
            continue
        if args.parse_only:
            print()
            continue

        new = build(entries, heading)
        backup = ROOT / "backups" / f"{short.replace('.json','')}-refs-{stamp}.json"
        backup.write_text(asset["value"])
        print(f"    backup {backup.relative_to(ROOT)}")
        print(f"    undo   python3 scripts/patch-template.py --restore "
              f"{backup.relative_to(ROOT)} --template {key}")
        sec["settings"]["html"] = new
        if args.dry_run:
            print(f"    DRY RUN — {len(old)} -> {len(new)} chars, not pushed\n")
            continue
        call(store, tok, f"themes/{theme['id']}/assets.json", "PUT",
             {"asset": {"key": key, "value": json.dumps(tpl, indent=2)}})
        print(f"    PUSHED ({len(old)} -> {len(new)} chars)\n")

    if failed:
        sys.exit("Some references could not be parsed — nothing was rebuilt for those pages.")


if __name__ == "__main__":
    main()
