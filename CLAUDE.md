# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

LND Studio (Light Novel Development Studio) is a multi-agent AI framework for adapting Japanese R18 manga/light novels into Vietnamese prose. The system uses 16 specialized AI agents orchestrated by a central Director (Director K / lnd-orchestrator).

## GitNexus Integration

This project is indexed by GitNexus as **lnd_dev** (21,899 symbols, 44,872 relationships, 300 execution flows).

**Before editing any symbol:**
- Run `gitnexus_impact({target: "symbolName", direction: "upstream"})` to check blast radius
- Run `gitnexus_detect_changes()` before committing

**When exploring code:**
- Use `gitnexus_query({query: "concept"})` to find execution flows
- Use `gitnexus_context({name: "symbolName"})` for full symbol context

## Core Architecture

### Agent Personas (in `studio/agents/`)
- **Director K** (`lnd-orchestrator`): Central boss, owns pipelines, manages state.yaml
- **Dr. Atomic** (`panel-forensic`): Visual forensic analysis from images
- **Kana** (`manga-adapter`): Visual context specialist, generates POC hypotheses
- **Suki** (`lewd-writer`): R18 prose specialist, psychological depth, explicit tone
- **Riko** (`gooner-editor`): Quality auditor, grades drafts 0-100, forces rewrites

### Pipeline Services (in `studio/services/`)
- `gooner-alchemist/`: 8-step manga-to-prose pipeline (main workflow)
- `renpy-adaptation/`: Extracts AST from .rpy game scripts
- `quality-audit/`: QA gate using GOONER_AUDIT_FRAMEWORK
- `character-builder/`: Character description generation
- `novel-development/`: Full novel production pipeline

### Core Engines (in `studio/core/`)
- `lewd-writer/`: R18 prose generation engine
- `panel-forensic/`: Visual extraction and forensics
- `party-mode/`: Multi-agent CLI orchestration ("War Room")
- `transformation-engine/`: Content transformation pipeline
- `scene-prelude/`: Scene setup and context
- `volume-context-extractor/`: Volume-level context extraction

## Critical Rules

**Canon Rules** (`studio/config/canon-rules.md`) OVERRIDE everything:
1. **Output Language:** 100% Vietnamese narration/dialogue, Romaji/English SFX only
2. **Zero Hallucination:** Never invent objects/characters not in source
3. **Mandatory Explicit Vocabulary:** Use vulgar terms (cặc, lồn, địt, etc.)
4. **One Page = One File:** Strict 1:1 mapping

**Mandatory reads before writing prose:**
- `studio/config/canon-rules.md`
- `studio/rules/lewd_writing_mechanics.md`
- `studio/rules/sensory_density.md`
- `studio/rules/prose_structure.md`

## Folder Structure

```
studio/
├── agents/          # Agent YAML definitions (13 agents)
├── config/          # Global config: config.yaml, canon-rules.md, pipeline-context.md
├── core/            # Foundation engines (lewd-writer, panel-forensic, party-mode)
├── services/        # Business logic pipelines
├── modules/         # Utilities: sfx-lookup, fetish-guidance, gooner-audit-engine
├── rules/           # Writing rules (18 files): lewd mechanics, sensory density, POV rules
├── knowledge/       # Canonical databases: sfx/, glossaries/, fetish-db/
├── schemas/         # JSON schema contracts
├── docs/            # Architecture diagrams (.puml), LLM developer guide
├── context/         # Dynamic context files
├── shared/          # Cross-cutting concerns
├── scripts/         # Python utilities
└── output/          # Working output directory

_lnd-output/          # Finalized QA-approved chapters
sources/             # Source materials (manga, assets, etc.)
```

## Key Config Files

| File | Purpose |
|------|---------|
| `studio/config/config.yaml` | Session secrets, user settings |
| `studio/config/canon-rules.md` | Global hard rules (ALWAYS READ FIRST) |
| `studio/config/pipeline-context.md` | Master reference for agents |
| `studio/agents/agent-registry.yaml` | Agent capabilities registry |
| `studio/rules/lewd_writing_mechanics.md` | Explicit prose guidelines |
| `studio/rules/sensory_density.md` | Density constraints |

## Entry Points

When user wants to adapt content:
1. Check `sources/ENTRY_POINTS.md` for source-specific handlers
2. Identify content type: manga images, .rpy scripts, or existing text
3. Route to appropriate service in `studio/services/`

## Novel Development Output

Output novels are stored in `_lnd-output/_novels/{project_name}/` with structure:
- `char_desc_{name}.md`: Character descriptions
- `novel_chapter_XX.md`: QA-approved chapters
- Lore and context files

## Development Notes

- **Caption Engine CLI**: Execute visual ingestions or captions via the unified local model CLI:
  `PYTHONPATH=. python3 studio/core/caption_engine/caption_engine.py --image <path> --type <manga|long_thoughts_v2> [--no-stream]`
- **State Persistence:** Pipelines resume at crash point via `state.yaml`
- **Schema Locked:** All inter-agent communication uses JSON schemas
- **Decentralized Knowledge:** Lore/SFX in `knowledge/`, summoned via Vector Delta

## Shell Scripts

This project uses **PowerShell** on Windows (scripts in `studio/scripts/` and `.agent/skills/*/`). If you ported from WSL/bash:

- Replace `.sh` with `.ps1`
- Use `python` instead of `python3`
- Use `\` path separators instead of `/`
- Set execution policy: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`

**Available PowerShell scripts:**
- `studio/scripts/run_rewrite_chapter09.ps1` - Rewrite chapter via Hermes CLI
- `studio/scripts/run_suki_local.ps1` - Run Suki with forensic input
- `.agent/skills/axel-cowork/run.ps1` - Multi-agent review panel entry
- `.agent/skills/axel-cowork/axel-panel.ps1` - Axel panel CLI wrapper
- `.agent/skills/lnd-web-researcher/scripts/ensure_browser.ps1` - Chrome CDP bootstrap

<!-- gitnexus:start -->
# GitNexus — Code Intelligence

This project is indexed by GitNexus as **lnd_dev** (22198 symbols, 44738 relationships, 300 execution flows). Use the GitNexus MCP tools to understand code, assess impact, and navigate safely.

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

<!-- gitnexus:end -->
