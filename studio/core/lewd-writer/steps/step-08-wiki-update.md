---
name: 'step-08-wiki-update'
description: 'Recursive Universe - Update Story Bible with new facts'

nextStepFile: './step-09-final-report.md' # Or end
bibleFile: '{output_folder}/_bible/{project_name}/story-bible.md'
proseFile: '{output_folder}/_prose/{manga_name}/chapter_{ch}/page_{page_num}_prose.md'
---

# Step 8: Recursive Universe Update

## STEP GOAL

Extract new narrative facts, character developments, and lore from the generated prose and update the Story Bible. ALL changes in the operational reality must be recorded for future consistency.

## MANDATORY EXECUTION RULES

### Universal Rules

- 📖 CRITICAL: Read the complete step file before taking any action
- ✅ YOU MUST speak in Vietnamese

### Step-Specific Rules

- 🎯 EXTRACT FACTS only. Do not invent new things.
- 🚫 FORBIDDEN to overwrite existing bible sections. APPEND only.
- 💬 Format as Bullet Points under "## Recursive Updates" section.

## MANDATORY SEQUENCE

### 1. Read Generated Prose

Read the content of `{proseFile}`.

### 2. Extract Key Facts

Identify:

- **Character Growth:** New emotional states, traumas, acceptances.
- **Physical Changes:** Injuries, marks, clothing damage.
- **Relationship Shifts:** Trust levels, power dynamics.
- **Lore Definitions:** New terms or mechanics introduced.

### 3. Generate Update Block

Create a markdown block:

```markdown
## Update: Page {page_num}
- **{Character} State:** {New state}
- **Physical:** {mark/injury}
- **Lore:** {New fact}
```

### 4. Append to Story Bible

Append this block to `{bibleFile}` under a "## Dynamic Recursive History" section (create if missing).

### 5. Present MENU OPTIONS

```
"✅ Story Bible Updated!

**New Facts Recorded:**
- {fact 1}
- {fact 2}

**Tiếp theo:** Verification and Final Report
**Chọn:** [C] Continue to Final Report"
```

#### Menu Handling Logic

- IF C: Completion sequence.
- IF other: Redisplay menu.

#### EXECUTION RULES:

- 🛑 **HALT** after displaying menu. Do NOT auto-proceed.
- ⏳ **WAIT** for explicit user input before taking any action.
- 🚫 Do NOT assume user intent or pre-load next step.
