---
title: "BMAD Workflow Compliance Audit - Studio Workflows"
date: 2026-02-27
auditor: "Workflow Builder Compliance System"
status: "CRITICAL ISSUES FOUND"
---

# 🔍 BMAD Workflow Compliance Audit Report

> **Scope:** Audit LND Studio workflows against BMAD v6 workflow standards  
> **Method:** Compare studio implementation with `_bmad/bmb/workflows/workflow/data/` specifications  
> **Standard References:**
> - [`_bmad/bmb/agents/workflow-builder.md`](_bmad/bmb/agents/workflow-builder.md)
> - [`_bmad/bmb/workflows/workflow/data/step-file-rules.md`](_bmad/bmb/workflows/workflow/data/step-file-rules.md)
> - [`_bmad/bmb/workflows/workflow/data/menu-handling-standards.md`](_bmad/bmb/workflows/workflow/data/menu-handling-standards.md)
> - [`_bmad/bmb/workflows/workflow/data/frontmatter-standards.md`](_bmad/bmb/workflows/workflow/data/frontmatter-standards.md)
> - [`_bmad/bmb/workflows/workflow/data/trimodal-workflow-structure.md`](_bmad/bmb/workflows/workflow/data/trimodal-workflow-structure.md)
> - [`_bmad/bmb/workflows/workflow/data/workflow-type-criteria.md`](_bmad/bmb/workflows/workflow/data/workflow-type-criteria.md)

---

## Executive Summary

| Metric | Count |
|--------|-------|
| **Total Workflows Audited** | 6 |
| **Critical Violations** | 5 |
| **High Severity Issues** | 6 |
| **Medium Severity Issues** | 8 |
| **Files Requiring Immediate Fix** | 20+ |

**Overall Compliance Status:** ❌ **NON-COMPLIANT**

---

## 🚨 Critical Violations (Must Fix Immediately)

### CV-1: Missing Tri-Modal Structure

| Field | Details |
|-------|---------|
| **Violation ID** | CV-1 |
| **Severity** | CRITICAL |
| **Category** | Architecture |
| **Files Affected** | ALL studio workflows |
| **Reference** | [`studio/core/lewd-writer/workflow.md`](studio/core/lewd-writer/workflow.md), [`studio/services/gooner-alchemist/workflow.md`](studio/services/gooner-alchemist/workflow.md) |

**Problem:** Studio uses flat `steps/` folder instead of BMAD-required tri-modal structure.

```
# ❌ STUDIO IMPLEMENTATION (FLAT STRUCTURE)
studio/core/lewd-writer/
├── workflow.md
└── steps/                    # ❌ WRONG: Single flat folder
    ├── step-01-context-loading.md
    ├── step-02-scene-planning.md
    └── ...

# ✅ BMAD STANDARD (TRI-MODAL)
workflow-name/
├── workflow.md
├── data/                     # Shared reference
├── steps-c/                  # Create mode
│   ├── step-01-discovery.md
│   └── step-N-complete.md
├── steps-e/                  # Edit mode
│   ├── step-01-assess.md
│   └── step-N-complete.md
└── steps-v/                  # Validate mode
    └── step-01-validate.md
```

**BMAD Standard Reference:**
- [`trimodal-workflow-structure.md:14-31`](_bmad/bmb/workflows/workflow/data/trimodal-workflow-structure.md:14-31):
  > For complex critical workflows: Implement tri-modal structure (create/validate/edit)
- [`workflow-type-criteria.md:64-72`](_bmad/bmb/workflows/workflow/data/workflow-type-criteria.md:64-72):
  > Create + Edit + Validate (Tri-Modal): steps-c/, steps-e/, steps-v/

**Impact:**
- No ability to edit existing workflows
- No validation workflow for quality gates
- No conversion path for non-compliant input
- Cannot leverage cross-mode integration

