#!/usr/bin/env python3
"""
Stub for RenPy AST Extractor.
In a full implementation, this would parse the .rpy file and extract dialogue, sprites, and transitions.
"""
import sys
import json
import os

def extract_ast(script_path):
    print(f"Extracting AST from {script_path}...")
    # Mock data
    context = {
        "source": script_path,
        "scenes": [
            {
                "label": "school_roof",
                "lines": 45,
                "characters": ["eileen", "kenji"],
                "backgrounds": ["bg school_roof_sunset"],
                "music": ["music sad_piano"]
            }
        ]
    }
    
    # Save to output
    output_dir = "output/demo_project"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "context.json")
    
    with open(output_path, "w") as f:
        json.dump(context, f, indent=2)
        
    print(f"Context saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: extract_renpy_ast.py <script_path>")
        sys.exit(1)
    extract_ast(sys.argv[1])
