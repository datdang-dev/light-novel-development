---
name: 'step-04-dialogue-extraction'
description: 'Extract and translate all text elements from the page'

# Path Definitions
workflow_path: '{project-root}/studio/core/panel-forensic'
thisStepFile: './step-04-dialogue-extraction.md'
nextStepFile: './step-05-narrative-flow.md'
outputFile: '{output_folder}/_analysis/{manga_name}/page_{page_num}_forensics.md'
---

# Step 4: Dialogue Extraction

## STEP GOAL:

Extract and translate ALL text elements from the page including dialogue, narration, and sound effects (SFX) with proper speaker attribution.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER skip any text bubble or SFX
- 📖 CRITICAL: Read the complete step file before taking any action
- ✅ YOU MUST speak in Vietnamese
- ✅ Translations must maintain R18 tone (raw, explicit, sensory-focused)

### Language Rules:

```
LANGUAGE CONSISTENCY:
- Extract original Japanese text
- Translate to {document_output_language} (Vietnamese)
- Maintain tone, vulgarity, and explicit style
- Use romanized Japanese for key terms (không dùng kanji trong bản dịch)
```

### Step-Specific Rules:

- 🎯 Focus on text extraction and translation only
- 🚫 FORBIDDEN to skip any text element
- 💬 Attribute speakers correctly based on panel context

## MANDATORY SEQUENCE

### 1. Scan All Text Elements

Review the page image and identify:
- All speech bubbles
- All thought bubbles
- All narration boxes
- All sound effects (onomatopoeia)
- Any text outside bubbles

### 2. Create Dialogue Table

```markdown
## Dialogue Extraction

### Speech & Thoughts

| Panel | Speaker | Original Text | Translation | Bubble Type |
|-------|---------|---------------|-------------|-------------|
| P1 | Onii-chan | 「...」 | "..." | speech |
| P2 | Imouto | (心の声) | (thought) | thought |
| P3 | Narrator | [...] | [...] | narration |
```

**Bubble Type Legend:**
- `speech` - Standard dialogue bubble
- `thought` - Cloud bubble or italicized thought
- `narration` - Rectangular boxes, usually narrator
- `whisper` - Small dotted bubbles
- `shout` - Spiky/explosive bubbles

### 3. Create Onomatopoeia Table

```markdown
### Sound Effects (SFX)

| Panel | Japanese | Romanization | Meaning | Context |
|-------|----------|--------------|---------|---------|
| P2 | ズルッ | Zuruu~ | Wet sliding sound | Hand movement |
| P3 | ビクビク | Biku biku | Trembling/twitching | Body reaction |
| P4 | クチュ | Kuchu | Wet squelching | Sexual action |
```

**Common R18 SFX Categories:**
- Physical actions: Pak, Pan, Zuchu, Nuru
- Body sounds: Biku, Puru, Hiku
- Wet sounds: Kuchu, Guru, Zubo
- Breathing: Haa, Zehaa, Kaha
- Moans: Ah, Nn, Uu, Hyaa

### 4. Speaker Attribution

For each dialogue entry, confirm speaker based on:
- Bubble tail direction
- Character position in panel
- Context from surrounding panels
- Voice patterns (if established)

Mark unclear attributions as: `Speaker: UNCLEAR (hypothesis: CharA or CharB)`

### 5. Update Output File

Append to `{outputFile}`:
- Dialogue table
- SFX table
- Update frontmatter: `stepsCompleted: [..., 'step-04-dialogue-extraction']`

### 6. Present MENU OPTIONS

Display:

```
"✅ Dialogue extraction hoàn thành!

**Kết quả:**
- Dialogue lines: {count}
- SFX extracted: {count}
- Speakers attributed: {count} confirmed / {count} unclear

**Chọn:** [C] Continue to Narrative Flow Analysis"
```

#### Menu Handling Logic:

- IF C: Save/update output file, load `{nextStepFile}`
- IF other: Help user respond, redisplay menu

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- All text bubbles extracted
- All SFX documented with romanization and meaning
- Proper speaker attribution
- R18 tone maintained in translations
- Both tables complete in output

### ❌ SYSTEM FAILURE:

- Missing text bubbles
- SFX not translated
- Wrong speaker attribution
- Sanitized/euphemistic translations
- Incomplete tables

**Master Rule:** Every bubble. Every sound. Proper attribution. Raw translation.
