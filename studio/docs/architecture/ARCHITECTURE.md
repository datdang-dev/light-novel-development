# LND Studio Architecture

## Overview

LND Studio là framework chuyên biệt cho adaptation và generation R18 JP light novel + manga prose. Built trên nguyên tắc multi-agent orchestration với kiến trúc knowledge-centric, layered. Framework chia thành hai macro-domain: **Production** (content generation) và **Meta** (quality audit & optimization).

> **Component Diagram:** `studio/docs/architecture/component-diagram.puml`

---

## Macro Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     USER / ENTRY POINTS                         │
│  Workflows (.agent/workflows/), Skills (.agents/skills/)       │
├──────────────────────────────┬──────────────────────────────────┤
│    PRODUCTION DOMAIN         │       META DOMAIN                │
│    (Content Generation)      │       (QA & Optimization)        │
│                              │                                  │
│  ┌────────────────────────┐  │  ┌──────────────────────────┐   │
│  │ PIPELINES (Layer 3.5)  │  │  │ DEVELOPERS (META)        │   │
│  │ EC_manifest, RP_manifest│  │  │ orchestrator.py          │   │
│  ├────────────────────────┤  │  │ HermesAgent, ClaudeAgent  │   │
│  │ AGENTS (Layer 3)       │  │  │ mode_registry.yaml        │   │
│  │ Director K, Kana, Suki │  │  │ roles/  templates/        │   │
│  │ Luna, Riko, Aria, Nova │  │  │ ReviewOutput schemas      │   │
│  ├────────────────────────┤  │  └───────────┬──────────────┘   │
│  │ SERVICES (Layer 2.5)   │  │              │                  │
│  │ gooner-alchemist, EC   │  │         audits output           │
│  │ character-builder, ... │  │              │                  │
│  ├────────────────────────┤  │              ▼                  │
│  │ CORE ENGINE (Layer 2)  │◄─┼──────── reviews ────────────── │
│  │ panel-forensic         │  │                                  │
│  │ lewd-writer            │  │                                  │
│  │ erotic-caption-writer  │  │                                  │
│  │ scene-prelude          │  │                                  │
│  │ orchestration/         │  │                                  │
│  ├────────────────────────┤  │                                  │
│  │ MODULES (Layer 1)      │  │                                  │
│  │ fetish-guidance        │  │                                  │
│  │ sfx-lookup             │  │                                  │
│  │ style-enforcer         │  │                                  │
│  └────────┬───────────────┘  │                                  │
│           │                  │                                  │
├───────────┴──────────────────┴──────────────────────────────────┤
│                    SHARED FOUNDATION                             │
│  Rules (Layer 0.5)           │  Knowledge Base (Layer 0)       │
│  rules/canon-preamble        │  packs/, fetish-db/             │
│  rules/mandatory/            │  glossaries/, sfx/              │
│  config/                     │  style-guides/, trope_beat_sheets│
├─────────────────────────────────────────────────────────────────┤
│                    INFRASTRUCTURE (Layer -1)                     │
│  schemas/ (JSON)  │  schemas/pydantic/ (Python)                 │
│  shared/                                                        │
├─────────────────────────────────────────────────────────────────┤
│                    TOOLING (Side Channel)                        │
│  scripts/ (validators, runners, OCR)  │  tools/ (RPG decrypter)│
└─────────────────────────────────────────────────────────────────┘
```

---

## Layer -1: Infrastructure

Foundational data structures, type definitions, and cross-cutting utilities.

### `studio/schemas/` — JSON Schema Contracts

Machine-readable output contracts for inter-agent communication.

| Schema | Consumer | Purpose |
| ------ | -------- | ------- |
| `forensic-state.schema.json` | Kana → Suki | Visual forensic analysis output |
| `draft-prose.schema.json` | Suki → Riko | Generated prose for audit |
| `audit-report.schema.json` | Riko → Director K | 100-point quality audit |
| `character-bible.schema.json` | Aria → All | Character consistency contract |
| `pipeline-state.schema.json` | Director K | Pipeline orchestration state |
| `scene-context.schema.json` | Luna → Suki | Scene prelude handoff |
| `dialogue-output.schema.json` | Miki → Suki | Extracted dialogue |
| `continuity-ledger.schema.json` | All | Cross-scene continuity tracking |

### `studio/schemas/pydantic/` — Pydantic Models

Python-native validation models for programmatic pipeline enforcement.

| Model | Role | Purpose |
| ----- | ---- | ------- |
| `ForensicOutput` | Kana | Validates visual forensic analysis |
| `PreludeOutput` | Luna | Validates scene context prelude |
| `CaptionOutput` | Suki | Validates erotic caption generation |

### `studio/shared/` — Cross-cutting Concerns

| Component | Purpose |
| --------- | ------- |
| `agent-memory/` | Persistent memory across sessions |
| `onboarding/` | First-run initialization guides |

---

## Layer 0: Knowledge Base (`studio/knowledge/`)

Domain knowledge packs — the intellectual foundation of all generation. Every SKILL.md must wire to knowledge via `dependencies.knowledge`.

### Index

**File:** `studio/knowledge/knowledge-index.yaml` — maps every knowledge file to consuming agents and scene tags.

### Knowledge Packs (`packs/`)

| Pack | Used By | Purpose |
| ---- | ------- | ------- |
| `arousal_architecture.md` | Suki, scene-expansion | Phase-based pacing (Setup→Tease→Escalation→Climax→Aftermath) |
| `narrative_style_pack.md` | Suki | Writing style directives |
| `japanese_reader_psychology.md` | Suki | 4 psychology hooks (ギャップ萌え, 征服感, 背徳感, ご褒美感) |
| `r18_sensory_pack.md` | Suki | Sensory density reference |
| `roleplay_st_pack.md` | Yua | SillyTavern RP conventions |
| `fetish_guidance_pack.md` | Suki, fetish-guidance | Kink taxonomy |

### Fetish Database (`fetish-db/`)

Deep-dive research files per fetish category: `anal_research.md`, `mindbreak_research.md`, `ntr_research.md`, `creampie_research.md`, etc.

### Glossaries (`glossaries/`)

| File | Purpose |
| ---- | ------- |
| `hentai_lexicon.md` | Master Vietnamese-Japanese erotic vocabulary |

### SFX Registry (`sfx/`)

| File | Purpose |
| ---- | ------- |
| `japanese_sfx_dictionary.md` | Comprehensive SFX reference |
| `moaning_sfx_research.md` | Moaning patterns and variations |
| `r18_sfx_quickref.yaml` | Quick-lookup YAML for generation |

### Style Guides (`style-guides/`)

| File | Purpose |
| ---- | ------- |
| `MESUGAKI_DIALOGUE_STYLE.md` | Bratty dialogue patterns |
| `R18_LIGHTNOVEL_CULTURE_GUIDE.md` | JP R18 culture conventions |

### Trope Beat Sheets (`trope_beat_sheets/`)

Genre-specific narrative structures: `corruption_beats.md`, `mindbreak_beats.md`, etc.

### Character Profiles (`characters/`)

Pre-built character profiles for recurring cast members.

---

## Layer 0.5: Rules & Configuration

Global constraints and mandatory context that ALL agents must respect.

### `studio/rules/` — Single Source of Truth

All production rules consolidated into one location.

| File | Priority | Purpose |
| ---- | -------- | ------- |
| `canon-preamble.md` | **ABSOLUTE** | 11 non-negotiable rules: Language, Zero Hallucination, Bounded Inference, Gooner Vocabulary, Formatting, One Page = One File, Sensory Density, Anti-Slop Gates, Continuity, Quality Thresholds, Hierarchy of Authority. |
| `canon-rules.md` | HIGH | Hard rules derived from canon-preamble |
| `gooner_principles.md` | HIGH | 9 core gooner principles (P1-P9) |
| `anti_slop.md` | HIGH | SLOP detection patterns |
| `sensory_density.md` | HIGH | Minimum sensory markers per page |
| `hentai_logic_gate.md` | HIGH | Logic constraints for R18 scenes |
| `GOONER_AUDIT_FRAMEWORK.md` | HIGH | 100-point quality audit framework |
| `dialogue_format.md` | MEDIUM | Dialogue bracket/pronoun rules |
| `continuity.md` | MEDIUM | Cross-scene continuity tracking |
| `+10 more...` | MEDIUM | Scene boundaries, character voice, fetish usage, etc. |

### `studio/rules/mandatory/` — Context Injection Payload

Ordered context files automatically injected into every generation session:

| Order | File | Purpose |
| ----- | ---- | ------- |
| 00 | `anti-slop.md` | SLOP detection rules |
| 01 | `writing-mechanics.md` | Core writing mechanics |
| 02 | `dialogue-format.md` | Dialogue formatting rules |
| 03 | `prose-template.md` | Prose output template |
| 04 | `language.md` | Language constraints |
| 05 | `quality-criteria.md` | Quality evaluation criteria |

### `studio/config/` — Pipeline & Studio Configuration

| File | Purpose |
| ---- | ------- |
| `BOOTSTRAP.md` | Resolves `{project-root}` path. Read FIRST by every agent. |
| `pipeline-context.md` | Architecture constraints for pipeline execution |
| `atmosphere_ledger.json` | Quality thresholds: `min_sensory_density: 0.20`, `min_entropy: 3.5` |
| `config.yaml` | General studio settings |
| `banned-words.txt` | Master banned word list |
| `pipelines/EC_manifest.md` | Pre-compiled EC pipeline manifest |
| `pipelines/RP_manifest.md` | Pre-compiled RP pipeline manifest |
| `protocols/one-shot-response.md` | Protocol for single-turn responses |
| `templates/` | Output templates (light-novel-prose, ST cards) |

---

## Layer 1: Modules (`studio/modules/`)

Plug-in rule sets and specialized engines. Loaded on-demand by Core skills.

| Module | Purpose | Used By |
| ------ | ------- | ------- |
| `fetish-guidance/` | Kink taxonomy and usage guidelines | Suki, Luna |
| `gooner-audit-engine/` | 100-point quality audit framework | Riko |
| `sfx-lookup/` | Sound effect dictionary and rotation | Suki, Miki |
| `style-enforcer/` | Writing style compliance engine | Suki |
| `lnd-re-specialist/` | Regex pattern matching utilities | RE Specialist agent |
| `sillytavern-expert/` | SillyTavern framework engineering + V3 card export | Export pipeline, preset engineering |

---

## Layer 2: Core Engine (`studio/core/`)

Primary content generation modules. Each maps 1:1 to an Agent persona.

### Generation Modules

| Module | Agent | Purpose |
| ------ | ----- | ------- |
| `panel-forensic/` | Kana | ATOMIC matrix visual analysis, SFX extraction, character anchoring. Produces `forensic-state.json`. |
| `lewd-writer/` | Suki | R18 prose generation. Transforms forensic data into sensory-dense narrative. Produces `draft-prose.json`. |
| `erotic-caption-writer/` | Suki (Caption Mode) | Punchy, 150-300 word image captions. Produces `caption.json`. |
| `scene-prelude/` | Luna | Scenario seed, power dynamic, sensory anchors. Bridges raw imagery to erotic context. |
| `transformation-engine/` | Director K | Text transformation and normalization utilities. |
| `volume-context-extractor/` | Kana | Extracts global volume context from manga series. |
| `roleplay-engine/` | Yua | Interactive conversational RP with Novel Format output. |
| `party-mode/` | All | Multi-agent collaborative generation. |

### Orchestration (`studio/core/orchestration/`)

Production pipeline management for sequential multi-agent execution.

| Component | Purpose |
| --------- | ------- |
| `pipeline_registry.yaml` | Declarative pipeline definitions (EC, MA) with step sequences, templates, and schema bindings |
| `pipeline_manager.py` | Registry loader and step accessor |
| `runner.py` | `ProductionRunner` — session management, step context loading, output persistence |

---

## Layer 2.5: Services (`studio/services/`)

Composite workflows that orchestrate multiple Core modules.

| Service | Primary Agent | Purpose |
| ------- | ------------- | ------- |
| `gooner-alchemist/` | Director K | Full Manga-to-Novel adaptation pipeline (Kana→Aria→Suki→Riko) |
| `erotic-image-captioner/` | Nova | Erotic Image Caption pipeline (Kana→Luna→Suki) |
| `character-builder/` | Aria | Character profile creation and bible management |
| `dialogue-scripting/` | Miki | Dialogue extraction and SFX generation |
| `manga-context-extractor/` | Kana | Volume-level context extraction |
| `novel-development/` | Luna | Raw text → structured R18 scene |
| `scene-expansion/` | Suki | Brief scenario → full prose chapter |
| `release-compiler/` | Director K | Final delivery packaging |
| `renpy-adaptation/` | Renpy Adapter | Ren'Py script → visual-novel format |
| `rpg-adapter/` | RPG Adapter | RPG Maker game data → chronological novel |
| `bible-sync/` | Aria | Story bible persistence and cross-session sync |

---

## Layer 3: Agents (`studio/agents/`)

Production personas. Each agent is a YAML definition file containing persona, critical actions, and menu triggers.

### Orchestration (Layer 1 Agent)

| Agent | Name | Role |
| ----- | ---- | ---- |
| `lnd-orchestrator.agent.yaml` | 🎬 Director K | Studio Director. Owns the end-to-end pipeline. Delegates to all Layer 2 agents. Enforces "Context Before Prose" policy. |

### Specialist Agents (Layer 2)

| Agent | Name | Role | Primary Skill |
| ----- | ---- | ---- | ------------- |
| `manga-adapter.agent.yaml` | 🖼️ Kana | Visual Context Specialist | `core/panel-forensic` |
| `lewd-writer.agent.yaml` | 🖋️ Suki | R18 Prose Specialist | `core/lewd-writer` |
| `world-weaver.agent.yaml` | 🌍 Luna | World Builder & Scene Prelude | `core/scene-prelude` |
| `gooner-editor.agent.yaml` | 🛡️ Riko | Quality Gatekeeper | `modules/gooner-audit-engine` |
| `character-architect.agent.yaml` | 👤 Aria | Character Profiler | `services/character-builder` |
| `dialogue-crafter.agent.yaml` | 💬 Miki | Dialogue & SFX Specialist | `services/dialogue-scripting` |
| `erotic-captioner.agent.yaml` | 📸 Nova | Erotic Caption Specialist | `services/erotic-image-captioner` |
| `roleplay-actor.agent.yaml` | 🎭 Yua | Roleplay Actor | `core/roleplay-engine` |
| `comfyui-prompter.agent.yaml` | 🎨 Pixel | Image Prompt Engineer | (External integration) |
| `re-specialist.agent.yaml` | 🔍 RE Specialist | Regex Pattern Expert | `modules/lnd-re-specialist` |
| `renpy-adapter.agent.yaml` | Renpy Adapter | Ren'Py Converter | `services/renpy-adaptation` |
| `rpg-adapter.agent.yaml` | RPG Adapter | RPG Maker Converter | `services/rpg-adapter` |

### Agent Infrastructure

| File | Purpose |
| ---- | ------- |
| `agent-protocol.md` | Standard initialization sequence for ALL agents (Bootstrap → Master Context → Global Rules → Schema Verify) |
| `agent-registry.yaml` | Single source of truth for agent hierarchy, layer assignments, and service mappings |

---

## Layer 3.5: Pipelines (`studio/pipelines/`)

Pre-compiled manifests that bundle ALL rules for a pipeline into a single document. Used in `ONE_SHOT` execution mode for token efficiency.

| Manifest | Pipeline | Execution Mode | Agents |
| -------- | -------- | -------------- | ------ |
| `EC_manifest.md` | Erotic Image Caption | ONE_SHOT | Kana → Luna → Suki |
| `RP_manifest.md` | Roleplay Session | CONVERSATIONAL | Yua |

---

## Meta Layer: Developers (`studio/developers/`)

The quality assurance and optimization layer. Invokes external AI CLIs (Hermes, Claude) to review, audit, and optimize production output. **This layer does NOT generate content — it ensures content quality.**

### Purpose

1. **Review production output** — Detect SLOP, generic prose, weak sensory density
2. **Architecture optimization** — Review prompt structure, pipeline design, knowledge wiring
3. **Prompt engineering** — Optimize templates for maximum instruction adherence

### Components

#### Agent Wrappers (`agents/`)

| Component | Purpose |
| --------- | ------- |
| `base.py` | `BaseAgent` abstract class — defines `call()` interface |
| `hermes_agent.py` | Hermes CLI wrapper (local LLM) |
| `claude_agent.py` | Claude Code CLI wrapper (API) |
| `mock_agent.py` | Mock agent for testing |
| `registry.py` | Agent factory — maps IDs to classes |

#### Configuration (`config/`)

| Component | Purpose |
| --------- | ------- |
| `mode_registry.yaml` | Declarative review workflow definitions: `arch_review`, `content_audit`, `prompt_opt`, `gooner_audit`, `review_debate` |
| `knowledge_index.json` | Knowledge file mappings for developer context injection |
| `roles/se/` | Software Engineering roles (`m-architect`) |
| `roles/dev/` | Developer roles (`m-prompt-expert`, `f-r18-expert`) + 15+ specialized rule files |
| `roles/qa/` | QA roles (`m-qa-gooner`) + `GOONER_AUDIT_FRAMEWORK.md` |
| `templates/` | Review prompt templates (`arch_review.md`, `code_review.md`) |

#### Schemas (`schemas/`)

| Model | Purpose |
| ----- | ------- |
| `ArchReviewOutput` | Architecture review findings |
| `CodeReviewOutput` | Content/prompt review findings |
| `QAAuditOutput` | Gooner quality audit results |

#### Orchestrator (`orchestrator.py`)

Multi-AI review runner. Supports execution modes:
- **single** — One agent reviews independently
- **sequential** — Multiple agents review in order
- **debate** — Multi-pass cross-agent debate with synthesis

#### Mode Registry Loader (`mode_registry.py`)

Python wrapper for loading and validating `mode_registry.yaml`.

---

## Tooling & Scripts (`studio/scripts/`, `studio/tools/`)

Side-channel utilities for validation, batch processing, and data extraction.

### Scripts (`studio/scripts/`)

| Script | Purpose |
| ------ | ------- |
| `pipeline_runner.py` | CLI pipeline execution engine |
| `anti_slop_validator.py` | Automated SLOP detection (entropy, n-gram, sensory density) |
| `output_validator.py` | JSON Schema validation for all outputs |
| `rule_injector.py` | Dynamic rule injection into agent context |
| `knowledge_validator.py` | Validates knowledge-index.yaml against physical files |
| `agent_compiler.py` | Compiles agent YAML into runtime context |
| `batch_manga_ocr.py` | Batch OCR for manga pages |
| `extract_dialogue.py` | Dialogue extraction from manga |
| `extract_scene_context.py` | Scene context extraction |
| `auto_repair.py` | Auto-repair for failed validations |
| `simulator.py` | Pipeline simulation for testing |
| `validate_links.py` | Cross-reference link validation |

### Tools (`studio/tools/`)

| Tool | Purpose |
| ---- | ------- |
| `RPG-Maker-MV-Decrypter/` | RPG Maker MV asset decryption |
| `bulk_decrypt.js` | Batch decryption utility |
| `clean_ev01.js` | Event data cleaner |
| `extract_scenes_from_trans.js` | Scene extraction from translations |
| `ln_linter.py` | Light novel prose linter |

---

## Primary Pipeline Flows

### [MA] Manga-to-Novel

```
Raw Manga Page
    ↓
