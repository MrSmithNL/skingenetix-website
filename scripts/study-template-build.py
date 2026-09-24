#!/usr/bin/env python3
"""Rebuild templates/metaobject/study.json from the theme's OWN stock sections.

Author: Claude (Opus 5) for Malcolm Smith · 2026-09-24
Rule: Malcolm, 2026-09-24 — "always use the existing shopify template/theme content modules
and options - before any custom code." The first study-page build ignored this and shipped
~18,000 characters of custom HTML in one field. It scored 100/100 on every audit axis and was
rejected on sight, because it had no header banner and fought the theme's own typography.

WHAT MADE THE STOCK ROUTE POSSIBLE
Liquid IS evaluated inside section settings on a metaobject template — probed on the live site
2026-09-24 across every setting type used here: `subheading.text`, `richtext.content`,
`impact-text` title/subheading/content, `specification-table` heading/value, and the banner's
`image` / `mobile_image`. Shopify even validates the reference, refusing the upload with
"must end with '.value' when not using a metafield filter". So a stock section can carry
per-study content. I had assumed otherwise without testing it.

  * `.value`            for single-line, multi-line and file_reference fields
  * `| metafield_tag`   for rich_text fields (renders the JSON as HTML)

SECTION MAP — every one of these is a section the hubs already use

  banner    image-with-text-overlay   the sub-page header banner, per-study image
  figures   impact-text               three key numbers, the hubs' own stat treatment
  answer    rich-text                 byline, the quotable answer paragraph, our verdict
  glance    specification-table       nine rows; LABELS are static (identical on every study
                                      page, so they translate once as template resources),
                                      values come from the metaobject
  chart     custom-html               the only custom block — the hubs render charts this way too
  story     media-with-text           what the researchers did, beside an image
  limits    rich-text on #1A1A1A      what this study does not show — the hubs' dark-section pattern
  means     rich-text + buttons       what it means for our products
  reference rich-text                 citation, read-at-source note, and the JSON-LD block

CONSTRAINT: a metaobject definition allows at most 40 fields. 37 are used. That is why the
at-a-glance labels and every section heading are static in the template rather than fields.
"""
import argparse
import datetime
import importlib.util
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
_s = importlib.util.spec_from_file_location("hu", ROOT / "scripts/hub-upgrade.py")
hu = importlib.util.module_from_spec(_s)
_argv, sys.argv = sys.argv, [sys.argv[0]]
_s.loader.exec_module(hu)
sys.argv = _argv
TPL = "templates/metaobject/study.json"

BONE, WHITE, INK = "#F0F0F0", "#ffffff", "#1A1A1A"

# The nine rows of "At a glance". Identical on every study page by design — a reader comparing
# two studies should find the same nine questions answered in the same order.
GLANCE_ROWS = [
    ("g1", "Design"), ("g2", "Participants"), ("g3", "What was applied"),
    ("g4", "Compared with"), ("g5", "Duration"), ("g6", "How it was measured"),
    ("g7", "Concentration"), ("g8", "Funding"), ("g9", "Our evidence grade"),
]


def rtp(field):
    """A prose field inside a setting that validates its top-level tags.

    `media-with-text` content and `specification-table` value both refuse a bare Liquid
    expression ("All top level nodes must be '<p>', '<ul>', '<ol>' or '<h1>'-'<h6>'"), and both
    accept `| metafield_tag` — but that filter is exactly what makes the text invisible to
    extraction. A literal <p> wrapper satisfies the validator and keeps the output clean, so
    these fields store inline markup with no wrapping <p> of their own.
    """
    return "<p>{{ metaobject.%s.value }}</p>" % field


def rt(field):
    """A prose field. Rendered by `.value`, NEVER by `| metafield_tag`.

    `metafield_tag` wraps rich text in <div class="metafield-rich_text_field">, and trafilatura
    — what the AI crawlers and our own auditor read — discards that div and everything inside it.
    Measured on the live page 2026-09-24: 214 words extracted with the wrapper, 941 without it.
    The byline, the verdict, every at-a-glance value, the limitations and the citation were all
    invisible. So these fields are multi_line_text_field holding HTML, emitted raw.
    """
    return "{{ metaobject.%s.value }}" % field


