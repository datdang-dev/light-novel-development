import re
import argparse
import os

def parse_script(script_path, character_tag, output_file):
    """
    Parses a Ren'Py script file to extract dialogue for a specific character,
    including the preceding context (line) and active sprite tags.
    """
    
    if not os.path.exists(script_path):
        print(f"Error: File not found at {script_path}")
        return

    print(f"Scanning {script_path} for character '{character_tag}'...")

    results = []
    
    # Regex patterns
    # Matches: a "Dialogue content"
    dialogue_pattern = re.compile(rf'^\s*{re.escape(character_tag)}\s+"(.*?)"')
    
    # Matches: show character_tag tag1 tag2
    # Simplified parsing: looks for 'show' statements
    show_pattern = re.compile(r'^\s*show\s+(\w+)\s*(.*)')
    
    # Matches: scene bg_name
    scene_pattern = re.compile(r'^\s*scene\s+(.*)')
    
    current_scene = "Unknown"
    active_sprites = {} # Map character_name -> [tags]
    prev_line_text = "start of script"
    
    count = 0
    
    try:
        with open(script_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            
        for i, line in enumerate(lines):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            # Track Scene
            scene_match = scene_pattern.match(line)
            if scene_match:
                current_scene = scene_match.group(1)
                active_sprites = {} # Reset sprites on new scene? usually yes in Renpy unless overlap
                prev_line_text = f"[Scene Change: {current_scene}]"
                continue

            # Track Shows (rudimentary)
            show_match = show_pattern.match(line)
            if show_match:
                char_name = show_match.group(1)
                tags = show_match.group(2)
                active_sprites[char_name] = tags
                # Don't update prev_line_text for show commands, keep the last dialogue/narration
                continue
                
            # Check for Target Dialogue
            dialogue_match = dialogue_pattern.match(line)
            if dialogue_match:
                content = dialogue_match.group(1)
                
                # Get sprite context for this character if available
                # Assuming character_tag maps to the sprite name used in 'show' 
                # (Start simple: User might need to specify sprite name if different from char tag)
                # For now, print all active sprites to be safe
                sprite_context = str(active_sprites)
                
                entry = f"Context: {prev_line_text}\nSprite: {sprite_context}\n{character_tag}: \"{content}\"\n"
                results.append(entry)
                results.append("-" * 40 + "\n")
                count += 1
                
                # Update prev line for next iteration
                prev_line_text = f"{character_tag}: \"{content}\""
            
            else:
                # It's some other line (narration or other char info)
                # Clean it up a bit if it's dialogue
                # Simple check for quoted string
                if '"' in line:
                    prev_line_text = line
                
    except Exception as e:
        print(f"Error parsing file: {e}")
        return

    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(results)
        
    print(f"Extraction complete. Found {count} lines. Saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ren'Py Dialogue Extractor")
    parser.add_argument("script_path", help="Path to the .rpy file")
    parser.add_argument("character_tag", help="The character variable name (e.g., 'a' for Asuka)")
    parser.add_argument("output_file", help="Path to save the output text file")
    
    args = parser.parse_args()
    
    parse_script(args.script_path, args.character_tag, args.output_file)
