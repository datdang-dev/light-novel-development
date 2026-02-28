---
name: 'step-05-final-report'
description: 'Phase 4: Final Report Assembly'

outputFile: '{output_folder}/_analysis/{manga_name}/page_{page_num}_forensics.md'
---

# Step 5: Final Report Assembly

## STEP GOAL

Compile the logs from Phases 1, 2, and 3 into a clean, unified document format, and update the status to COMPLETE.

## MANDATORY EXECUTION RULES (READ FIRST)

### Universal Rules

- 🛑 Present the summarized data clearly for the Lewd Writer (Suki).
- 📖 CRITICAL: Read the complete step file before taking any action.
- ✅ YOU MUST speak in Vietnamese.

## MANDATORY SEQUENCE

### 1. Assemble the Final Continuity Notes

Review the data across the 3 phases. Write a brief "Continuity Notes" section that summarizes what state the scene ends in, which will be critical for the next page.

```markdown
## 4. Continuity Check
- **Character A (State):** {Location/posture/arousal level at end of page}
- **Character B (State):** {Location/posture/arousal level at end of page}
- **Environment:** {Messy, fluids everywhere, etc.}
```

### 2. Update Output File

Append the "Continuity Check" to the `{outputFile}`.
Update frontmatter:

- `stepsCompleted: [..., 'step-05-final-report']`
- `status: COMPLETE`

### 3. Present MENU OPTIONS

Display:

```text
"✅ Phân tích Panel Forensic (V6.1) hoàn tất! Cấu trúc Dialogue-Anchor đã được thiết lập thành công.

**File Output:** `{outputFile}`

**Trạng thái:** COMPLETE. Orchestrator có thể thu hồi Agent và chuyển tiếp sang bước Prose Generation."
```

#### EXECUTION RULES

- 🛑 **HALT**. The panel forensic workflow is now fully concluded.
