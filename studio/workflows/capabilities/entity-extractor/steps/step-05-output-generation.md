---
name: 'step-05-output-generation'
description: 'Generate structured entity output files'

thisStepFile: './step-05-output-generation.md'
entitiesOutput: '{output_folder}/_entities/{manga_name}/page_{num}_entities.yaml'
---

# Step 5: Output Generation

## STEP GOAL:

Generate structured output files for consumption by other workflows.

## MANDATORY SEQUENCE

### 1. Generate Entities YAML

Write to `{entitiesOutput}`:

```yaml
---
source_forensic: "{path}"
page: {num}
extracted: "{timestamp}"
---

characters:
  - id: "char_001"
    name: "{if known}"
    alias: "{descriptor}"
    panels: [1, 2, 5]
    physical:
      hair: "{desc}"
      body: "{desc}"
      clothing_final: "{state}"
    emotional:
      mood: "{mood}"
      arousal: {0-10}
    
  - id: "char_002"
    # ...

relationships:
  - pair: ["char_001", "char_002"]
    type: "{dynamic}"
    confidence: "{HIGH/MEDIUM/LOW}"
    evidence:
      - panel: {X}
        observation: "{desc}"

states:
  char_001:
    physical:
      clothing: "{final}"
      injuries: []
      fluids: []
    emotional:
      mood: "{final}"
      arousal: {X}
      consent: "{type}"
```

### 2. Generate Character Stubs (if new)

For new characters, create stub in bible:

```markdown
---
id: "char_001"
name: "{if known}"
status: STUB
created_from: "{forensic_path}"
---

# Character: {name or id}

## Physical Description
{from extraction}

## Personality
*To be developed*

## Notes
- First seen: Page {X}, Panel {Y}
```

### 3. Workflow Completion

```
"✅ ENTITY EXTRACTION COMPLETE!

**Output:** {entitiesOutput}

**Summary:**
- Characters: {count}
- Relationships: {count}
- New character stubs: {count}

**Ready for:** bible-sync, prose-adapter

**WORKFLOW COMPLETE**"
```

---

## WORKFLOW END

Entity extraction complete. Outputs ready for downstream workflows.
