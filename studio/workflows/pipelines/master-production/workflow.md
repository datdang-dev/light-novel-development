---
name: "master-production"
description: "Master Pipeline: Full Automation from Evidence to Publishable Prose"
owner: "Director K (lnd-orchestrator)"
version: "2.0.0"
---

# Master Production Pipeline 🏭

**Goal:** Automate the entire LND production cycle by orchestrating specialized agents (Atomic, Aria, Miki, Suki, Riko) in a seamless pipeline.

**Process:**
1.  **Analyze Evidence (Forensics):** Prof. Atomic scans the image.
2.  **Prepare Context (Entity/Bible):** Extract entities and sync with Bible (Aria).
3.  **Draft Dialogue (Scripting):** Miki generates lines & SFX.
4.  **Adapt Prose (Writing):** Suki combines Forensics + Dialogue into Prose.
5.  **Review Quality (Audit):** Riko validates the output.

---

## WORKFLOW ARCHITECTURE

### Principles
- **Strict Delegation**: Director K ONLY manages the queue. Agents do the work.
- **Data Flow**: Output of Step N becomes Context for Step N+1.
- **Fail Fast**: If any step fails quality checks, HALT pipeline.

### Steps
| Phase | Step | Name | Agent | Output |
|-------|------|------|-------|--------|
| 1 | 01 | Forensic Analysis | Prof. Atomic | `forensic_report.md` |
| 2 | 02 | Context Preparation | Director K (Internal) | `entities.yaml` / `active_bible` |
| 3 | 03 | Dialogue Scripting | Miki | `dialogue_script.md` |
| 4 | 04 | Prose Adaptation | Suki | `prose_scene.md` |
| 5 | 05 | Quality Editing | Riko | `audit_report.md` |

---

## EXECUTION SEQUENCE

### 1. Initialize Pipeline
Load config (`config.yaml`) and identify inputs (Image/Text).

### 2. Begin Phase 1: Forensics
Load and execute: `./steps/step-01-forensic-dispatch.md`
