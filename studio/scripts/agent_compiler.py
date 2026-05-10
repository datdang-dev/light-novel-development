#!/usr/bin/env python3
"""
LND Studio - Agent Context Compiler
====================================
Parses an Agent YAML file to extract persona details and critical actions,
resolves any referenced knowledge/markdown files within the actions, and
combines them with the JIT rules from `rule_injector.py`.

This bridges the gap between Cloud Orchestration (where LLMs read files themselves)
and Local Headless Execution (where we need to feed a massive pre-compiled prompt).
"""

import argparse
import yaml
import re
import sys
from pathlib import Path

# Add current dir to sys.path to import rule_injector
SCRIPT_DIR = Path(__file__).parent
sys.path.append(str(SCRIPT_DIR))

try:
    from rule_injector import build_context_payload
except ImportError:
    print("❌ Error: Could not import rule_injector.py. Ensure you are running from the correct directory.", file=sys.stderr)
    sys.exit(1)

STUDIO_ROOT = SCRIPT_DIR.parent
PROJECT_ROOT = STUDIO_ROOT.parent


def load_yaml(path: Path) -> dict:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"❌ Error loading YAML {path}: {e}", file=sys.stderr)
        sys.exit(1)


def extract_file_paths(text: str) -> list[str]:
    """Extract file paths from placeholders like {{project_root}}/path/to/file.md or (path/to/file.md)."""
    matches1 = re.findall(r'\{\{project_root\}\}/([a-zA-Z0-9_/\.\-]+)', text)
    matches2 = re.findall(r'\((studio/[a-zA-Z0-9_/\.\-]+)\)', text)
    return list(set(matches1 + matches2))


def compile_agent_context(agent_yaml_path: Path, step_id: str, scene_tags: list[str]) -> str:
    data = load_yaml(agent_yaml_path)
    agent = data.get('agent', {})
    persona = agent.get('persona', {})
    actions = agent.get('critical_actions', [])

    parts = []
    
    # 1. PERSONA INJECTION
    parts.append("=========================================")
    parts.append("=== AGENT PERSONA (WHO YOU ARE)       ===")
    parts.append("=========================================")
    parts.append(f"ROLE:\n{persona.get('role', '').strip()}")
    parts.append(f"\nIDENTITY:\n{persona.get('identity', '').strip()}")
    parts.append(f"\nCOMMUNICATION STYLE:\n{persona.get('communication_style', '').strip()}")
    
    principles = persona.get('principles', [])
    if principles:
        parts.append("\nCORE PRINCIPLES:")
        for p in principles:
            parts.append(f"- {p}")

    # 2. CRITICAL ACTIONS & REFERENCED KNOWLEDGE
    parts.append("\n=========================================")
    parts.append("=== CRITICAL ACTIONS & KNOWLEDGE      ===")
    parts.append("=========================================")
    
    referenced_files = set()
    for action in actions:
        parts.append(f"- {action}")
        referenced_files.update(extract_file_paths(action))
    
    # Load all referenced markdown files dynamically
    for ref in referenced_files:
        full_path = PROJECT_ROOT / ref
        if full_path.exists() and full_path.is_file():
            content = full_path.read_text(encoding='utf-8')
            parts.append(f"\n<!-- 📖 LOADED FROM: {ref} -->\n{content}")
        elif full_path.is_dir():
             parts.append(f"\n<!-- 📁 REFERENCED DIRECTORY: {ref} (Skipping content read) -->")
        else:
            parts.append(f"\n<!-- ⚠️ WARNING: Missing referenced file {ref} -->")

    # 3. JIT RULES (Layer 1 + Layer 3)
    parts.append("\n=========================================")
    parts.append(f"=== JIT INJECTED RULES: {step_id} ===")
    parts.append("=========================================")
    jit_payload = build_context_payload(step_id, scene_tags, include_canon=True)
    parts.append(jit_payload)

    return "\n".join(parts)


def main():
    parser = argparse.ArgumentParser(description="LND Studio Agent Context Compiler")
    parser.add_argument("agent_file", help="Path to the agent YAML file")
    parser.add_argument("step_id", help="Pipeline step ID for rule injection (e.g. prose-generation)")
    parser.add_argument("--scene-tags", nargs="*", default=[], help="Scene tags (e.g. explicit, bedroom)")
    
    args = parser.parse_args()
    yaml_path = Path(args.agent_file)
    
    if not yaml_path.exists():
        print(f"❌ Error: Agent file not found at {yaml_path}", file=sys.stderr)
        sys.exit(1)
        
    compiled_prompt = compile_agent_context(yaml_path, args.step_id, args.scene_tags)
    print(compiled_prompt)


if __name__ == "__main__":
    main()
