---
name: rpg-adapter
description: "RPG Maker MV/MZ game-to-novel adaptation pipeline — specializes in extracting quest timelines, companion join conditions, R18 scene prerequisites, and assembling them into a chronologically correct novel script. Use when the user says 'adapt RPG game', 'extract game timeline', 'RPG to novel', 'map R18 scenes to chapters', or 'build novel from game data'."
injection:
  always:
    - "{{project_root}}/studio/knowledge/packs/narrative_style_pack.md"
  triggers:
    - scene_tag: "explicit|r18|sexual"
      loads:
        - "{{project_root}}/studio/knowledge/packs/r18_sensory_pack.md"
        - "{{project_root}}/studio/knowledge/packs/fetish_guidance_pack.md"
    - scene_tag: "dialogue-heavy|gaming"
      loads:
        - "{{project_root}}/studio/rules/character_voice.md"
dependencies:
  knowledge: []
  modules: []
---

# RPG Adapter Pipeline — Screenwriter Edition

## Core Philosophy

> **The Recollection Room is a MUSEUM, not a timeline.**
> Every R18 scene in Map029 (回想房) is a replay of something that happened in the main game.
> The screenwriter's job is to: (1) find WHERE in the main game each scene occurs, (2) identify ALL prerequisites, (3) place the scene in the novel AFTER all conditions are met.

**Two cardinal sins to avoid:**
1. Placing a companion's R18 event BEFORE that companion joins the party
2. Treating Recollection Room order as chronological story order

---

## Pipeline Overview

```
Phase 1: EXTRACTION
  Step 01 → Initialize (detect engine, validate paths)
  Step 02 → Route context (MV vs MZ, data vs log mode)
  Step 03 → Extract world info (maps, locations)
  Step 04 → Build character bibles (appearance + voice rules)
  Step 05 → Select heroines (who gets adapted)

Phase 2: QUEST-GATED TIMELINE CONSTRUCTION  ← CORE NEW PHASE
  Step 06  → Extract main quest backbone (主线进度 variable chain)
  Step 06b → R18 scene audit (catalog ALL scenes + their source map/event)
  Step 06c → Companion timeline (JOIN event + bond arc + R18 unlock chain per companion)
  Step 06d → Narrative assembly (screenwriter: weave scenes into chapters)

Phase 3: PROSE GENERATION
  Step 07 → Prose generation (Suki writes each chapter)
  Step 08 → Quality audit (Riko reviews)
  Step 10 → PlantUML graph (visual timeline)
```

---

## Phase 2 Deep-Dive: Quest-Gated Timeline Construction

### Step 06: Main Quest Backbone

Extract the main progress variable (e.g., `主线进度`) and map each SET point to a chapter boundary:

| Progress | Location | Chapter Boundary |
|---------|----------|----------------|
| SET=0 | 王城 (Castle) | Ch.1 Start |
| SET=1 | 王都街道 (Capital Streets) | Ch.2 |
| SET=2 | 執務室 (Office) + Lilith BJ | Ch.3 |
| SET=3 | 冒险者工会 (Guild) | Ch.4 |
| SET=4 | 冒险者工会 | Ch.5 |
| SET=5 | 街外修道院 (Monastery) | Ch.6 |
| SET=6 | 冒険者工会 | Ch.7 |
| SET=7 | 智与愚之塔 (Tower) | Ch.8 |
| SET=8-10 | 恶之城 (Evil City) | Ch.9+ |

### Step 06c: Companion Timeline (NEW — CRITICAL)

For EACH companion, extract in order:

**A. JOIN EVENT** — When/where does this companion first appear and become available?
```python
# Look for code 129 (Change Party Member, action=0 ADD) in map events
# Cross-reference with map name to get location
# Record: "Companion X joins at Map_Y_EV_Z, requires SW/V conditions"
```

**B. BOND PROGRESSION** — What variable tracks their relationship?
```python
# Look for named variables like 亚利佐羁绊, PM bond, etc.
# Find all events that SET or ADD to this variable
# These are the "dates" / bond events that must happen before R18 unlocks
```

