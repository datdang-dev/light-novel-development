---
name: step-07-prose-generation
description: "Generate light novel prose chapters for the heroine storyline"
---

# Step 7: Prose Generation

## Purpose
Generate Light Novel prose chapters from the heroine's timeline.

## 🔄 [Delegating to Suki (lewd-writer)]

## Inputs
- `_lnd-output/_rpg/{game_name}/novels/{heroine_name}/timeline.md`
- `_lnd-output/_rpg/{game_name}/characters/{heroine_name}_bible.md`
- `_lnd-output/_rpg/{game_name}/world_info.md`

## Delegation Instructions
Pass to Suki:
- The `timeline.md`, heroine's `bible.md`, and `world_info.md`
- Instruction: Generate Light Novel prose chapters following Suki standards (metadata block, 3-layer scent protocol, Romanized SFX, continuity table, Vietnamese titles)
- Each significant scene/event becomes one chapter

## Outputs
- `_lnd-output/_rpg/{game_name}/novels/{heroine_name}/chapters/ch{NN}_{title}.md`

## Progression
- ✅ Chapters generated → Load `./steps/step-08-quality-audit.md`
