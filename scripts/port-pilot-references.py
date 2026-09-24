#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Move the two pilot pages' `reference` field into their sections_html, as a final band.

Why: page-audit.py (2026-09-24) found two faults that share one cause — the citation lives in
the theme's `study_reference` rich-text section, which trafilatura drops (so the "Reference"
H2 never reaches an AI crawler) and which paints a second white band straight after the bone
one. The new template renders the citation inside sections_html instead. Before the theme
section can stop rendering `reference`, the pilots have to stop depending on it.

Content is preserved exactly; only the wrapper changes. Idempotent: a page that already ends
with a reference band is skipped.
"""
import importlib.util
import json
import pathlib
import sys

ROOT = pathlib.Path("/Users/malcolmsmith/Claude Code/Projects/skingenetix-website")


def load(name, path):
    s = importlib.util.spec_from_file_location(name, ROOT / path)
    m = importlib.util.module_from_spec(s)
    argv, sys.argv = sys.argv, [sys.argv[0]]
    s.loader.exec_module(m)
    sys.argv = argv
    return m


hu = load("hu", "scripts/hub-upgrade.py")
sx = load("sx", "scripts/study_sections.py")
LOCALES = ["de", "nl", "fr", "es", "it"]
PILOTS = ["argireline-crows-feet-trial-wang-2013", "pdrn-vs-retinol-split-face-trial-ye-2026"]
MARK = '<h2>Reference</h2>'


def inline(node):
    t = node.get("type")
    if t == "text":
        s = node.get("value", "")
        if node.get("bold"):
            s = f"<strong>{s}</strong>"
        if node.get("italic"):
            s = f"<em>{s}</em>"
        return s
    if t == "link":
        kids = "".join(inline(c) for c in node.get("children", []))
        tgt = ' target="_blank" rel="noopener"' if node.get("target") == "_blank" else ""
        return f'<a href="{node.get("url","")}"{tgt}>{kids}</a>'
    return "".join(inline(c) for c in node.get("children", []))


def block(node):
    t = node.get("type")
    kids = "".join(inline(c) for c in node.get("children", []))
    if t == "heading":
        return f"<h2>{kids}</h2>"          # never a second h1
    if t == "paragraph":
        return f"<p>{kids}</p>"
    if t == "list":
        tag = "ol" if node.get("listType") == "ordered" else "ul"
        items = "".join(f"<li>{''.join(inline(c) for c in i.get('children', []))}</li>"
                        for i in node.get("children", []))
        return f"<{tag}>{items}</{tag}>"
    return kids


def to_html(rich_json):
    if not rich_json:
        return ""
    return "".join(block(c) for c in json.loads(rich_json).get("children", []))


def append_band(sections_html, ref_html):
    """Put the citation in its own white band, at the end, inside the .sty wrapper."""
    band = sx.band("white", ref_html)
    assert sections_html.rstrip().endswith("</div>"), "unexpected sections_html shape"
    cut = sections_html.rstrip()[:-len("</div>")]
    return cut + band + "</div>"


Q = "query($h:MetaobjectHandleInput!){ metaobjectByHandle(handle:$h){ id fields{ key value } } }"
for handle in PILOTS:
    e = hu.gql(Q, {"h": {"type": "study", "handle": handle}})["metaobjectByHandle"]
    if not e:
        sys.exit(f"REFUSING: pilot {handle} not found")
    f = {x["key"]: x["value"] for x in e["fields"]}
    cur = f.get("sections_html") or ""
    if not cur:
        sys.exit(f"REFUSING: {handle} has no sections_html — run port_pilots.py first")
    if not (f.get("reference") or "").strip():
        print(f"  {handle}: already ported (reference field is empty)")
        continue
    ref = to_html(f.get("reference"))
    if len(ref) < 80:
        sys.exit(f"REFUSING: {handle} reference converted to only {len(ref)} chars")
    new = append_band(cur, ref)
    r = hu.gql("mutation($id:ID!,$m:MetaobjectUpdateInput!){ metaobjectUpdate(id:$id, metaobject:$m)"
               "{ userErrors{field message} } }",
               {"id": e["id"], "m": {"fields": [{"key": "sections_html", "value": new},
                                                {"key": "reference", "value": ""}]}})["metaobjectUpdate"]
    if r["userErrors"]:
        sys.exit(f"REFUSING: {r['userErrors']}")
    print(f"  {handle}: EN {len(cur)} -> {len(new)} chars, reference field cleared")

    rid = e["id"]
    tq = ("query($id:ID!){ translatableResource(resourceId:$id){ " + " ".join(
        f'{l}:translations(locale:"{l}"){{ key value }}' for l in LOCALES) + " } }")
    tr = hu.gql(tq, {"id": rid})["translatableResource"]
    tc = hu.gql("query($id:ID!){ translatableResource(resourceId:$id){ translatableContent{ key value digest } } }",
                {"id": rid})["translatableResource"]["translatableContent"]
    dig = {c["key"]: c["digest"] for c in tc}
    subs = []
    for l in LOCALES:
        cl = {x["key"]: x["value"] for x in tr[l]}
        base, rf = cl.get("sections_html"), to_html(cl.get("reference"))
        if not base or len(rf) < 80:
            print(f"    {l}: SKIPPED (sections_html {bool(base)}, reference {len(rf)} chars)")
            continue
        subs.append({"locale": l, "key": "sections_html", "value": append_band(base, rf),
                     "translatableContentDigest": dig["sections_html"]})
        if "reference" in dig:
            subs.append({"locale": l, "key": "reference", "value": "",
                         "translatableContentDigest": dig["reference"]})
    if subs:
        rr = hu.gql("mutation($id:ID!,$t:[TranslationInput!]!){ translationsRegister(resourceId:$id, translations:$t)"
                    "{ userErrors{field message} } }", {"id": rid, "t": subs})["translationsRegister"]
        print(f"    translations: {len(subs)} entries"
              + (f" ERR {rr['userErrors']}" if rr["userErrors"] else " OK"))