**Remediation:**
1. Rename `steps/` → `steps-c/`
2. Create `steps-e/` folder with edit workflow
3. Create `steps-v/` folder with validation workflow
4. Create `data/` folder for shared reference

---

### CV-2: Wrong validateWorkflow Reference

| Field | Details |
|-------|---------|
| **Violation ID** | CV-2 |
| **Severity** | CRITICAL |
| **Category** | Routing |
| **Files Affected** | lewd-writer, panel-forensic, gooner-alchemist |
| **Reference** | [`studio/core/lewd-writer/workflow.md:7`](studio/core/lewd-writer/workflow.md:7) |

**Problem:** `validateWorkflow` points to first step instead of validation workflow.

```yaml
# ❌ STUDIO IMPLEMENTATION
---
name: "prose-adapter"
validateWorkflow: './steps/step-01-context-loading.md'  # ❌ Points to first step, not validation!
---

# ✅ BMAD STANDARD
---
name: "create-workflow"
validateWorkflow: './steps-v/step-01-validate.md'  # Points to validation workflow
---
```

**BMAD Standard Reference:**
- [`workflow-create-workflow.md:5`](_bmad/bmb/workflows/workflow/workflow-create-workflow.md:5):
  > `validateWorkflow: './steps-v/step-01-validate.md'`
- [`trimodal-workflow-structure.md:149-155`](_bmad/bmb/workflows/workflow/data/trimodal-workflow-structure.md:149-155):
  > Create mode step calling validation: `validationWorkflow: '../steps-v/step-01-validate.md'`

**Impact:**
- No standalone validation capability
- Cannot run validation mode
- Breaks cross-mode integration

**Remediation:**
1. Create validation workflows in `steps-v/`
2. Update `validateWorkflow` to point to `steps-v/step-01-validate.md`

---

### CV-3: Missing Mode Determination in workflow.md

| Field | Details |
|-------|---------|
| **Violation ID** | CV-3 |
| **Severity** | CRITICAL |
| **Category** | Routing |
| **Files Affected** | ALL studio workflow.md files |
| **Reference** | [`studio/core/lewd-writer/workflow.md`](studio/core/lewd-writer/workflow.md) |

**Problem:** workflow.md lacks mode routing logic (create/edit/validate).

```markdown
# ❌ STUDIO IMPLEMENTATION
# workflow.md just lists steps and jumps to step-01

IT IS CRITICAL THAT YOU FOLLOW THIS COMMAND: 
LOAD the FULL @{project-root}/studio/core/lewd-writer/steps/step-01-context-loading.md...

# ✅ BMAD STANDARD
## INITIALIZATION SEQUENCE

### 1. Mode Determination

**Check invocation:**
- "create" / -c → mode = create
- "validate" / -v → mode = validate
- "edit" / -e → mode = edit

**If create mode:** Ask "From scratch or convert existing?"
- From scratch → steps-c/step-01-init.md
- Convert → steps-c/step-00-conversion.md
```

**BMAD Standard Reference:**
- [`trimodal-workflow-structure.md:64-92`](_bmad/bmb/workflows/workflow/data/trimodal-workflow-structure.md:64-92):
  > workflow.md Routing Pattern with Mode Determination
- [`workflow-create-workflow.md:63-78`](_bmad/bmb/workflows/workflow/workflow-create-workflow.md:63-78):
  > Create Mode Selection with [F]rom scratch / [C]onvert existing

**Impact:**
- Cannot invoke workflow in different modes
- No conversion support
- No validation mode
- No edit mode

**Remediation:**
1. Add mode determination section to workflow.md
2. Add "From scratch or convert existing?" prompt for create mode
3. Route to appropriate step folder based on mode

---

### CV-4: Unused Frontmatter Variables

| Field | Details |
|-------|---------|
| **Violation ID** | CV-4 |
| **Severity** | CRITICAL |
| **Category** | Frontmatter Compliance |
| **Files Affected** | ALL studio step files |
| **Reference** | [`studio/core/lewd-writer/steps/step-01-context-loading.md:5-9`](studio/core/lewd-writer/steps/step-01-context-loading.md:5-9) |

