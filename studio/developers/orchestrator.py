import asyncio
import textwrap
import sys
import argparse
from pathlib import Path
from .agents.registry import create_agent

# ── Configuration ────────────────────────────────────────────────────────────

TIMEOUT = 600.0
CONTEXT_SUMMARIZE_THRESHOLD = 120  # lines

DEVELOPERS_DIR = Path(__file__).parent.absolute()
CONFIG_DIR = DEVELOPERS_DIR / "config"
TEMPLATES_DIR = CONFIG_DIR / "templates"

# ── Utilities ────────────────────────────────────────────────────────────────

def _sep(title: str):
    print(f"\n== {title} " + "=" * (max(0, 78 - len(title) - 4)))

def _session_dir(task: str) -> Path:
    return Path.cwd() / "_out" / "agent-sessions" / task

def _write_atomic(path: Path, content: str):
    path.write_text(content, encoding="utf-8")

def _append_context(session_dir: Path, header: str, content: str):
    ctx_file = session_dir / "context.md"
    with open(ctx_file, "a", encoding="utf-8") as f:
        f.write(f"\n## {header}\n\n{content}\n")

def _inject_context(session_dir: Path, current_prompt: str) -> str:
    ctx_file = session_dir / "context.md"
    summary_file = session_dir / "context_summary.md"
    
    inject = []
    if summary_file.exists():
        inject.append(f"### Previous Summary\n{summary_file.read_text()}")
    elif ctx_file.exists():
        raw = ctx_file.read_text()
        # Only inject last ~4000 chars if no summary to avoid token overflow
        inject.append(f"### Recent Context\n{raw[-4000:] if len(raw) > 4000 else raw}")
    
    inject.append(f"### Current Task\n{current_prompt}")
    return "\n\n".join(inject)

def _load_template(name: str) -> str:
    f = TEMPLATES_DIR / name
    return f.read_text() if f.exists() else "Template not found: {name}"

def _load_files(file_paths: list[str]) -> str:
    ctx = []
    for fp in file_paths:
        p = Path(fp)
        if p.exists() and p.is_file():
            content = p.read_text(errors="replace")
            ctx.append(f"### FILE: {fp}\n```\n{content}\n```")
        else:
            ctx.append(f"### FILE: {fp}\n(File not found or not a file)")
    return "\n\n".join(ctx)

def _build_prompt(role_content: str, template: str, content: str) -> str:
    return f"{role_content}\n\n{template}\n\n{content}"

# ── Main Orchestration Logic ─────────────────────────────────────────────────

async def run_panel(
    task: str,
    mode: str,
    prompt: str,
    agent_configs: list[dict], # List of {"id": "hermes", "role": "dev-architect", ...}
    files: list[str] = None,
) -> None:
    session_dir = _session_dir(task)
    session_dir.mkdir(parents=True, exist_ok=True)

    file_ctx = _load_files(files) if files else ""
    full_prompt = f"{prompt}\n\n{file_ctx}" if file_ctx else prompt

    _sep(f"STUDIO  mode={mode}  task={task}")
    print(f"Agents: {', '.join(a['id'] for a in agent_configs)}")

    # Instantiate agents
    agents = []
    for cfg in agent_configs:
        try:
            agents.append({
                "instance": create_agent(cfg["id"], cfg["role"], CONFIG_DIR),
                "cfg": cfg
            })
        except Exception as e:
            print(f"[!] Error loading agent {cfg['id']}: {e}")
            return

    # Mode Dispatch
    if mode == "arch":
        await _mode_single(session_dir, full_prompt, agents[0], "Architecture Review", "arch_review.md")
    elif mode == "code":
        await _mode_single(session_dir, full_prompt, agents[0], "Code Review", "code_review.md")
    elif mode == "review":
        await _mode_review(session_dir, full_prompt, agents)
    elif mode == "cross":
        await _mode_cross(session_dir, full_prompt, agents)
    else:
        print(f"[!] Unknown mode: {mode}")

