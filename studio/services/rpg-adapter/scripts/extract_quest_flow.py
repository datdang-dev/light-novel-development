#!/usr/bin/env python3
"""
extract_quest_flow.py
=====================
RPG Maker MZ/MV quest flow extractor.
Analyzes Switch/Variable dependencies across all maps and CommonEvents
to build a quest progression graph.

Key features:
- Tracks Variable changes (especially 主线进度/main quest progress)
- Tracks Switch toggles (quest gates)
- Tracks Conditional Branches (quest requirements)
- Tracks Map Transfers (location progression)
- Tracks ShowPicture commands (CG/R18 scene markers)
- Outputs quest_flow_graph.json + quest_flow_report.md

Usage:
    python extract_quest_flow.py <game_root> --output-dir ./output
    python extract_quest_flow.py <game_root> --main-quest-var 1000 --output-dir ./output
"""

import json
import os
import re
import argparse
from pathlib import Path
from collections import defaultdict
from datetime import datetime

# ──────────────────────────────────────────────
# RPG Maker Command Codes
# ──────────────────────────────────────────────
CMD_SHOW_TEXT_SETUP  = 101
CMD_SHOW_TEXT_LINE   = 401
CMD_SHOW_CHOICES     = 102
CMD_CONDITIONAL      = 111  # Conditional Branch
CMD_ELSE             = 411
CMD_CONTROL_SWITCH   = 121  # [startId, endId, value(0=ON/1=OFF)]
CMD_CONTROL_VARIABLE = 122  # [startId, endId, operationType, operand, ...]
CMD_TRANSFER_PLAYER  = 201  # [mode, mapId, x, y, direction, fadeType]
CMD_SHOW_PICTURE     = 231  # [pictureId, name, ...]
CMD_COMMON_EVENT     = 117  # [commonEventId]
CMD_COMMENT          = 108
CMD_SCRIPT           = 355
CMD_LABEL            = 118
CMD_JUMP_LABEL       = 119
CMD_PLUGIN_CMD       = 357

ACTOR_REF_RE = re.compile(r'\\[nN]\[(\d+)\]')


def load_system_names(data_dir: Path) -> dict:
    """Load switch/variable names from System.json."""
    sys_path = data_dir / 'System.json'
    result = {'switches': {}, 'variables': {}, 'actors': {}}
    if not sys_path.exists():
        return result
    with open(sys_path, 'r', encoding='utf-8') as f:
        sys_data = json.load(f)
    for i, name in enumerate(sys_data.get('switches', [])):
        if name and name.strip():
            result['switches'][i] = name.strip()
    for i, name in enumerate(sys_data.get('variables', [])):
        if name and name.strip():
            result['variables'][i] = name.strip()
    # Load actors
    actors_path = data_dir / 'Actors.json'
    if actors_path.exists():
        with open(actors_path, 'r', encoding='utf-8') as f:
            actors = json.load(f)
        for a in actors:
            if a:
                result['actors'][a['id']] = a.get('name', '')
    return result


def load_map_names(data_dir: Path) -> dict:
    """Load map names from MapInfos.json."""
    path = data_dir / 'MapInfos.json'
    names = {}
    if path.exists():
        with open(path, 'r', encoding='utf-8') as f:
            infos = json.load(f)
        for m in infos:
            if m:
                names[m['id']] = m.get('name', f'Map{m["id"]:03d}')
    return names


def resolve_speaker(text: str, actors: dict) -> str:
    """Resolve \\n[X] actor references."""
    def repl(m):
        return actors.get(int(m.group(1)), f'Actor#{m.group(1)}')
    return ACTOR_REF_RE.sub(repl, str(text))


def extract_dialogue_preview(cmd_list: list, start_idx: int, actors: dict, max_chars=300) -> str:
    """Extract a dialogue preview from commands near the given index."""
    lines = []
    total = 0
    for i in range(max(0, start_idx - 5), min(len(cmd_list), start_idx + 50)):
        cmd = cmd_list[i]
        code = cmd.get('code', 0)
        params = cmd.get('parameters', [])
        if code == CMD_SHOW_TEXT_SETUP and len(params) > 4:
            speaker = resolve_speaker(str(params[4]), actors)
            if speaker:
                lines.append(f'[{speaker}]: ')
        elif code == CMD_SHOW_TEXT_LINE and params:
            text = re.sub(r'\\[cCvViI]\[\d+\]', '', str(params[0])).strip()
            text = ACTOR_REF_RE.sub(lambda m: actors.get(int(m.group(1)), '???'), text)
            if not lines:
                lines.append(text)
            elif not lines[-1].endswith(': '):
                lines.append(f'  {text}')
            else:
                lines[-1] = lines[-1] + text
            total += len(text)
            if total >= max_chars:
                break
    return ' | '.join(lines)[:max_chars]


