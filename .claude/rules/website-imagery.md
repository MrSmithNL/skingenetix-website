---
paths:
  - 'scripts/generate-banners*.py'
  - 'configs/banners/**/*'
  - 'assets/ai-generated/**/*'
---

# Website Imagery Rules

## 1. Every image goes to every supplier — no single-engine runs

**Never generate a website image on one backend.** Every brief for every slot on this site
fans out across **all available suppliers**, each on its **latest and most capable model**,
so Malcolm compares real alternatives and chooses. One candidate per supplier is the floor,
not the target.

Standing instruction from Malcolm, 2026-08-22.

### Why — this rule was bought with a wasted evening

On 2026-08-21 the whole homepage banner run went through **Seedream alone**, because
`scripts/generate-banners.py` hardcodes two Seedream endpoints and has no routing. One
product name — MATRIXYL — failed in roughly thirty of fifty candidates across five
rewritten briefs, with the word spelled letter by letter and every misspelling negated by
name. It was treated as a prompting problem for hours.

The same brief sent to **gpt-image** rendered `MATRIXYL 3000 PRO COLLAGEN` correctly on the
**first attempt, both candidates**, and got the fine ingredient line right too — something
no Seedream candidate managed all evening. gpt-image then broke `PDRN COLLAGEN REPAIR`,
which Seedream had rendered correctly.

That is the whole argument: **the failure modes do not overlap.** Neither engine is better.
What one ruins another gets right. The product-photography skill has said this for months —
"running the same brief across 3 backends raises per-variant pass rate from ~50% to ~85%" —
and the banner runner ignored it.

## 2. Check the roster is current before every run

Suppliers ship new models without notice and a stale model id **404s silently** — the run
just returns fewer candidates with no visible error (`gemini-2-flash-image` did exactly
this). Re-list before a production run:

```bash
# OpenAI
curl -s https://api.openai.com/v1/models -H "Authorization: Bearer $OPENAI_API_KEY" \
  | python3 -c "import json,sys; print(sorted(m['id'] for m in json.load(sys.stdin)['data'] if 'image' in m['id']))"
# Google
curl -s "https://generativelanguage.googleapis.com/v1beta/models?key=$GEMINI_API_KEY&pageSize=200" \
  | python3 -c "import json,sys; print(sorted(m['name'].split('/')[-1] for m in json.load(sys.stdin)['models'] if 'image' in m['name']))"
```

Checked 2026-08-22 — the roster had already drifted. `chatgpt-image-latest` and
`gpt-image-1.5` existed at OpenAI and were wired into nothing; `gemini-3.1-flash-lite-image`
was new at Google.

## 3. Judge at 100%, and again at rendered size

A contact sheet **cannot** judge label fidelity. `NEAT2_04` looked flawless tiled and read
`MATPIXYL` at full size. Both checks are needed, and they catch different faults:

- **100% zoom** catches generation errors — misspellings, wrong product colours.
- **Rendered size** catches *resampling* errors. A correct `PDRN` thinned into `PORN` purely
  through Shopify's downscale, because the theme emitted `sizes="350px"` against a srcset
  topping out at 700w. The pixels were right; the delivery was wrong.

## 4. Known supplier traps

| Supplier | Trap |
| --- | --- |
| **Luma** | No negative-prompt field, so negatives fold into the prompt body and trip the content filter. Keep its negative list short or it returns `content_moderated` and you lose the backend silently. |
| **FLUX.2** | Invents brand identities that look clean and are wrong. Barred from any shot where branding is legible; fine for reference-free material and skin studies. |
| **gpt-image** | Rejects any dimension not divisible by 16 with a 400. Long edge caps at 2048. |
| **NBP Pro** | 6x the price of NBP Flash and won *less often* on this project's own numbers ($0.81 vs $0.087 per chosen image). Justify per shot. |
| **Gemini** | Daily quota of 250 generate-requests shared across Pro and Flash. Run the most important brief first. |
| **All** | Named size presets are not portable — `square_hd` means 3072 on Seedream and 1024 on FLUX.2. Always pass explicit dimensions. |
