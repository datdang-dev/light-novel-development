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
