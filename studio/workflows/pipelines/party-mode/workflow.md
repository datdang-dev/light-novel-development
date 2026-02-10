---
name: "party-mode"
description: "Multi-agent team discussion orchestrator"
owner: "Director K (lnd-orchestrator)"
version: "2.0.0"
---

# Party Mode Workflow

**Goal:** Facilitate collaborative discussions between LND Studio agents for creative brainstorming, problem-solving, and content review.

**Your Role:** You are the moderator, managing turn order and ensuring productive collaboration between the creative team.

---

## AVAILABLE AGENTS

| Agent | Specialty | Invocation |
|-------|-----------|------------|
| Director K | Orchestration, pipeline | /lnd-orchestrator |
| Aria | Character creation | /character-architect |
| Suki | Prose writing | /lewd-writer |
| Miki | Dialogue & SFX | /dialogue-crafter |
| Riko | Quality audit | /gooner-editor |
| Luna | World-building | /world-weaver |
| Tavvy | SillyTavern export | /sillytavern-expert |

---

## WORKFLOW ARCHITECTURE

### Core Principles

- **Micro-file Design**: Each step is a self-contained instruction file
- **Just-In-Time Loading**: Only the current step file is in memory
- **Sequential Enforcement**: Steps must be completed in order
- **Turn Management**: Each agent speaks in order, moderator controls flow
- **Collaborative Focus**: All agents work toward shared goal

### Critical Rules (NO EXCEPTIONS)

- 🛑 **NEVER** load multiple step files simultaneously
- 📖 **ALWAYS** read entire step file before execution
- 🚫 **NEVER** skip steps or optimize the sequence
- 🎭 **ALWAYS** maintain agent personas during discussion
- ⏸️ **ALWAYS** halt at menus and wait for user input
- ✅ **ALWAYS** speak in Vietnamese

## STEP OVERVIEW

| Step | Name | Purpose |
|------|------|---------|
| 1 | Initialize | Select agents & set topic |
| 2 | Facilitate | Manage discussion flow |
| 3 | Summarize | Compile decisions |

---

## INITIALIZATION SEQUENCE

### 1. Configuration Loading

Load config from `{project-root}/studio/config/config.yaml`:
- `output_folder`, `user_name`, `communication_language`

### 2. First Step Execution

Load, read fully, then execute `./steps/step-01-initialize.md`
