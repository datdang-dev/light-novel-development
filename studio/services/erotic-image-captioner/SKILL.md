---
name: erotic-image-captioner
description: "Lightweight 3-step pipeline: Image → Forensic Analysis (Kana + Gut Reaction) → Erotic Caption (Suki Caption Mode with Mood Seed). Outputs short, explicit R18 image captions."
dependencies:
  core:
    - path: "{project-root}/studio/core/panel-forensic/SKILL.md"
    - path: "{project-root}/studio/core/erotic-caption-writer/SKILL.md"
  config:
    - path: "{project-root}/studio/config/canon-rules.md"
---

# Erotic Image Captioner Pipeline

## Overview

The Erotic Image Captioner is a **lightweight pipeline** for generating short, explicit R18 captions from manga/hentai images. Unlike the full `gooner-alchemist` pipeline (which produces novel-length prose), this pipeline produces punchy, visually-driven **image captions** optimized for maximum arousal in minimal words.

**Pipeline:** `Image → Kana (Forensic + Gut Reaction) → Suki (Caption Mode + Mood Seed)`

## On Activation

1. Load pipeline context from `{project-root}/studio/config/pipeline-context.md`
2. Load canon rules from `{project-root}/studio/config/canon-rules.md`
3. Begin at Step 1

## Steps

### Step 1 — Initialize

1. Validate image path exists
2. Extract image basename for output directory naming
3. Create output directory: `{project-root}/_lnd-output/_captions/{image-basename}/`
4. Check if user provided additional context (scene backstory) — store as `user_context`
5. Check if user provided `mood_seed` parameter — store as `mood_seed` (default: `AUTO`)
   - Valid values: `AUTO`, `MANIC`, `COLD`, `BRATTY`, `BROKEN`, `MASO`

### Step 2 — Forensic Analysis (Delegate to Kana)

1. **🔄 [Delegating to Kana]...**
2. Execute `{project-root}/studio/core/panel-forensic/SKILL.md`
3. Kana performs:
   - OCR extraction (if text present)
   - Character identification (appearance, clothing state, expression)
   - Explicit content documentation (acts, exposure, penetration, fluids)
   - Fetish tag extraction
   - SFX cataloguing
   - **🔥 Gut Reaction** — subjective vibe assessment with `suggested_mood` for Suki
4. Save forensic report to `_lnd-output/_captions/{image-basename}/forensic.md`

### Step 3 — Caption Generation (Delegate to Suki Caption Mode)

1. **🔄 [Delegating to Suki — Caption Mode]...**
2. Load forensic report from Step 2 (including Gut Reaction section)
3. Load user_context if provided
4. Pass `mood_seed` to Suki:
   - If user provided explicit mood → use it
   - If `AUTO` → Suki resolves from Kana's `gut_reaction.suggested_mood`
5. Execute `{project-root}/studio/core/erotic-caption-writer/SKILL.md`
6. Suki performs:
   - Internal COT Scratchpad (hidden planning)
   - Structure variant selection (Standard / Cold Open / Aftermath / Stream Fragment)
   - Caption generation with mood-consistent voice
7. Validate against quality gates in erotic-caption-writer SKILL.md
8. Save caption to `_lnd-output/_captions/{image-basename}/caption.md`
9. Pipeline complete ✅

## Output Directory Structure

```
_lnd-output/_captions/{image-basename}/
├── forensic.md      # Kana's analysis + Gut Reaction
└── caption.md       # Suki's erotic caption (mood-seeded)
```

## Quick Reference

| Intent | Trigger | Route |
|--------|---------|-------|
| **Single image caption** | `EC` or `erotic caption` | Start Step 1 |
| **Multi-image caption** | `EC` + multiple paths | Loop Steps 1–3 per image |
| **With mood override** | `EC --mood BRATTY` | Start Step 1 with mood_seed=BRATTY |

## Dependencies

- **Orchestrator**: Director K (`DIR`)
- **Sub-Systems**: `core/panel-forensic` (Kana), `core/erotic-caption-writer` (Suki)
- **Config**: `config/canon-rules.md`
