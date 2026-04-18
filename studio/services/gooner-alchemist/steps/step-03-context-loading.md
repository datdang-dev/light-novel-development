---
name: 'step-03-context-loading'
description: 'Invoke bible-sync LOAD and JIT Context Sharding for continuity context'

nextStepFile: './step-04-prose-generation.md'
bibleSyncWorkflow: '{project-root}/studio/services/bible-sync/references/workflow.md'
analysisFolder: '{output_folder}/_analysis/{project}'
---

# Step 3: Context Loading + JIT Context Sharding

## STEP GOAL

Invoke bible-sync in LOAD mode and perform **Context Sharding** — conditionally loading ONLY the rules relevant to the current scene type, saving 30-40% tokens per invocation.

## RULES

- ✅ YOU MUST ALWAYS SPEAK OUTPUT in Vietnamese
- MUST follow exact sequence below

---

## MANDATORY SEQUENCE

### 1. Invoke Bible-Sync LOAD

```text
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

### 3. ⚡ CONTEXT SHARDING (Performance Optimization #1)

**Read the forensic report** for the current page:

```text
forensic_data = READ {analysisFolder}/page-{current_page}-forensic.md
scene_tags = EXTRACT content_tags from forensic_data
```

**Conditionally load rules based on scene tags:**

```text
ALWAYS LOAD (Tier 1 — Core, ~500 tokens):
  ✅ {project-root}/studio/rules/dialogue_format.md
  ✅ {project-root}/studio/schemas/draft-prose.schema.json (structure only)

IF scene_tags CONTAINS "bedroom" OR "bathroom" OR "explicit":
  ✅ {project-root}/studio/rules/sensory_density.md
  ✅ {project-root}/studio/rules/lewd_writing_mechanics.md
  ✅ {project-root}/studio/core/lewd-writer/data/sensory-vocabulary.md

IF scene_tags CONTAINS "dialogue-heavy" OR "confrontation":
  ✅ {project-root}/studio/rules/character_voice.md
  ✅ {project-root}/studio/rules/dialogue_format.md (full version)

IF scene_tags CONTAINS "aftermath" OR "post-climax":
  ✅ {project-root}/studio/rules/sensory_density.md
  ✅ {project-root}/studio/rules/environmental_atmosphere.md

IF scene_tags CONTAINS "intro" OR "transition":
  ✅ {project-root}/studio/rules/environmental_atmosphere.md
  (Skip heavy sensory/lewd rules — save ~40% tokens)

SKIP rules that are NOT relevant to the current scene type.
```

**OUTPUT:**

```text
⚡ Context Sharding Applied:
  - Scene tags: {scene_tags}
  - Tier 1 (Core): 2 files loaded
  - Tier 2 (Scene-specific): {count} files loaded
  - Tier 2 (Skipped): {skipped_count} files
  - Estimated token savings: ~{percentage}%
```

### 4. Verify Context Output

```markdown
### Context Verification

| Check | Status |
|-------|--------|
| Priority Header injected | ✓/✗ |
| Bible-sync context | ✓/✗ |
| Characters loaded | {count} |
| States loaded | ✓/✗ |
| Context Sharding applied | ✓ |
| Scene-relevant rules | {count} loaded |
```

### 5. Update Pipeline State

Update pipeline doc:

- Step 3: ✅ DONE
- context_sharding_profile: {scene_tags}

### 6. Present MENU OPTIONS

```text
"✅ Context loaded with smart sharding!

**Characters:** {count}
**Scene Type:** {scene_tags}
**Rules Loaded:** {count} / {total_available}
**Token Savings:** ~{percentage}%

**Tiếp theo:** Prose generation

**Chọn:** [C] Continue to Prose"
```

**MANDATORY:** The generated `context_payload.md` must prepend a strict Priority Header with this precedence order:
1. Runtime Task Instructions
2. Output Contracts / Schemas
3. Canon Rules
4. Scene-specific Payloads
5. Persona / Heuristics

---
