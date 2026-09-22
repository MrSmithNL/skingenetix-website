#!/usr/bin/env python3
"""Replace an unsupported claim everywhere it lives on the store — English and all five translations at once.

Author: Claude (Opus 5) for Malcolm Smith · 2026-09-22
Purpose: a claim that fails verification at source is rarely in one place. The copper "most-studied peptide"
line was in product descriptions, the clinical-research product metafield, a product FAQ metaobject and
five page templates, worded differently per product and per language.

    python3 scripts/fix-claims.py configs/claim-fixes/<spec>.json            # dry run
    python3 scripts/fix-claims.py configs/claim-fixes/<spec>.json --apply
    python3 scripts/fix-claims.py configs/claim-fixes/<spec>.json --rollback

Spec: {"fixes": [{"where": [...], "patterns": {"en": regex, "de": ..., ...}, "replace": {"en": text, ...}}]}
  where — any of: "body_html"                 product descriptions
                  "metafield:custom.<key>"    a product rich-text metafield
                  "metaobject:<type>.<field>" e.g. "metaobject:faq_item.answer"
                  "templates"                 every string setting in templates/*.json of the live theme
Every English value matching `patterns.en` is changed. The dry run FAILS if any existing translation of a
changed value does not match its locale pattern — no language may be left serving the old claim.

Why it works this way:
  * A changed English value with no re-registered translation leaves each locale serving its OLD text
    (marked outdated) — i.e. the very claim being removed. Translations are registered against the digest
    of the value just written, as in hub-upgrade.py.
  * Rich-text metafields and templates are JSON; replacement text must not contain double quotes.
  * Templates are edited as parsed JSON, string by string — never as raw text — and backed up first.
"""
import argparse, datetime as dt, glob, importlib.util, json, pathlib, re, sys, time

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOCALES = ["de", "nl", "fr", "es", "it"]
_s = importlib.util.spec_from_file_location("hu", ROOT / "scripts/hub-upgrade.py")
hu = importlib.util.module_from_spec(_s)
_argv, sys.argv = sys.argv, [sys.argv[0]]
_s.loader.exec_module(hu)
sys.argv = _argv
gql, THEME = hu.gql, hu.THEME


# ---------- discovery: every (resource, translatable key, English value) in scope ----------

def targets(where):
    if where == "body_html":
        for p in gql('{ products(first:100){ nodes{ id handle descriptionHtml } } }')["products"]["nodes"]:
            yield {"kind": "product", "label": p["handle"], "rid": p["id"], "key": "body_html",
                   "owner": p["id"], "en": p["descriptionHtml"]}
    elif where.startswith("metafield:"):
        ns, key = where.split(":", 1)[1].split(".")
        q = '{ products(first:100){ nodes{ id handle metafield(namespace:"%s", key:"%s"){ id type value } } } }' % (ns, key)
        for p in gql(q)["products"]["nodes"]:
            mf = p.get("metafield")
            if mf:
                yield {"kind": "metafield", "label": f"{p['handle']} {ns}.{key}", "rid": mf["id"], "key": "value",
                       "owner": p["id"], "ns": ns, "mkey": key, "type": mf["type"], "en": mf["value"]}
    elif where.startswith("metaobject:"):
        typ, field = where.split(":", 1)[1].split(".")
        for m in gql('query($t:String!){ metaobjects(type:$t, first:250){ nodes{ id handle fields{ key value } } } }',
                     {"t": typ})["metaobjects"]["nodes"]:
            v = next((f["value"] for f in m["fields"] if f["key"] == field), None)
            if v:
                yield {"kind": "metaobject", "label": f"{typ}/{m['handle']}", "rid": m["id"], "key": field,
                       "owner": m["id"], "en": v}
    elif where == "templates":
        tid = THEME.rsplit("/", 1)[1]
        files = gql('query($id:ID!){ theme(id:$id){ files(first:250, filenames:["templates/*.json"]){ nodes{ filename } } } }',
                    {"id": THEME})["theme"]["files"]["nodes"]
        for f in files:
            name = f["filename"]
            rid = f"gid://shopify/OnlineStoreThemeJsonTemplate/{name[len('templates/'):-len('.json')]}?theme_id={tid}"
            try:
                tc = gql('query($id:ID!){ translatableResource(resourceId:$id){ translatableContent{ key value } } }',
                         {"id": rid})["translatableResource"]["translatableContent"]
            except Exception:
                continue
            for c in tc:
                yield {"kind": "template", "label": f"{name} {c['key'].split(':')[0].split('.json.')[-1]}",
                       "rid": rid, "key": c["key"], "file": name, "en": c["value"]}
    else:
        sys.exit(f"  unknown `where`: {where}")


