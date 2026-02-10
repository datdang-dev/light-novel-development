# LND Studio Audit Issues Log

> Created: 2026-02-09 | Audit Session

## Critical Issues 🔴

### 1. Missing Activation Step 3 (All Agents)
**Files**: `lewd-writer.md`, `gooner-editor.md`
**Issue**: Step numbering jumps from 2 → 4, skipping step 3
**Impact**: Inconsistent activation sequence
**Fix**: Add step 3 for user_name assignment

### 2. ENTRY_POINTS.md References Missing Workflows
**File**: `studio/ENTRY_POINTS.md`
**Issue**: `/prose-adapter` listed but entry point in `.agent/workflows/` not exist
**Fix**: Create `.agent/workflows/prose-adapter.md` entry point OR update ENTRY_POINTS

---

## Medium Issues ⚠️

### 3. Legacy Path References
**Found**: `studio/docs/` in `docs/architecture.md` line 59
**Impact**: May cause file loading errors
**Fix**: Replace with `studio/docs/`

### 4. Inconsistent Menu Items Across Agents
**Issue**: gooner-editor has `[RC] Release Compiler` but should have `[GA] Gooner Audit`
**Impact**: Users may expect different workflows
**Fix**: Update gooner-editor menu to focus on QA workflows

### 5. studio/rules/ vs .agent/rules/ Duplication
**Found**: Rules exist in both locations
**Impact**: Confusion about which is source of truth
**Fix**: Keep only `.agent/rules/` OR clearly mark studio/rules as agent-loadable copies

---

## Low Issues ℹ️

### 6. Missing Agent Files
**File**: `character-architect.md`, others not inspected yet
**Impact**: May be incomplete
**Action**: Full audit of all agents needed

### 7. Workflow Step File Counts
**Listed in README**: panel-forensic has 7 steps
**Actual**: Need to verify step files exist
**Action**: Count files in each workflow directory

---

## Resolved ✅

*(Move issues here after fixing)*
