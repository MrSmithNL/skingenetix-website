#!/usr/bin/env python3
"""Author and apply SEO alt text to every product image on the store.

    python3 scripts/finals/set-product-alt-text.py [--apply]

Alt text is the only image-level SEO field Shopify exposes through the API, and
it does double duty: it is what a screen reader announces and what Google Images
indexes. Both jobs are done by the same sentence, so it has to describe the
image truthfully AND carry the terms the product is searched by.

House format, capped at 125 characters:

    Skingenetix <Product>, <key active>, <size> - <what is actually in frame>

The tail is written from LOOKING at each image. Deriving it from the filename
produces "Pdrn collagen copper peptide deep renewal repair skin cream hero
whitebg", which serves neither reader.

Audited 2026-08-20: of 66 live images, 9 had no alt at all, 24 carried a thin
keyword phrase with no description, and 15 authored ones ran over 125 chars
because the product prefix ate the budget.

Author: Claude Code, 2026-08-20.
"""
import json
import os
import sys
import urllib.request

API = "2025-01"
LIMIT = 125

#: Brand + product + key active + size. Deliberately short: the tail needs room.
PREFIX = {
    "acetyl-hexapeptide-8-anti-wrinkle-serum":
        "Skingenetix Acetyl Hexapeptide-8 Anti-Wrinkle Serum, 10% Argireline, 30ml",
    "copper-peptide-ghk-cu-renewal-serum":
        "Skingenetix Copper Peptide Renewal Serum, 2% GHK-Cu, 30ml",
    "matrixyl-3000-hyaluronic-acid-collagen-serum":
        "Skingenetix Matrixyl 3000 Pro-Collagen Serum, 10% Matrixyl, 30ml",
    "copper-peptide-ghk-cu-day-gel-cream":
        "Skingenetix Copper Peptide Day Repair Cream, 2% GHK-Cu, 50ml",
    "copper-peptide-ghk-cu-night-cream":
        "Skingenetix Copper Peptide Night Repair Cream, 2% GHK-Cu, 50ml",
    "matrixyl-3000-pro-collagen-firming-cream":
        "Skingenetix Matrixyl 3000 Pro-Collagen Firming Cream, 50ml",
    "pdrn-renewal-serum":
        "Skingenetix PDRN Renewal Serum, 1% PDRN, 30ml",
    "pdrn-collagen-night-cream":
        "Skingenetix PDRN Collagen Repair Cream, 50ml",
    "glutathione-brightening-serum":
        "Skingenetix Glutathione Brightening Serum, 2% glutathione, 30ml",
    "copper-peptide-ghk-cu-microneedling-facial-stamp-set-1-month":
        "Skingenetix Copper Peptide Microneedling Facial Stamp Set, 1 month",
    "pdrn-microneedling-facial-stamp-set-1-month":
        "Skingenetix PDRN Microneedling Facial Stamp Set, 1 month",
}

