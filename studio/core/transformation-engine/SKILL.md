---
name: transformation-engine
description: "Director K's orchestration layer — takes forensic-state.json from any upstream source (manga forensics, Ren'Py extraction), runs knowledge injection, delegates to lewd-writer and quality-audit, manages rewrite loop until score >= 85. Input-agnostic; any source producing valid forensic-state.json can plug in."
owner: "datdang"
version: "1.0.0"
tags: [orchestration, pipeline, director, rewrite-loop, rag]
injection:
  always:
    - "{{project_root}}/studio/rules/canon-rules.md"
    - "{{project_root}}/studio/config/atmosphere_ledger.json"
  triggers:
    - scene_tag: "explicit|r18|adaptation|transformation"
      loads:
        - "{{project_root}}/studio/knowledge/packs/arousal_architecture.md"
        - "{{project_root}}/studio/rules/anti_slop.md"
dependencies:
  knowledge:
    - path: "{{project_root}}/studio/knowledge/packs/arousal_architecture.md"
    - path: "{{project_root}}/studio/knowledge/packs/r18_sensory_pack.md"
    - path: "{{project_root}}/studio/knowledge/packs/fetish_guidance_pack.md"
    - path: "{{project_root}}/studio/knowledge/glossaries/hentai_lexicon.md"
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
2. Verify all schemas exist in `{{project_root}}/studio/schemas/`
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
python3 {{project_root}}/studio/core/transformation-engine/knowledge_injector.py \
  {forensic_state_path} \
  {payload_output_path} \
  {{project_root}}/studio/knowledge/
```

## Dependencies

- **Orchestrator**: Director K (`DIR` — `lnd-orchestrator.agent.yaml`)
- **Input Schema**: `forensic-state.schema.json`
- **Output Schema**: `draft-prose.schema.json`, `audit-report.schema.json`
- **Sub-Engines**: `core/lewd-writer`, `services/quality-audit`
- **Knowledge Base**: `{{project_root}}/studio/knowledge/` (fetish-db, glossaries, style-guides)

## Quick Reference

| Intent | Trigger | Route |
|--------|---------|-------|
| **Full transformation** | Invoked by Gooner Alchemist pipeline | Execute steps 1 → delegate to Lewd Writer → Quality Audit |
| **Knowledge injection only** | Manual run | Execute `knowledge_injector.py` standalone |
