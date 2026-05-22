# 🌸 Light Novel Development (LND) Studio 🌸

> **The Ultimate Multi-Agent R18 Japanese Prose Adaptation Engine**
> Built on advanced agentic orchestration principles and optimized for forensic visual analysis, sensory-dense Vietnamese translation, and ruthless quality auditing.

---

## 🔮 Core Architecture: The 6-Layer Framework

LND Studio is governed by a strict, modular **6-Layer Architecture** that isolates infrastructure, domain knowledge, agent personas, and business execution workflows:

```text
┌──────────────────────────────────────────────────────────────┐
│  LAYER -1: INFRASTRUCTURE (Global Shared Concerns)          │
│  ├── schemas/           # Rigid JSON Contracts (Authoritative)│
│  ├── rules/            # Global Writing Standards             │
│  └── context/mandatory/ # Always-loaded Context Files         │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│  LAYER 0: KNOWLEDGE BASE (Central Brain DBs)                │
│  └── knowledge/        # Fetish DB, SFX Suggester, Trope Packs│
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│  LAYER 1: ABSTRACT / ORCHESTRATION (Boss Control Layer)      │
│  └── agents/lnd-orchestrator.agent.yaml (Director K)         │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│  LAYER 2: AGENT LAYER (10 Specialized Agent Personas)        │
│  └── agents/*.agent.yaml governed by agent-registry.yaml      │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│  LAYER 3: SERVICE LAYER (Automated Pipelines & Engines)      │
│  ├── services/         # Multi-Agent Orchestrated Pipelines   │
│  ├── core/            # Atomic Engines (e.g. Lewd Writer)    │
│  └── modules/           # Stateless Knowledge-Backed Utilities │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│  LAYER 4: RESOURCE LAYER (Sequential Executions)            │
│  ├── steps/           # Sequential script instructions       │
│  └── resources/      # Runtime states and session files     │
└──────────────────────────────────────────────────────────────┘
```

---

## 🎭 The Agent Roster (10 Specialists)

The studio utilizes a diverse roster of specialized AI agents, defined dynamically in `studio/agents/agent-registry.yaml`:

| Persona | Code | Role | Description |
| :--- | :---: | :--- | :--- |
| **Director K** | `DIR` | **Orchestration Leader** | Coordinates all pipeline steps, handles state recovery, and delegates tasks. |
| **Dr. Atomic** | `ATO` | **Panel Forensic Auditor** | Deep forensic analysis of manga panels (character coordinates, raw actions). |
| **Kana** | `KAN` | **Manga Adaptation Expert** | Visual context specialist; translates visual panels into descriptive prose schemas. |
| **Suki** | `SUK` | **Lewd Prose Specialist** | Creative engine producing sensory-dense Vietnamese R18 prose with deep psychology. |
| **Riko** | `RIK` | **Forensic QA Auditor** | Ruthless editor grading drafts (0-100) and forcing rewrites on quality failure. |
| **Aria** | `ARI` | **Character Builder** | Manages character profiles, archetypes, and dynamic card generation. |
| **Miki** | `MIK` | **Dialogue Scripting** | Specializes in direct speech, character tone consistency, and custom SFX suggestions. |
| **Orion** | `ORI` | **Continuity Enforcer** | Enforces narrative state-tracking and ledger synchronization across volume boundaries. |
| **Composer** | `COM` | **Chapter Composer** | Compiles page segments, checks formatting, and produces release packages. |
| **Luna** | `LUN` | **World Weaver** | Expert in dark fantasy world-building, lore synchronization, and tropes. |

---

## 🚀 Core Automation Pipelines

LND Studio provides highly integrated workflows tailored for various source materials:

1. **The Gooner Alchemist (`/gooner-alchemist`)**
   * *Manga-to-Novel Pipeline:* Standard 8-Step pipeline bridging visual forensic panels (`panel-forensic`) with sensory prose expansion (`lewd-writer`) and recursive QA audit gates (`quality-audit`).
2. **RenPy Adaptation (`/renpy-adaptation`)**
   * *Game script parsing:* Extracts semantic dialogues, choices, and state transitions directly from `.rpy` scripts, converting them into rich light novel formats.
3. **Dialogue & SFX Scripting (`/dialogue-scripting`)**
   * *Contextual translation:* Automatically localizes dialogues and injects highly optimized, Romaji-based adult SFX using a custom lexicon database.
4. **SillyTavern Card Export (`/st-card-export`)**
   * *Interactive Roleplay integration:* Generates advanced Character Card profiles (ST V3 standard) directly from light novel state ledgers.

---

## 🥂 Party Mode (Red-Team / Blue-Team CLI Orchestration)

To bypass single-LLM validation bias, **Party Mode** orchestrates multiple distinct CLI processes in the terminal:

1. **Antigravity (The Chair):** Orchestrates the adaptation flow, manages image analytics (Kana), and drafts the prose (Suki).
2. **Cursor CLI (`agent`):** Injected as the independent, objective **Riko** auditor. Cursor runs in the background, grading drafts against the 100-point rubrics in `studio/config/canon-rules.md`.

This adversarial setup ensures that all outputs are repeatedly rewritten until they pass the rigid quality requirements, completely eliminating "AI-slop".

---

## 📁 Encapsulated Repository Structure

The codebase has been fully refactored and cleaned up, removing all redundant local folders and AI assistant trash files:

```text
lnd_dev/
├── studio/
│   ├── agents/         # Dynamic agent persona specifications (.agent.yaml)
│   ├── core/           # Core execution engines (lewd-writer, panel-forensic, party-mode)
│   ├── services/       # Orchestrated multi-step business pipelines
│   ├── modules/        # Reusable stateless utilities (sfx-lookup, style-enforcer)
│   ├── rules/          # 18+ prose, POV, and formatting rule files (encapsulated)
│   ├── schemas/        # Strict JSON validation contracts for inter-agent communication
│   ├── config/         # Global configuration (canon-rules.md, pipeline-context.md)
│   ├── knowledge/      # SQLite memory database, fetish dictionary, glossaries
│   ├── shared/         # Shared agent memory and onboarding contexts
│   ├── docs/           # Architecture (.puml), manuals, guides, index
│   └── output/         # Runtime working folder
│
├── _lnd-output/         # Finalized, QA-approved novels and captions
├── sources/            # Raw input files (manga folders, .rpy files)
└── CLAUDE.md           # Quick start rules and GitNexus call graph configurations
```

---

## 📖 Accessing Documentation

For deep technical dives, setup guides, and development manuals, navigate to:
👉 **[LND Studio Documentation Index](file:///home/datdang/working/lnd_dev/studio/docs/index.md)** 👈

*LND Studio - Where Fantasies Become Structurally Verified Output.*
