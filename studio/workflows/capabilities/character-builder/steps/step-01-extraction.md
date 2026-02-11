# Step 1: Character Dialogue Extraction

**Goal:** Create a massive dataset of "Raw Voice" to train the AI on the character's nuances.

## Input Required

- **`script_path`**: Path to the Ren'Py `.rpy` file (e.g., `/mnt/d/WaifuAcademy/script.rpy`).
- **`character_tag`**: The variable name used for the character (e.g., `a` for Asuka in `define a = Character(...)`).

## Process

1. **Run Extraction Script:**
    Execute the python script to scan the file and extract every line of dialogue spoken by this character, packaged with the *preceding line* (context) and *active sprite tags* (visual emotion).

    ```bash
    python3 studio/scripts/extract_dialogue.py "{script_path}" "{character_tag}" "raw_{character_tag}_corpus.txt"
    ```

2. **Verify Output:**
    Check `raw_{character_tag}_corpus.txt` to ensure it contains:
    - Context (What happened before?)
    - Sprite State (What face were they making?)
    - Dialogue (What did they say?)

## Output

- **`raw_{character_tag}_corpus.txt`**: A text file containing ~1000+ interactions.

## Next Step

Proceed to **[Step 2: Voiceprint Analysis](./step-02-analysis.md)** to condense this raw data into a psychological profile.
