#!/usr/bin/env python3
import json
import os
import sys
import glob

def generate_knowledge_payload(forensic_state_path, payload_output_path, knowledge_dir):
    try:
        with open(forensic_state_path, 'r', encoding='utf-8') as f:
            state = json.load(f)
    except FileNotFoundError:
        print(f"Error: {forensic_state_path} not found.")
        sys.exit(1)

    tags = set(state.get("content_tags", []))
    if not tags:
        print("No content tags found in forensic state. Proceeding with empty payload.")
        with open(payload_output_path, 'w', encoding='utf-8') as f:
            f.write("# Knowledge Payload\n\nNo specific context tags detected.\n")
        return

    print(f"Searching for tags: {list(tags)}")
    
    # We will score files based on tag hits
    file_scores = {}
    
    # Search through all markdown files in knowledge directory
    for root, _, files in os.walk(knowledge_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                score = 0
                
                # Check filename first (higher weight)
                file_basename = os.path.basename(file).lower()
                for tag in tags:
                    if tag.lower() in file_basename:
                        score += 5
                
                # Check content (if no big hit on filename, do a quick scan)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read().lower()
                        for tag in tags:
                            if tag.lower() in content:
                                score += 1
                except Exception:
                    pass
                
                if score > 0:
                    file_scores[file_path] = score

    # Sort files by score and take top 2
    sorted_files = sorted(file_scores.items(), key=lambda item: item[1], reverse=True)
    top_files = sorted_files[:2]

    payload_content = "# Knowledge Payload (JIT RAG)\n\n"
    payload_content += "Based on the content tags from the forensic analysis, the following research files have been loaded for your context:\n\n"
    
    if top_files:
        for file_path, score in top_files:
            payload_content += f"## Source: `{os.path.basename(file_path)}` (Relevance Score: {score})\n\n"
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    payload_content += content + "\n\n---\n\n"
            except Exception as e:
                payload_content += f"[Error reading file: {e}]\n\n"
    else:
        payload_content += "*No highly relevant research files found for these tags.*\n"

    with open(payload_output_path, 'w', encoding='utf-8') as f:
        f.write(payload_content)

    print(f"Generated {payload_output_path} with {len(top_files)} research files included.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 knowledge_injector.py <path_to_forensic_state.json> <output_payload.md> <knowledge_dir>")
        sys.exit(1)
    
    generate_knowledge_payload(sys.argv[1], sys.argv[2], sys.argv[3])
