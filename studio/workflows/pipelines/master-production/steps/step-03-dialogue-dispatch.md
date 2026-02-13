---
name: step-03-dialogue-dispatch
description: Dispatch to Dialogue Generator
nextStepFile: ./step-04-prose-dispatch.md
dialogueGeneratorWorkflow: {project-root}/studio/workflows/capabilities/dialogue-generator/workflow.md
projectRoot: {project-root}
---

# Step 3: Dialogue Generation 💬

## STEP GOAL

Generate "Gooner-Grade" Dialogue Lines & SFX pattern matching character voices.

## MANDATORY EXECUTION RULES

- 🛑 **NEVER** accept sanitized dialogue.
- 🛑 **ALWAYS** prioritize character voice authenticity over politeness.
- ✅ **VERIFY** Miki follows the **Escalation Loop**.

## SEQUENCE OF INSTRUCTIONS

### 1. Identify Input

Ensure `forensic_report.md` (Action) and `active_character_context` (Voice) are available.

### 2. Dispatch to Sub-Workflow

Load and execute the **Dialogue Generator Workflow**:

**Workflow Path:** `{dialogueGeneratorWorkflow}`

**Instructions:**

- Pass the input files to Miki (Dialogue Crafter).
- Wait for the `dialogue_script.md` (or equivalent dialogue list) to be generated.

### 3. Verify Output

Ensure the dialogue script captures the correct tone, degradation level, and escalation.

### 4. Present MENU OPTIONS

```
"✅ Dialogue Generation Complete.

**Script:** {dialogueScriptPath}
**Characters:** {list_speakers}

**Tiếp theo:** Prose Adaptation (Suki)

**Chọn:** [C] Continue to Prose Dispatch"
```

#### Menu Handling Logic

- IF C: Load `{nextStepFile}`
- IF other: Redisplay menu

## SYSTEM FAILURE METRICS

- Accepting sanitized dialogue = **CRITICAL FAILURE**
