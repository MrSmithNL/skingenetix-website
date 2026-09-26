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
