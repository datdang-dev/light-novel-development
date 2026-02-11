import re
import argparse
import os

def extract_scene(script_path, label_name, output_file, end_label=None):
    """
    Extracts a scene starting from 'label_name'.
    If 'end_label' is provided, extracts until that label is reached (inclusive of the end label's content).
    If not, extracts only the content of 'label_name' until the next label.
    """
    
    if not os.path.exists(script_path):
        print(f"Error: File not found at {script_path}")
        return

    print(f"Scanning {script_path} for label '{label_name}'...")
    if end_label:
        print(f"   ...capturing flow until '{end_label}'")

    extracted_lines = []
    in_target_zone = False
    seen_end_label = False
    
    # Regex patterns
    start_label_pattern = re.compile(rf'^\s*label\s+{re.escape(label_name)}\s*:')
    any_label_pattern = re.compile(r'^\s*label\s+(\w+)\s*:')
    
    # Pattern to detect the end label
    end_label_pattern = None
    if end_label:
        end_label_pattern = re.compile(rf'^\s*label\s+{re.escape(end_label)}\s*:')
    
    try:
        with open(script_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            
        for i, line in enumerate(lines):
            stripped_line = line.strip()
            
            # 1. FIND START
            if not in_target_zone:
                if start_label_pattern.match(stripped_line):
                    in_target_zone = True
                    print(f"Found start label '{label_name}' at line {i+1}")
                    extracted_lines.append(f"# Scene Context: {label_name} -> {end_label if end_label else 'End of Label'}\n")
                    extracted_lines.append(f"# Source: {script_path}:{i+1}\n")
                    extracted_lines.append("-" * 40 + "\n")
                    extracted_lines.append(line) # Include the label def
                continue
            
            # 2. CHECK END CONDITIONS
            is_new_label = any_label_pattern.match(stripped_line) and not stripped_line.startswith('$') # Basic check
            
            if end_label:
                # If we found the end label previously, and we hit ANOTHER label now -> STOP
                if seen_end_label and is_new_label:
                     print(f"End of range (next label after target) at line {i+1}")
                     break
                
                # If we just hit the end label this line
                if end_label_pattern.match(stripped_line):
                    print(f"Found end label '{end_label}' at line {i+1}. Reading this block...")
                    seen_end_label = True
            
            else:
                # Single label mode: Stop at ANY new label
                # However, we must ignore jumps/calls inside the block. 
                # We assume labels are top-level.
                if is_new_label and not start_label_pattern.match(stripped_line):
                    print(f"End of scene detected (next label) at line {i+1}")
                    break

            extracted_lines.append(line)

    except Exception as e:
        print(f"Error parsing file: {e}")
        return

    # Write output
    if not extracted_lines:
        print(f"Warning: Label '{label_name}' not found in {script_path}")
        return

    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(extracted_lines)
        
    print(f"Extraction complete. Saved {len(extracted_lines)} lines to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ren'Py Scene Context Extractor")
    parser.add_argument("script_path", help="Path to the .rpy file")
    parser.add_argument("label_name", help="The label of the scene to extract")
    parser.add_argument("output_file", help="Path to save the output text file")
    parser.add_argument("--end_label", help="Optional: extraction stops after this label's block", default=None)
    
    args = parser.parse_args()
    
    extract_scene(args.script_path, args.label_name, args.output_file, args.end_label)
