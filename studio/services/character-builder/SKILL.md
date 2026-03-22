---
name: character-builder
description: "High-fidelity character profile and world lore builder — creates psychological profiles and biographical data for R18 characters via Aria agent."
---

# Character Builder Service

## Overview

The Character Builder creates **high-fidelity psychological character profiles** and foundational world lore contexts. Operated by **Aria** (Character Architect), it guides users through a 2-step process: world-info creation followed by detailed character profiling including personality traits, physical descriptions, relationship dynamics, and fetish archetypes.

Output profiles are used by downstream services (Lewd Writer, Dialogue Scripting, ST Card Export) and are the authoritative character source of truth for the story bible.

## On Activation

1. Check for existing story bible at the project's bible path
2. Load any existing character profiles from `character-bible/` sub-directory
3. Begin at `steps/step-01-world-info.md`

## Steps

| Step | File | Purpose |
|------|------|---------|
| 1 | `steps/step-01-world-info.md` | Create/update world lore and setting context |
| 2 | `steps/step-02-character-profile.md` | Build detailed character profiles with psychology |

## Sub-Workflows

The `character-bible/` directory contains additional resources for character management.

## Dependencies

- **Agent**: Aria (`CB` — `character-architect.agent.yaml`)
- **Modules**: `fetish-guidance`, `sillytavern-export`
- **Downstream**: Bible Sync, ST Card Export, Lewd Writer

## Quick Reference

| Intent | Trigger | Route |
|--------|---------|-------|
| **Create character** | `/character-bible` | Load `steps/step-01-world-info.md` |
| **Edit existing** | Provide character name | Load existing profile, edit in step 2 |
