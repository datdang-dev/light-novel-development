---
name: st-card-export
description: "SillyTavern character card export service — converts LND character profiles into SillyTavern V3 card format (JSON/PNG) with lorebooks."
dependencies:
  knowledge:
    - path: "{project-root}/studio/knowledge/packs/roleplay_st_pack.md"

  modules: []
---

# ST Card Export Service

## Overview

The ST Card Export service converts **LND character profiles** into SillyTavern-compatible character cards. Operated by **Tavvy** (SillyTavern Expert), it maps character bible fields to SillyTavern V3 card format, writes character descriptions optimized for roleplay, creates lorebook entries, and exports the final card package.

Cards can be exported as JSON or PNG (with embedded metadata) for direct import into SillyTavern or compatible roleplay platforms.

## On Activation

1. Load character profile from story bible
2. Load SillyTavern sidecar documentation from `{project-root}/studio/docs/sillytavern-expert-sidecar/`
3. Begin at `steps/step-01-load-profile.md`

## Steps

| Step | File | Purpose |
|------|------|---------|
| 1 | `steps/step-01-load-profile.md` | Load character profile and world context |
| 2 | `steps/step-02-map-fields.md` | Map profile fields to ST V3 card schema |
| 3 | `steps/step-03-write-description.md` | Write roleplay-optimized character description |
| 4 | `steps/step-04-create-lorebook.md` | Generate lorebook entries from world lore |
| 5 | `steps/step-05-export-card.md` | Export final card (JSON/PNG) |

## Dependencies

- **Agent**: Tavvy (`sillytavern-expert`)
- **Modules**: `sillytavern-export`
- **Knowledge**: `docs/sillytavern-expert-sidecar/`
- **Input**: Character profiles (from Character Builder)

## Quick Reference

| Intent | Trigger | Route |
|--------|---------|-------|
| **Export character** | `/st-card-export` | Load `steps/step-01-load-profile.md` |
| **Batch export** | Provide multiple character names | Process sequentially |