#: One description per image, in the product's live media order.
TAILS = {
    "acetyl-hexapeptide-8-anti-wrinkle-serum": [
        "frosted glass dropper bottle on white",
        "bottle beaded with water droplets against blue",
        "macro of a clear serum swipe on a pale surface",
        "a model applying the serum with the glass dropper",
        "a model holding the bottle beside their face",
    ],
    "copper-peptide-ghk-cu-renewal-serum": [
        "blue glass dropper bottle on white",
        "bottle beside its carton with a jade roller and eucalyptus",
        "hands holding the bottle, a blue drop on a fingertip",
        "macro of the pipette tip and a blue serum drop",
        "extreme close-up of the bottle shoulder and pipette collar",
        "dropper poised over the open bottle of blue serum",
        "dropper releasing a blue drop onto a cheek",
    ],
    "matrixyl-3000-hyaluronic-acid-collagen-serum": [
        "frosted glass dropper bottle on white",
        "bottle lit against a deep teal gradient",
        "bottle beaded with water against turquoise",
        "bottle standing on rippling turquoise water",
        "a winding trail of clear serum on teal",
        "dropper releasing a drop beside a model's cheek",
        "a model holding the bottle beside their face",
    ],
    "copper-peptide-ghk-cu-day-gel-cream": [
        "jar on a white background with a soft shadow",
        "open jar on a bathroom counter with a swatch of the blue cream",
        "a model holding the jar beside their face",
        "open jar beside its blue and silver cartons",
        "close-up of the jar with the label in sharp focus",
        "jar on dark stone with raw copper ore",
        "a model with the blue cream smoothed onto one cheek",
        "jar on a bathroom shelf beside a reed diffuser",
        "several jars arranged in a group",
    ],
    "copper-peptide-ghk-cu-night-cream": [
        "jar on a white background",
        "a model holding the jar beside their face",
        "open jar with a swatch of the pale blue cream",
        "jar resting in a swirl of the pale blue cream",
        "the pale blue cream smoothed onto a cheek",
        "jar resting on moonlit silk",
        "jar on a bathroom shelf with towels and eucalyptus",
        "several jars arranged in a group",
    ],
    "matrixyl-3000-pro-collagen-firming-cream": [
        "frosted glass jar with brushed lid on white",
        "jar resting in a swirl of the white cream",
        "a model holding the jar beside their face",
        "close-up of the white cream smoothed onto a cheek",
        "open jar with the lid beside it and a smear of cream on marble",
        "two swipes of the white cream on marble",
        "jar beaded with water droplets",
    ],
    "pdrn-renewal-serum": [
        "pink glass dropper bottle on white",
        "bottle on a pedestal against a deep pink gradient",
        "a model holding the bottle beside their face",
        "dropper releasing a pink drop into the open bottle",
        "dropper applying a pink drop to a cheek",
    ],
    "pdrn-collagen-night-cream": [
        "jar on a white background",
        "open jar with a swatch of the pink cream",
        "jar beside its pink and silver carton",
        "jar resting on cream silk",
        "jar on a colour-block pedestal",
        "stacked jars from the Skingenetix range",
        "close-up of the pink cream applied to a cheek",
        "a model with the cream applied",
    ],
    "glutathione-brightening-serum": [
        "bottle beside its gold carton on white",
        "hands lifting the glass dropper from the bottle",
        "frosted bottle on a pale stone pedestal",
        "a single drop of the serum on a fingertip",
        "a model holding the bottle beside their face",
        "bottle on travertine with dried flowers and linen",
        "overhead view of the bottle on sunlit water",
        "several bottles arranged in an angled group",
    ],
    # The images on both stamp sets currently show HAIRGENETIX packaging, not
    # Skingenetix. The alt describes what is in frame without asserting a brand;
    # the real fix is replacing the photographs. Flagged in docs/todo.md.
    "copper-peptide-ghk-cu-microneedling-facial-stamp-set-1-month": [
        "presentation box with the stamp and serum vials",
    ],
    "pdrn-microneedling-facial-stamp-set-1-month": [
        "open presentation box with the stamp and serum vials",
    ],
}


def compose(handle, i):
    """The alt text for image `i` of `handle`, or None if undescribed."""
    tails = TAILS.get(handle) or []
    if i >= len(tails):
        return None
    alt = f"{PREFIX[handle]} - {tails[i]}"
    if len(alt) > LIMIT:
        raise ValueError(f"{handle} #{i} is {len(alt)} chars: {alt}")
    return alt


def token(store, cid, sec):
    body = json.dumps({"client_id": cid, "client_secret": sec,
                       "grant_type": "client_credentials"}).encode()
    req = urllib.request.Request(f"https://{store}/admin/oauth/access_token", data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())["access_token"]


def gql(store, tok, query, variables=None):
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(f"https://{store}/admin/api/{API}/graphql.json", data=body,
                                 headers={"Content-Type": "application/json",
                                          "X-Shopify-Access-Token": tok})
    with urllib.request.urlopen(req, timeout=180) as r:
        d = json.loads(r.read())
    if d.get("errors"):
        raise RuntimeError(d["errors"])
    return d["data"]


def main():
    apply = "--apply" in sys.argv
    store = os.environ["SHOPIFY_SKINGENETIX_STORE"].replace("https://", "").rstrip("/")
    tok = token(store, os.environ["SHOPIFY_SKINGENETIX_CLIENT_ID"],
                os.environ["SHOPIFY_SKINGENETIX_CLIENT_SECRET"])

    prods = gql(store, tok, """{ products(first:40){ edges{ node{ id title handle
        media(first:60){ edges{ node{ ... on MediaImage { id alt } } } } } } } }"""
                )["products"]["edges"]

    changed = skipped = same = 0
    for e in prods:
        n = e["node"]
        eds = n["media"]["edges"]
        if not eds:
            continue
        updates = []
        for i, x in enumerate(eds):
            want = compose(n["handle"], i)
            if want is None:
                skipped += 1
                print(f"  ?  {n['handle']} #{i} has no description written")
                continue
            if (x["node"].get("alt") or "") == want:
                same += 1
                continue
            updates.append({"id": x["node"]["id"], "alt": want})
        if not updates:
            continue
        print(f"\n{n['title']}  ({len(updates)} to update)")
        for u in updates:
            print(f"   [{len(u['alt']):>3}] {u['alt']}")
        changed += len(updates)
        if apply:
            d = gql(store, tok, """mutation($id:ID!,$media:[UpdateMediaInput!]!){
                  productUpdateMedia(productId:$id, media:$media){
                    mediaUserErrors{ field message } } }""",
                    {"id": n["id"], "media": updates})
            errs = d["productUpdateMedia"]["mediaUserErrors"]
            if errs:
                raise RuntimeError(f"{n['handle']}: {errs}")

    print(f"\n{changed} to change, {same} already correct, {skipped} undescribed")
    if not apply:
        print("DRY RUN - pass --apply to write them")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
