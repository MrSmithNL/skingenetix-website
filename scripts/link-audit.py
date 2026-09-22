#!/usr/bin/env python3
"""Site-wide link audit — every page, every language, main content only (header/footer/nav excluded).

Author: Claude (Opus 5) for Malcolm Smith · 2026-09-22
Purpose: Malcolm, 2026-09-22 — "make sure the internal and external links are all updated and optimized on
every page, including the translated pages."

    python3 scripts/link-audit.py                       # all six locales → docs/audits/links/links-<date>.{md,json}
    python3 scripts/link-audit.py --locales en de       # subset

Per page:  in-content internal links, external links, study citations "(Author et al., YYYY)" and how many
           are linked, internal links in a translated page that LACK the locale prefix (they drop the reader
           into English), and broken internal targets (non-200).
Per hub:   inbound in-content links, distinct source pages, distinct anchors, head-term (exact-match)
           anchors — the Zyppy targets in docs/research-2026-ai-search-and-content-hubs.md §6.
Boilerplate: the repeated "Read Research" tile row and identical product-template anchors are counted but
           flagged, because Google discounts replicated blocks.
"""
import argparse, collections, datetime as dt, html as H, json, pathlib, re, time, urllib.error, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://www.skingenetix.com"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh) Chrome/126 link-audit"}
LOCALES = ["en", "de", "nl", "fr", "es", "it"]
HUBS = {"pdrn-research": ["pdrn"], "acetyl-hexapeptide-8-research": ["argireline", "acetyl hexapeptide"],
        "copper-peptide-research": ["copper peptide", "ghk-cu"], "matrixyl-3000-research": ["matrixyl"],
        "glutathione-research": ["glutathione"]}
BOILER = {"read research", "view the full clinical research & trials", "see clinical studies →", "learn more", "read more"}
CITE = re.compile(r"(?<![\w-])([A-Z][A-Za-zÀ-ſ\-]+) et al\.,? (\d{4})")


def get(u):
    for a in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40) as r:
                return r.status, r.read().decode("utf-8", "ignore")
        except urllib.error.HTTPError as e:
            if e.code in (429, 503):
                time.sleep(6 * (a + 1)); continue
            return e.code, ""
        except Exception:
            time.sleep(4 * (a + 1))
    return 0, ""


def english_paths():
    _, idx = get(BASE + "/sitemap.xml")
    out = {"/"}
    for sm in re.findall(r"<loc>(.*?)</loc>", idx):
        if re.search(r"/(de|nl|fr|es|it)/", sm):
            continue
        _, x = get(H.unescape(sm))
        for u in re.findall(r"<loc>(.*?)</loc>", x):
            u = H.unescape(u)
            if re.search(r"/(products|pages|collections|blogs)/", u) and not re.search(r"\.(jpg|png|webp)", u):
                out.add(u[len(BASE):] if u.startswith(BASE) else u)
    return sorted(out)


def main_content(page):
    m = re.search(r"<main\b.*?</main>", page, re.S)
    body = m.group(0) if m else page
    body = re.sub(r"<(script|style|noscript|template)\b.*?</\1>", "", body, flags=re.S)
    return body


def norm(href, loc):
    href = H.unescape(href).split("#")[0].split("?")[0]
    if href.startswith(BASE):
        href = href[len(BASE):]
    return href.rstrip("/") or "/"


