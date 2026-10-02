"""Offline tests for scripts/build-study-page.py — reviewer schema and the citation-identity check.

Run:  python3 -m pytest tests/ -q

No network: the citation resolver is injected, so each test states exactly what PubMed or Crossref "returned".
"""
import copy
import importlib.util
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
_s = importlib.util.spec_from_file_location("bsp", ROOT / "scripts/build-study-page.py")
bsp = importlib.util.module_from_spec(_s)
_s.loader.exec_module(bsp)

BADENHORST = json.loads((ROOT / "configs/studies/copper-peptide-wrinkle-trial-badenhorst-2016.json").read_text())
PERSON = {"@type": "Person", "name": "Esther Bodde", "honorificPrefix": "Dr", "jobTitle": "Cosmetic & Medical Physician"}


# ---------------------------------------------------------------- reviewer

def test_jsonld_names_the_reviewer_the_config_names():
    cfg = copy.deepcopy(BADENHORST)
    cfg["reviewer"] = PERSON
    assert bsp.jsonld(cfg, "en")["reviewedBy"] == PERSON


def test_jsonld_has_no_reviewer_when_the_config_has_none():
    """set-reviewer.py --remove must be able to take the credit off: a hard-coded reviewedBy survived it."""
    cfg = copy.deepcopy(BADENHORST)
    cfg.pop("reviewer", None)
    assert "reviewedBy" not in bsp.jsonld(cfg, "en")


# ---------------------------------------------------------------- citation identity

def fake(records):
    """A resolver that answers from a dict keyed (kind, id) — None for anything else, like a failed lookup."""
    return lambda kind, ident: records.get((kind, ident))


PICKART = {"title": "GHK Peptide as a Natural Modulator of Multiple Cellular Pathways in Skin Regeneration",
           "surnames": ["pickart", "vasquez-soltero", "margolina"], "year": 2015}
DENTAL = {"title": "Prevalence and severity of temporomandibular disorders among university students in Riyadh",
          "surnames": ["alhammadi", "fayed", "labib"], "year": 2015}


def test_links_are_found_in_markdown_and_in_raw_html():
    cfg = {"a": {"en": "See ([Pickart et al., 2015](https://pubmed.ncbi.nlm.nih.gov/26236730/))."},
           "b": {"en": "<p>(<a href='https://doi.org/10.4172/2329-8847.1000166' target='_blank'>Badenhorst et al., 2016</a>)</p>"},
           "c": [{"en": "[Aruan 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10456789/)"}]}
    found = {(k, i, l) for l, k, i in bsp.citation_links(cfg)}
    assert ("pmid", "26236730", "Pickart et al., 2015") in found
    assert ("doi", "10.4172/2329-8847.1000166", "Badenhorst et al., 2016") in found
    assert ("pmc", "PMC10456789", "Aruan 2023") in found


def test_a_pmid_that_belongs_to_another_paper_is_refused():
    """The live defect of 2026-09-25: 'Pickart et al., 2015' linked to a dental paper."""
    cfg = {"x": {"en": "([Pickart et al., 2015](https://pubmed.ncbi.nlm.nih.gov/26236125/))"}}
    errs = bsp.check_citations(cfg, fake({("pmid", "26236125"): DENTAL}))
    assert len(errs) == 1 and "26236125" in errs[0] and "Pickart" in errs[0]


def test_a_pmid_whose_authors_and_year_match_passes():
    cfg = {"x": {"en": "([Pickart et al., 2015](https://pubmed.ncbi.nlm.nih.gov/26236730/))"}}
    assert bsp.check_citations(cfg, fake({("pmid", "26236730"): PICKART})) == []


