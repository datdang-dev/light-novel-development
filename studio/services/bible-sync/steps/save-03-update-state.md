---
name: 'save-03-update-state'
description: 'Write changes to state files'

# Path Definitions
workflow_path: '{project-root}/studio/services/bible-sync'
thisStepFile: './save-03-update-state.md'
nextStepFile: './save-04-log-events.md'
statePath: '{output_folder}/_bible/{project_name}/state'
---

# SAVE Step 3: Update State

## STEP GOAL:

Persist extracted state changes to the state files.

## MANDATORY SEQUENCE

### 1. Update Current State YAML

Modify `{statePath}/current-state.yaml`:

```yaml
characters:
  {char_name}:
    physical:
      clothing: "{new state}"
      injuries: [{if any}]
      fluids: [{if any}]
    emotional:
      mood: "{new mood}"
      arousal: {new level}
    cumulative:
      encounter_count: {N+1}
      last_action: "{latest action}"
```

### 2. Update Character Profiles (if needed)

If new permanent information learned:
- Update character profile .md files
- Add new relationship information

### 3. Verify Updates

```markdown
## State Updates

### Updated Files

| File | Changes |
|------|---------|
| current-state.yaml | {summary} |
| {char}.md | {if updated} |
```

### 4. Present MENU OPTIONS

```
"✅ State files updated!

**Files modified:** {count}

**Tiếp theo:** Log cumulative events

**Chọn:** [C] Continue"
```

---