def analyze_event_page(cmd_list: list, actors: dict) -> dict:
    """Analyze a single event page for quest-relevant commands."""
    result = {
        'switches_set': [],      # [{id, value, name}]
        'switches_checked': [],  # [{id, value, name}]
        'variables_set': [],     # [{id, operation, operand, name}]
        'variables_checked': [], # [{id, comparison, value, name}]
        'map_transfers': [],     # [{map_id, map_name, x, y}]
        'pictures_shown': [],    # [name]
        'common_events': [],     # [id]
        'has_choices': False,
        'dialogue_count': 0,
    }

    for i, cmd in enumerate(cmd_list):
        code = cmd.get('code', 0)
        params = cmd.get('parameters', [])

        if code == CMD_CONTROL_SWITCH and len(params) >= 3:
            for sid in range(params[0], params[1] + 1):
                result['switches_set'].append({
                    'id': sid,
                    'value': 'ON' if params[2] == 0 else 'OFF',
                })

        elif code == CMD_CONTROL_VARIABLE and len(params) >= 4:
            for vid in range(params[0], params[1] + 1):
                op_type = params[2]  # 0=set, 1=add, 2=sub, 3=mul, 4=div, 5=mod
                op_names = {0: 'SET', 1: 'ADD', 2: 'SUB', 3: 'MUL', 4: 'DIV', 5: 'MOD'}
                operand_type = params[3]  # 0=constant, 1=variable, 2=random, etc.
                operand_val = params[4] if len(params) > 4 else 0
                result['variables_set'].append({
                    'id': vid,
                    'operation': op_names.get(op_type, f'OP{op_type}'),
                    'operand_type': operand_type,
                    'operand': operand_val,
                })

        elif code == CMD_CONDITIONAL and params:
            cond_type = params[0]
            if cond_type == 0 and len(params) >= 3:  # Switch
                result['switches_checked'].append({
                    'id': params[1],
                    'value': 'ON' if params[2] == 0 else 'OFF',
                })
            elif cond_type == 1 and len(params) >= 5:  # Variable
                result['variables_checked'].append({
                    'id': params[1],
                    'comparison': ['==', '>=', '<=', '>', '<', '!='][params[4]] if params[4] < 6 else f'CMP{params[4]}',
                    'operand_type': params[2],  # 0=constant, 1=variable
                    'value': params[3],
                })

        elif code == CMD_TRANSFER_PLAYER and len(params) >= 4:
            if params[0] == 0:  # Direct designation
                result['map_transfers'].append({
                    'map_id': params[1],
                    'x': params[2],
                    'y': params[3],
                })

        elif code == CMD_SHOW_PICTURE and len(params) > 1:
            pic_name = str(params[1])
            if pic_name:
                result['pictures_shown'].append(pic_name)

        elif code == CMD_COMMON_EVENT and params:
            result['common_events'].append(params[0])

        elif code == CMD_SHOW_CHOICES:
            result['has_choices'] = True

        elif code == CMD_SHOW_TEXT_SETUP:
            result['dialogue_count'] += 1

    return result


def classify_picture(name: str) -> dict:
    """Classify a picture name as R18, background, UI, etc."""
    name_lower = name.lower()
    r18_patterns = [
        'event-', '事件', 'cum', 'sex', 'blow', 'doggy', 'cowgirl',
        'missionary', 'anal', 'oral', 'naked', 'nude', 'fuck',
        'ejac', 'penis', 'cock', 'pussy', 'boob', 'tit',
        'gangbang', '4some', '3p', 'ntr', 'netori', 'cuck',
        'face1', 'face2', 'face3', 'base1', 'base2', 'base3',
        'squirt', 'ahegao', 'bukka',
    ]
    bg_patterns = ['bg_', 'background', 'map_', '背景', 'sky_', 'cloud']
    ui_patterns = ['ui_', 'hud_', 'icon_', 'button_', 'frame_', 'gauge_']

    if any(p in name_lower for p in r18_patterns):
        return {'type': 'r18', 'name': name}
    elif any(p in name_lower for p in bg_patterns):
        return {'type': 'background', 'name': name}
    elif any(p in name_lower for p in ui_patterns):
        return {'type': 'ui', 'name': name}
    # Check CG naming conventions (下水道事件, 暗精灵村, 亚利佐事件, etc.)
    cg_prefixes = ['下水道', '暗精灵', '亚利佐', '马车', '妓院', '娼妓', '绿帽',
                   '温泉', '牧场', '海滩', '酒馆', '监狱', '孤儿']
    if any(p in name for p in cg_prefixes):
        return {'type': 'r18', 'name': name}
    return {'type': 'unknown', 'name': name}