def test_a_year_one_off_passes_but_a_wrong_year_does_not():
    """Epub and issue years differ by one all the time; three years apart is a different paper."""
    cfg = {"x": {"en": "([Pickart et al., 2016](https://pubmed.ncbi.nlm.nih.gov/26236730/))"}}
    assert bsp.check_citations(cfg, fake({("pmid", "26236730"): PICKART})) == []
    cfg = {"x": {"en": "([Pickart et al., 2018](https://pubmed.ncbi.nlm.nih.gov/26236730/))"}}
    assert len(bsp.check_citations(cfg, fake({("pmid", "26236730"): PICKART}))) == 1


def test_an_identifier_that_does_not_resolve_is_refused():
    cfg = {"x": {"en": "([Pickart et al., 2015](https://pubmed.ncbi.nlm.nih.gov/99999999/))"}}
    errs = bsp.check_citations(cfg, fake({}))
    assert len(errs) == 1 and "did not resolve" in errs[0]


def test_a_label_with_no_author_is_only_required_to_resolve():
    """'doi:10.4172/…' names no author, so there is nothing to compare — but the DOI must still exist."""
    cfg = {"x": {"en": "[doi:10.4172/2329-8847.1000166](https://doi.org/10.4172/2329-8847.1000166)"}}
    rec = {"title": "t", "surnames": ["badenhorst"], "year": 2016}
    assert bsp.check_citations(cfg, fake({("doi", "10.4172/2329-8847.1000166"): rec})) == []


def test_accented_surnames_match():
    cfg = {"x": {"en": "([Müller et al., 2020](https://pubmed.ncbi.nlm.nih.gov/1/))"}}
    assert bsp.check_citations(cfg, fake({("pmid", "1"): {"title": "t", "surnames": ["muller"], "year": 2020}})) == []


def test_the_scholarly_title_must_be_the_title_of_its_identifier():
    """The JSON-LD isBasedOn is what an AI system uses to tie our page to the paper."""
    cfg = {"scholarly": {"name": "Effects of GHK-Cu on MMP and TIMP Expression, Collagen and Elastin Production, "
                                 "and Facial Wrinkle Parameters",
                         "identifier": "10.4172/2329-8847.1000166"}}
    same = {"title": "Effects of GHK-Cu on MMP and TIMP expression, collagen and elastin production, and facial "
                     "wrinkle parameters.", "surnames": ["badenhorst"], "year": 2016}
    assert bsp.check_citations(cfg, fake({("doi", "10.4172/2329-8847.1000166"): same})) == []
    other = dict(same, title="Something else entirely")
    errs = bsp.check_citations(cfg, fake({("doi", "10.4172/2329-8847.1000166"): other}))
    assert len(errs) == 1 and "title" in errs[0]


def test_a_numeric_scholarly_identifier_is_read_as_a_pmid():
    cfg = {"scholarly": {"name": "GHK Peptide as a Natural Modulator of Multiple Cellular Pathways in Skin Regeneration",
                         "identifier": "PMID:26236730"}}
    assert bsp.check_citations(cfg, fake({("pmid", "26236730"): PICKART})) == []


# ---------------------------------------------------------------- links

def test_links_to_our_own_site_open_in_the_same_tab():
    """Full https://www.skingenetix.com/… URLs were given target=_blank like a PubMed link (2026-09-26)."""
    out = bsp.md_html("[hub](https://www.skingenetix.com/pages/acetyl-hexapeptide-8-research) and "
                      "[paper](https://doi.org/10.1111/jocd.12314)")
    assert '<a href="https://www.skingenetix.com/pages/acetyl-hexapeptide-8-research">hub</a>' in out
    assert '<a href="https://doi.org/10.1111/jocd.12314" target=_blank rel=noopener>paper</a>' in out


# ---------------------------------------------------------------- the Clinical studies blog (2026-09-29)

def test_the_page_lives_in_the_clinical_studies_blog():
    ld = bsp.jsonld(BADENHORST, "de")
    assert ld["url"] == "https://www.skingenetix.com/de/blogs/clinical-studies/copper-peptide-wrinkle-trial-badenhorst-2016"
    crumbs = [i["name"] for i in ld["breadcrumb"]["itemListElement"]]
    assert crumbs == ["Skingenetix", "Wissenschaft", "Klinische Studien", BADENHORST["h1"].get("de", BADENHORST["h1"]["en"])]


