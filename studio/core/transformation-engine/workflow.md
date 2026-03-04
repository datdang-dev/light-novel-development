---
name: "core-transformation-engine"
description: "Core Engine: Abstracted Prose Generation & Audit Loop"
owner: "Director K"
version: "1.0.0"
---

# Core Transformation Engine

**Goal:** An input-agnostic pipeline that takes a standardized `forensic-state.json` (from any source like Kana or Ren'Py) and produces a verified `draft-prose.json`.

**Orchestrator:** Director K (LND Orchestrator).

---

## WORKFLOW ARCHITECTURE

### 1. Pre-Processing (Knowledge Injection)

- **Input:** `forensic-state.json` (Specifically `content_tags`)
- **Action:** Query RAG system to fetch relevant research files and glossary terms.
- **Output:** `knowledge_payload.md`

### 2. Prose Generation (Suki)

- **Input:** `forensic-state.json` + `knowledge_payload.md` + `bible.md`
- **Agent:** Lewd Writer (Suki)
- **Protocol:** Generate R18 prose strictly adhering to the sensory rules, character voice, and formatting conventions.
- **Output:** `draft-prose.json`

### 3. Quality Audit (Riko)

- **Input:** `draft-prose.json`
- **Agent:** Quality Audit (Riko)
- **Protocol:** Score the prose against the Quality Gates (Format Compliance, Sensory Immersion, Edging Rhythm, Fetish Psychology).
- **Output:** `audit-report.json`

### 4. Rewite Loop

- **Logic:** If `audit-report.json` score < 85, OR if `status` != "PASSED":
  - **Rewind to Step 2.** Suki must rewrite the prose incorporating the constraints and suggested rewrites from `audit-report.json`.
  - Loop until `status` == "PASSED".

---

## CRITICAL INSTRUCTIONS

1. **State Persistence:** Maintain the `forensic-state`, `draft-prose`, and `audit-report` JSON objects in memory or a local DB.
2. **Schema Enforcement:** Director K must validate the output of Suki and Riko against their respective JSON schemas.
3. **No Hallucinations:** Suki must only write based on the facts provided in `forensic-state.json`. Any extra lore must come from `knowledge_payload.md` or `bible.md`.
