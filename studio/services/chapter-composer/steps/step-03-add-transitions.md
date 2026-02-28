---
name: step-03-add-transitions
description: Write connecting prose for page gaps
nextStepFile: ./step-04-format-chapter.md
---

# Step 3: Add Transitions 🌉

## STEP GOAL

Write transitional prose to connect pages smoothly where needed.

## MANDATORY SEQUENCE OF INSTRUCTIONS

### 1. Identify Gaps

Look for the `⚠️` gaps identified in Step 2.
Determine Type:

- **Time Skip:** "Một lúc sau..."
- **Scene Break:** `* * *`
- **POV Shift:** Change perspective.
- **Micro-Action:** Small connecting movement.

### 2. Draft Transitions

Write prose to fill the gaps.

```markdown
## Transition: Page {X} → Page {Y}
**Type:** {type}
**Content:** {new_prose}
```

### 3. Present MENU OPTIONS

```
"✅ Transitions added!

**Scene breaks:** {count}
**Connecting prose:** {count}

**Tiếp theo:** Format Chapter

**Chọn:** [C] Continue to Formatting"
```

#### Menu Handling Logic

- IF C: Load `{nextStepFile}`
- IF other: Redisplay menu

#### EXECUTION RULES:

- 🛑 **HALT** after displaying menu. Do NOT auto-proceed.
- ⏳ **WAIT** for explicit user input before taking any action.
- 🚫 Do NOT assume user intent or pre-load next step.
