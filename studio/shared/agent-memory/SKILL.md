---
name: agent-memory
description: "Persistent learning layer for specialist agents — records what works and what fails across pipeline runs. Use when the user says 'save learnings', 'load memory', or 'agent memory'."
---

# Agent Memory Layer

## Overview

The Agent Memory Layer gives specialist agents (Suki, Riko, Kana) **persistent memory across pipeline runs**. Instead of starting cold every time, agents can reference past successes and failures — vocabulary that scored well, audit patterns, and forensic shortcuts.

Memory files are **append-only** and read during context loading as part of the JIT payload.

## On Activation

1. Determine mode: `READ` (context loading) or `WRITE` (post-audit persistence)
2. Resolve memory path at `{output_folder}/_pipeline/{project}/agent-memory/`
3. Execute appropriate mode below

## Modes

### READ Mode (During Context Loading — Step 3)

| Check | Action |
|-------|--------|
| Memory file exists? | Append to agent's context payload |
| Exceeds 2000 tokens? | Summarize: keep last 10 entries + 3-line pattern summary |

### WRITE Mode (After Audit PASS — Step 6)

| Agent | What to Record |
|-------|----------------|
| **Suki** (≥90 score) | Scene vibes, effective vocabulary, sensory ratios |
| **Suki** (revision needed) | Riko's flagged category, fix applied, bad pattern to avoid |
| **Riko** | Score, weakest/strongest categories |
| **Kana** | Forensic cache reuse, delta item counts |

## Memory File Structure

```text
{output_folder}/_pipeline/{project}/agent-memory/
├── suki-memory.md
├── riko-memory.md
└── kana-memory.md
```

## Dependencies

- **Upstream**: Pipeline orchestrator (gooner-alchemist) triggers READ/WRITE at appropriate steps
- **Integration**: JIT Context Sharding (context loading) and State Persistence (bible-sync)