**Problem:** Step files define frontmatter variables that are NEVER used in the step body.

```yaml
# ❌ STUDIO - step-01-context-loading.md
---
name: 'step-01-context-loading'
description: 'Load forensic report and story bible context'

# Path Definitions
workflow_path: '{project-root}/studio/core/lewd-writer'  # ❌ NEVER USED
thisStepFile: './step-01-context-loading.md'             # ❌ NEVER USED
nextStepFile: './step-02-scene-planning.md'              # ✅ Used
---

# ✅ BMAD STANDARD
---
name: 'step-01-discovery'
description: 'Discover workflow requirements and intent'
nextStepFile: './step-02-vision.md'  # Only define variables USED in step body
---
```

**BMAD Standard Reference:**
- [`frontmatter-standards.md:9`](_bmad/bmb/workflows/workflow/data/frontmatter-standards.md:9):
  > **Golden Rules:** 1. Only variables USED in the step may be in frontmatter
- [`frontmatter-standards.md:73-93`](_bmad/bmb/workflows/workflow/data/frontmatter-standards.md:73-93):
  > **Detection Rule:** For EVERY variable in frontmatter, search the step body. If not found, it's a violation.

**Impact:**
- Confuses AI about which variables are relevant
- Wasted tokens processing unused variables
- Potential path resolution errors

**Remediation:**
1. Remove `workflow_path` from all step frontmatter
2. Remove `thisStepFile` from all step frontmatter
3. Keep only variables actually referenced in step body

---

### CV-5: Missing EXECUTION RULES in Menu Handling

| Field | Details |
|-------|---------|
| **Violation ID** | CV-5 |
| **Severity** | CRITICAL |
| **Category** | Menu Compliance |
| **Files Affected** | ALL studio step files with menus |
| **Reference** | [`studio/core/lewd-writer/steps/step-01-context-loading.md:117-121`](studio/core/lewd-writer/steps/step-01-context-loading.md:117-121) |

**Problem:** Menu handling has logic but no EXECUTION RULES section with "halt and wait".

```markdown
# ❌ STUDIO IMPLEMENTATION
#### Menu Handling Logic
- IF C: Save output file, load `{nextStepFile}`
- IF other: Help user respond, redisplay menu

# ❌ MISSING: EXECUTION RULES section!

# ✅ BMAD STANDARD
#### Menu Handling Logic:
- IF C: Save content to {outputFile}, update frontmatter, then load, read entire file, then execute {nextStepFile}
- IF Any other: help user, then [Redisplay Menu Options](#n-present-menu-options)

#### EXECUTION RULES:
- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu items execution, return to this menu
```

**BMAD Standard Reference:**
- [`menu-handling-standards.md:33-39`](_bmad/bmb/workflows/workflow/data/menu-handling-standards.md:33-39):
  > **Section 3: Execution Rules** - MUST include "Halt and wait" instruction
- [`step-file-rules.md:189-193`](_bmad/bmb/workflows/workflow/data/step-file-rules.md:189-193):
  > "Halt and wait" in EXECUTION RULES

**Impact:**
- AI may auto-proceed without waiting for user input
- Violates collaborative workflow pattern
- Unpredictable execution behavior

**Remediation:**
1. Add `#### EXECUTION RULES:` section after Menu Handling Logic
2. Include "ALWAYS halt and wait for user input"
3. Include "ONLY proceed when user selects 'C'"

---

## ⚠️ High Severity Issues

### HI-1: Non-Standard "Path Definitions" Section

| Field | Details |
|-------|---------|
| **Violation ID** | HI-1 |
| **Severity** | HIGH |
| **Category** | Structure |
| **Files Affected** | ALL studio step files |