def test_the_banner_carries_a_translated_breadcrumb_to_the_hub():
    hero = bsp.fields(BADENHORST, "en")["hero_text"]
    assert hero.startswith('<p class="sg-crumb"><a href="/pages/the-science">Science</a> › '
                           '<a href="/blogs/clinical-studies">Clinical studies</a> › '
                           '<a href="/pages/copper-peptide-research">Copper peptide (GHK-Cu)</a></p><h1>')
    # Badenhorst has no German yet, so check the translated crumb itself
    assert bsp.crumb_parts(BADENHORST, "de") == [("Wissenschaft", "/de/pages/the-science"),
                                                 ("Klinische Studien", "/de/blogs/clinical-studies"),
                                                 ("Kupferpeptid (GHK-Cu)", "/de/pages/copper-peptide-research")]


# ---------------------------------------------------------------- English-first preview of a live article (2026-09-30)

def _recorder(calls):
    def gql(q, v=None):
        calls.append((q, v or {}))
        if "metaobjectByHandle" in q:
            return {"metaobjectByHandle": None}
        if "metaobjectCreate" in q:
            return {"metaobjectCreate": {"metaobject": {"id": "gid://shopify/Metaobject/9"}, "userErrors": []}}
        raise AssertionError(f"unexpected call: {q[:60]}")
    return gql


def test_a_preview_writes_only_the_draft_entry_and_registers_no_translation(monkeypatch):
    calls = []
    monkeypatch.setattr(bsp, "gql", _recorder(calls))
    monkeypatch.setattr(bsp, "media_gid", lambda stem: "gid://shopify/MediaImage/1")
    cfg = copy.deepcopy(BADENHORST)
    bsp.apply(cfg, "ACTIVE", entry_handle=bsp.draft_handle(cfg), english_only=True)
    handles = [v["h"]["handle"] for q, v in calls if "h" in v] + [v["m"]["handle"] for q, v in calls if "handle" in v.get("m", {})]
    assert handles and set(handles) == {cfg["handle"] + "-draft"}
    assert not any("translationsRegister" in q for q, _ in calls)


def test_the_preview_is_checked_through_the_draft_template():
    url = bsp.page_url(BADENHORST, "de", view="clinical-study-draft")
    assert url.startswith("https://www.skingenetix.com/de/blogs/clinical-studies/copper-peptide-wrinkle-trial-badenhorst-2016")
    assert "view=clinical-study-draft" in url
    assert "view=" not in bsp.page_url(BADENHORST, "en")


# ---------------------------------------------------------------- preview of a NEW study, before any live article (2026-09-30)
# A new study has no live article to borrow a ?view= from, so its English draft sits in a hidden, unlinked blog on the
# real study template, with its own title and description, so the audit judges the page it will become.

NEW = {**copy.deepcopy(BADENHORST), "handle": "pdrn-microneedling-split-face-trial-yogya-2022"}


def _blog_recorder(calls, articles=(), blog=True):
    def gql(q, v=None):
        calls.append((q, v or {}))
        if "blogs(" in q:
            return {"blogs": {"nodes": [{"id": "gid://shopify/Blog/7", "handle": bsp.DRAFTS_BLOG}] if blog else []}}
        if "blogCreate" in q:
            return {"blogCreate": {"blog": {"id": "gid://shopify/Blog/7"}, "userErrors": []}}
        if "metafieldsSet" in q:
            return {"metafieldsSet": {"userErrors": []}}
        if "metaobjectByHandle" in q:
            return {"metaobjectByHandle": {"id": "gid://shopify/Metaobject/9"}}
        if "articles(" in q:
            return {"articles": {"nodes": list(articles)}}
        if "articleCreate" in q:
            return {"articleCreate": {"article": {"id": "gid://shopify/Article/1"}, "userErrors": []}}
        if "articleUpdate" in q:
            return {"articleUpdate": {"article": {"id": "gid://shopify/Article/1"}, "userErrors": []}}
        raise AssertionError(f"unexpected call: {q[:60]}")
    return gql


