---
name: 'step-09-final-report'
description: 'Finalize Prose Adaptation and Handover'

# Path Definitions
workflow_path: '{project-root}/studio/workflows/capabilities/prose-adapter'
thisStepFile: './step-09-final-report.md'
outputFile: '{output_folder}/_prose/{manga_name}/chapter_{ch}/page_{page_num}_prose.md'
---

# Step 9: Final Report & Handover

## STEP GOAL

Finalize the adaptation process, ensure all artifacts are saved, and hand over to the auditing phase.

## MANDATORY SEQUENCE

### 1. Verification of recursive updates

Confirm that Sorty Bible updates (from Step 8) have been appended (if any).

### 2. Final Output Status Update

Update `{outputFile}` frontmatter to mark as complete:

```yaml
---
stepsCompleted: ['step-01-context-loading', 'step-02-scene-planning', 'step-03-environment-prose', 'step-04-action-prose', 'step-05-dialogue-integration', 'step-06-aftermath-polish', 'step-07-quality-check', 'step-08-wiki-update', 'step-09-final-report']
status: READY_FOR_AUDIT
last_update: {timestamp}
---
```

### 3. Generate Handover Report

Display the final status to the user:

```
"✅ PROSE ADAPTATION CYCLE COMPLETE!

**Output File:** {outputFile}
**Status:** READY FOR AUDIT
**Recursive Updates:** {Yes/No}

**System Ready For:**
1. `gooner-audit` (Quality Review)
2. `bible-sync` (Commit recursive facts)

**WORKFLOW ENDED**"
```

---

## WORKFLOW END

This concludes the Prose Adapter workflow.