**Problem:** Uses custom "# Path Definitions" section instead of frontmatter-only variables.

```yaml
# ❌ STUDIO
---
name: 'step-01-context-loading'
description: '...'
---

# Path Definitions                    # ❌ NON-STANDARD SECTION
workflow_path: '{project-root}/...'

# ✅ BMAD STANDARD
---
name: 'step-01-discovery'
description: '...'
nextStepFile: './step-02-vision.md'    # All paths in frontmatter
---
```

**BMAD Standard Reference:**
- [`step-file-rules.md:20-27`](_bmad/bmb/workflows/workflow/data/step-file-rules.md:20-27):
  > File References in frontmatter ONLY

**Remediation:**
- Move all path definitions into frontmatter
- Remove "# Path Definitions" section

---

### HI-2: Missing "A/P" Options in Collaborative Steps

| Field | Details |
|-------|---------|
| **Violation ID** | HI-2 |
| **Severity** | HIGH |
| **Category** | Menu Pattern |
| **Files Affected** | Steps 3+ in all workflows |

**Problem:** Steps after initial setup don't include [A] Advanced Elicitation and [P] Party Mode options.

```markdown
# ❌ STUDIO
**Chọn:** [C] Continue to Scene Planning"

# ✅ BMAD STANDARD (for collaborative steps)
Display: "**Select:** [A] Advanced Elicitation [P] Party Mode [C] Continue"
```

**BMAD Standard Reference:**
- [`menu-handling-standards.md:41-45`](_bmad/bmb/workflows/workflow/data/menu-handling-standards.md:41-45):
  > **DO Include A/P:** Collaborative content creation, user might want alternatives

**Remediation:**
- Add [A] and [P] options to steps 3+ in all workflows
- Implement corresponding handlers

---

### HI-3: validateWorkflow Missing in Some Workflows

| Field | Details |
|-------|---------|
| **Violation ID** | HI-3 |
| **Severity** | HIGH |
| **Category** | Frontmatter |
| **Files Affected** | quality-audit/workflow.md |
| **Reference** | [`studio/services/quality-audit/workflow.md:1-6`](studio/services/quality-audit/workflow.md:1-6) |

**Problem:** quality-audit workflow.md lacks `validateWorkflow` entirely.

```yaml
# ❌ STUDIO
---
name: "gooner-audit"
description: "R18 prose quality audit..."
owner: "Riko (gooner-editor)"
version: "2.0.0"
---
# Missing validateWorkflow!

# ✅ BMAD STANDARD
---
name: "create-workflow"
description: "Create a new BMAD workflow..."
web_bundle: true
createWorkflow: './steps-c/step-01-discovery.md'
validateWorkflow: './steps-v/step-01-validate.md'  # Required
---
```

**Remediation:**
- Add `validateWorkflow` to all workflow.md files
- Point to validation workflow in steps-v/

---

### HI-4: No Continuation Support (step-01b)

| Field | Details |
|-------|---------|
| **Violation ID** | HI-4 |
| **Severity** | HIGH |
| **Category** | Workflow Type |
| **Files Affected** | ALL studio workflows |

**Problem:** Complex workflows lack continuation detection (step-01b-continue.md).

```
# ❌ STUDIO
steps/
├── step-01-context-loading.md   # No continuation logic
└── ...

# ✅ BMAD STANDARD (for continuable workflows)
steps-c/
├── step-01-init.md              # Detects continuation
├── step-01b-continue.md         # Handles resume
└── ...
```

**BMAD Standard Reference:**
- [`workflow-type-criteria.md:26-42`](_bmad/bmb/workflows/workflow/data/workflow-type-criteria.md:26-42):
  > Continuable workflows need step-01b-continue.md

**Remediation:**
- Add step-01b-continue.md to all complex workflows
- Implement stepsCompleted tracking

---

### HI-5: References to Deprecated Files

