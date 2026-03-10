# AGENTS.md — Skingenetix (CLIENT-003)

> Tool-agnostic agent instructions. Works with Claude Code, Cursor, Codex, Aider, and any tool that supports AGENTS.md.

## Project Overview

Shopify e-commerce store for skincare products — sister brand to Hairgenetix (CLIENT-002). Built and managed primarily by AI via Shopify GraphQL Admin API.

## Tech Stack

- **Platform:** Shopify (GraphQL Admin API)
- **Theme:** Shopify 2.0 (Sense or Refresh)
- **Translation:** Langify (9 languages)
- **Linting:** markdownlint (.markdownlint.json), Prettier
- **Pre-commit:** Husky + lint-staged
- **CI:** GitHub Actions (lint, format, build — all hard gates)

## Commands

```bash
# Lint + format
npx markdownlint docs/
npx prettier --check "**/*.{md,json,yml,yaml}"

# Pre-commit (runs automatically)
npx lint-staged
```

## Project Structure

```
docs/        # Architecture, strategy, SEO, setup steps
scripts/     # Shopify automation scripts
research/    # Technical research
```

## Style Guide

- Markdown: markdownlint + Prettier formatted
- Shopify: GraphQL first (not REST), additive CSS only, no core Liquid edits
- One translation system: Langify only (never enable Shopify Translate & Adapt)
- Never rename/re-upload original images (breaks Langify translations)

## Boundaries

- **Always do:** Run lint-staged. Update docs after changes. Use GraphQL API.
- **Ask first:** Modifying core Liquid files, publishing/going live, changing pricing.
- **Never do:** Hardcode tokens, delete products without approval, mix translation systems.
