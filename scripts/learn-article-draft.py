#!/usr/bin/env python3
"""Publish or update a Learn spoke as a hidden English draft article, from configs/learn/drafts/<handle>.json.

Author: Claude (Fable 5.1) for Malcolm Smith · 2026-10-08
Why: the Learn spokes (docs/content-plan-2026.md §5; plan step 1.6) are plain articles on the stock Impact
article template, not trial appraisals, so the study template and its 40-field metaobject do not fit. The
English draft goes to the hidden drafts blog (`clinical-studies-drafts`, seo.hidden=1, the same route the
study articles use), where the central auditor and Malcolm can see it; on his approval the same config is
published into /blogs/learn with --blog learn, measured 14 days, then translated.

    python3 scripts/learn-article-draft.py configs/learn/drafts/<handle>.json            # dry run: checks only
    python3 scripts/learn-article-draft.py configs/learn/drafts/<handle>.json --apply    # hidden draft
    python3 scripts/learn-article-draft.py configs/learn/drafts/<handle>.json --apply --blog learn --public

Config keys: handle, title (H1 shown by the theme), seo_title (<=60), seo_description (<=155), summary, tags,
body_html (h2/p/ul/li/strong/a/table only). The theme's stock article template renders the title as the H1 and
the body as the content, so the body must not repeat the H1. Author is the team credit (ADR-2026-10-08-W).
"""
import argparse, importlib.util, json, pathlib, re, sys, time

ROOT = pathlib.Path(__file__).resolve().parent.parent
TEAM = "Skingenetix Research Team"
DRAFTS_BLOG = "clinical-studies-drafts"


def _load(name, path):
    s = importlib.util.spec_from_file_location(name, ROOT / path)
    m = importlib.util.module_from_spec(s)
    argv, sys.argv = sys.argv, [sys.argv[0]]
    s.loader.exec_module(m)
    sys.argv = argv
    return m


gql = _load("hu", "scripts/hub-upgrade.py").gql


def check(cfg):
    errs = []
    if len(cfg["seo_title"]) > 60:
        errs.append(f"seo_title {len(cfg['seo_title'])} > 60")
    if len(cfg["seo_description"]) > 155:
        errs.append(f"seo_description {len(cfg['seo_description'])} > 155")
    body = cfg["body_html"]
    if "<h1" in body:
        errs.append("body carries an <h1>; the theme renders the title as the H1")
    bad = set(re.findall(r"<(?!/?(?:h2|h3|p|ul|ol|li|strong|em|a|table|thead|tbody|tr|th|td|br)\b)[a-z]+", body))
    if bad:
        errs.append(f"tags outside the allowed set: {sorted(bad)}")
    words = len(re.sub(r"<[^>]+>", " ", body).split())
    if not 800 <= words <= 1500:
        errs.append(f"{words} words; the spokes run 800 to 1,500")
    for word in ("synergy", "clinically proven", "Botox", "relaxes muscle", "safe for sensitive", "penetrates deep", "stimulates collagen", "repairs"):
        if word.lower() in body.lower():
            errs.append(f"forbidden wording: {word}")
    return errs, words


def blog_id(handle):
    for n in gql('query{ blogs(first:50){ nodes{ id handle } } }')["blogs"]["nodes"]:
        if n["handle"] == handle:
            return n["id"]
    sys.exit(f"  ✗ no blog {handle}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--blog", default=DRAFTS_BLOG)
    ap.add_argument("--public", action="store_true", help="indexable (no seo.hidden); only with --blog learn on Malcolm's approval")
    a = ap.parse_args()
    cfg = json.loads(pathlib.Path(a.config).read_text())
    errs, words = check(cfg)
    # 2026-10-09: spoke 1 went public with "DRAFT for Malcolm:" still in its summary, which the Learn list shows as the
    # excerpt; a note meant for the reviewer must never reach a public article
    if a.public and re.search(r"\bDRAFT\b|for Malcolm", " ".join(str(cfg.get(k, "")) for k in ("summary", "title", "seo_title", "seo_description"))):
        errs.append("a reviewer note (DRAFT / for Malcolm) is still in the summary, title or SEO fields; remove it before --public")
    for e in errs:
        print("  ✗", e)
    print(f"  {cfg['handle']}: {words} words, seo title {len(cfg['seo_title'])}, description {len(cfg['seo_description'])}")
    if errs:
        return 1
    if not a.apply:
        print("  dry run; add --apply")
        return 0
    art = {"title": cfg["title"], "summary": cfg["summary"], "body": cfg["body_html"], "tags": cfg.get("tags", []),
           "author": {"name": TEAM}, "templateSuffix": "", "isPublished": True,
           "metafields": [{"namespace": "global", "key": "title_tag", "type": "single_line_text_field", "value": cfg["seo_title"]},
                          {"namespace": "global", "key": "description_tag", "type": "multi_line_text_field", "value": cfg["seo_description"]}]}
    if not a.public:
        art["metafields"].append({"namespace": "seo", "key": "hidden", "type": "number_integer", "value": "1"})
    found = [x for x in gql('query($q:String!){ articles(first:10, query:$q){ nodes{ id handle blog{ handle } } } }', {"q": f"handle:{cfg['handle']}"})["articles"]["nodes"] if x["handle"] == cfg["handle"] and x["blog"]["handle"] == a.blog]
    if found:
        r = gql('mutation($id:ID!,$a:ArticleUpdateInput!){ articleUpdate(id:$id, article:$a){ article{ id } userErrors{ field message } } }', {"id": found[0]["id"], "a": art})["articleUpdate"]
    else:
        r = gql('mutation($a:ArticleCreateInput!){ articleCreate(article:$a){ article{ id } userErrors{ field message } } }', {"a": {**art, "blogId": blog_id(a.blog), "handle": cfg["handle"]}})["articleCreate"]
    if r["userErrors"]:
        sys.exit(f"  ✗ {r['userErrors']}")
    time.sleep(1)
    print(f"  ✓ article {'updated' if found else 'created'} in /blogs/{a.blog}/ ({'public' if a.public else 'hidden'}): https://www.skingenetix.com/blogs/{a.blog}/{cfg['handle']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