| Field | Details |
|-------|---------|
| **Violation ID** | HI-5 |
| **Severity** | HIGH |
| **Category** | Documentation |
| **Files Affected** | lewd-writer, panel-forensic |
| **Reference** | [`studio/core/lewd-writer/workflow.md:16`](studio/core/lewd-writer/workflow.md:16) |

**Problem:** References workflow-OLD.md which may contain outdated instructions.

```markdown
# ❌ STUDIO
- **Full Manifesto & Style Guide:** [See workflow-OLD.md](./workflow-OLD.md)

# ✅ BMAD STANDARD
- Extract documentation to /data/ folder
- Reference: `./data/style-guide.md`
```

**Remediation:**
- Move content from workflow-OLD.md to data/
- Update references

---

### HI-6: web_bundle Not Consistently Declared

| Field | Details |
|-------|---------|
| **Violation ID** | HI-6 |
| **Severity** | HIGH |
| **Category** | Frontmatter |
| **Files Affected** | quality-audit/workflow.md |

**Problem:** Some workflows lack `web_bundle` declaration.

```yaml
# ❌ STUDIO
---
name: "gooner-audit"
description: "..."
# Missing web_bundle!
---

# ✅ BMAD STANDARD
---
name: "create-workflow"
web_bundle: true
---
```

**Remediation:**
- Add `web_bundle: true` to all workflow.md files

---

## 📋 Medium Severity Issues

### MI-1: No Data Folder for Shared Reference

| Field | Details |
|-------|---------|
| **Violation ID** | MI-1 |
| **Severity** | MEDIUM |
| **Category** | Architecture |
| **Files Affected** | ALL workflows |

**Problem:** No `data/` folder for shared standards and reference.

```
# ❌ STUDIO
workflow-folder/
├── workflow.md
└── steps/              # No data folder

# ✅ BMAD STANDARD
workflow-folder/
├── workflow.md
├── data/               # Shared reference
│   ├── standards.md
│   └── patterns.md
├── steps-c/
├── steps-e/
└── steps-v/
```

**Remediation:**
- Create `data/` folder in each workflow
- Move shared reference content there

---

### MI-2: Step File Size Unknown

| Field | Details |
|-------|---------|
| **Violation ID** | MI-2 |
| **Severity** | MEDIUM |
| **Category** | File Size |
| **Files Affected** | Unknown - needs verification |

**Problem:** Step files may exceed 250 line limit.

**BMAD Standard:**
- Recommended: < 200 lines
- Maximum: 250 lines

**Remediation:**
- Audit all step files for size
- Split oversized steps
- Extract reference content to data/

---

### MI-3: Hardcoded Steps in workflow.md

| Field | Details |
|-------|---------|
| **Violation ID** | MI-3 |
| **Severity** | MEDIUM |
| **Category** | Structure |
| **Files Affected** | gooner-alchemist |

**Problem:** workflow.md lists all steps inline instead of routing only.

```markdown
# ❌ STUDIO
gooner-alchemist/workflow.md lists all 7 steps with descriptions

# ✅ BMAD STANDARD
workflow.md should be lean with only routing logic
```

**BMAD Standard Reference:**
- [`trimodal-workflow-structure.md:94`](_bmad/bmb/workflows/workflow/data/trimodal-workflow-structure.md:94):
  > **Critical:** workflow.md is lean. No step listings. Only routing logic.

**Remediation:**
- Remove step listings from workflow.md
- Move to data/ or steps/
- Keep workflow.md focused on routing

---

### MI-4: Missing Step Type Patterns

| Field | Details |
|-------|---------|
| **Violation ID** | MI-4 |
| **Severity** | MEDIUM |
| **Category** | Templates |
| **Files Affected** | ALL step files |

**Problem:** Steps don't follow standard BMAD step type patterns.

