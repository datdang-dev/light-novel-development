---
name: 'step-02-forensic-analysis'
description: 'Invoke panel-forensic workflow for visual analysis'

nextStepFile: './step-03-context-loading.md'
panelForensicWorkflow: '{{project_root}}/studio/core/panel-forensic/references/workflow.md'
stateFile: '{{run_dir}}/_pipeline/{{project_name}}/state.yaml'
analysisFolder: '{{run_dir}}/_analysis/{{project_name}}'
---

# Step 2: Forensic Analysis

**Progress: Step 2 of 7** - Next: Context Loading

## RULES

- MUST NOT skip steps.
- MUST NOT optimize sequence.
- MUST follow exact instructions.
- MUST NOT write prose (that's Step 4).
- MUST process ONE page at a time.
- 🚨 **STRICT VISUAL RULE**: The `context_horizon.md` is for continuity only. THE IMAGE IS THE ABSOLUTE GROUND TRUTH for the current action. Do not hallucinate objects, actions, characters, or future events that are not explicitly painted on the current page.
- 🛑 **HARD GATE — IMAGE VIEW**: You MUST call `view_file({source_folder}/{current_page}.webp)` BEFORE writing ANY forensic content. No exceptions. No guessing from text. No inferring from context. If `view_file` fails, HALT.
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in Vietnamese

## CONTEXT

- Requires pipeline state from Step 1 with `pages_pending` defined.
- Focus: Invoke /panel-forensic for the CURRENT page only.
- Input Modifiers: Pass `context_horizon.md` alongside the image to provide trajectory context.
- Output: Forensic report at {{analysisFolder}}/page-{{XXX}}-forensic.md

---

## 0. PRE-EXECUTION GATE (MANDATORY)

### a) Load Pipeline State

Read `{{stateFile}}` and extract:

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
  - OUTPUT: "⏭️ Forensic already exists for page {{current_page}}"
  - Display menu: [C] Continue to Context | [R] Re-run Forensic
  - HALT and wait
```

---

## HARD GATE 0: IMAGE VIEW (MANDATORY — RETRO FIX 2026-04-25)

> [!CAUTION]
> This gate was added after the Page 004 Hallucination Incident.
> Kana generated a "wholesome flashback" forensic report for a hardcore NTR gangbang scene
> because `view_file` was never called on the actual image.

```
🛑 HARD GATE 0: IMAGE MUST BE VIEWED BEFORE ANY ANALYSIS

image_path = {{source_folder}}/{{current_page}}.webp

ACTION: Call view_file(image_path)

IF view_file SUCCEEDS:
  ✅ Image gate passed — visual ground truth established
  SET image_viewed = TRUE
  PROCEED

IF view_file FAILS:
  🚫 IMAGE GATE BLOCKED
  📋 Cannot view: {{image_path}}
  📤 ACTION: HALT. Request user to verify file path.
  DO NOT PROCEED. DO NOT GUESS. DO NOT INFER FROM TEXT.
```

**WHY THIS EXISTS:** The Page 004 Incident proved that without physically viewing the image, the agent will hallucinate scene content from OCR text and context files. This gate is NON-NEGOTIABLE.

---

## SEQUENCE OF INSTRUCTIONS

### 1. Announce Delegation

OUTPUT to user:

```
─────────────────────────────────────────────
📤 DELEGATING TO: Prof. Atomic 🔬 (Panel Forensic Analyst)
📋 TASK: Deep visual forensic analysis of page {{current_page}}
📁 INPUT: {{source_folder}}/{{current_page}}.webp
📁 OUTPUT: {{analysisFolder}}/page-{{current_page}}-forensic.md
─────────────────────────────────────────────
```

### 2. Execute Panel-Forensic Workflow

**CRITICAL**: Load and execute `{{panelForensicWorkflow}}` with:

- Input image: `{{source_folder}}/{{current_page}}.webp` (CURRENT FRAME GROUND TRUTH)
- Input context: `{{run_dir}}/{{current_page}}/context_horizon.md` (UPCOMING FRAME TRAJECTORY)
- Output path: `{{analysisFolder}}/page-{{current_page}}-forensic.md`

**⚡ FORENSIC CACHE (Performance Optimization):**

```text
previous_page = current_page - 1
previous_forensic = {{analysisFolder}}/page-{{previous_page}}-forensic.md

IF previous_forensic EXISTS:
  → Pass as BASELINE context to panel-forensic
  → Tell Kana: "Previous page had these characters, setting, and smells.
    Focus only on CHANGES from this baseline."
  → This reduces analysis time by ~50% for consecutive same-scene pages.

IF previous_forensic NOT EXISTS:
  → Proceed normally with full analysis (first page of chapter)
```

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
| File exists | {{analysisFolder}}/page-{{current_page}}-forensic.md | ✓/✗ | |
| image_path field | Present in frontmatter | ✓/✗ | |
| Panel count | ≥1 | | |
| Character IDs | ≥1 | | |
| SFX extracted | ≥1 | | |
| All 10 sections | Present | | |
```

**HANDOFF PROTOCOL (P1 Fix):** The forensic report MUST include `image_path` in its YAML frontmatter so downstream agents (Suki, Riko) can cross-reference the original image:

```yaml
---
manga: "{{manga_name}}"
page: {{page_num}}
image_path: "{{source_folder}}/{{current_page}}.webp"   # ← REQUIRED for cross-reference
created: "{{current_date}}"
---
```

**IF ANY CHECK FAILS:**

```
🚫 FORENSIC INCOMPLETE
Missing: {list_missing_items}
ACTION: Re-invoke panel-forensic
```

LOOP back to Step 2.

### 5. Update Pipeline State

Update `{{stateFile}}`:

```yaml
forensics_completed:
  - ... existing ...
  - {{current_page}}  # ADD this
```

### 6. Present Checkpoint Menu

OUTPUT:

```
✅ Forensic complete for page {{current_page}}!

📄 Report: {{analysisFolder}}/page-{{current_page}}-forensic.md
🔢 Panels: {count}
🎭 Characters: {count}
✨ SFX: {count}

**Select:** [C] Continue to Context Loading | [R] Re-run Forensic | [V] View Report
```

#### Menu Handling Logic

- IF C:
  - VERIFY forensic file exists (GATE CHECK)
  - IF EXISTS: Update state, load `./step-03-context-loading.md`
  - IF NOT EXISTS: "🚫 Cannot proceed - forensic missing" → Stay here
- IF R: Re-run from Step 2
- IF V: Display forensic report contents, then redisplay menu
- IF Any other: Respond helpfully, then redisplay menu

#### EXECUTION RULES (Interactive Mode)

- 🛑 **HALT** after displaying menu. Do NOT auto-proceed.
- ⏳ **WAIT** for explicit user input before taking any action.
- 🚫 Do NOT assume user intent or pre-load next step.

#### EXECUTION RULES (Batch Mode — `--batch`)

- ✅ **AUTO-CONTINUE**: If batch mode is active, skip the HALT and auto-select `[C]`.
- ✅ Gate checks still apply — if forensic file is missing, HALT even in batch mode.
- ✅ After completing this page's forensic, automatically advance `current_page` and loop back to **HARD GATE 0** for the next page in `pages_pending`.

---

## REQUIRED OUTPUTS

- MUST generate forensic report via /panel-forensic workflow
- MUST contain ALL 10 required sections
- MUST update pipeline state with completion

## VERIFICATION CHECKLIST

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
