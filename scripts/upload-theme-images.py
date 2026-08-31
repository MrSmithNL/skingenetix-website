#!/usr/bin/env python3
"""Upload chosen banner images to Shopify Files so the theme can reference them.

    python3 scripts/upload-theme-images.py configs/banners/homepage-publish.json

Theme sections reference imagery as `shopify://shop_images/<filename>`, which resolves
against Content > Files — NOT against product media. So this uses the Files API
(stagedUploadsCreate -> POST -> fileCreate) rather than the productCreateMedia path
that scripts/finals/shopify-*-media.py use.

New filenames only. Per .claude/rules/shopify.md rule 7 an existing image is never
renamed or re-uploaded, because Langify keys translations off the URL; these are
additional files and the originals are left untouched.

Writes the resolved shopify:// handles back into the plan file so the patch step
cannot guess a filename Shopify silently sanitised.

Author: Claude Code, 2026-08-21.
"""
import json
import mimetypes
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "2025-01"


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


def gql(store, tok, query, variables=None):
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(f"https://{store}/admin/api/{API}/graphql.json", data=body,
                                 headers={"X-Shopify-Access-Token": tok,
                                          "Content-Type": "application/json"})
    res = json.loads(urllib.request.urlopen(req, timeout=120).read())
    if res.get("errors"):
        raise RuntimeError(res["errors"])
    return res["data"]


STAGED = """
mutation($input:[StagedUploadInput!]!){
  stagedUploadsCreate(input:$input){
    stagedTargets{ url resourceUrl parameters{ name value } }
    userErrors{ field message }
  }
}"""

CREATE = """
mutation($files:[FileCreateInput!]!){
  fileCreate(files:$files){
    files{ id fileStatus alt ... on MediaImage { image { url } } }
    userErrors{ field message }
  }
}"""

POLL = """
query($q:String!){
  files(first:20, query:$q){
    edges{ node{ id fileStatus alt ... on MediaImage { image { url } } } }
  }
}"""


#: Malcolm's standing instruction, 2026-08-24: every image uploaded to the site is
#: optimised for fast loading and carries an SEO filename. Doing that by hand is
#: something a session forgets, so it happens here, in the one place every theme
#: image passes through.
#:
#: DO NOT "OPTIMISE" BY COMPRESSING THE SOURCE. That was tried here on 2026-08-24 and
#: it made the site SLOWER. Shopify's CDN transcodes every image to WebP and resizes it
#: per srcset, so the source JPEG is never what a visitor downloads. Re-encoding it at
#: q85 first simply hands the WebP encoder a picture full of JPEG artefacts, and those
#: artefacts cost bits to reproduce. Same photograph, measured off the live CDN:
#:
#:     source q93 ->  45,490B at w1000 |  83,478B at w1500 | 247,444B at w3000
#:     source q85 ->  45,746B at w1000 |  85,102B at w1500 | 255,844B at w3000
#:
#: Whole-page image weight over the same change: 974KB before, 979KB after. The
#: "41% smaller file" was real and bought nothing, because it was 41% off a number
#: no visitor ever downloads.
#:
#: So what is left here is only what genuinely helps: cap the long edge at the widest
#: size the theme ever requests, strip metadata, and keep the quality high so the CDN
#: gets a clean picture to encode from.
#:
#: The real page-weight levers are in the THEME, not in these files: the hero is the
#: LCP element and carries no fetchpriority="high", and the largest single image on the
#: homepage is a 163KB review-section file, not a hero.
WEB_MAX_EDGE = 3000        # the theme's srcset tops out at 3000w; larger is dead weight
WEB_QUALITY = 95           # high on purpose - the CDN, not this script, does the compressing

#: Words that carry no search value in a filename but keep appearing in them.
SEO_NOISE = {"final", "new", "copy", "image", "img", "photo", "untitled", "asset",
             "v1", "v2", "v3", "v4", "temp", "test"}

#: "A bare digit carries no search value" was too blunt, and on this brand it is
#: usually backwards. Digits here are nearly always the most searched part of the
#: name: MATRIXYL 3000, ACETYL HEXAPEPTIDE-8, a 3-bottle bundle, a 1-month set.
#: The noise this rule was written for is narrower than that - a revision or a
#: date - so it now flags only those.
#:
#: Caught twice on 2026-08-31, and the second time is the instructive one. The
#: first pass excused a digit when the NEXT word was counting something, which let
#: "3-bottle-bundle" through and still flagged "matrixyl-3000" and
#: "hexapeptide-8". Worse, that warning was printed during a 24-file upload and
#: went unread because the output was tailed - so the rule was quietly failing on
#: files that had already shipped.
#:
#: This matters more than tidiness. A warning left standing invites a later
#: session to "fix" a filename, and renaming is not free: Shopify SUFFIXES rather
#: than replaces on a name collision, so the rename lands a second file at a new
#: URL while everything pointing at the old one keeps serving the old one.
def _is_number_noise(word: str) -> bool:
    """True only for a year-like or revision-like numeral, not a naming one."""
    return word.isdigit() and len(word) == 4 and 1900 <= int(word) <= 2099


