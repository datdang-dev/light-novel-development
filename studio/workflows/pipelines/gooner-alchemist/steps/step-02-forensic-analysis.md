---
name: 'step-02-forensic-analysis'
description: 'Invoke panel-forensic workflow for visual analysis'

# Path Definitions
workflow_path: '{project-root}/studio/workflows/pipelines/gooner-alchemist'
thisStepFile: './step-02-forensic-analysis.md'
nextStepFile: './step-03-context-loading.md'
panelForensicWorkflow: '{project-root}/studio/workflows/capabilities/panel-forensic/workflow.md'
stateFile: '{output_folder}/_pipeline/{project}/state.yaml'
analysisFolder: '{output_folder}/_analysis/{project}'
---

# Step 2: Forensic Analysis

**Progress: Step 2 of 7** - Next: Context Loading

## RULES:

- MUST NOT skip steps.
- MUST NOT optimize sequence.
- MUST follow exact instructions.
- MUST NOT write prose (that's Step 4).
- MUST process ONE page at a time.
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in Vietnamese

## CONTEXT:

- Requires pipeline state from Step 1 with `pages_pending` defined.
- Focus: Invoke /panel-forensic for the CURRENT page only.
- Output: Forensic report at `{analysisFolder}/page-{XXX}-forensic.md`
- Objective: Generate comprehensive visual analysis before prose.

---

## 0. PRE-EXECUTION GATE (MANDATORY)

### a) Load Pipeline State

Read `{stateFile}` and extract:
- `current_page` - page being processed
- `pages_pending` - pages still to process
- `forensics_completed` - pages already analyzed

### b) Validate Current Page

```
IF current_page IS EMPTY:
  - SET current_page = first item from pages_pending
  - UPDATE state file
  
IF pages_pending IS EMPTY:
  - OUTPUT: "✅ All pages processed!"
  - HALT - workflow complete
```

### c) Check Not Already Done

```
IF current_page IN forensics_completed:
  - OUTPUT: "⏭️ Forensic already exists for page {current_page}"
  - Display menu: [C] Continue to Context | [R] Re-run Forensic
  - HALT and wait
```

---

## SEQUENCE OF INSTRUCTIONS

### 1. Announce Delegation

OUTPUT to user:
```
─────────────────────────────────────────────
📤 DELEGATING TO: Prof. Atomic 🔬 (Panel Forensic Analyst)
📋 TASK: Deep visual forensic analysis of page {current_page}
📁 INPUT: {source_folder}/{current_page}.webp
📁 OUTPUT: {analysisFolder}/page-{current_page}-forensic.md
─────────────────────────────────────────────
```

### 2. Execute Panel-Forensic Workflow

**CRITICAL**: Load and execute `{panelForensicWorkflow}` with:
- Input image: `{source_folder}/{current_page}.webp`
- Output path: `{analysisFolder}/page-{current_page}-forensic.md`

**DO NOT analyze the image yourself. INVOKE the workflow.**

### 3. Wait for Completion

Panel-forensic workflow produces report containing:
1. ✅ Panel Layout
2. ✅ Character Identification
3. ✅ Body Scan
4. ✅ Fluid Scan
5. ✅ SFX Extraction (Romanized Japanese)
6. ✅ Dialogue Extraction
7. ✅ Psychological Scan
8. ✅ Smell Matrix
9. ✅ Sound Matrix
10. ✅ Continuity Notes

### 4. Verify Forensic Output

**GATE CHECK - MANDATORY**

```markdown
## Forensic Output Verification

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| File exists | {analysisFolder}/page-{current_page}-forensic.md | ✓/✗ | |
| Panel count | ≥1 | | |
| Character IDs | ≥1 | | |
| SFX extracted | ≥1 | | |
| All 10 sections | Present | | |
```

**IF ANY CHECK FAILS:**
```
🚫 FORENSIC INCOMPLETE
Missing: {list_missing_items}
ACTION: Re-invoke panel-forensic
```
LOOP back to Step 2.

### 5. Update Pipeline State

Update `{stateFile}`:
```yaml
forensics_completed:
  - ... existing ...
  - {current_page}  # ADD this
```

### 6. Present Checkpoint Menu

OUTPUT:
```
✅ Forensic complete for page {current_page}!

📄 Report: {analysisFolder}/page-{current_page}-forensic.md
🔢 Panels: {count}
🎭 Characters: {count}
✨ SFX: {count}

**Select:** [C] Continue to Context Loading | [R] Re-run Forensic | [V] View Report
```

**HALT and wait for user selection.**

#### Menu Handling Logic:

- IF C: 
  - VERIFY forensic file exists (GATE CHECK)
  - IF EXISTS: Update state, load `{nextStepFile}`
  - IF NOT EXISTS: "🚫 Cannot proceed - forensic missing" → Stay here
- IF R: Re-run from Step 2
- IF V: Display forensic report contents, then redisplay menu
- IF Any other: Respond helpfully, then redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C' AND gate check passes
- After R or V execution, return to this menu

---

## REQUIRED OUTPUTS:

- MUST generate forensic report via /panel-forensic workflow
- MUST contain ALL 10 required sections
- MUST update pipeline state with completion

## VERIFICATION CHECKLIST:

- [ ] Pipeline state loaded FIRST before any action
- [ ] Delegation banner displayed
- [ ] /panel-forensic workflow invoked (NOT self-analyzed)
- [ ] Forensic report verified with all 10 sections
- [ ] `forensics_completed` updated in state
- [ ] User selected [C] to continue

---

## 🚨 SYSTEM FAILURE CONDITIONS

Director K performing forensics directly = **PROTOCOL VIOLATION**
Missing forensic report = **GATE BLOCKED**
Skipping to prose = **PIPELINE FAILURE**

**Master Rule:** DELEGATE. VERIFY. GATE. Never analyze directly.
