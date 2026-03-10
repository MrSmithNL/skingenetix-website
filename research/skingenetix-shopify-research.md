# Skingenetix Shopify Store — Research & Technical Plan

**Date:** 2026-03-05
**Status:** Research Phase
**Sister Brand Of:** Hairgenetix.com (same owner, same contact details)

---

## Table of Contents

1. [Hairgenetix Reference Analysis](#1-hairgenetix-reference-analysis)
2. [What Claude Code Can and Cannot Do on Shopify](#2-what-claude-code-can-and-cannot-do-on-shopify)
3. [Technical Architecture: How Claude Connects to Shopify](#3-technical-architecture-how-claude-connects-to-shopify)
4. [Translation Strategy](#4-translation-strategy)
5. [Image & Video Translation](#5-image--video-translation)
6. [Theme Selection & Customization](#6-theme-selection--customization)
7. [What Must Be Done Manually (Human Tasks)](#7-what-must-be-done-manually-human-tasks)
8. [What Claude Can Fully Automate](#8-what-claude-can-fully-automate)
9. [Plugin/App Recommendations](#9-pluginapp-recommendations)
10. [Pitfalls & Lessons Learned](#10-pitfalls--lessons-learned)
11. [Recommended Approach: Hybrid Model](#11-recommended-approach-hybrid-model)
12. [Implementation Phases](#12-implementation-phases)
13. [Sources](#13-sources)

---

## 1. Hairgenetix Reference Analysis

**Current Hairgenetix.com setup** (to replicate for Skingenetix where applicable):

| Component           | Hairgenetix Setup                                                                         |
| ------------------- | ----------------------------------------------------------------------------------------- |
| **Theme**           | Release - Satyam (premium Shopify Theme Store theme)                                      |
| **Languages**       | 9: English (primary), Dutch, German, French, Spanish, Swedish, Danish, Norwegian, Italian |
| **Translation App** | Langify                                                                                   |
| **Email Marketing** | Klaviyo (also handles reviews)                                                            |
| **Bundles**         | Kaching Bundles                                                                           |
| **Analytics**       | Google Analytics + Google Ads + Facebook Pixel                                            |
| **Form Security**   | hCaptcha                                                                                  |
| **Product Badges**  | Rimix Builder (badges + quantity discounts)                                               |
| **Base Currency**   | EUR (Netherlands-based)                                                                   |
| **Product Range**   | Peptide-based hair growth treatments, serums, mesotherapy kits                            |
| **Trust Elements**  | Money-back guarantee, 4.6★ (1,200+ reviews), clinical testing                             |

**Key structural pages:** Shop, Scientific Research, Learn, Guarantee, Reviews, Support

---

## 2. What Claude Code Can and Cannot Do on Shopify

### ✅ Claude CAN Do (via API/MCP)

| Capability                      | Method                         | Notes                                            |
| ------------------------------- | ------------------------------ | ------------------------------------------------ |
| **Create/edit/delete products** | GraphQL Admin API              | Full CRUD including variants, images, metafields |
| **Manage product variants**     | GraphQL Admin API              | Prices, inventory, SKUs, options                 |
| **Create/manage collections**   | GraphQL Admin API              | Custom and smart collections                     |
| **Create navigation menus**     | GraphQL `menuCreate` mutation  | Up to 3 levels of nesting                        |
| **Create/edit pages**           | GraphQL Admin API              | About, FAQ, policy pages etc.                    |
| **Manage blog posts**           | GraphQL Admin API              | Create, edit, schedule posts                     |
| **Upload images/files**         | GraphQL Admin API              | Product images, theme assets                     |
| **Manage customers**            | GraphQL Admin API              | Create, edit customer records                    |
| **Create/manage orders**        | GraphQL Admin API              | Generate orders, associate customers             |
| **Set metafields**              | GraphQL Admin API              | Custom data on any resource                      |
| **Register translations**       | GraphQL `translationsRegister` | Programmatic text translations                   |
| **Edit theme files**            | Theme API / Shopify CLI        | Liquid, CSS, JSON settings                       |
| **Validate themes**             | Theme Check via MCP            | Lint Liquid for errors                           |
| **Manage discounts**            | GraphQL Admin API              | Automatic and code-based discounts               |
| **Configure webhooks**          | GraphQL Admin API              | Real-time event notifications                    |
| **SEO settings**                | GraphQL Admin API              | Meta titles, descriptions, URL handles           |

### ❌ Claude CANNOT Do (Requires Human in Shopify Admin)

| Task                               | Why Manual                                     | One-Time or Ongoing?          |
| ---------------------------------- | ---------------------------------------------- | ----------------------------- |
| **Create the Shopify store**       | Requires account creation with email/payment   | One-time                      |
| **Set up Shopify Payments**        | KYC verification, bank details, identity check | One-time                      |
| **Connect domain**                 | DNS configuration + Shopify admin verification | One-time                      |
| **Install apps/plugins**           | Requires OAuth consent in browser              | One-time per app              |
| **Configure tax settings**         | Admin-only write (API is read-only for taxes)  | One-time                      |
| **Configure shipping zones/rates** | Complex admin-only settings                    | One-time (occasional updates) |
| **Set up checkout customization**  | Admin-only branding settings                   | One-time                      |
| **Activate payment methods**       | Requires provider authentication               | One-time per provider         |
| **Staff account management**       | Admin permissions and roles                    | As needed                     |
| **App configuration (initial)**    | Each app has its own settings UI               | One-time per app              |
| **Langify initial setup**          | OAuth install + language configuration         | One-time                      |
| **Klaviyo initial setup**          | Account connection + flow configuration        | One-time                      |
| **Theme purchase/install**         | Shopify Theme Store purchase flow              | One-time                      |

### ⚠️ Grey Area (Partial Automation)

| Task                    | What Claude Can Do                          | What Needs Human                                       |
| ----------------------- | ------------------------------------------- | ------------------------------------------------------ |
| **Theme customization** | Edit Liquid/JSON/CSS files programmatically | Visual preview and approval in theme editor            |
| **Translations**        | Register text translations via API          | Image/video translations need manual upload in Langify |
| **App settings**        | Some apps expose APIs Claude can use        | Most app configs need their own admin UI               |
| **Email templates**     | Edit Liquid notification templates          | Preview/test delivery needs manual check               |

---

## 3. Technical Architecture: How Claude Connects to Shopify

### Connection Method: Custom App + Admin API Access Token

**How it works:**

1. Malcolm creates a **Custom App** in Shopify Admin (Settings → Apps → Develop apps)
2. Grants the app the required **API access scopes** (products, collections, content, translations, themes, etc.)
3. Generates an **Admin API access token**
4. Token is stored in **Bitwarden** (never in git)
5. Claude uses this token to make GraphQL Admin API calls

**Important changes as of January 2026:**

- New custom apps must be created via the **Shopify Dev Dashboard** (not the old admin method)
- Uses **OAuth client credentials** instead of static access tokens
- All new apps **must use GraphQL** (REST is being deprecated)

### MCP Server Options

There are multiple Shopify MCP servers available:

| MCP Server                            | Purpose                                                          | Best For                                  |
| ------------------------------------- | ---------------------------------------------------------------- | ----------------------------------------- |
| **Shopify Dev MCP** (official)        | Development assistance — docs, API schemas, code generation      | Building the store initially              |
| **Shopify Storefront MCP** (official) | Live store data — catalog, cart, policies                        | Customer-facing AI features               |
| **GeLi2001/shopify-mcp** (community)  | Full Admin API access — products, customers, orders, collections | Day-to-day store management               |
| **Composio Shopify MCP**              | Managed integration with pre-built actions                       | Quick setup (note: deprecation announced) |

**Recommended approach:** Use the **community Admin API MCP server** (GeLi2001/shopify-mcp or similar) for day-to-day management, plus the **official Dev MCP** during initial build. Direct GraphQL calls via Bash/scripts for anything the MCP servers don't cover.

### Recommended API Scopes

```
write_products, read_products
write_themes, read_themes
write_content, read_content
write_translations, read_translations
write_customers, read_customers
write_orders, read_orders
write_inventory, read_inventory
write_discounts, read_discounts
write_menus, read_menus (navigation)
write_metaobjects, read_metaobjects
write_files, read_files
read_locales
read_shopify_payments_payouts (read-only for monitoring)
```

---

## 4. Translation Strategy

### The Core Question: Langify vs Shopify Native vs Hybrid

| Approach                                   | Pros                                                                                                                | Cons                                                                         |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| **Langify (same as Hairgenetix)**          | Consistency across brands, manual control over quality, media translation support, third-party app translation      | $17.50/month, all manual translations, URL-based image translation can break |
| **Shopify Translate & Adapt (native)**     | Free, 2 languages auto-translated free, deep Shopify Markets integration, API-compatible via `translationsRegister` | Limited auto-translate beyond 2 languages, less control than Langify         |
| **Hybrid: Native API + Langify for media** | Claude can push text translations via API, Langify handles image/video swaps                                        | Two systems to maintain, potential conflicts                                 |
| **Transcy or LangShop**                    | AI auto-translation, image translation built-in                                                                     | Different system from Hairgenetix, learning curve                            |

### Recommended: Langify (Consistency + Media Translation)

**Rationale:**

1. **Brand consistency** — Same system across both stores means the owner already knows how to use it
2. **Media translation** — Langify has built-in image and video translation that Shopify native doesn't
3. **Third-party app translation** — Langify can translate content from other apps (Klaviyo widgets, etc.)
4. **Manual quality control** — For a skincare brand, translation quality matters (legal claims, ingredient lists)

### How Claude Handles Translations

**Text content (products, pages, blogs, meta):**

- Claude creates all content in English first via the Admin API
- Claude then registers translations for all 9 languages using the GraphQL `translationsRegister` mutation
- Translations can be pre-generated using AI (DeepL/GPT) and then registered via API
- This means Claude handles 90%+ of text translation programmatically

**Process flow:**

```
Claude creates English content →
Claude generates translations (AI-assisted) →
Claude registers via translationsRegister API →
Malcolm/translator reviews in Langify UI for quality →
Langify handles the frontend language switching
```

**Limitation:** The `translationsRegister` mutation is NOT bulkable — each resource must be translated individually. For a store with 9 languages, this means 9 API calls per translatable resource. Manageable but worth knowing.

---

## 5. Image & Video Translation

### How It Works in Shopify

Shopify's native approach (as of late 2025): Theme section media and metafield file references can be localized per language/market. However, **product gallery images are NOT yet natively localizable** — the same product images show for all languages.

### How Langify Handles It

1. **Product images:** Upload translated versions in Langify's Products → Images section. Langify swaps images based on the customer's selected language.
2. **Banner/section images:** Upload translated images to Shopify Files, then use Langify's Custom Content to map original image URL → translated image URL.
3. **Videos:** Add the translated video URL to Langify's Custom Content section.

**Critical detail:** Image translation in Langify is **URL-based**. If you change the original image URL or filename, the translation link breaks and must be redone.

### What This Means for Claude-Driven Management

| Media Type                  | Claude's Role                 | Human's Role                                  |
| --------------------------- | ----------------------------- | --------------------------------------------- |
| Product images (original)   | Upload via API                | None                                          |
| Product images (translated) | Cannot automate in Langify    | Upload translated versions in Langify UI      |
| Banner images with text     | Cannot automate               | Design translated versions, upload in Langify |
| Video content               | Upload original via API       | Upload translated video URLs in Langify       |
| Image alt-text              | Register translations via API | Review for accuracy                           |

**Bottom line:** Image and video translations are the biggest area where human involvement is needed on an ongoing basis. Text translations can be almost fully automated; media translations cannot.

### Mitigation Strategies

1. **Minimize text on images** — Use Shopify's text overlay sections instead of baking text into images. This way the text is translatable via API and the image stays universal.
2. **Use icons/symbols** — Universal visual language reduces translation needs.
3. **Standardize image naming** — Use consistent naming convention (e.g., `hero-banner-en.jpg`, `hero-banner-nl.jpg`) to make manual uploads systematic.
4. **Create a translation asset checklist** — For each page, list which images need language variants.

---

## 6. Theme Selection & Customization

### Theme Options for Skingenetix

| Option                                  | Pros                                                              | Cons                                 |
| --------------------------------------- | ----------------------------------------------------------------- | ------------------------------------ |
| **Same theme as Hairgenetix (Release)** | Brand family consistency, already know the structure              | Premium cost, might look too similar |
| **Free: Sense**                         | Built for beauty/wellness, fresh aesthetic, product imagery focus | Less features than premium           |
| **Free: Refresh**                       | Bold visuals, storytelling, ingredient lists, certifications      | Newer, less community support        |
| **Free: Dawn**                          | Most popular, minimalist, great performance                       | Very common, might look generic      |
| **Different premium theme**             | Unique brand identity for Skingenetix                             | Learning new theme structure         |

### Recommended: Sense or Refresh (Free)

**Rationale:**

1. **Different visual identity** — Skingenetix should look distinct from Hairgenetix while sharing brand family values
2. **No custom code needed** — Free Shopify themes are built to Shopify 2.0 standards with full section/block architecture
3. **Claude-friendly** — Standard theme architecture means Claude can reliably edit JSON settings, Liquid files, and CSS
4. **Cost savings** — Free theme = no license cost, money goes to apps instead

### How Claude Customizes the Theme

**Safe, additive approach (best practice from community):**

1. **JSON settings files** — Claude edits `config/settings_data.json` and section JSON files to configure layout, colors, typography, content blocks. No Liquid editing needed for most customizations.
2. **Custom CSS** — For brand-specific styling, Claude adds CSS via the theme's custom CSS field or a dedicated `custom.css` asset. Never modifies core theme CSS.
3. **Section modifications** — If a section needs changes, Claude creates a **new section** rather than modifying existing ones. This prevents theme update conflicts.
4. **Annotation rule** — All Claude-written code is annotated with author, date, and purpose (per industry best practice).

**What Claude should NEVER do:**

- Modify core theme Liquid files directly
- Remove or rename existing theme sections
- Add inline JavaScript without proper async/defer
- Override theme editor settings with hardcoded values

---

## 7. What Must Be Done Manually (Human Tasks)

### One-Time Setup (Malcolm does these once)

| #   | Task                                                | Time Estimate | Notes                                          |
| --- | --------------------------------------------------- | ------------- | ---------------------------------------------- |
| 1   | Create Shopify account for Skingenetix              | 10 min        | New store, same Shopify account as Hairgenetix |
| 2   | Choose subscription plan                            | 5 min         | Same plan as Hairgenetix recommended           |
| 3   | Set up Shopify Payments (KYC)                       | 15-30 min     | Bank details, ID verification                  |
| 4   | Connect domain (skingenetix.com or similar)         | 15 min        | DNS settings                                   |
| 5   | Install apps: Langify, Klaviyo, Kaching, hCaptcha   | 10 min each   | OAuth consent per app                          |
| 6   | Configure Langify languages                         | 15 min        | Add same 9 languages                           |
| 7   | Configure tax settings                              | 10 min        | EU VAT, international rates                    |
| 8   | Configure shipping zones/rates                      | 20 min        | Copy from Hairgenetix logic                    |
| 9   | Set up checkout branding                            | 10 min        | Skingenetix logo/colors                        |
| 10  | Install theme (if free, auto; if premium, purchase) | 5 min         | Download from Theme Store                      |
| 11  | Create custom app for Claude API access             | 15 min        | Dev Dashboard, grant scopes, generate token    |
| 12  | Connect Google Analytics + Ads + FB Pixel           | 15 min        | Account linking                                |
| 13  | Configure Klaviyo email flows                       | 30 min        | Welcome, abandoned cart, post-purchase         |

**Total one-time human effort: ~3-4 hours**

### Ongoing Human Tasks

| Task                                       | Frequency                 | Why Human?                  |
| ------------------------------------------ | ------------------------- | --------------------------- |
| Review translated content for quality      | Per content batch         | Brand voice, legal accuracy |
| Upload translated images/videos in Langify | When new media is created | Langify UI only             |
| Approve theme visual changes               | When Claude makes changes | Visual judgment             |
| Monitor Klaviyo email performance          | Weekly                    | Strategic decisions         |
| Review and reply to customer reviews       | Daily/weekly              | Personal touch              |
| Financial reconciliation                   | Monthly                   | Business decisions          |
| App updates and compatibility checks       | Monthly                   | Admin UI only               |

---

## 8. What Claude Can Fully Automate

| Task                                         | Frequency                       | Method                               |
| -------------------------------------------- | ------------------------------- | ------------------------------------ |
| Create/update products with full details     | As needed                       | GraphQL Admin API                    |
| Generate product descriptions (multilingual) | Per product                     | AI generation + translationsRegister |
| Set up and manage collections                | As needed                       | GraphQL Admin API                    |
| Build navigation menus                       | Setup + changes                 | GraphQL `menuCreate`                 |
| Create content pages (About, FAQ, etc.)      | Setup + updates                 | GraphQL Admin API                    |
| Write and publish blog posts                 | As needed                       | GraphQL Admin API                    |
| SEO optimization (meta titles, descriptions) | Per page/product                | GraphQL Admin API                    |
| Upload product images                        | Per product                     | GraphQL Admin API                    |
| Set up discount codes                        | As needed                       | GraphQL Admin API                    |
| Configure metafields                         | As needed                       | GraphQL Admin API                    |
| Theme JSON settings adjustments              | As needed                       | Theme API                            |
| Custom CSS additions                         | As needed                       | Theme API                            |
| Translation registration (text)              | Per content piece × 9 languages | translationsRegister mutation        |
| Inventory management                         | As needed                       | GraphQL Admin API                    |
| Generate reports (orders, customers)         | On demand                       | GraphQL Admin API                    |

---

## 9. Plugin/App Recommendations

### Must-Have Apps (Same as Hairgenetix)

| App                 | Purpose                                        | Claude Can Manage?                  | Monthly Cost        |
| ------------------- | ---------------------------------------------- | ----------------------------------- | ------------------- |
| **Langify**         | Translations (9 languages) + media translation | Text via API, media needs UI        | ~$17.50             |
| **Klaviyo**         | Email marketing + reviews                      | Limited — has API but flows need UI | Free tier available |
| **Kaching Bundles** | Product bundles/discounts                      | Configuration needs UI              | ~$9.99+             |
| **hCaptcha**        | Form security                                  | One-time setup                      | Free                |

### Recommended Additional Apps

| App                  | Purpose                                               | Why                                  | Cost                |
| -------------------- | ----------------------------------------------------- | ------------------------------------ | ------------------- |
| **Shopify Flow**     | Workflow automation (order tagging, inventory alerts) | Free, reduces manual work            | Free (included)     |
| **Judge.me or Loox** | Product reviews (alternative to Klaviyo reviews)      | Better review display, photo reviews | Free tier available |
| **Rimix Builder**    | Badges + quantity discounts                           | Same as Hairgenetix                  | Varies              |

### Apps to AVOID

| Type                             | Why                                                                                 |
| -------------------------------- | ----------------------------------------------------------------------------------- |
| Page builders (Shogun, GemPages) | Add custom code complexity that breaks Claude's ability to manage the theme cleanly |
| Custom checkout apps             | Checkout is best kept standard for maintainability                                  |
| Multiple translation apps        | One translation system only — conflicts are common                                  |
| SEO apps with heavy JavaScript   | Performance impact; Claude can handle SEO via API directly                          |

---

## 10. Pitfalls & Lessons Learned

### From Community Experience with AI + Shopify

1. **"It works until it doesn't"** — AI-generated Liquid code often works initially but breaks on theme updates. **Mitigation:** Never modify core theme files. Only add new sections/snippets and use JSON settings.

2. **Translation conflicts** — Running multiple translation systems (e.g., Langify + Shopify native Translate & Adapt) causes display conflicts. **Mitigation:** Use ONE translation system only.

3. **URL-based image translations break** — Langify's image translation links to original image URLs. Renaming or re-uploading images breaks all translations. **Mitigation:** Establish naming conventions upfront and never change original image URLs.

4. **API rate limits** — Shopify has rate limits (40 requests/second for GraphQL). Bulk operations (translating many products) need throttling. **Mitigation:** Use bulk operations API where available; implement rate limiting in scripts.

5. **Theme editor vs code conflicts** — If Malcolm edits something in the visual theme editor AND Claude edits the same section via code, one overwrites the other. **Mitigation:** Clear ownership — Claude manages code files, Malcolm uses theme editor only for visual preview/approval.

6. **Custom app token rotation** — You can't rotate custom app API tokens. If compromised, you must delete and recreate the app. **Mitigation:** Store token in Bitwarden, never in git, restrict scopes to minimum needed.

7. **Product variant creation** — MCP servers create products with options but only generate one default variant. Must create variants separately. **Mitigation:** Use a two-step process — create product, then add all variant combinations.

8. **translationsRegister is not bulkable** — Each resource needs individual translation API calls. For 9 languages × many products, this adds up. **Mitigation:** Build a script that batches translations with rate limiting.

9. **Liquid syntax is fragile** — AI tools often generate Liquid code with subtle errors that pass basic checks but fail in edge cases. **Mitigation:** Always run Theme Check validation; test in preview before publishing.

10. **App settings live in app UI, not API** — Most Shopify apps don't expose their configuration via API. Langify settings, Klaviyo flows, Kaching bundle configs — all need their own admin panels. **Mitigation:** Accept this as "human territory" and document the settings clearly.

---

## 11. Recommended Approach: Hybrid Model

### The 80/20 Split

**Claude handles ~80% of store building and maintenance:**

- All product content creation and management
- All text translations (9 languages)
- Theme configuration via JSON/CSS (no core Liquid edits)
- Collections, navigation, pages, blog posts
- SEO settings
- Discount management
- Inventory updates
- Content updates and seasonal changes

**Humans handle ~20% (the parts that need eyes, hands, or legal authority):**

- One-time store setup (account, payments, domain, apps)
- Image/video translation uploads in Langify
- Visual approval of theme changes
- App configuration in their respective admin UIs
- Review response and customer service decisions
- Financial and strategic decisions
- Quality review of AI-generated translations

### Workflow Model

```
┌─────────────────────────────────────────────────────┐
│                  CLAUDE CODE                         │
│                                                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │
│  │ Products │  │ Content  │  │ Translations     │  │
│  │ CRUD     │  │ Pages    │  │ (text only)      │  │
│  │ Variants │  │ Blogs    │  │ 9 languages      │  │
│  │ Images   │  │ Menus    │  │ via GraphQL API  │  │
│  └────┬─────┘  └────┬─────┘  └────────┬─────────┘  │
│       │              │                  │            │
│  ┌────┴─────┐  ┌────┴─────┐  ┌────────┴─────────┐  │
│  │ Theme    │  │ SEO      │  │ Discounts &      │  │
│  │ Settings │  │ Meta     │  │ Promotions       │  │
│  │ JSON/CSS │  │ Tags     │  │ via GraphQL API  │  │
│  └──────────┘  └──────────┘  └──────────────────┘  │
│                                                      │
│  ══════════════ GraphQL Admin API ═══════════════   │
└─────────────────────┬───────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│              SHOPIFY STORE                           │
└─────────────────────┬───────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│                  HUMAN (Malcolm)                     │
│                                                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │
│  │ Store    │  │ App      │  │ Image/Video      │  │
│  │ Setup    │  │ Install  │  │ Translations     │  │
│  │ Payments │  │ & Config │  │ in Langify UI    │  │
│  │ Domain   │  │ UI       │  │                  │  │
│  └──────────┘  └──────────┘  └──────────────────┘  │
│                                                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │
│  │ Visual   │  │ Review   │  │ Strategic        │  │
│  │ Approval │  │ Quality  │  │ Decisions        │  │
│  │ of Theme │  │ Check    │  │ Pricing etc.     │  │
│  └──────────┘  └──────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────┘
```

---

## 12. Implementation Phases

### Phase 0: Pre-Setup (Human — ~1 hour)

- [ ] Register domain for Skingenetix
- [ ] Create Shopify store
- [ ] Choose subscription plan
- [ ] Set up Shopify Payments (KYC/bank)
- [ ] Connect domain

### Phase 1: Foundation (Human + Claude — ~2 hours human, Claude automated)

- [ ] **Human:** Install theme (Sense or Refresh recommended)
- [ ] **Human:** Install apps (Langify, Klaviyo, Kaching, hCaptcha)
- [ ] **Human:** Configure Langify with 9 languages
- [ ] **Human:** Create custom app in Dev Dashboard, generate API token, store in Bitwarden
- [ ] **Human:** Configure tax settings, shipping zones
- [ ] **Human:** Set up checkout branding
- [ ] **Claude:** Configure MCP server connection to new store
- [ ] **Claude:** Set up theme JSON settings (colors, typography, layout)
- [ ] **Claude:** Add custom CSS for Skingenetix brand identity

### Phase 2: Content & Products (Claude — mostly automated)

- [ ] **Claude:** Create all product listings with descriptions, images, variants, prices
- [ ] **Claude:** Set up collections (by product type, skin concern, etc.)
- [ ] **Claude:** Build navigation menus (main, footer)
- [ ] **Claude:** Create content pages (About, FAQ, Ingredients, Guarantee, Support)
- [ ] **Claude:** Write initial blog posts
- [ ] **Claude:** Configure SEO (meta titles, descriptions, handles)
- [ ] **Claude:** Set up metafields for any custom product data

### Phase 3: Translations (Claude + Human)

- [ ] **Claude:** Generate AI-assisted translations for all text content (9 languages)
- [ ] **Claude:** Register all translations via GraphQL API
- [ ] **Human:** Review translations for quality (especially legal/medical claims for skincare)
- [ ] **Human:** Upload translated images/videos in Langify
- [ ] **Human:** Review translated store in each language

### Phase 4: Polish & Launch (Collaborative)

- [ ] **Claude:** Final SEO audit and fixes
- [ ] **Claude:** Set up discount codes for launch
- [ ] **Human:** Configure Klaviyo email flows (welcome, abandoned cart, post-purchase)
- [ ] **Human:** Connect Google Analytics, Google Ads, Facebook Pixel
- [ ] **Human:** Test full purchase flow in each language
- [ ] **Human:** Final visual review and approval
- [ ] **Human:** Remove password page → Go live

### Phase 5: Ongoing Management (80% Claude, 20% Human)

- **Claude:** Product updates, new content, seasonal changes, translations, SEO
- **Claude:** Inventory management, discount management
- **Human:** Image/video translations, app config changes, customer service, strategic decisions

---

## 13. Sources

### Shopify API & Architecture

- [Shopify API Explained 2026](https://www.hellobizmia.com/insights/shopify-api) — API types and best practices
- [Shopify API Best Practices 2025](https://www.codersy.com/blog/shopify-api-development-best-practices) — GraphQL-first strategy
- [Shopify Custom App Deprecation 2026](https://datronixtech.com/shopify-custom-app-deprecation/) — Dev Dashboard requirement
- [Shopify GraphQL Admin API Reference](https://shopify.dev/docs/api/admin-graphql) — Official API docs
- [menuCreate Mutation](https://shopify.dev/docs/api/admin-graphql/latest/mutations/menucreate) — Navigation menu API
- [Manage Translated Content](https://shopify.dev/docs/apps/build/markets/manage-translated-content) — Translation API docs

### AI/Claude + Shopify

- [Shopify Dev MCP Server](https://shopify.dev/docs/apps/build/devmcp) — Official development MCP
- [GeLi2001/shopify-mcp](https://github.com/GeLi2001/shopify-mcp) — Community Admin API MCP
- [Composio Shopify MCP](https://composio.dev/toolkits/shopify/framework/claude-code) — Managed MCP integration
- [AI Shopify Theme Customisation](https://seotldr.substack.com/p/ai-shopify-theme-customisation) — Pitfalls and best practices
- [AI for Shopify Theme Development](https://flagship.cc/en/blogs/columns/ai-for-shopify-theme-development) — Real-world experience
- [Advanced Prompting for Shopify Development](https://www.capaxe.com/blog/advanced-prompting-claude) — Claude-specific guidance
- [Shopify Winter '26 Edition Dev](https://www.shopify.com/news/winter-26-edition-dev) — AI-native development features

### Translation

- [Langify App](https://apps.shopify.com/langify) — Translation app used on Hairgenetix
- [Langify Media Translation](https://blog.langify-app.com/media-translation/) — Image/video translation guide
- [Langify Image Translation Support](https://support.langify-app.com/support/solutions/articles/11000082046-image-translations) — How image swapping works
- [Shopify Translate & Adapt](https://apps.shopify.com/translate-and-adapt) — Native Shopify translation
- [Top Shopify Translation Apps Comparison](https://transcy.io/blog/best-shopify-translation-apps/) — 2026 comparison
- [Shopify Media Localization Changelog](https://changelog.shopify.com/posts/online-store-media-localizable-to-different-languages-and-markets) — Native media support

### Themes

- [Best Beauty Shopify Themes 2026](https://tiny-img.com/best-shopify-themes/for-beauty-stores/) — Theme recommendations
- [Best Free Shopify Themes 2026](https://firebearstudio.com/blog/free-shopify-themes.html) — Free theme comparison
- [Shopify Beauty Stores Examples](https://www.omnisend.com/blog/shopify-beauty-stores/) — Inspiration

### Store Setup & Management

- [Shopify General Store Checklist](https://help.shopify.com/en/manual/intro-to-shopify/initial-setup/new-to-shopify-checklists/general-checklist) — Official setup guide
- [Shopify Store Duplication](https://help.shopify.com/en/manual/shopify-admin/duplicate-store) — Cloning limitations
- [Shopify Custom Apps](https://help.shopify.com/en/manual/apps/app-types/custom-apps) — API access setup
- [Shopify Access Scopes](https://shopify.dev/docs/api/usage/access-scopes) — API permissions guide
- [Shopify Payments Configuration](https://help.shopify.com/en/manual/payments/shopify-payments/configuring-shopify-payments) — Payment setup
- [Bulk Translation Operations Discussion](https://community.shopify.com/c/new-graphql-product-apis/bulk-operation-for-translations/td-p/2779268) — API limitation
