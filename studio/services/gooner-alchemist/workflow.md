---
name: "gooner-alchemist"
description: "Pipeline: Ultimate Manga Adaptation Orchestrator (V6)"
owner: "Kana (manga-adapter)"
version: "6.0.0"
web_bundle: true
validateWorkflow: './steps/step-01-initialize.md'
---

# Gooner Alchemist Pipeline (V6)

**Goal:** The definitive "Studio Grade" manga-to-prose pipeline.
**Features:** Context Injection (POC), Structured Artifacts, JSON Quality Gates, Service Integration.

**Orchestrator:** Kana (Manga Adapter).

---

## WORKFLOW ARCHITECTURE (V6)

### 1. Initialization & Setup

- **Step 1:** Initialize Pipeline & State (`step-01-initialize.md`)
  - *Action:* Validate File Integrity. Check Character Bible.
  - *Service:* Call **Aria** if unknown characters detected.

### 2. Adaptation Loop (Per Page or Batch)

**Context Injection Phase**

- **Step 1b:** Generate POC Hypothesis (`step-01b-generate-poc.md`)
  - *Input:* Bible + Previous Page State.
  - *Output:* `output/{ch}/{pg}/poc.md`
  - *Goal:* "Tell the engine what to look for."

**Forensic Phase**

- **Step 2:** Directed Forensic Scan (`step-02-forensic-analysis.md`)
  - *Input:* Image + `poc.md`
  - *Output:* `output/{ch}/{pg}/forensic.json`
  - *Agent:* Panel Forensic (Atomic)

**Context Loading**

- **Step 3:** Load Bible Context (`step-03-context-loading.md`)
  - *Input:* `forensic.json` (to filter specific lore)

**Prose Generation**

- **Step 4:** Context-Aware Drafting (`step-04-prose-generation.md`)
  - *Input:* `forensic.json` + `poc.md` + `bible`
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
3. **POC VALIDATION:** If the POC says "Asuka" but Forensic says "Empty", HALT for human review.
4. **DELEGATION:** Director K does NOT run this. Kana runs this.

---

## EXECUTION LOOP

For each page:

1. Initialize Step 1
2. Generate POC Step 1b -> poc.md
3. Forensic Scan Step 2 -> forensic.json
4. Context Loading Step 3
5. Prose Generation Step 4 -> draft.md
6. Quality Audit Step 5 -> audit.json
7. Persist Step 6
8. Finalize Step 7
