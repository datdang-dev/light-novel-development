---
name: step-04-prose-dispatch
description: Dispatch to Prose Adapter
nextStepFile: ./step-05-quality-edit.md
proseAdapterWorkflow: {project-root}/studio/workflows/capabilities/prose-adapter/workflow.md
projectRoot: {project-root}
---

# Step 4: Prose Adaptation ✍️

## STEP GOAL

Transform Forensic Data + Dialogue Script into "Gooner-Grade" Prose.

## MANDATORY EXECUTION RULES

- 🛑 **NEVER** rewrite the prose yourself.
- ✅ **DELEGATE** strictly to Suki's workflow.
- ✅ **ENSURE** input files (Forensic + Dialogue) are available.

## SEQUENCE OF INSTRUCTIONS

### 1. Identify Input

Verify existence of:

- `forensic_report.md` (Skeleton)
- `dialogue_script.md` (Voice)

### 2. Dispatch to Sub-Workflow

Load and execute the **Prose Adapter Workflow**:

**Workflow Path:** `{proseAdapterWorkflow}`

**Usage:**

- Pass both `forensic_report.md` and `dialogue_script.md` as context.
- Ensure Suki combines them into a single prose output.

### 3. Verify Output

Monitor for `prose_scene.md` (or `prose_output.md`).

### 4. Present MENU OPTIONS

```
"✅ Prose Adaptation Complete.

**Scene:** {proseScenePath}
**Word Count:** {word_count}

**Tiếp theo:** Quality Editing (Riko)

**Chọn:** [C] Continue to Quality Edit"
```

#### Menu Handling Logic

- IF C: Load `{nextStepFile}`
- IF other: Redisplay menu

## SYSTEM FAILURE METRICS

- Director K attempting to write prose = **PROTOCOL VIOLATION**
