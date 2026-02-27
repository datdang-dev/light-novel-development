#!/usr/bin/env python3
"""
Context Horizon Generator (Universal Look-Ahead Engine)
Analyzes N upcoming frames/pages to establish a strict Scene Trajectory.

Usage:
    python generate_horizon.py --state <state_file> --mode <video|manga> --window <N> --out <output_file>
"""

import argparse
import os
import sys
import yaml
from pathlib import Path

def generate_horizon_summary(image_files, mode, start_index):
    """
    Simulates the Vision Model call.
    In a real environment, this would pass the batch of images to an LLM/VLM.
    """
    total = len(image_files)
    print(f"👁️ Analyzing Horizon Window: {total} {mode} frames ahead...")
    
    # Placeholder for actual Vision LLM logic
    summary = f"""# Context Horizon: Scene Trajectory

**Medium:** {mode.capitalize()}
**Look-Ahead Window:** {total} upcoming images (Start: {start_index})

## 1. Concrete Trajectory (Foreshadowing Ground Truth)
- [VISION MODEL] The action will escalate towards...
- [VISION MODEL] Guaranteed events in the next {total} frames: ...

## 2. Action Deduplicator Flag
- **Redundancy Detected:** [True/False]
- **Merge Recommendation:** 
  - If redundant thrusting or static posing is detected across these frames, MERGE them into a single intense Action Beat in the Prose Generation step.
  - DO NOT write 1-for-1 page prose if the action is static.

---
*CRITICAL FOR SUKI (LEWD WRITER):* Use this trajectory to foreshadow the climax. Do not treat the current frame in isolation.
"""
    return summary

def main():
    parser = argparse.ArgumentParser(description='Context Horizon Look-Ahead Engine')
    parser.add_argument('--state', required=True, help='Path to pipeline state.yaml')
    parser.add_argument('--mode', required=True, choices=['video', 'manga'], help='Medium type for horizon scale')
    parser.add_argument('--window', type=int, default=5, help='Number of upcoming frames/pages to analyze')
    parser.add_argument('--out', required=True, help='Path to output context_horizon.md')
    
    args = parser.parse_args()
    
    # 1. Read State File
    if not os.path.exists(args.state):
        print(f"Error: State file not found: {args.state}")
        sys.exit(1)
        
    with open(args.state, 'r', encoding='utf-8') as f:
        state = yaml.safe_load(f)
        
    current_page = int(state.get('current_page', 1))
    source_folder = state.get('source_folder', '')
    
    if not os.path.exists(source_folder):
        print(f"Error: Source folder not found: {source_folder}")
        sys.exit(1)
        
    # 2. Gather Horizon Window Images
    # Sort files naturally
    all_files = sorted([f for f in os.listdir(source_folder) if f.lower().endswith(('.jpg', '.png', '.webp'))])
    
    if not all_files:
        print(f"Error: No images found in {source_folder}")
        sys.exit(1)
        
    # Find current index
    try:
        current_index = current_page - 1 # Assuming 1-based indexing for simple test
    except ValueError:
        current_index = 0
        
    # Slice the horizon window
    horizon_files = all_files[current_index:current_index + args.window]
    
    if not horizon_files:
        print("Warning: Horizon window is empty. No future frames available.")
        sys.exit(0)
        
    # 3. Generate Summary
    horizon_content = generate_horizon_summary(horizon_files, args.mode, current_page)
    
    # 4. Write Output
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, 'w', encoding='utf-8') as f:
        f.write(horizon_content)
        
    print(f"✅ Context Horizon generated at: {args.out}")
    print(f"   Window spanned {len(horizon_files)} images.")

if __name__ == '__main__':
    main()
