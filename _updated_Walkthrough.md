# _updated_Walkthrough.md

## 1. System Overview

**Objective:**
This system functions as a controlled, agent-driven "Studio" specifically designed for the development, analysis, and structuring of R18 fiction and manga adaptations. It acts as a multi-agent orchestration pipeline that translates visual data (manga panels/images) and logs into formalized, highly specific prose.

**Core Design Philosophy:**

- **Agent-Driven Specialization:** Modeled after a real-world studio. An "Orchestrator" (Director K) routes work, while "Specialists" (e.g., Kana for forensics, Suki for prose, Riko for QA) handle distinct pipeline phases.
- **Workflow Orchestration & Pipeline Constraints:** The system relies on rigid, sequential pipelines (such as the "V6.1 Gooner Alchemist Pipeline") mapped inside Markdown files (e.g., `workflow.md`). It employs strict quality gates, automated rewriting loops, and distinct phases (Discovery -> Forensics -> Prose -> Audit -> Bible Update).
- **Prompt Chaining & Explicit Handoff:** Agents exist not as arbitrary LLM wrappers but as compartmentalized prompt profiles defined in YAML. Control flow between them relies on structured Markdown banners (`🔄 DELEGATING TO...`) and JSON schema contracts (`forensic-state.schema.json`, `draft-prose.json`).

---

## 2. Agent Architecture

**Structure:**
Agents are defined in `.agent.yaml` files located in `studio/agents/` (not `.agent/`, which houses workflows and rules). The YAML schema typically includes:

- `metadata`: Basic identification (name, role, icon).
- `persona`: Detailed identity framing (role, communication style, distinct principles).
- `critical_actions`: Heavily declarative constraint injections guiding behavior (e.g., "NO KANJI in prose output").
- `menu`: Triggers (often fuzzy-matched abbreviations like `[GA]`) that map the agent to internal workflows (`.md` files).

**Prompt Construction Patterns:**

1. **Aggressive Role Framing:** Agents are heavily anthropomorphized with deep psychological constraints (e.g., Suki acts as a "disciplined prose craftsman" who despises "mechanical translation").
2. **Path Dependency Injections:** Agents are instructed to strictly load hardcoded paths (e.g., `"Load and read {project-root}/studio/config/config.yaml"` or `"READ ARCHITECTURE: .../sq_v6_1_gooner_alchemist_pipeline.puml"`).
3. **Implicit Contracts & State:** State is persisted entirely via the file system rather than an overarching memory bus. Agents output explicit schema-validated JSON files (`forensic-state.json`) into structured directories (`output/{chapter}/{page}/`). Subsequent agents read these files to continue the chain.

---

## 3. Workflow & Execution Model

**Triggers and Routing:**
The "Master Orchestrator" (`lnd-orchestrator.agent.yaml`) reads user intention utilizing the `sequential-thinking` tool, creates a "Delegation Mandate", and triggers corresponding Specialist workflows.

**Control Flow (Example: `gooner-alchemist` pipeline):**

1. **Phase 0:** Initialization & Context Sync (loads Character Bibles, checks consistency).
2. **Phase 1 (Manga Adapter - Kana):** Generates a `context_horizon.md` to prevent hallucinatory continuity errors, followed by `panel-forensic` executing OCR and environmental scans. Output is `forensic-state.json`.
3. **Phase 2 (Lewd Writer - Suki):** The Transformation Engine runs. Translates forensic data into narrative prose. Output is `draft.json`.
4. **Phase 3 (Gooner Editor - Riko):** Arousal Audit. Checks quantitative metrics (e.g., Smell ≥3, Texture ≥5).
5. **Phase 4:** Bible Update.

**Execution Nature:**
The execution model is heavily **Sequential** but handles **Conditional Recursion**. If Phase 3 (Audit) fails the quantitative threshold (Score < 85/100), the loop conditionally reverses to Phase 2 for a rewrite.

---

## 4. Prompting Strategy

**Major Techniques Extracted:**

- **Constraint Injection & Banning:** Strict negative prompts prohibiting specific behaviors (e.g., "Do NOT perform QA directly", "NO euphemisms").
- **Self-Critique & Scepticism Protocols:** Agents are instructed not to trust raw data blindly. (e.g., Kana's "Context > Raw Data" or Suki's "SKEPTIC PROTOCOL").
- **Decomposition:** `sequential-thinking` is heavily recommended within the prompt boundaries to mandate step-by-step logic before generation.
- **Rule Book Injection:** Shared contextual files from `.agent/rules/` (e.g., `lewd_writing_mechanics.md`, `prose_structure.md`) are injected en masse to enforce output formatting.

**Ambiguities & Inconsistencies:**

- **Prompt Duplication:** Every agent has the exact same string to load `config.yaml` or understand the V6.1 Architecture.
- **Cognitive Overload:** Injecting massive formatting rules files (like `lewd_writing_mechanics.md` - 6KB+) into every generation cycle creates context bloat and can degrade the LLM's adherence to nuanced instructions.

---

## 5. Known Structural Weak Points

- **Hardcoded Path Fragility:** Agents embed strict `{project-root}/studio/...` absolute paths for architecture documents, workflows, and state files. Any directory refactoring will break the prompts instantly.
- **Delegation Parsing Risk:** The orchestration layer uses Regex/Fuzzy Matching on UI `menu` triggers (e.g., `trigger: GA or fuzzy match`) which is extremely fragile if conversational bleed occurs or if the UI parsing engine updates.
- **Disk-Bound State Passing:** Artifact generation (`output/{ch}/{pg}/...`) is the *only* way state passes between agents. If a pipeline errors and the file isn't created, the next agent in the sequence will hallucinate data or crash, lacking a centralized fallback memory broker.
- **Redundant Rule Injecting:** Because the Orchestrator isn't passing refined context, Specialist agents are forced to manually look up formatting rules (`prose_structure.md`) every time they spin up.

---

## 6. Refactoring Readiness Assessment

**Key Architectural Improvements Needed:**

1. **Abstract Dynamic Dependencies (Context Bus Layer):**
   Remove hardcoded `{project-root}/...` file paths from the agent YAML definition strings. Instead, utilize a context payload builder that injects rules and configs at runtime via a centralized state abstraction.

2. **Standardize Artifact Routing:**
   Instead of forcing the prompt to manually output to `{output_folder}/{chapter}/{page}/`, the pipeline execution engine should manage the file I/O layer. Agents should return standard outputs to the execution runner, which then persists the artifacts to disk.

3. **Decouple Tool Instruction from Persona:**
   YAML definitions mix identity framing ("Suki is disciplined") with runtime operational instructions ("use sequential-thinking tool"). Separate behavioral identity constraints from pipeline execution constraints to clarify agent boundaries.

4. **Enhance the Auditing Feedback Loop:**
   The fallback loop (Phase 3 -> Phase 2) relies implicitly on the language model understanding why it failed an audit. Introduce an explicit Error-Contract that parses the failed JSON gate and feeds exact failed tokens/rules back into the Phase 2 prompt.
