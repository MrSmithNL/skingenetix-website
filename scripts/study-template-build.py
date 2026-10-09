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
  limits    media-with-text           how to read this result (white, like the other media rows)
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

# Design critique 2026-09-26 (docs/audits/2026-09-26-study-pages-design-critique.md) fixes, T1/T4/T5/T9.
#
# T1 — the key figures took a fixed template colour (copper blue), so an Argireline page showed its
# −7.4% in blue above a slate chart. Malcolm's rule (2026-09-24): each ingredient page uses its own
# accent. A colour setting cannot read a metaobject field, and the definition has no free field, so a
# stock `liquid` block picks the accent from the study's handle and overrides the figures' inline
# --text-color on the numbers only (the section wrapper carries .text-custom too, and matching it
# turned every label and note blue on 2026-09-26). Rung 4 (custom code) — forced: no stock setting varies per metaobject entry.
# Keep the braces on separate lines: "}}" trips Shopify's Liquid validation.
ACCENT = """{%- liquid
  assign h = metaobject.system.handle
  assign acc = '1 78 177'
  if h contains 'argireline' or h contains 'acetyl-hexapeptide'
    assign acc = '62 74 82'
  elsif h contains 'pdrn'
    assign acc = '158 79 92'
  elsif h contains 'matrixyl' or h contains 'palmitoyl'
    assign acc = '1 101 105'
  elsif h contains 'glutathione'
    assign acc = '138 105 20'
  endif
-%}
<style>
  .shopify-section--impact-text .impact-text__text .text-custom {
    --text-color: {{ acc }} !important;
  }
</style>"""

# T4 — long prose was centred at 102 characters a line in 15px, and the answer paragraph (the one an
# AI engine quotes) had lost its emphasis. Left-aligned by the stock text_position setting; the
# column width and the answer size need section CSS (≤ 500 characters, no `content:`).
# text_position "start" also sets the flex container to justify-start, which pushed the column to
# the left edge; centre the column, keep the text left-aligned inside it
READING = [".rich-text {justify-content: center;}", ".prose {max-width: 66ch; margin-inline: auto;}"]
# the liquid block wraps its output in a bare <div>, so the answer is the third <p> inside it
ANSWER = READING + [".prose div > p:nth-of-type(3) {font-size: 20px; line-height: 1.5;}",
                    "@media (max-width: 699px) {.prose div > p:nth-of-type(3) {font-size: 17px;} }"]

# The "Before you try it" note (Malcolm, 2026-09-30; docs/research-2026-09-30-safety-notes-on-study-articles.md).
# Its words live in the theme's locale files under skingenetix.study_safety (six languages, one source file:
# configs/study-safety-note.json, uploaded with --safety-locales), so the languages cannot drift. The PDRN line —
# PDRN is salmon-derived, fish allergy — shows only on PDRN studies. Use guidance only: EU claims rules make any
# "safe" statement a claim that needs evidence.
SAFETY = """{%- liquid
  assign h = metaobject.system.handle
-%}
<div class="study-safety">
<h2>{{ 'skingenetix.study_safety.title' | t }}</h2>
<p>{{ 'skingenetix.study_safety.body' | t }}</p>
{%- if h contains 'pdrn' -%}
<p><strong>{{ 'skingenetix.study_safety.pdrn' | t }}</strong></p>
{%- endif -%}
</div>"""
SAFETY_KEYS = ("title", "body", "pdrn")
LOCALE_FILES = {"en": "locales/en.default.json", "de": "locales/de.json", "nl": "locales/nl.json",
                "fr": "locales/fr.json", "es": "locales/es.json", "it": "locales/it.json"}

# The nine rows of "At a glance". Identical on every study page by design — a reader comparing
# two studies should find the same nine questions answered in the same order.
# The same four questions on every study page. Fixed here rather than per study so a reader
# comparing two trials finds the same questions answered in the same order — and so they
# translate once, as template resources.
FAQ_QUESTIONS = [
    ("faq_a1", "Does this trial prove the ingredient works?"),
    ("faq_a2", "What concentration did the study use?"),
    ("faq_a3", "Is the trial independent?"),
    ("faq_a4", "Do Skingenetix products reproduce this result?"),
]