def val(field):
    """A single-line, multi-line or file_reference field."""
    return "{{ metaobject.%s.value }}" % field


def build():
    return {
        "sections": {
            # ---- the sub-page header banner -------------------------------------------------
            "banner": {
                "type": "image-with-text-overlay",
                "blocks": {
                    "eyebrow": {"type": "subheading", "settings": {"text": val("eyebrow")}},
                    "head": {"type": "liquid", "settings": {"liquid": rt("hero_text")}},
                },
                "block_order": ["eyebrow", "head"],
                "settings": {
                    "full_width": True, "allow_transparent_header": False,
                    "enable_parallax": False, "image_size": "sm",
                    "image": val("banner"), "mobile_image": val("banner_mobile"),
                    "mobile_text_position": "place-self-start-center text-center",
                    "desktop_text_position": "sm:place-self-center-start sm:text-start",
                    "text_color": "#ffffff", "overlay_color": INK, "overlay_opacity": 28,
                },
            },
            # ---- the three key numbers ------------------------------------------------------
            "figures": {
                "type": "impact-text",
                "blocks": {
                    f"s{i}": {"type": "item", "settings": {
                        "animate_impact_text": False,
                        "title": val(f"fig{i}_value"),
                        "subheading": val(f"fig{i}_label"),
                        "content": rtp(f"fig{i}_body")}}
                    for i in (1, 2, 3)
                },
                "block_order": ["s1", "s2", "s3"],
                # mirrors the hubs' stats band exactly, so a reader arriving from a hub
                # meets the same treatment rather than a downgrade
                "settings": {"full_width": True, "stack_mobile": True,
                             "text_alignment": "center", "impact_text_style": "fill",
                             "text_divider": "none", "impact_text_size_ratio": 0.7,
                             "background": BONE, "heading_text_color": "#014EB1",
                             "text_color": INK},
            },
            # ---- byline, the quotable answer, our verdict -----------------------------------
            "answer": {
                "type": "rich-text",
                "blocks": {"a": {"type": "liquid", "settings": {"liquid": rt("intro")}},
                           # the two pilot pages still hold their whole body in `sections_html`.
                           # As a block it costs nothing when the field is blank; as a section it
                           # left ~200px of dead band on every page that does not use it.
                           "l": {"type": "liquid", "settings": {"liquid": val("sections_html")}}},
                "block_order": ["a", "l"],
                "settings": {"full_width": True, "content_width": "medium",
                             "text_position": "center", "background": WHITE},
            },
            # ---- at a glance ----------------------------------------------------------------
            "glance": {
                "type": "specification-table",
                "blocks": {
                    key: {"type": "row", "settings": {"heading": label, "value": rtp(key)}}
                    for key, label in GLANCE_ROWS
                },
                "block_order": [k for k, _ in GLANCE_ROWS],
                "settings": {"full_width": True, "subheading": "", "title": "",
                             "text_position": "center", "max_rows": 10,
                             "background": BONE, "chart_background": WHITE,
                             "content": "<h2>At a glance</h2><p>The nine things worth knowing "
                                        "before you weigh what this trial found.</p>"},
            },
            # ---- the chart ------------------------------------------------------------------
            # A stock rich-text section with a stock `liquid` block. NOT custom-html: its `html`
            # setting refuses Liquid outright ("can't include Liquid syntax without valid dynamic
            # sources"), so the hubs' custom-html route cannot carry per-study content at all.
            "chart": {
                "type": "rich-text",
                "blocks": {
                    "c": {"type": "liquid", "settings": {"liquid":
                        '<h2 style="text-align:center">What the measurements showed</h2>'
                        + val("chart_html")}},
                },
                "block_order": ["c"],
                "settings": {"full_width": True, "content_width": "large",
                             "text_position": "center", "background": WHITE},
            },
            # ---- what the researchers did ---------------------------------------------------
            "story": {
                "type": "media-with-text",
                "blocks": {"m": {"type": "image", "settings": {
                    "image": val("story_image"), "media_width": 50, "media_position": "start",
                    "text_position": "place-self-center-start text-start", "icon": "none",
                    "icon_width": 48, "title": "What the researchers did",
                    "content": rtp("story"),
                    "background": WHITE, "text_color": INK}}},
                "block_order": ["m"],
                "settings": {"full_width": False},
            },
            # ---- what this study does not show: the dark band --------------------------------
            "limits": {
                "type": "rich-text",
                "blocks": {
                    "b": {"type": "liquid", "settings": {"liquid": rt("limits")}},
                },
                "block_order": ["b"],
                # left-aligned: a centred numbered list leaves the numerals ragged, and these
                # six items are the page's argument, not a pull quote
                "settings": {"full_width": True, "content_width": "medium",
                             "text_position": "start", "background": INK,
                             "text_color": "#ffffff"},
            },
            # ---- background on the ingredient ------------------------------------------------
            # The auditors marked the page down for having no definition of GHK-Cu and for
            # depth: it appraised one trial with no account of what the ingredient is.
            "context": {
                "type": "rich-text",
                "blocks": {"c": {"type": "liquid", "settings": {"liquid": rt("context_html")}}},
                "block_order": ["c"],
                "settings": {"full_width": True, "content_width": "medium",
                             "text_position": "center", "background": WHITE},
            },
            # ---- common questions -------------------------------------------------------------
            "faq": {
                "type": "rich-text",
                "blocks": {"f": {"type": "liquid", "settings": {"liquid": rt("faq_html")}}},
                "block_order": ["f"],
                "settings": {"full_width": True, "content_width": "medium",
                             "text_position": "center", "background": BONE},
            },
            # ---- what it means for our products ----------------------------------------------
            "means": {
                "type": "rich-text",
                "blocks": {
                    "b": {"type": "liquid", "settings": {"liquid": rt("meaning")}},
                    "b1": {"type": "button", "settings": {
                        "style": "solid", "size": "base",
                        "text": "Read the full evidence", "url": val("hub_url")}},
                    "b2": {"type": "button", "settings": {
                        "style": "outline", "size": "base",
                        "text": "See the product", "url": val("product_url")}},
                },
                "block_order": ["b", "b1", "b2"],
                "settings": {"full_width": True, "content_width": "medium",
                             "text_position": "center", "background": WHITE},
            },
            # ---- reference + schema -----------------------------------------------------------
            "reference": {
                "type": "rich-text",
                "blocks": {
                    "r": {"type": "liquid", "settings": {"liquid": rt("reference")}},
                    "ld": {"type": "liquid", "settings": {"liquid": val("jsonld")}},
                },
                "block_order": ["r", "ld"],
                "settings": {"full_width": True, "content_width": "medium",
                             "text_position": "center", "background": BONE},
            },
        },
        "order": ["banner", "figures", "answer", "glance", "chart",
                  "story", "limits", "context", "faq", "means", "reference"],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    raw = hu.read_file(TPL)
    m = re.match(r"^\s*(/\*.*?\*/\s*)+", raw, re.S)   # Shopify prepends SEVERAL comments
    hdr = raw[:m.end()] if m else ""
    j = build()
    out = hdr + json.dumps(j, indent=2, ensure_ascii=False)
    types = sorted({s["type"] for s in j["sections"].values()})
    custom = [k for k, s in j["sections"].items() if s["type"] == "custom-html"]
    print(f"  {len(j['sections'])} sections · types: {', '.join(types)}")
    print(f"  custom-html: {custom or 'none'}  (the hubs render charts this way too)")
    if not a.apply:
        print("  dry run — pass --apply to upload")
        return 0
    pathlib.Path(ROOT / f"backups/metaobject-study-{datetime.datetime.now():%Y%m%d-%H%M%S}.json").write_text(raw)
    r = hu.gql('mutation($t:ID!,$f:[OnlineStoreThemeFilesUpsertFileInput!]!){ themeFilesUpsert(themeId:$t, files:$f)'
               '{ userErrors{field message} } }',
               {"t": hu.THEME, "f": [{"filename": TPL, "body": {"type": "TEXT", "value": out}}]})["themeFilesUpsert"]
    if r["userErrors"]:
        sys.exit(f"  ✗ {r['userErrors']}")
    print("  ✓ uploaded")
    return 0


if __name__ == "__main__":
    sys.exit(main())
