# Axel Co-work Panel (DeepSeek Edition)

Simple multi-agent review using DeepSeek CLI as primary agent.

## Usage

```bash
bash .deepseek/skills/axel-cowork/run.sh --task <id> --mode <mode> --prompt "..." [--agents "role1 role2"]
```

## Options

- `--task <id>`: Session identifier
- `--mode`: `arch_review`, `content_audit`, `prompt_opt`, `gooner_audit`, `review_debate`
- `--prompt`: Instructions (required)
- `--agents`: Roles for DeepSeek (default: `dev/m-prompt-expert`)

## DeepSeek Role Mapping

| Role | Focus |
|---|---|
| `dev/m-prompt-expert` | Prompt engineering, anti-slop |
| `dev/f-r18-expert` | R18 prose / adaptation review |
| `qa/m-qa-gooner` | QA gatekeeping, SLOP detection |

## Example

```bash
bash .deepseek/skills/axel-cowork/run.sh --task ds-qa --mode gooner_audit --prompt "Audit scene" --agents "qa/m-qa-gooner"
```

## Storage

Results: `_out/agent-sessions/<task-id>/`