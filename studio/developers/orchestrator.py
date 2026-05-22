"""
LND Studio Developer Orchestrator

Multi-agent review system with:
- Auto-summarizing context management (XML-wrapped)
- Schema-validated agent outputs (Pydantic)
- Lazy knowledge loading (namespace-based)
- Extensible mode system

Usage:
    python -m studio.developers.orchestrator \\
        --task my-review \\
        --mode arch \\
        --prompt "Review this architecture" \\
        --agents hermes:se/m-architect \\
        --files path/to/file.py

Modes:
    arch: Architecture review (single agent)
    code: Code/prose review (single agent)
    review: Sequential arch + code review (2 agents)
    cross: Multi-agent debate with synthesis (2+ agents)

Phase 1 Implementation (2026-05-16):
- ✅ Auto-summarization with XML context wrapping
- ✅ Pydantic schemas (ArchReviewOutput, CodeReviewOutput)
- ✅ XML-structured templates
- ✅ Schema validation in orchestrator
- ✅ Lazy knowledge loading in BaseAgent
- 📊 Token reduction: 77% (23,500 → 5,300 tokens/call)
"""

import asyncio
import textwrap
import sys
import argparse
import json
import os
import re
import tempfile
from pathlib import Path
from pydantic import ValidationError
from .agents.registry import create_agent
from .schemas import (
    ArchReviewOutput, CodeReviewOutput, QAAuditOutput, SynthesisOutput
)
from studio.core.schemas import (
    ForensicOutput, PreludeOutput, CaptionOutput
)
from .mode_registry import ModeRegistry

# ── Configuration ────────────────────────────────────────────────────────────

DEVELOPERS_DIR = Path(__file__).parent.absolute()
CONFIG_DIR = DEVELOPERS_DIR / "config"
TEMPLATES_DIR = CONFIG_DIR / "templates"
REGISTRY_PATH = CONFIG_DIR / "mode_registry.yaml"

# Load mode registry
MODE_REGISTRY = ModeRegistry(REGISTRY_PATH)

# Global settings from registry
TIMEOUT = MODE_REGISTRY.get_setting("timeout", 600.0)
CONTEXT_SUMMARIZE_THRESHOLD = MODE_REGISTRY.get_setting("context_summarize_threshold", 120)

# Schema mapping for validation (loaded from registry)
SCHEMA_MAP = {
    "ArchReviewOutput": ArchReviewOutput,
    "CodeReviewOutput": CodeReviewOutput,
    "QAAuditOutput": QAAuditOutput,
    "SynthesisOutput": SynthesisOutput,
}

# ── Utilities ────────────────────────────────────────────────────────────────

