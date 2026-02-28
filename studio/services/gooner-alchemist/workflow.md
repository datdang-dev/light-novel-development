---
name: "gooner-alchemist"
description: "Pipeline: Ultimate Manga Adaptation Orchestrator (V6)"
owner: "Kana (manga-adapter)"
version: "6.0.0"
web_bundle: true
validateWorkflow: './steps/step-01-initialize.md'
---

# Gooner Alchemist Pipeline (V6)

**Goal:** The definitive "Studio Grade" manga-to-prose and video-to-prose pipeline.
**Features:** Universal Context Horizon, Action Deduplicator, Structured Artifacts, JSON Quality Gates, Service Integration.

**Orchestrator:** Kana (Manga Adapter).

**Architecture Reference:** [V6.1 Gooner Alchemist Pipeline](../../docs/architecture/dynamic_design/service_manga_adapter/sq_v6_1_gooner_alchemist_pipeline.puml)

---

## WORKFLOW ARCHITECTURE (V6)

### 1. Initialization & Setup

- **Step 1:** Initialize Pipeline & State (`step-01-initialize.md`)
  - *Action:* Validate File Integrity. Check Character Bible.
  - *Service:* Call **Aria** if unknown characters detected.

### 2. Adaptation Loop (Per Page or Batch)

**Context Horizon Phase**

- **Step 1b:** Generate Context Horizon (`step-01b-context-horizon.md`)
  - *Input:* Next N frames/pages (`generate_horizon.py`)
  - *Output:* `output/{ch}/{pg}/context_horizon.md`
  - *Goal:* "Pre-fetch factual upcoming trajectories and flag Action Deduplication instead of hallucinating the current frame."

**PHASE 1: Dialogue-Anchor Forensics (V6.1)**

- **Step 2:** Directed Forensic Scan
  - *Input:* Current Image + `context_horizon.md`
  - *Output:* `output/{ch}/{pg}/forensic.md`
  - *Agent:* Panel Forensic (Atomic)
  - *Protocol:* Execute Pure OCR -> Dialogue Alignment -> Environmental Scan -> Report Assembly.

**PHASE 2: Dialogue-Driven Prose Generation (V6.1)**

- **Step 3:** Prose Adaptation
  - *Input:* `forensic.md` + `context_horizon.md` + `bible.md`
  - *Output:* `output/{ch}/{pg}/draft.md`
  - *Agent:* Lewd Writer (Suki)
  - *Protocol:* Execute Context Loading -> Environment Prose -> Dialogue-Driven Action (Chain Reaction) -> Internal Quality Check (Gate 0).

**Quality Assurance**

- **Step 4:** Structured Audit (`step-04-quality-audit.md`)
  - *Input:* `draft.md`
  - *Output:* `audit.json` (`{score, issues, fix}`)
  - *Agent:* Quality Audit (Riko)
  - *Logic:* If Score < 85 -> **Rewind to Step 3** with `fix` instructions.

### 3. Commit & Handoff

- **Step 5:** Persist State
- **Step 6:** Finalize
  - *Service:* Call **Composer** to buffer the finished scene or perform "Director's Cut" optimization.

---

## CRITICAL INSTRUCTIONS

1. **ARTIFACTS:** All intermediate files MUST be saved to the structure: `{output_folder}/{chapter}/{page_number}/`.
2. **JSON GATES:** Do not parse "Pass/Fail" text. Parse the JSON output from Audit.
3. **HORIZON VALIDATION:** The `context_horizon.md` dictates Trajectory. The FORENSIC IMAGE dictates current Ground Truth. Do not hallucinate future facts onto the current frame.
4. **ACTION DEDUPLICATION:** If Context Horizon flags a sequence as Continuous Action, LEWD WRITER MUST MERGE THEM into a single Action Beat instead of writing repetitive short pages.
5. **DELEGATION:** Director K does NOT run this. Kana runs this.

---

## EXECUTION LOOP

For each page/frame:

1. Initialize Step 1
2. Generate Context Horizon Step 1b -> `context_horizon.md`
3. Forensic Scan (Phase 1) -> `forensic.md`
4. Prose Generation (Phase 2) -> `draft.md`
5. Quality Audit -> `audit.json`
6. Persist State
7. Finalize & Handoff
