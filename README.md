# Skingenetix Website (CLIENT-003)

Shopify e-commerce store for Skingenetix skincare products — a sister brand to [Hairgenetix.com](https://hairgenetix.com).

## What This Repo Contains

This is **not** the Shopify store itself (that lives on Shopify's servers). This repo contains:
- Project documentation and architecture
- Product content drafts and translations
- Scripts for Shopify API automation
- Research and decision records
- Setup steps and configuration records

## Folder Structure

```
skingenetix-website/
├── CLAUDE.md                    ← Project rules for Claude Code
├── README.md                    ← This file
├── docs/
│   ├── architecture.md          ← System diagram, components, connections
│   ├── todo.md                  ← Task tracking
│   ├── accounts-and-access.md   ← Platforms and credentials (refs only)
│   ├── decisions-log.md         ← Technical decisions (ADR format)
│   ├── security-risk-log.md     ← Risks and mitigations
│   ├── setup-steps.md           ← Every setup step + how to undo
│   ├── processes-and-flows.md   ← Workflows and procedures
│   ├── content-strategy.md      ← Product positioning and content plan
│   ├── seo-strategy.md          ← Keywords and optimisation
│   └── metrics.md               ← Analytics setup and KPIs
├── content/
│   ├── pages/                   ← Page content drafts
│   └── products/                ← Product descriptions and data
├── research/                    ← Technical research and analysis
├── scripts/                     ← Shopify API automation scripts
├── assets/
│   └── images/                  ← Design assets (not product photos)
└── .github/
    └── workflows/
        └── ci.yml               ← CI/CD pipeline
```

## Key Rules

1. **No secrets in this repo** — All credentials stored in Bitwarden
2. **Document everything** — Every change, decision, and account recorded
3. **Shopify is the host** — This repo is for management, not hosting
4. **One translation system** — Langify only (same as Hairgenetix)
5. **No core theme edits** — Only additive changes to Shopify theme
