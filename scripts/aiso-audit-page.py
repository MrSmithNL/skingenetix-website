#!/usr/bin/env python3
"""Dual-model SEO+AISO page audit (ChatGPT + Gemini), per the seo-aiso-validator skill.

Scores the trafilatura-extracted content (what AI crawlers see) against the skill's
20 criteria, with the documented prompt fixes: meta tags injected (stripped from
extraction by definition), today's date injected (Gemini date-blindness), page-type
context. Prints the combined score table and writes a markdown report.

    python3 scripts/aiso-audit-page.py <url> [--round N]

Keys: OPENAI_API_KEY + GOOGLE_API_KEY from ~/Claude Code/Projects/seo-toolkit/.env

Skingenetix copy (2026-09-22), adapted from hairgenetix/scripts/aiso-audit-page.py:
  * the brand's own domain is read from the URL, not hardcoded (the original excluded
    "hairgenetix" from the external-link count, so every skingenetix link counted as external);
  * scope is <main> when there is no <article> — Shopify pages on Impact have no <article>;
  * report goes to docs/audits/pages/aiso-<slug>-<locale>-<date>-r<N>.md;
  * page type "ymyl-hub" for ingredient research hubs (scientific YMYL).
  ⚠️ Two copies now exist. Centralise into the seo-aiso-validator skill (logged in docs/todo.md).
"""

import argparse
import datetime
import json
import pathlib
import re
import time
import urllib.error
import urllib.request
from urllib.parse import urlparse

ROOT = pathlib.Path(__file__).resolve().parent.parent
ENV = pathlib.Path.home() / "Claude Code/Projects/seo-toolkit/.env"

CRITERIA = [
    "Answer-first format",
    "Definition paragraph",
    "Heading hierarchy",
    "Atomic paragraphs",
    "Fact density",
    "Comparison content",
    "List/table format",
    "Content depth",
    "Front-loading",
    "Multi-modal",
    "Schema markup",
    "FAQ section",
    "Citation quality",
    "Internal linking",
    "Meta optimization",
    "Author attribution",
    "Medical/expert review",
    "Recency",
    "Brand mention readiness",
    "AI citation readiness",
]


def env_keys():
    keys = {}
    for line in ENV.read_text().splitlines():
        if "=" in line and not line.strip().startswith("#"):
            k, v = line.split("=", 1)
            keys[k.strip()] = v.strip()
    return keys


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; GPTBot/1.0)"})
    return urllib.request.urlopen(req).read().decode()


def heading_outline(html):
    m = re.search(r"<article.*?</article>", html, re.S) or re.search(r"<main.*?</main>", html, re.S)
    scope = m.group(0) if m else html
    out = []
    for tag, txt in re.findall(r"<(h[1-4])[^>]*>(.*?)</\1>", scope, re.S):
        clean = re.sub(r"<[^>]+>", "", txt).strip()
        if clean:
            out.append(f"{tag.upper()}: {clean[:90]}")
    return "\n".join(out[:40])


PAGE_TYPE_CONTEXT = {
    "article": "PAGE TYPE: blog article with YMYL (scientific/health) characteristics. Score all 20 criteria at full weight.",
    "ymyl-hub": (
        "PAGE TYPE: ingredient research hub on a skincare brand's store (scientific YMYL). Citations and "
        "authority are REQUIRED. The page must define the ingredient up front, grade the evidence honestly "
        "(manufacturer vs independent data, lab vs human), and link to products and sibling hubs. Score all "
        "20 criteria at full weight."
    ),
    "product": (
        "PAGE TYPE: e-commerce product page. Adjust expectations accordingly: Product JSON-LD schema is "
        "REQUIRED for criterion 11. Criterion 13 (citation quality): PubMed-style references are NOT "
        "expected on a product page; score 9-10 if claims link out to the site's science/research pages, "
        "lower only if health claims have no evidence path at all. Criteria 16-17 (author/reviewer): "
        "brand accountability and reviewer signals suffice; do not demand an article-style byline. "
        "Criterion 6 (comparison) and 12 (FAQ) are high-value for product pages."
    ),
}


