---
name: 'step-02-voice-calibration'
description: 'Establish dialogue parameters per character'

thisStepFile: './step-02-voice-calibration.md'
nextStepFile: './step-03-escalation-mapping.md'
---

# Step 2: Voice Calibration

## STEP GOAL:

Calibrate dialogue parameters for each character based on their profiles.

## MANDATORY SEQUENCE

### 1. Extract Voice Parameters

For each character:

```markdown
## Voice Calibration

### {Character Name}

**Base Speech:**
- Formality: {casual/formal/crude}
- Speed: {fast/slow/variable}
- Quirks: {specific patterns}

**R18 Speech:**
- When dominant: {style}
- When submissive: {style}
- Moaning style: {loud/quiet/specific sounds}

**Vocabulary:**
- Preferred crude words: {list}
- Catchphrases: {list}
- Words to avoid: {antithema to character}
```

### 2. Contrast Check

Ensure characters sound distinct:

```
Character A says: "{example}"
Character B says: "{example}"

→ Distinct? YES/NO
→ Adjustments needed: {if any}
```

### 3. Present MENU

```
"✅ Voices calibrated!

**{Char1}:** {brief style}
**{Char2}:** {brief style}

**Tiếp theo:** Map escalation

**Chọn:** [C] Continue"
```

---
