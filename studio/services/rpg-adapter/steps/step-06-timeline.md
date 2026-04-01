---
name: step-06-timeline
description: "Assemble story timeline for selected heroine"
---

# Step 6: Story Timeline Assembly

## Purpose
Filter the full context report to extract ONLY scenes relevant to the selected heroine, then arrange them chronologically.

## 🔄 [Self-Executed by Director K]

## Inputs
- `{selected_heroine}` from Step 5
- `_lnd-output/_rpg/{game_name}/characters/{selected_heroine}_bible.md`
- `_lnd-output/_rpg/{game_name}/context_report.md`

## Actions

### 6.1 Filter Scenes
Extract all scenes/dialogues/events from `context_report.md` that involve `{selected_heroine}`.

### 6.2 Chronological Ordering
Arrange filtered scenes into a story timeline using the event timestamps from the playthrough log.

### 6.3 Chapter Segmentation
Group scenes into logical chapter boundaries based on:
- Map transitions
- Time gaps
- Narrative arc shifts

## Outputs
- `_lnd-output/_rpg/{game_name}/novels/{heroine_name}/timeline.md`

## Progression
- ✅ Timeline assembled → Load `./steps/step-07-prose-generation.md`
