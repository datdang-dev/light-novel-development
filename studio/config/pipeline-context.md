# Pipeline Context (LND Studio Master Reference)

**CRITICAL RULE: All Specialist Agents and Orchestrators MUST adhere to the following definitions.**

## 1. Architecture & Execution

- **Architecture Diagram:** `{{project_root}}/studio/docs/architecture/dynamic_design/service_gooner_alchemist/sq_v1_0_0_ga_pipeline.puml`
- **Global Variables:** Load `{{project_root}}/studio/config/config.yaml` for session secrets and settings (`{user_name}`, `{communication_language}`, `{output_folder}`).
- **Delegation Protocol (Single-Session):** Read `{{project_root}}/studio/docs/protocols/delegation-protocol.md`. Use pipeline manifests from `{{project_root}}/studio/pipelines/` — ONE manifest read replaces all individual SKILL.md reads.
- **One-Shot Protocol:** For lightweight pipelines (EC, PA), read `{{project_root}}/studio/protocols/one-shot-response.md`.

## 2. Dynamic State Passing

- **Artifact Handoff:** Agents MUST NOT hardcode `output/{chapter}/{page}` paths in their prompt instructions. The pipeline runner (`workflow.md`) determines the output location dynamically via execution variables (e.g., `{{run_dir}}`). All output artifacts must be saved to the run directory established by the orchestrator.
- **Single-Session Handoff:** In ONE_SHOT mode, intermediate artifacts (forensic.md, prelude.md) are NOT written to disk. Data is passed inline through `<think>` context using the PASS/DROP declarations in each SKILL.md.

## 3. Mandatory Formatting & Canon Rules

- **Canon Rules (CRITICAL):** You MUST read `{{project_root}}/studio/config/canon-rules.md`. These represent the highest-priority rules regarding language output, hallucination boundaries, and banned words.
- **Gooner Principles (CRITICAL):** You MUST internalize `{{project_root}}/studio/rules/gooner_principles.md`. This is the foundational philosophy (Layer 0) that ALL other rules derive from. The 7 Principles are non-negotiable.
- **Prose Rules:** Read `{{project_root}}/studio/rules/prose_structure.md` for standard metadata blocks and formatting.
- **Lewd Mechanics:** Read `{{project_root}}/studio/rules/lewd_writing_mechanics.md` when writing prose.
- **Sensory Bounds:** Read `{{project_root}}/studio/rules/sensory_density.md` for density constraints.

*(Note: These files provide contextual framing. Rely on them as guidelines and use specific `knowledge_payload.md` drops from the Orchestrator for scene-specific parameters. Canon Rules always override local instructions.)*