**C. R18 UNLOCK CHAIN** — For each R18 scene, what prerequisites?
```python
# From Recollection Room (Map029), trace each EV back to source map
# Extract: requires_switch / requires_variable_min / requires_main_progress_min
# Sort by earliest possible unlock = max(all prerequisites satisfied)
```

**D. Output format per companion:**
```
COMPANION: 亚利佐 (Yarizo)
JOIN: Map_Unicorn_Tavern, after main_progress >= 1, at 独角兽酒馆
BOND TRACK: V[亚利佐羁绊]

BOND ARC:
  Bond=0 → CE370: First sighting (Yarizo sees Kohaku at tavern)
  Bond=1 → EV001: Yarizo shows cock, Kohaku smells
  Bond=2 → EV002: Yarizo threatens insertion
  Bond=3 → EV005: Debt repayment begins
  ...

R18 SCENES (sorted by earliest unlock):
  earliest: bond >= 1, main_progress >= 1
    → EV001 (tavern, sniff scene)
  earliest: bond >= 2, main_progress >= 1
    → EV002 (threat scene)
  ...
```

### Step 06d: Narrative Assembly (Screenwriter Step)

**Input:** Main quest backbone + all companion timelines
**Output:** `novel_script.md` with chapters that respect ALL prerequisites

**Assembly rules:**

1. **Chapter = Main Quest Beat**: Each chapter advances main progress by 1 step
2. **Companion scenes are WOVEN IN** after their unlock conditions, not dumped at once
3. **Scene density**: Max 2-3 R18 scenes per chapter to maintain pacing
4. **Scene type classification**:
   - `MAIN` → Must appear, drives plot
   - `BOND` → Companion relationship scene, ordered by bond level
   - `BATTLE_LOSS` → Conditional; in novel = nightmare/what-if/flashback
   - `RECOLLECTION` → Never first-time; always memory/replay context
5. **Emotional escalation**: Within each companion's arc, order scenes from lightest to most explicit

**Screenwriter judgment calls:**
- If a companion has 10+ R18 scenes, space them across 3-4 chapters minimum
- Battle loss scenes are best used as Kohaku's nightmares during rest/inn scenes
- Locked DLC scenes → appendix chapters or post-epilogue bonus content

---

## On Activation

1. Ask user for: game root path + main quest variable name + target heroines
2. Auto-detect engine version (MV `www/data/` vs MZ flat `data/`)
3. Run extraction scripts to build companion timelines
4. **MANDATORY**: Complete Step 06c (companion timeline) BEFORE building novel_script.md
5. Only route to Suki (prose) AFTER novel_script.md is validated against prerequisites

---

## Scripts

| Script | Purpose |
|--------|---------|
| `./scripts/validate_game_structure.py` | Validate RPG Maker directory structure |
| `./scripts/build_map_index.py` | Build map lookup index from MapInfos.json |
| `./scripts/extract_character_events.py` | Extract all events for a character across all maps |
| `./scripts/extract_quest_flow.py` | Extract quest progression graph + R18 catalog |
| `./scripts/extract_companion_timeline.py` | **NEW** — Extract companion join + bond arc + R18 unlock chain |
| `./scripts/parse_playthrough_log.py` | Parse TimelineLogger.js logs (optional) |

---

## Quick Reference

| Intent | Trigger | Route |
|--------|---------|-------|
| **Adapt RPG game** | Provide game path | Load `./steps/step-01-initialize.md` |
| **Map quest timeline** | After initialization | Load `./steps/step-06-timeline.md` |
| **Build companion arc** | Per companion | Load `./steps/step-06c-companion-timeline.md` |
| **Assemble novel script** | After all companion arcs done | Load `./steps/step-06d-narrative-assembly.md` |
| **R18 scene audit** | Verify no scenes missed | Load `./steps/step-06b-r18-audit.md` |
| **Write prose** | After novel_script.md validated | Route to Suki (lewd-writer) |
| **Quality check** | After prose written | Load `./steps/step-08-quality-audit.md` |
| **Decrypt assets** | Need images | See studio tools (RPG-Maker-MV-Decrypter) |

---

## Downstream Agents

- **Orchestrator**: Director K
- **Prose**: Suki (lewd-writer)
- **Character**: Aria (character-architect)  
- **World**: Luna (world-weaver)
- **QA**: Riko (gooner-editor)
