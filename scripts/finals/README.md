# Finals workflow — from generated candidate to live store image

Five scripts, in the order they run. They existed only in a session scratchpad
until 2026-08-20; they are here because Malcolm's selection workflow is ongoing
and a scratchpad does not survive a session.

| Script | What it does |
| --- | --- |
| `collect-all-candidates.py` | Hardlinks EVERY candidate from EVERY run of a product into one `ALL-<product>/` folder to browse. Nothing is excluded — QA verdicts go in a sidecar text file as information, not as a filter. |
| `prepare-selected-for-upload.py` | Takes the images Malcolm marked with a leading `_`, gives each an SEO filename carrying the actives and search terms, optimises it for web, and writes `_upload-manifest.json`. |
| `add-supplied-image.py` | Adds one image Malcolm supplied by hand. Derives the next free candidate number so it cannot collide with a generated one, keeps the untouched original in the ALL folder, and tags it `backend: external` so it stays out of cost-per-winner. |
| `sweep-finals-folder.py` | Re-optimises anything that has drifted: replaced files (byte count no longer matches the manifest), unknown files (adopted onto the naming convention), deleted files (dropped from the manifest). Preserves Malcolm's `_`/`__` marks through any rename. Idempotent — run it before every upload. |
| `shopify-replace-media.py` | Uploads the `__`-marked images to a product, replacing existing media. Adds and waits for `READY` **before** deleting the old, then sets the order. |

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
