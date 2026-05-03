#!/usr/bin/env python3
"""
SillyTavern Card Quality Validator
================================
Validates a ST V3 JSON card for roleplay quality.
Checks if the AI model will understand context and respond as intended.
"""

import json
import re
import sys
from pathlib import Path


def validate_card(card_path: str) -> dict:
    """Run all validation checks on a ST card."""
    with open(card_path, 'r', encoding='utf-8') as f:
        card = json.load(f)

    results = {
        "passed": [],
        "warnings": [],
        "errors": []
    }

    # 1. Core Fields
    data = card.get('data', card)

    if not data.get('name') or data['name'] == 'Character Name':
        results["errors"].append("name is missing or placeholder")
    else:
        results["passed"].append("name is set")

    if not data.get('description'):
        results["errors"].append("description is empty")
    elif len(data['description']) > 4000:
        results["warnings"].append("description > 4000 chars (reduce for local models)")
    else:
        results["passed"].append("description is valid length")

    if not data.get('first_mes'):
        results["warnings"].append("first_mes is empty")
    else:
        results["passed"].append("first_mes is set")

    # 2. Token Replacement
    char_name = data.get('name', '')
    desc = data.get('description', '')

    if char_name and char_name != 'Character Name':
        # Check if name appears without {{char}}
        pattern = rf'\b{re.escape(char_name)}\b(?!}})'
        if re.search(pattern, desc):
            results["warnings"].append(f"name '{char_name}' appears without {{char}} in description")

    # Check {{char}} usage
    if '{{char}}' not in desc and char_name not in ['Character Name', '']:
        results["warnings"].append("description doesn't use {{char}} macro")

    # Check {{user}} in scenario
    scenario = data.get('scenario', '')
    if '{{user}}' not in scenario:
        results["warnings"].append("scenario doesn't use {{user}} macro")

    # 3. Example Dialogues
    mes_example = data.get('mes_example', '')
    if mes_example:
        if '<START>' not in mes_example:
            results["warnings"].append("mes_example missing <START> blocks")
        if '{{char}}' not in mes_example:
            results["warnings"].append("mes_example doesn't use {{char}}")
        if '{{user}}' not in mes_example:
            results["warnings"].append("mes_example doesn't use {{user}}")
        results["passed"].append("mes_example format is valid")
    else:
        results["warnings"].append("mes_example is empty (recommended for style)")

    # 4. First Message Quality
    first_mes = data.get('first_mes', '')
    if first_mes:
        if '{{char}}' in first_mes or '{{user}}' in first_mes:
            results["passed"].append("first_mes uses token macros")
        if '*' in first_mes:
            results["passed"].append("first_mes uses actions (asterisks)")
        # Check for hook (ending with question or prompt)
        if any(marker in first_mes for marker in ['?', '「', '!', '..."', '..."']):
            results["passed"].append("first_mes has hook/dialogue")
    else:
        results["warnings"].append("first_mes is empty")

    # 5. Lorebook Validation
    char_book = data.get('character_book', {})
    entries = char_book.get('entries', [])

    for i, entry in enumerate(entries):
        keys = entry.get('keys', [])
        content = entry.get('content', '')

        if not keys:
            results["warnings"].append(f"lorebook entry {i+1} has no keys")

        if not content:
            results["warnings"].append(f"lorebook entry {i+1} has empty content")

        # Check {{char}} usage in lorebook
        if '{{char}}' not in content and char_name not in ['Character Name', '']:
            results["warnings"].append(f"lorebook entry {i+1} doesn't use {{char}}")

    if entries:
        results["passed"].append(f"lorebook has {len(entries)} entries")
    else:
        results["warnings"].append("lorebook is empty (optional but recommended)")

    # 6. System Prompt Length
    system_prompt = data.get('system_prompt', '')
    if system_prompt and len(system_prompt) > 2000:
        results["warnings"].append("system_prompt > 2000 chars")
    if system_prompt:
        results["passed"].append("system_prompt is set")

    # 7. Personality Field
    personality = data.get('personality', '')
    if personality:
        results["passed"].append("personality field is set")
        # Check for keywords
        keyword_count = len([w for w in personality.split(',') if w.strip()])
        if keyword_count >= 3:
            results["passed"].append(f"personality has {keyword_count} keywords (good)")
        else:
            results["warnings"].append(f"personality has only {keyword_count} keywords (recommend 3+)")
    else:
        results["warnings"].append("personality field is empty (optional but recommended)")

    # 8. Post History Instructions
    post_history = data.get('post_history_instructions', '')
    if post_history:
        results["passed"].append("post_history_instructions is set (high influence)")

    # 9. Alternate Greetings
    alt_greetings = data.get('alternate_greetings', [])
    if alt_greetings:
        results["passed"].append(f"{len(alt_greetings)} alternate greeting(s)")

    # 10. NSFW/R18 specific checks
    tags = data.get('tags', [])
    if any(tag in ['R18', 'NSFW', 'explicit', 'adult'] for tag in tags):
        results["passed"].append("card marked as NSFW/R18")

    # Check for explicit vocabulary in description
    r18_keywords = ['cặc', 'lồn', 'địt', 'đụ', 'chịch', 'tinh', 'vú', 'âm hộ', 'onahole']
    explicit_count = sum(1 for kw in r18_keywords if kw in desc.lower())
    if explicit_count >= 3:
        results["passed"].append(f"description has {explicit_count} explicit terms")
    elif explicit_count > 0:
        results["warnings"].append(f"description has only {explicit_count} explicit terms (R18 card should have more)")

    return results


def print_report(results: dict, card_name: str = ""):
    """Print validation report."""
    print("=" * 60)
    print("SILLYTAVERN CARD VALIDATION REPORT")
    if card_name:
        print(f"Card: {card_name}")
    print("=" * 60)

    if results["errors"]:
        print(f"\n[ERRORS] ({len(results['errors'])}):")
        for e in results["errors"]:
            print(f"  - {e}")

    if results["warnings"]:
        print(f"\n[WARNINGS] ({len(results['warnings'])}):")
        for w in results["warnings"]:
            print(f"  - {w}")

    if results["passed"]:
        print(f"\n[PASSED] ({len(results['passed'])}):")
        for p in results["passed"]:
            print(f"  + {p}")

    print(f"\n{'=' * 60}")
    if not results["errors"] and not results["warnings"]:
        print("[OK] Card is ready for SillyTavern!")
    elif not results["errors"]:
        print("[OK] Card is usable, but fix warnings for better quality.")
    else:
        print("[FAIL] Fix errors before using in roleplay.")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python validate_st_card.py <card.json>")
        print()
        print("Checks:")
        print("  - Core fields (name, description, first_mes)")
        print("  - Token replacement ({{char}}, {{user}})")
        print("  - Example dialogues format")
        print("  - Lorebook entries")
        print("  - System prompt length")
        print("  - NSFW/R18 specific quality")
        sys.exit(1)

    card_path = sys.argv[1]
    results = validate_card(card_path)
    card_name = Path(card_path).name
    print_report(results, card_name)