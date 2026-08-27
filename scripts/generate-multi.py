#!/usr/bin/env python3
"""Generate one banner brief across EVERY image supplier, for side-by-side choice.

    source ~/.claude/config/image-credentials.env
    python3 scripts/generate-multi.py configs/banners/<wave>.json
    python3 scripts/generate-multi.py configs/banners/<wave>.json --only SLOTID

Enforces .claude/rules/website-imagery.md rule 1: no website image is generated on
one backend. generate-banners.py hardcodes two Seedream endpoints, which is how a
single engine's blind spot cost an evening on 2026-08-21.

Why not just import the product-photography skill's backends.py: its aspect
vocabulary is 1:1 / 4:5 / 9:16 only, and full-bleed bands are 2.4:1. Every backend
speaks a different dialect for size and none of them errors on a value it does not
recognise — they substitute a default silently, which is how 4:5 ad plates once came
back square. So each supplier gets explicit dimensions in its own vocabulary here.

Author: Claude Code, 2026-08-22.
"""
import argparse
import base64
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

#: The credential file this script's own usage line tells you to `source` contains bare
#: `KEY=value` lines with no `export`, so sourcing it creates SHELL parameters and not
#: environment variables — and a child python process inherits nothing. Every supplier
#: that reads os.environ therefore dies instantly with "no GEMINI_API_KEY" / KeyError,
#: while Luma keeps working because it falls back to ~/.config/luma/api-key. On
#: 2026-08-27 that turned a six-supplier run into a one-supplier run with no visible
#: error: python block-buffers stdout through a pipe, so the five failures printed
#: nothing until the process exited, and a run failing 5/6 looks exactly like a run
#: that is merely slow. Reading the file here rather than trusting the shell makes the
#: documented invocation correct instead of silently wrong.
#: Author: Claude Code, 2026-08-27.
CRED_FILE = Path.home() / ".claude" / "config" / "image-credentials.env"


def _load_credentials():
    """Fill any missing key from the central credential file. Never overwrites a real
    environment variable, so an explicitly exported key still wins."""
    if not CRED_FILE.exists():
        return
    for line in CRED_FILE.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k, v = k.strip().removeprefix("export "), v.strip().strip('"').strip("'")
        if v and not os.environ.get(k):
            os.environ[k] = v


#: Long edge each supplier can actually deliver, measured not documented.
#: Seedream reaches 4096; FLUX.2 and gpt-image cap at 2048; Gemini tiers by name.
SUPPLIERS = ["seedream", "gpt_image", "nbp_pro", "nbp_flash", "flux2", "luma"]


def die(msg):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def _save(data: bytes, out_dir: Path, stem: str, i: int) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    p = out_dir / f"{stem}_{i:02d}.png"
    p.write_bytes(data)
    return p


def _fetch(url: str) -> bytes:
    return urllib.request.urlopen(url, timeout=180).read()


# --------------------------------------------------------------------- fal pair

def _fal(model: str, prompt: str, negative: str, w: int, h: int, n: int,
         refs: list[str], out_dir: Path, stem: str) -> list[Path]:
    import fal_client

    args = {"prompt": prompt, "image_size": {"width": w, "height": h}, "num_images": n}
    if negative:
        args["negative_prompt"] = negative
    if refs:
        args["image_urls"] = [fal_client.upload_file(r) for r in refs]
    res = fal_client.subscribe(model, arguments=args, with_logs=False)
    return [_save(_fetch(im["url"]), out_dir, stem, i)
            for i, im in enumerate(res.get("images", []), 1) if im.get("url")]


def seedream(prompt, negative, w, h, n, refs, out_dir, stem):
    base = "fal-ai/bytedance/seedream/v5/lite"
    model = f"{base}/edit" if refs else f"{base}/text-to-image"
    return _fal(model, prompt, negative, w, h, n, refs, out_dir, stem)


def flux2(prompt, negative, w, h, n, refs, out_dir, stem):
    # FLUX.2 invents brand identities, so it is only ever sent reference-free
    # material briefs — never anything with legible branding in frame.
    if refs:
        raise RuntimeError("flux2 is barred from reference/branding shots")
    cap = 2048
    if max(w, h) > cap:
        s = cap / max(w, h)
        w, h = int(w * s) // 8 * 8, int(h * s) // 8 * 8
    # The model id is bare - "fal-ai/flux-2-pro/text-to-image" 404s. Seedream is the
    # one that takes a /text-to-image suffix; the two are not symmetrical.
    return _fal("fal-ai/flux-2-pro", prompt, negative, w, h, n, refs, out_dir, stem)