def test_a_new_study_preview_is_read_from_the_drafts_blog():
    url = bsp.page_url(NEW, "en", blog=bsp.DRAFTS_BLOG)
    assert url.startswith(f"https://www.skingenetix.com/blogs/{bsp.DRAFTS_BLOG}/{NEW['handle']}?")
    assert "view=" not in url
    assert bsp.DRAFTS_BLOG != "clinical-studies"


def test_the_new_study_preview_article_is_hidden_and_on_the_study_template(monkeypatch):
    calls = []
    monkeypatch.setattr(bsp, "gql", _blog_recorder(calls))
    bsp.preview_article(NEW)
    a = next(v["a"] for q, v in calls if "articleCreate" in q)
    assert a["blogId"] == "gid://shopify/Blog/7" and a["handle"] == NEW["handle"]
    assert a["templateSuffix"] == "clinical-study" and a["isPublished"] is True
    assert a["title"] == NEW["h1"]["en"] and a["summary"] == NEW["seo_description"]["en"]
    mf = {(m["namespace"], m["key"]): m["value"] for m in a["metafields"]}
    assert mf[("seo", "hidden")] == "1"                                   # noindex, out of the sitemap
    assert mf[("study", "entry")] == "gid://shopify/Metaobject/9"
    assert mf[("global", "title_tag")] == NEW["seo_title"]["en"]
    assert not any("translationsRegister" in q for q, _ in calls)          # English first


def test_the_new_study_preview_updates_its_own_draft_article(monkeypatch):
    calls = []
    mine = {"id": "gid://shopify/Article/1", "handle": NEW["handle"], "blog": {"handle": bsp.DRAFTS_BLOG}}
    monkeypatch.setattr(bsp, "gql", _blog_recorder(calls, articles=[mine]))
    bsp.preview_article(NEW)
    assert any("articleUpdate" in q for q, _ in calls) and not any("articleCreate" in q for q, _ in calls)


def test_the_new_study_preview_refuses_a_study_that_is_already_live(monkeypatch):
    """A live article gets the draft-entry route; writing its handle into the drafts blog would fork it."""
    calls = []
    live = {"id": "gid://shopify/Article/2", "handle": NEW["handle"], "blog": {"handle": "clinical-studies"}}
    monkeypatch.setattr(bsp, "gql", _blog_recorder(calls, articles=[live]))
    try:
        bsp.preview_article(NEW)
    except SystemExit:
        pass
    else:
        raise AssertionError("expected a refusal")
    assert not any("articleCreate" in q or "articleUpdate" in q for q, _ in calls)


def test_the_drafts_blog_is_created_once_and_hidden(monkeypatch):
    calls = []
    monkeypatch.setattr(bsp, "gql", _blog_recorder(calls, blog=False))
    bsp.preview_article(NEW)
    b = next(v["b"] for q, v in calls if "blogCreate" in q)
    assert b["handle"] == bsp.DRAFTS_BLOG and b["commentPolicy"] == "CLOSED"
    hid = [m for q, v in calls if "metafieldsSet" in q for m in v["m"]]
    assert hid == [{"ownerId": "gid://shopify/Blog/7", "namespace": "seo", "key": "hidden",
                    "type": "number_integer", "value": "1"}]            # the blog's own index page is noindexed too


# ---------------------------------------------------------------- one section per result, and "how it works" (2026-10-01)
# Malcolm: separate content sections for each proven trial outcome, with a before/after picture where one can be used,
# and separate blocks for the proven effects that explain how the active works. They live in a companion
# `study_detail` entry (the study entry is full, 40 of 40 fields) linked from the article as study.detail.

