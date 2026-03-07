---
name: "gooner-alchemist"
description: "Pipeline: Ultimate Manga Adaptation Orchestrator (V6)"
owner: "Director K (lnd-orchestrator)"
version: "6.0.0"
web_bundle: true
validateWorkflow: './steps/step-01-initialize.md'
---

# Gooner Alchemist Pipeline (V6)

**Goal:** The definitive "Studio Grade" manga-to-prose and video-to-prose pipeline.
**Features:** Universal Context Horizon, Action Deduplicator, Structured Artifacts, JSON Quality Gates, Service Integration.

**Orchestrator:** Director K (LND Orchestrator).

**Architecture Reference:** [V6.1 Gooner Alchemist Pipeline](../../docs/architecture/dynamic_design/service_manga_adapter/sq_v6_1_gooner_alchemist_pipeline.puml)

---

## WORKFLOW ARCHITECTURE (V6)

### 1. Initialization & Setup

- **Step 1:** Initialize Pipeline & State (`step-01-initialize.md`)
  - *Action:* Validate File Integrity. Check Character Bible.
  - *Service:* Call **Aria** if unknown characters detected.

### 2. Adaptation Loop (Per Page or Batch)

### Context Horizon Phase

- **Step 1b:** Generate Context Horizon (`step-01b-context-horizon.md`)
  - *Input:* Next N frames/pages (`generate_horizon.py`)
  - *Output:* `output/{ch}/{pg}/context_horizon.md`
  - *Goal:* "Pre-fetch factual upcoming trajectories and flag Action Deduplication instead of hallucinating the current frame."

### PHASE 1: Dialogue-Anchor Forensics (V6.1)

- **Step 2:** Directed Forensic Scan
  - *Input:* Current Image + `context_horizon.md`
  - *Output:* `output/{ch}/{pg}/forensic.md`
  - *Agent:* Panel Forensic (Atomic)
  - *Protocol:* Execute Pure OCR -> Dialogue Alignment -> Environmental Scan -> Report Assembly.

### PHASE 2: Core Transformation Engine

- **Step 3:** Invoke Core Transformation Engine
  - *Input:* `forensic.json` + `context_horizon.md` + JIT Compiled Context
  - *JIT Compilation:* Before invoking Suki, compile `{project-root}/studio/config/pipeline-context.md` and `{project-root}/.agent/rules/lewd_writing_mechanics.md` into the agent payload `context_payload.md` to prevent mid-execution disk reads.
  - *Engine:* `studio/core/transformation-engine/workflow.md`
  - *Goal:* Perform the strict Prose Generation -> Quality Audit -> Rewrite loop agnostically.
  - *Output:* Verified `draft.json`

### 3. Commit & Handoff

- **Step 5:** Persist State
- **Step 6:** Finalize
  - *Service:* Call **Composer** to buffer the finished scene or perform "Director's Cut" optimization.

---

## CRITICAL INSTRUCTIONS

1. **ARTIFACTS:** All intermediate files MUST be saved to the dynamic execution directory provided by the runner (e.g., `{{run_dir}}`). Do NOT hardcode file paths like `{output_folder}/{chapter}/{page}/`.
2. **JSON GATES:** Do not parse "Pass/Fail" text. Parse the JSON output from Audit.
3. **HORIZON VALIDATION:** The `context_horizon.md` dictates Trajectory. The FORENSIC IMAGE dictates current Ground Truth. Do not hallucinate future facts onto the current frame.
4. **ACTION DEDUPLICATION:** If Context Horizon flags a sequence as Continuous Action, LEWD WRITER MUST MERGE THEM into a single Action Beat instead of writing repetitive short pages.
5. **DELEGATION:** Director K runs this pipeline directly. He orchestrates the hands-offs to Kana, Suki, and Riko using the `forensic-state`, `draft-prose`, and `audit-report` schemas.
6. **AUDIT FALLBACK (ERROR-CONTRACT):** If Phase 3 Audit fails, it is MANDATORY to inject the failed `audit-report` (containing the exact failed constraints and deductions) directly into Suki's prompt for the Phase 2 retry. Do not return to Phase 2 blindly.
7. **AUDIT LOOP BREAKER:** The Orchestrator MUST track `"audit_attempts": N` in the `state.yaml` file for each page. If `audit_attempts >= 3` and the page still fails, the Orchestrator MUST **STOP** the loop, record `last_error` in the state, and escalate to the user. Do NOT infinitely loop.

---

## EXECUTION LOOP

For each page/frame:

1. Initialize Step 1
2. Generate Context Horizon Step 1b -> `context_horizon.md`
3. Forensic Scan -> `forensic-state.json` (with Forensic Cache #2)
4. JIT Context Sharding Compilation -> `context_payload.md` (Optimization #1)
5. Core Transformation Engine (`forensic-state.json` + `context_payload.md` -> `draft-prose.json`)
6. Auto-Repair JSON (Optimization #5) -> Schema-validated `draft-prose.json`
7. Quality Audit with Prefetch (Optimization #3) -> `audit-report.json`
8. On FAIL: Diff-Based Revision (Optimization #8) -> Patch only failing sections
9. Persist State
10. Finalize & Handoff

### ⚡ BATCH PAGE PROCESSING (Optimization #4)

```text
BEFORE starting the per-page loop, analyze pages_pending:

FOR consecutive pages with SAME scene_tags (e.g., pages 10-14 all "bedroom"):
  → Group them as a BATCH
  → Run Forensic Scan for ALL pages in the batch in ONE session
    (Kana keeps context window open, each subsequent page uses Forensic Cache #2)
  → Run Context Loading ONCE for the batch (same scene = same rules)
  → Run Prose Generation per-page but with RETAINED context window
    (Suki does NOT re-read rules between pages in the same batch)

FOR pages with DIFFERENT scene_tags:
  → Process individually as normal (context switch required)

RESULT: ~60% reduction in context-loading overhead for multi-page scenes.
```

### ⚡ PROGRESSIVE QUALITY (Optimization #6)

```text
DURING Step 5 (Prose Generation), apply micro-audits per section:

AFTER Suki writes the ENVIRONMENT section:
  → Quick-check: sensory count ≥ 3? Smell present? Sound present?
  → IF FAIL: Fix NOW before writing the next section

AFTER Suki writes the ACTION section:
  → Quick-check: explicit detail level sufficient? SFX present?
  → IF FAIL: Fix NOW

AFTER Suki writes the DIALOGUE section:
  → Quick-check: Vietnamese only? 「」brackets? Character voice match?
  → IF FAIL: Fix NOW

RESULT: Eliminates full-prose rewrites. Issues caught at source = ~70% fewer audit failures.
```
