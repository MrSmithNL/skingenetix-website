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