GLANCE_ROWS = [
    ("g1", "Design"), ("g2", "Participants"), ("g3", "What was applied"),
    ("g4", "Compared with"), ("g5", "Duration"), ("g6", "How it was measured"),
    ("g7", "Concentration"), ("g8", "Funding"), ("g9", "Our evidence grade"),
]


CHART_HEADING = ("{%- case request.locale.iso_code -%}"
                 "{%- when 'de' -%}Was die Messungen zeigten"
                 "{%- when 'nl' -%}Wat de metingen lieten zien"
                 "{%- when 'fr' -%}Ce que les mesures ont montré"
                 "{%- when 'es' -%}Qué mostraron las mediciones"
                 "{%- when 'it' -%}Cosa hanno mostrato le misurazioni"
                 "{%- else -%}What the measurements showed{%- endcase -%}")


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
                    "accent": {"type": "liquid", "settings": {"liquid": ACCENT}},
                },
                "block_order": ["eyebrow", "head", "accent"],
                "settings": {
                    "full_width": True, "allow_transparent_header": False,
                    "enable_parallax": False, "image_size": "sm",
                    "image": val("banner"), "mobile_image": val("banner_mobile"),
                    "mobile_text_position": "place-self-start-center text-center",
                    "desktop_text_position": "sm:place-self-center-start sm:text-start",
                    "text_color": "#ffffff", "overlay_color": INK, "overlay_opacity": 28,
                },
                # The banner shows at once instead of fading in (the fade held the largest paint back about 10 s);
                # scripts/hero-reveal-off.py, ADR-2026-10-08-X. Claude (Opus 5.5), 2026-10-09.
                "custom_css": ["image-banner{opacity:1!important}"],
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
                "custom_css": ANSWER,
                "settings": {"full_width": True, "content_width": "medium",
                             "text_position": "start", "background": WHITE},
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
                    # A liquid setting is not translatable, so the heading is chosen by locale here (2026-09-30:
                    # it showed in English on /de…/it once Wang and Ye went live translated on this template).
                    "c": {"type": "liquid", "settings": {"liquid":
                        '<h2 style="text-align:center">' + CHART_HEADING + '</h2>'
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
                    "icon_width": 48, "title": "",
                    "content": "<h2>" + "What the researchers did" + "</h2>" + rtp("story"),
                    "background": WHITE, "text_color": INK}}},
                "block_order": ["m"],
                "settings": {"full_width": False},
            },
            # ---- how to read this result -----------------------------------------------------
            # Same shape and the same ground as the other two media rows — Malcolm, 2026-09-24:
            # no black backgrounds, and these content blocks stay identical. The image sits on
            # the right so the three rows alternate left / right / left down the page.
            # Retitled 2026-09-26 (ADR-2026-09-26-L): the appraisal stays, written as plain facts
            # with the positive side first, not as "what this study does not show".
            "limits": {
                "type": "media-with-text",
                "blocks": {"m": {"type": "image", "settings": {
                    "image": "shopify://shop_images/"
                             "skingenetix-philosophy-published-research-microscope-petri-dish.jpg",
                    "media_width": 50, "media_position": "end",
                    "text_position": "place-self-center-start text-start", "icon": "none",
                    "icon_width": 48, "title": "",
                    # <ol> is one of the top-level tags this setting accepts, so the field holds
                    # only the <li> items
                    "content": "<h2>" + "How to read this result" + "</h2>" + "<ol>" + val("limits") + "</ol>",
                    "background": WHITE, "text_color": INK}}},
                "block_order": ["m"],
                "settings": {"full_width": False, "background": WHITE},
            },
            # ---- background on the ingredient ------------------------------------------------
            # The auditors marked the page down for having no definition of GHK-Cu and for
            # depth: it appraised one trial with no account of what the ingredient is.
            "context": {
                "type": "media-with-text",
                "blocks": {"m": {"type": "image", "settings": {
                    "image": "shopify://shop_images/skingenetix-menu-scientific-research-2026.jpg",
                    "media_width": 50, "media_position": "start",
                    "text_position": "place-self-center-start text-start", "icon": "none",
                    "icon_width": 48, "title": "",
                    "content": "<h2>" + "Where this trial sits in the evidence" + "</h2>" + rtp("context_html"), "background": WHITE, "text_color": INK}}},
                "block_order": ["m"],
                "settings": {"full_width": False, "background": BONE},
            },
            # ---- common questions -------------------------------------------------------------
            "faq": {
                "type": "faq",
                "blocks": {
                    key: {"type": "item", "settings": {"title": q, "content": rtp(key)}}
                    for key, q in FAQ_QUESTIONS
                },
                "block_order": [k for k, _ in FAQ_QUESTIONS],
                # the theme ships customer-support defaults in this section ("Our customer
                # support is available Monday to Friday...") — blanked, they are not this page's job
                "settings": {"full_width": False, "subheading": "", "text_position": "center",
                             "title": "Common questions about this trial",
                             "content": "", "background": WHITE,
                             "team_avatar": "", "team_avatar_width": 50,
                             "support_hours": "", "answer_time": "", "show_contact": False},
            },
            # ---- before you try it (safety note) ---------------------------------------------
            # Right before the product buttons: the research placed it after the trial's side effects
            # and limits and before the product link, as one calm block — not a footer, not a pop-up.
            "safety": {
                "type": "rich-text",
                "blocks": {"n": {"type": "liquid", "settings": {"liquid": SAFETY}}},
                "block_order": ["n"],
                "custom_css": READING,
                "settings": {"full_width": True, "content_width": "medium",
                             "text_position": "start", "background": BONE},
            },
            # ---- what it means for our products ----------------------------------------------
            "means": {
                "type": "rich-text",
                "blocks": {
                    "b": {"type": "liquid", "settings": {"liquid": rt("meaning")}},
                    "b1": {"type": "button", "settings": {
                        "style": "solid", "size": "lg",
                        "text": "Read the full evidence", "url": val("hub_url")}},
                    "b2": {"type": "button", "settings": {
                        "style": "outline", "size": "lg",
                        "text": "See the product", "url": val("product_url")}},
                },
                "block_order": ["b", "b1", "b2"],
                "custom_css": READING,
                "settings": {"full_width": True, "content_width": "medium",
                             "text_position": "start", "background": BONE},
            },
            # ---- reference + schema -----------------------------------------------------------
            "reference": {
                "type": "rich-text",
                "blocks": {
                    "r": {"type": "liquid", "settings": {"liquid": rt("reference")}},
                    "ld": {"type": "liquid", "settings": {"liquid": val("jsonld")}},
                },
                "block_order": ["r", "ld"],
                "custom_css": READING,
                "settings": {"full_width": True, "content_width": "medium",
                             "text_position": "start", "background": WHITE},
            },
        },
        "order": ["banner", "figures", "answer", "glance", "chart",
                  "story", "limits", "context", "faq", "safety", "means", "reference"],
    }


