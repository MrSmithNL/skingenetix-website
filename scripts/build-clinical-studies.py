#!/usr/bin/env python3
"""Generate the hub-upgrade spec for /pages/clinical-studies from the five LIVE hub evidence tables.

Author: Claude (Opus 5.5) for Malcolm Smith · 2026-09-29
Decision: ADR-2026-09-29-C (docs/decision-research-section-navigation-2026-09-29.md).

    python3 scripts/build-clinical-studies.py            # writes the spec, prints a summary
    python3 scripts/hub-upgrade.py configs/hub-upgrades/clinical-studies.json --apply

WHY A GENERATOR, NOT A HAND-WRITTEN SPEC
The page's rows ARE the hubs' Evidence & Sources tables — same vetted rows, same wording, same
six-locale translations, already under ADR-2026-09-24-P (positive results only). Copying them by hand
would fork five tables that change whenever a hub does. So this reads each hub's live template (and its
registered translations) and rebuilds the index from them; re-run it after any hub table changes.

WHAT IT CHANGES IN A COPIED TABLE
  * strips the hub's own WebPage JSON-LD (left in, the index would claim to be five other pages)
  * re-ids the block (#copper-peptide …) for the "By ingredient" jump links, and sets the hub's accent
    inline — on its hub the colour comes from a style defined elsewhere on that page
  * retitles it and replaces its lead with a link to the hub (the head-term anchor the hub should own)
  * adds "Read our appraisal →" to rows whose study has its own page (configs/studies/*.json)
  * keeps the "titles are quoted exactly" footnote on the last table only

Build rung: stock sections (banner, intro, closing) plus custom-html for the tables — the same forced
rung as the hubs, because no stock section renders a three-column table.
"""
import glob
import html as H
import importlib.util
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://www.skingenetix.com"
LOCALES = ["en", "de", "nl", "fr", "es", "it"]
TEMPLATE = "templates/page.clinical-studies.json"
OUT = ROOT / "configs/hub-upgrades/clinical-studies.json"
PHRASES = json.loads((ROOT / "configs/hub-i18n/clinical-studies.json").read_text())

# Menu order, so the page reads in the order the Science menu lists the ingredients.
HUBS = [
    # slug, label, hub handle, template, accent, tint, spec used only while the hub is not yet live
    ("copper-peptide", "Copper peptide (GHK-Cu)", "copper-peptide-research", "templates/page.research-copper-peptide.json",
     "#014EB1", "#E4EDFA", None),
    ("matrixyl-3000", "Matrixyl 3000", "matrixyl-3000-research", "templates/page.research-matrixyl.json",
     "#016569", "#E0EFEF", "configs/hub-upgrades/matrixyl-3000-research-evidence-merge-2026-09-26.json"),
    ("argireline", "Argireline®", "acetyl-hexapeptide-8-research", "templates/page.research-argireline.json",
     "#3E4A52", "#E9ECEE", None),
    ("pdrn", "PDRN", "pdrn-research", "templates/page.pdrn-research.json", "#9E4F5C", "#F6E9EB", None),
    ("glutathione", "Glutathione", "glutathione-research", "templates/page.glutathione-research.json",
     "#8A6914", "#F5EEDC", None),
]
BANNER = "shopify://shop_images/skingenetix-peptide-laboratory-glassware-blue-pink-serum-actives.jpg"
BANNER_MOBILE = "shopify://shop_images/skingenetix-peptide-laboratory-glassware-blue-pink-actives-mobile.jpg"
LD_TAG = '<script type="application/ld+json" id="sgx-webpage-jsonld">'


def _load(name, path):
    s = importlib.util.spec_from_file_location(name, ROOT / path)
    m = importlib.util.module_from_spec(s)
    argv, sys.argv = sys.argv, [sys.argv[0]]        # these modules parse args at import
    s.loader.exec_module(m)
    sys.argv = argv
    return m


def pre(loc):
    return "" if loc == "en" else f"/{loc}"


def p(key, loc, **kw):
    s = PHRASES[key][loc]
    for k, v in kw.items():
        s = s.replace("{" + k + "}", str(v))
    return s


# ---------------------------------------------------------------- pure transforms (tested offline)

def appraisal_keys(configs):
    """(surname, year, handle) for every study page, read from its config — the new stock-template shape
    (`citation`) and the pilot shape (`jsonld` isBasedOn author) both."""
    out = []
    for c in configs:
        if "citation" in c:
            surname = re.match(r"\s*([A-ZÀ-Ý][\w'’-]+)", c["citation"]["en"]).group(1)
            year = c["scholarly"]["datePublished"][:4]
        else:
            based = c["jsonld"].get("mainEntity", {}).get("isBasedOn", {}) or {}
            surname = re.match(r"\s*([A-ZÀ-Ý][\w'’-]+)", based.get("author", "")).group(1)
            year = str(based.get("datePublished", ""))[:4]
        out.append((surname, year, c["handle"]))
    return out


