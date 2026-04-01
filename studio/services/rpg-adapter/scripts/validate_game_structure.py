#!/usr/bin/env python3
"""Validate RPG Maker MV/MZ game directory structure for the rpg-adapter pipeline.

Supports:
  - RPG Maker MZ (flat structure: game_root/data/)
  - RPG Maker MV (www wrapper: game_root/www/data/)
  - RPG Maker MV (deployed flat: game_root/data/)

Usage:
    python3 validate_game_structure.py <game_root_path>
    python3 validate_game_structure.py <game_root_path> --log <log_path> --translation <translation_path>
"""
import argparse
import json
import os
import sys
from glob import glob


def detect_engine(game_root: str) -> tuple[str, str]:
    """Detect RPG Maker engine version and return (engine, data_dir)."""
    # MZ: flat structure with game.rmmzproject
    if os.path.exists(os.path.join(game_root, "game.rmmzproject")):
        data_dir = os.path.join(game_root, "data")
        if os.path.isdir(data_dir):
            return "MZ", data_dir

    # MV: www wrapper with Game.rpgproject
    if os.path.exists(os.path.join(game_root, "Game.rpgproject")):
        data_dir = os.path.join(game_root, "www", "data")
        if os.path.isdir(data_dir):
            return "MV", data_dir

    # MV deployed or generic: www/data/ exists
    www_data = os.path.join(game_root, "www", "data")
    if os.path.isdir(www_data):
        return "MV", www_data

    # Flat fallback: data/ exists directly
    flat_data = os.path.join(game_root, "data")
    if os.path.isdir(flat_data):
        return "unknown", flat_data

    return "none", ""


def validate(game_root: str, log_path: str = None, translation_path: str = None) -> dict:
    engine, data_dir = detect_engine(game_root)

    results = {
        "engine": engine,
        "data_dir": data_dir,
        "hard_checks": [],
        "soft_checks": [],
        "stats": {},
        "passed": True,
    }

    # ── HARD checks ──
    def hard(ok: bool, desc: str, path: str = "N/A"):
        status = "PASS" if ok else "FAIL"
        results["hard_checks"].append({"check": desc, "status": status, "path": path})
        if not ok:
            results["passed"] = False

    hard(os.path.isdir(game_root), "Game root path exists", game_root)
    hard(engine != "none", f"Engine detected: {engine}", data_dir)
    hard(os.path.isdir(data_dir), "Data directory exists", data_dir)

    # Map files
    map_files = sorted(glob(os.path.join(data_dir, "Map[0-9]*.json"))) if data_dir else []
    hard(len(map_files) > 0, f"Map*.json files found ({len(map_files)})", data_dir)
    results["stats"]["map_count"] = len(map_files)

    # Core data files
    for fname in ["MapInfos.json", "Actors.json", "CommonEvents.json"]:
        fpath = os.path.join(data_dir, fname)
        hard(os.path.exists(fpath), f"{fname} exists", fpath)

    # ── SOFT checks ──
    def soft(ok: bool, desc: str, path: str = "N/A"):
        status = "PASS" if ok else "WARN"
        results["soft_checks"].append({"check": desc, "status": status, "path": path})

    # Translation file (check multiple locations)
    trans_paths = [
        translation_path,
        os.path.join(game_root, "ManualTransFile.json"),
        os.path.join(game_root, "www", "ManualTransFile.json"),
    ]
    trans_found = any(p and os.path.exists(p) for p in trans_paths)
    soft(trans_found, "Translation file found (ManualTransFile.json)",
         next((p for p in trans_paths if p and os.path.exists(p)), "N/A"))

    # Playthrough log
    if log_path:
        soft(os.path.exists(log_path), "Playthrough log accessible", log_path)
    else:
        soft(False, "Playthrough log (optional — data-only mode will be used)", "N/A")

    # CG pictures
    for img_dir in [
        os.path.join(game_root, "img", "pictures"),
        os.path.join(game_root, "www", "img", "pictures"),
    ]:
        if os.path.isdir(img_dir):
            pic_count = len(os.listdir(img_dir))
            soft(True, f"CG pictures directory ({pic_count} files)", img_dir)
            results["stats"]["picture_count"] = pic_count
            break
    else:
        soft(False, "CG pictures directory", "N/A")

    # Save files
    save_dir = os.path.join(game_root, "save")
    if os.path.isdir(save_dir):
        save_count = len([f for f in os.listdir(save_dir) if f.endswith('.rmmzsave') or f.endswith('.rpgsave')])
        results["stats"]["save_count"] = save_count

    # Actor count
    actors_path = os.path.join(data_dir, "Actors.json")
    if os.path.exists(actors_path):
        with open(actors_path, 'r', encoding='utf-8') as f:
            actors = json.load(f)
        named_actors = [a for a in actors if a is not None and a.get('name', '').strip()]
        results["stats"]["actor_count"] = len(named_actors)
        results["stats"]["actors"] = [{"id": a["id"], "name": a["name"]} for a in named_actors[:30]]

    # CE count
    ce_path = os.path.join(data_dir, "CommonEvents.json")
    if os.path.exists(ce_path):
        with open(ce_path, 'r', encoding='utf-8') as f:
            ces = json.load(f)
        named_ces = [e for e in ces if e is not None and e.get('name', '').strip()]
        results["stats"]["common_event_count"] = len(named_ces)

    return results


def main():
    parser = argparse.ArgumentParser(description="Validate RPG Maker game directory for rpg-adapter pipeline")
    parser.add_argument("game_root", help="Absolute path to game root directory")
    parser.add_argument("--log", default=None, help="Path to playthrough_log.txt (optional)")
    parser.add_argument("--translation", default=None, help="Path to manual_translation.json (optional)")
    parser.add_argument("-o", "--output", help="Output JSON file path (default: stdout)")
    args = parser.parse_args()

    results = validate(args.game_root, args.log, args.translation)

    output = json.dumps(results, indent=2, ensure_ascii=False)
    if args.output:
        os.makedirs(os.path.dirname(args.output) or '.', exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Results written to {args.output}", file=sys.stderr)
    else:
        print(output)

    sys.exit(0 if results["passed"] else 1)


if __name__ == "__main__":
    main()
