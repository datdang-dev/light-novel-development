# Pipeline Context (LND Studio Master Reference)

**CRITICAL RULE: All Specialist Agents and Orchestrators MUST adhere to the following definitions.**

## 1. Architecture & Execution

- **Architecture Diagram:** `{project-root}/studio/docs/architecture/dynamic_design/service_manga_adapter/sq_v6_1_gooner_alchemist_pipeline.puml`
- **Global Variables:** Load `{project-root}/studio/config/config.yaml` for session secrets and settings (`{user_name}`, `{communication_language}`, `{output_folder}`).
- **Delegation Protocol:** Read `{project-root}/studio/docs/protocols/delegation-protocol.md` when handing off tasks.

## 2. Dynamic State Passing

- **Artifact Handoff:** Agents MUST NOT hardcode `output/{chapter}/{page}` paths in their prompt instructions. The pipeline runner (`workflow.md`) determines the output location dynamically via execution variables (e.g., `{{run_dir}}`). All output artifacts must be saved to the run directory established by the orchestrator.

## 3. Mandatory Formatting & Canon Rules

- **Canon Rules (CRITICAL):** You MUST read `{project-root}/studio/config/canon-rules.md`. These represent the highest-priority rules regarding language output, hallucination boundaries, and banned words.
- **Prose Rules:** Read `{project-root}/.agent/rules/prose_structure.md` for standard metadata blocks and formatting.
- **Lewd Mechanics:** Read `{project-root}/.agent/rules/lewd_writing_mechanics.md` when writing prose.
- **Sensory Bounds:** Read `{project-root}/.agent/rules/sensory_density.md` for density constraints.

*(Note: These files provide contextual framing. Rely on them as guidelines and use specific `knowledge_payload.md` drops from the Orchestrator for scene-specific parameters. Canon Rules always override local instructions.)*
