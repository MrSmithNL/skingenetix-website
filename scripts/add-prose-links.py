#!/usr/bin/env python3
"""Append in-prose links to existing rich-text settings in theme JSON templates.

Author: Claude (Opus 5) for Malcolm Smith · 2026-09-22
Purpose: Phase 1 item 4 of docs/content-plan-2026.md — join the concern pages and
the ingredient research hubs, which linked only within their own family.

    python3 scripts/add-prose-links.py configs/link-changes/phase1-links-2026-09-22.json            # dry run
    python3 scripts/add-prose-links.py configs/link-changes/phase1-links-2026-09-22.json --apply
    python3 scripts/add-prose-links.py configs/link-changes/phase1-links-2026-09-22.json --verify-live
    python3 scripts/add-prose-links.py SPEC --rollback            # restores from the backups this run wrote

Spec entry: {"file": "templates/page.x.json", "at": "section/block/setting", "href": "...", "html": "<p>...</p>"}

Rules it enforces:
  * Only EXISTING settings in EXISTING sections are touched — the standard-sections-first rule.
  * Idempotent: an entry whose href is already in that setting is skipped, so a re-run never doubles a link.
  * The file's leading /* ... */ header comment (Shopify-generated) is preserved.
  * Never inside a table — a link in a table collapses it in AI extraction (sister-brand finding HG-159).
  * Every touched file is backed up to backups/ before upload.
"""
import argparse, datetime as dt, html as H, importlib.util, json, pathlib, re, sys, time, urllib.error, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://www.skingenetix.com"
THEME = "gid://shopify/OnlineStoreTheme/184835965313"

_s = importlib.util.spec_from_file_location("uti", ROOT / "scripts/upload-theme-images.py")
_uti = importlib.util.module_from_spec(_s); _s.loader.exec_module(_uti)
_env = _uti.env(); STORE = _env["SHOPIFY_SKINGENETIX_STORE"]; TOKEN = _uti.token(_env)


def gql(query, variables=None):
    r = urllib.request.Request(f"https://{STORE}/admin/api/2025-07/graphql.json",
                               data=json.dumps({"query": query, "variables": variables or {}}).encode(),
                               method="POST", headers={"X-Shopify-Access-Token": TOKEN,
                                                       "Content-Type": "application/json"})
    d = json.loads(urllib.request.urlopen(r, timeout=120).read())
    if d.get("errors"):
        raise RuntimeError(json.dumps(d["errors"])[:400])
    return d["data"]


def read_files(names):
    d = gql('query($id:ID!,$f:[String!]!){ theme(id:$id){ files(filenames:$f){ nodes{ filename '
            'body{ ... on OnlineStoreThemeFileBodyText{ content } } } } } }', {"id": THEME, "f": names})
    return {n["filename"]: n["body"]["content"] for n in d["theme"]["files"]["nodes"]}


def split(raw):
    m = re.match(r"\s*(/\*.*?\*/)\s*", raw, re.S)
    return (m.group(1) if m else ""), json.loads(raw[m.end():] if m else raw)


def locate(j, at):
    sec, blk, key = at.split("/")
    block = j["sections"][sec]["blocks"][blk]["settings"]
    if key not in block:
        raise KeyError(f"{at}: setting does not exist — this tool only edits existing settings")
    return block, key


def page_for(file):
    suffix = file.split("templates/page.", 1)[1].rsplit(".json", 1)[0]
    pages = gql('{ pages(first:100){ nodes{ handle templateSuffix } } }')["pages"]["nodes"]
    return [p["handle"] for p in pages if p["templateSuffix"] == suffix]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--verify-live", action="store_true")
    ap.add_argument("--rollback", action="store_true")
    a = ap.parse_args()
    spec = json.loads(pathlib.Path(a.spec).read_text())["links"]
    files = sorted({e["file"] for e in spec})
    stem = pathlib.Path(a.spec).stem

    if a.rollback:
        up = []
        for f in files:
            bk = sorted(ROOT.glob(f"backups/{stem}-{f.replace('/', '__')}-*.json"))
            if not bk:
                sys.exit(f"  no backup for {f}")
            up.append({"filename": f, "body": {"type": "TEXT", "value": bk[-1].read_text()}})
        r = gql('mutation($t:ID!,$f:[OnlineStoreThemeFilesUpsertFileInput!]!){ themeFilesUpsert(themeId:$t, files:$f)'
                '{ userErrors{field message} } }', {"t": THEME, "f": up})["themeFilesUpsert"]
        print("  rollback:", r["userErrors"] or f"{len(up)} files restored")
        return 0

    if a.verify_live:
        bad = 0
        for e in spec:
            for h in page_for(e["file"]):
                url = f"{BASE}/pages/{h}?linkcheck={int(time.time())}"
                for attempt in range(6):
                    try:
                        page = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}),
                                                      timeout=40).read().decode("utf-8", "ignore"); break
                    except urllib.error.HTTPError as ex:
                        if ex.code not in (429, 503) or attempt == 5: raise
                        time.sleep(10 * (attempt + 1))
                main_ = re.search(r"<main[^>]*>(.*)</main>", page, re.S)
                body = main_.group(1) if main_ else page
                anchor = re.search(r'<a href="%s">(.*?)</a>' % re.escape(e["href"]), e["html"]).group(1)
                text = re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", body)))
                ok = f'href="{e["href"]}"' in body and re.sub(r"\s+", " ", anchor) in text
                bad += not ok
                print(f"  {'✓' if ok else '✗'} /pages/{h:<34} → {e['href']:<38} “{anchor}”")
                time.sleep(1.5)
        print(f"\n  {'all links live' if not bad else str(bad) + ' missing'}")
        return 1 if bad else 0

    raw = read_files(files)
    docs = {f: split(raw[f]) for f in files}
    changes = 0
    for e in spec:
        if "<table" in e["html"]:
            sys.exit(f"  ✗ {e['at']}: links inside tables are not allowed")
        _hdr, j = docs[e["file"]]
        block, key = locate(j, e["at"])
        if e["href"] in block[key]:
            print(f"  = {e['file']} {e['at']}: already links {e['href']} — skipped")
            continue
        block[key] = block[key].rstrip() + e["html"]
        changes += 1
        print(f"  + {e['file']:<44} {e['at']:<32} → {e['href']}")
    print(f"\n  {changes} link(s) to add across {len(files)} file(s)")
    if not a.apply or not changes:
        print("  dry run — nothing written." if not a.apply else "  nothing to do.")
        return 0

    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    up = []
    for f in files:
        (ROOT / f"backups/{stem}-{f.replace('/', '__')}-{stamp}.json").write_text(raw[f])
        hdr, j = docs[f]
        body = (hdr + "\n" if hdr else "") + json.dumps(j, indent=2, ensure_ascii=False)
        up.append({"filename": f, "body": {"type": "TEXT", "value": body}})
    r = gql('mutation($t:ID!,$f:[OnlineStoreThemeFilesUpsertFileInput!]!){ themeFilesUpsert(themeId:$t, files:$f)'
            '{ upsertedThemeFiles{ filename } userErrors{field message} } }', {"t": THEME, "f": up})["themeFilesUpsert"]
    if r["userErrors"]:
        print("  ✗", r["userErrors"]); return 1
    after = read_files(files)
    missing = [(e["file"], e["href"]) for e in spec if e["href"] not in json.dumps(split(after[e["file"]])[1])]
    print(f"  uploaded {len(up)} files · backups stamped {stamp} · read-back missing: {missing or 'none'}")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
