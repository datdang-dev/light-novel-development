# Step 2: Semantic Modeling (Logic to Meaning)

**Agent:** `renpy-adapter`
**Action:** Convert Raw AST Data into Narrative Semantics.

## Instructions

1. **Load Context:** Read `output/{project}/context.json`.
2. **Run Tool:** Execute `tools/analyze_semantics.py` with the context.
3. **Analyze Mood:** Determine the emotional tone based on music, sprites (`eileen_angry`), and punctuation.
4. **Determine Objective:** What is the goal of this scene? (e.g., "Confession", "Argument", "Exposition").
5. **Save Artifact:** Write to `output/{project}/scene_model.json`.

## Output Payload

```json
{
  "scene_id": "school_roof",
  "mood": "Melancholic but hopeful",
  "lighting": "Sunset (derived from bg sunset)",
  "objective": "Kenji tries to apologize to Eileen",
  "tension_level": "Medium",
  "key_context": "Eileen is refusing to look at him (sprite: lookaway)"
}
```
