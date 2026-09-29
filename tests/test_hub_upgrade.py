"""Offline tests for scripts/hub-upgrade.py build() — no Shopify calls.

Run:  python3 -m pytest tests/ -q
"""
import copy
import importlib.util
import json
import pathlib

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
_s = importlib.util.spec_from_file_location("hu", ROOT / "scripts/hub-upgrade.py")
hu = importlib.util.module_from_spec(_s)
_s.loader.exec_module(hu)

L6 = ["en", "de", "nl", "fr", "es", "it"]


def six(text):
    return {l: text if l == "en" else f"[{l}] {text}" for l in L6}


REF_HTML = ('<style>.sgref{}</style><div class="sgref"><h2 class="sgref__h">Published References</h2>'
            '<div class="sgref__list"><div class="sgref__r"><div><p class="sgref__ti">Old</p></div>'
            '<a class="sgref__lk" href="https://pubmed.ncbi.nlm.nih.gov/1/">View on PubMed &rarr;</a></div></div></div>')


def template():
    return {"sections": {
        "overview": {"type": "rich-text", "settings": {"background": "#ffffff"},
                     "blocks": {"op": {"type": "richtext", "settings": {"content": "<p>old</p>"}}}, "block_order": ["op"]},
        "references": {"type": "custom-html", "settings": {"html": REF_HTML}},
        "faq": {"type": "faq", "settings": {"title": "FAQ"},
                "blocks": {"q1": {"type": "item", "settings": {"title": "a", "content": "<p>b</p>"}}}, "block_order": ["q1"]},
    }, "order": ["overview", "references", "faq"]}


def keys(tt):
    return [k for k, _ in tt]


def test_add_section_extracts_every_translatable_setting():
    spec = {"add_sections": [{"id": "stats", "after": "overview", "section": {
        "type": "impact-text", "settings": {"background": "#F0F0F0"},
        "blocks": {"s1": {"type": "item", "settings": {"title": "−39%", "subheading": six("Deep-wrinkle area"),
                                                      "content": six("<p>2 months</p>")}}},
        "block_order": ["s1"]}}]}
    j = template()
    tt = hu.build(spec, j)
    assert j["order"] == ["overview", "stats", "references", "faq"]
    b = j["sections"]["stats"]["blocks"]["s1"]["settings"]
    assert b["subheading"] == "Deep-wrinkle area" and b["title"] == "−39%"
    assert set(keys(tt)) == {"stats.s1.subheading", "stats.s1.content"}


def test_add_section_is_idempotent_on_rerun():
    spec = {"add_sections": [{"id": "stats", "after": "overview", "section": {
        "type": "rich-text", "settings": {}, "blocks": {}, "block_order": []}}]}
    j = template()
    hu.build(copy.deepcopy(spec), j)
    hu.build(copy.deepcopy(spec), j)
    assert j["order"].count("stats") == 1


def test_section_level_set_uses_two_part_path():
    tt = hu.build({"set": [{"at": "faq/title", "values": six("Matrixyl 3000 FAQ")}]}, j := template())
    assert j["sections"]["faq"]["settings"]["title"] == "Matrixyl 3000 FAQ"
    assert keys(tt) == ["faq.title"]


def test_add_block_after_an_existing_block():
    spec = {"add_blocks": [{"section": "faq", "id": "q2", "after": "q1",
                            "block": {"type": "item", "settings": {"title": six("Is it safe?"), "content": six("<p>Yes.</p>")}}}]}
    tt = hu.build(spec, j := template())
    assert j["sections"]["faq"]["block_order"] == ["q1", "q2"]
    assert set(keys(tt)) == {"faq.q2.title", "faq.q2.content"}


def test_missing_locale_is_refused():
    bad = six("x")
    del bad["it"]
    with pytest.raises(SystemExit):
        hu.build({"set": [{"at": "faq/title", "values": bad}]}, template())


