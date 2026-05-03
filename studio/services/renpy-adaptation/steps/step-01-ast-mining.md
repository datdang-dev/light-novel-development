# Step 1: AST Mining (Context Extraction)

**Agent:** `renpy-adapter`
**Action:** Extract Raw State from Ren'Py Script.

## Instructions

1. **Locate Target:** Identify the `.rpy` script provided in the input.
2. **Run Tool:** Execute `tools/extract_renpy_ast.py` against the script.
3. **Validate Output:** Ensure `output/{project}/context.json` is created.
4. **Verify Integrity:** Check that `context.json` contains:
    - `dialogue_lines` (List)
    - `sprite_tags` (Set)
    - `backgrounds` (List)
    - `audio_cues` (List)

## Output Payload

```json
{
  "source": "script.rpy",
  "scenes": [
    {
      "label": "school_roof",
      "lines": 45,
      "characters": ["eileen", "kenji"]
    }
  ]
}
```
