#!/usr/bin/env python3
"""Link in-text study citations in a hub spec to their source — first mention per text block, every language.

Author: Claude (Opus 5) for Malcolm Smith · 2026-09-22
Purpose: the hubs cite studies as "(Kang et al., 2009)" in prose, but only the References list at the foot of
the page linked anywhere — 14 in-text citations on the three upgraded hubs, none clickable. A reader checking
a claim had to scroll past the rest of the page to find it.

    python3 scripts/link-citations.py configs/hub-upgrades/copper-peptide-research.json            # show changes
    python3 scripts/link-citations.py configs/hub-upgrades/copper-peptide-research.json --write    # edit the spec
    then: python3 scripts/hub-upgrade.py <spec> --apply   (the spec is the source of truth; this only edits it)

Rules:
  * The author/year → URL map is built from the spec's own `jsonld.citation` list, so a link can only point
    at a study the page already lists in its References and structured data.
  * First mention of each study per text block only. Repeating the link on every mention is clutter.
  * Opens in a new tab: the reader is mid-page and should not lose their place.
  * Citations not in the map (e.g. a conference abstract with no PubMed record) stay as plain text.
  * Idempotent: an already-linked citation is left alone.
"""
import argparse, json, pathlib, re, sys


def cite_map(spec):
    m = {}
    for c in spec.get("jsonld", {}).get("citation", []):
        surname = re.split(r"[ ,]", c["author"].strip())[0]
        m[(surname.lower(), str(c["datePublished"])[:4])] = c["url"]
    return m


CITE = re.compile(r"(?<![>\w-])([A-Z][A-Za-zÀ-ſ\-]+) et al\.,? (\d{4})")


def link_text(html, cmap):
    done, out, pos = set(), [], 0
    for m in CITE.finditer(html):
        key = (m.group(1).lower(), m.group(2))
        before = html[:m.start()]
        inside_link = before.rfind("<a ") > before.rfind("</a>")
        if key not in cmap or key in done or inside_link:
            continue
        done.add(key)
        out.append(html[pos:m.start()])
        out.append(f"<a href='{cmap[key]}' target='_blank' rel='noopener'>{m.group(0)}</a>")
        pos = m.end()
    out.append(html[pos:])
    return "".join(out), len(done)


def locale_values(node, label):
    """Yield (label, {en:..., de:...}) for every six-locale text inside add_sections / add_blocks (2026-09-22).
    The dicts are yielded by reference, so linking them edits the spec in place."""
    if isinstance(node, dict):
        if "en" in node and isinstance(node["en"], str):
            if "<p>" in node["en"]:           # richtext only: a plain text setting would print the <a> tag
                yield label, node
            return
        for k, v in node.items():
            yield from locale_values(v, f"{label}.{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from locale_values(v, f"{label}[{v.get('id', i) if isinstance(v, dict) else i}]")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    p = pathlib.Path(a.spec)
    spec = json.loads(p.read_text())
    cmap = cite_map(spec)
    blocks = [(s["at"], s["values"]) for s in spec.get("set", [])] + \
             [(s["id"], s["values"]) for s in spec.get("insert_sections", [])] + \
             list(locale_values(spec.get("add_sections", []), "add_sections")) + \
             list(locale_values(spec.get("add_blocks", []), "add_blocks"))
    total = 0
    for label, values in blocks:
        counts = {}
        for loc, v in values.items():
            values[loc], counts[loc] = link_text(v, cmap)
        if counts.get("en"):
            uneven = {l: n for l, n in counts.items() if n != counts["en"]}
            print(f"  {label:<28} {counts['en']} citation(s) linked" + (f"  ⚠ locale counts differ: {uneven}" if uneven else " in all six languages"))
            total += counts["en"]
            if uneven:
                sys.exit("  ✗ a locale lost or gained a citation — check its text before writing")
    unlinked = sorted({f"{m.group(1)} {m.group(2)}" for _, v in blocks for m in CITE.finditer(v["en"])
                       if (m.group(1).lower(), m.group(2)) not in cmap})
    if unlinked:
        print(f"  not in References, left as text: {', '.join(unlinked)}")
    print(f"  {total} links")
    if a.write:
        p.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n")
        print(f"  written: {p}")


if __name__ == "__main__":
    main()
