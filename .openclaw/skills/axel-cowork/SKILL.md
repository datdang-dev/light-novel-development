# Axel Co-work Panel (OpenClaw Edition)

Simple multi-agent review using OpenClaw CLI as primary agent.

## Usage

```bash
bash .openclaw/skills/axel-cowork/run.sh --task <id> --mode <mode> --prompt "..." [--agents "role1 role2"]
```

## Options

- `--task <id>`: Session identifier
- `--mode`: `arch_review`, `content_audit`, `prompt_opt`, `gooner_audit`, `review_debate`
- `--prompt`: Instructions (required)
- `--agents`: Roles for OpenClaw (default: `se/m-architect`)

## OpenClaw Role Mapping

| Role | Focus |
|---|---|
| `se/m-architect` | System architecture, agentic framework design |

## Example

```bash
bash .openclaw/skills/axel-cowork/run.sh --task oc-arch --mode arch_review --prompt "Review architecture" --agents "se/m-architect"
```

## Storage

Results: `_out/agent-sessions/<task-id>/`