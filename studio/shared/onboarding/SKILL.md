---
name: onboarding
description: "Context grounding session — gives AI agents full project awareness before discussion, planning, or roleplay tasks. Use when the user says '/onboard', 'project onboarding', or 'load context'."
---

# Project Onboarding

## Overview

The Onboarding workflow grounds the current AI agent with comprehensive LND Studio project context. After completion, the agent can participate effectively in strategic discussions, architectural reviews, party-mode sessions, or roleplay.

All output is in **Vietnamese**.

## On Activation

1. Load config from `{project-root}/studio/config/config.yaml`
2. Execute the 6-step sequence below in order
3. Present onboarding summary and **HALT** for user input

## Steps

| Step | Name | What to Load |
|------|------|-------------|
| 1 | Studio Identity | `module.yaml`, `agent-registry.csv`, `config/pipeline-context.md` |
| 2 | World & Lore Context | `hentai_lexicon.md`, `fetish-db/README.md`, `gooner-manifesto.md` |
| 3 | Active Project State | Scan `{output_folder}/_pipeline/` for `state.yaml` |
| 4 | Character Bible | Scan `{output_folder}/_bible/` for character profiles |
| 5 | Writing Rules | Load `studio/rules/` files (lewd_writing_mechanics, sensory_density, dialogue_format, character_voice) |
| 6 | Summary | Present onboarding report and wait for user input |

## Expected Output

Each step produces a structured Vietnamese status block. Final output:

```text
✅ ONBOARDING HOÀN TẤT!
Tôi đã nắm bắt: Studio architecture, agents, lore, dự án hiện tại, bible, quy tắc viết.
```

## Dependencies

- **Config**: `module.yaml`, `agent-registry.csv`, `pipeline-context.md`
- **Knowledge**: `fetish-db/`, `hentai_lexicon.md`, `gooner-manifesto.md`
- **Rules**: `studio/rules/` (project-root level)