def test_references_rows_added_once_and_translated():
    spec = {"references_add": [{"title": "New paper", "meta": "Doe J et al., 2020", "url": "https://doi.org/10.1/x",
                                "link": "View study &rarr;"}],
            "references_i18n": {l: {"Published References": f"Refs-{l}", "View study &rarr;": f"Study-{l}",
                                    "View on PubMed &rarr;": f"PubMed-{l}"} for l in L6[1:]}}
    j = template()
    hu.build(copy.deepcopy(spec), j)
    tt = hu.build(copy.deepcopy(spec), j)          # second run must not duplicate the row
    h = j["sections"]["references"]["settings"]["html"]
    assert h.count("https://doi.org/10.1/x") == 1
    assert h.index("New paper") > h.index("Old")   # appended inside the list, after existing rows
    vals = dict(tt)["references.html"]
    assert "Refs-de" in vals["de"] and "Study-de" in vals["de"] and "PubMed-de" in vals["de"]
    assert "Published References" in vals["en"]


def test_jsonld_is_localised_per_locale():
    spec = {"jsonld": {"@type": "WebPage", "@id": "https://www.skingenetix.com/pages/x#webpage",
                       "url": "https://www.skingenetix.com/pages/x", "name": "EN name", "description": "EN d"},
            "jsonld_i18n": {l: {"name": f"name-{l}", "description": f"d-{l}"} for l in L6[1:]},
            "references_i18n": {l: {} for l in L6[1:]}}
    tt = hu.build(spec, template())
    de = dict(tt)["references.html"]["de"]
    ld = json.loads(de.split('id="sgx-webpage-jsonld">', 1)[1].split("</script>")[0])
    assert ld["name"] == "name-de" and ld["inLanguage"] == "de"
    assert ld["url"] == "https://www.skingenetix.com/de/pages/x"
    en = dict(tt)["references.html"]["en"]
    assert json.loads(en.split('id="sgx-webpage-jsonld">', 1)[1].split("</script>")[0])["inLanguage"] == "en"


def test_chart_placeholder_expands_to_six_locales():
    spec = {"charts": {"c1": {"kind": "bars", "title": six("Collagen I"), "caption": six("<p>Lab</p>"),
                              "unit": "%", "domain": [-20, 260], "series": [{"key": "a", "label": six("Change"), "color": "#016569"}],
                              "rows": [{"label": six("Both"), "values": {"a": 256}}]}},
            "add_sections": [{"id": "fig", "after": "overview", "section": {
                "type": "custom-html", "settings": {"html": {"$chart": ["c1"]}}}}]}
    tt = hu.build(spec, j := template())
    vals = dict(tt)["fig.html"]
    assert set(vals) == set(L6)
    assert "+256%" in vals["en"] and "[de] Collagen I" in vals["de"]
    for d in ("{{", "}}", "{%", "%}"):                        # custom-html rejects all four (422)
        assert all(d not in v for v in vals.values()), d


_c = importlib.util.spec_from_file_location("hc", ROOT / "scripts/hub_charts.py")
hc = importlib.util.module_from_spec(_c)
_c.loader.exec_module(hc)


def _chart(rows, **kw):
    base = {"title": six("T"), "caption": six("<p>c</p>"), "unit": "%", "domain": [-30, 5],
            "series": [{"key": "a", "label": six("A"), "color": "#016569"}], "rows": rows}
    base.update(kw)
    return base


def test_range_value_draws_a_band_and_labels_it_per_locale():
    c = _chart([{"label": six("Crow's feet area"), "values": {"a": [-20, -23]}}], table_head=six("Measure"))
    en, de = hc.render_chart(c, "en"), hc.render_chart(c, "de")
    assert "−20 to −23%" in en and "−20 bis −23" in de
    assert en.count('class="sgfig-bar') == 2          # solid part + lighter band
    assert "<td>−20 to −23%</td>" in en               # the table view carries the same label


def test_label_override_replaces_the_number():
    c = _chart([{"label": six("Copper peptide"), "values": {"a": 70},
                 "labels": {"a": {l: ("7 of 10" if l == "en" else f"7/10 [{l}]") for l in L6}}}], domain=[0, 100])
    assert "7 of 10" in hc.render_chart(c, "en") and "7/10 [it]" in hc.render_chart(c, "it")


def test_unsigned_ratio_with_prefix():
    c = _chart([{"label": six("Wrinkles"), "values": {"a": 2}}], unit="×", signed=False, domain=[0, 2.4],
               series=[{"key": "a", "label": six("PDRN"), "color": "#016569", "prefix": "≈"}])
    assert "≈2×" in hc.render_chart(c, "en") and "+2" not in hc.render_chart(c, "en")


# ---- 2026-09-24: the live checks were blind to classed headings and to #anchors ----