# ------------------------------------------------------------------- gpt-image

def gpt_image(prompt, negative, w, h, n, refs, out_dir, stem, model="gpt-image-2"):
    from openai import OpenAI

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    # Rejects any dimension not divisible by 16 with a 400, and caps the long edge
    # at 2048 — a 1638x2048 once lost this backend on three plates in one run.
    cap = 2048
    s = cap / max(w, h)
    gw, gh = [max(16, round(v * s / 16) * 16) for v in (w, h)]
    full = prompt + (f"\n\nAvoid: {negative}" if negative else "")
    out = []
    if refs:
        handles = [open(r, "rb") for r in refs]
        try:
            res = client.images.edit(model=model, image=handles, prompt=full,
                                     size=f"{gw}x{gh}", n=n)
        finally:
            for fh in handles:
                fh.close()
    else:
        res = client.images.generate(model=model, prompt=full, size=f"{gw}x{gh}", n=n)
    for i, d in enumerate(res.data, 1):
        raw = base64.b64decode(d.b64_json) if d.b64_json else _fetch(d.url)
        out.append(_save(raw, out_dir, stem, i))
    return out


# ---------------------------------------------------------------------- gemini

#: google-genai 1.47's ImageConfig exposes only aspect_ratio, so imageSize has to
#: go over raw REST — the sole reason this talks HTTP rather than the SDK.
def _gemini(model_id, prompt, negative, w, h, n, refs, out_dir, stem):
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_AI_API_KEY")
    if not key:
        raise RuntimeError("no GEMINI_API_KEY")
    ratio = w / h
    aspect = min({"1:1": 1.0, "4:3": 4 / 3, "16:9": 16 / 9, "21:9": 21 / 9},
                 key=lambda k: abs({"1:1": 1.0, "4:3": 4 / 3, "16:9": 16 / 9,
                                    "21:9": 21 / 9}[k] - ratio))
    parts = [{"text": prompt + (f"\n\nAvoid: {negative}" if negative else "")}]
    for r in refs:
        parts.append({"inline_data": {"mime_type": "image/jpeg",
                                      "data": base64.b64encode(Path(r).read_bytes()).decode()}})
    body = {"contents": [{"parts": parts}],
            "generationConfig": {"imageConfig": {"imageSize": "4K", "aspectRatio": aspect}}}
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_id}:generateContent?key={key}"
    out = []
    for i in range(1, n + 1):
        req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                     headers={"Content-Type": "application/json"})
        res = json.loads(urllib.request.urlopen(req, timeout=300).read())
        for c in res.get("candidates", []):
            for p in c.get("content", {}).get("parts", []):
                d = p.get("inlineData") or p.get("inline_data")
                if d and d.get("data"):
                    out.append(_save(base64.b64decode(d["data"]), out_dir, stem, len(out) + 1))
        time.sleep(1)
    if not out:
        raise RuntimeError("gemini returned no image parts")
    return out


def nbp_pro(prompt, negative, w, h, n, refs, out_dir, stem):
    return _gemini("gemini-3-pro-image", prompt, negative, w, h, n, refs, out_dir, stem)


def nbp_flash(prompt, negative, w, h, n, refs, out_dir, stem):
    return _gemini("gemini-3.1-flash-image", prompt, negative, w, h, n, refs, out_dir, stem)


# ------------------------------------------------------------------------ luma

