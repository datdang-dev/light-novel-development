---
name: 'step-05-final-report'
description: 'Phase 4: Final Report Assembly'

outputFile: '{output_folder}/_analysis/{manga_name}/page_{page_num}_forensics.json'
---

# Step 5: Final Report Assembly

## STEP GOAL

Compile the logs from Phases 1, 2, and 3 into the final `forensic-state.json` format, ensuring Content Tags are extracted for the JIT RAG system.

## MANDATORY EXECUTION RULES (READ FIRST)

### Universal Rules

- 🛑 Present the summarized data strictly adhering to the `studio/schemas/forensic-state.schema.json` format.
- 📖 CRITICAL: Read the complete step file before taking any action.

## MANDATORY SEQUENCE

### 1. Extract Content Tags

Analyze the visual and dialogue content to generate an array of `content_tags`.

- These are keywords that describe the fetish, setting, or specific actions (e.g., `["creampie", "mesugaki", "indoor_office"]`).
- These tags will be used by the RAG system to fetch relevant research files.

### 2. Assemble the JSON

Review the data across the 3 phases. Assemble a strict JSON object that validates against `forensic-state.schema.json`.

### 3. Update Output File

Write the generated JSON to `{outputFile}`.
Update frontmatter of the session state:

- `stepsCompleted: [..., 'step-05-final-report']`
- `status: COMPLETE`

### 4. Present MENU OPTIONS

Display:

```text
"✅ Phân tích Panel Forensic (V6.1) hoàn tất! Cấu trúc Dialogue-Anchor đã được thiết lập thành công.

**File Output:** `{outputFile}`

**Trạng thái:** COMPLETE. Orchestrator có thể thu hồi Agent và chuyển tiếp sang Core Transformation Engine."
```

#### EXECUTION RULES

- 🛑 **HALT**. The panel forensic workflow is now fully concluded.