async def _mode_single(session_dir: Path, prompt: str, agent_pkg: dict, title: str, template_name: str):
    agent = agent_pkg["instance"]
    tmpl = _load_template(template_name)
    ctx_prompt = _inject_context(session_dir, prompt)
    full = _build_prompt(agent.role_content, tmpl, ctx_prompt)
    
    _sep(f"{agent_pkg['cfg']['id']} [{agent.role_name}] — {title}")
    out = await agent.call(full, session_dir)
    print(out)
    _write_atomic(session_dir / f"{agent_pkg['cfg']['id']}_last.md", out)
    _append_context(session_dir, f"{agent_pkg['cfg']['id']} [{agent.role_name}] {title}", out)

async def _mode_review(session_dir: Path, prompt: str, agents: list[dict]):
    # Agent 1 (Arch)
    await _mode_single(session_dir, prompt, agents[0], "Architecture Review", "arch_review.md")
    
    # Agent 2 (Code) if exists
    if len(agents) > 1:
        await _mode_single(session_dir, prompt, agents[1], "Code Review", "code_review.md")

async def _mode_cross(session_dir: Path, prompt: str, agents: list[dict]):
    if len(agents) < 2:
        print("[!] Cross mode requires at least 2 agents.")
        return

    # Pass 1 — independent reviews
    results = []
    for pkg in agents:
        agent = pkg["instance"]
        tmpl = _load_template("arch_review.md" if agents.index(pkg) == 0 else "code_review.md")
        full = _build_prompt(agent.role_content, tmpl, _inject_context(session_dir, prompt))
        _sep(f"Pass 1 — {pkg['cfg']['id']} [{agent.role_name}]")
        out = await agent.call(full, session_dir)
        print(out)
        results.append(out)
        _append_context(session_dir, f"{pkg['cfg']['id']} Pass 1", out)

    # Pass 2 — Challenge each other
    _sep(f"Pass 2 — {agents[0]['cfg']['id']} vs {agents[1]['cfg']['id']}")
    h2 = await agents[0]["instance"].call(
        f"The other reviewer ({agents[1]['cfg']['id']}) said:\n\n{results[1]}\n\n"
        f"Do you agree or disagree? Add implications they missed. Max 200 words.",
        session_dir
    )
    print(f"\n{agents[0]['cfg']['id']} response:\n{h2}")
    _append_context(session_dir, f"{agents[0]['cfg']['id']} Pass 2 (cross)", h2)

    c2 = await agents[1]["instance"].call(
        f"The other reviewer ({agents[0]['cfg']['id']}) said:\n\n{results[0]}\n\n"
        f"Do you agree or disagree? Add concerns they missed. Max 200 words.",
        session_dir
    )
    print(f"\n{agents[1]['cfg']['id']} response:\n{c2}")
    _append_context(session_dir, f"{agents[1]['cfg']['id']} Pass 2 (cross)", c2)

    # Synthesis by first agent
    _sep("Synthesis")
    syn = await agents[0]["instance"].call(
        "Synthesize this panel review. Produce 3 actionable conclusions.\n"
        f"Review 1:\n{results[0]}\n\nReview 2:\n{results[1]}\n\nDebate:\n{h2}\n{c2}",
        session_dir
    )
    print(syn)
    _append_context(session_dir, "Synthesis", syn)

# ── CLI Interface ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="LND Studio Developer Orchestrator")
    p.add_argument("--task", required=True)
    p.add_argument("--mode", default="review", choices=["arch", "code", "review", "cross"])
    p.add_argument("--prompt", required=True)
    p.add_argument("--agents", default="hermes:se/m-architect claude:dev/m-prompt-expert", 
                   help="Space separated agent_id:role_name pairs")
    p.add_argument("--files", default="", help="Space separated file paths")
    
    args = p.parse_args()
    
    agent_configs = []
    for pair in args.agents.split():
        if ":" in pair:
            aid, role = pair.split(":", 1)
        else:
            aid, role = pair, "m-architect"
        agent_configs.append({"id": aid, "role": role})

    files = [f for f in args.files.split() if f] if args.files else []
    asyncio.run(run_panel(args.task, args.mode, args.prompt, agent_configs, files=files))
