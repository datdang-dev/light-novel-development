---
name: gooner-alchemist
description: "Ultimate manga-to-prose adaptation pipeline — 8-step orchestrated flow from initialization through forensic analysis, prose generation, quality audit, to state persistence."
dependencies:
  knowledge:
    - path: "{project-root}/studio/knowledge/packs/narrative_style_pack.md"
    - path: "{project-root}/studio/knowledge/packs/fetish_guidance_pack.md"

  modules: []
---

# Gooner Alchemist Pipeline

## Overview

The Gooner Alchemist is the **primary pipeline** of LND Studio — the complete end-to-end manga adaptation engine. Orchestrated by **Director K**, it processes manga pages sequentially through 8 steps: initialization, context horizon check, forensic analysis, context loading (JIT compilation), prose generation, quality audit, state persistence, and completion handoff.

The pipeline is **state-persisted** — if a crash occurs at any step on any page, running `/gooner-alchemist` again resumes exactly where it left off. All intermediate artifacts are validated against strict JSON schemas.

## On Activation

1. Load pipeline context from `{project-root}/studio/config/pipeline-context.md`
2. Check `state.yaml` for existing session — resume if found
3. Verify all schemas in `{project-root}/studio/schemas/`
4. Load agent registry from `{project-root}/studio/agent-registry.csv`
5. Begin at `steps/step-01-initialize.md`

## Steps

| Step | File | Purpose |
|------|------|---------|
| 1 | `steps/step-01-initialize.md` | Initialize pipeline state, verify inputs |
| 1b | `steps/step-01b-context-horizon.md` | Context window budget check |
| 2 | `steps/step-02-forensic-analysis.md` | Delegate to Panel Forensic engine |
| 3 | `steps/step-03-context-loading.md` | JIT payload compilation |
| 4 | `steps/step-04-prose-generation.md` | Delegate to Lewd Writer engine |
| 5 | `steps/step-05-quality-audit.md` | Delegate to Quality Audit service |
| 6 | `steps/step-06-state-persistence.md` | Persist state, update continuity ledger |
| 7 | `steps/step-07-complete.md` | Handoff and page completion |

## Dependencies

- **Orchestrator**: Director K (`DIR` — `lnd-orchestrator.agent.yaml`)
- **Sub-Systems**: `core/panel-forensic`, `core/transformation-engine`, `core/lewd-writer`, `services/quality-audit`
- **Schemas**: `forensic-state.schema.json`, `draft-prose.schema.json`, `audit-report.schema.json`, `continuity-ledger.schema.json`
- **Config**: `config/pipeline-context.md`, `config/canon-rules.md`

## Quick Reference

| Intent | Trigger | Route |
|--------|---------|-------|
| **Full adaptation** | `/gooner-alchemist` | Load `steps/step-01-initialize.md` |
| **Resume** | `/gooner-alchemist` (auto-detects state) | Resume from last checkpoint |
| **YOLO mode** | `/gooner-alchemist --yolo` | Batch process without confirmation prompts |