ARTICLE_TPL = "templates/article.clinical-study.json"
PILOT_TPL = "templates/article.clinical-study-pilot.json"
ENTRY = "article.metafields.study.entry.value."

# ---- one section per result, and "how it works" (Malcolm, 2026-10-01) ------------------------------------------------
# "every study blog article should have seperate content sections for each of the proven trial outcomes with before and
# after images where this can be used (similar to the ingredient science pages). And these should also be separate
# content blocks for the proven working active effects of what was tested to explain the workings of what they were
# testing on skin (also like the science ingredient pages)."
#
# Both reuse the science pages' own section, research-before-after (key_findings_ba on the hubs): the stock
# media-with-text has no labels and the stock before-after slider takes two files and two labels (rung 1, an existing
# section, though our own). The study entry is full — 40 of 40 fields, read live 2026-10-01 — so the content lives in a
# companion `study_detail` entry that the article reaches through study.detail (fields: build-study-page.py
# DETAIL_FIELDS). The slots are fixed; the section draws nothing for an empty slot, or for a section with none filled.
DETAIL_ENTRY = "article.metafields.study.detail.value."
DRAFT_DETAIL_ENTRY = "article.metafields.study.draft_detail.value."
OUTCOME_SLOTS, MECHANISM_SLOTS = 4, 3


