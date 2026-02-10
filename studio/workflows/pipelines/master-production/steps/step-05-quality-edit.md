# Phase 5: Quality Audit & Critique 🧐

**Goal:** Submit the prose for GOONER QUALITY AUDIT.

**Agent:** Riko (gooner-editor)

**Instructions to Director K:**
1.  **Identify Input:** The scene prose (`prose_scene.md` or `prose_output.md`).
2.  **Dispatch:** EXECUTE the `gooner-audit` workflow located at:
    `{project-root}/studio/workflows/capabilities/gooner-audit/workflow.md`
    (Using `exec` logic: Read the file, process it fully, then return here).
3.  **Monitor:** Ensure the report is generated: `audit_report.md`.
4.  **Validate:**
    - IF Status = PASS -> Compile final output (`master-production-complete.md`) and notify user of SUCCESS.
    - IF Status = FAIL -> Halt and Flag for Re-write.
5.  **Conclusion:** Report "Pipeline Complete" to the User.
