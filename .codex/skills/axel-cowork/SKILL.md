# Axel Co-work Panel (Codex Edition)

Simple multi-agent review using Codex CLI as primary agent.

## Usage

```bash
bash .codex/skills/axel-cowork/run.sh --task <id> --mode <mode> --prompt "..." [--agents "role1 role2"]
```

## Options

- `--task <id>`: Session identifier
- `--mode`: `arch_review`, `content_audit`, `prompt_opt`, `gooner_audit`, `review_debate`
- `--prompt`: Instructions (required)
- `--agents`: Roles for Codex (default: `qa/m-qa-gooner`)

## Codex Role Mapping

| Role | Focus |
|---|---|
| `qa/m-qa-gooner` | QA gatekeeping, SLOP detection |

## Example

```bash
bash .codex/skills/axel-cowork/run.sh --task cx-qa --mode gooner_audit --prompt "Audit scene" --agents "qa/m-qa-gooner"
```

## Storage

Results: `_out/agent-sessions/<task-id>/`