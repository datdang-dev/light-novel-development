---
name: step-06-timeline
description: "Quest-driven timeline assembly using automated quest flow extraction"
---

# Step 6: Quest-Driven Timeline Assembly

## Purpose

Build a story timeline by extracting quest flow data (Switch/Variable dependencies) from game files, then ordering scenes chronologically based on the main quest variable progression.

## 🔄 [Self-Executed by Director K]

## Prerequisites

- Game root path confirmed (Step 1)
- Character extraction completed (Step 2)
- `{selected_heroine}` chosen (Step 5)

## Actions

### 6.1 Run Quest Flow Extraction

```bash
python scripts/extract_quest_flow.py <game_root> \
  --main-quest-var <VARIABLE_ID> \
  --output-dir _lnd-output/_rpg/{game_name}/quest_flow
```

**Finding the main quest variable:**

1. Open `data/System.json` → search `variables` array for names containing: `主线`, `进度`, `main`, `quest`, `chapter`, `story`
2. Common patterns: Variable 1000 = `主线进度` (main quest progress)
3. If uncertain, scan for the variable with the most conditional checks across maps

**Output:** `quest_flow_graph.json` + `quest_flow_report.md`

### 6.2 Analyze Main Quest Milestones

From the report's **Main Quest Progression** section:

1. List all milestones (Variable SET operations) in order
2. Identify which maps/events correspond to each milestone
3. Note any R18 CGs attached to main quest nodes

### 6.3 Map Side Events to Timeline Windows

For each gap between main quest milestones:

1. Identify side events accessible in that window (same map, no higher quest gate)
2. Group side events by type: R18, character development, world-building
3. Decide chapter placement (before/after milestone)

### 6.4 Character-Specific Timeline

Cross-reference with `{heroine}_events.md`:

1. Filter quest_flow_report for events involving `{selected_heroine}`
2. Mark heroine-specific R18 CGs
3. Build heroine arc within the main quest framework

### 6.5 Chapter Segmentation

Group scenes into chapters based on:

- Main quest milestone boundaries
- Map transitions (location changes)
- Narrative arc shifts (tone changes, new characters introduced)
- R18 scene density (balance erotic content across chapters)

## Outputs

- `_lnd-output/_rpg/{game_name}/quest_flow/quest_flow_graph.json`
- `_lnd-output/_rpg/{game_name}/quest_flow/quest_flow_report.md`
- `_lnd-output/_rpg/{game_name}/novels/{heroine_name}/timeline.md`

## Progression

- ✅ Timeline assembled → Load `./steps/step-06b-r18-audit.md`
