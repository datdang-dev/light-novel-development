#!/usr/bin/env python3
import os
import json
import sys

def index_assets(game_dir):
    images_dir = os.path.join(game_dir, "images")
    if not os.path.exists(images_dir):
        print(f"Error: {images_dir} not found.")
        return

    manifest = {
        "backgrounds": {},
        "sprites": {},
        "others": []
    }

    print(f"Indexing assets in: {images_dir}...")

    for root, dirs, files in os.walk(images_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.webp')):
                rel_path = os.path.relpath(os.path.join(root, file), game_dir)
                filename = os.path.splitext(file)[0]
                
                # Logic: Infer type from directory or filename tokens
                if "bg" in rel_path.lower() or "background" in rel_path.lower():
                    manifest["backgrounds"][filename] = {
                        "path": rel_path,
                        "description": "PENDING_ANALYSIS",
                        "atmosphere": "unknown"
                    }
                elif "sprite" in rel_path.lower() or any(c in filename.lower() for c in ["side", "face", "body"]):
                    manifest["sprites"][filename] = {
                        "path": rel_path,
                        "character": filename.split('_')[0],
                        "expression": "neutral",
                        "description": "PENDING_ANALYSIS"
                    }
                else:
                    manifest["others"].append(rel_path)

    output_path = "output/renpy_context/visual_manifest.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)

    print(f"Indexed {len(manifest['backgrounds'])} backgrounds and {len(manifest['sprites'])} sprites.")
    print(f"Manifest saved to: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: index_assets.py <game_root_directory>")
        sys.exit(1)
    index_assets(sys.argv[1])