OUT = {"heading": {"en": "What the trial found, result by result"},
       "items": [{"title": {"en": "Wrinkle volume fell 55.8% more than with the plain serum"},
                  "image": "skingenetix-copper-peptide-ghk-cu-crows-feet-wrinkles-before-after.jpg",
                  "before_after": True, "after": {"en": "After 8 weeks", "de": "Nach 8 Wochen"},
                  "result": {"en": "Wrinkle volume −24.1% vs −15.0% with the plain serum"},
                  "body": [{"en": "First paragraph."}, {"en": "Second paragraph."}]},
                 {"title": {"en": "Wrinkle depth fell further too"},
                  "image": "skingenetix-copper-peptide-ghk-cu-wrinkle-depth-scan-study.jpg",
                  "body": [{"en": "Depth paragraph."}]}]}
MECH = {"heading": {"en": "How GHK-Cu works on skin"},
        "items": [{"title": {"en": "More collagen from skin cells"}, "evidence": "laboratory",
                   "image": "skingenetix-copper-peptide-ghk-cu-fibroblast-culture-study.jpg",
                   "body": [{"en": "In the laboratory, skin cells grown with GHK-Cu made more collagen."}]}]}


def with_detail(**changes):
    cfg = copy.deepcopy(BADENHORST)
    cfg["outcomes"], cfg["mechanisms"] = copy.deepcopy(OUT), copy.deepcopy(MECH)
    cfg.update(changes)
    return cfg


# a study config without the two keys (every live article until 2026-10-02 had neither)
PLAIN = {k: v for k, v in BADENHORST.items() if k not in ("outcomes", "mechanisms")}


def test_a_config_without_the_new_keys_builds_exactly_as_before():
    """A config with neither key must write no companion entry and pass every check."""
    assert bsp.detail_fields(PLAIN, "en") is None
    assert bsp.check_detail(PLAIN) == []


def test_used_slots_are_filled_and_unused_slots_are_cleared():
    f = bsp.detail_fields(with_detail(), "en")
    assert f["outcomes_heading"] == "What the trial found, result by result"
    assert f["o1_title"] == "Wrinkle volume fell 55.8% more than with the plain serum"
    assert (f["o1_before"], f["o1_after"]) == ("Before", "After 8 weeks")
    assert f["o1_result"] == "Wrinkle volume −24.1% vs −15.0% with the plain serum"
    assert f["o1_body"] == "First paragraph.</p><p>Second paragraph."      # the template supplies the outer <p>
    assert f["o2_before"] == f["o2_after"] == f["o2_result"] == ""      # a plain photograph carries no labels
    assert f["m1_title"] == "More collagen from skin cells" and f["mechanism_heading"] == "How GHK-Cu works on skin"
    # a slot a study no longer uses is written empty, so an old result cannot linger on the page
    assert f["o3_title"] == f["o4_body"] == f["m2_title"] == f["m3_body"] == ""
    assert set(f) == {k for k, kind in bsp.DETAIL_FIELDS if kind != "file_reference"}


def test_the_before_label_uses_the_science_pages_words():
    assert bsp.detail_fields(with_detail(), "de")["o1_before"] == "Vorher"
    assert bsp.detail_fields(with_detail(), "de")["o1_after"] == "Nach 8 Wochen"
    assert [bsp.BEFORE[l] for l in bsp.LOCALES] == ["Before", "Vorher", "Voor", "Avant", "Antes", "Prima"]


def test_the_images_of_each_slot_are_listed_and_unused_ones_cleared():
    imgs = dict(bsp.detail_images(with_detail()))
    assert imgs["o1_image"] == "skingenetix-copper-peptide-ghk-cu-crows-feet-wrinkles-before-after"
    assert imgs["m1_image"] == "skingenetix-copper-peptide-ghk-cu-fibroblast-culture-study"
    assert imgs["o3_image"] is None and imgs["m3_image"] is None


