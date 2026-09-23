#!/usr/bin/env python3
"""Credit a medical reviewer on the science pages — visible byline + JSON-LD, all six languages. --remove undoes it.

Author: Claude (Opus 5) for Malcolm Smith · 2026-09-22
Purpose: Malcolm, 2026-09-22: "Lets already add Esther Bodde as verified. I will check with her." The credit
goes live before she has read the pages, so taking it off again has to be one command.

    python3 scripts/set-reviewer.py configs/reviewers/esther-bodde.json                  # dry run
    python3 scripts/set-reviewer.py configs/reviewers/esther-bodde.json --apply
    python3 scripts/set-reviewer.py configs/reviewers/esther-bodde.json --remove --apply  # take it off everywhere

What it edits, per the reviewer config:
  hubs     the dated italic byline paragraph (<p><em>… Last updated …</em></p>) in the hub template, English and
           the five translations, plus reviewedBy/lastReviewed in the page's WebPage JSON-LD (inside the
           references custom-html; per-locale copies too where that block is translated). The hub SPEC file is
           updated to match, so a later `hub-upgrade.py --apply` keeps the credit instead of silently dropping it.
  studies  the Evidence Library config files (configs/studies/*.json): the "*Appraised by … Last reviewed …*"
           intro line in six languages and the WebPage JSON-LD, then republished with scripts/study-pages.py.

Rules:
  * Idempotent: a value already naming the reviewer is left alone. --remove deletes only the reviewer sentence
    and reviewedBy; the author sentence and lastReviewed (our own review date) stay.
  * The reviewer sentence goes straight after the author sentence ("By Skingenetix."). A byline with no author
    sentence gets one: the external audit scores author and reviewer as separate signals.
  * A locale whose byline cannot be found fails the run: no page may credit the reviewer in some languages only.
  * The previous English values and translations are backed up to backups/ before anything is written.
"""
import argparse, datetime as dt, importlib.util, json, pathlib, re, subprocess, sys, time

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOCALES = ["de", "nl", "fr", "es", "it"]
TAG = '<script type="application/ld+json" id="sgx-webpage-jsonld">'


# ---------- pure edits (tested offline in tests/test_set_reviewer.py) ----------

def _html(s):
    return s.replace("&", "&amp;")


def add_to_byline(value, loc, cfg):
    """Insert the reviewer sentence into the last dated <p><em> byline. None if there is no such byline."""
    if cfg["marker"] in value:
        return value
    pat = re.compile(r"<p><em>((?:(?!</p>).)*?(?:%s)(?:(?!</p>).)*?)</em></p>" % cfg["date_marker"][loc], re.S)
    found = list(pat.finditer(value))
    if not found:
        return None
    m = found[-1]
    inner, author, sentence = m.group(1), cfg["author"][loc], _html(cfg["sentence"][loc])
    if inner.startswith(author):
        new = author + " " + sentence + inner[len(author):]
    else:
        new = author + " " + sentence + " " + inner
    return value[:m.start(1)] + new + value[m.end(1):]


def remove_from_byline(value, loc, cfg):
    for s in (_html(cfg["sentence"][loc]), cfg["sentence"][loc]):
        value = value.replace(" " + s, "")
    return value


def jsonld_edit(html, cfg, add=True):
    """Add (or remove) reviewedBy/lastReviewed on the WebPage JSON-LD inside a custom-html value. None if absent."""
    m = re.search(re.escape(TAG) + r"(.*?)</script>", html, re.S)
    if not m:
        return None
    ld = json.loads(m.group(1))
    if add:
        ld["reviewedBy"] = cfg["person"]
        ld["lastReviewed"] = cfg["reviewed"]
    else:
        ld.pop("reviewedBy", None)
    block = TAG + "\n" + json.dumps(ld, indent=2, ensure_ascii=False) + "\n</script>"
    return html[:m.start()] + block + html[m.end():]


def add_to_study_markup(text, loc, cfg):
    """'*Appraised by … team. Last reviewed …*' → the reviewer sentence after the first sentence."""
    if cfg["marker"] in text:
        return text
    m = re.match(r"(\*[^*]*?\.) ", text)
    if not m:
        return None
    return text[:m.end(1)] + " " + cfg["sentence"][loc] + text[m.end(1):]


