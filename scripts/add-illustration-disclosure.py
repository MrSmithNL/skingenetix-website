#!/usr/bin/env python3
"""Add the text disclosure to every AI-generated before/after finding block.

⛔ DO NOT RUN. Malcolm, 2026-09-22: "No AI disclosure please." Applied and reverted the same
day (English restored from backups/, 30 locale translations restored). Kept only as the record
of what was tried and how it was undone.

Author: Claude (Opus 5) for Malcolm Smith · 2026-09-22

    python3 scripts/add-illustration-disclosure.py            # dry run
    python3 scripts/add-illustration-disclosure.py --apply
    python3 scripts/add-illustration-disclosure.py --verify-live

Why: on 2026-08-27 Malcolm had the "Illustration" pill removed from these images
(scripts/clear-before-after-note-label.py) and asked for the disclosure to move
into the copy — "lets fix it in the text later though". It never was. Every one
of these diptychs is AI-generated and sits beside a real number from a real
paper, so without the line a reader takes it as a photograph from the study.

What it does: appends one italic line under the citation in each
research-before-after block's `content`, in English, and appends the matching
line to each locale's EXISTING translation, registered against the new digest so
Translate & Adapt marks it current. Idempotent — a block that already carries the
line is skipped. Section JSON only; no Liquid (.claude/rules/shopify.md rule 2).
"""
import argparse, datetime as dt, importlib.util, json, pathlib, re, sys, time, urllib.error, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
THEME = "gid://shopify/OnlineStoreTheme/184835965313"
BASE = "https://www.skingenetix.com"
TEMPLATES = {"page.pdrn-research.json": "pdrn-research",
             "page.research-argireline.json": "acetyl-hexapeptide-8-research",
             "page.glutathione-research.json": "glutathione-research"}
LINE = {
    "en": "Image: an illustration of this finding, not a photograph from a study.",
    "de": "Bild: eine Illustration dieses Ergebnisses, kein Studienfoto.",
    "nl": "Afbeelding: een illustratie van deze bevinding, geen foto uit onderzoek.",
    "fr": "Image : une illustration de ce résultat, et non une photo d'étude.",
    "es": "Imagen: una ilustración de este resultado, no una foto de un estudio.",
    "it": "Immagine: un'illustrazione di questo risultato, non una foto di uno studio.",
}

_s = importlib.util.spec_from_file_location("uti", ROOT / "scripts/upload-theme-images.py")
_uti = importlib.util.module_from_spec(_s); _s.loader.exec_module(_uti)
_env = _uti.env(); STORE = _env["SHOPIFY_SKINGENETIX_STORE"]; TOKEN = _uti.token(_env)


def gql(query, variables=None):
    r = urllib.request.Request(f"https://{STORE}/admin/api/2025-07/graphql.json",
                               data=json.dumps({"query": query, "variables": variables or {}}).encode(),
                               method="POST", headers={"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"})
    d = json.loads(urllib.request.urlopen(r, timeout=120).read())
    if d.get("errors"):
        raise RuntimeError(json.dumps(d["errors"])[:400])
    return d["data"]


def line_html(loc):
    return f"<p><em>{LINE[loc]}</em></p>"


def has_line(html, loc):
    return LINE[loc] in html


