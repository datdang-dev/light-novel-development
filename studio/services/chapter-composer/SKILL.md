---
name: chapter-composer
description: "Chapter compilation service — merges individual page prose files into cohesive chapter documents with transitions and continuity verification."
---

# Chapter Composer Service

## Overview

The Chapter Composer compiles **individual page prose files** into cohesive chapter documents. Operated by **Director K**, it gathers all adapted prose for a chapter, reviews page ordering, adds inter-page transitions, formats the chapter according to light novel standards, and performs a final polish pass.

This is a post-production service that runs after all pages in a chapter have been individually adapted and audited through the Gooner Alchemist pipeline.

## On Activation

1. Identify the chapter and locate all adapted page prose files
2. Verify all pages have passed quality audit (score ≥ 85)
3. Load continuity ledger for the chapter
4. Begin at `steps/step-01-gather-prose.md`

## Steps

| Step | File | Purpose |
|------|------|---------|
| 1 | `steps/step-01-gather-prose.md` | Gather and validate all page prose files |
| 2 | `steps/step-02-order-review.md` | Review page ordering and identify gaps |
| 3 | `steps/step-03-add-transitions.md` | Add transitions between pages |
| 4 | `steps/step-04-format-chapter.md` | Apply chapter formatting standards |
| 5 | `steps/step-05-final-polish.md` | Final continuity and quality polish |

## Dependencies

- **Orchestrator**: Director K (`DIR` — `lnd-orchestrator.agent.yaml`)
- **Input**: Adapted page prose files (from Gooner Alchemist)
- **Upstream**: Quality Audit (all pages must PASS)
- **Downstream**: Release Compiler

## Quick Reference

| Intent | Trigger | Route |
|--------|---------|-------|
| **Compose chapter** | `/chapter-composer` | Load `steps/step-01-gather-prose.md` |
| **Specify chapter** | Provide chapter number/path | Pre-fill metadata and begin |
