#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Give study pages the same layout capability the science hubs have.

The pilot template is four centred rich-text sections: no images, no charts, no tables.
Shopify richtext strips classes, so nothing richer can live in those fields.

The lever already exists in the template: the `jsonld` field is a multi_line_text_field
holding raw HTML, emitted unescaped by a `liquid` block as {{ metaobject.jsonld.value }}.
So one more multi_line_text_field, rendered the same way, carries the whole designed body
— key figures, at-a-glance, chart plus a real <table>, image rows, limitations.

Additive: the four existing fields and the two live pages are untouched, so the pilot keeps
rendering while the new field is empty.
"""
import importlib.util, json, pathlib, re, sys

ROOT = pathlib.Path("/Users/malcolmsmith/Claude Code/Projects/skingenetix-website")
sp = importlib.util.spec_from_file_location("hu", ROOT / "scripts/hub-upgrade.py")
hu = importlib.util.module_from_spec(sp); sp.loader.exec_module(hu)
TPL = "templates/metaobject/study.json"
DEF = "gid://shopify/MetaobjectDefinition/27495661953"

# ---- 1. the new field -------------------------------------------------------
have = {f["key"] for f in hu.gql(
    'query{ metaobjectDefinitionByType(type:"study"){ fieldDefinitions{ key } } }'
)["metaobjectDefinitionByType"]["fieldDefinitions"]}
if "sections_html" in have:
    print("  field sections_html already exists")
else:
    r = hu.gql('''mutation($id:ID!,$d:MetaobjectDefinitionUpdateInput!){
      metaobjectDefinitionUpdate(id:$id, definition:$d){ userErrors{field message} } }''',
      {"id": DEF, "d": {"fieldDefinitions": [{"create": {
          "key": "sections_html", "name": "Designed sections (HTML)",
          "type": "multi_line_text_field",
          "description": "Raw HTML for the designed body: key figures, at-a-glance, chart, image rows, limitations. Rendered unescaped by a liquid block."}}]}})
    errs = r["metaobjectDefinitionUpdate"]["userErrors"]
    if errs: sys.exit(f"REFUSING: {errs}")
    print("  field sections_html created")

# ---- 2. the template renders it --------------------------------------------
raw = hu.read_file(TPL)
m = re.match(r"^\s*(/\*.*?\*/\s*)+", raw, re.S)      # Shopify prepends MULTIPLE comments
hdr, body = (raw[:m.end()], raw[m.end():]) if m else ("", raw)
j = json.loads(body)

if "study_designed" in j["sections"]:
    print("  section study_designed already present")
else:
    (ROOT / f"backups/metaobject-study-{__import__('datetime').datetime.now():%Y%m%d-%H%M%S}.json").write_text(raw)
    j["sections"]["study_designed"] = {
        "type": "rich-text",
        "blocks": {"d": {"type": "liquid",
                         "settings": {"liquid": "{{ metaobject.sections_html.value }}"}}},
        "block_order": ["d"],
        "settings": {"full_width": True, "content_width": "large",
                     "text_position": "center", "background": "#ffffff",
                     "remove_vertical_spacing": True},
    }
    # between the head and the reference; the old facts/body sections stay for the pilot pages
    j["order"].insert(j["order"].index("study_reference"), "study_designed")
    out = hdr + json.dumps(j, indent=2, ensure_ascii=False)
    for bad in ("{{ metaobject.sections_html.value }}",):
        assert bad in out
    hu.gql('mutation($t:ID!,$f:[OnlineStoreThemeFilesUpsertFileInput!]!){ themeFilesUpsert(themeId:$t, files:$f)'
           '{ userErrors{field message} } }',
           {"t": hu.THEME, "f": [{"filename": TPL, "body": {"type": "TEXT", "value": out}}]})
    print("  template updated; order:", j["order"])
