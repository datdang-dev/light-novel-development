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
import hashlib
from pathlib import Path

# ─── Resolve paths ───────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
STUDIO_ROOT = SCRIPT_DIR.parent
RULES_DIR = STUDIO_ROOT / "rules"
BOOT_DIR = RULES_DIR
KNOWLEDGE_DIR = STUDIO_ROOT / "knowledge"
CACHE_DIR = STUDIO_ROOT / ".context_cache"



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


def get_static_hash(step_id: str, include_canon: bool) -> str:
    """Compute hash of the static rules configuration and their content modification times."""
    hasher = hashlib.sha256()
    hasher.update(step_id.encode('utf-8'))
    hasher.update(str(include_canon).encode('utf-8'))
    
    paths = []
    if include_canon:
        paths.append(BOOT_DIR / "canon-preamble.md")
    rules = STEP_RULES.get(step_id, [])
    for r in rules:
        paths.append(STUDIO_ROOT / r)
        
    for p in paths:
        if p.exists():
            hasher.update(p.name.encode('utf-8'))
            hasher.update(str(p.stat().st_mtime).encode('utf-8'))
    return hasher.hexdigest()[:16]


def build_context_payload(
    step_id: str,
    scene_tags: list[str] | None = None,
    include_canon: bool = True,
) -> str:
    """Build the complete context payload for a pipeline step with file-based caching."""
    # Ensure cache directory exists
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. Check/Build cache for Static Layer (Canon + Step rules)
    static_hash = get_static_hash(step_id, include_canon)
    cache_file = CACHE_DIR / f"{step_id}_static_{static_hash}.md"
    
    if cache_file.exists():
        static_content = cache_file.read_text(encoding="utf-8")
    else:
        # Compile static layers
        parts = []
        if include_canon:
            parts.append("<!-- === CANON PREAMBLE (ALWAYS LOADED) === -->")
            parts.append(get_canon_preamble())
            
        parts.append(f"<!-- === STEP RULES: {step_id} === -->")
        parts.append(get_step_rules(step_id))
        
        static_content = "\n\n".join(parts)
        
        # Clean up older cache files for this step_id
        for old_file in CACHE_DIR.glob(f"{step_id}_static_*.md"):
            try:
                old_file.unlink()
            except OSError:
                pass
                
        # Write to cache
        cache_file.write_text(static_content, encoding="utf-8")

    # 2. Add Dynamic/Conditional Scene Knowledge
    parts = [static_content]
    if scene_tags:
        # Dynamic scene tags can also be hashed/cached
        sorted_tags = sorted(scene_tags)
        tags_str = "_".join(sorted_tags)
        # Compute dynamic knowledge paths to hash
        knowledge_paths = []
        for tag in sorted_tags:
            for p in SCENE_TAG_KNOWLEDGE.get(tag, []):
                knowledge_paths.append(STUDIO_ROOT / p)
                
        k_hasher = hashlib.sha256()
        k_hasher.update(tags_str.encode('utf-8'))
        for kp in knowledge_paths:
            if kp.exists():
                k_hasher.update(kp.name.encode('utf-8'))
                k_hasher.update(str(kp.stat().st_mtime).encode('utf-8'))
        knowledge_hash = k_hasher.hexdigest()[:16]
        
        k_cache_file = CACHE_DIR / f"knowledge_{tags_str}_{knowledge_hash}.md"
        
        if k_cache_file.exists():
            knowledge_content = k_cache_file.read_text(encoding="utf-8")
        else:
            knowledge_content = get_scene_knowledge(scene_tags)
            # Clean up old knowledge caches for these tags
            for old_file in CACHE_DIR.glob(f"knowledge_{tags_str}_*.md"):
                try:
                    old_file.unlink()
                except OSError:
                    pass
            if knowledge_content:
                k_cache_file.write_text(knowledge_content, encoding="utf-8")
                
        if knowledge_content:
            parts.append(f"<!-- === SCENE KNOWLEDGE: {', '.join(scene_tags)} === -->")
            parts.append(knowledge_content)

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
