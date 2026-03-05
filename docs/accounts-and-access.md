# Accounts & Access — Skingenetix (CLIENT-003)

**Rule:** NO passwords or tokens in this file. Only references to where they're stored.

---

## Platforms & Accounts

| Service | URL | Account Holder | Use Case | Credentials Storage |
|---------|-----|---------------|----------|-------------------|
| Shopify | TBD | Malcolm Smith | Store platform + hosting | Bitwarden |
| OpenDomainRegistry | opendomainregistry.net | Malcolm Smith | Domain registrar | Bitwarden |
| GoDaddy | godaddy.com | Malcolm Smith | Email hosting | Bitwarden |
| Langify | (Shopify app) | Via Shopify | Translation (9 languages) | Via Shopify OAuth |
| Klaviyo | klaviyo.com | Malcolm Smith | Email marketing + reviews | Bitwarden |
| Kaching | (Shopify app) | Via Shopify | Product bundles | Via Shopify OAuth |
| Google Analytics | analytics.google.com | Malcolm Smith | Traffic analytics | Google account |
| Google Ads | ads.google.com | Malcolm Smith | Ad tracking | Google account |
| Facebook/Meta | business.facebook.com | Malcolm Smith | Social ad tracking | Bitwarden |

## API Keys & Integrations

| Service | Key Type | Status | Storage | Purpose |
|---------|---------|--------|---------|---------|
| Shopify Admin API | Access token (custom app) | 🔜 Pending | Bitwarden | Claude Code store management |
| Klaviyo | API key | 🔜 Pending | Bitwarden | Email automation |
| Google Analytics | Measurement ID | 🔜 Pending | Bitwarden | Analytics tracking |

## Shared Accounts with Hairgenetix

The following accounts are shared with the Hairgenetix (CLIENT-002) store:
- Shopify account (same owner, separate stores)
- Google Analytics (separate property)
- Klaviyo (separate account or separate list)
- GoDaddy hosting (multi-domain)

## TBD Items

- [ ] Shopify store URL once created
- [ ] Exact domain name (skingenetix.com / skingenetix.nl / other)
- [ ] Custom app client ID (stored in Bitwarden after creation)
- [ ] GA4 measurement ID
