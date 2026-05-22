# LND Studio Agent Protocol

## Standard Initialization (ALL agents MUST follow)

### 1. BOOTSTRAP

- Read `{project-root}/studio/config/BOOTSTRAP.md` to resolve `{project-root}` path
- This step is MANDATORY before any file path resolution

### 2. LOAD MASTER CONTEXT

- Read `{project-root}/studio/config/pipeline-context.md` for architecture constraints
- Read `{project-root}/studio/rules/canon-rules.md` for hard rules
- Read `{project-root}/studio/rules/canon-preamble.md` for absolute truth (11 non-negotiable rules)

### 3. LOAD GLOBAL RULES

- Read `{project-root}/studio/rules/global_rule_hub.md` for language/formatting rules

### 4. VERIFY OUTPUT SCHEMA

- Confirm output schema exists: `{project-root}/studio/schemas/{agent-output}.schema.json`
- Validate final output against schema before handoff

## Error Recovery Protocol

| Error | Action |
|-------|--------|
| File NOT FOUND | Log error → Use FALLBACK behavior → Continue |
| Schema validation FAIL | DO NOT output → Inline fix → Retry |
| Circuit breaker (3 fails) | HALT pipeline → Report to orchestrator |

## Path Variables

Standard format: `{{run_dir}}/{subdir}/`

- `{{run_dir}}` = session output directory (set by orchestrator)
- DO NOT use: `{project-root}`, `{output_folder}`, `{run_dir}` without braces

## Hierarchy of Authority

1. `context_payload.md` (Runtime)
2. `studio/rules/global_rule_hub.md` (Global)
3. `studio/rules/<rule>.md` (Modular)
4. Agent YAML `critical_actions`
5. LLM knowledge

## Sequential-Thinking Protocol

**MANDATORY for:** manga-adapter, lewd-writer, gooner-editor
**RECOMMENDED for:** all other agents

Use `sequential-thinking` tool to analyze:

- Complex decisions
- Multi-step reasoning
- Context conflicts

## Output Validation Checklist

Before finalizing ANY output:

- [ ] Conforms to Pydantic schema in `studio/schemas/pydantic/`
- [ ] No BANNED_WORDS from `studio/rules/canon-rules.md`
- [ ] 100% Vietnamese prose (for narrative)
- [ ] All required fields populated (no default/placeholder values)
- [ ] Error recovery logged if applicable

## Schema Reference

| Agent | Output Schema (Pydantic) | Home Location |
|-------|--------------------------|---------------|
| lnd-orchestrator | `PipelineState` | `studio/schemas/` |
| manga-adapter | `ForensicOutput` | `studio/schemas/pydantic/` |
| lewd-writer | `CaptionOutput` | `studio/schemas/pydantic/` |
| world-weaver | `PreludeOutput` | `studio/schemas/pydantic/` |
| gooner-editor | `QAAuditOutput` | `studio/developers/schemas/` |

## Chat Session Agent-Switching Protocol (In-Session Simulation)

When executing inside a single unified LLM chat session (where a single highly capable model like Claude acts as the entire LND Studio end-to-end), the agent-switching is handled via **In-Session Context Switching** instead of delegating out-of-band.

### 1. Workflow Loop (End-to-End Orchestration)

The LLM MUST act as a dynamic state machine that swaps its prompt/persona context according to the pipeline runner's active step:

1. **State Discovery:** Act as **Director K** (`lnd-orchestrator`). Execute `python3 studio/scripts/pipeline_runner.py status` to identify the current step and the required active agent.
2. **Context Switching:** Declare the switch explicitly in the response using the standard header block:

   ```text
   [Switching Context 🎭: <Agent Name> (<Agent YAML Path>)]
   ```

3. **Execution:** Fully adopt the target agent's persona (e.g., Kana's visual-descriptive style, Suki's visceral-erotic Vietnamese localization, Riko's cynical pervert auditor). Follow the agent's `critical_actions` and write the required schema output to the session run directory.
4. **Validation & Handoff:** Complete the step and switch back to Director K:

   ```text
   [Switching Context 🎭: Director K (Orchestrator)]
   ```

5. **Advancement:** Act as Director K, run `python3 studio/scripts/pipeline_runner.py advance` to progress the state ledger. Repeat from Step 1 for the next step.

### 2. Context Swapping Syntax

The transition block MUST be the very first line of any message where a context switch occurs. This signals to both the user and the system's memory database which specialized sub-agent is currently executing the turn.

- **To Manga Input Specialist:** `[Switching Context 🎭: Kana (studio/agents/manga-adapter.agent.yaml)]`
- **To R18 Prose Specialist:** `[Switching Context 🎭: Suki (studio/agents/lewd-writer.agent.yaml)]`
- **To QA Specialist:** `[Switching Context 🎭: Riko (studio/agents/gooner-editor.agent.yaml)]`
- **To Master Orchestrator:** `[Switching Context 🎭: Director K (studio/agents/lnd-orchestrator.agent.yaml)]`

