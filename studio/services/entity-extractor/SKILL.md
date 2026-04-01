---
name: entity-extractor
description: "Structured character and entity data extraction from forensic reports — parses visual analysis to populate story bible entries."
dependencies:
  knowledge: []
  modules: []
---

# Entity Extractor Service

## Overview

The Entity Extractor parses **forensic reports** to extract structured character data, physical descriptions, relationship indicators, and state information. Operated by **Director K**, it bridges the gap between raw forensic analysis and the story bible, automatically populating character entries from visual evidence.

This service is particularly useful for first-pass character discovery when adapting a new manga — it identifies all characters, their physical attributes, and inter-character dynamics from the forensic data.

## On Activation

1. Load forensic reports from the specified path
2. Check existing story bible for known characters
3. Begin at `steps/step-01-load-forensics.md`

## Steps

| Step | File | Purpose |
|------|------|---------|
| 1 | `steps/step-01-load-forensics.md` | Load and parse forensic report data |
| 2 | `steps/step-02-character-extraction.md` | Extract character identities and physical traits |
| 3 | `steps/step-03-relationship-mapping.md` | Map character relationships and dynamics |
| 4 | `steps/step-04-state-compilation.md` | Compile state data (outfits, injuries, fluids) |
| 5 | `steps/step-05-output-generation.md` | Generate structured output for bible population |

## Dependencies

- **Orchestrator**: Director K (`DIR` — `lnd-orchestrator.agent.yaml`)
- **Input**: Forensic state reports (from Panel Forensic)
- **Downstream**: Character Builder, Bible Sync

## Quick Reference

| Intent | Trigger | Route |
|--------|---------|-------|
| **Extract entities** | `/entity-extractor` | Load `steps/step-01-load-forensics.md` |
| **Batch extraction** | Provide directory of forensic reports | Process all sequentially |
