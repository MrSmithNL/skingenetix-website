#!/usr/bin/env python3
"""Stand up the data model for the per-product before/after review carousel.

    python3 scripts/product-reviews-setup.py --check
    python3 scripts/product-reviews-setup.py --create-schema

Creates, idempotently:
  1. metaobject definition `customer_review`
  2. product metafield definition `custom.customer_reviews` (list.metaobject_reference)

WHY METAOBJECTS AND NOT A TEMPLATE PER PRODUCT
Full reasoning in docs/product-reviews-before-after-plan.md §3 and §3a. The short version is
that the sister brand answers this question by counter-example: Hairgenetix drives its
before/after from section blocks in template JSON, and the same fourteen customers are
copy-pasted into all four of its product templates. Blocks-in-template make duplication the
path of least resistance. Metaobjects give one section on one shared template, content
resolved per product, and 76 translation units instead of ~460 hash-keyed template settings.

This also follows what the store already does: `custom.faq_items` and `custom.how_to_steps`
are already `list.metaobject_reference` on products.

⚠️ TRANSLATION. The definition is created with the `translatable` capability on, and the four
text fields carry it. Metaobject entries are a first-class resource in Translate & Adapt
(ADR-002a - Translate & Adapt, NOT Langify, whatever older docs say). Settle the English
before translating: the translation key hashes the value, so editing English orphans it.

Author: Claude Code, 2026-08-29.
"""
import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "2025-01"

MO_TYPE = "customer_review"
MF_NAMESPACE = "custom"
MF_KEY = "customer_reviews"

# `concern` is not decoration: it records which Drive pool a photograph came from, so the
# allocation in the plan stays auditable after the files are renamed on upload. Slot letters
# and filenames have drifted before on this project.
FIELDS = [
    ("image", "Image (before/after diptych)", "file_reference", False,
     '[{"name":"file_type_options","value":"[\\"Image\\"]"}]'),
    ("author", "Customer name", "single_line_text_field", True, "[]"),
    ("rating", "Rating (1-5)", "number_integer", False,
     '[{"name":"min","value":"1"},{"name":"max","value":"5"}]'),
    ("title", "Review headline", "single_line_text_field", True, "[]"),
    ("body", "Review text", "multi_line_text_field", True, "[]"),
    ("before_label", "Label on the left half", "single_line_text_field", True, "[]"),
    ("after_label", "Label on the right half", "single_line_text_field", True, "[]"),
    ("verified", "Verified customer", "boolean", False, "[]"),
    ("concern", "Concern pool", "single_line_text_field", False, "[]"),
]


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
    req = urllib.request.Request(
        f"https://{e['SHOPIFY_SKINGENETIX_STORE']}/admin/oauth/access_token",
        data=body, headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=60).read())["access_token"]


def gql(store, tok, query, variables=None):
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    req = urllib.request.Request(
        f"https://{store}/admin/api/{API}/graphql.json", data=json.dumps(payload).encode(),
        headers={"X-Shopify-Access-Token": tok, "Content-Type": "application/json"})
    try:
        out = json.loads(urllib.request.urlopen(req, timeout=90).read())
    except urllib.error.HTTPError as ex:
        # Shopify names the offending field in the BODY; the status line alone is useless
        # and has cost this project a round before.
        sys.exit(f"HTTP {ex.code}\n{ex.read().decode()[:3000]}")
    if "errors" in out:
        sys.exit("GraphQL errors:\n" + json.dumps(out["errors"], indent=2)[:3000])
    return out["data"]


def find_definition(store, tok):
    d = gql(store, tok, "{ metaobjectDefinitions(first:50){nodes{id type name "
                        "fieldDefinitions{key name type{name}}}} }")
    for n in d["metaobjectDefinitions"]["nodes"]:
        if n["type"] == MO_TYPE:
            return n
    return None


def find_metafield(store, tok):
    d = gql(store, tok, '{ metafieldDefinitions(first:60, ownerType:PRODUCT)'
                        '{nodes{id namespace key type{name}}} }')
    for n in d["metafieldDefinitions"]["nodes"]:
        if n["namespace"] == MF_NAMESPACE and n["key"] == MF_KEY:
            return n
    return None


def create_definition(store, tok):
    field_defs = []
    for key, name, ftype, translatable, validations in FIELDS:
        field_defs.append({
            "key": key, "name": name, "type": ftype,
            "validations": json.loads(validations),
            # required is deliberately False on every field: an entry with no rating and no
            # author is exactly what the "illustrative, not testimony" option in the plan
            # needs, and a required field would block it.
            "required": False,
        })
    q = """
    mutation ($definition: MetaobjectDefinitionCreateInput!) {
      metaobjectDefinitionCreate(definition: $definition) {
        metaobjectDefinition { id type }
        userErrors { field message code }
      }
    }"""
    variables = {"definition": {
        "type": MO_TYPE,
        "name": "Customer Review",
        "description": "One customer before/after review card. Rendered on product pages by "
                       "sections/product-reviews-before-after.liquid, via the product "
                       "metafield custom.customer_reviews.",
        "fieldDefinitions": field_defs,
        "capabilities": {"translatable": {"enabled": True}},
        "access": {"storefront": "PUBLIC_READ"},
    }}
    d = gql(store, tok, q, variables)
    res = d["metaobjectDefinitionCreate"]
    if res["userErrors"]:
        sys.exit("metaobjectDefinitionCreate failed:\n"
                 + json.dumps(res["userErrors"], indent=2))
    return res["metaobjectDefinition"]


def create_metafield(store, tok, definition_id):
    q = """
    mutation ($definition: MetafieldDefinitionInput!) {
      metafieldDefinitionCreate(definition: $definition) {
        createdDefinition { id namespace key }
        userErrors { field message code }
      }
    }"""
    variables = {"definition": {
        "name": "Customer reviews (before/after)",
        "namespace": MF_NAMESPACE,
        "key": MF_KEY,
        "description": "The before/after review cards shown on this product's page, in order.",
        "type": "list.metaobject_reference",
        "ownerType": "PRODUCT",
        # Without this validation any metaobject could be referenced, and a mistyped handle
        # would attach a FAQ item to the review carousel and render an empty card.
        "validations": [{"name": "metaobject_definition_id", "value": definition_id}],
        "access": {"storefront": "PUBLIC_READ"},
    }}
    d = gql(store, tok, q, variables)
    res = d["metafieldDefinitionCreate"]
    if res["userErrors"]:
        sys.exit("metafieldDefinitionCreate failed:\n" + json.dumps(res["userErrors"], indent=2))
    return res["createdDefinition"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="report what exists, change nothing")
    ap.add_argument("--create-schema", action="store_true")
    args = ap.parse_args()

    e = env()
    store = e["SHOPIFY_SKINGENETIX_STORE"]
    tok = token(e)

    mo = find_definition(store, tok)
    mf = find_metafield(store, tok)

    print(f"metaobject `{MO_TYPE}`: " + (f"EXISTS ({mo['id']})" if mo else "missing"))
    if mo:
        for f in mo["fieldDefinitions"]:
            print(f"    {f['key']:<14} {f['type']['name']}")
    print(f"metafield `{MF_NAMESPACE}.{MF_KEY}`: " + (f"EXISTS ({mf['id']})" if mf else "missing"))

    if args.check or not args.create_schema:
        return

    if not mo:
        mo = create_definition(store, tok)
        print(f"created metaobject definition {mo['id']}")
    if not mf:
        mf = create_metafield(store, tok, mo["id"])
        print(f"created metafield definition {mf['id']}")
    print("schema ready")


if __name__ == "__main__":
    main()
