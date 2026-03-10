# Security Risk Log — Skingenetix (CLIENT-003)

## Active Risks

| ID       | Risk                                            | Likelihood | Impact | Mitigation                                                                                                      | Status       |
| -------- | ----------------------------------------------- | ---------- | ------ | --------------------------------------------------------------------------------------------------------------- | ------------ |
| RISK-001 | Shopify API token compromise                    | Low        | High   | Token stored in Bitwarden only, never in git. Minimum required scopes. If compromised: delete app and recreate. | ⚠️ Mitigated |
| RISK-002 | Image URL changes break Langify translations    | Medium     | Medium | Document naming convention. Never rename/re-upload originals.                                                   | ⚠️ Mitigated |
| RISK-003 | Theme update breaks custom additions            | Low        | Medium | Never modify core Liquid files. Only additive sections/CSS. Annotate all custom code.                           | ⚠️ Mitigated |
| RISK-004 | Translation quality for medical/skincare claims | Medium     | High   | AI-generated translations reviewed by human before publishing. Legal claims flagged for professional review.    | ⚠️ Mitigated |

## Resolved Risks

| ID         | Risk | Resolution | Date |
| ---------- | ---- | ---------- | ---- |
| (none yet) |      |            |      |

## Security Principles

1. All credentials in Bitwarden — never in git, never in plain text files
2. API token scoped to minimum required permissions
3. Custom app token cannot be rotated — must delete and recreate if compromised
4. hCaptcha on all public forms
5. HTTPS enforced by Shopify (automatic)
