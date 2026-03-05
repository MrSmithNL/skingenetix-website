# Setup Steps — Skingenetix (CLIENT-003)

Every setup action is recorded here with reversal instructions.

---

## Completed Steps

| # | Date | Action | Who | How to Undo |
|---|------|--------|-----|-------------|
| 1 | 2026-03-05 | Created project folder and standard files | Claude Code | Delete folder: `rm -rf ~/Claude\ Code/Projects/skingenetix-website/` |

---

## Pending Steps (In Order)

### Step 2: Create Shopify Store
**Who:** Malcolm
**Action:** Log into Shopify admin → Create new store → Choose plan
**How to undo:** Settings → Plan → Pause or close store

### Step 3: Connect Domain
**Who:** Malcolm
**Action:** In Shopify admin: Settings → Domains → Connect existing domain. At OpenDomainRegistry: set A record to Shopify IP, CNAME `www` to `shops.myshopify.com`
**How to undo:** Remove DNS records at OpenDomainRegistry, remove domain in Shopify

### Step 4: Configure Email (MX Records)
**Who:** Malcolm
**Action:** Add domain to GoDaddy hosting. At OpenDomainRegistry: add MX records pointing to GoDaddy mail servers
**How to undo:** Remove MX records at OpenDomainRegistry, remove domain from GoDaddy

### Step 5: Set Up Shopify Payments
**Who:** Malcolm
**Action:** Settings → Payments → Shopify Payments → Complete setup
**How to undo:** Settings → Payments → Manage → Deactivate

### Step 6: Install Theme
**Who:** Malcolm
**Action:** Online Store → Themes → Visit Shopify Theme Store → Install free theme (Sense or Refresh)
**How to undo:** Online Store → Themes → switch back to default Dawn theme

### Step 7: Create Custom App (API Access for Claude)
**Who:** Malcolm
**Action:**
1. Go to Shopify Dev Dashboard (partners.shopify.com or dev.shopify.com)
2. Create new app
3. Grant API scopes (see CLAUDE.md for list)
4. Generate access token
5. Store token in Bitwarden as "Skingenetix Shopify API Token"
**How to undo:** Delete the app in Dev Dashboard

### Step 8: Install Apps
**Who:** Malcolm
**Action:** Visit Shopify App Store → Install each: Langify, Klaviyo, Kaching Bundles, hCaptcha
**How to undo:** Settings → Apps → Uninstall each app

### Step 9: Configure Langify Languages
**Who:** Malcolm
**Action:** Open Langify app → Add languages: Dutch, German, French, Spanish, Swedish, Danish, Norwegian, Italian
**How to undo:** Remove languages in Langify settings

### Step 10: Configure Tax & Shipping
**Who:** Malcolm
**Action:** Settings → Taxes and duties → Configure EU VAT. Settings → Shipping and delivery → Set zones and rates.
**How to undo:** Reset to default tax/shipping settings
