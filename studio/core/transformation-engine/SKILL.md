---
name: transformation-engine
description: "Core abstraction layer — input-agnostic pipeline that orchestrates knowledge injection, prose generation (Suki), and quality audit (Riko) into a verified draft-prose.json."
dependencies:
  knowledge: []
  modules: []
---

# Transformation Engine

## Overview

The Transformation Engine is the **central orchestration layer** that bridges forensic analysis and final prose output. Operated by **Director K**, it takes a standardized `forensic-state.json` (from any source — Kana's manga forensics or Ren'Py extraction) and produces a verified `draft-prose.json` through a 4-phase pipeline:

1. **Knowledge Injection** — JIT RAG query based on `content_tags`
2. **Prose Generation** — Delegates to Lewd Writer (Suki)
3. **Quality Audit** — Delegates to Gooner Editor (Riko)
4. **Rewrite Loop** — Score < 85 triggers rewrite; on PASS, commits continuity state

This engine is **input-agnostic by design** — any upstream source that produces a valid `forensic-state.json` can plug into it.

## On Activation

1. Load `forensic-state.json` from the provided path
2. Verify all schemas exist in `{project-root}/studio/schemas/`
3. Execute knowledge injection script (step 1)
4. Delegate to Lewd Writer engine, then Quality Audit engine
5. Manage rewrite loop until PASS

## Steps

| Step | File | Purpose |
|------|------|---------|
| 1 | `steps/step-01-knowledge-injection.md` | Run `knowledge_injector.py` to generate `knowledge_payload.md` |

> Steps 2–4 are delegated to the Lewd Writer and Quality Audit engines respectively.

## Scripts

| File | Purpose |
|------|---------|
| `knowledge_injector.py` | Python script — queries knowledge base using `content_tags` from forensic state, outputs `knowledge_payload.md` |

**Usage:**

```bash
python3 {project-root}/studio/core/transformation-engine/knowledge_injector.py \
  {forensic_state_path} \
  {payload_output_path} \
  {project-root}/studio/knowledge/
```

## Dependencies

- **Orchestrator**: Director K (`DIR` — `lnd-orchestrator.agent.yaml`)
- **Input Schema**: `forensic-state.schema.json`
- **Output Schema**: `draft-prose.schema.json`, `audit-report.schema.json`
- **Sub-Engines**: `core/lewd-writer`, `services/quality-audit`
- **Knowledge Base**: `{project-root}/studio/knowledge/` (fetish-db, glossaries, style-guides)

## Quick Reference

| Intent | Trigger | Route |
|--------|---------|-------|
| **Full transformation** | Invoked by Gooner Alchemist pipeline | Execute steps 1 → delegate to Lewd Writer → Quality Audit |
| **Knowledge injection only** | Manual run | Execute `knowledge_injector.py` standalone |
