---
name: 'step-04-state-compilation'
description: 'Compile physical and emotional states'

thisStepFile: './step-04-state-compilation.md'
nextStepFile: './step-05-output-generation.md'
---

# Step 4: State Compilation

## STEP GOAL:

Compile character states for bible-sync consumption.

## STATE CATEGORIES

```yaml
physical:
  clothing: "{current state at end of page}"
  injuries: []
  fluids: []
  position: "{final position}"

emotional:
  mood: "{dominant emotion}"
  arousal: 0-10
  consent: "explicit / implied / coerced / none"
```

## MANDATORY SEQUENCE

### 1. Determine Final States

For each character, at END of page:

```markdown
## State Compilation

### char_001 Final State

**Physical:**
- Clothing: {end state}
- Position: {where/how}
- Injuries: {if any}
- Fluids: {if any}

**Emotional:**
- Mood: {primary emotion}
- Arousal: {0-10}
- Consent status: {type}

**Source Panel:** {last appearance}
```

### 2. Track State Changes

Document progression through page:

```markdown
### State Progression

| Panel | Physical Change | Emotional Change |
|-------|-----------------|------------------|
| 1 | {starting state} | {starting mood} |
| 3 | {change} | {change} |
| 7 | {final} | {final} |
```

### 3. Present MENU

```
"✅ States compiled!

**Characters with state:** {count}

**Final states:**
- char_001: {brief physical}, {mood}
- char_002: {brief physical}, {mood}

**Chọn:** [C] Continue to Output Generation"
```

---