def test_heading_count_check_sees_headings_that_carry_a_class():
    # the science-page template's headings are <h2 class="evd__h">; a bare "<h2>" count saw none of them
    vals = {l: '<h2 class="evd__h">Title</h2><p>x</p>' for l in L6}
    vals["de"] = "<p>Titel</p><p>x</p>"
    with pytest.raises(SystemExit):
        hu.check_values("evidence.html", vals)


def test_wanted_headings_include_classed_h2s():
    texts = [{l: '<h2 class="ovw__ih">What Is Argireline?</h2><h2>At a glance</h2><h2x>no</h2x>' for l in L6}]
    assert hu.wanted_headings(texts, "en", "h2") == ["What Is Argireline?", "At a glance"]


def test_missing_anchors_reports_a_fragment_with_no_target():
    texts = [{l: '<a href="#rba-f1">one</a><a href="#evidence-sources">all</a><a href="/pages/x">x</a>' for l in L6}]
    page = '<div id="rba-f1"></div><div class="est"></div>'
    assert hu.missing_anchors(texts, "de", page) == ["#evidence-sources"]


def test_a_retired_spec_refuses_to_apply(tmp_path, monkeypatch):
    # re-applying a superseded spec silently reverted a whole layout pass once (2026-09-23)
    spec = tmp_path / "old.json"
    spec.write_text(json.dumps({"_retired": "superseded by x.json", "template": "templates/page.t.json", "page": "t"}))
    monkeypatch.setattr(hu, "read_file", lambda name: pytest.fail("must refuse before touching the store"))
    monkeypatch.setattr("sys.argv", ["hub-upgrade.py", str(spec), "--apply"])
    with pytest.raises(SystemExit) as e:
        hu.main()
    assert "retired" in str(e.value)


def test_fetch_falls_back_to_curl_when_cloudflare_throttles_python(monkeypatch):
    # 2026-09-24: Cloudflare answered every urllib request with 429 while curl got 200
    import subprocess
    import urllib.error

    def throttled(*a, **k):
        raise urllib.error.HTTPError("u", 429, "Too Many Requests", {}, None)
    monkeypatch.setattr(hu.urllib.request, "urlopen", throttled)
    monkeypatch.setattr(hu.time, "sleep", lambda s: None)
    calls = []

    def fake_run(cmd, **k):
        calls.append(cmd)
        return subprocess.CompletedProcess(cmd, 0, stdout=b"<html>ok</html>\n200", stderr=b"")
    monkeypatch.setattr(hu.subprocess, "run", fake_run)
    assert hu.fetch("https://www.skingenetix.com/pages/x") == "<html>ok</html>"
    assert calls and calls[0][0] == "curl"
    assert hu.status("https://www.skingenetix.com/pages/x") == 200


# ── section_css: a stock section's own Custom CSS (2026-09-26) ──────────────────────────────────────────────
# Shopify keeps it as a top-level `custom_css` list beside `settings` (memory custom-css-is-a-sibling-of-settings);
# written into settings it is silently ignored. Custom CSS is capped at 500 characters and refuses `content:`.

def test_section_css_is_written_beside_settings_not_inside():
    j = template()
    hu.build({"section_css": {"faq": ["h1 em{display:block;font-size:.42em}"]}}, j)
    assert j["sections"]["faq"]["custom_css"] == ["h1 em{display:block;font-size:.42em}"]
    assert "custom_css" not in j["sections"]["faq"]["settings"]


def test_section_css_refuses_what_shopify_refuses():
    for rules in (["a{color:red}" * 60], ["p::before{content:'x'}"]):
        with pytest.raises(SystemExit):
            hu.build({"section_css": {"faq": rules}}, template())


def test_section_css_allows_justify_content():
    """`justify-content:` contains the substring "content:" — the check refused a legal rule (2026-09-29)."""
    j = template()
    hu.build({"section_css": {"faq": [".rich-text {justify-content: center;}", ".a{align-content:start}"]}}, j)
    assert j["sections"]["faq"]["custom_css"][0] == ".rich-text {justify-content: center;}"


