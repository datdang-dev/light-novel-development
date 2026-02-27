---
name: 'step-01b-context-horizon'
description: 'Step 01b: Generate Context Horizon'
---

# Universal Context Horizon

**Progress: Step 1b of 7** - Next: Forensic Analysis

**Goal:** Look ahead `N` frames/pages to build a factual Scene Trajectory and identify continuous Action Beats for Suki to foreshadow and deduplicate. **CRITICAL:** This replaces predictive hallucination with actual upcoming visual evidence.

## 0. PRE-EXECUTION GATE (MANDATORY)

### a) Load Pipeline State

Read `{stateFile}` (`{output_folder}/_pipeline/{project}/state.yaml`) and extract:

- `current_page` - page being processed
- `pages_pending` - pages still to process

### b) Verify Prior State

```markdown
IF current_page IS NOT first page AND previous_page state IS MISSING:
  ─────────────────────────────────────────────
  🚫 GATE BLOCKED: PRIOR STATE MISSING
  📋 Missing: {output_folder}/_pipeline/{project}/page-{prev}-state.yaml
  📤 ACTION: Cannot generate hypothesis without prior context.
  ─────────────────────────────────────────────
  HALT - DO NOT PROCEED
```

## 1. Announce Execution

OUTPUT to user:

```markdown
─────────────────────────────────────────────
📤 GENERATING CONTEXT: Universal Context Horizon
📋 TASK: Scanning {WINDOW_SIZE} upcoming frames/pages from {current_page}
📁 OUTPUT: {output_folder}/{chapter}/{page}/context_horizon.md
─────────────────────────────────────────────
```

## 2. Trigger Horizon Generator

*Determine medium mode (video/manga) based on project specs.* Default window for video is 10, manga is 3.

```bash
# Execute the Horizon Generator Script
# Output: {output_folder}/{chapter}/{page}/context_horizon.md
python3 {project-root}/studio/services/gooner-alchemist/tools/generate_horizon.py \
  --state "{output_folder}/_pipeline/{project}/state.yaml" \
  --mode "video" \
  --window 10 \
  --out "{output_folder}/{chapter}/{page}/context_horizon.md"
```

## 3. Verify Output

**GATE CHECK - MANDATORY**

Check that `context_horizon.md` exists. It should contain:

- **Look-Ahead Window:** Confirmation of frames analyzed.
- **Concrete Trajectory:** Foreshadowing anchor points.
- **Action Deduplicator Flag:** Instructions on whether to merge redundant frames.

```markdown
IF FILE NOT EXISTS:
  🚫 HORIZON GENERATION FAILED
  ACTION: Re-run script or manual intervention required.
  HALT - DO NOT PROCEED
```

## 4. Human Review (Optional)

Display the Context Horizon summary to the user for quick verification if Redundancy was triggered.

## 5. Update Pipeline State

Update `{stateFile}`:

```yaml
horizon_generated:
  - ... existing ...
  - {current_page}  # ADD this
```

## 6. Proceed

Move to **Step 02: Forensic Analysis** with the `{horizon_path}` argument.