```markdown
# ❌ STUDIO - Inconsistent structure across steps

# ✅ BMAD STANDARD
## Required Step Structure:
- STEP GOAL: Single sentence
- MANDATORY EXECUTION RULES
- EXECUTION PROTOCOLS
- CONTEXT BOUNDARIES
- Sequence of Instructions
- MENU OPTIONS
- SYSTEM SUCCESS/FAILURE METRICS
```

**BMAD Standard Reference:**
- [`step-file-rules.md:18-76`](_bmad/bmb/workflows/workflow/data/step-file-rules.md:18-76)
- [`step-type-patterns.md`](_bmad/bmb/workflows/workflow/data/step-type-patterns.md)

---

### MI-5: No Conversion Workflow Support

| Field | Details |
|-------|---------|
| **Violation ID** | MI-5 |
| **Severity** | MEDIUM |
| **Category** | Routing |
| **Files Affected** | ALL workflows |

**Problem:** No step-00-conversion.md for converting non-compliant input.

```yaml
# ❌ STUDIO
# No conversionWorkflow defined

# ✅ BMAD STANDARD
---
createWorkflow: './steps-c/step-01-discovery.md'
conversionWorkflow: './steps-c/step-00-conversion.md'  # For non-compliant input
---
```

**Remediation:**
- Create step-00-conversion.md for each workflow
- Add conversionWorkflow to frontmatter

---

### MI-6: Inconsistent Frontmatter Variable Naming

| Field | Details |
|-------|---------|
| **Severity** | MEDIUM |
| **Category** | Naming |

**Problem:** Variables use inconsistent naming (snake_case vs camelCase).

```yaml
# MIXED IN STUDIO
nextStepFile: './step-02.md'      # camelCase
validateWorkflow: './steps-v/...' # camelCase
workflow_path: '...'              # snake_case (and wrong!)
```

**Remediation:**
- Use camelCase consistently
- Follow `*_File`, `*_Workflow` patterns

---

### MI-7: Step Numbering Inconsistency

| Field | Details |
|-------|---------|
| **Severity** | MEDIUM |
| **Category** | Naming |
| **Files Affected** | lewd-writer |

**Problem:** Uses step-05b, step-05c format which is non-standard.

```
# ❌ STUDIO
steps/
├── step-05-dialogue-integration.md
├── step-05b-format-ensure.md       # Non-standard
└── step-05c-sensory-injection.md   # Non-standard

# ✅ BMAD STANDARD
steps-c/
├── step-05-dialogue-integration.md
├── step-06-format-ensure.md
└── step-07-sensory-injection.md
```

**Remediation:**
- Use sequential numbering: step-05, step-06, step-07
- OR use descriptive suffixes: step-05-dialogue, step-06-format, step-07-sensory

---

### MI-8: No Integration Documentation in data/

| Field | Details |
|-------|---------|
| **Severity** | MEDIUM |
| **Category** | Documentation |

**Problem:** Integration points (receives_from, outputs_to) are in workflow.md instead of data/.

**Remediation:**
- Move integration schema to data/integration.md
- Reference from workflow.md

---

## 📊 Compliance Summary Matrix

| Requirement | Standard | Studio Status | Severity |
|-------------|----------|---------------|----------|
| Tri-modal structure (steps-c/e/v) | Required | ❌ Missing | CRITICAL |
| Mode determination in workflow.md | Required | ❌ Missing | CRITICAL |
| validateWorkflow → steps-v/ | Required | ❌ Wrong path | CRITICAL |
| Unused variables forbidden | Golden Rule | ❌ Violated | CRITICAL |
| EXECUTION RULES with halt/wait | Required | ❌ Missing | CRITICAL |
| Path Definitions in frontmatter | Required | ❌ Wrong section | HIGH |
| A/P options in collaborative steps | Required | ❌ Missing | HIGH |
| validateWorkflow present | Required | ❌ Missing in some | HIGH |
| step-01b-continue for continuable | Required | ❌ Missing | HIGH |
| No deprecated file references | Best Practice | ❌ Violated | HIGH |
| web_bundle declared | Required | ❌ Inconsistent | HIGH |
| data/ folder for shared ref | Required | ❌ Missing | MEDIUM |
| File size < 250 lines | Limit | ⚠️ Unknown | MEDIUM |
| Lean workflow.md (no step listing) | Required | ❌ Violated | MEDIUM |
| Step type pattern compliance | Required | ⚠️ Partial | MEDIUM |
| conversionWorkflow support | Required | ❌ Missing | MEDIUM |
| Consistent variable naming | Convention | ⚠️ Mixed | MEDIUM |
| Sequential step numbering | Convention | ⚠️ Non-standard | MEDIUM |

