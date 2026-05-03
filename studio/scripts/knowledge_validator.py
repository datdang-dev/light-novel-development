#!/usr/bin/env python3
"""
Knowledge Architecture Validator v2.0
=====================================
Phát hiện:
  1. Orphan files: file tồn tại nhưng KHÔNG có trong knowledge-index.yaml
  2. Unused entries: có trong index nhưng file không tồn tại
  3. Missing triggers: SKILL.md có scene_tag nhưng không có knowledge load tương ứng
  4. Broken wiring: index nói "used_by: [lewd-writer]" nhưng lewd-writer/SKILL.md
     không reference file đó

Usage:
  python3 studio/scripts/knowledge_validator.py
  python3 studio/scripts/knowledge_validator.py --fix    # generate fix suggestions
  python3 studio/scripts/knowledge_validator.py --dot   # output dependency graph
"""
import os, re, json, sys, yaml
from pathlib import Path

PROJECT_ROOT = os.getenv('PROJECT_ROOT') or '/home/datdang/working/lnd_dev'
KNOWLEDGE_ROOT = Path(PROJECT_ROOT) / 'studio' / 'knowledge'
INDEX_FILE = KNOWLEDGE_ROOT / 'knowledge-index.yaml'

# ── 1. Load knowledge-index.yaml ──────────────────────────────────────────────
def load_index():
    if not INDEX_FILE.exists():
        return {'index': [], 'scene_tags': {}, 'metadata': {}}
    with open(INDEX_FILE, encoding='utf-8') as f:
        raw = yaml.safe_load(f)
    # Normalize entries: some may be commented out with #
    entries = []
    for item in raw.get('index', []):
        if isinstance(item, dict) and 'file' in item:
            entries.append(item)
    return {
        'index': entries,
        'scene_tags': raw.get('scene_tags', {}),
        'metadata': raw.get('metadata', {}),
    }

# ── 2. List all physical knowledge files ──────────────────────────────────────
def list_knowledge_files():
    exts = {'.md', '.yaml', '.yml', '.json', '.txt'}
    files = []
    for p in KNOWLEDGE_ROOT.rglob('*'):
        if p.is_file() and not p.name.startswith('.') and p.suffix in exts:
            rel = p.relative_to(PROJECT_ROOT).as_posix()
            # Skip the index itself
            if rel != 'studio/knowledge/knowledge-index.yaml':
                files.append(rel)
    return sorted(files)

# ── 3. List all SKILL.md and agent YAML files ─────────────────────────────────
def list_skill_files():
    studio = Path(PROJECT_ROOT) / 'studio'
    files = []
    for p in studio.rglob('*'):
        if p.is_file() and (p.suffix == '.SKILL.md' or
                            (p.suffix == '.yaml' and 'agents' in p.as_posix())):
            files.append(p.relative_to(PROJECT_ROOT).as_posix())
    return sorted(files)

# ── 4. Extract referenced knowledge files from a SKILL/YAML file ───────────────
def extract_references_from_file(filepath):
    """Return set of knowledge paths (rel) referenced in this file."""
    try:
        txt = open(Path(PROJECT_ROOT) / filepath, encoding='utf-8').read()
    except:
        return set()
    refs = set()
    # Pattern: {{project_root}}/studio/knowledge/...
    for m in re.finditer(r'\{\{project_root\}\}/studio/knowledge/([^\s`"\')\]]+)', txt):
        raw = m.group(1).strip().rstrip('`').rstrip('.').rstrip(')')
        refs.add(f'studio/knowledge/{raw}')
    return refs

# ── 5. Extract scene_tags from a file ────────────────────────────────────────
def extract_scene_tags_from_file(filepath):
    try:
        txt = open(Path(PROJECT_ROOT) / filepath, encoding='utf-8').read()
    except:
        return set()
    tags = set()
    for m in re.finditer(r'scene_tag[s]?[:\s]+["\']?([^"\'\n]+)', txt):
        tags.update(t.strip() for t in m.group(1).split('|'))
    return tags

