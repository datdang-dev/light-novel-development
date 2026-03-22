---
name: party-mode
description: "Multi-agent collaborative discussion facilitator — structured meetings between LND Studio specialist agents chaired by Antigravity."
---

# Party Mode

## Overview

Party Mode enables **structured multi-agent discussions** where LND Studio's specialized agents collaborate on complex architectural or creative problems. The meeting is chaired by Antigravity (meeting-chair agent) who maintains each guest agent's unique persona and voice throughout the discussion.

This is a facilitation engine, not a pipeline — it produces meeting minutes and action items rather than prose or data artifacts.

## On Activation

1. Load `agents/meeting-chair.agent.yaml` for chair persona
2. Load `{project-root}/studio/agent-registry.csv` for available participants
3. Define agenda topic and invite relevant agents
4. Begin meeting workflow at `workflows/meeting-session.md`

## Workflow

The meeting follows a 3-phase structure defined in `workflows/meeting-session.md`:

| Phase | Purpose |
|-------|---------|
| **Preparation** | Define agenda, invite agents, load context |
| **Discussion** | Round-table perspectives, synthesis, debate |
| **Conclusion** | Action items, meeting minutes, optional drafting |

## Structure

| Path | Purpose |
|------|---------|
| `agents/meeting-chair.agent.yaml` | Chair persona definition |
| `workflows/meeting-session.md` | Meeting protocol and phase structure |
| `references/` | Context documents for meetings |
| `logs/` | Saved meeting minutes (`{date}_{topic}.md`) |
| `riko-workspace/` | Dedicated workspace for QA agent during meetings |

## Dependencies

- **Chair**: Antigravity (meeting-chair)
- **Participants**: Any agents from `agent-registry.csv`
- **Output**: Meeting minutes in `logs/`

## Quick Reference

| Intent | Trigger | Route |
|--------|---------|-------|
| **Start meeting** | `/party-mode` | Load chair agent → `workflows/meeting-session.md` |
| **Review past meetings** | Browse `logs/` | Read meeting minutes |
