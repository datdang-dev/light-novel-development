---
name: 'step-01-context-loading'
description: 'Load forensic report and story bible context'

# Path Definitions
workflow_path: '{project-root}/studio/workflows/capabilities/prose-adapter'
thisStepFile: './step-01-context-loading.md'
nextStepFile: './step-02-scene-planning.md'
---

# Step 1: Context Loading

## STEP GOAL:

Load and internalize the forensic analysis and any available story bible context before beginning prose generation.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER start writing prose before context is loaded
- 📖 CRITICAL: Read the complete step file before taking any action
- ✅ YOU MUST speak in Vietnamese

### Step-Specific Rules:

- 🎯 Focus only on loading and understanding context
- 🚫 FORBIDDEN to begin prose generation here
- 💬 Confirm understanding with user before proceeding

## MANDATORY SEQUENCE

### 1. Request Forensic Report Path

If not provided:

```
"Chào bạn! Mình là Suki, chuyên gia viết prose R18. 🖊️

Để bắt đầu adapt từ forensic analysis, mình cần:

1. **Đường dẫn forensic report** (output từ panel-forensic)
2. **Manga name** và **page number**
3. **Story bible path** (nếu có, để maintain continuity)

Vui lòng cung cấp thông tin!"
```

### 2. Load Forensic Report

**CRITICAL:** Use `view_file` tool to load the complete forensic report.

Extract and note:
- Panel count and layout
- Character positions and actions
- Dialogue and SFX
- Fetish tags
- R18 elements
- Narrative flow

### 3. Load Story Bible (if available)

If bible path provided, load:
- Character profiles
- Relationship dynamics
- Previously established details
- Ongoing state (injuries, cumulative events)

### 4. Create Output File

Initialize prose output file:

```markdown
---
manga: "{manga_name}"
page: {page_num}
chapter: {ch_num}
created: "{date}"
stepsCompleted: ['step-01-context-loading']
status: IN_PROGRESS
source_forensics: "{forensics_path}"
---

# Prose: {manga_name} - Chapter {ch} Page {page_num}

## Context Summary

**Characters Present:** {list from forensics}
**Setting:** {from forensics}
**Primary Action:** {from forensics}
**Fetish Tags:** {from forensics}

---
```

### 5. Present MENU OPTIONS

```
"✅ Context loaded!

**Forensic Report:** {path}
**Panels:** {count}
**Characters:** {list}
**Primary Tags:** {tags}

**Bible Context:** {loaded / not available}

**Tiếp theo:** Scene structure planning

**Chọn:** [C] Continue to Scene Planning"
```

#### Menu Handling Logic:

- IF C: Save output file, load `{nextStepFile}`
- IF other: Help user respond, redisplay menu

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Forensic report fully loaded
- Key elements extracted
- Bible context loaded (if available)
- Output file initialized
- User confirms context understanding

### ❌ SYSTEM FAILURE:

- Not loading forensic report
- Starting prose without context
- Missing character identification
- Not creating output file

**Master Rule:** Understand completely before writing anything.