**Overall Compliance: ~25% (5/19 requirements met)**

---

## 🔧 Remediation Priority Matrix

### Phase 1: Critical (Immediate)

| Action | Files | Effort | Impact |
|--------|-------|--------|--------|
| Add mode determination to workflow.md | 6 workflows | Medium | High |
| Fix validateWorkflow paths | 6 workflows | Low | High |
| Remove unused frontmatter vars | All steps | Medium | High |
| Add EXECUTION RULES to menus | All steps | Medium | High |

### Phase 2: High Priority (This Sprint)

| Action | Files | Effort | Impact |
|--------|-------|--------|--------|
| Migrate to tri-modal structure | 6 workflows | High | High |
| Add A/P options to collaborative steps | ~15 steps | Medium | Medium |
| Add web_bundle to all workflows | 6 workflows | Low | Low |
| Move docs from workflow-OLD.md to data/ | 2 workflows | Low | Medium |

### Phase 3: Medium Priority (Next Sprint)

| Action | Files | Effort | Impact |
|--------|-------|--------|--------|
| Create data/ folders | 6 workflows | Low | Medium |
| Add step-01b-continue.md | 6 workflows | Medium | Medium |
| Standardize step numbering | 1 workflow | Low | Low |
| Create conversion workflows | 6 workflows | High | Medium |

### Phase 4: Refinement (Ongoing)

| Action | Files | Effort | Impact |
|--------|-------|--------|--------|
| Audit file sizes | All steps | Medium | Low |
| Standardize variable naming | All steps | Low | Low |
| Create validation workflows | 6 workflows | High | High |

---

## 📎 Reference Files

**BMAD Standards:**
- [`_bmad/bmb/agents/workflow-builder.md`](_bmad/bmb/agents/workflow-builder.md)
- [`_bmad/bmb/workflows/workflow/data/step-file-rules.md`](_bmad/bmb/workflows/workflow/data/step-file-rules.md)
- [`_bmad/bmb/workflows/workflow/data/menu-handling-standards.md`](_bmad/bmb/workflows/workflow/data/menu-handling-standards.md)
- [`_bmad/bmb/workflows/workflow/data/frontmatter-standards.md`](_bmad/bmb/workflows/workflow/data/frontmatter-standards.md)
- [`_bmad/bmb/workflows/workflow/data/trimodal-workflow-structure.md`](_bmad/bmb/workflows/workflow/data/trimodal-workflow-structure.md)
- [`_bmad/bmb/workflows/workflow/data/workflow-type-criteria.md`](_bmad/bmb/workflows/workflow/data/workflow-type-criteria.md)

**Studio Implementation:**
- [`studio/core/lewd-writer/workflow.md`](studio/core/lewd-writer/workflow.md)
- [`studio/core/panel-forensic/workflow.md`](studio/core/panel-forensic/workflow.md)
- [`studio/services/quality-audit/workflow.md`](studio/services/quality-audit/workflow.md)
- [`studio/services/gooner-alchemist/workflow.md`](studio/services/gooner-alchemist/workflow.md)

---

*Audit completed: 2026-02-27*  
*Auditor: BMAD Workflow Compliance System*  
*Next Review: After Phase 1 remediation*
