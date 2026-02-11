---
name: 'step-01-context'
description: 'Activate Ren'Py Adapter to mine scene context'
nextStepFile: './step-02-forensics.md'
---

# Step 1: Context Mining

## STEP GOAL

Extract the raw dialogue and scene description from the Ren'Py game script.

## EXECUTION

1. **Activate Agent:** Load and activate `studio/agents/L2_developers/renpy-adapter.md`.
    * *Note:* Ensure the agent is loaded with the [EX] (Extract) capability.
2. **Execute Extraction:** Run the extraction command for the target label.
    * **Command:** `python3 studio/scripts/extract_scene_context.py ...`
    * **Input:** User provided label (e.g. `d31helenoffice`).
3. **Validate:** Ensure `studio/generated/{scene}_context.txt` is created and contains text.
4. **Save State:** Note the path of the generated context file.
5. **Proceed:** Once complete, load `step-02-forensics.md`.
