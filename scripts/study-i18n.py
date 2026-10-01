#!/usr/bin/env python3
"""Translate a study config into de/nl/fr/es/it: extract its English strings, merge checked translations back.

Author: Claude (Opus 5.5) for Malcolm Smith · 2026-10-01
Purpose: a study config (configs/studies/*.json, built by scripts/build-study-page.py) holds every visible string as
{"en": ...}. Translators (one agent per language) work from a flat list, never the config itself, so five can work at
once without clobbering each other. This tool puts their strings back and refuses to write on any defect.

    python3 scripts/study-i18n.py extract configs/studies/drafts/<handle>.json   # -> configs/studies/i18n/<handle>.en.json
    # translators write configs/studies/i18n/<handle>.<loc>.json with the same keys
    python3 scripts/study-i18n.py merge configs/studies/drafts/<handle>.json --locales de --check   # a translator's own check
    python3 scripts/study-i18n.py merge configs/studies/drafts/<handle>.json     # checks, then writes the five locales

What it does per string and locale:
  * keeps every number (decimal commas and thousand spaces allowed), every markdown link, every HTML tag and every URL
  * locale-prefixes internal links (https://www.skingenetix.com/pages/x -> .../de/pages/x; href='/pages/x' -> '/de/pages/x')
  * composes the byline from a live study's translated byline with this study's date, so set-reviewer.py can find and
    remove the reviewer sentence as an exact substring in every language (a hand-translated variant would strand it)
Never translated: `_notes`, `checks` (English probes), `scholarly` (the journal's own title) and the byline.
The `citation` paragraph is kept verbatim; a locale may only append a note such as "(auf Englisch)".
"""
import argparse, collections, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
I18N = ROOT / "configs/studies/i18n"
LOCALES = ["de", "nl", "fr", "es", "it"]
SKIP = {"checks", "scholarly", "byline"}
# a live, six-language study whose byline is the reference wording (the reviewer sentence must match it exactly)
REF_BYLINE = ROOT / "configs/studies/argireline-crows-feet-trial-wang-2013.json"

_SITE = re.compile(r"(https://www\.skingenetix\.com)/(?!(?:de|nl|fr|es|it)/)(pages|products|collections|blogs)/")
_REL = re.compile(r"""((?:href=|\]\()['"]?)/(?!(?:de|nl|fr|es|it)/)(pages|products|collections|blogs)/""")
_THOUSANDS = re.compile(r"\b\d{1,3}(?:[ ,.  ]\d{3})+\b")
_NUM = re.compile(r"\d+(?:[.,]\d+)?")
_TAG = re.compile(r"</?[a-zA-Z][^>]*>")
_MDLINK = re.compile(r"\]\(([^)\s]+)\)")
_URL = re.compile(r"https?://[^\s)\"'<>]+")


def strings(cfg, path=""):
    """{json-pointer: English} for every translatable leaf ({"en": str}), skipping notes, probes, citation, byline."""
    out = {}
    if isinstance(cfg, dict):
        if isinstance(cfg.get("en"), str) and path:
            return {path: cfg["en"]}
        for k, v in cfg.items():
            if k.startswith("_") or (not path and k in SKIP):
                continue
            out.update(strings(v, f"{path}/{k}"))
    elif isinstance(cfg, list):
        for i, v in enumerate(cfg):
            out.update(strings(v, f"{path}/{i}"))
    return out


def node(cfg, pointer):
    for part in pointer.strip("/").split("/"):
        cfg = cfg[int(part)] if isinstance(cfg, list) else cfg[part]
    return cfg


def localise_links(text, loc):
    return _REL.sub(rf"\1/{loc}/\2/", _SITE.sub(rf"\1/{loc}/\2/", text))


def _numbers(s):
    s = _THOUSANDS.sub(lambda m: re.sub(r"[ ,.  ]", "", m.group(0)), s)
    return collections.Counter(n.replace(",", ".") for n in _NUM.findall(s))


def _urls(s, loc=None):
    return sorted(localise_links(u, loc) if loc else u for u in _URL.findall(s))


def problems(en, tr, loc):
    """Every defect of one translated string against its English."""
    errs = []
    lost = _numbers(en) - _numbers(tr)
    if lost:
        errs.append(f"numbers lost: {sorted(lost)}")
    if len(_TAG.findall(en)) != len(_TAG.findall(tr)):
        errs.append(f"HTML tags {len(_TAG.findall(en))} -> {len(_TAG.findall(tr))}")
    if len(_MDLINK.findall(en)) != len(_MDLINK.findall(tr)):
        errs.append(f"links {len(_MDLINK.findall(en))} -> {len(_MDLINK.findall(tr))}")
    if _urls(en, loc) != _urls(localise_links(tr, loc), loc):
        errs.append("URLs differ")
    if tr.strip() == en.strip() and len(en.split()) > 3:
        errs.append("identical to the English")
    return errs