def remove_from_study_markup(text, loc, cfg):
    return text.replace(" " + cfg["sentence"][loc], "")


# ---------- Shopify side ----------

def _hub():
    s = importlib.util.spec_from_file_location("hu", ROOT / "scripts/hub-upgrade.py")
    m = importlib.util.module_from_spec(s)
    argv, sys.argv = sys.argv, [sys.argv[0]]
    s.loader.exec_module(m)
    sys.argv = argv
    return m


def template_rid(template):
    name = template.split("templates/", 1)[1].rsplit(".json", 1)[0]
    return f"gid://shopify/OnlineStoreThemeJsonTemplate/{name}?theme_id=184835965313"


def translations(hu, template):
    prefix = f"section.{template.split('templates/', 1)[1]}."
    q = "query($id:ID!){ translatableResource(resourceId:$id){ " + " ".join(
        f'{l}:translations(locale:"{l}"){{ key value outdated }}' for l in LOCALES) + " } }"
    r = hu.gql(q, {"id": template_rid(template)})["translatableResource"]
    # An OUTDATED translation is still served, but it belongs to an older English value (the nl references block
    # on three hubs, found 2026-09-22). Re-registering an edited copy would certify stale content as current,
    # so it is left out here and reported; the fix is a fresh translation of the current value.
    out = {l: {x["key"].split(":")[0][len(prefix):]: x["value"] for x in r[l]
               if x["key"].startswith(prefix) and not x["outdated"]} for l in LOCALES}
    stale = {l: [x["key"].split(":")[0][len(prefix):] for x in r[l] if x["key"].startswith(prefix) and x["outdated"]]
             for l in LOCALES}
    return out, {l: v for l, v in stale.items() if v}


def register(hu, template, key, values):
    """Register the given locales against the digest of the English value just uploaded."""
    rid, prefix = template_rid(template), f"section.{template.split('templates/', 1)[1]}."
    for _ in range(8):
        tc = hu.gql('query($id:ID!){ translatableResource(resourceId:$id){ translatableContent{ key value digest } } }',
                    {"id": rid})["translatableResource"]["translatableContent"]
        c = next((c for c in tc if c["key"].split(":")[0] == prefix + key), None)
        if c and c["value"] == values["en"]:
            break
        time.sleep(5)
    else:
        raise RuntimeError(f"{template} {key}: the English value did not reach the translatable index")
    locs = [l for l in LOCALES if l in values]
    r = hu.gql('mutation($id:ID!,$t:[TranslationInput!]!){ translationsRegister(resourceId:$id, translations:$t)'
               '{ userErrors{field message} } }',
               {"id": rid, "t": [{"locale": l, "key": c["key"], "value": values[l],
                                  "translatableContentDigest": c["digest"]} for l in locs]})
    if r["translationsRegister"]["userErrors"]:
        raise RuntimeError(r["translationsRegister"]["userErrors"])
    return locs


def hub_cfg(cfg, hub):
    """A hub rebuilt after the credit was first given carries its own review date (schema.org lastReviewed is
    the date the page's content was last checked): the glutathione hub was rebuilt on 2026-09-23 while the
    other four were reviewed on 2026-09-22, and one config-wide date left the visible byline and the JSON-LD
    disagreeing on that page."""
    return {**cfg, "reviewed": hub.get("reviewed", cfg["reviewed"])}


