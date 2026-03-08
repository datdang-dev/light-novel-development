#!/usr/bin/env python3
import sys
import json
import os

def analyze_semantics(context_path, ledger_path, spatial_path):
    if not os.path.exists(context_path):
        print(f"Error: {context_path} not found.")
        sys.exit(1)

    print(f"Analyzing semantics from {context_path}...")
    
    with open(context_path, 'r', encoding='utf-8') as f:
        context = json.load(f)

    # Load ledgers
    ledger = {}
    if os.path.exists(ledger_path):
        with open(ledger_path, 'r', encoding='utf-8') as f:
            ledger = json.load(f).get("locations", {})

    spatial = {}
    if os.path.exists(spatial_path):
        with open(spatial_path, 'r', encoding='utf-8') as f:
            spatial = json.load(f)

    scene_models = []

    for scene in context.get("scenes", []):
        model = {
            "scene_id": scene.get("label"),
            "location": {},
            "characters": [],
            "mood": "Neutral",
            "objective": "Unknown",
            "game_flags": scene.get("flags", {})
        }

        # 1. Location / Atmosphere
        bg_id = scene.get("backgrounds", [None])[0]
        if bg_id and bg_id in ledger:
            model["location"] = ledger[bg_id]
        else:
            model["location"] = {"name": bg_id or "Unknown", "desc": "Bối cảnh chưa xác định"}

        # 2. Spatial Mapping for characters
        for visual in scene.get("visuals", []):
            char_state = {
                "name": visual.get("character"),
                "expression": visual.get("expression"),
                "shot_type": "Medium Shot",
                "position_desc": "Chính diện"
            }

            # Map zoom to shot type
            zoom = visual.get("zoom", 1.0)
            for rule in spatial.get("zoom_mapping", []):
                if rule["min"] <= zoom <= rule["max"]:
                    char_state["shot_type"] = rule["shot"]
                    char_state["shot_desc"] = rule["desc"]
                    break
            
            # Map position
            pos = visual.get("position", "center")
            char_state["position_desc"] = spatial.get("position_mapping", {}).get(pos, pos)

            model["characters"].append(char_state)

        # 3. Basic Mood Inference
        # In a real tool, we'd check text sentiment or specific music tags
        if "sad" in str(scene.get("music", [])):
            model["mood"] = "Melancholic"
        elif "happy" in str(scene.get("dialogue", [])):
            model["mood"] = "Cheerful"

        scene_models.append(model)

    # Save to output
    output_dir = os.path.dirname(context_path)
    output_path = os.path.join(output_dir, "scene_model.json")
    
    with open(output_path, "w", encoding='utf-8') as f:
        json.dump(scene_models, f, indent=2, ensure_ascii=False)
        
    print(f"Scene Model saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: analyze_semantics.py <context_path> <ledger_path> <spatial_path>")
        sys.exit(1)

    project_root = "/home/datdang/working/lnd_dev/studio"
    ledger = f"{project_root}/config/atmosphere_ledger.json"
    spatial = f"{project_root}/config/spatial_mapping.json"
    
    analyze_semantics(sys.argv[1], ledger, spatial)
