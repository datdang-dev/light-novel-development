# Project Overview: Light Novel Development Framework (LND)

> **Generated:** 2026-02-06
> **Version:** 3.0 (Studio Edition)
> **Type:** Agentic Creative Framework

## Executive Summary
The **Light Novel Development Framework (LND)** is a specialized AI-agent system designed to automate and orchestrate the creation of R18 light novels from manga/hentai source material. It utilizes the **BMAD (Brave New Agent Design)** architecture, treating prompts, workflows, and personas as code components within a structured `studio/` environment.

## Technology Stack

| Category | Technology | Usage |
|----------|------------|-------|
| **Core Architecture** | BMAD | Agent/Workflow orchestration |
| **Configuration** | YAML | `studio/config/config.yaml` |
| **Logic/Instructions** | Markdown (XML) | Agent definitions & prompts |
| **Automation** | Python | Utility scripts (legacy/support) |
| **Knowledge Base** | Markdown | `studio/docs/` |

## Repository Structure

The project follows a **Monolith Framework** structure centered around the `studio` directory:

```
light_novel_development_framework/
├── studio/                  # CORE APPLICATION
│   ├── agents/              # AI Personas (L1 Managers, L2 Devs, L3 QA)
│   ├── workflows/           # Task Pipelines (gooner-alchemist, etc.)
│   ├── config/              # System Configuration
│   └── docs/                # Internal Knowledge Base
├── projects/                # User Content (Active Novels)
├── standalone/              # User Content (Single Scenes)
├── sources/                 # Raw Inputs (Untracked)
└── output/                  # Build Artifacts
```

## Key Capabilities
1.  **Orchestration**: `lnd-orchestrator` (Director K) manages the entire lifecycle.
2.  **Forensics**: `panel-forensic` workflow decomposes images into narrative data.
3.  **Adaptation**: `lewd-writer` converts data into sensory-rich R18 prose.
4.  **Quality Assurance**: `gooner-editor` (Riko) audits content against strict "Gooner" metrics.
5.  **World Building**: `world-weaver` & `character-architect` manage consistency.
