---
title: "LND Studio Framework Bug Analysis"
date: 2026-02-27
author: "Code Review System"
status: "DRAFT"
---

# 🚨 LND Studio Framework Bug Analysis Report

> Analysis of LND Studio framework against BMAD v6 standards
> Detected issues causing AI misunderstanding, hallucination, and misalignment

---

## Executive Summary

**Total Bugs Found:** 10 (3 HIGH, 7 MEDIUM severity)

These bugs collectively explain why AI may: misunderstand requirements, execute wrong workflows, hallucinate content, skip validation steps, or produce inconsistent output.

---

## 🚨 Critical Issues (HIGH Severity)

### Bug #1: Unused Frontmatter Variables

| Field | Value |
|-------|-------|
| **Severity** | HIGH |
| **Category** | Schema Compliance |
| **Files Affected** | All step files in `studio/core/` and `studio/services/` |
| **Reference** | [`studio/core/lewd-writer/steps/step-01-context-loading.md`](studio/core/lewd-writer/steps/step-01-context-loading.md:5-9) |

**Problem:** Frontmatter defines variables that are NEVER used in the step body:

```yaml
# ❌ VIOLATION - These variables are never referenced in the step body
workflow_path: '{project-root}/studio/core/lewd-writer'
thisStepFile: './step-01-context-loading.md'

# ✅ This IS used
nextStepFile: './step-02-scene-planning.md'
```

**BMAD Standard Violation:** Per [`_bmad/bmb/workflows/workflow/data/frontmatter-standards.md`](_bmad/bmb/workflows/workflow/data/frontmatter-standards.md:75):

> "For EVERY variable in frontmatter, search the step body for {variableName}. If not found, it's a violation."

**Impact:** AI gets confused about which variables are actually relevant, causing incorrect path resolution.

**Fix:** Remove unused variables from frontmatter, or reference them in the step body.

---

### Bug #2: Agent Menu Schema Mismatch

| Field | Value |
|-------|-------|
| **Severity** | HIGH |
| **Category** | Schema Compliance |
| **Files Affected** | All `.agent.yaml` files in `studio/agents/` |
| **Reference** | [`studio/agents/lewd-writer.agent.yaml:40-47`](studio/agents/lewd-writer.agent.yaml:40-47) |

**Problem:** Agent uses `exec:` field instead of BMAD's `action:` field:

```yaml
# ❌ CURRENT (WRONG)
menu:
  - trigger: PA or fuzzy match on prose-adapter
    exec: "{project-root}/studio/core/lewd-writer/workflow.md"
    description: "[PA] Execute Prose Adapter"

# ✅ BMAD STANDARD
menu:
  - trigger: WC or fuzzy match on write
    action: "#write-commit"  # or inline instruction
    description: "[XX] Description"
```

**BMAD Standard:** Per [`_bmad/bmb/workflows/agent/data/agent-architecture.md`](_bmad/bmb/workflows/agent/data/agent-architecture.md:141-145).

**Impact:** Menu handlers may fail to trigger properly because the compiler expects `action:` not `exec:`.

**Fix:** Replace `exec:` with `action:` in all agent YAML files.

---

### Bug #3: Scoring Category Discrepancy

| Field | Value |
|-------|-------|
| **Severity** | HIGH |
| **Category** | Logic Error |
| **Files Affected** | [`studio/rules/quality_gates.md`](studio/rules/quality_gates.md) vs [`studio/services/quality-audit/workflow.md`](studio/services/quality-audit/workflow.md) |
| **Reference** | Lines: [`quality_gates.md:34-42`](studio/rules/quality_gates.md:34-42) vs [`workflow.md:39-45`](studio/services/quality-audit/workflow.md:39-45) |

**Problem:** Two different scoring systems in conflict:

| Category | quality_gates.md | workflow.md | Difference |
|----------|-----------------|-------------|------------|
| B: Edging Rhythm | 25 pts | 20 pts | -5 |
| C: Fetish Exploitation | 25 pts | 20 pts | -5 |
| D: Psychological | 15 pts | 25 pts | +10 |

**Impact:** AI receives contradictory instructions about scoring weights, causing inconsistent quality assessments.

**Fix:** Unify scoring categories and weights in both files.

---

## ⚠️ Medium Issues (MEDIUM Severity)

### Bug #4: Non-Standard Step Header

| Field | Value |
|-------|-------|
| **Severity** | MEDIUM |
| **Category** | Schema Compliance |
| **Files Affected** | All step files in studio/ |

