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

**Forensic Phase**

- **Step 2:** Directed Forensic Scan (`step-02-forensic-analysis.md`)
  - *Input:* Current Image + `context_horizon.md`
  - *Output:* `output/{ch}/{pg}/forensic.json`
  - *Agent:* Panel Forensic (Atomic)

**Context Loading**

- **Step 3:** Load Bible Context (`step-03-context-loading.md`)
  - *Input:* `forensic.json` (to filter specific lore)

**Prose Generation**

- **Step 4:** Context-Aware Drafting (`step-04-prose-generation.md`)
  - *Input:* `forensic.json` + `context_horizon.md` + `bible`
  - *Output:* `output/{ch}/{pg}/draft.md`
  - *Agent:* Lewd Writer (Suki)

**Quality Assurance**

- **Step 5:** Structured Audit (`step-05-quality-audit.md`)
  - *Input:* `draft.md`
  - *Output:* `audit.json` (`{score, issues, fix}`)
  - *Logic:* If Score < 85 -> **Rewind to Step 4** with `fix` instructions.

### 3. Commit & Handoff

- **Step 6:** Persist State (`step-06-state-persistence.md`)
- **Step 7:** Finalize (`step-07-finalize.md`)
  - *Service:* Call **Composer** to buffer the finished scene.

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
2. Generate Context Horizon Step 1b -> context_horizon.md
3. Forensic Scan Step 2 -> forensic.json
4. Context Loading Step 3
5. Prose Generation Step 4 -> draft.md
6. Quality Audit Step 5 -> audit.json
7. Persist Step 6
8. Finalize Step 7
