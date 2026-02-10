---
name: 'save-01-mode-check'
description: 'Verify SAVE mode and load approved prose'

# Path Definitions
workflow_path: '{project-root}/studio/workflows/capabilities/bible-sync'
thisStepFile: './save-01-mode-check.md'
nextStepFile: './save-02-extract-changes.md'
---

# SAVE Step 1: Mode Check

## STEP GOAL:

Verify this is SAVE mode and load the approved prose for state extraction.

## MANDATORY SEQUENCE

### 1. Verify Mode

```
IF mode != "SAVE":
  ERROR: Wrong mode. Use LOAD mode steps for loading.
  EXIT
```

### 2. Verify Prose Approved

```
REQUIRED:
- Prose file path provided
- Audit status = PASS
- Audit score ≥ 85

IF not approved:
  ERROR: Only PASSED prose can be saved to bible
  EXIT
```

### 3. Load Approved Prose

Use `view_file` to load the full prose content for state extraction.

### 4. Present MENU OPTIONS

```
"✅ SAVE mode verified!

**Prose:** {path}
**Audit Score:** {score}

**Tiếp theo:** Extract state changes

**Chọn:** [C] Continue"
```

---
