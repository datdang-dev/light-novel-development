---
name: 'step-05-quality-audit'
description: 'Pre-repair JSON, invoke gooner-audit, and handle diff-based revision on failure'

nextStepOnPass: './step-06-state-persistence.md'
nextStepOnFail: './step-04-prose-generation.md'
goonerAuditWorkflow: '{project-root}/studio/services/quality-audit/references/workflow.md'
autoRepairScript: '{project-root}/studio/scripts/auto_repair.py'
draftProseSchema: '{project-root}/studio/schemas/draft-prose.schema.json'
auditReportSchema: '{project-root}/studio/schemas/audit-report.schema.json'
---

# Step 5: Quality Audit (with Pre-Repair + Diff-Based Revision)

## STEP GOAL

1. **Pre-Repair** the draft JSON using Python script (#5)
2. **Prefetch audit criteria** into context while pre-repair runs (#3)
3. Invoke gooner-audit to score prose quality
4. On failure, use **Diff-Based Revision** to fix only failing sections (#8)

## RULES

- ✅ YOU MUST ALWAYS SPEAK OUTPUT in Vietnamese
- MUST follow exact sequence below

---

## MANDATORY SEQUENCE

### 0. ⚡ PARALLEL PREFETCH (Performance Optimization #3)

**While the user reviews the prose from Step 4, pre-load Riko's audit criteria:**

```text
PRE-LOAD into context NOW (do not wait for audit invocation):
  ✅ {auditReportSchema} — Riko's grading structure
  ✅ Banned words list from pipeline-context.md
  ✅ Sensory density thresholds from quality_gates.md

PURPOSE: When audit is invoked, Riko can grade IMMEDIATELY
         without spending tokens re-reading scoring criteria.
```

### 1. ⚡ SCHEMA AUTO-REPAIR (Performance Optimization #5)

**Before sending to Riko, run the Python auto-repair script:**

```text
RUN: python3 {autoRepairScript} {prose_json_path} {draftProseSchema}

IF exit_code == 0:
  ✅ "Auto-repair complete — no structural issues (or auto-fixed)"
  → Proceed to audit

IF exit_code == 1:
  ❌ "Unfixable JSON error — needs LLM re-generation"
  → Return to Step 4 immediately (skip audit entirely)
```

**WHY:** This eliminates ~80% of audit failures caused by missing fields, wrong types, or miscounted words — all trivially fixable without spending LLM tokens.

### 2. Invoke Gooner-Audit

```bash
# 📋 INVOKING CURSOR CLI AUDITOR (RIKO)
# Delegating to Riko for quality audit...

agent -f {project-root}/studio/core/party-mode/riko-workspace/.cursorrules "Read {prose_path}. Follow AUDIT_STANDARD_v2.md exactly. Output the full structured JSON block as defined in Phase 6. Include per-category scores, violations with line numbers, and top_3_fixes."
```

**EXECUTION:** Execute the `agent` bash command above and capture the JSON output.

### 3. Wait for Completion

Gooner-audit will:

1. Load prose
2. Banned word scan
3. Category scoring
4. Generate feedback
5. Render verdict

### 4. Process Verdict

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

### 5. Route Based on Verdict

```text
IF verdict == PASS (≥85):
  → Update step 5: ✅ DONE
  → Proceed to step 6 (bible-sync SAVE)

IF verdict == REVIEW (70-84) or FAIL (<70):
  → ⚡ USE DIFF-BASED REVISION (Optimization #8)
  → DO NOT ask Suki to rewrite the entire 2000-word prose
  → Instead:
    1. Extract ONLY the failing categories from audit-report.json
    2. Extract the SPECIFIC paragraphs/sections that scored lowest
    3. Send to Suki: "Here is ONLY the failing section.
       Here is Riko's feedback. Rewrite ONLY this section."
    4. Suki returns ONLY the replacement paragraphs
    5. Python merge script patches the replacement into the original draft
    6. Re-run audit on the patched version

  → Increment revision_count
  → Check max_attempts (3)
  
  IF revision_count < 3:
    → Execute diff-based revision loop
  ELSE:
    → PIPELINE PAUSE - Manual intervention required
```

### 6. Present MENU OPTIONS

**IF PASS:**

```text
"✅ Audit PASSED!

**Score:** {X}/100
**Pre-Repair:** {repairs_count} auto-fixes applied
**Revision Method:** {full_rewrite | diff_patch | none}

**Tiếp theo:** Save to bible

**Chọn:** [C] Continue to Bible Save"
```

**IF REVISION NEEDED:**

```text
"⚠️ Audit: {verdict}

**Score:** {X}/100
**Revision attempt:** {X}/3
**Method:** Diff-Based (only failing sections will be rewritten)

**Failing Sections:**
{list of failing categories with scores}

**Chọn:** [R] Return to Diff-Based Revision"
```

#### Menu Handling Logic

- IF PASS + C: Load `{nextStepOnPass}`
- IF FAIL + R: Execute diff-based revision loop, then re-audit

#### EXECUTION RULES

- 🛑 **HALT** after displaying menu. Do NOT auto-proceed.
- ⏳ **WAIT** for explicit user input before taking any action.
- 🚫 Do NOT assume user intent or pre-load next step.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS

- Auto-repair applied before audit
- Audit criteria pre-loaded
- Diff-based revision used (not full rewrite)
- Correct routing applied

### ❌ SYSTEM FAILURE

- Passing prose <85
- Full rewrite instead of diff-patch
- Not following revision loop
- Exceeding max attempts without pause

**Master Rule:** Pre-repair. Prefetch. Audit. Diff-patch. Never full-rewrite.
