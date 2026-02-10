#!/usr/bin/env python3
import sys
import re
import os

def check_file(filepath):
    """
    Checks a markdown file for LND Studio violations.
    """
    if not os.path.exists(filepath):
        print(f"Error: File not found - {filepath}")
        return

    print(f"Scanning {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    errors = []
    
    # Banned words list (from lewd-writer.md)
    banned_words = [
        "hôi thối", "dơ bẩn", "bẩn thỉu", "ghê tởm",
        "đê tiện", "đáng khinh", "ô uế",
        "birth canal", "manhood"
    ]

    for i, line in enumerate(lines):
        line_num = i + 1
        content = line.strip()
        
        # 1. Check for Standard Quotes in Dialogue
        # Heuristic: Text inside double quotes that looks like dialogue
        # We ignore headers, code blocks (basic check)
        if '"' in content and not content.startswith(('#', '-', '*', '>', '`')):
            # Simple check: if a line contains quotes, it might be using standard quotes instead of brackets
            # We assume dialogue lines usually start with quotes or Name: "..."
            if re.search(r'".+"', content):
                 errors.append(f"Line {line_num}: Standard quotes detected. Use Japanese brackets 「...」 for dialogue.")

        # 2. Check for Standard Parentheses in Thoughts
        # Heuristic: Text inside (...) that looks like thought bubble
        if '(' in content and ')' in content and not content.startswith(('#', '-', '*', '>', '`', '[')):
             # Ignore markdown links [text](url)
             if not re.search(r'\[.*\]\(.*\)', content):
                if re.search(r'\(.+\)', content):
                    errors.append(f"Line {line_num}: Standard parentheses detected. Use Japanese brackets （...） for thoughts/internal monologue.")

        # 3. Banned Words Check
        for word in banned_words:
            if word.lower() in content.lower():
                errors.append(f"Line {line_num}: Banned word detected: '{word}'")

    if errors:
        print(f"\n❌ FOUND {len(errors)} ISSUES:")
        for err in errors:
            print(err)
        sys.exit(1)
    else:
        print("\n✅ NO FORMATTING ERRORS FOUND.")
        sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 ln_linter.py <file_path>")
        sys.exit(1)
    
    check_file(sys.argv[1])
