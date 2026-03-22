---
name: bible-sync
description: "Story bible and continuity state synchronization — manages LOAD and SAVE modes for character, relationship, and environmental state across adaptation sessions."
---

# Bible Sync Service

## Overview

Bible Sync manages **story bible persistence** and **continuity state synchronization** across manga adaptation sessions. Operated by **Director K**, it has two modes:

- **LOAD mode** — retrieves character profiles, relationship state, and environmental context from the story bible to establish session continuity
- **SAVE mode** — extracts changes from the current session and persists them back to the bible, logging events for audit trail

This ensures that character injuries, fluid state, outfit changes, and relationship dynamics carry forward consistently between pages and chapters.

## On Activation

1. Detect mode: LOAD or SAVE (from pipeline state or user input)
2. Load bible directory path from config
3. Route to appropriate step sequence

## Steps — LOAD Mode

| Step | File | Purpose |
|------|------|---------|
| L1 | `steps/load-01-mode-check.md` | Verify LOAD mode, locate bible path |
| L2 | `steps/load-02-load-characters.md` | Load character profiles and states |
| L3 | `steps/load-03-load-state.md` | Load environmental and continuity state |
| L4 | `steps/load-04-generate-context.md` | Generate session context payload |

## Steps — SAVE Mode

| Step | File | Purpose |
|------|------|---------|
| S1 | `steps/save-01-mode-check.md` | Verify SAVE mode, identify changes |
| S2 | `steps/save-02-extract-changes.md` | Extract state deltas from session |
| S3 | `steps/save-03-update-state.md` | Persist updates to bible files |
| S4 | `steps/save-04-log-events.md` | Log event trail for audit |

## Dependencies

- **Orchestrator**: Director K (`DIR` — `lnd-orchestrator.agent.yaml`)
- **Schema**: `continuity-ledger.schema.json`
- **Upstream**: Gooner Alchemist pipeline (step 6)
- **Downstream**: Character Builder, Lewd Writer

## Quick Reference

| Intent | Trigger | Route |
|--------|---------|-------|
| **Load bible** | `/bible-sync` (LOAD) | Execute steps L1–L4 |
| **Save state** | `/bible-sync` (SAVE) | Execute steps S1–S4 |
| **Pipeline integration** | Invoked by Gooner Alchemist | Auto-detect mode |