def targets(j):
    for sid, sec in j["sections"].items():
        if sec["type"] != "research-before-after" or sec.get("disabled"):
            continue
        for bid, b in sec["blocks"].items():
            if b["settings"].get("image"):
                yield sid, bid, b["settings"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--verify-live", action="store_true")
    a = ap.parse_args()
    L = [l for l in LINE if l != "en"]

    if a.verify_live:
        bad = 0
        for tpl, handle in TEMPLATES.items():
            for loc in ["en"] + L:
                url = f"{BASE}{'' if loc == 'en' else '/' + loc}/pages/{handle}?d={int(time.time())}"
                page = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=40).read().decode("utf-8", "ignore")
                text = re.sub(r"&#39;|&rsquo;", "'", page)
                n = text.count(LINE[loc])
                raw = json.loads(re.sub(r"^\s*/\*.*?\*/", "", gql('query($id:ID!){ theme(id:$id){ files(filenames:["templates/%s"]){ nodes{ body{ ... on OnlineStoreThemeFileBodyText{ content } } } } } }' % tpl, {"id": THEME})["theme"]["files"]["nodes"][0]["body"]["content"], flags=re.S)) if loc == "en" else None
                want = len(list(targets(raw))) if raw else want
                ok = n == want
                bad += not ok
                print(f"  {'✓' if ok else '✗'} /{loc}/pages/{handle:<32} disclosure lines {n}/{want}")
                time.sleep(1.2)
        return 1 if bad else 0

    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    for tpl in TEMPLATES:
        name = f"templates/{tpl}"
        raw = gql('query($id:ID!){ theme(id:$id){ files(filenames:["%s"]){ nodes{ body{ ... on OnlineStoreThemeFileBodyText{ content } } } } } }' % name, {"id": THEME})["theme"]["files"]["nodes"][0]["body"]["content"]
        m = re.match(r"\s*(/\*.*?\*/)\s*", raw, re.S)
        hdr, j = (m.group(1) if m else ""), json.loads(raw[m.end():] if m else raw)
        rid = f"gid://shopify/OnlineStoreThemeJsonTemplate/{tpl[:-5]}?theme_id={THEME.rsplit('/', 1)[1]}"
        tr = gql('query($id:ID!){ translatableResource(resourceId:$id){ %s } }' % " ".join(
            f'{l}:translations(locale:"{l}"){{key value}}' for l in L), {"id": rid})["translatableResource"]
        todo = []
        for sid, bid, st in targets(j):
            key = f".{sid}.{bid}.content:"
            if has_line(st["content"], "en"):
                print(f"  = {tpl} {sid}/{bid}: already disclosed")
                continue
            new_en = st["content"].rstrip() + line_html("en")
            loc_new = {}
            for l in L:
                cur = next((x["value"] for x in tr[l] if key in x["key"]), None)
                if cur is not None and not has_line(cur, l):
                    loc_new[l] = cur.rstrip() + line_html(l)
            todo.append((sid, bid, new_en, loc_new))
            print(f"  + {tpl} {sid}/{bid}: EN + {len(loc_new)} locale translation(s)")
        if not a.apply or not todo:
            continue
        (ROOT / f"backups/illustration-disclosure-{tpl}-{stamp}.json").write_text(raw)
        for sid, bid, new_en, _ in todo:
            j["sections"][sid]["blocks"][bid]["settings"]["content"] = new_en
        body = (hdr + "\n" if hdr else "") + json.dumps(j, indent=2, ensure_ascii=False)
        r = gql('mutation($t:ID!,$f:[OnlineStoreThemeFilesUpsertFileInput!]!){ themeFilesUpsert(themeId:$t, files:$f){ userErrors{field message} } }',
                {"t": THEME, "f": [{"filename": name, "body": {"type": "TEXT", "value": body}}]})
        if r["themeFilesUpsert"]["userErrors"]:
            sys.exit(r["themeFilesUpsert"]["userErrors"])
        for attempt in range(6):
            tc = gql('query($id:ID!){ translatableResource(resourceId:$id){ translatableContent{ key value digest } } }', {"id": rid})["translatableResource"]["translatableContent"]
            idx = {c["key"]: c for c in tc}
            ready = all(any(f".{sid}.{bid}.content:" in k and c["value"] == en for k, c in idx.items()) for sid, bid, en, _ in todo)
            if ready:
                break
            time.sleep(5)
        for sid, bid, en, loc_new in todo:
            c = next(c for k, c in idx.items() if f".{sid}.{bid}.content:" in k)
            if loc_new:
                r = gql('mutation($id:ID!,$t:[TranslationInput!]!){ translationsRegister(resourceId:$id, translations:$t){ userErrors{field message} } }',
                        {"id": rid, "t": [{"locale": l, "key": c["key"], "value": v, "translatableContentDigest": c["digest"]} for l, v in loc_new.items()]})
                print(f"    {tpl} {sid}/{bid}: translations {r['translationsRegister']['userErrors'] or 'registered'}")
    if not a.apply:
        print("  dry run — nothing written.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