def test_section_css_refuses_two_statements_in_one_entry():
    """Shopify scopes only the first top-level statement of an entry: in "h1{…}@media(…){h1{…}}" the @media went out
    unscoped and silently lost to the section's own h1 rule (collagen preview, 2026-09-29)."""
    for entry in ("h1{overflow-wrap:break-word}@media (max-width:299px){h1{font-size:2.25rem}}", ".a{color:red}.b{color:blue}"):
        with pytest.raises(SystemExit):
            hu.build({"section_css": {"faq": [entry]}}, template())
    j = template()                                  # one @media holding several rules is one statement, and is scoped whole
    hu.build({"section_css": {"faq": ["@media (min-width:700px){.x{color:red}h1{font-size:4rem}}"]}}, j)
    assert j["sections"]["faq"]["custom_css"] == ["@media (min-width:700px){.x{color:red}h1{font-size:4rem}}"]


def test_add_section_with_no_after_goes_first_and_reruns_cleanly():
    """A generated spec must re-apply after its placeholder section is gone (clinical-studies, 2026-09-29)."""
    j = template()
    sec = {"type": "rich-text", "settings": {}}
    spec = {"add_sections": [{"id": "banner", "after": None, "section": sec}]}
    hu.build(spec, j)
    assert j["order"][0] == "banner"
    hu.build(spec, j)
    assert j["order"].count("banner") == 1 and j["order"][0] == "banner"


# ── a new template built from nothing, previewed through ?view= (collagen-skincare, 2026-09-29) ─────────────
# A copied template carries no translations (they are keyed to the template resource), so a new page is built
# from an empty template by one spec that owns every text on it, and is checked on /pages/<page>?view=<suffix>
# before any page uses it.

def test_a_missing_template_is_refused_unless_the_spec_creates_it():
    def missing(name):
        raise IndexError("no such file")
    with pytest.raises(SystemExit) as e:
        hu.load_template({"template": "templates/page.new.json"}, missing)
    assert "create" in str(e.value)
    raw, hdr, j = hu.load_template({"template": "templates/page.new.json", "create": True}, missing)
    assert raw is None and j == {"sections": {}, "order": []} and "Claude" in hdr


def test_create_never_replaces_a_template_that_exists():
    live = '{"sections": {"hero": {"type": "rich-text", "settings": {}}}, "order": ["hero"]}'
    raw, hdr, j = hu.load_template({"template": "templates/page.t.json", "create": True}, lambda name: live)
    assert raw == live and j["order"] == ["hero"]


def test_split_reads_a_created_template_back_after_shopify_prepends_its_own_header():
    """Shopify puts its "auto-generated" comment in front of ours, so a created template came back with two
    comments and the first re-apply failed with "Expecting value: line 1 column 1" (collagen-skincare, 2026-09-29)."""
    stored = ("/*\n * IMPORTANT: The contents of this file are auto-generated.\n */\n"
              "/* templates/page.collagen-skincare.json: built from spec.json by scripts/hub-upgrade.py */\n"
              '{"sections": {"hero": {"type": "rich-text"}}, "order": ["hero"]}')
    hdr, j = hu.split(stored)
    assert j["order"] == ["hero"]
    assert "auto-generated" in hdr and "built from spec.json" in hdr


def test_verify_url_uses_the_view_suffix_and_the_locale_prefix():
    spec = {"page": "collagen-skin-plumping", "view": "collagen-skincare"}
    assert hu.page_url(spec, "en").startswith(f"{hu.BASE}/pages/collagen-skin-plumping?view=collagen-skincare&hub=")
    assert hu.page_url(spec, "de").startswith(f"{hu.BASE}/de/pages/collagen-skin-plumping?view=collagen-skincare&hub=")
    assert hu.page_url({"page": "x"}, "fr").startswith(f"{hu.BASE}/fr/pages/x?hub=")


# ── english_first: finish the English on a hidden preview, translate afterwards (Malcolm, 2026-09-29) ──────────
# "only translate when the english version is fully completed and correct and optimized". The six-language rule
# exists because an untranslated setting on a LIVE template serves English in five locales; a template no page
# uses has no visitors, so an English-only draft is allowed there, and only there.

EN_FIRST = {"english_first": True, "template": "templates/page.collagen-skincare.json", "create": True,
            "page": "collagen-skin-plumping", "view": "collagen-skincare"}


def en(text):
    return {"en": text}


