/*
 * Skingenetix (CLIENT-003) — Structurizr C4 workspace
 *
 * Phase 5 carry-forward C — multi-product C4 fan-out (2026-04-28).
 *
 * Skingenetix is the sister brand to Hairgenetix (CLIENT-002): same
 * owner, same Shopify-based commerce stack, different product line
 * (skincare vs. hair). Lighter operations footprint than Hairgenetix
 * (no audit reports archive yet — earlier in the lifecycle). Translation
 * uses Langify (not Translate & Adapt), email uses Klaviyo (planned).
 *
 * Source of truth. Hand-authored. Re-export via:
 *   python3 ~/Claude\ Code/Projects/smith-os/packages/forge/tools/architecture-artefacts/render_c4.py \
 *     ~/Claude\ Code/Projects/skingenetix-website
 */

workspace "skingenetix-website" "CLIENT-003 — Skingenetix brand operations: Shopify storefront + skincare product line + Langify localisation." {

    !identifiers hierarchical

    model {

        # ---- People ----

        customer = person "Customer" "Visitor / shopper across 9 languages. Sister-brand audience to Hairgenetix; skincare-focused."
        operator = person "Brand Operator" "Malcolm (and Smith AI Agency staff). Manages content drafts, scripts, translations, and Shopify Admin API operations."

        # ---- External Software Systems ----

        seoToolkit = softwareSystem "SEO Toolkit" "PROD-002 — Smith AI Agency's autonomous SEO/AISO audit + recommendation engine. Runs against the live storefront (planned next-step audit cadence)." {
            tags "External" "Smith Product"
        }
        hairgenetix = softwareSystem "Hairgenetix (sister brand)" "CLIENT-002 — sister Shopify brand. Skingenetix shares ownership, contact details, and operational patterns." {
            tags "External" "Smith Product"
        }
        shopifyPlatform = softwareSystem "Shopify Platform" "Hosted commerce platform. Provides storefront runtime, checkout, orders, inventory, customer accounts." {
            tags "External"
        }
        langify = softwareSystem "Langify" "Shopify translation app handling 9-language localisation. Note: different choice from Hairgenetix (Translate & Adapt) — pending consolidation." {
            tags "External"
        }
        klaviyo = softwareSystem "Klaviyo" "Planned email + marketing automation, mirroring Hairgenetix setup." {
            tags "External" "Planned"
        }
        searchEngines = softwareSystem "Search Engines" "Google + Bing — discover pages via sitemap, hreflang, structured data." {
            tags "External"
        }

        # ---- The Skingenetix Brand Operations system ----

        brand = softwareSystem "Skingenetix" "Brand operations: Shopify storefront + content/script/research workspace." {

            storefront = container "Shopify Storefront" "The live customer-facing site. Sense or Refresh theme (TBD) + 9 locales via Langify. Hosted on Shopify." "Shopify Liquid + JSON Templates" {
                tags "Web App"
            }

            docsSite = container "Operations Docs Site" "MkDocs Material site (encrypted). Strategy, architecture, decisions, accounts. Deployed at mrsmithnl.github.io/skingenetix-website/." "MkDocs Material + encryptcontent" {
                tags "Web App"
            }

            contentDrafts = container "Content Drafts" "Markdown drafts for product pages + product descriptions before publish. Source for Shopify GraphQL imports." "Markdown (content/)" {
                tags "Static Asset"
            }

            scriptsDir = container "Shopify Scripts" "Python scripts for Shopify Admin API automation: product imports, content sync, translation push, asset upload." "Python 3 / Shopify Admin GraphQL" {
                tags "CLI Tool"
            }

            researchDir = container "Research Notes" "Technical research and analysis (theme picks, app comparisons, content strategy). Pre-decision input feeding decisions-log." "Markdown (research/)" {
                tags "Static Asset"
            }
        }

        # ---- Relationships: People ↔ Containers ----

        customer -> brand.storefront "Browses + purchases skincare products" "HTTPS"
        operator -> brand.docsSite "Reviews strategy / decisions / setup" "HTTPS"
        operator -> brand.contentDrafts "Authors product / page content" "Editor"
        operator -> brand.scriptsDir "Runs Shopify operations" "CLI"
        operator -> brand.researchDir "Captures research before decisions" "Editor"

        # ---- Relationships: Containers ↔ Internal ----

        brand.scriptsDir -> brand.storefront "Imports products, syncs translations, uploads assets" "Shopify Admin GraphQL"
        brand.contentDrafts -> brand.scriptsDir "Source for content sync" "File read"
        brand.researchDir -> brand.docsSite "Promoted into decisions-log when decisions are made" "Markdown"

        # ---- Relationships: Containers ↔ External Systems ----

        brand.storefront -> shopifyPlatform "Hosted by; checkout + orders handled by" "Shopify-managed"
        brand.storefront -> langify "Reads localised content via" "Shopify app"
        brand.storefront -> klaviyo "Emits customer events for email automation (planned)" "Klaviyo SDK"
        searchEngines -> brand.storefront "Crawl + index for organic discovery" "HTTPS"

        seoToolkit -> brand.storefront "Audits live pages (planned cadence)" "HTTPS / crawler"
        hairgenetix -> brand.researchDir "Cross-brand learnings shared into research" "Process"
    }

    views {

        systemContext brand "SystemContext" "Who interacts with Skingenetix and what external systems it depends on." {
            include *
            autolayout lr
        }

        container brand "Containers" "The pieces that make up Skingenetix: live storefront + operations workspace." {
            include *
            autolayout lr
        }

        styles {
            element "Person" {
                shape Person
                background #08427b
                color #ffffff
            }
            element "Software System" {
                background #1168bd
                color #ffffff
            }
            element "External" {
                background #999999
                color #ffffff
            }
            element "Smith Product" {
                background #4b9c4b
                color #ffffff
            }
            element "Planned" {
                background #cccccc
                color #444444
            }
            element "Container" {
                background #438dd5
                color #ffffff
            }
            element "Web App" {
                shape WebBrowser
            }
            element "Static Asset" {
                shape Folder
            }
            element "CLI Tool" {
                shape Hexagon
            }
        }

        theme default
    }

}
