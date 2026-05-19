# Axel Co-work Panel (Qwen Edition)

Simple multi-agent review using Qwen CLI as primary agent.

## Usage

```bash
bash .qwen/skills/axel-cowork/run.sh --task <id> --mode <mode> --prompt "..." [--agents "role1 role2"]
```

## Options

- `--task <id>`: Session identifier
- `--mode`: `arch_review`, `content_audit`, `prompt_opt`, `gooner_audit`, `review_debate`
- `--prompt`: Instructions (required)
- `--agents`: Roles for Qwen (default: `dev/m-prompt-expert`)

## Qwen Role Mapping

| Role | Focus |
|---|---|
| `dev/m-prompt-expert` | Prompt engineering, anti-slop |
| `dev/f-r18-expert` | R18 prose / adaptation review |

## Example

```bash
bash .qwen/skills/axel-cowork/run.sh --task qwen-prompt --mode prompt_opt --prompt "Review prompt" --agents "dev/m-prompt-expert"
```

## Storage

Results: `_out/agent-sessions/<task-id>/`