def _problems(cfg):
    return " | ".join(bsp.check_detail(cfg))


def test_at_most_four_results_and_three_mechanisms():
    cfg = with_detail()
    cfg["outcomes"]["items"] *= 3
    cfg["mechanisms"]["items"] *= 4
    p = _problems(cfg)
    assert "6 results" in p and "4 mechanisms" in p


def test_a_before_after_needs_its_after_and_result_labels():
    cfg = with_detail()
    del cfg["outcomes"]["items"][0]["result"]
    assert "o1" in _problems(cfg) and "result" in _problems(cfg)


def test_labels_on_a_plain_photograph_are_refused():
    """A Before/After pill on a single photograph would claim a before/after the picture does not show."""
    cfg = with_detail()
    cfg["outcomes"]["items"][1]["after"] = {"en": "After 8 weeks"}
    assert "o2" in _problems(cfg) and "before_after" in _problems(cfg)


def test_every_image_names_the_ingredient():
    """Malcolm, 2026-09-24: every content image on an ingredient's page carries that ingredient in its filename."""
    cfg = with_detail()
    cfg["mechanisms"]["items"][0]["image"] = "skingenetix-acetyl-hexapeptide-8-skin-cell-microscopy-research.jpg"
    assert "m1" in _problems(cfg) and "ingredient" in _problems(cfg)


def test_no_image_is_used_twice_on_one_page():
    cfg = with_detail()
    cfg["outcomes"]["items"][1]["image"] = cfg["media"]["image"]
    assert "twice" in _problems(cfg)


def test_a_laboratory_mechanism_must_say_it_is_one():
    """Register rule: mechanism detail is framed as laboratory findings, never as what happens in the reader's skin."""
    cfg = with_detail()
    cfg["mechanisms"]["items"][0]["body"] = [{"en": "GHK-Cu makes your skin produce more collagen."}]
    assert "m1" in _problems(cfg) and "laborator" in _problems(cfg)
    cfg["mechanisms"]["items"][0]["evidence"] = "anecdote"
    assert "evidence" in _problems(cfg)


def test_a_result_label_must_fit_on_the_picture():
    cfg = with_detail()
    cfg["outcomes"]["items"][0]["result"]["de"] = "x" * 70
    assert "o1" in _problems(cfg) and "de" in _problems(cfg)


def test_a_section_with_blocks_needs_its_heading():
    cfg = with_detail()
    del cfg["mechanisms"]["heading"]
    assert "heading" in _problems(cfg)


def test_the_results_count_towards_the_verified_figures():
    """The `checks` probes look at everything published, so a figure may live in a result block alone."""
    cfg = with_detail(checks=["−24.1% vs −15.0% with the plain serum"])
    assert not [e for e in bsp.check(cfg) if "verified figures" in e]


def _detail_recorder(calls, exists=False):
    def gql(q, v=None):
        calls.append((q, v or {}))
        if "metaobjectDefinitionByType" in q:
            return {"metaobjectDefinitionByType": {"id": "gid://shopify/MetaobjectDefinition/5", "fieldDefinitions":
                    [{"key": k} for k, _ in bsp.DETAIL_FIELDS]}}
        if "metafieldDefinitions(" in q:          # both article links already defined
            return {"metafieldDefinitions": {"nodes": [{"key": "entry"}, {"key": "detail"}, {"key": "draft_detail"}]}}
        if "metaobjectByHandle" in q:
            return {"metaobjectByHandle": {"id": "gid://shopify/Metaobject/77"} if exists else None}
        if "metaobjectCreate" in q:
            return {"metaobjectCreate": {"metaobject": {"id": "gid://shopify/Metaobject/77"}, "userErrors": []}}
        if "metaobjectUpdate" in q:
            return {"metaobjectUpdate": {"metaobject": {"id": "gid://shopify/Metaobject/77"}, "userErrors": []}}
        raise AssertionError(f"unexpected call: {q[:60]}")
    return gql


