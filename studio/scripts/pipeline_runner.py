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
import re
import sys
import fcntl
from datetime import datetime, timezone
from pathlib import Path

import yaml


# Import ledger tools safely
try:
    from ledger_manager import verify_preflight, lock_and_update_ledger
except ImportError:
    # Fallback to local import if needed
    sys.path.append(str(Path(__file__).parent))
    from ledger_manager import verify_preflight, lock_and_update_ledger

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
                "rule_step": None,
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
                "gate": None,
            },
            {
                "id": "context-loading",
                "name": "Step 3: Context Loading",
                "agent": "lnd-orchestrator",
                "step_file": "services/gooner-alchemist/steps/step-03-context-loading.md",
                "rule_step": "context-loading",
                "output_schema": None,
                "gate": "forensic_complete",
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
    "erotic-captioner": {
        "description": "EC: Erotic Image Captioning Pipeline",
        "steps": [
            {
                "id": "forensic-analysis",
                "name": "Forensic Analysis",
                "agent": "manga-adapter",
                "step_file": "studio/core/panel-forensic/templates/forensic_analysis.md",
                "rule_step": "forensic-analysis",
                "output_schema": "forensic-state.schema.json",
                "gate": None,
            },
            {
                "id": "context-loading",
                "name": "Context Loading",
                "agent": "lnd-orchestrator",
                "step_file": "studio/core/volume-context-extractor/templates/context_extraction.md",
                "rule_step": "context-loading",
                "output_schema": None,
                "gate": "forensic_complete",
            },
            {
                "id": "prose-generation",
                "name": "Prose Generation",
                "agent": "lewd-writer",
                "step_file": "studio/core/erotic-caption-writer/templates/erotic_caption.md",
                "rule_step": "prose-generation",
                "output_schema": "draft-prose.schema.json",
                "gate": "context_loaded",
            },
            {
                "id": "quality-audit",
                "name": "Quality Audit",
                "agent": "gooner-editor",
                "step_file": "studio/core/gooner-audit-engine/templates/quality_audit.md",
                "rule_step": "quality-audit",
                "output_schema": "audit-report.schema.json",
                "gate": "prose_complete",
            },
            {
                "id": "complete",
                "name": "Completion",
                "agent": "lnd-orchestrator",
                "step_file": "studio/core/orchestration/templates/complete.md",
                "rule_step": None,
                "output_schema": None,
                "gate": "audit_pass",
            },
        ],
        "circuit_breaker_limit": 3,
    },
    "novel-development": {
        "description": "ND: Full Novel/Doujinshi Localization Pipeline",
        "steps": [
            {
                "id": "forensic-analysis",
                "name": "Forensic Analysis",
                "agent": "manga-adapter",
                "step_file": "studio/core/panel-forensic/templates/forensic_analysis.md",
                "rule_step": "forensic-analysis",
                "output_schema": "forensic-state.schema.json",
                "gate": None,
            },
            {
                "id": "character-alignment",
                "name": "Character Alignment",
                "agent": "character-architect",
                "step_file": "studio/core/roleplay-engine/templates/character_card.md",
                "rule_step": "character-alignment",
                "output_schema": "character-bible.schema.json",
                "gate": "forensic_complete",
            },
            {
                "id": "prose-generation",
                "name": "Prose Generation",
                "agent": "lewd-writer",
                "step_file": "studio/core/lewd-writer/templates/lewd_prose.md",
                "rule_step": "prose-generation",
                "output_schema": "draft-prose.schema.json",
                "gate": "forensic_complete",
            },
            {
                "id": "quality-audit",
                "name": "Quality Audit",
                "agent": "gooner-editor",
                "step_file": "studio/core/gooner-audit-engine/templates/quality_audit.md",
                "rule_step": "quality-audit",
                "output_schema": "audit-report.schema.json",
                "gate": "prose_complete",
            },
            {
                "id": "complete",
                "name": "Completion",
                "agent": "lnd-orchestrator",
                "step_file": "studio/core/orchestration/templates/complete.md",
                "rule_step": None,
                "output_schema": None,
                "gate": "audit_pass",
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
        "scene_continuity": {
            "characters": {},
            "environment": {},
            "active_fetishes": []
        },
        "last_continuity_delta": None,
        "created_at": now,
        "updated_at": now,
    }


def load_state(state_file: Path) -> dict | None:
    """Load state from YAML file with flock mutex shared lock."""
    if not state_file.exists():
        return None
    lock_file_path = state_file.parent / (state_file.name + ".lock")
    lock_file = open(lock_file_path, "w")
    try:
        fcntl.flock(lock_file, fcntl.LOCK_SH)
        with open(state_file, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    finally:
        fcntl.flock(lock_file, fcntl.LOCK_UN)
        lock_file.close()


def save_state(state: dict, state_file: Path):
    """Save state to YAML file with flock mutex exclusive lock."""
    state["updated_at"] = datetime.now(timezone.utc).isoformat()
    state_file.parent.mkdir(parents=True, exist_ok=True)
    lock_file_path = state_file.parent / (state_file.name + ".lock")
    lock_file = open(lock_file_path, "w")
    try:
        fcntl.flock(lock_file, fcntl.LOCK_EX)
        with open(state_file, "w", encoding="utf-8") as f:
            yaml.dump(state, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    finally:
        fcntl.flock(lock_file, fcntl.LOCK_UN)
        lock_file.close()


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

    if state.get("scene_continuity"):
        lines.append("## 🔄 Scene Continuity State")
        sc = state["scene_continuity"]
        if sc.get("characters"):
            lines.append("### Characters present:")
            for char, c_state in sorted(sc["characters"].items()):
                lines.append(f"- **{char}**: clothing_state=`{c_state.get('clothing_state', 'normal')}`, arousal_level=`{c_state.get('arousal_level', 'neutral')}`, fluids=`{c_state.get('fluids', 'none')}`")
        if sc.get("environment"):
            lines.append("### Environment:")
            env = sc["environment"]
            if env.get("location"):
                lines.append(f"- **Location**: `{env['location']}`")
            if env.get("atmosphere"):
                lines.append(f"- **Atmosphere**: `{env['atmosphere']}`")
        lines.append("")

    if state.get("last_continuity_delta"):
        lines.append(state["last_continuity_delta"])
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


def update_scene_continuity(state: dict, page_num: int):
    """Load forensic report for page_num, parse its JSON, compute diff, and update state."""
    run_dir = Path(state["run_dir"])
    forensics_file = run_dir / "_forensics" / f"{page_num:03d}_forensics.md"
    
    if not forensics_file.exists():
        return
        
    try:
        content = forensics_file.read_text(encoding="utf-8").strip()
        # Extract JSON from markdown if wrapped in ```json ... ```
        json_str = content
        if "```json" in content:
            match = re.search(r"```json\s*(.*?)\s*```", content, re.DOTALL)
            if match:
                json_str = match.group(1)
        elif "```" in content:
            match = re.search(r"```\s*(.*?)\s*```", content, re.DOTALL)
            if match:
                json_str = match.group(1)
                
        # Parse forensic JSON
        forensic_data = json.loads(json_str)
        
        # Load previous continuity
        prev_continuity = state.setdefault("scene_continuity", {
            "characters": {},
            "environment": {},
            "active_fetishes": []
        })
        
        # Compute diff and update continuity
        from context_diff import compute_state_diff
        updated_continuity, diff_md = compute_state_diff(prev_continuity, forensic_data)
        
        state["scene_continuity"] = updated_continuity
        
        # Store the current diff in state
        state["last_continuity_delta"] = diff_md
        print(f"🔄 State continuity updated for page {page_num:03d}.")
        if diff_md:
            print("   Delta computed:")
            for line in diff_md.split("\n"):
                if line.strip().startswith("-"):
                    print(f"     {line}")
    except Exception as e:
        print(f"⚠️ Warning: Could not update scene continuity: {e}")


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

    # If forensic-analysis step is completed, update scene continuity
    if step["id"] == "forensic-analysis":
        pages = state.get("pages", [])
        page_idx = state.get("current_page_index", 0)
        if page_idx < len(pages):
            page_num = pages[page_idx]
            update_scene_continuity(state, page_num)

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

    # run
    p_run = sub.add_parser("run", help="Run a pipeline end-to-end with validation")
    p_run.add_argument("pipeline", help="Pipeline name (e.g., erotic-captioner, novel-development)")
    p_run.add_argument("--input", required=True, help="Input directory or image path")
    p_run.add_argument("--pages", type=str, default=None, help="Page range (e.g., 1-5)")
    p_run.add_argument("--state-file", type=Path, default=DEFAULT_STATE_FILE)

    # dry-run
    p_dry = sub.add_parser("dry-run", help="Dry-run a pipeline to verify configurations and gates")
    p_dry.add_argument("pipeline", help="Pipeline name")

    # resume
    p_resume = sub.add_parser("resume", help="Resume a saved pipeline execution session")
    p_resume.add_argument("run_id", help="Session ID to resume")
    p_resume.add_argument("--state-file", type=Path, default=DEFAULT_STATE_FILE)

    # reload
    sub.add_parser("reload", help="Synchronize the State Ledger and reload dynamic contexts")

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

    elif args.command == "run":
        pipeline = get_pipeline(args.pipeline)
        # Create a unique session ID
        run_id = f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        session_dir = PROJECT_ROOT / "_out" / "production-sessions" / run_id
        session_dir.mkdir(parents=True, exist_ok=True)
        
        pages = None
        if args.pages:
            start, end = map(int, args.pages.split("-"))
            pages = list(range(start, end + 1))

        # Copy input info or record it
        input_info = session_dir / "input_source.json"
        with open(input_info, "w") as f:
            json.dump({"input_path": args.input, "run_id": run_id}, f, indent=2)

        # Preflight check all agents used in this pipeline
        print("🔍 Performing Pre-flight Consistency checks on all pipeline agents...")
        all_passed = True
        for step in pipeline["steps"]:
            agent_filename = f"{step['agent']}.agent.yaml"
            passed = verify_preflight(agent_filename)
            if not passed:
                print(f"❌ Consistency verification failed for agent config: {agent_filename}")
                all_passed = False
            else:
                print(f"✅ Agent verified: {agent_filename}")

        if not all_passed:
            print("❌ Pipeline initiation aborted due to agent prompt drift from State Ledger. Run reload to update.")
            sys.exit(1)

        # Create session state
        state = create_state(args.pipeline, str(session_dir), pages)
        state["run_id"] = run_id
        state["input_path"] = args.input
        
        # Save to session dir and current state
        session_state_file = session_dir / "state.yaml"
        save_state(state, session_state_file)
        save_state(state, args.state_file)

        print(f"🚀 Initiated run '{run_id}' for pipeline '{args.pipeline}' successfully!")
        print(f"   Session Directory: {session_dir}")
        print(f"   Active Step: {pipeline['steps'][0]['name']}")

    elif args.command == "dry-run":
        pipeline = get_pipeline(args.pipeline)
        print(f"🔍 Running Dry-Run validation for pipeline: '{args.pipeline}'")
        print(f"   Description: {pipeline['description']}")
        print(f"   Steps sequence: {' → '.join(s['id'] for s in pipeline['steps'])}")
        
        # Preflight verification check
        all_passed = True
        for step in pipeline["steps"]:
            agent_filename = f"{step['agent']}.agent.yaml"
            passed = verify_preflight(agent_filename)
            if not passed:
                print(f"❌ Configuration drift detected on agent config: {agent_filename}")
                all_passed = False
            else:
                print(f"✅ Verified step '{step['id']}' agent card: {agent_filename}")

        if all_passed:
            print("🏆 DRY-RUN SUCCESSFUL: All agent cards consistent with State Ledger!")
        else:
            print("❌ DRY-RUN FAILED: Configuration drifts detected. Synchronize with 'reload' command.")
            sys.exit(1)

    elif args.command == "resume":
        run_id = args.run_id
        session_state_file = PROJECT_ROOT / "_out" / "production-sessions" / run_id / "state.yaml"
        if not session_state_file.exists():
            print(f"❌ Session ID '{run_id}' not found at {session_state_file}.")
            sys.exit(1)
        
        # Load state from session directory
        state = load_state(session_state_file)
        if state is None:
            print(f"❌ Failed to load state for session '{run_id}'.")
            sys.exit(1)

        # Save as the default active state file
        save_state(state, args.state_file)
        print(f"🔄 Resumed session '{run_id}' for pipeline '{state['pipeline_name']}' successfully.")
        print(build_context(state))

    elif args.command == "reload":
        print("🔄 Reloading configuration context and synchronizing State Ledger...")
        lock_and_update_ledger()
        print("✅ State Ledger successfully synchronized with current agents and lexicons on disk.")

    elif args.command == "status":
        state = load_state(args.state_file)
        if state is None:
            print("❌ No active pipeline. Run 'init' or 'run' first.")
            sys.exit(1)
        print(build_context(state))

    elif args.command == "advance":
        state = load_state(args.state_file)
        if state is None:
            print("❌ No active pipeline.")
            sys.exit(1)
        # Verify active agent before advancing
        step = get_current_step(state)
        if step:
            agent_filename = f"{step['agent']}.agent.yaml"
            if not verify_preflight(agent_filename):
                print(f"❌ Pre-flight check failed for {agent_filename}. Aborting step progression.")
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
