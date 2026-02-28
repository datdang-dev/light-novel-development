---
name: 'step-01-context-load'
description: 'Load character profiles and scene context'

nextStepFile: './step-02-voice-calibration.md'
---

# Step 1: Context Load

## STEP GOAL:

Load character profiles and scene context for dialogue generation.

## MANDATORY SEQUENCE

### 1. Miki Introduction

```
"**💬 DIALOGUE GENERATOR - Miki speaking**

Chào! Mình là Miki, dialogue specialist.

Mình cần:
1. **Character profiles:** Những ai trong scene?
2. **Scene context:** Đang ở đâu, làm gì?
3. **Forensic/prose reference:** (optional) để match context

Cung cấp thông tin nhé!"
```

### 2. Load Character Profiles

For each character in scene:
- Load speech patterns
- Load R18 dialogue samples
- Note catchphrases

### 3. Understand Scene

```markdown
## Scene Context

**Location:** {where}
**Characters:** {who}
**Current beat:** {setup/build/action/climax/aftermath}
**Power dynamic:** {who dominant}
```

### 4. Present MENU

```
"✅ Context loaded!

**Characters:** {list}
**Scene:** {brief}

**Tiếp theo:** Voice calibration

**Chọn:** [C] Continue"
```

---
