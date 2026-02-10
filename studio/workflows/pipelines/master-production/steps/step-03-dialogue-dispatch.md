# Phase 3: Dialogue Generation 💬

**Goal:** Generate "Gooner-Grade" Dialogue Lines & SFX pattern matching character voices.

**Agent:** Miki (dialogue-crafter)

**Instructions to Director K:**
1.  **Identify Input:** `forensic_report.md` (Action) + `active_character_context` (Voice).
2.  **Dispatch:** EXECUTE the `dialogue-generator` workflow:
    `{project-root}/studio/workflows/capabilities/dialogue-generator/workflow.md`
    (Using `exec` logic).
3.  **Monitor:** Ensure Miki generates `dialogue_script.md` (or equivalent dialogue list).
4.  **Transition:** Upon successful completion, LOAD and EXECUTE the next step:
    `./steps/step-04-prose-dispatch.md`

**Critical Rule:** Do NOT accept sanitized dialogue. Miki must follow the Escalation Loop.
