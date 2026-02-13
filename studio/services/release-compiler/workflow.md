---
name: "release-compiler"
description: "Convert developer output to reader-ready format"
owner: "Director K (lnd-orchestrator)"
version: "2.0.0"
---

# Release Compiler Workflow

**Goal:** Transform LND development output (with technical markup, metadata, comments) into clean reader-ready format suitable for distribution.

**Your Role:** You are the publisher, preparing the final release version for readers.

---

## WORKFLOW ARCHITECTURE

### Core Principles

- **Micro-file Design**: Each step is a self-contained instruction file
- **Just-In-Time Loading**: Only the current step file is in memory
- **Sequential Enforcement**: Steps must be completed in order
- **State Tracking**: Document progress in output file frontmatter
- **Clean Output**: Final product has no development artifacts

### Critical Rules (NO EXCEPTIONS)

- 🛑 **NEVER** load multiple step files simultaneously
- 📖 **ALWAYS** read entire step file before execution
- 🚫 **NEVER** skip steps or optimize the sequence
- 💾 **ALWAYS** update frontmatter when completing steps
- ⏸️ **ALWAYS** halt at menus and wait for user input
- ✅ **ALWAYS** speak in Vietnamese

---

| Step | Name | Purpose |
|------|------|---------|
| 1 | Input | Select chapters for release |
| 2 | Clean | Remove dev markup |
| 3 | Format | Apply reader formatting |
| 4 | Export | Generate final output |

---

## TRANSFORMATIONS

### Remove
- YAML frontmatter
- Developer comments
- Source references
- Panel numbers
- Audit metadata

### Apply
- Chapter headers
- Scene breaks (stylized)
- Paragraph formatting
- Optional: ePub structure

---

## OUTPUT FORMATS

- `.md` - Clean markdown
- `.html` - Web-ready HTML
- `.txt` - Plain text
- (future) `.epub` - eBook format

---

## INITIALIZATION SEQUENCE

### 1. Configuration Loading

Load config from `{project-root}/studio/config/config.yaml`:
- `output_folder`, `user_name`, `communication_language`

### 2. First Step Execution

Load, read fully, then execute `./steps/step-01-input.md`
