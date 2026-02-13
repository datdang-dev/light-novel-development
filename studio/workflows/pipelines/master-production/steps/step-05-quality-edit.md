---
name: step-05-quality-edit
description: Dispatch to Quality Audit
goonerAuditWorkflow: {project-root}/studio/workflows/capabilities/gooner-audit/workflow.md
rewriteStepFile: ./step-04-prose-dispatch.md
projectRoot: {project-root}
---

# Step 5: Quality Audit & Critique 🧐

## STEP GOAL

Submit the prose for GOONER QUALITY AUDIT and determine final status.

## MANDATORY SEQUENCE OF INSTRUCTIONS

### 1. Identify Input

Locate the generated `prose_scene.md` (or `prose_output.md`).

### 2. Dispatch to Sub-Workflow

Load and execute the **Gooner Audit Workflow**:

**Workflow Path:** `{goonerAuditWorkflow}`

**Instructions:**

- Pass the prose file to Riko (Gooner Editor).
- Wait for the `audit_report.md` to be generated.

### 3. Analyze Verdict

Check the `audit_report.md`:

- **PASS:** Score >= 85 (or User Approval)
- **FAIL:** Score < 85 (or Critical Issues)

### 4. Present MENU OPTIONS

```
"✅ Audit Complete.

**Verdict:** {PASS/FAIL}
**Report:** {auditReportPath}

**Options:**
[F] Finish Pipeline (if PASS)
[R] Request Rewrite (if FAIL, returns to Prose dispatched)"
```

#### Menu Handling Logic

- IF [F]:
  - Generate `master-production-complete.md` summary
  - Notify User: "🚀 Pipeline Execution Successful!"
  - EXIT
- IF [R]:
  - Notify User: "Returning to Prose Adaptation..."
  - Load `{rewriteStepFile}`

## SYSTEM FAILURE METRICS

- Ignoring a FAIL verdict = **PROTOCOL VIOLATION**
