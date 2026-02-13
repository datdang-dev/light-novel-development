---
name: step-02-context-prep
description: Prepare Context and Sync Bible
nextStepFile: ./step-03-dialogue-dispatch.md
entityExtractorWorkflow: {project-root}/studio/workflows/capabilities/entity-extractor/workflow.md
characterBibleWorkflow: {project-root}/studio/workflows/capabilities/character-bible/workflow.md
projectRoot: {project-root}
---

# Step 2: Context Preparation (Bible Sync) 📚

## STEP GOAL

Ensure all characters in the scene have active profiles and the world state is updated.

## MANDATORY SEQUENCE OF INSTRUCTIONS

### 1. Extract Entities

Execute the **Entity Extractor Workflow** to identify characters, locations, and objects.

**Workflow Path:** `{entityExtractorWorkflow}`
**Input:** `forensic_report.md` (from Step 1)
**Output:** `entities.yaml`

### 2. Sync Profiles (Character Bible)

Execute the **Character Bible Workflow** to update or retrieve character data.

**Workflow Path:** `{characterBibleWorkflow}`
**Input:** `entities.yaml`

### 3. Verify Context

Ensure `active_character_context.md` (or equivalent profile dump) is ready for Miki (Dialogue Crafter).

### 4. Present MENU OPTIONS

```
"✅ Context Preparation Complete.

**Entities Identified:** {list_from_entities_yaml}
**Profiles Synced:** {list_synced_profiles}

**Tiếp theo:** Dialogue Scripting (Miki)

**Chọn:** [C] Continue to Dialogue Dispatch"
```

#### Menu Handling Logic

- IF C: Load `{nextStepFile}`
- IF other: Redisplay menu

## SYSTEM FAILURE METRICS

- Failing to extract entities or sync profiles before proceeding.
