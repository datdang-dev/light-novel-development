#!/usr/bin/env bash
# Axel Co-work Panel - Qwen Edition

set -euo pipefail
SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SKILL_DIR/../../../.." && pwd)"
export PYTHONPATH="$REPO_ROOT:${PYTHONPATH:-}"
[ -d "$REPO_ROOT/.venv" ] && source "$REPO_ROOT/.venv/bin/activate" 2>/dev/null || true

TASK="qwen-$(date +%s)"
MODE="content_audit"
PROMPT=""
ROLES="dev/m-prompt-expert"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --task) TASK="$2"; shift 2 ;;
    --mode) MODE="$2"; shift 2 ;;
    --prompt) PROMPT="$2"; shift 2 ;;
    --agents) ROLES="$2"; shift 2 ;;
    *) echo "[!] Unknown: $1"; exit 1 ;;
  esac
done

[ -z "$PROMPT" ] && echo "[!] --prompt required" && exit 1
AGENT_STR=$(echo "$ROLES" | tr ' ' '\n' | while read role; do echo "qwen:$role"; done | tr '\n' ' ')
cd "$REPO_ROOT"
python3 -m studio.developers.orchestrator --task "$TASK" --mode "$MODE" --prompt "$PROMPT" --agents "$AGENT_STR"