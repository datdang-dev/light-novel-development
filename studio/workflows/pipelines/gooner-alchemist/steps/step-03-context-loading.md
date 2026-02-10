---
name: 'step-03-context-loading'
description: 'Invoke bible-sync LOAD for continuity context'

# Path Definitions
workflow_path: '{project-root}/studio/workflows/pipelines/gooner-alchemist'
thisStepFile: './step-03-context-loading.md'
nextStepFile: './step-04-prose-generation.md'
bibleSyncWorkflow: '{project-root}/studio/workflows/capabilities/bible-sync/workflow.md'
---

# Step 3: Context Loading

## STEP GOAL:

Invoke bible-sync in LOAD mode to prepare continuity context for prose generation.

## MANDATORY SEQUENCE

### 1. Invoke Bible-Sync LOAD

```
"**📘 INVOKING BIBLE-SYNC LOAD**

Loading story context...

---

@/bible-sync mode=LOAD project={project_name}

---"
```

**EXECUTION:** Load bible-sync workflow with mode=LOAD

### 2. Wait for Completion

Bible-sync LOAD will:
1. Check bible existence
2. Load character profiles
3. Load current states
4. Generate context document

### 3. Verify Context Output

```markdown
### Context Verification

| Check | Status |
|-------|--------|
| Context doc created | ✓/✗ |
| Characters loaded | {count} |
| States loaded | ✓/✗ |
```

### 4. Update Pipeline State

Update pipeline doc:
- Step 3: ✅ DONE

### 5. Present MENU OPTIONS

```
"✅ Context loaded!

**Characters:** {count}
**Carry-forward items:** {count}

**Tiếp theo:** Prose generation

**Chọn:** [C] Continue to Prose"
```

---
