---
name: 'step-05-quality-audit'
description: 'Invoke gooner-audit for quality check'

# Path Definitions
workflow_path: '{project-root}/studio/workflows/pipelines/gooner-alchemist'
thisStepFile: './step-05-quality-audit.md'
nextStepOnPass: './step-06-state-persistence.md'
nextStepOnFail: './step-04-prose-generation.md'
goonerAuditWorkflow: '{project-root}/studio/workflows/capabilities/gooner-audit/workflow.md'
---

# Step 5: Quality Audit

## STEP GOAL:

Invoke gooner-audit workflow to score and validate prose quality. Handle pass/fail routing.

## MANDATORY SEQUENCE

### 1. Invoke Gooner-Audit

```
"**📋 INVOKING GOONER-AUDIT**

Delegating to Riko for quality audit...

---

@/gooner-audit prose={prose_path}

---"
```

**EXECUTION:** Load gooner-audit workflow

### 2. Wait for Completion

Gooner-audit will:
1. Load prose
2. Banned word scan
3. Category scoring
4. Generate feedback
5. Render verdict

### 3. Process Verdict

```markdown
### Audit Results

**Score:** {X}/100
**Verdict:** {PASS / REVIEW / FAIL}

**Category Breakdown:**
- A: Sensory: {X}/25
- B: Rhythm: {X}/20
- C: Fetish: {X}/20
- D: Psychological: {X}/25
- E: Technical: {X}/10
```

### 4. Route Based on Verdict

```
IF verdict == PASS (≥85):
  → Update step 5: ✅ DONE
  → Proceed to step 6 (bible-sync SAVE)

IF verdict == REVIEW (70-84) or FAIL (<70):
  → Log revision feedback
  → Increment revision_count
  → Check max_attempts (3)
  
  IF revision_count < 3:
    → Return to step 4 (prose-adapter) with feedback
  ELSE:
    → PIPELINE PAUSE - Manual intervention required
```

### 5. Present MENU OPTIONS

**IF PASS:**

```
"✅ Audit PASSED!

**Score:** {X}/100

**Tiếp theo:** Save to bible

**Chọn:** [C] Continue to Bible Save"
```

**IF REVISION NEEDED:**

```
"⚠️ Audit: {verdict}

**Score:** {X}/100
**Revision attempt:** {X}/3

**Priority Fixes:**
{feedback summary}

**Chọn:** [R] Return to Prose Revision"
```

#### Menu Handling Logic:

- IF PASS + C: Load `{nextStepOnPass}`
- IF FAIL + R: Load `{nextStepOnFail}` with feedback

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Audit invoked properly
- Verdict processed
- Correct routing applied
- Revision loop handled

### ❌ SYSTEM FAILURE:

- Passing prose <85
- Not following revision loop
- Exceeding max attempts without pause

**Master Rule:** Quality gate. Route correctly. Loop until pass.
