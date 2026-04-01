---
name: step-04-character-bibles
description: "Generate character bibles from extracted event data — delegate to Aria (character-architect)"
---

# Step 4: Character Bibles

## Purpose
Build a comprehensive character bible for each target character, using the extracted event data as source material.

## Prerequisites
- Character extraction from Step 2 completed (`{actor_name}_events.md` + `.json`)
- World info from Step 3 completed

## Actions

### 4.1 Parse Character Introduction
From the extracted events, locate the **introduction CommonEvent** (usually named `{actor_name}的介绍` or `{actor_name}攻略`). Extract:
- Bio sheet (height, BWH, likes, dislikes, hobbies)
- Background lore text
- Lover field (tracks corruption state)

### 4.2 Analyze Dialogue Patterns
From `{actor_name}_events.json`, compute:
- **Top locations** — maps where character appears most
- **Key relationships** — who they speak to most
- **NSFW scene catalog** — CommonEvents with sexual content (detected by keywords + CG picture references)
- **Personality markers** — recurring speech patterns, verbal tics, catchphrases

### 4.3 Identify Corruption Arc (if NTR route)
Look for `侵蚀度` (erosion) CommonEvents and track how the character's bio sheet changes:
- Lover field progression
- Evaluation text changes
- Scene escalation pattern

### 4.4 🔄 Delegate to Aria (character-architect)
Pass the following to Aria:
- Extracted dialogue samples (top 20 most representative blocks)
- Bio sheet data
- Corruption arc stages (if applicable)
- NSFW scene summaries
- World info context from Step 3

**Aria produces**: `_lnd-output/_rpg/{game_name}/{actor_name}_bible.md`

### 4.5 ⏸️ Human Audit
Present the character bible to the user for review.

## Outputs
- `_lnd-output/_rpg/{game_name}/{actor_name}_bible.md`

## Progression
- ✅ User approves → Load `./steps/step-05-heroine-select.md`
- ❌ User requests changes → Revise with Aria
