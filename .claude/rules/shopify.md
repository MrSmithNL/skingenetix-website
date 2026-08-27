---
paths:
  - 'scripts/**/*'
  - '*.liquid'
  - 'sections/**/*'
  - 'snippets/**/*'
  - 'templates/**/*'
---

# Shopify Development Rules

1. **GraphQL first** — All API calls use GraphQL Admin API (REST is deprecated)
2. **No core Liquid edits** — Never modify existing theme Liquid files. Add new sections/snippets only.
3. **Additive CSS only** — Brand styling in custom CSS, never overwrite theme CSS
4. **Annotate all code** — Every Claude-written code block includes author, date, and purpose comment
5. **Theme Check validation** — Run Theme Check on any Liquid changes before committing
6. **One translation system** — **Translate & Adapt** (Shopify native) only; it is what is actually installed. Never add Langify alongside it. ⚠️ This rule said the exact opposite until 2026-08-27, when `appInstallations` showed Translate & Adapt installed and no Langify. Theme/template text is translatable natively as `ONLINE_STORE_THEME_JSON_TEMPLATE` resources — see `docs/research-before-after-section.md` §3.
7. **Image URL stability** — Never rename or re-upload original images (breaks translations, which key off the URL)
8. **Rate limit awareness** — Shopify allows 40 req/sec on GraphQL. Batch operations must be throttled.

## Quality Gates

- Markdown linted with markdownlint (`.markdownlint.json`)
- Prettier for markdown/JSON/YAML formatting
- Husky + lint-staged pre-commit hooks
- CI hardened (no continue-on-error, errors block build)
- No secrets in git — tokens and passwords in Bitwarden
