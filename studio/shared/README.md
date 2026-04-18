# Shared — Cross-Cutting Concerns

This directory contains **cross-cutting services** used by multiple agents and pipelines.

## Subdirectories

### `agent-memory/`
Provides persistent memory and context-carryover capabilities for agents across sessions. Enables agents to recall previous interactions, decisions, and learned preferences.

- **SKILL.md:** `shared/agent-memory/SKILL.md`
- **Consumers:** All agents (via Director K orchestration)

### `onboarding/`
Handles first-time setup and project initialization workflows. Guides new users through configuring LND Studio for their specific manga/source material.

- **SKILL.md:** `shared/onboarding/SKILL.md`
- **Consumers:** Director K, System Engineer (Mavis)
