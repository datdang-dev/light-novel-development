---
name: 'step-05-export-card'
description: 'Generate final JSON output'
cardOutput: '{output_folder}/_cards/{char_name}.json'
---

# Step 5: Export Card

## STEP GOAL:

Generate final ST-compatible character card.

## MANDATORY SEQUENCE

### 1. Compile Full Card JSON

```json
{
  "name": "{name}",
  "description": "{description}",
  "personality": "{personality}",
  "scenario": "{default scenario}",
  "first_mes": "{greeting}",
  "mes_example": "{examples}",
  "system_prompt": "{system instructions}",
  "post_history_instructions": "",
  "tags": ["{tags}"],
  "creator": "LND Studio",
  "character_version": "1.0",
  "extensions": {
    "world": "{lorebook entries}"
  }
}
```

### 2. Validate JSON

- [ ] Valid JSON syntax
- [ ] All required fields present
- [ ] No empty required fields

### 3. Write Output

Save to `{cardOutput}`

### 4. Workflow Completion

```
"✅ ST CARD EXPORT COMPLETE!

**Output:** {cardOutput}

**Card Summary:**
- Name: {name}
- Description: ~{words} words
- Examples: {count}
- Lorebook entries: {count}

**Import to SillyTavern:**
Settings → Import Character → Select JSON

**WORKFLOW COMPLETE**"
```

---

## WORKFLOW END

ST card ready for import into SillyTavern.
