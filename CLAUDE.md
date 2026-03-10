# Project Instructions — Skingenetix (CLIENT-003)

These instructions apply to this project in every session.

---

## What This Project Is

**Skingenetix** is a Shopify e-commerce store for skincare products — a sister brand to Hairgenetix.com (CLIENT-002). Same owner, same contact details, different product line.

The store is **built and managed primarily by Claude Code** via Shopify's GraphQL Admin API, with human involvement for one-time setup tasks and visual/strategic decisions.

---

## Skills Check — Always First

Before taking any action, check `~/.claude/skills/` for a relevant skill. 40 core skills installed (plus ~832 Composio tool connectors).

---

## Capability Hierarchy — Mandatory

This project follows the agency's 5-layer capability hierarchy:
**Products -> Capabilities -> Agents -> Skills -> Tools**.
See the [Capability Hierarchy](~/Claude Code/Projects/smith-ai-agency/docs/capability-hierarchy.md) reference.
Use terms precisely: Tools are external connections (Composio, MCP, APIs).
Skills are procedural knowledge (`~/.claude/skills/`).
Agents are autonomous workers (`~/.claude/agents/`).
Capabilities are business-level abilities. Products are sellable platforms.

---

## Tech Stack

| Layer                   | Choice                             | Notes                                          |
| ----------------------- | ---------------------------------- | ---------------------------------------------- |
| **E-commerce Platform** | Shopify                            | Hosted by Shopify — no separate hosting needed |
| **Theme**               | TBD (Sense or Refresh recommended) | Free Shopify 2.0 theme                         |
| **API Access**          | GraphQL Admin API                  | Via custom app access token                    |
| **Translation**         | Langify                            | Same as Hairgenetix — 9 languages              |
| **Email Marketing**     | Klaviyo                            | Same as Hairgenetix                            |
| **Bundles**             | Kaching Bundles                    | Same as Hairgenetix                            |
| **Analytics**           | GA4 + Google Ads + FB Pixel        | Standard tracking                              |
| **Domain Registrar**    | OpenDomainRegistry.net             | DNS pointing to Shopify                        |
| **Email Hosting**       | TBD                                | Separate from Shopify                          |
| **Credentials**         | Bitwarden                          | All tokens/keys stored here                    |

---

## Key Docs

| File                                       | What's In It                                      |
| ------------------------------------------ | ------------------------------------------------- |
| `docs/architecture.md`                     | System diagram, components, connections, accounts |
| `docs/todo.md`                             | Tasks with IDs and priorities                     |
| `docs/accounts-and-access.md`              | Platforms and credentials (Bitwarden refs only)   |
| `docs/decisions-log.md`                    | Technical decisions with reasoning (ADR format)   |
| `docs/security-risk-log.md`                | Risks and mitigations                             |
| `docs/setup-steps.md`                      | Every setup step with reversal instructions       |
| `docs/processes-and-flows.md`              | Workflows and procedures                          |
| `docs/content-strategy.md`                 | Content plan and product positioning              |
| `docs/seo-strategy.md`                     | Keywords and optimisation                         |
| `docs/metrics.md`                          | Analytics setup and KPIs                          |
| `research/skingenetix-shopify-research.md` | Full technical research report                    |

---

## Autonomous Permissions

Claude has full autonomous permission to:

- Update any `.md` documentation file in this repo
- Create new `.md` files in `docs/` or `research/`
- Create and edit scripts in `scripts/`
- Commit and push documentation-only changes to GitHub
- Make Shopify API calls (products, collections, translations, content, SEO, menus)
- Edit theme JSON settings and custom CSS files
- Register translations via GraphQL API

Always confirm before:

- Modifying core Liquid theme files
- Publishing/going live
- Changing pricing or payment settings
- Any action with permanent external effects
- Deleting products or collections

---

## Architecture Maintenance — Always Automatic

After any change to infrastructure, services, tools, accounts, or connections:

1. Update `docs/architecture.md`
2. Update `docs/todo.md`
3. Commit and push

---

## Shopify Development Rules

1. **GraphQL first** — All API calls use GraphQL Admin API (REST is deprecated)
2. **No core Liquid edits** — Never modify existing theme Liquid files. Add new sections/snippets only.
3. **Additive CSS only** — Brand styling goes in custom CSS, never overwrite theme CSS
4. **Annotate all code** — Every Claude-written code block includes author, date, and purpose comment
5. **Theme Check validation** — Run Theme Check on any Liquid changes before committing
6. **One translation system** — Langify only. Never enable Shopify native Translate & Adapt alongside it.
7. **Image URL stability** — Never rename or re-upload original images (breaks Langify translations)
8. **Rate limit awareness** — Shopify allows 40 req/sec on GraphQL. Batch operations must be throttled.

---

## Non-Negotiable Rules

1. No secrets in git — Tokens and passwords go in Bitwarden
2. Document every change — Architecture and todo updated before session ends
3. Plain English — All docs readable by non-technical owner
4. Reversibility — Every setup step has an undo procedure documented
5. Security tracking — Any risk gets logged in `docs/security-risk-log.md`
