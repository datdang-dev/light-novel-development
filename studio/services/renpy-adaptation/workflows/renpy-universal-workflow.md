# Workflow: Universal Ren'Py Playthrough Novelization

This workflow describes the standardized 5-phase process for adapting any Ren'Py-based game into a high-sensory, interactive Markdown/HTML Light Novel within LND Studio.

## Phase 1: Playthrough Mapping & Choice Matrix

- **Objective**: Establish the target timeline and resolve branching choices.
- **Actions**:
  1. Define or load the **Playthrough Choice Matrix** (e.g. `choices = {"day26_asuka": "slut"}`).
  2. Map out the linear route or multi-route structure by identifying all decision labels (`label`, `menu`, `jump`, `call`).
  3. Scan the `.rpy` files to locate variable usages (e.g. `[day26_leavestatus_asuka]`) that depend on the chosen path.

## Phase 2: AST Extraction & Narrative Flattening (Ren)

- **Objective**: Extract the raw dialogue tree and flatten it into a linear timeline.
- **Actions**:
  1. Run `extract_renpy_ast.py` with the Choice Matrix.
  2. Resolve all conditional flags (e.g., `if day26_secondchoice_asuka == "fuck":`) to select the active branching text block.
  3. Replace all variable placeholders (e.g., `[day26_leavestatus_asuka]` becomes `"slut"`) to produce a coherent, linear screenplay script.

## Phase 3: Visual & Audio Cue Merging (Kana)

- **Objective**: Align multi-modal game cues (sprites, backgrounds, SFX, music) as stage directions.
- **Actions**:
  1. Map `scene` and `show` tags to physical files in the game's `images/` directory.
  2. Audit visual assets using the Forensic Engine to compile a **Visual Cue Ledger** (descriptions of poses, outfits, and environment).
  3. Extract sound files (`play sound`, `play music`, `play movie`) and map them as sensory markers (e.g., the hum of school AC, high-pitched moans).

## Phase 4: High-Sensory Vietnamese Prose Synthesis (Suki)

- **Objective**: Transform raw dialogue and stage directions into R18 Vietnamese prose.
- **Actions**:
  1. Feed the flattened screenplay script + Visual Ledgers + Sensory markers to Suki (`lewd-writer`).
  2. Convert stage directions (e.g., `vpunch`, `impact.mp3`) into visceral physiological reactions (e.g., *"Cơ thể nàng giật bắn, tấm lưng dập mạnh vào bức tường gạch men"*).
  3. Embed the physical image illustrations directly as visual breaks (`![Caption](file://...)`).

## Phase 5: Web Book Compilation & Packaging

- **Objective**: Compile written chapters into an interactive, premium reading experience.
- **Actions**:
  1. Run the unified Web Book Compiler script to sort and aggregate all generated chapters.
  2. Embed chapters in the self-contained, glassmorphic Single Page Application reader (`full-novel-reader.html`).
  3. Pack the final outputs (Markdown, HTML, physical image assets) for distribution or offline reading.

---
**CRITICAL**: All prose generation must strictly follow Suki's zero-judgment, high-sensory-density R18 Vietnamese writing mechanics, focusing on exact physiological descriptions and sensory cues.
