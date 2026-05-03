#!/usr/bin/env python3
import sys
import json
import os
import re

def extract_ast(script_path):
    if not os.path.exists(script_path):
        print(f"Error: {script_path} not found.")
        sys.exit(1)

    print(f"Parsing RenPy script: {script_path}...")
    
    with open(script_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    context = {
        "source": script_path,
        "characters": {},
        "global_flags": {},
        "scenes": []
    }

    # Enhanced Regex Patterns for Universal Discovery
    char_def_pat = re.compile(r'define\s+(\w+)\s*=\s*Character\("([^"]+)"')
    label_pat = re.compile(r'label\s+(\w+):')
    show_pat = re.compile(r'show\s+(\w+)\s*([\w\s]*)')
    at_pat = re.compile(r'at\s+(\w+)')
    zoom_pat = re.compile(r'zoom\s+([\d.]+)')
    say_pat = re.compile(r'(\w+)?\s+"([^"]+)"')
    var_pat = re.compile(r'\$\s+(\w+)\s*=\s*([\w\d\(\)\'"]+)')
    default_var_pat = re.compile(r'default\s+(\w+)\s*=\s*([\w\d\(\)\'"]+)')

    current_scene = None

    for line in lines:
        line_clean = line.strip()
        if not line_clean or line_clean.startswith('#'):
            continue

        # Global Character Discovery
        char_match = char_def_pat.search(line_clean)
        if char_match:
            context["characters"][char_match.group(1)] = {
                "name": char_match.group(2),
                "vars": []
            }
            continue

        # Global Variable Discovery
        def_var_match = default_var_pat.search(line_clean)
        if def_var_match:
            context["global_flags"][def_var_match.group(1)] = def_var_match.group(2)
            continue

        # Label / Scene detection
        label_match = label_pat.search(line_clean)
        if label_match:
            if current_scene:
                context["scenes"].append(current_scene)
            current_scene = {
                "label": label_match.group(1),
                "visuals": [],
                "dialogue": [],
                "flags": {}
            }
            continue

        if not current_scene:
            continue

        # Show / Sprites
        if line_clean.startswith('show'):
            show_match = show_pat.search(line_clean)
            if show_match:
                sprite = {
                    "character": show_match.group(1),
                    "expression": show_match.group(2).strip(),
                    "position": "center",
                    "zoom": 1.0
                }
                at_match = at_pat.search(line_clean)
                if at_match:
                    sprite["position"] = at_match.group(1)
                zoom_match = zoom_pat.search(line_clean)
                if zoom_match:
                    sprite["zoom"] = float(zoom_match.group(1))
                current_scene["visuals"].append(sprite)

        # Dialogue
        say_match = say_pat.search(line_clean)
        # Avoid matching 'show' as dialogue
        if say_match and not line_clean.startswith('show') and not line_clean.startswith('image'):
            current_scene["dialogue"].append({
                "who": say_match.group(1) or "narrator",
                "text": say_match.group(2)
            })

        # Inline Flags
        var_match = var_pat.search(line_clean)
        if var_match:
            current_scene["flags"][var_match.group(1)] = var_match.group(2)

    if current_scene:
        context["scenes"].append(current_scene)

    # Output Logic
    output_dir = "output/renpy_context"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "universal_context.json")
    
    with open(output_path, "w", encoding='utf-8') as f:
        json.dump(context, f, indent=2, ensure_ascii=False)
        
    print(f"Universal extraction complete: {len(context['characters'])} characters, {len(context['scenes'])} scenes found.")
    print(f"Log saved to: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: extract_renpy_ast.py <script_file.rpy>")
        sys.exit(1)
    extract_ast(sys.argv[1])
