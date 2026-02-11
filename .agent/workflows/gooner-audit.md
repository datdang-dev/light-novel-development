---
description: Gooner Audit - Quality gate for R18 prose (invoked by gooner-editor agent)
---

This workflow is executed by the Gooner Editor agent (Riko).

<execution>
1. INVOKE the Gooner Editor agent via `/gooner-editor`
2. The agent will load {project-root}/studio/workflows/capabilities/gooner-audit/workflow.md
3. Execute the 100-point scoring system from gooner-audit-engine module
</execution>

<quick-reference>
THRESHOLDS (see .agent/rules/quality_gates.md):
- 95-100: 🔥 GOONER PERFECTION
- 85-94:  ✅ APPROVED (publish ready)
- 70-84:  ⚠️ NEEDS REVISION
- <70:    ❌ FAILED (major rewrite)

MINIMUM PASS: 85 points

SCORING MODULE: studio/modules/gooner-audit-engine.md
WORKFLOW: studio/workflows/capabilities/gooner-audit/
</quick-reference>
