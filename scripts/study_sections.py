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
.sty{--ink:#1A1A1A;--mut:#5b6264;--line:#e3e5e6;--blue:#014EB1;--bone:#F0F0F0}
.sty,.sty__band,.sty__in{box-sizing:border-box;max-width:100%;}
/* NO viewport breakout here. Tried 2026-09-24: `.sty{overflow-x:clip}` plus
   `.sty__band{margin-inline:calc(50% - 50vw);width:100vw}` rendered the page BLANK on the live
   site. The theme gives .sty no width of its own, so it shrink-to-fits; with every child pulled
   out by -50vw its width computed to 0, and the clip context then cut the whole body away.
   Computed styles looked correct (margin -720px, width 1440px) — only the screenshot showed it.
   If full-bleed bands are wanted, the width has to come from the theme section, not from CSS
   inside the section. */
.sty__band--bone{background:var(--bone)}
.sty__band--white{background:#fff}
.sty__in{max-width:1080px;margin:0 auto;padding:0 24px;text-align:left}

/* Rhythm. Six bands at one padding value is a colour stripe, not pacing: the critic measured
   distinctSectionPaddings 2 against a floor of 3. Padding now carries the band's rank. */
.sty__band{padding:64px 0}
.sty__band--figs{padding:56px 0}
.sty__band--glance{padding:72px 0}
.sty__band--data{padding:72px 0}
.sty__band--story{padding:88px 0}
.sty__band--means{padding:80px 0}
.sty__band--ref{padding:40px 0}

/* The heading ladder. The theme sets H1 60px weight 300 and its own H2 rule beat `.sty h2`,
   so the bands rendered at 48px weight 600 — heavier than the H1 above them. These selectors
   are specific enough to win, and the weight matches the H1 so the H1 stays dominant. */
.sty .sty__band h2{font-family:Fraunces,Georgia,serif;font-weight:300;letter-spacing:-.015em;
 line-height:1.12;margin:0 0 20px;color:var(--ink);font-size:40px}
.sty .sty__band--glance h2,.sty .sty__band--data h2{font-size:36px}
.sty .sty__band--ref h2{font-size:26px;margin-bottom:12px}
.sty .sty__limits h2{font-size:54px;color:#fff;margin:0 0 28px}

.sty p{font-size:17px;line-height:1.65;color:#3b3f40;margin:0 0 16px}
.sty p:last-child{margin-bottom:0}
.sty a{color:var(--blue)}
.sty a:focus-visible{outline:3px solid var(--blue);outline-offset:3px;border-radius:2px}
/* 87 characters is a third over the comfortable band. Prose gets a measure; tables and the
   chart keep the full 1032px, because their job is comparison, not reading. */
.sty__prose{max-width:640px}
.sty__band--ref p{font-size:15px;color:var(--mut);max-width:560px}

.sty__figs{display:grid;grid-template-columns:repeat(3,1fr);gap:28px}
.sty__fig{border-top:3px solid var(--blue);padding-top:16px}
/* Fraunces, matching the hubs' key figures — a reader arriving from the hub met a generic
   sans stat strip where the hub uses large serif numerals. */
.sty__n{display:block;font-family:Fraunces,Georgia,serif;font-size:56px;line-height:1;
 font-weight:300;letter-spacing:-.02em;color:var(--blue);font-variant-numeric:tabular-nums}
.sty__lab{display:block;font-size:15px;font-weight:600;margin:10px 0 6px;color:var(--ink)}
.sty__sub{display:block;font-size:14px;line-height:1.55;color:var(--mut)}

.sty__glance{width:100%;border-collapse:collapse;font-size:16px;font-variant-numeric:tabular-nums}
.sty__glance th{text-align:left;width:31%;padding:14px 16px 14px 0;vertical-align:top;
 font-weight:600;color:var(--ink);border-bottom:1px solid var(--line)}
.sty__glance td{padding:14px 0;vertical-align:top;color:#3b3f40;border-bottom:1px solid var(--line)}
.sty__glance tr:last-child th,.sty__glance tr:last-child td{border-bottom:none}

/* The chart card is white; on a white band it is a box that changed nothing about its ground. */
.sty .sgfig-card{background:#FAFAFA;border-color:#DCDEDF}
/* The chart caption is the one piece of real prose inside the chart, and it ran at 109
   characters. The title, sub-label and legend are labels, not prose, so they keep the card. */
.sty .sgfig-caption p{max-width:580px}

.sty__media{display:grid;grid-template-columns:5fr 6fr;gap:64px;align-items:center}
.sty__media img{width:100%;height:auto;display:block;border-radius:12px}

/* Band 5 is the reason the page exists, and it shipped as the narrowest, least-padded, most
   boxed element on the page — the standard aside component. It is now the one dominant event:
   full-bleed on ink, the largest body text on the page, a heading no other band gets. */
.sty__limits{background:var(--ink);padding:104px 0}
.sty__limits .sty__in{max-width:800px}
.sty__limits ol{margin:0;padding-left:28px;counter-reset:lim;list-style:none}
.sty__limits li{counter-increment:lim;position:relative;font-size:20px;line-height:1.55;
 color:#D9DBDC;margin:0 0 26px;padding-left:16px}
.sty__limits li:last-child{margin-bottom:0}
.sty__limits li::before{content:counter(lim);position:absolute;left:-28px;top:2px;
 font-family:Fraunces,Georgia,serif;font-size:17px;color:#8E9698}
.sty__limits strong{color:#fff;font-weight:600}
.sty__limits em{color:#fff}

/* The theme paints an animated underline on every `a` using background-image + background-size,
   which collapsed the button fill to a 1px strip across the label and left the text blue on
   transparent — it rendered as struck-through text. Every longhand has to be overridden. */
.sty__cta{display:inline-block;font-size:16px;font-weight:600;line-height:1;padding:17px 30px;
 border-radius:999px;text-decoration:none;margin-top:8px;
 background-color:var(--blue) !important;background-image:none !important;
 background-size:auto !important;background-repeat:repeat !important;color:#fff !important;
 border:1px solid var(--blue)}
.sty__cta--ghost{background-color:transparent !important;color:var(--ink) !important;
 border:1px solid var(--mut);margin-left:12px}

/* ---- outside .sty, on purpose -------------------------------------------------------
   The H1, byline and answer paragraph live in the theme's own rich-text section, which sets
   them at 15px — the smallest text on the page, under a 60px H1, with nothing in between.
   The answer paragraph is the sentence an engine quotes and a sceptic reads first, so it
   cannot be the page's small print. This block ships inside sections_html, so it only ever
   loads on a study page. */
/* The theme caps the H1 at 60px. Against a 20px body — the limits list is deliberately the
   page's largest body text — that is a display-to-body ratio of 3.0 against a 4.4 floor, and at
   390 the old long H1 pushed the first figure below the fold. A short H1 can carry more size. */
/* !important because the theme's own h1 rule beat a plain `main h1` — the same way it beat
   `.sty h2`. Verified on the live page, not assumed. */
.shopify-section--rich-text .metafield-rich_text_field h1{text-wrap:balance;
 font-size:clamp(52px,6vw,88px) !important;line-height:1.03 !important;
 max-width:900px;margin-left:auto;margin-right:auto}
.shopify-section--rich-text .metafield-rich_text_field p{font-size:20px;line-height:1.58;
 color:#2f3334;max-width:620px;margin-left:auto;margin-right:auto}
.shopify-section--rich-text .metafield-rich_text_field p:has(>em:only-child){font-size:14px;
 line-height:1.5;color:#5b6264}

@media(max-width:899px){
.shopify-section--rich-text .metafield-rich_text_field p{font-size:17px}
.sty__band,.sty__band--figs,.sty__band--glance,.sty__band--data{padding:44px 0}
.sty__band--story{padding:56px 0}
.sty__band--means{padding:52px 0}
.sty__band--ref{padding:32px 0}
.sty__limits{padding:64px 0}
.sty .sty__band h2{font-size:30px}
.sty .sty__band--glance h2,.sty .sty__band--data h2{font-size:28px}
.sty .sty__limits h2{font-size:36px}
.sty .sty__band--ref h2{font-size:22px}
.sty__n{font-size:44px}
.sty__figs{grid-template-columns:1fr;gap:22px}
.sty__media{grid-template-columns:1fr;gap:26px}
.sty__limits li{font-size:18px}
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


_MD = __import__("re").compile(r"\*\*(.+?)\*\*|\*(.+?)\*|\[([^\]]+)\]\(([^)]+)\)")


def md(text, loc):
    """Inline markdown -> HTML, for values shared with the rich-text fields (the citation).

    Those fields are written in the same **bold** / *italic* / [label](url) markup that
    study-pages.py parses, so a value can be reused verbatim rather than kept twice.
    """
    def sub(m):
        if m.group(1):
            return f"<strong>{m.group(1)}</strong>"
        if m.group(2):
            return f"<em>{m.group(2)}</em>"
        url, ext = m.group(4), m.group(4).startswith("http")
        tgt = ' target="_blank" rel="noopener"' if ext else ""
        return f'<a href="{url if ext else _href(url, loc)}"{tgt}>{m.group(3)}</a>'
    return _MD.sub(sub, text)


def band(cls, inner, role=None):
    """One band. `cls` is the ground (white/bone); `role` carries its rank in the rhythm.

    The role class is what varies padding and heading size per band — six bands at one padding
    value read as a colour stripe rather than as pacing (design-critic, 2026-09-24).
    """
    r = f" sty__band--{role}" if role else ""
    return (f'<section class="sty__band sty__band--{cls}{r}">'
            f'<div class="sty__in">{inner}</div></section>')


def figures(cfg, loc):
    """Three proof points. Malcolm's rule: the numbers sit at the top, before the definition."""
    out = "".join(
        f'<div class="sty__fig"><span class="sty__n">{t(f["n"], loc)}</span>'
        f'<span class="sty__lab">{t(f["label"], loc)}</span>'
        f'<span class="sty__sub">{t(f["note"], loc)}</span></div>'
        for f in cfg["figures"])
    return band("white", f'<div class="sty__figs">{out}</div>', "figs")


def glance(cfg, loc):
    rows = "".join(f"<tr><th>{t(r['k'], loc)}</th><td>{t(r['v'], loc)}</td></tr>"
                   for r in cfg["glance"]["rows"])
    return band("bone", f"<h2>{t(cfg['glance']['heading'], loc)}</h2>"
                        f'<table class="sty__glance"><tbody>{rows}</tbody></table>', "glance")


def measurements(cfg, loc):
    m = cfg["measurements"]
    chart = hc.render_group({"$chart": ["c"]}, {"c": m["chart"]}, loc)
    intro = "".join(f"<p>{t(p, loc)}</p>" for p in m.get("intro", []))
    return band("white", f"<h2>{t(m['heading'], loc)}</h2>"
                         f'<div class="sty__prose">{intro}</div>{chart}', "data")


def media(cfg, loc):
    m = cfg["media"]
    body = "".join(f"<p>{t(p, loc)}</p>" for p in m["body"])
    # The phone was served the full 1200px asset for a 302px slot — 2.7x the bytes it needs.
    src = f"{CDN}{m['image']}"
    srcset = ", ".join(f"{src}?width={w} {w}w" for w in (400, 600, 800, 1200))
    img = (f'<div><img src="{src}?width=1200" srcset="{srcset}" '
           f'sizes="(max-width:899px) calc(100vw - 48px), 44vw" '
           f'width="1200" height="1200" alt="{t(m["alt"], loc)}" loading="lazy"></div>')
    txt = f"<div><h2>{t(m['heading'], loc)}</h2><div class=\"sty__prose\">{body}</div></div>"
    # image first reads as a caption to the prose; the config may flip it
    order = (txt + img) if m.get("image_right") else (img + txt)
    return band("bone", f'<div class="sty__media">{order}</div>', "story")


def limits(cfg, loc):
    """The band the page exists for — full-bleed, on ink, the largest body text on the page.

    It shipped as a tinted, rounded, inset box narrower and less padded than its neighbours:
    the standard aside component, i.e. the register of a footnote. If you hid the words you
    could not tell which band mattered (design-critic, 2026-09-24). It is now the one break
    in the rhythm, and the page's dominant screenful.
    """
    li = "".join(f"<li>{t(x, loc)}</li>" for x in cfg["limits"]["items"])
    return ('<section class="sty__band sty__limits"><div class="sty__in">'
            f'<h2>{t(cfg["limits"]["heading"], loc)}</h2><ol>{li}</ol></div></section>')


def meaning(cfg, loc):
    m = cfg["meaning"]
    body = "".join(f"<p>{t(p, loc)}</p>" for p in m["body"])
    ctas = "".join(
        f'<a class="sty__cta{" sty__cta--ghost" if i else ""}" href="{_href(c["href"], loc)}">'
        f'{t(c["label"], loc)}</a>'
        for i, c in enumerate(m["ctas"]))
    return band("white", f"<h2>{t(m['heading'], loc)}</h2>"
                          f'<div class="sty__prose">{body}</div><p>{ctas}</p>', "means")


def reference(cfg, loc):
    """The citation, in the designed body rather than the theme's own section.

    Two reasons: trafilatura drops the theme section, so the H2 that anchors our sourcing
    never reached an AI crawler; and an extra theme section painted a second white band
    straight after the bone one. Both found by scripts/page-audit.py on 2026-09-24.
    """
    r = cfg["reference_band"]
    body = "".join(f"<p>{md(t(p, loc), loc)}</p>" for p in r["body"])
    return band("bone", f"<h2>{t(r['heading'], loc)}</h2>{body}", "ref")


BANDS = [figures, glance, measurements, media, limits, meaning, reference]


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
