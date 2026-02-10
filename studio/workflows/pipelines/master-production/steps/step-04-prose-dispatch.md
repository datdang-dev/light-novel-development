# Phase 4: Prose Adaptation ✍️

**Goal:** Transform Forensic Data + Dialogue Script into "Gooner-Grade" Prose.

**Agent:** Suki (lewd-writer)

**Instructions to Director K:**
1.  **Identify Input:** Verify existence of `forensic_report.md` AND `dialogue_script.md`.
2.  **Pass Context:** The forensic report is the SKELETON. The dialogue script provides VOICE.
3.  **Dispatch:** EXECUTE the `prose-adapter` workflow located at:
    `{project-root}/studio/workflows/capabilities/prose-adapter/workflow.md`
    (Using `exec` logic: Pass both files as `data` context).
4.  **Monitor:** Ensure the sub-workflow completes and generates `prose_scene.md` (or `prose_output.md`).
5.  **Transition:** Upon successful completion of prose, LOAD and EXECUTE the next step:
    `./steps/step-05-quality-edit.md`

**Critical Rule:** Do NOT rewrite the prose yourself. Delegate strictly to Suki's workflow.
