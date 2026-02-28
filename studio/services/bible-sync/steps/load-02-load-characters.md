---
name: 'load-02-load-characters'
description: 'Load relevant character profiles'

nextStepFile: './load-03-load-state.md'
charactersPath: '{output_folder}/_bible/{project_name}/characters'
---

# LOAD Step 2: Load Characters

## STEP GOAL:

Load character profiles relevant to the current adaptation page.

## MANDATORY SEQUENCE

### 1. Identify Characters Needed

From forensic report or user input, identify:
- Characters appearing in current page
- Characters referenced in dialogue
- Characters relevant for relationship context

### 2. Load Character Profiles

For each character:

```markdown
## Character Loading

### Characters Loaded

| Character | File | Status |
|-----------|------|--------|
| {name} | {name}.md | ✅ Loaded |
| {name} | - | ⚠️ Not found (will create) |
```

### 3. Load Relationship Matrix

If exists, load `relationships.md`:
- Current relationship states
- Power dynamics
- History references

### 4. Handle New Characters

If character in forensics but no profile:

```markdown
### New Character Detected

**Name:** {from forensics}
**Action:** Create placeholder profile for completion after scene

Placeholder created at: {charactersPath}/{name}.md
```

### 5. Present MENU OPTIONS

```
"✅ Characters loaded!

**Loaded:** {count} profiles
**New (placeholder):** {count}

**Tiếp theo:** Load current states

**Chọn:** [C] Continue"
```

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- All relevant profiles loaded
- Relationships loaded
- New characters handled

### ❌ SYSTEM FAILURE:

- Missing character profiles not flagged
- Not loading relationships