def optimise(src: Path, work: Path) -> Path:
    """Cap dimensions, force JPEG, strip metadata. Returns the path to upload.

    Deliberately does NOT compress - see the note above WEB_QUALITY.
    """
    from PIL import Image

    im = Image.open(src)
    w, h = im.size
    resized = max(w, h) > WEB_MAX_EDGE
    # A source that is already small enough and carries no metadata used to be returned
    # untouched — but that test was blind to the FORMAT, so a PNG straight out of a
    # generation run was uploaded as a PNG. It is not a cosmetic difference. Measured off
    # this store's own CDN on 2026-08-27, the same 2048px picture delivered at w1000:
    #
    #     PNG source  -> 166,464B WebP  ... and 1,591,711B of raw PNG to any client
    #                                       that does not send `Accept: image/webp`
    #     JPEG source ->  45,490B WebP  (the measured table above WEB_QUALITY)
    #
    # Roughly 3.7x the bytes for WebP clients and about 35x for everyone else, because
    # Shopify's WebP pass inherits losslessness from a lossless source. So format is now
    # part of what "web-ready" means, and a photograph is always re-encoded to JPEG.
    # Author: Claude Code, 2026-08-27.
    is_jpeg = (im.format or "").upper() in ("JPEG", "MPO")
    if resized:
        s = WEB_MAX_EDGE / max(w, h)
        im = im.resize((round(w * s), round(h * s)), Image.LANCZOS)
    elif is_jpeg and not (im.info.get("exif") or im.info.get("icc_profile")):
        print(f"    already web-ready: {w}x{h} JPEG, no metadata, left untouched")
        return src
    elif not is_jpeg:
        print(f"    {im.format} source at {w}x{h} — re-encoding to JPEG")
    work.parent.mkdir(parents=True, exist_ok=True)
    # 4:4:4 rather than 4:2:0: chroma subsampling throws away colour detail that the
    # CDN's WebP pass would otherwise have kept, and costs nothing here.
    # No exif= argument, so metadata is dropped rather than shipped to visitors.
    im.convert("RGB").save(work, "JPEG", quality=WEB_QUALITY, optimize=True,
                           progressive=True, subsampling="4:4:4")
    note = f"capped to {im.width}x{im.height}" if resized else "metadata stripped"
    print(f"    {note}: {src.stat().st_size/1024:.0f}K -> {work.stat().st_size/1024:.0f}K")
    return work


def check_seo_name(filename: str) -> list[str]:
    """Warn, never block: a bad name is worth flagging, not worth failing an upload."""
    stem = Path(filename).stem
    out = []
    if stem != stem.lower():
        out.append("not lowercase")
    if "_" in stem or " " in stem:
        out.append("use hyphens, not underscores or spaces")
    words = [w for w in stem.split("-") if w]
    noise = [w for w in words if w in SEO_NOISE or _is_number_noise(w)]
    if noise:
        out.append(f"words carrying no search value: {', '.join(noise)}")
    if len(words) < 4:
        out.append("too few keywords to describe the subject")
    if len(stem) > 80:
        out.append("over 80 characters")
    return out


