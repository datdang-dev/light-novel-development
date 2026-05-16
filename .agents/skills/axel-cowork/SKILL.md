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
* `--mode`: `arch`, `code`, `review`, or `cross`.
* `--prompt`: Instructions for the agents.
* `--agents`: (Optional) Space-separated list of developers.
  * Defaults to: `hermes:se/m-architect claude:dev/m-prompt-expert`.

## 🎭 Developers (Agents)

All roles are stored in `studio/developers/config/roles/`.

| Role ID | Expertise | Focus |
|---|---|---|
| `se/m-architect` | Senior System Architect (Male) | Multi-agent structural design, token efficiency, bounds & invariants. |
| `dev/m-prompt-expert` | Prompt Engineer (Male) | Prompt mechanics, LLM steering, and strict instruction adherence. |
| `dev/f-r18-expert` | Adult Industry Dev (Female) | R18 narrative fidelity, fetish accuracy, making male users engaged. |
| `qa/m-qa-gooner` | QA / Gooner (Male) | SLOP detection, pacing, physiological quality metrics, brutal reviews. |

### Example Combinations

* **Prompt Architecture**: `--agents "hermes:se/m-architect claude:dev/m-prompt-expert"`
* **R18 Content Review**: `--agents "hermes:qa/m-qa-gooner claude:dev/f-r18-expert"`
* **Solo R18 Audit**: `--agents "claude:dev/f-r18-expert"`

## 📁 Storage

Results are stored in `_out/agent-sessions/<task-id>/`.

* `context.md`: Unified log of decisions.
* `*_last.md`: Latest output from each agent.
