---
name: 'step-04-create-lorebook'
description: 'Generate character-specific lorebook'
nextStepFile: './step-05-export-card.md'
---

# Step 4: Create Lorebook

## STEP GOAL:

Create embedded lorebook entries for the character.

## LOREBOOK ENTRY STRUCTURE

```json
{
  "entries": {
    "0": {
      "keys": ["{trigger words}"],
      "content": "{lore content}",
      "enabled": true,
      "insertion_order": 100,
      "case_sensitive": false
    }
  }
}
```

## MANDATORY SEQUENCE

### 1. Identify Lore Topics

From character profile:
- Relationships (triggers on other char names)
- Backstory elements (triggers on keywords)
- Fetish preferences (triggers on kink terms)
- World context (triggers on location/terms)

### 2. Write Lore Entries

For each topic:

```markdown
## Lorebook Entry: {topic}

**Keys:** {trigger words}
**Priority:** {1-100}

**Content:**
{Concise lore text, ~100-200 words}
```

### 3. Format for ST

Generate lorebook JSON structure.

### 4. Present MENU

```
"✅ Lorebook created!

**Entries:** {count}
**Topics covered:** {list}

**Chọn:** [C] Continue to Export"
```

---
