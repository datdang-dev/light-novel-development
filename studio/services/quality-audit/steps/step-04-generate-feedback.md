---
name: 'step-04-generate-feedback'
description: 'Generate specific improvement feedback'

# Path Definitions
workflow_path: '{project-root}/studio/services/quality-audit'
thisStepFile: './step-04-generate-feedback.md'
nextStepFile: './step-05-verdict-report.md'
---

# Step 4: Generate Feedback

## STEP GOAL:

Generate specific, actionable feedback for prose improvement based on category scores.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 📖 CRITICAL: Read the complete step file before taking any action
- ✅ YOU MUST speak in Vietnamese

### Feedback Rules:

```
FEEDBACK PRINCIPLES:
- Specific, not vague ("add 2 more smell descriptions in section 3")
- Actionable ("change X to Y")
- Prioritized by impact
- Include examples when possible
```

### Step-Specific Rules:

- 🎯 Focus on LOW-scoring areas first
- 🚫 FORBIDDEN to give vague feedback like "improve sensory details"
- 💬 Provide specific line/section references

## MANDATORY SEQUENCE

### 1. Identify Weak Categories

Based on scoring:

```markdown
## Improvement Feedback

### Priority Analysis

| Category | Score | Status | Priority |
|----------|-------|--------|----------|
| {lowest} | {X/max} | NEEDS WORK | 🔴 HIGH |
| {second} | {X/max} | IMPROVE | 🟡 MEDIUM |
| {third} | {X/max} | OK | 🟢 LOW |
```

### 2. Generate Category-Specific Feedback

For each category scoring below threshold:

```markdown
### Category {X}: {Name} - Feedback

**Current Score:** {X}/{max}
**Target Score:** {threshold}
**Gap:** {points needed}

**Specific Issues:**

1. **{Issue 1}**
   - Location: {section/line}
   - Problem: {what's wrong}
   - Fix: {specific action}
   - Example: "{before}" → "{after}"

2. **{Issue 2}**
   - Location: {section/line}
   - Problem: {what's wrong}
   - Fix: {specific action}
```

### 3. Generate Sensory Fixes (if A < threshold)

```markdown
### Sensory Additions Required

**Smell (Current: {X}, Need: 3+):**
- Add at: {section} - Suggest: "{specific smell description}"
- Add at: {section} - Suggest: "{specific smell description}"

**Touch (Current: {X}, Need: 5+):**
- Add at: {section} - Suggest: "{texture description}"

**Sound (Current: {X}, Need: 3+):**
- Add at: {section} - Suggest: "{sound/SFX}"
```

### 4. Generate Structure Fixes (if B < threshold)

```markdown
### Structure Improvements

**Escalation Issues:**
- {specific pacing problem}
- Fix: {how to improve}

**Aftermath Issues:**
- {what's missing/truncated}
- Fix: {what to add}
```

### 5. Generate Quick Wins

Identify easy fixes for +5-10 points:

```markdown
### Quick Wins (Easy +5-10 points)

1. **{Quick fix 1}** (+{X} pts)
   - Action: {simple change}

2. **{Quick fix 2}** (+{X} pts)
   - Action: {simple change}
```

### 6. Update Audit Report

Append feedback to audit report:
- Update frontmatter: `stepsCompleted: [..., 'step-04-generate-feedback']`

### 7. Present MENU OPTIONS

```
"✅ Feedback generated!

**Priority Areas:**
🔴 {category}: {brief issue}
🟡 {category}: {brief issue}

**Quick wins available:** {count}

**Tiếp theo:** Final verdict

**Chọn:** [C] Continue to Verdict"
```

#### Menu Handling Logic:

- IF C: Save audit, load `{nextStepFile}`
- IF other: Help user respond, redisplay menu

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Weak categories identified
- Specific feedback for each issue
- Examples provided where helpful
- Quick wins identified
- Actionable improvements listed

### ❌ SYSTEM FAILURE:

- Vague feedback like "needs more detail"
- No specific locations cited
- No examples provided
- Missing priority ranking

**Master Rule:** Specific. Actionable. With examples.
