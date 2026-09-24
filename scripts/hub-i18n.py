#!/usr/bin/env python3
"""Translate a science page's custom-html sections by phrase substitution — six languages, refuses on any defect.

Author: Claude (Opus 5.5) for Malcolm Smith · 2026-09-24
Purpose: the science-page template (docs/science-page-template.md) builds four sections as custom-html. Shopify
translates a custom-html section as ONE blob per language, so any change to its English leaves all five translations
stale — and a stale translation is still served. This tool rebuilds the five from a per-page phrase table.
Generalised from the 2026-09-23 Argireline recipe; tests/test_hub_i18n.py proves it reproduces that page's live
translations byte for byte.

    python3 scripts/hub-i18n.py configs/hub-i18n/acetyl-hexapeptide-8-research.json           # build + check, writes nothing
    python3 scripts/hub-i18n.py configs/hub-i18n/acetyl-hexapeptide-8-research.json --write   # six-locale values into the specs
    python3 scripts/hub-upgrade.py <each owning spec> --apply                                  # then upload + register

Method, per locale:
  1. substitute phrases, longest English key first, so a short key never eats part of a long one
  2. swap the byline for this locale's, COMPOSED from the reviewer config — set-reviewer.py removes the reviewer
     sentence as an exact substring, so a hand-typed variant would strand Dr Bodde's credit in that language
  3. locale-prefix internal hrefs (/pages/x -> /de/pages/x); anchors (#rba-f1) and external links stay as they are
  4. localise the WebPage JSON-LD (inLanguage, /loc/ url and @id, name/description from the config's jsonld_i18n);
     phrases never touch it

The CSS, the JSON-LD and the verbatim published study titles never enter the phrase table, so they are untouched by
construction (ADR-2026-09-23-G: titles are quoted exactly as the journal printed them).

It REFUSES to write unless, for every locale: the <h2>, <table>, <tr>, <li> and <a> counts match English; every
internal href carries the locale prefix; no English prose survives (bar the allowlist and the verbatim fragments);
no Cyrillic or Greek look-alike letter appears — the Italian "deterсa" of 2026-09-23 rendered identically; and
the WebPage JSON-LD parses and declares this locale.
"""
import argparse, datetime as dt, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://www.skingenetix.com"
LOCALES = ["de", "nl", "fr", "es", "it"]

MONTHS = {
    "en": "January February March April May June July August September October November December",
    "de": "Januar Februar März April Mai Juni Juli August September Oktober November Dezember",
    "nl": "januari februari maart april mei juni juli augustus september oktober november december",
    "fr": "janvier février mars avril mai juin juillet août septembre octobre novembre décembre",
    "es": "enero febrero marzo abril mayo junio julio agosto septiembre octubre noviembre diciembre",
    "it": "gennaio febbraio marzo aprile maggio giugno luglio agosto settembre ottobre novembre dicembre",
}
# Each must match set-reviewer's date_marker for its locale (tested), or the byline cannot be found again.
DATE_FORMAT = {
    "en": "Last reviewed {d} {m} {y}.",
    "de": "Zuletzt geprüft am {d}. {m} {y}.",
    "nl": "Laatst gecontroleerd op {d} {m} {y}.",
    "fr": "Dernière vérification le {d} {m} {y}.",
    "es": "Última revisión el {d} de {m} de {y}.",
    "it": "Ultima revisione il {d} {m} {y}.",
}
TAGS = ("<h2", "<table", "<tr", "<li", "<a ")
LOOKALIKE = re.compile(r"[Ͱ-ϿЀ-ӿ]")          # Greek and Cyrillic blocks


def date_sentence(iso, loc):
    d = dt.date.fromisoformat(iso)
    day = "1er" if loc == "fr" and d.day == 1 else str(d.day)
    return DATE_FORMAT[loc].format(d=day, m=MONTHS[loc].split()[d.month - 1], y=d.year)


def bylines(rv, process, reviewed):
    """The dated byline paragraph's text per locale: author, reviewer sentence, process sentence, date."""
    return {l: f'{rv["author"][l]} {rv["sentence"][l].replace("&", "&amp;")} {process[l]} {date_sentence(reviewed, l)}'
            for l in ["en"] + LOCALES}


def keep_pattern(extra):
    """Text nodes that are SUPPOSED to stay English: grade letters, numbers, punctuation, names."""
    base = [r"A", r"B", r"C", r"\d+", r"[\d.,%+−–—\s]+", r"[\.\)\(,;:\s]+"]
    return re.compile(r"^(" + "|".join(base + list(extra)) + r")$")


def text_nodes(html):
    body = re.sub(r"<style>.*?</style>", "", html, flags=re.S)
    body = re.sub(r'<script type="application/ld\+json".*?</script>', "", body, flags=re.S)
    return [p.strip() for p in re.split(r"<[^>]+>", body) if p.strip()]


LD_BLOCK = re.compile(r'(<script type="application/ld\+json"[^>]*>)(.*?)(</script>)', re.S)


