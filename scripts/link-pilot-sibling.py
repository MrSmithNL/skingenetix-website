#!/usr/bin/env python3
"""Link the Wang 2013 pilot to its sibling appraisal, Raikou 2017, in all six languages.

Found by the central SEO/GEO/AISO audit on 2026-09-29 (P3, confirmed by hand): Wang cites
"Raikou et al., 2017" but links only to PubMed, never to Skingenetix's own appraisal of that
trial, so the two Argireline studies were not linked across. The PubMed citation stays (the
audit's citation check verifies it); a descriptive link to our appraisal goes right after it.

The pilots hold their body as finished HTML in `sections_html` (no builder renders it any more),
so the English field is updated in place and the five translations are re-registered against
the new digest — the pattern of scripts/port-pilot-references.py. Idempotent.

    python3 scripts/link-pilot-sibling.py            # dry run
    python3 scripts/link-pilot-sibling.py --apply
"""
import importlib.util
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
_s = importlib.util.spec_from_file_location("hu", ROOT / "scripts/hub-upgrade.py")
hu = importlib.util.module_from_spec(_s)
_argv, sys.argv = sys.argv, [sys.argv[0]]
_s.loader.exec_module(hu)
sys.argv = _argv

HANDLE = "argireline-crows-feet-trial-wang-2013"
TARGET = "blogs/clinical-studies/argireline-forehead-roughness-trial-raikou-2017"
CITATION = ('<a href="https://pubmed.ncbi.nlm.nih.gov/28150423/" target="_blank" rel="noopener">'
            "Raikou et al., 2017</a>")
ANCHOR = {
    "en": "our appraisal of the forehead-lines trial",
    "de": "unsere Bewertung der Stirnfalten-Studie",
    "nl": "onze beoordeling van de voorhoofdsstudie",
    "fr": "notre analyse de l'essai sur les rides du front",
    "es": "nuestro análisis del ensayo sobre las arrugas de la frente",
    "it": "la nostra analisi dello studio sulle rughe della fronte",
}
TRANSLATED = ["de", "nl", "fr", "es", "it"]


def linked(html, locale):
    """The body with the appraisal link after the Raikou citation; unchanged if already there."""
    if TARGET in html:
        return html
    if html.count(CITATION) != 1:
        raise ValueError(f"{locale}: expected the Raikou citation once, found {html.count(CITATION)}")
    prefix = "" if locale == "en" else f"/{locale}"
    link = f'{CITATION} — <a href="{prefix}/{TARGET}">{ANCHOR[locale]}</a>'
    return html.replace(CITATION, link)


def main():
    apply = "--apply" in sys.argv
    e = hu.gql('query($h:MetaobjectHandleInput!){ metaobjectByHandle(handle:$h){ id fields{ key value } } }',
               {"h": {"type": "study", "handle": HANDLE}})["metaobjectByHandle"]
    rid = e["id"]
    en = {x["key"]: x["value"] for x in e["fields"]}["sections_html"]
    q = ("query($id:ID!){ translatableResource(resourceId:$id){ "
         + " ".join(f'{l}:translations(locale:"{l}"){{ key value }}' for l in TRANSLATED) + " } }")
    tr = hu.gql(q, {"id": rid})["translatableResource"]
    tr = {l: {x["key"]: x["value"] for x in tr[l]}.get("sections_html", "") for l in TRANSLATED}
    new_en = linked(en, "en")
    new_tr = {l: linked(v, l) for l, v in tr.items() if v}
    print(f"  {HANDLE}: EN {'already linked' if new_en == en else 'link added'}; "
          f"translations {sorted(new_tr)} (missing: {sorted(set(TRANSLATED) - set(new_tr)) or 'none'})")
    if not apply:
        print("  dry run — pass --apply to write")
        return 0
    if new_en != en:
        r = hu.gql("mutation($id:ID!,$m:MetaobjectUpdateInput!){ metaobjectUpdate(id:$id, metaobject:$m)"
                   "{ userErrors{field message} } }",
                   {"id": rid, "m": {"fields": [{"key": "sections_html", "value": new_en}]}})["metaobjectUpdate"]
        if r["userErrors"]:
            sys.exit(f"  ✗ {r['userErrors']}")
    tc = hu.gql("query($id:ID!){ translatableResource(resourceId:$id){ translatableContent{ key digest } } }",
                {"id": rid})["translatableResource"]["translatableContent"]
    digest = next(c["digest"] for c in tc if c["key"] == "sections_html")
    subs = [{"locale": l, "key": "sections_html", "value": v, "translatableContentDigest": digest}
            for l, v in new_tr.items()]
    r = hu.gql("mutation($id:ID!,$t:[TranslationInput!]!){ translationsRegister(resourceId:$id, translations:$t)"
               "{ userErrors{field message} } }", {"id": rid, "t": subs})["translationsRegister"]
    if r["userErrors"]:
        sys.exit(f"  ✗ translations: {r['userErrors']}")
    print(f"  ✓ EN written; {len(subs)} translations re-registered against the new text")
    return 0


if __name__ == "__main__":
    sys.exit(main())
