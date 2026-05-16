---
name: qa-audit-wrapper
description: Automated R18 prose quality audit service. Delegates scoring and SLOP detection to the Studio Developers via the axel-cowork multi-agent wrapper.
injection:
  always:
  - '{{project_root}}/studio/developers/config/roles/qa/rules/GOONER_AUDIT_FRAMEWORK.md'
dependencies:
  knowledge:
  - path: '{{project_root}}/studio/rules/anti_slop.md'
  - path: '{{project_root}}/studio/knowledge/packs/r18_sensory_pack.md'
  modules: 
  - axel-cowork (Studio Wrapper)
---

# Quality Audit Service (Automated)

## Overview

The Quality Audit service performs **comprehensive quality scoring** of R18 prose using the framework defined in `GOONER_AUDIT_FRAMEWORK.md`.

Previously a manual multi-step checklist, this service is now fully automated and delegated to the **Studio Developers**.

- **Owner**: Antigravity Developer (You)
- **Primary Agent**: `qa/m-qa-gooner` (QA Gatekeeper / Slop Detector)
- **Secondary Agent (Optional)**: `f-r18-expert` (For Cross-Review)

## On Activation (`/gooner-audit`)

When the Product Owner triggers this skill, the **Antigravity Developer** must:

1. **Locate the Draft**: Identify the prose or JSON caption file that needs review.
2. **Execute the Co-Work Wrapper**: Trigger `.agents/skills/axel-cowork/run.sh`.

   ```bash
   bash .agents/skills/axel-cowork/run.sh \
     --task "audit-$(date +%s)" \
     --mode review \
     --agents "hermes:qa/m-qa-gooner" \
     --prompt "Perform a strict 100-point Gooner Framework Audit on the attached draft. Provide the final Total Score, Category breakdowns, and detect any SLOP." \
     --files "studio/developers/config/roles/qa/rules/GOONER_AUDIT_FRAMEWORK.md path/to/draft-prose.json"
   ```

3. **Cross-Review (Optional)**: If the PO requests a deeper review, run in `--mode cross` adding `claude:f-r18-expert` to the `--agents` argument.

## Review Outputs

The output of the audit will be automatically stored by the orchestrator in `_out/agent-sessions/<task>/context.md`. The Antigravity developer will summarize the verdict and present actionable rewrite instructions back to the PO.
