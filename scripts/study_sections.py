"""The designed body of a study page, built from a config — one locale at a time.

Author: Claude (Opus 5) for Malcolm Smith · 2026-09-24
Used by: scripts/build-study-page.py
Template doc: docs/study-page-template.md

WHY THIS EXISTS
Study pages used to be four plain `rich-text` sections reading metaobject fields.
Shopify richtext strips class and style attributes, so nothing richer than paragraphs
and lists could live there: no key figures, no chart, no table, no image. The pages read
as documents rather than as designed pages, and a page that only summarises an abstract
is exactly what Google's raters call Lowest quality.

The lever was already in the template: `jsonld` is a multi_line_text_field emitted
unescaped by a `liquid` block. A second field of the same type — `sections_html` — carries
a fully designed body. This module renders it.

THE SIX BANDS, alternating white and bone, each painting its own background:
  1 figures      three numbers, the hubs' key-figures treatment
  2 glance       a real <table>: design, n, what was applied, comparators, duration,
                 measurement, concentration, funding, our grade
  3 measurements the chart from hub_charts, its <table>, and a caption carrying the link
  4 media        prose beside an image
  5 limits       "What this study does not show" — bordered, tinted, numbered
  6 meaning      what it means for our products, then a solid CTA and a ghost CTA

Band 5 is the reason the page exists. Any competitor can generate a summary; an appraisal
that states what the study cannot support is the part that earns the citation.

CONSTRAINTS
  * The CSS ships inside the value, so a page never depends on a theme style that may change.
  * Never emit "{{", "}}", "{%" or "%}" — all four 422 a custom-html upload, and the same
    text passes through hub_charts. CSS nests braces, so a rule closing a media query
    ("…;}}") must be spaced. render() checks the finished string and refuses.
  * Every localisable string is a {locale: text} dict; a bare string is used for all six.
"""
import importlib.util
import pathlib

_ROOT = pathlib.Path(__file__).resolve().parent.parent
_sp = importlib.util.spec_from_file_location("hub_charts", _ROOT / "scripts/hub_charts.py")
hc = importlib.util.module_from_spec(_sp)
_sp.loader.exec_module(hc)

LOCALES = ["en", "de", "nl", "fr", "es", "it"]

CSS = """
.sty{--ink:#1A1A1A;--mut:#5b6264;--line:#e3e5e6;--blue:#014EB1}
.sty__band{padding:64px 0}
.sty__band--bone{background:#F0F0F0}
.sty__band--white{background:#fff}
.sty__in{max-width:1080px;margin:0 auto;padding:0 24px;text-align:left}
.sty h2{font-size:32px;line-height:1.18;margin:0 0 18px;font-weight:600;letter-spacing:-.015em;color:var(--ink)}
.sty p{font-size:17px;line-height:1.65;color:#3b3f40;margin:0 0 16px}
.sty p:last-child{margin-bottom:0}
.sty a{color:var(--blue)}
.sty__figs{display:grid;grid-template-columns:repeat(3,1fr);gap:28px}
.sty__fig{border-top:3px solid var(--blue);padding-top:16px}
.sty__n{display:block;font-size:40px;line-height:1.05;font-weight:600;letter-spacing:-.02em;color:var(--blue)}
.sty__lab{display:block;font-size:15px;font-weight:600;margin:8px 0 6px;color:var(--ink)}
.sty__sub{display:block;font-size:14px;line-height:1.55;color:var(--mut)}
.sty__glance{width:100%;border-collapse:collapse;font-size:16px}
.sty__glance th{text-align:left;width:31%;padding:14px 16px 14px 0;vertical-align:top;
 font-weight:600;color:var(--ink);border-bottom:1px solid var(--line)}
.sty__glance td{padding:14px 0;vertical-align:top;color:#3b3f40;border-bottom:1px solid var(--line)}
.sty__glance tr:last-child th,.sty__glance tr:last-child td{border-bottom:none}
.sty__media{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:center}
.sty__media img{width:100%;height:auto;display:block;border-radius:12px}
.sty__warn{border:1px solid #d9c9a3;background:#FBF7EE;border-radius:14px;padding:32px 34px}
.sty__warn h2{margin-top:0}
.sty__warn ol{margin:0;padding-left:22px}
.sty__warn li{font-size:17px;line-height:1.62;color:#3b3f40;margin:0 0 14px}
.sty__warn li:last-child{margin-bottom:0}
.sty__warn strong{color:var(--ink)}
.sty__cta{display:inline-block;font-size:15px;font-weight:600;line-height:1;padding:16px 28px;
 border-radius:999px;text-decoration:none;background:var(--blue);color:#fff;margin-top:8px}
.sty__cta--ghost{background:transparent;color:var(--ink);border:1px solid #9aa3a4;margin-left:10px}
@media(max-width:899px){
.sty__band{padding:44px 0}
.sty h2{font-size:25px}
.sty__figs{grid-template-columns:1fr;gap:22px}
.sty__media{grid-template-columns:1fr;gap:26px}
.sty__warn{padding:24px 22px}
.sty__glance th{width:auto;display:block;padding-bottom:2px;border-bottom:none}
.sty__glance td{display:block;padding-top:0}
.sty__cta,.sty__cta--ghost{display:block;text-align:center;margin-left:0;margin-top:12px}
}
"""