def audit(locales):
    paths = english_paths()
    pages, inbound = {}, collections.defaultdict(list)
    targets = set()
    for loc in locales:
        pre = "" if loc == "en" else f"/{loc}"
        for p in paths:
            status, page = get(BASE + pre + p)
            body = main_content(page)
            links = [(norm(h, loc), H.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", t))).strip())
                     for h, t in re.findall(r"<a\b[^>]*href=[\"']([^\"']+)[\"'][^>]*>(.*?)</a>", body, re.S)]
            internal = [(h, a) for h, a in links if h.startswith("/") and not h.startswith("//")]
            external = [(h, a) for h, a in links if h.startswith("http") and "skingenetix.com" not in h]
            no_prefix = sorted({h for h, _ in internal if loc != "en" and not h.startswith(f"/{loc}/") and h != f"/{loc}"
                                and re.match(r"/(pages|products|collections|blogs)/", h)})
            text = H.unescape(re.sub(r"<[^>]+>", " ", body))
            cites = len({(a.lower(), y) for a, y in CITE.findall(text)})   # distinct studies; repeats stay plain by design
            linked = len(re.findall(r"<a\b[^>]*>\s*[A-Z][A-Za-zÀ-ſ\-]+ et al\.,? \d{4}\s*</a>", body))
            pages[f"{loc}:{p}"] = {"status": status, "internal": len(internal), "external": len(external),
                                   "external_domains": sorted({re.sub(r"https?://([^/]+).*", r"\1", h) for h, _ in external}),
                                   "citations": cites, "citations_linked": linked, "no_locale_prefix": no_prefix}
            for h, a in internal:
                bare = re.sub(rf"^/{loc}(?=/)", "", h) if loc != "en" else h
                targets.add(bare)
                if bare != p:
                    inbound[(loc, bare)].append((p, a))
            time.sleep(0.35)
        print(f"  {loc}: {len(paths)} pages crawled")
    broken = {}
    for t in sorted(targets):
        if re.match(r"/(pages|products|collections|blogs)/", t):
            s, _ = get(BASE + t)
            if s != 200:
                broken[t] = s
            time.sleep(0.2)
    return paths, pages, inbound, broken


def report(locales, paths, pages, inbound, broken):
    date = dt.date.today().isoformat()
    out = ROOT / "docs/audits/links"; out.mkdir(parents=True, exist_ok=True)
    L = [f"# Link audit — {date}", "", f"{len(paths)} pages × {len(locales)} languages, main content only. "
         "Tool: `scripts/link-audit.py`.", "", "## Hubs — inbound in-content links", "",
         "| Hub | " + " | ".join(f"{l} in / pages / anchors / exact / boilerplate" for l in locales) + " |",
         "|---|" + "---|" * len(locales)]
    for hub, heads in HUBS.items():
        row = []
        for loc in locales:
            inn = inbound.get((loc, f"/pages/{hub}"), [])
            anchors = {a.lower() for _, a in inn if a}
            exact = sum(1 for _, a in inn if any(h in a.lower() for h in heads))
            boiler = sum(1 for _, a in inn if a.lower() in BOILER)
            row.append(f"{len(inn)} / {len({s for s, _ in inn})} / {len(anchors)} / {exact} / {boiler}")
        L.append(f"| {hub} | " + " | ".join(row) + " |")
    L += ["", "## Pages with problems", "", "| Page | Problem |", "|---|---|"]
    for k, v in sorted(pages.items()):
        probs = []
        if v["status"] != 200:
            probs.append(f"HTTP {v['status']}")
        if v["no_locale_prefix"]:
            probs.append(f"{len(v['no_locale_prefix'])} internal link(s) without locale prefix → English: {', '.join(v['no_locale_prefix'][:4])}")
        if v["citations"] and v["citations_linked"] < v["citations"]:
            probs.append(f"{v['citations'] - v['citations_linked']} of {v['citations']} study citations unlinked")
        if v["internal"] < 3 and v["status"] == 200:
            probs.append(f"only {v['internal']} in-content internal links")
        if probs:
            L.append(f"| `{k}` | {'; '.join(probs)} |")
    L += ["", "## Broken internal targets", ""] + ([f"- `{t}` → {s}" for t, s in broken.items()] or ["None."])
    (out / f"links-{date}.md").write_text("\n".join(L) + "\n")
    (out / f"links-{date}.json").write_text(json.dumps(
        {"pages": pages, "inbound": {f"{l}:{t}": v for (l, t), v in inbound.items() if t.startswith("/pages/")},
         "broken": broken}, ensure_ascii=False, indent=1))
    print(f"  → docs/audits/links/links-{date}.md")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--locales", nargs="*", default=LOCALES)
    a = ap.parse_args()
    report(a.locales, *audit(a.locales))
