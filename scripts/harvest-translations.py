#!/usr/bin/env python3
"""Harvest a page template's live English and its approved translations into phrase pairs — step 2 of a rollout.

Author: Claude (Opus 5.5) for Malcolm Smith · 2026-09-25
Purpose: docs/science-page-template.md §6 step 2. Before a science page's sections are replaced, pair every live
English text with its approved translation in all five other languages, so the new build REUSES approved wording
(hub-i18n.py's phrase table) instead of re-translating it. The PDRN rollout did this by hand; this is that recipe.

    python3 scripts/harvest-translations.py page.research-copper-peptide <out.json>

Method (§6.1):
  * Only keys translated in ALL five locales and not outdated are used — an outdated translation is still served,
    but it describes old English.
  * Pair by element (<p>, <li>, <h2>…, <td>) when every locale has the same number of elements, so a paragraph that
    holds links or a short connector ("and the") is taken whole rather than as a fragment that would be substituted
    everywhere. A value with no elements (a label, a title) is paired whole. A value whose structure differs in any
    locale is skipped and listed.
  * Every pair's numbers are compared across languages (1,500 = 1500; 7.4 = 7,4). A mismatch is flagged, not dropped:
    on PDRN every mismatch was word order or a thousands separator, but it is the check that catches a wrong figure.
Read-only against Shopify: it queries translatableResource and writes one local JSON file.
"""
import importlib.util
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOCALES = ["de", "nl", "fr", "es", "it"]
ELEMENT = re.compile(r"<(p|li|h[1-6]|td|th|dt|dd)\b[^>]*>(.*?)</\1>", re.S)


def pair_elements(values):
    """values: {"en": html, "de": html, ...} -> [{"en": inner, "de": inner, ...}], or [] if structures differ."""
    split = {l: [m.group(2).strip() for m in ELEMENT.finditer(v)] for l, v in values.items()}
    if not split["en"]:
        if any(split[l] for l in LOCALES):
            return []
        return [{l: values[l].strip() for l in ["en"] + LOCALES}]
    if any(len(split[l]) != len(split["en"]) for l in LOCALES):
        return []
    return [{l: split[l][i] for l in ["en"] + LOCALES} for i in range(len(split["en"]))]


def _numbers(text):
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"(?<=\d)[,.](?=\d{3}\b)", "", text)      # thousands separators: 1,500 / 1.500 -> 1500
    text = re.sub(r"(?<=\d),(?=\d)", ".", text)              # decimal comma: 7,4 -> 7.4
    return sorted(re.findall(r"\d+(?:\.\d+)?", text))


def numbers_agree(en, other):
    return _numbers(en) == _numbers(other)


def harvest(content, translations):
    """content: translatableContent [{key, value}]; translations: {loc: [{key, value, outdated}]}."""
    current = {l: {t["key"]: t["value"] for t in translations[l] if not t["outdated"]} for l in LOCALES}
    pairs, skipped = [], []
    for c in content:
        k, en = c["key"], c["value"]
        if not en or not all(k in current[l] for l in LOCALES):
            skipped.append({"key": k, "why": "not current in all five locales"})
            continue
        found = pair_elements({"en": en, **{l: current[l][k] for l in LOCALES}})
        if not found:
            skipped.append({"key": k, "why": "element structure differs between locales"})
            continue
        for p in found:
            bad = [l for l in LOCALES if not numbers_agree(p["en"], p[l])]
            pairs.append({**p, "key": k, "numbers_ok": not bad, "number_mismatch": bad})
    return {"pairs": pairs, "skipped": skipped}


def fetch(template):
    s = importlib.util.spec_from_file_location("hu", ROOT / "scripts/hub-upgrade.py")
    hu = importlib.util.module_from_spec(s)
    argv, sys.argv = sys.argv, ["hub-upgrade"]
    s.loader.exec_module(hu)
    sys.argv = argv
    rid = f"gid://shopify/OnlineStoreThemeJsonTemplate/{template}?theme_id={hu.THEME.rsplit('/', 1)[1]}"
    loc = " ".join(f'{l}:translations(locale:"{l}"){{key value outdated}}' for l in LOCALES)
    r = hu.gql(f'query($id:ID!){{ translatableResource(resourceId:$id){{ translatableContent{{ key value }} {loc} }} }}',
               {"id": rid})["translatableResource"]
    return r["translatableContent"], {l: r[l] for l in LOCALES}


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__.split("\n\n")[2])
    template, out = sys.argv[1], pathlib.Path(sys.argv[2])
    content, translations = fetch(template)
    result = harvest(content, translations)
    out.write_text(json.dumps({"template": template, **result}, indent=1, ensure_ascii=False))
    flagged = [p for p in result["pairs"] if not p["numbers_ok"]]
    print(f"  {template}: {len(result['pairs'])} phrase pairs from {len(content)} keys · "
          f"{len(result['skipped'])} keys skipped · {len(flagged)} pairs with differing numbers (check by eye)")
    for p in flagged:
        print(f"    ⚠ {p['number_mismatch']}: {re.sub(r'<[^>]+>', '', p['en'])[:90]}")
    print(f"  wrote {out}")


if __name__ == "__main__":
    main()
