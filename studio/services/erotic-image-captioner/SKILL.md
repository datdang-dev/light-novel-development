---
name: erotic-image-captioner
description: 'Lightweight 4-step pipeline: Image → Forensic Analysis (Kana) → Scene
  Prelude (Luna) → Erotic Caption (Suki Caption Mode with Mood Seed). Outputs short,
  explicit R18 image captions with narrative context.'
injection:
  always:
  - '{{project_root}}/studio/config/canon-rules.md'
  triggers:
  - scene_tag: explicit|r18|sexual
    loads:
    - '{{project_root}}/studio/knowledge/packs/r18_sensory_pack.md'
    - '{{project_root}}/studio/knowledge/packs/arousal_architecture.md'
dependencies:
  knowledge:
  - path: '{{project_root}}/studio/knowledge/packs/r18_sensory_pack.md'
  - path: '{{project_root}}/studio/knowledge/glossaries/hentai_lexicon.md'
  modules: []
---


# Erotic Image Captioner Pipeline

## Overview

The Erotic Image Captioner is a **lightweight pipeline** for generating short, explicit R18 captions from manga/hentai images. Unlike the full `gooner-alchemist` pipeline (which produces novel-length prose), this pipeline produces punchy, visually-driven **image captions** optimized for maximum arousal in minimal words.

**Pipeline:** `Image → Kana (Forensic) → Luna (Scene Prelude) → Suki (Caption Mode + Mood Seed)`

## On Activation

1. Load pipeline context from `{{project_root}}/studio/config/pipeline-context.md`
2. Load canon rules from `{{project_root}}/studio/config/canon-rules.md`
3. Begin at Step 1

## Steps

### Step 1 — Initialize

1. Validate image path exists
2. Extract image basename for output directory naming
3. Create output directory: `{{project_root}}/_lnd-output/_captions/{image-basename}/`
4. Check if user provided additional context (scene backstory) — store as `user_context`
5. Check if user provided `mood_seed` parameter — store as `mood_seed` (default: `AUTO`)
   - Valid values: `AUTO`, `MANIC`, `COLD`, `BRATTY`, `BROKEN`, `MASO`

### Step 2 — Forensic Analysis (Delegate to Kana)

1. **🔄 [Delegating to Kana]...**
2. Execute `{{project_root}}/studio/core/panel-forensic/SKILL.md`
3. Kana performs:
   - OCR extraction (if text present)
   - Character identification (appearance, clothing state, expression)
   - Explicit content documentation (acts, exposure, penetration, fluids)
   - Fetish tag extraction
   - SFX cataloguing
   - **🔥 Gut Reaction** — subjective vibe assessment with `suggested_mood` for Suki
4. Save forensic report to `_lnd-output/_captions/{image-basename}/forensic.md`

### Step 2.5 — Scene Prelude (Delegate to Luna)

1. **🔄 [Delegating to Luna]...**
2. Load forensic report from Step 2
3. Load `user_context` if provided
4. Pass `mood_seed` to Luna for scenario tone alignment
5. Execute `{{project_root}}/studio/core/scene-prelude/SKILL.md`
6. Luna performs:
   - Forensic tag cluster analysis
   - Scenario derivation (WHO, WHERE, WHEN, WHY)
   - Power topology mapping
   - Kink integration from `user_fetish_profile.md`
   - Sensory anchor generation (smell, texture, sound)
   - Anti-cliché validation
7. Save prelude to `_lnd-output/_captions/{image-basename}/prelude.md`

### Step 3 — Caption Generation (Delegate to Suki Caption Mode)

1. **🔄 [Delegating to Suki — Caption Mode]...**
2. Load forensic report from Step 2 (including Gut Reaction section)
3. Load **prelude from Step 2.5** (Luna's scenario seed)
4. Load user_context if provided
5. Pass `mood_seed` to Suki:
   - If user provided explicit mood → use it
   - If `AUTO` → Suki resolves from Kana's `gut_reaction.suggested_mood`
6. Execute `{{project_root}}/studio/core/erotic-caption-writer/SKILL.md`
7. Suki performs:
   - Internal COT Scratchpad (hidden planning)
   - **Prelude integration** — incorporate Luna's scenario, relationships, and sensory anchors
   - Structure variant selection (Standard / Cold Open / Aftermath / Stream Fragment)
   - Caption generation with mood-consistent voice
8. Validate against quality gates in erotic-caption-writer SKILL.md
9. Save caption to `_lnd-output/_captions/{image-basename}/caption.md`
10. Pipeline complete ✅

## Output Directory Structure

```
_lnd-output/_captions/{image-basename}/
├── forensic.md      # Kana's analysis + Gut Reaction
├── prelude.md       # Luna's scenario seed (context blueprint)
└── caption.md       # Suki's erotic caption (prelude-informed, mood-seeded)
```

## Quick Reference

| Intent | Trigger | Route |
|--------|---------|-------|
| **Single image caption** | `EC` or `erotic caption` | Start Step 1 |
| **Multi-image caption** | `EC` + multiple paths | Loop Steps 1–3 per image |
| **With mood override** | `EC --mood BRATTY` | Start Step 1 with mood_seed=BRATTY |
| **Skip prelude** | `EC --no-prelude` | Skip Step 2.5, direct Kana→Suki |

## Dependencies

- **Orchestrator**: Director K (`DIR`)
- **Sub-Systems**: `core/panel-forensic` (Kana), `core/scene-prelude` (Luna), `core/erotic-caption-writer` (Suki)
- **Config**: `config/canon-rules.md`

---

## 🔄 HANDOFF PROTOCOL

**This SKILL is the EC pipeline coordinator. Nova delegates to sub-agents.**

- **Nova → Kana:** PASS `image_path`, `mood_seed`, `user_context`. DROP nothing (fresh start).
- **Kana → Luna:** Follow `panel-forensic/SKILL.md` HANDOFF section.
- **Luna → Suki:** Follow `scene-prelude/SKILL.md` HANDOFF section.
- **Suki → Director K:** Return `caption.json` path. Drop all intermediate context.

### ⚡ Single-Session Shortcut

**Instead of reading this file + 3× sub-SKILL.md files, read ONE manifest:**

```
studio/pipelines/EC_manifest.md
```

This file pre-compiles all rules for Kana, Luna, and Suki. Use it for all single-session EC runs.
