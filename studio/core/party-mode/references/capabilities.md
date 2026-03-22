---
name: "party-mode-orchestrator"
description: "Framework extension enabling terminal-based multi-agent CLI orchestration (War Room)"
version: "1.0.0"
type: "core-extension"
---

# 🥂 Party Mode Orchestrator (Meeting Session)

## Overview

The Party Mode Orchestrator is a structural extension for LND Studio that enables collaborative, multi-agent discussions. It allows **Antigravity** (the Meeting Chair) to dynamically convene specialized agents (Ren, Kana, Suki, Riko, etc.) to brainstorm, plan, and optimize studio workflows.

## Role Assignments

- **Antigravity (Meeting Chair):** Facilitates the session, synthesizes inputs, and maintains the agenda.
- **Specialized Agents:** Participants provide domain-specific insights based on their individual personas and professional rulesets.
- **Cursor CLI (`agent`):** Invoked for formal, unbiased auditing when the meeting results in critical rule changes or code generation.

## Architecture & Integration

- **Agent:** `studio/core/party-mode/agents/meeting-chair.agent.yaml`
- **Workflow:** `studio/core/party-mode/workflows/meeting-session.md`

## Usage

Activate by instructing Antigravity: "Start a meeting about X" or "Run Party Mode for Y". The Chair will then define the agenda and invite the relevant participant pool.
