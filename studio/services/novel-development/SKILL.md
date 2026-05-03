---
name: novel-development
description: 'Ultimate Novel Development Pipeline — A slow-paced, deeply contextualized
  narrative engine. Orchestrated flow: Kana (Visuals) -> Luna (World/Pacing) -> Suki
  (Long-form Prose).'
injection:
  always:
  - '{{project_root}}/studio/rules/user_fetish_profile.md'
  - '{{project_root}}/studio/rules/xcom_degenerate_style.md'
  triggers:
  - scene_tag: explicit|r18|sexual
    loads:
    - '{{project_root}}/studio/knowledge/packs/arousal_architecture.md'
    - '{{project_root}}/studio/knowledge/packs/fetish_guidance_pack.md'
  - scene_tag: world-building|intro
    loads:
    - '{{project_root}}/studio/knowledge/packs/japanese_reader_psychology.md'
dependencies:
  knowledge:
  - path: '{{project_root}}/studio/rules/user_fetish_profile.md'
  - path: '{{project_root}}/studio/rules/xcom_degenerate_style.md'
  modules: []
---

# Novel Development Pipeline (ND)

## Overview

The Novel Development Pipeline is a heavy-weight narrative engine designed to produce **full-length, slow-paced novels** rather than short captions or quick adaptations. 

It explicitly forces coordination between **Luna (World Weaver)** and **Suki (Lewd Writer)** to ensure that world-building, character motivations, and slow-burn pacing are established *before* any explicit prose is written.

**Core Philosophy:** A novel requires an anchor. We cannot rush to the climax. We must build the world, the rules, the stakes, and the suppressed desires before breaking them.

**Pipeline Position:** `Kana (Optional Forensic) → **Luna (Novel Outline & World Building)** → **Suki (Chapter Prose Generation)** → Riko (Audit)`

## Architecture

This pipeline runs sequentially:

### Step 1: Initialization & Context Gathering
- Accept user prompt and any reference images.
- If images exist, delegate to **Kana** to extract `forensic.md` (visual tags, expressions, clothing).

### Step 2: Luna's World Weaving (`novel_outline.md`)
- **Agent:** Luna
- **Input:** User prompt + `forensic.md`
- **Action:** Luna generates a comprehensive `novel_outline.md`.
- **Requirements for Outline:**
  - **World Building:** Lore, rules, religious/societal constraints.
  - **Character Profiles:** Detailed backstory, hidden desires, the "facade" vs the "reality".
  - **The "Why":** The logical, world-consistent reason why the character is in the erotic situation (e.g., "Investigating Mana Crystals" to hide sexual frustration).
  - **Chapter Breakdown (Pacing):** A structured roadmap of chapters (e.g., Chapter 1: The Setup, Chapter 2: The Trap, Chapter 3: The Breaking). Pacing MUST be slow.

### Step 3: Suki's Prose Expansion (`novel_chapter_X.md`)
- **Agent:** Suki
- **Input:** `novel_outline.md` + Fetish Profiles
- **Action:** Suki generates the actual novel text, one chapter at a time.
- **Requirements for Prose:**
  - Strictly adhere to Luna's pacing. Do not jump to sex in Chapter 1 if it's meant for Chapter 3.
  - Maximize sensory density (sweat, nylon indentations, smells).
  - Exploit the user's fetish profile (e.g., Bratty, Degradation, Scent).

### Step 4: Riko's Quality Audit
- **Agent:** Riko
- **Input:** The drafted chapters.
- **Action:** Check against Canon Rules and Anti-Slop gates. Reject if pacing is too fast or if language is generic.

## Execution Triggers

When the user calls `/novel-development` or requests a "rework of the novel pipeline", Director K must:
1. Acknowledge the shift to the **ND Pipeline**.
2. Request the initial context/images from the user.
3. Call **Luna** to draft the `novel_outline.md` first.
4. Wait for user approval of the outline before calling **Suki** to write the chapters.
