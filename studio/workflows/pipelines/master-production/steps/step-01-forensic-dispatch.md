# Phase 1: Forensic Analysis 🔬

**Goal:** Execute the Panel Forensic Workflow on the provided input (Image/Page).

**Agent:** Prof. Atomic (panel-forensic-analyst)

**Instructions to Director K:**
1.  **Identify Input:** Locate the image or page reference provided by the user.
2.  **Dispatch:** EXECUTE the `panel-forensic` workflow located at:
    `{project-root}/studio/workflows/capabilities/panel-forensic/workflow.md`
    (Using `exec` logic: Read the file, process it fully, then return here).
3.  **Monitor:** Ensure the sub-workflow completes and generates `forensic_report.md`.
4.  **Transition:** Upon successful completion of forensics, LOAD and EXECUTE the next step:
    `./steps/step-02-context-prep.md`

**Critical Rule:** Do NOT summarize the report yourself. Just verify its existence and move to production.
