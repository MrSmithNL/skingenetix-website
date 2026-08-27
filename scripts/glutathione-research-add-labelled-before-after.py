#!/usr/bin/env python3
"""Move both before/after findings on /pages/glutathione-research into labelled sections.

    python3 scripts/glutathione-research-add-labelled-before-after.py --dry-run
    python3 scripts/glutathione-research-add-labelled-before-after.py

Malcolm, 2026-08-27: "lets use the labels content block for this - to add the labels with
the research conclusions". Same treatment as /pages/acetyl-hexapeptide-8-research and
/pages/pdrn-research: the diptychs move into `research-before-after` sections, whose
`finding` blocks render Before / After / a result line as DOM TEXT over the image rather
than baked into the pixels. Two reasons, both on this project's record: no engine ever
renders the conclusion, so it cannot be garbled into a false claim; and the labels stay
translatable, because Translate & Adapt reaches theme JSON and cannot touch pixels.

WHY THIS IS ITS OWN SCRIPT. patch-template.py assigns images and appends sections; it does
not move blocks between sections or rewrite the alternation. Same reasoning as
scripts/pdrn-research-add-before-after.py, which did the single-block version of this.

WHY IT IS HARDER HERE THAN ON PDRN, AND WHY THE SPACING FIX IS IN THE SAME SCRIPT.
PDRN lifted ONE block off the top of `key_findings`. Here f1 and f3 are both diptychs and
f2 — the antioxidant-defence diagram — sits between them and must stay a media-with-text
row. So the single section becomes THREE, in order:

    key_findings_ba1   research-before-after   f1 (Watanabe 2014)
    key_findings       media-with-text         f2 (Grandi 2019 diagram)
    key_findings_ba3   research-before-after   f3 (Khanna 2025)

which opens TWO section boundaries where there used to be grid row gaps. Measured on the
PDRN page when it made one: 160px at 1440 and 128px at 1024, against the grid's own 24px,
because the space becomes the sum of two .section wrappers' 80px vertical padding. Doing
the split without the spacing fix would ship that regression twice, so both land together.

⚠️ THE PDRN FIX DOES NOT COVER THIS PAGE, IN EITHER SENSE. It is a template-local
custom-html section on page.pdrn-research.json, so it does not leak here — and its selector
is the adjacency `research-before-after` FOLLOWED BY `media-with-text`, which is only one of
the two boundaries here. The second boundary is the reverse pair. Both directions are
handled below.

ALTERNATION. `media-with-text` derives left/right from BLOCK INDEX when
`alternate_media_position` is true, so today's three rows read left / right / left. With f1
and f3 lifted out, f2 would be index 0 and flip to left. Alternation is therefore switched
off and f2 carries an explicit `end`, reproducing the current rhythm exactly.

THE LABELS ARE NEW TEXT, THE BODY COPY IS NOT. `title` and `content` are carried across
VERBATIM from the existing blocks — changing page copy is a stop condition. Only the four
label settings are authored here, and `note_label` is left EMPTY: the "Illustration" label
was an unrequested addition on the other research pages and was removed from all four in
commit c9d0cf1. Do not reintroduce it.

⚠️ TRANSLATION KEYS. A section id change creates entirely new
ONLINE_STORE_THEME_JSON_TEMPLATE keys and orphans the old ones. That is free today because
only `en` is published and no translations exist. After nine locales are populated it would
mean redoing them. See docs/research-before-after-section.md §3.

Only section JSON is touched, never Liquid — .claude/rules/shopify.md rule 2.

Author: Claude Code, 2026-08-27.
"""
import argparse
import json
import urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "2025-01"
TEMPLATE = "templates/page.glutathione-research.json"
BA1 = "key_findings_ba1"
BA3 = "key_findings_ba3"
SPACING = "findings_spacing_fix"

