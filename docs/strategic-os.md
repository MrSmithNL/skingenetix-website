# Skingenetix — Strategic Operating System

> Cascaded from the company-level Strategic OS (smith-ai-agency/docs/strategic-frameworks.md).
> Contains 4 frameworks adapted for this client engagement. Updated quarterly.
> Last updated: 2026-03-06

---

## 1. Engagement Model Canvas

| Block                       | Skingenetix (CLIENT-003)                                                                                                                                                                                            |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Client Profile**          | Malcolm Smith, internal client. New Shopify e-commerce store for skincare products — sister brand to Hairgenetix (CLIENT-002). Same owner, same operational model, different product line (peptide-based skincare). |
| **Value Delivered**         | Store setup and configuration via Shopify GraphQL API, SEO foundation from day one, multilingual store (9 languages via Langify), brand positioning leveraging Hairgenetix credibility.                             |
| **Delivery Channels**       | Managed service — Claude Code builds and manages the store via Shopify GraphQL Admin API. Malcolm approves visual/strategic decisions.                                                                              |
| **Relationship Model**      | Internal client. Setup phase transitioning to continuous engagement. No contract end date.                                                                                                                          |
| **Revenue from Engagement** | Internal — no direct agency revenue. Strategic value = second Shopify proof of concept (validates reusability of Hairgenetix playbook), demonstrates agency can launch new brands efficiently.                      |
| **Resources Required**      | Shopify GraphQL Admin API, Claude Code execution time. SEO Toolkit (planned, after setup complete). Same app stack as Hairgenetix (Langify, Klaviyo, Kaching Bundles).                                              |
| **Key Activities**          | Store setup (theme, products, pages, translations), product migration/creation, SEO foundation (meta, schema, sitemap), brand differentiation from Hairgenetix.                                                     |
| **Agency Products Used**    | PROD-001 SEO Toolkit (planned — after store setup). PROD-003 Marketing Engine (planned).                                                                                                                            |
| **Cost to Serve**           | ~EUR 0 incremental — shared infrastructure. Shopify subscription + app costs paid separately by business.                                                                                                           |

**Company BMC connection:** Skingenetix is the third internal proof-of-concept client.
It validates the agency's ability to rapidly stand up new e-commerce brands
by reusing the Hairgenetix playbook and SEO Toolkit.
Speed-to-launch here becomes a selling point for external clients.
Feeds the "AI Operations" primary activity in the company BMC.

---

## 2. Client OKRs — Q2 2026 (April-June)

> Feeds into Company O2 (market credibility) and Production BU OKRs.
> See smith-ai-agency/docs/okrs/q2-2026.md for company-level OKRs.

**Objective: Complete Skingenetix store setup and establish SEO foundation**

| #   | Key Result                                                           | Target             | Current                                    | Score |
| --- | -------------------------------------------------------------------- | ------------------ | ------------------------------------------ | ----- |
| KR1 | Store fully configured (theme, products, pages, legal)               | Complete           | Store created, API connected, rest pending | --    |
| KR2 | All products live with optimised meta and translations (9 languages) | 100% products live | 0 products migrated                        | --    |
| KR3 | Technical SEO baseline score                                         | 75+ on first audit | Not audited yet                            | --    |
| KR4 | Domain (skingenetix.com) connected with DNS and email                | Complete           | Domain registered, DNS pending             | --    |

**Alignment:**

- KR1 --> Company O2 (credibility — demonstrates rapid brand launch capability)
- KR2 --> Content & Creative Dept KR2 (optimised content across client sites)
- KR3 --> Company O2 KR2 (All client SEO scores at 80+)
- KR4 --> Infrastructure — standard setup process

**Blockers to resolve:**

- Shopify API access token needs saving to Bitwarden
- Theme selection (Sense or Refresh) — design decision needed
- Product range definition — which products to migrate from Hairgenetix / create new
- Langify, Klaviyo, Kaching app installations pending

---

## 3. Client Balanced Scorecard