def test_the_companion_entry_is_written_under_the_study_handle(monkeypatch):
    calls = []
    monkeypatch.setattr(bsp, "gql", _detail_recorder(calls))
    monkeypatch.setattr(bsp, "media_gid", lambda stem: "gid://shopify/MediaImage/" + stem[-6:])
    rid = bsp.apply_detail(with_detail(), entry_handle=None, english_only=True)
    assert rid == "gid://shopify/Metaobject/77"
    m = next(v["m"] for q, v in calls if "metaobjectCreate" in q)
    assert m["type"] == "study_detail" and m["handle"] == BADENHORST["handle"]
    vals = {f["key"]: f["value"] for f in m["fields"]}
    assert vals["o1_title"].startswith("Wrinkle volume") and vals["o1_image"].startswith("gid://shopify/MediaImage/")
    assert "o3_image" not in vals                     # an empty file reference is not sent on create
    assert not any("translationsRegister" in q for q, _ in calls)


def test_an_update_clears_the_images_of_slots_no_longer_used(monkeypatch):
    calls = []
    monkeypatch.setattr(bsp, "gql", _detail_recorder(calls, exists=True))
    monkeypatch.setattr(bsp, "media_gid", lambda stem: "gid://shopify/MediaImage/1")
    bsp.apply_detail(with_detail(), entry_handle="x-draft", english_only=True)
    m = next(v["m"] for q, v in calls if "metaobjectUpdate" in q)
    vals = {f["key"]: f["value"] for f in m["fields"]}
    assert vals["o3_image"] == "" and vals["m3_image"] == ""


def test_no_companion_entry_for_a_config_without_the_new_keys(monkeypatch):
    calls = []
    monkeypatch.setattr(bsp, "gql", _detail_recorder(calls))
    assert bsp.apply_detail(PLAIN, entry_handle=None, english_only=True) is None
    assert calls == []


def test_the_new_study_preview_links_its_companion_entry(monkeypatch):
    calls = []
    monkeypatch.setattr(bsp, "gql", _blog_recorder(calls))
    bsp.preview_article({**NEW, "outcomes": OUT}, detail_id="gid://shopify/Metaobject/77")
    a = next(v["a"] for q, v in calls if "articleCreate" in q)
    mf = {(m["namespace"], m["key"]): m["value"] for m in a["metafields"]}
    assert mf[("study", "detail")] == "gid://shopify/Metaobject/77"


def test_a_preview_without_a_companion_entry_sets_no_detail_link(monkeypatch):
    calls = []
    monkeypatch.setattr(bsp, "gql", _blog_recorder(calls))
    bsp.preview_article(NEW)
    a = next(v["a"] for q, v in calls if "articleCreate" in q)
    assert ("study", "detail") not in {(m["namespace"], m["key"]) for m in a["metafields"]}


def test_the_detail_link_key_follows_the_route():
    assert bsp.detail_link_key(draft=False) == "detail"
    assert bsp.detail_link_key(draft=True) == "draft_detail"


def test_a_full_publish_refuses_a_block_missing_one_of_the_studys_languages():
    """t() falls back to English, so an English-only result on a six-language study would be registered as the German,
    Dutch, French, Spanish and Italian translation. The English-first preview is the one place English alone is right."""
    cfg = with_detail()
    cfg["h1"] = {**cfg["h1"], "de": "Kann ein Kupferpeptid-Serum Falten mindern?"}    # the study is now in German too
    full = " | ".join(bsp.check_detail(cfg))
    assert "o1" in full and "de" in full and "title" in full
    assert bsp.check_detail(cfg, english_only=True) == []


