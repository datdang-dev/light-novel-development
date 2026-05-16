#!/usr/bin/env bash
# axel-cowork/run.sh — Entry point for the Multi-Agent Review Panel.
#
# This script routes to the core Studio logic.
#
# Usage:
#   bash run.sh --task <name> --mode review --prompt "..." --agents "hermes:role claude:role"

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SKILL_DIR/../../.." && pwd)"

# Add REPO_ROOT to PYTHONPATH so studio.developers can be imported
export PYTHONPATH="$REPO_ROOT:${PYTHONPATH:-}"

# Defaults
TASK="default"
MODE="review"
PROMPT=""
AGENTS="hermes:se/m-architect claude:dev/m-prompt-expert"
FILES=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --task)    TASK="$2";       shift 2 ;;
        --mode)    MODE="$2";       shift 2 ;;
        --prompt)  PROMPT="$2";     shift 2 ;;
        --agents)  AGENTS="$2";     shift 2 ;;
        --files)   FILES="$2";      shift 2 ;;
        *) echo "[!] Unknown arg: $1"; exit 1 ;;
    esac
done

python3 -m studio.developers.orchestrator --task "$TASK" --mode "$MODE" --prompt "$PROMPT" --agents "$AGENTS" --files "$FILES"

