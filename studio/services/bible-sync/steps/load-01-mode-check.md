---
name: 'load-01-mode-check'
description: 'Verify LOAD mode and check bible existence'

nextStepFile: './load-02-load-characters.md'
biblePath: '{output_folder}/_bible/{project_name}'
---

# LOAD Step 1: Mode Check

## STEP GOAL:

Verify this is LOAD mode and check if story bible exists for the project.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 📖 CRITICAL: Read the complete step file before taking any action
- ✅ YOU MUST speak in Vietnamese

### Step-Specific Rules:

- 🎯 Focus on verification only
- 🚫 FORBIDDEN to modify bible in LOAD mode
- 💬 Detect first chapter scenario if no bible

## MANDATORY SEQUENCE

### 1. Verify Mode

```
IF mode != "LOAD":
  ERROR: Wrong mode. Use SAVE mode steps for saving.
  EXIT
```

### 2. Request Project Info

If not provided:

```
"**BIBLE-SYNC: LOAD MODE**

Cần thông tin:
1. **Project name:** (folder name)
2. **Chapter/Page:** đang adapt
3. **Characters cần load:** (nếu biết trước)

Vui lòng cung cấp!"
```

### 3. Check Bible Existence

```markdown
## Mode Check

**Mode:** LOAD
**Project:** {project_name}
**Bible Path:** {biblePath}

### Bible Status Check

- [ ] story-bible.md exists
- [ ] characters/ folder exists
- [ ] state/ folder exists
```

### 4. Determine Path

```
IF bible exists:
  → Proceed to load-02-load-characters.md
  → Status: EXISTING_BIBLE

IF bible does NOT exist:
  → First Chapter Protocol
  → Create initial bible structure
  → Status: NEW_BIBLE
```

### 5. First Chapter Protocol (if needed)

If no bible exists, create structure:

```
mkdir -p {biblePath}/characters
mkdir -p {biblePath}/world
mkdir -p {biblePath}/state

Create story-bible.md with template
Create current-state.yaml (empty)
Create cumulative-log.md (empty)
```

### 6. Present MENU OPTIONS

**IF EXISTING:**

```
"✅ Bible found!

**Project:** {project_name}
**Status:** EXISTING_BIBLE

**Tiếp theo:** Load character profiles

**Chọn:** [C] Continue to Load Characters"
```

**IF NEW:**

```
"📘 No bible found - First Chapter Protocol

**Project:** {project_name}
**Status:** NEW_BIBLE (created structure)

**Tiếp theo:** Load characters from forensics

**Chọn:** [C] Continue"
```

#### Menu Handling Logic:

- IF C: Load `{nextStepFile}`

#### EXECUTION RULES:

- 🛑 **HALT** after displaying menu. Do NOT auto-proceed.
- ⏳ **WAIT** for explicit user input before taking any action.
- 🚫 Do NOT assume user intent or pre-load next step.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Mode verified as LOAD
- Bible existence checked
- First chapter handled if needed
- Correct path determined

### ❌ SYSTEM FAILURE:

- Wrong mode executed
- Missing project info
- Not detecting first chapter

**Master Rule:** Check first. Create if needed. Never lose context.
