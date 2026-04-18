---
name: lewd-writer
description: "Core R18 prose generation engine — transforms forensic analysis into gooner-grade, sensory-saturated Vietnamese Light Novel prose via Suki agent. Use when the user says '/prose-adapter', '/lewd-writer', or 'write prose'."
dependencies:
  knowledge:
    - path: "{project-root}/studio/core/lewd-writer/knowledge/lewd_core_rules.md"
    - path: "{project-root}/studio/core/lewd-writer/knowledge/lewd_archetypes.md"
    - path: "{project-root}/studio/core/lewd-writer/knowledge/lewd_modules.md"
    - path: "{project-root}/studio/core/lewd-writer/knowledge/lewd_forensic_framework.md"
    - path: "{project-root}/studio/core/lewd-writer/knowledge/dialogue_playbook.md"

  modules: []
---

# Lewd Writer Engine

## Overview

The Lewd Writer is the **primary prose generation engine** of LND Studio. Operated by the **Suki** agent, it takes a completed `forensic-state.json` (from Panel Forensic) and an optional `knowledge_payload.md` (from Transformation Engine) and produces a `draft-prose.json` containing fully realized R18 Vietnamese Light Novel prose.

The engine enforces a 10-step sequential pipeline with strict escalation loops, sensory density requirements, and format compliance checks. Output is validated against `draft-prose.schema.json` before handoff to the Quality Audit engine.

## On Activation

1. Load config from `{project-root}/studio/config/config.yaml` (resolve `output_folder`, `communication_language`)
2. Load forensic state from the provided `forensic-state.json` path
3. Load knowledge payload from `knowledge_payload.md` (if available)
4. Load story bible and continuity ledger (if available)
5. Verify output schema exists at `{project-root}/studio/schemas/draft-prose.schema.json`
6. Begin at `steps/step-01-context-loading.md`

## Steps

| Step | File | Purpose |
|------|------|---------|
| 1 | `steps/step-01-context-loading.md` | Load forensic report, knowledge payload, and story bible context |
| 2 | `steps/step-02-scene-planning.md` | Plan scene structure, pacing, and escalation loops |
| 3 | `steps/step-03-environment-prose.md` | Write environmental atmosphere and spatial setup |
| 4 | `steps/step-04-dialogue-driven-action.md` | Generate dialogue-driven action sequences |
| 5b | `steps/step-05b-format-ensure.md` | **HARD GATE** — enforce light-novel-prose template format compliance |
| 5c | `steps/step-05c-sensory-injection.md` | Inject mandatory sensory markers (smell, touch, fluid, etc.) |
| 6 | `steps/step-06-aftermath-polish.md` | Write post-climax aftermath and lingering effects |
| 7 | `steps/step-07-quality-check.md` | Self-audit against quality gates before handoff |
| 8 | `steps/step-08-wiki-update.md` | Update character wiki/bible with new state |
| 9 | `steps/step-09-final-report.md` | Generate final prose report and `draft-prose.json` — **WORKFLOW COMPLETE** on output |

> **Note on 5b/5c naming:** These are intentionally sub-steps of a single quality enforcement phase. Step 5b is a hard gate — prose CANNOT proceed to 5c if format violations remain.

## Data Resources

| File | Purpose |
|------|---------|
| `data/gooner-manifesto.md` | Core writing philosophy and style guide |
| `data/onomatopoeia-library.md` | Vietnamese SFX/onomatopoeia reference |
| `data/sensory-vocabulary.md` | Sensory descriptor vocabulary bank |

## Dependencies

- **Agent**: Suki (`MOD` — `lewd-writer.agent.yaml`)
- **Input Schema**: `forensic-state.schema.json`
- **Output Schema**: `draft-prose.schema.json`
- **Modules**: `sfx-lookup`, `fetish-guidance`, `style-enforcer`
- **Upstream**: Panel Forensic → Transformation Engine → **Lewd Writer**
- **Downstream**: **Lewd Writer** → Quality Audit

## Quick Reference

| Intent | Trigger | Route |
|--------|---------|-------|
| **Full prose generation** | `/prose-adapter` | Load `steps/step-01-context-loading.md` |
| **Resume from step** | `/prose-adapter --resume` | Read frontmatter `stepsCompleted` and resume |
| **Modification pass** | Agent receives rewrite instructions from audit | Re-enter at step 4 with fix notes |
