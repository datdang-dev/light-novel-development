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

- **Input:** `forensic-state.json` + `knowledge_payload.md` + `bible.md` + `continuity-ledger.json`
- **Agent:** Lewd Writer (Suki)
- **Protocol:** Generate R18 prose. Suki MUST read the `continuity-ledger.json` to maintain outfit, fluid, and stamina consistency from previous pages.
- **Output:** `draft-prose.json`

### 3. Quality Audit (Riko)

- **Input:** `draft-prose.json` + `continuity-ledger.json`
- **Agent:** Cursor CLI Auditor (Riko)
- **Protocol:** Score the prose and generate a `continuity_update`. Execute: `agent -f {project-root}/studio/core/party-mode/riko-workspace/.cursorrules "Read draft-prose.json and continuity-ledger.json. Output strict JSON."`
- **Output:** `audit-report.json`

### 4. Rewrite & Commit Loop

- **Logic:** If `audit-report.json` score < 85, OR if `status` != "PASSED":
  - **Rewind to Step 2.** Suki must rewrite incorporating fix instructions.
- **On PASS:**
  - **Commit State:** Director K must update `continuity-ledger.json` using the `continuity_update` block from Riko's audit report.
  - Loop finished for this page.

---

## CRITICAL INSTRUCTIONS

1. **State Persistence:** Maintain the `forensic-state`, `draft-prose`, and `audit-report` JSON objects in memory or a local DB.
2. **Schema Enforcement:** Director K must validate the output of Suki and Riko against their respective JSON schemas.
3. **No Hallucinations:** Suki must only write based on the facts provided in `forensic-state.json`. Any extra lore must come from `knowledge_payload.md` or `bible.md`.
