---
name: step-03-world-info
description: "Extract world information and lore from context report"
---

# Step 3: World Info Extraction

## Purpose
Extract world systems, locations, factions, and magic/technology rules from the game content.

## 🔄 [Delegating to Luna (world-weaver)]

## Inputs
- `_lnd-output/_rpg/{game_name}/context_report.md`
- `manual_translation.json`

## Delegation Instructions
Pass to Luna:
- The full `context_report.md`
- Access to `manual_translation.json` for supplementary lore extraction
- Instruction: Extract world systems, locations, factions, magic/technology rules

## Outputs
- `_lnd-output/_rpg/{game_name}/world_info.md`

## Progression
- ✅ Complete → Load `./steps/step-04-character-bibles.md`
