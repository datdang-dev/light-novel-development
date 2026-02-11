---
description: "Data mining workflow to extract character dialogue and context from Ren'Py scripts to build psychological profiles."
---

# Character Builder Workflow

**Goal:** Create a high-fidelity "Voiceprint" and Psychological Profile for a specific character by mining the game script.

## Workflow Structure

1. **[Step 1: Context Extraction](./steps/step-01-extraction.md)**
    - **Input:** `script.rpy` path, Character Variable (e.g., `a`).
    - **Action:** Python script scans game files.
    - **Output:** `raw_{char}_corpus.txt` (1000+ lines of dialogue + context).

2. **[Step 2: Voiceprint Analysis](./steps/step-02-analysis.md)**
    - **Input:** `raw_{char}_corpus.txt`.
    - **Action:** AI analyzes speech patterns, triggers, and kinks.
    - **Output:** `analysis_{char}.md`.

3. **[Step 3: Profile Generation](./steps/step-03-profile-generation.md)**
    - **Input:** `analysis_{char}.md`.
    - **Action:** Synthesize into a "System Prompt" format.
    - **Output:** `studio/profiles/{char}_profile.md`.

## Usage

Run this workflow when you want to "onboard" a new character into the LND Studio knowledge base.
