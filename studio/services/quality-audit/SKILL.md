---
name: quality-audit
description: "R18 prose quality audit service — 100-point scoring from pervert perspective across five categories with actionable revision feedback."
dependencies:
  knowledge: []
  modules: []
---

# Quality Audit Service

## Overview

The Quality Audit service performs **comprehensive quality scoring** of R18 prose using a pervert-perspective evaluation framework. Operated by **Riko** (Gooner Editor), it scores prose across five categories (A through E) on a 100-point scale, scans for banned words, validates sensory density, and generates actionable rewrite instructions when scores fall below the 85-point threshold.

The audit produces an `audit-report.json` containing the verdict (PASS/FAIL), category scores, continuity updates, and specific fix recommendations per failing paragraph.

## On Activation

1. Load the `draft-prose.json` to audit
2. Load `continuity-ledger.json` for state consistency checking
3. Load audit framework from `{project-root}/studio/docs/GOONER_AUDIT_FRAMEWORK.md`
4. Verify schema at `{project-root}/studio/schemas/audit-report.schema.json`
5. Begin at `steps/step-01-load-prose.md`

## Steps

| Step | File | Purpose |
|------|------|---------|
| 1 | `steps/step-01-load-prose.md` | Load and parse draft prose |
| 2 | `steps/step-02-banned-scan.md` | Scan for banned words and formatting violations |
| 3 | `steps/step-03-category-scoring.md` | Score across categories A–E (100-point scale) |
| 4 | `steps/step-04-generate-feedback.md` | Generate actionable rewrite instructions |
| 5 | `steps/step-05-verdict-report.md` | Compile final `audit-report.json` with verdict |

## Dependencies

- **Agent**: Riko (`QA` — `gooner-editor.agent.yaml`)
- **Input Schema**: `draft-prose.schema.json`
- **Output Schema**: `audit-report.schema.json`
- **Modules**: `gooner-audit-engine`, `style-enforcer`
- **Framework**: `docs/GOONER_AUDIT_FRAMEWORK.md`
- **Upstream**: Lewd Writer → **Quality Audit**
- **Downstream**: PASS → State Persistence | FAIL → Rewrite loop

## Quick Reference

| Intent | Trigger | Route |
|--------|---------|-------|
| **Full audit** | `/gooner-audit` | Load `steps/step-01-load-prose.md` |
| **Standalone audit** | Provide `draft-prose.json` path | Execute all 5 steps independently |
| **Re-audit after rewrite** | Invoked by pipeline | Re-run from step 1 with revised prose |
