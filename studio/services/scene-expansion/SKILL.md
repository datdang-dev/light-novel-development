---
name: scene-expansion
description: "Scene expansion service — transforms brief scene summaries or outlines into full R18 prose with escalation, sensory density, and character voice integration."
---

# Scene Expansion Service

## Overview

The Scene Expansion service transforms **brief scene summaries or outlines** into fully realized R18 prose. Operated by **Suki** (Lewd Writer), it takes minimal scene descriptions and expands them through escalation planning, environmental layering, action expansion, dialogue integration, and quality checking.

This is an alternative entry point to the Lewd Writer engine — while the standard pipeline starts from forensic analysis, Scene Expansion starts from human-written outlines or synopsis notes.

## On Activation

1. Load scene outline or summary input
2. Load character profiles and bible context (if available)
3. Begin at `steps/step-01-input-processing.md`

## Steps

| Step | File | Purpose |
|------|------|---------|
| 1 | `steps/step-01-input-processing.md` | Parse and validate input outline/summary |
| 2 | `steps/step-02-escalation-planning.md` | Plan escalation loops and pacing |
| 3 | `steps/step-03-environment-layer.md` | Build environmental atmosphere prose |
| 4 | `steps/step-04-action-expansion.md` | Expand action sequences with sensory detail |
| 5 | `steps/step-05-dialogue-integration.md` | Integrate character dialogue and SFX |
| 6 | `steps/step-06-quality-check.md` | Self-audit against quality gates |

## Dependencies

- **Agent**: Suki (`MOD` — `lewd-writer.agent.yaml`)
- **Modules**: `fetish-guidance`, `sfx-lookup`, `style-enforcer`
- **Downstream**: Quality Audit, Chapter Composer

## Quick Reference

| Intent | Trigger | Route |
|--------|---------|-------|
| **Expand scene** | `/scene-expansion` | Load `steps/step-01-input-processing.md` |
| **From outline file** | Provide outline path | Load and parse automatically |
