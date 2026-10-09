"""Deep measurement of the top-3 organic results for the 2026-10-09 new-article keywords.

Reads audits/2026-10-09-new-article-keywords/serp/serp.json; writes teardowns/measurements.jsonl (one row per
keyword x position, top 3 positions literally, UGC and video included and described rather than measured).
Fields beyond serp_gap.py `pages`: H1 and H2/H3 text, first 80 words of main text, author / reviewer / medical
review lines, visible and JSON-LD dates, citations (PubMed/PMC/DOI/journal domains), named studies, schema types,
tables, FAQ blocks, video embeds, product links and prices, mentions of the ingredients we sell, Botox/filler
mentions, before/after imagery, and the page's angle words. Scratch tool for the article plan.
"""
import json, re, subprocess, sys, pathlib, time, html
import trafilatura
from lxml import html as LH

D = pathlib.Path("/Users/malcolmsmith/Claude Code/Projects/skingenetix-website/audits/2026-10-09-new-article-keywords")
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
PAIRS = sys.argv[1].split("|")
UGC = ("reddit.com", "youtube.com", "instagram.com", "facebook.com", "tiktok.com", "quora.com")
OURS = re.compile(r"pdrn|polynucleotide|copper peptide|ghk|argireline|acetyl hexapeptide|matrixyl|glutathione|peptide", re.I)
CITE = re.compile(r"pubmed|ncbi\.nlm|pmc\.|doi\.org|onlinelibrary\.wiley|sciencedirect|springer|jamanetwork|mdpi\.com|nature\.com|tandfonline|karger|jaad\.org|jcadonline|frontiersin", re.I)


def fetch(url):
    try:
        p = subprocess.run(["curl", "-sL", "-m", "25", "-A", UA, "-H", "Accept-Language: en", "-w", "\n%{http_code}", url],
                           capture_output=True, timeout=40)
        body = p.stdout.decode("utf-8", "replace")
        body, _, code = body.rpartition("\n")
        return body, code
    except Exception as e:
        return "", f"ERR {e}"


def measure(url, raw):
    doc = LH.fromstring(raw) if raw.strip() else None
    out = {}
    if doc is None:
        return out
    t = lambda xp: [re.sub(r"\s+", " ", x.text_content()).strip() for x in doc.xpath(xp)]
    out["title"] = (t("//title") or [""])[0][:140]
    out["h1"] = [x for x in t("//h1") if x][:3]
    out["h2"] = [x[:90] for x in t("//h2") if x][:25]
    out["h3_count"] = len(doc.xpath("//h3"))
    text = trafilatura.extract(raw, include_tables=True, favor_recall=True) or ""
    out["words"] = len(text.split())
    out["first_words"] = " ".join(text.split()[:80])
    low = raw.lower()
    out["tables"] = len(doc.xpath("//table"))
    out["faq"] = bool(re.search(r"faqpage|frequently asked|>faq<|faqs", low))
    out["video"] = bool(re.search(r"youtube\.com/embed|player\.vimeo|<video", low))
    types = re.findall(r'"@type"\s*:\s*"([^"]+)"', raw)
    out["schema"] = sorted(set(types))[:15]
    out["date_modified"] = (re.findall(r'"dateModified"\s*:\s*"([^"]+)"', raw) or [None])[0]
    out["date_published"] = (re.findall(r'"datePublished"\s*:\s*"([^"]+)"', raw) or [None])[0]
    m = re.search(r"(medically reviewed by|reviewed by|written by|by dr\.?|author:?)\s*([A-Z][^<\n]{2,60})", re.sub(r"<[^>]+>", " ", raw), re.I)
    out["byline"] = (m.group(1) + " " + m.group(2)).strip()[:90] if m else None
    links = doc.xpath("//a/@href")
    out["citations"] = len({l for l in links if CITE.search(l or "")})
    out["named_studies"] = len(re.findall(r"\bet al\.?|\(\d{4}\)|study (published|in|by)|randomi[sz]ed|clinical trial|double-blind|placebo", text, re.I))
    out["product_links"] = len({l for l in links if re.search(r"/products?/|/shop/|add-to-cart|/p/", l or "")})
    out["price"] = bool(re.search(r"[$£€]\s?\d", text))
    out["mentions_ours"] = sorted({m.lower() for m in OURS.findall(text)})
    out["botox_filler"] = len(re.findall(r"botox|filler|injectable|neurotoxin|dysport", text, re.I))
    out["before_after"] = bool(re.search(r"before (and|&) after", text, re.I))
    out["topical_mentions"] = len(re.findall(r"retinol|retinoid|tretinoin|peptide|vitamin c|hyaluronic|sunscreen|spf", text, re.I))
    return out


rows = json.load(open(D / "serp/serp.json"))["rows"]
done = set()
outp = D / "teardowns/measurements.jsonl"
outp.parent.mkdir(exist_ok=True)
if outp.exists():
    for l in outp.read_text().splitlines():
        r = json.loads(l); done.add((r["market"], r["q"], r["rank"]))
with open(outp, "a") as f:
    for r in rows:
        key = f"{r['market']}:{r['q']}"
        if key not in PAIRS:
            continue
        for o in r["organic"][:3]:
            if (r["market"], r["q"], o["rank"]) in done:
                continue
            row = {"market": r["market"], "q": r["q"], "rank": o["rank"], "domain": o["domain"], "url": o["url"], "serp_title": o["title"]}
            if any(u in o["domain"] for u in UGC):
                row["kind"] = "UGC/video"
            else:
                raw, code = fetch(o["url"])
                row["http"] = code
                row.update(measure(o["url"], raw))
                time.sleep(1.0)
            f.write(json.dumps(row, ensure_ascii=False) + "\n"); f.flush()
            print(f"{key:<45} #{o['rank']} {o['domain']:<30} words={row.get('words')} h2={len(row.get('h2', []))} cites={row.get('citations')} by={row.get('byline')}")
