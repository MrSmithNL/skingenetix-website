#!/usr/bin/env python3
"""Register translations for a named set of theme-template keys, one locale at a time.

Why this exists rather than the shopify-website-translator skill: that skill audits
and retranslates a WHOLE locale across eight content layers, which is right when a
language is being brought up but wrong for a surgical fix. Here a single section was
rewritten in English and only its own keys need new translations in five locales.
Running the whole-theme layer would re-touch every other string on the store and put
translations that are already correct at risk.

Two things this guards that are easy to get wrong:

  * THE DIGEST IS FETCHED IMMEDIATELY BEFORE REGISTERING, never taken from the config.
    `translatableContentDigest` is a hash of the CURRENT English value. If the English
    text is edited between reading and writing, a stale digest silently registers a
    translation against text that no longer exists and Shopify marks it outdated.

  * KEYS ARE MATCHED BY PREFIX, NOT BY FULL KEY. A key carries a `:hash` suffix of its
    own English value — `...standards.title:3n6agclaws4vo` — so hardcoding a full key
    breaks the moment the English changes. The config names the stable prefix.

Anything not named in the config is left alone, which matters here because Shopify
exposes the injected CSS block (`standards_layout_css.html`) as a translatable string.
Translating that would put a stylesheet through a translator.

Author: Claude Code, 2026-09-10.

    python3 scripts/register-translations.py configs/translations/<plan>.json [--dry-run]
"""
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "2025-01"


def env():
    d = {}
    for line in (ROOT / ".env").read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            d[k] = v.strip().strip('"').strip("'")
    return d


def token(e):
    req = urllib.request.Request(
        f"https://{e['SHOPIFY_SKINGENETIX_STORE']}/admin/oauth/access_token",
        data=json.dumps({
            "client_id": e["SHOPIFY_SKINGENETIX_CLIENT_ID"],
            "client_secret": e["SHOPIFY_SKINGENETIX_CLIENT_SECRET"],
            "grant_type": "client_credentials"}).encode(),
        headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req).read())["access_token"]


def gql(store, tok, query, variables=None):
    req = urllib.request.Request(
        f"https://{store}/admin/api/{API}/graphql.json",
        data=json.dumps({"query": query, "variables": variables or {}}).encode(),
        headers={"X-Shopify-Access-Token": tok, "Content-Type": "application/json"})
    out = json.loads(urllib.request.urlopen(req).read())
    if "errors" in out:
        sys.exit(f"GraphQL: {out['errors']}")
    return out["data"]


FETCH = """
query($id: ID!, $locale: String!) {
  translatableResource(resourceId: $id) {
    resourceId
    translatableContent { key value digest }
    translations(locale: $locale) { key value outdated }
  }
}"""

REGISTER = """
mutation($id: ID!, $translations: [TranslationInput!]!) {
  translationsRegister(resourceId: $id, translations: $translations) {
    userErrors { field message }
    translations { key locale value }
  }
}"""


def main():
    plan_path = ROOT / sys.argv[1]
    dry = "--dry-run" in sys.argv
    plan = json.loads(plan_path.read_text())
    e = env()
    store = e["SHOPIFY_SKINGENETIX_STORE"]
    tok = token(e)
    rid = plan["resource_id"]

    print(f"Store    : {store}")
    print(f"Resource : {rid}")
    print(f"Locales  : {', '.join(plan['translations'].keys())}")
    print(f"Keys     : {len(plan['keys'])}  ({'DRY RUN' if dry else 'LIVE'})\n")

    for locale, values in plan["translations"].items():
        data = gql(store, tok, FETCH, {"id": rid, "locale": locale})
        content = {c["key"]: c for c in data["translatableResource"]["translatableContent"]}
        existing = {t["key"]: t for t in data["translatableResource"]["translations"]}

        inputs, report = [], []
        for prefix in plan["keys"]:
            # Resolve the stable prefix to the live hashed key.
            matches = [k for k in content if k.rsplit(":", 1)[0] == prefix]
            if not matches:
                report.append(f"    !! no live key for prefix {prefix}")
                continue
            if len(matches) > 1:
                report.append(f"    !! prefix {prefix} matched {len(matches)} keys — skipped")
                continue
            key = matches[0]
            if prefix not in values:
                report.append(f"    -- {prefix.split('.')[-1]}: no translation supplied, left alone")
                continue
            was = existing.get(key)
            state = "new" if not was else ("outdated -> replaced" if was["outdated"] else "overwritten")
            inputs.append({"key": key,
                           "locale": locale,
                           "value": values[prefix],
                           "translatableContentDigest": content[key]["digest"]})
            report.append(f"    {prefix.split('.')[-1]:<14} {state}")

        print(f"  {locale}:")
        for r in report:
            print(r)
        if dry:
            print(f"    would register {len(inputs)}\n")
            continue
        res = gql(store, tok, REGISTER, {"id": rid, "translations": inputs})
        errs = res["translationsRegister"]["userErrors"]
        if errs:
            sys.exit(f"    userErrors: {errs}")
        print(f"    registered {len(res['translationsRegister']['translations'])}\n")

    if dry:
        return

    # Verify by re-reading, never trust the mutation's own response.
    print("Verify:")
    ok = True
    for locale, values in plan["translations"].items():
        data = gql(store, tok, FETCH, {"id": rid, "locale": locale})
        content = {c["key"]: c for c in data["translatableResource"]["translatableContent"]}
        live = {t["key"]: t for t in data["translatableResource"]["translations"]}
        missing, stale = [], []
        for prefix in plan["keys"]:
            if prefix not in values:
                continue
            m = [k for k in content if k.rsplit(":", 1)[0] == prefix]
            if not m:
                continue
            t = live.get(m[0])
            if not t:
                missing.append(prefix.split(".")[-1])
            elif t["outdated"]:
                stale.append(prefix.split(".")[-1])
        flag = "ok" if not missing and not stale else "FAIL"
        if flag == "FAIL":
            ok = False
        print(f"  {locale}: {flag}"
              + (f"  missing={missing}" if missing else "")
              + (f"  outdated={stale}" if stale else ""))
    print("\nAll locales verified." if ok else "\nSOME LOCALES INCOMPLETE — see above.")


if __name__ == "__main__":
    main()
