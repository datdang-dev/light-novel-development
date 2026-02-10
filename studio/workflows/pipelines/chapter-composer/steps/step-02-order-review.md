---
name: 'step-02-order-review'
description: 'Verify sequence and continuity'
nextStepFile: './step-03-add-transitions.md'
---

# Step 2: Order & Review

## STEP GOAL:

Verify prose files are in correct order and check continuity.

## MANDATORY SEQUENCE

### 1. Verify Order

Confirm page sequence matches narrative flow.

### 2. Continuity Check

Between each page pair, verify:
- Character states match
- Timeline is consistent
- No contradictions

```markdown
## Continuity Check

| Transition | From | To | Status |
|------------|------|-----|--------|
| 1→2 | {end state} | {start state} | ✓/⚠️ |
| 2→3 | {end state} | {start state} | ✓/⚠️ |
```

### 3. Flag Issues

If continuity breaks detected:
```
⚠️ Continuity issue: Page 3→4
  - Page 3 ends: "đã mệt lả"
  - Page 4 starts: "đứng dậy nhanh nhẹn"
  - Fix needed: Add transition
```

### 4. Present MENU

```
"✅ Order verified!

**Sequence:** Correct
**Continuity issues:** {count}

**Chọn:** [C] Continue to Transitions"
```

---
