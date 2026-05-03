#!/usr/bin/env python3
"""
extract_character_events.py
===========================
RPG Maker MZ/MV character event extractor.
Mines ALL maps + CommonEvents for a specific character's dialogue,
scenes, and interactions. Outputs structured Markdown + JSON.

Usage:
    python extract_character_events.py <game_root> --actor-id 2 --actor-name 琥珀 --output-dir ./output
"""

import json
import os
import argparse
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime


# ──────────────────────────────────────────────
# RPG Maker Command Codes
# ──────────────────────────────────────────────
CMD_SHOW_TEXT_SETUP = 101   # [faceName, faceIndex, bg, pos, speakerName]
CMD_SHOW_TEXT_LINE  = 401   # [text]
CMD_SHOW_CHOICES    = 102   # [choices[], cancelType]
CMD_WHEN_CHOICE     = 402   # [choiceIndex, choiceName]
CMD_COMMENT         = 108   # [comment]
CMD_COMMENT_CONT    = 408   # [comment continuation]
CMD_SCRIPT_CALL     = 355   # [script]
CMD_SHOW_PICTURE    = 231   # [pictureId, name, ...]
CMD_CHANGE_SWITCH   = 121   # [switchId, ...]
CMD_COMMON_EVENT    = 117   # [commonEventId]

# Text codes that reference actors: \n[X], \N[X]
ACTOR_REF_RE = re.compile(r'\\[nN]\[(\d+)\]')


def strip_rpgmaker_codes(text: str) -> str:
    """Remove RPG Maker formatting codes for cleaner output."""
    text = re.sub(r'\\[cC]\[\d+\]', '', text)
    text = re.sub(r'\\I\[\d+\]', '', text)
    text = re.sub(r'\\[vV]\[\d+\]', '{VAR}', text)
    text = re.sub(r'\\pop\[-?\d+\]', '', text)
    text = re.sub(r'\\>', '', text)
    text = text.strip()
    return text


def resolve_speaker(speaker: str, actor_names: dict) -> str:
    """Resolve \\n[X] references in speaker name."""
    def replace_ref(match):
        aid = int(match.group(1))
        return actor_names.get(aid, f'Actor#{aid}')
    return ACTOR_REF_RE.sub(replace_ref, speaker)


def resolve_text(text: str, actor_names: dict) -> str:
    """Resolve actor references in dialogue text."""
    def replace_ref(match):
        aid = int(match.group(1))
        return actor_names.get(aid, f'Actor#{aid}')
    result = ACTOR_REF_RE.sub(replace_ref, text)
    return strip_rpgmaker_codes(result)


def is_character_relevant(cmd_list: list, actor_id: int, actor_name: str, actor_names: dict) -> bool:
    """Check if a command list references the target character."""
    actor_ref_patterns = [f'\\n[{actor_id}]', f'\\N[{actor_id}]']
    for cmd in cmd_list:
        code = cmd.get('code', 0)
        params = cmd.get('parameters', [])
        if code == CMD_SHOW_TEXT_SETUP and len(params) > 4:
            speaker = str(params[4])
            if actor_name in speaker or any(p in speaker for p in actor_ref_patterns):
                return True
        if code == CMD_SHOW_TEXT_LINE and params:
            text = str(params[0])
            if actor_name in text or any(p in text for p in actor_ref_patterns):
                return True
    return False


