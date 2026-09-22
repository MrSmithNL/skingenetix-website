"""Bar charts for the research hubs, as plain HTML + CSS — one per locale.

Author: Claude (Opus 5) for Malcolm Smith · 2026-09-22
Used by: scripts/hub-upgrade.py, which expands {"$chart": [...]} in a spec into six
localised custom-html values.

Why HTML and not SVG or a PNG:
  * An SVG scales its text with the drawing, so 13px labels become ~7px on a phone;
    HTML labels stay 14px at every width.
  * A PNG cannot be translated (six locales), and its numbers are invisible to AI
    crawlers. Here every label and value is real text.
  * The caption is a <div> + <p>, not <figure>/<figcaption>: extraction tools strip
    figcaptions on many layouts (seo-aiso-validator lessons, 2026-06-15). It should
    spell out the numbers, so the finding survives even if the bars do not.

Design rules (dataviz skill): one zero baseline per chart, bars <= 14px thick, 4px
rounded data-end and square at zero, value at the bar's end in text ink, a legend
whenever there are two or more series, recessive gridline. Palette validated with
the skill's validate_palette.js: #016569 (Matrixyl teal) vs #9AA3A4 (placebo grey)
passes CVD (ΔE 22.4) and normal vision (ΔE 25.7); the grey is < 3:1 on white, so every
bar carries a visible value and the page repeats the numbers in a table.

Never emit "{{", "}}", "{%" or "%}": the custom-html setting rejects all four as Liquid
syntax. CSS nests braces, so a media query closing right after a rule ("…;}}") trips it —
render_group() spaces every "}}" out (hit on the first Matrixyl upload, 2026-09-22).
"""
import html as H

MINUS = "−"
PCT = {"en": "%", "de": " %", "fr": " %", "es": " %", "nl": "%", "it": "%"}

CSS = (".sgfig{max-width:1120px;margin:0 auto;padding:8px 20px 8px;color:#1A1A1A;}"
       ".sgfig h2{text-align:center;margin:0 0 12px;}"
       ".sgfig-intro{max-width:720px;margin:0 auto 28px;text-align:center;}"
       ".sgfig-grid{display:grid;grid-template-columns:1fr;gap:24px;align-items:start;}"
       "@media (min-width:900px){.sgfig-grid.sgfig-two{grid-template-columns:1fr 1fr;}}"
       ".sgfig-card{background:#fff;border:1px solid #E4E4E4;border-radius:12px;padding:24px 22px 20px;}"
       ".sgfig-title{font-size:18px;font-weight:700;line-height:1.35;margin:0 0 4px;}"
       ".sgfig-sub{font-size:14px;color:#5A5A5A;margin:0 0 14px;line-height:1.45;}"
       ".sgfig-legend{display:flex;flex-wrap:wrap;gap:6px 18px;font-size:13px;color:#3A3A3A;margin:0 0 14px;}"
       ".sgfig-legend span{display:inline-flex;align-items:center;gap:7px;}"
       ".sgfig-key{width:14px;height:14px;border-radius:3px;display:inline-block;}"
       ".sgfig-row{padding:9px 0;border-top:1px solid #F0F0F0;}"
       ".sgfig-label{font-size:14px;font-weight:600;margin:0 0 6px;line-height:1.35;}"
       ".sgfig-line{display:grid;grid-template-columns:1fr 70px;align-items:center;gap:10px;margin:3px 0;}"
       ".sgfig-track{position:relative;height:14px;}"
       ".sgfig-zero{position:absolute;top:-4px;bottom:-4px;width:1px;background:#C9C9C9;}"
       ".sgfig-bar{position:absolute;top:0;height:14px;min-width:2px;}"
       ".sgfig-val{font-size:14px;font-weight:700;font-variant-numeric:tabular-nums;white-space:nowrap;}"
       ".sgfig-val.sgfig-quiet{font-weight:500;color:#5A5A5A;}"
       ".sgfig-axis{display:grid;grid-template-columns:1fr 70px;gap:10px;font-size:12px;color:#5A5A5A;margin-top:6px;}"
       ".sgfig-axis div{position:relative;height:14px;}"
       ".sgfig-axis span{position:absolute;transform:translateX(-50%);white-space:nowrap;}"
       ".sgfig-table{width:100%;border-collapse:collapse;margin-top:16px;font-size:13px;font-variant-numeric:tabular-nums;}"
       ".sgfig-table th,.sgfig-table td{padding:6px 8px;border-bottom:1px solid #EDEDED;text-align:right;}"
       ".sgfig-table th:first-child,.sgfig-table td:first-child{text-align:left;}"
       ".sgfig-table th{font-weight:600;color:#3A3A3A;}"
       ".sgfig-caption{margin-top:14px;font-size:14px;line-height:1.55;color:#3A3A3A;}"
       ".sgfig-caption p{margin:0 0 6px;}")


