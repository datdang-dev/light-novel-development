#!/usr/bin/env python3
"""
LND Studio Rule Injector
=========================
JIT (Just-In-Time) rule loading for pipeline steps.
Instead of loading ALL 22 rule files, only inject rules relevant to the current step.

This is Layer 3 of the 4-Layer Rule Enforcement Architecture.

Usage:
    python rule_injector.py <step_id>
    python rule_injector.py forensic-analysis
    python rule_injector.py prose-generation
    python rule_injector.py quality-audit

Output:
    Concatenated markdown content to stdout (pipe to context payload)
"""

import argparse
import sys
from pathlib import Path

# ─── Resolve paths ───────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
STUDIO_ROOT = SCRIPT_DIR.parent
RULES_DIR = STUDIO_ROOT / "rules"
BOOT_DIR = STUDIO_ROOT / "boot"
KNOWLEDGE_DIR = STUDIO_ROOT / "knowledge"


# ═══════════════════════════════════════════════════════════════════
# STEP → RULES MAPPING
# ═══════════════════════════════════════════════════════════════════

# Each step gets ONLY the rules it needs, not all 22 files
STEP_RULES: dict[str, list[str]] = {
    # Step 2: Forensic Analysis (Kana)
    "forensic-analysis": [
        "rules/visual_forensics.md",
        "rules/one_page_one_file.md",
        "rules/naming_conventions.md",
    ],

    # Step 3: Context Loading
    "context-loading": [
        "rules/continuity.md",
        "rules/scene_boundaries.md",
    ],

    # Step 4: Prose Generation (Suki)
    "prose-generation": [
        "rules/lewd_writing_mechanics.md",
        "rules/sensory_density.md",
        "rules/anti_slop.md",
        "rules/prose_structure.md",
        "rules/dialogue_format.md",
        "rules/character_voice.md",
        "rules/continuity.md",
    ],

    # Step 5: Quality Audit (Riko)
    "quality-audit": [
        "rules/anti_slop.md",
        "rules/pervert_pov.md",
        "rules/sensory_density.md",
        "rules/continuity.md",
    ],

    # Character building (Aria)
    "character-building": [
        "rules/character_voice.md",
        "rules/naming_conventions.md",
    ],

    # Dialogue scripting (Miki)
    "dialogue-scripting": [
        "rules/dialogue_format.md",
        "rules/character_voice.md",
        "rules/rp_sfx_registry.md",
    ],

    # World building (Luna)
    "world-building": [
        "rules/environmental_atmosphere.md",
        "rules/scene_boundaries.md",
        "rules/continuity.md",
    ],

    # Roleplay
    "roleplay": [
        "rules/rp_novel_format.md",
        "rules/rp_sfx_registry.md",
        "rules/dialogue_format.md",
        "rules/character_voice.md",
    ],
}

# Knowledge packs loaded conditionally based on scene tags
SCENE_TAG_KNOWLEDGE: dict[str, list[str]] = {
    "explicit": [
        "knowledge/packs/arousal_architecture.md",
        "knowledge/packs/r18_sensory_pack.md",
    ],
    "intimate": [
        "knowledge/packs/arousal_architecture.md",
    ],
    "bedroom": [
        "knowledge/packs/arousal_architecture.md",
        "knowledge/packs/narrative_style_pack.md",
    ],
    "fetish": [
        "knowledge/packs/fetish_guidance_pack.md",
    ],
    "roleplay": [
        "knowledge/packs/roleplay_st_pack.md",
    ],
}


# ═══════════════════════════════════════════════════════════════════
# CORE FUNCTIONS
# ═══════════════════════════════════════════════════════════════════

def get_canon_preamble() -> str:
    """Always-injected canon preamble (Layer 1)."""
    canon_path = BOOT_DIR / "canon-preamble.md"
    if canon_path.exists():
        return canon_path.read_text(encoding="utf-8")
    return "⚠️ canon-preamble.md not found!"


def get_step_rules(step_id: str) -> str:
    """Get concatenated rules for a specific step (Layer 3)."""
    rules = STEP_RULES.get(step_id)
    if rules is None:
        available = ", ".join(sorted(STEP_RULES.keys()))
        return f"⚠️ Unknown step: '{step_id}'. Available: {available}"

    sections = []
    for rule_path in rules:
        full_path = STUDIO_ROOT / rule_path
        if full_path.exists():
            content = full_path.read_text(encoding="utf-8")
            sections.append(f"<!-- RULE: {rule_path} -->\n{content}")
        else:
            sections.append(f"<!-- ⚠️ MISSING: {rule_path} -->")

    return "\n\n---\n\n".join(sections)


def get_scene_knowledge(scene_tags: list[str]) -> str:
    """Get knowledge packs based on scene tags."""
    loaded_paths: set[str] = set()
    sections = []

    for tag in scene_tags:
        paths = SCENE_TAG_KNOWLEDGE.get(tag, [])
        for p in paths:
            if p not in loaded_paths:
                loaded_paths.add(p)
                full_path = STUDIO_ROOT / p
                if full_path.exists():
                    content = full_path.read_text(encoding="utf-8")
                    sections.append(f"<!-- KNOWLEDGE: {p} -->\n{content}")

    return "\n\n---\n\n".join(sections) if sections else ""


def build_context_payload(
    step_id: str,
    scene_tags: list[str] | None = None,
    include_canon: bool = True,
) -> str:
    """Build the complete context payload for a pipeline step."""
    parts = []

    # Layer 1: Canon preamble (always)
    if include_canon:
        parts.append("<!-- === CANON PREAMBLE (ALWAYS LOADED) === -->")
        parts.append(get_canon_preamble())

    # Layer 3: Step-specific rules
    parts.append(f"<!-- === STEP RULES: {step_id} === -->")
    parts.append(get_step_rules(step_id))

    # Scene-tag knowledge (conditional)
    if scene_tags:
        knowledge = get_scene_knowledge(scene_tags)
        if knowledge:
            parts.append(f"<!-- === SCENE KNOWLEDGE: {', '.join(scene_tags)} === -->")
            parts.append(knowledge)

    return "\n\n".join(parts)


def estimate_tokens(text: str) -> int:
    """Rough token estimate (1 token ≈ 4 chars for mixed Vietnamese/English)."""
    return len(text) // 4


# ═══════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="LND Studio Rule Injector")
    parser.add_argument("step_id", help="Pipeline step ID")
    parser.add_argument("--scene-tags", nargs="*", default=[], help="Scene tags for knowledge loading")
    parser.add_argument("--no-canon", action="store_true", help="Skip canon preamble")
    parser.add_argument("--estimate", action="store_true", help="Show token estimate instead of content")
    parser.add_argument("--list-steps", action="store_true", help="List available step IDs")

    args = parser.parse_args()

    if args.list_steps:
        print("Available pipeline steps:")
        for step_id, rules in sorted(STEP_RULES.items()):
            rule_names = [Path(r).stem for r in rules]
            print(f"  {step_id}: {', '.join(rule_names)}")
        return

    payload = build_context_payload(
        step_id=args.step_id,
        scene_tags=args.scene_tags,
        include_canon=not args.no_canon,
    )

    if args.estimate:
        tokens = estimate_tokens(payload)
        print(f"Step: {args.step_id}")
        print(f"Scene tags: {args.scene_tags or 'none'}")
        print(f"Estimated tokens: ~{tokens}")
        print(f"Canon included: {not args.no_canon}")
    else:
        print(payload)


if __name__ == "__main__":
    main()