def transform(html, loc, slug, label, hub, acc, tint, keys, last):
    """One hub's evidence block, rebuilt for the index page in one locale."""
    h = re.sub(re.escape(LD_TAG) + r".*?</script>", "", html, flags=re.S).rstrip()
    rows = re.findall(r"<tr>\s*<td", h)
    n = len(rows)
    h = h.replace('id="evidence-sources"', f'id="{slug}"', 1)
    h = h.replace('<div class="est"', f'<div class="est" style="--sg-accent:{acc};--sg-accent-tint:{tint}"', 1)
    h = re.sub(r'(<h2 class="est__h">).*?(</h2>)', lambda m: m.group(1) + p("section_title", loc, x=label) + m.group(2),
               h, count=1, flags=re.S)
    link = f'<a href="{pre(loc)}/pages/{hub}">{label}</a>'
    h = re.sub(r'(<p class="est__lead">).*?(</p>)', lambda m: m.group(1) + p("section_lead", loc, link=link, n=n) + m.group(2),
               h, count=1, flags=re.S)

    def add_link(m):
        row = m.group(0)
        meta = re.search(r'<p class="est__me">(.*?)</p>', row, re.S)
        if not meta:
            return row
        text = H.unescape(re.sub(r"<[^>]+>", "", meta.group(1)))
        for surname, year, handle in keys:
            if surname in text and year in text:
                a = f'<a class="est__lk est__lk--ap" href="{pre(loc)}/pages/study/{handle}">{p("appraisal", loc)}</a>'
                return row.replace('<a class="est__lk"', a + '<a class="est__lk"', 1)
        return row
    h = re.sub(r"<tr>.*?</tr>", add_link, h, flags=re.S)
    if not last:
        h = re.sub(r'<p class="est__key">.*?</p>', "", h, flags=re.S)
    return h, n


def jsonld(loc, items, appraisals, n):
    url = f"{BASE}{pre(loc)}/pages/clinical-studies"
    science = f"{BASE}{pre(loc)}/pages/the-science"
    return {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": url + "#webpage", "url": url, "inLanguage": loc,
         "name": p("title", loc), "description": p("seo_description", loc, n=n),
         "isPartOf": {"@id": f"{BASE}/#website"},
         "about": [{"@type": "Thing", "name": x} for x in
                   ("PDRN", "Argireline", "Copper peptide GHK-Cu", "Matrixyl 3000", "Glutathione")],
         "author": {"@type": "Person", "name": "Malcolm Smith", "jobTitle": "Founder, Skingenetix"},
         # no reviewedBy yet: set-reviewer.py cannot remove it from this page, and her credit must come off
         # everywhere in one command (memory reviewer-credit-live-before-review)
         "publisher": {"@type": "Organization", "@id": f"{BASE}/#organization", "name": "Skingenetix"},
         "hasPart": [{"@type": "WebPage", "url": f"{BASE}{pre(loc)}/pages/study/{h}"} for h in appraisals],
         "mainEntity": {"@type": "ItemList", "numberOfItems": len(items), "itemListElement": [
             {"@type": "ListItem", "position": i, "item": {"@type": "ScholarlyArticle", "name": t, "url": u}}
             for i, (t, u) in enumerate(items, 1)]}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Skingenetix", "item": BASE + pre(loc) + "/"},
            {"@type": "ListItem", "position": 2, "name": p("science", loc), "item": science},
            {"@type": "ListItem", "position": 3, "name": p("title", loc), "item": url}]}]}


def scholarly_items(html):
    """(published title, source URL) for every row of an English table."""
    out = []
    for row in re.findall(r"<tr>\s*<td.*?</tr>", html, flags=re.S):
        t = re.search(r'<p class="[^"]*est__ti[^"]*">(.*?)</p>', row, re.S)
        u = re.search(r'<a class="est__lk" href="([^"]+)"', row)
        if t:
            out.append((H.unescape(re.sub(r"<[^>]+>", "", t.group(1))).strip(), u.group(1) if u else None))
    return out


# ---------------------------------------------------------------- the live side

def live_tables(hu, sr):
    tables = []
    for slug, label, hub, tpl, acc, tint, fallback in HUBS:
        hdr, j = hu.split(hu.read_file(tpl))
        sec = j["sections"].get("evidence_sources")
        if sec and "What it found" in sec["settings"].get("html", ""):
            tr, stale = sr.translations(hu, tpl)
            vals = {"en": sec["settings"]["html"], **{l: tr[l].get("evidence_sources.html") for l in LOCALES[1:]}}
            src = "live"
            if stale:
                print(f"  ⚠ {slug}: outdated translations on the hub: {stale}")
        elif fallback:
            spec = json.loads((ROOT / fallback).read_text())
            vals = next(a["section"]["settings"]["html"] for a in spec["add_sections"] if a["id"] == "evidence_sources")
            src = f"spec {pathlib.Path(fallback).name} (hub not live yet)"
        else:
            sys.exit(f"  ✗ {slug}: no evidence table live and no fallback spec")
        missing = [l for l in LOCALES if not vals.get(l)]
        if missing:
            sys.exit(f"  ✗ {slug}: no {missing} translation of the evidence table — the index ships in six languages")
        tables.append((slug, label, hub, acc, tint, vals, src))
    return tables


