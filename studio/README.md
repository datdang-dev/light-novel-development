# LND Studio V7.0 (Light Novel Development Studio)

> **The Ultimate Multi-Agent Japanese R18 Prose Adaptation Engine**
> Operating on the **BMAD Framework**, LND Studio is an enterprise-grade automated pipeline designed to transform visual media (Manga, Ren'Py Scripts) into sensory-dense, canonical Vietnamese Light Novel prose using strict JSON state contracts and specialized Agent Personas.

---

## 🏗️ The Multi-Agent Ecosystem

LND Studio operates using a specialized team of **16 AI Agents**, orchestrated completely dynamically. There is no single massive prompt; instead, strict workflows isolate concerns:

- 🎬 **Director K** (`lnd-orchestrator`): The Boss. Owns the core pipelines, manages state (`state.yaml`), and enforces delegations.
- 🔬 **Dr. Atomic** (`panel-forensic`): Visual forensic analysis. Extracts objects, bodily fluids, panel flow, and translates SFX from raw images.
- 🖼️ **Kana** (`manga-adapter`): Visual Context Specialist. Generates POC (Proof of Concept) hypothesis to bridge image context.
- ✍️ **Suki** (`lewd-writer`): The R18 Prose Specialist. Handles the "Lewd/Dark" narrative tone and psychological depth.
- 🛡️ **Riko** (`gooner-editor` / Quality Audit): The uncompromising Forensic Gatekeeper. Audits Suki's drafts on a 100-pt scale and forces rewrites if standards fail.

---

## 🚀 Core Pipelines

LND Studio provides several automation pipelines triggered via `/slash` commands:

### 1. The Gooner Alchemist (`/gooner-alchemist`)
The flagship 8-Step pipeline for manga-to-prose adaptation. 
Run by **Director K**, the pipeline flows sequentially:
1. **Initialize & Horizon:** Load `state.yaml` and look-ahead trajectory.
2. **Forensic Analysis:** Request Dr. Atomic for visual extractions (`forensic.md`).
3. **Context Loading:** JIT (Just-In-Time) compilation of Lore + Output.
4. **Prose Generation:** Request Suki to draft the text (`draft.md`).
5. **Quality Audit:** Request Riko to grade the text (`audit_feedback.json`). Auto-rewrites if failed.
6. **State Persistence:** Write continuity ledger and proceed to the next page.

### 2. RenPy Adaptation (`/renpy-adaptation`)
Extracts AST from `.rpy` game scripts, builds a semantic payload, and directly feeds it into the Transformation Engine (Suki), bypassing the visual step.

---

## 📁 Folder Architecture (The Context Tree)

The repository is structured to prioritize AI readability and modularity:

```text
studio/
├── agents/            # Individual Agent Definitions (.agent.yaml)
├── core/              # Foundation Engines (lewd-writer, panel-forensic, party-mode)
├── services/          # Business Logic Pipelines (gooner-alchemist, renpy, etc.)
├── modules/           # Reusable Utility Services (sfx-lookup, fetish-guidance)
├── shared/            # Cross-cutting concerns (onboarding, agent-memory)
├── knowledge/         # Canonical Databases (sfx/, glossaries/, fetish-db/)
├── schemas/           # Strict JSON Schema Contracts (forensic-state, draft-prose)
├── config/            # Global Config (pipeline-context.md, canon-rules)
├── docs/              # Architectural diagrams (.puml) & LLM developer guides
└── tools/             # Python utilities (generate_horizon.py, simulator.py)
```

---

## 🔒 Engineering Principles

1. **State Resilience**: Pipelines are structurally persistent. If a crash occurs at Page 40, Step 5, running `/gooner-alchemist` resumes *exactly* at Page 40, Step 5.
2. **Schema Locked**: All inter-agent communication (Forensic -> Prose -> Audit) MUST validate against rigid JSON schemas (`additionalProperties: false`). Hallucination is impossible across boundaries.
3. **Decentralized Knowledge**: Lore and SFX rules are not stuffed into single prompts. They live in `knowledge/`, summoned only when a specific Vector Delta requires them.

---

## 📖 For Developers & AI Agents (LLMs)

If you are an AI assistant or a new developer modifying this framework, please immediately read:
👉 **[docs/LLM_DEVELOPER_GUIDE.md](docs/LLM_DEVELOPER_GUIDE.md)** for a deep dive into how to build new services, inject knowledge, and modify agent YAMLs without breaking the framework.

*LND Studio - Where Fantasies Become Structurally Verified Output.*
