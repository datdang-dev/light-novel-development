---
name: rpg-adapter
description: "RPG game log adaptation pipeline — processes RPG Maker game logs and translation scripts into context routing for world/character foundation and novel loop."
---

# RPG Adapter Pipeline

## Overview

The RPG Adapter is a **V1 pipeline** for adapting RPG Maker game content into light novel prose. It processes game logs and translation scripts through context routing to establish world/character foundations, then feeds into the standard novel generation loop.

This pipeline is in early development — currently containing reference documentation only.

## On Activation

1. Load RPG game log or translation script
2. Reference workflow documentation in `references/`
3. Route to appropriate processing path

## Structure

| Path | Purpose |
|------|---------|
| `references/` | Pipeline documentation and reference materials |

> **Note**: Step files are not yet implemented. This pipeline currently operates from reference documentation.

## Dependencies

- **Orchestrator**: Director K (`DIR` — `lnd-orchestrator.agent.yaml`)
- **Tools**: `{project-root}/studio/tools/RPG-Maker-MV-Decrypter/` (for encrypted game asset extraction)
- **Downstream**: Transformation Engine (once forensic state is produced)

## Quick Reference

| Intent | Trigger | Route |
|--------|---------|-------|
| **Adapt RPG game** | Provide game log/script | Load reference documentation |
| **Decrypt RPG assets** | Use decrypter tool | `tools/RPG-Maker-MV-Decrypter/` |
