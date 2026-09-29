"""Offline tests for scripts/build-clinical-studies.py — the transforms that turn a hub's evidence table
into a block of the Clinical studies index. No Shopify calls.

Run:  python3 -m pytest tests/ -q
"""
import importlib.util
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
_s = importlib.util.spec_from_file_location("bcs", ROOT / "scripts/build-clinical-studies.py")
bcs = importlib.util.module_from_spec(_s)
_argv, sys.argv = sys.argv, [sys.argv[0]]
_s.loader.exec_module(bcs)
sys.argv = _argv

HUB_TABLE = (
    '<style>.est{}</style>\n<div class="est" id="evidence-sources">\n'
    '<h2 class="est__h">Argireline Evidence &amp; Sources</h2>\n'
    '<p class="est__lead">Every study this page relies on. Graded <strong>A</strong> controlled.</p>\n'
    '<div class="est__wrap"><table><thead><tr><th>Study</th><th>Grade</th><th>What it found</th></tr></thead><tbody>'
    '<tr><td class="est__study"><p class="sgref__ti est__ti">The efficacy study of the combination</p>'
    '<p class="est__me">Raikou et al., 2017 &middot; J Cosmet Dermatol</p>'
    '<a class="est__lk" href="https://pubmed.ncbi.nlm.nih.gov/28150423/">View on PubMed &rarr;</a></td>'
    '<td class="est__grade">A</td><td>24 women.</td></tr>'
    '<tr><td class="est__study"><p class="sgref__ti est__ti">In vitro skin penetration</p>'
    '<p class="est__me">Kraeling et al., 2015 &middot; Cutan Ocul Toxicol</p>'
    '<a class="est__lk" href="https://pubmed.ncbi.nlm.nih.gov/24303801/">View on PubMed &rarr;</a></td>'
    '<td class="est__grade">C</td><td>Lab.</td></tr>'
    '</tbody></table></div>\n<p class="est__key">Published titles are quoted exactly.</p>\n</div>\n'
    '<script type="application/ld+json" id="sgx-webpage-jsonld">{"@type": "WebPage", "url": "hub"}</script>'
)
KEYS = [("Raikou", "2017", "argireline-forehead-roughness-trial-raikou-2017"),
        ("Wang", "2013", "argireline-crows-feet-trial-wang-2013")]


def run(loc="en", last=False):
    return bcs.transform(HUB_TABLE, loc, "argireline", "Argireline®", "acetyl-hexapeptide-8-research",
                         "#3E4A52", "#E9ECEE", KEYS, last)


def test_the_hubs_own_webpage_schema_is_stripped():
    """Left in, the index would carry five other pages' WebPage JSON-LD."""
    h, _ = run()
    assert "ld+json" not in h and '"WebPage"' not in h


def test_rows_are_counted_and_the_lead_links_the_hub_with_its_head_term():
    h, n = run()
    assert n == 2
    assert '<p class="est__lead">What it is and what the evidence shows is explained on the ' in h
    assert '<a href="/pages/acetyl-hexapeptide-8-research">Argireline®</a> research page.' in h
    assert "Graded <strong>A</strong>" not in h            # the legend moves to the intro, once
    assert "<h2" not in h                                   # the section bar above carries the heading


def test_a_study_with_its_own_page_gets_the_appraisal_link_and_one_without_does_not():
    h, _ = run()
    raikou, kraeling = h.split("Kraeling")[0], h.split("Kraeling")[1]
    assert 'href="/pages/study/argireline-forehead-roughness-trial-raikou-2017">Read our appraisal →</a>' in raikou
    assert "Read our appraisal" not in kraeling


def test_translated_links_carry_the_locale_prefix():
    h, _ = run("de")
    assert 'href="/de/pages/acetyl-hexapeptide-8-research"' in h
    assert 'href="/de/pages/study/argireline-forehead-roughness-trial-raikou-2017">Unsere Bewertung lesen →' in h


def test_the_block_takes_its_jump_id_and_accent():
    h, _ = run()
    assert 'id="argireline-table"' in h and 'id="evidence-sources"' not in h
    assert '<div class="est" style="--sg-accent:#3E4A52;--sg-accent-tint:#E9ECEE"' in h


def test_the_footnote_stays_only_on_the_last_table():
    assert "est__key" not in run(last=False)[0]
    assert "est__key" in run(last=True)[0]


