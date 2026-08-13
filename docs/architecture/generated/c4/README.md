<!-- markdownlint-disable MD013 -->

# skingenetix-website — C4 Architecture (auto-generated)

> **Auto-generated** by `smith-os/packages/forge/tools/architecture-artefacts/render_c4.py`.
> **Do not hand-edit.** Re-run the generator to refresh.
>
> - Generated: `2026-04-28 15:24 UTC`
> - Source: [`../workspace.dsl`](../../workspace.dsl)
> - Views: 2
>
> Phase 5 carry-forward A — Structurizr C4 DSL.
> See [structurizr-plan.md](https://github.com/MrSmithNL/smith-ai-agency/blob/main/docs/ecosystem-reorganisation/structurizr-plan.md).

## Views

| View                               | Slug             | Nodes | Edges |
| ---------------------------------- | ---------------- | ----- | ----- |
| [Container](containers.md)         | `containers`     | 13    | 14    |
| [SystemContext](system-context.md) | `system-context` | 9     | 8     |

## What is C4?

The [C4 model](https://c4model.com) is a hierarchical architecture documentation
notation: System Context → Containers → Components → Code. Authored as
[Structurizr DSL](https://docs.structurizr.com/dsl) and exported to mermaid via
[Structurizr CLI](https://github.com/structurizr/cli) (pinned v2025.11.09).

C4 captures **architectural intent** — what the system _is meant to be_. Its
sister artefact `dependency-graph.md` captures the **import-derived shape** —
what the code currently _is_ — and the two together close Layer 3 of the
research-03 three-layer model. That graph is **not generated for this repo**:
Skingenetix is a documentation and automation repo with no application source
tree to derive imports from, so only the C4 half exists here.

## How to regenerate

```bash
python3 ~/Claude\ Code/Projects/smith-os/packages/forge/tools/architecture-artefacts/render_c4.py \
  ~/Claude\ Code/Projects/skingenetix-website
```
