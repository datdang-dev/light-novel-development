---
name: 'step-02-map-fields'
description: 'Map LND fields to ST schema'
nextStepFile: './step-03-write-description.md'
---

# Step 2: Map Fields

## STEP GOAL:

Map LND character profile fields to SillyTavern card schema.

## FIELD MAPPING

| LND Field | ST Field | Notes |
|-----------|----------|-------|
| Name | name | Direct |
| Archetype + Physical | description | Combine |
| Psychology + Voice | personality | Extract key traits |
| - | scenario | Generate default |
| Voice samples | first_mes | Craft greeting |
| Dialogue samples | mes_example | Format examples |
| Psychology + Fetish | system_prompt | Encode behavior |

## MANDATORY SEQUENCE

### 1. Extract and Map

```markdown
## Field Mapping

### Direct Fields
- name: "{name}"
- tags: ["{archetype}", "{kink tags}"]

### Composite Fields
- description: physical + core identity
- personality: psychology summary + voice pattern

### Generated Fields
- scenario: default roleplay setup
- first_mes: in-character greeting
```

### 2. Present MENU

```
"✅ Fields mapped!

**Direct:** {count}
**Composite:** {count}
**To generate:** {count}

**Chọn:** [C] Continue to Description"
```

---