def test_scholarly_items_read_title_and_source():
    assert bcs.scholarly_items(HUB_TABLE) == [
        ("The efficacy study of the combination", "https://pubmed.ncbi.nlm.nih.gov/28150423/"),
        ("In vitro skin penetration", "https://pubmed.ncbi.nlm.nih.gov/24303801/")]


def test_appraisal_keys_read_both_config_shapes():
    stock = json.loads((ROOT / "configs/studies/argireline-forehead-roughness-trial-raikou-2017.json").read_text())
    pilot = json.loads((ROOT / "configs/studies/argireline-crows-feet-trial-wang-2013.json").read_text())
    assert bcs.appraisal_keys([stock, pilot]) == [
        ("Raikou", "2017", "argireline-forehead-roughness-trial-raikou-2017"),
        ("Wang", "2013", "argireline-crows-feet-trial-wang-2013")]


def test_the_page_schema_is_a_collection_with_a_breadcrumb():
    ld = bcs.jsonld("de", [("T", "https://x")], ["a"], 32)
    page, crumb = ld["@graph"]
    assert page["@type"] == "CollectionPage" and page["url"].endswith("/de/pages/clinical-studies")
    assert page["mainEntity"]["numberOfItems"] == 1 and page["hasPart"][0]["url"].endswith("/de/pages/study/a")
    assert [i["name"] for i in crumb["itemListElement"]] == ["Skingenetix", "Wissenschaft", "Klinische Studien"]


# ---------------------------------------------------------------- design critique 2026-09-29 fixes

def graded(grade_classes):
    rows = "".join(f'<tr><td class="est__study"><p class="sgref__ti est__ti">T{i}</p><p class="est__me">X et al., 2001</p>'
                   f'<a class="est__lk" href="https://x/{i}">View</a></td><td class="est__grade">'
                   f'<span class="est__pill est__pill--{g}">{g}</span></td><td>f</td></tr>'
                   for i, g in enumerate(grade_classes))
    return (f'<div class="est" id="evidence-sources"><h2 class="est__h">H</h2><p class="est__lead">L</p>'
            f'<div class="est__wrap"><table><thead><tr><th>S</th></tr></thead><tbody>{rows}</tbody></table></div></div>')


def test_rows_are_sorted_strongest_grade_first():
    """F-medium: no visible sort order. A, B, C, D, then reviews; the hub's own order within a grade."""
    h, _ = bcs.transform(graded(["r", "c", "a", "b", "a", "d"]), "en", "s", "L", "hub", "#000", "#fff", [], True)
    assert [x for x in __import__("re").findall(r"est__pill--(\w)", h)] == ["a", "a", "b", "c", "d", "r"]
    assert h.index(">T2<") < h.index(">T4<")               # stable within a grade


def fake_tables():
    return [(slug, label, hub, "#123456", "#abcdef", {l: graded(["a", "r"]) for l in bcs.LOCALES}, "test",
             {l: f"Best {slug} {l}" for l in bcs.LOCALES})
            for slug, label, hub, *_ in bcs.HUBS]


def test_tables_sit_on_white_and_the_closing_on_bone():
    """F2: left unset, the custom-html sections took the bone intro's ground, and a Review pill vanished (1.00:1)."""
    spec, _, _ = bcs.build_spec(fake_tables(), [], "2026-09-29")
    secs = {a["id"]: a["section"] for a in spec["add_sections"]}
    assert all(s["settings"]["background"] == "#ffffff" for k, s in secs.items() if k.startswith("ev_"))
    assert secs["closing"]["settings"]["background"] == "#F0F0F0"


def test_ingredient_names_follow_each_locale():
    """F12: the German page said 'Glutathione' where the German hub says 'Glutathion'."""
    spec, _, _ = bcs.build_spec(fake_tables(), [], "2026-09-29")
    secs = {a["id"]: a["section"] for a in spec["add_sections"]}
    assert "<h2>Glutathion: Studien</h2>" in secs["bar_glutathione"]["blocks"]["head"]["settings"]["content"]["de"]
    assert "Kupferpeptid (GHK-Cu): 2 Studien" in secs["index"]["settings"]["html"]["de"]


