---
name: step-02-context-routing
description: "Extract character events and build context report — supports data-only and log-assisted modes"
---

# Step 2: Context Extraction & Routing

## Purpose
Extract all dialogue, scenes, and character data from the game files. Route to either data-only extraction or log-assisted triangulation.

## Mode A: Data-Only (Default)

### 2A.1 Identify Target Characters
From `Actors.json`, present all named actors to the user. Ask which character(s) to focus on.

### 2A.2 Extract Character Events
For each target character, run the extraction script:
```bash
python3 ./scripts/extract_character_events.py "{game_root_path}" \
  --actor-id {ACTOR_ID} \
  --actor-name "{ACTOR_NAME}" \
  --output-dir "_lnd-output/_rpg/{game_name}/extractions" \
  --format both
```

This produces:
- `{actor_name}_events.md` — Human-readable Markdown (grouped by CommonEvent → Map)
- `{actor_name}_events.json` — Structured JSON for pipeline processing

### 2A.3 Analyze Extraction Results
From the extracted data, compile:
- **Character bio** (from introduction CommonEvent)
- **NSFW scene index** (scenes with sexual dialogue/content)
- **Relationship map** (which characters interact with the target)
- **Location heatmap** (which maps have the most dialogue)

### 2A.4 Compile Context Report
Generate `context_report.md` containing:
- Per-character extraction summary (blocks, maps, key scenes)
- NSFW scene catalog with brief descriptions
- Recommended adaptation order (by narrative arc, not map order)

---

## Mode B: Log-Assisted (Optional)

### 2B.1 Parse Playthrough Log
```bash
python3 ./scripts/parse_playthrough_log.py "{log_path}" \
  --map-index "_lnd-output/_rpg/{game_name}/map_index.json" \
  -o "_lnd-output/_rpg/{game_name}/parsed_events.json"
```

### 2B.2 Triangulate with Translation Script
Using parsed events as anchors, search `ManualTransFile.json` for:
- Dialogue before each event (buildup)
- Dialogue after each event (aftermath)
- Related dialogue from same map context

### 2B.3 Merge with Character Extraction
Run character extraction (same as Mode A) and merge with log timeline for scene ordering.

---

## Outputs
- `_lnd-output/_rpg/{game_name}/extractions/{actor_name}_events.md`
- `_lnd-output/_rpg/{game_name}/extractions/{actor_name}_events.json`
- `_lnd-output/_rpg/{game_name}/context_report.md`

## Progression
- ⏸️ **CHECKPOINT: Human Audit** — Present extraction results and context report to user
- ✅ User approves → Load `./steps/step-03-world-info.md`
- ❌ User rejects → Re-extract with different parameters
