#!/usr/bin/env python3
"""
LND Studio Pipeline Runner (State Machine)
============================================
Lightweight state machine for pipeline orchestration.
Enforces step ordering, validates gates, implements circuit breaker.

This is Layer 2 of the 4-Layer Rule Enforcement Architecture.

Usage:
    python pipeline_runner.py init <pipeline> <run_dir> [--pages 1-20]
    python pipeline_runner.py status [<state_file>]
    python pipeline_runner.py advance [<state_file>]
    python pipeline_runner.py gate <step_id> [<state_file>]
    python pipeline_runner.py context [<state_file>]
    python pipeline_runner.py fail-audit [<state_file>]
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

# ─── Resolve paths ───────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
STUDIO_ROOT = SCRIPT_DIR.parent
PROJECT_ROOT = STUDIO_ROOT.parent
DEFAULT_STATE_FILE = PROJECT_ROOT / ".agent" / "state" / "current.yaml"
SCHEMAS_DIR = STUDIO_ROOT / "schemas"


# ═══════════════════════════════════════════════════════════════════
# PIPELINE DEFINITIONS
# ═══════════════════════════════════════════════════════════════════

PIPELINES: dict[str, dict] = {
    "gooner-alchemist": {
        "description": "Manga-to-Novel Full Pipeline",
        "steps": [
            {
                "id": "initialize",
                "name": "Step 1: Initialize",
                "agent": "lnd-orchestrator",
                "step_file": "services/gooner-alchemist/steps/step-01-initialize.md",
                "rule_step": None,  # No JIT rules needed
                "output_schema": "pipeline-state.schema.json",
                "gate": None,
            },
            {
                "id": "forensic-analysis",
                "name": "Step 2: Forensic Analysis",
                "agent": "manga-adapter",
                "step_file": "services/gooner-alchemist/steps/step-02-forensic-analysis.md",
                "rule_step": "forensic-analysis",
                "output_schema": "forensic-state.schema.json",
                "gate": None,  # First real step, no gate
            },
            {
                "id": "context-loading",
                "name": "Step 3: Context Loading",
                "agent": "lnd-orchestrator",
                "step_file": "services/gooner-alchemist/steps/step-03-context-loading.md",
                "rule_step": "context-loading",
                "output_schema": None,
                "gate": "forensic_complete",  # Requires forensic output
            },
            {
                "id": "prose-generation",
                "name": "Step 4: Prose Generation",
                "agent": "lewd-writer",
                "step_file": "services/gooner-alchemist/steps/step-04-prose-generation.md",
                "rule_step": "prose-generation",
                "output_schema": "draft-prose.schema.json",
                "gate": "context_loaded",
            },
            {
                "id": "quality-audit",
                "name": "Step 5: Quality Audit",
                "agent": "gooner-editor",
                "step_file": "services/gooner-alchemist/steps/step-05-quality-audit.md",
                "rule_step": "quality-audit",
                "output_schema": "audit-report.schema.json",
                "gate": "prose_complete",
            },
            {
                "id": "state-persistence",
                "name": "Step 6: State Persistence",
                "agent": "lnd-orchestrator",
                "step_file": "services/gooner-alchemist/steps/step-06-state-persistence.md",
                "rule_step": None,
                "output_schema": None,
                "gate": "audit_pass",
            },
            {
                "id": "complete",
                "name": "Step 7: Completion",
                "agent": "lnd-orchestrator",
                "step_file": "services/gooner-alchemist/steps/step-07-complete.md",
                "rule_step": None,
                "output_schema": None,
                "gate": None,
            },
        ],
        "circuit_breaker_limit": 3,
    },
}


# ═══════════════════════════════════════════════════════════════════
# STATE MANAGEMENT
# ═══════════════════════════════════════════════════════════════════

def create_state(pipeline_name: str, run_dir: str, pages: list[int] | None = None) -> dict:
    """Create initial pipeline state."""
    now = datetime.now(timezone.utc).isoformat()
    return {
        "pipeline_name": pipeline_name,
        "current_step": 0,
        "steps_completed": [],
        "status": "initialized",
        "audit_attempts": 0,
        "failed_gate": None,
        "last_error": None,
        "run_dir": run_dir,
        "agent_outputs": {},
        "pages": pages or [],
        "current_page_index": 0,
        "created_at": now,
        "updated_at": now,
    }


def load_state(state_file: Path) -> dict | None:
    """Load state from YAML file."""
    if not state_file.exists():
        return None
    with open(state_file, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_state(state: dict, state_file: Path):
    """Save state to YAML file."""
    state["updated_at"] = datetime.now(timezone.utc).isoformat()
    state_file.parent.mkdir(parents=True, exist_ok=True)
    with open(state_file, "w", encoding="utf-8") as f:
        yaml.dump(state, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


# ═══════════════════════════════════════════════════════════════════
# GATE ENFORCEMENT
# ═══════════════════════════════════════════════════════════════════

def check_gate(state: dict, gate_name: str | None) -> tuple[bool, str]:
    """Check if a pipeline gate is satisfied."""
    if gate_name is None:
        return True, "No gate required"

    run_dir = Path(state["run_dir"])

    if gate_name == "forensic_complete":
        # Check that forensic output exists for current page
        forensics_dir = run_dir / "_forensics"
        if not forensics_dir.exists():
            return False, f"Forensics directory not found: {forensics_dir}"
        pages = state.get("pages", [])
        if pages:
            page_idx = state.get("current_page_index", 0)
            if page_idx < len(pages):
                page_num = pages[page_idx]
                expected = forensics_dir / f"{page_num:03d}_forensics.md"
                if not expected.exists():
                    return False, f"Missing forensic report: {expected.name}. Run forensic analysis first."
        return True, "Forensic gate passed"

    elif gate_name == "context_loaded":
        # Context loading is a soft gate - just check step completed
        if "context-loading" in state.get("steps_completed", []):
            return True, "Context loaded"
        return False, "Context loading step not completed"

    elif gate_name == "prose_complete":
        if "prose-generation" in state.get("steps_completed", []):
            return True, "Prose generated"
        return False, "Prose generation step not completed"

    elif gate_name == "audit_pass":
        if "quality-audit" in state.get("steps_completed", []):
            return True, "Audit passed"
        return False, "Quality audit not completed or not passed"

    return True, f"Unknown gate '{gate_name}' — allowing (permissive)"


# ═══════════════════════════════════════════════════════════════════
# PIPELINE OPERATIONS
# ═══════════════════════════════════════════════════════════════════

def get_pipeline(name: str) -> dict:
    """Get pipeline definition."""
    if name not in PIPELINES:
        available = ", ".join(PIPELINES.keys())
        print(f"❌ Unknown pipeline: '{name}'. Available: {available}", file=sys.stderr)
        sys.exit(1)
    return PIPELINES[name]


def get_current_step(state: dict) -> dict | None:
    """Get current step definition."""
    pipeline = get_pipeline(state["pipeline_name"])
    idx = state["current_step"]
    steps = pipeline["steps"]
    if idx >= len(steps):
        return None
    return steps[idx]


def build_context(state: dict) -> str:
    """Build context string for current pipeline state (Layer 2 bootstrap)."""
    step = get_current_step(state)
    pipeline = get_pipeline(state["pipeline_name"])

    pages = state.get("pages", [])
    page_idx = state.get("current_page_index", 0)
    current_page = pages[page_idx] if page_idx < len(pages) else None

    lines = [
        "# 📋 Pipeline State (Auto-Generated by pipeline_runner.py)",
        "",
        f"- **Pipeline**: {state['pipeline_name']}",
        f"- **Status**: {state['status']}",
        f"- **Current Step**: {step['name'] if step else 'COMPLETE'}",
        f"- **Step Index**: {state['current_step']}/{len(pipeline['steps']) - 1}",
        f"- **Active Agent**: {step['agent'] if step else 'none'}",
        f"- **Audit Attempts**: {state['audit_attempts']}/{pipeline.get('circuit_breaker_limit', 3)}",
        f"- **Run Dir**: `{state['run_dir']}`",
        "",
    ]

    if current_page is not None:
        lines.append(f"- **Current Page**: {current_page:03d}")
        lines.append(f"- **Page Progress**: {page_idx + 1}/{len(pages)}")
        lines.append("")

    if state.get("steps_completed"):
        lines.append("## Completed Steps")
        for s in state["steps_completed"]:
            lines.append(f"- ✅ {s}")
        lines.append("")

    if state.get("agent_outputs"):
        lines.append("## Agent Outputs")
        for agent, path in state["agent_outputs"].items():
            lines.append(f"- `{agent}` → `{path}`")
        lines.append("")

    if state.get("last_error"):
        lines.append(f"## ⚠️ Last Error")
        lines.append(f"```\n{state['last_error']}\n```")
        lines.append("")

    if step and step.get("step_file"):
        lines.append(f"## Next Action")
        lines.append(f"Execute: `{step['step_file']}`")
        if step.get("rule_step"):
            lines.append(f"JIT Rules: `python rule_injector.py {step['rule_step']}`")
        lines.append("")

    return "\n".join(lines)


def advance_step(state: dict, state_file: Path) -> dict:
    """Advance to next pipeline step."""
    step = get_current_step(state)
    if step is None:
        state["status"] = "completed"
        save_state(state, state_file)
        print("🎉 Pipeline already completed!")
        return state

    # Mark current step as completed
    if step["id"] not in state["steps_completed"]:
        state["steps_completed"].append(step["id"])

    # Advance
    state["current_step"] += 1
    state["status"] = "running"

    # Reset audit attempts on non-audit steps
    if step["id"] != "quality-audit":
        state["audit_attempts"] = 0

    next_step = get_current_step(state)
    if next_step is None:
        state["status"] = "completed"
        print("🎉 Pipeline completed!")
    else:
        # Check gate for next step
        gate_pass, gate_msg = check_gate(state, next_step.get("gate"))
        if not gate_pass:
            state["status"] = "blocked"
            state["failed_gate"] = next_step.get("gate")
            state["last_error"] = gate_msg
            print(f"🚫 GATE BLOCKED: {gate_msg}")
        else:
            print(f"➡️ Advanced to: {next_step['name']} (agent: {next_step['agent']})")

    save_state(state, state_file)
    return state


def record_audit_failure(state: dict, state_file: Path) -> dict:
    """Record an audit failure and check circuit breaker."""
    pipeline = get_pipeline(state["pipeline_name"])
    limit = pipeline.get("circuit_breaker_limit", 3)

    state["audit_attempts"] += 1

    if state["audit_attempts"] >= limit:
        state["status"] = "halted"
        state["last_error"] = f"CIRCUIT BREAKER: {state['audit_attempts']}/{limit} audit failures. Pipeline halted. Escalating to user."
        print(f"🔴 CIRCUIT BREAKER TRIGGERED: {state['audit_attempts']}/{limit} failures")
        print("   Pipeline HALTED. Manual intervention required.")
    else:
        # Revert to prose generation step for rewrite
        prose_step_idx = None
        for i, step in enumerate(pipeline["steps"]):
            if step["id"] == "prose-generation":
                prose_step_idx = i
                break

        if prose_step_idx is not None:
            state["current_step"] = prose_step_idx
            # Remove prose-generation and quality-audit from completed
            state["steps_completed"] = [
                s for s in state["steps_completed"]
                if s not in ("prose-generation", "quality-audit")
            ]
            state["status"] = "running"
            state["last_error"] = f"Audit attempt {state['audit_attempts']}/{limit} failed. Reverting to prose generation."
            print(f"⚠️ Audit failed ({state['audit_attempts']}/{limit}). Reverting to prose generation.")
        else:
            state["status"] = "failed"
            state["last_error"] = "Cannot find prose-generation step to revert to"

    save_state(state, state_file)
    return state


# ═══════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="LND Studio Pipeline Runner")
    sub = parser.add_subparsers(dest="command")

    # init
    p_init = sub.add_parser("init", help="Initialize pipeline state")
    p_init.add_argument("pipeline", help="Pipeline name (e.g., gooner-alchemist)")
    p_init.add_argument("run_dir", help="Output directory for this run")
    p_init.add_argument("--pages", type=str, default=None, help="Page range (e.g., 1-20)")
    p_init.add_argument("--state-file", type=Path, default=DEFAULT_STATE_FILE)

    # status
    p_status = sub.add_parser("status", help="Show pipeline status")
    p_status.add_argument("--state-file", type=Path, default=DEFAULT_STATE_FILE)

    # advance
    p_advance = sub.add_parser("advance", help="Advance to next step")
    p_advance.add_argument("--state-file", type=Path, default=DEFAULT_STATE_FILE)

    # gate
    p_gate = sub.add_parser("gate", help="Check if a gate is satisfied")
    p_gate.add_argument("step_id", help="Step ID to check gate for")
    p_gate.add_argument("--state-file", type=Path, default=DEFAULT_STATE_FILE)

    # context
    p_context = sub.add_parser("context", help="Output context string for current state")
    p_context.add_argument("--state-file", type=Path, default=DEFAULT_STATE_FILE)

    # fail-audit
    p_fail = sub.add_parser("fail-audit", help="Record audit failure + circuit breaker check")
    p_fail.add_argument("--state-file", type=Path, default=DEFAULT_STATE_FILE)

    # list-pipelines
    sub.add_parser("list", help="List available pipelines")

    args = parser.parse_args()

    if args.command == "init":
        pipeline = get_pipeline(args.pipeline)
        pages = None
        if args.pages:
            start, end = map(int, args.pages.split("-"))
            pages = list(range(start, end + 1))

        state = create_state(args.pipeline, args.run_dir, pages)
        save_state(state, args.state_file)
        print(f"✅ Pipeline '{args.pipeline}' initialized")
        print(f"   Run dir: {args.run_dir}")
        print(f"   State file: {args.state_file}")
        if pages:
            print(f"   Pages: {pages[0]:03d}-{pages[-1]:03d} ({len(pages)} pages)")
        print(f"   First step: {pipeline['steps'][0]['name']}")

    elif args.command == "status":
        state = load_state(args.state_file)
        if state is None:
            print("❌ No active pipeline. Run 'init' first.")
            sys.exit(1)
        print(build_context(state))

    elif args.command == "advance":
        state = load_state(args.state_file)
        if state is None:
            print("❌ No active pipeline.")
            sys.exit(1)
        advance_step(state, args.state_file)

    elif args.command == "gate":
        state = load_state(args.state_file)
        if state is None:
            print("❌ No active pipeline.")
            sys.exit(1)
        pipeline = get_pipeline(state["pipeline_name"])
        target_step = None
        for step in pipeline["steps"]:
            if step["id"] == args.step_id:
                target_step = step
                break
        if target_step is None:
            print(f"❌ Unknown step: {args.step_id}")
            sys.exit(1)
        gate_pass, gate_msg = check_gate(state, target_step.get("gate"))
        print(f"{'✅' if gate_pass else '🚫'} {gate_msg}")
        sys.exit(0 if gate_pass else 1)

    elif args.command == "context":
        state = load_state(args.state_file)
        if state is None:
            print("❌ No active pipeline.")
            sys.exit(1)
        print(build_context(state))

    elif args.command == "fail-audit":
        state = load_state(args.state_file)
        if state is None:
            print("❌ No active pipeline.")
            sys.exit(1)
        record_audit_failure(state, args.state_file)

    elif args.command == "list":
        print("Available pipelines:")
        for name, pipeline in PIPELINES.items():
            steps = [s["id"] for s in pipeline["steps"]]
            print(f"  {name}: {pipeline['description']}")
            print(f"    Steps: {' → '.join(steps)}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