def build_prompt(url, extracted, schemas, meta_title, meta_desc, today, outline="", link_count=0, ext_count=0, page_type="article"):
    page_type_context = PAGE_TYPE_CONTEXT[page_type]
    crit_lines = "\n".join(f"{i + 1}. {c}" for i, c in enumerate(CRITERIA))
    return f"""You are an expert SEO and AI search optimization (AISO) auditor. Be precise and quantitative.

TODAY'S DATE IS {today}. Dates on or before this date are valid past/present dates, NOT future errors.

{page_type_context}

IMPORTANT CONTEXT: The content below was extracted with Trafilatura, the same extraction
library used by AI training pipelines. This is EXACTLY what AI crawlers see after boilerplate
removal. Score ONLY what is present in the extracted content, EXCEPT criterion 15 (meta
optimization), which must be scored from the META TAGS section below (meta tags live in <head>
and are stripped from extraction by definition).

URL: {url}
JSON-LD schemas on the page: {schemas}

--- META TAGS (for criterion 15) ---
Meta title ({len(meta_title)} chars): {meta_title}
Meta description ({len(meta_desc)} chars): {meta_desc}
--- END META TAGS ---

--- HEADING OUTLINE from raw HTML (for criterion 3; extraction flattens heading levels) ---
{outline}
--- END HEADING OUTLINE ---

FACT (measured from raw HTML, use for criterion 14): the article body contains {link_count}
in-content internal links to other pages on this site, plus {ext_count} external reference links.

--- EXTRACTED CONTENT (what AI crawlers see) ---
{extracted}
--- END EXTRACTED CONTENT ---

Score each criterion 1-10 (10 = perfect). Scoring rubric notes:
- Criterion 4 (Atomic paragraphs): score 10 if all paragraphs are 2-5 sentences; 9 if at least
  90% are; 8 only if many run 6+ sentences. Bullet lists do not count as long paragraphs.
- Criterion 14 (Internal linking): markdown links [text](/path) in the extraction ARE internal
  links; count them.
- Criterion 18 (Recency): a "Last updated" date within 6 months of today scores 9-10.

The criteria:
{crit_lines}

Respond with ONLY valid JSON in this exact shape:
{{"scores": [{{"n": 1, "criterion": "Answer-first format", "score": 9, "note": "...", "fix": "..."}} , ... 20 items],
 "overall": 0.0, "top_fixes": ["...", "...", "..."], "assessment": "one paragraph"}}"""