**Problem:** Uses custom `# Path Definitions` section instead of BMAD's standard structure embedded in frontmatter:

```markdown
# ❌ CURRENT (NON-STANDARD)
# Path Definitions
workflow_path: '{project-root}/studio/core/lewd-writer'

# ✅ BMAD STANDARD
---
# File References (ONLY variables used in this step!)
nextStepFile: './step-02-scene-planning.md'
---
```

**Impact:** AI may not recognize this as a BMAD-compliant workflow, causing unexpected parsing.

---

### Bug #5: Missing "Halt and Wait" in Execution Rules

| Field | Value |
|-------|-------|
| **Severity** | MEDIUM |
| **Category** | Protocol Violation |
| **Files Affected** | All step files with menus |
| **Reference** | [`studio/core/lewd-writer/steps/step-01-context-loading.md:117-121`](studio/core/lewd-writer/steps/step-01-context-loading.md:117-121) |

**Problem:** Menu handling lacks "halt and wait" instruction:

```markdown
# ❌ CURRENT
#### Menu Handling Logic:
- IF C: Save output file, load `{nextStepFile}`
- IF other: Help user respond, redisplay menu
# MISSING: EXECUTION RULES

# ✅ BMAD STANDARD
#### EXECUTION RULES:
- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
```

**BMAD Standard:** Per [`_bmad/bmb/workflows/workflow/data/menu-handling-standards.md`](_bmad/bmb/workflows/workflow/data/menu-handling-standards.md:34-39).

**Impact:** AI may auto-proceed without waiting for user input.

---

### Bug #6: Reserved Menu Code Conflict

| Field | Value |
|-------|-------|
| **Severity** | MEDIUM |
| **Category** | Schema Compliance |
| **Files Affected** | [`studio/agents/lewd-writer.agent.yaml:45-47`](studio/agents/lewd-writer.agent.yaml:45-47), [`studio/agents/lnd-orchestrator.agent.yaml`](studio/agents/lnd-orchestrator.agent.yaml) |

**Problem:** Using `PM` trigger which is a reserved code:

```yaml
# ❌ CURRENT
menu:
  - trigger: PM or fuzzy match on party-mode  # PM IS RESERVED!
    exec: "..."

# ✅ FIX
menu:
  - trigger: PT or fuzzy match on party-mode  # Use different code
    action: "..."
```

**BMAD Standard:** Per [`_bmad/bmb/workflows/agent/data/agent-architecture.md`](_bmad/bmb/workflows/agent/data/agent-architecture.md:149):

> Reserved codes: MH, CH, PM, DA (auto-injected - do NOT use)

**Impact:** PM menu item may conflict with auto-injected system menu.

---

### Bug #7: Missing Intent Analysis in Critical Actions

| Field | Value |
|-------|-------|
| **Severity** | MEDIUM |
| **Category** | Best Practice |
| **Files Affected** | [`studio/agents/lewd-writer.agent.yaml`](studio/agents/lewd-writer.agent.yaml) |
| **Reference** | Lines 30-38 |

**Problem:** Agent doesn't mandate `sequential-thinking` tool for intent analysis:

```yaml
# ❌ CURRENT
critical_actions:
  - "Load and read {project-root}/studio/config/config.yaml..."
  # MISSING: Intent analysis

# ✅ CORRECT (see lnd-orchestrator)
critical_actions:
  - "INTENT ANALYSIS: **MANDATORY**: Use `sequential-thinking` tool to analyze the User's Request."
  - "  - Break down the goal into steps."
  - "  - Identify which Specialist Agent is best suited for each step."
```

**Impact:** AI may execute tasks without proper intent decomposition, leading to wrong agent/workflow selection.

---

### Bug #8: Inconsistent Workflow Directory Structure

| Field | Value |
|-------|-------|
| **Severity** | MEDIUM |
| **Category** | Architecture |
| **Files Affected** | All workflows in `studio/core/` and `studio/services/` |

**Problem:** Studio uses flat structure instead of BMAD's tri-modal:

```
# ❌ CURRENT
studio/
├── core/
│   └── lewd-writer/        # Mixed create/validate in one folder
│       └── steps/
│           ├── step-01-*.md
│           └── step-02-*.md
├── services/
│   └── quality-audit/
│       └── steps/

# ✅ BMAD STANDARD
workflow-name/
├── workflow.md
├── steps-c/    # Create mode
│   ├── step-01-*.md
│   └── step-02-*.md
├── steps-e/    # Edit mode
│   └── step-e-*.md
├── steps-v/    # Validate mode
│   └── step-v-*.md
└── data/      # Shared reference
```