def build_spec(tables, keys):
    appraisals = [h for _, _, h in keys]
    per_loc, counts, items = {l: [] for l in LOCALES}, {}, []
    for i, (slug, label, hub, acc, tint, vals, src) in enumerate(tables):
        last = i == len(tables) - 1
        for loc in LOCALES:
            h, n = transform(vals[loc], loc, slug, label, hub, acc, tint, keys, last)
            per_loc[loc].append(h)
            counts[slug] = n
        items += scholarly_items(vals["en"])
    total = sum(counts.values())
    # the hub link in each lead must look like a link (the hubs' lead has none, so it had no style)
    style = ('<style>.est__lk--ap{display:block;margin:0 0 6px;font-weight:600}'
             '.est__lead a{color:var(--sg-accent);text-decoration:underline;text-underline-offset:2px}</style>')
    jump = {l: p("by_ingredient", l) + " " + ", ".join(f'<a href="#{s}">{lab}</a>' for s, lab, *_ in tables) for l in LOCALES}

    def rt(values):
        return {"type": "richtext", "settings": {"content": values}}

    add = [{"id": "banner", "after": None, "section": {
        "type": "image-with-text-overlay",
        "blocks": {
            "crumb": rt({l: f'<p><a href="{pre(l)}/pages/the-science">{p("science", l)}</a> › {p("title", l)}</p>' for l in LOCALES}),
            "head": rt({l: f'<h1>{p("title", l)}</h1><p>{p("deck", l)}</p>' for l in LOCALES})},
        "block_order": ["crumb", "head"],
        "settings": {"full_width": True, "allow_transparent_header": False, "enable_parallax": False, "image_size": "sm",
                     "image": BANNER, "mobile_image": BANNER_MOBILE,
                     "mobile_text_position": "place-self-start-center text-center",
                     "desktop_text_position": "sm:place-self-center-start sm:text-start",
                     "text_color": "#ffffff", "overlay_color": "#1A1A1A", "overlay_opacity": 35}}}]
    add.append({"id": "intro", "after": "banner", "section": {
        "type": "rich-text",
        "blocks": {"t": rt({l: f'<p>{p("answer", l, n=total)}</p><p>{p("grading", l)}</p><p>{jump[l]}</p>' for l in LOCALES})},
        "block_order": ["t"],
        "settings": {"full_width": True, "content_width": "medium", "text_position": "start", "background": "#F0F0F0"}}})
    prev = "intro"
    for i, (slug, *_rest) in enumerate(tables):
        sid = "ev_" + slug.replace("-", "_")
        vals = {l: (style if i == 0 else "") + per_loc[l][i] for l in LOCALES}
        if i == len(tables) - 1:
            for l in LOCALES:
                vals[l] += "\n" + LD_TAG + "\n" + json.dumps(jsonld(l, items, appraisals, total), indent=1,
                                                             ensure_ascii=False) + "\n</script>"
        add.append({"id": sid, "after": prev, "section": {"type": "custom-html", "settings": {"html": vals}}})
        prev = sid
    add.append({"id": "closing", "after": prev, "section": {
        "type": "rich-text",
        "blocks": {"t": rt({l: f'<h2>{p("closing_title", l)}</h2><p>'
                               + p("closing", l, science_link=f'<a href="{pre(l)}/pages/the-science">{p("science", l)}</a>')
                               + "</p>" for l in LOCALES})},
        "block_order": ["t"],
        "settings": {"full_width": True, "content_width": "medium", "text_position": "start", "background": "#ffffff"}}})
    spec = {
        "_about": ("GENERATED by scripts/build-clinical-studies.py — do not edit by hand; re-run the generator. "
                   "ADR-2026-09-29-C. Rows are the five hubs' live Evidence & Sources tables. Sources: "
                   + "; ".join(f"{t[0]} = {t[6]}" for t in tables)),
        "template": TEMPLATE,
        "page": "clinical-studies",
        "add_sections": add,
        "remove_sections": ["start"],
        "section_css": {
            "intro": [".rich-text {justify-content: center;}", ".prose {max-width: 66ch; margin-inline: auto;}",
                      ".prose p:first-child {font-size: 20px; line-height: 1.5;}",
                      "@media (max-width: 699px) {.prose p:first-child {font-size: 17px;} }"],
            "closing": [".rich-text {justify-content: center;}", ".prose {max-width: 66ch; margin-inline: auto;}"]},
    }
    return spec, counts, total


def main():
    hu = _load("hu", "scripts/hub-upgrade.py")
    sr = _load("sr", "scripts/set-reviewer.py")
    configs = [json.loads(pathlib.Path(f).read_text()) for f in sorted(glob.glob(str(ROOT / "configs/studies/*.json")))]
    keys = appraisal_keys(configs)
    tables = live_tables(hu, sr)
    spec, counts, total = build_spec(tables, keys)
    OUT.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n")
    print(f"  study pages: {', '.join(f'{s} {y}' for s, y, _ in keys)}")
    for slug, *_x, src in tables:
        print(f"  {slug:<16} {counts[slug]:>2} rows · {src}")
    print(f"  {total} studies · spec written to {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