def translations(rid, key):
    out = {}
    for loc in LOCALES:
        tr = gql('query($id:ID!,$l:String!){ translatableResource(resourceId:$id){ translations(locale:$l){ key value } } }',
                 {"id": rid, "l": loc})["translatableResource"]["translations"]
        out[loc] = next((t["value"] for t in tr if t["key"] == key), None)
    return out


def plan(spec):
    items = {}
    for fx in spec["fixes"]:
        for where in fx["where"]:
            for t in targets(where):
                if not t["en"] or not re.search(fx["patterns"]["en"], t["en"]):
                    continue
                uid = (t["rid"], t["key"])
                it = items.get(uid)
                if not it:
                    it = items[uid] = {**t, "old": {"en": t["en"], **translations(t["rid"], t["key"])}, "problems": []}
                    it["new"] = dict(it["old"])
                it["new"]["en"] = re.sub(fx["patterns"]["en"], fx["replace"]["en"], it["new"]["en"])
                for loc in LOCALES:
                    if it["old"][loc] is None:
                        continue
                    nv, k = re.subn(fx["patterns"][loc], fx["replace"][loc], it["new"][loc])
                    if not k:
                        it["problems"].append(f"{loc}: pattern not found")
                    it["new"][loc] = nv
    return list(items.values())


# ---------- writing English ----------

def write_template(name, changes):
    """changes: {old English string: new English string}; applied to every matching string in the JSON."""
    hdr, j = hu.split(hu.read_file(name))
    hit = 0

    def walk(x):
        nonlocal hit
        if isinstance(x, dict):
            return {k: walk(v) for k, v in x.items()}
        if isinstance(x, list):
            return [walk(v) for v in x]
        if isinstance(x, str) and x in changes:
            hit += 1
            return changes[x]
        return x
    j = walk(j)
    if hit < len(changes):
        raise RuntimeError(f"{name}: only {hit} of {len(changes)} strings found in the file")
    hu.upload(name, hdr, j)


def write_en(it):
    v = it["new"]["en"]
    if it["kind"] == "product":
        r = gql('mutation($p:ProductUpdateInput!){ productUpdate(product:$p){ userErrors{ field message } } }',
                {"p": {"id": it["owner"], "descriptionHtml": v}})["productUpdate"]
    elif it["kind"] == "metafield":
        r = gql('mutation($m:[MetafieldsSetInput!]!){ metafieldsSet(metafields:$m){ userErrors{ field message } } }',
                {"m": [{"ownerId": it["owner"], "namespace": it["ns"], "key": it["mkey"], "type": it["type"],
                        "value": v}]})["metafieldsSet"]
    elif it["kind"] == "metaobject":
        r = gql('mutation($id:ID!,$m:MetaobjectUpdateInput!){ metaobjectUpdate(id:$id, metaobject:$m){ userErrors{ field message } } }',
                {"id": it["owner"], "m": {"fields": [{"key": it["key"], "value": v}]}})["metaobjectUpdate"]
    else:
        raise ValueError(it["kind"])
    if r["userErrors"]:
        raise RuntimeError(r["userErrors"])


