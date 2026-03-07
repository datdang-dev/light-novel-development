---
name: "party-mode-orchestrator"
description: "Framework extension enabling terminal-based multi-agent CLI orchestration (War Room)"
version: "1.0.0"
type: "core-extension"
---

# 🥂 Party Mode Orchestrator

## Overview

The Party Mode Orchestrator is a structural extension for LND Studio that shifts execution from a single API-bound LLM to a hybrid, command-line-driven "War Room". It allows **Antigravity** (the Architect) to dynamically invoke specialized AI CLIs natively in the terminal to prevent self-bias and bypass provider-specific limitations.

## Role Assignments

- **Antigravity (Chair / Orchestrator):** Manages the meeting, analyzes forensic data (Kana role), and writes the R18 prose (Suki role).
- **Cursor CLI (`agent`):** Acts as the ruthless Quality Auditor (Riko role). Enforces `canon-rules.md` objectively.

## Architecture & Integration

- **Agent:** `studio/core/party-mode/agents/war-room-orchestrator.agent.yaml`
- **Workflow:** `studio/core/party-mode/workflows/war-room-debate.md`

## Usage

Instead of deploying the traditional `gooner-alchemist` pipeline via text prompts, the User activates Party Mode by instructing Antigravity: "Let's run Party Mode on chapter X, page Y". Antigravity will then assume the `war-room-orchestrator` persona and orchestrate the CLIs.
