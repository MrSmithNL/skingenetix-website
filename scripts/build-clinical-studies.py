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
    ("copper-peptide", PHRASES["label_copper"], "copper-peptide-research", "templates/page.research-copper-peptide.json",
     "#014EB1", "#E4EDFA", None),
    ("matrixyl-3000", "Matrixyl 3000", "matrixyl-3000-research", "templates/page.research-matrixyl.json",
     "#016569", "#E0EFEF", ("configs/hub-upgrades/matrixyl-3000-research-evidence-merge-2026-09-26.json",
                            "configs/hub-upgrades/matrixyl-3000-research-layout-2026-09-26.json")),
    ("argireline", "Argireline®", "acetyl-hexapeptide-8-research", "templates/page.research-argireline.json",
     "#3E4A52", "#E9ECEE", None),
    ("pdrn", "PDRN", "pdrn-research", "templates/page.pdrn-research.json", "#9E4F5C", "#F6E9EB", None),
    ("glutathione", PHRASES["label_glutathione"], "glutathione-research", "templates/page.glutathione-research.json",
     "#8A6914", "#F5EEDC", None),
]
BANNER = "shopify://shop_images/skingenetix-peptide-laboratory-glassware-blue-pink-serum-actives.jpg"
# One picture bar per ingredient (Malcolm, 2026-09-29): crops of unused product-banner library candidates,
# chosen and label-checked in configs/banners/clinical-studies-section-bars-2026-09-29.json
BAR = "shopify://shop_images/skingenetix-clinical-studies-{slug}-bar.jpg"
BAR_MOBILE = "shopify://shop_images/skingenetix-clinical-studies-{slug}-bar-mobile.jpg"
# a scrimmed copy (critique F1): configs/banners/clinical-studies-banner-2026-09-29.json
BANNER_MOBILE = "shopify://shop_images/skingenetix-clinical-studies-research-banner-mobile.jpg"
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


def lab(label, loc):
    """An ingredient name: a per-locale dict (the hubs translate copper peptide and glutathione) or one string."""
    return label[loc] if isinstance(label, dict) else label


def fmt_date(iso, loc):
    y, m, d = (int(x) for x in iso.split("-"))
    return (PHRASES["date_format"][loc].replace("{d}", str(d))
            .replace("{m}", PHRASES["months"][loc][m - 1]).replace("{y}", str(y)))


