# Processes & Flows — Skingenetix (CLIENT-003)

---

## Adding a New Product

```
1. Claude creates product via GraphQL Admin API
   - Title, description, images, variants, pricing
   - Metafields for custom data
   - SEO meta title and description

2. Claude generates translations (AI-assisted)
   - 9 languages × all text fields
   - Registered via translationsRegister mutation

3. Claude adds product to collection(s)
   - Via GraphQL collectionAddProducts

4. Malcolm reviews in Shopify admin
   - Visual check
   - Price verification
   - Translation quality spot-check

5. Malcolm uploads translated images (if needed)
   - In Langify → Products → Images
   - Only needed if images contain text
```

## Updating Existing Content

```
1. Claude edits via GraphQL Admin API
2. Claude updates translations for changed text
3. Changes are live immediately (no deploy needed)
```

## Theme Changes

```
1. Claude edits JSON settings or adds custom CSS
   - via Theme API or direct file edit
2. Theme Check validation run
3. Malcolm previews in theme editor
4. Malcolm publishes (or Claude does if pre-approved)
```

## Translation Workflow

```
Text content:
  Claude creates English → generates translations → registers via API → Malcolm reviews

Media content:
  Claude uploads original images → Malcolm creates translated versions → Malcolm uploads in Langify UI
```

## Monthly Maintenance

```
1. Claude: SEO audit (broken links, meta gaps, ranking changes)
2. Claude: Content freshness check (outdated info, seasonal updates)
3. Malcolm: Review Klaviyo email performance
4. Malcolm: Check app updates in Shopify admin
5. Malcolm: Financial reconciliation
```
