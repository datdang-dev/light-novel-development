---
name: 'step-03-dialogue-alignment'
description: 'Phase 2: Dialogue Alignment and Character Mapping'

nextStepFile: './step-04-environmental-scan.md'
outputFile: '{output_folder}/_analysis/{manga_name}/page_{page_num}_forensics.md'
---

# Step 3: Dialogue Alignment & Character Mapping

## STEP GOAL

Take the raw text extracted in Phase 1 (Step 02) and physically anchor it to the characters in the artwork. Establish *who* is speaking, and their immediate *physical/emotional state* at the exact moment the line is delivered.

## MANDATORY EXECUTION RULES (READ FIRST)

### Universal Rules

- 🛑 YOU MUST USE the exact text from Step 02. Do NOT re-translate or invent new dialogue.
- 📖 CRITICAL: Read the complete step file before taking any action.
- ✅ YOU MUST speak in Vietnamese.
- 👁️ **ANCHOR RULE:** Evaluate cause-and-effect based *on the dialogue lines*, not the overarching R18 tropes.

## MANDATORY SEQUENCE

### 1. Load Raw Text Log

Read the "Phase 1: OCR Raw Text Log" generated from the previous step.

### 2. Anchor Characters to Dialogue

For each line of text, look at the image and locate the origin of the speech bubble tail or the placement of the text.

Define for each line:

- **Speaker:** Who is saying this?
- **Action/Expression:** What is their face/body doing *while* saying this? (e.g. `Đỏ mặt, mồ hôi đầm đìa, tay đang sờ vào...`)

### 3. Build the Alignment Matrix

Construct the following table based on your anchoring:

```markdown
## Phase 2: Dialogue Anchor Matrix

| Ref # | Speaker | Delivered Dialogue / Translation | Concurrent Physical Action / Expression |
|-------|---------|----------------------------------|-----------------------------------------|
| 1 | Kida | "Cái gì thế này...?" | Đổ mồ hôi hột, tay đang giữ mép cửa |
| 2 | Reira | "Trả lời tôi đi!" | Cau mày, tức giận, hai tay chống nạnh |
| 3 | [SFX] | *Biku biku* (Run rẩy) | Đùi của Reira đang cọ vào nhau |
```

*(Ensure all items from the Phase 1 OCR log are mapped here).*

### 4. Update Output File

Append the "Phase 2: Dialogue Anchor Matrix" to the `{outputFile}`.
Update frontmatter: `stepsCompleted: [..., 'step-03-dialogue-alignment']`

### 5. Present MENU OPTIONS

Display:

```text
"✅ Phase 2: Dialogue Alignment hoàn thành!

**Kết quả:**
- Số dòng thoại đã được gán nhân vật: {count}
- Các hành động vật lý đã được neo giữ thành công.

**Chọn:** [C] Continue to Phase 3: Environmental & Lewd Scanning"
```

#### Menu Handling Logic

- IF C: Save/update output file, load `{nextStepFile}`
- IF other: Help user respond, redisplay menu

#### EXECUTION RULES

- 🛑 **HALT** after displaying menu. Do NOT auto-proceed.
- ⏳ **WAIT** for explicit user input before taking any action.
- 🚫 Do NOT assume user intent or pre-load next step.
