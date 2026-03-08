# Workflow: Universal Ren'Py Adaptation

This workflow describes the standardized 5-step process for adapting any Ren'Py-based game into a high-fidelity AI roleplay environment within LND Studio.

## Phase 1: Forensic Survey

- **Objective**: Map the game's file structure and identify key assets.
- **Actions**:
  1. Scan `game/` for `.rpy` scripts and `images/` for assets.
  2. Identify the primary `script.rpy` and any supplemental variable files (e.g., `game_vars.rpy`).
  3. Detect character IDs used in `define character` lines.

## Phase 2: Visual Asset Audit (Kana)

- **Objective**: Provide the AI with a "visual memory" of characters and locations.
- **Actions**:
  1. Process the `images/bg/` and `images/sprites/` folders.
  2. Use the Forensic Engine to generate a **Visual Context Ledger** (descriptions of backgrounds and character designs).
  3. Map script-level `bg` and `show` tags to these descriptions.

## Phase 3: Semantic Extraction (Ren)

- **Objective**: Extract narrative beats, flags, and character logic.
- **Actions**:
  1. Run the `extract_renpy_ast.py` with the Hybrid Engine.
  2. Generate a `universal_context.json` containing:
     - All character definitions and name mappings.
     - Global and scene-specific flags.
     - Dialogue and visual cues organized by labels.

## Phase 4: Character Bible Generation

- **Objective**: Create a structured profile for the Roleplay Actor.
- **Actions**:
  1. Synthesize the Semantic Model and Visual Ledger into a `character_bible.md`.
  2. Use the **Context Sharding** mechanism to segment the bible into modular chunks (Core, Sexual, Social).

## Phase 5: Roleplay Fusion & Activation (Yua)

- **Objective**: Initiate the roleplay with full situational awareness.
- **Actions**:
  1. Enforce the **Context Pre-Flight** protocol.
  2. Yua reads the relevant Shards, the Visual Ledger, and the current Scene Anchor.
  3. Start the roleplay session using the **Dynamic Context Horizon** strategy.

---
**CRITICAL**: All Vietnamese output must strictly follow the `pervert_pov` and `lewd_writing_mechanics`. Visual details from Phase 2 MUST be incorporated into Yua's sensory descriptions.