# ── 6. Build skill → knowledge mapping from SKILL files directly ─────────────
def build_skill_to_knowledge_map():
    skill_map = {}
    for f in list_skill_files():
        refs = extract_references_from_file(f)
        tags = extract_scene_tags_from_file(f)
        if refs or tags:
            skill_map[f] = {'references': sorted(refs), 'scene_tags': sorted(tags)}
    return skill_map

# ── 7. Find orphans vs index-registered ───────────────────────────────────────
def main(fix=False):
    index_data = load_index()
    index_entries = index_data['index']

    # Build set of files in index
    indexed_files = set(e['file'] for e in index_entries)

    # Build set of physical files
    physical_files = set(list_knowledge_files())

    # Files in index but missing from disk
    missing_from_disk = indexed_files - physical_files

    # Physical files NOT in index → orphans (candidates for deletion or indexing)
    orphans = physical_files - indexed_files

    # Build skill → knowledge map
    skill_map = build_skill_to_knowledge_map()

    # Cross-reference: index says "used_by: [lewd-writer]" but lewd-writer
    # doesn't actually reference it → broken wiring
    broken_wiring = []
    for entry in index_entries:
        f = entry['file']
        used_by = entry.get('used_by', [])
        for skill in used_by:
            # Find skill file
            skill_patterns = [
                f"studio/core/{skill}/SKILL.md",
                f"studio/services/{skill}/SKILL.md",
                f"studio/agents/{skill}.agent.yaml",
                f"studio/agents/{skill}.yaml",
            ]
            skill_file = None
            for pat in skill_patterns:
                if Path(PROJECT_ROOT) / pat exists():
                    skill_file = pat
                    break
            if not skill_file:
                broken_wiring.append({
                    'entry': f,
                    'used_by_skill': skill,
                    'issue': 'skill_not_found',
                    'fix': f'Add skill file for "{skill}" or remove from used_by',
                })
                continue
            refs = extract_references_from_file(skill_file)
            expected = f'studio/knowledge/{f}'
            if expected not in refs and f not in refs:
                broken_wiring.append({
                    'entry': f,
                    'skill_file': skill_file,
                    'used_by_skill': skill,
                    'issue': 'not_referenced_in_skill',
                    'fix': f'Add "{expected}" to {skill_file} injection or dependencies',
                })

    # Scene tag → knowledge gaps
    scene_tag_issues = []
    defined_tags = set(index_data['scene_tags'].keys())
    for skill_file, data in skill_map.items():
        for tag in data['scene_tags']:
            if tag not in defined_tags and tag not in ['bedroom', 'explicit', 'dialogue-heavy', 'aftermath', 'intro']:
                scene_tag_issues.append({
                    'skill': skill_file,
                    'tag': tag,
                    'issue': 'scene_tag_not_in_index',
                    'fix': f'Add scene_tag "{tag}" to knowledge-index.yaml scene_tags section',
                })

    # Summary
    result = {
        'summary': {
            'total_physical_files': len(physical_files),
            'total_indexed_files': len(indexed_files),
            'orphans': len(orphans),
            'missing_from_disk': len(missing_from_disk),
            'broken_wiring_count': len(broken_wiring),
            'scene_tag_issues': len(scene_tag_issues),
        },
        'orphans': sorted(orphans),
        'missing_from_disk': sorted(missing_from_disk),
        'broken_wiring': broken_wiring,
        'scene_tag_issues': scene_tag_issues,
        'skill_to_knowledge_map': skill_map,
        'indexed_files': sorted(indexed_files),
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))

    if fix or '--fix' in sys.argv:
        print('\n\n=== FIX SUGGESTIONS ===')
        for item in broken_wiring:
            print(f"  [{item['issue']}] {item.get('entry','?')} → {item['fix']}")
        for item in scene_tag_issues:
            print(f"  [{item['issue']}] {item['skill']} tag={item['tag']} → {item['fix']}")
        if orphans:
            print(f"\n  ORPHANS ({len(orphans)} files):")
            for o in orphans:
                print(f"    - {o}")

if __name__ == '__main__':
    main(fix='--fix' in sys.argv)