#: The labels. Each result line states the study's own conclusion in the study's own terms.
#:
#: f1 — Watanabe F et al. (2014), Clinical, Cosmetic and Investigational Dermatology.
#:   Randomised, double-blind, split-face, placebo-controlled; 30 women aged 30-50; 2% GSSG
#:   lotion twice daily for 10 weeks. "After 10 weeks" is the trial's own duration.
#:   The result line drops the word "significantly" that the body copy uses. Not a softening
#:   of the finding: in a short label, beside no other statistics, "significantly" reads as
#:   "a lot" rather than "statistically significant", and the p-value carries the real
#:   meaning precisely. The body copy above it is untouched and still says it.
#:
#: f3 — Khanna R, Rambhia P, Chapas A (2025), Journal of Clinical and Aesthetic Dermatology.
#:   A SYSTEMATIC REVIEW, not a trial. It pools studies of differing lengths, so there is no
#:   honest duration to put on the after label and it stays a bare "After". The result line
#:   is the review's own conclusion, and deliberately carries no number, because the review
#:   reports none.
LABELS = {
    "f1": {"after": "After 10 weeks",
           "result": "More even-looking skin tone vs placebo (p < 0.001)"},
    "f3": {"after": "After",
           "result": "Measurable benefits for the appearance of skin tone"},
}

# `custom-html` rejects a value containing '{{', '}}', '{%' or '%}' with a 422 whose real
# message is only in the response body. Plain CSS trips it by accident: a rule closing
# immediately before a media query's own closing brace produces '}}'. Hence the space
# before each closing brace below, and the assertion under it that scans for all four.
CSS = (
    "<style>"
    "/* Added by Claude Code 2026-08-27. f1 and f3 live in their own research-before-after "
    "sections, so the space to the neighbouring finding is two section paddings "
    "(80+80=160px) instead of the media-with-text grid row gap (24px). Trim only the four "
    "facing edges. BOTH adjacency directions are needed here: ba1 sits ABOVE the "
    "media-with-text row and ba3 sits BELOW it. Scoped by structure rather than by section "
    "id, because ids are template-scoped and go stale on rebuild; and never by class alone, "
    "because the acetyl page's research-before-after section is followed by `references` "
    "and its 80px is correct there. */"
    ".shopify-section--research-before-after:has(+ .shopify-section--media-with-text) "
    "> .section { padding-block-end: 12px; }"
    ".shopify-section--research-before-after + .shopify-section--media-with-text "
    "> .section { padding-block-start: 12px; }"
    ".shopify-section--media-with-text:has(+ .shopify-section--research-before-after) "
    "> .section { padding-block-end: 12px; }"
    ".shopify-section--media-with-text + .shopify-section--research-before-after "
    "> .section { padding-block-start: 12px; }"
    "@media (max-width: 999px) {"
    ".shopify-section--research-before-after:has(+ .shopify-section--media-with-text) "
    "> .section { padding-block-end: 10px; }"
    ".shopify-section--research-before-after + .shopify-section--media-with-text "
    "> .section { padding-block-start: 10px; }"
    ".shopify-section--media-with-text:has(+ .shopify-section--research-before-after) "
    "> .section { padding-block-end: 10px; }"
    ".shopify-section--media-with-text + .shopify-section--research-before-after "
    "> .section { padding-block-start: 10px; } "   # trailing space: avoids '}}'
    "}"
    "</style>"
)

for _bad in ("{{", "}}", "{%", "%}"):
    assert _bad not in CSS, f"custom-html will 422 on {_bad!r}"


def env():
    out = {}
    for line in (ROOT / ".env").read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            out[k.strip()] = v.strip()
    return out


def token(e):
    body = json.dumps({"client_id": e["SHOPIFY_SKINGENETIX_CLIENT_ID"],
                       "client_secret": e["SHOPIFY_SKINGENETIX_CLIENT_SECRET"],
                       "grant_type": "client_credentials"}).encode()
    req = urllib.request.Request(f"https://{e['SHOPIFY_SKINGENETIX_STORE']}/admin/oauth/access_token",
                                 data=body, headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=60).read())["access_token"]


def call(store, tok, path, method="GET", payload=None):
    data = json.dumps(payload).encode() if payload else None
    r = urllib.request.Request(f"https://{store}/admin/api/{API}/{path}", data=data, method=method,
                               headers={"X-Shopify-Access-Token": tok,
                                        "Content-Type": "application/json"})
    with urllib.request.urlopen(r, timeout=120) as res:
        return json.loads(res.read())


