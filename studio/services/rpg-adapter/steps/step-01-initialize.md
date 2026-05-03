---
name: step-01-initialize
description: "Initialize pipeline, auto-detect engine version, validate game structure"
---

# Step 1: Initialize & Validate

## Purpose
Validate the RPG Maker game directory and auto-detect engine version before any adaptation begins.

## Inputs Required
- `{game_root_path}` — absolute path to the game's root directory
- `{game_name}` — name identifier for this adaptation project

## Actions

### 1.1 Collect User Inputs
Ask the user for:
- Game root path
- Game name (or derive from directory name)

### 1.2 Auto-Detect Engine Version
Check for engine markers:
```
IF {game_root_path}/game.rmmzproject exists → RPG Maker MZ (flat structure)
  data_dir = {game_root_path}/data/
ELIF {game_root_path}/www/data/ exists → RPG Maker MV (www wrapper)
  data_dir = {game_root_path}/www/data/
ELIF {game_root_path}/data/ exists → RPG Maker MV (deployed/flat)
  data_dir = {game_root_path}/data/
ELSE → FAIL: Not a valid RPG Maker game
```

### 1.3 Detect Available Data Sources
Check and report what's available:

| Data Source | Path | Required? |
|-------------|------|-----------|
| Map*.json | `{data_dir}/Map*.json` | ✅ HARD |
| MapInfos.json | `{data_dir}/MapInfos.json` | ✅ HARD |
| Actors.json | `{data_dir}/Actors.json` | ✅ HARD |
| CommonEvents.json | `{data_dir}/CommonEvents.json` | ✅ HARD |
| ManualTransFile.json | `{game_root_path}/ManualTransFile.json` | ⚠️ SOFT (translation tool) |
| playthrough_log.txt | user-provided | ⚠️ SOFT (optional) |

### 1.4 Route Mode Selection
```
IF playthrough_log exists → Log-Assisted Mode
ELSE → Data-Only Mode (default, recommended)
```

### 1.5 Create Output Directory & Map Index
```bash
mkdir -p "_lnd-output/_rpg/{game_name}/extractions"
python3 ./scripts/build_map_index.py "{data_dir}" -o "_lnd-output/_rpg/{game_name}/map_index.json"
```

### 1.6 Generate Game Summary
Report to user:
- Engine version (MV/MZ)
- Number of maps
- Number of actors (with names)
- Total CommonEvents
- Available data sources
- Selected mode (Data-Only / Log-Assisted)

## Outputs
- `_lnd-output/_rpg/{game_name}/` directory (created)
- `_lnd-output/_rpg/{game_name}/map_index.json` (generated)
- Engine version + mode selection

## Progression
- ✅ Pass → Load `./steps/step-02-context-routing.md`
- ❌ Fail → HALT and report