**BMAD Standard:** Per [`_bmad/bmb/workflows/workflow/data/trimodal-workflow-structure.md`](_bmad/bmb/workflows/workflow/data/trimodal-workflow-structure.md:14-31).

**Impact:** Hard to validate, edit, or convert workflows - missing cross-mode integration.

---

### Bug #9: Workflow Entry Point Routing Missing

| Field | Value |
|-------|-------|
| **Severity** | MEDIUM |
| **Category** | Protocol Violation |
| **Files Affected** | All workflow.md files |
| **Reference** | [`studio/core/lewd-writer/workflow.md`](studio/core/lewd-writer/workflow.md) |

**Problem:** Workflow doesn't include BMAD-required initialization sequence:

```yaml
# ❌ CURRENT
---
validateWorkflow: './steps/step-01-context-loading.md'
---
# Missing mode determination

# ✅ BMAD STANDARD
## INITIALIZATION SEQUENCE
### 1. Mode Determination
**Check invocation:**
- "create" / -c → mode = create
- "validate" / -v → mode = validate  
- "edit" / -e → mode = edit
```

**BMAD Standard:** Per [`_bmad/bmb/workflows/workflow/data/trimodal-workflow-structure.md`](_bmad/bmb/workflows/workflow/data/trimodal-workflow-structure.md:64-92).

**Impact:** AI doesn't know how to handle different invocation modes.

---

### Bug #10: Deprecated Documentation References

| Field | Value |
|-------|-------|
| **Severity** | LOW |
| **Category** | Documentation |
| **Files Affected** | [`studio/core/lewd-writer/workflow.md`](studio/core/lewd-writer/workflow.md:16) |

**Problem:** References deprecated files:

```markdown
# ❌ CURRENT
- **Full Manifesto & Style Guide:** [See workflow-OLD.md](./workflow-OLD.md)

# ✅ FIX
- **Full Manifesto & Style Guide:** [See workflow.md](./workflow.md) or extract to /data/
```

**Impact:** AI may load outdated instructions from workflow-OLD.md files.

---

## 📊 Summary Table

| # | Category | Severity | Impact | Fix Complexity |
|---|----------|----------|--------|----------------|
| 1 | Frontmatter | HIGH | Path resolution failures | Easy |
| 2 | Agent Schema | HIGH | Menu handler failures | Easy |
| 3 | Scoring | HIGH | Inconsistent quality | Medium |
| 4 | Step Structure | MEDIUM | Parsing confusion | Medium |
| 5 | Menu Handling | MEDIUM | Auto-proceed errors | Easy |
| 6 | Reserved Codes | MEDIUM | Menu conflicts | Easy |
| 7 | Intent Analysis | MEDIUM | Wrong execution | Easy |
| 8 | Directory | MEDIUM | Workflow isolation | Hard |
| 9 | Routing | MEDIUM | Mode confusion | Medium |
| 10 | Documentation | LOW | Outdated info | Easy |

---

## 🔧 Recommended Actions

### Immediate (Easy Fixes)
1. Replace `exec:` → `action:` in all agent YAML files
2. Remove unused variables from step frontmatter
3. Add "EXECUTION RULES" with "halt and wait" to all menus
4. Change `PM` trigger to `PT` in agent menus
5. Add intent analysis to lewd-writer critical_actions
6. Update documentation links

### Short-term (Medium Effort)
1. Unify scoring categories between quality_gates.md and workflow.md
2. Add mode routing to workflow.md files
3. Replace `# Path Definitions` with frontmatter-based variables

### Long-term (Architectural)
1. Migrate to BMAD tri-modal structure (steps-c/steps-e/steps-v)

---

## 📎 References

- BMAD Workflow Standards: [`_bmad/bmb/workflows/workflow/data/`](_bmad/bmb/workflows/workflow/data/)
- Agent Architecture: [`_bmad/bmb/workflows/agent/data/agent-architecture.md`](_bmad/bmb/workflows/agent/data/agent-architecture.md)
- Menu Handling: [`_bmad/bmb/workflows/workflow/data/menu-handling-standards.md`](_bmad/bmb/workflows/workflow/data/menu-handling-standards.md)
- Frontmatter: [`_bmad/bmb/workflows/workflow/data/frontmatter-standards.md`](_bmad/bmb/workflows/workflow/data/frontmatter-standards.md)

---

*Report generated: 2026-02-27*
*Analysis tool: BMAD Compliance Checker*
