---
name: rpg-adapter
description: RPG Maker MV/MZ game-to-novel adaptation pipeline — specializes in extracting
  quest timelines, companion join conditions, R18 scene prerequisites, and assembling
  them into a chronologically correct novel script. Use when the user says 'adapt
  RPG game', 'extract game timeline', 'RPG to novel', 'map R18 scenes to chapters',
  or 'build novel from game data'.
injection:
  always:
  - '{{project_root}}/studio/knowledge/packs/narrative_style_pack.md'
  triggers:
  - scene_tag: explicit|r18|sexual
    loads:
    - '{{project_root}}/studio/knowledge/packs/r18_sensory_pack.md'
    - '{{project_root}}/studio/knowledge/packs/fetish_guidance_pack.md'
  - scene_tag: dialogue-heavy|gaming
    loads:
    - '{{project_root}}/studio/rules/character_voice.md'
dependencies:
  knowledge:
  - path: '{{project_root}}/studio/knowledge/packs/narrative_style_pack.md'
  - path: '{{project_root}}/studio/knowledge/packs/r18_sensory_pack.md'
  - path: '{{project_root}}/studio/knowledge/packs/fetish_guidance_pack.md'
  - path: '{{project_root}}/studio/knowledge/glossaries/hentai_lexicon.md'
  modules: []
---


## Pipeline Overview

```
Phase 1: EXTRACTION
  Step 01 → Initialize (detect engine, validate paths)
  Step 02 → Route context (MV vs MZ, data vs log mode)
  Step 03 → Extract world info (maps, locations)
  Step 04 → Build character bibles (appearance + voice rules)
  Step 05 → Select heroines (who gets adapted)

Phase 2: QUEST-GATED TIMELINE CONSTRUCTION  ← CORE NEW PHASE
  Step 06  → Extract main quest backbone (主线进度 variable chain)
  Step 06b → R18 scene audit (catalog ALL scenes + their source map/event)
  Step 06c → Companion timeline (JOIN event + bond arc + R18 unlock chain per companion)
  Step 06d → Narrative assembly (screenwriter: weave scenes into chapters)

Phase 3: PROSE GENERATION
  Step 07 → Prose generation (Suki writes each chapter)
  Step 08 → Quality audit (Riko reviews)
  Step 10 → PlantUML graph (visual timeline)
```


## On Activation

1. Ask user for: game root path + main quest variable name + target heroines
2. Auto-detect engine version (MV `www/data/` vs MZ flat `data/`)
3. Run extraction scripts to build companion timelines
4. **MANDATORY**: Complete Step 06c (companion timeline) BEFORE building novel_script.md
5. Only route to Suki (prose) AFTER novel_script.md is validated against prerequisites


## Quick Reference

| Intent | Trigger | Route |
|--------|---------|-------|
| **Adapt RPG game** | Provide game path | Load `./steps/step-01-initialize.md` |
| **Map quest timeline** | After initialization | Load `./steps/step-06-timeline.md` |
| **Build companion arc** | Per companion | Load `./steps/step-06c-companion-timeline.md` |
| **Assemble novel script** | After all companion arcs done | Load `./steps/step-06d-narrative-assembly.md` |
| **R18 scene audit** | Verify no scenes missed | Load `./steps/step-06b-r18-audit.md` |
| **Write prose** | After novel_script.md validated | Route to Suki (lewd-writer) |
| **Quality check** | After prose written | Load `./steps/step-08-quality-audit.md` |
| **Decrypt assets** | Need images | See studio tools (RPG-Maker-MV-Decrypter) |
