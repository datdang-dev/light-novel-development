#!/usr/bin/env python3
"""
Schema-Driven Auto-Repair (Optimization #5)
Validates LLM-generated JSON outputs against studio schemas and auto-fixes
trivial structural errors BEFORE sending to Riko for content audit.

Usage:
    python3 auto_repair.py <json_file> <schema_file>

Exit codes:
    0 = Valid (or repaired successfully)
    1 = Unfixable structural error (needs LLM re-generation)
"""

import json
import sys
import os
from pathlib import Path

STUDIO_ROOT = Path(__file__).parent.parent

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def load_schema(schema_path):
    return load_json(schema_path)

def get_required_fields(schema):
    """Extract required fields and their defaults from a schema."""
    required = schema.get('required', [])
    properties = schema.get('properties', {})
    return required, properties

def auto_repair(data, schema, path="root"):
    """Recursively validate and repair JSON data against a schema."""
    repairs = []
    required, properties = get_required_fields(schema)

    # Fix 1: Add missing required fields with sensible defaults
    for field in required:
        if field not in data:
            field_schema = properties.get(field, {})
            field_type = field_schema.get('type', 'string')
            default = {
                'string': '',
                'number': 0,
                'integer': 0,
                'boolean': False,
                'array': [],
                'object': {}
            }.get(field_type, None)
            data[field] = default
            repairs.append(f"[AUTO-FIX] Added missing field '{path}.{field}' with default {default}")

    # Fix 2: Recalculate word_count if present but wrong.
    # Draft prose payloads store the body under `prose_content`.
    if 'word_count' in data and 'prose_content' in data:
        actual_count = len(str(data['prose_content']).split())
        if data['word_count'] != actual_count:
            repairs.append(f"[AUTO-FIX] Corrected word_count: {data['word_count']} -> {actual_count}")
            data['word_count'] = actual_count

    # Fix 3: Ensure boolean fields are actually booleans
    for field, field_schema in properties.items():
        if field in data and field_schema.get('type') == 'boolean':
            if not isinstance(data[field], bool):
                old_val = data[field]
                data[field] = bool(data[field])
                repairs.append(f"[AUTO-FIX] Cast '{path}.{field}' to boolean: {old_val} -> {data[field]}")

    # Fix 4: Recurse into nested objects
    for field, field_schema in properties.items():
        if field in data and field_schema.get('type') == 'object' and isinstance(data[field], dict):
            nested_repairs = auto_repair(data[field], field_schema, f"{path}.{field}")
            repairs.extend(nested_repairs)

    # Fix 5: Recurse into arrays of objects
    for field, field_schema in properties.items():
        if field in data and field_schema.get('type') == 'array' and isinstance(data[field], list):
            items_schema = field_schema.get('items', {})
            if items_schema.get('type') == 'object':
                for i, item in enumerate(data[field]):
                    if isinstance(item, dict):
                        nested_repairs = auto_repair(item, items_schema, f"{path}.{field}[{i}]")
                        repairs.extend(nested_repairs)

    return repairs

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 auto_repair.py <json_file> <schema_file>")
        sys.exit(1)

    json_path = sys.argv[1]
    schema_path = sys.argv[2]

    if not os.path.exists(json_path):
        print(f"❌ File not found: {json_path}")
        sys.exit(1)

    if not os.path.exists(schema_path):
        print(f"❌ Schema not found: {schema_path}")
        sys.exit(1)

    print(f"🔧 Auto-Repair Engine v1.0")
    print(f"📄 Input:  {json_path}")
    print(f"📐 Schema: {schema_path}")
    print()

    try:
        data = load_json(json_path)
        schema = load_schema(schema_path)
    except json.JSONDecodeError as e:
        print(f"❌ UNFIXABLE: JSON parse error - {e}")
        print("   → Needs LLM re-generation")
        sys.exit(1)

    repairs = auto_repair(data, schema)

    if repairs:
        print(f"🔧 Applied {len(repairs)} auto-repairs:")
        for r in repairs:
            print(f"   {r}")
        save_json(json_path, data)
        print(f"\n✅ Repaired file saved: {json_path}")
    else:
        print("✅ No repairs needed - JSON is structurally valid.")

    sys.exit(0)

if __name__ == "__main__":
    main()
