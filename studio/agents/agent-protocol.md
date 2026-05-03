# LND Studio Agent Protocol

## Standard Initialization (ALL agents MUST follow)

### 1. BOOTSTRAP
- Read `{project-root}/studio/config/BOOTSTRAP.md` to resolve `{project-root}` path
- This step is MANDATORY before any file path resolution

### 2. LOAD MASTER CONTEXT
- Read `{project-root}/studio/config/pipeline-context.md` for architecture constraints
- Read `{project-root}/studio/config/canon-rules.md` for hard rules

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
- [ ] Conforms to `schemas/{agent-output}.schema.json`
- [ ] No BANNED_WORDS from `canon-rules.md`
- [ ] 100% Vietnamese prose (for narrative)
- [ ] All required fields populated
- [ ] Error recovery logged if applicable

## Schema Reference

| Agent | Output Schema |
|-------|--------------|
| lnd-orchestrator | `pipeline-state.schema.json` |
| manga-adapter | `forensic-state.schema.json` |
| lewd-writer | `draft-prose.schema.json` |
| gooner-editor | `audit-report.schema.json` |
| character-architect | `character-bible.schema.json` |
| dialogue-crafter | (JSON output, validate structure) |