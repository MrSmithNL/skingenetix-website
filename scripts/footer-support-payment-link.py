#!/usr/bin/env python3
"""Add a "Payment" link to the footer's Support menu, pointing at the FAQ's payment answers, in six languages.

Author: Claude (Opus 5.5) for Malcolm Smith · 2026-09-30
Why: the central audit (2026-09-30, R6, confirmed by all four judges) found no payment help reachable from any page.
Malcolm approved the payment Q&As (configs/hub-upgrades/faq-payment-2026-09-30.json) and this footer link.

    python3 scripts/footer-support-payment-link.py            # dry run
    python3 scripts/footer-support-payment-link.py --apply
    python3 scripts/footer-support-payment-link.py --rollback  # restore the snapshot in backups/

How: menuUpdate replaces the whole tree, so the existing items are sent back WITH their ids (their translations are
keyed to them and survive), and the snapshot goes to backups/ first. The link is a PAGE link to /pages/faq, not an
HTTP link with a #fragment: a literal URL is not localised and drops readers into English (memory: literal URL
settings drop readers into English), and the FAQ's section ids carry a template-scoped prefix that changes if the
template is rebuilt. The new item's title is translated in the same run.
"""
import argparse, datetime as dt, importlib.util, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
_s = importlib.util.spec_from_file_location("hu", ROOT / "scripts/hub-upgrade.py")
hu = importlib.util.module_from_spec(_s)
_argv, sys.argv = sys.argv, [sys.argv[0]]
_s.loader.exec_module(hu)
sys.argv = _argv

HANDLE = "footer-support"
AFTER = "/pages/shipping-returns"
TITLE = {"en": "Payment", "de": "Zahlung", "nl": "Betalen", "fr": "Paiement", "es": "Pago", "it": "Pagamento"}


def read_menu():
    ms = hu.gql('{ menus(first:30){ nodes{ id handle title items{ id title type url resourceId tags } } } }')["menus"]["nodes"]
    return next(m for m in ms if m["handle"] == HANDLE)


def item_input(i):
    out = {"id": i["id"], "title": i["title"], "type": i["type"], "items": []}
    if i.get("resourceId"):
        out["resourceId"] = i["resourceId"]
    else:
        out["url"] = i["url"]
    if i.get("tags"):
        out["tags"] = i["tags"]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--rollback", action="store_true")
    a = ap.parse_args()
    menu = read_menu()
    if a.rollback:
        snaps = sorted((ROOT / "backups").glob(f"menu-{HANDLE}-*.json"))
        if not snaps:
            sys.exit("  no snapshot")
        snap = json.loads(snaps[-1].read_text())
        r = hu.gql('mutation($id:ID!,$t:String!,$h:String!,$i:[MenuItemUpdateInput!]!){ menuUpdate(id:$id, title:$t, handle:$h, items:$i)'
                   '{ userErrors{ field message } } }', {"id": menu["id"], "t": snap["title"], "h": HANDLE,
                                                        "i": [item_input(i) for i in snap["items"]]})
        print("  restored from", snaps[-1].name, r["menuUpdate"]["userErrors"] or "ok")
        return 0
    if any(i["title"] == TITLE["en"] for i in menu["items"]):
        print("  a Payment item is already there, nothing to do:", [i["title"] for i in menu["items"]])
        return 0
    faq = next(i for i in menu["items"] if i["url"].endswith("/pages/faq"))
    items = [item_input(i) for i in menu["items"]]
    at = next(n for n, i in enumerate(menu["items"]) if i["url"].endswith(AFTER)) + 1
    items.insert(at, {"title": TITLE["en"], "type": "PAGE", "resourceId": faq["resourceId"], "items": []})
    print("  before:", [i["title"] for i in menu["items"]])
    print("  after :", [i["title"] for i in items])
    if not a.apply:
        print("  dry run, nothing written")
        return 0
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    (ROOT / f"backups/menu-{HANDLE}-{stamp}.json").write_text(json.dumps(menu, indent=1, ensure_ascii=False))
    r = hu.gql('mutation($id:ID!,$t:String!,$h:String!,$i:[MenuItemUpdateInput!]!){ menuUpdate(id:$id, title:$t, handle:$h, items:$i)'
               '{ menu{ items{ id title } } userErrors{ field message } } }',
               {"id": menu["id"], "t": menu["title"], "h": HANDLE, "i": items})["menuUpdate"]
    if r["userErrors"]:
        sys.exit(f"  ✗ menuUpdate: {r['userErrors']}")
    new = next(i for i in r["menu"]["items"] if i["title"] == TITLE["en"])
    rid = new["id"].replace("MenuItem", "Link")
    tc = hu.gql('query($id:ID!){ translatableResource(resourceId:$id){ translatableContent{ key digest } } }',
                {"id": rid})["translatableResource"]["translatableContent"]
    dig = next(c["digest"] for c in tc if c["key"] == "title")
    t = [{"locale": l, "key": "title", "value": v, "translatableContentDigest": dig} for l, v in TITLE.items() if l != "en"]
    e = hu.gql('mutation($id:ID!,$t:[TranslationInput!]!){ translationsRegister(resourceId:$id, translations:$t)'
               '{ userErrors{ message } } }', {"id": rid, "t": t})["translationsRegister"]["userErrors"]
    print(f"  ✓ added {new['id']} (backup menu-{HANDLE}-{stamp}.json); translations: {e or '5 locales ok'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
