---
name: "renpy-adaptation"
description: "Pipeline: Ren'Py -> Semantics -> Kana (V6)"
owner: "Ren'Py Adapter (renpy-adapter)"
version: "6.0.0"
web_bundle: true
validateWorkflow: './steps/step-01-ast-mining.md'
---

# Ren'Py Adaptation Pipeline (V6)

**Goal:** Adapt Ren'Py scripts into Light Novel prose by Extracting Truth (AST), Modeling Meaning (Semantics), and Delegating Creation (Kana).

**Architecture:**

- **Step 1:** [AST Mining](./steps/step-01-ast-mining.md) - Extract raw data (Dialogue, Sprites, BGs).
- **Step 2:** [Semantic Modeling](./steps/step-02-semantic-model.md) - Convert data to Mood/Objectives.
- **Step 3:** [Delegation to Kana](./steps/step-03-delegate.md) - Hand off Scene Model for Prose Generation.

## Execution Flow

1. **Initialize:** `renpy-adapter` receives `.rpy` file.
2. **Mine:** Run `extract_renpy_ast.py` -> `context.json`.
3. **Analyze:** Run `analyze_semantics.py` -> `scene_model.json`.
4. **Delegate:** Loop through scenes, calling `manga-adapter` triggers.
