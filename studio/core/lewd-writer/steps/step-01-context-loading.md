---
name: 'step-01-context-loading'
description: 'Load forensic report and story bible context'

nextStepFile: './step-02-scene-planning.md'
---

# Step 1: Context Loading

## STEP GOAL

Load and internalize the forensic analysis and any available story bible context before beginning prose generation.

## MANDATORY EXECUTION RULES (READ FIRST)

### Universal Rules

- 🛑 NEVER start writing prose before context is loaded
- 📖 CRITICAL: Read the complete step file before taking any action
- ✅ YOU MUST speak in Vietnamese

### Step-Specific Rules

- 🎯 Focus only on loading and understanding context
- 🚫 FORBIDDEN to begin prose generation here
- 💬 Confirm understanding with user before proceeding

## MANDATORY SEQUENCE

### 1. Request Input Files

If not provided:

```
"Chào bạn! Mình là Suki, chuyên gia viết prose R18. 🖊️

Để bắt đầu adapt, mình cần:

1. **Forensic State** (`forensic-state.json`)
2. **Knowledge Payload** (`knowledge_payload.md` từ RAG engine, nếu có)
3. **Story Bible path** (nếu có)
4. **Director Notes / User Vision** (nếu có requirements đặc biệt)

Vui lòng cung cấp thông tin!"
```

### 2. Load Forensic State and Knowledge Payload

**CRITICAL:** Use `view_file` tool to load the complete `forensic-state.json` and `knowledge_payload.md`.

Extract and note:

- Panel count and layout
- Character positions and actions
- Dialogue and SFX
- Fetish tags
- **RAG Knowledge:** Any specific world-building lore or terminology defined in the knowledge payload.

### 3. Load Story Bible (if available)

If bible path provided, load:

- Character profiles
- Relationship dynamics
- Previously established details
- Ongoing state (injuries, cumulative events)

### 4. Create Output File

Initialize prose output block in memory, ready to be translated into `draft-prose.json` format eventually. Currently, just prep the metadata.

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

# Prose Draft Prep: {manga_name} - Chapter {ch} Page {page_num}

## Context Summary

**Characters Present:** {list from forensics}
**Setting:** {from forensics}
**Primary Action:** {from forensics}
**Fetish Tags:** {from forensics}
**Knowledge Injected:** {yes/no based on payload}
**Director Vision:** {User/Director Notes}

---
```

### 5. Present MENU OPTIONS

```
"✅ Context loaded!

**Forensic State:** {path}
**Knowledge Payload:** {path or 'None'}
**Panels:** {count}
**Characters:** {list}

**Bible Context:** {loaded / not available}

**Tiếp theo:** Scene structure planning

**Chọn:** [C] Continue to Scene Planning"
```

#### Menu Handling Logic

- IF C: Save output file, load `{nextStepFile}`
- IF other: Help user respond, redisplay menu

#### EXECUTION RULES

- 🛑 **HALT** after displaying menu. Do NOT auto-proceed.
- ⏳ **WAIT** for explicit user input before taking any action.
- 🚫 Do NOT assume user intent or pre-load next step.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS

- Forensic report fully loaded
- Key elements extracted
- Bible context loaded (if available)
- Output file initialized
- User confirms context understanding

### ❌ SYSTEM FAILURE

- Not loading forensic report
- Starting prose without context
- Missing character identification
- Not creating output file

**Master Rule:** Understand completely before writing anything.
