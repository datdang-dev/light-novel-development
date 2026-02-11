---
name: "renpy-adaptation"
description: "Pipeline: Ren'Py Game -> Light Novel (Context-Aware)"
owner: "Director K (lnd-orchestrator)"
version: "1.0.0"
---

# Ren'Py Adaptation Pipeline 🕹️➡️📖

**Goal:** Adapt a Ren'Py game scene into a Light Novel chapter using the Game Script as the "Truth" and the Studio Agents for "Creativity".

## 🔄 The Flow

1. **Input (User + Adapter):** User selects a Scene/Label. Adapter mines the context.
2. **Visuals (Forensics):** Atomic analyzes the extracted assets (CGs, Sprites, BGs).
3. **Dialogue (Miki):** Miki refines the raw script into Novel-ready dialogue.
4. **Prose (Suki):** Suki merges Visuals + Dialogue into Scene Prose.
5. **Audit (Riko):** Quality Control.

---

## 🛠️ Execution Steps

### Step 1: Context Mining (The Handshake)

**Agent:** `renpy-adapter`
**Action:** Interactive session to identify the scope.

- **User:** Provides `label` (e.g., `d31restroom_asuka`).
- **Adapter:**
  - Extracts Raw Script (Dialogue tree).
  - Identifies Assets (Background file names, Sprite tags).
  - *Output:* `context_scene_{label}.md` (The "Bible" for this scene).

### Step 2: Visual Forensics (The Eye)

**Agent:** `panel-forensic` (Prof. Atomic)
**Action:** Analyze the visual assets identified in Step 1.

- **Input:** `context_scene_{label}.md` (List of image files).
- **Process:** detailed description of the environment and character states.
- **Output:** `visual_forensics_{label}.md`.

### Step 3: Production (The Craft)

**Agents:** `dialogue-crafter` (Miki) & `lewd-writer` (Suki)
**Action:** Standard Studio Production.

- **Input:**
  - Context (Script)
  - Forensics (Visuals)
  - Character Bible (Profiles)
- **Output:** `draft_chapter_{label}.md`

---

## 📝 Usage for Director K

When User requests: *"Adapt scene X from the game"* -> **Run this pipeline.**