def fmt(v, loc, unit="%", signed=True, decimals=None):
    if decimals is not None:
        s = f"{abs(v):.{decimals}f}"
    else:
        s = f"{abs(v):.1f}".rstrip("0").rstrip(".") if abs(v) % 1 else f"{abs(v):.0f}"
    if loc != "en":
        s = s.replace(".", ",")
    sign = (MINUS if v < 0 else "+" if v > 0 else "") if signed else (MINUS if v < 0 else "")
    return sign + s + (PCT.get(loc, "%") if unit == "%" else unit)


def _pos(v, a, b):
    return (v - a) / (b - a) * 100


def render_chart(c, loc):
    a, b = c["domain"]
    z = _pos(0, a, b)
    out = [f'<div class="sgfig-card"><p class="sgfig-title">{c["title"][loc]}</p>']
    if c.get("subtitle"):
        out.append(f'<p class="sgfig-sub">{c["subtitle"][loc]}</p>')
    if len(c["series"]) > 1:
        out.append('<p class="sgfig-legend">' + "".join(
            f'<span><i class="sgfig-key" style="background:{s["color"]}"></i>{s["label"][loc]}</span>' for s in c["series"]) + "</p>")
    for r in c["rows"]:
        out.append(f'<div class="sgfig-row"><p class="sgfig-label">{r["label"][loc]}</p>')
        for s in c["series"]:
            if s["key"] not in r["values"]:
                continue
            v = r["values"][s["key"]]
            color = r.get("colors", {}).get(s["key"], s["color"])
            left, width = (_pos(v, a, b), z - _pos(v, a, b)) if v < 0 else (z, _pos(v, a, b) - z)
            radius = "4px 0 0 4px" if v < 0 else "0 4px 4px 0"
            quiet = " sgfig-quiet" if s.get("quiet") else ""
            val = fmt(v, loc, c.get("unit", "%"), decimals=c.get("decimals"))
            tip = H.escape(f'{H.unescape(s["label"][loc])}: {val}', quote=True)
            out.append(f'<div class="sgfig-line" title="{tip}"><div class="sgfig-track">'
                       f'<span class="sgfig-zero" style="left:{z:.2f}%"></span>'
                       f'<span class="sgfig-bar" style="left:{left:.2f}%;width:{width:.2f}%;background:{color};border-radius:{radius}"></span>'
                       f'</div><span class="sgfig-val{quiet}">{val}</span></div>')
        out.append("</div>")
    ticks = c.get("ticks")
    if ticks:
        out.append('<div class="sgfig-axis" aria-hidden="true"><div>' + "".join(
            f'<span style="left:{_pos(t, a, b):.2f}%">{fmt(t, loc, c.get("unit", "%"), signed=t != 0)}</span>' for t in ticks) + "</div><span></span></div>")
    if c.get("table_head"):
        # The table view the dataviz skill asks for, and the one element AI extraction reliably keeps
        # (seo-aiso-validator: <table> survives, div rows do not). One line, no links (a link inside a
        # table makes extractors drop it). Round-1 external audit, 2026-09-22: "use true HTML tables".
        head = "".join(f"<th>{h}</th>" for h in [c["table_head"][loc]] + [s["label"][loc] for s in c["series"]])
        body = "".join("<tr><td>" + r["label"][loc] + "</td>" + "".join(
            f'<td>{fmt(r["values"][s["key"]], loc, c.get("unit", "%"), decimals=c.get("decimals"))}</td>'
            for s in c["series"] if s["key"] in r["values"]) + "</tr>" for r in c["rows"])
        out.append(f'<table class="sgfig-table"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>')
    out.append(f'<div class="sgfig-caption">{c["caption"][loc]}</div></div>')
    return "".join(out)


def render_group(placeholder, charts, loc):
    names = placeholder["$chart"]
    head = ""
    if placeholder.get("heading"):
        head += f'<h2 class="h2">{placeholder["heading"][loc]}</h2>'   # theme styles headings by class only
    if placeholder.get("intro"):
        head += f'<div class="sgfig-intro">{placeholder["intro"][loc]}</div>'
    grid = "sgfig-grid sgfig-two" if len(names) == 2 else "sgfig-grid"
    body = "".join(render_chart(charts[n], loc) for n in names)
    out = f'<style>{CSS}</style><div class="sgfig">{head}<div class="{grid}">{body}</div></div>'
    while "}}" in out or "{{" in out:
        out = out.replace("}}", "} }").replace("{{", "{ {")
    return out
