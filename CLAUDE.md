# Project Instructions — Skingenetix (CLIENT-003)

<!-- project-classification
type: client
work_nature: content-site
hierarchy_position: client-delivery
enforcement_profile: light
-->

These instructions apply to this project in every session.

---

## What This Project Is

**Skingenetix** is a Shopify e-commerce store for skincare products — a sister brand to Hairgenetix (CLIENT-002). Same owner, same contact details, different product line. Built and managed primarily by Claude Code via Shopify's GraphQL Admin API.

---

## Related Projects

- **Agency standards:** `~/Claude Code/Projects/smith-ai-agency/docs/capabilities/`
- **Sister brand (CLIENT-002):** `~/Claude Code/Projects/hairgenetix/`
- **SEO engine (PROD-001):** `~/Claude Code/Projects/seo-toolkit/`

---

## Tech Stack

| Layer           | Choice                 | Notes                             |
| --------------- | ---------------------- | --------------------------------- |
| **Platform**    | Shopify                | Hosted — no separate hosting      |
| **Theme**       | TBD (Sense or Refresh) | Free Shopify 2.0 theme            |
| **API**         | GraphQL Admin API      | Via custom app access token       |
| **Translation** | Langify                | 9 languages (same as Hairgenetix) |
| **Email**       | Klaviyo                | Same as Hairgenetix               |
| **Credentials** | Bitwarden              | All tokens/keys stored here       |

---

## Agency-Wide Delivery Framework

This project operates under the agency's autonomous delivery framework. All standards, processes, and department manager oversight apply here:

- **Quality Manager** — Code quality, testing, documentation standards (`smith-ai-agency/docs/capabilities/quality-manager.md`)
- **DevOps Manager** — CI/CD, deployment, infrastructure reliability (`smith-ai-agency/docs/capabilities/devops-manager.md`)
- **Technical Architect** — Architecture decisions, fitness functions, dependency governance (`smith-ai-agency/docs/capabilities/technical-architect.md`)
- **Delivery Manager** — Sprint planning, objective tracking, blocker resolution (`smith-ai-agency/docs/capabilities/delivery-manager.md`)
- **Requirements Engineering** — Spec-driven development, 3-gate process (`smith-ai-agency/docs/capabilities/requirements-engineering.md`)
- **Sprint Management** — 2-week cadence, velocity tracking (`smith-ai-agency/objectives/sprints/`)

---

## Autonomous Permissions

No confirmation needed: update `.md` files, create docs/scripts, commit/push docs-only, Shopify API calls (products, collections, translations, content, SEO, menus), edit theme JSON/CSS.

Always confirm before: modifying core Liquid files, publishing/going live, changing pricing/payment, deleting products/collections, any permanent external effect.

---

## Architecture Maintenance — Always Automatic

After any change to infrastructure, services, tools, or accounts: update `docs/architecture.md` + `docs/todo.md`, commit and push.

---

## Key Docs

| File                       | What It Covers                        |
| -------------------------- | ------------------------------------- |
| `docs/todo.md`             | Tasks with IDs and priorities         |
| `docs/architecture.md`     | System diagram, connections, accounts |
| `docs/setup-steps.md`      | Every setup step with undo procedure  |
| `docs/content-strategy.md` | Content plan and product positioning  |
