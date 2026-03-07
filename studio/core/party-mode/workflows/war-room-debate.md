---
name: "war-room-debate"
description: "Workflow for Antigravity engaging Cursor CLI in a QA Loop"
owner: "Antigravity (war-room-orchestrator)"
version: "2.0.0"
---

# ⚔️ War Room Debate Workflow (Party Mode)

**Goal:** Execute the Gooner Alchemist logic natively in the terminal by splitting Generation and QA across two different AI providers to eliminate self-bias.

## Phase 1: Context & Generation (Antigravity's Turn)

1. **Initialize:** Read the target source material (Manga page or prompt).
2. **Forensics (Kana Mode):** Antigravity analyzes the image/text context, establishing the forensic baseline.
3. **Drafting (Suki Mode):** Antigravity generates the first draft of the R18 prose, adhering strictly to `{project-root}/studio/config/pipeline-context.md` and the Canon Rules.
4. **Staging:** Antigravity saves this draft to a temporary file (e.g., `tmp_draft.md` in the current working directory).

## Phase 2: Independent Audit (Cursor's Turn)

1. **CLI Invocation:** Antigravity opens a terminal and runs the `agent` command:

   ```bash
   agent -f studio/core/party-mode/riko-workspace/.cursorrules "Read tmp_draft.md. Follow AUDIT_STANDARD_v2.md exactly. Output full structured JSON as defined in Phase 6."
   ```

2. **Waiting:** Antigravity monitors the terminal output, waiting for Cursor to finish its analysis.
3. **Parsing:** Antigravity extracts the structured JSON from Cursor's output. The JSON includes per-category scores (`metrics`, `qualitative`), `violations` with line numbers, and `top_3_fixes`.

## Phase 3: Synthesis & Revision

1. **Review:** Antigravity reads the structured JSON output from Cursor.
2. **Conditional Loop:**
   - IF `pass: false`: Antigravity uses the `violations` and `top_3_fixes` to perform **diff-based revision** — only rewriting the failing sections, not the entire prose.
   - IF `pass: true`: Antigravity moves the file from `tmp_draft.md` to the official `_lnd-output` folder structure.
3. **Escalation:** If the loop fails 3 times, Antigravity halts and asks the User for manual intervention.

---
**CRITICAL:** Under no circumstances should Antigravity pretend to be Cursor or simulate the `agent` command output. Antigravity MUST execute the actual bash command and wait for the real Cursor agent's reply.