def test_study_i18n_extracts_the_new_blocks_for_translation():
    s = importlib.util.spec_from_file_location("si18n", ROOT / "scripts/study-i18n.py")
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    strings = json.dumps(m.strings(with_detail()), ensure_ascii=False)
    assert "Wrinkle volume fell 55.8% more than with the plain serum" in strings
    assert "In the laboratory, skin cells grown with GHK-Cu made more collagen." in strings
    assert "After 8 weeks" in strings


# ---------------------------------------------------------------- the study's own authors are credited (Malcolm, 2026-10-02)
# The researchers are credited as the authors of the study, visibly and in the schema. Our appraisal keeps its own
# author: naming the researchers as authors of a page that links our products would claim an endorsement they never gave.

AUTHORED = {**copy.deepcopy(BADENHORST), "scholarly": {**BADENHORST["scholarly"],
            "authors": ["Badenhorst T", "Svirskis D", "Merrilees M", "Bolke L", "Wu Z"]}}


def test_the_study_authors_are_people_on_the_scholarly_article():
    ld = bsp.jsonld(AUTHORED, "en")
    want = [{"@type": "Person", "name": n} for n in AUTHORED["scholarly"]["authors"]]
    assert ld["citation"][0]["author"] == want
    assert ld["mainEntity"]["isBasedOn"]["author"] == want
    assert ld["author"]["name"] not in AUTHORED["scholarly"]["authors"]          # our page is not theirs


def test_the_intro_opens_with_the_research_credit_in_every_locale():
    en = bsp.fields(AUTHORED, "en")["intro"]
    assert en.startswith("<p>Original research by Badenhorst T, Svirskis D, Merrilees M, Bolke L and Wu Z, published in "
                         "<em>Journal of Aging Science</em> (2016).</p><p><em>")
    for loc in ("de", "nl", "fr", "es", "it"):
        credit = bsp.research_credit(AUTHORED, loc)
        assert "Badenhorst T" in credit and "Wu Z" in credit and "<em>Journal of Aging Science</em>" in credit
        assert " and " not in credit                                               # the joining word is translated


def test_a_study_without_its_authors_is_refused():
    cfg = copy.deepcopy(BADENHORST)
    cfg["scholarly"].pop("authors", None)
    assert any("authors" in e for e in bsp.check(cfg))


def test_the_credited_authors_must_be_the_records_authors():
    rec = {"title": AUTHORED["scholarly"]["name"], "year": 2016,
           "surnames": ["Badenhorst", "Svirskis", "Merrilees", "Bolke", "Wu"]}
    resolve = lambda kind, ident: rec
    assert not [e for e in bsp.check_citations(AUTHORED, resolve) if e.startswith("scholarly.authors")]
    wrong = {**rec, "surnames": ["Badenhorst", "Svirskis", "Merrilees", "Wu"]}
    assert any(e.startswith("scholarly.authors") for e in bsp.check_citations(AUTHORED, lambda k, i: wrong))


def test_a_truncated_record_passes_only_when_the_full_list_was_read_at_source():
    """Crossref holds 3 of Badenhorst 2016's 5 authors; the paper's own first page names all five (read 2026-10-02)."""
    short = {"title": AUTHORED["scholarly"]["name"], "year": 2016, "surnames": ["Badenhorst", "Svirskis", "Merrilees"]}
    bare = {**AUTHORED, "scholarly": {k: v for k, v in AUTHORED["scholarly"].items() if k != "authors_read_at_source"}}
    assert any(e.startswith("scholarly.authors") for e in bsp.check_citations(bare, lambda k, i: short))
    noted = {**AUTHORED, "scholarly": {**AUTHORED["scholarly"], "authors_read_at_source": "the paper's first page"}}
    assert not [e for e in bsp.check_citations(noted, lambda k, i: short) if e.startswith("scholarly.authors")]
    other = {**short, "surnames": ["Pickart", "Margolina", "Badenhorst"]}
    assert any(e.startswith("scholarly.authors") for e in bsp.check_citations(noted, lambda k, i: other))
