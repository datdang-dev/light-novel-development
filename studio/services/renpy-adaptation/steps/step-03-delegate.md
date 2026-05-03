# Step 3: Delegation to Kana (Manga Adapter)

**Agent:** `renpy-adapter`
**Action:** Hand off the Semantic Model to the Prose Specialist.

## Instructions

1. **Load Model:** Read `output/{project}/scene_model.json`.
2. **Package Assets:** Identify the Image Assets associated with the scene (Background + Character Sprites).
3. **Construct Prompt:**
    > "Kana, please adapt this scene.
    > Context: [Scene Model content]
    > Image: [Composite or Reference Image]
    > Dialogue: [Dialogue Block]"
4. **Delegate:** Trigger `manga-adapter` (via `gooner-alchemist` pipeline) with the packaged input.
5. **Await Result:** Wait for Kana to return the `draft.md`.
6. **Aggregate:** Compile the returned drafts into the final chapter.

## Validation

- Ensure Kana receives the *Interpretation* (Semantic Model), not just the *Raw Data*.
- Verify Kana's output matches the `dialogue_lines` count from Step 1.
