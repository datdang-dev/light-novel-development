---
name: 'step-02-pure-ocr-extraction'
description: 'Phase 1: MCP-Assisted OCR Extraction (Zero-Skip Protocol)'

nextStepFile: './step-03-dialogue-alignment.md'
outputFile: '{output_folder}/_analysis/{manga_name}/page_{page_num}_forensics.md'
---

# Step 2: Pure OCR Extraction (MCP-Assisted)

## STEP GOAL

Prevent AI hallucination by isolating the text extraction process completely from visual semantics. Use the **manga-ocr MCP tool** as the primary text extraction engine, then perform a visual verification pass to catch anything the tool missed.

> [!IMPORTANT]
> **Text-First Philosophy:** You MUST extract text via MCP tool BEFORE looking at the artwork. This prevents visual bias from contaminating your text reading.

## MANDATORY EXECUTION RULES (READ FIRST)

### Universal Rules

- 🛑 NEVER assume or invent text. If you can't read it clearly, mark it as `[...]`.
- 📖 CRITICAL: Read the complete step file before taking any action.
- ✅ YOU MUST output the final translations in Vietnamese.
- ✅ FORBIDDEN: Do NOT guess who is speaking. Do NOT describe what they are doing. JUST EXTRACT TEXT.

### Step-Specific Rules

- 👁️ **IGNORE THE ART** during OCR phase. You are ONLY looking for text content.
- 🎯 MCP tool already sorts output Right-to-Left, Top-to-Bottom (standard manga format).
- 🌐 **Language Support:** `en` (English translations), `ja` (Japanese RAW), `ch` (Chinese scanlations).

## MANDATORY SEQUENCE

### 1. MCP Tool Extraction (Primary)

Call the `ocr_full_page` MCP tool on the page image:

```
Tool: ocr_full_page
Args:
  image_path: "{file_path}"    ← Absolute path to the page image
  lang: "{lang}"               ← "en", "ja", or "ch" based on source material
```

**Language Selection Guide:**

- `en` → English-translated manga (ALL CAPS output, best accuracy)
- `ja` → Japanese RAW manga (Hiragana/Katakana/Kanji output)
- `ch` → Chinese scanlation/翻译版 (Simplified/Traditional Chinese output)

Record the raw MCP output as-is. This is your **OCR Ground Truth**.

### 2. Visual Verification Pass (Secondary)

NOW view the image with `view_file` tool. Compare what you see against the MCP output:

- ✅ Confirm each MCP bubble matches a visible text element on the page
- 🔍 Look for text the MCP **missed** (small SFX, background text, narration boxes)
- ⚠️ Flag any MCP text that looks wrong or garbled (OCR artifacts)
- 📝 Add any missed items with `[MANUAL]` prefix

> [!CAUTION]
> **Inference Rule:** If you see artwork that is ambiguous (unclear what's being drawn), use the OCR text to INFER what the art depicts. Text is more reliable than visual interpretation for manga with complex/dense art.

### 3. Build the OCR Raw Text Log

Merge MCP output + manual additions into the standardized format:

```markdown
## Phase 1: OCR Raw Text Log

*Extracted via MCP `ocr_full_page` tool + Visual Verification.*
*Source Language: {lang} | Reading Order: RTL*

1. **[Bubble 1]**
   - **Original:** "..."
   - **Translation (VN):** "..."
2. **[Bubble 2]**
   - **Original:** "..."
   - **Translation (VN):** "..."
3. **[SFX 1]** [MANUAL]
   - **Original/Romanized:** ドキドキ (Doki doki)
   - **Translation (VN):** *Tim đập thình thịch*
```

**Types to extract:**

- Speech bubbles (from MCP output)
- Thought bubbles (from MCP output)
- Narration rectangles (from MCP output)
- Prominent SFX text (usually requires MANUAL addition — MCP filters these as noise)

### 4. Update Output File

Append the "Phase 1: OCR Raw Text Log" to the `{outputFile}`.
Update frontmatter: `stepsCompleted: [..., 'step-02-pure-ocr-extraction']`

### 5. Present MENU OPTIONS

Display:

```text
"✅ Phase 1: Pure OCR Extraction hoàn thành!

**Kết quả:**
- Nguồn: MCP `ocr_full_page` ({lang}) + Visual Verification
- Số lượng hộp thoại quét được: {count_mcp} (MCP) + {count_manual} (Manual)
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
