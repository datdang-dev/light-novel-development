---
name: "master-production"
description: "Pipeline: Master Production Orchestrator (V6)"
owner: "Director K (lnd-orchestrator)"
version: "6.0.0"
web_bundle: true
validateWorkflow: './steps/step-01-forensic-dispatch.md'
---

# Master Production Pipeline (V6)

**Goal:** Automate the entire LND production cycle by orchestrating specialized agents.

**Documentation:**

- **Full Architecture & Principles:** [See workflow-OLD.md](./workflow-OLD.md)

**Architecture:**

- **Step 1:** Forensic Analysis (Dispatch to Atomic)
- **Step 2:** Context Preparation (Internal)
- **Step 3:** Dialogue Scripting (Dispatch to Miki)
- **Step 4:** Prose Adaptation (Dispatch to Suki)
- **Step 5:** Quality Editing (Dispatch to Riko)

IT IS CRITICAL THAT YOU FOLLOW THIS COMMAND: LOAD the FULL @{project-root}/studio/workflows/pipelines/master-production/steps/step-01-forensic-dispatch.md, READ its entire contents and follow its directions exactly!
