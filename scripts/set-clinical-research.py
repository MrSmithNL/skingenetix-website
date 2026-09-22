#!/usr/bin/env python3
"""Write the product 'Clinical Research' block from per-ingredient claim kits — English + five translations.

Author: Claude (Opus 5) for Malcolm Smith · 2026-09-22
Purpose: lead every product's clinical block with the strongest verified claim for its ingredient(s)
(docs/claims/), worded for conversion, with the binding study conditions in a footnote line.

    python3 scripts/set-clinical-research.py configs/copy/clinical-research-2026-09-22.json            # dry run
    python3 scripts/set-clinical-research.py configs/copy/clinical-research-2026-09-22.json --apply
    python3 scripts/set-clinical-research.py configs/copy/clinical-research-2026-09-22.json --rollback

Block shape (the existing custom.clinical_research rich_text_field): per kit — bold headline paragraph, intro
paragraph, bulleted list (bold items), italic footnote paragraph, link paragraph to the ingredient hub. A
product with two kits (e.g. the PDRN + copper bundles) gets both, in order. Hub links in a translation carry
the locale prefix. Previous English values and all translations are backed up first.
"""
import argparse, datetime as dt, glob, importlib.util, json, pathlib, sys, time

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOCALES = ["de", "nl", "fr", "es", "it"]
_s = importlib.util.spec_from_file_location("hu", ROOT / "scripts/hub-upgrade.py")
hu = importlib.util.module_from_spec(_s)
_argv, sys.argv = sys.argv, [sys.argv[0]]
_s.loader.exec_module(hu)
sys.argv = _argv
gql = hu.gql


def text(v, **fmt):
    return {"type": "text", "value": v, **fmt}


def block(cfg, kits, loc):
    children = []
    for k in kits:
        kit, c = cfg["kits"][k], cfg["kits"][k][loc]
        url = kit["hub"] if loc == "en" else f"/{loc}{kit['hub']}"
        children += [
            {"type": "paragraph", "children": [text(c["headline"], bold=True)]},
            {"type": "paragraph", "children": [text(c["intro"])]},
            {"type": "list", "listType": "unordered",
             "children": [{"type": "list-item", "children": [text(b, bold=True)]} for b in c["bullets"]]},
            {"type": "paragraph", "children": [text(c["footnote"], italic=True)]},
            {"type": "paragraph", "children": [{"type": "link", "url": url, "children": [text(c["link"] + " →")]}]},
        ]
    return json.dumps({"type": "root", "children": children}, ensure_ascii=False, separators=(",", ":"))


def products(handles):
    out = {}
    for h in handles:
        n = gql('query($q:String!){ products(first:1, query:$q){ nodes{ id handle metafield(namespace:"custom", key:"clinical_research"){ id value } } } }',
                {"q": f"handle:{h}"})["products"]["nodes"]
        if not n or n[0]["handle"] != h:
            sys.exit(f"  ✗ product not found: {h}")
        out[h] = n[0]
    return out


def translations(rid):
    out = {}
    for l in LOCALES:
        tr = gql('query($id:ID!,$l:String!){ translatableResource(resourceId:$id){ translations(locale:$l){ key value } } }',
                 {"id": rid, "l": l})["translatableResource"]["translations"]
        out[l] = next((t["value"] for t in tr if t["key"] == "value"), None)
    return out


def write(pid, mf_id, values):
    r = gql('mutation($m:[MetafieldsSetInput!]!){ metafieldsSet(metafields:$m){ metafields{ id } userErrors{ message } } }',
            {"m": [{"ownerId": pid, "namespace": "custom", "key": "clinical_research", "type": "rich_text_field",
                    "value": values["en"]}]})["metafieldsSet"]
    if r["userErrors"]:
        raise RuntimeError(r["userErrors"])
    rid = r["metafields"][0]["id"]
    for _ in range(8):
        c = next(x for x in gql('query($id:ID!){ translatableResource(resourceId:$id){ translatableContent{ key value digest } } }',
                                {"id": rid})["translatableResource"]["translatableContent"] if x["key"] == "value")
        if c["value"] == values["en"]:
            break
        time.sleep(3)
    t = [{"locale": l, "key": "value", "value": values[l], "translatableContentDigest": c["digest"]} for l in LOCALES if values.get(l)]
    r = gql('mutation($id:ID!,$t:[TranslationInput!]!){ translationsRegister(resourceId:$id, translations:$t){ userErrors{ message } } }',
            {"id": rid, "t": t})["translationsRegister"]
    if r["userErrors"]:
        raise RuntimeError(r["userErrors"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--rollback", action="store_true")
    a = ap.parse_args()
    cfg = json.loads(pathlib.Path(a.config).read_text())
    tag = pathlib.Path(a.config).stem
    ps = products(cfg["products"])
    if a.rollback:
        bk = json.loads(pathlib.Path(sorted(glob.glob(str(ROOT / f"backups/clinical-{tag}-*.json")))[-1]).read_text())
        for h, v in bk.items():
            write(ps[h]["id"], None, v)
            print(f"  restored {h}")
        return 0
    plan = {h: {l: block(cfg, kits, l) for l in ["en"] + LOCALES} for h, kits in cfg["products"].items()}
    for h, v in plan.items():
        print(f"  {h[:60]:<61} kits={cfg['products'][h]}  {len(v['en'])} chars")
    if not a.apply:
        print("  dry run — nothing written. Sample (en, first product):")
        print("  " + plan[next(iter(plan))]["en"][:400])
        return 0
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = {}
    for h, p in ps.items():
        mf = p["metafield"]
        backup[h] = {"en": mf["value"] if mf else None, **(translations(mf["id"]) if mf else {})}
    (ROOT / f"backups/clinical-{tag}-{stamp}.json").write_text(json.dumps(backup, ensure_ascii=False, indent=1))
    for h, v in plan.items():
        write(ps[h]["id"], None, v)
        print(f"  ✓ {h[:60]:<61} English + 5 translations")
    print(f"  backup {stamp}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