def luma(prompt, negative, w, h, n, refs, out_dir, stem):
    # The key file carries comment lines. Reading it whole put a comment - em dash
    # and all - into the Authorization header, and http.client encodes headers as
    # latin-1, so the request died on the dash rather than on anything to do with
    # Luma. Scan for the first non-comment line, as the skill's own reader does.
    key = os.environ.get("LUMA_API_KEY")
    if not key:
        for line in Path(os.path.expanduser("~/.config/luma/api-key")).read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                key = line
                break
    if not key:
        raise RuntimeError("no luma key")
    base = "https://agents.lumalabs.ai/v1"
    # Luma has no negative-prompt field, so a negative list folds into the prompt
    # body and trips the content filter — two attempts were lost to
    # `content_moderated` on 2026-08-22. Negatives are therefore dropped entirely.
    ratio = w / h
    aspect = "16:9" if ratio > 1.3 else "1:1"
    out = []
    for i in range(1, n + 1):
        body = {"model": "uni-1", "type": "image", "prompt": prompt, "aspect_ratio": aspect}
        req = urllib.request.Request(f"{base}/generations", data=json.dumps(body).encode(),
                                     headers={"Authorization": f"Bearer {key}",
                                              "Content-Type": "application/json"})
        gen = json.loads(urllib.request.urlopen(req, timeout=120).read())
        gid = gen.get("id")
        for _ in range(60):
            time.sleep(4)
            r = urllib.request.Request(f"{base}/generations/{gid}",
                                       headers={"Authorization": f"Bearer {key}"})
            st = json.loads(urllib.request.urlopen(r, timeout=60).read())
            if st.get("state") in ("completed", "failed"):
                break
        if st.get("state") != "completed":
            raise RuntimeError(f"luma {st.get('state')}: {str(st.get('failure_reason'))[:160]}")
        out.append(_save(_fetch(st["output"][0]["url"]), out_dir, stem, i))
    return out


FNS = {"seedream": seedream, "gpt_image": gpt_image, "nbp_pro": nbp_pro,
       "nbp_flash": nbp_flash, "flux2": flux2, "luma": luma}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    ap.add_argument("--only")
    ap.add_argument("--suppliers", default=",".join(SUPPLIERS))
    ap.add_argument("--candidates", type=int, default=2)
    args = ap.parse_args()

    _load_credentials()
    cfg = json.loads((ROOT / args.config).read_text())
    slots = cfg["slots"]
    if args.only:
        slots = [s for s in slots if s["id"].startswith(tuple(args.only.split(",")))]
    want = [s.strip() for s in args.suppliers.split(",") if s.strip()]

    out_root = ROOT / "assets" / "ai-generated" / f"2026-08-22-multi-{cfg['wave']}"
    manifest = []
    for slot in slots:
        neg = ", ".join(x for x in (cfg["defaults"].get("negative_global"),
                                    slot.get("negative_extra")) if x)
        refs = [str(ROOT / r) for r in slot.get("ref_files") or []]
        # flush= on every line below: this runs for the best part of an hour and is
        # almost always piped to tee or a log, where python block-buffers stdout and
        # nothing appears until the process exits. A supplier that fails in the first
        # minute has to say so in the first minute, or the run cannot be rescued.
        print(f"\n{'=' * 62}\n{slot['id']} — {slot['width']}x{slot['height']}", flush=True)
        for sup in want:
            if sup == "flux2" and refs:
                print(f"  {sup:<10} skipped (barred from reference shots)", flush=True)
                continue
            t0 = time.time()
            try:
                paths = FNS[sup](slot["prompt"], neg, slot["width"], slot["height"],
                                 args.candidates, refs, out_root / slot["id"],
                                 f"{slot['id']}-{sup}")
                print(f"  {sup:<10} {len(paths)} in {time.time() - t0:.0f}s", flush=True)
                manifest += [{"slot": slot["id"], "supplier": sup, "path": str(p)} for p in paths]
            except Exception as e:                                # noqa: BLE001
                print(f"  {sup:<10} FAILED: {str(e)[:170]}", flush=True)
                manifest.append({"slot": slot["id"], "supplier": sup, "error": str(e)[:300]})
    out_root.mkdir(parents=True, exist_ok=True)
    (out_root / "manifest.json").write_text(json.dumps(manifest, indent=2))
    ok = sum(1 for m in manifest if m.get("path"))
    print(f"\n{ok} images across {len(want)} suppliers -> {out_root.relative_to(ROOT)}", flush=True)
    # Rule 1 of website-imagery.md is that every image goes to every supplier. A run
    # that quietly lost half its backends still prints a cheerful image count, which is
    # how five silent failures survived a whole wave — so name them at the end too.
    lost = sorted({m["supplier"] for m in manifest if m.get("error")})
    if lost:
        print(f"WARNING: {len(lost)} supplier(s) returned nothing — {', '.join(lost)}",
              flush=True)


if __name__ == "__main__":
    main()
