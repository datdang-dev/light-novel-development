---
name: dialogue-scripting
description: "R18 dialogue and SFX generation service — creates degradation dialogue, voice-calibrated speech, and Japanese SFX mapping via Miki agent."
---

# Dialogue Scripting Service

## Overview

The Dialogue Scripting service generates **R18 dialogue and SFX** tailored to character voices and escalation dynamics. Operated by **Miki** (Dialogue Crafter), it takes forensic context and character profiles, calibrates to each character's voice archetype, maps escalation beats, generates crude/degrading dialogue, integrates Japanese SFX with Vietnamese onomatopoeia, and polishes for rhythm and pacing.

This service can run standalone or be invoked by the Lewd Writer engine during prose generation when dialogue requires specialist attention.

## On Activation

1. Load forensic state and character profiles
2. Reference voice calibration from story bible
3. Load SFX lookup module
4. Begin at `steps/step-01-context-load.md`

## Steps

| Step | File | Purpose |
|------|------|---------|
| 1 | `steps/step-01-context-load.md` | Load scene context and character data |
| 2 | `steps/step-02-voice-calibration.md` | Calibrate to character voice archetypes |
| 3 | `steps/step-03-escalation-mapping.md` | Map dialogue escalation beats |
| 4 | `steps/step-04-dialogue-generation.md` | Generate R18 dialogue lines |
| 5 | `steps/step-05-sfx-integration.md` | Integrate SFX and onomatopoeia |
| 6 | `steps/step-06-polish-review.md` | Polish rhythm, pacing, and review |

## Dependencies

- **Agent**: Miki (`DC` — `dialogue-crafter.agent.yaml`)
- **Modules**: `sfx-lookup`, `style-enforcer`
- **Upstream**: Panel Forensic (forensic state), Character Builder (profiles)
- **Consumer**: Lewd Writer (dialogue integration)

## Quick Reference

| Intent | Trigger | Route |
|--------|---------|-------|
| **Generate dialogue** | `/dialogue-generator` | Load `steps/step-01-context-load.md` |
| **SFX mapping only** | Reference `sfx-lookup` module directly | — |
