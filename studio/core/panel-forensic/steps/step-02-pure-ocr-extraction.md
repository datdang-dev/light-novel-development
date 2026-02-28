---
name: 'step-02-pure-ocr-extraction'
description: 'Phase 1: Pure Optical Character Recognition (Zero-Skip Protocol)'

nextStepFile: './step-03-dialogue-alignment.md'
outputFile: '{output_folder}/_analysis/{manga_name}/page_{page_num}_forensics.md'
---

# Step 2: Pure OCR Extraction

## STEP GOAL

Prevent AI hallucination by isolating the text extraction process completely from visual semantics. Your ONLY objective is to transcribe 100% of the visible text bubbles and text boxes on the page and translate them, WITHOUT interpreting the art, characters, or context.

## MANDATORY EXECUTION RULES (READ FIRST)

### Universal Rules

- 🛑 NEVER assume or invent text. If you can't read it clearly, mark it as `[...]`.
- 📖 CRITICAL: Read the complete step file before taking any action.
- ✅ YOU MUST output the final translations in Vietnamese.
- ✅ FORBIDDEN: Do NOT guess who is speaking. Do NOT describe what they are doing. JUST EXTRACT TEXT.

### Step-Specific Rules

- 👁️ **IGNORE THE ART:** You must mentally blur the character artwork and background. You are ONLY looking for speech bubbles, thought bubbles, and hardcoded text boxes.
- 🎯 Read from Top-Right to Bottom-Left (standard Japanese manga format).

## MANDATORY SEQUENCE

### 1. Execute Pure OCR Scan

Scan the provided `{file_path}` image solely for text bounding boxes.

```markdown
## Phase 1: OCR Raw Text Log

*List extracted text from Top-Right to Bottom-Left.*

1. **[Bubble/Box 1]**
   - **Original:** 「...」
   - **Translation:** "..."
2. **[Bubble/Box 2]**
   - **Original:** 「...」
   - **Translation:** "..."
3. **[SFX 1]**
   - **Original/Romanized:** Zuruu~ (ズルッ)
```

**Types to extract:**

- Speech bubbles
- Thought bubbles
- Narration rectangles
- Prominent SFX text (Romanize them)

### 2. Update Output File

Append the "Phase 1: OCR Raw Text Log" to the `{outputFile}`.
Update frontmatter: `stepsCompleted: [..., 'step-02-pure-ocr-extraction']`

### 3. Present MENU OPTIONS

Display:

```text
"✅ Phase 1: Pure OCR Extraction hoàn thành!

**Kết quả:**
- Số lượng hộp thoại quét được: {count}
- Tình trạng: OCR thô, chưa gán nhân vật.

**Chọn:** [C] Continue to Phase 2: Dialogue Alignment"
```

#### Menu Handling Logic

- IF C: Save/update output file, load `{nextStepFile}`
- IF other: Help user respond, redisplay menu

#### EXECUTION RULES

- 🛑 **HALT** after displaying menu. Do NOT auto-proceed.
- ⏳ **WAIT** for explicit user input before taking any action.
- 🚫 Do NOT assume user intent or pre-load next step.
