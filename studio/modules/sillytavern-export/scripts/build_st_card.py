#!/usr/bin/env python3
"""
SillyTavern V3 Character Card Builder
======================================
Converts a structured Markdown file into a SillyTavern V3 JSON character card.

Usage:
    python build_st_card.py <input.md> [output.json]

If output is not specified, it defaults to {name}_v3.json in the current directory.

No external dependencies — uses only Python stdlib.
"""

import json
import re
import sys
import os
import datetime
from pathlib import Path


# ─────────────────────────────────────────────
# YAML Frontmatter Parser (minimal, no PyYAML)
# ─────────────────────────────────────────────

def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Extract YAML frontmatter and body from markdown text."""
    pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(pattern, text, re.DOTALL)
    if not match:
        return {}, text

    yaml_str = match.group(1)
    body = match.group(2)
    meta = parse_simple_yaml(yaml_str)
    return meta, body


def parse_simple_yaml(yaml_str: str) -> dict:
    """
    Minimal YAML parser for frontmatter.
    Handles: key: value, key: [list], key:\\n  - item
    Skips comments (#).
    """
    result = {}
    current_key = None
    current_list = None

    for line in yaml_str.split('\n'):
        stripped = line.strip()

        # Skip comments and empty lines
        if not stripped or stripped.startswith('#'):
            continue

        # List item under a key
        if stripped.startswith('- ') and current_key:
            item = stripped[2:].strip().strip('"').strip("'")
            if current_list is None:
                current_list = []
            current_list.append(item)
            result[current_key] = current_list
            continue

        # Key: value pair
        if ':' in stripped:
            # Close previous list
            current_list = None

            key, _, value = stripped.partition(':')
            key = key.strip()
            value = value.strip()

            if not value:
                # Key with no value — might be followed by list items
                current_key = key
                continue

            # Inline list: [a, b, c]
            if value.startswith('[') and value.endswith(']'):
                items = [i.strip().strip('"').strip("'")
                         for i in value[1:-1].split(',') if i.strip()]
                result[key] = items
            # Boolean
            elif value.lower() in ('true', 'false'):
                result[key] = value.lower() == 'true'
            # Number
            elif re.match(r'^-?\d+(\.\d+)?$', value):
                result[key] = float(value) if '.' in value else int(value)
            # String
            else:
                result[key] = value.strip('"').strip("'")

            current_key = key

    return result


# ─────────────────────────────────────────────
# Markdown Section Parser
# ─────────────────────────────────────────────

def parse_sections(body: str) -> dict[str, str]:
    """
    Split markdown body into sections by ## headers.
    Returns dict of {header_name: content}.
    """
    sections = {}
    current = None
    lines = []

    for line in body.split('\n'):
        h2_match = re.match(r'^##\s+(.+)$', line)
        if h2_match:
            # Save previous section
            if current is not None:
                sections[current] = '\n'.join(lines).strip()
            current = h2_match.group(1).strip()
            lines = []
        else:
            lines.append(line)

    # Save last section
    if current is not None:
        sections[current] = '\n'.join(lines).strip()

    return sections


def strip_comments(text: str) -> str:
    """Remove HTML comments from text."""
    return re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL).strip()


# ─────────────────────────────────────────────
# Lorebook Parser
# ─────────────────────────────────────────────

def parse_lorebook(lorebook_text: str) -> list[dict]:
    """
    Parse ## Lorebook section into character_book entries.
    Each ### subsection is one entry.
    """
    entries = []
    if not lorebook_text:
        return entries

    # Split by ### headers
    parts = re.split(r'^###\s+(.+)$', lorebook_text, flags=re.MULTILINE)

    # parts[0] is text before first ###, then alternating name/content
    i = 1
    entry_id = 1
    while i < len(parts) - 1:
        name = parts[i].strip()
        content_block = parts[i + 1].strip()
        i += 2

        # Parse metadata from content
        keys = []
        secondary_keys = []
        position = "after_char"
        constant = False
        use_regex = False
        sticky = 0
        cooldown = 0
        delay = 0
        selective_logic = 0
        role = 0
        vectorized = False
        automation_id = ""
        triggers = []
        group = ""
        group_weight = 100
        prevent_recursion = False
        delay_until_recursion = False
        content_lines = []

        for line in content_block.split('\n'):
            stripped = line.strip()
            # Strip bold markers for metadata detection
            clean = stripped.replace('**', '')
            clower = clean.lower()
            if clower.startswith('keys:'):
                keys_str = clean.split(':', 1)[1].strip()
                keys = [k.strip() for k in keys_str.split(',') if k.strip()]
            elif clower.startswith('secondary_keys:'):
                sk_str = clean.split(':', 1)[1].strip()
                secondary_keys = [k.strip() for k in sk_str.split(',') if k.strip()]
            elif clower.startswith('position:'):
                position = clean.split(':', 1)[1].strip()
            elif clower.startswith('constant:'):
                const_val = clean.split(':', 1)[1].strip().lower()
                constant = const_val == 'true'
            elif clower.startswith('regex:'):
               use_regex = clean.split(':', 1)[1].strip().lower() == 'true'
            elif clower.startswith('sticky:'):
               val = clean.split(':', 1)[1].strip()
               sticky = int(val) if val else 0
            elif clower.startswith('cooldown:'):
               val = clean.split(':', 1)[1].strip()
               cooldown = int(val) if val else 0
            elif clower.startswith('delay:'):
               val = clean.split(':', 1)[1].strip()
               delay = int(val) if val else 0
            elif clower.startswith('selectivelogic:'):
               val = clean.split(':', 1)[1].strip()
               selective_logic = int(val) if val else 0
            elif clower.startswith('role:'):
               val = clean.split(':', 1)[1].strip()
               role = int(val) if val else 0
            elif clower.startswith('vectorized:'):
               vectorized = clean.split(':', 1)[1].strip().lower() == 'true'
            elif clower.startswith('automation_id:'):
               automation_id = clean.split(':', 1)[1].strip()
            elif clower.startswith('triggers:'):
               tr_str = clean.split(':', 1)[1].strip()
               triggers = [t.strip() for t in tr_str.split(',') if t.strip()]
            elif clower.startswith('group:'):
               group = clean.split(':', 1)[1].strip()
            elif clower.startswith('group_weight:'):
               val = clean.split(':', 1)[1].strip()
               group_weight = int(val) if val else 100
            elif clower.startswith('prevent_recursion:'):
               prevent_recursion = clean.split(':', 1)[1].strip().lower() == 'true'
            elif clower.startswith('delay_until_recursion:'):
               delay_until_recursion = clean.split(':', 1)[1].strip().lower() == 'true'
            else:
                content_lines.append(line)

        entry_content = strip_comments('\n'.join(content_lines).strip())
        if not entry_content and not keys:
            continue

        # Map position string to numeric
        position_num = 1 if position == "after_char" else 0

        entry = {
            "id": entry_id,
            "keys": keys if keys else [name.lower()],
            "secondary_keys": secondary_keys,
            "content": entry_content,
            "comment": name,
            "enabled": True,
            "position": position,
            "use_regex": use_regex,
            "constant": constant,
            "selective": len(secondary_keys) > 0,
            "insertion_order": entry_id * 10,
            "extensions": {
                "position": position_num,
                "exclude_recursion": False,
                "display_index": entry_id - 1 if entry_id - 1 >= 0 else 0,
                "probability": 100,
                "useProbability": True,
                "depth": 4,
                "selectiveLogic": selective_logic,
                "outlet_name": "",
                "group": group,
                "group_override": False,
                "group_weight": group_weight,
                "prevent_recursion": prevent_recursion,
                "delay_until_recursion": delay_until_recursion,
                "scan_depth": None,
                "match_whole_words": None,
                "use_group_scoring": False,
                "case_sensitive": None,
                "automation_id": automation_id,
                "role": role,
                "vectorized": vectorized,
                "sticky": sticky,
                "cooldown": cooldown,
                "delay": delay,
                "match_persona_description": False,
                "match_character_description": False,
                "match_character_personality": False,
                "match_character_depth_prompt": False,
                "match_scenario": False,
                "match_creator_notes": False,
                "triggers": triggers,
                "ignore_budget": False
            }
        }
        entries.append(entry)
        entry_id += 1

    return entries


# ─────────────────────────────────────────────
# Alternate Greetings Parser
# ─────────────────────────────────────────────

def parse_alternate_greetings(text: str) -> list[str]:
    """Split alternate greetings by --- separators."""
    if not text:
        return []
    parts = re.split(r'^---\s*$', text, flags=re.MULTILINE)
    return [strip_comments(p.strip()) for p in parts if p.strip()]


# ─────────────────────────────────────────────
# Card Builder
# ─────────────────────────────────────────────

def build_card(meta: dict, sections: dict) -> dict:
    """Assemble the SillyTavern V3 JSON card."""

    name = meta.get('name', 'Unnamed')
    description = strip_comments(sections.get('Description', ''))
    personality = strip_comments(sections.get('Personality', ''))
    scenario = strip_comments(sections.get('Scenario', ''))
    first_mes = strip_comments(sections.get('First Message', ''))
    mes_example = strip_comments(sections.get('Example Dialogues', ''))
    system_prompt = strip_comments(sections.get('System Prompt', ''))
    post_history = strip_comments(sections.get('Post History Instructions', ''))
    creator_notes = strip_comments(sections.get('Creator Notes', ''))

    # Lorebook
    lorebook_raw = sections.get('Lorebook', '')
    lorebook_entries = parse_lorebook(lorebook_raw)

    # Alternate greetings
    alt_greetings_raw = sections.get('Alternate Greetings', '')
    alt_greetings = parse_alternate_greetings(alt_greetings_raw)

    # Metadata
    tags = meta.get('tags', [])
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(',')]

    talkativeness = str(meta.get('talkativeness', '0.5'))
    fav = meta.get('fav', False)
    creator = meta.get('creator', 'LND Studio')
    version = meta.get('version', '1.0.0')
    create_date = datetime.datetime.now(datetime.timezone.utc).isoformat()

    inner_data = {
        "name": name,
        "description": description,
        "personality": personality,
        "scenario": scenario,
        "first_mes": first_mes,
        "mes_example": mes_example,
        "creator_notes": creator_notes,
        "system_prompt": system_prompt,
        "post_history_instructions": post_history,
        "tags": tags,
        "talkativeness": talkativeness,
        "fav": fav,
        "avatar": "none",
        "alternate_greetings": alt_greetings,
        "group_only_greetings": [],
        "creator": creator,
        "character_version": version,
        "extensions": {
            "talkativeness": talkativeness,
            "fav": fav,
            "world": "",
            "depth_prompt": {
                "prompt": system_prompt,
                "depth": 4,
                "role": "system"
            }
        }
    }

    # Character book (lorebook)
    if lorebook_entries:
        inner_data["character_book"] = {
            "name": f"{name} Lorebook",
            "description": f"Embedded lorebook for {name}",
            "scan_depth": 3000,
            "token_budget": 500,
            "recursive_scanning": True,
            "extensions": {},
            "entries": lorebook_entries
        }

    card = {
        "spec": "chara_card_v3",
        "spec_version": "3.0",
        "data": inner_data,
        "fav": fav,
        "name": name,
        "description": description,
        "personality": personality,
        "scenario": scenario,
        "first_mes": first_mes,
        "mes_example": mes_example,
        "talkativeness": talkativeness,
        "tags": tags,
        "create_date": create_date.replace("+00:00", "Z"),
        "creatorcomment": creator_notes,
        "avatar": "none",
    }

    return card


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Usage: python build_st_card.py <input.md> [output.json]")
        print()
        print("Examples:")
        print("  python build_st_card.py rin_card.md")
        print("  python build_st_card.py rin_card.md ./output/rin_v3.json")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"Error: File not found: {input_path}")
        sys.exit(1)

    # Read input
    text = input_path.read_text(encoding='utf-8')

    # Parse
    meta, body = parse_frontmatter(text)
    sections = parse_sections(body)

    # Validate
    name = meta.get('name', '')
    if not name or name == 'Character Name':
        print("Warning: 'name' in frontmatter is missing or still the placeholder!")

    if not sections.get('Description'):
        print("Warning: ## Description section is empty!")

    if not sections.get('First Message'):
        print("Warning: ## First Message section is empty!")

    # Build
    card = build_card(meta, sections)

    # Output path
    if len(sys.argv) >= 3:
        output_path = Path(sys.argv[2])
    else:
        safe_name = re.sub(r'[^\w\-]', '_', name.lower().strip())
        output_path = Path(f"{safe_name}_v3.json")

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write
    output_path.write_text(
        json.dumps(card, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )

    # Summary
    section_names = list(sections.keys())
    data = card.get('data', {})
    lorebook_count = len(data.get('character_book', {}).get('entries', []))
    alt_count = len(data.get('alternate_greetings', []))

    print(f"✅ Built: {output_path}")
    print(f"   Name: {card['name']}")
    print(f"   Sections: {', '.join(section_names)}")
    print(f"   Lorebook entries: {lorebook_count}")
    print(f"   Alternate greetings: {alt_count}")
    print(f"   Tags: {', '.join(card['tags'])}")


if __name__ == '__main__':
    main()
