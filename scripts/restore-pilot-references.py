#!/usr/bin/env python3
"""Restore the five translated citations on the two pilot pages.

port_pilot_refs.py cleared the English `reference` field and THEN read the translations, and
Shopify drops a translation whose source value has been emptied. The English band was appended
correctly; the five locales lost theirs. The configs are the source of truth, so the translated
citations are rebuilt from them rather than recovered from the store.
"""
import importlib.util, json, pathlib, sys

ROOT = pathlib.Path("/Users/malcolmsmith/Claude Code/Projects/skingenetix-website")


def load(n, p):
    s = importlib.util.spec_from_file_location(n, ROOT / p)
    m = importlib.util.module_from_spec(s)
    a, sys.argv = sys.argv, [sys.argv[0]]
    s.loader.exec_module(m)
    sys.argv = a
    return m


hu, sx = load("hu", "scripts/hub-upgrade.py"), load("sx", "scripts/study_sections.py")
LOCALES = ["de", "nl", "fr", "es", "it"]
PILOTS = ["argireline-crows-feet-trial-wang-2013", "pdrn-vs-retinol-split-face-trial-ye-2026"]


def blocks_to_html(blocks, loc):
    out = []
    for kind, content in blocks:
        if kind in ("h2", "h3"):
            out.append(f"<h2>{sx.md(content, loc)}</h2>")
        elif kind == "p":
            out.append(f"<p>{sx.md(content, loc)}</p>")
        elif kind == "ul":
            items = "".join(f"<li>{sx.md(i, loc)}</li>" for i in content)
            out.append(f"<ul>{items}</ul>")
    return "".join(out)


def append_band(sections_html, ref_html):
    assert sections_html.rstrip().endswith("</div>"), "unexpected sections_html shape"
    return sections_html.rstrip()[:-len("</div>")] + sx.band("white", ref_html) + "</div>"


for handle in PILOTS:
    cfg = json.loads((ROOT / f"configs/studies/{handle}.json").read_text())
    e = hu.gql("query($h:MetaobjectHandleInput!){ metaobjectByHandle(handle:$h){ id } }",
               {"h": {"type": "study", "handle": handle}})["metaobjectByHandle"]
    rid = e["id"]
    tq = ("query($id:ID!){ translatableResource(resourceId:$id){ "
          + " ".join(f'{l}:translations(locale:"{l}"){{ key value }}' for l in LOCALES) + " } }")
    tr = hu.gql(tq, {"id": rid})["translatableResource"]
    tc = hu.gql("query($id:ID!){ translatableResource(resourceId:$id){ translatableContent{ key value digest } } }",
                {"id": rid})["translatableResource"]["translatableContent"]
    dig = {c["key"]: c["digest"] for c in tc}
    subs = []
    for l in LOCALES:
        cur = {x["key"]: x["value"] for x in tr[l]}
        base = cur.get("sections_html")
        if not base:
            sys.exit(f"REFUSING: {handle} {l} has no translated sections_html")
        ref = blocks_to_html(cfg["fields"]["reference"][l], l)
        if len(ref) < 80:
            sys.exit(f"REFUSING: {handle} {l} reference is only {len(ref)} chars")
        if "</h2>" in base.rsplit("sty__band--white", 1)[-1] and ref[:40] in base:
            print(f"    {l}: already restored")
            continue
        subs.append({"locale": l, "key": "sections_html", "value": append_band(base, ref),
                     "translatableContentDigest": dig["sections_html"]})
    if not subs:
        print(f"  {handle}: nothing to restore")
        continue
    r = hu.gql("mutation($id:ID!,$t:[TranslationInput!]!){ translationsRegister(resourceId:$id, translations:$t)"
               "{ userErrors{field message} } }", {"id": rid, "t": subs})["translationsRegister"]
    if r["userErrors"]:
        sys.exit(f"REFUSING: {r['userErrors']}")
    print(f"  {handle}: restored {len(subs)} locales")
