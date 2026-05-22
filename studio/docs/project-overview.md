# 🌸 Project Overview: LND Studio 🌸

> **The Ultimate Multi-Agent R18 Japanese Prose Adaptation Engine**
> Executive Summary, Design Philosophy, and Architectural Principles of LND Studio.

---

## 📖 Executive Summary

LND Studio is an enterprise-grade automated pipeline designed for the adaptation and generation of Japanese adult (R18) manga, games, and light novels into sensory-dense, canonical Vietnamese prose. 

Rather than relying on generic, single-prompt AI generation—which often suffers from context drift, "AI-slop", formatting errors, and lack of thematic depth—LND Studio utilizes a highly specialized, modular **multi-persona pipeline**. By breaking down the complex workflow of literary adaptation into explicit, isolated sub-tasks (visual analysis, prose drafting, quality auditing, dialogue localization), LND Studio guarantees outputs that are both structurally validated and artistically mature.

---

## 🛠️ Technology Stack & Integrations

The LND Studio ecosystem combines state-of-the-art AI tooling with robust configuration standards:

| Component | Technology | Role / Usage |
| :--- | :--- | :--- |
| **Core Framework** | BMAD (v1.0.0) | Multi-agent lifecycle management, task routing, and skill injection. |
| **Orchestrator** | Director K (`lnd-orchestrator`) | Dynamic state management, error recovery, and process delegation. |
| **OCR & Vision** | Manga-OCR / Claude Vision | Forensic visual data extraction and coordinate-based action mapping. |
| **JSON Schemas** | draft-prose, forensic-state, continuity-ledger | Authoritative validation contracts for inter-agent communication. |
| **Continuous Integration** | GitHub Actions / persistent terminals | Automated testing, verification gates, and deployment scripts. |
| **Database** | SQLite + ruvector.db | Vector-delta based lore, glossary, and fetish knowledge retrieval. |

---

## 🔒 Design & Architectural Philosophy

The development of LND Studio is governed by three non-negotiable engineering principles:

### 1. State Resilience and Persistence
Adaptation pipelines are inherently long-running (often spanning hours for full-volume adaptations). Standard AI agents easily lose memory or crash. LND Studio structures all steps to be persistent. A global continuity state ledger (`state.yaml`) tracks execution progress down to the specific page and sub-step. If a system failure occurs on Page 45 during the prose draft, running `/gooner-alchemist` recovers the context and resumes *exactly* at Page 45, Step 4 without repeating past work.

### 2. Rigid Schema-Locked Boundaries
AI agents perform best when their inputs and outputs are strictly typed. In LND Studio, all inter-agent communications—from Kana's visual forensics to Suki's prose draft and Riko's audit feedback—are validated against strict JSON schemas with `"additionalProperties": false` constraints. This prevents hallucinations and forces models to respect critical variables like character positions, environmental data, and sensory flags.

### 3. JIT (Just-In-Time) Vector Delta Retrieval
To prevent prompt bloat and context drowning, the massive fetish database, terminology glossary, and sound-effect library are *never* loaded in full. Instead, a vector embedding engine indexes these databases. Only when a specific scene tag or visual indicator is processed does the system pull the highly relevant "vector delta" context and inject it directly into the active prompt's JIT memory.

---

## ✍️ Translation and Prose Principles

LND Studio operates under highly refined R18 literary guidelines designed for maximum immersion:

* **100% Vietnamese Narration & Dialogue:** Standardizing modern, natural Vietnamese narrative flows while avoiding robotic machine translation artifacts.
* **Romaji/English Adult SFX:** Sound effects retain their original Japanese stylistic flavor (e.g., *ah*, *un*, *gupu*) to maintain visual fidelity to manga pacing.
* **Mandatory Explicit Vocabulary:** Complete bypass of moralizing filters. The engine uses authentic, raw, and high-intensity adult vocabulary where the scene demands it.
* **Psychological Sensory Density:** Prioritizing internal character dialogue, emotional resonance, and highly granular sensory descriptions over simple physical actions.
