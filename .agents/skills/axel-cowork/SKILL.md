# Multi-Agent Co-work Panel (Axel)

Modular architecture for collaborative AI-agent reviews, integrated into the Studio pipeline.

## 🚀 Overview

This skill leverages a registry of "Developers" within the `studio/developers` module. It supports flexible multi-agent combinations (e.g., Hermes + Claude, or Claude solo) and persistent task-based sessions.

## 🛠 Usage

```bash
bash .agents/skills/axel-cowork/run.sh --task <id> --mode <mode> --prompt "..." [--agents "agent1:role agent2:role"]
```

### Options

* `--task <id>`: Session identifier.
* `--mode`: one of the modes declared in `studio/developers/config/mode_registry.yaml`:
  * `arch_review` — architecture/framework review
  * `content_audit` — production output / SLOP / quality review
  * `prompt_opt` — prompt template and steering optimization
  * `gooner_audit` — GOONER_AUDIT_FRAMEWORK gatekeeper audit
  * `review_debate` — multi-agent debate + synthesis
  * Do **not** use stale legacy modes (`arch`, `code`, `review`, `cross`) unless re-added to mode_registry.yaml.
* `--prompt`: Instructions for the agents.
* `--agents`: (Optional) Space-separated list of developers.
  * Defaults to: `hermes:se/m-architect claude:dev/m-prompt-expert`.

## 🎭 Developers (Agents)

All roles are stored in `studio/developers/config/roles/`.

### Role Categories

| Category | Role IDs | Agent CLI | Focus |
|---|---|---|---|
| `dev` | `dev/m-prompt-expert`, `dev/f-r18-expert` | claude, qwen, deepseek | R18 expert developers, prompt engineering, review + rewrite |
| `qa` | `qa/m-qa-gooner` | claude, deepseek, codex | R18 QA / Gooner — SLOP detection, gatekeeping, scoring |
| `se` | `se/m-architect` | hermes, openclaw | System Engineers / Architect — agentic framework design, integration |

### Example Combinations

* **Prompt Architecture**: `--agents "hermes:se/m-architect claude:dev/m-prompt-expert"`
* **R18 Content Review**: `--agents "claude:dev/f-r18-expert qwen:dev/m-prompt-expert"`
* **QA Gate (multi-agent)**: `--agents "claude:qa/m-qa-gooner deepseek:qa/m-qa-gooner codex:qa/m-qa-gooner"`
* **System Design Review**: `--agents "hermes:se/m-architect openclaw:se/m-architect"`
* **Full Pipeline**: `--agents "hermes:se/m-architect claude:dev/f-r18-expert codex:qa/m-qa-gooner"`

## 🧩 Hiring new CLI agents

This skill supports lightweight "hiring" of external CLI-backed agents. Pattern:

1) Drop a developer descriptor YAML into `studio/developers/config/agents/` named `<agent>.yaml`.

   Example: `studio/developers/config/agents/claude.yaml`

   ```yaml
   id: claude
   name: claude
   type: cli
   cli: claude
   entrypoint: "--acp --stdio"
   roles:
     - dev/f-r18-expert
     - dev/m-prompt-expert
     - qa/m-qa-gooner
   capabilities:
     - llm
     - prompt-review
     - r18-development
     - slop-detection
     - rewrite-targets
   meta:
     vendor: claude
     category: dev
     version: "auto-detect"
   ```

2) Ensure the CLI is executable and reachable (chmod +x, or put in PATH). If the agent ships as a Python package, install into the repo venv: `pip install /path/to/package`.

3) Restart the panel/orchestrator (rerun `.agents/skills/axel-cowork/run.sh`) — the orchestrator scans `studio/developers/config/agents/` at startup and loads new descriptors.

4) Invoke a session specifying the hired agent by name and role. Format: `--agents "<cli_name>:<role_id> ..."`

   Example: `bash .agents/skills/axel-cowork/run.sh --task try-claude --mode gooner_audit --prompt "Audit this scene" --agents "claude:qa/m-qa-gooner deepseek:qa/m-qa-gooner codex:qa/m-qa-gooner"`

5) Output and logs appear under `_out/agent-sessions/<task-id>/` (context.md, per-agent *_last.md).

Notes / Pitfalls

- The YAML keys above are the canonical minimal surface; the orchestrator tolerates extra fields but requires `id`, `name`, and `cli` for CLI-based agents.
- If a CLI uses stdin/stdout JSON framing, set `entrypoint` and document its framing in `meta`.
- For quick testing, you can point `cli` to a wrapper script that translates the studio JSON protocol to the third-party CLI.
- Role IDs follow the pattern `<category>/<gender>/<name>` (e.g., `dev/m-prompt-expert`, `qa/m-qa-gooner`, `se/m-architect`).
- Multiple roles can be assigned to one agent (e.g., `dev/m-prompt-expert` + `qa/m-qa-gooner`).

## 📁 Storage

Results are stored in `_out/agent-sessions/<task-id>/`.

* `context.md`: Unified log of decisions.
* `*_last.md`: Latest output from each agent.