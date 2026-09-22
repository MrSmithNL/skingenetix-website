#!/usr/bin/env python3
"""Full page audit: technical SEO, GEO/AI-search (AISO), and live-browser design.

Author: Claude (Opus 5) for Malcolm Smith · 2026-09-22
Purpose: Malcolm's standard (2026-09-22) — every page validated in a live browser,
checked against the design system, and audited for SEO, GEO and AISO, including
URL, technical and on-page factors and HTML tagging. Image needs become to-dos.

    python3 scripts/page-audit.py /pages/pdrn-research
    python3 scripts/page-audit.py /pages/pdrn-research /pages/the-science --out docs/audits/pages

Writes docs/audits/pages/<slug>-<date>.md (+ .json) and prints a summary.

WHAT IT CHECKS, AND ON WHOSE AUTHORITY
  SEO   Google Search Central basics: one H1, title/description present and sized,
        self-canonical, hreflang for every published locale + x-default, indexable,
        Open Graph, image alt text, clean URL, valid structured data.
  GEO   The agency AISO 36-factor model (~/.claude/.../skills/aiso/SKILL.md), page-level
        factors only, RE-WEIGHTED by docs/research-2026-ai-search-and-content-hubs.md
        where 2026 evidence disagrees: llms.txt (measured null — reported, not scored),
        FAQ schema (weak — informational), Q&A genre (−5.7% — not rewarded), publishing
        frequency (site-level, not scored here). The strongest surviving signals are
        weighted highest: answer in the first 30% of text, extractable text without JS,
        semantic headings matching the query, fact and citation density, freshness.
  DESIGN Rendered in Chromium at 1440 and 390 px: blank bands, empty-but-tall sections
        (a padded custom-html wrapper left 160 px above the PDRN hero), background
        alternation and palette (docs/visual-identity: Bone #F0F0F0, White, Graphite
        #1A1A1A), horizontal overflow, headings broken mid-word on mobile, broken images.
"""
import argparse, asyncio, datetime as dt, html as H, json, pathlib, re, sys, time, urllib.error, urllib.request
from urllib.parse import urlparse

import trafilatura
from lxml import html as LH

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://www.skingenetix.com"
LOCALES = ["en", "de", "nl", "fr", "es", "it"]
PALETTE = {"rgb(240, 240, 240)": "Bone", "rgb(255, 255, 255)": "White", "rgb(26, 26, 26)": "Graphite"}
AI_BOTS = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "PerplexityBot",
           "Google-Extended", "Bingbot", "Applebot-Extended", "CCBot"]
TARGETS = json.loads((ROOT / "configs/page-targets.json").read_text())


def fetch(url, ua="Mozilla/5.0"):
    for a in range(6):
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": ua}), timeout=40)
            return r.status, r.geturl(), r.read().decode("utf-8", "ignore")
        except urllib.error.HTTPError as e:
            if e.code in (429, 503) and a < 5:
                time.sleep(8 * (a + 1)); continue
            return e.code, url, ""


def words(s):
    return re.findall(r"[\w'’-]+", s)


class Report:
    def __init__(self):
        self.items = []

    def add(self, area, check, ok, detail="", severity="med", weight=1.0):
        self.items.append({"area": area, "check": check, "ok": bool(ok), "detail": detail,
                           "severity": "pass" if ok else severity, "weight": weight})

    def score(self, area):
        xs = [i for i in self.items if i["area"] == area and i["severity"] != "info"]
        if not xs:
            return None
        return round(100 * sum(i["weight"] for i in xs if i["ok"]) / sum(i["weight"] for i in xs))


# ------------------------------------------------------------------ SEO + GEO (raw HTML)

MKT = json.loads((ROOT / "configs/marketing-rules.json").read_text())