GRADE_ORDER = {"a": 0, "b": 1, "c": 2, "d": 3, "x": 4, "n": 5, "r": 6}


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
    h = h.replace('id="evidence-sources"', f'id="{slug}-table"', 1)    # the anchor #{slug} is on the section bar
    h = h.replace('<div class="est"', f'<div class="est" style="--sg-accent:{acc};--sg-accent-tint:{tint}"', 1)
    # the section bar above carries the <h2> and the count, so the table keeps only the link to its hub
    h = re.sub(r'<h2 class="est__h">.*?</h2>\s*', "", h, count=1, flags=re.S)
    link = f'<a href="{pre(loc)}/pages/{hub}">{label}</a>'
    h = re.sub(r'(<p class="est__lead">).*?(</p>)', lambda m: m.group(1) + p("table_lead", loc, link=link) + m.group(2),
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

    def by_grade(m):
        # design critique 2026-09-29: "no visible sort order" — A, B, C, D, then reviews; hub order within a grade
        rows = re.findall(r"<tr>.*?</tr>", m.group(2), flags=re.S)
        key = lambda r: GRADE_ORDER.get((re.search(r"est__pill--(\w)", r) or [None, "r"])[1], 9)
        return m.group(1) + "".join(sorted(rows, key=key)) + m.group(3)
    h = re.sub(r"(<tbody>)(.*?)(</tbody>)", by_grade, h, count=1, flags=re.S)
    if not last:
        h = re.sub(r'<p class="est__key">.*?</p>', "", h, flags=re.S)
    return h, n


def jsonld(loc, items, appraisals, n, today="2026-09-29"):
    url = f"{BASE}{pre(loc)}/pages/clinical-studies"
    science = f"{BASE}{pre(loc)}/pages/the-science"
    return {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": url + "#webpage", "url": url, "inLanguage": loc,
         "name": p("title", loc), "description": p("seo_description", loc, n=n),
         "isPartOf": {"@id": f"{BASE}/#website"}, "dateModified": today,
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

def first_claim(html):
    """The hub index's row 01: its strongest result, already worded under the claims register."""
    m = re.search(r'<span class="evd__claim">(.*?)</span>', html or "", re.S)
    return m.group(1).strip() if m else None


def _spec_html(path, sid):
    spec = json.loads((ROOT / path).read_text())
    return next(a["section"]["settings"]["html"] for a in spec["add_sections"] if a["id"] == sid)


def live_tables(hu, sr):
    tables = []
    for slug, label, hub, tpl, acc, tint, fallback in HUBS:
        hdr, j = hu.split(hu.read_file(tpl))
        sec = j["sections"].get("evidence_sources")
        if sec and "What it found" in sec["settings"].get("html", ""):
            tr, stale = sr.translations(hu, tpl)
            vals = {"en": sec["settings"]["html"], **{l: tr[l].get("evidence_sources.html") for l in LOCALES[1:]}}
            ev = {"en": j["sections"]["evidence"]["settings"]["html"], **{l: tr[l].get("evidence.html") for l in LOCALES[1:]}}
            src = "live"
            if stale:
                print(f"  ⚠ {slug}: outdated translations on the hub: {stale}")
        elif fallback:
            vals, ev = _spec_html(fallback[0], "evidence_sources"), _spec_html(fallback[1], "evidence")
            src = f"specs {pathlib.Path(fallback[0]).name} + layout (hub not live yet)"
        else:
            sys.exit(f"  ✗ {slug}: no evidence table live and no fallback spec")
        claims = {l: first_claim(ev.get(l)) for l in LOCALES}
        missing = [l for l in LOCALES if not vals.get(l) or not claims[l]]
        if missing:
            sys.exit(f"  ✗ {slug}: no {missing} translation of the evidence table or index — the page ships in six languages")
        tables.append((slug, label, hub, acc, tint, vals, src, claims))
    return tables


def index_css(hu):
    """The hubs' own numbered-index styles (the Argireline template is the reference build)."""
    hdr, j = hu.split(hu.read_file("templates/page.research-argireline.json"))
    m = re.search(r"<style>.*?</style>", j["sections"]["evidence"]["settings"]["html"], re.S)
    return m.group(0) if m else ""


def unbrace(vals):
    """custom-html refuses "{{" / "}}" as Liquid, and minified CSS closes media queries as ";}}"."""
    out = {}
    for l, v in vals.items():
        while "}}" in v or "{{" in v:
            v = v.replace("}}", "} }").replace("{{", "{ {")
        out[l] = v
    return out


def build_spec(tables, keys, today, evd_css=""):
    appraisals = [h for _, _, h in keys]
    per_loc, counts, items = {l: [] for l in LOCALES}, {}, []
    # badges in table rows only: each copied table's <style> also names .est__pill--a (it read 13, not 8)
    grade_a = sum(len(re.findall(r'<span class="est__pill est__pill--a"', t[5]["en"])) for t in tables)
    for i, (slug, label, hub, acc, tint, vals, src, claims) in enumerate(tables):
        last = i == len(tables) - 1
        for loc in LOCALES:
            h, n = transform(vals[loc], loc, slug, lab(label, loc), hub, acc, tint, keys, last)
            per_loc[loc].append(h)
            counts[slug] = n
        items += scholarly_items(vals["en"])
    total = sum(counts.values())
    # The index's own rules, ahead of the five copied hub styles (".est ." out-ranks their single classes):
    #  * the hub link in each lead must look like a link (the hubs' lead has none, so it had no style)
    #  * one grade ramp for every table (critique F3: "A" took each hub's accent, so A differed per table
    #    and nearly matched B or C on some), darker = stronger evidence, and larger (the grade was the
    #    faintest thing in its row)
    #  * the ingredient headings in the theme's heading face (F5: 36px bold Muli under a 48px Fraunces close)
    #  * row links at least 44px tall on phones, not 16-21px (F4)
    style = ("<style>"
             ".est__lk--ap{display:block;margin:0 0 6px;font-weight:600}"
             ".est__lead a{color:var(--sg-accent);text-decoration:underline;text-underline-offset:2px}"
             ".est .est__pill{font-size:13px;font-weight:700;padding:5px 12px}"
             ".est .est__pill--a{background:#3A3F41;color:#fff}"
             ".est .est__pill--b{background:#6B7173;color:#fff}"
             ".est .est__pill--c{background:#E4E6E7;color:#2E3233}"
             ".est .est__pill--d{background:#fff;color:#3A3F41;box-shadow:inset 0 0 0 1px #9AA0A2}"
             ".est .est__pill--r{background:#fff;color:#3A3F41;border:1px dashed #6B7173}"
             ".est .est__h{font-family:var(--heading-font-family);font-weight:var(--heading-font-weight);"
             "font-size:40px;line-height:1.1;letter-spacing:var(--heading-letter-spacing)}"
             "@media(max-width:749px){.est .est__h{font-size:30px}"
             ".est .est__lk{display:block;padding:14px 0;line-height:1.3}}"   # 13px x 1.3 + 28 = 45px (39 measured at 11px)
             "</style>")

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
    # key figures, as the hubs' stats band (stock impact-text)
    stats = [(str(total), "stat1"), (str(grade_a), "stat2"), (str(len(appraisals)), "stat3")]
    add.append({"id": "stats", "after": "banner", "section": {
        "type": "impact-text",
        "blocks": {f"s{i}": {"type": "item", "settings": {
            "animate_impact_text": False, "title": v,
            "subheading": {l: p(k + "_label", l) for l in LOCALES},
            "content": {l: f"<p>{p(k + '_body', l)}</p>" for l in LOCALES}}} for i, (v, k) in enumerate(stats, 1)},
        "block_order": ["s1", "s2", "s3"],
        "settings": {"full_width": True, "stack_mobile": True, "text_alignment": "center", "impact_text_style": "fill",
                     "text_divider": "none", "impact_text_size_ratio": 0.7, "background": "#ffffff",
                     "heading_text_color": "#1A1A1A", "text_color": "#1A1A1A"}}})
    # overview: answer first, the grading key, the dated byline (the hubs' byline shape, without the reviewer)
    add.append({"id": "intro", "after": "stats", "section": {
        "type": "rich-text",
        "blocks": {"t": rt({l: f'<h2>{p("overview_title", l)}</h2><p>{p("answer", l, n=total)}</p><p>{p("grading", l)}</p>'
                               f'<p><em>{p("byline", l, date=fmt_date(today, l))}</em></p>' for l in LOCALES})},
        "block_order": ["t"],
        "settings": {"full_width": True, "content_width": "medium", "text_position": "start", "background": "#F0F0F0"}}})
    # quick links: the hubs' numbered index, one row per ingredient in its accent, each opening its section bar
    rows = {l: "".join(
        f'<a class="evd__row" href="#{slug}" style="--sg-accent:{acc}"><span class="evd__n">{i:02d}</span><span>'
        f'<span class="evd__claim">{p("index_claim", l, x=lab(label, l), n=counts[slug])}</span>'
        f'<span class="evd__qual">{p("index_qual", l, claim=claims[l])}</span></span></a>'
        for i, (slug, label, hub, acc, tint, vals, src, claims) in enumerate(tables, 1)) for l in LOCALES}
    # one heading system on the page (critique F5): the index heading in the theme's heading face, as the bars
    evd_css += ("<style>.evd .evd__h{font-family:var(--heading-font-family);font-weight:var(--heading-font-weight);"
                "font-size:40px;letter-spacing:var(--heading-letter-spacing)}"
                "@media(max-width:749px){.evd .evd__h{font-size:30px}}</style>")
    index = {l: (evd_css + f'<div class="evd"><h2 class="evd__h">{p("index_title", l)}</h2>'
                 f'<p class="evd__cap">{p("index_caption", l)}</p><div class="evd__list">{rows[l]}</div></div>')
             for l in LOCALES}
    add.append({"id": "index", "after": "intro", "section": {"type": "custom-html",
                                                             "settings": {"background": "#ffffff", "html": unbrace(index)}}})
    prev = "index"
    for i, (slug, label, *_rest) in enumerate(tables):
        # the picture bar: the section's <h2>, the count, and the anchor the quick links jump to
        bid = "bar_" + slug.replace("-", "_")
        add.append({"id": bid, "after": prev, "section": {
            "type": "image-with-text-overlay",
            "blocks": {
                "anchor": {"type": "liquid", "settings": {"liquid":
                    f'<span id="{slug}" style="display:block;position:relative;top:-110px;visibility:hidden"></span>'}},
                "head": rt({l: f'<h2>{p("section_title", l, x=lab(label, l))}</h2><p>{p("bar_sub", l, n=counts[slug])}</p>'
                            for l in LOCALES})},
            "block_order": ["anchor", "head"],
            "settings": {"full_width": True, "allow_transparent_header": False, "enable_parallax": False,
                         "image_size": "auto", "image": BAR.format(slug=slug), "mobile_image": BAR_MOBILE.format(slug=slug),
                         "mobile_text_position": "place-self-center-start text-start",
                         "desktop_text_position": "sm:place-self-center-start sm:text-start",
                         "text_color": "#ffffff", "overlay_color": "#1A1A1A", "overlay_opacity": 30}}})
        prev = bid
        sid = "ev_" + slug.replace("-", "_")
        vals = {l: (style if i == 0 else "") + per_loc[l][i] for l in LOCALES}
        if i == len(tables) - 1:
            for l in LOCALES:
                vals[l] += "\n" + LD_TAG + "\n" + json.dumps(jsonld(l, items, appraisals, total, today), indent=1,
                                                             ensure_ascii=False) + "\n</script>"
        vals = unbrace(vals)
        # white, as on the hubs: left unset, the section took the bone intro's ground (critique F2)
        add.append({"id": sid, "after": prev, "section": {"type": "custom-html",
                                                          "settings": {"background": "#ffffff", "html": vals}}})
        prev = sid
    add.append({"id": "closing", "after": prev, "section": {
        "type": "rich-text",
        "blocks": {"t": rt({l: f'<h2>{p("closing_title", l)}</h2><p>'
                               + p("closing", l, science_link=f'<a href="{pre(l)}/pages/the-science">{p("science", l)}</a>')
                               + "</p><p>" + p("shop", l, shop_link=f'<a href="{pre(l)}/collections/all">{p("shop_link", l)}</a>')
                               + "</p>" for l in LOCALES})},
        "block_order": ["t"],
        "settings": {"full_width": True, "content_width": "medium", "text_position": "start", "background": "#F0F0F0"}}})
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
                      ".prose h2 + p {font-size: 20px; line-height: 1.5;}",
                      "@media (max-width: 699px) {.prose h2 + p {font-size: 17px;} }"],
            **{"bar_" + t[0].replace("-", "_"): [".prose h2 {font-size: 40px; margin: 0 0 4px;}",
                                                 ".prose p {font-size: 16px; margin: 0;}",
                                                 "@media (max-width: 749px) {.prose h2 {font-size: 26px;} .prose p {font-size: 14px;} }"]
               for t in tables},
            "closing": [".rich-text {justify-content: center;}", ".prose {max-width: 66ch; margin-inline: auto;}",
                        ".prose h2 {font-size: 32px;}", "@media (max-width: 749px) {.prose h2 {font-size: 26px;} }"]},
    }
    return spec, counts, total


def main():
    hu = _load("hu", "scripts/hub-upgrade.py")
    sr = _load("sr", "scripts/set-reviewer.py")
    configs = [json.loads(pathlib.Path(f).read_text()) for f in sorted(glob.glob(str(ROOT / "configs/studies/*.json")))]
    keys = appraisal_keys(configs)
    tables = live_tables(hu, sr)
    import datetime
    spec, counts, total = build_spec(tables, keys, datetime.date.today().isoformat(), index_css(hu))
    OUT.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n")
    print(f"  study pages: {', '.join(f'{s} {y}' for s, y, _ in keys)}")
    for t in tables:
        print(f"  {t[0]:<16} {counts[t[0]]:>2} rows · {t[6]}")
    print(f"  {total} studies · spec written to {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
