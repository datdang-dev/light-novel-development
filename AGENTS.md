<!-- gitnexus:start -->
# GitNexus — Code Intelligence

This project is indexed by GitNexus as **lnd_dev** (21899 symbols, 44872 relationships, 300 execution flows). Use the GitNexus MCP tools to understand code, assess impact, and navigate safely.

> If any GitNexus tool warns the index is stale, run `npx gitnexus analyze` in terminal first.

## Always Do

- **MUST run impact analysis before editing any symbol.** Before modifying a function, class, or method, run `gitnexus_impact({target: "symbolName", direction: "upstream"})` and report the blast radius (direct callers, affected processes, risk level) to the user.
- **MUST run `gitnexus_detect_changes()` before committing** to verify your changes only affect expected symbols and execution flows.
- **MUST warn the user** if impact analysis returns HIGH or CRITICAL risk before proceeding with edits.
- When exploring unfamiliar code, use `gitnexus_query({query: "concept"})` to find execution flows instead of grepping. It returns process-grouped results ranked by relevance.
- When you need full context on a specific symbol — callers, callees, which execution flows it participates in — use `gitnexus_context({name: "symbolName"})`.

## Never Do

- NEVER edit a function, class, or method without first running `gitnexus_impact` on it.
- NEVER ignore HIGH or CRITICAL risk warnings from impact analysis.
- NEVER rename symbols with find-and-replace — use `gitnexus_rename` which understands the call graph.
- NEVER commit changes without running `gitnexus_detect_changes()` to check affected scope.

## Resources

| Resource | Use for |
|----------|---------|
| `gitnexus://repo/lnd_dev/context` | Codebase overview, check index freshness |
| `gitnexus://repo/lnd_dev/clusters` | All functional areas |
| `gitnexus://repo/lnd_dev/processes` | All execution flows |
| `gitnexus://repo/lnd_dev/process/{name}` | Step-by-step execution trace |

## CLI

| Task | Read this skill file |
|------|---------------------|
| Understand architecture / "How does X work?" | `.claude/skills/gitnexus/gitnexus-exploring/SKILL.md` |
| Blast radius / "What breaks if I change X?" | `.claude/skills/gitnexus/gitnexus-impact-analysis/SKILL.md` |
| Trace bugs / "Why is X failing?" | `.claude/skills/gitnexus/gitnexus-debugging/SKILL.md` |
| Rename / extract / split / refactor | `.claude/skills/gitnexus/gitnexus-refactoring/SKILL.md` |
| Tools, resources, schema reference | `.claude/skills/gitnexus/gitnexus-guide/SKILL.md` |
| Index, status, clean, wiki CLI commands | `.claude/skills/gitnexus/gitnexus-cli/SKILL.md` |
| Work in the Scripts area (2381 symbols) | `.claude/skills/generated/scripts/SKILL.md` |
| Work in the Tts area (388 symbols) | `.claude/skills/generated/tts/SKILL.md` |
| Work in the Public area (225 symbols) | `.claude/skills/generated/public/SKILL.md` |
| Work in the Endpoints area (222 symbols) | `.claude/skills/generated/endpoints/SKILL.md` |
| Work in the Slash-commands area (105 symbols) | `.claude/skills/generated/slash-commands/SKILL.md` |
| Work in the Stable-diffusion area (95 symbols) | `.claude/skills/generated/stable-diffusion/SKILL.md` |
| Work in the Libs area (94 symbols) | `.claude/skills/generated/libs/SKILL.md` |
| Work in the Vectors area (89 symbols) | `.claude/skills/generated/vectors/SKILL.md` |
| Work in the Autocomplete area (72 symbols) | `.claude/skills/generated/autocomplete/SKILL.md` |
| Work in the Engine area (72 symbols) | `.claude/skills/generated/engine/SKILL.md` |
| Work in the Memory area (60 symbols) | `.claude/skills/generated/memory/SKILL.md` |
| Work in the Regex area (50 symbols) | `.claude/skills/generated/regex/SKILL.md` |
| Work in the Middleware area (49 symbols) | `.claude/skills/generated/middleware/SKILL.md` |
| Work in the Expressions area (49 symbols) | `.claude/skills/generated/expressions/SKILL.md` |
| Work in the Cluster_527 area (48 symbols) | `.claude/skills/generated/cluster-527/SKILL.md` |
| Work in the Quick-reply area (42 symbols) | `.claude/skills/generated/quick-reply/SKILL.md` |
| Work in the Cluster_530 area (38 symbols) | `.claude/skills/generated/cluster-530/SKILL.md` |
| Work in the Backends area (36 symbols) | `.claude/skills/generated/backends/SKILL.md` |
| Work in the Api area (35 symbols) | `.claude/skills/generated/api/SKILL.md` |
| Work in the Ui area (34 symbols) | `.claude/skills/generated/ui/SKILL.md` |

<!-- gitnexus:end -->
