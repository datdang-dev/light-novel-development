# Phase 2: Context Preparation (Bible Sync) 📚

**Goal:** Ensure all characters in the scene have active profiles and the world state is updated.

**Agents:** Director K (internal) + Aria (character-architect)

**Instructions to Director K:**
1.  **Extract Data:** EXECUTE the `entity-extractor` workflow:
    `{project-root}/studio/workflows/capabilities/entity-extractor/workflow.md`
    (Input: `forensic_report.md` | Output: `entities.yaml`)

2.  **Sync Profiles:** EXECUTE the `character-bible` workflow:
    `{project-root}/studio/workflows/capabilities/character-bible/workflow.md`
    (Input: `entities.yaml`)

3.  **Verify Context:** Ensure `active_character_context.md` (or equivalent profile dump) is ready for Miki.

4.  **Transition:** LOAD and EXECUTE the next step:
    `./steps/step-03-dialogue-dispatch.md`
