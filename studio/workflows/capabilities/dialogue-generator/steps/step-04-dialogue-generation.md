---
name: 'step-04-dialogue-generation'
description: 'Generate scene-specific dialogue'

thisStepFile: './step-04-dialogue-generation.md'
nextStepFile: './step-05-sfx-integration.md'
---

# Step 4: Dialogue Generation

## STEP GOAL:

Generate explicit dialogue for each scene beat following escalation and voice parameters.

## MANDATORY RULES

- Match calibrated voice for each character
- Follow escalation intensity
- Vietnamese with romanized Japanese terms
- Crude and explicit for R18 content

## MANDATORY SEQUENCE

### 1. Generate Per Beat

For each beat in escalation map:

```markdown
## Dialogue: {Beat Name} ({intensity}%)

### Context
{what's happening in this beat}

### Dialogue

**{Char1}:** "{appropriate dialogue for beat}"

**{Char2}:** "{response matching their voice}"

### Notes
- Voice check: ✓ sounds like {char}
- Intensity match: ✓ appropriate for {X}%
```

### 2. Dialogue Patterns

**Setup (10-20%):**
```
"Này... em có muốn...?" (complete, hesitant)
```

**Build (30-60%):**
```
"Thích... thích lắm... cho em thêm đi..." (fragmenting)
```

**Action (70-90%):**
```
"Đ-đừng dừng... ah... ah... sâu... sâu hơn—nn!" (broken, SFX)
```

**Climax (100%):**
```
"A—AHHHH! Ra... ra rồi... nnngh...!" (pure reaction)
```

**Aftermath (20%):**
```
"Hah... hah... nhiều quá..." (breathless recovery)
```

### 3. Present MENU

```
"✅ Dialogue generated!

**Lines created:** {count}
**Beats covered:** {list}

**Tiếp theo:** Add SFX

**Chọn:** [C] Continue"
```

---