def call_openai(key, prompt):
    body = json.dumps(
        {
            "model": "gpt-4o",
            "messages": [{"role": "user", "content": prompt}],
            "response_format": {"type": "json_object"},
            "max_tokens": 4096,
        }
    ).encode()
    req = urllib.request.Request("https://api.openai.com/v1/chat/completions", data=body, headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    r = json.load(urllib.request.urlopen(req))
    return json.loads(r["choices"][0]["message"]["content"])


def call_gemini(key, prompt):
    body = json.dumps(
        {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"maxOutputTokens": 24576, "responseMimeType": "application/json"},
        }
    ).encode()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={key}"
    for attempt in range(5):
        try:
            req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
            r = json.load(urllib.request.urlopen(req))
            return json.loads(r["candidates"][0]["content"]["parts"][0]["text"])
        except urllib.error.HTTPError as e:
            if e.code in (429, 503) and attempt < 4:
                time.sleep(2**attempt)
                continue
            raise


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--round", type=int, default=1)
    ap.add_argument("--page-type", choices=["article", "ymyl-hub", "product"], default="ymyl-hub")
    ap.add_argument("--html", help="audit a saved HTML file (e.g. a pre-publish preview) instead of fetching the URL")
    args = ap.parse_args()

    import trafilatura

    html = pathlib.Path(args.html).read_text() if args.html else fetch(args.url)
    extracted = trafilatura.extract(html, include_tables=True, include_images=True, output_format="markdown") or ""
    extracted = extracted[:60000]
    schemas = sorted(set(re.findall(r'"@type":\s*"([A-Za-z]+)"', html)))
    mt = re.search(r"<title[^>]*>(.*?)</title>", html, re.S)
    md = re.search(r'<meta name="description" content="([^"]*)"', html)
    meta_title = mt.group(1).strip() if mt else ""
    meta_desc = md.group(1) if md else ""
    today = datetime.date.today().isoformat()

    keys = env_keys()
    art = re.search(r"<article.*?</article>", html, re.S) or re.search(r"<main.*?</main>", html, re.S)
    scope = art.group(0) if art else html
    own = re.sub(r"^www\\.", "", urlparse(args.url).netloc).split(".")[0]
    link_count = len(set(re.findall(r'<a[^>]+href="(/(?:blogs|products|pages|collections)/[^"#?]*)"', scope)))
    ext_count = len(set(re.findall(rf'<a[^>]+href="(https?://(?!(?:www\\.)?{own})[^"]+)"', scope)))
    prompt = build_prompt(args.url, extracted, schemas, meta_title, meta_desc, today, outline=heading_outline(html), link_count=link_count, ext_count=ext_count, page_type=args.page_type)
    gpt = call_openai(keys["OPENAI_API_KEY"], prompt)
    gem = call_gemini(keys.get("GOOGLE_API_KEY") or keys["GOOGLE_AI_API_KEY"], prompt)

    rows, gsum, msum = [], 0.0, 0.0
    for i, c in enumerate(CRITERIA):
        g = next((s for s in gpt["scores"] if s["n"] == i + 1), {})
        m = next((s for s in gem["scores"] if s["n"] == i + 1), {})
        gs, ms = float(g.get("score", 0)), float(m.get("score", 0))
        gsum += gs
        msum += ms
        avg = (gs + ms) / 2
        flag = "PASS" if min(gs, ms) >= 9 else ("avg-ok" if avg >= 9 else "FAIL")
        rows.append((i + 1, c, gs, ms, avg, flag, g.get("fix", ""), m.get("fix", "")))

    overall = (gsum + msum) / (2 * len(CRITERIA))
    slug = args.url.split("?")[0].rstrip("/").split("/")[-1]
    path = urlparse(args.url).path.strip("/").split("/")
    loc = path[0] if path and len(path[0]) == 2 else "en"
    lines = [
        f"# Page audit round {args.round} — {slug}",
        f"\nDate: {today} · URL: {args.url}",
        f"\n**ChatGPT overall: {gsum / len(CRITERIA):.2f} · Gemini overall: {msum / len(CRITERIA):.2f} · Combined: {overall:.2f}** (pass ≥ 9.0)\n",
        "| # | Criterion | GPT | Gem | Avg | Status |",
        "|---|---|---|---|---|---|",
    ]
    for n, c, gs, ms, avg, flag, gf, mf in rows:
        lines.append(f"| {n} | {c} | {gs:.0f} | {ms:.0f} | {avg:.1f} | {flag} |")
    lines.append("\n## Fixes suggested (criteria below 9 on either model)\n")
    for n, c, gs, ms, avg, flag, gf, mf in rows:
        if min(gs, ms) < 9:
            lines.append(f"- **{c}** (GPT {gs:.0f}: {gf or '-'}) (Gem {ms:.0f}: {mf or '-'})")
    lines.append(f"\nGPT top fixes: {gpt.get('top_fixes')}\nGemini top fixes: {gem.get('top_fixes')}")
    lines.append(f"\nGPT assessment: {gpt.get('assessment', '')}\n\nGemini assessment: {gem.get('assessment', '')}")
    import textwrap

    lines = [line if len(line) <= 300 or line.startswith("|") else textwrap.fill(line, width=280, subsequent_indent="  ") for line in lines]
    out = ROOT / "docs" / "audits" / "pages" / f"aiso-{slug}-{loc}-{today}-r{args.round}.md"
    (out.with_suffix(".json")).write_text(json.dumps({"gpt": gpt, "gemini": gem, "combined": overall}, indent=1, ensure_ascii=False))
    out.write_text("\n".join(lines))
    print("\n".join(lines[:30]))
    print(f"\nreport: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
