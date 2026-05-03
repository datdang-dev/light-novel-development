# LND Workflow Template

This template provides the standard structure for LND Studio workflow entry files.

<!-- TEMPLATE START -->

---
name: "[WORKFLOW_NAME]"
description: "[Brief description of what this workflow accomplishes]"
owner: "[Agent name who owns this workflow]"
---

# [WORKFLOW_DISPLAY_NAME]

**Goal:** [State the primary goal of this workflow in one clear sentence]

**Your Role:** In addition to your name, communication_style, and persona, you are a [specific role] specializing in R18 Light Novel production. You bring expertise in [your specialty], while the user brings their creative vision. Work together as equals.

---

## WORKFLOW ARCHITECTURE

### Core Principles

- **Micro-file Design**: Each step is a self-contained instruction file executed one at a time
- **Just-In-Time Loading**: Only the current step file is in memory
- **Sequential Enforcement**: Steps must be completed in order, no skipping
- **State Tracking**: Document progress in output file frontmatter using `stepsCompleted` array
- **Append-Only Building**: Build documents by appending content as directed

### Step Processing Rules

1. **READ COMPLETELY**: Always read the entire step file before taking any action
2. **FOLLOW SEQUENCE**: Execute all numbered sections in order
3. **WAIT FOR INPUT**: If a menu is presented, halt and wait for user selection
4. **CHECK CONTINUATION**: Only proceed when user selects 'C' (Continue)
5. **SAVE STATE**: Update `stepsCompleted` in frontmatter before loading next step
6. **LOAD NEXT**: When directed, load, read entire file, then execute next step

### Critical Rules (NO EXCEPTIONS)

- 🛑 **NEVER** load multiple step files simultaneously
- 📖 **ALWAYS** read entire step file before execution
- 🚫 **NEVER** skip steps or optimize the sequence
- 💾 **ALWAYS** update frontmatter when completing steps
- 🎯 **ALWAYS** follow the exact instructions
- ⏸️ **ALWAYS** halt at menus and wait for user input
- 📋 **NEVER** create mental todo lists from future steps
- ✅ **ALWAYS** speak in Vietnamese (communication_language from config)

---

## LND-SPECIFIC RULES

### R18 Content Standards

- Apply OBSERVER-CAMERA perspective (third-person, clinical, no moral judgment)
- Follow Zero-Skip Protocol for visual analysis
- Maintain sensory density requirements (smell ≥3, sound ≥3, texture ≥5)
- Never use banned words or euphemisms

### Quality Gates

- All prose must pass gooner-audit (≥85/100) before saving
- Continuity must be maintained via bible-sync

---

## INITIALIZATION SEQUENCE

### 1. Configuration Loading

Load and read config from `{project-root}/studio/config/config.yaml`:
- `output_folder`, `user_name`, `communication_language`, `document_output_language`

### 2. First Step Execution

Load, read the full file and execute `./steps/step-01-[first-step].md` to begin.

<!-- TEMPLATE END -->

## Usage Notes

1. Copy template to new workflow folder
2. Replace all `[PLACEHOLDERS]`
3. Create steps folder with step files
4. Ensure consistency with LND quality standards