def detail_sections():
    """The results section (labelled before/after pictures) and the how-it-works section (plain pictures)."""
    def d(field):
        return "{{ " + DETAIL_ENTRY + field + ".value }}"

    def block(slot, position, labels):
        return {"type": "finding", "settings": {
            "image": d(f"{slot}_image"), "media_position": position,
            "before_label": d(f"{slot}_before") if labels else "",
            "after_label": d(f"{slot}_after") if labels else "",
            "result_label": d(f"{slot}_result") if labels else "",
            "note_label": "",                     # Malcolm, 2026-09-22: "No AI disclosure please."
            "label_background": "#1a1a1a", "label_text_color": "#ffffff",
            "subheading": "", "title": d(f"{slot}_title"),
            # the richtext setting validates its top-level tags, like media-with-text (rtp() above)
            "content": "<p>" + d(f"{slot}_body") + "</p>"}}

    outs = [f"o{i}" for i in range(1, OUTCOME_SLOTS + 1)]
    mechs = [f"m{j}" for j in range(1, MECHANISM_SLOTS + 1)]
    return {
        # pictures alternate left / right, as on the hubs
        "outcomes": {"type": "research-before-after",
                     "blocks": {k: block(k, "start" if i % 2 else "end", True) for i, k in enumerate(outs, 1)},
                     "block_order": outs, "settings": {"title": d("outcomes_heading")}},
        # the first sits opposite "What the researchers did", whose picture is on the left. When a study has no
        # how-it-works block, the empty section hands on that row's background hash (0, no background) so the
        # theme still closes the gap to "How to read this result" (an 80px band opened otherwise, 2026-10-02)
        "mechanism": {"type": "research-before-after",
                      "blocks": {k: block(k, "end" if j % 2 else "start", False) for j, k in enumerate(mechs, 1)},
                      "block_order": mechs, "settings": {"title": d("mechanism_heading"), "empty_previous_hash": "0"}},
    }


def build_article():
    """The same page as an ARTICLE template for the Clinical studies blog (decision 2026-09-29).

    The study stays a metaobject — its fields, and their six-locale translations, are untouched — and each blog
    article points at it through the article metafield study.entry. So every `metaobject.<field>` becomes
    `article.metafields.study.entry.value.<field>`, the accent is picked from the article's handle (the same
    handle as the study), and the eyebrow block goes: the breadcrumb (Science › Clinical studies › ingredient)
    is written into hero_text by build-study-page.py, where it translates with the rest of the banner.
    """
    def swap(node):
        if isinstance(node, dict):
            return {k: swap(v) for k, v in node.items()}
        if isinstance(node, list):
            return [swap(v) for v in node]
        if isinstance(node, str):
            return node.replace("metaobject.system.handle", "article.handle").replace("metaobject.", ENTRY)
        return node
    j = swap(build())
    banner = j["sections"]["banner"]
    banner["blocks"].pop("eyebrow", None)
    banner["block_order"] = [b for b in banner["block_order"] if b != "eyebrow"]
    # results straight after "At a glance", before the chart that sums them up (the hubs' key_findings_ba → charts);
    # how it works straight after "What the researchers did"
    j["sections"].update(detail_sections())
    j["order"].insert(j["order"].index("glance") + 1, "outcomes")
    j["order"].insert(j["order"].index("story") + 1, "mechanism")
    return j


def build_pilot_article():
    """The article template for the two PILOT studies (Wang 2013, Ye 2026) until they are rebuilt.

    A pilot keeps its whole designed body in `sections_html` and leaves every stock field empty, so the
    stock template printed seven empty section headings under it ("What the measurements showed", "How to
    read this result", "Where this trial sits in the evidence", "Common questions about this trial", …) and
    the reference twice — found by the central SEO/GEO/AISO audit on 2026-09-29. This template keeps only
    what a pilot fills: the banner, the intro and body, and the JSON-LD (the body carries its own reference).
    Assign it with the article's template suffix `clinical-study-pilot`; move the article back to
    `clinical-study` once its study is rebuilt in the stock-template format.
    """
    j = build_article()
    keep = ["banner", "answer", "safety", "reference"]
    j["sections"] = {k: j["sections"][k] for k in keep}
    ref = j["sections"]["reference"]
    ref["blocks"] = {"ld": ref["blocks"]["ld"]}
    ref["block_order"] = ["ld"]
    j["order"] = keep
    return j