def extract_dialogue_blocks(cmd_list: list, actor_id: int, actor_name: str,
                             actor_names: dict) -> list:
    """Extract dialogue blocks from a command list, returning structured data."""
    blocks = []
    current_block = None
    actor_ref_patterns = [f'\\n[{actor_id}]', f'\\N[{actor_id}]']

    i = 0
    while i < len(cmd_list):
        cmd = cmd_list[i]
        code = cmd.get('code', 0)
        params = cmd.get('parameters', [])

        if code == CMD_SHOW_TEXT_SETUP:
            # Save previous block
            if current_block and current_block['lines']:
                blocks.append(current_block)

            speaker_raw = params[4] if len(params) > 4 else ''
            face_name = params[0] if params else ''
            speaker = resolve_speaker(str(speaker_raw), actor_names)

            is_target = (actor_name in str(speaker_raw) or
                        any(p in str(speaker_raw) for p in actor_ref_patterns))

            current_block = {
                'speaker': speaker,
                'speaker_raw': str(speaker_raw),
                'face': face_name,
                'is_target_speaking': is_target,
                'lines': [],
                'cmd_index': i,
            }

        elif code == CMD_SHOW_TEXT_LINE:
            text_raw = str(params[0]) if params else ''
            text_clean = resolve_text(text_raw, actor_names)

            mentions_target = (actor_name in text_raw or
                             any(p in text_raw for p in actor_ref_patterns))

            if current_block is not None:
                current_block['lines'].append(text_clean)
                if mentions_target:
                    current_block['mentions_target'] = True
            else:
                # Orphan text line (e.g., narration via \pop)
                blocks.append({
                    'speaker': '(narration)',
                    'speaker_raw': '',
                    'face': '',
                    'is_target_speaking': False,
                    'mentions_target': mentions_target,
                    'lines': [text_clean],
                    'cmd_index': i,
                })

        elif code == CMD_SHOW_PICTURE:
            # Track CG pictures shown
            if current_block is None:
                current_block = {
                    'speaker': '(system)',
                    'speaker_raw': '',
                    'face': '',
                    'is_target_speaking': False,
                    'lines': [],
                    'cmd_index': i,
                }
            pic_name = params[1] if len(params) > 1 else ''
            current_block.setdefault('pictures', []).append(str(pic_name))

        elif code == CMD_SHOW_CHOICES:
            if current_block and current_block['lines']:
                blocks.append(current_block)
                current_block = None
            choices = params[0] if params else []
            blocks.append({
                'speaker': '(choices)',
                'speaker_raw': '',
                'face': '',
                'is_target_speaking': False,
                'lines': [f'→ {c}' for c in choices],
                'cmd_index': i,
            })

        elif code not in [CMD_SHOW_TEXT_LINE, CMD_SHOW_TEXT_SETUP]:
            # Non-dialogue command: flush current block
            if current_block and current_block['lines']:
                blocks.append(current_block)
                current_block = None

        i += 1

    # Flush remaining
    if current_block and current_block['lines']:
        blocks.append(current_block)

    return blocks