def register(it, values):
    """Register translations against the digest of the English value now live. Template keys carry a hash
    suffix that changes with the value, so they are matched on the part before the colon."""
    base = it["key"].split(":")[0]
    for attempt in range(8):
        tc = gql('query($id:ID!){ translatableResource(resourceId:$id){ translatableContent{ key value digest } } }',
                 {"id": it["rid"]})["translatableResource"]["translatableContent"]
        c = next((x for x in tc if x["key"].split(":")[0] == base and x["value"] == values["en"]), None)
        if c:
            break
        time.sleep(4)
    else:
        raise RuntimeError(f"{it['label']}: translatable value never matched the upload")
    t = [{"locale": l, "key": c["key"], "value": values[l], "translatableContentDigest": c["digest"]}
         for l in LOCALES if values.get(l)]
    if t:
        r = gql('mutation($id:ID!,$t:[TranslationInput!]!){ translationsRegister(resourceId:$id, translations:$t)'
                '{ userErrors{ field message } } }', {"id": it["rid"], "t": t})["translationsRegister"]
        if r["userErrors"]:
            raise RuntimeError(r["userErrors"])
    return len(t)


def apply(items, values_key):
    by_file = {}
    for it in items:
        if it["kind"] == "template":
            by_file.setdefault(it["file"], []).append(it)
        else:
            it2 = {**it, "new": it[values_key]}
            write_en(it2)
    for name, its in by_file.items():
        write_template(name, {i["old" if values_key == "new" else "new"]["en"]: i[values_key]["en"] for i in its})
    for it in items:
        n = register(it, it[values_key])
        print(f"  ✓ {it['label'][:70]:<71} English + {n} translations")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--rollback", action="store_true")
    a = ap.parse_args()
    spec = json.loads(pathlib.Path(a.spec).read_text())
    tag = pathlib.Path(a.spec).stem

    if a.rollback:
        bk = sorted(glob.glob(str(ROOT / f"backups/claim-fix-{tag}-*.json")))
        if not bk:
            sys.exit("  no backup")
        items = json.loads(pathlib.Path(bk[-1]).read_text())
        for it in items:                      # backups written by the first, product-only version
            if "field" in it and "kind" not in it:
                prod = it["field"] == "body_html"
                it.update({"kind": "product" if prod else "metafield", "owner": it["product_id"], "label": it["handle"],
                           "ns": "custom", "mkey": "clinical_research", "type": "rich_text_field"})
        apply(items, "old")
        print(f"  restored from {pathlib.Path(bk[-1]).name}")
        return 0

    items = plan(spec)
    bad = 0
    for it in items:
        print(f"  {it['label'][:70]:<71} "
              f"{'✗ ' + '; '.join(it['problems']) if it['problems'] else str(1 + sum(1 for l in LOCALES if it['old'][l])) + ' languages ✓'}")
        bad += bool(it["problems"])
    print(f"  {len(items)} values to change")
    if bad:
        sys.exit(f"  ✗ {bad} value(s) would leave a language serving the old claim — fix the spec patterns first")
    if not a.apply or not items:
        return 0

    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    (ROOT / f"backups/claim-fix-{tag}-{stamp}.json").write_text(json.dumps(items, ensure_ascii=False, indent=1))
    apply(items, "new")

    # read back: English everywhere, and every translation of every changed value
    left = [f"{i['label']} en" for i in plan(spec)]
    for it in items:
        now = gql('query($id:ID!){ translatableResource(resourceId:$id){ translatableContent{ key value } } }',
                  {"id": it["rid"]})["translatableResource"]["translatableContent"]
        key = next((c["key"] for c in now if c["key"].split(":")[0] == it["key"].split(":")[0]), it["key"])
        for loc, val in translations(it["rid"], key).items():
            if val and any(re.search(fx["patterns"][loc], val) for fx in spec["fixes"]):
                left.append(f"{it['label']} {loc}")
    for x in left:
        print(f"  ✗ still carries the claim: {x}")
    print(f"  backup {stamp} · read-back {'clean in all six languages' if not left else f'{len(left)} still carry it'}")
    return 1 if left else 0


if __name__ == "__main__":
    sys.exit(main())
