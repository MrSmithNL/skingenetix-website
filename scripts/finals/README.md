# Finals workflow — from generated candidate to live store image

Five scripts, in the order they run. They existed only in a session scratchpad
until 2026-08-20; they are here because Malcolm's selection workflow is ongoing
and a scratchpad does not survive a session.

| Script                           | What it does                                                                                                                                                                                                                                                                                       |
| -------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `collect-all-candidates.py`      | Hardlinks EVERY candidate from EVERY run of a product into one `ALL-<product>/` folder to browse. Nothing is excluded — QA verdicts go in a sidecar text file as information, not as a filter.                                                                                                     |
| `prepare-selected-for-upload.py` | Takes the images Malcolm marked with a leading `_`, gives each an SEO filename carrying the actives and search terms, optimises it for web, and writes `_upload-manifest.json`.                                                                                                                    |
| `add-supplied-image.py`          | Adds one image Malcolm supplied by hand. Derives the next free candidate number so it cannot collide with a generated one, keeps the untouched original in the ALL folder, and tags it `backend: external` so it stays out of cost-per-winner.                                                     |
| `sweep-finals-folder.py`         | Re-optimises anything that has drifted: replaced files (byte count no longer matches the manifest), unknown files (adopted onto the naming convention), deleted files (dropped from the manifest). Preserves Malcolm's `_`/`__` marks through any rename. Idempotent — run it before every upload. |
| `shopify-replace-media.py`       | Uploads the `__`-marked images to a product, replacing existing media. Adds and waits for `READY` **before** deleting the old, then sets the order. Takes a plan from `upload-plans/`.                                                                                                             |

Two test files cover the parts that can fail silently against a live product page:
`test_upload_plan.py` and `test_collect_candidates.py`. Both are stdlib `unittest`, no
dependencies — `python3 scripts/finals/test_*.py`.

## Upload plans

Gallery order and alt text cannot be derived from a filename and are not Claude's to
choose, so each product has a plan in `upload-plans/<handle>.json`: the product GID, the
label alt text is built from, and the shots **in gallery order** with the alt text for
each. Anything marked `__` that does not map to a planned shot is a hard error — the
previous version ranked unknowns last and gave them generic alt text, which would have put
a mis-swept image on a live page unnoticed.

Always dry-run first; it resolves the full order and alt text without contacting the store:

```bash
python3 scripts/finals/shopify-replace-media.py <finals-dir> <plan.json> --dry-run
```

## How Malcolm selects

He marks files in place, in Finder, by prefixing the name:

- `_name.jpg` — a keeper
- `__name.jpg` — a final selection, to be published

Never shortlist for him and never drop a candidate from the browse folder — both were
explicitly rejected. Never let a rename lose his marks.

## Gotchas paid for once already

- Staging a `.jpg` under the optimiser's own output path makes the cleanup delete the
  finished image. Stage under a name the optimiser cannot produce.
- Alt text derived from a filename reads as keyword soup. Author it per shot.
- Deleting store media before the replacements are `READY` can leave a live product with
  no images.
- `collect-all-candidates.py` used to test for the _unmarked_ filename when deciding
  whether a candidate was already collected. Because Malcolm marks by renaming in place, a
  re-run — which is exactly what a Gemini top-up triggers — would have linked the original
  back and left an unmarked duplicate of every image he had chosen. Caught by test before
  it ran; the browse folders were still clean.

## Two more scripts (2026-08-21)

| Script                         | What it does                                                                                                                                                                                                                                                           |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `prepare-marked-run-output.py` | Prepares images Malcolm marked directly in a fan-out's own output folder, where files already carry their SEO name. Takes the engine from the run's `manifest.json`, because that filename form drops it — and engine attribution is what cost-per-winner is built on. |
| `shopify-merge-media.py`       | Uploads a chosen set while retiring only the live images it supersedes. `shopify-replace-media.py` swaps the whole gallery; use this when some live images have no replacement and should stay. Refuses to run if a plan names a media id that is not on that product. |
| `set-product-alt-text.py`      | Authors and applies SEO alt text to every product image on the store. Idempotent — diffs against live alt text and reports anything undescribed, so a new image shows up as a gap.                                                                                     |

## Marks are fragile — four bugs in two days

Every tool here has had a silent mark-handling bug. The marks are added by renaming in
Finder _after_ the file is written, so each tool must map a mangled name back to a record,
and the mangling has four shapes: the marks themselves, Finder's `" copy"`, a browser's
`-2`, and Finder **eating the first character** when the underscore is typed over it
(`_atrixyl_…`).

When writing anything new that reads these folders: strip any number of underscores, strip
`-\d+` and `" copy( N)"`, fall back to a unique _suffix_ match, **raise on ambiguity**, put
the marks back after a rename, and check what you processed against what was marked.

47 tests cover this — `python3 scripts/finals/test_*.py`.