| Perspective           | KPI                                    | Current                    | Target                                         | Source                                           |
| --------------------- | -------------------------------------- | -------------------------- | ---------------------------------------------- | ------------------------------------------------ |
| **Financial**         | Cost to serve (setup phase)            | ~EUR 0 incremental         | <EUR 50 total setup                            | Infrastructure costs                             |
| **Financial**         | Time to launch                         | Not started                | Store live within Q2                           | Project timeline                                 |
| **Financial**         | Reuse savings vs building from scratch | Not measured               | 50%+ time saved (vs Hairgenetix setup)         | Session tracking                                 |
| **Customer**          | Technical SEO score (first audit)      | Not audited                | 75+                                            | Audit Agent                                      |
| **Customer**          | Products live with full SEO meta       | 0                          | 100% of products                               | Shopify API                                      |
| **Customer**          | Languages configured                   | 0                          | 9 (matching Hairgenetix)                       | Langify                                          |
| **Internal Process**  | Setup steps completed (of total)       | 2 (store + API)            | All steps per [setup-steps.md](setup-steps.md) | Setup checklist                                  |
| **Internal Process**  | Playbook reuse from Hairgenetix        | Identified                 | Documented and applied                         | [processes-and-flows.md](processes-and-flows.md) |
| **Internal Process**  | Cross-brand SEO separation verified    | Not checked                | No keyword cannibalisation                     | GSC                                              |
| **Learning & Growth** | Shopify store launch playbook          | Partial (from Hairgenetix) | Complete reusable playbook                     | Agency docs                                      |
| **Learning & Growth** | GraphQL API automation patterns        | Established                | Documented and reusable                        | [architecture.md](architecture.md)               |

**Company BSC connection:** Setup speed feeds Internal Process (factory process efficiency). Playbook reuse feeds Learning & Growth (compounding advantage from each project). SEO foundation feeds Customer perspective once audited. See smith-ai-agency/docs/strategic-frameworks.md.

---

## 4. Client SWOT

> Last reviewed: 2026-03-06 (baseline). Next review: June 2026 (Q2 scoring).

### Strengths (Internal)

- **Sister brand leverage** — Hairgenetix is established with 1,200+ reviews. "From the makers of Hairgenetix" provides instant credibility.
- **Shared infrastructure** — same Shopify setup, same app stack (Langify, Klaviyo, Kaching), same 9-language framework. Dramatically reduces setup time and cost.
- **Science-backed positioning** — peptide-based skincare inherits the same research-backed credibility as Hairgenetix's copper peptide products.
- **Proven playbook** — every SEO optimisation, schema implementation, and API workflow proven on Hairgenetix can be reapplied immediately.
- **AI-managed from day one** — store built entirely via Claude Code + Shopify GraphQL API. No legacy technical debt.
- **Cross-brand SEO strategy** — explicit plan to avoid keyword cannibalisation between Hairgenetix and Skingenetix.

### Weaknesses (Internal)

- **New brand, no traffic** — zero organic traffic, zero domain authority, no indexed pages yet.
- **No reviews** — starting from zero social proof. Cannot match Hairgenetix's 1,200+ reviews for months/years.
- **Product range not defined** — which products to sell and how to position them is still being decided.
- **Setup phase** — store not yet functional. Theme, products, pages, translations all pending.
- **No content strategy** — [content-strategy.md](content-strategy.md) exists but is a draft. No content pillars or publishing plan.
- **Analytics not connected** — GA4, GSC, and ad tracking all pending setup.

### Opportunities (External)

- **Skincare market larger than hair care** — global skincare market projected at $200B+ by 2028, significantly larger than the hair care segment.
- **Peptide skincare trending** — consumer awareness of peptides in skincare is growing rapidly. Search volume increasing year over year.
- **9-language advantage from launch** — most skincare competitors launch in one language. Starting multilingual gives immediate international reach.
- **Cross-selling with Hairgenetix** — existing Hairgenetix customers are a warm audience for skincare products. Built-in distribution channel.
- **SEO-first approach** — building SEO into every page from the start (unlike Hairgenetix where SEO was retrofitted) means faster ranking potential.
- **AI Discovery from day one** — can implement llms.txt, full schema markup, and AI-friendly structure before launch, getting ahead of competitors.

### Threats (External)

- **Saturated skincare market** — skincare is one of the most competitive e-commerce categories. Established brands (CeraVe, The Ordinary, Paula's Choice) dominate search.
- **High customer acquisition cost** — skincare CAC is notoriously high due to competition. Organic SEO is critical to avoid paid acquisition dependency.
- **Established peptide skincare competitors** — brands like The Ordinary already sell peptide serums at low prices. Price competition is fierce.
- **Review bootstrapping challenge** — new store with zero reviews faces conversion rate disadvantage vs established competitors.
- **Google YMYL scrutiny** — skincare claims face the same YMYL (Your Money Your Life) algorithm scrutiny as health products. E-E-A-T requirements are high.
- **Platform dependency** — fully dependent on Shopify. Platform fee increases or policy changes could impact margins.

**Company SWOT connection:** Skingenetix's "sister brand leverage" strength is a specific instance
of the company's compounding advantage — each project builds on the last.
The "new brand, no traffic" weakness is expected for a setup-phase project
and mirrors the company's pre-revenue state.
The skincare market size opportunity is larger than Hairgenetix's hair care segment,
expanding the company's addressable market. See smith-ai-agency/docs/swot-analysis.md.
