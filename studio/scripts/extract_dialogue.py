import re
import argparse
import os

def parse_script(script_path, character_tag, output_file):
    """
    Parses a Ren'Py script file (or directory of files) to extract dialogue for a specific character.
    """
    
    files_to_process = []
    if os.path.isdir(script_path):
        for root, dirs, files in os.walk(script_path):
            for file in files:
                if file.endswith(".rpy"):
                    files_to_process.append(os.path.join(root, file))
    else:
        files_to_process.append(script_path)

    print(f"Scanning {len(files_to_process)} files for character '{character_tag}'...")
    
    total_count = 0
    all_results = []

    # Regex patterns
    dialogue_pattern = re.compile(rf'^\s*{re.escape(character_tag)}\s+"(.*?)"')
    show_pattern = re.compile(r'^\s*show\s+(\w+)\s*(.*)')
    scene_pattern = re.compile(r'^\s*scene\s+(.*)')

    for file_path in files_to_process:
        try:
            # print(f"  - Processing {os.path.basename(file_path)}...") 
            current_scene = "Unknown"
            active_sprites = {} 
            prev_line_text = "start of file"
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                
            for i, line in enumerate(lines):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                    
                # Track Scene
                scene_match = scene_pattern.match(line)
                if scene_match:
                    current_scene = scene_match.group(1)
                    active_sprites = {} 
                    prev_line_text = f"[Scene Change: {current_scene}]"
                    continue

                # Track Shows
                show_match = show_pattern.match(line)
                if show_match:
                    char_name = show_match.group(1)
                    tags = show_match.group(2)
                    active_sprites[char_name] = tags
                    continue
                    
                # Check for Target Dialogue
                dialogue_match = dialogue_pattern.match(line)
                if dialogue_match:
                    content = dialogue_match.group(1)
                    
                    # Context info
                    sprite_context = str(active_sprites)
                    origin = os.path.basename(file_path)
                    
                    entry = f"File: {origin}\nContext: {prev_line_text}\nSprite: {sprite_context}\n{character_tag}: \"{content}\"\n"
                    all_results.append(entry)
                    all_results.append("-" * 40 + "\n")
                    total_count += 1
                    
                    prev_line_text = f"{character_tag}: \"{content}\""
                
                else:
                    if '"' in line:
                        prev_line_text = line
                        
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")

    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(all_results)
        
    print(f"Extraction complete. Found {total_count} lines. Saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ren'Py Dialogue Extractor")
    parser.add_argument("script_path", help="Path to the .rpy file or directory")
    parser.add_argument("character_tag", help="The character variable name (e.g., 'a' for Asuka)")
    parser.add_argument("output_file", help="Path to save the output text file")
    
    args = parser.parse_args()
    
    parse_script(args.script_path, args.character_tag, args.output_file)
