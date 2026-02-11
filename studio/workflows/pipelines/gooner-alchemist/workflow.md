---
name: "gooner-alchemist"
description: "Pipeline: Ultimate Manga Adaptation Orchestrator (V6)"
owner: "Director K (lnd-orchestrator)"
version: "6.0.0"
web_bundle: true
validateWorkflow: './steps/step-01-initialize.md'
---

# Gooner Alchemist Pipeline (V6)

**Goal:** Orchestrate the complete manga-to-light-novel adaptation pipeline with automated quality audits.

**Documentation:**

- **Full Principles, Gates & State Schema:** [See workflow-OLD.md](./workflow-OLD.md)

**Architecture:**

- **Step 1:** Initialize & State Creation
- **Step 2:** Forensic Analysis (Delegates to `panel-forensic`)
- **Step 3:** Context Loading
- **Step 4:** Prose Generation (Delegates to `prose-adapter`)
- **Step 5:** Quality Audit (Delegates to `gooner-audit`)
- **Step 6:** State Persistence
- **Step 7:** Finalize / Loop

IT IS CRITICAL THAT YOU FOLLOW THIS COMMAND: LOAD the FULL @{project-root}/studio/workflows/pipelines/gooner-alchemist/steps/step-01-initialize.md, READ its entire contents and follow its directions exactly!
