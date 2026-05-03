# Light Novel Development (LND) Studio

LND Studio is a highly specialized, agentic framework designed for the adaptation and generation of Japanese R18 light novels and manga prose. It is built upon the BMAD AI orchestrator principles but heavily modified to enforce strict narrative structures, canonical state-tracking, and forensic-level quality gates.

## Core Architecture

The LND Studio utilizes a multi-persona pipeline to orchestrate content transformation:

- **Kana (Data Forensics):** Extracts visual data, metadata, and scene context from raw frames.
- **Suki (Lewd Writer):** The creative engine responsible for spinning raw metadata into R18 Vietnamese prose, adhering to the strict Lewd Writing Mechanics and sensory density requirements.
- **Riko (Quality Audit):** The ruthless QA auditor, guarding the gates of the output folder against any AI hallucinations, OOC dialogue, or format violations using the GOONER_AUDIT_FRAMEWORK.

## 🥂 Party Mode (Multi-Agent CLI Orchestration)

LND Studio now features a **Multi-Agent CLI Architecture** (The "War Room") to completely eliminate model self-bias and bypass provider-specific limitations.

Instead of a single LLM trying to write and audit itself, **Party Mode** orchestrates multiple specialized AI CLI engines seamlessly in the terminal:

1. **Antigravity (The Chair):** Orchestrates the loop, analyzes forensics (Kana), and drafts the prose (Suki) based on the `pipeline-context.md`.
2. **Cursor CLI (`agent`):** Injected as the objective **Riko** auditor. Cursor is invoked dynamically in the background to score Antigravity's drafts ruthlessly against `canon-rules.md` and the 5-Category QA gate.

This Red-Team/Blue-Team loop forces the orchestrator to repeatedly rewrite its drafts until the independent CLI auditor passes it, ensuring the highest possible quality for adult fiction adaptation.

## Project Structure

- `studio/config/`: Contains the global contextual rules (`canon-rules.md`, `pipeline-context.md`).
- `studio/agents/`: Defines the agent personas and capabilities.
- `studio/core/party-mode/`: The structural extension housing the War Room workflows and CLI workspaces.
- `_lnd-output/`: The finalized, QA-approved output chapters.
