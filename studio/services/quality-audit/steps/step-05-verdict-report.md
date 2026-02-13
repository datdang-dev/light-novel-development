---
name: 'step-05-verdict-report'
description: 'Render final verdict and complete audit report'

# Path Definitions
workflow_path: '{project-root}/studio/services/quality-audit'
thisStepFile: './step-05-verdict-report.md'
auditOutput: '{output_folder}/_prose/{manga_name}/chapter_{ch}/page_{page_num}_audit.md'
---

# Step 5: Verdict & Report

## STEP GOAL:

Render the final audit verdict and complete the audit report with routing decision.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 📖 CRITICAL: This is the final step
- ✅ YOU MUST speak in Vietnamese

### Verdict Rules:

```
VERDICT THRESHOLDS:
- PASS (≥85): Prose approved for output
- REVIEW (70-84): Minor revisions, can re-audit
- FAIL (<70): Major revisions required
```

### Step-Specific Rules:

- 🎯 Render clear verdict
- 🚫 FORBIDDEN to pass prose <85
- 💬 Include clear next steps

## MANDATORY SEQUENCE

### 1. Determine Final Verdict

```markdown
## Final Verdict

### Score Summary

**TOTAL SCORE:** {X}/100

| Threshold | Range | Status |
|-----------|-------|--------|
| PASS | ≥85 | {✅ / ❌} |
| REVIEW | 70-84 | {✅ / ❌} |
| FAIL | <70 | {✅ / ❌} |

### VERDICT: {PASS / REVIEW / FAIL}
```

### 2. Route Based on Verdict

**IF PASS (≥85):**

```markdown
### ✅ VERDICT: PASS

**Prose Status:** APPROVED
**Quality:** Production Ready

**Next Steps:**
1. Prose can proceed to bible-sync SAVE
2. Ready for chapter compilation
3. No revisions required

**Pipeline Continuation:** Ready for gooner-alchemist step 6
```

**IF REVIEW (70-84):**

```markdown
### ⚠️ VERDICT: REVIEW

**Prose Status:** NEEDS MINOR REVISION
**Quality:** Almost Ready

**Required Actions:**
1. Address HIGH priority feedback items
2. Apply quick wins
3. Re-submit for audit

**Revision Attempt:** {X}/3

**Next Steps:**
1. Return prose to prose-adapter
2. Apply feedback from this audit
3. Re-run gooner-audit
```

**IF FAIL (<70):**

```markdown
### ❌ VERDICT: FAIL

**Prose Status:** MAJOR REVISION REQUIRED
**Quality:** Not Ready

**Critical Issues:**
{List top 3 critical problems}

**Required Actions:**
1. Address ALL HIGH priority items
2. Significant rewrite needed
3. Focus on {weakest category}

**Revision Attempt:** {X}/3

**Next Steps:**
1. Return to prose-adapter step 3 (environment)
2. Heavy revision required
3. Re-run full audit
```

### 3. Finalize Audit Report

Update `{auditOutput}` frontmatter:

```yaml
---
stepsCompleted: ['step-01-load-prose', 'step-02-banned-scan', 'step-03-category-scoring', 'step-04-generate-feedback', 'step-05-verdict-report']
status: {PASS / REVIEW / FAIL}
final_score: {X}
verdict: "{verdict}"
revision_needed: {true/false}
completed: "{timestamp}"
---
```

### 4. Workflow Completion

**IF PASS:**

```
"✅ GOONER AUDIT: PASS

**Score:** {X}/100
**Status:** APPROVED ✓

**Prose ready for:**
- bible-sync SAVE
- Chapter compilation

**AUDIT COMPLETE**"
```

**IF REVIEW/FAIL:**

```
"{emoji} GOONER AUDIT: {verdict}

**Score:** {X}/100
**Status:** REVISION NEEDED

**Priority Fixes:**
1. {top fix}
2. {second fix}

**Action:** Return to prose-adapter with feedback
**Attempts Remaining:** {3-X}

**AUDIT COMPLETE - REVISION REQUIRED**"
```

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Clear verdict rendered
- Correct routing based on score
- Audit report finalized
- Next steps clearly stated
- Revision loop tracked

### ❌ SYSTEM FAILURE:

- Ambiguous verdict
- Wrong routing
- Passing prose <85
- Missing next steps
- Not tracking revision attempts

**Master Rule:** Clear verdict. Correct routing. Track revisions.

---

## WORKFLOW END

This concludes the Gooner Audit workflow.

**Routes:**
- PASS → bible-sync SAVE → gooner-alchemist continuation
- REVIEW/FAIL → prose-adapter revision → re-audit
