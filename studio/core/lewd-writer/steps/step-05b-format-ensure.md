---
name: 'step-05b-format-ensure'
description: 'Enforce strict Light Novel dialogue formatting rules'

# Path Definitions
workflow_path: '{project-root}/studio/core/lewd-writer'
thisStepFile: './step-05b-format-ensure.md'
nextStepFile: './step-06-aftermath-polish.md'
outputFile: '{output_folder}/_prose/{manga_name}/chapter_{ch}/page_{page_num}_prose.md'
---

# Step 5b: Ensure Dialogue Format

## STEP GOAL:
Strictly enforce Light Novel formatting standards for dialogue and thoughts before polishing.

## ⚠️ CRITICAL FORMATTING RULES (ZERO TOLERANCE)

### 1. Dialogue Brackets
- **RULE:** Spoken dialogue MUST use Japanese-style corner brackets `「...」`.
- **FORBIDDEN:** Standard quotation marks `""` or `""` for speech.
- **CORRECTION:**
  - ❌ "Dừng lại!"
  - ✅ 「Dừng lại!」

### 2. Internal Thoughts
- **RULE:** Internal monologues/thoughts MUST use parentheses `(...)`.
- **FORBIDDEN:** Italics *text* or quotes `""` for thoughts.
- **CORRECTION:**
  - ❌ *Hắn ta đang nhìn mình...*
  - ❌ "Hắn ta đang nhìn mình..."
  - ✅ (Hắn ta đang nhìn mình...)

### 3. Sound Effects (SFX)
- **RULE:** SFX should be in italics `*SFX*` or plain text if capitalized for impact.
- **standard:** `*Kinh coong~*` or `KINH COONG~`

---

## EXECUTION SEQUENCE

### 1. Scan Content
Read the current state of `{outputFile}`.

### 2. Identify Violations
Check for:
- [ ] Usage of double quotes `"` for dialogue.
- [ ] Usage of plain italics or quotes for thoughts.
- [ ] Inconsistent spacing around brackets.

### 3. Apply Fixes
- **Global Replace:** Convert all `"Speech"` to `「Speech」`.
- **Global Replace:** Convert all *"Thought"* or "Thought" to `(Thought)`.
- **Verify:** Ensure no stray quotes remain.

### 4. Update Frontmatter
Update `stepsCompleted` to include `step-05b-format-ensure`.

```yaml
stepsCompleted: [..., 'step-05-dialogue-integration', 'step-05b-format-ensure']
```

---

## COMPLETION CHECK
- [ ] All dialogue inside `「...」`?
- [ ] All thoughts inside `(...)`?
- [ ] File saved with corrections?

If YES, proceed to `step-06-aftermath-polish.md`.