def process_game(game_root: Path, main_quest_var: int, sys_names: dict,
                 map_names: dict) -> dict:
    """Process entire game and build quest flow data."""
    data_dir = game_root / 'data'
    if not data_dir.exists():
        data_dir = game_root / 'www' / 'data'

    actors = sys_names.get('actors', {})
    all_nodes = []
    all_r18_scenes = []

    # ── Process Maps ──
    map_files = sorted(data_dir.glob('Map[0-9]*.json'))
    for mf in map_files:
        map_id = int(mf.stem.replace('Map', ''))
        map_name = map_names.get(map_id, mf.stem)

        with open(mf, 'r', encoding='utf-8') as f:
            map_data = json.load(f)

        events = [e for e in (map_data.get('events') or []) if e]
        for ev in events:
            ev_id = ev.get('id', 0)
            ev_name = ev.get('name', f'Event_{ev_id}')

            for pi, page in enumerate(ev.get('pages', [])):
                cmd_list = page.get('list', [])
                analysis = analyze_event_page(cmd_list, actors)

                # Skip empty pages
                if (not analysis['switches_set'] and not analysis['variables_set']
                    and not analysis['pictures_shown'] and analysis['dialogue_count'] == 0
                    and not analysis['map_transfers']):
                    continue

                # Check for main quest variable
                main_quest_sets = [v for v in analysis['variables_set'] if v['id'] == main_quest_var]
                main_quest_checks = [v for v in analysis['variables_checked'] if v['id'] == main_quest_var]

                node_id = f'Map{map_id:03d}_EV{ev_id}_P{pi}'
                node = {
                    'id': node_id,
                    'source_type': 'map',
                    'map_id': map_id,
                    'map_name': map_name,
                    'event_id': ev_id,
                    'event_name': ev_name,
                    'page': pi,
                    'is_main_quest': bool(main_quest_sets or main_quest_checks),
                    'main_quest_sets': main_quest_sets,
                    'main_quest_checks': main_quest_checks,
                    'switches_set': analysis['switches_set'],
                    'switches_checked': analysis['switches_checked'],
                    'variables_set': analysis['variables_set'],
                    'variables_checked': analysis['variables_checked'],
                    'map_transfers': analysis['map_transfers'],
                    'pictures_shown': analysis['pictures_shown'],
                    'common_events': analysis['common_events'],
                    'has_choices': analysis['has_choices'],
                    'dialogue_count': analysis['dialogue_count'],
                    'dialogue_preview': extract_dialogue_preview(cmd_list, 0, actors),
                    'page_conditions': {
                        'switch_id': page.get('conditions', {}).get('switch1Id', 0) if page.get('conditions', {}).get('switch1Valid') else 0,
                        'variable_id': page.get('conditions', {}).get('variableId', 0) if page.get('conditions', {}).get('variableValid') else 0,
                        'variable_value': page.get('conditions', {}).get('variableValue', 0) if page.get('conditions', {}).get('variableValid') else 0,
                    },
                }
                all_nodes.append(node)

                # Collect R18 scenes
                for pic in analysis['pictures_shown']:
                    cls = classify_picture(pic)
                    if cls['type'] == 'r18':
                        all_r18_scenes.append({
                            'picture': pic,
                            'node_id': node_id,
                            'map_id': map_id,
                            'map_name': map_name,
                            'event_id': ev_id,
                            'event_name': ev_name,
                            'page': pi,
                            'dialogue_preview': extract_dialogue_preview(cmd_list, 0, actors, 200),
                            'is_main_quest': node['is_main_quest'],
                        })

    # ── Process CommonEvents ──
    ce_path = data_dir / 'CommonEvents.json'
    if ce_path.exists():
        with open(ce_path, 'r', encoding='utf-8') as f:
            ce_data = json.load(f)

        for ce in ce_data:
            if not ce:
                continue
            ce_id = ce.get('id', 0)
            ce_name = ce.get('name', '')
            cmd_list = ce.get('list', [])
            analysis = analyze_event_page(cmd_list, actors)

            if (not analysis['switches_set'] and not analysis['variables_set']
                and not analysis['pictures_shown'] and analysis['dialogue_count'] == 0):
                continue

            main_quest_sets = [v for v in analysis['variables_set'] if v['id'] == main_quest_var]
            main_quest_checks = [v for v in analysis['variables_checked'] if v['id'] == main_quest_var]

            node_id = f'CE{ce_id:03d}'
            node = {
                'id': node_id,
                'source_type': 'common_event',
                'map_id': None,
                'map_name': None,
                'event_id': ce_id,
                'event_name': ce_name,
                'page': 0,
                'is_main_quest': bool(main_quest_sets or main_quest_checks),
                'main_quest_sets': main_quest_sets,
                'main_quest_checks': main_quest_checks,
                'switches_set': analysis['switches_set'],
                'switches_checked': analysis['switches_checked'],
                'variables_set': analysis['variables_set'],
                'variables_checked': analysis['variables_checked'],
                'map_transfers': analysis['map_transfers'],
                'pictures_shown': analysis['pictures_shown'],
                'common_events': analysis['common_events'],
                'has_choices': analysis['has_choices'],
                'dialogue_count': analysis['dialogue_count'],
                'dialogue_preview': extract_dialogue_preview(cmd_list, 0, actors),
                'page_conditions': {},
            }
            all_nodes.append(node)

            for pic in analysis['pictures_shown']:
                cls = classify_picture(pic)
                if cls['type'] == 'r18':
                    all_r18_scenes.append({
                        'picture': pic,
                        'node_id': node_id,
                        'map_id': None,
                        'map_name': f'CE: {ce_name}',
                        'event_id': ce_id,
                        'event_name': ce_name,
                        'page': 0,
                        'dialogue_preview': extract_dialogue_preview(cmd_list, 0, actors, 200),
                        'is_main_quest': node['is_main_quest'],
                    })

    # ── Build Edges ──
    edges = []
    # Switch-based edges: if node A sets switch X, and node B checks switch X
    switch_setters = defaultdict(list)
    switch_checkers = defaultdict(list)
    for node in all_nodes:
        for sw in node['switches_set']:
            switch_setters[sw['id']].append(node['id'])
        for sw in node['switches_checked']:
            switch_checkers[sw['id']].append(node['id'])
        # Page conditions
        pc_sw = node['page_conditions'].get('switch_id', 0)
        if pc_sw:
            switch_checkers[pc_sw].append(node['id'])

    for sw_id in set(switch_setters.keys()) & set(switch_checkers.keys()):
        for src in switch_setters[sw_id]:
            for dst in switch_checkers[sw_id]:
                if src != dst:
                    edges.append({
                        'from': src, 'to': dst,
                        'type': 'switch',
                        'switch_id': sw_id,
                        'switch_name': sys_names['switches'].get(sw_id, ''),
                    })

    return {
        'nodes': all_nodes,
        'edges': edges,
        'r18_scenes': all_r18_scenes,
        'metadata': {
            'total_nodes': len(all_nodes),
            'main_quest_nodes': sum(1 for n in all_nodes if n['is_main_quest']),
            'total_r18_scenes': len(all_r18_scenes),
            'unique_r18_pictures': len(set(s['picture'] for s in all_r18_scenes)),
            'total_edges': len(edges),
            'main_quest_variable': main_quest_var,
            'main_quest_variable_name': sys_names['variables'].get(main_quest_var, ''),
        }
    }


