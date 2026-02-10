---
name: 'step-06-state-persistence'
description: 'Invoke bible-sync SAVE for state updates'

# Path Definitions
workflow_path: '{project-root}/studio/workflows/pipelines/gooner-alchemist'
thisStepFile: './step-06-state-persistence.md'
nextStepFile: './step-07-complete.md'
bibleSyncWorkflow: '{project-root}/studio/workflows/capabilities/bible-sync/workflow.md'
---

# Step 6: State Persistence

## STEP GOAL:

Invoke bible-sync in SAVE mode to persist state changes from the approved prose.

## MANDATORY SEQUENCE

### 1. Invoke Bible-Sync SAVE

```
"**💾 INVOKING BIBLE-SYNC SAVE**

Saving state changes to bible...

---

@/bible-sync 
  mode=SAVE 
  prose={approved_prose_path}
  audit_score={score}

---"
```

**EXECUTION:** Load bible-sync workflow with mode=SAVE

### 2. Wait for Completion

Bible-sync SAVE will:
1. Verify SAVE mode
2. Extract state changes
3. Update state files
4. Log cumulative events

### 3. Verify Save Complete

```markdown
### Bible Sync Verification

| Check | Status |
|-------|--------|
| State updated | ✓/✗ |
| Log entry added | ✓/✗ |
| Characters updated | {count} |
```

### 4. Update Pipeline State

Update pipeline doc:
- Step 6: ✅ DONE

### 5. Present MENU OPTIONS

```
"✅ Bible synchronized!

**State updates:** {count}
**Events logged:** {count}

**Tiếp theo:** Complete pipeline

**Chọn:** [C] Continue to Complete"
```

---