def finding_section(src_settings: dict, key: str, position: str) -> dict:
    """One research-before-after section carrying one finding block.

    `title` and `content` come straight off the media-with-text block, unedited.
    """
    return {
        "type": "research-before-after",
        "blocks": {
            key: {
                "type": "finding",
                "settings": {
                    "image": src_settings["image"],
                    "media_position": position,
                    "before_label": "Before",
                    "after_label": LABELS[key]["after"],
                    "result_label": LABELS[key]["result"],
                    # Deliberately empty — see the module docstring.
                    "note_label": "",
                    "label_background": "#1a1a1a",
                    "label_text_color": "#ffffff",
                    "title": src_settings["title"],
                    "content": src_settings["content"],
                },
            }
        },
        "block_order": [key],
        "settings": {},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    e = env()
    store = e["SHOPIFY_SKINGENETIX_STORE"]
    tok = token(e)
    theme = [t for t in call(store, tok, "themes.json")["themes"] if t["role"] == "main"][0]
    print(f"Live theme : {theme['name']} (id {theme['id']})")

    asset = call(store, tok, f"themes/{theme['id']}/assets.json?asset[key]={TEMPLATE}")["asset"]
    tpl = json.loads(asset["value"])

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = ROOT / "backups" / f"page.glutathione-research-{stamp}.json"
    backup.write_text(asset["value"])
    print(f"Backup     : {backup.relative_to(ROOT)}")
    print(f"Undo with  : python3 scripts/patch-template.py --restore "
          f"{backup.relative_to(ROOT)} --template {TEMPLATE}\n")

    if BA1 in tpl["sections"] or BA3 in tpl["sections"]:
        print("Already converted — nothing to do.")
        return

    kf = tpl["sections"]["key_findings"]
    f1 = kf["blocks"]["f1"]["settings"]
    f3 = kf["blocks"]["f3"]["settings"]

    # Refuse rather than publish a labelled before/after over a picture that is not one.
    # Both blocks were repointed to diptychs earlier today; if a later session swaps one
    # back to a single photograph the labels would sit over nothing and say "Before".
    for name, s in (("f1", f1), ("f3", f3)):
        if "before-after" not in s.get("image", ""):
            raise SystemExit(f"{name} image is {s.get('image')!r} — not a before/after "
                             f"master. Refusing to put Before/After labels on it.")

    # 1. the two labelled sections. f1 keeps image-LEFT and f3 keeps image-LEFT, which is
    #    what today's alternation produces for block indices 0 and 2.
    tpl["sections"][BA1] = finding_section(f1, "f1", "start")
    tpl["sections"][BA3] = finding_section(f3, "f3", "start")

    # 2. key_findings keeps f2 alone. Alternation off, explicit `end`, so the middle row
    #    stays image-RIGHT instead of flipping to index 0's left.
    for b in ("f1", "f3"):
        del kf["blocks"][b]
    kf["block_order"] = [b for b in kf["block_order"] if b == "f2"]
    kf["settings"]["alternate_media_position"] = False
    kf["blocks"]["f2"]["settings"]["media_position"] = "end"

    # 3. order: ba1 immediately before key_findings, ba3 immediately after it.
    order = list(tpl["order"])
    i = order.index("key_findings")
    order.insert(i, BA1)
    order.insert(i + 2, BA3)

    # 4. the spacing carrier, which must add no height of its own.
    tpl["sections"][SPACING] = {
        "type": "custom-html",
        "settings": {
            "full_width": True,
            "remove_vertical_spacing": True,
            "remove_horizontal_spacing": True,
            "html": CSS,
            "background": "",
        },
    }
    if SPACING not in order:
        order.append(SPACING)
    tpl["order"] = order

    print("Section order now: " + " -> ".join(tpl["order"]))
    for key in ("f1", "f3"):
        print(f"  {key}: Before / {LABELS[key]['after']} / '{LABELS[key]['result']}'")
    print(f"  key_findings: block_order now {kf['block_order']}, "
          f"alternate_media_position False, f2=end")
    print("  spacing: four facing edges trimmed to 12px (24px total, = the grid row gap); "
          "10px under 1000px")

    if args.dry_run:
        out = ROOT / "backups" / f"page.glutathione-research-PROPOSED-{stamp}.json"
        out.write_text(json.dumps(tpl, indent=2))
        print(f"\nDRY RUN — proposed template at {out.relative_to(ROOT)}, nothing pushed")
        return

    call(store, tok, f"themes/{theme['id']}/assets.json", "PUT",
         {"asset": {"key": TEMPLATE, "value": json.dumps(tpl, indent=2)}})
    print("\nPUSHED to the live theme.")


if __name__ == "__main__":
    main()
