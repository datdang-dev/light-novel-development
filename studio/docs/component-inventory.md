# Component Inventory: LND Agents

> **Scope:** `studio/agents/`
> **Total Agents:** 7

## L1: Management Layer (Orchestration)
*Responsible for receiving user intent, routing tasks, and maintaining project state.*

| Agent ID | Persona | Role | Key Functions |
|----------|---------|------|---------------|
| `lnd-orchestrator` | **Director K** 👑 | Team Conductor | Task Routing, Session Mgmt, Party Mode Host |

## L2: Development Layer (Creation)
*Responsible for generating content and executing creative tasks.*

| Agent ID | Persona | Role | Key Functions |
|----------|---------|------|---------------|
| `lewd-writer` | **Suki** 🔥 | Prose Specialist | Sensory-rich writing, NSFW descriptions |
| `dialogue-crafter` | **Miki** 💋 | Dialogue Specialist | Speech patterns, Verbal tics, SFX |
| `world-weaver` | **Luna** 🌍 | World Builder | Lore consistency, Setting description |
| `character-architect` | **Aria** 🎭 | Character Designer | Character Cards (ST), Personality profiles |
| `content-architect` | **Kuro** 🏗️ | Structure Specialist | Outlining, Blueprints, Pacing control |

## L3: Quality Assurance Layer (Audit)
*Responsible for verifying output against quality standards.*

| Agent ID | Persona | Role | Key Functions |
|----------|---------|------|---------------|
| `gooner-editor` | **Riko** ✅ | QA/Audit | Sensory metrics, "Gooner" score, Pacing check |

## Workflow Integration
Agents are typically invoked via specific workflows:
- **Manga Adaptation**: `gooner-alchemist` (Uses Director K -> Suki -> Riko)
- **Character Creation**: `character-bible` (Uses Aria)
- **Planning**: `scene-expansion` (Uses Kuro)
