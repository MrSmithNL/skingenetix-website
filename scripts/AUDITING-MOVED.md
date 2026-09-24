# The SEO / GEO / AISO auditor is not here

An audit script used to live in this directory. It was **deleted on 2026-09-24** because three
divergent copies existed across the agency, each scoring 2 models against a frozen criteria list.

**Use the one canonical auditor:**

```bash
cd ~/"Claude Code/Projects/seo-toolkit"
.venv/bin/python scripts/audit_page.py "<url>"
```

- **Skill (front door):** `~/.claude/skills/seo-aiso-validator/SKILL.md`
- **Engine:** `seo-toolkit/src/optimisation_engine/services/` — Claude + ChatGPT + Gemini +
  Perplexity in parallel, a criteria registry that learns from every run, page-type weighting
- **Docs:** `seo-toolkit/docs/SEO-AISO-AUDITING.md`
- **Archive of the retired scripts:** `~/.claude/archive/retired-audit-scripts-2026-09-24/`

**Do not write another local copy.** If the central tool cannot do what you need, extend it there —
every project gets the benefit, and the registry learns. (Rule 12, Rule 21.)
