---
name: step-08-quality-audit
description: "Quality audit of generated prose chapters"
---

# Step 8: Quality Audit

## Purpose
Audit the generated prose chapters against the Gooner Audit Framework.

## 🔄 [Delegating to Riko (quality-audit service)]

## Inputs
- Generated chapter `draft.md`

## Delegation Instructions
Delegate to the shared `quality-audit` service (Riko):
- Pass `draft.md` as input
- Riko outputs strict JSON with `'pass'`, `'score'`, `'reason'`

## Audit Gate
- Score ≥ 85 → **PASS** — Chapter accepted
- Score < 85 → **FAIL** — Rewind to Step 7 with fix instructions from audit JSON
- Max 3 retry attempts (circuit breaker)

## Outputs
- `audit.json` per chapter

## Progression
- ✅ All chapters pass → ⏸️ **CHECKPOINT: Loop Decision**
  - Return to `./steps/step-05-heroine-select.md`
  - Ask: *"Heroine {name}'s storyline is complete. Write for another heroine?"*
- ❌ Audit fails after 3 retries → HALT and report to user