def test_english_first_builds_from_english_only_values():
    spec = dict(EN_FIRST, add_sections=[{"id": "answer", "after": None, "section": {
        "type": "rich-text", "settings": {},
        "blocks": {"p": {"type": "richtext", "settings": {"content": en("<h2>Do Collagen Creams Work?</h2><p>Yes.</p>")}}},
        "block_order": ["p"]}}])
    j = {"sections": {}, "order": []}
    tt = hu.build(spec, j)
    assert j["sections"]["answer"]["blocks"]["p"]["settings"]["content"].startswith("<h2>Do Collagen")
    assert keys(tt) == ["answer.p.content"]


def test_english_only_values_are_refused_without_the_flag():
    spec = {"set": [{"at": "faq/title", "values": en("FAQ")}]}
    with pytest.raises(SystemExit):
        hu.build(spec, template())


def test_english_first_still_checks_a_translation_that_is_present():
    bad = en('<p><a href="/pages/x">x</a></p>')
    bad["de"] = '<p><a href="/pages/x">x</a></p>'            # a German value that forgot its /de/ prefix
    with pytest.raises(SystemExit):
        hu.build(dict(EN_FIRST, set=[{"at": "faq/title", "values": bad}]), template())


def run_main(tmp_path, monkeypatch, spec, *flags):
    p = tmp_path / "spec.json"
    p.write_text(json.dumps(spec))
    monkeypatch.setattr("sys.argv", ["hub-upgrade.py", str(p), *flags])
    return hu.main()


def test_english_first_apply_needs_a_hidden_preview(tmp_path, monkeypatch):
    spec = {k: v for k, v in EN_FIRST.items() if k != "view"}
    monkeypatch.setattr(hu, "upload", lambda *a: pytest.fail("must refuse before writing"))
    with pytest.raises(SystemExit) as e:
        run_main(tmp_path, monkeypatch, spec, "--apply")
    assert "view" in str(e.value)


def test_english_first_apply_refuses_a_template_a_live_page_uses(tmp_path, monkeypatch):
    pages = {"pages": {"nodes": [{"handle": "collagen-skin-plumping", "templateSuffix": "collagen-skincare"}],
                       "pageInfo": {"hasNextPage": False, "endCursor": None}}}
    monkeypatch.setattr(hu, "gql", lambda q, v=None: pages)
    monkeypatch.setattr(hu, "upload", lambda *a: pytest.fail("must refuse before writing"))
    with pytest.raises(SystemExit) as e:
        run_main(tmp_path, monkeypatch, EN_FIRST, "--apply")
    assert "collagen-skin-plumping" in str(e.value)


def test_pages_using_matches_the_whole_suffix_across_pages_of_results():
    batches = iter([
        {"pages": {"nodes": [{"handle": "a", "templateSuffix": "collagen-skincare-old"}, {"handle": "b", "templateSuffix": None}],
                   "pageInfo": {"hasNextPage": True, "endCursor": "c1"}}},
        {"pages": {"nodes": [{"handle": "c", "templateSuffix": "collagen-skincare"}],
                   "pageInfo": {"hasNextPage": False, "endCursor": None}}},
    ])
    assert hu.pages_using("templates/page.collagen-skincare.json", lambda q, v=None: next(batches)) == ["c"]


def test_english_first_apply_uploads_and_registers_nothing(tmp_path, monkeypatch, capsys):
    no_pages = {"pages": {"nodes": [], "pageInfo": {"hasNextPage": False, "endCursor": None}}}
    monkeypatch.setattr(hu, "gql", lambda q, v=None: no_pages)

    def missing(name):
        raise IndexError("no such file")
    monkeypatch.setattr(hu, "read_file", missing)
    uploaded = []
    monkeypatch.setattr(hu, "upload", lambda name, hdr, j: uploaded.append((name, j)))
    monkeypatch.setattr(hu, "register", lambda *a: pytest.fail("an English-only draft registers no translations"))
    spec = dict(EN_FIRST, add_sections=[{"id": "answer", "after": None, "section": {
        "type": "rich-text", "settings": {}, "blocks": {"p": {"type": "richtext", "settings": {"content": en("<p>Yes.</p>")}}},
        "block_order": ["p"]}}])
    assert run_main(tmp_path, monkeypatch, spec, "--apply") == 0
    assert uploaded and uploaded[0][0] == "templates/page.collagen-skincare.json"
    assert "english-first" in capsys.readouterr().out.lower()


