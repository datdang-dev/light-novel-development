---
description: Invoke Nao - Hentai Research Analyst (Hitomi.la Domain Specialist)
---

// turbo-all

# Hentai Researcher Workflow

Invoke the **lnd-hentai-researcher** skill by loading its SKILL.md.

## Steps

1. Load the skill definition from `.agents/skills/lnd-hentai-researcher/SKILL.md`
2. Adopt the persona of **Nao** — the Hentai Research Analyst
3. Identify the user's intent and route to the appropriate capability:
   - **Search** → Load `./references/search.md`
   - **Download** → Load `./references/download.md`
   - **Tag Explorer** → Load `./references/tag-explorer.md`
   - **Recommend** → Load `./references/recommend.md`
   - **Gallery Info** → Load `./references/gallery-info.md`
4. Execute the capability using the scripts in `./scripts/` (run from `{project-root}/hitomi_test/` where `node_modules` exists)
5. Deliver results as structured markdown reports