def audit_marketing(path, rep, raw, main, main_text, tgt, h1=None):
    """MARKETING — the strongest supported claim, worded to sell (Malcolm, 2026-09-22).

    Deterministic checks only; every rule lives in configs/marketing-rules.json with its reason.
    A score under MKT['threshold'] means: run deeper claims research (docs/claims/), don't soften.
    """
    kind = tgt.get("type") or ("product" if path.startswith("/products/") else "collection" if path.startswith("/collections/")
                              else "home" if path == "/" else "page")
    txt = main_text
    wl = words(txt)
    # The opening is read from the page title on: product galleries put "zoom / go to item N"
    # control text first in <main>, which is not copy (found on the copper night cream, 2026-09-22).
    start = txt.find(h1[0]) if h1 and h1[0] and h1[0] in txt else 0
    hero = " ".join(words(txt[start:])[:80]).lower()
    first30 = " ".join(wl[: max(60, len(wl) * 3 // 10)])
    rep.add("MARKETING", "Opening states a concrete skin outcome", any(w in hero for w in MKT["outcome_words"]),
            hero[:140], "high", 2)
    proof = re.search(r"\d+(\.\d+)? ?%(?! ?(?:GHK|PDRN|Argireline|GSSG|glutathione|Matrixyl|copper))|\b\d+ (?:days|weeks|women|people|participants|volunteers)\b",
                      first30, re.I)
    rep.add("MARKETING", "A proof point (result %, time frame or trial size) in the first 30% of text",
            bool(proof), proof.group(0) if proof else "none", "med", 2)
    low = txt.lower()
    hedges = [h for h in MKT["hedges"] if h in low]
    n_hedge = sum(low.count(h) for h in MKT["hedges"])
    per100 = 100 * n_hedge / max(len(wl), 1)
    limit = 2.0 if kind == "hub" else 1.0
    rep.add("MARKETING", f"Hedging ≤ {limit} per 100 words ({'science page' if kind == 'hub' else 'sales copy'})",
            per100 <= limit, f"{per100:.1f}/100 words: {hedges[:6]}", "med", 2)
    bad = [(m.group(0), r["why"]) for r in MKT["unsupported"] for m in re.finditer(r["re"], raw, re.I)]
    rep.add("MARKETING", "No claim known to be unsupported (docs/claims/)", not bad,
            "; ".join(f"'{b}' — {w}" for b, w in dict(bad).items()) or "clean", "high", 3)
    med = [(m.group(0), r["why"]) for r in MKT["medicinal"] for m in re.finditer(r["re"], txt, re.I)]
    rep.add("MARKETING", "No medicinal wording (EU cosmetic-claims rules)", not med,
            "; ".join(f"'{b}' — {w}" for b, w in dict(med).items()) or "clean", "high", 3)
    if kind == "product":
        buy = bool(re.search(r'action="[^"]*/cart/add', raw))
        rep.add("MARKETING", "Add-to-cart present", buy, "", "high", 1)
    else:
        buy = len(set(re.findall(r'href="(?:/[a-z]{2})?/products/([^"?#]+)', raw)))
        rep.add("MARKETING", "Path to purchase: links to at least one product", buy >= 1, f"{buy} products linked", "med", 1)
    # A paragraph that links out to its source (patent, brochure, DOI) is sourced even when it names none of
    # the words below — the Matrixyl chart captions cite a Sederma patent and brochure (2026-09-22).
    paras = [(p_.text_content(), bool(p_.xpath(".//a[starts-with(@href,'http')]"))) for p_ in main.xpath(".//p|.//li")]
    unsourced = [p_[:90] for p_, linked in paras if re.search(r"\d+(\.\d+)? ?%", p_)
                 and not linked
                 and not re.search(MKT["own_concentrations"], p_, re.I)
                 and not re.search(r"et al|study|trial|studies|PubMed|research", p_, re.I)]
    rep.add("MARKETING", "Every result figure sits next to its source", not unsourced,
            f"{len(unsourced)} unsourced: {unsourced[:2]}", "low", 1)

def audit_html(path, rep, site):
    url = BASE + path
    status, final, raw = fetch(url)
    rep.add("SEO", "HTTP 200, no redirect", status == 200 and final.rstrip("/") == url.rstrip("/"),
            f"{status} → {final}", "high", 2)
    doc = LH.fromstring(raw)
    head = doc.find("head")
    tgt = TARGETS.get(path, {})
    primary = tgt.get("primary", "")

    # URL
    p = urlparse(url).path
    rep.add("SEO", "Clean URL (lowercase, hyphens, no params, ≤ 60 chars)",
            p == p.lower() and "_" not in p and "?" not in url and len(p) <= 60, p, "low")
    rep.add("SEO", "URL carries the head term", not primary or all(w in p for w in primary.split()[:1]),
            f"head term '{primary}'", "low", 0.5)

    # Title / description
    title = (doc.findtext(".//title") or "").strip()
    rep.add("SEO", "Title present, 30–60 chars", 30 <= len(title) <= 60, f"{len(title)}c: {title}", "high", 2)
    rep.add("SEO", "Title contains head term", primary.lower() in title.lower(), f"'{primary}'", "high", 2)
    desc = (doc.xpath('//meta[@name="description"]/@content') or [""])[0].strip()
    rep.add("SEO", "Meta description 70–160 chars", 70 <= len(desc) <= 160, f"{len(desc)}c", "med")
    rep.add("SEO", "Meta description contains head term", primary.lower() in desc.lower(), "", "low", 0.5)

    # Indexability
    robots = (doc.xpath('//meta[@name="robots"]/@content') or [""])[0].lower()
    rep.add("SEO", "Indexable (no noindex)", "noindex" not in robots, robots or "no robots meta", "high", 3)
    canon = (doc.xpath('//link[@rel="canonical"]/@href') or [""])[0]
    rep.add("SEO", "Self-referencing absolute canonical", canon.rstrip("/") == url.rstrip("/"), canon, "high", 2)
    hl = {l.get("hreflang"): l.get("href") for l in doc.xpath('//link[@rel="alternate"][@hreflang]')}
    need = set(LOCALES) | {"x-default"}
    rep.add("SEO", "hreflang for all 6 locales + x-default", need <= set(hl),
            f"missing {sorted(need - set(hl))}" if not need <= set(hl) else f"{len(hl)} alternates", "med")

    # Social
    og = {m.get("property"): m.get("content") for m in doc.xpath('//meta[starts-with(@property,"og:")]')}
    rep.add("SEO", "Open Graph title/description/image/url", all(og.get(k) for k in ("og:title", "og:description", "og:image", "og:url")),
            ", ".join(k for k in ("og:title", "og:description", "og:image", "og:url") if not og.get(k)) or "complete", "low")
    rep.add("SEO", "og:title matches the page title", (og.get("og:title") or "").strip() == title, og.get("og:title", ""), "low", 0.5)

    # Main content
    # Structured data is read BEFORE scripts are stripped from <main> — JSON-LD can live
    # inside a content section (it does on the hub pages), and stripping first hid it.
    ld_scripts = [s.text_content() for s in doc.xpath('//script[@type="application/ld+json"]')]
    main = doc.find(".//main")
    if main is None:
        rep.add("SEO", "<main> landmark present", False, "", "med")
        return {}
    for bad in main.xpath(".//script|.//style|.//noscript"):
        bad.drop_tree()
    main_text = re.sub(r"\s+", " ", main.text_content()).strip()

    h1 = [re.sub(r"\s+", " ", e.text_content()).strip() for e in doc.xpath("//h1")]
    rep.add("SEO", "Exactly one <h1>", len(h1) == 1, " | ".join(h1) or "none", "high", 2)
    audit_marketing(path, rep, raw, main, main_text, tgt, h1)
    rep.add("SEO", "<h1> contains head term", any(primary.lower() in x.lower() for x in h1), "", "med")
    h2 = [re.sub(r"\s+", " ", e.text_content()).strip() for e in main.xpath(".//h2")]
    pseudo = [re.sub(r"\s+", " ", e.text_content()).strip() for e in main.xpath('.//*[not(self::h1 or self::h2 or self::h3 or self::h4) and (contains(concat(" ",@class," ")," h1 ") or contains(concat(" ",@class," ")," h2 ") or contains(concat(" ",@class," ")," h3 "))]')]
    rep.add("SEO", "Topic headings are real <h2> (≥ 3)", len(h2) >= 3, f"{len(h2)} <h2>: {h2}", "high", 2)
    rep.add("SEO", "Visual-only headings (styled <p>/<span>)", False if pseudo else True,
            f"{len(pseudo)} that look like headings but are not: {pseudo[:8]}", "info", 0)
    levels = [int(e.tag[1]) for e in doc.xpath("//h1|//h2|//h3|//h4|//h5|//h6")]
    skips = [f"h{a}→h{b}" for a, b in zip(levels, levels[1:]) if b > a + 1]
    rep.add("SEO", "No skipped heading levels", not skips, ", ".join(skips) or "clean", "low")

    imgs = main.xpath(".//img")
    no_alt = [i.get("src", "")[-60:] for i in imgs if not (i.get("alt") or "").strip()]
    rep.add("SEO", "Content images have alt text", not no_alt, f"{len(imgs) - len(no_alt)}/{len(imgs)}" + (f" missing: {no_alt[:4]}" if no_alt else ""), "med")
    rep.add("SEO", "Images declare width/height (CLS)", all(i.get("width") and i.get("height") for i in imgs),
            f"{sum(1 for i in imgs if not (i.get('width') and i.get('height')))} without", "low", 0.5)

    links = [a.get("href", "") for a in main.xpath(".//a[@href]")]
    internal = sorted({l.split("?")[0] for l in links if l.startswith("/") and not l.startswith("//")})
    external = sorted({l for l in links if l.startswith("http") and "skingenetix" not in l})
    rep.add("SEO", "Internal links in content ≥ 5", len(internal) >= 5, f"{len(internal)} unique", "med")
    in_tables = main.xpath(".//table//a")
    rep.add("GEO", "No links inside tables (AI extraction drops the table)", not in_tables, f"{len(in_tables)} found", "med")

    # Structured data
    lds, bad_ld = [], 0
    for s in ld_scripts:
        try:
            d = json.loads(s)
            lds.extend(d.get("@graph", [d]) if isinstance(d, dict) else d)
        except Exception:
            bad_ld += 1
    types = [n.get("@type") for n in lds if isinstance(n, dict)]
    rep.add("SEO", "All JSON-LD parses", bad_ld == 0, f"{bad_ld} invalid block(s)", "high", 2)
    dup = sorted({t for t in types if isinstance(t, str) and types.count(t) > 1 and t not in ("ListItem", "Question", "ScholarlyArticle")})
    rep.add("SEO", "No duplicate schema types", not dup, f"duplicates {dup}" if dup else f"types {types}", "med")
    wp = next((n for n in lds if isinstance(n, dict) and n.get("@type") in ("WebPage", "Article", "MedicalWebPage")), None)
    rep.add("GEO", "Page entity schema (WebPage/Article) with dateModified", bool(wp and wp.get("dateModified")),
            f"{wp.get('@type')} modified {wp.get('dateModified')}" if wp else "none", "med", 1.5)
    rep.add("GEO", "Schema cites sources (citation[])", bool(wp and wp.get("citation")),
            f"{len(wp.get('citation', []))} citations" if wp else "", "low")
    rep.add("GEO", "Reviewer/author in schema (reviewedBy/author)", bool(wp and (wp.get("reviewedBy") or wp.get("author"))),
            "pending Dr Bodde's review" if wp else "", "info", 0)
    rep.add("SEO", "BreadcrumbList present", "BreadcrumbList" in types, "", "low", 0.5)
    faq = next((n for n in lds if isinstance(n, dict) and n.get("@type") == "FAQPage"), None)
    if faq:
        qs = [q.get("name", "") for q in faq.get("mainEntity", [])]
        missing = [q for q in qs if q.lower()[:25] not in main_text.lower()]
        rep.add("SEO", "FAQ schema matches visible questions", not missing, f"{len(qs)} Qs; not visible: {missing}", "high", 1.5)

    # GEO / AISO — content
    mw = words(main_text)
    first30 = " ".join(mw[: max(1, int(len(mw) * 0.30))]).lower()
    rep.add("GEO", "A10 · head term in first 30% of text", primary.lower() in first30, f"'{primary}'", "high", 3)
    defn = re.search(r"\b(is|are)\b (a|an|the)\b", " ".join(mw[:400]))
    rep.add("GEO", "A1 · definition sentence early ('X is a …')", bool(defn), defn.group(0) if defn else "", "high", 2)
    secondary = tgt.get("secondary", [])
    # An intent counts as covered when all its words occur in one sentence, in any order —
    # "the benefits of PDRN" answers "pdrn benefits". Exact-string matching penalised good prose.
    sentences = [x.lower() for x in re.split(r"(?<=[.!?])\s+", main_text)]
    hit = [s for s in secondary if any(all(w in sen for w in s.lower().split()) for sen in sentences)]
    rep.add("GEO", "A8 · secondary intents covered on the page", len(hit) == len(secondary), f"{hit} / {secondary}", "med", 1.5)
    paras = [re.sub(r"\s+", " ", p.text_content()).strip() for p in main.xpath(".//p")]
    paras = [p for p in paras if len(words(p)) >= 12]
    long = [p[:50] for p in paras if len(words(p)) > 120]
    rep.add("GEO", "A2 · atomic paragraphs (none > 120 words)", not long, f"{len(paras)} paragraphs, {len(long)} too long", "low")
    snippets = [p for p in paras if 35 <= len(words(p)) <= 70]
    rep.add("GEO", "F2 · snippet-sized answer blocks (35–70 words) ≥ 3", len(snippets) >= 3, f"{len(snippets)}", "low")
    nums = len(re.findall(r"\b\d+(?:[.,]\d+)?\s?(?:%|kDa|ppm|days|weeks|women|participants)", main_text))
    cites = len(re.findall(r"\bet al\.?,? \(?\d{4}|\(\d{4}\)|doi\.org|pubmed", main_text + " ".join(links), re.I))
    rep.add("GEO", "A3 · fact density (measured figures ≥ 5)", nums >= 5, f"{nums} figures", "med", 1.5)
    rep.add("GEO", "A3 · cited sources ≥ 3", cites >= 3, f"{cites} citation markers", "med", 1.5)
    years = [int(y) for y in re.findall(r"\b(20[12]\d)\b", main_text)]
    rep.add("GEO", "E3 · cites recent research (2024+)", any(y >= 2024 for y in years), f"latest {max(years) if years else '—'}", "low")
    date_vis = re.search(r"(last (reviewed|updated)|updated on|reviewed on)", main_text, re.I)
    rep.add("GEO", "E1 · visible last-reviewed/updated date", bool(date_vis), "pending reviewer sign-off" if not date_vis else date_vis.group(0), "med", 1.5)
    has_list = bool(main.xpath(".//ul/li|.//ol/li|.//table"))
    rep.add("GEO", "A6 · structured list or table present", has_list, "", "low", 0.5)
    q_h2 = [h for h in h2 if h.endswith("?")]
    rep.add("GEO", "A4 · headings mirror search questions", len(q_h2) >= 1 or any(primary.lower() in h.lower() for h in h2),
            f"{len(q_h2)} question-form H2", "low")

    # Extractability — what an AI crawler that does not run JS actually gets
    ext = trafilatura.extract(raw, include_tables=True, include_links=False, favor_recall=True) or ""
    ext_w = len(words(ext))
    rep.add("GEO", "D7 · extractable text without JavaScript ≥ 600 words", ext_w >= 600, f"{ext_w} words extracted (main text {len(mw)})", "high", 3)
    rep.add("GEO", "Head term survives extraction", primary.lower() in ext.lower(), "", "high", 2)
    # Navigation blocks (product carousels, "explore more" cards) are boilerplate that an
    # extractor is SUPPOSED to drop; only content headings must survive.
    NAV = re.compile(r"^(shop|explore|more|related|you may also|frequently asked)", re.I)
    lost = [h for h in h2 if h and not NAV.match(h) and h.lower()[:30] not in ext.lower()]
    rep.add("GEO", "H2 sections survive extraction", not lost, f"lost: {lost}" if lost else f"{len(h2)} kept", "med", 1.5)

    # Site-level, reported per page for completeness
    rep.add("GEO", "D1 · robots.txt allows the major AI crawlers", not site["blocked"],
            f"blocked: {site['blocked']}" if site["blocked"] else "all allowed", "high", 3)
    rep.add("SEO", "Page listed in XML sitemap", site["in_sitemap"](path), "", "med")
    rep.add("GEO", "llms.txt present (evidence: fetched 0× by frontier crawlers — not scored)", site["llms"], "", "info", 0)
    return {"title": title, "h1": h1, "h2": h2, "pseudo_headings": pseudo, "internal_links": internal,
            "external_links": external, "schema_types": types, "extracted_words": ext_w, "main_words": len(mw),
            "images": [{"src": i.get("src", ""), "alt": i.get("alt", "")} for i in imgs]}


def site_checks():
    _, _, robots = fetch(BASE + "/robots.txt")
    blocked = []
    groups = re.split(r"(?im)^user-agent:", robots)
    for bot in AI_BOTS:
        for g in groups:
            agents = [a.strip() for a in g.split("\n")[0].split(",")]
            if bot.lower() in [a.lower() for a in agents] and re.search(r"(?im)^disallow:\s*/\s*$", g):
                blocked.append(bot)
    _, _, sm = fetch(BASE + "/sitemap.xml")
    subs = re.findall(r"<loc>([^<]+)</loc>", sm)
    locs = set()
    for s in subs:
        if "sitemap" in s and s.endswith(".xml") or "sitemap" in s:
            _, _, x = fetch(s)
            locs |= set(re.findall(r"<loc>([^<]+)</loc>", x))
    st, _, _ = fetch(BASE + "/llms.txt")
    return {"blocked": blocked, "in_sitemap": lambda p: any(l.rstrip("/").endswith(p) for l in locs), "llms": st == 200}


# ------------------------------------------------------------------ Design (live browser)
DESIGN_JS = """() => {
  const sec=[...document.querySelectorAll('main .shopify-section')].filter(s=>s.id);
  const header=document.querySelector('[id*="__header"], header');
  const hb=header?header.getBoundingClientRect().bottom+scrollY:0;
  const rows=sec.map(s=>{const r=s.getBoundingClientRect(); const inner=s.querySelector('.section')||s;
    let bg=getComputedStyle(inner).backgroundColor; if(bg==='rgba(0, 0, 0, 0)') bg=getComputedStyle(s).backgroundColor;
    return {id:s.id.split('__').pop(), type:[...s.classList].find(c=>c.startsWith('shopify-section--'))?.slice(17),
            top:Math.round(r.top+scrollY), h:Math.round(r.height), bg, text:(s.innerText||'').trim().length,
            media:s.querySelectorAll('img,video,svg image').length}});
  const broken=[...document.querySelectorAll('main img')].filter(i=>i.complete&&i.naturalWidth===0).map(i=>i.src.slice(-60));
  const c=document.createElement('canvas').getContext('2d'); const wordBreaks=[];
  for(const h of document.querySelectorAll('main h1, main h2, main h3, main .h1, main .h2, main .h3')){
    const cs=getComputedStyle(h); c.font=`${cs.fontWeight} ${cs.fontSize} ${cs.fontFamily}`;
    const w=h.getBoundingClientRect().width;
    for(const word of (h.innerText||'').split(/\\s+/)){ if(word && c.measureText(word).width > w+1){ wordBreaks.push(word); } } }
  return {headerBottom:Math.round(hb), rows, broken, wordBreaks,
          overflow:document.documentElement.scrollWidth-window.innerWidth};
}"""


async def audit_design(path, rep, shots_dir):
    from playwright.async_api import async_playwright
    out = {}
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for name, vp in (("desktop", {"width": 1440, "height": 900}), ("mobile", {"width": 390, "height": 844})):
            ctx = await b.new_context(viewport=vp, reduced_motion="reduce", is_mobile=name == "mobile")
            pg = await ctx.new_page()
            await pg.goto(BASE + path, wait_until="domcontentloaded", timeout=60000)
            await pg.wait_for_timeout(2500)
            for sel in ['button:has-text("Accept")', 'button:has-text("Akzeptieren")']:
                try:
                    if await pg.locator(sel).first.is_visible(timeout=800):
                        await pg.locator(sel).first.click()
                except Exception:
                    pass
            h = await pg.evaluate("document.body.scrollHeight")
            for y in range(0, h, 500):
                await pg.evaluate(f"window.scrollTo(0,{y})"); await pg.wait_for_timeout(100)
            await pg.evaluate("window.scrollTo(0,0)"); await pg.wait_for_timeout(800)
            d = await pg.evaluate(DESIGN_JS)
            await pg.screenshot(path=str(shots_dir / f"{name}.png"), full_page=True)
            out[name] = d
        await b.close()
    d = out["desktop"]
    content = [r for r in d["rows"] if r["type"] not in ("footer",) and not (r["h"] == 0)]
    first = content[0] if content else None
    gap = (first["top"] - d["headerBottom"]) if first else 0
    rep.add("DESIGN", "No blank band between header and first section", gap <= 2, f"{gap}px", "high", 2)
    empty = [f"{r['id']} ({r['h']}px)" for r in d["rows"] if r["text"] < 2 and r["media"] == 0 and r["h"] > 4]
    rep.add("DESIGN", "No empty-but-tall sections", not empty, ", ".join(empty) or "none", "high", 2)
    seq = [r for r in content if r["type"] != "image-with-text-overlay"]
    same = [f"{a['id']}+{b['id']} ({PALETTE.get(a['bg'], a['bg'])})" for a, b in zip(seq, seq[1:])
            if a["bg"] == b["bg"] and not (a["type"] == "research-before-after" and b["type"] == "media-with-text")]
    rep.add("DESIGN", "Section backgrounds alternate", not same, "; ".join(same) or
            " → ".join(PALETTE.get(r["bg"], r["bg"]) for r in seq), "med", 1.5)
    off = sorted({r["bg"] for r in content if r["bg"] not in PALETTE})
    rep.add("DESIGN", "Backgrounds on the brand palette", not off, f"off-palette {off}" if off else "Bone / White / Graphite", "low")
    for name in ("desktop", "mobile"):
        o = out[name]
        rep.add("DESIGN", f"No horizontal overflow ({name})", o["overflow"] <= 0, f"{o['overflow']}px", "high", 1.5)
        rep.add("DESIGN", f"No broken images ({name})", not o["broken"], ", ".join(o["broken"]) or "none", "high", 1.5)
        rep.add("DESIGN", f"Headings never break mid-word ({name})", not o["wordBreaks"],
                ", ".join(sorted(set(o["wordBreaks"]))) or "none", "med" if name == "mobile" else "low", 1.5)
    return out


def write(path, rep, data, design, out_dir):
    slug = path.strip("/").replace("/", "-")
    day = dt.date.today().isoformat()
    out_dir.mkdir(parents=True, exist_ok=True)
    scores = {a: rep.score(a) for a in ("SEO", "GEO", "DESIGN", "MARKETING")}
    lines = [f"# Page audit — `{path}`", "", f"**Date:** {day} · **Tool:** `scripts/page-audit.py` · **Live:** {BASE}{path}", "",
             "| Area | Score |", "|---|---|"] + [f"| {a} | **{s}/100** |" for a, s in scores.items()] + [""]
    for area in ("SEO", "GEO", "DESIGN", "MARKETING"):
        lines += [f"## {area}", "", "| | Check | Detail |", "|---|---|---|"]
        for i in rep.items:
            if i["area"] != area:
                continue
            mark = "✅" if i["ok"] else {"high": "🔴", "med": "🟠", "low": "🟡", "info": "ℹ️"}[i["severity"]]
            lines.append(f"| {mark} | {i['check']} | {str(i['detail']).replace('|', '/')[:220]} |")
        lines.append("")
    lines += ["## Outline as served", "", f"- **H1:** {data.get('h1')}", f"- **H2:** {data.get('h2')}",
              f"- **Visual-only headings:** {data.get('pseudo_headings')}", f"- **Schema types:** {data.get('schema_types')}",
              f"- **Extracted words (no JS):** {data.get('extracted_words')} of {data.get('main_words')}", "",
              "## Section map (desktop)", "", "| Top | Height | Section | Type | Background |", "|---|---|---|---|---|"]
    for r in design["desktop"]["rows"]:
        lines.append(f"| {r['top']} | {r['h']} | {r['id']} | {r['type']} | {PALETTE.get(r['bg'], r['bg'])} |")
    (out_dir / f"{slug}-{day}.md").write_text("\n".join(lines) + "\n")
    (out_dir / f"{slug}-{day}.json").write_text(json.dumps({"path": path, "scores": scores, "items": rep.items,
                                                            "data": data, "design": design}, indent=1, default=str))
    return scores


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--out", default="docs/audits/pages")
    a = ap.parse_args()
    site = site_checks()
    for path in a.paths:
        rep = Report()
        data = audit_html(path, rep, site)
        shots = pathlib.Path("/tmp") / ("audit-" + path.strip("/").replace("/", "-"))
        shots.mkdir(exist_ok=True)
        design = asyncio.run(audit_design(path, rep, shots))
        scores = write(path, rep, data, design, ROOT / a.out)
        fails = [i for i in rep.items if not i["ok"] and i["severity"] != "info"]
        print(f"\n  {path}   SEO {scores['SEO']} · GEO {scores['GEO']} · DESIGN {scores['DESIGN']} · MARKETING {scores['MARKETING']}   ({len(fails)} findings)")
        if scores["MARKETING"] is not None and scores["MARKETING"] < MKT["threshold"]:
            print(f"    ⚠ MARKETING below {MKT['threshold']}: strengthen the claims — run the claims research (docs/claims/) before rewording")
        for i in sorted(fails, key=lambda x: {"high": 0, "med": 1, "low": 2}[x["severity"]]):
            print(f"    {i['severity']:<4} {i['area']:<9} {i['check']} — {str(i['detail'])[:110]}")
        print(f"    screenshots: {shots}/desktop.png, mobile.png")
    return 0


if __name__ == "__main__":
    sys.exit(main())