def localise_jsonld(block, loc, i18n):
    """The WebPage JSON-LD for one locale: inLanguage, the /loc/ url and @id, and the translated name/description.

    The 2026-09-23 recipe left this block in English on every locale (inLanguage "en", English URL on /de/),
    undoing the per-locale JSON-LD the references blocks had carried since 2026-09-22. Fixed 2026-09-24.
    """
    def fix(m):
        ld = json.loads(m.group(2))
        if ld.get("@type") != "WebPage":
            return m.group(0)
        ld["inLanguage"] = loc
        for k in ("url", "@id"):
            if k in ld:
                ld[k] = ld[k].replace(f"{BASE}/pages/", f"{BASE}/{loc}/pages/")
        ld.update(i18n.get(loc, {}))
        return m.group(1) + "\n" + json.dumps(ld, indent=2, ensure_ascii=False) + "\n" + m.group(3)
    return LD_BLOCK.sub(fix, block)


def localise(html, loc, phrases, byline, jsonld_i18n):
    # the JSON-LD is set aside first, so no phrase can land inside it and break the JSON
    parts = LD_BLOCK.split(html)
    prose = [p for i, p in enumerate(parts) if i % 4 == 0]
    for n, chunk in enumerate(prose):
        for en in sorted(phrases, key=len, reverse=True):
            chunk = chunk.replace(en, phrases[en][loc])
        if byline:
            chunk = chunk.replace(byline["en"], byline[loc])
        prose[n] = re.sub(r'href="(/(?!' + loc + r'/)[^"#][^"]*)"', lambda m: f'href="/{loc}{m.group(1)}"', chunk)
    out = []
    for i, p in enumerate(parts):
        if i % 4 == 0:
            out.append(prose[i // 4])
        elif i % 4 == 1:
            out.append(localise_jsonld("".join(parts[i:i + 3]), loc, jsonld_i18n))
    return "".join(out)


def check(en, value, loc, keep, fragments):
    problems = []
    for tag in TAGS:
        if value.count(tag) != en.count(tag):
            problems.append(f"[{loc}] {tag} count {value.count(tag)} != English {en.count(tag)}")
    for href in re.findall(r'href="(/[^"]*)"', value):
        if not href.startswith(f"/{loc}/"):
            problems.append(f"[{loc}] internal link without the /{loc}/ prefix: {href}")
    en_nodes = set(text_nodes(en))
    for node in text_nodes(value):
        if node in en_nodes and not keep.match(node) and not any(f in node for f in fragments):
            problems.append(f"[{loc}] English left behind: {node[:80]}")
        if LOOKALIKE.search(node) and not LOOKALIKE.search(en):
            problems.append(f"[{loc}] Cyrillic/Greek look-alike letters in: {node[:80]}")
    for m in LD_BLOCK.finditer(value):
        try:
            ld = json.loads(m.group(2))
        except ValueError:
            problems.append(f"[{loc}] JSON-LD is not valid JSON")
            continue
        if ld.get("@type") == "WebPage" and (ld.get("inLanguage") != loc or f"/{loc}/pages/" not in ld.get("url", "")):
            problems.append(f"[{loc}] JSON-LD WebPage says inLanguage {ld.get('inLanguage')!r}, url {ld.get('url')!r}")
    return problems


def _section(spec, sid):
    return next(a for a in spec["add_sections"] if a["id"] == sid)["section"]["settings"]


def review_date(cfg, rv):
    if cfg.get("reviewed"):
        return cfg["reviewed"]
    owners = set(cfg["sections"].values())
    hub = next((h for h in rv["hubs"] if h["spec"] in owners), {})
    return hub.get("reviewed", rv["reviewed"])


def build(cfg, root=ROOT):
    """Six-locale html per section, and every problem found. Reads the specs; writes nothing."""
    rv = json.loads((root / cfg["reviewer"]).read_text())
    byline = bylines(rv, cfg["process_sentence"], review_date(cfg, rv))
    keep, fragments, phrases = keep_pattern(cfg["keep_english"]), cfg["verbatim_fragments"], cfg["phrases"]
    values, problems = {}, []
    for sid, spec_path in cfg["sections"].items():
        html = _section(json.loads((root / spec_path).read_text()), sid)["html"]
        en = html["en"] if isinstance(html, dict) else html
        values[sid] = {"en": en}
        for loc in LOCALES:
            values[sid][loc] = localise(en, loc, phrases, byline, cfg.get("jsonld_i18n", {}))
            problems += [f"{sid}{p}" for p in check(en, values[sid][loc], loc, keep, fragments)]
    return values, list(dict.fromkeys(problems))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    ap.add_argument("--write", action="store_true", help="write the six-locale values into the owning specs")
    a = ap.parse_args()
    cfg = json.loads(pathlib.Path(a.config).read_text())
    values, problems = build(cfg)
    if problems:
        print(f"  REFUSING — {len(problems)} problem(s):")
        for p in problems[:40]:
            print(f"    {p}")
        return 1
    for sid, v in values.items():
        print(f"  {sid:<18} {len(v['en']):>6} chars English -> 6 locales ✓")
    print(f"  {len(cfg['phrases'])} phrases · structure, link, leak and look-alike checks passed")
    if not a.write:
        print("  check only — nothing written. --write puts the values into the specs; then hub-upgrade.py --apply.")
        return 0
    for spec_path in sorted(set(cfg["sections"].values())):
        p = ROOT / spec_path
        spec = json.loads(p.read_text())
        for sid, owner in cfg["sections"].items():
            if owner == spec_path:
                _section(spec, sid)["html"] = values[sid]
        p.write_text(json.dumps(spec, indent=2, ensure_ascii=False))
        print(f"  wrote {spec_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