def post_multipart(url, params, filepath, filename):
    boundary = "----skingenetix" + str(int(time.time()))
    body = b""
    for p in params:
        body += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"{p['name']}\"\r\n\r\n"
                 f"{p['value']}\r\n").encode()
    ctype = mimetypes.guess_type(filename)[0] or "image/jpeg"
    body += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; "
             f"filename=\"{filename}\"\r\nContent-Type: {ctype}\r\n\r\n").encode()
    body += Path(filepath).read_bytes() + f"\r\n--{boundary}--\r\n".encode()
    req = urllib.request.Request(url, data=body,
                                 headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return r.status


def main():
    plan_path = ROOT / sys.argv[1]
    plan = json.loads(plan_path.read_text())
    e = env()
    store = e["SHOPIFY_SKINGENETIX_STORE"]
    tok = token(e)

    items = [i for i in plan["images"] if not i.get("uploaded_handle")]
    if not items:
        print("Every image in the plan already has a handle — nothing to upload.")
        return

    print(f"Store : {store}")
    print(f"Upload: {len(items)} images\n")

    # 0. optimise, and check the name is worth having in a search result
    for it in items:
        src = ROOT / it["source"]
        if not src.exists():
            sys.exit(f"missing source: {it['source']}")
        print(f"  {it['filename']}")
        problems = check_seo_name(it["filename"])
        if problems:
            print(f"    SEO filename: {'; '.join(problems)}")
        it["_upload_path"] = optimise(
            src, ROOT / ".web-optimised" / it["filename"])
    print()

    # 1. staged targets
    staged_in = []
    for it in items:
        up = Path(it["_upload_path"])
        staged_in.append({"resource": "FILE", "filename": it["filename"],
                          "mimeType": mimetypes.guess_type(it["filename"])[0] or "image/jpeg",
                          "httpMethod": "POST", "fileSize": str(up.stat().st_size)})

    data = gql(store, tok, STAGED, {"input": staged_in})
    errs = data["stagedUploadsCreate"]["userErrors"]
    if errs:
        sys.exit(f"stagedUploadsCreate: {errs}")
    targets = data["stagedUploadsCreate"]["stagedTargets"]

    # 2. push bytes, 3. register
    files_in = []
    for it, tgt in zip(items, targets):
        src = Path(it["_upload_path"])
        print(f"  uploading {it['filename']} ...", end=" ", flush=True)
        post_multipart(tgt["url"], tgt["parameters"], src, it["filename"])
        print("ok")
        files_in.append({"originalSource": tgt["resourceUrl"], "contentType": "IMAGE",
                         "alt": it["alt"]})

    data = gql(store, tok, CREATE, {"files": files_in})
    errs = data["fileCreate"]["userErrors"]
    if errs:
        sys.exit(f"fileCreate: {errs}")
    print(f"\n  registered {len(data['fileCreate']['files'])} files, waiting for READY")

    # 4. poll until Shopify has processed them, and read back the REAL filename
    #
    # Shopify sanitises names and suffixes on collision, so the name that comes back
    # is authoritative. Matching it is where this used to go wrong: a startswith on
    # the first 40 characters binds the WRONG file the moment a longer name shares
    # that prefix. On 2026-08-24 the stem
    #   skingenetix-glutathione-brightening-radiant-glow-serum
    # matched ...-radiant-glow-serum-COLLECTION.jpg first - a different picture, at a
    # different aspect, uploaded by another session - and would have published it.
    # So: gather every READY candidate, then prefer an exact stem, and only fall back
    # to the shortest prefix match when Shopify has genuinely renamed the file.
    for attempt in range(30):
        time.sleep(4)
        done = 0
        for it in items:
            stem = it["filename"].rsplit(".", 1)[0]
            res = gql(store, tok, POLL, {"q": f"filename:{stem}*"})
            cands = []
            for edge in res["files"]["edges"]:
                node = edge["node"]
                if node["fileStatus"] != "READY" or not node.get("image"):
                    continue
                real = node["image"]["url"].split("?")[0].split("/")[-1]
                if real.rsplit(".", 1)[0].startswith(stem):
                    cands.append((real, node["image"]["url"]))
            if not cands:
                continue
            # Match the WHOLE filename first, extension included. Comparing only the
            # extension-stripped stem treats `<stem>.png` and `<stem>.jpg` as equally
            # exact, so the winner is whichever Shopify happened to return first — and
            # on 2026-08-27 that was a superseded PNG of the same picture, uploaded
            # minutes earlier by the format bug fixed in optimise(). The plan asked for
            # a .jpg and got a handle pointing at the .png. Same family of fault as the
            # prefix note above: a match that is nearly right is not right.
            # Author: Claude Code, 2026-08-27.
            exact = [c for c in cands if c[0] == it["filename"]]
            if not exact:
                exact = [c for c in cands if c[0].rsplit(".", 1)[0] == stem]
            # A prefix match is only ever a guess, and while polling it is the WRONG
            # guess: a file that is merely still processing looks identical to one
            # Shopify renamed. On 2026-08-25 the desktop stem
            #   skingenetix-brightening-glow-glutathione-serum-2-percent
            # was not READY on the first pass, so the only candidate was its own
            # ...-2-percent-MOBILE sibling, and both slots bound to the phone crop --
            # which would have published a 1380x848 portrait as a 3750x848 banner. The
            # note it printed was the only warning, and it scrolls past.
            # So: hold out for the exact stem until the polling budget is nearly spent,
            # and only then accept a rename, and only when it is unambiguous.
            last_chance = attempt >= 26
            if not exact and not (last_chance and len(cands) == 1):
                continue
            real, url = exact[0] if exact else cands[0]
            if not exact:
                print(f"    note: {stem} resolved to {real} (Shopify renamed it)")
            it["uploaded_handle"] = f"shopify://shop_images/{real}"
            it["cdn_url"] = url
            done += 1
        print(f"    ready {done}/{len(items)}")
        if done == len(items):
            break
    else:
        sys.exit("timed out waiting for files to reach READY")

    # _upload_path is a scratch path for this run, not part of the plan's record.
    for it in plan["images"]:
        it.pop("_upload_path", None)
    plan_path.write_text(json.dumps(plan, indent=2) + "\n")
    print("\nResolved handles:")
    for it in plan["images"]:
        if it.get("uploaded_handle"):
            print(f"  {it['slot']:<26} {it['uploaded_handle']}")
    print(f"\nWrote handles back into {sys.argv[1]}")


if __name__ == "__main__":
    main()
