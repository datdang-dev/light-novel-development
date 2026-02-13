---
name: step-01-forensic-dispatch
description: Dispatch to Panel Forensic Workflow
nextStepFile: ./step-02-context-prep.md
panelForensicWorkflow: {project-root}/studio/workflows/capabilities/panel-forensic/workflow.md
projectRoot: {project-root}
---

# Step 1: Forensic Analysis 🔬

## STEP GOAL

Execute the Panel Forensic Workflow to analyze the input image/page.

## MANDATORY EXECUTION RULES

- 🛑 **NEVER** skip forensic analysis.
- 🛑 **ALWAYS** load the sub-workflow fully.
- ✅ **VERIFY** the forensic report exists before proceeding.

## SEQUENCE OF INSTRUCTIONS

### 1. Identify Input

Locate the image or page reference provided by the user.

### 2. Dispatch to Sub-Workflow

Load and execute the **Panel Forensic Workflow**:

**Workflow Path:** `{panelForensicWorkflow}`

**Instructions:**

- Pass the input image/page to the sub-workflow.
- Wait for it to complete and generate `forensic_report.md`.

### 3. Verify Output

Check that the report was generated successfully.

### 4. Present MENU OPTIONS

```
"✅ Forensic Analysis Complete (or skipped if existing).

**Report:** {forensicReportPath}

**Tiếp theo:** Prepare Context

**Chọn:** [C] Continue to Context Prep"
```

#### Menu Handling Logic

- IF C: Load `{nextStepFile}`
- IF other: Redisplay menu

## SYSTEM FAILURE METRICS

- Proceeding without forensic report = **CRITICAL FAILURE**
