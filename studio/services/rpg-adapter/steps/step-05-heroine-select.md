---
name: step-05-heroine-select
description: "Present heroine list and get user selection for novelization"
---

# Step 5: Character Selection

## Purpose
Present available heroines and let the user choose which storyline to develop next.

## 🔄 [Self-Executed by Director K]

## Actions

### 5.1 List Available Heroines
Scan `_lnd-output/_rpg/{game_name}/characters/` for all `*_bible.md` files. Present as a numbered list.

### 5.2 Get User Selection
Ask: *"Which heroine's storyline do you want to develop next?"*

### 5.3 Handle Response
- User selects a heroine → Store `{selected_heroine}` and proceed
- User says "Done" or "Exit" → 🏁 Pipeline complete

## Outputs
- `{selected_heroine}` stored for Steps 6–8

## Progression
- ✅ Heroine selected → Load `./steps/step-06-timeline.md`
- 🏁 User exits → Pipeline complete
