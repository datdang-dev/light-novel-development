---
name: 'save-02-extract-changes'
description: 'Parse prose for state changes'

# Path Definitions
workflow_path: '{project-root}/studio/services/bible-sync'
thisStepFile: './save-02-extract-changes.md'
nextStepFile: './save-03-update-state.md'
---

# SAVE Step 2: Extract Changes

## STEP GOAL:

Parse the approved prose to identify all state changes that need to be persisted.

## MANDATORY SEQUENCE

### 1. Scan for Physical State Changes

Identify from prose:
- Clothing changes (removed, torn, stained)
- Physical conditions (injuries, exhaustion, fluids)
- Positioning changes

```markdown
## State Changes Extraction

### Physical Changes

| Character | Before | After | Evidence |
|-----------|--------|-------|----------|
| {name} | {state} | {new state} | "{quote from prose}" |
```

### 2. Scan for Emotional State Changes

Identify:
- Mood shifts
- Arousal level changes
- Psychological state changes

```markdown
### Emotional Changes

| Character | Before | After | Evidence |
|-----------|--------|-------|----------|
| {name} | {state} | {new state} | "{quote}" |
```

### 3. Scan for Relationship Changes

Identify:
- Power dynamic shifts
- Revealed feelings
- New dynamics established

### 4. Identify Cumulative Events

Events to log:
- First encounters
- Significant actions
- State milestones

### 5. Present MENU OPTIONS

```
"✅ Changes extracted!

**Physical changes:** {count}
**Emotional changes:** {count}
**Relationship changes:** {count}
**Events to log:** {count}

**Chọn:** [C] Continue to Update State"
```

---
