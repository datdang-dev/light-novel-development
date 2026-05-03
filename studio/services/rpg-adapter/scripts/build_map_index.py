#!/usr/bin/env python3
"""Build a map index from RPG Maker Map*.json files.

Usage:
    python3 build_map_index.py <data_dir> -o <output_path>
"""
import argparse
import json
import os
import sys
from glob import glob


def build_index(data_dir: str) -> dict:
    index = {}
    map_files = sorted(glob(os.path.join(data_dir, "Map*.json")))

    for map_file in map_files:
        basename = os.path.basename(map_file)
        # Extract map ID from filename (e.g., Map001.json -> 1)
        map_id_str = basename.replace("Map", "").replace(".json", "")
        try:
            map_id = int(map_id_str)
        except ValueError:
            continue

        try:
            with open(map_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            display_name = data.get("displayName", "") or f"Map {map_id}"
            index[str(map_id)] = {
                "file": basename,
                "display_name": display_name,
                "width": data.get("width", 0),
                "height": data.get("height", 0),
                "event_count": len(data.get("events", []) or []),
            }
        except (json.JSONDecodeError, IOError) as e:
            index[str(map_id)] = {
                "file": basename,
                "display_name": f"Map {map_id} (parse error)",
                "error": str(e),
            }

    return {"total_maps": len(index), "maps": index}


def main():
    parser = argparse.ArgumentParser(description="Build map index from RPG Maker Map*.json files")
    parser.add_argument("data_dir", help="Path to www/data/ directory containing Map*.json")
    parser.add_argument("-o", "--output", required=True, help="Output JSON file path")
    args = parser.parse_args()

    if not os.path.isdir(args.data_dir):
        print(f"Error: {args.data_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    index = build_index(args.data_dir)

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    print(f"Map index built: {index['total_maps']} maps → {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