def test_english_first_refuses_a_spec_whose_texts_are_all_translated(tmp_path, monkeypatch):
    """Post-build review 2026-09-29: translating every value but forgetting to drop the flag would upload the
    translations and silently register none of them."""
    monkeypatch.setattr(hu, "read_file", lambda name: '{"sections": {}, "order": []}')
    monkeypatch.setattr(hu, "upload", lambda *a: pytest.fail("must refuse before writing"))
    spec = dict(EN_FIRST, add_sections=[{"id": "answer", "after": None, "section": {
        "type": "rich-text", "settings": {}, "blocks": {"p": {"type": "richtext", "settings": {"content": six("<p>Yes.</p>")}}},
        "block_order": ["p"]}}])
    with pytest.raises(SystemExit) as e:
        run_main(tmp_path, monkeypatch, spec)
    assert "english_first" in str(e.value)


def test_an_english_first_backup_is_marked_as_a_draft(tmp_path, monkeypatch):
    no_pages = {"pages": {"nodes": [], "pageInfo": {"hasNextPage": False, "endCursor": None}}}
    monkeypatch.setattr(hu, "gql", lambda q, v=None: no_pages)
    monkeypatch.setattr(hu, "ROOT", tmp_path)
    (tmp_path / "backups").mkdir()
    monkeypatch.setattr(hu, "read_file", lambda name: '{"sections": {}, "order": []}')
    monkeypatch.setattr(hu, "upload", lambda *a: None)
    run_main(tmp_path, monkeypatch, EN_FIRST, "--apply")
    names = [p.name for p in (tmp_path / "backups").iterdir()]
    assert len(names) == 1 and names[0].endswith("-english-draft.json")


def test_rollback_never_restores_an_english_draft_onto_a_template_a_page_uses(tmp_path, monkeypatch):
    """Post-build review 2026-09-29: --rollback skipped the english_first guard entirely."""
    monkeypatch.setattr(hu, "ROOT", tmp_path)
    (tmp_path / "backups").mkdir()
    (tmp_path / "backups" / "hub-upgrade-templates__page.collagen-skincare.json-20260929-171038-english-draft.json").write_text(
        '{"sections": {}, "order": []}')
    monkeypatch.setattr(hu, "pages_using", lambda template, query=None: ["collagen-skincare"])
    monkeypatch.setattr(hu, "upload", lambda *a: pytest.fail("must refuse before writing"))
    spec = {k: v for k, v in EN_FIRST.items() if k != "english_first"}      # the spec after translation
    with pytest.raises(SystemExit) as e:
        run_main(tmp_path, monkeypatch, spec, "--rollback")
    assert "english" in str(e.value).lower()


def test_verify_checks_the_json_ld_type_the_spec_declares(monkeypatch):
    page = ('<h1>Collagen Cream</h1><script type="application/ld+json">{"@type": "Article", "headline": "x"}</script>')
    monkeypatch.setattr(hu, "fetch", lambda url: page)
    monkeypatch.setattr(hu, "status", lambda url: 200)
    monkeypatch.setattr(hu.time, "sleep", lambda s: None)
    spec = dict(EN_FIRST, jsonld={"@type": "Article"}, add_sections=[{"id": "hero", "after": None, "section": {"settings": {
        "x": en("<h1>Collagen Cream</h1>")}}}])
    assert hu.verify(spec) == 0


def test_english_first_verify_reads_the_english_preview_only(monkeypatch):
    fetched = []
    page = '<h1>Collagen Cream</h1><h2>Do Collagen Creams Work?</h2>'
    monkeypatch.setattr(hu, "fetch", lambda url: fetched.append(url) or page)
    monkeypatch.setattr(hu, "status", lambda url: 200)
    monkeypatch.setattr(hu.time, "sleep", lambda s: None)
    spec = dict(EN_FIRST, add_sections=[{"id": "answer", "after": None, "section": {"settings": {
        "x": en("<h1>Collagen Cream</h1><h2>Do Collagen Creams Work?</h2><p><a href=\"/pages/firming-skin-density\">f</a></p>")}}}])
    assert hu.verify(spec) == 0
    assert len(fetched) == 1 and "/pages/collagen-skin-plumping?view=collagen-skincare" in fetched[0]
    assert "/de/" not in fetched[0]
