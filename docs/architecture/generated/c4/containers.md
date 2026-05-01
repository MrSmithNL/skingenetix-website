<!-- markdownlint-disable MD013 -->

# skingenetix-website — Container (auto-generated C4)

> **Auto-generated** by `smith-os/packages/forge/tools/architecture-artefacts/render_c4.py`.
> **Do not hand-edit.** Re-run the generator to refresh.
>
> - Generated: `2026-04-28 15:24 UTC`
> - View: `Container` (slug `containers`)
> - Nodes: 13
> - Subgraphs: 2
> - Edges: 14
>
> Source: [`workspace.dsl`](../../workspace.dsl). Phase 5 carry-forward A
> ([structurizr-plan.md](https://github.com/MrSmithNL/smith-ai-agency/blob/main/docs/ecosystem-reorganisation/structurizr-plan.md)).

```mermaid
graph LR
  linkStyle default fill:#ffffff

  subgraph diagram ["Container View: Skingenetix"]
    style diagram fill:#ffffff,stroke:#ffffff

    1["<div style='font-weight: bold'>Customer</div><div style='font-size: 70%; margin-top: 0px'>[Person]</div><div style='font-size: 80%; margin-top:10px'>Visitor / shopper across 9<br />languages. Sister-brand<br />audience to Hairgenetix;<br />skincare-focused.</div>"]
    style 1 fill:#08427b,stroke:#052e56,color:#ffffff
    2["<div style='font-weight: bold'>Brand Operator</div><div style='font-size: 70%; margin-top: 0px'>[Person]</div><div style='font-size: 80%; margin-top:10px'>Malcolm (and Smith AI Agency<br />staff). Manages content<br />drafts, scripts,<br />translations, and Shopify<br />Admin API operations.</div>"]
    style 2 fill:#08427b,stroke:#052e56,color:#ffffff
    3("<div style='font-weight: bold'>SEO Toolkit</div><div style='font-size: 70%; margin-top: 0px'>[Software System]</div><div style='font-size: 80%; margin-top:10px'>PROD-002 — Smith AI Agency's<br />autonomous SEO/AISO audit +<br />recommendation engine. Runs<br />against the live storefront<br />(planned next-step audit<br />cadence).</div>")
    style 3 fill:#4b9c4b,stroke:#346d34,color:#ffffff
    4("<div style='font-weight: bold'>Hairgenetix (sister brand)</div><div style='font-size: 70%; margin-top: 0px'>[Software System]</div><div style='font-size: 80%; margin-top:10px'>CLIENT-002 — sister Shopify<br />brand. Skingenetix shares<br />ownership, contact details,<br />and operational patterns.</div>")
    style 4 fill:#4b9c4b,stroke:#346d34,color:#ffffff
    5("<div style='font-weight: bold'>Shopify Platform</div><div style='font-size: 70%; margin-top: 0px'>[Software System]</div><div style='font-size: 80%; margin-top:10px'>Hosted commerce platform.<br />Provides storefront runtime,<br />checkout, orders, inventory,<br />customer accounts.</div>")
    style 5 fill:#999999,stroke:#6b6b6b,color:#ffffff
    6("<div style='font-weight: bold'>Langify</div><div style='font-size: 70%; margin-top: 0px'>[Software System]</div><div style='font-size: 80%; margin-top:10px'>Shopify translation app<br />handling 9-language<br />localisation. Note: different<br />choice from Hairgenetix<br />(Translate & Adapt) — pending<br />consolidation.</div>")
    style 6 fill:#999999,stroke:#6b6b6b,color:#ffffff
    7("<div style='font-weight: bold'>Klaviyo</div><div style='font-size: 70%; margin-top: 0px'>[Software System]</div><div style='font-size: 80%; margin-top:10px'>Planned email + marketing<br />automation, mirroring<br />Hairgenetix setup.</div>")
    style 7 fill:#cccccc,stroke:#8e8e8e,color:#444444
    8("<div style='font-weight: bold'>Search Engines</div><div style='font-size: 70%; margin-top: 0px'>[Software System]</div><div style='font-size: 80%; margin-top:10px'>Google + Bing — discover<br />pages via sitemap, hreflang,<br />structured data.</div>")
    style 8 fill:#999999,stroke:#6b6b6b,color:#ffffff

    subgraph 9 ["Skingenetix"]
      style 9 fill:#ffffff,stroke:#0b4884,color:#0b4884

      10["<div style='font-weight: bold'>Shopify Storefront</div><div style='font-size: 70%; margin-top: 0px'>[Container: Shopify Liquid + JSON Templates]</div><div style='font-size: 80%; margin-top:10px'>The live customer-facing<br />site. Sense or Refresh theme<br />(TBD) + 9 locales via<br />Langify. Hosted on Shopify.</div>"]
      style 10 fill:#438dd5,stroke:#2e6295,color:#ffffff
      11["<div style='font-weight: bold'>Operations Docs Site</div><div style='font-size: 70%; margin-top: 0px'>[Container: MkDocs Material + encryptcontent]</div><div style='font-size: 80%; margin-top:10px'>MkDocs Material site<br />(encrypted). Strategy,<br />architecture, decisions,<br />accounts. Deployed at<br />mrsmithnl.github.io/skingenetix-website/.</div>"]
      style 11 fill:#438dd5,stroke:#2e6295,color:#ffffff
      12["<div style='font-weight: bold'>Content Drafts</div><div style='font-size: 70%; margin-top: 0px'>[Container: Markdown (content/)]</div><div style='font-size: 80%; margin-top:10px'>Markdown drafts for product<br />pages + product descriptions<br />before publish. Source for<br />Shopify GraphQL imports.</div>"]
      style 12 fill:#438dd5,stroke:#2e6295,color:#ffffff
      13["<div style='font-weight: bold'>Shopify Scripts</div><div style='font-size: 70%; margin-top: 0px'>[Container: Python 3 / Shopify Admin GraphQL]</div><div style='font-size: 80%; margin-top:10px'>Python scripts for Shopify<br />Admin API automation: product<br />imports, content sync,<br />translation push, asset<br />upload.</div>"]
      style 13 fill:#438dd5,stroke:#2e6295,color:#ffffff
      14["<div style='font-weight: bold'>Research Notes</div><div style='font-size: 70%; margin-top: 0px'>[Container: Markdown (research/)]</div><div style='font-size: 80%; margin-top:10px'>Technical research and<br />analysis (theme picks, app<br />comparisons, content<br />strategy). Pre-decision input<br />feeding decisions-log.</div>"]
      style 14 fill:#438dd5,stroke:#2e6295,color:#ffffff
    end

    1-. "<div>Browses + purchases skincare<br />products</div><div style='font-size: 70%'>[HTTPS]</div>" .->10
    2-. "<div>Reviews strategy / decisions<br />/ setup</div><div style='font-size: 70%'>[HTTPS]</div>" .->11
    2-. "<div>Authors product / page<br />content</div><div style='font-size: 70%'>[Editor]</div>" .->12
    2-. "<div>Runs Shopify operations</div><div style='font-size: 70%'>[CLI]</div>" .->13
    2-. "<div>Captures research before<br />decisions</div><div style='font-size: 70%'>[Editor]</div>" .->14
    13-. "<div>Imports products, syncs<br />translations, uploads assets</div><div style='font-size: 70%'>[Shopify Admin GraphQL]</div>" .->10
    12-. "<div>Source for content sync</div><div style='font-size: 70%'>[File read]</div>" .->13
    14-. "<div>Promoted into decisions-log<br />when decisions are made</div><div style='font-size: 70%'>[Markdown]</div>" .->11
    10-. "<div>Hosted by; checkout + orders<br />handled by</div><div style='font-size: 70%'>[Shopify-managed]</div>" .->5
    10-. "<div>Reads localised content via</div><div style='font-size: 70%'>[Shopify app]</div>" .->6
    10-. "<div>Emits customer events for<br />email automation (planned)</div><div style='font-size: 70%'>[Klaviyo SDK]</div>" .->7
    8-. "<div>Crawl + index for organic<br />discovery</div><div style='font-size: 70%'>[HTTPS]</div>" .->10
    3-. "<div>Audits live pages (planned<br />cadence)</div><div style='font-size: 70%'>[HTTPS / crawler]</div>" .->10
    4-. "<div>Cross-brand learnings shared<br />into research</div><div style='font-size: 70%'>[Process]</div>" .->14

  end
```

## How to regenerate

```bash
python3 ~/Claude\ Code/Projects/smith-os/packages/forge/tools/architecture-artefacts/render_c4.py \
  ~/Claude\ Code/Projects/skingenetix-website
```
