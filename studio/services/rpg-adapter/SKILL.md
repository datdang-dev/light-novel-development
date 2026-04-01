---
name: rpg-adapter
description: "RPG Maker MV/MZ game-to-novel adaptation pipeline — extracts dialogue, characters, and world data from game files to generate light novel prose. Supports data-only mode (no playthrough log required). Use when the user says 'adapt RPG game', 'process game log', 'RPG to novel', or 'extract game events'."
dependencies:
  knowledge: []
  modules: []
---

# RPG Adapter Pipeline

## Overview

The RPG Adapter is a pipeline for adapting **RPG Maker MV/MZ** game content into R18 light novel prose. It works in two modes:

- **Data-Only Mode** (recommended): Extracts directly from `Map*.json`, `CommonEvents.json`, `Actors.json`, and `ManualTransFile.json` — no playthrough log needed.
- **Log-Assisted Mode**: Uses a TimelineLogger.js playthrough log for scene ordering (optional enhancement).

## On Activation

1. Ask user for game root path
2. Auto-detect engine version (MV `www/data/` vs MZ flat `data/`)
3. Reference workflow documentation in `./references/`
4. Route to appropriate processing path

## Structure

| Path | Purpose |
|------|---------|
| `./references/` | Pipeline documentation and reference materials |
| `./steps/` | Progressive step files for the 3-phase pipeline |
| `./scripts/` | Deterministic Python utilities for data processing |

## Scripts

| Script | Purpose |
|--------|---------|
| `./scripts/validate_game_structure.py` | Validate RPG Maker directory structure (MV + MZ) |
| `./scripts/build_map_index.py` | Build map lookup index from MapInfos.json |
| `./scripts/extract_character_events.py` | **Core tool** — extract all events for a specific character across all maps + CommonEvents |
| `./scripts/parse_playthrough_log.py` | Parse TimelineLogger.js logs (optional, log-assisted mode only) |

## Dependencies

- **Orchestrator**: Director K (`DIR` — `lnd-orchestrator.agent.yaml`)
- **Downstream**: lewd-writer (Suki), character-architect (Aria), world-weaver (Luna)

## Quick Reference

| Intent | Trigger | Route |
|--------|---------|-------|
| **Adapt RPG game** | Provide game path | Load `./steps/step-01-initialize.md` |
| **Extract character** | Provide actor name/ID | Run `./scripts/extract_character_events.py` |
| **Decrypt assets** | Need encrypted images | See studio tools (RPG-Maker-MV-Decrypter) |