DRAFT_TPL = "templates/article.clinical-study-draft.json"
DRAFT_ENTRY = "article.metafields.study.draft.value."


def build_draft_article():
    """The stock article template reading the article's DRAFT study (Malcolm, 2026-09-30: English first).

    Wang 2013 and Ye 2026 are live in six languages on the pilot template. Their stock-format rebuild goes into a
    separate study entry, `<handle>-draft` (build-study-page.py --preview), linked from the article's second
    metafield study.draft. This template reads only that, so ?view=clinical-study-draft shows the rebuild while the
    live article, which reads study.entry, is untouched until go-live.
    """
    def swap(node):
        if isinstance(node, dict):
            return {k: swap(v) for k, v in node.items()}
        if isinstance(node, list):
            return [swap(v) for v in node]
        if isinstance(node, str):
            return node.replace(ENTRY, DRAFT_ENTRY).replace(DETAIL_ENTRY, DRAFT_DETAIL_ENTRY)
        return node
    return swap(build_article())


def merge_locale(raw, strings):
    """A theme locale file with skingenetix.study_safety set to `strings`; everything else kept.

    Shopify prepends /* … */ comments to theme JSON; they are kept as they were.
    """
    m = re.match(r"^\s*(/\*.*?\*/\s*)+", raw, re.S)
    hdr = raw[:m.end()] if m else ""
    body = json.loads(raw[len(hdr):])
    body.setdefault("skingenetix", {})["study_safety"] = {k: strings[k] for k in SAFETY_KEYS}
    return hdr + json.dumps(body, indent=2, ensure_ascii=False)


def upload_safety_locales(apply):
    """Put the six-language note into the theme's locale files (before the templates reference it)."""
    note = json.loads((ROOT / "configs/study-safety-note.json").read_text())
    files = []
    for loc, filename in LOCALE_FILES.items():
        raw = hu.read_file(filename)
        files.append((filename, raw, merge_locale(raw, note[loc])))
        print(f"  {filename}: study_safety ← {note[loc]['title']!r}")
    if not apply:
        print("  dry run — pass --apply to upload")
        return 0
    stamp = f"{datetime.datetime.now():%Y%m%d-%H%M%S}"
    for filename, raw, _ in files:
        pathlib.Path(ROOT / f"backups/{filename.replace('/', '__')}-{stamp}").write_text(raw)
    r = hu.gql('mutation($t:ID!,$f:[OnlineStoreThemeFilesUpsertFileInput!]!){ themeFilesUpsert(themeId:$t, files:$f)'
               '{ userErrors{field message} } }',
               {"t": hu.THEME, "f": [{"filename": f, "body": {"type": "TEXT", "value": new}} for f, _, new in files]}
               )["themeFilesUpsert"]
    if r["userErrors"]:
        sys.exit(f"  ✗ {r['userErrors']}")
    print(f"  ✓ uploaded {len(files)} locale files (backups/*-{stamp})")
    return 0


SECTION = "sections/research-before-after.liquid"


def upload_section(apply):
    """Upload our research-before-after section from the repo (theme/ is its source of truth), backing up the live file.

    The results and how-it-works sections rely on it skipping empty slots (2026-10-01), so it goes up before any
    article template that has those sections. The science pages use the same file: check one after uploading.
    """
    new = (ROOT / "theme" / SECTION).read_text()
    raw = hu.read_file(SECTION)
    print(f"  {SECTION}: {len(raw)} → {len(new)} characters" + (" (unchanged)" if raw == new else ""))
    if not apply or raw == new:
        print("  dry run — pass --apply to upload" if not apply else "  nothing to upload")
        return 0
    pathlib.Path(ROOT / f"backups/section-research-before-after-{datetime.datetime.now():%Y%m%d-%H%M%S}.liquid").write_text(raw)
    r = hu.gql('mutation($t:ID!,$f:[OnlineStoreThemeFilesUpsertFileInput!]!){ themeFilesUpsert(themeId:$t, files:$f)'
               '{ userErrors{field message} } }',
               {"t": hu.THEME, "f": [{"filename": SECTION, "body": {"type": "TEXT", "value": new}}]})["themeFilesUpsert"]
    if r["userErrors"]:
        sys.exit(f"  ✗ {r['userErrors']}")
    print("  ✓ uploaded")
    return 0


