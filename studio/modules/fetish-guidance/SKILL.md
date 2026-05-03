---
name: fetish-guidance
description: "Fetish pattern and escalation guidance module — provides research-backed fetish-specific writing patterns, do's/don'ts, and combination strategies from 30+ research files. Integrates with lewd-writer and scene-expansion to enforce kink-appropriate escalation pacing."
owner: "datdang"
version: "1.0.0"
tags: [fetish, escalation, kink, research, mindbreak, ntr, creampie]
injection:
  always:
    - "{{project_root}}/studio/rules/canon-rules.md"
    - "{{project_root}}/studio/rules/user_fetish_profile.md"
  triggers:
    - scene_tag: "explicit|r18|sexual|mindbreak|ntr|fetish"
      loads:
        - "{{project_root}}/studio/knowledge/packs/fetish_guidance_pack.md"
        - "{{project_root}}/studio/knowledge/fetish-db/mindbreak_research.md"
dependencies:
  knowledge:
    - path: "{{project_root}}/studio/knowledge/packs/fetish_guidance_pack.md"
    - path: "{{project_root}}/studio/knowledge/fetish-db/mindbreak_research.md"
    - path: "{{project_root}}/studio/knowledge/fetish-db/ntr_research.md"
    - path: "{{project_root}}/studio/knowledge/fetish-db/creampie_research.md"
    - path: "{{project_root}}/studio/knowledge/fetish-db/anal_research.md"
    - path: "{{project_root}}/studio/knowledge/trope_beat_sheets/mindbreak_beats.md"
    - path: "{{project_root}}/studio/knowledge/trope_beat_sheets/corruption_beats.md"
  modules: []
---

## Capabilities

### 1. Fetish Detection

Parse scene tags and identify relevant fetishes with primary/secondary/tertiary ranking.

### 2. Pattern Library

Retrieve escalation patterns (e.g., mindbreak's 5 phases: Resistance → Confusion → Crack → Fall → Completion).

### 3. Do's and Don'ts

Fetish-specific writing rules (what to emphasize, what to avoid, pacing).

### 4. Combination Guidance

How to blend multiple fetishes effectively (e.g., mesugaki + mindbreak = confident start → satisfying break).