[Kana] Panel Forensic → forensic-state.json
    ↓
[Kana] POC Context Vectors → psychological intent bridge
    ↓
[Aria] Character Builder → character-bible.json
    ↓
[Suki] R18 Prose Generation → draft-prose.json
    ↓
[Riko] Quality Audit (100-pt) → audit-report.json (PASS/FAIL)
    ↓
Final Output
```

### [EC] Erotic Image Caption

```
Source Image + mood_seed
    ↓
[Kana] Forensic Analysis → forensic inline data
    ↓ (fetish_tags, gut_reaction, explicit_acts)
[Luna] Scene Prelude → setting, "The Why", sensory anchors
    ↓ (setting_seed, power_dynamic, kink_name)
[Suki] Caption Writer → caption.json (150-300 words)
```

### [RP] Roleplay Session

```
User Turn
    ↓
[Yua] Turn Planning (think block) → archetype analysis, sensory mirror
    ↓
[Yua] Novel Format Output → narrator block + dialogue + SFX
```

---

## Quality Gates

Thresholds from `atmosphere_ledger.json`:

| Metric | Threshold |
| ------ | --------- |
| `min_sensory_density` | 0.20 |
| `max_boilerplate_ratio` | 0.10 |
| `min_entropy` | 3.5 |
| `max_ngram_repeat` | 0.05 |
| Audit PASS | ≥85/100 |
| Audit WARN | 70-84 |
| Audit FAIL | <70 |
| Circuit breaker | 3 consecutive fails → HALT |

Validator: `studio/scripts/anti_slop_validator.py`

---

## AI Slop Detection

### Signs

- Entropy < 3.5 (too repetitive)
- N-gram repeat > 5% (copy-paste pattern)
- Sensory density < 0.20 (dry, lifeless)
- 3+ consecutive same-starter sentences
- Banned phrases: "ửng hồng", "ánh lên", "trắng nõi", "khuôn chậu"

### Anti-Slop Files

- `studio/boot/canon-preamble.md` §8 — Anti-Slop Gates
- `studio/context/mandatory/00-anti-slop.md` — Mandatory context injection
- `studio/data/banned-words.txt` — Master banned word list
- `studio/scripts/anti_slop_validator.py` — Automated scanner

---

## CI/CD

GitHub Actions: `.github/workflows/knowledge-quality.yml`

- **yaml-parse:** All SKILL.md must parse YAML frontmatter correctly
- **knowledge-sync:** `knowledge-index.yaml` must be in sync with physical files
- **anti-slop:** Knowledge files must pass entropy + ngram thresholds

---

## File Naming Conventions

| Type | Convention |
| ---- | ---------- |
| Skill folder | `kebab-case` |
| Knowledge pack | `snake_case.md` |
| Research file | `*_research.md` |
| Glossary | `*_lexicon.md` |
| Beat sheet | `*_beats.md` |
| SFX reference | `*_sfx_*.md` |
| Agent YAML | `kebab-case.agent.yaml` |
| JSON Schema | `kebab-case.schema.json` |
| Pipeline manifest | `XX_manifest.md` |

---

## Anti-Patterns

1. **Orphan knowledge** — file exists but not in index or unreferenced by any SKILL
2. **Broken wiring** — index says `used_by: [lewd-writer]` but lewd-writer doesn't load it
3. **Multi-doc YAML** — SKILL.md frontmatter parses as 2+ YAML documents due to extra `---`
4. **Empty dependencies** — SKILL.md has `dependencies: []` but engine needs knowledge
5. **Slop prose** — generic pattern writing, lacking sensory detail, repeated vocabulary
6. **Layer violation** — Production logic in `developers/` or meta-review logic in `core/`
7. **Schema drift** — JSON Schema and Pydantic model define different fields for same output
