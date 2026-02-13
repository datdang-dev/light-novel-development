---
name: "chapter-composer"
description: "Compile adapted pages into chapter format"
owner: "Director K (lnd-orchestrator)"
version: "2.0.0"
---

# Chapter Composer Workflow

**Goal:** Compile individual page prose files into a cohesive chapter document with proper formatting, transitions, and continuity verification.

**Your Role:** You are the editor, assembling prose sections into a polished chapter ready for reading.

---

## WORKFLOW ARCHITECTURE

### Core Principles

- **Micro-file Design**: Each step is a self-contained instruction file
- **Just-In-Time Loading**: Only the current step file is in memory
- **Sequential Enforcement**: Steps must be completed in order
- **State Tracking**: Document progress in output file frontmatter
- **Continuity First**: Seamless flow between pages

### Critical Rules (NO EXCEPTIONS)

- 🛑 **NEVER** load multiple step files simultaneously
- 📖 **ALWAYS** read entire step file before execution
- 🚫 **NEVER** skip steps or optimize the sequence
- 💾 **ALWAYS** update frontmatter when completing steps
- ⏸️ **ALWAYS** halt at menus and wait for user input
- ✅ **ALWAYS** speak in Vietnamese

---

## STEP OVERVIEW

| Step | Name | Purpose |
|------|------|---------|
| 1 | Gather Prose | Collect all page prose files |
| 2 | Order & Review | Verify sequence and continuity |
| 3 | Add Transitions | Write connecting prose |
| 4 | Format Chapter | Apply chapter formatting |
| 5 | Final Polish | Review and output |

---

## INITIALIZATION SEQUENCE

### 1. Configuration Loading

Load config from `{project-root}/studio/config/config.yaml`:
- `output_folder`, `user_name`, `communication_language`

### 2. First Step Execution

Load, read fully, then execute `./steps/step-01-gather-prose.md`