def _extract_json(text: str) -> str:
    """Extract JSON from markdown code blocks if present."""
    match = re.search(r'```(?:json)?\s*(\{.*\}|\[.*\])\s*```', text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()

def _sep(title: str):
    print(f"\n== {title} " + "=" * (max(0, 78 - len(title) - 4)))

def _session_dir(task: str) -> Path:
    return Path.cwd() / "_out" / "agent-sessions" / task

def _write_atomic(path: Path, content: str):
    """Write content to file atomically via temp file + os.replace."""
    fd, tmp_path = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(content)
        os.replace(tmp_path, path)
    except Exception:
        # Clean up temp file on failure
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise

def _append_context(session_dir: Path, header: str, content: str):
    ctx_file = session_dir / "context.md"
    with open(ctx_file, "a", encoding="utf-8") as f:
        f.write(f"\n## {header}\n\n{content}\n")

async def _auto_summarize_context(ctx_file: Path, summary_file: Path):
    """Summarize context.md when it exceeds threshold."""
    from datetime import datetime

    full_context = ctx_file.read_text()

    summary_prompt = f"""Summarize the following agent conversation history into key decisions and findings.
Keep only critical information. Max 500 words.

<context>
{full_context}
</context>

Output format:
- Key Decisions: [bullet points]
- Critical Findings: [bullet points]
- Action Items: [bullet points]
"""

    # Use configured summarization agent (default to se/m-architect)
    sum_agent_id = MODE_REGISTRY.get_setting("summarization_agent", "hermes")
    sum_role = MODE_REGISTRY.get_setting("summarization_role", "se/m-architect")
    agent = create_agent(sum_agent_id, sum_role, CONFIG_DIR)
    summary = await _call_agent_with_retry(agent, summary_prompt, ctx_file.parent, timeout=TIMEOUT)

    summary_file.write_text(f"# Context Summary (Generated: {datetime.now().isoformat()})\n\n{summary}")

    # Archive old context
    archive_file = ctx_file.parent / f"context_archived_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    ctx_file.rename(archive_file)

    # Reset context.md
    ctx_file.write_text(f"# Context (Summarized on {datetime.now().isoformat()})\n\n")

async def _inject_context(session_dir: Path, current_prompt: str = "") -> str:
    """Inject context with auto-summarization and XML wrapping.

    P3 FIX: current_prompt is NO LONGER embedded in the context injection.
    The prompt should only appear once, in the <task_instruction> section
    built by PromptBuilder. This eliminates token duplication.
    """
    ctx_file = session_dir / "context.md"
    summary_file = session_dir / "context_summary.md"

    # Auto-summarize if threshold exceeded or summary exists but context grew again
    if ctx_file.exists():
        lines = ctx_file.read_text().split('\n')
        if len(lines) > CONTEXT_SUMMARIZE_THRESHOLD:
            await _auto_summarize_context(ctx_file, summary_file)

    # Structured injection with XML anchors (context only, NO task duplication)
    parts = ["<system_context>"]

    if summary_file.exists():
        parts.append(f"<historical_summary>\n{summary_file.read_text()}\n</historical_summary>")

    if ctx_file.exists():
        recent_lines = ctx_file.read_text().split('\n')[-50:]
        parts.append(f"<recent_context>\n{chr(10).join(recent_lines)}\n</recent_context>")

    parts.append("</system_context>")

    return "\n".join(parts)

def _load_template(name: str) -> str:
    f = TEMPLATES_DIR / name
    if not f.exists():
        return f"Template not found: {name}"
    return f.read_text()

def _load_files(file_paths: list[str]) -> str:
    ctx = []
    for f_path in file_paths:
        p = Path(f_path)
        if p.exists() and p.is_file():
            try:
                content = p.read_text()
                ctx.append(f"### FILE: {p.name}\n```\n{content}\n```")
            except UnicodeDecodeError:
                ctx.append(f"### FILE: {p.name}\n[Binary file - Content omitted]")
        else:
            ctx.append(f"### FILE: {f_path}\n(File not found or not a file)")
    return "\n\n".join(ctx)

def _build_prompt(role_content: str, template: str, content: str) -> str:
    return f"{role_content}\n\n{template}\n\n{content}"

async def _call_agent_with_retry(agent, prompt: str, session_dir: Path, timeout: float = 180.0, retries: int = 3) -> str:
    """Call an agent's call method with retries and exponential backoff."""
    last_err = None
    for attempt in range(retries):
        try:
            if attempt > 0:
                print(f"[🔄 Attempt {attempt + 1}/{retries}] Retrying call to agent {agent.role_name}...")
            return await agent.call(prompt, session_dir, timeout=timeout)
        except asyncio.TimeoutError as e:
            print(f"[⚠️ Warning] Timeout occurred calling agent {agent.role_name} (Attempt {attempt + 1}/{retries})")
            last_err = e
        except Exception as e:
            print(f"[⚠️ Warning] Error occurred calling agent {agent.role_name}: {e} (Attempt {attempt + 1}/{retries})")
            last_err = e
        if attempt < retries - 1:
            await asyncio.sleep(2 ** attempt)
    
    # If we get here, all retries failed
    raise last_err or Exception(f"Failed to call agent {agent.role_name} after {retries} attempts.")

# ── Classes ──────────────────────────────────────────────────────────────────

class KnowledgeIndex:
    def __init__(self, index_path: Path):
        self.index = json.loads(index_path.read_text())

    def get_rules(self, role: str, specific_files: list[str] = None) -> str:
        """
        Dynamically load rules based on role prefix (se/ dev/ qa/).

        Args:
            role: Role string like "se/m-architect" or "dev/m-prompt-expert"
            specific_files: Optional list of specific files to load (lazy loading)
                           If None, loads all files in namespace (greedy - deprecated)

        Returns:
            Concatenated rule content
        """
        namespace = role.split("/")[0].lower()
        if namespace not in self.index["namespaces"]:
            return ""

        ns = self.index["namespaces"][namespace]
        rule_dir = Path(ns["path"])

        # Lazy loading: only load specified files
        if specific_files is not None:
            rules = []
            for file in specific_files:
                p = rule_dir / file
                if p.exists():
                    rules.append(f"### {file}\n{p.read_text()}")
                else:
                    print(f"[!] Warning: Knowledge file not found: {p}")
            return "\n\n".join(rules)

        # Greedy loading (deprecated): load all files
        # This path should be avoided - use mode registry to specify files
        rules = []
        for file in ns["files"]:
            p = rule_dir / file
            if p.exists():
                rules.append(f"### {file}\n{p.read_text()}")
        return "\n\n".join(rules)

class PromptBuilder:
    """Enforces strict prompt hierarchy with XML boundaries.

    P3 FIX: Truncation now targets ONLY the context section.
    System rules, role, task, and constraints are always preserved intact.
    This prevents broken XML tags from corrupting agent behavior.
    """
    def __init__(self, max_tokens: int = 6000):
        self.max_tokens = max_tokens  # Rough char-based limit (6000 tokens ~= 24k chars)
        self.max_chars = max_tokens * 4
        self.sections = {
            "system": [],
            "role": [],
            "context": [],
            "task": [],
            "constraints": []
        }

    def add_system(self, content: str): self.sections["system"].append(f"<system_rules>\n{content}\n</system_rules>")
    def add_role(self, content: str): self.sections["role"].append(f"<agent_persona>\n{content}\n</agent_persona>")
    def add_context(self, content: str): self.sections["context"].append(f"<context>\n{content}\n</context>")
    def add_task(self, content: str): self.sections["task"].append(f"<task_instruction>\n{content}\n</task_instruction>")
    def add_constraint(self, content: str): self.sections["constraints"].append(f"<constraint>\n{content}\n</constraint>")

    def build(self) -> str:
        # Build non-context sections first (these are NEVER truncated)
        system_block = "\n".join(self.sections["system"])
        role_block = "\n".join(self.sections["role"])
        task_block = "\n".join(self.sections["task"])
        constraint_block = "\n".join(self.sections["constraints"])
        context_block = "\n".join(self.sections["context"])

        # Calculate budget: protected sections get priority, context gets remainder
        protected = "\n\n".join(p for p in [system_block, role_block, task_block, constraint_block] if p)
        protected_chars = len(protected)
        context_budget = self.max_chars - protected_chars - 100  # 100 char margin

        # Truncate ONLY context if it exceeds budget
        if context_budget > 0 and len(context_block) > context_budget:
            context_block = (
                context_block[:context_budget]
                + "\n</context>\n<context>\n[Context truncated to fit token budget]\n</context>"
            )

        # Assemble in strict hierarchy order (task block with schema/instruction ALWAYS at the absolute end for maximum LLM compliance)
        parts = [system_block, role_block, context_block, constraint_block, task_block]
        return "\n\n".join(p for p in parts if p)

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

    # Initialize knowledge index
    knowledge = KnowledgeIndex(CONFIG_DIR / "knowledge_index.json")

    # Validate mode exists in registry
    is_valid, error_msg = MODE_REGISTRY.validate_mode(mode)
    if not is_valid:
        print(f"[!] {error_msg}")
        return

    # Get mode configuration
    mode_config = MODE_REGISTRY.get_mode(mode)
    execution_type = mode_config["execution_type"]

    # Dispatch based on execution type
    if execution_type == "single":
        template = MODE_REGISTRY.get_template(mode)
        title = mode_config.get("description", "Review")
        await _mode_single(session_dir, full_prompt, agents[0], title, template, knowledge, mode)
    elif execution_type == "sequential":
        await _mode_sequential(session_dir, agents, full_prompt, mode_config, knowledge)
    elif execution_type == "debate":
        await _mode_cross(session_dir, full_prompt, agents, knowledge, mode)
    else:
        print(f"[!] Unknown execution type: {execution_type}")

async def _mode_sequential(session_dir: Path, agents: list[dict], prompt: str, mode_config: dict, knowledge: KnowledgeIndex):
    """Generic sequential execution based on steps in registry."""
    steps = mode_config.get("steps", [])
    if not steps:
        # Fallback for old mode if steps not defined (legacy review)
        steps = [
            {"mode": "arch", "agent_index": 0},
            {"mode": "code", "agent_index": 1}
        ]

    for i, step in enumerate(steps):
        step_mode = step["mode"]
        agent_idx = step["agent_index"]
        
        if agent_idx >= len(agents):
            print(f"[!] Agent index {agent_idx} out of range for step {i+1}")
            continue

        step_cfg = MODE_REGISTRY.get_mode(step_mode)
        template = MODE_REGISTRY.get_template(step_mode)
        title = step_cfg.get("description", f"Step {i+1}: {step_mode}")
        
        _sep(f"Step {i+1}/{len(steps)}: {title}")
        await _mode_single(session_dir, prompt, agents[agent_idx], title, template, knowledge, step_mode)

async def _mode_single(session_dir: Path, prompt: str, agent_pkg: dict, title: str, template_name: str, knowledge: KnowledgeIndex, mode: str):
    agent = agent_pkg["instance"]

    # Use PromptBuilder for structured output
    builder = PromptBuilder(max_tokens=MODE_REGISTRY.get_setting("max_tokens", 6000))

    # 1. Load domain rules from registry (lazy loading)
    namespaces = MODE_REGISTRY.get_knowledge_namespaces(mode)
    for namespace in namespaces:
        files = MODE_REGISTRY.get_knowledge_files(mode, namespace)
        if files:
            # Use lazy loading from BaseAgent
            rules = agent._load_knowledge(namespace, files)
            builder.add_system(rules)

    # 2. Add persona
    builder.add_role(agent.role_content)

    # 3. Add context (structured with tags)
    builder.add_context(await _inject_context(session_dir, prompt))

    # 4. Add template as guidance (moved to protected constraints to prevent truncation)
    builder.add_constraint(f"GUIDANCE TEMPLATE:\n{_load_template(template_name)}")

    # 5. Add specific task
    schema_name = MODE_REGISTRY.get_schema(mode)
    schema_instruction = ""
    if schema_name and schema_name in SCHEMA_MAP:
        schema_cls = SCHEMA_MAP[schema_name]
        schema_instruction = (
            f"\n\nCRITICAL DIRECTIVE: Regardless of any output format specified in your role description or persona, "
            f"you MUST return ONLY raw JSON matching the following schema. Do NOT include any markdown text outside the JSON. "
            f"Do NOT output headings, bullet points, or markdown formatting outside the JSON structure. Output ONLY valid JSON:\n"
            f"{json.dumps(schema_cls.model_json_schema(), indent=2)}"
        )
    builder.add_task(prompt + schema_instruction)

    full = builder.build()

    _sep(f"{agent_pkg['cfg']['id']} [{agent.role_name}] — {title}")
    raw_output = await _call_agent_with_retry(agent, full, session_dir, timeout=TIMEOUT)

    # Validate against schema if applicable (from registry)
    if schema_name and schema_name in SCHEMA_MAP:
        try:
            schema_cls = SCHEMA_MAP[schema_name]
            clean_json = _extract_json(raw_output)
            validated = schema_cls.model_validate_json(clean_json)
            output = validated.model_dump_json(indent=2)
            print(f"✅ Schema validation passed ({schema_name})")
        except ValidationError as e:
            print(f"❌ Schema validation failed ({schema_name}):")
            print(f"   {e}")
            print(f"\nRaw output:\n{raw_output[:500]}...")
            return  # HALT on invalid output
    else:
        output = raw_output

    print(output)
    _write_atomic(session_dir / f"{agent_pkg['cfg']['id']}_last.md", output)
    _append_context(session_dir, f"{agent_pkg['cfg']['id']} [{agent.role_name}] {title}", output)

async def _mode_review(session_dir: Path, prompt: str, agents: list[dict], knowledge: KnowledgeIndex):
    # Agent 1 (Arch)
    await _mode_single(session_dir, prompt, agents[0], "Architecture Review", "arch_review.md", knowledge, "arch")
    
    # Agent 2 (Code) if exists
    if len(agents) > 1:
        await _mode_single(session_dir, prompt, agents[1], "Code Review", "code_review.md", knowledge, "code")

async def _mode_cross(session_dir: Path, prompt: str, agents: list[dict], knowledge: KnowledgeIndex, mode: str = "review_debate"):
    if len(agents) < 2:
        print("[!] Cross mode requires at least 2 agents.")
        return

    # ── P0 FIX: Freeze context BEFORE Pass 1 loop ────────────────────────
    # Snapshot current context so all agents receive identical baseline.
    # This guarantees true independence — no agent sees another's Pass 1 output.
    frozen_context = await _inject_context(session_dir, prompt)

    # ── Pass 1 — Independent reviews with frozen context ─────────────────
    summaries = []
    results = []
    for i, pkg in enumerate(agents):
        agent = pkg["instance"]
        builder = PromptBuilder(max_tokens=6000)

        # P1 FIX: Use lazy knowledge loading via mode registry instead of greedy
        mode_namespaces = MODE_REGISTRY.get_knowledge_namespaces("review_debate")
        if mode_namespaces:
            for ns in mode_namespaces:
                files = MODE_REGISTRY.get_knowledge_files("review_debate", ns)
                if files:
                    rules = agent._load_knowledge(ns, files)
                else:
                    rules = agent._load_knowledge(ns)
                if rules:
                    builder.add_system(rules)
        else:
            # Fallback: load rules based on agent role (greedy, but only if registry has no config)
            rules = knowledge.get_rules(pkg["cfg"]["role"])
            if rules:
                builder.add_system(rules)

        builder.add_role(agent.role_content)
        builder.add_context(frozen_context)  # P0 FIX: Use frozen snapshot

        # Select template based on agent role, not hardcoded index
        role_prefix = pkg["cfg"]["role"].split("/")[0]
        if role_prefix == "se":
            tmpl_name = "arch_review.md"
        elif role_prefix == "qa":
            tmpl_name = "qa_audit.md"
        else:
            tmpl_name = "code_review.md"
        # Moved guidance template to protected constraints to prevent context truncation
        builder.add_constraint(f"GUIDANCE TEMPLATE:\n{_load_template(tmpl_name)}")

        # Task with forced summary constraint
        task_plus = f"{prompt}\n\nIMPORTANT: End your review with a structured summary tagged with <review_summary> containing 3 key bullet points."
        builder.add_task(task_plus)

        _sep(f"Pass 1 — {pkg['cfg']['id']} [{agent.role_name}]")
        out = await _call_agent_with_retry(agent, builder.build(), session_dir, timeout=TIMEOUT)
        print(out)
        results.append(out)

        # Extract summary (naive fallback if tag missing)
        summary = out
        if "<review_summary>" in out and "</review_summary>" in out:
            summary = out.split("<review_summary>")[1].split("</review_summary>")[0].strip()
        summaries.append(summary)

        _write_atomic(session_dir / f"{pkg['cfg']['id']}_last.md", out)

    # P0 FIX: Batch-append ALL Pass 1 outputs AFTER the loop completes
    for i, pkg in enumerate(agents):
        _append_context(session_dir, f"{pkg['cfg']['id']} Pass 1", results[i])

    # ── Pass 2 — Round-robin cross-examination (supports N agents) ───────
    debates = {}  # {agent_id: debate_response}
    for i, pkg in enumerate(agents):
        # Each agent challenges all OTHER agents' summaries
        other_summaries = []
        for j, other_pkg in enumerate(agents):
            if i == j:
                continue
            other_summaries.append(
                f"<other_summary agent='{other_pkg['cfg']['id']}'>\n{summaries[j]}\n</other_summary>"
            )

        challenge_prompt = (
            f"The following reviewer(s) summarized their findings:\n"
            f"{''.join(other_summaries)}\n\n"
            f"Do you agree or disagree with their assessments? "
            f"Challenge assumptions, identify missing concerns, and highlight areas of agreement. Max 200 words."
        )

        _sep(f"Pass 2 — {pkg['cfg']['id']} cross-examining")
        response = await _call_agent_with_retry(pkg["instance"], challenge_prompt, session_dir, timeout=TIMEOUT)
        print(f"\n{pkg['cfg']['id']} response:\n{response}")

        debates[pkg['cfg']['id']] = response
        _write_atomic(session_dir / f"{pkg['cfg']['id']}_pass2.md", response)
        _append_context(session_dir, f"{pkg['cfg']['id']} Pass 2 (cross)", response)

    # ── Synthesis by lead agent ───────────────────────────────────────────
    _sep("Synthesis")

    summary_block = "\n".join(
        f"- {agents[i]['cfg']['id']}: {summaries[i]}" for i in range(len(agents))
    )
    debate_block = "\n".join(
        f"- {aid}: {resp}" for aid, resp in debates.items()
    )

    schema_name = MODE_REGISTRY.get_schema(mode)
    schema_instruction = ""
    if schema_name and schema_name in SCHEMA_MAP:
        schema_cls = SCHEMA_MAP[schema_name]
        schema_instruction = (
            f"\n\nCRITICAL DIRECTIVE: Regardless of any output format specified in your role description or persona, "
            f"you MUST return ONLY raw JSON matching the following schema. Do NOT include any markdown text outside the JSON. "
            f"Do NOT output headings, bullet points, or markdown formatting outside the JSON structure. Output ONLY valid JSON:\n"
            f"{json.dumps(schema_cls.model_json_schema(), indent=2)}"
        )

    syn_prompt = (
        "Synthesize this panel review into a structured, highly actionable synthesis.\n"
        "Provide 3 actionable conclusions. For each conclusion include:\n"
        "- decision: what to do\n"
        "- rationale: why\n"
        "- implementation_steps: concrete steps\n\n"
        f"Agent Summaries:\n{summary_block}\n\n"
        f"Cross-Examination Debate:\n{debate_block}"
        f"{schema_instruction}"
    )
    syn = await _call_agent_with_retry(agents[0]["instance"], syn_prompt, session_dir, timeout=TIMEOUT)
    
    # Validate against schema if applicable (from registry)
    if schema_name and schema_name in SCHEMA_MAP:
        try:
            schema_cls = SCHEMA_MAP[schema_name]
            clean_json = _extract_json(syn)
            validated = schema_cls.model_validate_json(clean_json)
            output = validated.model_dump_json(indent=2)
            print(f"✅ Debate synthesis schema validation passed ({schema_name})")
        except ValidationError as e:
            print(f"❌ Debate synthesis schema validation failed ({schema_name}):")
            print(f"   {e}")
            print(f"\nRaw synthesis output:\n{syn[:500]}...")
            return  # HALT on invalid output
        except json.JSONDecodeError as e:
            print(f"❌ JSON Decode Error ({schema_name}):")
            print(f"   {e}")
            print(f"\nRaw synthesis output:\n{syn[:500]}...")
            return
    else:
        output = syn

    print(output)
    _write_atomic(session_dir / "synthesis.md", output)
    _append_context(session_dir, "Synthesis", output)
    print(f"\n[✓] Synthesis saved: {session_dir / 'synthesis.md'}")

# ── CLI Interface ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="LND Studio Developer Orchestrator")
    p.add_argument("--task", required=True)
    p.add_argument("--mode", default="review")
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
