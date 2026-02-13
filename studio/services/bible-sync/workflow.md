---
name: "bible-sync"
description: "Story bible and state synchronization for continuity management"
owner: "Director K (lnd-orchestrator)"
version: "2.0.0"
---

# Bible Sync Workflow

**Goal:** Manage story bible loading (LOAD mode) and state persistence (SAVE mode) to maintain continuity across manga adaptation sessions.

**Your Role:** You are the continuity manager, ensuring that character states, relationships, and story context are properly loaded before prose generation and saved after completion.

---

## WORKFLOW ARCHITECTURE

### Dual Mode Operation

```
MODE: LOAD
- Called before prose-adapter
- Loads character profiles, relationships, cumulative state
- Provides context for prose generation

MODE: SAVE
- Called after gooner-audit PASS
- Updates character states from prose
- Records cumulative events
```

### Core Principles

- **Micro-file Design**: Each step is self-contained
- **Just-In-Time Loading**: Only current step in memory
- **State Tracking**: Frontmatter tracks completion
- **Continuity First**: Never lose established context

### Critical Rules (NO EXCEPTIONS)

- 🛑 **NEVER** overwrite bible without SAVE mode
- 📖 **ALWAYS** read entire step file before execution
- 🚫 **NEVER** create new bible if one exists (LOAD mode)
- ✅ **ALWAYS** speak in Vietnamese

---

## BIBLE STRUCTURE

```
{output_folder}/_bible/{project_name}/
├── story-bible.md           # Master context document
├── characters/
│   ├── {char_name}.md       # Per-character profiles
│   └── relationships.md     # Relationship matrix
├── world/
│   ├── locations.md         # Setting descriptions
│   └── timeline.md          # Event timeline
└── state/
    ├── current-state.yaml   # Live character states
    └── cumulative-log.md    # Running event log
```

---

## MODE-SPECIFIC STEPS

### LOAD Mode (4 steps)

| Step | Name | Purpose |
|------|------|---------|
| 1 | Mode Check | Verify LOAD mode, check bible exists |
| 2 | Load Characters | Load relevant character profiles |
| 3 | Load State | Load current physical/emotional states |
| 4 | Generate Context | Create context document for prose-adapter |

### SAVE Mode (4 steps)

| Step | Name | Purpose |
|------|------|---------|
| 1 | Mode Check | Verify SAVE mode, load prose output |
| 2 | Extract Changes | Parse prose for state changes |
| 3 | Update State | Write changes to state files |
| 4 | Log Events | Add to cumulative event log |

---

## INITIALIZATION SEQUENCE

### 1. Determine Mode

```
IF called with mode=LOAD:
  → Load ./steps/load-01-mode-check.md

IF called with mode=SAVE:
  → Load ./steps/save-01-mode-check.md
```

### 2. First Step Execution

Load appropriate mode's first step file.

---

## INPUT/OUTPUT

```yaml
# LOAD Mode
input:
  - mode: "LOAD"
  - project_name: "{name}"
  - chapter: {num}
  - page: {num}
  - characters: [{list of relevant chars}]

output:
  - context_doc: "{output_folder}/_bible/{project}/prose-context.md"

# SAVE Mode  
input:
  - mode: "SAVE"
  - prose_file: "{path to approved prose}"
  - audit_score: {score}

output:
  - updated state files
  - cumulative log entry
```

---

## INTEGRATION

```yaml
# LOAD Mode
called_by:
  - gooner-alchemist (before prose-adapter)
  - prose-adapter initialization

outputs_to:
  - prose-adapter (context document)

# SAVE Mode
called_by:
  - gooner-alchemist (after audit PASS)

receives_from:
  - prose-adapter (approved prose)
  - gooner-audit (pass confirmation)
```

---

## FIRST CHAPTER PROTOCOL

If no bible exists (first adaptation):

```
1. Create bible structure
2. Generate initial character profiles from forensics
3. Establish baseline states
4. Create empty cumulative log
```