def generate_report(graph: dict, sys_names: dict, map_names: dict, output_path: str):
    """Generate Markdown quest flow report."""
    nodes = graph['nodes']
    r18 = graph['r18_scenes']
    meta = graph['metadata']
    lines = []

    lines.append(f'# Quest Flow Report')
    lines.append(f'> Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    lines.append(f'')
    lines.append(f'## Summary')
    lines.append(f'| Metric | Value |')
    lines.append(f'|--------|-------|')
    for k, v in meta.items():
        lines.append(f'| {k} | {v} |')
    lines.append(f'')

    # ── Main Quest Nodes ──
    lines.append(f'## Main Quest Progression (Variable {meta["main_quest_variable"]}: {meta["main_quest_variable_name"]})')
    lines.append(f'')
    mq_nodes = [n for n in nodes if n['is_main_quest']]
    mq_nodes.sort(key=lambda n: (
        min((v['value'] for v in n['main_quest_checks']), default=0),
        min((v['operand'] for v in n['main_quest_sets']), default=0),
    ))
    for n in mq_nodes:
        checks_str = ', '.join(f'{v["comparison"]}{v["value"]}' for v in n['main_quest_checks'])
        sets_str = ', '.join(f'{v["operation"]}={v["operand"]}' for v in n['main_quest_sets'])
        loc = f'{n["map_name"]}' if n['map_name'] else f'CE: {n["event_name"]}'
        lines.append(f'### [{n["id"]}] {loc} / {n["event_name"]}')
        if checks_str:
            lines.append(f'- **Requires**: 主线进度 {checks_str}')
        if sets_str:
            lines.append(f'- **Sets**: 主线进度 → {sets_str}')
        if n['pictures_shown']:
            lines.append(f'- **CGs**: {", ".join(n["pictures_shown"][:5])}')
        if n['dialogue_preview']:
            lines.append(f'- **Preview**: {n["dialogue_preview"][:150]}...')
        lines.append(f'')

    # ── R18 Scene Catalog ──
    lines.append(f'---')
    lines.append(f'## R18 Scene Catalog ({meta["total_r18_scenes"]} scenes, {meta["unique_r18_pictures"]} unique CGs)')
    lines.append(f'')
    lines.append(f'| # | CG Name | Location | Event | Main Quest? |')
    lines.append(f'|---|---------|----------|-------|-------------|')

    seen = set()
    for i, scene in enumerate(r18):
        if scene['picture'] in seen:
            continue
        seen.add(scene['picture'])
        loc = scene['map_name'] or 'CommonEvent'
        mq = '✅' if scene['is_main_quest'] else ''
        lines.append(f'| {i+1} | `{scene["picture"]}` | {loc} | {scene["event_name"]} | {mq} |')
    lines.append(f'')

    # ── Quest-relevant Switches ──
    lines.append(f'---')
    lines.append(f'## Key Switches (used in quest flow)')
    lines.append(f'')
    switch_usage = defaultdict(lambda: {'set_by': [], 'checked_by': []})
    for n in nodes:
        for sw in n['switches_set']:
            switch_usage[sw['id']]['set_by'].append(n['id'])
        for sw in n['switches_checked']:
            switch_usage[sw['id']]['checked_by'].append(n['id'])

    for sw_id in sorted(switch_usage.keys()):
        name = sys_names['switches'].get(sw_id, '')
        usage = switch_usage[sw_id]
        if len(usage['set_by']) > 0 and len(usage['checked_by']) > 0:
            lines.append(f'- **[{sw_id}] {name}**: set by {len(usage["set_by"])} events, checked by {len(usage["checked_by"])} events')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    return len(lines)


def main():
    parser = argparse.ArgumentParser(description='Extract quest flow from RPG Maker game')
    parser.add_argument('game_root', help='Path to RPG Maker game root')
    parser.add_argument('--main-quest-var', type=int, default=1000,
                        help='Variable ID for main quest progress (default: 1000)')
    parser.add_argument('--output-dir', default='.', help='Output directory')
    args = parser.parse_args()

    game_root = Path(args.game_root)
    data_dir = game_root / 'data'
    if not data_dir.exists():
        data_dir = game_root / 'www' / 'data'
    if not data_dir.exists():
        print(f'ERROR: No data/ directory found in {game_root}')
        return 1

    print(f'Game root: {game_root}')
    print(f'Main quest variable: {args.main_quest_var}')

    # Load metadata
    sys_names = load_system_names(data_dir)
    map_names = load_map_names(data_dir)
    print(f'Loaded {len(sys_names["switches"])} switches, {len(sys_names["variables"])} variables, {len(sys_names["actors"])} actors')
    print(f'Loaded {len(map_names)} maps')

    # Process
    print(f'\nAnalyzing game...')
    graph = process_game(game_root, args.main_quest_var, sys_names, map_names)

    meta = graph['metadata']
    print(f'  Nodes: {meta["total_nodes"]}')
    print(f'  Main quest nodes: {meta["main_quest_nodes"]}')
    print(f'  R18 scenes: {meta["total_r18_scenes"]} ({meta["unique_r18_pictures"]} unique CGs)')
    print(f'  Edges: {meta["total_edges"]}')

    # Output
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # JSON
    json_path = out_dir / 'quest_flow_graph.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)
    print(f'\nJSON: {json_path}')

    # Markdown report
    md_path = out_dir / 'quest_flow_report.md'
    line_count = generate_report(graph, sys_names, map_names, str(md_path))
    print(f'Report: {md_path} ({line_count} lines)')

    return 0


if __name__ == '__main__':
    exit(main())