CDN = "https://cdn.shopify.com/s/files/1/0932/8679/3601/files/"


def t(v, loc):
    """A localisable value: {"en": "...", "de": "..."} or a plain string for all six."""
    if isinstance(v, dict):
        if loc in v:
            return v[loc]
        if "en" not in v:
            raise KeyError(f"no {loc} and no en fallback in {list(v)}")
        return v["en"]
    return v


def _href(url, loc):
    """A site-internal link needs the locale prefix, or the reader lands back in English."""
    if loc != "en" and url.startswith("/") and not url.startswith(f"/{loc}/"):
        return f"/{loc}{url}"
    return url


def band(cls, inner):
    return f'<section class="sty__band sty__band--{cls}"><div class="sty__in">{inner}</div></section>'


def figures(cfg, loc):
    """Three proof points. Malcolm's rule: the numbers sit at the top, before the definition."""
    out = "".join(
        f'<div class="sty__fig"><span class="sty__n">{t(f["n"], loc)}</span>'
        f'<span class="sty__lab">{t(f["label"], loc)}</span>'
        f'<span class="sty__sub">{t(f["note"], loc)}</span></div>'
        for f in cfg["figures"])
    return band("white", f'<div class="sty__figs">{out}</div>')


def glance(cfg, loc):
    rows = "".join(f"<tr><th>{t(r['k'], loc)}</th><td>{t(r['v'], loc)}</td></tr>"
                   for r in cfg["glance"]["rows"])
    return band("bone", f"<h2>{t(cfg['glance']['heading'], loc)}</h2>"
                        f'<table class="sty__glance"><tbody>{rows}</tbody></table>')


def measurements(cfg, loc):
    m = cfg["measurements"]
    chart = hc.render_group({"$chart": ["c"]}, {"c": m["chart"]}, loc)
    intro = "".join(f"<p>{t(p, loc)}</p>" for p in m.get("intro", []))
    return band("white", f"<h2>{t(m['heading'], loc)}</h2>{intro}{chart}")


def media(cfg, loc):
    m = cfg["media"]
    body = "".join(f"<p>{t(p, loc)}</p>" for p in m["body"])
    img = (f'<div><img src="{CDN}{m["image"]}?width=1200" width="1200" height="1200" '
           f'alt="{t(m["alt"], loc)}" loading="lazy"></div>')
    txt = f"<div><h2>{t(m['heading'], loc)}</h2>{body}</div>"
    # image first reads as a caption to the prose; the config may flip it
    order = (txt + img) if m.get("image_right") else (img + txt)
    return band("bone", f'<div class="sty__media">{order}</div>')


def limits(cfg, loc):
    li = "".join(f"<li>{t(x, loc)}</li>" for x in cfg["limits"]["items"])
    return band("white", f'<div class="sty__warn"><h2>{t(cfg["limits"]["heading"], loc)}</h2>'
                         f"<ol>{li}</ol></div>")


def meaning(cfg, loc):
    m = cfg["meaning"]
    body = "".join(f"<p>{t(p, loc)}</p>" for p in m["body"])
    ctas = "".join(
        f'<a class="sty__cta{" sty__cta--ghost" if i else ""}" href="{_href(c["href"], loc)}">'
        f'{t(c["label"], loc)}</a>'
        for i, c in enumerate(m["ctas"]))
    return band("bone", f"<h2>{t(m['heading'], loc)}</h2>{body}<p>{ctas}</p>")


BANDS = [figures, glance, measurements, media, limits, meaning]


def render(cfg, loc):
    """The whole designed body for one locale."""
    html = (f"<style>{CSS}</style>\n<div class=\"sty\">\n"
            + "".join(b(cfg, loc) for b in BANDS) + "</div>")
    for bad in ("{{", "}}", "{%", "%}"):
        if bad in html:
            i = html.index(bad)
            raise ValueError(f"{loc}: Liquid delimiter {bad!r} at {i}: …{html[i-60:i+20]}…")
    return html


def report(cfg, loc, html):
    """What was actually built — printed so a wrong config is visible before it goes live."""
    return ("  %-3s %6d chars · bands %d · figures %d · glance rows %d · limitations %d · "
            "tables %d · images %d"
            % (loc, len(html), html.count('<section class="sty__band'), html.count('class="sty__fig"'),
               len(cfg["glance"]["rows"]), len(cfg["limits"]["items"]),
               html.count("<table"), html.count("<img")))
