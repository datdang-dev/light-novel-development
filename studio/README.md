# LND Studio v2.0

> **BMAD v6.1 Compliant Light Novel Development Studio**
> Orchestrated to automate the processing of R18 explicit manga into highly detailed, sensory-dense Vietnamese Light Novel prose.

## 🚀 Quick Start

Ensure you have a fully working BMAD environment installed. LND Studio is loaded dynamically as a module.

### Core Pipelines

To begin the primary adaptation flow, use the Orchestrator command:

```bash
/gooner-alchemist
```

*This triggers the Director K agent to load the state-persisted, JIT-compiled pipeline that processes pages sequentially from input to audited output.*

### Development Tools

To verify pipeline payloads without using LLM tokens, use the Dry Run Simulator:

```bash
python3 scripts/simulator.py
```

## 🏗️ Architecture & Documentation

The studio operates purely on **Just-In-Time (JIT) Loading**, a 14-Agent diverse registry array, and strict **JSON Schema Valildation**.

For the comprehensive technical breakdown including component roles, sequence generation charts, and schema enforcement logic, please refer to the official architectural documentation:
👉 **[Read the Studio Architecture Documentation](docs/ARCHITECTURE.md)**

---

## 🛡️ Enterprise Grade Quality Gates

LND studio enforces extreme structural rigor out-of-the-box:

* **Schema Strictness**: All JSON outputs (`forensic-state`, `draft-prose`, `audit-report`) use recursive `additionalProperties: false` locked schemas. LLM Hallucination is structurally impossible.
* **State Recovery**: The pipeline checks intermediate artifacts at `step-01-initialize.md`. If a crash occurs at page 40, step 5, simply run `/gooner-alchemist` and it will resume exactly at page 40, step 5 automatically.
* **Simulation Testing**: A built-in Python JIT Compiler stringifier allows for unit-testing the exact context payloads sent to instances before money is spent.

---

## 🎭 The Cast (Agents)

All 14 specialized agents are defined in `agents/*.agent.yaml` and routed dynamically through `agent-registry.csv`.
To load them into a collaborative brainstorming session discussing studio lore or workflow improvements, run:

```bash
/party-mode
```

---
*LND Studio - Where Fantasies Become Verified Output.*