def extract_from_map(map_path: str, actor_id: int, actor_name: str,
                     actor_names: dict, map_name: str) -> list:
    """Extract all character-relevant events from a single map."""
    with open(map_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    events = [e for e in (data.get('events') or []) if e is not None]
    results = []

    for ev in events:
        ev_id = ev.get('id', 0)
        ev_name = ev.get('name', f'Event_{ev_id}')

        for pi, page in enumerate(ev.get('pages', [])):
            cmd_list = page.get('list', [])
            if not is_character_relevant(cmd_list, actor_id, actor_name, actor_names):
                continue

            blocks = extract_dialogue_blocks(cmd_list, actor_id, actor_name, actor_names)
            if blocks:
                results.append({
                    'source_type': 'map',
                    'source_id': os.path.basename(map_path).replace('.json', ''),
                    'source_name': map_name,
                    'event_id': ev_id,
                    'event_name': ev_name,
                    'page': pi,
                    'total_blocks': len(blocks),
                    'target_speaks': sum(1 for b in blocks if b.get('is_target_speaking')),
                    'blocks': blocks,
                })

    return results


def extract_from_common_events(ce_path: str, actor_id: int, actor_name: str,
                                actor_names: dict) -> list:
    """Extract all character-relevant CommonEvents."""
    with open(ce_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    results = []
    for ev in data:
        if ev is None:
            continue
        ev_id = ev.get('id', 0)
        ev_name = ev.get('name', '')
        cmd_list = ev.get('list', [])

        # Check name-level relevance first
        name_relevant = (actor_name in ev_name or '祭司' in ev_name)

        if not name_relevant and not is_character_relevant(cmd_list, actor_id, actor_name, actor_names):
            continue

        blocks = extract_dialogue_blocks(cmd_list, actor_id, actor_name, actor_names)
        if blocks or name_relevant:
            results.append({
                'source_type': 'common_event',
                'source_id': f'CE{ev_id:03d}',
                'source_name': ev_name,
                'event_id': ev_id,
                'event_name': ev_name,
                'page': 0,
                'total_blocks': len(blocks),
                'target_speaks': sum(1 for b in blocks if b.get('is_target_speaking')),
                'blocks': blocks,
            })

    return results


def generate_markdown(all_results: list, actor_name: str, actor_id: int,
                      output_path: str, actor_names: dict):
    """Generate a comprehensive Markdown report."""
    # Separate maps and CEs
    map_results = [r for r in all_results if r['source_type'] == 'map']
    ce_results = [r for r in all_results if r['source_type'] == 'common_event']

    # Stats
    total_blocks = sum(r['total_blocks'] for r in all_results)
    target_speaks = sum(r['target_speaks'] for r in all_results)

    lines = []
    lines.append(f'# {actor_name} (Actor #{actor_id}) — Complete Event Extraction')
    lines.append(f'')
    lines.append(f'> Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    lines.append(f'')
    lines.append(f'## Summary')
    lines.append(f'| Metric | Value |')
    lines.append(f'|--------|-------|')
    lines.append(f'| Maps with presence | {len(set(r["source_id"] for r in map_results))} |')
    lines.append(f'| CommonEvents | {len(ce_results)} |')
    lines.append(f'| Total events | {len(all_results)} |')
    lines.append(f'| Total dialogue blocks | {total_blocks} |')
    lines.append(f'| {actor_name} speaks | {target_speaks} blocks |')
    lines.append(f'')
    lines.append(f'---')
    lines.append(f'')

    # ── CommonEvents Section ──
    lines.append(f'## CommonEvents ({len(ce_results)} events)')
    lines.append(f'')
    for r in sorted(ce_results, key=lambda x: x['event_id']):
        lines.append(f'### {r["source_id"]}: {r["event_name"]}')
        lines.append(f'*Blocks: {r["total_blocks"]} | {actor_name} speaks: {r["target_speaks"]}*')
        lines.append(f'')
        for block in r['blocks']:
            speaker = block['speaker'] or '(narration)'
            is_target = '**' if block.get('is_target_speaking') else ''
            for line in block['lines']:
                lines.append(f'{is_target}[{speaker}]{is_target}: {line}')
            # Show pictures if any
            for pic in block.get('pictures', []):
                lines.append(f'  📷 `{pic}`')
        lines.append(f'')

    # ── Map Events Section ──
    lines.append(f'---')
    lines.append(f'')
    lines.append(f'## Map Events ({len(map_results)} events across {len(set(r["source_id"] for r in map_results))} maps)')
    lines.append(f'')

    # Group by map
    by_map = defaultdict(list)
    for r in map_results:
        by_map[r['source_id']].append(r)

    # Sort maps by total target-speak count
    sorted_maps = sorted(by_map.items(),
                         key=lambda x: sum(r['target_speaks'] for r in x[1]),
                         reverse=True)

    for map_id, results_in_map in sorted_maps:
        map_name = results_in_map[0]['source_name']
        total_speaks = sum(r['target_speaks'] for r in results_in_map)
        lines.append(f'### {map_id}: {map_name} ({total_speaks} {actor_name} blocks)')
        lines.append(f'')

        for r in sorted(results_in_map, key=lambda x: x['event_id']):
            lines.append(f'#### Event {r["event_id"]}: {r["event_name"]} (page {r["page"]})')
            lines.append(f'')
            for block in r['blocks']:
                speaker = block['speaker'] or '(narration)'
                is_target = '**' if block.get('is_target_speaking') else ''
                for line in block['lines']:
                    lines.append(f'{is_target}[{speaker}]{is_target}: {line}')
                for pic in block.get('pictures', []):
                    lines.append(f'  📷 `{pic}`')
            lines.append(f'')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    return len(lines)


def main():
    parser = argparse.ArgumentParser(description='Extract all events for a specific RPG Maker character')
    parser.add_argument('game_root', help='Path to RPG Maker game root directory')
    parser.add_argument('--actor-id', type=int, required=True, help='Actor ID (from Actors.json)')
    parser.add_argument('--actor-name', type=str, required=True, help='Actor name to search for')
    parser.add_argument('--aliases', nargs='*', default=[], help='Additional names/aliases to search')
    parser.add_argument('--output-dir', type=str, default='.', help='Output directory')
    parser.add_argument('--format', choices=['md', 'json', 'both'], default='both', help='Output format')
    args = parser.parse_args()

    game_root = Path(args.game_root)
    data_dir = game_root / 'data'

    if not data_dir.exists():
        # Try www/data for MV
        data_dir = game_root / 'www' / 'data'
        if not data_dir.exists():
            print(f'ERROR: Cannot find data/ directory in {game_root}')
            return 1

    # ── Load Actors ──
    actors_path = data_dir / 'Actors.json'
    actor_names = {}
    if actors_path.exists():
        with open(actors_path, 'r', encoding='utf-8') as f:
            actors = json.load(f)
        for a in actors:
            if a is not None:
                actor_names[a['id']] = a.get('name', '')
        print(f'Loaded {len(actor_names)} actors')

    # ── Load MapInfos ──
    mapinfos_path = data_dir / 'MapInfos.json'
    map_names = {}
    if mapinfos_path.exists():
        with open(mapinfos_path, 'r', encoding='utf-8') as f:
            mapinfos = json.load(f)
        for m in mapinfos:
            if m is not None:
                map_names[m['id']] = m.get('name', f'Map{m["id"]:03d}')

    actor_id = args.actor_id
    actor_name = args.actor_name
    print(f'Extracting events for: {actor_name} (Actor #{actor_id})')
    print(f'Aliases: {args.aliases}')

    # ── Extract from CommonEvents ──
    ce_path = data_dir / 'CommonEvents.json'
    all_results = []
    if ce_path.exists():
        print(f'Scanning CommonEvents...')
        ce_results = extract_from_common_events(str(ce_path), actor_id, actor_name, actor_names)
        all_results.extend(ce_results)
        print(f'  Found {len(ce_results)} relevant CommonEvents')

    # ── Extract from Maps ──
    map_files = sorted(data_dir.glob('Map[0-9]*.json'))
    print(f'Scanning {len(map_files)} maps...')
    maps_with_hits = 0
    for mf in map_files:
        # Extract map ID from filename
        map_id_str = mf.stem.replace('Map', '')
        try:
            map_id = int(map_id_str)
        except ValueError:
            continue
        map_name = map_names.get(map_id, mf.stem)

        results = extract_from_map(str(mf), actor_id, actor_name, actor_names, map_name)
        if results:
            all_results.extend(results)
            maps_with_hits += 1

    print(f'  Found events in {maps_with_hits} maps')

    # ── Output ──
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    safe_name = actor_name.replace(' ', '_')

    if args.format in ('md', 'both'):
        md_path = output_dir / f'{safe_name}_events.md'
        line_count = generate_markdown(all_results, actor_name, actor_id, str(md_path), actor_names)
        print(f'Markdown: {md_path} ({line_count} lines)')

    if args.format in ('json', 'both'):
        json_path = output_dir / f'{safe_name}_events.json'
        # Strip blocks for JSON (they're huge)
        json_summary = []
        for r in all_results:
            json_summary.append({
                'source_type': r['source_type'],
                'source_id': r['source_id'],
                'source_name': r['source_name'],
                'event_id': r['event_id'],
                'event_name': r['event_name'],
                'page': r['page'],
                'total_blocks': r['total_blocks'],
                'target_speaks': r['target_speaks'],
                'blocks': r['blocks'],
            })
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_summary, f, ensure_ascii=False, indent=2)
        print(f'JSON: {json_path}')

    # ── Final Stats ──
    total_blocks = sum(r['total_blocks'] for r in all_results)
    target_speaks = sum(r['target_speaks'] for r in all_results)
    print(f'\n=== DONE ===')
    print(f'Total events: {len(all_results)}')
    print(f'Total dialogue blocks: {total_blocks}')
    print(f'{actor_name} speaks in: {target_speaks} blocks')

    return 0


if __name__ == '__main__':
    exit(main())
