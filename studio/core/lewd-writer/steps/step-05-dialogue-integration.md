---
name: 'step-05-dialogue-integration'
description: 'Weave dialogue and SFX into prose'

# Path Definitions
workflow_path: '{project-root}/studio/core/lewd-writer'
thisStepFile: './step-05-dialogue-integration.md'
nextStepFile: './step-05b-format-ensure.md'
---

# Step 5: Dialogue Integration

## STEP GOAL

Integrate dialogue and sound effects from the forensic extraction into the prose naturally, maintaining character voices and explicit tone.

## MANDATORY EXECUTION RULES (READ FIRST)

### Universal Rules

- 📖 CRITICAL: Read the complete step file before taking any action
- ✅ Write prose in {document_output_language} (Vietnamese)

### Dialogue Rules

```
LANGUAGE CONSISTENCY:
- ALL dialogue in Vietnamese
- ADAPT, DON'T TRANSLATE: Capture intent, not literal words
- Use romanized Japanese for specific terms ONLY (onii-chan, oppai)
- NO kanji or hiragana in final prose
- Maintain crude, degrading tone when appropriate
```

### Step-Specific Rules

- 🎯 Focus on weaving dialogue into existing prose
- 📖 READ AND APPLY: `{project-root}/.agent/rules/lewd_writing_mechanics.md`
- 🔄 REQUIRED to ADAPT dialogue. Do not translate literally. Capture intent and personality.
- 💬 Match dialogue to action timing from forensics

## MANDATORY SEQUENCE

### 1. Review Dialogue from Forensics

Load dialogue table from forensic report:

- Speaker attributions
- Bubble types (speech, thought, whisper, shout)
- SFX with romanizations and meanings

### 2. Integrate Speech Dialogue

For each dialogue entry:

```markdown
### Dialogue Integration

**Insert dialogue using SCRIPT FORMAT:**

[Revise existing prose to match this STRICT pattern:]

1. **Dialogue:** `Character Name: 「Speech content」`
2. **Thoughts:** `(Internal thought content)`
3. **Action/Narrative:** `*Action description or SFX*`

**Format Example:**
Alice: 「Em cảm thấy... ahh...」
*Cô bé rên rỉ, đầu ngả về phía sau, mái tóc vàng xõa tung trên gối.*
(Sướng quá... mình sắp hỏng mất...)
*Tiếng nịt đùi thắt chặt vào da thịt vang lên sột soạt.*
```

### 3. Integrate Thought/Narration

For thought bubbles and narration:

```markdown
**Thought Integration:**
- Italicize internal thoughts: *Không thể tin được...*
- Or use thought indicators: 'Trong đầu cô, chỉ còn...'

**Narration boxes:**
- Integrate as scene description or transition
```

### 4. Integrate SFX

From SFX table, weave sound effects:

```markdown
### SFX Integration

**Onomatopoeia Weaving:**

Replace generic descriptions with specific SFX:
- Generic: "Tiếng ướt át vang lên"
- With SFX: "Kuchu... kuchu... tiếng ướt nhẹp của ngón tay"

**Common Integration Patterns:**
- "Piak!" - impact sounds inline
- "Zuruu~" - extending sounds with ~
- "Biku biku" - body reactions
```

### 5. Review Dialogue Flow

Check all dialogue:

- [ ] All dialogue from forensics integrated
- [ ] All SFX used or adapted
- [ ] Dialogue matches character voices from planning
- [ ] Timing aligns with action prose
- [ ] No Japanese characters (use romanization only)

### 6. Update Output File

Update prose sections with dialogue:

- Update frontmatter: `stepsCompleted: [..., 'step-05-dialogue-integration']`

### 7. Present MENU OPTIONS

```
"✅ Dialogue integration hoàn thành!

**Dialogue lines:** {count}
**SFX integrated:** {count}

**Sample:**
> {dialogue sample with action}

**Tiếp theo:** Aftermath + Final polish

**Chọn:** [R] Revise dialogue [C] Continue to Aftermath"
```

#### Menu Handling Logic

- IF R: Ask what to revise, make changes, redisplay menu
- IF C: Save/update output file, load `{nextStepFile}`

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS

- All dialogue integrated naturally
- All SFX woven into prose
- Character voices consistent
- Timing matches action
- Vietnamese throughout (romanized JP only for terms)

### ❌ SYSTEM FAILURE

- Missing dialogue entries
- SFX not integrated
- Inconsistent character voice
- Japanese characters in text
- Dialogue not matching action timing

**Master Rule:** Every word spoken. Every sound made. Naturally woven.