def upload(filename, j, backup_name, apply):
    """Write one article template to the live theme, backing up what was there."""
    try:
        raw = hu.read_file(filename)
    except IndexError:                                       # a new template: no file yet
        raw = ""
    m = re.match(r"^\s*(/\*.*?\*/\s*)+", raw, re.S)
    hdr = raw[:m.end()] if m else ""
    out = hdr + json.dumps(j, indent=2, ensure_ascii=False)
    print(f"  {filename}: {len(j['sections'])} sections, entry fields via {ENTRY}")
    if not apply:
        print("  dry run — pass --apply to upload")
        return 0
    if raw:
        pathlib.Path(ROOT / f"backups/{backup_name}-{datetime.datetime.now():%Y%m%d-%H%M%S}.json").write_text(raw)
    r = hu.gql('mutation($t:ID!,$f:[OnlineStoreThemeFilesUpsertFileInput!]!){ themeFilesUpsert(themeId:$t, files:$f)'
               '{ userErrors{field message} } }',
               {"t": hu.THEME, "f": [{"filename": filename, "body": {"type": "TEXT", "value": out}}]})["themeFilesUpsert"]
    if r["userErrors"]:
        sys.exit(f"  ✗ {r['userErrors']}")
    print("  ✓ uploaded")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--article", action="store_true", help="build templates/article.clinical-study.json instead")
    ap.add_argument("--article-pilot", action="store_true",
                    help="build templates/article.clinical-study-pilot.json (the two pilot studies)")
    ap.add_argument("--article-draft", action="store_true",
                    help="build templates/article.clinical-study-draft.json (English-first preview of a rebuilt study)")
    ap.add_argument("--safety-locales", action="store_true",
                    help="upload the 'Before you try it' note into the six theme locale files")
    ap.add_argument("--section", action="store_true",
                    help="upload theme/sections/research-before-after.liquid (the results and how-it-works sections)")
    a = ap.parse_args()
    if a.section:
        return upload_section(a.apply)
    if a.safety_locales:
        return upload_safety_locales(a.apply)
    if a.article_pilot:
        return upload(PILOT_TPL, build_pilot_article(), "article-clinical-study-pilot", a.apply)
    if a.article_draft:
        return upload(DRAFT_TPL, build_draft_article(), "article-clinical-study-draft", a.apply)
    if a.article:
        j = build_article()
        try:
            raw = hu.read_file(ARTICLE_TPL)
        except IndexError:                                   # a new template: no file yet
            raw = ""
        m = re.match(r"^\s*(/\*.*?\*/\s*)+", raw, re.S)
        hdr = raw[:m.end()] if m else ""
        out = hdr + json.dumps(j, indent=2, ensure_ascii=False)
        print(f"  {ARTICLE_TPL}: {len(j['sections'])} sections, entry fields via {ENTRY}")
        if not a.apply:
            print("  dry run — pass --apply to upload")
            return 0
        if raw:
            pathlib.Path(ROOT / f"backups/article-clinical-study-{datetime.datetime.now():%Y%m%d-%H%M%S}.json").write_text(raw)
        r = hu.gql('mutation($t:ID!,$f:[OnlineStoreThemeFilesUpsertFileInput!]!){ themeFilesUpsert(themeId:$t, files:$f)'
                   '{ userErrors{field message} } }',
                   {"t": hu.THEME, "f": [{"filename": ARTICLE_TPL, "body": {"type": "TEXT", "value": out}}]})["themeFilesUpsert"]
        if r["userErrors"]:
            sys.exit(f"  ✗ {r['userErrors']}")
        print("  ✓ uploaded")
        return 0
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
