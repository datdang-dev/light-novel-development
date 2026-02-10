---
name: 'load-03-load-state'
description: 'Load current character states'

# Path Definitions
workflow_path: '{project-root}/studio/workflows/capabilities/bible-sync'
thisStepFile: './load-03-load-state.md'
nextStepFile: './load-04-generate-context.md'
statePath: '{output_folder}/_bible/{project_name}/state'
---

# LOAD Step 3: Load State

## STEP GOAL:

Load current character states including physical, emotional, and cumulative conditions.

## MANDATORY SEQUENCE

### 1. Load Current State YAML

Load `{statePath}/current-state.yaml`:

```yaml
# current-state.yaml structure
characters:
  {char_name}:
    physical:
      clothing: "{current state}"
      injuries: []
      fluids: []
    emotional:
      mood: "{current}"
      arousal: 0-10
    cumulative:
      encounter_count: N
      last_action: "{description}"
```

### 2. Load Cumulative Log

Load recent entries from `cumulative-log.md`:
- Last 5-10 relevant events
- Any ongoing conditions
- State changes to carry forward

### 3. Document Loaded States

```markdown
## State Loading

### Current Character States

| Character | Physical State | Emotional | Cumulative Notes |
|-----------|---------------|-----------|------------------|
| {name} | {brief} | {mood} | {notes} |
```

### 4. Identify Carry-Forward Items

Things that MUST be reflected in prose:
- Ongoing physical conditions (injuries, exhaustion)
- Emotional states from previous scenes
- Clothing states
- Relationship dynamics established

### 5. Present MENU OPTIONS

```
"✅ States loaded!

**Characters with state:** {count}
**Carry-forward items:** {count}

**Tiếp theo:** Generate context document

**Chọn:** [C] Continue"
```

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Current states loaded
- Cumulative history checked
- Carry-forward items identified

### ❌ SYSTEM FAILURE:

- Missing state file not handled
- Not checking cumulative log
