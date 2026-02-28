---
name: step-02-order-review
description: Verify Sequence and Continuity
nextStepFile: ./step-03-add-transitions.md
---

# Step 2: Order & Review 🔍

## STEP GOAL

Verify prose files are in correct order and check continuity between pages.

## MANDATORY SEQUENCE OF INSTRUCTIONS

### 1. Verification Table

Check the end of Page N and start of Page N+1.
Look for:

- Clothing state changes
- Position shifts
- Dialogue flow

```markdown
## Continuity Check

| Transition | From | To | Status |
|------------|------|-----|--------|
| 1→2 | {end state} | {start state} | ✓/⚠️ |
| 2→3 | {end state} | {start state} | ✓/⚠️ |
```

### 2. Flag Issues

If continuity breaks are detected, list them:
`⚠️ Page 3→4: Sudden position change without transition.`

### 3. Present MENU OPTIONS

```
"✅ Order verified!

**Sequence:** Correct
**Continuity issues:** {count}

**Tiếp theo:** Add Transitions

**Chọn:** [C] Continue to Transitions"
```

#### Menu Handling Logic

- IF C: Load `{nextStepFile}`
- IF other: Redisplay menu

#### EXECUTION RULES:

- 🛑 **HALT** after displaying menu. Do NOT auto-proceed.
- ⏳ **WAIT** for explicit user input before taking any action.
- 🚫 Do NOT assume user intent or pre-load next step.
