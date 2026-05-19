#!/usr/bin/env bash
# axel-panel.sh - Simplified CLI wrapper for Axel multi-agent co-work panel
# Usage: ./axel-panel.sh --prompt "..." --agents "agent1:role1 agent2:role2" [--mode mode_name]

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SKILL_DIR/../../.." && pwd)"

# Auto-activate venv if exists
if [ -d "$REPO_ROOT/.venv" ]; then
    source "$REPO_ROOT/.venv/bin/activate" 2>/dev/null || true
fi

# Defaults
TASK="axel-$(date +%s)"
MODE="content_audit"
PROMPT=""
AGENTS="hermes:se/m-architect claude:dev/m-prompt-expert"

usage() {
    cat <<EOF
Axel Multi-Agent Co-work Panel

Usage: $0 --prompt "..." [OPTIONS]

Options:
  --prompt TEXT      Task prompt (required)
  --agents TEXT    Space-separated agent:role pairs (default: ${AGENTS})
  --mode MODE      Review mode: arch_review|content_audit|prompt_opt|gooner_audit|review_debate
  --task ID        Session ID (default: axel-<timestamp>)

Modes:
  arch_review      Architecture/framework review (1 agent)
  content_audit    Production output review/SLOP detection (1 agent)
  prompt_opt       Prompt optimization (1 agent)
  gooner_audit     GOONER_AUDIT_FRAMEWORK gatekeeper (1 agent)
  review_debate    Multi-agent debate + synthesis (2+ agents)

Agent:Role examples:
  hermes:se/m-architect    (System architect)
  claude:dev/f-r18-expert (R18 prose expert)
  qwen:dev/m-prompt-expert (Prompt engineer)
  deepseek:qa/m-qa-gooner (QA gatekeeper)
  codex:qa/m-qa-gooner   (QA gatekeeper)
  openclaw:se/m-architect (System integrator)

Example:
  $0 --mode gooner_audit --prompt "Audit this scene for SLOP" --agents "claude:qa/m-qa-gooner deepseek:qa/m-qa-gooner codex:qa/m-qa-gooner"
EOF
    exit 1
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --prompt) PROMPT="$2"; shift 2 ;;
        --agents) AGENTS="$2"; shift 2 ;;
        --mode) MODE="$2"; shift 2 ;;
        --task) TASK="$2"; shift 2 ;;
        -h|--help) usage ;;
        *) echo "[!] Unknown: $1"; usage ;;
    esac
done

if [ -z "$PROMPT" ]; then
    echo "[!] --prompt is required"
    usage
fi

# Run orchestrator
export PYTHONPATH="$REPO_ROOT:${PYTHONPATH:-}"
cd "$REPO_ROOT"
python3 - "$TASK" "$MODE" "$PROMPT" "$AGENTS" <<'PYEOF'
import asyncio
import sys

async def main():
    task, mode, prompt, agents = sys.argv[1:5]
    from studio.developers.orchestrator import run_panel
    agent_configs = []
    for pair in agents.split():
        if ":" in pair:
            aid, role = pair.split(":", 1)
        else:
            aid, role = pair, "m-architect"
        agent_configs.append({"id": aid, "role": role})
    await run_panel(task, mode, prompt, agent_configs, files=[])

asyncio.run(main())
PYEOF