def test_the_intro_is_dated_and_the_closing_leads_to_the_shop():
    spec, _, _ = bcs.build_spec(fake_tables(), [], "2026-09-29")
    secs = {a["id"]: a["section"] for a in spec["add_sections"]}
    assert "Zuletzt aktualisiert am 29. September 2026." in secs["intro"]["blocks"]["t"]["settings"]["content"]["de"]
    assert "<em>By Skingenetix. Every figure checked" in secs["intro"]["blocks"]["t"]["settings"]["content"]["en"]
    assert "29 de septiembre de 2026" in secs["intro"]["blocks"]["t"]["settings"]["content"]["es"]
    assert 'href="/fr/collections/all">notre boutique</a>' in secs["closing"]["blocks"]["t"]["settings"]["content"]["fr"]


def test_no_custom_html_value_carries_liquid_braces():
    """Shopify refuses a custom-html setting containing "{{" or "}}" (a media query closing as ";}}" did it,
    2026-09-29) — memory custom-html-rejects-double-braces."""
    spec, _, _ = bcs.build_spec(fake_tables(), [], "2026-09-29")
    for a in spec["add_sections"]:
        if a["section"]["type"] == "custom-html":
            for loc, v in a["section"]["settings"]["html"].items():
                assert "}}" not in v and "{{" not in v, (a["id"], loc)



# ---------------------------------------------------------------- the science-page layout (Malcolm, 2026-09-29)

def layout():
    spec, _, _ = bcs.build_spec(fake_tables(), [("Raikou", "2017", "raikou-page")], "2026-09-29", "<style>.evd{}</style>")
    return spec, [a["id"] for a in spec["add_sections"]], {a["id"]: a["section"] for a in spec["add_sections"]}


def test_the_page_follows_the_science_page_order():
    """banner · key figures · overview · quick-link index · (picture bar + table) per ingredient · closing."""
    _, order, _ = layout()
    assert order[:4] == ["banner", "stats", "intro", "index"]
    assert order[4:6] == ["bar_copper_peptide", "ev_copper_peptide"] and order[-1] == "closing"
    assert order.count("closing") == 1 and len(order) == 4 + 2 * len(bcs.HUBS) + 1


def test_the_key_figures_count_studies_grade_a_trials_and_appraisals():
    _, _, secs = layout()
    titles = [b["settings"]["title"] for b in secs["stats"]["blocks"].values()]
    assert titles == [str(2 * len(bcs.HUBS)), str(len(bcs.HUBS)), "1"]   # fake tables: one A and one Review each


def test_quick_links_open_each_section_bar_in_its_accent():
    _, _, secs = layout()
    html = secs["index"]["settings"]["html"]["de"]
    assert html.startswith("<style>.evd{ }</style>") or html.startswith("<style>.evd{}</style>")
    assert html.count('class="evd__row"') == len(bcs.HUBS)
    assert '<a class="evd__row" href="#pdrn" style="--sg-accent:#123456">' in html
    assert "Stärkstes Ergebnis: Best pdrn de" in html


def test_each_section_bar_carries_the_anchor_heading_and_its_own_images():
    _, _, secs = layout()
    bar = secs["bar_pdrn"]
    assert 'id="pdrn"' in bar["blocks"]["anchor"]["settings"]["liquid"]
    assert bar["settings"]["image"].endswith("skingenetix-clinical-studies-pdrn-bar.jpg")
    assert bar["settings"]["mobile_image"].endswith("skingenetix-clinical-studies-pdrn-bar-mobile.jpg")
    assert bar["settings"]["image_size"] == "auto"
    assert "<h2>PDRN studies</h2><p>2 studies, graded, strongest first.</p>" in bar["blocks"]["head"]["settings"]["content"]["en"]
    images = [secs[k]["settings"]["image"] for k in secs if k.startswith("bar_")]
    assert len(set(images)) == len(images)                  # unique image per ingredient


def test_grade_a_count_ignores_the_tables_own_css():
    """Rendered 13 controlled trials where there are 8: the count matched `.est__pill--a{` inside each copied
    table's <style> as well as the badges (2026-09-29). Count badges in rows only."""
    t = fake_tables()
    t = [(s, l, h, a, ti, {k: "<style>.est__pill--a{color:red}</style>" + v for k, v in vals.items()}, src, c)
         for s, l, h, a, ti, vals, src, c in t]
    spec, _, _ = bcs.build_spec(t, [], "2026-09-29")
    secs = {a["id"]: a["section"] for a in spec["add_sections"]}
    assert secs["stats"]["blocks"]["s2"]["settings"]["title"] == str(len(bcs.HUBS))
