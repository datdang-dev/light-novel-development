---
name: renpy-adaptation
description: "Ren'Py game-to-prose adaptation pipeline — extracts semantic models from Ren'Py scripts via AST mining and delegates to the standard prose generation flow."
---

# Ren'Py Adaptation Pipeline

## Overview

The Ren'Py Adaptation pipeline enables **visual novel game script adaptation** — an alternative input source to manga pages. Operated by the **Ren'Py Adapter** agent, it mines Ren'Py `.rpy` scripts via AST analysis, builds a semantic model of scenes/dialogue/choices, and then delegates to the standard Transformation Engine for prose generation.

This pipeline demonstrates the **input-agnostic design** of the Transformation Engine — any source that can produce a standardized `forensic-state.json` can feed into the prose generation flow.

## On Activation

1. Load Ren'Py script file(s) (`.rpy`)
2. Verify tools are available (`tools/` directory)
3. Begin at `steps/step-01-ast-mining.md`

## Steps

| Step | File | Purpose |
|------|------|---------|
| 1 | `steps/step-01-ast-mining.md` | Parse Ren'Py scripts and extract AST |
| 2 | `steps/step-02-semantic-model.md` | Build semantic model from AST data |
| 3 | `steps/step-03-delegate.md` | Convert to `forensic-state.json` and delegate to Transformation Engine |

## Tools

| Path | Purpose |
|------|---------|
| `tools/` | Ren'Py parsing and extraction utilities (3 tools) |
| `test_script.rpy` | Test script for validation |

## Dependencies

- **Agent**: Ren'Py Adapter (`renpy-adapter.agent.yaml`)
- **Output**: `forensic-state.json` (standard format)
- **Downstream**: Transformation Engine → Lewd Writer → Quality Audit

## Quick Reference

| Intent | Trigger | Route |
|--------|---------|-------|
| **Adapt Ren'Py game** | Provide `.rpy` file path | Load `steps/step-01-ast-mining.md` |
| **Test with sample** | Use built-in `test_script.rpy` | — |