def sync_spec(spec, byline_key, edit, cfg, add):
    """Keep the hub spec (source of truth) in step with the live page."""
    at = byline_key.replace(".", "/")
    item = next((i for i in spec.get("set", []) if i["at"] == at), None)
    missing = []
    if item:
        for loc, v in item["values"].items():
            nv = edit(v, loc, cfg)
            if nv is None:
                missing.append(loc)
            else:
                item["values"][loc] = nv
    if spec.get("jsonld"):
        if add:
            spec["jsonld"]["reviewedBy"] = cfg["person"]
            spec["jsonld"]["lastReviewed"] = cfg["reviewed"]
        else:
            spec["jsonld"].pop("reviewedBy", None)
    return "no overview item in spec" if not item else (f"byline not in spec for {missing}" if missing else "synced")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--remove", action="store_true")
    a = ap.parse_args()
    cfg = json.loads(pathlib.Path(a.config).read_text())
    add = not a.remove
    edit = add_to_byline if add else (lambda v, loc, c: remove_from_byline(v, loc, c))
    hu = _hub()
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    failed = False

    for h in cfg["hubs"]:
        spec_path = ROOT / h["spec"]
        spec = json.loads(spec_path.read_text())
        template = spec["template"]
        hdr, j = hu.split(hu.read_file(template))
        sec, blk, key = h["byline"].split(".")
        hcfg = hub_cfg(cfg, h)
        settings = j["sections"][sec]["blocks"][blk]["settings"]
        tr, stale = translations(hu, template)
        if stale:
            print(f"  ⚠ {spec['page']}: outdated translations left untouched (still served, need a fresh translation): {stale}")
        values = {"en": edit(settings[key], "en", cfg)}
        for loc in LOCALES:
            old = tr[loc].get(h["byline"])
            values[loc] = edit(old, loc, cfg) if old else None
        bad = [l for l, v in values.items() if v is None]
        host = h["jsonld_host"]
        host_html = j["sections"][host]["settings"]["html"]
        host_values = {"en": jsonld_edit(host_html, hcfg, add)}
        for loc in LOCALES:
            if tr[loc].get(f"{host}.html"):
                host_values[loc] = jsonld_edit(tr[loc][f"{host}.html"], hcfg, add)
        print(f"  {spec['page']:<34} byline {'✗ not found in ' + str(bad) if bad else '✓ 6 languages'}"
              f" · JSON-LD {'✓' if host_values['en'] else '✗ none'} (translated copies: {len(host_values) - 1})")
        if bad or not host_values["en"]:
            failed = True
            continue
        if not a.apply:
            print("      " + re.sub(r"<[^>]+>", "", re.findall(r"<p><em>.*?</em></p>", values["en"])[-1])[:170])
            continue
        (ROOT / f"backups/reviewer-{spec['page']}-{stamp}.json").write_text(json.dumps(
            {"en": {h["byline"]: settings[key], f"{host}.html": host_html}, **tr}, ensure_ascii=False, indent=1))
        settings[key] = values["en"]
        j["sections"][host]["settings"]["html"] = host_values["en"]
        hu.upload(template, hdr, j)
        done = register(hu, template, h["byline"], values)
        extra = register(hu, template, f"{host}.html", host_values) if len(host_values) > 1 else []
        state = sync_spec(spec, h["byline"], edit, hcfg, add)
        spec_path.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n")
        print(f"      ✓ live: byline en + {len(done)} translations, JSON-LD en + {len(extra)} · spec {state}")

    sedit = add_to_study_markup if add else remove_from_study_markup
    for path in cfg.get("studies", []):
        p = ROOT / path
        c = json.loads(p.read_text())
        bad = []
        for loc, blocks in c["fields"]["intro"].items():
            hit = next((b for b in blocks if b[0] == "p" and re.search(cfg["date_marker"][loc], b[1])), None)
            nv = sedit(hit[1], loc, cfg) if hit else None
            if nv is None:
                bad.append(loc)
            else:
                hit[1] = nv
        if add:
            c["jsonld"]["reviewedBy"] = cfg["person"]
            c["jsonld"]["lastReviewed"] = cfg["reviewed"]
        else:
            c["jsonld"].pop("reviewedBy", None)
        print(f"  study {c['handle']:<52} intro {'✗ not found in ' + str(bad) if bad else '✓ 6 languages'} · JSON-LD ✓")
        if bad:
            failed = True
            continue
        if a.apply:
            (ROOT / f"backups/reviewer-study-{c['handle']}-{stamp}.json").write_text(p.read_text())
            p.write_text(json.dumps(c, indent=2, ensure_ascii=False) + "\n")
            r = subprocess.run([sys.executable, str(ROOT / "scripts/study-pages.py"), str(p), "--apply"],
                               capture_output=True, text=True)
            print("      " + (r.stdout.strip().splitlines() or ["(no output)"])[-1][:160])
            if r.returncode:
                print(r.stderr[-800:])
                failed = True

    if not a.apply:
        print("  dry run — nothing written.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