def byline(en_byline, ref_loc_byline):
    """The reference locale byline with this study's review date (same month: refuses otherwise)."""
    m = re.search(r"(\d{1,2}) (\w+) (\d{4})\.?$", en_byline.strip())
    if not m:
        raise ValueError(f"no date at the end of the English byline: {en_byline!r}")
    out, n = re.subn(r"\b\d{1,2}(?=\.? (?:de )?\w+ (?:de )?\d{4}\.?$)", m.group(1), ref_loc_byline.strip())
    if n != 1 or m.group(3) not in out:
        raise ValueError(f"cannot re-date the reference byline: {ref_loc_byline!r}")
    return out


def merge(cfg, translations, ref_byline):
    """Write each locale into cfg. Returns (cfg, errors); with any error nothing should be saved."""
    want, errs = strings(cfg), []
    for loc, tr in translations.items():
        for key in sorted(set(want) - set(tr)):
            errs.append(f"{loc} {key}: missing")
        for key in sorted(set(tr) - set(want)):
            errs.append(f"{loc} {key}: not in the English")
        for key, en in want.items():
            if key in tr:
                # the citation is the journal's own words and may stand verbatim (the live studies keep it so, 2026-10-01)
                errs += [f"{loc} {key}: {e}" for e in problems(en, tr[key], loc)
                         if not (key == "/citation" and e == "identical to the English")]
        # the reference is the journal's own words: a translation may only add a note after it (e.g. "(auf Englisch)")
        if "/citation" in tr and "/citation" in want and not tr["/citation"].startswith(want["/citation"].rstrip()):
            errs.append(f"{loc} /citation: the English reference must stay verbatim at the start")
        # the builder's own per-locale limits (build-study-page.py check()), caught before a merge, not at --apply
        if len(tr.get("/seo_title", "")) > 60:
            errs.append(f"{loc} /seo_title: SEO title {len(tr['/seo_title'])} chars (max 60)")
        if len(tr.get("/seo_description", "")) > 160:
            errs.append(f"{loc} /seo_description: {len(tr['/seo_description'])} chars (max 160, aim 155)")
        if "/answer" in tr and not 35 <= len(tr["/answer"].split()) <= 75:
            errs.append(f"{loc} /answer: answer {len(tr['/answer'].split())} words (35-75)")
    if errs:
        return cfg, errs
    for loc, tr in translations.items():
        for key, text in tr.items():
            node(cfg, key)[loc] = localise_links(text, loc)
        cfg["byline"][loc] = byline(cfg["byline"]["en"], ref_byline[loc])
    return cfg, []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("action", choices=["extract", "merge"])
    ap.add_argument("config")
    ap.add_argument("--locales", default=",".join(LOCALES))
    ap.add_argument("--check", action="store_true", help="merge: report problems only, write nothing (safe in parallel)")
    a = ap.parse_args()
    path = pathlib.Path(a.config); cfg = json.loads(path.read_text()); h = cfg["handle"]
    I18N.mkdir(parents=True, exist_ok=True)
    if a.action == "extract":
        out = I18N / f"{h}.en.json"
        out.write_text(json.dumps(strings(cfg), indent=2, ensure_ascii=False) + "\n")
        print(f"  ✓ {len(strings(cfg))} strings -> {out.relative_to(ROOT)}")
        return 0
    locs = [l for l in a.locales.split(",") if (I18N / f"{h}.{l}.json").exists()]
    tr = {l: json.loads((I18N / f"{h}.{l}.json").read_text()) for l in locs}
    ref = json.loads(REF_BYLINE.read_text())["byline"]
    cfg, errs = merge(cfg, tr, ref)
    for e in errs:
        print("  ✗", e)
    if errs:
        print(f"  REFUSED: {len(errs)} problem(s); nothing written")
        return 1
    if a.check:
        print(f"  ✓ {h}: {', '.join(locs) or 'nothing'} clean (check only, nothing written)")
        return 0
    path.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")
    print(f"  ✓ {h}: merged {', '.join(locs) or 'nothing'} ({len(strings(cfg))} strings each)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
